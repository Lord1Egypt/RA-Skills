#!/usr/bin/env python3
"""
Whisper Local - 本地 Docker Whisper ASR

通过 Docker 运行的 Faster-Whisper 服务进行语音转录。
支持自动检测服务状态、自动启动容器。
"""

import requests
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, Optional


class WhisperLocal:
    """本地 Docker Whisper ASR 客户端"""
    
    DEFAULT_URL = "http://localhost:PORT"
    CONTAINER_NAME = "whisper-asr"
    DOCKER_IMAGE = "onerahmet/openai-whisper-asr-webservice:latest"
    
    def __init__(self, model: str = "medium", url: Optional[str] = None):
        self.model = model
        self.base_url = url or self.DEFAULT_URL
        self.asr_url = f"{self.base_url}/asr"
        
    def check_service(self) -> bool:
        """检查 ASR 服务是否运行"""
        try:
            resp = requests.get(self.base_url, timeout=3)
            return True
        except Exception:
            return False
    
    def check_docker_container(self) -> str:
        """检查 Docker 容器状态
        
        Returns:
            "running" | "stopped" | "not_found" | "docker_not_available"
        """
        try:
            # 检查 Docker 是否可用
            result = subprocess.run(
                ["docker", "version"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode != 0:
                return "docker_not_available"
            
            # 检查容器状态
            result = subprocess.run(
                ["docker", "inspect", "--format", "{{.State.Status}}", self.CONTAINER_NAME],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode != 0:
                return "not_found"
            
            status = result.stdout.strip()
            return status  # "running", "exited", "created", etc.
            
        except FileNotFoundError:
            return "docker_not_available"
        except Exception:
            return "docker_not_available"
    
    def start_docker_container(self) -> bool:
        """启动或创建 Docker 容器
        
        Returns:
            是否成功启动
        """
        container_status = self.check_docker_container()
        
        if container_status == "docker_not_available":
            print("❌ Docker 不可用，请先安装并启动 Docker")
            return False
        
        if container_status == "running":
            print("✅ Whisper ASR 容器已在运行")
            return True
        
        if container_status in ("exited", "created"):
            # 容器存在但未运行，启动它
            print(f"🔄 启动已有容器 {self.CONTAINER_NAME}...")
            result = subprocess.run(
                ["docker", "start", self.CONTAINER_NAME],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                return True
            else:
                print(f"⚠️ 启动失败: {result.stderr}")
                return False
        
        # 容器不存在，创建新的
        print(f"🆕 创建新容器 {self.CONTAINER_NAME} (模型: {self.model})...")
        cmd = [
            "docker", "run", "-d",
            "-p", "9000:9000",
            "-e", f"ASR_MODEL={self.model}",
            "-e", "ASR_ENGINE=faster_whisper",
            "--name", self.CONTAINER_NAME,
            self.DOCKER_IMAGE
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            return True
        else:
            print(f"❌ 创建容器失败: {result.stderr}")
            return False
    
    def ensure_service_ready(self, max_wait: int = 30) -> bool:
        """确保服务就绪
        
        如果服务未运行，尝试启动容器并等待服务就绪。
        
        Args:
            max_wait: 最大等待时间（秒）
            
        Returns:
            服务是否就绪
        """
        # 先检查服务
        if self.check_service():
            return True
        
        # 尝试启动容器
        if not self.start_docker_container():
            return False
        
        # 等待服务就绪
        print(f"⏳ 等待 ASR 服务就绪（最多 {max_wait} 秒）...")
        for i in range(max_wait // 2):
            time.sleep(2)
            if self.check_service():
                print(f"✅ ASR 服务已就绪（等待了 {(i+1)*2} 秒）")
                return True
        
        print(f"❌ ASR 服务启动超时（{max_wait} 秒）")
        return False
    
    def transcribe(self, audio_path: str, language: Optional[str] = None) -> Dict:
        """转录音频文件
        
        Args:
            audio_path: 音频文件路径（建议 WAV 16kHz 单声道）
            language: 语言代码（zh/en），None 为自动检测
            
        Returns:
            {
                "success": bool,
                "text": str,
                "segments": list,
                "language": str,
                "error": str (if failed)
            }
        """
        # 检查文件
        if not Path(audio_path).exists():
            return {"success": False, "error": f"音频文件不存在: {audio_path}"}
        
        file_size = Path(audio_path).stat().st_size
        if file_size < 100:
            return {"success": False, "error": f"音频文件过小 ({file_size} bytes)"}
        
        # 根据文件大小估算超时时间
        # 大约 1MB 音频 ≈ 1 分钟内容，small 模型处理约需 12 秒
        estimated_duration_sec = max(60, int(file_size / 1024 / 1024 * 15) + 30)
        
        # 准备请求
        try:
            with open(audio_path, "rb") as f:
                files = {"audio_file": (Path(audio_path).name, f, "audio/wav")}
                data = {}
                
                if language:
                    data["language"] = language
                
                resp = requests.post(
                    self.asr_url,
                    files=files,
                    data=data,
                    timeout=estimated_duration_sec
                )
                resp.raise_for_status()
            
            # 解析结果
            result = resp.json()
            
            text = result.get("text", "")
            
            segments = []
            if "segments" in result:
                for seg in result["segments"]:
                    segments.append({
                        "start": seg.get("start", 0.0),
                        "end": seg.get("end", 0.0),
                        "text": seg.get("text", "")
                    })
            
            if not text and not segments:
                return {
                    "success": False,
                    "error": "转录结果为空，可能音频没有语音内容"
                }
            
            return {
                "success": True,
                "text": text,
                "segments": segments,
                "language": result.get("language", language or "auto")
            }
            
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": f"ASR 服务超时（{estimated_duration_sec}秒），音频可能太长。"
                        f"建议：1) 换更小模型 2) 分段处理 3) 增加超时"
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "无法连接 ASR 服务。请检查：\n"
                        "1. docker ps --filter name=whisper-asr\n"
                        "2. docker start whisper-asr\n"
                        "3. 或重新部署：docker run -d -p 9000:9000 "
                        "-e ASR_MODEL=medium -e ASR_ENGINE=faster_whisper "
                        "--name whisper-asr onerahmet/openai-whisper-asr-webservice:latest"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"转录失败: {e}"
            }


# 测试代码
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python whisper_local.py <音频文件> [语言代码]")
        print("\n检查服务状态:")
        
        transcriber = WhisperLocal()
        service_ok = transcriber.check_service()
        container_status = transcriber.check_docker_container()
        
        print(f"  ASR 服务: {'✅ 运行中' if service_ok else '❌ 未运行'}")
        print(f"  Docker 容器: {container_status}")
        sys.exit(0)
    
    audio_path = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else None
    
    transcriber = WhisperLocal()
    
    # 确保服务就绪
    if not transcriber.ensure_service_ready():
        print("❌ 无法启动 ASR 服务")
        sys.exit(1)
    
    # 转录
    result = transcriber.transcribe(audio_path, language)
    
    if result["success"]:
        print(f"✅ 转录成功")
        print(f"语言: {result['language']}")
        print(f"\n{result['text']}")
    else:
        print(f"❌ 失败: {result['error']}")