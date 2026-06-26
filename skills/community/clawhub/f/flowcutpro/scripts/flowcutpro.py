#!/usr/bin/env python3
"""
FlowCutPro — AI Cinematic Video Production
Powered by Google Veo 3 + OpenClaw LLM brain

Usage:
  python3 flowcutpro.py --concept "luxury hotel sunset arrival" --shots 6 --aspect-ratio 9:16
  python3 flowcutpro.py --concept "..." --dry-run
  python3 flowcutpro.py --concept "..." --shots 8 --only-shots 3 5  # re-render misses
"""

import sys, os, json, time, argparse, subprocess, textwrap
from pathlib import Path
from datetime import datetime

# ─── CONFIG ───────────────────────────────────────────────────────────────────

API_KEY  = os.environ.get("VEO_API_KEY", "AIzaSyDmN9-L3Y6q9fFIZY5OiH4E0_1t0wIbVjI")
API_BASE = "https://generativelanguage.googleapis.com/v1beta"
MODEL    = "veo-3.1-generate-preview"

DEFAULT_ASPECT   = "9:16"
DEFAULT_DURATION = 8
DEFAULT_SHOTS    = 5
BATCH_SIZE       = 5       # Veo concurrent limit
POLL_INTERVAL    = 15      # seconds
SHOT_TIMEOUT     = 600     # 10 min per shot max
MAX_RETRIES      = 2

# ─── IMPORTS (stdlib only — no pip required) ──────────────────────────────────
import urllib.request
import urllib.error


# ─── LLM SHOT PLANNER ─────────────────────────────────────────────────────────

def plan_shots(concept: str, n_shots: int, aspect: str, duration: int) -> list[dict]:
    """
    Use OpenClaw's configured LLM to break a concept into N cinematic shots.
    Falls back to a simple single-shot plan if LLM is unavailable.
    """
    orientation = "vertical 9:16 portrait" if aspect == "9:16" else \
                  "horizontal 16:9 widescreen" if aspect == "16:9" else "square 1:1"

    system_prompt = textwrap.dedent(f"""
        You are a professional cinematographer and creative director. Your job is to
        break a video concept into individual cinematic shots optimized for Google Veo 3.

        Rules:
        1. Each shot is {duration} seconds long.
        2. Format: {orientation}
        3. Each shot prompt must:
           - Start with: "Cinematic {orientation}, [camera movement]."
           - Describe the exact scene, subject, environment, and lighting
           - Name a specific camera move (slow push-in, static wide, crane descent, dolly, tracking)
           - Specify lighting (golden hour, blue hour, candlelit, harsh noon, overcast)
           - End with 2-3 aesthetic/mood words (e.g. "Cinematic. Warm. Intimate.")
        4. Maintain visual style consistency across all shots (same color palette, same mood)
        5. Build narrative arc: establish → develop → climax → resolve
        6. NO text overlays, NO logos, NO graphics in prompts

        Return ONLY a JSON array of shot objects:
        [
          {{
            "id": 1,
            "name": "slug-for-filename",
            "prompt": "Full cinematic prompt...",
            "duration_seconds": {duration},
            "aspect_ratio": "{aspect}"
          }},
          ...
        ]
        Return nothing else. Pure JSON.
    """).strip()

    user_prompt = f"Create {n_shots} cinematic shots for this concept:\n\n{concept}"

    # Try OpenClaw's Anthropic SDK integration
    try:
        import anthropic
        client = anthropic.Anthropic()
        msg = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        raw = msg.content[0].text.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        shots = json.loads(raw.strip())
        print(f"  ✅ LLM planned {len(shots)} shots")
        return shots
    except Exception as e:
        print(f"  ⚠️  LLM unavailable ({e}), using concept as single prompt")
        # Fallback: treat concept as one shot prompt per shot
        return [
            {
                "id": i + 1,
                "name": f"shot-{i+1:02d}",
                "prompt": (
                    f"Cinematic {orientation}, slow push-in. "
                    f"{concept}. Shot {i+1} of {n_shots}. "
                    f"Photorealistic. Cinematic. Beautiful."
                ),
                "duration_seconds": duration,
                "aspect_ratio": aspect,
            }
            for i in range(n_shots)
        ]


# ─── VEO 3 API ────────────────────────────────────────────────────────────────

def fire_shot(shot: dict) -> str | None:
    """Submit a shot to Veo 3. Returns operation name or None."""
    url = f"{API_BASE}/models/{MODEL}:predictLongRunning?key={API_KEY}"
    payload = {
        "instances": [{"prompt": shot["prompt"]}],
        "parameters": {
            "aspectRatio": shot["aspect_ratio"],
            "durationSeconds": shot["duration_seconds"],
            "sampleCount": 1,
        }
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=data, method="POST",
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            resp = json.loads(r.read())
        op = resp.get("name", "")
        if op:
            print(f"    → op: ...{op.split('/')[-1][-20:]}")
        return op
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"    HTTP {e.code}: {body[:200]}")
        return None
    except Exception as e:
        print(f"    Error: {e}")
        return None


def poll_op(op_name: str, timeout: int = SHOT_TIMEOUT) -> dict | None:
    """Poll a long-running operation until done or timeout."""
    url = f"{API_BASE}/{op_name}?key={API_KEY}"
    start = time.time()
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=15) as r:
                resp = json.loads(r.read())
            if resp.get("done"):
                return resp
            elapsed = int(time.time() - start)
            print(f"    ...{elapsed}s", end="\r")
        except Exception as e:
            print(f"    poll err: {e}")
        time.sleep(POLL_INTERVAL)
    print(f"    ⏱ timeout after {timeout}s")
    return None


def download_clip(uri: str, out: Path) -> bool:
    """Download a Veo output video to disk."""
    # Handle URL parameter correctly
    sep = "&" if "?" in uri else "?"
    url = f"{uri}{sep}key={API_KEY}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=120) as r:
            out.write_bytes(r.read())
        mb = out.stat().st_size / 1_048_576
        print(f"    ✅ {out.name} ({mb:.1f}MB)")
        return True
    except Exception as e:
        print(f"    ❌ download failed: {e}")
        return False


def render_shot(shot: dict, out_dir: Path, ts: str, retry: int = 0) -> Path | None:
    """Render one shot with retry logic."""
    name = shot.get("name", f"shot-{shot['id']:02d}")
    out = out_dir / f"{ts}-shot{shot['id']:02d}-{name}.mp4"

    # Skip if already exists
    if out.exists():
        print(f"  ✓ shot {shot['id']} already exists, skipping")
        return out

    for attempt in range(retry + 1):
        if attempt > 0:
            print(f"  ↩ retry {attempt}/{retry} for shot {shot['id']}")
        op = fire_shot(shot)
        if not op:
            continue
        result = poll_op(op)
        if not result:
            continue
        try:
            uri = result["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
            if download_clip(uri, out):
                return out
        except Exception as e:
            print(f"  ❌ parse error: {e}")
            print(f"     resp snippet: {str(result)[:200]}")
    return None


# ─── FFMPEG STITCH ────────────────────────────────────────────────────────────

def get_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True
    )
    return float(r.stdout.strip())


def stitch_clips(clips: dict, out_dir: Path, ts: str) -> Path | None:
    """Stitch ordered clips with xfade crossfades into a final video."""
    ordered = [clips[i] for i in sorted(clips.keys())]
    if len(ordered) < 2:
        print("  ⚠️  Need at least 2 clips to stitch")
        return ordered[0] if ordered else None

    durations = [get_duration(c) for c in ordered]
    total = sum(durations) - 0.5 * (len(ordered) - 1)
    print(f"  Clips: {len(ordered)} | Total: {total:.1f}s")

    n = len(ordered)
    xfade = 0.5
    inputs = []
    for c in ordered:
        inputs += ["-i", str(c)]

    # Build xfade filter chain
    parts = []
    offset = 0.0
    prev = "[0:v]"
    for i in range(1, n):
        offset += durations[i - 1] - xfade
        tag = f"[v{i}]" if i < n - 1 else "[vout]"
        parts.append(
            f"{prev}[{i}:v]xfade=transition=fade:duration={xfade}:offset={offset:.2f}{tag}"
        )
        prev = f"[v{i}]"

    aspect = clips[sorted(clips.keys())[0]].stem
    # Detect aspect from first clip
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "quiet", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=p=0",
             str(ordered[0])],
            capture_output=True, text=True
        )
        w, h = r.stdout.strip().split(",")
        suffix = "9x16" if int(h) > int(w) else "16x9" if int(w) > int(h) else "1x1"
    except Exception:
        suffix = "output"

    final = out_dir / f"{ts}-FINAL-{suffix}.mp4"
    cmd = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", ";".join(parts),
        "-map", "[vout]",
        "-c:v", "libx264", "-crf", "18", "-preset", "slow",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        str(final)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("  ❌ ffmpeg error:", result.stderr[-400:])
        return None
    dur = get_duration(final)
    mb = final.stat().st_size / 1_048_576
    print(f"  ✅ FINAL: {final.name} ({mb:.1f}MB, {dur:.1f}s)")
    return final


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="FlowCutPro — AI cinematic video production with Veo 3"
    )
    parser.add_argument("--concept", required=True, help="Video concept or brief")
    parser.add_argument("--shots", type=int, default=DEFAULT_SHOTS, help="Number of shots")
    parser.add_argument("--aspect-ratio", default=DEFAULT_ASPECT,
                        choices=["9:16", "16:9", "1:1"], help="Video aspect ratio")
    parser.add_argument("--duration", type=int, default=DEFAULT_DURATION,
                        help="Seconds per shot (5-8)")
    parser.add_argument("--output-dir", default="~/clawd/output/flowcutpro/",
                        help="Output directory")
    parser.add_argument("--only-shots", nargs="*", type=int,
                        help="Only render these shot IDs (re-render misses)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Plan shots without rendering")
    parser.add_argument("--retries", type=int, default=MAX_RETRIES,
                        help="Max retries per failed shot")
    args = parser.parse_args()

    out_dir = Path(args.output_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")

    print("=" * 64)
    print("FlowCutPro — AI Cinematic Video Production")
    print(f"Concept: {args.concept[:80]}")
    print(f"Shots: {args.shots} × {args.duration}s | Aspect: {args.aspect_ratio}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE RENDER'}")
    print(f"Output: {out_dir}")
    print("=" * 64)

    # Plan shots
    print("\n── Shot Planning ──")
    shots = plan_shots(args.concept, args.shots, args.aspect_ratio, args.duration)

    # Filter if --only-shots provided
    if args.only_shots:
        shots = [s for s in shots if s["id"] in args.only_shots]
        print(f"  Rendering only shots: {args.only_shots}")

    if args.dry_run:
        print("\n── Shot Plan (dry run) ──")
        for s in shots:
            print(f"\n  Shot {s['id']}: {s['name']}")
            wrapped = textwrap.fill(s['prompt'], width=72, initial_indent="    ",
                                    subsequent_indent="    ")
            print(wrapped)
        print(f"\n  Total: {len(shots)} shots × {args.duration}s = {len(shots)*args.duration}s")
        return

    # Render in batches of BATCH_SIZE
    clips = {}
    for batch_start in range(0, len(shots), BATCH_SIZE):
        batch = shots[batch_start:batch_start + BATCH_SIZE]
        print(f"\n── Batch: shots {[s['id'] for s in batch]} ──")

        # Fire all shots in batch simultaneously
        operations = {}
        for shot in batch:
            print(f"  Shot {shot['id']}: {shot['name']}")
            op = fire_shot(shot)
            if op:
                operations[shot["id"]] = (shot, op)

        if not operations:
            print("  No operations submitted.")
            continue

        # Poll all ops
        print(f"\n  Polling {len(operations)} operations...")
        for shot_id, (shot, op) in operations.items():
            print(f"\n  [shot-{shot_id}] polling...")
            result = poll_op(op)
            if result:
                try:
                    uri = result["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
                    name = shot.get("name", f"shot-{shot_id:02d}")
                    out = out_dir / f"{ts}-shot{shot_id:02d}-{name}.mp4"
                    if download_clip(uri, out):
                        clips[shot_id] = out
                    else:
                        # Retry
                        for retry_n in range(1, args.retries + 1):
                            print(f"  ↩ retry {retry_n}/{args.retries} for shot {shot_id}")
                            op2 = fire_shot(shot)
                            if not op2:
                                continue
                            result2 = poll_op(op2)
                            if result2:
                                try:
                                    uri2 = result2["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
                                    if download_clip(uri2, out):
                                        clips[shot_id] = out
                                        break
                                except Exception:
                                    pass
                except Exception as e:
                    print(f"  ❌ parse error: {e}")
                    print(f"     resp: {str(result)[:200]}")
            else:
                print(f"  ❌ shot {shot_id} timed out")

    # Stitch
    if len(clips) >= 2:
        print(f"\n── Stitching {len(clips)}/{len(shots)} clips ──")
        final = stitch_clips(clips, out_dir, ts)
        if final:
            print(f"\n{'='*64}")
            print(f"Complete. {len(clips)}/{len(shots)} shots rendered.")
            for sid in sorted(clips.keys()):
                print(f"  shot {sid:02d}: {clips[sid].name}")
            print(f"\n  MASTER: {final}")
            print(f"{'='*64}")
    elif len(clips) == 1:
        sid = list(clips.keys())[0]
        print(f"\n  Single clip rendered: {clips[sid]}")
    else:
        print("\n  ❌ No clips rendered successfully.")


if __name__ == "__main__":
    main()
