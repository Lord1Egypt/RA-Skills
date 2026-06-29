#!/usr/bin/env python3
"""
🎯 BigFocus · 追踪管家核心脚本

用法:
  python3 scripts/bigfocus.py add <名称> <类型> <目标> [间隔(h)]
  python3 scripts/bigfocus.py remove <ID>
  python3 scripts/bigfocus.py update <ID> <字段> <值>
  python3 scripts/bigfocus.py list [--json]
  python3 scripts/bigfocus.py scan
  python3 scripts/bigfocus.py record <ID> <最后值> <摘要>
  python3 scripts/bigfocus.py info <ID>
"""

import sys
import os
import json
import re
from datetime import datetime, timedelta

WORKSPACE = os.environ.get('OPENCLAW_WORKSPACE',
                           os.path.expanduser('~/.openclaw/workspace'))
MEMORY_DIR = os.path.join(WORKSPACE, 'memory')
TRACKER_FILE = os.path.join(MEMORY_DIR, 'bigfocus-tracker.md')
RAW_DATA_FILE = os.path.join(MEMORY_DIR, 'bigfocus-raw-data.json')

os.makedirs(MEMORY_DIR, exist_ok=True)

# ── 类型定义 ──────────────────────────────────────

VALID_TYPES = {
    '商品': '💰',
    '人物': '🌟',
    '行业': '🏭',
    '指标': '📊',
}
TYPE_ICON = VALID_TYPES

VALID_INTERVALS = [1, 2, 3, 6, 12, 24]

# ── tracker.md 解析/写入 ──────────────────────────

TRACKER_HEADER_TEMPLATE = """# 🎯 BigFocus 追踪列表

> 自动维护。用户添加/删除/修改优先。

## 追踪项

| # | 名称 | 类型 | 目标/描述 | 间隔(h) | 下次检查 | 最后更新 | 最后值 | 状态 |
|---|------|------|----------|---------|---------|---------|-------|------|
"""


def _normalize_tracker_content(text):
    """Strip optional whitespace before/after the table area."""
    return text.strip() + '\n'


def parse_tracker():
    """
    解析 tracker.md 文件，返回 [{id, name, type_, target, interval_h, next_check, last_update, last_value, status}]
    如果文件不存在或为空表格，返回 []
    """
    if not os.path.exists(TRACKER_FILE):
        return []

    with open(TRACKER_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    items = []
    in_table = False
    for line in content.split('\n'):
        line = line.strip()
        # 跳过空行和非表格行
        if not line or line.startswith('#'):
            continue
        if line.startswith('|---') or line.startswith('| -'):
            in_table = True
            continue
        if line.startswith('|') and in_table:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 9:  # 前有空列 + 8列数据
                # parts[0] 是第一个 | 前面的空串
                # parts[1]~parts[8] 是8列数据
                item = {
                    'id': int(parts[1]) if parts[1].isdigit() else parts[1],
                    'name': parts[2],
                    'type_': parts[3],
                    'target': parts[4],
                    'interval_h': int(parts[5].rstrip('hH')) if parts[5].replace('h','').replace('H','').strip().isdigit() else 24,
                    'next_check': parts[6],
                    'last_update': parts[7],
                    'last_value': parts[8],
                    'status': parts[9] if len(parts) > 9 else 'active',
                }
                items.append(item)
    return items


def _format_table_row(item):
    """Format a single item dict as a table row."""
    name = item['name']
    type_ = item.get('type_', '')
    target = item.get('target', '')
    interval_h = item.get('interval_h', 24)
    next_check = item.get('next_check', '-')
    last_update = item.get('last_update', '-')
    last_value = item.get('last_value', '-')
    status = item.get('status', 'active')
    idx = item.get('id', 0)
    # 只写数字，列标题已标注 (h)
    interval_str = str(int(interval_h))
    return f'| {idx} | {name} | {type_} | {target} | {interval_str} | {next_check} | {last_update} | {last_value} | {status} |'


def write_tracker(items):
    """
    Write items list to tracker.md
    items: list of dicts with keys: id, name, type_, target, interval_h, next_check, last_update, last_value, status
    """
    # Sort by id
    items = sorted(items, key=lambda x: int(x['id']))

    lines = [TRACKER_HEADER_TEMPLATE.rstrip('\n')]
    for item in items:
        lines.append(_format_table_row(item))
    lines.append('')  # trailing newline

    with open(TRACKER_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return items


# ── raw-data.json 操作 ──────────────────────────

def _load_raw_data():
    if not os.path.exists(RAW_DATA_FILE):
        return {}
    with open(RAW_DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save_raw_data(data):
    with open(RAW_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── CRUD 操作 ──────────────────────────────────

def add_item(name, type_, target, interval_h=None):
    """添加追踪项。type_ 必须是 VALID_TYPES 的 key 之一。"""
    if type_ not in VALID_TYPES:
        return {'error': f'无效类型: {type_}，可选: {", ".join(VALID_TYPES.keys())}'}

    if interval_h is None:
        # 默认间隔根据类型
        defaults = {'商品': 6, '人物': 12, '行业': 24, '指标': 1}
        interval_h = defaults.get(type_, 24)

    interval_h = int(interval_h)
    if interval_h < 1:
        return {'error': '最小间隔为 1 小时'}
    # 如果不是标准间隔，允许（但最小1h）
    if interval_h not in VALID_INTERVALS and interval_h > 24:
        return {'error': f'间隔最大为 24 小时'}

    items = parse_tracker()

    # 生成新 ID
    new_id = max([int(i['id']) for i in items] + [0]) + 1

    now = datetime.now()
    next_check = now.strftime('%Y-%m-%d %H:%M')

    new_item = {
        'id': new_id,
        'name': name,
        'type_': type_,
        'target': target,
        'interval_h': interval_h,
        'next_check': next_check,
        'last_update': '-',
        'last_value': '-',
        'status': 'active',
    }

    items.append(new_item)
    write_tracker(items)

    return {
        'success': True,
        'item': new_item,
        'message': f'已添加追踪 #{new_id}: {name} ({type_})，间隔 {interval_h}h'
    }


def remove_item(item_id):
    """移除追踪项（标记为 inactive）。"""
    items = parse_tracker()
    item_id = int(item_id)
    found = False
    for item in items:
        if int(item['id']) == item_id:
            item['status'] = 'inactive'
            found = True
            name = item['name']
            break

    if not found:
        return {'error': f'未找到 #{item_id}'}

    write_tracker(items)
    return {'success': True, 'message': f'已删除追踪 #{item_id}: {name}'}


def update_item(item_id, field, value):
    """更新追踪项的字段。"""
    items = parse_tracker()
    item_id = int(item_id)
    found = None

    valid_fields = {
        'name': 'name',
        'type': 'type_',
        'target': 'target',
        '间隔': 'interval_h',
        'interval': 'interval_h',
        '状态': 'status',
        'status': 'status',
    }

    mapped_field = valid_fields.get(field, field)

    for item in items:
        if int(item['id']) == item_id:
            found = item
            break

    if not found:
        return {'error': f'未找到 #{item_id}'}

    # 类型校验
    if mapped_field == 'type_' and value not in VALID_TYPES:
        return {'error': f'无效类型: {value}'}
    if mapped_field == 'interval_h':
        value = int(value)
        if value < 1:
            return {'error': '最小间隔 1 小时'}
        # 重置下次检查时间
        now = datetime.now()
        found['next_check'] = now.strftime('%Y-%m-%d %H:%M')
    if mapped_field == 'status' and value not in ('active', 'inactive', 'paused'):
        return {'error': f'无效状态: {value}，可选 active/inactive/paused'}

    old_val = found.get(mapped_field, '')
    found[mapped_field] = value
    write_tracker(items)

    field_display = field
    return {'success': True, 'message': f'已更新 #{item_id} {field_display}: {old_val} → {value}'}


def list_items(as_json=False):
    """列出所有活跃追踪项。"""
    items = parse_tracker()
    active = [i for i in items if i['status'] == 'active']
    inactive = [i for i in items if i['status'] != 'active']

    if as_json:
        return {'active': active, 'inactive': inactive, 'total': len(items), 'active_count': len(active)}

    # 文本输出
    if not active:
        return {'text': '🎯 BigFocus · 当前没有活跃追踪项。回复「添加追踪」开始追踪吧！'}

    lines = ['🎯 BigFocus · 追踪列表', '']
    lines.append(f'| # | 名称 | 类型 | 目标 | 间隔 | 下次检查 | 最后更新 | 最后值 |')
    lines.append(f'|---|------|------|------|------|---------|---------|-------|')

    for item in active:
        icon = TYPE_ICON.get(item['type_'], '')
        interval_str = f"{item['interval_h']}h"
        lines.append(
            f"| {item['id']} | {icon} {item['name']} | {item['type_']} | {item['target'][:20]} | {interval_str} | {item['next_check']} | {item['last_update'][:10]} | {item['last_value'][:15]} |"
        )

    if inactive:
        lines.append('')
        lines.append(f'📦 已暂停/删除: {len(inactive)} 项')

    lines.append('')
    lines.append('💡 操作: 添加 / 删除 #N / 暂停 #N / 间隔 #N 6h / 列表')

    return {'text': '\n'.join(lines)}


def info_item(item_id):
    """查看单条追踪详情。"""
    items = parse_tracker()
    item_id = int(item_id)
    found = None
    for item in items:
        if int(item['id']) == item_id:
            found = item
            break

    if not found:
        return {'error': f'未找到 #{item_id}'}

    # 读取 raw-data
    raw = _load_raw_data()
    history = raw.get(str(item_id), {}).get('history', [])

    icon = TYPE_ICON.get(found['type_'], '')
    lines = [
        f'🎯 {icon} {found["name"]}',
        f'  #ID: {found["id"]}',
        f'  类型: {found["type_"]}',
        f'  目标: {found["target"]}',
        f'  间隔: {found["interval_h"]}h',
        f'  下次检查: {found["next_check"]}',
        f'  最后更新: {found["last_update"]}',
        f'  最后值: {found["last_value"]}',
        f'  状态: {found["status"]}',
    ]

    if history:
        lines.append(f'  历史记录 ({len(history)} 条):')
        for h in history[-5:]:  # 最近5条
            lines.append(f'    [{h.get("time","")}] {h.get("value","")} — {h.get("summary","")[:30]}')
    else:
        lines.append('  历史记录: 暂无')

    return {'text': '\n'.join(lines)}


# ── Scan 逻辑 ────────────────────────────────

def scan():
    """
    扫描追踪列表，找出到期项。
    返回：
    {
        "expired": [到期项列表],
        "auto_updated": [自动采集更新的项],
        "need_ai": [需要 AI 搜索的项],
        "next_run_hint": "下次到期项提示",
        "total_active": N
    }
    """
    items = parse_tracker()
    now = datetime.now()
    active = [i for i in items if i['status'] == 'active']
    expired = []
    need_ai = []
    auto_updated = []

    for item in active:
        try:
            next_dt = datetime.strptime(item['next_check'], '%Y-%m-%d %H:%M')
        except (ValueError, TypeError):
            # 格式不对，立即到期
            next_dt = datetime.min

        if next_dt <= now:
            expired.append(item)
            # 商品和指标类型的到期项，尝试自动采集
            if item['type_'] in ('商品', '指标'):
                result = _auto_fetch(item)
                if result:
                    auto_updated.append(result)
                else:
                    # 自动采集失败，交给 AI 处理
                    need_ai.append(item)
            else:
                need_ai.append(item)

    # 更新自动采集项到 tracker
    for au in auto_updated:
        for i, item in enumerate(items):
            if int(item['id']) == int(au['id']):
                items[i] = au['item']
                break
    write_tracker(items)

    # 计算下次到期提示
    next_hint = _get_next_hint(items)

    result = {
        'expired_count': len(expired),
        'expired': [{'id': i['id'], 'name': i['name'], 'type_': i['type_']} for i in expired],
        'auto_updated': [{'id': a['id'], 'name': a['name'], 'change': a.get('change', '')} for a in auto_updated],
        'need_ai': [{'id': i['id'], 'name': i['name'], 'type_': i['type_'], 'target': i['target']} for i in need_ai],
        'total_active': len(active),
        'next_run_hint': next_hint,
    }

    return result


def _auto_fetch(item):
    """
    尝试自动采集商品价格或指标数值。
    返回 dict 或 None。
    """
    import hashlib
    from urllib.request import Request, urlopen
    from urllib.error import URLError

    name = item['name']
    target = item['target']
    type_ = item['type_']
    old_value = item['last_value']

    new_value = None
    summary = ''

    if type_ == '商品':
        # 尝试从京东商品页抓取（如果 URL 是京东的）
        if 'jd.com' in target:
            try:
                req = Request(target, headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
                    'Accept': 'text/html,application/xhtml+xml',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                })
                resp = urlopen(req, timeout=10)
                html = resp.read().decode('utf-8', errors='ignore')

                # 尝试多种模式匹配价格
                price_patterns = [
                    r'￥([\d,]+\.?\d*)',
                    r'price["\']:\s*["\']?([\d.]+)',
                    r'"price"\s*:\s*([\d.]+)',
                    r'<span class="price"[^>]*>([\d.]+)',
                ]
                for pat in price_patterns:
                    m = re.search(pat, html)
                    if m:
                        new_value = f'¥{m.group(1)}'
                        summary = f'抓取价格: {m.group(1)}'
                        break
            except Exception:
                pass

    elif type_ == '指标':
        # 尝试识别常见指标并提供搜索关键词
        # 比特币/加密货币
        if any(k in target.lower() for k in ['btc', 'bitcoin', '比特币', 'eth', '以太坊']):
            try:
                # CoinGecko 免费 API
                req = Request(
                    'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd',
                    headers={'Accept': 'application/json'}
                )
                resp = urlopen(req, timeout=10)
                data = json.loads(resp.read())
                price = data.get('bitcoin', {}).get('usd', '')
                if price:
                    new_value = f'${price:,.2f}' if isinstance(price, (int, float)) else f'${price}'
                    summary = 'CoinGecko 自动获取'
            except Exception:
                pass

        # 其他指标，留空让 AI 处理
        if not new_value:
            return None

    if new_value is not None and new_value != old_value:
        now = datetime.now()
        change = ''
        if old_value != '-':
            change = f'{old_value} → {new_value}'

        # 记录到 raw-data
        raw = _load_raw_data()
        item_id_str = str(item['id'])
        if item_id_str not in raw:
            raw[item_id_str] = {'history': []}
        raw[item_id_str]['last_value'] = new_value
        raw[item_id_str]['last_fetch'] = now.strftime('%Y-%m-%d %H:%M')
        raw[item_id_str]['history'].append({
            'time': now.strftime('%Y-%m-%d %H:%M'),
            'value': new_value,
            'summary': summary,
            'source': 'auto_fetch',
        })
        # 保留最近 50 条
        raw[item_id_str]['history'] = raw[item_id_str]['history'][-50:]
        _save_raw_data(raw)

        # 更新 tracker 项
        item['last_update'] = now.strftime('%Y-%m-%d %H:%M')
        item['last_value'] = new_value
        item['next_check'] = (now + timedelta(hours=int(item['interval_h']))).strftime('%Y-%m-%d %H:%M')

        return {
            'id': item['id'],
            'name': name,
            'old_value': old_value,
            'new_value': new_value,
            'change': change,
            'item': item,
        }

    elif new_value is not None and new_value == old_value:
        # 没变化，只更新下次检查时间
        now = datetime.now()
        item['next_check'] = (now + timedelta(hours=int(item['interval_h']))).strftime('%Y-%m-%d %H:%M')

        return {
            'id': item['id'],
            'name': name,
            'no_change': True,
            'item': item,
        }

    return None


def _get_next_hint(items):
    """计算下一次到期时间提示。"""
    now = datetime.now()
    next_time = None
    next_item = None
    for item in items:
        if item['status'] != 'active':
            continue
        try:
            dt = datetime.strptime(item['next_check'], '%Y-%m-%d %H:%M')
            if dt > now and (next_time is None or dt < next_time):
                next_time = dt
                next_item = item
        except (ValueError, TypeError):
            pass

    if next_item:
        remaining = (next_time - now).seconds // 60
        if remaining < 60:
            return f'{next_item["name"]} 约 {remaining} 分钟后到期'
        else:
            return f'{next_item["name"]} 在 {next_time.strftime("%H:%M")}'
    return '暂无到期项'


# ── Record 操作 ──────────────────────────────

def record_result(item_id, last_value, summary):
    """
    AI 搜索到结果后，记录到 raw-data 并更新 tracker。
    用于人物/行业等需要 AI web_search 的项。
    """
    items = parse_tracker()
    item_id = int(item_id)
    found = None
    for item in items:
        if int(item['id']) == item_id:
            found = item
            break

    if not found:
        return {'error': f'未找到 #{item_id}'}

    now = datetime.now()
    old_value = found['last_value']

    # 记录到 raw-data
    raw = _load_raw_data()
    item_id_str = str(item_id)
    if item_id_str not in raw:
        raw[item_id_str] = {'history': []}
    raw[item_id_str]['last_value'] = last_value
    raw[item_id_str]['last_fetch'] = now.strftime('%Y-%m-%d %H:%M')
    raw[item_id_str]['history'].append({
        'time': now.strftime('%Y-%m-%d %H:%M'),
        'value': last_value,
        'summary': summary,
        'source': 'ai_search',
    })
    raw[item_id_str]['history'] = raw[item_id_str]['history'][-50:]
    _save_raw_data(raw)

    # 更新 tracker
    found['last_update'] = now.strftime('%Y-%m-%d %H:%M')
    found['last_value'] = last_value
    found['next_check'] = (now + timedelta(hours=int(found['interval_h']))).strftime('%Y-%m-%d %H:%M')
    write_tracker(items)

    change = ''
    if old_value != '-' and old_value != last_value:
        change = f'{old_value} → {last_value}'

    return {
        'success': True,
        'id': item_id,
        'name': found['name'],
        'old_value': old_value,
        'new_value': last_value,
        'change': change,
    }


# ── 主入口 ──────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == 'add':
        if len(sys.argv) < 4:
            print('用法: python3 bigfocus.py add <名称> <类型(商品/人物/行业/指标)> <目标> [间隔(h)]')
            sys.exit(1)
        name = sys.argv[2]
        type_ = sys.argv[3]
        target = sys.argv[4] if len(sys.argv) > 4 else name
        interval_h = int(sys.argv[5]) if len(sys.argv) > 5 else None
        result = add_item(name, type_, target, interval_h)
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0 if result.get('success') else 1)

    elif cmd == 'remove':
        if len(sys.argv) < 3:
            print('用法: python3 bigfocus.py remove <ID>')
            sys.exit(1)
        result = remove_item(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0 if result.get('success') else 1)

    elif cmd == 'update':
        if len(sys.argv) < 5:
            print('用法: python3 bigfocus.py update <ID> <字段(name/type/target/interval/status)> <值>')
            sys.exit(1)
        result = update_item(sys.argv[2], sys.argv[3], sys.argv[4])
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0 if result.get('success') else 1)

    elif cmd == 'list':
        as_json = '--json' in sys.argv
        result = list_items(as_json=as_json)
        if as_json:
            print(json.dumps(result, ensure_ascii=False))
        else:
            print(result.get('text', ''))
        sys.exit(0 if 'error' not in result else 1)

    elif cmd == 'info':
        if len(sys.argv) < 3:
            print('用法: python3 bigfocus.py info <ID>')
            sys.exit(1)
        result = info_item(sys.argv[2])
        if 'error' in result:
            print(json.dumps(result, ensure_ascii=False))
            sys.exit(1)
        print(result.get('text', ''))
        sys.exit(0)

    elif cmd == 'scan':
        result = scan()
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)

    elif cmd == 'record':
        if len(sys.argv) < 5:
            print('用法: python3 bigfocus.py record <ID> <最后值> <摘要>')
            sys.exit(1)
        last_value = sys.argv[3]
        summary = ' '.join(sys.argv[4:])
        result = record_result(sys.argv[2], last_value, summary)
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0 if result.get('success') else 1)

    else:
        print(f'未知命令: {cmd}')
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
