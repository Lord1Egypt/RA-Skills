#!/usr/bin/env python3
"""
Douyin Transcriber - 语音转录模块

支持多种转录方式：
1. Docker Whisper ASR（本地，推荐）
2. 硅基流动 API（云端）
3. 阿里云百炼 API（云端）

自动处理：
- 视频文件自动提取音频
- 音频格式自动转换（16kHz 单声道 WAV）
- 转录方式自动 fallback
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, Optional

# 配置路径
DEFAULT_CONFIG_PATH = Path.home() / ".openclaw" / "skills" / "douyin-config.json"
FALLBACK_CONFIG_PATH = Path.home() / ".openclaw" / "config.json"
TEMP_DIR = Path("/path/to/temp/douyin")

# 视频文件扩展名
VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm', '.m4v'}
# 需要转换的音频扩展名（非 WAV 16kHz）
AUDIO_NEED_CONVERT = {'.m4a', '.mp3', '.aac', '.ogg', '.flac', '.wma', '.opus'}


def load_douyin_config() -> Dict:
    """加载抖音模块配置"""
    if DEFAULT_CONFIG_PATH.exists():
        with open(DEFAULT_CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    if FALLBACK_CONFIG_PATH.exists():
        with open(FALLBACK_CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f).get("douyin", {})
    return {}


class DouyinTranscriber:
    """语音转录器"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or load_douyin_config()
        self.temp_dir = Path(self.config.get("temp_dir", str(TEMP_DIR)))
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
    def transcribe(self, input_path: str, language: Optional[str] = None) -> Dict:
        """转录音频/视频文件
        
        自动处理：
        - 视频文件 → 提取音频 → 转录
        - 非 WAV 音频 → 转换格式 → 转录
        - WAV 音频 → 直接转录
        
        Args:
            input_path: 音频/视频文件路径
            language: 语言代码（zh/en），None 为自动检测
            
        Returns:
            {
                "success": bool,
                "text": str,
                "segments": list,
                "language": str,
                "method_used": str,
                "audio_path": str,
                "error": str (if failed)
            }
        """
        # 检查文件是否存在
        if not Path(input_path).exists():
            return {
                "success": False,
                "error": f"文件不存在: {input_path}"
            }
        
        # Step 1: 准备音频文件
        audio_path = input_path
        suffix = Path(input_path).suffix.lower()
        
        try:
            if suffix in VIDEO_EXTENSIONS:
                # 视频文件 → 提取音频
                print(f"📹 检测到视频文件，正在提取音频...")
                audio_path = self.extract_audio(input_path)
                print(f"✅ 音频提取完成: {audio_path}")
                
            elif suffix in AUDIO_NEED_CONVERT:
                # 非 WAV 音频 → 转换格式
                print(f"🔄 转换音频格式: {suffix} → .wav")
                audio_path = self.convert_audio(input_path)
                print(f"✅ 格式转换完成: {audio_path}")
                
            elif suffix == '.wav':
                # WAV 文件，检查是否需要重采样
                audio_path = self.ensure_wav_format(input_path)
            else:
                # 未知格式，尝试用 ffmpeg 转换
                print(f"⚠️ 未知音频格式 {suffix}，尝试转换...")
                audio_path = self.convert_audio(input_path)
                
        except Exception as e:
            return {
                "success": False,
                "error": f"音频预处理失败: {e}"
            }
        
        # Step 2: 转录
        print(f"🎙️ 正在转录...")
        method = self.config.get("transcriber", "whisper_local")
        
        # 构建候选方式列表（预检可用性）
        methods_to_try = []
        all_methods = [method] + [m for m in ["whisper_local", "sili_flow_api", "dashscope_api"] if m != method]
        
        for m in all_methods:
            if m in methods_to_try:
                continue
            if self._check_method_available(m):
                methods_to_try.append(m)
        
        if not methods_to_try:
            return {
                "success": False,
                "error": "没有可用的转录方式。请检查：\n"
                        "1. Docker 是否安装并运行（whisper_local）\n"
                        "2. 或配置云端 API Key（sili_flow_api_key / dashscope_api_key）"
            }
        
        errors = []
        for try_method in methods_to_try:
            try:
                result = self._do_transcribe(audio_path, language, try_method)
                
                if result.get("success"):
                    result["method_used"] = try_method
                    result["audio_path"] = audio_path
                    result["language"] = language or result.get("language", "auto")
                    return result
                else:
                    errors.append(f"{try_method}: {result.get('error', '未知错误')}")
                    
            except Exception as e:
                errors.append(f"{try_method}: {e}")
                continue
        
        return {
            "success": False,
            "error": "所有转录方式都失败了",
            "errors": errors
        }
    
    def _check_method_available(self, method: str) -> bool:
        """预检转录方式是否可用（快速判断）"""
        if method == "whisper_local":
            # 检查 Docker 是否可用
            try:
                result = subprocess.run(
                    ["docker", "version"],
                    capture_output=True, text=True, timeout=3
                )
                if result.returncode != 0:
                    print(f"  ⏭️ whisper_local: Docker 不可用，跳过")
                    return False
            except (FileNotFoundError, subprocess.TimeoutExpired):
                print(f"  ⏭️ whisper_local: Docker 未安装或无响应，跳过")
                return False
            return True
        
        elif method == "sili_flow_api":
            if not self.config.get("sili_flow_api_key"):
                print(f"  ⏭️ sili_flow_api: API Key 未配置，跳过")
                return False
            return True
        
        elif method == "dashscope_api":
            if not self.config.get("dashscope_api_key"):
                print(f"  ⏭️ dashscope_api: API Key 未配置，跳过")
                return False
            return True
        
        return False
    
    def _do_transcribe(self, audio_path: str, language: Optional[str], method: str) -> Dict:
        """执行转录"""
        if method == "whisper_local":
            return self._transcribe_via_whisper_local(audio_path, language)
        elif method == "sili_flow_api":
            return self._transcribe_via_sili_flow(audio_path, language)
        elif method == "dashscope_api":
            return self._transcribe_via_dashscope(audio_path, language)
        else:
            return {"success": False, "error": f"不支持的转录方式: {method}"}
    
    def _transcribe_via_whisper_local(self, audio_path: str, language: Optional[str]) -> Dict:
        """通过本地 Docker Whisper ASR 转录"""
        sys.path.append(str(Path(__file__).parent))
        from whisper_local import WhisperLocal
        
        transcriber = WhisperLocal(
            model=self.config.get("whisper_model", "medium")
        )
        
        # 使用 ensure_service_ready() 统一处理服务检测/启动/等待
        if not transcriber.ensure_service_ready(max_wait=30):
            return {
                "success": False,
                "error": "Whisper ASR 服务无法启动"
            }
        
        return transcriber.transcribe(audio_path, language)
    
    def _transcribe_via_sili_flow(self, audio_path: str, language: Optional[str]) -> Dict:
        """通过硅基流动 API 转录"""
        api_key = self.config.get("sili_flow_api_key")
        if not api_key:
            raise ValueError("缺少硅基流动 API Key")
        
        sys.path.append(str(Path(__file__).parent))
        from sili_flow_api import SiliFlowASR
        
        return SiliFlowASR(api_key).transcribe(audio_path, language)
    
    def _transcribe_via_dashscope(self, audio_path: str, language: Optional[str]) -> Dict:
        """通过阿里云百炼 API 转录"""
        api_key = self.config.get("dashscope_api_key")
        if not api_key:
            raise ValueError("缺少阿里云百炼 API Key")
        
        sys.path.append(str(Path(__file__).parent))
        from dashscope_api import DashScopeASR
        
        return DashScopeASR(api_key).transcribe(audio_path, language)
    
    def extract_audio(self, video_path: str, output_path: Optional[str] = None) -> str:
        """从视频提取音频（16kHz 单声道 WAV）"""
        if not output_path:
            output_path = str(self.temp_dir / f"{Path(video_path).stem}.wav")
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            "ffmpeg", "-i", video_path,
            "-ar", "16000",
            "-ac", "1",
            "-c:a", "pcm_s16le",
            output_path, "-y"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            raise RuntimeError(f"音频提取失败: {result.stderr[:500]}")
        
        # 验证输出文件
        if not Path(output_path).exists() or Path(output_path).stat().st_size < 100:
            raise RuntimeError("音频提取失败：输出文件为空或不存在")
        
        return output_path
    
    def convert_audio(self, audio_path: str, output_path: Optional[str] = None) -> str:
        """转换音频格式为 16kHz 单声道 WAV"""
        if not output_path:
            output_path = str(self.temp_dir / f"{Path(audio_path).stem}.wav")
        
        return self.extract_audio(audio_path, output_path)  # 复用同一个 ffmpeg 命令
    
    def ensure_wav_format(self, wav_path: str) -> str:
        """确保 WAV 文件是 16kHz 单声道格式
        
        如果已经是正确格式，直接返回原路径。
        否则转换后返回新路径。
        """
        # 用 ffprobe 检查格式
        try:
            cmd = [
                "ffprobe", "-v", "quiet",
                "-print_format", "json",
                "-show_streams",
                wav_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                info = json.loads(result.stdout)
                for stream in info.get("streams", []):
                    if stream.get("codec_type") == "audio":
                        sample_rate = int(stream.get("sample_rate", 0))
                        channels = int(stream.get("channels", 0))
                        if sample_rate == 16000 and channels == 1:
                            return wav_path  # 已经是正确格式
        except Exception:
            pass
        
        # 需要转换
        return self.convert_audio(wav_path)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="语音转录模块")
    parser.add_argument("input", help="音频/视频文件路径")
    parser.add_argument("--language", choices=["zh", "en"], help="语言代码")
    parser.add_argument("--method", choices=["whisper_local", "sili_flow_api", "dashscope_api"], help="转录方式")
    parser.add_argument("-o", "--output", help="输出文本文件路径")
    
    args = parser.parse_args()
    
    transcriber = DouyinTranscriber()
    
    if args.method:
        transcriber.config["transcriber"] = args.method
    
    result = transcriber.transcribe(args.input, args.language)
    
    if result.get("success"):
        print(f"\n✅ 转录成功")
        print(f"语言: {result.get('language', 'auto')}")
        print(f"方式: {result['method_used']}")
        print(f"\n{'='*60}")
        print(result["text"])
        print(f"{'='*60}\n")
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result["text"])
            print(f"✅ 已保存到: {args.output}")
    else:
        print(f"\n❌ 转录失败: {result.get('error')}")
        if result.get("errors"):
            for err in result["errors"]:
                print(f"  - {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()