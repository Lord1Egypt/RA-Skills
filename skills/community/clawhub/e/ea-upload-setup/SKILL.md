---
name: "ea-upload-setup"
description: "Standardized EA deployment for MT5: copy, compile, restart, verify. One command to deploy your MetaTrader Expert Advisor and confirm it is running with heartbeat verification."
metadata: {"clawbot": {"requires": {"bins": ["wine", "xdotool"]}, "permissions": {"exec": ["bash", "wine", "xdotool", "cp"], "files": ["/home/openclaw/.wine-mt5/", "/home/openclaw/.openclaw/workspace/tradevault/ea/"], "services": ["mt5.service"], "network": [], "notes": "State-changing: copies files into a LIVE MT5 install, compiles, restarts mt5.service, commits to git. Requires explicit confirmation before running."}}}
---

# EA Upload & Setup (DRT-Axe on MT5/Vantage) 🪓

> ⚠️ **WARNING — STATE-CHANGING OPERATIONS:** This skill copies files into a LIVE MetaTrader 5 installation, compiles an Expert Advisor, restarts the `mt5.service` system service, and may commit changes to git. It can disrupt a running trading service. **Do NOT run without explicit operator confirmation**, and review `deploy_ea.sh` before first use.

**Purpose:** Standardized EA upload → compile → restart → attach → verify. Written 19/8 2026 after repeated failures (Boss: "you have made the same mistake several times"). **FOLLOW THIS SKILL — ALWAYS — when the EA needs to change.**

## 🚨 The 3 mistakes we HAVE made (learn from them!)
1. **`ArraySetAsSeries` missing** → CopyRates without `ArraySetAsSeries(rates, true)` returns the array OLDEST-FIRST. The code assumes rates[0]=newest → reads history backwards → the scan only finds OLD sweeps (e.g. 13/8) → the age gate drops EVERYTHING → 0 trades. **ALWAYS check: after every CopyRates/CopyClose call, `ArraySetAsSeries(arr, true)` must be present (also applies to DRT.mqh's DRT_ICTBias + DRT_DailyBias + SilverBullet scan).**
2. **OCR fumbling instead of DevOps scripts** → NEVER use xdotool/OCR to find the Algo button manually. Run `mt5-ea-fix.py` (DevOps script) — and if an EA dialog is open, press `Enter` (OK).
3. **Tokens wasted on code review** → the change is typically 1-4 lines. Fix → run deploy → verify. Do NOT read the whole code first.

## ⚡ Standard procedure (1 command)
```bash
bash /home/openclaw/.openclaw/workspace/tradevault/ea/deploy_ea.sh
```
The script: copies .mqh+.mq5 → MT5 → compiles (MetaEditor64 via wine+xvfb) → restarts mt5.service → verifies "DRT-Axe started" in the log.
- ✅ SUCCESS = "EA RUNNING" + fresh heartbeat
- ⚠️ "not confirmed after 5 min" = a dialog is waiting → `xdotool key Return` (with correct DISPLAY/XAUTHORITY)
- ❌ compile error = fix the code, run again

## 🛠️ Manual chain (if deploy fails)
```bash
MT5="/home/openclaw/.wine-mt5/drive_c/Program Files/MetaTrader 5"
EA="/home/openclaw/.openclaw/workspace/tradevault/ea"
# 1) Copy
cp "$EA"/DRT.mqh "$MT5/MQL5/Include/DRT.mqh"
cp "$EA"/SilverBullet.mqh "$MT5/MQL5/Include/SilverBullet.mqh"
cp "$EA"/Risk.mqh "$MT5/MQL5/Include/Risk.mqh"
cp "$EA"/TimeFilter.mqh "$MT5/MQL5/Include/TimeFilter.mqh"
cp "$EA"/News.mqh "$MT5/MQL5/Include/News.mqh"
cp "$EA"/Notify.mqh "$MT5/MQL5/Include/Notify.mqh"
cp "$EA"/AntiFlag.mqh "$MT5/MQL5/Include/AntiFlag.mqh"
cp "$EA"/DRT-Axe.mq5 "$MT5/MQL5/Experts/DRT-Axe.mq5"
# 2) Compile (0 errors = OK)
cd "$MT5/MQL5/Experts"
WINEPREFIX=/home/openclaw/.wine-mt5 WINEDLLOVERRIDES=mscoree,mshtml= HOME=/home/openclaw \
  xvfb-run -a wine "$MT5/MetaEditor64.exe" /compile:"DRT-Axe.mq5" /log:"compile_deploy.log" >/dev/null 2>&1
sleep 12
iconv -f UTF-16LE -t UTF-8 compile_deploy.log | grep "Result:"
# 3) Restart + verify
sudo systemctl restart mt5.service
sleep 150   # login ~60s + attach
tail -5 "$MT5/MQL5/Files/DRT-Axe_Log.txt"   # should show "DRT-Axe started — 17 symbols"
```

## 🔍 Verification (ALWAYS after deploy)
| Check | Command | OK sign |
|---|---|---|
| EA runs | `grep "started" DRT-Axe_Log.txt \| tail -1` | today's date + "17 symbols" |
| Fresh heartbeat | `stat -c %y DRT-Axe_HB.txt` | < 2 min old |
| Fresh scan | `tail DRT-Axe_Log.txt` | sweeps with TODAY's prices (not 13/8 levels) |
| Algo ON | `mt5-algo-ensure.py` | "EA heartbeat fresh — Algo is ON" |

## 🪟 If a dialog is waiting (EA properties)
- Symptom: EA loaded but "started" missing / HB frozen
- Fix: find DISPLAY+XAUTHORITY, press Enter:
```bash
export DISPLAY=:99 XAUTHORITY=$(ps aux | grep 'Xvfb :99' | grep -v grep | grep -oE '\-auth [^ ]+' | awk '{print $2}' | head -1)
xdotool key Return
```

## 📁 Fixed paths
- EA code (edit ONLY here): `/home/openclaw/.openclaw/workspace/tradevault/ea/`
- MT5 folder: `/home/openclaw/.wine-mt5/drive_c/Program Files/MetaTrader 5`
- EA log: `$MT5/MQL5/Files/DRT-Axe_Log.txt` (server time GMT+3 = UTC+3)
- Heartbeat: `$MT5/MQL5/Files/DRT-Axe_HB.txt`
- Data for the bot: `$MT5/MQL5/Files/DRT-Axe_Data.json` (written every 60s)
- DevOps scripts: `/home/openclaw/.local/bin/mt5-ea-fix.py`, `mt5-ea-attach.sh`, `mt5-login-helper.sh`, `mt5-algo-ensure.py` (cron every 2 min)

## ⏰ Trading windows (entries)
London 09-11 · NY open 14:30-17:00 · SB PM 19:30-21:00 (CET/Danish time). Night pause 23-08.
**Outside windows = no entries** — that is by design, not a bug. Expect trades in the NY/PM windows.

## 📌 Rules for EA changes (Boss 19/8)
1. Make the CHANGE (typically a few lines) — do not read the whole code
2. Run `deploy_ea.sh` — not manual OCR fumbling
3. Verify with the table above
4. Commit: `git add tradevault/ea/ && git commit -m "EA fix: ..."` (part of the workspace repo)
5. Report briefly: what was changed + proof that it is running
