#!/usr/bin/env python3
"""
钉钉→飞书 日程自动同步 - 本周版（今天+未来6天）
从 ~/.dingtalk/config.json 读取钉钉配置，从 ~/.feishu/config.json 读取飞书配置
"""

import requests
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scripts.config_loader import load_config, get_feishu_config, get_dingtalk_config

FEISHU_CONFIG_PATH = os.path.expanduser("~/.feishu/config.json")

_session = requests.Session()

def get_ding_events():
    config = load_config()
    ding_cfg = get_dingtalk_config(config)
    ding_config_path = os.path.expanduser(ding_cfg.get('config_path', '~/.dingtalk/config.json'))
    with open(ding_config_path, 'r', encoding='utf-8') as f:
        ding_config = json.load(f)

    app_key = ding_config.get('app_key')
    app_secret = ding_config.get('app_secret')
    union_id = ding_config.get('user_id')

    resp = _session.post(
        "https://api.dingtalk.com/v1.0/oauth2/accessToken",
        json={"appKey": app_key, "appSecret": app_secret},
        timeout=10
    )
    data = resp.json()
    token = data.get('accessToken')
    if not token:
        print(f"❌ 获取钉钉token失败: {data}")
        sys.exit(1)

    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    start_dt = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_dt = (now + datetime.timedelta(days=7)).replace(hour=23, minute=59, second=59)

    resp = _session.get(
        f"https://api.dingtalk.com/v1.0/calendar/users/{union_id}/calendars/primary/events",
        headers={"x-acs-dingtalk-access-token": token},
        params={
            "timeMin": start_dt.strftime('%Y-%m-%dT%H:%M:%S+08:00'),
            "timeMax": end_dt.strftime('%Y-%m-%dT%H:%M:%S+08:00'),
            "maxResults": 100
        },
        timeout=15
    )
    result = resp.json()
    return result.get('events', [])

def format_events(events):
    formatted = []
    current_year = datetime.datetime.now().year
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    start_of_week = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_week = (now + datetime.timedelta(days=7)).replace(hour=23, minute=59, second=59, microsecond=0)

    for ev in events:
        ev_status = ev.get('status', 'confirmed')
        if ev_status == 'cancelled':
            continue
        summary = ev.get('summary', '无标题')
        start = ev.get('start', {})
        end = ev.get('end', {})
        start_time = start.get('dateTime', start.get('date'))
        end_time = end.get('dateTime', end.get('date'))

        if not start_time:
            continue

        try:
            dt_start = datetime.datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            dt_start = dt_start.astimezone(datetime.timezone(datetime.timedelta(hours=8)))
            if dt_start.year != current_year:
                dt_start = dt_start.replace(year=current_year)
            start_ts = int(dt_start.timestamp())
            start_str = dt_start.strftime('%Y-%m-%d %H:%M')
        except:
            continue

        try:
            dt_end = datetime.datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            dt_end = dt_end.astimezone(datetime.timezone(datetime.timedelta(hours=8)))
            if dt_end.year != current_year:
                dt_end = dt_end.replace(year=current_year)
            end_str = dt_end.strftime('%H:%M')
            end_ts = int(dt_end.timestamp())
        except:
            end_str = '未知'
            end_ts = start_ts

        if start_of_week.timestamp() <= start_ts <= end_of_week.timestamp():
            formatted.append({
                'summary': summary,
                'start': start_str,
                'end': end_str,
                'start_ts': start_ts,
                'end_ts': end_ts,
                'location': ev.get('location', {}).get('displayName', ''),
                'description': ev.get('description', ''),
                'status': ev_status
            })

    return formatted

def refresh_and_get_token():
    feishu_cfg = get_feishu_config(load_config())
    app_id = feishu_cfg.get('app_id')
    app_secret = feishu_cfg.get('app_secret')

    with open(FEISHU_CONFIG_PATH, 'r', encoding='utf-8') as f:
        token_data = json.load(f)

    refresh_token = token_data.get('refresh_token')
    if not refresh_token:
        return None, False

    resp = _session.post(
        "https://open.feishu.cn/open-apis/authen/v1/refresh_access_token",
        json={"grant_type": "refresh_token", "app_id": app_id, "app_secret": app_secret, "refresh_token": refresh_token},
        timeout=10
    )
    data = resp.json()
    if data.get('code') == 0:
        new_data = data.get('data', {})
        for k in ['access_token', 'refresh_token', 'expires_in', 'refresh_expires_in']:
            if k in new_data:
                token_data[k] = new_data[k]
        with open(FEISHU_CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(token_data, f, indent=2, ensure_ascii=False)
        print(f"✅ token自动刷新成功")
        return new_data.get('access_token'), True
    else:
        print(f"⚠️ token刷新失败: {data.get('msg')}，使用旧token")
        return token_data.get('access_token'), False

def sync_to_feishu(events):
    feishu_cfg = get_feishu_config(load_config())
    calendar_id = feishu_cfg.get('calendar_id')

    access_token, _ = refresh_and_get_token()
    headers = {"Authorization": f"Bearer {access_token}"}

    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    start_ts = int(now.replace(hour=0, minute=0, second=0).timestamp())
    end_ts = int((now + datetime.timedelta(days=7)).replace(hour=23, minute=59, second=59).timestamp())

    dingtalk_keys = {(ev['summary'].strip(), ev['start_ts']) for ev in events}

    print(f"\n🧹 清理本周钉钉同步日程...")
    resp = _session.get(
        f"https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events",
        headers=headers,
        params={"start_timestamp": start_ts, "end_timestamp": end_ts, "page_size": 500},
        timeout=20
    )
    data = resp.json()
    deleted = 0
    if data.get('code') == 0:
        items = data.get('data', {}).get('items', [])
        to_delete = []
        for item in items:
            try:
                s_ts = int(item['start_time']['timestamp'])
                title = item.get('summary', '').strip()
                desc = item.get('description', '')
                key = (title, s_ts)
                if '从钉钉自动同步' in desc or key in dingtalk_keys:
                    to_delete.append(item['event_id'])
            except (ValueError, TypeError):
                pass
        for eid in to_delete:
            del_resp = _session.delete(
                f"https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events/{eid}",
                headers=headers, timeout=10
            )
            if del_resp.json().get('code') == 0:
                deleted += 1
        print(f"  ✅ 清理了 {deleted} 个旧日程\n")

    print(f"📝 创建 {len(events)} 个日程到飞书...\n")
    success = 0

    for ev in events:
        summary = ev.get('summary', '无标题').strip()
        start_ts = ev.get('start_ts')
        end_ts = ev.get('end_ts')
        location = ev.get('location', '')
        description = ev.get('description', '')

        if not start_ts or not end_ts:
            continue

        body = {
            "summary": summary,
            "description": description or '从钉钉自动同步',
            "start_time": {"timestamp": str(start_ts), "time_zone": "Asia/Shanghai"},
            "end_time": {"timestamp": str(end_ts), "time_zone": "Asia/Shanghai"}
        }
        if location:
            body["location"] = {"name": location}

        resp = _session.post(
            f"https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events",
            headers=headers, json=body, timeout=10
        )
        result = resp.json()

        if result.get('code') == 0:
            print(f"  {summary} {ev['start']}")
            print(f"    ✅ 成功\n")
            success += 1
        else:
            print(f"  {summary} {ev['start']}")
            print(f"    ❌ 失败: {result.get('msg')}\n")

    return success, deleted, len(events)

def main():
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    week_end = now + datetime.timedelta(days=6)
    print(f"🔍 从钉钉获取本周日程（{now.strftime('%m-%d')} ~ {week_end.strftime('%m-%d')}）...\n")

    raw_events = get_ding_events()
    events = format_events(raw_events)

    if not events:
        print("😯 本周没有钉钉日程")
        return

    print(f"✅ 找到 {len(events)} 个本周日程:\n")
    for ev in events:
        status_icon = "❌" if ev.get('status') == 'cancelled' else "📅"
        print(f"  {status_icon} {ev['summary']}: {ev['start']} ~ {ev['end']} [{ev.get('status', 'confirmed')}]")
        if ev['location']:
            print(f"    地点: {ev['location']}")
        print()

    success, deleted, total = sync_to_feishu(events)

    print(f"\n🎉 同步完成！删除了 {deleted} 个旧日程，创建了 {success}/{total} 个新日程")

    print(f"\n📅 本周同步结果（{now.strftime('%m-%d')} ~ {week_end.strftime('%m-%d')}）:\n")
    for i, ev in enumerate(sorted(events, key=lambda x: x['start_ts']), 1):
        print(f"  {i}. {ev['summary']} | {ev['start']} ~ {ev['end']}")
        if ev['location']:
            print(f"     📍 {ev['location']}")
        print(f"     状态: {ev.get('status', 'confirmed')}")

    print()

if __name__ == '__main__':
    main()
