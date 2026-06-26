#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度智能云 VOD 视频翻译 - 公共模块

包含：
1. BCE v1 签名认证
2. 媒资上传功能
3. 视频翻译项目管理（创建/查询/删除）
4. 视频翻译任务管理（创建/修改/查询）
5. 网盘交互功能
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


# ==================== 视频翻译项目管理 ====================

def create_translate_project(ak, sk, name=None, description="", project_type="ShortSeries", debug=False):
    """
    创建翻译项目
    
    Args:
        ak: Access Key
        sk: Secret Key
        name: 项目名称
        description: 项目描述
        project_type: 项目类型
            - ShortSeries: 短剧场景（默认）
            - Ecommerce: 电商场景
        debug: 调试模式
    
    Returns:
        str: 项目ID
    """
    project_name = name or f"translate_{int(time.time())}"
    uri = "/v2/translation/project"
    json_data = {
        "name": project_name,
        "description": description,
        "type": project_type
    }
    response = request_vod("POST", uri, ak, sk, json_data=json_data, debug=debug)
    
    if response.status_code == 200:
        return response.json().get("projectId")
    else:
        raise Exception(f"创建翻译项目失败: {response.text}")


def query_translate_projects(ak, sk, project_id=None, name=None, 
                             page_no=1, page_size=10, sort_by="CREATE_TIME", debug=False):
    """
    查询翻译项目列表
    
    Args:
        ak: Access Key
        sk: Secret Key
        project_id: 项目ID筛选
        name: 项目名称筛选
        page_no: 页码
        page_size: 每页大小
        sort_by: 排序方式 (CREATE_TIME/-CREATE_TIME)
    
    Returns:
        dict: 查询结果
    """
    uri = "/v2/translation/projects"
    params = {"pageNo": page_no, "pageSize": page_size, "sortBy": sort_by}
    
    if project_id:
        params["projectId"] = project_id
    if name:
        params["name"] = name
    
    response = request_vod("GET", uri, ak, sk, params=params, debug=debug)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"查询翻译项目失败: {response.text}")


def delete_translate_projects(ak, sk, project_ids, debug=False):
    """
    删除翻译项目
    
    Args:
        ak: Access Key
        sk: Secret Key
        project_ids: 项目ID列表
    
    Returns:
        bool: 是否成功
    """
    uri = "/v2/translation/projects/delete"
    json_data = {"projectIdList": project_ids if isinstance(project_ids, list) else [project_ids]}
    
    response = request_vod("POST", uri, ak, sk, json_data=json_data, debug=debug)
    
    if response.status_code == 200:
        return True
    else:
        raise Exception(f"删除翻译项目失败: {response.text}")


# ==================== 视频翻译任务管理 ====================

# 支持的语言
SUPPORTED_LANGUAGES = {
    "zh": ("中文", "zh-CN"),
    "zh-TW": ("中文繁体", "zh-TW"),
    "en": ("英语", "en-US"),
    "ja": ("日语", "ja-JP"),
    "ko": ("韩语", "ko-KR"),
    "de": ("德语", "de-DE"),
    "fr": ("法语", "fr-FR"),
    "ru": ("俄语", "ru-RU"),
    "th": ("泰语", "th-TH"),
    "ar": ("阿拉伯语", "ar-SA"),
    "es": ("西班牙语", "es-ES"),
    "pt": ("葡萄牙语", "pt-PT")
}


def create_translate_task(ak, sk, project_id, media_id_list, source_lang, target_lang,
                          translation_types=None, subtitle_config=None, tts_config=None, debug=False):
    """
    创建翻译任务
    
    Args:
        ak: Access Key
        sk: Secret Key
        project_id: 项目ID
        media_id_list: 媒资ID列表
        source_lang: 源语言 (zh/en/...)
        target_lang: 目标语言 (zh/en/...)
        translation_types: 翻译类型列表 ["subtitle", "speech"]
        subtitle_config: 字幕配置
            {
                "recognitionType": "OCR/ASR/USER",
                "ocrConfig": {"areaList": [...], "regionIOU": 1},
                "textTypeList": ["dialog", "castName", ...],
                "targetSubtitleCompose": True,
                "desubtitleConfig": {
                    "modelType": "v3/v4",
                    "desubtitleType": "global/dialog/manual",
                    "areaList": [...]
                },
                "fontConfig": {...}
            }
        tts_config: 配音配置
            {
                "type": "VOICE_CLONE/AI_DUB",
                "voiceList": [{"voiceId": "..."}]
            }
    
    Returns:
        list: 任务创建结果列表
    """
    # 语言代码转换
    source = SUPPORTED_LANGUAGES.get(source_lang, (source_lang, source_lang))[1]
    target = SUPPORTED_LANGUAGES.get(target_lang, (target_lang, target_lang))[1]
    
    uri = "/v2/translation/tasks"
    
    # 翻译配置
    translation_config = {
        "sourceLanguage": source,
        "targetLanguage": target,
        "translationTypeList": translation_types or ["subtitle"]
    }
    
    if tts_config:
        translation_config["ttsConfig"] = tts_config
    
    # 字幕配置
    default_subtitle_config = {
        "recognitionType": "OCR",
        "targetSubtitleCompose": True
    }
    
    if subtitle_config:
        default_subtitle_config.update(subtitle_config)
    
    json_data = {
        "projectId": project_id,
        "mediaIdList": media_id_list if isinstance(media_id_list, list) else [media_id_list],
        "translationConfig": translation_config,
        "subtitleConfig": default_subtitle_config
    }
    
    response = request_vod("POST", uri, ak, sk, json_data=json_data, debug=debug)
    
    if response.status_code == 200:
        result = response.json()
        return result.get("translationTaskCreateResultList", [])
    else:
        raise Exception(f"创建翻译任务失败: {response.text}")


def update_translate_task(ak, sk, task_id, update_type, subtitle_file, debug=False):
    """
    修改翻译任务
    
    Args:
        ak: Access Key
        sk: Secret Key
        task_id: 任务ID
        update_type: 更新类型 (sourceSubtitle/targetSubtitle)
        subtitle_file: SRT字幕文件内容
    
    Returns:
        str: 新任务ID
    """
    uri = "/v2/translation/task"
    json_data = {
        "taskId": task_id,
        "updateType": update_type,
        "subtitleFile": subtitle_file
    }
    
    response = request_vod("PUT", uri, ak, sk, json_data=json_data, debug=debug)
    
    if response.status_code == 200:
        return response.json().get("taskId")
    else:
        raise Exception(f"修改翻译任务失败: {response.text}")


def query_translate_tasks(ak, sk, project_id, task_id=None, media_id=None,
                          marker=None, max_size=10, debug=False):
    """
    查询项目中所有翻译任务
    
    Args:
        ak: Access Key
        sk: Secret Key
        project_id: 项目ID
        task_id: 任务ID筛选
        media_id: 媒资ID筛选
        marker: 分页游标
        max_size: 分页大小
    
    Returns:
        dict: 查询结果
    """
    uri = f"/v2/translation/project/{project_id}/tasks"
    params = {"maxSize": max_size}
    
    if task_id:
        params["taskId"] = task_id
    if media_id:
        params["mediaId"] = media_id
    if marker:
        params["marker"] = marker
    
    response = request_vod("GET", uri, ak, sk, params=params, debug=debug)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"查询翻译任务失败: {response.text}")


def query_translate_task(ak, sk, task_id, project_id, debug=False):
    """查询单个翻译任务"""
    result = query_translate_tasks(ak, sk, project_id, task_id=task_id, debug=debug)
    data = result.get("data", [])
    if data:
        task_info = data[0]
        return {
            "taskId": task_info.get("taskId"),
            "projectId": task_info.get("projectId"),
            "mediaId": task_info.get("mediaInfo", {}).get("mediaId"),
            "status": task_info.get("status"),
            "targetUrl": task_info.get("url"),
            "coverUrl": task_info.get("coverUrl"),
            "desubtitleUrl": task_info.get("desubtitleUrl"),
            "errMsg": task_info.get("errMsg"),
            "name": task_info.get("name"),
            "translationConfig": task_info.get("translationConfig"),
            "subtitleConfig": task_info.get("subtitleConfig"),
            "createTime": task_info.get("createTime"),
            "updateTime": task_info.get("updateTime")
        }
    return None


# ==================== 任务等待 ====================

def wait_for_task(ak, sk, task_id, project_id, max_retries=120, interval=10, debug=False):
    """
    等待翻译任务完成
    
    Args:
        ak: Access Key
        sk: Secret Key
        task_id: 任务ID
        project_id: 项目ID
        max_retries: 最大重试次数
        interval: 检查间隔（秒）
    
    Returns:
        dict: 任务结果
    """
    import time

    for i in range(max_retries):
        time.sleep(interval)
        
        result = query_translate_task(ak, sk, task_id, project_id, debug=False)
        
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
                    if result.get("errMsg"):
                        print(f"错误信息: {result.get('errMsg')}")
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
    解析区域字符串
    
    Args:
        area_str: 格式 "x,y,width,height" 或 "x,y,width,height,start,end"
    
    Returns:
        dict: 区域配置
    """
    parts = area_str.split(",")
    if len(parts) >= 4:
        area = {
            "x": int(parts[0]),
            "y": int(parts[1]),
            "width": int(parts[2]),
            "height": int(parts[3])
        }
        if len(parts) >= 6:
            area["startTimeInMillisecond"] = int(float(parts[4]) * 1000)
            area["endTimeInMillisecond"] = int(float(parts[5]) * 1000)
        return area
    return None


def parse_srt_file(file_path):
    """
    读取 SRT 字幕文件
    
    Args:
        file_path: SRT 文件路径
    
    Returns:
        str: SRT 内容字符串
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def build_font_config(family="Hei", size=None, color="#FFFFFFFF", outline_color="#000000FF",
                       outline_thickness=1, bold=False, italic=False, underline=False,
                       strike_out=False, alignment="center", spacing=0, line_spacing=0, 
                       bg_color="#00000000", font_bg_color="#00000000", padding=0):
    """
    构建字体配置
    
    Args:
        family: 字体名称 (Hei/Song/Kai)
        size: 字号（像素），None 则与原字幕同大小
        color: 字体颜色 (#RRGGBBAA)
        outline_color: 描边颜色
        outline_thickness: 描边宽度
        bold: 是否加粗
        italic: 是否斜体
        underline: 是否下划线
        strike_out: 是否删除线
        alignment: 对齐方式 (left/center/right)
        spacing: 字间距
        line_spacing: 行间距（字号的倍数）
        bg_color: 字幕区域背景颜色
        font_bg_color: 字体逐行背景颜色
        padding: 内边距
    
    Returns:
        dict: 字体配置
    """
    font_config = {
        "color": bg_color,
        "padding": padding,
        "font": {
            "family": family,
            "alignment": alignment,
            "color": color,
            "outlineColor": outline_color,
            "outlineThickness": outline_thickness,
            "bold": bold,
            "italic": italic,
            "underline": underline,
            "strikeOut": strike_out,
            "spacing": spacing,
            "lineSpacing": line_spacing,
            "bgColor": font_bg_color
        }
    }
    
    if size:
        font_config["font"]["size"] = size
    
    return font_config


def build_ocr_config(area_list=None, region_iou=1):
    """
    构建 OCR 识别配置
    
    Args:
        area_list: OCR 识别区域列表
        region_iou: OCR 区域与字幕区域的重叠阈值（0或1，默认1）
            1 表示需完全覆盖才识别
            0 表示有交集即识别
    
    Returns:
        dict: OCR 配置
    """
    ocr_config = {"regionIOU": region_iou}
    if area_list:
        ocr_config["areaList"] = area_list
    return ocr_config


def build_full_font_config(dialog_config=None, cast_name_config=None, 
                           cast_description_config=None, other_config=None):
    """
    构建完整字体配置（支持不同类型文字）
    
    Args:
        dialog_config: 对白字幕字体配置
        cast_name_config: 角色名字体配置
        cast_description_config: 角色描述字体配置
        other_config: 其他文字字体配置
    
    Returns:
        dict: 完整字体配置
    """
    font_config = {}
    
    if dialog_config:
        font_config["dialog"] = dialog_config
    if cast_name_config:
        font_config["castName"] = cast_name_config
    if cast_description_config:
        font_config["castDescription"] = cast_description_config
    if other_config:
        font_config["other"] = other_config
    
    # 默认至少有 dialog 配置
    if not font_config:
        font_config["dialog"] = build_font_config()
    
    return font_config
