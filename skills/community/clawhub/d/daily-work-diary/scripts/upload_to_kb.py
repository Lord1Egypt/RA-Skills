#!/usr/bin/env python3

import os
import sys
import json
import argparse
from pathlib import Path
import datetime
import hashlib
import hmac
import time
import urllib.parse
import urllib.request
from http.client import HTTPSConnection

# --- 从 preflight_check.py 导入的常量 ---

# 扩展名 → media_type + content_type 映射
EXT_MAP = {
    'pdf': {'media_type': 1, 'content_type': 'application/pdf'},
    'doc': {'media_type': 3, 'content_type': 'application/msword'},
    'docx': {'media_type': 3, 'content_type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'},
    'ppt': {'media_type': 4, 'content_type': 'application/vnd.ms-powerpoint'},
    'pptx': {'media_type': 4, 'content_type': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'},
    'xls': {'media_type': 5, 'content_type': 'application/vnd.ms-excel'},
    'xlsx': {'media_type': 5, 'content_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'},
    'csv': {'media_type': 5, 'content_type': 'text/csv'},
    'md': {'media_type': 7, 'content_type': 'text/markdown'},
    'markdown': {'media_type': 7, 'content_type': 'text/markdown'},
    'png': {'media_type': 9, 'content_type': 'image/png'},
    'jpg': {'media_type': 9, 'content_type': 'image/jpeg'},
    'jpeg': {'media_type': 9, 'content_type': 'image/jpeg'},
    'webp': {'media_type': 9, 'content_type': 'image/webp'},
    'txt': {'media_type': 13, 'content_type': 'text/plain'},
    'xmind': {'media_type': 14, 'content_type': 'application/x-xmind'},
    'mp3': {'media_type': 15, 'content_type': 'audio/mpeg'},
    'm4a': {'media_type': 15, 'content_type': 'audio/x-m4a'},
    'wav': {'media_type': 15, 'content_type': 'audio/wav'},
    'aac': {'media_type': 15, 'content_type': 'audio/aac'},
    'html': {'media_type': 20, 'content_type': 'text/html'},
    'epub': {'media_type': 21, 'content_type': 'application/epub+zip'},
}

# 按 media_type 设置大小限制（字节）
MB = 1024 * 1024
SIZE_LIMITS = {
    5: 10 * MB,   # Excel / CSV
    7: 10 * MB,   # Markdown
    13: 10 * MB,  # TXT
    14: 10 * MB,  # Xmind
    20: 20 * MB,  # HTML
    21: 50 * MB,  # EPUB
    9: 30 * MB,   # 图片
}
DEFAULT_SIZE_LIMIT = 200 * MB  # PDF、Word、PPT、音频等默认限制

# 明确不支持的扩展名
UNSUPPORTED_VIDEO_EXT = {'mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm', 'm4v', 'rmvb', 'rm', '3gp'}

MAGIC_NUMBERS = [
    # PDF
    (b'%PDF', {'media_type': 1, 'content_type': 'application/pdf'}),
    
    # 图片
    (b'\x89PNG', {'media_type': 9, 'content_type': 'image/png'}),
    (b'\xFF\xD8\xFF', {'media_type': 9, 'content_type': 'image/jpeg'}),
    (b'GIF8', {'media_type': 9, 'content_type': 'image/gif'}),
    (b'BM', {'media_type': 9, 'content_type': 'image/bmp'}),
    (b'RIFF', {'media_type': 9, 'content_type': 'image/webp'}),  # WebP 以 RIFF....WEBP 开头
    
    # Office文档（基于ZIP格式）
    (b'PK\x03\x04', {'media_type': 3, 'content_type': None}),  # docx/xlsx/pptx 是ZIP格式,需要进一步检查
    
    # 音频
    (b'ID3', {'media_type': 15, 'content_type': 'audio/mpeg'}),  # MP3
    (b'\xFF\xFB', {'media_type': 15, 'content_type': 'audio/mpeg'}),  # MP3
    (b'\xFF\xFA', {'media_type': 15, 'content_type': 'audio/mpeg'}),  # MP3
    (b'\xFF\xF3', {'media_type': 15, 'content_type': 'audio/mpeg'}),  # MP3
    (b'RIFF', {'media_type': 15, 'content_type': 'audio/wav'}),  # WAV
    (b'\xFF\xF1', {'media_type': 15, 'content_type': 'audio/aac'}),  # AAC
    (b'\xFF\xF9', {'media_type': 15, 'content_type': 'audio/aac'}),  # AAC
]

# --- 从 preflight_check.py 导入的辅助函数 ---

def format_size(bytes_val):
    """将字节数转换为人类可读的大小格式"""
    if bytes_val < MB:
        return f"{bytes_val / 1024:.1f} KB"
    return f"{bytes_val / MB:.1f} MB"

def detect_by_magic_number(file_path):
    """
    通过读取魔数（文件头）检测文件类型
    返回: (media_type, content_type) 元组,如果未知则返回 None
    """
    try:
        with open(file_path, 'rb') as f:
            header = f.read(12)  # 读取前12个字节用于魔数检测
        
        for magic, type_info in MAGIC_NUMBERS:
            if header.startswith(magic):
                media_type = type_info['media_type']
                content_type = type_info['content_type']
                
                # 对ZIP格式的文档进行特殊处理（docx/xlsx/pptx）
                if content_type is None and magic == b'PK\x03\x04':
                    # 读取更多内容以检查Office签名
                    f.seek(0)
                    full_header = f.read(1024)
                    
                    if b'[Content_Types].xml' in full_header:
                        # 这是一个Office文档,但需要更多信息
                        # 暂时默认为docx
                        return (3, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                
                return (media_type, content_type) if content_type else None
    except Exception:
        pass
    
    return None

def check_file(file_path):
    file_path = os.path.abspath(file_path)
    file_name = os.path.basename(file_path)
    
    # 提取文件扩展名
    ext_match = os.path.splitext(file_name)[1]
    ext = ext_match[1:].lower() if ext_match else ''
    
    base = {
        'file_path': file_path,
        'file_name': file_name,
        'file_ext': ext
    }
    
    # 1. 检查文件是否存在
    try:
        stat = os.stat(file_path)
    except FileNotFoundError:
        return {
            'pass': False,
            **base,
            'reason': '文件未找到'
        }
    except Exception as e:
        return {
            'pass': False,
            **base,
            'reason': f'访问文件出错: {e}'
        }
    
    # 2. 检查是否为不支持的视频类型（通过扩展名）
    if ext in UNSUPPORTED_VIDEO_EXT:
        return {
            'pass': False,
            **base,
            'reason': f"视频文件 (.{ext}) 不支持。仅在IMA桌面应用中支持。"
        }
    
    # 3. 解析 media_type 和 content_type
    #    首先尝试使用扩展名,然后降级为魔数检测
    media_type = None
    content_type = None
    
    ext_mapping = EXT_MAP.get(ext) if ext else None
    
    if ext_mapping:
        media_type = ext_mapping['media_type']
        content_type = ext_mapping['content_type']
    elif ext:
        # 提供了扩展名但无法识别,尝试使用魔数作为降级方案
        magic_result = detect_by_magic_number(file_path)
        if magic_result:
            media_type, content_type = magic_result
        else:
            return {
                'pass': False,
                **base,
                'reason': f"无法识别的文件扩展名 .{ext} 且文件签名未知。此文件类型不受支持。"
            }
    else:
        # 没有扩展名,尝试魔数检测
        magic_result = detect_by_magic_number(file_path)
        if magic_result:
            media_type, content_type = magic_result
        else:
            return {
                'pass': False,
                **base,
                'reason': '文件没有扩展名且文件签名未知。无法确定文件类型。'
            }
    
    # 4. 检查文件大小
    file_size = stat.st_size
    size_limit = SIZE_LIMITS.get(media_type, DEFAULT_SIZE_LIMIT)
    
    if file_size > size_limit:
        return {
            'pass': False,
            **base,
            'file_size': file_size,
            'media_type': media_type,
            'content_type': content_type,
            'reason': f"文件大小 {format_size(file_size)} 超过了该文件类型的 {format_size(size_limit)} 限制。"
        }
    
    # 5. 所有检查通过
    return {
        'pass': True,
        **base,
        'file_size': file_size,
        'media_type': media_type,
        'content_type': content_type,
    }

# --- 从 cos_upload.py 导入的辅助函数 ---

def hmac_sha1(key, data):
    """HMAC-SHA1签名"""
    if isinstance(key, str):
        key = key.encode('utf-8')
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hmac.new(key, data, hashlib.sha1).hexdigest()

def sha1(data):
    """SHA1哈希"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha1(data).hexdigest()

def build_authorization(secret_id, secret_key, method, pathname, headers, start_time, expired_time):
    key_time = f"{start_time};{expired_time}"
    
    # 1. SignKey = HMAC-SHA1(SecretKey, KeyTime)
    sign_key = hmac_sha1(secret_key, key_time)
    
    # 2. HttpString = method\npathname\nparams\nheaders\n
    # 对于PUT,没有查询参数；需要签名的头部：host, content-length
    header_keys = sorted(headers.keys())
    http_headers = '&'.join([f"{k.lower()}={urllib.parse.quote(headers[k])}" for k in header_keys])
    http_string = f"{method.lower()}\n{pathname}\n\n{http_headers}\n"
    
    # 3. StringToSign = sha1\nKeyTime\nSHA1(HttpString)\n
    string_to_sign = f"sha1\n{key_time}\n{sha1(http_string)}\n"
    
    # 4. Signature = HMAC-SHA1(SignKey, StringToSign)
    signature = hmac_sha1(sign_key, string_to_sign)
    
    # 5. 构建Authorization
    header_list = ';'.join([k.lower() for k in header_keys])
    return '&'.join([
        f"q-sign-algorithm=sha1",
        f"q-ak={secret_id}",
        f"q-sign-time={key_time}",
        f"q-key-time={key_time}",
        f"q-header-list={header_list}",
        f"q-url-param-list=",
        f"q-signature={signature}",
    ])

def upload(args):
    secret_id = args['secret-id']
    secret_key = args['secret-key']
    token = args['token']
    bucket = args['bucket']
    region = args['region']
    cos_key = args['cos-key']
    file_path = args['file']
    
    start_time = args.get('start-time', str(int(time.time())))
    expired_time = args.get('expired-time', str(int(time.time()) + 3600))
    
    # 读取文件内容
    with open(file_path, 'rb') as f:
        file_content = f.read()
    
    hostname = f"{bucket}.cos.{region}.myqcloud.com"
    pathname = f"/{cos_key}"
    
    # 需要签名的头部
    sign_headers = {
        'content-length': str(len(file_content)),
        'host': hostname,
    }
    
    authorization = build_authorization(
        secret_id, secret_key, 'PUT', pathname, 
        sign_headers, start_time, expired_time
    )
    
    # 使用check_file函数自动设置content-type
    if 'content-type' not in args:
        # 使用check_file函数检测文件类型
        check_result = check_file(file_path)
        if check_result['pass']:
            content_type = check_result['content_type']
            print(f"自动检测到文件类型: {content_type}")
        else:
            content_type = 'application/octet-stream'
            print(f"文件类型检测失败，使用默认类型: {content_type}")
    else:
        content_type = args['content-type']
    
    # 构建HTTP请求
    conn = HTTPSConnection(hostname, 443)
    
    headers = {
        'Content-Type': content_type,
        'Content-Length': str(len(file_content)),
        'Authorization': authorization,
        'x-cos-security-token': token,
    }
    
    try:
        conn.request('PUT', pathname, body=file_content, headers=headers)
        response = conn.getresponse()
        body = response.read().decode('utf-8')
        
        if 200 <= response.status < 300:
            return True
        else:
            raise Exception(f"COS upload failed (HTTP {response.status}): {body}")
    except Exception as e:
        raise Exception(f"COS upload error: {str(e)}")
    finally:
        conn.close()

def cos_upload(args):
    """
    腾讯云COS文件上传函数
    
    参数:
        args (dict): 包含以下键的字典:
            - secret-id: COS SecretId
            - secret-key: COS SecretKey  
            - token: 临时安全令牌
            - bucket: 存储桶名称
            - region: 区域
            - cos-key: COS对象键
            - file: 本地文件路径
            - start-time: 可选,开始时间戳(默认当前时间)
            - expired-time: 可选,过期时间戳(默认当前时间+3600秒)
            - content-type: 可选,Content-Type(默认自动检测)
    
    返回:
        bool: 上传是否成功
    """
    required_keys = ['secret-id', 'secret-key', 'token', 'bucket', 'region', 'cos-key', 'file']
    missing = [k for k in required_keys if k not in args]
    if missing:
        raise ValueError(f"Missing required arguments: {', '.join(missing)}")
    
    file_path = args['file']
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return upload(args)

# --- 从 imaapi.py 导入的函数 ---

def send_ima_api_request(api_path, body_str):
    # 检查必需的环境变量
    missing_vars = []
    if "IMA_OPENAPI_CLIENTID" not in os.environ:
        missing_vars.append("IMA_OPENAPI_CLIENTID")
    if "IMA_OPENAPI_APIKEY" not in os.environ:
        missing_vars.append("IMA_OPENAPI_APIKEY")
    
    if missing_vars:
        raise ValueError(
            f"未设置必需的环境变量: {', '.join(missing_vars)}\n"
            "获取方式：\n"
            "  1. 访问 https://ima.qq.com/agent-interface 获取 Client ID 和 API Key\n"
            "  2. 设置环境变量：\n"
            "     export IMA_OPENAPI_CLIENTID=\"your_client_id\"\n"
            "     export IMA_OPENAPI_APIKEY=\"your_api_key\""
        )
    
    client_id = os.environ["IMA_OPENAPI_CLIENTID"]
    api_key = os.environ["IMA_OPENAPI_APIKEY"]
    
    # 验证JSON格式
    try:
        json.loads(body_str)
    except json.JSONDecodeError:
        raise ValueError("JSON格式不正确")
    
    # 所有请求的base url
    url = f"https://ima.qq.com/{api_path}"
    headers = {
        "ima-openapi-clientid": client_id,
        "ima-openapi-apikey": api_key,
        "Content-Type": "application/json"
    }
    
    # 创建请求对象
    req = urllib.request.Request(
        url,
        data=body_str.encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    # 发送请求
    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8')

# --- 原有的 upload_file.py 函数 ---

def get_file_size(file_path):
    """获取文件大小"""
    try:
        return os.path.getsize(file_path)
    except OSError as e:
        raise FileNotFoundError(f"error in get file size: {e}")

def create_media(knowledge_base_id, filename, file_size, media_type, content_type):
    """创建媒体,获取COS上传凭证"""
    # 提取文件扩展名（无点号）
    file_ext = Path(filename).suffix.lower()
    if file_ext.startswith('.'):
        file_ext = file_ext[1:]
    
    body = {
        "media_type": media_type,
        "file_name": filename,
        "file_size": file_size,
        "content_type": content_type,
        "knowledge_base_id": knowledge_base_id,
        "file_ext": file_ext
    }
    
    result = send_ima_api_request("openapi/wiki/v1/create_media", json.dumps(body))
    response = json.loads(result)
    
    # 检查API响应是否包含错误信息
    if "code" in response and response["code"] != 0:
        raise Exception(f"{response}")
    
    return response["data"]["media_id"], response["data"]["cos_credential"]

def check_repeat_name(knowledge_base_id, filename, media_type, folder_id=None):
    """检查文件名是否重复，如果重复则添加时间戳后缀"""
    # 构建API请求体
    body = {
        "params": [{
            "name": filename,
            "media_type": media_type
        }],
        "knowledge_base_id": knowledge_base_id
    }
    
    # 添加folder_id参数（可选）
    if folder_id:
        body["folder_id"] = folder_id
    
    # 调用API检查重复名称
    result = send_ima_api_request("openapi/wiki/v1/check_repeated_names", json.dumps(body))
    response = json.loads(result)
    
    # 检查API响应是否包含错误信息
    if "code" in response and response["code"] != 0:
        raise Exception(f"检查重复名称失败: {response}")
    
    # 检查是否重名
    if response["data"]["results"][0]["is_repeated"]:
        # 重名，添加时间戳后缀
        file_stem = Path(filename).stem
        file_ext = Path(filename).suffix
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"{file_stem}_{timestamp}{file_ext}"
        print(f"文件名 '{filename}' 已存在，自动重命名为 '{new_filename}'")
        return new_filename
    
    # 不重名，返回原文件名
    return filename

def add_knowledge(knowledge_base_id, media_id, title, media_type, folder_id=None):
    """将已上传的文件关联到知识库"""
    body = {
        "media_type": media_type,
        "media_id": media_id,
        "title": title,
        "knowledge_base_id": knowledge_base_id,
    }
    
    # 添加folder_id参数（可选）
    if folder_id:
        body["folder_id"] = folder_id
    
    result = send_ima_api_request("openapi/wiki/v1/add_knowledge", json.dumps(body))
    response = json.loads(result)
    
    # 检查API响应是否包含错误信息
    if "code" in response and response["code"] != 0:
        raise Exception(f"{response}")
    
    return True

def upload_file_to_knowledge_base(file_path, knowledge_base_id, rename_filename=None, folder_id=None):

    
    # 1. 使用新函数检查文件并获取元数据
    check_result = check_file(file_path)
    
    # 检查文件是否通过验证
    if not check_result['pass']:
        raise ValueError(f"文件检查失败: {check_result.get('reason', '未知错误')}")
    
    # 从检查结果中提取文件元数据
    filename = Path(file_path).name
    
    # 如果提供了重命名参数,则使用重命名后的文件名
    if rename_filename:
        filename = rename_filename
    
    file_size = check_result['file_size']
    media_type = check_result['media_type']
    content_type = check_result['content_type']
    
    # 2. 检查文件名是否重复，如果重复则添加时间戳后缀
    filename = check_repeat_name(knowledge_base_id, filename, media_type, folder_id)
    
    # 3. 创建媒体,获取COS上传凭证
    media_id, cos_credential = create_media(knowledge_base_id, filename, file_size, media_type, content_type)
    
    # 4. 上传文件到COS
    cos_args = {
        'file': file_path,
        'secret-id': cos_credential['secret_id'],
        'secret-key': cos_credential['secret_key'],
        'token': cos_credential['token'],
        'bucket': cos_credential['bucket_name'],
        'region': cos_credential['region'],
        'cos-key': cos_credential['cos_key'],
        'content-type': content_type,
        'start-time': str(cos_credential['start_time']),
        'expired-time': str(cos_credential['expired_time'])
    }
    
    cos_upload(cos_args)
    
    # 5. 将已上传的文件关联到知识库
    success = add_knowledge(knowledge_base_id, media_id, filename, media_type, folder_id)
    
    return success

def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(
        description="将文件上传到知识库的工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument('--file-path', required=True, help='要上传的文件路径')
    parser.add_argument('--knowledge-base-id', required=True, help='目标知识库ID')
    parser.add_argument('--rename', help='重命名文件,指定上传后的文件名')
    parser.add_argument('--folder-id', help='目标文件夹ID')
    
    args = parser.parse_args()
    
    file_path = args.file_path
    knowledge_base_id = args.knowledge_base_id
    rename_filename = args.rename
    folder_id = args.folder_id
        
    try:
        # 执行上传
        success = upload_file_to_knowledge_base(file_path, knowledge_base_id, rename_filename, folder_id)
        
        if success:
            print(f"upload success {file_path} -> knowledge_base_id {knowledge_base_id}")
            sys.exit(0)
        else:
            print(f"upload failed: {file_path}", file=sys.stderr)
            sys.exit(1)
    
    except Exception as e:
        print(f"error occurred in upload: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()