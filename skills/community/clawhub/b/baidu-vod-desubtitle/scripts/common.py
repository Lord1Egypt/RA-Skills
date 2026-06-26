#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度智能云 VOD 字幕擦除 - 公共模块

包含：
1. BCE v1 签名认证
2. 媒资上传功能
3. 字幕擦除任务管理（创建/查询/删除）
4. 网盘交互功能
"""

import os
import sys
import hmac
import hashlib
import time
import urllib.parse
import requests
import subprocess
import json
from datetime import datetime, timezone

# API 配置
HOST = "vod.bj.baidubce.com"
BASE_URL = f"https://{HOST}"


# ==================== 凭证管理 ====================

def get_credentials():
    """
    获取 AK/SK 凭证
    
    Returns:
        tuple: (access_key, secret_key)
    
    Raises:
        SystemExit: 未配置凭证时退出
    """
    ak = os.environ.get("BAIDU_VOD_AK", "")
    sk = os.environ.get("BAIDU_VOD_SK", "")
    
    if not ak or not sk:
        print("\n" + "=" * 50)
        print("⚠️  未检测到百度云 VOD 凭证，请先设置环境变量：")
        print()
        print("  export BAIDU_VOD_AK='你的 Access Key'")
        print("  export BAIDU_VOD_SK='你的 Secret Key'")
        print()
        print("💡 提示：AK/SK 可在百度智能云控制台 → 右上角头像 →")
        print("       'Access Key 管理' 中获取。")
        print("=" * 50 + "\n")
        sys.exit(1)
    
    return ak, sk


# ==================== 签名相关 ====================

def get_timestamp():
    """生成 ISO 8601 格式的时间"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_hexdigest(s):
    """计算 SHA256 hex digest"""
    if isinstance(s, str):
        s = s.encode('utf-8')
    return hashlib.sha256(s).hexdigest()


def hmac_sha256_hex(key, msg):
    """计算 HMAC-SHA256，返回 hex"""
    if isinstance(key, str):
        key = key.encode('utf-8')
    if isinstance(msg, str):
        msg = msg.encode('utf-8')
    return hmac.new(key, msg, hashlib.sha256).hexdigest()


def uri_encode(value, encode_slash=False):
    """URL 编码"""
    if value is None:
        return ""
    encoded = urllib.parse.quote(str(value), safe='')
    encoded = encoded.replace('+', '%20')
    encoded = encoded.replace('*', '%2A')
    encoded = encoded.replace('%7E', '~')
    if not encode_slash:
        encoded = encoded.replace('%2F', '/')
    return encoded


def normalize_query_string(query):
    """规范化 query string"""
    if not query:
        return ""
    if query.startswith('?'):
        query = query[1:]
    pairs = query.split('&')
    normalized = []
    for pair in pairs:
        if not pair:
            continue
        idx = pair.find('=')
        if idx < 0:
            key = pair
            value = ""
        else:
            key = pair[:idx]
            value = pair[idx + 1:]
        normalized.append(f"{uri_encode(key, False)}={uri_encode(value, False)}")
    normalized.sort()
    return '&'.join(normalized)


def sign_bce_v1(method, path, query, headers, access_key, secret_key, x_bce_date, expiration_in_seconds=1800):
    """BCE v1 签名"""
    auth_string_prefix = f"bce-auth-v1/{access_key}/{x_bce_date}/{expiration_in_seconds}"
    signing_key = hmac_sha256_hex(secret_key, auth_string_prefix)
    
    signed_header_keys = []
    for header_name in headers.keys():
        h = header_name.lower()
        if h == 'host' or h == 'content-length' or h.startswith('x-bce-'):
            signed_header_keys.append(h)
    signed_header_keys.sort()
    
    canonical_header_items = []
    for header_name in signed_header_keys:
        value = None
        for k in headers.keys():
            if k.lower() == header_name.lower():
                value = headers[k]
                break
        if value is None:
            value = ""
        item = f"{uri_encode(header_name, False)}:{uri_encode(value.strip(), False)}"
        canonical_header_items.append(item)
    canonical_headers = '\n'.join(canonical_header_items)
    
    normalized_query = normalize_query_string(query) if query else ""
    canonical_request = f"{method.upper()}\n{path}\n{normalized_query}\n{canonical_headers}"
    
    signature = hmac_sha256_hex(signing_key, canonical_request)
    signed_headers = ';'.join(signed_header_keys)
    authorization = f"{auth_string_prefix}/{signed_headers}/{signature}"
    
    return authorization


# ==================== API 请求 ====================

def request_vod(method, uri, ak, sk, params=None, json_data=None, query=None, debug=False):
    """发送 VOD API 请求"""
    # 将 params 转换为 query string 用于签名
    if params and not query:
        query_parts = []
        for key, value in sorted(params.items()):
            if value is not None:
                query_parts.append(f"{key}={value}")
        query = "&".join(query_parts)
    
    url = f"{BASE_URL}{uri}"
    x_bce_date = get_timestamp()
    
    headers = {
        "Host": HOST,
        "x-bce-date": x_bce_date,
    }
    
    authorization = sign_bce_v1(method, uri, query, headers, ak, sk, x_bce_date, 1800)
    
    headers["Authorization"] = authorization
    headers["Content-Type"] = "application/json; charset=utf-8"
    headers["accept"] = "application/json"
    
    if debug:
        print(f"请求: {method} {uri}")
        if query:
            print(f"Query: {query}")
        if json_data:
            print(f"Body: {json.dumps(json_data, ensure_ascii=False, indent=2)}")
    
    if method == "GET":
        response = requests.get(url, headers=headers, params=params, timeout=30)
    elif method == "POST":
        response = requests.post(url, headers=headers, json=json_data, timeout=30)
    elif method == "PUT":
        response = requests.put(url, headers=headers, json=json_data, timeout=30)
    else:
        raise ValueError(f"不支持的 HTTP 方法: {method}")
    
    if debug:
        print(f"响应状态: {response.status_code}")
        if response.text:
            print(f"响应内容: {response.text[:500]}")
    
    return response


# ==================== 媒资上传 ====================

def apply_upload(ak, sk, video_name, debug=False):
    """申请上传"""
    uri = "/v2/medias/upload"
    json_data = {
        "name": video_name,
        "container": "mp4",
        "isMultipartUpload": False
    }
    response = request_vod("POST", uri, ak, sk, json_data=json_data, debug=debug)
    
    if response.status_code == 200:
        result = response.json()
        return result.get("urls", [])[0], result.get("sessionKey")
    else:
        raise Exception(f"申请上传失败: {response.text}")


def upload_file(upload_url, video_path, debug=False):
    """上传文件（流式上传，避免大文件 OOM）"""
    file_size = os.path.getsize(video_path) / (1024 * 1024)
    if debug:
        print(f"文件大小: {file_size:.2f} MB，使用流式上传...")

    headers = {"Content-Type": "video/mp4"}
    with open(video_path, 'rb') as f:
        response = requests.put(upload_url, data=f, headers=headers, timeout=600)

    if response.status_code in [200, 100]:
        if debug:
            print("文件上传成功!")
        return True
    else:
        raise Exception(f"文件上传失败: {response.text}")


def complete_upload(ak, sk, session_key, debug=False):
    """完成上传"""
    uri = "/v2/medias/complete_upload"
    json_data = {
        "sessionKey": session_key,
        "isMultipartUpload": False
    }
    response = request_vod("POST", uri, ak, sk, json_data=json_data, debug=debug)
    
    if response.status_code == 200:
        result = response.json()
        return result.get("mediaId")
    else:
        raise Exception(f"完成上传失败: {response.text}")


def upload_media(ak, sk, video_path, debug=False):
    """完整的媒资上传流程"""
    video_name = os.path.basename(video_path)
    
    if debug:
        print("[1/3] 申请上传...")
    upload_url, session_key = apply_upload(ak, sk, video_name, debug=debug)
    
    if debug:
        print("[2/3] 上传文件...")
    upload_file(upload_url, video_path, debug=debug)
    
    if debug:
        print("[3/3] 完成上传...")
    media_id = complete_upload(ak, sk, session_key, debug=debug)
    
    if debug:
        print(f"  ✓ 媒资ID: {media_id}")
    
    return media_id


# ==================== 字幕擦除任务管理 ====================

def create_desubtitle_task(ak, sk, media_id, subtitle_type="global", model_type="v4", 
                           desubtitle_params=None, debug=False):
    """
    创建字幕擦除任务
    
    Args:
        ak: Access Key
        sk: Secret Key
        media_id: 媒资ID
        subtitle_type: 字幕擦除类型 (global/dialog/manual)
        model_type: 模型类型 (v3/v4)
        desubtitle_params: 自定义参数列表
            [
                {
                    "startTimeInMillisecond": int,
                    "endTimeInMillisecond": int,
                    "areaList": [
                        {"x": float, "y": float, "width": float, "height": float}
                    ]
                }
            ]
    
    Returns:
        str: 任务ID
    """
    uri = "/v2/desubtitle"
    json_data = {
        "mediaId": media_id,
        "subtitleType": subtitle_type,
        "modelType": model_type
    }
    
    if desubtitle_params:
        json_data["desubtitleParams"] = desubtitle_params
    
    response = request_vod("POST", uri, ak, sk, json_data=json_data, debug=debug)
    
    if response.status_code == 200:
        return response.json().get("taskId")
    else:
        raise Exception(f"创建字幕擦除任务失败: {response.text}")


def query_desubtitle_tasks(ak, sk, task_id=None, media_id=None, status=None, 
                           marker=None, max_size=10, begin_time=None, end_time=None,
                           sort_by="-CREATE_TIME", debug=False):
    """
    查询字幕擦除任务列表
    
    Args:
        ak: Access Key
        sk: Secret Key
        task_id: 任务ID筛选
        media_id: 媒资ID筛选
        status: 状态筛选 (READY/RUNNING/FINISHED)
        marker: 分页游标
        max_size: 分页大小
        begin_time: 开始时间
        end_time: 结束时间
        sort_by: 排序方式 (CREATE_TIME/-CREATE_TIME)
    
    Returns:
        dict: {"data": [...], "marker": str, "isTruncated": bool}
    """
    uri = "/v2/desubtitle/list"
    params = {"maxSize": max_size, "sortBy": sort_by}
    
    if task_id:
        params["taskId"] = task_id
    if media_id:
        params["mediaId"] = media_id
    if status:
        params["status"] = status
    if marker:
        params["marker"] = marker
    if begin_time:
        params["beginTime"] = begin_time
    if end_time:
        params["endTime"] = end_time
    
    response = request_vod("GET", uri, ak, sk, params=params, debug=debug)
    
    if response.status_code == 200:
        result = response.json()
        return {
            "data": result.get("data", []),
            "marker": result.get("marker"),
            "isTruncated": result.get("isTruncated", False)
        }
    else:
        raise Exception(f"查询字幕擦除任务失败: {response.text}")


def query_desubtitle_task(ak, sk, task_id, debug=False):
    """
    查询单个字幕擦除任务
    
    Returns:
        dict: {"taskId", "mediaId", "status", "targetUrl", "coverUrl"}
    """
    result = query_desubtitle_tasks(ak, sk, task_id=task_id, debug=debug)
    data = result.get("data", [])
    if data:
        task_info = data[0]
        return {
            "taskId": task_info.get("taskId"),
            "mediaId": task_info.get("mediaId"),
            "status": task_info.get("status"),
            "targetUrl": task_info.get("targetUrl"),
            "coverUrl": task_info.get("coverUrl")
        }
    return None


def delete_desubtitle_tasks(ak, sk, task_ids, debug=False):
    """
    删除字幕擦除任务
    
    Args:
        task_ids: 任务ID列表
    
    Returns:
        bool: 是否成功
    """
    uri = "/v2/desubtitle/batchDelete"
    json_data = {"taskIds": task_ids if isinstance(task_ids, list) else [task_ids]}
    
    response = request_vod("POST", uri, ak, sk, json_data=json_data, debug=debug)
    
    if response.status_code == 200:
        return True
    else:
        raise Exception(f"删除字幕擦除任务失败: {response.text}")


# ==================== 任务等待 ====================

def wait_for_task(ak, sk, task_id, max_retries=120, interval=10, debug=False):
    """
    等待字幕擦除任务完成
    
    Args:
        ak: Access Key
        sk: Secret Key
        task_id: 任务ID
        max_retries: 最大重试次数
        interval: 检查间隔（秒）
    
    Returns:
        dict: 任务结果
    """
    for i in range(max_retries):
        time.sleep(interval)

        result = query_desubtitle_task(ak, sk, task_id, debug=False)
        
        if result:
            status = result.get("status")
            if debug:
                print(f"  状态: {status} ({i+1}/{max_retries})")
            
            if status in ["FINISHED", "SUCCESS"]:
                return result
            elif status in ["READY", "RUNNING"]:
                continue
            else:
                if debug:
                    print(f"任务状态异常: {status}")
                return result
    
    if debug:
        print("任务超时未完成")
    return None


# ==================== 网盘交互 ====================

def check_bdpan_installed():
    """检查 bdpan 是否安装"""
    try:
        result = subprocess.run(
            ["bdpan", "version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except:
        return False


def check_bdpan_logged_in():
    """检查 bdpan 是否已登录"""
    try:
        result = subprocess.run(
            ["bdpan", "whoami"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0 and "已登录" in result.stdout
    except:
        return False


def download_from_netdisk(remote_path, local_path, debug=False):
    """从网盘下载文件"""
    cmd = ["bdpan", "download", remote_path, local_path]
    if debug:
        print(f"执行: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    
    if result.returncode == 0:
        if debug:
            print(f"✓ 下载成功: {local_path}")
        return True
    else:
        if debug:
            print(f"✗ 下载失败: {result.stderr}")
        return False


def upload_to_netdisk(local_path, remote_path, debug=False):
    """上传文件到网盘"""
    cmd = ["bdpan", "upload", local_path, remote_path]
    if debug:
        print(f"执行: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    
    if result.returncode == 0:
        if debug:
            print(f"✓ 上传成功: {remote_path}")
        return True
    else:
        if debug:
            print(f"✗ 上传失败: {result.stderr}")
        return False


def list_netdisk_files(path="", debug=False):
    """列出网盘文件"""
    cmd = ["bdpan", "ls", path, "--json"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    
    if result.returncode == 0:
        try:
            return json.loads(result.stdout)
        except:
            return None
    return None


# ==================== 文件下载 ====================

def download_result(url, output_path, debug=False):
    """下载处理结果"""
    if debug:
        print(f"下载: {url}")
        print(f"保存到: {output_path}")
    
    response = requests.get(url, timeout=300)
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        if debug:
            print(f"✓ 下载完成: {output_path}")
        return True
    else:
        if debug:
            print(f"✗ 下载失败: HTTP {response.status_code}")
        return False


# ==================== 辅助函数 ====================

def parse_area_string(area_str):
    """
    解析区域字符串，支持两种格式：
    - 纯坐标: "x,y,width,height"
    - 带时间戳: "x,y,width,height,start_ms,end_ms"

    Args:
        area_str: 区域字符串

    Returns:
        dict: {
            "x": float, "y": float, "width": float, "height": float,
            "has_time": bool,
            "startTimeInMillisecond"?: int,
            "endTimeInMillisecond"?: int
        }
        has_time=True 表示该区域自带时间范围，需要在 process_video 中单独成 param
        若格式非法返回 None
    """
    parts = area_str.split(",")
    if len(parts) < 4:
        return None

    try:
        result = {
            "x": float(parts[0]),
            "y": float(parts[1]),
            "width": float(parts[2]),
            "height": float(parts[3]),
            "has_time": False,
        }
    except ValueError:
        return None

    # 支持带时间戳的 6 参数格式: x,y,w,h,start,end
    if len(parts) >= 6:
        try:
            result["startTimeInMillisecond"] = int(parts[4])
            result["endTimeInMillisecond"] = int(parts[5])
            result["has_time"] = True
        except ValueError:
            return None

    return result
