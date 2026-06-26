#!/usr/bin/env python3
import json
import re
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path.cwd()
STATE_DIR = ROOT / '.openclaw-state'
BASELINE_PATH = STATE_DIR / 'boc-forex-alerts.json'
TRIGGER_PATH = STATE_DIR / 'boc-forex-alerts-trigger.json'
PAUSE_PATH = STATE_DIR / 'boc-forex-paused.json'
CONFIG_PATH = STATE_DIR / 'boc-forex-monitor-config.json'
URL = 'https://www.boc.cn/sourcedb/whpj/'
SH_TZ = timezone(timedelta(hours=8), name='Asia/Shanghai')
COLUMN_MAP = {
    '现汇买入价': 'xh_buy',
    '现钞买入价': 'xc_buy',
    '现汇卖出价': 'xh_sell',
    '现钞卖出价': 'xc_sell',
    '中行折算价': 'boc_avg',
}
DEFAULT_CONFIG = {
    'timezone': 'Asia/Shanghai',
    'quietHours': {'enabled': True, 'start': 23, 'end': 9},
    'baselineUpdateThreshold': 0.5,
    'targets': [
        {'currency': '英镑', 'enabled': False, 'column': '现汇卖出价', 'threshold': 0.5, 'direction': 'both'},
        {'currency': '日元', 'enabled': True, 'column': '现汇卖出价', 'threshold': 0.5, 'direction': 'both'},
        {'currency': '港币', 'enabled': True, 'column': '现汇买入价', 'threshold': 0.5, 'direction': 'rise'},
    ],
}


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


def save_json(path: Path, data):
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def strip_tags(html: str) -> str:
    html = re.sub(r'<script[\s\S]*?</script>', ' ', html, flags=re.IGNORECASE)
    html = re.sub(r'<style[\s\S]*?</style>', ' ', html, flags=re.IGNORECASE)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = html.replace('\u00A0', ' ')
    html = re.sub(r'[\t\r\n]+', ' ', html)
    html = re.sub(r'\s{2,}', ' ', html)
    return html.strip()


def parse_table_rows(html: str):
    parts = re.split(r'<\s*/\s*tr\s*>', html, flags=re.IGNORECASE)
    return [p.strip() for p in parts if p.strip()]


def extract_row_values(row_html: str):
    text = strip_tags(row_html)
    tokens = [t for t in text.split(' ') if t]
    if len(tokens) < 8:
        return None
    first_num_idx = -1
    for i, t in enumerate(tokens):
        if re.match(r'^(\d+)(\.\d+)?$', t):
            first_num_idx = i
            break
    if first_num_idx < 0:
        return None
    name = ''.join(tokens[:first_num_idx])
    nums_tokens = tokens[first_num_idx:]
    nums = []
    for t in nums_tokens:
        if re.match(r'^(\d+)(\.\d+)?$', t):
            nums.append(float(t))
        else:
            break
    if len(nums) < 5:
        return None
    rest = ' '.join(nums_tokens[len(nums):])
    m_date = re.search(r'(\d{4}/\d{2}/\d{2})', rest)
    m_time = re.search(r'(\d{2}:\d{2}:\d{2})', rest)
    return {
        'name': name,
        'cols': {
            'xh_buy': nums[0],
            'xc_buy': nums[1],
            'xh_sell': nums[2],
            'xc_sell': nums[3],
            'boc_avg': nums[4],
        },
        'pubDate': m_date.group(1) if m_date else None,
        'pubTime': m_time.group(1) if m_time else None,
    }


def fetch_html() -> str:
    last_error = None
    for attempt in range(3):
        try:
            req = Request(URL, headers={'User-Agent': 'Mozilla/5.0 (OpenClaw forex monitor)'})
            with urlopen(req, timeout=20) as resp:
                if resp.status != 200:
                    raise RuntimeError(f'HTTP {resp.status}')
                data = resp.read()
            for encoding in ('utf-8', 'gbk', 'gb18030'):
                try:
                    html = data.decode(encoding)
                    if '外汇牌价' in html:
                        return html
                except UnicodeDecodeError:
                    continue
            html = data.decode('latin1', errors='ignore')
            if html:
                return html
            raise RuntimeError('empty response body after decode')
        except Exception as e:
            last_error = e
            if attempt < 2:
                time.sleep(1.2 * (attempt + 1))
    raise last_error


def now_shanghai() -> datetime:
    return datetime.now(SH_TZ)


def in_quiet_hours(now: datetime, config: dict) -> bool:
    quiet = config.get('quietHours') or {}
    if not quiet.get('enabled', True):
        return False
    start = int(quiet.get('start', 23))
    end = int(quiet.get('end', 9))
    return now.hour >= start or now.hour < end


def to_fixed_trim(n: float, digits: int = 4) -> float:
    return float(f'{n:.{digits}f}')


def normalize_target(raw: dict) -> dict:
    target = dict(raw or {})
    target['currency'] = str(target.get('currency', '')).strip()
    target['enabled'] = bool(target.get('enabled', True))
    target['column'] = str(target.get('column', '现汇卖出价')).strip()
    target['threshold'] = float(target.get('threshold', 0.5))
    target['direction'] = str(target.get('direction', 'both')).strip().lower()
    if target['direction'] not in {'rise', 'drop', 'both'}:
        target['direction'] = 'both'
    if target['column'] not in COLUMN_MAP:
        raise RuntimeError(f"Invalid column for {target['currency']}: {target['column']}")
    if not target['currency']:
        raise RuntimeError('Target currency cannot be empty')
    return target


def load_config() -> dict:
    config = load_json(CONFIG_PATH) or DEFAULT_CONFIG
    targets = [normalize_target(t) for t in (config.get('targets') or []) if (t or {}).get('enabled', True) or True]
    config = {
        'timezone': config.get('timezone', DEFAULT_CONFIG['timezone']),
        'quietHours': config.get('quietHours', DEFAULT_CONFIG['quietHours']),
        'baselineUpdateThreshold': float(config.get('baselineUpdateThreshold', 0.5)),
        'targets': targets,
    }
    enabled = [t for t in targets if t.get('enabled', True)]
    if not enabled:
        raise RuntimeError('No enabled monitoring targets configured')
    return config


def pick_configured_values(rows: list[dict], config: dict):
    enabled_targets = [t for t in config['targets'] if t.get('enabled', True)]
    picked = {}
    monitoring = []
    for target in enabled_targets:
        currency = target['currency']
        row = next((x for x in rows if currency in x['name']), None)
        if not row:
            continue
        col_key = COLUMN_MAP[target['column']]
        picked[currency] = {
            'name': row['name'],
            'column': target['column'],
            'value': row['cols'][col_key],
            'pubDate': row['pubDate'],
            'pubTime': row['pubTime'],
        }
        monitoring.append({
            'currency': currency,
            'column': target['column'],
            'threshold': target['threshold'],
            'direction': target['direction'],
            'enabled': True,
        })
    missing = [t['currency'] for t in enabled_targets if t['currency'] not in picked]
    return picked, monitoring, missing


def build_summary(picked: dict, monitoring: list[dict]):
    pub_date = None
    pub_time = None
    for item in monitoring:
        row = picked.get(item['currency'])
        if row and (row.get('pubDate') or row.get('pubTime')):
            pub_date = row.get('pubDate')
            pub_time = row.get('pubTime')
            break
    parts = []
    for item in monitoring:
        row = picked.get(item['currency'])
        if row:
            parts.append(f"{row['name']}（{row['column']}）：{row['value']}")
    main = '；'.join(parts)
    if pub_date or pub_time:
        ts = ' '.join([x for x in [pub_date, pub_time] if x])
        return f'「BOC 当前汇率」{main}；页面时间 {ts}；来源 {URL}'
    return f'「BOC 当前汇率」{main}；来源 {URL}'


def build_trigger_summaries(triggers):
    lines = []
    for t in triggers:
        ts = ' '.join([x for x in [t.get('pubDate'), t.get('pubTime')] if x])
        line = f"「中国银行外汇牌价 5 分钟监控提醒」{t['currency']}（{t['column']}）：上次 {t['previous']} → 本次 {t['current']}，变化 {t['change']}"
        if ts:
            line += f'；页面时间 {ts}'
        line += f'。来源：{URL}'
        lines.append(line)
    return '\n'.join(lines)


def main():
    now_sh = now_shanghai()
    pause_state = load_json(PAUSE_PATH)
    if pause_state and pause_state.get('paused', True):
        print(json.dumps({'status': 'skipped', 'reason': 'paused', 'timestamp': datetime.now(timezone.utc).isoformat(), 'localTime': now_sh.isoformat(), 'pause': pause_state, 'message': '监控已暂停，本次跳过。'}, ensure_ascii=False))
        return 0

    config = load_config()
    if in_quiet_hours(now_sh, config):
        quiet = config.get('quietHours') or {}
        print(json.dumps({'status': 'skipped', 'reason': 'quiet-hours', 'timezone': config.get('timezone', 'Asia/Shanghai'), 'quietHours': f"{int(quiet.get('start', 23)):02d}:00-{int(quiet.get('end', 9)):02d}:00", 'timestamp': datetime.now(timezone.utc).isoformat(), 'localTime': now_sh.isoformat(), 'message': '北京时间免监控时段，本次跳过。'}, ensure_ascii=False))
        return 0

    try:
        html = fetch_html()
        rows = [v for r in parse_table_rows(html) if (v := extract_row_values(r))]
        picked, monitoring, missing = pick_configured_values(rows, config)
        if missing:
            raise RuntimeError(f"ParseError: missing currency rows: {', '.join(missing)}")

        baseline = load_json(BASELINE_PATH)
        now_iso = datetime.now(timezone.utc).isoformat()
        establish_baseline = baseline is None
        if baseline is not None:
            for item in monitoring:
                currency = item['currency']
                current = picked[currency]
                prev = baseline.get(currency)
                if not prev or prev.get('column') != current['column']:
                    establish_baseline = True
                    break

        summary = build_summary(picked, monitoring)
        config_snapshot = {'targets': monitoring, 'baselineUpdateThreshold': config['baselineUpdateThreshold']}

        if establish_baseline:
            save_json(BASELINE_PATH, {**picked, '_meta': {'timestamp': now_iso, 'targets': monitoring}})
            print(json.dumps({'status': 'baseline-updated', 'timestamp': now_iso, 'url': URL, 'picked': picked, 'summary': summary, 'monitoring': monitoring, 'config': config_snapshot}, ensure_ascii=False))
            return 0

        deltas = {}
        for item in monitoring:
            currency = item['currency']
            deltas[currency] = to_fixed_trim(picked[currency]['value'] - baseline[currency]['value'], 6)

        triggers = []
        for item in monitoring:
            currency = item['currency']
            prev_v = baseline[currency]['value']
            cur_v = picked[currency]['value']
            rise = to_fixed_trim(cur_v - prev_v, 6)
            drop = to_fixed_trim(prev_v - cur_v, 6)
            threshold = float(item['threshold'])
            if item['direction'] in {'rise', 'both'} and rise > threshold:
                triggers.append({'code': f"{currency}_RISE_{str(threshold).replace('.', '_')}", 'currency': currency, 'column': item['column'], 'previous': prev_v, 'current': cur_v, 'change': rise, 'pubDate': picked[currency]['pubDate'], 'pubTime': picked[currency]['pubTime'], 'direction': 'rise', 'threshold': threshold})
            if item['direction'] in {'drop', 'both'} and drop > threshold:
                triggers.append({'code': f"{currency}_DROP_{str(threshold).replace('.', '_')}", 'currency': currency, 'column': item['column'], 'previous': prev_v, 'current': cur_v, 'change': -drop, 'pubDate': picked[currency]['pubDate'], 'pubTime': picked[currency]['pubTime'], 'direction': 'drop', 'threshold': threshold})

        if any(abs(delta) > config['baselineUpdateThreshold'] for delta in deltas.values()):
            save_json(BASELINE_PATH, {**picked, '_meta': {'timestamp': now_iso, 'targets': monitoring}})

        if not triggers:
            print(json.dumps({'status': 'ok', 'timestamp': now_iso, 'url': URL, 'picked': picked, 'deltas': deltas, 'summary': summary, 'monitoring': monitoring, 'config': config_snapshot}, ensure_ascii=False))
            return 0

        payload = {'status': 'trigger', 'timestamp': now_iso, 'url': URL, 'picked': picked, 'deltas': deltas, 'triggers': triggers, 'summary': summary, 'triggerSummary': build_trigger_summaries(triggers), 'monitoring': monitoring, 'config': config_snapshot, 'note': 'Threshold triggered. Another job may read this and send a short message.'}
        save_json(TRIGGER_PATH, payload)
        print(json.dumps(payload, ensure_ascii=False))
        return 10
    except (HTTPError, URLError) as e:
        msg = f'HTTPError: {e}'
    except Exception as e:
        msg = f'{e.__class__.__name__}: {e}'

    print(json.dumps({'status': 'error', 'error': msg}, ensure_ascii=False), file=sys.stderr)
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
