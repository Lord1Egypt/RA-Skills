"""消息模块 - 增强版

支持文件发送、音频卡片、图片预览等功能
基于 feishu-file-sender 优化，增加 UTF-8 编码支持
"""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from fastapi import APIRouter, File, Form, UploadFile
from pydantic import BaseModel, Field

from feishu_supertoolkit.auth import feishu_request, get_tenant_access_token

router = APIRouter()


# ── 请求模型 ──────────────────────────────────────────────

class SendFileRequest(BaseModel):
    file_path: str = Field(..., description="文件路径")
    receive_id: str = Field(..., description="接收者 ID")
    receive_id_type: str = Field(default="open_id", description="ID 类型：open_id/user_id/email/chat_id")
    msg_type: str = Field(default="auto", description="消息类型：auto/image/file/interactive")


class SendTextRequest(BaseModel):
    receive_id: str = Field(..., description="接收者 ID")
    receive_id_type: str = Field(default="open_id", description="ID 类型")
    text: str = Field(..., description="文本内容（UTF-8 编码）")


# ── 工具函数 ──────────────────────────────────────────────

def convert_to_opus(input_path: str, output_path: str) -> bool:
    """将音频转换为 OPUS 格式"""
    try:
        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-c:a", "libopus",
            "-b:a", "64k",
            "-y",
            output_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.returncode == 0
    except Exception as e:
        print(f"FFmpeg 转换失败：{e}")
        return False


def get_audio_duration(file_path: str) -> int:
    """获取音频时长（秒）"""
    try:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return int(float(result.stdout.strip()))
    except Exception as e:
        print(f"获取音频时长失败：{e}")
    return 0


def detect_file_type(file_path: str) -> str:
    """根据文件扩展名检测文件类型"""
    ext = Path(file_path).suffix.lower()
    
    image_exts = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    audio_exts = {".mp3", ".wav", ".ogg", ".m4a", ".opus"}
    video_exts = {".mp4", ".mov", ".avi", ".mkv"}
    
    if ext in image_exts:
        return "image"
    elif ext in audio_exts:
        return "audio"
    elif ext in video_exts:
        return "video"
    else:
        return "file"


# ── 路由 ──────────────────────────────────────────────────

@router.post("/send-file", summary="发送文件")
def send_file(req: SendFileRequest) -> dict:
    """发送文件到飞书（支持图片、音频、视频、文档）
    
    - 图片：直接预览
    - 音频：自动转换为 OPUS，使用内嵌播放器卡片
    - 视频：文件卡片（大视频自动截取封面）
    - 其他：文件卡片
    """
    import requests
    from requests_toolbelt import MultipartEncoder
    
    file_path = req.file_path
    
    if not os.path.exists(file_path):
        raise Exception(f"文件不存在：{file_path}")
    
    # 检测文件类型
    file_type = detect_file_type(file_path)
    
    # 获取访问令牌
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    token = get_tenant_access_token(app_id, app_secret)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 上传文件
    with open(file_path, "rb") as f:
        file_name = os.path.basename(file_path)
        
        if file_type == "audio":
            # 音频需要转换为 OPUS
            with tempfile.NamedTemporaryFile(suffix=".opus", delete=False) as tmp:
                tmp_path = tmp.name
            
            try:
                if convert_to_opus(file_path, tmp_path):
                    upload_path = tmp_path
                    upload_type = "opus"
                    duration = get_audio_duration(tmp_path)
                else:
                    upload_path = file_path
                    upload_type = "file"
                    duration = 0
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        else:
            upload_path = file_path
            upload_type = "file"
            duration = 0
        
        # 上传到飞书
        with open(upload_path, "rb") as f:
            form = MultipartEncoder(
                fields={
                    "file_type": upload_type if file_type == "audio" else "stream",
                    "file_name": file_name,
                    "file": (file_name, f, "application/octet-stream"),
                }
            )
            
            upload_headers = headers.copy()
            upload_headers["Content-Type"] = form.content_type
            
            upload_url = "https://open.feishu.cn/open-apis/im/v1/files"
            upload_response = requests.post(
                upload_url,
                headers=upload_headers,
                data=form,
                timeout=60,
            )
            upload_response.raise_for_status()
            upload_data = upload_response.json()
    
    file_key = upload_data.get("data", {}).get("file_key")
    if not file_key:
        raise Exception(f"文件上传失败：{upload_data}")
    
    # 发送消息
    if file_type == "image":
        # 图片消息 - 直接预览
        msg_type = "image"
        content = {
            "file_key": file_key,
            "image_type": "message",
        }
    elif file_type == "audio" and duration > 0:
        # 音频卡片 - 内嵌播放器
        msg_type = "interactive"
        content = {
            "config": {
                "wide_screen_mode": True,
                "enable_forward": False,
            },
            "elements": [
                {
                    "tag": "audio",
                    "file_key": file_key,
                    "duration": duration,
                    "title": {"tag": "plain_text", "content": os.path.basename(file_path)},
                }
            ],
        }
    else:
        # 文件消息 - 文件卡片
        msg_type = "file"
        content = {"file_key": file_key}
    
    # 发送消息
    send_url = "https://open.feishu.cn/open-apis/im/v1/messages"
    params = {"receive_id_type": req.receive_id_type}
    json_body = {
        "receive_id": req.receive_id,
        "msg_type": msg_type,
        "content": content,
    }
    
    send_response = requests.post(
        send_url,
        headers=headers,
        params=params,
        json=json_body,
        timeout=30,
    )
    send_response.raise_for_status()
    send_data = send_response.json()
    
    return {
        "message_id": send_data.get("data", {}).get("message_id", ""),
        "msg_type": msg_type,
        "file_type": file_type,
        "file_key": file_key,
    }


@router.post("/send-text", summary="发送文本消息")
def send_text(req: SendTextRequest) -> dict:
    """发送文本消息（UTF-8 编码）"""
    msg_type = "text"
    content = {"text": req.text}
    
    data = feishu_request(
        "POST",
        "/open-apis/im/v1/messages",
        params={"receive_id_type": req.receive_id_type},
        json_body={
            "receive_id": req.receive_id,
            "msg_type": msg_type,
            "content": content,
        },
    )
    
    return {
        "message_id": data.get("data", {}).get("message_id", ""),
        "msg_type": msg_type,
    }


@router.post("/send-image", summary="发送图片")
def send_image(
    receive_id: str = Form(...),
    receive_id_type: str = Form(default="open_id"),
    file: UploadFile = File(...),
) -> dict:
    """发送图片（直接预览）"""
    import requests
    from requests_toolbelt import MultipartEncoder
    
    # 保存上传的文件
    with tempfile.NamedTemporaryFile(suffix=Path(file.filename or "").suffix, delete=False) as tmp:
        tmp_path = tmp.name
        tmp.write(file.file.read())
    
    try:
        req = SendFileRequest(
            file_path=tmp_path,
            receive_id=receive_id,
            receive_id_type=receive_id_type,
            msg_type="image",
        )
        return send_file(req)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@router.post("/send-audio-card", summary="发送音频卡片")
def send_audio_card(
    receive_id: str = Form(...),
    receive_id_type: str = Form(default="open_id"),
    file: UploadFile = File(...),
) -> dict:
    """发送音频卡片（内嵌播放器，支持进度条和时间显示）"""
    import requests
    from requests_toolbelt import MultipartEncoder
    
    # 保存上传的文件
    with tempfile.NamedTemporaryFile(suffix=Path(file.filename or "").suffix, delete=False) as tmp:
        tmp_path = tmp.name
        tmp.write(file.file.read())
    
    try:
        req = SendFileRequest(
            file_path=tmp_path,
            receive_id=receive_id,
            receive_id_type=receive_id_type,
            msg_type="interactive",
        )
        return send_file(req)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
