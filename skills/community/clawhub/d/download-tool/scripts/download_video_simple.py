#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download Tool - Video Download Script
"""

import requests
import json
import time
import os

# Read config
config_path = os.path.expanduser('~/.openclaw/config.json')

with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

api_key = config.get('download_tool_api_key')
base_url = config.get('download_tool_base_url', 'https://www.datamass.cn/ai-back')

# Headers
headers = {
    'X-Api-Key': api_key,
    'Content-Type': 'application/json'
}

# Video URL from user input
video_url = "{{VIDEO_URL}}"

print(f"🎬 开始下载视频: {video_url}")
print()

# Step 1: Check quota before download
print("📊 检查账户信息...")
try:
    quota_url = f"{base_url}/sys/openapi/quota"
    response = requests.get(quota_url, headers=headers, timeout=10)

    if response.status_code == 200:
        quota_data = response.json()
        result = quota_data.get('result', quota_data)
        balance_before = result.get('balance', 0)
        print(f"  账户积分: {balance_before} 积分")
    else:
        balance_before = None
        print(f"  ⚠️  获取账户信息失败")
except Exception as e:
    balance_before = None
    print(f"  ⚠️  查询异常: {e}")

print()

# Step 2: Create download task
print("🚀 创建下载任务...")
try:
    download_url = f"{base_url}/sys/openapi/download"
    data = {"url": video_url}

    response = requests.post(download_url, json=data, headers=headers, timeout=10)

    if response.status_code == 200:
        result = response.json()
        result_data = result.get('result', result)
        task_id = result_data.get('task_id') or result_data.get('taskId')

        print(f"  ✅ 任务创建成功! 任务ID: {task_id}")
        print()

        # Step 3: Poll status
        print("⏳ 等待下载完成...")
        status_url = f"{base_url}/sys/openapi/download/status/{task_id}"
        max_attempts = 360  # 30分钟 = 360次 * 5秒
        attempt = 0

        while attempt < max_attempts:
            try:
                response = requests.get(status_url, headers=headers, timeout=10)

                if response.status_code == 200:
                    status_response = response.json()
                    status_data = status_response.get('result', status_response)
                    status = status_data.get('status', 'unknown')
                    progress = status_data.get('progress', 0)
                    message = status_data.get('message', '')

                    if status == 2 or status == 'completed' or status == 'success':
                        oss_url = status_data.get('oss_url') or status_data.get('ossUrl')
                        print(f"  ✅ 下载完成!")
                        print()

                        # Check quota after download to calculate cost
                        if balance_before is not None:
                            try:
                                response = requests.get(quota_url, headers=headers, timeout=10)
                                if response.status_code == 200:
                                    quota_data = response.json()
                                    result = quota_data.get('result', quota_data)
                                    balance_after = result.get('balance', 0)
                                    cost = balance_before - balance_after

                                    print("="*60)
                                    print("🎉 下载成功！")
                                    print("="*60)
                                    print(f"📎 下载链接: {oss_url}")
                                    print(f"⏰ 有效期: 24小时")
                                    print(f"💰 本次消耗: {cost} 积分")
                                    print(f"💎 剩余积分: {balance_after} 积分")
                                    print("="*60)
                                else:
                                    print("="*60)
                                    print("🎉 下载成功！")
                                    print("="*60)
                                    print(f"📎 下载链接: {oss_url}")
                                    print(f"⏰ 有效期: 24小时")
                                    print("="*60)
                            except:
                                print("="*60)
                                print("🎉 下载成功！")
                                print("="*60)
                                print(f"📎 下载链接: {oss_url}")
                                print(f"⏰ 有效期: 24小时")
                                print("="*60)
                        else:
                            print("="*60)
                            print("🎉 下载成功！")
                            print("="*60)
                            print(f"📎 下载链接: {oss_url}")
                            print(f"⏰ 有效期: 24小时")
                            print("="*60)
                        break
                    elif status == 3 or status == 'failed' or status == 'error':
                        error = status_data.get('error') or status_data.get('message', '未知错误')
                        print()
                        print(f"❌ 下载失败: {error}")
                        break
                    else:
                        # Show progress
                        status_text = {0: "等待中", 1: "下载中"}.get(status, "处理中")
                        print(f"  📥 {status_text}... 进度: {progress}")
                        time.sleep(5)
                        attempt += 1
                else:
                    print(f"  ⚠️  查询失败: {response.status_code}")
                    break
            except Exception as e:
                time.sleep(5)
                attempt += 1

        if attempt >= max_attempts:
            print()
            print("⏱️  下载超时，请稍后查看任务状态")
            print(f"任务ID: {task_id}")
    else:
        error_msg = response.text
        try:
            error_data = response.json()
            error_msg = error_data.get('message', error_msg)
        except:
            pass
        print(f"  ❌ 任务创建失败: {response.status_code}")
        print(f"  错误信息: {error_msg}")

except Exception as e:
    print(f"  ❌ 请求失败: {e}")
    import traceback
    traceback.print_exc()