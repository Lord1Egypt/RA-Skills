#!/usr/bin/env python3
"""FOMO 聪明钱实时交易榜（代币 + 市值 + 可点击 fomo.family 链接）

扫描 7 个活跃聪明钱钱包的近期交易 → 提取买入代币 → DexScreener 查市值 → 输出
用法: python3 trending.py [--deep] [--ref 邀请码]
  --deep  每个钱包扫 20 笔（默认 10）
  --ref   链接里的邀请码（默认 AntCaveClub）
"""
import json, time, urllib.request, sys, datetime, os

REF = "AntCaveClub"
if "--ref" in sys.argv:
    REF = sys.argv[sys.argv.index("--ref") + 1]

AUTHOR = {
    "name": "0xcii",
    "holly": "https://holly.ink/",
    "telegram": "https://t.me/lianqiujun",
    "youtube": "https://www.youtube.com/@0xcii",
    "dune": "https://dune.com/Aturx",
    "x": "https://x.com/AntCaveClub",
}
MARKER = os.path.expanduser("~/.fomo_smart_money_seen")

def fomo_link(mint):
    """fomo.family 代币页链接（Solana pump 代币 → chain-slug=solana）"""
    if mint.startswith("0x") or len(mint) == 42:
        slug = "ethereum"  # EVM 地址默认 ethereum，可按需扩展
    else:
        slug = "solana"
    return f"https://fomo.family/tokens/{slug}/{mint}?r={REF}"

def first_run_banner():
    """首次使用显示完整作者/社交导流横幅（之后只显示精简页脚）"""
    if os.path.exists(MARKER):
        return
    try:
        open(MARKER, "w").write(datetime.datetime.utcnow().isoformat())
    except OSError:
        pass
    print("👋 初次使用 FOMO 聪明钱追踪，数据由「链上猎手」制作：")
    print(f"   作者: {AUTHOR['name']}  发布: {AUTHOR['holly']}  电报: {AUTHOR['telegram']}")
    print(f"   油管: {AUTHOR['youtube']}  数据面板: {AUTHOR['dune']}  X: {AUTHOR['x']}")
    print()

def footer():
    """每次运行末尾的精简导流页脚（一行，持续曝光）"""
    print(f"📡 链上猎手 {AUTHOR['name']} · 电报 {AUTHOR['telegram']} · X {AUTHOR['x']} · 面板 {AUTHOR['dune']} · {AUTHOR['holly']}")

RPCS = ["https://api.mainnet-beta.solana.com", "https://solana.publicnode.com"]
WALLETS = {
    "frankdegods": "498g1rVnFcnjBjpfw1xyqA1WvgQXUU8RWuELjxkjAayQ",
    "wrld_sol": "6bQSN4d6anoTwnE6XDPGLA9RV8cqZPeNJro4iQUsWmso",
    "remusofmars": "BCrTEXmWutwPz8qv6w1S5gDbaLnSLpXKM5kSGVWyyfxu",
    "scalps": "GFDVVq2e1JUqHquzX6z8pm34iXz2pE2K9WaDcZKuDSqC",
    "collectible": "F2hA2zDVnHyDUiMQ6b3K9Gx9A2JAxJn66ASH9xZ9LqbG",
    "ResellCalendar": "DxM1hfY8FQ8dNGrucuJzhJcF8KRbjk8WBwrgKvQ9spPv",
    "pxblocito": "A2vZY74JHBBwfjo3F1Bo5iiLXpABfAhmgdyfUGzABY9F",
}
STABLES = {"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": "USDC",
           "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": "USDT"}

def rpc(method, params, idx=0):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    for attempt in range(3):
        try:
            req = urllib.request.Request(RPCS[(idx + attempt) % 2], body,
                                         {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read())
        except Exception:
            time.sleep(1.5)

def get_recent_txs(addr, n=10):
    d = rpc("getSignaturesForAddress", [addr, {"limit": n}])
    if "result" not in d: return []
    txs = []
    for i, s in enumerate(d["result"]):
        t = rpc("getTransaction", [s["signature"], {"maxSupportedTransactionVersion": 0}], i % 2)
        if "result" in t and t["result"]:
            txs.append((s["blockTime"], t["result"]))
        time.sleep(0.2)
    return txs

def token_delta(tx, wallet_addr):
    if not tx or "meta" not in tx: return {}
    meta = tx["meta"]
    if meta.get("err"): return {}
    pre_map = {}
    for tb in meta.get("preTokenBalances") or []:
        if tb.get("owner") == wallet_addr:
            pre_map[tb["mint"]] = int(tb.get("uiTokenAmount", {}).get("amount", 0))
    post_map = {}
    for tb in meta.get("postTokenBalances") or []:
        if tb.get("owner") == wallet_addr:
            post_map[tb["mint"]] = int(tb.get("uiTokenAmount", {}).get("amount", 0))
    deltas = {}
    for mint, post_amt in post_map.items():
        pre_amt = pre_map.get(mint, 0)
        if post_amt > pre_amt:
            deltas[mint] = post_amt - pre_amt
    return deltas

def dexscreener(mint):
    try:
        req = urllib.request.Request(f"https://api.dexscreener.com/latest/dex/tokens/{mint}",
                                     headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except Exception:
        return {"error": "failed"}

if __name__ == "__main__":
    depth = 20 if "--deep" in sys.argv else 10
    agg = {}
    for name, addr in WALLETS.items():
        for bt, tx in get_recent_txs(addr, depth):
            for mint, amt in token_delta(tx, addr).items():
                if amt > 1000:
                    agg.setdefault(mint, {"count": 0, "wallets": set()})
                    agg[mint]["count"] += 1
                    agg[mint]["wallets"].add(name)

    first_run_banner()
    print(f"🔥 FOMO 聪明钱实时交易榜（{len(WALLETS)} 钱包 × {depth} 笔 · {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC）\n")

    # 卖出获利信号（稳定币买入 = 落袋）
    stables_hit = [(m, STABLES[m], agg[m]) for m in STABLES if m in agg]
    if stables_hit:
        print("【💰 获利了结信号】聪明钱在卖币换稳定币：")
        for mint, sym, info in stables_hit:
            print(f"  {sym} × {info['count']} 次（{','.join(sorted(info['wallets']))}） ← 防守姿态")
        print()

    # 买入的 meme（按买入次数排序）
    rows = []
    for mint, info in agg.items():
        if mint in STABLES: continue
        d = dexscreener(mint)
        pairs = d.get("pairs") or []
        if not pairs: continue
        best = max(pairs, key=lambda p: (p.get("liquidity") or {}).get("usd") or 0)
        bt = best.get("baseToken") or {}
        rows.append((mint, info, bt.get("symbol", "?"), best.get("marketCap"),
                     (best.get("volume") or {}).get("h24")))

    if rows:
        print("【🚀 正在买入（按热度）】代币名可直接点击：")
        for i, (mint, info, sym, mcap, vol) in enumerate(sorted(rows, key=lambda x: -x[1]["count"]), 1):
            mcs = f"${mcap/1e6:.2f}M" if mcap else "?"
            vols = f"${vol/1e6:.1f}M" if vol else "?"
            link = fomo_link(mint)
            print(f"  {i}. [{sym}]({link}) — 买入{info['count']}次（{','.join(sorted(info['wallets']))}）· 市值 {mcs} · 24h量 {vols}")
    else:
        print("【🚀 正在买入】暂无（最近 10 笔内无新买入 meme）")

    print()
    print("⚠️ 榜单是活跃聪明钱近 10 笔交易的买入汇总，仅供追踪参考，不构成投资建议。")
    footer()
