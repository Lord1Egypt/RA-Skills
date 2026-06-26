#!/usr/bin/env python3
"""早期项目发现筛选器"""
import csv, sys, re
from datetime import datetime

INPUT = "/Users/moer/.openclaw/workspace/skills/agentfarm-finder/output/results_{}.csv".format(datetime.now().strftime('%Y-%m-%d'))
OUTPUT = "/Users/moer/.openclaw/workspace/skills/agentfarm-finder/output/results_{}_projects.csv".format(datetime.now().strftime('%Y-%m-%d'))

STRONG_LAUNCH = ['introducing', 'launch', 'announcing', 'announced', 'alpha', 'beta', 'v1', 'v2', 'v3', 'version', 'mint now', 'mint soon', 'free mint', 'whitelist', 'debut', 'reveal', 'unveil', 'release', 'live on', 'now live', 'dropped', 'coming soon', 'just dropped', 'now available']
DOMAIN_KEYWORDS = ['agent', 'openclaw', '8004', '8183', 'defi', 'yield', 'farm', 'crypto', 'token', 'eth', 'btc', 'base', 'arbitrum', 'solana', 'autonomous', 'on-chain', 'onchain', 'blockchain', 'erc-', 'airdrop', 'staking', 'liquidity', 'trading bot']
EXCLUDE_USERS = ['gta6alerts', 'clipstudiopaint', 'cryptopulse', 'veizau', 'tippity', 'bl_zonee', 'sleezbomb', 'jamiejhcyw', 'farmgirlcarrie', 'winstarfarm', 'wingriderscom', 'shivst3r', 'prsmdev', 'metalheadmosh', 'cisco', 'morgan_shami', 'roxxyn13', 'stock_highalert', 'shitcoinaire', 'potatoz', 'moltlens', 'shield_ai_agent', 'aiwire', 'coccollectibles', '4chipandcompany', 'mrdiamondballz', 'autotrade_d', 'smallcapgrowthx', 'chai_lens', 'adityabhatia89', 'leftshift42', 'yourcountdownto', 'pulsecrypto24', 'shill_ivey', 'asaio87', 'sebithefounder', 'sushantsparty', 'plusite', 'mydeghana', 'sykkupdates', 'jeetface', 'epaminonda671', 'alpharadarai', 'ethw_chain', 'tokyo87313395', 'mintclawk', 'cblovescode', 'jbritto93', 'ruma_intern', 'santisairi', 'thevoid', 'byreal_io', 'slowmist', 'slowmist_team', 'dailypostngr', 'ranjan3118', 'marco_lobo']
EXCLUDE_CHAT = ['what are', 'how do', 'can someone', 'does anyone', 'working on', 'im working', 'thoughts on', 'opinion', 'is there', 'does anybody', 'help me', 'why ', 'how to', 'podcast', 'episode', 'discussion', 'testing', 'booted up', 'pokemon', 'pokopia', 'sykkuno', 'thanks a ton', 'product hunt']

try:
    with open(INPUT, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
except:
    print(f"找不到原始数据: {INPUT}")
    sys.exit(1)

kept = []
for row in rows:
    username = row.get('用户名', '').lower()
    author = row.get('作者', '').lower()
    text = row.get('内容', '').lower()
    hotness = int(row.get('热度', 0))
    
    if any(u in username or u in author for u in EXCLUDE_USERS): continue
    if any(c in text for c in EXCLUDE_CHAT): continue
    
    has_launch = any(k in text for k in STRONG_LAUNCH)
    has_domain = any(k in text for k in DOMAIN_KEYWORDS)
    
    if has_launch and has_domain: kept.append(row)
    elif hotness >= 15 and has_domain: kept.append(row)

kept.sort(key=lambda x: int(x.get('热度', 0)), reverse=True)

with open(OUTPUT, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['热度', '作者', '用户名', '内容', '链接', '发布时间'])
    writer.writeheader()
    writer.writerows(kept)

print(f"项目发现: {len(kept)} 条")
