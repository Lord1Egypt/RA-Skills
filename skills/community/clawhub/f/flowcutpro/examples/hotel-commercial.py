#!/usr/bin/env python3
"""
FlowCutPro — Hotel Commercial Example
8-shot luxury hotel commercial, 9:16 portrait, Veo 3

Usage:
  python3 hotel-commercial.py
  python3 hotel-commercial.py --dry-run
  python3 hotel-commercial.py --only-shots 3 5  # re-render misses
"""

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent / "scripts"))

import json, time, subprocess, argparse
from pathlib import Path
from datetime import datetime
import urllib.request, urllib.error, os

API_KEY  = os.environ.get("VEO_API_KEY", "AIzaSyDmN9-L3Y6q9fFIZY5OiH4E0_1t0wIbVjI")
API_BASE = "https://generativelanguage.googleapis.com/v1beta"
MODEL    = "veo-3.1-generate-preview"
OUT_DIR  = Path("~/clawd/output/flowcutpro/hotel-commercial").expanduser()
OUT_DIR.mkdir(parents=True, exist_ok=True)

SHOTS = [
    {
        "id": 1,
        "name": "exterior-arrival",
        "prompt": (
            "Cinematic vertical 9:16 portrait, slow push-in from street level. "
            "A sleek black luxury SUV pulls up to a stunning beachfront boutique hotel entrance. "
            "White Mediterranean stucco facade with terracotta and olive green architectural accents. "
            "Wood-framed glass entrance doors flanked by coconut palms. "
            "A uniformed doorman in crisp linen steps forward. "
            "Golden hour light. The ocean glints at the end of the street. "
            "Elegant. Unhurried. Aspirational."
        ),
        "duration_seconds": 8,
        "aspect_ratio": "9:16",
    },
    {
        "id": 2,
        "name": "lobby-checkin",
        "prompt": (
            "Cinematic vertical 9:16 portrait, medium tracking shot slowly forward. "
            "A boutique hotel lobby with creamy travertine limestone walls, "
            "sculptural concrete bust planters, warm amber Edison pendant lights. "
            "A staff attendant in linen uniform slides a key card across a marble reception desk "
            "to a woman in elegant resort wear. She smiles. "
            "Through the lobby's glass doors: the blue Caribbean. "
            "Mediterranean minimalist design. New and pristine. Warm. Intimate."
        ),
        "duration_seconds": 8,
        "aspect_ratio": "9:16",
    },
    {
        "id": 3,
        "name": "suite-reveal",
        "prompt": (
            "Cinematic vertical 9:16 portrait, door swings open in slow motion, "
            "camera slowly pushes into the suite. "
            "Art Deco mirrored accent wall with geometric angular panels and rose-gold trim. "
            "Crystal chandelier cascading from recessed tray ceiling. "
            "King bed in crisp white linens. Dusty teal velvet settee. "
            "Champagne in an ice bucket, crystal glasses. Rose petals on white duvet. "
            "Woman steps in and stops — breathless."
        ),
        "duration_seconds": 8,
        "aspect_ratio": "9:16",
    },
    {
        "id": 4,
        "name": "balcony-ocean",
        "prompt": (
            "Cinematic vertical 9:16 portrait, shot from inside through open French doors. "
            "Private hotel balcony. White railings. Two rattan chairs, marble side table. "
            "Beyond: the full arc of a Caribbean beachfront, turquoise sea, coconut palms. "
            "Curtains billow inward in the trade wind breeze. "
            "A woman stands at the railing, looking out. "
            "Golden afternoon light. She is completely at peace."
        ),
        "duration_seconds": 8,
        "aspect_ratio": "9:16",
    },
    {
        "id": 5,
        "name": "beach-loungers",
        "prompt": (
            "Cinematic vertical 9:16 portrait, slow dolly from sand level looking up. "
            "Private hotel beach, mid-afternoon. Two branded loungers with white hotel towels. "
            "A small service table between them: two frosted cocktails. "
            "A beach attendant in linen walks away having just delivered them. "
            "Turquoise Caribbean sea, white sand. A couple rests on the loungers. "
            "Coconut palms sway. Slow motion. Cinematic. Golden."
        ),
        "duration_seconds": 8,
        "aspect_ratio": "9:16",
    },
    {
        "id": 6,
        "name": "rooftop-pool",
        "prompt": (
            "Cinematic vertical 9:16 portrait, wide establishing shot from across the pool. "
            "Rooftop pool terrace at a boutique hotel. "
            "Geometric black-and-white hexagonal mosaic tile deck. "
            "Striped marble walls. Gray chaise lounges with brass frames. "
            "Pool turquoise and still — a woman floats on her back, eyes closed. "
            "Skyline and Caribbean beyond. Late afternoon golden light on the water. "
            "A waiter delivers a glass of prosecco poolside. Total silence implied."
        ),
        "duration_seconds": 8,
        "aspect_ratio": "9:16",
    },
    {
        "id": 7,
        "name": "rooftop-dinner",
        "prompt": (
            "Cinematic vertical 9:16 portrait, slow crane descend from above. "
            "Rooftop restaurant terrace at night. "
            "A small table for two: white linen, candlelight, wine glasses, a single orchid. "
            "String lights overhead. City skyline glitters below. Stars above. "
            "A couple leans in, talking quietly. A server silently refills their glasses. "
            "Film grain. Cinematic. Romantic."
        ),
        "duration_seconds": 8,
        "aspect_ratio": "9:16",
    },
    {
        "id": 8,
        "name": "morning-departure",
        "prompt": (
            "Cinematic vertical 9:16 portrait, slow push-in from behind. "
            "Early morning. A woman stands at the hotel entrance. "
            "A black car waits at the curb. Her luggage already loaded. "
            "She turns and looks back at the beautiful hotel over her shoulder. "
            "A slow smile. She turns back, walks to the car, gets in. "
            "The hotel facade glows in pre-dawn light. "
            "The ocean visible at the end of the block. Still. Beautiful."
        ),
        "duration_seconds": 8,
        "aspect_ratio": "9:16",
    },
]


def fire_shot(shot):
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
    req = urllib.request.Request(url, data=data, method="POST",
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            resp = json.loads(r.read())
        op = resp.get("name", "")
        if op:
            print(f"    → op: ...{op.split('/')[-1][-20:]}")
        return op
    except urllib.error.HTTPError as e:
        print(f"    HTTP {e.code}: {e.read().decode()[:200]}")
        return None
    except Exception as e:
        print(f"    Error: {e}")
        return None


def poll_op(op_name, timeout=600):
    url = f"{API_BASE}/{op_name}?key={API_KEY}"
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(urllib.request.Request(url), timeout=15) as r:
                resp = json.loads(r.read())
            if resp.get("done"):
                return resp
            print(f"    ...{int(time.time()-start)}s", end="\r")
        except Exception as e:
            print(f"    poll err: {e}")
        time.sleep(15)
    return None


def download(uri, out):
    sep = "&" if "?" in uri else "?"
    url = f"{uri}{sep}key={API_KEY}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url), timeout=120) as r:
            out.write_bytes(r.read())
        mb = out.stat().st_size / 1_048_576
        print(f"    ✅ {out.name} ({mb:.1f}MB)")
        return True
    except Exception as e:
        print(f"    ❌ {e}")
        return False


def get_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True)
    return float(r.stdout.strip())


def stitch(clips, ts):
    ordered = [clips[i] for i in sorted(clips.keys())]
    durations = [get_duration(c) for c in ordered]
    n, xfade = len(ordered), 0.5
    inputs = []
    for c in ordered:
        inputs += ["-i", str(c)]
    parts, offset, prev = [], 0.0, "[0:v]"
    for i in range(1, n):
        offset += durations[i-1] - xfade
        tag = f"[v{i}]" if i < n - 1 else "[vout]"
        parts.append(f"{prev}[{i}:v]xfade=transition=fade:duration={xfade}:offset={offset:.2f}{tag}")
        prev = f"[v{i}]"
    final = OUT_DIR / f"{ts}-hotel-commercial-FINAL-9x16.mp4"
    cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(parts),
           "-map", "[vout]", "-c:v", "libx264", "-crf", "18", "-preset", "slow",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(final)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("  ❌ ffmpeg:", r.stderr[-300:])
        return None
    dur = get_duration(final)
    mb = final.stat().st_size / 1_048_576
    print(f"  ✅ FINAL: {final.name} ({mb:.1f}MB, {dur:.1f}s)")
    return final


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--only-shots", nargs="*", type=int)
    args = parser.parse_args()

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    shots = [s for s in SHOTS if not args.only_shots or s["id"] in args.only_shots]

    print("=" * 60)
    print("FlowCutPro — Luxury Hotel Commercial")
    print(f"Veo 3 | 9:16 Portrait | {len(shots)} shots × 8s")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print("=" * 60)

    if args.dry_run:
        for s in shots:
            print(f"\n  Shot {s['id']}: {s['name']}")
            print(f"  {s['prompt'][:100]}...")
        return

    BATCH = 5
    clips = {}
    for batch_start in range(0, len(shots), BATCH):
        batch = shots[batch_start:batch_start + BATCH]
        print(f"\n── Batch: shots {[s['id'] for s in batch]} ──")
        operations = {}
        for shot in batch:
            print(f"  Shot {shot['id']}: {shot['name']}")
            op = fire_shot(shot)
            if op:
                operations[shot["id"]] = (shot, op)
        print(f"\n  Polling {len(operations)} ops...")
        for shot_id, (shot, op) in operations.items():
            print(f"\n  [shot-{shot_id}]")
            result = poll_op(op)
            if result:
                try:
                    uri = result["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
                    out = OUT_DIR / f"{ts}-shot{shot_id:02d}-{shot['name']}.mp4"
                    if download(uri, out):
                        clips[shot_id] = out
                except Exception as e:
                    print(f"  ❌ parse: {e}")
            else:
                print(f"  ❌ shot {shot_id} timeout")

    if len(clips) >= 2:
        print(f"\n── Stitching {len(clips)} clips ──")
        stitch(clips, ts)


if __name__ == "__main__":
    main()
