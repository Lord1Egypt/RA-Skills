#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广西威能全平台招标信息监控脚本 v5.0
- 覆盖50+平台：政府公共资源、南方电网、能源央企、房地产集团、国企央企、行业平台
- 支持分类扫描、批次轮换、登录/免登录区分
- 电力类关键词筛选 + 微信消息推送
"""

import json
import re
import time
import datetime
import subprocess
import sys
import os
import random
import argparse

# ============ 配置 ============

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
SITES_JSON = os.path.join(SCRIPT_DIR, "../references/gx_websites.json")

POWER_KEYWORDS = [
    '配电', '供配电', '扩容', '线路', '迁改', '增容', '一户一表',
    '10kV', '35kV', '110kV', '10kv', '35kv', '110kv',
    '变压器', '箱变', '开闭所', '配电房', '配电室', '电缆',
    '电力', '供电', '用电', '配网', '电网', '输变电', '变电站',
    '配电工程', '电力工程', '电气', '电能', '用电工程', '供电所',
    '充电桩', '充电站', '新能源', '光伏', '储能', '风电', '光伏',
    '高压', '低压', '开关柜', '断路器', '母线', '桥架', '接地',
    '电气安装', '电气工程', '电气设备', '成套设备', '无功补偿',
    '防雷', '接地', '计量', '互感器', '避雷器', '绝缘', '试验'
]

EXCLUDE_WORDS = ['拍卖', '出让', '土地', '矿产', '采矿权', '探矿权', '国有产权', '林权', '海域', '排污权']

# 每日默认扫描的分类（轮换机制）
DEFAULT_DAILY_CATEGORIES = ['gov_public', 'power_grid']
ROTATION_CATEGORIES = ['energy', 'real_estate', 'state_owned', 'central_enterprises', 'industry', 'other']

# ============ 工具函数 ============

def load_sites():
    """加载网站配置"""
    with open(SITES_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def is_power_related(text):
    if not text:
        return False
    text_lower = text.lower()
    for exclude in EXCLUDE_WORDS:
        if exclude in text:
            return False
    for kw in POWER_KEYWORDS:
        if kw.lower() in text_lower:
            return True
    return False

def run(cmd, timeout=25):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout, r.stderr, r.returncode
    except Exception as e:
        return '', str(e), 1

def browser_open(url, label):
    out, err, rc = run(['openclaw', 'browser', 'open', '--label', label, url], timeout=25)
    if rc == 0:
        m = re.search(r'tab:\s*(\S+)', out)
        return m.group(1) if m else None, None
    return None, out + err

def browser_open_with_retry(url, label, max_retries=2):
    for i in range(max_retries):
        tab, err = browser_open(url, label)
        if tab:
            return tab, None
        print(f"      ⚠️ 第{i+1}次打开失败，等待3秒重试...")
        time.sleep(3)
    return None, f"重试{max_retries}次后仍失败: {err[:80]}"

def browser_close(tab_id):
    run(['openclaw', 'browser', 'close', tab_id], timeout=10)

def browser_text(tab_id, max_chars=5000):
    run(['openclaw', 'browser', 'focus', tab_id], timeout=10)
    out, err, rc = run(
        ['openclaw', 'browser', 'evaluate', '--fn',
         f'() => document.body.innerText.substring(0, {max_chars})'],
        timeout=20
    )
    if rc == 0:
        t = out.strip()
        if t.startswith('"') and t.endswith('"'):
            t = t[1:-1]
        return t.replace('\\n', '\n').replace('\\t', '\t')
    return f"ERROR: {err}"

def extract_items(text, site_name, site_url, category):
    """提取信息条目"""
    items = []
    if not text or text.startswith('ERROR'):
        return items

    date_pat = [r'(\d{4}-\d{2}-\d{2})', r'(\d{4}年\d{1,2}月\d{1,2}日)', r'(\d{2}-\d{2})']
    skip = ['首页', '下一页', '上一页', '当前位置', '网站地图', '版权', '备案', '访问量',
            '无障碍', '长者', '简体', '繁体', '更多>>', '设为首页', '加入收藏', '登录', '注册']

    for line in text.split('\n'):
        line = line.strip()
        if len(line) < 25 or len(line) > 150:
            continue
        if any(s in line for s in skip):
            continue

        date = None
        for p in date_pat:
            m = re.search(p, line)
            if m:
                date = m.group(1)
                break
        if not date:
            continue

        # 全平台统一：仅采集电力类标讯
        if not is_power_related(line):
            continue

        items.append({'title': line, 'date': date, 'source': site_name, 'url': site_url, 'category': category})

    # 去重
    seen = set()
    unique = []
    for it in items:
        k = it['title'][:50]
        if k not in seen:
            seen.add(k)
            unique.append(it)
    return unique[:8]

def get_daily_categories():
    """根据星期几决定今日轮换分类"""
    weekday = datetime.datetime.now().weekday()
    rotation = ROTATION_CATEGORIES[weekday % len(ROTATION_CATEGORIES)]
    return DEFAULT_DAILY_CATEGORIES + [rotation]

def format_wechat_message(result, auth_sites):
    """格式化微信推送消息。无电力标讯时返回空字符串，不推送。"""
    # 收集所有电力标讯（extract_items 已做电力筛选，这里直接汇总）
    all_items = []
    for cat_key in [
        'gov_public', 'power_grid', 'energy', 'real_estate',
        'state_owned', 'central_enterprises', 'industry', 'other'
    ]:
        items = result.get(cat_key, [])
        all_items.extend(items)

    # 无电力标讯，不推送任何消息
    if not all_items:
        return ''

    ds = datetime.datetime.now().strftime('%Y%m%d')
    lines = [f"📋 威能招标日报 ({ds})", ""]

    # 按分类归组
    for cat_key, cat_name in [
        ('gov_public', '🏛️ 政府公共资源'),
        ('power_grid', '⚡ 电力电网'),
        ('energy', '🔋 能源央企'),
        ('real_estate', '🏗️ 房地产集团'),
        ('state_owned', '🏢 国企/大型集团'),
        ('central_enterprises', '🏭 央企平台'),
        ('industry', '🌐 行业平台'),
        ('other', '📦 其他企业')
    ]:
        items = result.get(cat_key, [])
        if items:
            lines.append(f"{cat_name}: {len(items)}条")
            for it in items[:3]:
                lines.append(f"  • {it['title'][:50]}")
                lines.append(f"    📍 {it['source']}")
            lines.append("")

    lines.append(f"📊 今日电力标讯: {len(all_items)}条")
    lines.append("")

    # 需登录提醒
    if auth_sites:
        lines.append("🔐【今日需登录查看】")
        for site in auth_sites[:5]:
            lines.append(f"  • {site['name']}")
        if len(auth_sites) > 5:
            lines.append(f"  ... 等共{len(auth_sites)}个平台")
        lines.append("")

    lines.append("—")
    return '\n'.join(lines)

def scan_category(category_key, category_data, browser_active=True):
    """扫描一个分类下的所有网站"""
    print(f"\n{'='*50}")
    print(f"📂 {category_data['name']} ({len(category_data['sites'])}个网站)")
    print(f"{'='*50}")

    results = []
    if not browser_active:
        print("⚠️ Browser 未启动，跳过扫描")
        return results

    for i, site in enumerate(category_data['sites'], 1):
        name = site['name']
        url = site['url']
        print(f"  [{i}] {name}...", end=' ', flush=True)

        tab, err = browser_open_with_retry(url, f"{category_key}_{i}")
        if not tab:
            print(f"❌ 打开失败")
            continue

        time.sleep(2)
        text = browser_text(tab, 5000)
        browser_close(tab)

        if text.startswith('ERROR'):
            print(f"❌ 提取失败")
            continue

        items = extract_items(text, name, url, category_key)
        power_items = [it for it in items if is_power_related(it['title'])]

        if power_items:
            print(f"✅ {len(power_items)}条电力")
            results.extend(power_items)
        elif items:
            print(f"ℹ️ {len(items)}条,无电力")
        else:
            print(f"⚠️ 无数据")

        time.sleep(1)

    return results

def main():
    parser = argparse.ArgumentParser(description='威能全平台招标信息监控')
    parser.add_argument('--category', '-c', help='指定扫描分类 (gov_public/power_grid/energy/real_estate/state_owned/central_enterprises/industry/other)')
    parser.add_argument('--all', '-a', action='store_true', help='扫描所有分类（耗时较长）')
    parser.add_argument('--auth-only', action='store_true', help='仅输出需登录平台清单')
    parser.add_argument('--no-browser', action='store_true', help='不使用 browser，仅输出配置清单')
    args = parser.parse_args()

    print(f"🔍 威能全平台招标监控 v5.0 {datetime.datetime.now().strftime('%H:%M:%S')}")

    # 加载配置
    try:
        config = load_sites()
    except Exception as e:
        print(f"❌ 加载配置失败: {e}")
        sys.exit(1)

    categories = config.get('categories', {})
    auth_data = config.get('auth_required', {})
    auth_sites = auth_data.get('sites', [])

    # 仅输出登录清单
    if args.auth_only:
        print(f"\n🔐 需登录查看的平台 ({len(auth_sites)}个):")
        for site in auth_sites:
            print(f"  • {site['name']}: {site['url']}")
            if 'account' in site:
                print(f"    账号: {site['account']}")
        return

    # 确定今日扫描分类
    if args.all:
        target_categories = list(categories.keys())
    elif args.category:
        if args.category not in categories:
            print(f"❌ 未知分类: {args.category}")
            print(f"可用: {', '.join(categories.keys())}")
            sys.exit(1)
        target_categories = [args.category]
    else:
        target_categories = get_daily_categories()

    print(f"\n📅 今日扫描分类: {', '.join(target_categories)}")
    print(f"🔐 需登录平台: {len(auth_sites)}个 (建议手动查看)")

    # 启动 browser
    browser_active = False
    if not args.no_browser:
        out, _, rc = run(['openclaw', 'browser', 'status'], timeout=10)
        if rc != 0 or 'running' not in out.lower():
            print("⚠️ 启动 browser...")
            run(['openclaw', 'browser', 'start'], timeout=15)
            time.sleep(3)

        out, _, rc = run(['openclaw', 'browser', 'status'], timeout=10)
        if rc == 0 and 'running' in out.lower():
            browser_active = True
            print("✅ Browser 已就绪")
        else:
            print("⚠️ Browser 启动失败，将仅输出配置清单")

    # 扫描
    result = {}
    for cat_key in target_categories:
        if cat_key in categories:
            result[cat_key] = scan_category(cat_key, categories[cat_key], browser_active)
        else:
            print(f"⚠️ 分类 {cat_key} 不存在")

    # 汇总
    total = sum(len(v) for v in result.values())
    print(f"\n📊 汇总: 共扫描 {len(target_categories)} 个分类，发现 {total} 条信息")

    # 保存结果
    ds = datetime.datetime.now().strftime('%Y%m%d')
    result_data = {
        'datetime': datetime.datetime.now().isoformat(),
        'categories_scanned': target_categories,
        'results': result,
        'auth_sites_count': len(auth_sites)
    }

    result_path = os.path.join(WORKSPACE, f'bidding_results_{ds}.json')
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    print(f"💾 结果已保存: {result_path}")

    # 微信消息
    msg = format_wechat_message(result, auth_sites)
    if msg:
        msg_path = os.path.join(WORKSPACE, f'wechat_msg_{ds}.txt')
        with open(msg_path, 'w', encoding='utf-8') as f:
            f.write(msg)
        print(f"\n💬 微信消息:\n{msg}")
    else:
        print(f"\n📭 今日无电力标讯，不推送")

    return result_data

if __name__ == '__main__':
    main()
