# Cloud Drive Unified Download Orchestrator

> cloud-drive-downloader (cloud-drive-downloader) v0.20.1 · overseas-friendly lightweight layer. 中文版见 [README.md](README.md).

## What it is
A unified download scheduler with Agent/MCP/CLI, Web UI and browser-plugin entry points. It routes share links through official web sessions or official APIs, prefers browser-captured direct links, and never cracks login/pay/rate-limit/anti-bot/DRM.

## When to use it
Use when you need to download legally authorized files from cloud drives on macOS, Windows, or Linux, locally by default, or on a NAS/server via optional Docker.

## Quick start
```bash
bash scripts/pan.sh setup --mode local --root <download-dir> --port 17890
bash scripts/pan.sh get "<link>" --to <download-dir>
```

## Install across the three platforms
- **GitHub**: clone or download the repo, copy the skill folder into `$CODEX_HOME/skills/` (or `~/.claude/skills/` / your agent's skill directory).
- **SkillHub**: install the SkillHub lightweight package (text-only). The lightweight package removes platform-only launcher files (`.cmd`/`.ps1`, extensionless scripts and binary language models) and documents the Windows usage inside its own README; the GitHub full package keeps all platform launchers and assets.
- **ClawHub**: install the ClawHub full package, which keeps cross-platform launchers and assets.
- All platform packages serve the same canonical logic; platform copies never change the canonical code.

## Dependencies
Python 3; each drive engine may require its official CLI (AList/aria2/rclone) which setup checks; system credential store (Keychain/Credential Manager/secret-tool) for saved secrets.

## Privacy
Links and downloads stay on your machine; no cloud routing except the official sessions you authorize.

## Boundaries / limitations
You must ensure downloads are legal in your jurisdiction. The tool does not bypass limits, auth, or DRM.

## License
CC-BY-NC-SA-4.0

---

## Culture note
- `--lang en|zh` controls UI/help/JSON message language (default `zh`); business algorithms are identical in both languages.
- For image-ocr, `--lang` remains the OCR language; UI language is `--ui-lang en|zh`.
- Local Chinese templates and plant/concept dictionaries are NOT replaced; overseas inputs can select alternatives via parameters (e.g. `--plant-library`, `--project-rules`) so existing Chinese users are unaffected.
- Review flags, confidence tiers and evidence coordinates are language-independent fields.
