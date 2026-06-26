from pathlib import Path
import subprocess


def run(input_text: str):
    script = Path(__file__).with_name("skill.js")
    proc = subprocess.run(
        ["node", str(script), input_text or ""],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        return f"Skill JS failed: {err}"
    return (proc.stdout or "").strip()
