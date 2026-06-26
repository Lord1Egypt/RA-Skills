# Setup

## Runtime requirements

- Python 3.10 or newer.
- Google Chrome or Chromium installed locally.
- Network access to https://www.cde.org.cn.

## Install on Windows

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\scripts\requirements.txt
```

If `python` is not on `PATH`, OpenClaw can usually use `py` instead. The skill metadata only gates on a Python launcher being available. Chrome itself does not need to be on `PATH`, but Selenium must be able to launch it on the local machine.

## Install on Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r ./scripts/requirements.txt
```

Install Chrome or Chromium through the system package manager if it is not already present.

## Smoke test

```bash
python ./scripts/cde_query.py --help
python ./scripts/cde_query.py breakthrough-announcements --pretty
```

## Troubleshooting

- If Selenium cannot start Chrome, verify that Chrome or Chromium is installed and can be opened manually on the same machine.
- If the first query hangs or times out, retry once with `--show-browser` so you can see where the CDE page flow breaks.
- If a company or drug query returns no results, confirm the exact company or drug name first. CDE matching is strict.
- If the CDE page layout changes, inspect the visible browser flow first, then update the selector helpers in `scripts/cde_client.py`.
