#!/usr/bin/env python3
"""End-to-end headless lookbook orchestrator.

Composes the deterministic chain:
  score (event-driven only) → discover candidates → curate
  → build (Premium for one-shot/event when available; weekly Editorial by default)
  → deploy with voting (gated on _auto)
  → validate → write summary

Spec: references/headless-mode.md § "The end-to-end orchestrator".

Modes
-----
  --weekly                 Recurring weekly newsletter mode. Uses
                           scripts/discover-weekly-candidates.py to surface
                           recently-live + previously-unproposed products.

  --event <path>           Event-driven mode. Reads the event JSON, scores
                           it via scripts/score-calendar-event.py, and
                           proceeds only if action ∈ {editorial, premium}.
                           skip / hard-veto exits with summary, no lookbook.
                           soft (score=6) emits a one-line "ready when you
                           are" summary, no generation.

Common args
-----------
  --profile <path>         profile.md (or YAML/JSON sibling). Reads sizes,
                           gender, ethos, link_payment_method,
                           preferred_lookbook_host*, weekly_lookbook_*,
                           lookbook_project_prefix, lookbook_votes_kv_id,
                           notify_url.

  --runs-dir <path>        Default ~/.buck-mason-stylist/runs/
  --wishlist <path>        Default ~/.buck-mason-stylist/wishlist.jsonl
  --max-pieces N           Default 6; cap on candidates picked
  --tier <auto|editorial|premium>
                           Default `auto` — one-shot/event runs pick Premium
                           when OPENAI_API_KEY is present and ≥2 reference
                           photos exist. Weekly runs stay Editorial unless
                           weekly_lookbook_tier: premium. `--tier editorial`
                           or `--tier premium` forces.

Premium tier note
-----------------
Premium tier requires gpt-image-2 calls (~$0.40/run) which need a
specifically-crafted prompt template (see references/image-generation.md).
This orchestrator does NOT invoke OpenAI directly — it stops at the build
step with the run config + picks ready, and the agent generates the look
images separately, drops them into runs/<id>/looks/, then re-runs the
orchestrator with --resume-build to pick up at the build stage.
"""
import argparse, atexit, concurrent.futures, contextlib, json, os, pathlib, re, subprocess, sys, time, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent
SKILL_ROOT = ROOT.parent

# Make scripts/lib importable when this file is invoked directly.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from lib.profile import parse_profile_path  # noqa: E402

# ── Timing log ──────────────────────────────────────────────────────────────
# Phase-level timings written to <run_dir>/_timings.jsonl (machine, per-phase
# JSON line) and <run_dir>/_run.log (human-readable, sorted-by-duration). On
# any exit path the log is flushed via atexit so we keep a record of slow or
# failed runs. Top-3 slowest phases also print to stderr at end so cron-like
# environments capture the signal in their job-runner output.

class TimingLog:
    def __init__(self):
        self.run_dir = None      # set after we know lookbook_id
        self.entries = []
        self.t_start = time.time()

    @contextlib.contextmanager
    def phase(self, name, **meta):
        t0 = time.time()
        ok = True
        err = None
        try:
            yield
        except SystemExit:
            # Treat sys.exit(N) inside a phase as ok=False if N != 0,
            # but still record the duration before re-raising.
            if sys.exc_info()[1].code not in (None, 0):
                ok = False
                err = f"sys.exit({sys.exc_info()[1].code})"
            raise
        except Exception as e:
            ok = False
            err = f"{type(e).__name__}: {str(e)[:200]}"
            raise
        finally:
            t1 = time.time()
            entry = {
                "phase":      name,
                "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)),
                "duration_s": round(t1 - t0, 2),
                "ok":         ok,
                **{k: v for k, v in meta.items() if v is not None},
            }
            if err:
                entry["error"] = err
            self.entries.append(entry)

    def write(self):
        if not self.run_dir or not self.entries:
            return
        try:
            self.run_dir.mkdir(parents=True, exist_ok=True)
            (self.run_dir / "_timings.jsonl").write_text(
                "\n".join(json.dumps(e) for e in self.entries) + "\n"
            )
            total = time.time() - self.t_start
            lines = [
                f"# Run timings — {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(self.t_start))}",
                f"# Total elapsed: {total:.2f}s",
                f"# Phase order (chronological):",
            ]
            for e in self.entries:
                pct = (e["duration_s"] / total * 100) if total > 0 else 0.0
                mark = "✓" if e["ok"] else "✗"
                extra = f"  {e.get('error', '')}" if not e["ok"] else ""
                lines.append(f"  {mark} {e['duration_s']:>7.2f}s ({pct:>5.1f}%)  {e['phase']}{extra}")
            lines.append("")
            lines.append("# Slowest phases (by duration):")
            for e in sorted(self.entries, key=lambda x: x["duration_s"], reverse=True)[:5]:
                lines.append(f"    {e['duration_s']:>7.2f}s  {e['phase']}")
            (self.run_dir / "_run.log").write_text("\n".join(lines) + "\n")
        except Exception as e:
            print(f"warn: failed to write timings log: {e}", file=sys.stderr)

    def print_summary_to_stderr(self):
        if not self.entries:
            return
        total = time.time() - self.t_start
        top3 = sorted(self.entries, key=lambda x: x["duration_s"], reverse=True)[:3]
        msg = " | ".join(f"{e['phase']} {e['duration_s']:.1f}s" for e in top3)
        print(f"[timings] total {total:.1f}s · slowest: {msg}", file=sys.stderr)

timings = TimingLog()
atexit.register(timings.write)
atexit.register(timings.print_summary_to_stderr)

# ── CLI ─────────────────────────────────────────────────────────────────────
EPILOG = """\
Run states (first line of stdout + first line of summary.md):
  ✅ Deployed: <url>             — full success; URL is permanent if --auto
                                    triggered the deploy and the project was
                                    fresh (deploy-lookbook.sh --no-overwrite).
  📦 READY TO DEPLOY              — local build + validation passed but the
                                    deploy gate is closed (profile.md →
                                    preferred_lookbook_host_auto is unset).
                                    The summary names the exact interactive
                                    `bash scripts/deploy-lookbook.sh ...`
                                    command to publish.
  READY_FOR_PREMIUM_IMAGE_STEP   — Premium tier was selected but
                                    runs/<id>/looks/look<N>.png aren't there
                                    yet. Generate the try-on imagery per
                                    references/image-generation.md, drop the
                                    PNGs + the .lookbook_id marker, then
                                    re-run with --resume-build. (The
                                    orchestrator never invokes gpt-image-2
                                    itself — that step lives outside the
                                    deterministic chain because the prompt
                                    template is taste-aware.)
  ❌ BLOCKER: <reason>            — fail-closed at fetch / discover / curate
                                    / build / verify-face / validate-local /
                                    deploy / validate-deployed.

Premium-tier face-verification gate:
  Premium-tier --resume-build runs the generated PNGs through
  scripts/verify-face.py against the customer's reference_photos before
  consumption. A failed face → BLOCKER summary naming which look
  failed and the rubric reason. Override with --no-verify (not
  recommended). See references/image-generation.md § "Face
  verification gate".

Per-run logging (always written to the run dir):
  _timings.jsonl   one JSON line per phase (machine-readable, append
                   across runs to track timing distribution over time).
                   Fields: phase, started_at, duration_s, ok, error?,
                   plus per-phase metadata (tier, project, look, ...).
  _run.log         human-readable trace: chronological phase list with
                   ✓/✗ + duration + percent-of-total, then a "Slowest
                   phases (by duration)" bottom block. Inspect this
                   first when a run takes longer than expected.

  At end-of-run, the orchestrator also prints a one-line "[timings]
  total Xs · slowest: A Ys | B Ys | C Ys" to stderr so cron/loop
  invocations capture the signal in their job-runner output.

Examples:
  # Weekly newsletter (Editorial tier; honors profile gate for deploy)
  python3 scripts/run-headless-lookbook.py --weekly \\
      --profile ~/agent-workspace/profile.md

  # Event-driven (auto-scored — exits silently on hard-veto medical/therapy)
  python3 scripts/run-headless-lookbook.py --event ~/Downloads/event.json \\
      --profile ~/agent-workspace/profile.md

  # Premium tier weekly — pauses for the agent to drop look images
  python3 scripts/run-headless-lookbook.py --weekly \\
      --profile ~/agent-workspace/profile.md --tier premium

  # Resume after dropping the gpt-image-2 PNGs + marker into runs/<id>/looks/
  python3 scripts/run-headless-lookbook.py --weekly \\
      --profile ~/agent-workspace/profile.md --tier premium --resume-build

Cross-references:
  references/headless-mode.md      — when this orchestrator runs, defaults,
                                      run-summary format, the 5 hard rules
  references/event-suitability.md  — calendar event scoring rubric (event mode)
  references/run-layout.md         — per-lookbook directory isolation rules
  scripts/build-html-lookbook.py --help
  scripts/deploy-lookbook.sh --help
  scripts/validate-lookbook.py --help
"""

ap = argparse.ArgumentParser(
    description="Headless lookbook orchestrator. Composes score (event mode) → "
                "discover → curate → build → deploy → validate → wishlist append "
                "→ run summary. Designed to be safe under cron / /loop / voice.",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=EPILOG,
)
mode = ap.add_mutually_exclusive_group(required=True)
mode.add_argument("--weekly", action="store_true",
                  help="Weekly newsletter mode — discovers recently-live + "
                       "previously-unproposed products, dedupes against the "
                       "wishlist, builds 1-2 looks. See references/headless-mode.md.")
mode.add_argument("--event",  type=pathlib.Path,
                  help="Event JSON file. Scored via scripts/score-calendar-event.py; "
                       "skip / soft-surface / editorial / premium per the rubric "
                       "in references/event-suitability.md.")
ap.add_argument("--profile",     type=pathlib.Path, required=True,
                help="Path to the customer's profile.md. Reads gender, sizes, "
                     "style_ethos, link_payment_method, preferred_lookbook_host*, "
                     "weekly_lookbook_*, lookbook_project_prefix, "
                     "lookbook_votes_kv_id, notify_url, reference_photos.")
ap.add_argument("--runs-dir",    type=pathlib.Path,
                default=pathlib.Path.home() / ".buck-mason-stylist/runs",
                help="Where per-lookbook run directories live "
                     "(default: ~/.buck-mason-stylist/runs/).")
ap.add_argument("--wishlist",    type=pathlib.Path,
                default=pathlib.Path.home() / ".buck-mason-stylist/wishlist.jsonl",
                help="Long-term JSONL of every piece ever proposed/purchased. "
                     "Read for dedup; appended-to after a successful deploy "
                     "(default: ~/.buck-mason-stylist/wishlist.jsonl).")
ap.add_argument("--max-pieces",  type=int, default=6,
                help="Cap on the number of pieces in the lookbook (default: 6).")
ap.add_argument("--tier",        choices=["auto", "editorial", "premium"], default="auto",
                help="auto = Premium for one-shot/event runs when OPENAI_API_KEY "
                     "+ ≥2 reference photos are present; weekly runs stay "
                     "Editorial unless weekly_lookbook_tier: premium. "
                     "editorial = no AI try-on. premium = gpt-image-2 try-on "
                     "per look (~$0.40/run).")
ap.add_argument("--resume-build",action="store_true",
                help="Skip discover/curate; re-enter the build step using the "
                     "existing run directory. Pair with --tier premium after "
                     "dropping gpt-image-2 PNGs into runs/<id>/looks/.")
ap.add_argument("--lookbook-id", type=str,
                help="Override the auto-derived lookbook_id. Default: weekly = "
                     "<YYYY>-weekly-<ISO_week>; event = <YYYY-MM-DD>-<title-slug>.")
ap.add_argument("--no-verify", action="store_true",
                help="Skip the face-verification gate on Premium-tier resume "
                     "builds. Default is verify-on. See references/image-"
                     "generation.md § \"Face verification gate\".")
args = ap.parse_args()

args.runs_dir.mkdir(parents=True, exist_ok=True)
args.wishlist.parent.mkdir(parents=True, exist_ok=True)

# Profile parsing lives in scripts/lib/profile.py for unit-testability.
with timings.phase("parse_profile", path=str(args.profile)):
    profile = parse_profile_path(args.profile) if args.profile.exists() else {}
gender               = profile.get("gender", "u")
sizes                = profile.get("sizes", {})
ethos                = profile.get("style_ethos", "")
favorites            = profile.get("favorites") or ""
auto_publish         = bool(profile.get("preferred_lookbook_host_auto", False))
project_prefix       = profile.get("lookbook_project_prefix") or "buckmason"
weekly_tier          = str(profile.get("weekly_lookbook_tier") or "editorial").lower()
lookbook_votes_kv_id = str(profile.get("lookbook_votes_kv_id") or os.environ.get("LOOKBOOK_VOTES_KV_ID") or "")
home_zip             = profile.get("home_zip", "")
reference_photos     = profile.get("reference_photos", [])
openai_key_set       = bool(os.environ.get("OPENAI_API_KEY"))

# ── Summary writer ─────────────────────────────────────────────────────────
def write_summary(run_dir: pathlib.Path, body: str):
    """Per references/headless-mode.md § run summary format."""
    (run_dir / "summary.md").write_text(body)
    # Single-line URL/blocker on stdout for headless callers
    first = body.strip().splitlines()[0] if body.strip() else ""
    print(first)

def fail(run_dir: pathlib.Path, stage: str, reason: str, tier: str = "—"):
    body = (
        f"# Lookbook run — {time.strftime('%Y-%m-%d')}\n"
        f"\n"
        f"❌ BLOCKER: {reason}\n"
        f"Tier attempted: {tier}\n"
        f"Stage failed: {stage}\n"
        f"\n"
        f"Detail\n"
        f"{reason}\n"
    )
    write_summary(run_dir, body)
    sys.exit(2)

# ── Mode: --event ──────────────────────────────────────────────────────────
event_action = None
event_score  = None
event_label  = None
if args.event:
    if not args.event.exists():
        print(f"error: event file not found: {args.event}", file=sys.stderr)
        sys.exit(2)
    with timings.phase("score_event"):
        score_p = subprocess.run(
            ["python3", str(ROOT / "score-calendar-event.py")],
            input=args.event.read_text(),
            capture_output=True, text=True,
        )
    if score_p.returncode != 0:
        print(f"error: scorer exited non-zero: {score_p.stderr}", file=sys.stderr)
        sys.exit(2)
    score_obj = json.loads(score_p.stdout)
    event_score  = score_obj.get("score")
    event_action = score_obj.get("action")
    event_label  = score_obj.get("reason")
    if event_action == "skip":
        # Hard veto or below threshold — silent skip; no run dir needed.
        print(f"score={event_score} action=skip reason={event_label} — no lookbook generated.")
        sys.exit(0)
    if event_action == "soft":
        # One-line surface; no generation in headless mode.
        print(f"score={event_score} action=soft — surface to customer next interactive turn.")
        sys.exit(0)

# ── Lookbook id + run dir ──────────────────────────────────────────────────
today = time.strftime("%Y-%m-%d")
if args.lookbook_id:
    lookbook_id = args.lookbook_id
elif args.weekly:
    iso_year, iso_week, _ = time.gmtime().tm_year, time.strftime("%V"), 0
    lookbook_id = f"{time.strftime('%Y')}-weekly-{time.strftime('%V')}"
else:
    # Event-driven — derive from event title
    ev_data = json.loads(args.event.read_text())
    slug = re.sub(r'[^a-z0-9]+', '-', (ev_data.get("title") or "event").lower()).strip('-')[:32] or "event"
    lookbook_id = f"{today}-{slug}"

run_dir = args.runs_dir / lookbook_id
(run_dir / "looks").mkdir(parents=True, exist_ok=True)
(run_dir / "deploy").mkdir(parents=True, exist_ok=True)
timings.run_dir = run_dir   # connect the log to its destination now that we know it

# ── Curate (skipped on --resume-build) ─────────────────────────────────────
picks_path  = run_dir / "picks.json"
config_path = run_dir / "config.json"
candidates_path = run_dir / "candidates.json"

def derive_tier() -> str:
    if args.tier != "auto":
        return args.tier
    if args.weekly:
        if weekly_tier == "premium" and openai_key_set and len(reference_photos) >= 2:
            return "premium"
        return "editorial"
    if openai_key_set and len(reference_photos) >= 2:
        return "premium"
    return "editorial"

if not args.resume_build:
    # ── Discover candidates ────────────────────────────────────────────────
    if args.weekly:
        sizes_arg = json.dumps({k: str(v) for k, v in sizes.items() if v})
        with timings.phase("discover_candidates", source="weekly"):
            disc_p = subprocess.run([
                "python3", str(ROOT / "discover-weekly-candidates.py"),
                "--gender", str(gender),
                "--since-days", "30",
                "--wishlist", str(args.wishlist),
                "--sizes", sizes_arg,
                "--max", str(max(args.max_pieces * 3, 18)),
            ], capture_output=True, text=True)
        if disc_p.returncode != 0:
            fail(run_dir, "discover", f"discover-weekly-candidates failed: {disc_p.stderr.strip()[:200]}")
        cand = json.loads(disc_p.stdout)
        candidates_path.write_text(json.dumps(cand, indent=2))
    else:
        # Event-driven: use the event's hint to query MCP (light-weight)
        # The agent typically pre-curates and writes picks.json directly,
        # then re-runs with --resume-build. If picks.json is missing here,
        # we fall back to the same discover script with the event's gender.
        if not picks_path.exists():
            sizes_arg = json.dumps({k: str(v) for k, v in sizes.items() if v})
            with timings.phase("discover_candidates", source="event"):
                disc_p = subprocess.run([
                    "python3", str(ROOT / "discover-weekly-candidates.py"),
                    "--gender", str(gender),
                    "--since-days", "60",
                    "--wishlist", str(args.wishlist),
                    "--sizes", sizes_arg,
                    "--max", str(max(args.max_pieces * 3, 18)),
                ], capture_output=True, text=True)
            if disc_p.returncode != 0:
                fail(run_dir, "discover", f"discover-weekly-candidates failed: {disc_p.stderr.strip()[:200]}")
            cand = json.loads(disc_p.stdout)
            candidates_path.write_text(json.dumps(cand, indent=2))

    # ── Curate (taste-light v1: take top N, group into 1–2 looks) ─────────
    if not picks_path.exists():
        cand = json.loads(candidates_path.read_text()) if candidates_path.exists() else {"candidates": []}
        chosen = cand.get("candidates", [])[: args.max_pieces]
        if not chosen:
            fail(run_dir, "curate", f"discover returned 0 candidates — nothing new to surface this run", tier="—")
        # Group: half the picks into look1, half into look2 (or all into look1
        # if fewer than 4)
        half = max(1, len(chosen) // 2)
        for i, p in enumerate(chosen):
            p["look"] = "look1" if i < half else "look2"
            p["picked_size"] = p.get("size") or sizes.get("shirt") or "L"
        picks_path.write_text(json.dumps(chosen, indent=2))

    # ── Config ────────────────────────────────────────────────────────────
    if not config_path.exists():
        if args.weekly:
            title = f"This Week from Buck Mason — {today}"
            subtitle = f"What's new on buckmason.com plus pieces I haven't pitched you before, in your size."
        else:
            ev = json.loads(args.event.read_text())
            ev_title = ev.get("title") or "Event"
            title = f"For {ev_title}"
            subtitle = ev.get("description") or "An outfit suggestion for this event."
        looks_meta = []
        for look_id in ("look1", "look2"):
            if any(p["look"] == look_id for p in json.loads(picks_path.read_text())):
                idx = 1 if look_id == "look1" else 2
                looks_meta.append({
                    "id": look_id,
                    "eyebrow": f"Look {idx:02d}",
                    "title": f"Look {idx}",
                    "note": "",
                })
        project = f"{project_prefix}-{lookbook_id}"
        page_url = f"https://{project}.pages.dev/"
        config_path.write_text(json.dumps({
            "lookbook_id":    lookbook_id,
            "lookbook_title": title,
            "lookbook_date":  today,
            "subtitle":       subtitle,
            "page_url":       page_url,
            "looks":          looks_meta,
        }, indent=2))

# ── Build ──────────────────────────────────────────────────────────────────
tier = derive_tier()
deploy_dir = run_dir / "deploy"

build_args = [
    "python3", str(ROOT / "build-html-lookbook.py"),
    "--config", str(config_path),
    "--picks",  str(picks_path),
    "--out",    str(deploy_dir),
]
if tier == "premium":
    looks_dir = run_dir / "looks"
    # Verify we actually have the per-look images + the marker
    pngs = sorted(looks_dir.glob("look*.png"))
    if not pngs:
        # Premium path needs the agent to drop look images first.
        # Use an unmistakable machine-readable marker on stdout + a structured
        # heading in the summary so an agent (or another script) can branch
        # on the run state without parsing prose.
        body = (
            f"READY_FOR_PREMIUM_IMAGE_STEP\n"
            f"\n"
            f"# Lookbook run — {today}\n"
            f"\n"
            f"Status: READY_FOR_PREMIUM_IMAGE_STEP\n"
            f"Tier:   premium\n"
            f"Stage:  awaiting-look-images\n"
            f"\n"
            f"Premium tier needs gpt-image-2 outputs at:\n"
            f"  {looks_dir}/look1.png\n"
            f"  {looks_dir}/look2.png\n"
            f"  {looks_dir}/.lookbook_id  (must contain: {lookbook_id})\n"
            f"\n"
            f"Next steps (pick ONE):\n"
            f"  (a) Generate the try-on images per references/image-generation.md.\n"
            f"      ⚡ Issue the gpt-image-2 calls IN PARALLEL — each look is an\n"
            f"         independent image-edit call; sequential generation costs an\n"
            f"         extra 30–60s per look of wallclock for no reason. See\n"
            f"         references/image-generation.md § \"Run multi-look generations\n"
            f"         in parallel\" for the worked concurrent.futures pattern.\n"
            f"      Drop the PNGs at the paths above, write the .lookbook_id marker,\n"
            f"      then re-run this orchestrator with --resume-build.\n"
            f"  (b) Fall back to Editorial tier (no AI try-on) with --tier editorial.\n"
            f"\n"
            f"Run dir: {run_dir}\n"
        )
        write_summary(run_dir, body)
        sys.exit(0)
    build_args += ["--look-images", str(looks_dir)]

    # Face-verification gate (references/image-generation.md § "Face
    # verification gate"). Premium-tier outputs run through verify-face.py
    # against the customer's reference photos before consumption. A single
    # off-putting AI-face shipped to the customer is the trust-damaging
    # failure this whole pipeline is built to prevent.
    if not args.no_verify and reference_photos and openai_key_set:
        verify_failures = []
        pngs = sorted(looks_dir.glob("look*.png"))

        # Verify-face calls are independent per look (same reference photos,
        # different generated PNG). Issue them concurrently — each call is a
        # GPT-4o-vision round-trip ~5-15s, so a 3-look gate sequentially is
        # 15-45s vs ~5-15s in parallel. Bound at the look count.
        def verify_one(png):
            t0 = time.time()
            v = subprocess.run(
                ["python3", str(ROOT / "verify-face.py"),
                 "--generated", str(png),
                 *sum([["--reference", rp] for rp in reference_photos], [])],
                capture_output=True, text=True,
            )
            return png, v, round(time.time() - t0, 2)

        # Per-look duration list, captured by reference into the phase meta
        # so the timing entry includes per-look detail without depending on
        # phase-finally ordering.
        per_look = []
        with timings.phase("verify_face_concurrent", looks=len(pngs), per_look=per_look):
            with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, len(pngs))) as ex:
                for png, v, dur in ex.map(verify_one, pngs):
                    per_look.append({"look": png.name, "duration_s": dur, "rc": v.returncode})
                    if v.returncode == 1:
                        try:
                            info = json.loads(v.stdout)
                            reason = info.get("reason", "(no reason)")
                            scores = info.get("scores", {})
                            off_putting = info.get("off_putting", "?")
                            detail = f"{png.name}: {reason} | scores={scores} | off_putting={off_putting}"
                        except Exception:
                            detail = f"{png.name}: {v.stdout.strip()[:200]}"
                        verify_failures.append(detail)
                    elif v.returncode == 2:
                        fail(run_dir, "verify-face",
                             f"face-verification gate inconclusive for {png.name}: {v.stderr.strip()[:200]}",
                             tier=tier)
        if verify_failures:
            body = (
                f"# Lookbook run — {today}\n"
                f"\n"
                f"❌ BLOCKER: face-verification gate failed on {len(verify_failures)} look(s)\n"
                f"Tier:  premium\n"
                f"Stage: verify-face\n"
                f"\n"
                f"Failures (most-likely-cause first per look):\n"
                + "\n".join(f"  - {f}" for f in verify_failures) +
                f"\n\n"
                f"Recovery (per references/image-generation.md § \"Recovery flow\"):\n"
                f"  (a) Regenerate the failed look(s) with a stronger IDENTITY block — move\n"
                f"      reference photo #1 to position 0 and append the rubric `reason` as a\n"
                f"      directive. Drop the new PNG into {looks_dir}/ and re-run with\n"
                f"      --resume-build.\n"
                f"  (b) Fall back to Editorial tier for this run with --tier editorial.\n"
                f"  (c) Override the gate (NOT recommended) with --no-verify.\n"
                f"\n"
                f"Run dir: {run_dir}\n"
            )
            write_summary(run_dir, body)
            sys.exit(2)
else:
    build_args += ["--no-tryon"]

with timings.phase("build", tier=tier):
    build_p = subprocess.run(build_args, capture_output=True, text=True)
if build_p.returncode != 0:
    fail(run_dir, "build", f"build-html-lookbook.py exit {build_p.returncode}: {build_p.stderr.strip()[:400]}", tier=tier)

# ── Validate (local) ───────────────────────────────────────────────────────
with timings.phase("validate_local"):
    validate_p = subprocess.run(
        ["python3", str(ROOT / "validate-lookbook.py"), "--dir", str(deploy_dir)],
        capture_output=True, text=True,
    )
if validate_p.returncode != 0:
    fail(run_dir, "validate-local", f"local validation failed: {validate_p.stdout.strip()[-400:]}", tier=tier)

# ── Deploy (gated on profile) ─────────────────────────────────────────────
project_name = f"{project_prefix}-{lookbook_id}"
page_url = f"https://{project_name}.pages.dev/"

if not auto_publish:
    kv_arg = f" --kv-id {lookbook_votes_kv_id}" if lookbook_votes_kv_id else " --kv-id <lookbook_votes_kv_id>"
    voting_note = (
        f"Voting: enabled by default. "
        f"{'KV id resolved from profile/env.' if lookbook_votes_kv_id else 'Set profile.md → lookbook_votes_kv_id or LOOKBOOK_VOTES_KV_ID before publishing.'}\n"
    )
    body = (
        f"# {json.loads(config_path.read_text())['lookbook_title']}\n"
        f"\n"
        f"📦 READY TO DEPLOY\n"
        f"Tier: {tier.title()}\n"
        f"Looks: {len(json.loads(config_path.read_text())['looks'])}\n"
        f"Pieces: {len(json.loads(picks_path.read_text()))}\n"
        f"{voting_note}"
        f"\n"
        f"Run dir: {run_dir}\n"
        f"\n"
        f"To publish, set profile.md → preferred_lookbook_host_auto: true\n"
        f"or run interactively:\n"
        f"  bash scripts/deploy-lookbook.sh {deploy_dir} {project_name} --no-overwrite{kv_arg}\n"
    )
    write_summary(run_dir, body)
    sys.exit(0)

with timings.phase("deploy", project=project_name):
    deploy_cmd = ["bash", str(ROOT / "deploy-lookbook.sh"), str(deploy_dir), project_name, "--auto", "--no-overwrite"]
    if lookbook_votes_kv_id:
        deploy_cmd += ["--kv-id", lookbook_votes_kv_id]
    deploy_p = subprocess.run(
        deploy_cmd,
        capture_output=True, text=True,
    )
if deploy_p.returncode != 0:
    fail(run_dir, "deploy", f"deploy-lookbook.sh exit {deploy_p.returncode}: {deploy_p.stderr.strip()[-400:]}", tier=tier)

# ── Validate (deployed) ───────────────────────────────────────────────────
with timings.phase("validate_deployed"):
    validate_d = subprocess.run(
        ["python3", str(ROOT / "validate-lookbook.py"), "--url", page_url],
        capture_output=True, text=True,
    )
if validate_d.returncode != 0:
    fail(run_dir, "validate-deployed", f"deployed validation failed: {validate_d.stdout.strip()[-400:]}", tier=tier)

# ── Wishlist append ───────────────────────────────────────────────────────
with timings.phase("wishlist_append"):
    proposed_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with args.wishlist.open("a") as f:
        for p in json.loads(picks_path.read_text()):
            f.write(json.dumps({
                "sku":           p.get("sku"),
                "name":          p.get("name"),
                "size":          p.get("picked_size") or p.get("size"),
                "qty":           1,
                "lookbook_id":   lookbook_id,
                "lookbook_url":  page_url,
                "proposed_at":   proposed_at,
                "purchased_at":  None,
                "order_id":      None,
            }) + "\n")

# ── Success summary ───────────────────────────────────────────────────────
cfg  = json.loads(config_path.read_text())
picks = json.loads(picks_path.read_text())
in_stock_count = sum(
    1 for p in picks
    if isinstance(p.get("in_stock_online"), dict) and p["in_stock_online"].get("in_stock")
)
subtotal = sum(p.get("price_cents", 0) for p in picks) / 100

body = (
    f"# {cfg['lookbook_title']}\n"
    f"\n"
    f"✅ Deployed: {page_url}\n"
    f"Tier: {tier.title()}\n"
    f"Looks: {len(cfg['looks'])}\n"
    f"Pieces: {len(picks)} · in stock {in_stock_count}/{len(picks)}\n"
    f"Subtotal at pick: ${subtotal:.2f}\n"
    f"\n"
    f"Notes\n"
    + (f"- Event score: {event_score} ({event_label})\n" if event_score is not None else "")
    + f"- Voting tally: {page_url}api/votes\n"
    + f"- Run dir: {run_dir}\n"
    f"\n"
    f"Verify: https://www.opengraph.xyz/url/{urllib.parse.quote(page_url, safe='')}\n"
)
write_summary(run_dir, body)
