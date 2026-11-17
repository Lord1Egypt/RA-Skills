#!/usr/bin/env python3
"""FOMO Smart Money TOP50 查询工具

用法:
  python3 query.py list [--n 50]               列出钱包（按排名）
  python3 query.py get <handle>                查单个钱包详情
  python3 query.py top <n> [--by pnl|volume|trades|followers]  TOP N
  python3 query.py filter [--chain sol|evm] [--min-pnl X] [--min-volume Y] [--min-trades N]
  python3 query.py stats                       整体统计
  python3 query.py links <handle>              输出所有链上链接
  python3 query.py live <handle>               查实时余额（Solana RPC / Blockscout）
"""
import json
import sys
import os
import urllib.request

DATA = os.path.join(os.path.dirname(__file__), '..', 'data', 'wallets.json')

def load():
    with open(DATA) as f:
        return json.load(f)['wallets']

def fmt_money(v):
    if v is None: return '—'
    if v >= 1e9: return f'${v/1e9:.2f}B'
    if v >= 1e6: return f'${v/1e6:.2f}M'
    if v >= 1e3: return f'${v/1e3:.1f}K'
    return f'${v:.0f}'

def row_line(w, verbose=False):
    base = (f"#{w['rank']:<3} {w['handle']:<18} PnL={fmt_money(w['pnl_usd']):>10} "
            f"Vol={fmt_money(w['volume_usd']):>10} Trades={w['trades']:>5} "
            f"Fans={w['followers']:>6} SOL={fmt_money(w['solana_usd'])} EVM={fmt_money(w['evm_usd'])}")
    if verbose:
        base += f"\n     SOL: {w['solana'] or '—'}\n     EVM: {w['evm'] or '—'}"
    return base

def solscan(addr): return f"https://solscan.io/account/{addr}"
def etherscan(addr): return f"https://etherscan.io/address/{addr}"

def cmd_list(args):
    n = 50
    if '--n' in args:
        n = int(args[args.index('--n') + 1])
    for w in load()[:n]:
        print(row_line(w))

def cmd_get(args):
    handle = args[0]
    for w in load():
        if w['handle'].lower() == handle.lower():
            print(row_line(w, verbose=True))
            if w['fomo_solana']: print(f"     FOMO内部(SOL): {w['fomo_solana']}")
            if w['fomo_evm']:    print(f"     FOMO内部(EVM): {w['fomo_evm']}")
            if w['twitter']:     print(f"     Twitter: {w['twitter']}")
            return
    print(f"未找到 handle: {handle}")

def cmd_top(args):
    n = int(args[0]) if args else 10
    by = 'pnl_usd'
    if '--by' in args:
        m = {'pnl': 'pnl_usd', 'volume': 'volume_usd', 'trades': 'trades', 'followers': 'followers'}
        by = m[args[args.index('--by') + 1]]
    for w in sorted(load(), key=lambda x: -(x[by] or 0))[:n]:
        print(row_line(w))

def cmd_filter(args):
    ws = load()
    if '--chain' in args:
        c = args[args.index('--chain') + 1]
        ws = [w for w in ws if (c == 'sol' and w['solana']) or (c == 'evm' and w['evm'])]
    if '--min-pnl' in args:
        v = float(args[args.index('--min-pnl') + 1])
        ws = [w for w in ws if (w['pnl_usd'] or 0) >= v]
    if '--min-volume' in args:
        v = float(args[args.index('--min-volume') + 1])
        ws = [w for w in ws if (w['volume_usd'] or 0) >= v]
    if '--min-trades' in args:
        v = int(args[args.index('--min-trades') + 1])
        ws = [w for w in ws if w['trades'] >= v]
    print(f"匹配 {len(ws)} 个钱包:")
    for w in ws:
        print(row_line(w))

def cmd_stats(args):
    ws = load()
    tot_pnl = sum(w['pnl_usd'] for w in ws)
    tot_vol = sum(w['volume_usd'] for w in ws)
    print(f"钱包数: {len(ws)}")
    print(f"总 PnL: {fmt_money(tot_pnl)} | 总交易量: {fmt_money(tot_vol)}")
    print(f"平均 PnL: {fmt_money(tot_pnl/len(ws))} | 平均交易数: {sum(w['trades'] for w in ws)//len(ws)}")
    print(f"链分布: 双链 {sum(1 for w in ws if w['solana'] and w['evm'])} | 仅SOL {sum(1 for w in ws if w['solana'] and not w['evm'])} | 无链上 {sum(1 for w in ws if not w['solana'] and not w['evm'])}")
    print(f"SOL 资产合计: {fmt_money(sum(w['solana_usd'] or 0 for w in ws))} | EVM 资产合计: {fmt_money(sum(w['evm_usd'] or 0 for w in ws))}")

def cmd_links(args):
    handle = args[0]
    for w in load():
        if w['handle'].lower() == handle.lower():
            if w['solana']: print(f"Solscan: {solscan(w['solana'])}")
            if w['evm']:    print(f"Etherscan: {etherscan(w['evm'])}")
            if w['fomo_solana']: print(f"FOMO内部 SOL: {solscan(w['fomo_solana'])}")
            if w['fomo_evm']:    print(f"FOMO内部 EVM: {etherscan(w['fomo_evm'])}")
            if w['twitter']:     print(f"Twitter: {w['twitter']}")
            return
    print(f"未找到 handle: {handle}")

def rpc_solana_balance(addr):
    body = json.dumps({"jsonrpc":"2.0","id":1,"method":"getBalance","params":[addr]}).encode()
    req = urllib.request.Request("https://api.mainnet-beta.solana.com", body, {"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.loads(r.read())
            lamports = d['result']['value']
            return lamports / 1e9
    except Exception as e:
        return f"ERR: {e}"

def rpc_evm_balance(addr):
    body = json.dumps({"jsonrpc":"2.0","id":1,"method":"eth_getBalance","params":[addr, "latest"]}).encode()
    for rpc in ["https://eth.drpc.org", "https://ethereum.publicnode.com", "https://1rpc.io/eth"]:
        try:
            req = urllib.request.Request(rpc, body, {"Content-Type":"application/json", "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=15) as r:
                d = json.loads(r.read())
                if 'result' in d:
                    return int(d['result'], 16) / 1e18
        except Exception:
            continue
    return "ERR: 所有 RPC 失败"

def cmd_live(args):
    handle = args[0]
    for w in load():
        if w['handle'].lower() == handle.lower():
            print(f"=== {w['handle']} 实时余额（{__import__('datetime').datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC）===")
            if w['solana']:
                bal = rpc_solana_balance(w['solana'])
                print(f"SOL: {bal if isinstance(bal,str) else f'{bal:.2f} SOL'}  (快照时 {fmt_money(w['solana_usd'])})")
            if w['evm']:
                bal = rpc_evm_balance(w['evm'])
                print(f"ETH: {bal if isinstance(bal,str) else f'{bal:.4f} ETH'}  (快照时 {fmt_money(w['evm_usd'])})")
            if not w['solana'] and not w['evm']:
                print("该钱包无链上地址（仅 FOMO 内部）")
            return
    print(f"未找到 handle: {handle}")


def cmd_status(args):
    from collections import Counter
    ws = load()
    c = Counter(w['status'] for w in ws)
    print(f"状态分布: 活跃 {c.get('active',0)} | 已搬家 {c.get('moved',0)} | 空 {c.get('empty',0)} | 静默 {c.get('quiet',0)} | 未知 {c.get('unknown',0)}\n")
    print("🟢 仍活跃（近2周有交易，真信号源）:")
    for w in ws:
        if w['status'] == 'active':
            print(f"  #{w['rank']:<3} {w['handle']:<18} 当前SOL={w.get('current_sol','?')} 最后活动={w.get('last_active')}")
    print("\n🔴 已搬家（快照有钱→现在空，谨慎参考）:")
    for w in ws:
        if w['status'] == 'moved':
            print(f"  #{w['rank']:<3} {w['handle']:<18} 最后活动={w.get('last_active')}")

CMDS = {
    'list': cmd_list, 'get': cmd_get, 'top': cmd_top,
    'filter': cmd_filter, 'stats': cmd_stats, 'links': cmd_links, 'live': cmd_live, 'status': cmd_status,
}

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print(__doc__)
        sys.exit(1)
    CMDS[sys.argv[1]](sys.argv[2:])
