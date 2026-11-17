#!/usr/bin/env python3
"""crypto-alerts CLI: monitor top-50 crypto trade setups via CoinGecko.

States per setup:
  stage 1 = waiting entry   -> entry touch => ask "pasang?" (reminds max 3x/6h)
  stage 2 = position open   -> favorable move >= +0.2% => ask to place SL+ (once)
  stage 3 = SL+ confirmed   -> TP hit / CL hit / SL+ hit => alert + delete setup

Storage: setups.json next to this file's parent dir (crypto-alerts/setups.json).
Prices: CoinGecko /coins/markets (free, no key) in one call for all coin ids.
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SETUPS_PATH = os.path.join(BASE_DIR, "setups.json")
COINS_PATH = os.path.join(BASE_DIR, "coins.json")
COINS_TTL = 7 * 24 * 3600
SLOP = 0.002          # 0.2% favorable-move threshold for SL+ prompt
ENTRY_HIT_BPS = 30    # 0.30% entry-touch tolerance band
REMIND_MAX = 3
REMIND_WINDOW = 6 * 3600
TOP_N = 50

API = ("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
       "&order=market_cap_desc&per_page={n}&page=1")


def load(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default


def save(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=1)
    os.replace(tmp, path)


def resolve_ids(symbols):
    """Map symbols like BTC -> coingecko ids via cached top-50 list."""
    now = time.time()
    cache = load(COINS_PATH, None)
    if not cache or now - cache.get("fetched_at", 0) > COINS_TTL:
        try:
            with urllib.request.urlopen(API.format(n=TOP_N), timeout=15) as r:
                rows = json.load(r)
            cache = {"fetched_at": now,
                     "map": {r["symbol"].upper(): r["id"] for r in rows}}
            save(COINS_PATH, cache)
        except Exception as e:
            if cache:
                print(f"[warn] coin list refresh failed: {e}", file=sys.stderr)
            else:
                sys.exit(f"[error] cannot fetch coin list: {e}")
    m = cache["map"]
    return {s: m.get(s.upper()) for s in symbols}


def fetch_prices(ids):
    ids = sorted({i for i in ids if i})
    if not ids:
        return {}
    url = API.format(n=TOP_N) if len(ids) >= TOP_N else (
        "https://api.coingecko.com/api/v3/simple/price?ids="
        + urllib.parse.quote(",".join(ids)) + "&vs_currencies=usd")
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            data = json.load(r)
    except Exception as e:
        sys.exit(f"[error] price fetch failed: {e}")
    out = {}
    for row in (data if isinstance(data, list) else []):
        out[row["id"]] = row["current_price"]
    for k, v in (data if isinstance(data, dict) else {}).items():
        out[k] = v.get("usd")
    return out


def fmt(sym, side, entry, tp, cl, price=None, extra=""):
    p = f" (sekarang {price:g})" if price else ""
    return (f"{sym} {side.upper()} | entry {entry:g} | TP {tp:g} | CL {cl:g}{p}"
            + (f" | {extra}" if extra else ""))


# ----------------------------------------------------------------- commands

def cmd_check(args=None):
    """Headless run: print alert lines (silent when nothing to say)."""
    setups = load(SETUPS_PATH, {})
    if not setups:
        return
    now = time.time()
    ids = resolve_ids({s["symbol"] for s in setups.values()})
    prices = fetch_prices(ids.values())

    alerts, remove = [], []
    for sid, s in setups.items():
        sym, price = s["symbol"], prices.get(ids.get(s["symbol"]))
        if not price:
            continue
        side, entry, tp, cl = s["side"], s["entry"], s["tp"], s["cl"]
        long_ = side == "long"
        hit_tp = price >= tp if long_ else price <= tp
        hit_cl = price <= cl if long_ else price >= cl

        if s["stage"] == 1:
            lo, hi = min(entry, tp, cl), max(entry, tp, cl)
            touched = (hi * (1 + ENTRY_HIT_BPS / 10000) >= price
                       >= lo * (1 - ENTRY_HIT_BPS / 10000))
            if touched or hit_tp or hit_cl:
                r = s.setdefault("remind", {"count": 0, "last": 0})
                if r["count"] < REMIND_MAX and now - r["last"] > 3600:
                    r["count"] += 1
                    r["last"] = now
                    line = ("🔔 PASANG POSISI? " + fmt(sym, side, entry, tp, cl, price)
                            + " → jawab: pasang / ga jadi")
                    if hit_tp:
                        line += " (harga sudah melewati TP — mungkin ga worth)"
                    if hit_cl:
                        line += " (harga sudah kena CL — setup batal)"
                    alerts.append(line)
                if hit_tp or hit_cl:
                    remove.append(sid)  # stage-1 CL hit / missed: auto-cancel
        elif s["stage"] == 2:
            fav = price >= entry * (1 + SLOP) if long_ else price <= entry * (1 - SLOP)
            cl_now = hit_cl or (price <= entry * (1 - SLOP) if long_
                                else price >= entry * (1 + SLOP))
            if hit_tp:
                alerts.append(f"🎯 SAATNYA TP! " + fmt(sym, side, entry, tp, cl, price))
                remove.append(sid)
            elif hit_cl:
                alerts.append(f"🛑 SAATNYA CL! " + fmt(sym, side, entry, tp, cl, price))
                remove.append(sid)
            elif cl_now:
                alerts.append("🛑 CL tersentuh sebelum SL+ terpasang! "
                              + fmt(sym, side, entry, tp, cl, price))
                remove.append(sid)
            elif fav and not s.get("slplus_asked"):
                s["slplus_asked"] = True
                alerts.append("✅ +/-0.2% tercapai — PASANG SL+ sekarang! "
                              + fmt(sym, side, entry, tp, cl, price)
                              + " → jawab: sudah <harga SL+> / batal")
            elif fav:
                pass  # already asked; quiet until TP/CL/SL+
        elif s["stage"] == 3:
            slp = s["slplus"]
            hit_slp = price <= slp if long_ else price >= slp
            if hit_tp:
                alerts.append(f"🎯 SAATNYA TP! " + fmt(sym, side, entry, tp, cl, price))
                remove.append(sid)
            elif hit_cl:
                alerts.append(f"🛑 SAATNYA CL! " + fmt(sym, side, entry, tp, cl, price))
                remove.append(sid)
            elif hit_slp:
                alerts.append("ℹ️ SL+ kena — posisi keluar BE, setup ditutup. "
                              + fmt(sym, side, entry, tp, cl, price))
                remove.append(sid)

    for sid in remove:
        setups.pop(sid, None)
    save(SETUPS_PATH, setups)
    if alerts:
        print("CRYPTO ALERTS\n" + "\n".join(alerts))


def cmd_add(args):
    # alert BTC long entry 76000 tp 78000 cl 74500
    m = re.match(r"(\S+)\s+(long|short)\s+entry\s+([\d.,]+)\s+tp\s+([\d.,]+)\s+"
                 r"cl\s+([\d.,]+)\s*$", " ".join(args).strip().lower())
    if not m:
        sys.exit('Format: alert add BTC long entry 76000 tp 78000 cl 74500')
    sym, side = m.group(1).upper(), m.group(2)
    entry, tp, cl = (float(x.replace(",", "")) for x in m.groups()[2:5])
    if side == "long" and not (cl < entry < tp):
        sys.exit("Validasi long gagal: harus cl < entry < tp")
    if side == "short" and not (tp < entry < cl):
        sys.exit("Validasi short gagal: harus tp < entry < cl")
    setups = load(SETUPS_PATH, {})
    sid = f"{sym}-{side}-{int(time.time())}"
    setups[sid] = {"symbol": sym, "side": side, "entry": entry, "tp": tp,
                   "cl": cl, "stage": 1, "created": int(time.time()),
                   "remind": {"count": 0, "last": 0}}
    save(SETUPS_PATH, setups)
    print(f"OK setup {sid} tersimpan (stage 1: menunggu entry).")


def cmd_list(args=None):
    setups = load(SETUPS_PATH, {})
    if not setups:
        print("Tidak ada setup aktif.")
        return
    stage = {1: "menunggu entry", 2: "posisi jalan (belum SL+)",
             3: "SL+ terpasang"}
    for sid, s in setups.items():
        extra = f" | SL+ {s['slplus']:g}" if s.get("slplus") else ""
        print(f"{sid} | stage {s['stage']} ({stage[s['stage']]}) | "
              + fmt(s["symbol"], s["side"], s["entry"], s["tp"], s["cl"]) + extra)


def cmd_remove(args):
    sid = args[0] if args else ""
    setups = load(SETUPS_PATH, {})
    if sid in setups:
        setups.pop(sid)
        save(SETUPS_PATH, setups)
        print(f"OK {sid} dihapus.")
    else:
        sys.exit(f"{sid} tidak ditemukan. Lihat: alert_cli.py list")


def cmd_resolve(args):
    # resolve <sid> sudah 76100   -> stage 3, slplus=76100
    # resolve <sid> batal         -> delete
    sid, word = args[0], (args[1].lower() if len(args) > 1 else "")
    setups = load(SETUPS_PATH, {})
    if sid not in setups:
        sys.exit(f"{sid} tidak ditemukan. Lihat: alert_cli.py list")
    if word == "batal":
        setups.pop(sid)
        save(SETUPS_PATH, setups)
        print(f"OK {sid} dibatalkan & dihapus.")
        return
    m = re.search(r"([\d.,]+)", " ".join(args[1:]))
    if word == "pasang":
        setups[sid]["stage"] = 2
        save(SETUPS_PATH, setups)
        print(f"OK {sid} → stage 2 (pantau +0.2% untuk SL+).")
    elif word == "sudah" and m:
        slp = float(m.group(1).replace(",", ""))
        setups[sid].update(stage=3, slplus=slp, slplus_asked=True)
        save(SETUPS_PATH, setups)
        print(f"OK {sid} → stage 3 (SL+ {slp:g} dipantau; TP/CL/SL+ kena = tutup).")
    else:
        sys.exit('Format: resolve <id> pasang | resolve <id> sudah <harga-sl+> | resolve <id> batal')


def main():
    cmds = {"check": cmd_check, "add": cmd_add, "list": cmd_list,
            "remove": cmd_remove, "resolve": cmd_resolve}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print("Usage: alert_cli.py check|add|list|remove|resolve ...")
        sys.exit(2)
    cmds[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    main()
