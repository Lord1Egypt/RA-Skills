#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音 MCP Server - 支持硅基流动和阿里云百炼 API

从抖音分享链接下载无水印视频并提取文本内容
支持两种语音识别服务：
- 硅基流动 SenseVoice（推荐，国内访问快）
- 阿里云百炼 paraformer-v2

自动检测并安装 FFmpeg
"""

import os
import re
import json
import sys
import tempfile
import shutil
import subprocess
from pathlib import Path
from typing import Optional
import requests

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context


def check_ffmpeg():
    """检查 FFmpeg 是否可用"""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return True, result.stdout.split('\n')[0]
    except Exception:
        pass
    
    return False, None

# 创建 MCP 服务器实例
mcp = FastMCP("Douyin MCP Server", 
              dependencies=["requests", "ffmpeg-python", "dashscope"])

# 请求头，模拟移动端访问
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15'
}

# 硅基流动 API 配置
SILICONFLOW_API_URL = "https://api.siliconflow.cn/v1/audio/transcriptions"
SILICONFLOW_MODEL = "FunAudioLLM/SenseVoiceSmall"

# 阿里云百炼配置
DEFAULT_ALI_MODEL = "paraformer-v2"


class DouyinProcessor:
    """抖音视频处理器"""
    
    def __init__(self, api_key: str = "", service: str = "siliconflow"):
        """
        初始化处理器
        
        Args:
            api_key: API Key（硅基流动或阿里云）
            service: 语音识别服务（siliconflow 或 aliyun）
        """
        self.api_key = api_key
        self.service = service
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # 配置阿里云 API Key
        if service == "aliyun":
            import dashscope
            dashscope.api_key = api_key
    
    def __del__(self):
        """清理临时目录"""
        if hasattr(self, 'temp_dir') and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def parse_share_url(self, share_text: str) -> dict:
        """从分享文本中提取无水印视频链接"""
        # 提取分享链接
        urls = re.findall(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 
            share_text
        )
        if not urls:
            raise ValueError("未找到有效的分享链接")
        
        share_url = urls[0]
        
        # 处理重定向
        try:
            response = requests.get(share_url, headers=HEADERS, allow_redirects=False)
            if response.status_code in [301, 302]:
                share_url = response.headers.get("Location", share_url)
        except:
            pass
        
        # 提取视频 ID
        video_id_match = re.search(r'/video/(\d+)', share_url)
        if video_id_match:
            video_id = video_id_match.group(1)
        else:
            video_id = share_url.split("?")[0].strip("/").split("/")[-1]
        
        # 构建标准 URL
        share_url = f'https://www.iesdouyin.com/share/video/{video_id}'
        
        # 获取视频页面内容
        response = requests.get(share_url, headers=HEADERS)
        response.raise_for_status()
        
        # 解析 JSON 数据
        pattern = re.compile(
            pattern=r"window\._ROUTER_DATA\s*=\s*(.*?)</script>",
            flags=re.DOTALL,
        )
        find_res = pattern.search(response.text)

        if not find_res or not find_res.group(1):
            # 备用解析方式
            json_match = re.search(r'\{.*"aweme_id".*\}', response.text)
            if json_match:
                data = json.loads(json_match.group())
                video_url = data.get("video", {}).get("play_addr", {}).get("url_list", [""])[0]
                desc = data.get("desc", f"douyin_{video_id}")
            else:
                raise ValueError("从 HTML 中解析视频信息失败")
        else:
            json_data = json.loads(find_res.group(1).strip())
            VIDEO_ID_PAGE_KEY = "video_(id)/page"
            NOTE_ID_PAGE_KEY = "note_(id)/page"
            
            if VIDEO_ID_PAGE_KEY in json_data["loaderData"]:
                original_video_info = json_data["loaderData"][VIDEO_ID_PAGE_KEY]["videoInfoRes"]
            elif NOTE_ID_PAGE_KEY in json_data["loaderData"]:
                original_video_info = json_data["loaderData"][NOTE_ID_PAGE_KEY]["videoInfoRes"]
            else:
                raise Exception("无法从 JSON 中解析视频信息")

            data = original_video_info["item_list"][0]
            video_url = data["video"]["play_addr"]["url_list"][0].replace("playwm", "play")
            desc = data.get("desc", "").strip() or f"douyin_{video_id}"

        # 替换文件名中的非法字符
        desc = re.sub(r'[\\/:*?"<>|]', '_', desc)
        
        return {
            "url": video_url,
            "title": desc,
            "video_id": video_id
        }
    
    def download_video(self, video_info: dict, ctx: Context = None) -> Path:
        """下载视频到临时目录"""
        filename = f"{video_info['video_id']}.mp4"
        filepath = self.temp_dir / filename
        
        if ctx:
            ctx.info(f"正在下载视频：{video_info['title']}")
        
        response = requests.get(video_info['url'], headers=HEADERS, stream=True)
        response.raise_for_status()
        
        # 获取文件大小
        total_size = int(response.headers.get('content-length', 0))
        
        # 下载文件
        with open(filepath, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0 and ctx:
                        progress = downloaded / total_size
                        # ctx.report_progress 仅在 MCP 上下文中可用
        
        if ctx:
            ctx.info(f"视频下载完成：{filepath}")
        return filepath
    
    def extract_audio(self, video_path: Path) -> Path:
        """从视频文件中提取音频"""
        # 检查 FFmpeg
        ffmpeg_available, version = check_ffmpeg()
        
        if not ffmpeg_available:
            raise Exception(
                "FFmpeg 未安装！\n"
                "请运行以下命令安装：\n"
                "  python scripts/install_ffmpeg.py\n"
                "  或 brew install ffmpeg (macOS)\n"
                "  或 apt install ffmpeg (Ubuntu)"
            )
        
        audio_path = video_path.with_suffix('.mp3')
        
        try:
            (
                ffmpeg
                .input(str(video_path))
                .output(str(audio_path), acodec='libmp3lame', q=0, ar='16000')
                .run(capture_stdout=True, capture_stderr=True, overwrite_output=True)
            )
            return audio_path
        except Exception as e:
            raise Exception(f"提取音频时出错：{str(e)}")
    
    def transcribe_siliconflow(self, audio_path: str) -> str:
        """使用硅基流动 API 进行语音识别"""
        with open(audio_path, "rb") as f:
            files = {"audio": f}
            headers = {"Authorization": f"Bearer {self.api_key}"}
            data = {"model": SILICONFLOW_MODEL}
            
            response = requests.post(
                SILICONFLOW_API_URL,
                headers=headers,
                files=files,
                data=data
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("text", "")
    
    def transcribe_aliyun(self, video_url: str) -> str:
        """使用阿里云百炼 API 进行语音识别"""
        import dashscope
        from http import HTTPStatus
        
        try:
            # 发起转录任务
            task_response = dashscope.audio.asr.Transcription.async_call(
                model=self.service_model or DEFAULT_ALI_MODEL,
                file_urls=[video_url],
                language_hints=['zh', 'en']
            )
            
            # 等待转录完成
            transcription_response = dashscope.audio.asr.Transcription.wait(
                task=task_response.output.task_id
            )
            
            if transcription_response.status_code == HTTPStatus.OK:
                for transcription in transcription_response.output['results']:
                    url = transcription['transcription_url']
                    result = json.loads(requests.get(url).read().decode('utf8'))
                    
                    if 'transcripts' in result and len(result['transcripts']) > 0:
                        return result['transcripts'][0]['text']
                
                return "未识别到文本内容"
            else:
                raise Exception(f"转录失败：{transcription_response.output.message}")
                
        except Exception as e:
            raise Exception(f"阿里云转录出错：{str(e)}")
    
    def extract_text(self, share_link: str, ctx: Context = None) -> str:
        """
        从抖音视频提取文本（完整流程）
        
        Args:
            share_link: 抖音分享链接
            ctx: MCP 上下文
            
        Returns:
            提取的文本内容
        """
        try:
            # 解析视频链接
            if ctx:
                ctx.info("正在解析抖音分享链接...")
            video_info = self.parse_share_url(share_link)
            
            # 下载视频
            if ctx:
                ctx.info(f"正在下载视频：{video_info['title']}")
            video_path = self.download_video(video_info, ctx)
            
            # 提取音频
            if ctx:
                ctx.info("正在提取音频...")
            audio_path = self.extract_audio(video_path)
            
            # 语音识别
            if ctx:
                ctx.info(f"正在使用{self.service}进行语音识别...")
            
            if self.service == "siliconflow":
                text = self.transcribe_siliconflow(str(audio_path))
            else:
                text = self.transcribe_aliyun(video_info['url'])
            
            if ctx:
                ctx.info("文本提取完成!")
            
            return text
            
        except Exception as e:
            if ctx:
                ctx.error(f"处理过程中出现错误：{str(e)}")
            raise Exception(f"提取抖音视频文本失败：{str(e)}")
        finally:
            # 清理临时文件
            self.__del__()


@mcp.tool()
def get_douyin_download_link(share_link: str) -> str:
    """
    获取抖音视频的无水印下载链接
    
    参数:
    - share_link: 抖音分享链接或包含链接的文本
    
    返回:
    - 包含下载链接和视频信息的 JSON 字符串
    """
    try:
        processor = DouyinProcessor("")  # 获取下载链接不需要 API 密钥
        video_info = processor.parse_share_url(share_link)
        
        return json.dumps({
            "status": "success",
            "video_id": video_info["video_id"],
            "title": video_info["title"],
            "download_url": video_info["url"],
            "description": f"视频标题：{video_info['title']}",
            "usage_tip": "可以直接使用此链接下载无水印视频"
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "error": f"获取下载链接失败：{str(e)}"
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def extract_douyin_text(
    share_link: str,
    service: str = "siliconflow",
    ctx: Context = None
) -> str:
    """
    从抖音分享链接提取视频中的文本内容
    
    参数:
    - share_link: 抖音分享链接或包含链接的文本
    - service: 语音识别服务（siliconflow 或 aliyun）
    
    返回:
    - 提取的文本内容
    
    注意: 
    - 硅基流动：设置环境变量 API_KEY 或 SILICONFLOW_API_KEY
    - 阿里云百炼：设置环境变量 DASHSCOPE_API_KEY
    """
    try:
        # 获取 API 密钥
        if service == "siliconflow":
            api_key = os.getenv('API_KEY') or os.getenv('SILICONFLOW_API_KEY', '')
            if not api_key:
                raise ValueError(
                    "未设置硅基流动 API Key\n"
                    "请设置环境变量：export API_KEY=\"sk-xxx\"\n"
                    "注册获取：https://cloud.siliconflow.cn/i/84kySW0S\n"
                    "使用邀请码 84kySW0S 获取免费额度"
                )
        else:
            api_key = os.getenv('DASHSCOPE_API_KEY', '')
            if not api_key:
                raise ValueError(
                    "未设置阿里云百炼 API Key\n"
                    "请设置环境变量：export DASHSCOPE_API_KEY=\"sk-xxx\""
                )
        
        processor = DouyinProcessor(api_key, service)
        text = processor.extract_text(share_link, ctx)
        return text
        
    except Exception as e:
        if ctx:
            ctx.error(f"处理过程中出现错误：{str(e)}")
        raise Exception(f"提取抖音视频文本失败：{str(e)}")


@mcp.tool()
def parse_douyin_video_info(share_link: str) -> str:
    """
    解析抖音分享链接，获取视频基本信息
    
    参数:
    - share_link: 抖音分享链接或包含链接的文本
    
    返回:
    - 视频信息（JSON 格式字符串）
    """
    try:
        processor = DouyinProcessor("")  # 不需要 API 密钥
        video_info = processor.parse_share_url(share_link)
        
        return json.dumps({
            "video_id": video_info["video_id"],
            "title": video_info["title"],
            "download_url": video_info["url"],
            "status": "success"
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.resource("douyin://video/{video_id}")
def get_video_info(video_id: str) -> str:
    """
    获取指定视频 ID 的详细信息
    
    参数:
    - video_id: 抖音视频 ID
    
    返回:
    - 视频详细信息
    """
    share_url = f"https://www.iesdouyin.com/share/video/{video_id}"
    try:
        processor = DouyinProcessor("")
        video_info = processor.parse_share_url(share_url)
        return json.dumps(video_info, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"获取视频信息失败：{str(e)}"


@mcp.prompt()
def douyin_text_extraction_guide() -> str:
    """抖音视频文本提取使用指南"""
    return """
# 抖音视频文本提取使用指南

## 功能说明
这个 MCP 服务器可以从抖音分享链接中提取视频的文本内容，以及获取无水印下载链接。

## 支持的语音识别服务

### 1. 硅基流动 SenseVoice（推荐）
- **优点**: 国内访问速度快，价格低廉，新用户有免费额度
- **注册**: https://cloud.siliconflow.cn/i/84kySW0S
- **邀请码**: 84kySW0S（使用邀请码获得额外免费额度）
- **环境变量**: `export API_KEY="sk-xxx"`

### 2. 阿里云百炼 paraformer-v2
- **优点**: 阿里云服务稳定，识别准确率高
- **注册**: https://dashscope.console.aliyun.com/
- **环境变量**: `export DASHSCOPE_API_KEY="sk-xxx"`

## MCP 工具说明

| 工具名 | 功能 | API 需求 |
|--------|------|---------|
| `parse_douyin_video_info` | 解析视频基本信息 | ❌ |
| `get_douyin_download_link` | 获取无水印下载链接 | ❌ |
| `extract_douyin_text` | 提取视频文案 | ✅ |
| `douyin://video/{video_id}` | 获取指定视频详情 | ❌ |

## Claude Desktop 配置示例

```json
{
  "mcpServers": {
    "douyin-mcp": {
      "command": "uvx",
      "args": ["douyin-mcp-server"],
      "env": {
        "API_KEY": "sk-xxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

## 使用示例

### 获取下载链接（无需 API）
```
获取这个视频的下载链接 https://v.douyin.com/xxxxx/
```

### 提取文案（需要 API）
```
提取这个视频的文案 https://v.douyin.com/xxxxx/
使用硅基流动提取文案 https://v.douyin.com/xxxxx/
```

## 注意事项
- 获取下载链接和解析信息无需 API Key
- 提取文案需要设置 API Key
- 推荐使用硅基流动，新用户有免费额度
- 使用邀请码 84kySW0S 注册获得额外奖励
"""


def main():
    """启动 MCP 服务器"""
    mcp.run()


if __name__ == "__main__":
    main()
