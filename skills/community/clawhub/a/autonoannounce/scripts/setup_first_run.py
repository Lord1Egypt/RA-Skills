#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CFG = ROOT / "config" / "tts-queue.json"
SCRIPTS = ROOT / "skills" / "autonoannounce" / "scripts"


def detect_backend() -> str:
    script = SCRIPTS / "backend-detect.sh"
    try:
        out = subprocess.check_output([str(script)], text=True).strip()
        return out or "auto"
    except Exception:
        return "auto"


def probe_devices(backend: str) -> list[str]:
    script = SCRIPTS / "playback-probe.sh"
    try:
        out = subprocess.check_output([str(script), backend], text=True)
    except Exception:
        return []
    devices = []
    for line in out.splitlines():
        if line.startswith("device:"):
            devices.append(line.split(":", 1)[1])
    return devices


def prompt(msg: str, default: str) -> str:
    v = input(f"{msg} [{default}]: ").strip()
    return v or default


def atomic_write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False) as tf:
        json.dump(data, tf, indent=2)
        tf.write("\n")
        tmp = Path(tf.name)
    os.replace(tmp, path)


def main():
    p = argparse.ArgumentParser(description="autonoannounce first run setup")
    p.add_argument("--noninteractive", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--earcons", choices=["y", "n"], default=None)
    p.add_argument("--style", default=None)
    p.add_argument("--voice-id", default=os.environ.get("ELEVENLABS_VOICE_ID", ""))
    p.add_argument("--backend", default=None)
    p.add_argument("--device", default="")
    p.add_argument("--generate-starters", choices=["y", "n"], default=None)
    p.add_argument("--run-playback-test", choices=["y", "n"], default=None)
    args = p.parse_args()

    backend_default = detect_backend()
    earcons = args.earcons
    style = args.style
    voice_id = args.voice_id
    backend = args.backend
    device = args.device
    generate = args.generate_starters
    run_test = args.run_playback_test

    if not args.noninteractive:
        print("== autonoannounce first run setup (python) ==")
        earcons = earcons or prompt("Enable earcons? (y/n)", "y")
        style = style or prompt("Earcon style direction", "subtle chime")
        if not voice_id:
            has = prompt("Do you already have an ElevenLabs voice ID? (y/n)", "n")
            if has.lower().startswith("y"):
                voice_id = input("Enter voice ID: ").strip()
        backend = backend or prompt("Playback backend", backend_default)

        if not device:
            devices = probe_devices(backend)
            if devices:
                print(f"Detected playback devices for {backend}:")
                for i, d in enumerate(devices, start=1):
                    print(f"  {i}) {d}")
                idx = input("Choose device number (or press enter for default): ").strip()
                if idx.isdigit() and 1 <= int(idx) <= len(devices):
                    device = devices[int(idx) - 1]

        run_test = run_test or prompt("Run playback test tone now? (y/n)", "y")
        if run_test.lower().startswith("y"):
            cmd = [str(SCRIPTS / "playback-test.sh"), "--backend", backend]
            if device:
                cmd += ["--device", device]
            subprocess.call(cmd)
            heard = prompt("Did you hear it? (y/n)", "y")
            if not heard.lower().startswith("y"):
                print("Tip: rerun setup and choose a different backend/device.")

        if earcons.lower().startswith("y"):
            generate = generate or prompt("Generate starter earcons now? (y/n)", "y")
    else:
        earcons = earcons or "y"
        style = style or "subtle chime"
        backend = backend or backend_default
        run_test = run_test or "n"
        if earcons.lower().startswith("y"):
            generate = generate or "n"
        else:
            generate = "n"

    cfg = {
        "queueFile": str(ROOT / ".openclaw" / "tts-queue.jsonl"),
        "lockFile": str(ROOT / ".openclaw" / "tts-queue.lock"),
        "logFile": str(ROOT / ".openclaw" / "tts-queue.log"),
        "voice": {
            "voiceId": voice_id,
            "modelId": os.environ.get("ELEVENLABS_MODEL_ID", "eleven_turbo_v2_5"),
        },
        "earcons": {
            "enabled": earcons.lower().startswith("y"),
            "style": style,
            "categories": {"start": "", "end": "", "update": "", "important": "", "error": ""},
            "libraryPath": str(ROOT / ".openclaw" / "earcon-library.json"),
        },
        "playback": {"backend": backend, "device": device},
    }

    if args.dry_run:
        print(json.dumps(cfg, indent=2))
        return 0

    atomic_write_json(CFG, cfg)
    print(f"Wrote {CFG}")
    print("Next: run skills/autonoannounce/scripts/elevenlabs-preflight.sh")

    if cfg["earcons"]["enabled"] and generate and generate.lower().startswith("y"):
        gen_script = SCRIPTS / "earcon-library.sh"
        for cat in ["start", "end", "update", "important", "error"]:
            subprocess.call([str(gen_script), "generate", cat, f"{style} {cat} notification sound", "1"])
        print("Starter earcons generated (where API/key permits).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
