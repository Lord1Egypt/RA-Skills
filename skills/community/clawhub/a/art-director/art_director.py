#!/usr/bin/env python3
"""
Art Director — ClawHub Skill

Generates on-aesthetic images for brands telling stories with images.
Wraps nano-banana-pro (Gemini) for the underlying generation, adds two layers
on top:

  1. A persistent brand aesthetic loaded from aesthetic.md (set once by the
     operator, stable across every call).
  2. Per-image art-direction thinking applied by the calling agent using
     the guidance in SKILL.md.

The mechanical execution lives here. The editorial thinking that turns a
topic into a proper brief happens in the calling agent, guided by SKILL.md.

Commands:
  install --preset <name>              copy a preset to ./aesthetic.md
  generate --brief "..." --output ...  generate one image
  batch --briefs <file> --outdir ...   generate one image per line in briefs file
  check-nano                           verify nano-banana-pro is installed

See SKILL.md for how to construct a brief.
"""

import sys
import os
import argparse
import subprocess
import shutil
from datetime import datetime
from pathlib import Path


# ── Config ────────────────────────────────────────────────────────────────────

SKILL_DIR = Path(__file__).resolve().parent
PRESETS_DIR = SKILL_DIR / "presets"
TEMPLATE_PATH = SKILL_DIR / "aesthetic.md"

DEFAULT_RESOLUTION = "2K"
DEFAULT_OUTPUT_DIR = os.environ.get("OUTPUT_DIR", ".")
AESTHETIC_PATH = os.environ.get("AESTHETIC_PATH", "aesthetic.md")

# Candidate locations for the nano-banana-pro generate script. Overridable
# via NANO_BANANA_SCRIPT. Checked in order; first match wins.
NANO_BANANA_CANDIDATES = [
    os.environ.get("NANO_BANANA_SCRIPT", ""),
    "/usr/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py",
    "/usr/local/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py",
    str(Path.home() / ".openclaw" / "skills" / "nano-banana-pro" / "scripts" / "generate_image.py"),
    str(Path.home() / ".openclaw" / "clawhub-skills" / "nano-banana-pro" / "scripts" / "generate_image.py"),
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def find_nano_banana():
    """Locate the nano-banana-pro generate script. Returns path or None."""
    for candidate in NANO_BANANA_CANDIDATES:
        if candidate and Path(candidate).exists():
            return candidate

    # Last resort: shell out to find (Unix) or where (Windows)
    try:
        if sys.platform == "win32":
            # Windows: try a recursive search under common roots
            for root in [
                Path.home() / ".openclaw",
                Path("C:/Program Files/nodejs/node_modules"),
            ]:
                if root.exists():
                    matches = list(root.rglob("nano-banana*/scripts/generate_image.py"))
                    if matches:
                        return str(matches[0])
        else:
            result = subprocess.run(
                ["find", "/usr", str(Path.home() / ".openclaw"),
                 "-name", "generate_image.py", "-path", "*/nano-banana*"],
                capture_output=True, text=True, timeout=5,
            )
            candidates = [c for c in result.stdout.strip().split("\n") if c]
            if candidates:
                return candidates[0]
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def load_aesthetic(path=None):
    """Load the brand aesthetic file. Returns its body as a prompt preamble, or
    empty string if not found."""
    aesthetic_file = Path(path or AESTHETIC_PATH)
    if not aesthetic_file.exists():
        return ""
    raw = aesthetic_file.read_text(encoding="utf-8")
    # Strip HTML comments (operator guidance not meant for the model)
    import re
    stripped = re.sub(r"<!--.*?-->", "", raw, flags=re.DOTALL)
    # Collapse whitespace runs
    stripped = re.sub(r"\n{3,}", "\n\n", stripped).strip()
    return stripped


def compose_prompt(aesthetic_text, brief):
    """Merge brand aesthetic + per-image brief into a single prompt."""
    brief = brief.strip()

    # Always enforce technical specs
    additions = []
    if "16:9" not in brief and "aspect ratio" not in brief.lower():
        additions.append("16:9 aspect ratio")
    if "no text" not in brief.lower() and "no embedded text" not in brief.lower():
        additions.append("no embedded text or typography")
    if additions:
        brief = brief.rstrip(" ,") + ", " + ", ".join(additions)

    if not aesthetic_text:
        return brief

    # Aesthetic first (establishes the brand frame), brief second (this image's specifics)
    return f"{aesthetic_text}\n\n---\n\nImage brief: {brief}"


def available_presets():
    """List preset names (stems) available for install."""
    if not PRESETS_DIR.exists():
        return []
    return sorted(
        p.stem for p in PRESETS_DIR.glob("*.md")
        if p.name != "README.md"
    )


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_install(args):
    """Copy a preset (or the blank template) to ./aesthetic.md."""
    target = Path(args.target or "aesthetic.md")

    if target.exists() and not args.force:
        print(f"ERROR: {target} already exists. Use --force to overwrite.", file=sys.stderr)
        sys.exit(1)

    if args.preset == "blank":
        source = TEMPLATE_PATH
        label = "blank template"
    else:
        source = PRESETS_DIR / f"{args.preset}.md"
        label = f"preset: {args.preset}"
        if not source.exists():
            presets = available_presets()
            print(f"ERROR: preset '{args.preset}' not found.", file=sys.stderr)
            print(f"  Available: blank, {', '.join(presets)}", file=sys.stderr)
            sys.exit(1)

    shutil.copyfile(source, target)
    print(f"[OK] Installed {label} to: {target}")
    print()
    print("Next steps:")
    print(f"  1. Open {target} and edit to reflect your brand.")
    print(f"  2. Generate a test batch to see how it reads:")
    print(f"     python3 art_director.py batch --briefs briefs.txt --outdir ./iteration-01/")
    print(f"  3. Tune the aesthetic, regenerate, repeat until it looks like you.")


def cmd_generate(args):
    """Generate a single image from a brief, merged with the brand aesthetic."""
    script = find_nano_banana()
    if not script:
        print("ERROR: nano-banana-pro skill not found.", file=sys.stderr)
        print("  Install it first: openclaw skill install nano-banana-pro", file=sys.stderr)
        print("  Or set NANO_BANANA_SCRIPT to the full path of generate_image.py", file=sys.stderr)
        sys.exit(1)

    # Resolve output path
    output_filename = args.output
    if not output_filename:
        output_filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".png"

    output_path = Path(output_filename)
    if not output_path.is_absolute() and str(output_path) == output_path.name:
        output_path = Path(DEFAULT_OUTPUT_DIR) / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Build the composed prompt
    aesthetic = load_aesthetic(args.aesthetic)
    prompt = compose_prompt(aesthetic, args.brief)

    resolution = args.resolution or DEFAULT_RESOLUTION

    print(f"Generating image...")
    print(f"  Resolution:  {resolution}")
    print(f"  Output:      {output_path}")
    if aesthetic:
        aesthetic_source = args.aesthetic or AESTHETIC_PATH
        print(f"  Aesthetic:   loaded from {aesthetic_source}")
    else:
        print(f"  Aesthetic:   none (no aesthetic.md found -- using brief only)")
    print(f"  Brief:       {args.brief[:100]}{'...' if len(args.brief) > 100 else ''}")
    print()

    cmd = [
        "uv", "run", script,
        "--prompt", prompt,
        "--filename", str(output_path),
        "--resolution", resolution,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("Generation failed:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)

    if result.stdout:
        print(result.stdout)
    print(f"[OK] Image saved: {output_path}")


def cmd_batch(args):
    """Generate one image per line in a briefs file. For the iteration loop."""
    briefs_file = Path(args.briefs)
    if not briefs_file.exists():
        print(f"ERROR: briefs file not found: {briefs_file}", file=sys.stderr)
        sys.exit(1)

    briefs = [
        line.strip() for line in briefs_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not briefs:
        print(f"ERROR: no briefs found in {briefs_file}", file=sys.stderr)
        sys.exit(1)

    outdir = Path(args.outdir or "./batch")
    outdir.mkdir(parents=True, exist_ok=True)

    script = find_nano_banana()
    if not script:
        print("ERROR: nano-banana-pro skill not found.", file=sys.stderr)
        sys.exit(1)

    aesthetic = load_aesthetic(args.aesthetic)
    resolution = args.resolution or DEFAULT_RESOLUTION

    print(f"Batch generating {len(briefs)} image(s) -> {outdir}")
    if aesthetic:
        aesthetic_source = args.aesthetic or AESTHETIC_PATH
        print(f"Aesthetic loaded from: {aesthetic_source}")
    else:
        print("No aesthetic.md found -- briefs will be used alone.")
    print()

    failures = []
    for i, brief in enumerate(briefs, start=1):
        output_path = outdir / f"{i:02d}.png"
        prompt = compose_prompt(aesthetic, brief)

        print(f"[{i}/{len(briefs)}] {brief[:80]}{'...' if len(brief) > 80 else ''}")

        cmd = [
            "uv", "run", script,
            "--prompt", prompt,
            "--filename", str(output_path),
            "--resolution", resolution,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"  [ERR] failed: {result.stderr.strip().splitlines()[-1] if result.stderr else 'unknown error'}")
            failures.append((i, brief))
        else:
            print(f"  [OK] saved:   {output_path}")

    print()
    print(f"Batch complete: {len(briefs) - len(failures)}/{len(briefs)} succeeded")
    if failures:
        print(f"  Failures: {', '.join(str(i) for i, _ in failures)}")
    print()
    print("Next step: review the batch side by side. What feels on-brand?")
    print("What doesn't? Tune aesthetic.md, regenerate.")


def cmd_check_nano(args):
    """Report the full setup status before exiting. Checks every dependency
    even if earlier ones are missing, so the operator sees the complete picture
    in one run."""
    problems = []

    script = find_nano_banana()
    if script:
        print(f"[OK] nano-banana-pro found at: {script}")
    else:
        print("[ERR] nano-banana-pro not found.")
        print("      Install it: openclaw skill install nano-banana-pro")
        print("      Or set NANO_BANANA_SCRIPT to an explicit path.")
        problems.append("nano-banana-pro")

    if shutil.which("uv"):
        print("[OK] uv is available")
    else:
        print("[ERR] uv not found -- install: curl -LsSf https://astral.sh/uv/install.sh | sh")
        problems.append("uv")

    aesthetic = load_aesthetic()
    if aesthetic:
        print(f"[OK] aesthetic.md found ({len(aesthetic)} chars)")
    else:
        print("[i]  no aesthetic.md in current directory")
        presets = available_presets()
        print(f"     To install one: python3 art_director.py install --preset <{'|'.join(presets)}>")

    if os.environ.get("GEMINI_API_KEY"):
        print("[OK] GEMINI_API_KEY is set")
    else:
        print("[i]  GEMINI_API_KEY not set in environment")
        print("     (nano-banana-pro needs this; image generation will fail without it)")

    print()
    if problems:
        print(f"Art Director is NOT ready. Missing: {', '.join(problems)}")
        sys.exit(1)
    else:
        print("Art Director is ready.")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        description="Art Director -- on-aesthetic image generation for brand storytelling"
    )
    sub = p.add_subparsers(dest="command", required=True)

    # install
    presets = available_presets()
    preset_choices = ["blank"] + presets
    inst = sub.add_parser("install", help="Copy a preset (or blank template) to ./aesthetic.md")
    inst.add_argument("--preset", required=True, choices=preset_choices,
                      help=f"Which preset to install. One of: {', '.join(preset_choices)}")
    inst.add_argument("--target", default="",
                      help="Target path (default: ./aesthetic.md)")
    inst.add_argument("--force", action="store_true",
                      help="Overwrite existing aesthetic.md")

    # generate
    gen = sub.add_parser("generate", help="Generate one image from a brief")
    gen.add_argument("--brief", required=True,
                     help="The per-image art-directed brief (see SKILL.md for how to construct one)")
    gen.add_argument("--output", default="",
                     help="Output filename or path. Defaults to timestamped file in OUTPUT_DIR.")
    gen.add_argument("--aesthetic", default="",
                     help="Path to aesthetic.md (default: $AESTHETIC_PATH or ./aesthetic.md)")
    gen.add_argument("--resolution", default=DEFAULT_RESOLUTION,
                     choices=["1K", "2K", "4K"],
                     help="Image resolution. 1K=draft, 2K=standard (default), 4K=hi-res final")

    # batch
    batch = sub.add_parser("batch", help="Generate one image per brief in a file (for iteration)")
    batch.add_argument("--briefs", required=True,
                       help="Text file, one brief per line (# comments and blank lines ignored)")
    batch.add_argument("--outdir", default="./batch",
                       help="Directory for generated images (default: ./batch)")
    batch.add_argument("--aesthetic", default="",
                       help="Path to aesthetic.md (default: $AESTHETIC_PATH or ./aesthetic.md)")
    batch.add_argument("--resolution", default=DEFAULT_RESOLUTION,
                       choices=["1K", "2K", "4K"],
                       help="Image resolution")

    # check
    sub.add_parser("check-nano", help="Verify nano-banana-pro and aesthetic.md are in place")

    args = p.parse_args()
    {
        "install": cmd_install,
        "generate": cmd_generate,
        "batch": cmd_batch,
        "check-nano": cmd_check_nano,
    }[args.command](args)


if __name__ == "__main__":
    main()
