# Local CAD Reader & Evidence Extractor

> cad-file-reader (cad-file-reader) v0.34.0 · overseas-friendly lightweight layer. 中文版见 [README.md](README.md).

## What it is
A local AutoCAD reader that extracts DWG/DXF/DWT and PDF content from construction drawings without needing AutoCAD. It reads layers, text, blocks, title frames, geometry, and landscape legend candidates, and returns them with source evidence, coordinates and review flags.

## When to use it
Use when you receive a DWG/DXF/PDF drawing and need its text, layers, block lists, geometry candidates, MEP topology, or length/area/volume measurement candidates. It outputs read-only candidates (final_quantity=false) for review — it is not a calculator for final bills of quantities, materials, cost or settlement.

## Quick start
```bash
bash scripts/doctor.sh            # environment health check (read-only)
python3 scripts/read_cad.py drawing.dwg --json
python3 scripts/cad_scan.py drawing.dwg --format json -o drawing.scan
```

## Install across the three platforms
- **GitHub**: clone or download the repo, copy the skill folder into `$CODEX_HOME/skills/` (or `~/.claude/skills/` / your agent's skill directory), then run `bash scripts/setup.sh` (idempotent).
- **SkillHub**: install the SkillHub lightweight package (text-only). The lightweight package removes platform-only launcher files (`.cmd`/`.ps1`, extensionless scripts and binary language models) and documents the Windows usage inside its own README; the GitHub full package keeps all platform launchers and assets.
- **Windows**: full package: `powershell -ExecutionPolicy Bypass -File scripts\setup_windows.ps1`; lightweight package (text-only, no `.cmd`/`.ps1`): `python scripts/setup_win.py` (add `--dry-run` to inspect first).
- **lis-skill-bus (recommended, optional)**: install the lis-skill-bus skill first (SkillHub slug: `lis-skill-bus`; GitHub: `lisong2003-lgtm/lis-skill-bus`), then run `python install_py.py --apply`. Without it, cad-file-reader auto-degrades to `$HOME/.codex/skills/.skillbus/state.json` and the five qto skills remain usable.
- **ClawHub**: install the ClawHub full package, which keeps cross-platform launchers and assets.
- All platform packages serve the same canonical logic; platform copies never change the canonical code.

## Dependencies
Python 3; supported DWG parsing uses public PyPI packages (ezdwg/ezdxf/fonttools/pyparsing/numpy) that `scripts/ensure_runtime.sh` installs on first run (SHA-256 verified when fetched via GitHub Release). PDF paths use local OCR/vector extraction. `bash scripts/deps_check.sh --minimal` shows what is missing.

## Privacy
Fully local; drawing bytes never leave your machine. No cloud OCR, no uploads.

## Boundaries / limitations
- The skill returns review candidates, not final quantities or legal/engineering sign-off.
- Large drawings above the entrance gate (default 40 MB) are normally parsed with the low-memory scanner; full-parse options are available but watch memory.
- `-` English output is a lightweight layer: help, JSON status/message/error and this README are localized; some deep report labels and stored Chinese data remain as-is.

## License
CC-BY-NC-SA-4.0

---

## Culture note
- CLI interfaces accept `--lang en|zh` (default `zh`): `--lang en --help` shows English help; Chinese behaviour stays unchanged.
- Primary reader `scripts/read_cad.py` and health check `scripts/doctor.py` are localized; specialized geometry scripts may still print Chinese detail labels.
- Review flags, confidence tiers and evidence coordinates are language-independent fields.
