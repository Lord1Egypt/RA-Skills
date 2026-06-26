#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
抖音数据导出技能 (Refactored for Portability and Security)
"""

import os
import sys
import json
import time
import csv
import argparse
import requests
from datetime import datetime
import io

# ==================== 动态与安全配置 ====================

# 动态计算核心路径
try:
    SKILL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    SKILLS_ROOT = os.path.abspath(os.path.join(SKILL_DIR, '..'))
    OPENCLAW_ROOT = os.path.abspath(os.path.join(SKILLS_ROOT, '..'))
except NameError:
    SKILL_DIR = os.getcwd()
    SKILLS_ROOT = os.path.abspath(os.path.join(SKILL_DIR, '..'))
    OPENCLAW_ROOT = os.path.abspath(os.path.join(SKILLS_ROOT, '..'))

CONFIG_PATH = os.path.join(OPENCLAW_ROOT, 'config.json')
WORKSPACE_DIR = os.path.join(OPENCLAW_ROOT, 'workspace')
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, "data", "douyin-data-exporter")

# 强制 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# API 接口
API_BASE = "https://api.tikhub.io/api/v1"
USER_POST_VIDEOS_URL = f"{API_BASE}/douyin/app/v3/fetch_user_post_videos"

def get_config_value(key: str, default: str = None) -> str:
    """从 config.json 安全地读取配置值"""
    if not os.path.exists(CONFIG_PATH):
        return default
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
        # 支持嵌套键，例如 "api_keys.tikhub"
        keys = key.split('.')
        value = config
        for k in keys:
            if not isinstance(value, dict) or k not in value:
                return default
            value = value[k]
        return value
    except (json.JSONDecodeError, IOError):
        return default

# 从 config.json 或环境变量获取 Token
TIKHUB_TOKEN = get_config_value('tikhub_api_token', os.getenv('TIKHUB_TOKEN'))

# ==================== 辅助函数 ====================
def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_json(data, filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filepath

def save_csv(video_list, filename):
    if not video_list or not isinstance(video_list, list):
        return None
    flattened = []
    for item in video_list:
        aweme = item.get('aweme', item) if isinstance(item, dict) else {}
        if not aweme: continue
        flat = {
            '视频id': aweme.get('aweme_id', ''),
            '描述': aweme.get('desc', ''),
            '创建时间': datetime.fromtimestamp(aweme.get('create_time', 0)).strftime('%Y-%m-%d %H:%M:%S') if aweme.get('create_time') else '',
            '时长': aweme.get('duration', 0),
            '播放数': aweme.get('statistics', {}).get('play_count', 0),
            '点赞数': aweme.get('statistics', {}).get('digg_count', 0),
            '评论数': aweme.get('statistics', {}).get('comment_count', 0),
            '分享数': aweme.get('statistics', {}).get('share_count', 0)
        }
        flattened.append(flat)
    if not flattened: return None
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=flattened[0].keys())
        writer.writeheader()
        writer.writerows(flattened)
    return filepath

def call_tikhub_api(url, params=None):
    if not TIKHUB_TOKEN:
        return {"error": "TIKHUB_TOKEN 未在 config.json 或环境变量中配置"}
    headers = {'Authorization': f'Bearer {TIKHUB_TOKEN}', 'Accept': 'application/json'}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_msg = f"API 请求失败: {e}"
        if hasattr(e, 'response') and e.response is not None:
            error_msg += f"\n状态码: {e.response.status_code}\n响应内容: {e.response.text}"
        return {"error": error_msg}

# ==================== 数据获取函数 ====================
def fetch_all_user_videos(sec_user_id, max_count=100):
    all_videos, cursor, has_more, page = [], 0, True, 1
    while has_more and len(all_videos) < max_count:
        print(f"  正在获取第 {page} 页...", file=sys.stderr)
        params = {'sec_user_id': sec_user_id, 'max_cursor': cursor, 'count': 20, 'sort_type': 0}
        response = call_tikhub_api(USER_POST_VIDEOS_URL, params)
        if 'error' in response: return response
        data = response.get('data', {})
        videos = data.get('aweme_list', [])
        if not videos: break
        all_videos.extend(videos)
        cursor = data.get('max_cursor', 0)
        has_more = data.get('has_more', False)
        page += 1
        time.sleep(0.5)
    return all_videos

def fetch_douplus_export(customer_id: str, token: str):
    url = "https://boss-ip.da-mai.com/api/v1/lead/dou-plus/order-list/export"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json, application/vnd.ms-excel"}
    params = {"customerId": customer_id}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=60, stream=True)
        print(f"请求URL: {resp.url}", file=sys.stderr)
        resp.raise_for_status()
        content_type = resp.headers.get('Content-Type', '').lower()
        if 'excel' in content_type or 'spreadsheet' in content_type:
            return {"type": "file", "data": resp.content}
        return {"type": "json", "data": resp.json()}
    except requests.exceptions.RequestException as e:
        return {"type": "error", "data": str(e)}

# ==================== 主程序 ====================
def main():
    parser = argparse.ArgumentParser(description="抖音数据导出技能")
    parser.add_argument("--sec-user-id", required=True)
    parser.add_argument("--account-name", required=True)
    parser.add_argument("--max-videos", type=int, default=100)
    parser.add_argument("--export-format", choices=['json', 'csv', 'both'], default='both')
    parser.add_argument("--douplus-token")
    parser.add_argument("--douplus-customer-id")
    args = parser.parse_args()

    ensure_output_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = {}

    print(f"\n[下载] 正在获取用户视频列表 (sec_user_id: {args.sec_user_id})...", file=sys.stderr)
    videos = fetch_all_user_videos(args.sec_user_id, args.max_videos)
    if isinstance(videos, dict) and 'error' in videos:
        print(f"  ❌ 失败：{videos['error']}", file=sys.stderr)
        results['videos'] = {"status": "failed", "error": videos['error']}
    else:
        count = len(videos)
        print(f"  ✅ 成功获取 {count} 条视频", file=sys.stderr)
        base_filename = f"{args.account_name}_短视频数据_{timestamp}"
        saved_files = []
        if args.export_format in ['json', 'both']:
            saved_files.append(save_json(videos, f"{base_filename}.json"))
        if args.export_format in ['csv', 'both']:
            csv_path = save_csv(videos, f"{base_filename}.csv")
            if csv_path: saved_files.append(csv_path)
        results['videos'] = {"status": "success", "count": count, "files": saved_files}

    if args.douplus_token and args.douplus_customer_id:
        print(f"\n[下载] 正在获取投流数据...", file=sys.stderr)
        result = fetch_douplus_export(args.douplus_customer_id, args.douplus_token)
        if result["type"] == "file":
            filename = f"{args.account_name}_投流数据_{timestamp}.xlsx"
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, "wb") as f: f.write(result["data"])
            print(f"  ✅ 文件已保存为: {filepath}", file=sys.stderr)
            results.setdefault('douplus', {})['files'] = [filepath]
        else:
            print(f"  ❌ 投流数据获取失败: {result['data']}", file=sys.stderr)
            results.setdefault('douplus', {})['error'] = result['data']
    
    report = {
        "task": "抖音数据导出", "account_name": args.account_name,
        "timestamp": timestamp, "results": results
    }
    report_path = save_json(report, f"{args.account_name}_导出汇总报告_{timestamp}.json")
    # 标准化输出，便于其他工具捕获
    print(f"REPORT_PATH:{report_path}")

if __name__ == "__main__":
    main()
