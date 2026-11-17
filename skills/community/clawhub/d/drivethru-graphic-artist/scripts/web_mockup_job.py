#!/usr/bin/env python3
"""Storefront web mockups, end to end — the ONE command the web-image routine runs.

Everything that used to go wrong in the "General Purpose Web image generation
routine" was the agent handling images itself: pulling base64 into its context
(sessions ballooned), chunking bytes into product fields (never lands), fetching
Odoo's placeholder as if it were a blank, compositing a thumbnail's background
plate onto the garment, and mirroring left/right chest. This script takes all of
that out of the agent's hands:

1. **Plan** — calls the ``web_mockup_plan`` MCP tool (server-side: which colours
   need an image, which blank photo per colour — empty fields are skips, never
   placeholders — and each decoration's raw location name and art sources
   best-first). Odoo does NOT decide placement: ``locations.py`` (this skill)
   maps each location name to a WEARER-side placement + image side and picks
   the front layers; a product with nothing showable is reported, with why.
2. **Fetch** — downloads blanks/art to local files over HTTP
   (``GET <ODOO_MCP_URL>/image`` 404s on an empty field; CDN URLs directly).
3. **Prep art** — production PNGs (embroidery/DTF, already transparent) first;
   the thumbnail only as a fallback, with its background removed and VERIFIED
   gone (opaque borders ⇒ rejected, next source tried).
4. **Compose** — every front-visible decoration layered onto the blank with
   ``compose_mockup.compose`` (orientation-guarded rules).
5. **Check** — deterministic geometry (right side of the image, inside the
   garment) then an independent **vision review** (``vision_review.py``) → yes/no.
6. **Write** — only on "yes": a web JPEG POSTed multipart to
   ``<ODOO_MCP_URL>/upload`` for every size variant of the colour at once, and
   verified byte-exact (``bytes_received`` == file size, every record stored).

The agent sees JSON summaries only. It never opens, reads, or transmits images.

**Live progress** — as each colour finishes, one line goes to stderr and to
``$MOCKUP_DATA_DIR/web_jobs/progress.log`` (``[3/16] 24941-black
needs_adjustment too_high(+6y) a1 $0.012``); the final JSON stays on stdout.
Every summary carries a ``cost`` block (vision spend from OpenRouter's per-call
``usage.cost``) and a ``tuning`` block: the deltas approved mockups needed, per
(category, placement), with the catalog edit to bake them in once a correction
keeps recurring.

Usage:
    web_mockup_job.py run --site-id 10 [--limit 10] [--max-colors 30] [--dry-run]
    web_mockup_job.py run --product-tmpl-ids 24921,24920
    web_mockup_job.py run --site-id 17 --include-imaged   # deliberate redo
    web_mockup_job.py adjust --job 24921-black --apply-suggested
    web_mockup_job.py adjust --job 24921-black --decoration-id 8934 --offset-y-pct 4
    web_mockup_job.py status [--job 24921-black] [--tail 20]
    web_mockup_job.py status --brief        # poll a backgrounded run
    web_mockup_job.py status --last-run     # its final JSON once finished

Env: ODOO_MCP_URL (…/drivethru_mcp/v1), ODOO_MCP_TOKEN, and a vision key
(MOCKUP_VISION_API_KEY or OPENROUTER_API_KEY) — see vision_review.py.
Exit code is 0 whenever the run itself completed (per-job failures are in the
JSON); non-zero only for configuration / transport errors.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _paths  # noqa: E402
import _bootstrap  # noqa: E402
from locations import resolve_layers  # noqa: E402

_bootstrap.ensure(_bootstrap.REMBG + ["requests>=2.31,<3"],
                  _bootstrap.REMBG_MODS + ["requests"])

MAX_ATTEMPTS = 3
WEB_MAX_PX = 1200
WEB_JPEG_QUALITY = 85
ART_MAX_PX = 1600
MIN_BLANK_PX = 300
HTTP_TIMEOUT = 60
# Failures only a human can fix (bad source art / blank). Not retried each fire.
# How far reviewer fixes may move a print from its placement rule, in total.
# The rules are measured against approved mockups; a reviewer asking for more
# than this is more likely wrong than the rule (store 17: +6 x pushed a correct
# hoodie chest logo out to the armhole). Beyond it the job is rejected for a
# human instead of written.
MAX_TOTAL_DELTA = {"offset_x_pct": 4.0, "offset_y_pct": 5.0, "width_delta_pct": 15.0}

# Where a chest print's centre may sit, as a fraction of the garment width.
# Rules place left chest at 0.65 (0.67 read a touch wide); 0.73 was the
# armhole-seam case.
CHEST_ZONE = {"left_chest": (0.58, 0.71), "right_chest": (0.29, 0.42)}

# Reviewer issues no nudge can fix: the BLANK photo itself is unusable.
BLANK_ISSUES = {"bad_blank"}

# Statuses a person has to look at — the routine escalates these, it does not
# just report them.
HUMAN_STATUSES = {"rejected", "blank_rejected", "failed", "review_error", "unreviewed"}

PERMANENT_FAILURES = {"art_unusable", "background_not_removed", "blank_looks_like_placeholder",
                      "blank_too_small", "blank_unreadable", "source_empty"}


class JobError(Exception):
    """A per-job failure with a machine-readable ``code``."""

    def __init__(self, code, detail=""):
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


# ---------------------------------------------------------------------------
# Odoo transport — JSON-RPC tools/call for the plan, HTTP for bytes.
# ---------------------------------------------------------------------------
class Odoo:
    def __init__(self, base_url: str, token: str):
        base = (base_url or "").rstrip("/")
        if base.endswith("/upload"):
            base = base[: -len("/upload")]
        if not base.endswith("/drivethru_mcp/v1"):
            base += "/drivethru_mcp/v1"
        self.base = base
        self.token = token
        import requests

        self.http = requests.Session()
        self.http.headers["Authorization"] = f"Bearer {token}"

    def call_tool(self, name: str, arguments: dict) -> dict:
        body = {"jsonrpc": "2.0", "id": int(time.time() * 1000), "method": "tools/call",
                "params": {"name": name, "arguments": arguments}}
        resp = self.http.post(self.base, json=body, timeout=HTTP_TIMEOUT)
        if resp.status_code != 200:
            raise SystemExit(f"ERROR: MCP HTTP {resp.status_code}: {resp.text[:300]}")
        msg = resp.json()
        if "error" in msg:
            raise SystemExit(f"ERROR: MCP error: {msg['error']}")
        env = (msg.get("result") or {}).get("structuredContent") or {}
        if env.get("status") != "ok":
            raise SystemExit(f"ERROR: {name} failed: {json.dumps(env.get('error') or env)[:500]}")
        return env.get("data") or {}

    def download(self, source: dict, dest: Path) -> Path:
        """Fetch one image source (``{"url"}`` or ``{"fetch": {model,…}}``)."""
        if source.get("fetch"):
            ref = source["fetch"]
            resp = self.http.get(f"{self.base}/image", params=ref, timeout=HTTP_TIMEOUT)
            if resp.status_code == 404:
                raise JobError("source_empty", f"{ref['model']} {ref['record_id']} {ref['field']}")
        elif source.get("url"):
            import requests

            # Public CDN/vendor URL — do not send the Odoo credential elsewhere.
            resp = requests.get(source["url"], timeout=HTTP_TIMEOUT)
        else:
            raise JobError("source_missing")
        if resp.status_code != 200:
            raise JobError("download_failed", f"HTTP {resp.status_code}")
        ctype = resp.headers.get("Content-Type", "")
        if "json" in ctype or "html" in ctype:
            raise JobError("download_not_image", ctype)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(resp.content)
        return dest

    def upload(self, path: Path, model: str, field: str, record_ids: list[int]) -> dict:
        size = path.stat().st_size
        with path.open("rb") as fh:
            resp = self.http.post(
                f"{self.base}/upload",
                data={"model": model, "field": field,
                      "record_ids": ",".join(str(i) for i in record_ids)},
                files={"file": (path.name, fh, "image/jpeg")},
                timeout=HTTP_TIMEOUT * 2)
        try:
            body = resp.json()
        except ValueError:
            raise JobError("upload_failed", f"HTTP {resp.status_code} non-JSON")
        if resp.status_code != 200 or not body.get("success"):
            raise JobError("upload_failed", str(body.get("error") or body)[:300])
        data = body.get("data") or {}
        records = data.get("records") or [data]
        if data.get("bytes_received") != size:
            raise JobError("upload_truncated",
                           f"sent {size} bytes, server received {data.get('bytes_received')}")
        if not data.get("all_present") or any(not r.get("bytes_stored") for r in records):
            raise JobError("upload_not_stored", "server reports an empty field after write")
        return {"bytes": size, "records": len(records)}


# ---------------------------------------------------------------------------
# State — one JSON file so `adjust` can pick a job back up.
# ---------------------------------------------------------------------------
def _state_dir() -> Path:
    d = _paths.data_dir() / "web_jobs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _load_state() -> dict:
    p = _state_dir() / "state.json"
    if p.exists():
        try:
            return json.loads(p.read_text())
        except ValueError:
            pass
    return {"jobs": {}, "templates_written": []}


def _save_state(state: dict) -> None:
    p = _state_dir() / "state.json"
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=1))
    tmp.replace(p)


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-") or "x"


def _progress(line: str) -> None:
    """One human-readable line per finished job: stderr (live, for whoever runs
    the script) + progress.log (for `status --tail` / another session)."""
    stamped = f"{time.strftime('%H:%M:%S')} {line}"
    print(stamped, file=sys.stderr, flush=True)
    try:
        with (_state_dir() / "progress.log").open("a") as fh:
            fh.write(stamped + "\n")
    except OSError:
        pass


def _write_json(path: Path, data: dict) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=1, default=str))
    tmp.replace(path)


def _run_state(**fields) -> None:
    """``web_jobs/active_run.json`` — what a backgrounded run is doing, for
    ``status`` to report while it goes (pid, done/total, latest line)."""
    p = _state_dir() / "active_run.json"
    cur = {}
    if p.exists():
        try:
            cur = json.loads(p.read_text())
        except ValueError:
            cur = {}
    cur.update(fields)
    _write_json(p, cur)


def _pid_alive(pid) -> bool:
    try:
        os.kill(int(pid), 0)
        return True
    except (OSError, TypeError, ValueError):
        return False


def _fmt_money(v) -> str:
    return "$?" if v is None else f"${v:.3f}"


def _progress_line(i: int, n: int, job: dict, cost_delta) -> str:
    bits = [f"[{i}/{n}]", job["job_id"], job["status"]]
    if job["status"] == "image_written":
        w = job.get("write") or {}
        bits.append(f"{w.get('records', '?')} sizes, {round((w.get('bytes') or 0) / 1024)} KB")
    elif job.get("error"):
        bits.append(job["error"].get("code", "error"))
    else:
        for it in (job.get("review") or {}).get("issues", [])[:2]:
            fix = it.get("fix") or {}
            axis = {"offset_x_pct": "x", "offset_y_pct": "y", "width_delta_pct": "w"}
            f = ",".join(f"{v:+g}{axis.get(k, '?')}" for k, v in fix.items())
            bits.append(f"{it.get('code')}({f})" if f else str(it.get("code")))
    bits.append(f"a{job['attempts']}")
    bits.append(_fmt_money(cost_delta))
    return "  ".join(bits)


def _job_cost(job: dict):
    """(usd_or_None, calls). usd is None if any call's cost was unreported."""
    total, calls, unknown = 0.0, 0, False
    for h in job.get("history", []):
        if h.get("vision_called"):
            calls += 1
            if h.get("cost_usd") is None:
                unknown = True
            else:
                total += h["cost_usd"]
    return (None if unknown and calls else round(total, 6)), calls


def _cost_block(jobs_before_after) -> dict:
    """Spend for the attempts made in THIS invocation."""
    usd, calls, unknown = 0.0, 0, False
    written = 0
    for before, job in jobs_before_after:
        b_usd, b_calls = before
        a_usd, a_calls = _job_cost(job)
        calls += a_calls - b_calls
        if a_usd is None or b_usd is None:
            unknown = unknown or (a_calls - b_calls) > 0
        else:
            usd += a_usd - b_usd
        written += job["status"] == "image_written"
    out = {"vision_usd": None if unknown else round(usd, 4), "vision_calls": calls}
    if written and not unknown:
        out["per_written_colour_usd"] = round(usd / written, 4)
    if unknown:
        out["note"] = "the vision endpoint did not report cost for some calls"
    return out


def _tuning(jobs) -> list[dict]:
    """What approved mockups needed, per (category, placement).

    Only written jobs count, and only their final deltas (what the reviewer
    accepted). When >= 2 agree in sign on an axis, the mean correction is
    offered as a catalog edit so future mockups start right.
    """
    groups = {}
    for job in jobs:
        if job.get("status") != "image_written":
            continue
        for lay in job.get("layout", []):
            key = (lay["category_resolved"], lay["placement"])
            d = job.get("deltas", {}).get(str(lay["decoration_id"]), {})
            g = groups.setdefault(key, {"rule": lay["rule"], "n": 0, "deltas": []})
            g["n"] += 1
            g["deltas"].append(d)
    out = []
    for (cat, placement), g in sorted(groups.items()):
        adjusted = [d for d in g["deltas"] if any(d.values())]
        row = {"category": cat, "placement": placement, "approved": g["n"],
               "needed_adjustment": len(adjusted)}
        if adjusted:
            mean, flags = {}, []
            for k in ("offset_x_pct", "offset_y_pct", "width_delta_pct"):
                vals = [d.get(k, 0) for d in adjusted if d.get(k)]
                if len(vals) >= 2 and (all(v > 0 for v in vals) or all(v < 0 for v in vals)):
                    mean[k] = round(sum(vals) / len(vals), 1)
            row["deltas"] = adjusted
            row["mean_delta"] = mean or None
            if mean:
                r = g["rule"]
                if "offset_x_pct" in mean:
                    flags.append(f"--x-center-ratio {r['x_center_ratio'] + mean['offset_x_pct'] / 100:.3f}")
                if "offset_y_pct" in mean:
                    flags.append(f"--y-top-ratio {r['y_top_ratio'] + mean['offset_y_pct'] / 100:.3f}")
                if "width_delta_pct" in mean:
                    flags.append(f"--width-ratio {r['width_ratio'] * (1 + mean['width_delta_pct'] / 100):.3f}")
                row["suggest"] = (f"python3 scripts/edit_placement_rule.py update {cat} "
                                  f"{placement} " + " ".join(flags) +
                                  "   # human decision — affects every future mockup")
        out.append(row)
    return out


def _category_for(blank_name: str) -> str | None:
    n = (blank_name or "").lower()
    if "hood" in n:
        return "hoodie"
    if re.search(r"\b(hat|cap|beanie|visor|trucker)\b", n):
        return "hat"
    if re.search(r"\b(mug|tumbler)\b", n):
        return "mug"
    if re.search(r"\b(tee|t-shirt|tshirt)\b", n):
        return "tee"
    return None


# ---------------------------------------------------------------------------
# Image checks + prep
# ---------------------------------------------------------------------------
def _check_blank(path: Path) -> None:
    """Reject anything that is not a real product photo."""
    from PIL import Image, ImageStat

    try:
        im = Image.open(path)
        im.load()
    except Exception as exc:  # noqa: BLE001
        raise JobError("blank_unreadable", str(exc))
    if min(im.size) < MIN_BLANK_PX:
        raise JobError("blank_too_small", f"{im.size[0]}x{im.size[1]}")
    small = im.convert("RGB").resize((64, 64))
    colors = len(set(small.getdata()))
    std = sum(ImageStat.Stat(small.convert("L")).stddev)
    # Both must be low: a real white tee on a white sweep is low-variance but
    # still has shading; a placeholder/icon is flat AND nearly colourless.
    if colors < 8 and std < 2:
        raise JobError("blank_looks_like_placeholder",
                       f"{colors} colours, stddev {std:.1f}")


def _border_opaque_fraction(img) -> float:
    """Fraction of the outer ring that is opaque — a surviving plate shows up
    as an opaque border around the art."""
    import numpy as np

    a = np.asarray(img.getchannel("A"))
    h, w = a.shape
    r = max(1, int(round(min(h, w) * 0.02)))
    ring = np.concatenate([a[:r].ravel(), a[-r:].ravel(), a[:, :r].ravel(), a[:, -r:].ravel()])
    return float((ring > 200).mean())


def _key_inner_plate(img):
    """Key out a solid background plate that sits INSIDE transparent art.

    Production PNGs aren't always clean cut-outs: an embroidery preview can be
    the design on a swatch of fabric colour with transparent padding around it
    (decoration 5444: an orange plate). Such a file has transparent pixels, so
    it looks "already cut out" — and the plate got composited onto the garment.
    After trimming to the visible content, a clean logo's outer ring is mostly
    transparent; a plate's is opaque and one colour. Key that colour out
    (colour-to-alpha, so edges stay clean — the plate colour is fabric, not
    thread/ink). Returns ``(image, key_hex or None)``.
    """
    import numpy as np
    from PIL import Image
    from compose_mockup import _trim_to_content, _color_to_alpha

    t = _trim_to_content(img, {})
    a = np.asarray(t).astype(np.float32)
    h, w = a.shape[:2]
    r = max(2, int(round(min(h, w) * 0.03)))
    ring = np.concatenate([a[:r].reshape(-1, 4), a[-r:].reshape(-1, 4),
                           a[:, :r].reshape(-1, 4), a[:, -r:].reshape(-1, 4)])
    opaque = ring[ring[:, 3] > 200]
    if len(opaque) < 0.85 * len(ring):
        return t, None
    key = np.median(opaque[:, :3], axis=0)
    dist = np.sqrt(((opaque[:, :3] - key) ** 2).sum(axis=1))
    if np.percentile(dist, 90) > 30:
        return t, None                      # not one colour: leave it to the border check
    out_rgb, a01 = _color_to_alpha(a[..., :3], key)
    new_alpha = np.clip(a01 * a[..., 3], 0, 255)
    removed = float(((new_alpha < 20) & (a[..., 3] >= 20)).mean())
    if removed < 0.05:
        return t, None
    cut = Image.fromarray(np.dstack([out_rgb, new_alpha.round().astype(np.uint8)]), "RGBA")
    return (_trim_to_content(cut, {}),
            "#{:02X}{:02X}{:02X}".format(*(int(round(v)) for v in key)))


def _prepare_art(odoo: Odoo, deco: dict, work: Path):
    """Return ``(rgba_image, info)`` for a decoration, best source first."""
    from PIL import Image
    import numpy as np
    from compose_mockup import _prepare_decoration

    tried = []
    for i, src in enumerate(deco.get("art_sources") or []):
        kind = src.get("kind")
        try:
            raw = odoo.download(src, work / f"art_{deco['decoration_id']}_{i}_{kind}")
            img = Image.open(raw)
            img.load()
            img = img.convert("RGBA")
            if max(img.size) > ART_MAX_PX:
                img.thumbnail((ART_MAX_PX, ART_MAX_PX), Image.LANCZOS)
            alpha = np.asarray(img.getchannel("A"))
            if int(alpha.min()) < 250:
                prepared, method = img, "already_transparent"
            else:
                # Opaque art (every thumbnail; a production PNG exported without
                # alpha): key the plate, or segment it — never paste it as-is.
                flat = work / f"art_{deco['decoration_id']}_{i}_flat.png"
                img.convert("RGB").save(flat)
                prepared, prep = _prepare_decoration(flat, auto_remove_bg=True)
                method = prep.get("method")
            # Transparent art can still carry a plate inside it — key it out.
            prepared, plate = _key_inner_plate(prepared)
            clear = float((np.asarray(prepared.getchannel("A")) < 20).mean())
            border = _border_opaque_fraction(prepared)
            # After trimming, a clean cut-out's outer ring is mostly transparent
            # (the space around its shapes). If it is still a solid rectangle,
            # a background survived (textured / multi-colour plate): reject this
            # source and try the next rather than composite a box.
            if border > 0.85:
                raise JobError("background_not_removed",
                               f"{kind}: border {border:.0%} opaque after prep "
                               f"({clear:.0%} transparent)")
            return prepared, {"source": kind, "method": method,
                              "plate_keyed": plate,
                              "transparent_fraction": round(clear, 3),
                              "sources_tried": tried}
        except JobError as exc:
            tried.append({"source": kind, "error": exc.code, "detail": exc.detail})
        except Exception as exc:  # noqa: BLE001
            tried.append({"source": kind, "error": type(exc).__name__, "detail": str(exc)[:160]})
    raise JobError("art_unusable", json.dumps(tried)[:400])


def _geometry_checks(layer: dict, receipt: dict) -> list[dict]:
    """Deterministic side/bounds checks from the compose receipt."""
    bb = receipt["garment_bbox"]
    px, py = receipt["paste_top_left_px"]
    w, h = receipt["decoration_size_px"]
    rel_x = (px + w / 2 - bb["left"]) / max(1, bb["width"])
    side = layer.get("image_side")
    issues = []
    wrong = ((side == "right" and rel_x <= 0.52) or (side == "left" and rel_x >= 0.48)
             or (side == "center" and not 0.40 <= rel_x <= 0.60))
    if wrong:
        issues.append({
            "decoration_id": layer["decoration_id"], "code": "wrong_side",
            "detail": (f"{layer['placement']} centre at {rel_x:.0%} of garment width; "
                       f"must be on the image {side}"),
            "fix": {"offset_x_pct": round((1 - 2 * rel_x) * 100, 1)} if side != "center"
            else {"offset_x_pct": round((0.5 - rel_x) * 100, 1)},
        })
    zone = CHEST_ZONE.get(layer.get("placement"))
    if zone and not wrong and not zone[0] <= rel_x <= zone[1]:
        target = (zone[0] + zone[1]) / 2
        issues.append({
            "decoration_id": layer["decoration_id"],
            "code": "outside_chest_zone",
            "detail": (f"{layer['placement']} centre at {rel_x:.0%} of garment width; "
                       f"a chest print belongs between {zone[0]:.0%} and {zone[1]:.0%}"),
            "fix": {"offset_x_pct": round((target - rel_x) * 100, 1)},
        })
    tol_x, tol_y = 0.02 * bb["width"], 0.02 * bb["height"]
    if (px < bb["left"] - tol_x or px + w > bb["left"] + bb["width"] + tol_x
            or py < bb["top"] - tol_y or py + h > bb["top"] + bb["height"] + tol_y):
        issues.append({"decoration_id": layer["decoration_id"], "code": "clipped",
                       "detail": "print extends past the garment", "fix": {}})
    return issues


# ---------------------------------------------------------------------------
# One job = one product colour
# ---------------------------------------------------------------------------
def _new_job(product: dict, color: dict, resolved: dict) -> dict:
    return {
        "job_id": f"{product['product_tmpl_id']}-{_slug(color['color'])}",
        "product_tmpl_id": product["product_tmpl_id"],
        "product_name": product["name"],
        "template_needs_image": not product.get("template_has_image"),
        "category": _category_for(product.get("blank_name")),
        "color": color["color"],
        "target_variant_ids": color["target_variant_ids"],
        "blank": color["blank"],
        "blank_product_tmpl_id": product.get("blank_product_tmpl_id"),
        "layers": resolved["layers"],
        "omitted_decoration_ids": [o["decoration_id"] for o in resolved["omitted"]],
        "deltas": {},
        "attempts": 0,
        "history": [],
        "status": "pending",
    }


def _run_job(odoo: Odoo, job: dict, state: dict, *, dry_run: bool, vision: bool) -> dict:
    from PIL import Image
    from compose_mockup import compose, _detect_bbox
    import vision_review

    if job["attempts"] >= MAX_ATTEMPTS:
        job["status"] = "rejected"
        return job
    job["attempts"] += 1
    attempt = job["attempts"]
    work = _state_dir() / job["job_id"]
    work.mkdir(parents=True, exist_ok=True)

    try:
        blank = work / "blank"
        if attempt == 1 or not blank.exists():
            # Fresh on a new job (the blank may have been fixed since); reused
            # across `adjust` attempts so every attempt composes the same photo.
            odoo.download(job["blank"], blank)
        _check_blank(blank)
        if not job.get("bbox"):
            job["bbox"] = _detect_bbox(blank)

        arts, art_info = [], {}
        for layer in job["layers"]:
            img, info = _prepare_art(odoo, layer, work)
            arts.append(img)
            art_info[str(layer["decoration_id"])] = info
        job["art"] = art_info

        base, receipts, issues = None, [], []
        for i, (layer, art) in enumerate(zip(job["layers"], arts)):
            d = job["deltas"].get(str(layer["decoration_id"]), {})
            out = work / f"attempt{attempt}_layer{i}.png"
            receipt = compose(
                blank_path=blank, decoration_path=out, category=job["category"],
                placement=layer["placement"], rules_path=_paths.effective_rules_path(),
                output_path=out, auto_remove_bg=False,
                width_delta_pct=float(d.get("width_delta_pct", 0)),
                offset_x_pct=float(d.get("offset_x_pct", 0)),
                offset_y_pct=float(d.get("offset_y_pct", 0)),
                rotate_deg_override=None, side_pad_pct_override=None,
                bbox=job["bbox"], base_path=base, decoration_image=art)
            base = out
            receipts.append(receipt)
            if i == 0:
                job["layout"] = []
            job["layout"].append({"decoration_id": layer["decoration_id"],
                                  "placement": layer["placement"],
                                  "category_resolved": receipt["category_resolved"],
                                  "rule": receipt["rule"]})
            issues += _geometry_checks(layer, receipt)
        final_png = base

        web = work / f"attempt{attempt}_web.jpg"
        im = Image.open(final_png).convert("RGBA")
        flat = Image.new("RGB", im.size, (255, 255, 255))
        flat.paste(im, mask=im.getchannel("A"))
        flat.thumbnail((WEB_MAX_PX, WEB_MAX_PX), Image.LANCZOS)
        flat.save(web, format="JPEG", quality=WEB_JPEG_QUALITY, optimize=True)
        job["web_jpeg"] = str(web)

        if issues:
            review = {"verdict": "no", "source": "geometry", "issues": issues}
        elif job.get("human_redo"):
            # A person sent the written image back with this exact correction:
            # they are the reviewer. Geometry still applies; vision does not.
            review = {"verdict": "yes", "source": "human_redo", "issues": []}
        elif not vision:
            review = {"verdict": "unreviewed", "source": "none", "issues": []}
        else:
            spec = {"product_name": job["product_name"], "color": job["color"],
                    "omitted": bool(job["omitted_decoration_ids"]),
                    "layers": job["layers"]}
            review = vision_review.review(final_png, spec, arts)
            review["source"] = "vision"
        called = review.get("source") == "vision"
        job["history"].append({"attempt": attempt, "deltas": json.loads(json.dumps(job["deltas"])),
                               "verdict": review.get("verdict"),
                               "issues": review.get("issues", []),
                               "error": review.get("error"),
                               "vision_called": called,
                               "cost_usd": (review.get("usage") or {}).get("cost_usd")
                               if called else 0.0})
        job["review"] = review

        if review.get("verdict") != "yes":
            job["suggested"] = _suggested(review)
            if review.get("verdict") == "error":
                job["status"] = "review_error"
            elif any(i.get("code") in BLANK_ISSUES for i in review.get("issues", [])):
                # The photo is a placeholder / on-model / unusable shot: moving
                # the print cannot fix it. `run` re-fetches it from the vendor.
                job["status"] = "blank_rejected"
            elif review.get("verdict") == "unreviewed":
                job["status"] = "unreviewed"
            else:
                job["status"] = "rejected" if attempt >= MAX_ATTEMPTS else "needs_adjustment"
            return job

        if dry_run:
            job["status"] = "approved_dry_run"
            return job
        job["write"] = odoo.upload(web, "product.product", "image_variant_1920",
                                   job["target_variant_ids"])
        tmpl = job["product_tmpl_id"]
        if job["template_needs_image"] and tmpl not in state["templates_written"]:
            odoo.upload(web, "product.template", "image_1920", [tmpl])
            state["templates_written"].append(tmpl)
            job["template_written"] = True
        job["status"] = "image_written"
    except JobError as exc:
        job["status"] = "failed"
        job["error"] = {"code": exc.code, "detail": exc.detail}
    except SystemExit as exc:
        job["status"] = "failed"
        job["error"] = {"code": "compose_error", "detail": str(exc)[:300]}
    except Exception as exc:  # noqa: BLE001
        # An unexpected error is a bug in this pipeline, not bad data — keep
        # where it happened (last few frames) so it can be fixed from the
        # report alone instead of re-running blind.
        import traceback

        frames = traceback.extract_tb(exc.__traceback__)[-4:]
        job["status"] = "failed"
        job["error"] = {"code": type(exc).__name__, "detail": str(exc)[:300],
                        "where": [f"{Path(f.filename).name}:{f.lineno} {f.name}: "
                                  f"{(f.line or '').strip()[:120]}" for f in frames]}
    return job


def _suggested(review: dict) -> dict:
    """Merge the reviewer's per-decoration fixes into one delta set."""
    out = {}
    for it in review.get("issues", []):
        fix = it.get("fix") or {}
        if not fix:
            continue
        key = str(it.get("decoration_id") or "*")
        cur = out.setdefault(key, {})
        for k, v in fix.items():
            cur[k] = round(cur.get(k, 0) + v, 1)
    return out


def _job_summary(job: dict) -> dict:
    s = {"job": job["job_id"], "product": job["product_name"], "color": job["color"],
         "status": job["status"], "attempts": job["attempts"]}
    if job.get("error"):
        s["error"] = job["error"]
    if job["status"] in ("needs_adjustment", "rejected", "review_error", "unreviewed",
                         "blank_rejected"):
        rv = job.get("review") or {}
        s["issues"] = [{"decoration_id": i.get("decoration_id"), "code": i.get("code"),
                        "detail": i.get("detail")} for i in rv.get("issues", [])]
        if rv.get("error"):
            s["review_error"] = rv["error"]
        if job["status"] == "needs_adjustment":
            fixable = bool(job.get("suggested"))
            s["next"] = (f"python3 scripts/web_mockup_job.py adjust --job {job['job_id']} "
                         f"--apply-suggested") if fixable else (
                "not fixable by moving (background/blank/art problem) — leave it; "
                "it is logged for a human")
            s["suggested"] = job.get("suggested")
        if job["status"] == "review_error":
            s["next"] = f"python3 scripts/web_mockup_job.py adjust --job {job['job_id']}  # re-review"
    if job.get("art"):
        s["art_sources"] = {k: v["source"] for k, v in job["art"].items()}
    usd, calls = _job_cost(job)
    if calls:
        s["vision_cost_usd"] = usd
    return s


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------
def _odoo() -> Odoo:
    url, token = os.environ.get("ODOO_MCP_URL"), os.environ.get("ODOO_MCP_TOKEN")
    if not url or not token:
        raise SystemExit("ERROR: ODOO_MCP_URL and ODOO_MCP_TOKEN must be set")
    return Odoo(url, token)


def cmd_run(args) -> dict:
    odoo = _odoo()
    plan_args = {"limit": args.limit}
    if args.include_imaged:
        plan_args["include_imaged"] = True
    if args.site_id:
        plan_args["site_id"] = args.site_id
    elif args.product_tmpl_ids:
        plan_args["product_tmpl_ids"] = [int(x) for x in args.product_tmpl_ids.split(",")]
    else:
        raise SystemExit("ERROR: pass --site-id or --product-tmpl-ids")
    blank_refresh = None
    if not args.no_refresh_blanks:
        # Blank colours with no photo (or only an on-model one) are filled from
        # the integrated vendor first — SanMar SDL flat front / S&S
        # colorFrontImage — so they get a mockup in this same run. Always
        # asked (cheap): a product whose only problem is missing blanks is not
        # in the default plan at all. A dry run only reports.
        try:
            blank_refresh = odoo.call_tool("web_mockup_refresh_blanks",
                                           {**plan_args, "dry_run": bool(args.dry_run)})
            _progress(f"blank refresh ({'dry run' if args.dry_run else 'write'}): "
                      f"{blank_refresh.get('counts') or 'nothing missing'}")
        except (SystemExit, Exception) as exc:  # noqa: BLE001 — never block the run on it
            blank_refresh = {"error": str(exc)[:300]}
            _progress(f"blank refresh unavailable: {str(exc)[:160]}")
    plan = odoo.call_tool("web_mockup_plan", plan_args)

    state = _load_state()
    skipped, results, queue, not_imaged = {}, [], [], []
    for product in plan.get("products", []):
        if product.get("skip_reason"):
            skipped[product["skip_reason"]] = skipped.get(product["skip_reason"], 0) + 1
            continue
        # Placement is decided HERE from the raw location names — never by Odoo.
        resolved = resolve_layers(product.get("decorations") or [])
        if resolved["skip_reason"]:
            skipped[resolved["skip_reason"]] = skipped.get(resolved["skip_reason"], 0) + 1
            not_imaged.append({"product_tmpl_id": product["product_tmpl_id"],
                               "name": product.get("name"),
                               "reason": resolved["skip_reason"],
                               "decorations": resolved["omitted"]})
            continue
        for color in product.get("colors", []):
            if not color.get("needs_image"):
                r = color.get("skip_reason") or "not_needed"
                skipped[r] = skipped.get(r, 0) + 1
                continue
            if len(queue) >= args.max_colors:
                skipped["deferred_max_colors"] = skipped.get("deferred_max_colors", 0) + 1
                continue
            job = _new_job(product, color, resolved)
            if args.include_imaged:
                # A deliberate redo: the existing image (e.g. a blank photo the
                # store-build wizard copied over) is replaced, template included.
                job["template_needs_image"] = True
            prev = state["jobs"].get(job["job_id"])
            parked = prev and (
                prev.get("status") in ("needs_adjustment", "rejected", "review_error",
                                       "blank_rejected")
                or (prev.get("status") == "failed"
                    and (prev.get("error") or {}).get("code") in PERMANENT_FAILURES))
            if parked and not args.retry_stuck:
                # Waiting on `adjust`, given up on, or blocked on source data a
                # human must fix — don't burn every fire re-running it.
                results.append(_job_summary(prev))
                continue
            queue.append(job)

    ran = []
    rules = _paths.effective_rules_path()
    start_line = (f"run start: {len(queue)} colour job(s), scope {plan_args}, rules "
                  f"{'BUNDLED' if rules == _paths.BUNDLED_RULES else rules}")
    _progress(start_line)
    (_state_dir() / "active_run.json").unlink(missing_ok=True)
    _run_state(pid=os.getpid(), started=time.strftime("%Y-%m-%d %H:%M:%S"),
               scope=plan_args, done=0, total=len(queue), latest=start_line)
    def run_queue(jobs):
        out = []
        for i, job in enumerate(jobs, 1):
            before = _job_cost(job)
            job = _run_job(odoo, job, state, dry_run=args.dry_run, vision=not args.no_vision)
            state["jobs"][job["job_id"]] = job
            _save_state(state)
            ran.append((before, job))
            after = _job_cost(job)
            delta = None if after[0] is None or before[0] is None else after[0] - before[0]
            line = _progress_line(i, len(jobs), job, delta)
            _progress(line)
            _run_state(done=i, latest=line)
            out.append(job)
        return out

    done = run_queue(queue)
    blank_refetch = None
    bad = [j for j in done if j["status"] == "blank_rejected" and j.get("blank_product_tmpl_id")]
    if bad and not args.dry_run and not args.no_refresh_blanks:
        # The reviewer rejected the blank photo itself (a stored "image not
        # available" graphic, an on-model shot). Ask the vendor for that exact
        # colour, and if a new photo lands, image the colour again right now.
        done, blank_refetch = _refetch_rejected_blanks(odoo, bad, done, plan_args, args,
                                                       run_queue)
    results += [_job_summary(j) for j in done]

    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    cost = _cost_block(ran)
    _progress(f"run end: {counts}  vision {_fmt_money(cost['vision_usd'])} "
              f"over {cost['vision_calls']} call(s)")
    result = {"scope": plan_args, "products_planned": plan.get("count"),
            "remaining_unscanned": plan.get("remaining_unscanned"),
            "counts": counts, "skipped": skipped, "not_imaged": not_imaged, "cost": cost,
            "tuning": _tuning([j for _, j in ran]), "jobs": results,
            "needs_human": _needs_human(results, not_imaged)}
    if blank_refetch is not None:
        result["blank_refetch"] = blank_refetch
    if blank_refresh is not None:
        result["blank_refresh"] = {
            "counts": blank_refresh.get("counts"),
            "error": blank_refresh.get("error"),
            "colors": [{k: r.get(k) for k in ("blank_product_tmpl_id", "vendor", "style",
                                              "color", "outcome")}
                       for r in blank_refresh.get("colors") or []],
        }
    result["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
    # Saved so a backgrounded run's result can be read with `status --last-run`.
    _write_json(_state_dir() / "last_run.json", result)
    (_state_dir() / "active_run.json").unlink(missing_ok=True)
    return result


def _refetch_rejected_blanks(odoo, bad, done, plan_args, args, run_queue):
    """Re-fetch reviewer-rejected blank colours from the vendor; rerun the
    colours that got a new photo. Returns ``(jobs, report)``."""
    wanted = [{"blank_product_tmpl_id": j["blank_product_tmpl_id"], "color": j["color"]}
              for j in bad]
    try:
        res = odoo.call_tool("web_mockup_refresh_blanks",
                             {"blank_colors": wanted, "dry_run": False})
    except (SystemExit, Exception) as exc:  # noqa: BLE001 — never block the run on it
        _progress(f"blank re-fetch unavailable: {str(exc)[:160]}")
        return done, {"error": str(exc)[:300], "requested": wanted}
    fixed = {(r.get("blank_product_tmpl_id"), (r.get("color") or "").lower())
             for r in res.get("colors") or [] if r.get("outcome") == "updated"}
    report = {"requested": wanted, "counts": res.get("counts"),
              "colors": [{k: r.get(k) for k in ("blank_product_tmpl_id", "style", "color",
                                                "outcome")} for r in res.get("colors") or []]}
    _progress(f"blank re-fetch for {len(wanted)} rejected photo(s): {res.get('counts')}")
    retry = [j for j in bad
             if (j["blank_product_tmpl_id"], j["color"].lower()) in fixed]
    if not retry:
        return done, report
    replan = odoo.call_tool("web_mockup_plan", {
        "product_tmpl_ids": sorted({j["product_tmpl_id"] for j in retry}),
        "include_imaged": bool(args.include_imaged), "limit": 50})
    fresh = []
    for product in replan.get("products", []):
        resolved = resolve_layers(product.get("decorations") or [])
        if resolved["skip_reason"]:
            continue
        for color in product.get("colors", []):
            key = f"{product['product_tmpl_id']}-{_slug(color['color'])}"
            if color.get("needs_image") and any(j["job_id"] == key for j in retry):
                job = _new_job(product, color, resolved)
                if args.include_imaged:
                    job["template_needs_image"] = True
                fresh.append(job)
    _progress(f"re-imaging {len(fresh)} colour(s) on the new vendor photo")
    rerun = {j["job_id"]: j for j in run_queue(fresh)}
    report["reimaged"] = sorted(rerun)
    return [rerun.get(j["job_id"], j) for j in done], report


# What a person needs to do about each status the routine cannot resolve.
_HUMAN_ACTION = {
    "blank_rejected": "blank photo is unusable and the vendor had no replacement — "
                      "add a flat front photo for this colour on the blank",
    "rejected": "3 attempts or the fix exceeded the adjustment limit — look at the "
                "mockup; fix the art/placement rule or accept it",
    "review_error": "vision review could not run — re-run the job",
    "unreviewed": "written without a vision review — check it",
    "needs_adjustment": "reviewer's objection has no automatic fix — look at it",
}


def _needs_human(summaries: list[dict], not_imaged: list[dict] | None = None) -> list[dict]:
    """Everything the routine must ESCALATE (not just report) after a run."""
    out = []
    for s in summaries:
        st = s.get("status")
        unfixable = st == "needs_adjustment" and not s.get("suggested")
        if st not in HUMAN_STATUSES and not unfixable:
            continue
        err = s.get("error") or {}
        if st == "failed":
            action = ("pipeline bug — report error.where" if "where" in err
                      else f"fix the source data ({err.get('code')}), then run --retry-stuck")
        else:
            action = _HUMAN_ACTION.get(st, "look at it")
        out.append({"job": s["job"], "product": s.get("product"), "color": s.get("color"),
                    "status": st,
                    "why": err.get("code") or s.get("review_error") or ", ".join(
                        f"{i.get('code')}: {i.get('detail')}" for i in s.get("issues", []))[:300],
                    "action": action})
    for p in not_imaged or []:
        out.append({"job": None, "product": p.get("name"), "color": None,
                    "status": "not_imaged", "why": p.get("reason"),
                    "action": "no decoration can go on a front photo — check the "
                              "decoration locations: " + ", ".join(
                                  str(d.get("location_name")) for d in p.get("decorations", []))})
    return out


def cmd_adjust(args) -> dict:
    state = _load_state()
    job = state["jobs"].get(args.job)
    if not job:
        raise SystemExit(f"ERROR: unknown job {args.job!r} (see `status`)")
    manual_given = any(v for v in (args.offset_x_pct, args.offset_y_pct,
                                   args.width_delta_pct))
    if args.redo:
        # A reviewer sent a written image back with a concrete correction.
        if not manual_given:
            raise SystemExit("ERROR: --redo needs the reviewer's correction as "
                             "--offset-x-pct / --offset-y-pct / --width-delta-pct")
        if job.get("template_written"):
            state["templates_written"] = [t for t in state["templates_written"]
                                          if t != job["product_tmpl_id"]]
            job["template_needs_image"] = True
        job["attempts"] = 0
        job["human_redo"] = True
        job["redos"] = job.get("redos", 0) + 1
        job.pop("error", None)
    elif job["status"] == "image_written":
        return {"job": args.job, "status": "image_written",
                "note": "already written — a reviewer's correction goes through --redo"}
    else:
        job.pop("human_redo", None)
    if job["attempts"] >= MAX_ATTEMPTS:
        job["status"] = "rejected"
        _save_state(state)
        return {**_job_summary(job), "note": f"hit the {MAX_ATTEMPTS}-attempt cap — "
                "not written; logged for a human"}

    patch = {}
    if args.apply_suggested:
        patch = json.loads(json.dumps(job.get("suggested") or {}))
    manual = {k: v for k, v in (("offset_x_pct", args.offset_x_pct),
                                ("offset_y_pct", args.offset_y_pct),
                                ("width_delta_pct", args.width_delta_pct)) if v}
    if manual:
        deco = args.decoration_id
        if deco is None:
            if len(job["layers"]) != 1:
                raise SystemExit("ERROR: this mockup has several decorations — pass --decoration-id")
            deco = job["layers"][0]["decoration_id"]
        cur = patch.setdefault(str(deco), {})
        for k, v in manual.items():
            cur[k] = cur.get(k, 0) + v
    if "*" in patch:
        star = patch.pop("*")
        for layer in job["layers"]:
            cur = patch.setdefault(str(layer["decoration_id"]), {})
            for k, v in star.items():
                cur[k] = cur.get(k, 0) + v

    # Layer onto the previous deltas; halve a correction whose sign flips
    # (oscillation guard — we overshot, so we're close).
    for deco_id, fix in patch.items():
        prev_last = (job.get("last_patch") or {}).get(deco_id, {})
        cur = job["deltas"].setdefault(deco_id, {})
        for k, v in fix.items():
            if not args.redo and prev_last.get(k) and (prev_last[k] > 0) != (v > 0):
                v = v / 2.0
            cur[k] = round(cur.get(k, 0) + v, 1)
    job["last_patch"] = patch

    over = {f"{deco_id}.{k}": v for deco_id, d in job["deltas"].items()
            for k, v in d.items() if abs(v) > MAX_TOTAL_DELTA.get(k, 1e9)}
    if over and not args.redo:  # the cap guards the reviewer model, not a person
        # Don't compose it: a fix this large means the reviewer and the measured
        # rule disagree, and a human should decide which is right.
        job["status"] = "rejected"
        job["error"] = {"code": "adjustment_limit",
                        "detail": (f"total fix {over} exceeds the limit "
                                   f"{MAX_TOTAL_DELTA} — left for a human")}
        state["jobs"][job["job_id"]] = job
        _save_state(state)
        _progress(f"adjust {job['job_id']} rejected: adjustment_limit {over}")
        return {**_job_summary(job), "deltas": job["deltas"]}

    odoo = _odoo()
    before = _job_cost(job)
    job = _run_job(odoo, job, state, dry_run=args.dry_run, vision=not args.no_vision)
    state["jobs"][job["job_id"]] = job
    _save_state(state)
    after = _job_cost(job)
    delta = None if after[0] is None or before[0] is None else after[0] - before[0]
    _progress("adjust " + _progress_line(1, 1, job, delta))
    return {**_job_summary(job), "deltas": job["deltas"],
            "cost": _cost_block([(before, job)])}


def cmd_status(args) -> dict:
    state = _load_state()
    if args.last_run:
        p = _state_dir() / "last_run.json"
        if not p.exists():
            return {"last_run": None, "note": "no run has finished yet"}
        return json.loads(p.read_text())
    if args.job:
        job = state["jobs"].get(args.job)
        if not job:
            raise SystemExit(f"ERROR: unknown job {args.job!r}")
        return {**_job_summary(job), "deltas": job["deltas"],
                "history": [{k: h.get(k) for k in ("attempt", "verdict", "deltas")}
                            for h in job["history"]]}
    counts, open_jobs = {}, []
    usd, calls, unknown = 0.0, 0, False
    for job in state["jobs"].values():
        counts[job["status"]] = counts.get(job["status"], 0) + 1
        if job["status"] in HUMAN_STATUSES | {"needs_adjustment"}:
            open_jobs.append(_job_summary(job))
        j_usd, j_calls = _job_cost(job)
        calls += j_calls
        if j_usd is None:
            unknown = unknown or j_calls > 0
        else:
            usd += j_usd
    recent = []
    log = _state_dir() / "progress.log"
    if args.tail and log.exists():
        recent = log.read_text().splitlines()[-args.tail:]
    active = None
    ap = _state_dir() / "active_run.json"
    if ap.exists():
        try:
            active = json.loads(ap.read_text())
        except ValueError:
            active = {}
        active["alive"] = _pid_alive(active.get("pid"))
        if not active["alive"]:
            active["note"] = ("process is gone without finishing — it crashed or was "
                              "killed; see `recent` and report it")
    lp = _state_dir() / "last_run.json"
    last_finished = None
    if lp.exists():
        try:
            last_finished = json.loads(lp.read_text()).get("finished")
        except ValueError:
            pass
    if args.brief:
        tail = recent[-3:] if recent else []
        return {"active_run": active, "last_run_finished": last_finished, "recent": tail}
    return {"active_run": active, "last_run_finished": last_finished,
            "counts": counts, "open": open_jobs, "needs_human": _needs_human(open_jobs),
            "cost_all_time": {"vision_usd": None if unknown else round(usd, 4),
                              "vision_calls": calls},
            "tuning": _tuning(state["jobs"].values()),
            "recent": recent}


def main() -> None:
    ap = argparse.ArgumentParser(description="Storefront web mockups, end to end")
    sub = ap.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="plan → compose → review → write")
    run.add_argument("--site-id", type=int)
    run.add_argument("--product-tmpl-ids", help="comma-separated product.template ids")
    run.add_argument("--limit", type=int, default=10, help="products per run (max 50)")
    run.add_argument("--max-colors", type=int, default=30, help="colour jobs per run")
    run.add_argument("--dry-run", action="store_true", help="review but never write")
    run.add_argument("--no-vision", action="store_true",
                     help="skip the vision review (testing only — never writes)")
    run.add_argument("--include-imaged", action="store_true",
                     help="also redo colours (and the template) that already have an "
                          "image — e.g. a blank photo copied over by the store-build "
                          "wizard. Only when explicitly asked.")
    run.add_argument("--no-refresh-blanks", action="store_true",
                     help="don't fill missing blank-colour photos from SanMar / S&S "
                          "before planning")
    run.add_argument("--retry-stuck", action="store_true",
                     help="restart jobs parked as rejected / permanently failed "
                          "(after a human fixed the art or blank)")

    adj = sub.add_parser("adjust", help="re-compose one job with deltas, re-review, write on yes")
    adj.add_argument("--job", required=True)
    adj.add_argument("--apply-suggested", action="store_true",
                     help="apply the reviewer's suggested deltas")
    adj.add_argument("--decoration-id", type=int)
    adj.add_argument("--offset-x-pct", type=float, help="+ moves RIGHT in the image")
    adj.add_argument("--offset-y-pct", type=float, help="+ moves DOWN")
    adj.add_argument("--width-delta-pct", type=float, help="+ makes it bigger")
    adj.add_argument("--dry-run", action="store_true")
    adj.add_argument("--no-vision", action="store_true")
    adj.add_argument("--redo", action="store_true",
                     help="a person sent this WRITTEN image back: apply their "
                          "--offset-*/--width-delta-pct and rewrite it (no vision "
                          "review, no adjustment cap; geometry still checked)")

    st = sub.add_parser("status", help="what is written / waiting / rejected")
    st.add_argument("--job")
    st.add_argument("--brief", action="store_true",
                    help="only the active run, last finish time and last 3 lines "
                         "(for polling a backgrounded run)")
    st.add_argument("--last-run", action="store_true",
                    help="print the saved final JSON of the last finished run")
    st.add_argument("--tail", type=int, default=20,
                    help="last N progress lines (0 = none)")

    args = ap.parse_args()
    if getattr(args, "no_vision", False):
        args.dry_run = True
    out = {"run": cmd_run, "adjust": cmd_adjust, "status": cmd_status}[args.cmd](args)
    print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
