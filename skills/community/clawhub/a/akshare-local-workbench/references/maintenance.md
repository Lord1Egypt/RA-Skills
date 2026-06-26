# AKShare Local Workbench Standalone ClawHub Maintenance

## What This Skill Distributes

This standalone ClawHub package includes the full AKShare workbench application source under:

```text
assets/akshare-workbench
```

The controller copies that bundled source into a user-selected local project directory. It does not clone GitHub during normal use.

## Project Detection

The controller detects the app project by looking for:

- `backend/app/main.py`
- `backend/app/catalog/indicators.yaml`
- `frontend/package.json`

Detection order:

1. `--root /path/to/akshare-workbench`
2. `AKSHARE_WORKBENCH_ROOT`
3. current working directory and parents
4. `akshare-workbench` nested under those directories

## Install And Start

```bash
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py init-project --target akshare-workbench
cd akshare-workbench
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py setup
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py start
```

Use the installed skill script path in place of `/path/to/akshare-local-workbench`.

## Common Commands

```bash
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py doctor
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py setup
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py start
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py status
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py restart
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py test
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py clear-cache
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py stop
```

## Conservative Defaults

The controller sets these defaults unless the user already provided them:

- `AKSHARE_MAX_CONCURRENT=1`
- `AKSHARE_EASTMONEY_INTERVAL_SECONDS=12`
- `AKSHARE_EASTMONEY_HTTP_RETRIES=2`
- `AKSHARE_EASTMONEY_CALL_ATTEMPTS=1`
- `AKSHARE_EASTMONEY_CACHE_TTL_SECONDS=1800`
- `AKSHARE_RESULT_CACHE_TTL_SECONDS=900`
- `AKSHARE_ENRICH_NAMES=0`
- `AKSHARE_BACKEND_PORT=8000`
- `AKSHARE_FRONTEND_PORT=5173`

If Eastmoney rate-limits or disconnects, increase `AKSHARE_EASTMONEY_INTERVAL_SECONDS` before increasing retry counts.

## Catalog Maintenance

To add indicators, edit the copied app project:

- `backend/app/catalog/indicators.yaml`
- `backend/app/catalog/sectors.yaml`

Then run:

```bash
python3 /path/to/akshare-local-workbench/scripts/workbench_ctl.py test --root /path/to/akshare-workbench
```

Avoid adding broad full-market real-time endpoints when a targeted single-symbol endpoint exists.

## Security And Data Source Notes

- The app may store local AI configuration in `backend/app/config/ai_config.json`; do not commit or redistribute that file.
- Do not publish `.env`, API keys, cookies, proxy credentials, cache files, logs, generated virtual environments, or `node_modules`.
- This project is not financial advice.
- Users are responsible for complying with AKShare and upstream data provider terms.

## Licensing Note

The bundled workbench source includes its MIT license and disclaimer files. ClawHub may apply its own license handling to skill packages; keep the bundled app's `LICENSE` and `DISCLAIMER.md` with copied project files.
