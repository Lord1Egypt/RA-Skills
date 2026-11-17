# Local CAD Reader & Evidence Extractor

> cad-file-reader (cad-file-reader) v0.41.3 · overseas-friendly lightweight layer. 中文版见 [README.md](README.md).

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
Local by default. Drawing bytes are not sent to cloud models, online OCR/conversion, or third parties without your explicit scope, byte count, and consent.

## Contract flow & ODA fallback (verified locally 2026-10-31)

- DWG/DXF is parsed **once** by cad-file-reader (`cad_scan`/`cad_contract`) into a `cad-file-reader/v0` contract; quantity/clash skills consume only the contract JSON and do not re-parse the drawing themselves. `CODEX_DIRECT`/`CAD_ALLOW_DIRECT` are not set by default (explicit escape hatch exists for regression/debug only).
- For the medical-university structure drawings `sample-struct-A.dwg` / `sample-struct-B.dwg` (review versions), the fixed path is: copy a working copy, convert it to DXF with `ODAFileConverter` on the copy only (never overwrite the original), then re-scan the copy DXF with `cad_scan --dwg-dxf-fallback --with-geom`. The converted DXF is a reproduction artifact, not authoritative original-bytes evidence.
- Verified replay: structure 2# texts=12054 / layers=356 / geometry_segments=37831 / sheets=22; structure 3# texts=13407 / layers=351 / geometry_segments=42002 / sheets=24. Working-copy DWG sha256 matched the originals; only the DXF copy was parsed.
- All outputs remain candidates with `final_quantity=false`; no final quantity or cost conclusions.

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
