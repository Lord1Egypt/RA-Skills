#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度智能云语音合成 (TTS) API 客户端
支持多说话人对话合成（SSML模式或分段合并回退）
"""

import os
import sys
import json
import argparse
import time
import requests
import base64
import hashlib
import urllib.parse
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# 尝试导入本地模块
sys.path.insert(0, str(Path(__file__).parent))
try:
    from dialogue_formatter import DialogueFormatter, VoiceMapper
    from audio_merger import AudioMerger
except ImportError as e:
    print(f"警告：无法导入本地模块 {e}，某些功能可能受限")
    DialogueFormatter = None
    VoiceMapper = None
    AudioMerger = None

class BaiduTTSClient:
    """百度TTS API客户端"""
    
    # API端点
    TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"  # 注意：使用 aip.baidubce.com 而非 openapi.baidu.com（后者可能已弃用）
    TTS_URL = "https://tsn.baidu.com/text2audio"
    
    # 默认参数
    DEFAULT_SPEED = 5    # 语速 0-15
    DEFAULT_PITCH = 5    # 音调 0-15
    DEFAULT_VOLUME = 5   # 音量 0-15
    DEFAULT_AUE = 3      # 音频格式 3=mp3, 4=pcm, 5=pcm, 6=wav
    DEFAULT_PER = 511    # 音色代码（511支持SSML多音色）
    
    def __init__(self, api_key: str = None, secret_key: str = None):
        """
        初始化客户端
        
        Args:
            api_key: 百度API Key、access_token 或 IAM Key
            secret_key: 百度Secret Key（如果 api_key 是普通 API Key 则需要）
        
        支持三种认证方式：
        1. access_token（以 "1." 开头） -> 直接使用 tok 参数
        2. IAM Key（以 "bce-v3/" 开头） -> 使用 iam-apikey 参数
        3. API Key + Secret Key -> 自动获取 access_token 后使用 tok 参数
        """
        self.api_key = api_key or os.getenv("BAIDU_API_KEY")
        self.secret_key = secret_key or os.getenv("BAIDU_SECRET_KEY")
        
        # 检测认证类型
        self.auth_type = None
        self.access_token = None
        self.token_expires_at = 0
        self.iam_key = None
        
        if not self.api_key:
            raise ValueError(
                "请设置环境变量 BAIDU_API_KEY\n"
                "支持以下格式：\n"
                "1. access_token（以 '1.' 开头）\n"
                "2. IAM Key（以 'bce-v3/' 开头）\n"
                "3. 普通 API Key（需要同时设置 BAIDU_SECRET_KEY）"
            )
        
        # 检测 access_token 格式（通常以 "1." 开头）
        if self.api_key.startswith("1."):
            self.auth_type = "token"
            self.access_token = self.api_key
            self.token_expires_at = time.time() + 86400 * 365  # 假设长期有效
            print("检测到 access_token 格式，将直接使用 tok 参数")
        
        # 检测 IAM Key 格式（bce-v3/...）
        elif self.api_key.startswith("bce-v3/"):
            self.auth_type = "iam"
            self.iam_key = self.api_key
            print("检测到 IAM Key 格式，将使用 iam-apikey 参数")
        
        # 否则视为普通 API Key，需要 Secret Key
        else:
            self.auth_type = "apikey_secret"
            if not self.secret_key:
                raise ValueError(
                    "普通 API Key 需要同时设置 BAIDU_SECRET_KEY\n"
                    "或提供 access_token（以 '1.' 开头）或 IAM Key（以 'bce-v3/' 开头）"
                )
            print("检测到 API Key + Secret Key 模式，将自动获取 access_token")
        
        # 分段合成模式配置
        self.segment_mode = False  # 是否强制使用分段模式
        self.force_ssml = False    # 是否强制使用SSML API（忽略多音色检测）
        
    def get_access_token(self) -> str:
        """获取或刷新访问令牌（仅适用于 apikey_secret 模式）"""
        if self.auth_type == "token":
            return self.access_token
        elif self.auth_type == "iam":
            # IAM 模式不需要 access_token
            return None
        elif self.auth_type == "apikey_secret":
            current_time = time.time()
            if self.access_token and current_time < self.token_expires_at - 60:
                return self.access_token
            
            params = {
                "grant_type": "client_credentials",
                "client_id": self.api_key,
                "client_secret": self.secret_key
            }
            
            try:
                response = requests.get(self.TOKEN_URL, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if "access_token" not in data:
                    raise ValueError(f"获取令牌失败: {data}")
                
                self.access_token = data["access_token"]
                self.token_expires_at = current_time + data.get("expires_in", 2592000)
                print(f"令牌获取成功，有效期至 {time.ctime(self.token_expires_at)}")
                return self.access_token
                
            except requests.exceptions.RequestException as e:
                raise RuntimeError(f"获取令牌网络错误: {e}")
            except json.JSONDecodeError:
                raise RuntimeError("令牌响应不是有效JSON")
        else:
            raise ValueError(f"未知的认证类型: {self.auth_type}")
    
    def _detect_multivoice_ssml(self, ssml_text: str) -> bool:
        """
        检测SSML是否包含多个<voice>标签（多音色）
        
        Args:
            ssml_text: SSML文本
            
        Returns:
            True 如果包含多个<voice>标签
        """
        import re
        # 简单统计<voice>标签数量
        voice_tags = re.findall(r'<voice\s', ssml_text, re.IGNORECASE)
        return len(voice_tags) > 1
    
    def _synthesize_multivoice_segment(self, ssml_text: str, spd: int = None, pit: int = None,
                                       vol: int = None, aue: int = None, per: int = None,
                                       pause_ms: int = 300) -> bytes:
        """
        多音色分段合成（绕过百度API限制）
        
        Args:
            ssml_text: 包含多个<voice>标签的SSML文本
            pause_ms: 音色间的静音间隔（毫秒）
            
        Returns:
            合并后的音频数据
        """
        # 导入本地模块
        try:
            from dialogue_formatter import DialogueFormatter
            from audio_merger import AudioMerger
        except ImportError as e:
            raise RuntimeError(f"分段合成需要本地模块: {e}")
        
        # 解析SSML获取分段
        formatter = DialogueFormatter()
        segments = formatter.parse_ssml_segments(ssml_text)
        
        if not segments:
            raise RuntimeError("无法从SSML解析出语音分段")
        
        print(f"检测到多音色SSML，自动切换到分段合成模式")
        print(f"分段合成: {len(segments)} 个片段，静音间隔 {pause_ms}ms")
        
        audio_files = []
        import tempfile
        import os
        from pathlib import Path
        
        temp_dir = tempfile.mkdtemp(prefix="baidu_tts_segment_")
        
        try:
            # 逐个合成
            for i, (text, voice_name, voice_id) in enumerate(segments, 1):
                print(f"  片段 {i}: 音色={voice_name}({voice_id}), 文本='{text[:50]}...'")
                
                # 合成该片段（使用单音色SSML）
                # 创建单音色SSML
                single_ssml = formatter.create_simple_ssml(text, voice_id)
                
                try:
                    # 尝试使用SSML模式合成（单音色）
                    audio_data = self.synthesize_ssml(
                        single_ssml, spd=spd, pit=pit,
                        vol=vol, aue=aue, per=voice_id
                    )
                except Exception as e:
                    print(f"  SSML模式失败，回退到文本模式: {e}")
                    # 回退到普通文本合成
                    audio_data = self.synthesize_text(
                        text, spd=spd, pit=pit,
                        vol=vol, aue=aue, per=voice_id
                    )
                
                # 保存临时文件
                temp_file = Path(temp_dir) / f"segment_{i}.mp3"
                with open(temp_file, "wb") as f:
                    f.write(audio_data)
                
                audio_files.append(str(temp_file))
            
            # 合并音频
            merger = AudioMerger()
            merged_audio = merger.merge_audio_files(audio_files, pause_ms=pause_ms)
            
            return merged_audio
            
        finally:
            # 清理临时文件
            import shutil
            try:
                shutil.rmtree(temp_dir)
            except OSError:
                pass  # Cleanup failure is non-critical
    
    def synthesize_ssml(self, ssml_text: str, spd: int = None, pit: int = None, 
                       vol: int = None, aue: int = None, per: int = None,
                       pause_ms: int = 300) -> bytes:
        """
        使用SSML合成语音
        
        Args:
            ssml_text: SSML格式文本
            spd: 语速 0-15
            pit: 音调 0-15
            vol: 音量 0-15
            aue: 音频格式 3=mp3, 4=pcm, 5=pcm, 6=wav
            per: 音色代码（511支持SSML多音色）
            
        Returns:
            音频二进制数据
        """
        # 检测是否是多音色SSML，考虑用户配置
        is_multivoice = self._detect_multivoice_ssml(ssml_text)
        
        # 强制SSML模式：忽略多音色检测，直接使用API
        if self.force_ssml:
            print("强制SSML模式，忽略多音色检测")
            is_multivoice = False
        
        # 分段模式：强制使用分段合成
        if self.segment_mode and is_multivoice:
            print("分段模式启用，使用分段合成")
            return self._synthesize_multivoice_segment(
                ssml_text, spd=spd, pit=pit, vol=vol, aue=aue, per=per,
                pause_ms=pause_ms
            )
        
        # 自动检测多音色并分段
        if is_multivoice and not self.force_ssml:
            print("检测到多音色SSML，自动切换到分段合成模式")
            # 使用分段合成（默认静音间隔300ms）
            return self._synthesize_multivoice_segment(
                ssml_text, spd=spd, pit=pit, vol=vol, aue=aue, per=per,
                pause_ms=pause_ms
            )
        
        # 单音色SSML，使用原API
        # 根据认证类型构建参数
        params = {
            "ctp": 1,  # 客户端类型
            "lan": "zh",  # 语言
            "cuid": "openclaw_tts_client",
        }
        
        # 添加认证参数
        if self.auth_type == "token":
            token = self.get_access_token()
            if token:
                params["tok"] = token
            else:
                raise ValueError("access_token 为空")
        elif self.auth_type == "iam":
            params["iam-apikey"] = self.iam_key
        elif self.auth_type == "apikey_secret":
            token = self.get_access_token()
            if token:
                params["tok"] = token
            else:
                raise ValueError("获取 access_token 失败")
        else:
            raise ValueError(f"不支持的认证类型: {self.auth_type}")
        
        # 添加可选参数
        if spd is not None:
            params["spd"] = spd
        if pit is not None:
            params["pit"] = pit
        if vol is not None:
            params["vol"] = vol
        if aue is not None:
            params["aue"] = aue
        if per is not None:
            params["per"] = per
        
        # SSML模式需要tex_type=3
        params["tex_type"] = 3
        params["tex"] = base64.b64encode(ssml_text.encode("utf-8")).decode("ascii")
        
        try:
            response = requests.post(self.TTS_URL, data=params, timeout=30)
            response.raise_for_status()
            
            content_type = response.headers.get("content-type", "")
            
            # 检查是否是错误JSON
            if "application/json" in content_type:
                error_data = response.json()
                err_no = error_data.get("err_no", 0)
                err_msg = error_data.get("err_msg", "")
                if err_no != 0:
                    raise RuntimeError(f"合成失败 {err_no}: {err_msg}")
            
            # 返回音频数据
            return response.content
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"合成请求网络错误: {e}")
    
    def synthesize_text(self, text: str, spd: int = None, pit: int = None,
                       vol: int = None, aue: int = None, per: int = None) -> bytes:
        """
        合成普通文本（单音色）
        
        Args:
            text: 要合成的文本
            spd, pit, vol, aue, per: 同上
            
        Returns:
            音频二进制数据
        """
        # 根据认证类型构建参数
        params = {
            "tex": text,
            "cuid": "openclaw_tts_client",
            "ctp": 1,
            "lan": "zh",
        }
        
        # 添加认证参数
        if self.auth_type == "token":
            token = self.get_access_token()
            if token:
                params["tok"] = token
            else:
                raise ValueError("access_token 为空")
        elif self.auth_type == "iam":
            params["iam-apikey"] = self.iam_key
        elif self.auth_type == "apikey_secret":
            token = self.get_access_token()
            if token:
                params["tok"] = token
            else:
                raise ValueError("获取 access_token 失败")
        else:
            raise ValueError(f"不支持的认证类型: {self.auth_type}")
        
        if spd is not None:
            params["spd"] = spd
        if pit is not None:
            params["pit"] = pit
        if vol is not None:
            params["vol"] = vol
        if aue is not None:
            params["aue"] = aue
        if per is not None:
            params["per"] = per
        
        try:
            response = requests.post(self.TTS_URL, data=params, timeout=30)
            response.raise_for_status()
            
            content_type = response.headers.get("content-type", "")
            
            if "application/json" in content_type:
                error_data = response.json()
                err_no = error_data.get("err_no", 0)
                err_msg = error_data.get("err_msg", "")
                if err_no != 0:
                    raise RuntimeError(f"合成失败 {err_no}: {err_msg}")
            
            return response.content
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"合成请求网络错误: {e}")
    
    def save_audio(self, audio_data: bytes, output_path: str):
        """保存音频数据到文件"""
        with open(output_path, "wb") as f:
            f.write(audio_data)
        print(f"音频已保存: {output_path} ({len(audio_data)} bytes)")

def main():
    parser = argparse.ArgumentParser(
        description="百度智能云语音合成 (TTS) 命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 单个对话文件合成
  python baidu_tts.py --input dialogue.txt --output conversation.mp3
  
  # 指定音色映射
  python baidu_tts.py --input script.txt --map 小明:1 小红:0 老师:106
  
  # 批量处理目录
  python baidu_tts.py --dir ./dialogues --format mp3
  
  # 调节参数
  python baidu_tts.py --input text.txt --spd 7 --pit 6 --vol 5 --aue 3
  
  # 直接合成SSML文件
  python baidu_tts.py --ssml input.ssml --output audio.mp3
        """
    )
    
    # 输入选项
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--input", "-i", help="输入文本文件路径")
    input_group.add_argument("--text", "-t", help="直接输入文本")
    input_group.add_argument("--ssml", "-s", help="输入SSML文件路径")
    input_group.add_argument("--dir", "-d", help="批量处理目录路径")
    
    # 输出选项
    parser.add_argument("--output", "-o", help="输出音频文件路径（默认: output.mp3）", default="output.mp3")
    parser.add_argument("--format", "-f", help="批量处理时的音频格式（默认: mp3）", default="mp3")
    
    # 音色映射
    parser.add_argument("--map", "-m", nargs="+", help="角色->音色映射，如 '小明:1' '小红:0'")
    parser.add_argument("--voice", "-v", type=int, help="单音色模式下的音色代码（默认: 511）", default=511)
    
    # 音频参数
    parser.add_argument("--spd", type=int, help="语速 0-15（默认: 5）", default=5)
    parser.add_argument("--pit", type=int, help="音调 0-15（默认: 5）", default=5)
    parser.add_argument("--vol", type=int, help="音量 0-15（默认: 5）", default=5)
    parser.add_argument("--aue", type=int, help="音频格式 3=mp3, 4=pcm, 6=wav（默认: 3）", default=3)
    
    # 其他选项
    parser.add_argument("--segment-mode", action="store_true", help="显式启用分段合成模式（绕过百度API多音色限制）")
    parser.add_argument("--force-ssml", action="store_true", help="强制使用SSML模式（即使检测到多音色也尝试使用API，可能失败）")
    parser.add_argument("--pause", type=int, help="分段合成时的静音间隔毫秒数（默认: 300）", default=300)
    parser.add_argument("--keep-temp", action="store_true", help="保留临时文件（用于调试）")
    parser.add_argument("--verbose", action="store_true", help="显示详细信息")
    # 兼容旧版参数
    parser.add_argument("--merge", action="store_true", help="已弃用，使用分段合并回退方案（如果SSML失败）")
    
    args = parser.parse_args()
    
    # 检查环境变量
    baidu_api_key = os.getenv("BAIDU_API_KEY")
    baidu_secret_key = os.getenv("BAIDU_SECRET_KEY")
    
    if not baidu_api_key:
        print("错误: 请设置环境变量 BAIDU_API_KEY")
        print("支持以下格式：")
        print("1. access_token（以 '1.' 开头，从百度AI开放平台获取）")
        print("2. IAM Key（以 'bce-v3/' 开头，从百度智能云控制台获取）")
        print("3. 普通 API Key（需要同时设置 BAIDU_SECRET_KEY）")
        sys.exit(1)
    
    # 判断是否需要 Secret Key
    needs_secret = True
    if baidu_api_key.startswith("1."):
        # access_token 格式，不需要 Secret Key
        needs_secret = False
        print("检测到 access_token 格式，将使用 tok 参数认证")
    elif baidu_api_key.startswith("bce-v3/"):
        # IAM Key 格式，不需要 Secret Key
        needs_secret = False
        print("检测到 IAM Key 格式，将使用 iam-apikey 参数认证")
    else:
        # 普通 API Key，需要 Secret Key
        if not baidu_secret_key:
            print("错误: 普通 API Key 需要同时设置 BAIDU_SECRET_KEY")
            print("或提供 access_token（以 '1.' 开头）或 IAM Key（以 'bce-v3/' 开头）")
            sys.exit(1)
        print("检测到 API Key + Secret Key 模式，将自动获取 access_token")
    
    # 初始化客户端
    try:
        client = BaiduTTSClient()
        
        # 设置分段合成选项
        if args.segment_mode:
            client.segment_mode = True
            print("分段模式已启用")
        if args.force_ssml:
            client.force_ssml = True
            print("强制SSML模式已启用")
        
    except ValueError as e:
        print(f"初始化失败: {e}")
        sys.exit(1)
    
    # 批量处理目录
    if args.dir:
        process_directory(client, args)
        return
    
    # 处理单个文件
    try:
        # 读取输入内容
        if args.text:
            content = args.text
            is_ssml = False
        elif args.ssml:
            with open(args.ssml, "r", encoding="utf-8") as f:
                content = f.read()
            is_ssml = True
        else:  # args.input
            with open(args.input, "r", encoding="utf-8") as f:
                content = f.read()
            is_ssml = False
        
        # 如果是普通文本且需要音色映射，转换为SSML
        if not is_ssml and args.map and DialogueFormatter:
            # 创建音色映射器
            voice_map = {}
            for mapping in args.map:
                if ":" not in mapping:
                    print(f"警告: 忽略无效映射 '{mapping}'，格式应为 '角色:音色代码'")
                    continue
                role, voice = mapping.split(":", 1)
                try:
                    voice_map[role.strip()] = int(voice.strip())
                except ValueError:
                    print(f"警告: 音色代码必须为整数 '{voice}'")
            
            if voice_map:
                formatter = DialogueFormatter()
                ssml_text = formatter.text_to_ssml(content, voice_map)
                is_ssml = True
                content = ssml_text
                print("已将对话文本转换为SSML格式")
        
        # 合成语音
        if args.verbose:
            print(f"参数: spd={args.spd}, pit={args.pit}, vol={args.vol}, aue={args.aue}, per={args.voice}")
        
        if is_ssml:
            try:
                audio_data = client.synthesize_ssml(
                    content, spd=args.spd, pit=args.pit, 
                    vol=args.vol, aue=args.aue, per=args.voice,
                    pause_ms=args.pause
                )
                print("SSML模式合成成功")
            except Exception as e:
                print(f"SSML模式失败: {e}")
                if args.merge:
                    print("尝试分段合并回退方案...")
                    audio_data = fallback_merge(client, content, args)
                else:
                    raise
        else:
            # 单音色普通文本
            audio_data = client.synthesize_text(
                content, spd=args.spd, pit=args.pit,
                vol=args.vol, aue=args.aue, per=args.voice
            )
            print("单音色文本合成成功")
        
        # 保存音频
        client.save_audio(audio_data, args.output)
        
    except Exception as e:
        print(f"处理失败: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def process_directory(client, args):
    """批量处理目录中的所有文本文件"""
    dir_path = Path(args.dir)
    if not dir_path.is_dir():
        print(f"错误: '{args.dir}' 不是有效目录")
        sys.exit(1)
    
    output_dir = dir_path / "output"
    output_dir.mkdir(exist_ok=True)
    
    # 查找文本文件
    text_files = list(dir_path.glob("*.txt")) + list(dir_path.glob("*.text"))
    
    if not text_files:
        print(f"在 '{args.dir}' 中未找到文本文件 (*.txt, *.text)")
        return
    
    print(f"找到 {len(text_files)} 个文本文件，开始批量处理...")
    
    for i, text_file in enumerate(text_files, 1):
        output_file = output_dir / f"{text_file.stem}.{args.format}"
        
        print(f"[{i}/{len(text_files)}] 处理: {text_file.name} -> {output_file.name}")
        
        try:
            with open(text_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 简单处理：单音色合成
            audio_data = client.synthesize_text(
                content, spd=args.spd, pit=args.pit,
                vol=args.vol, aue=args.aue, per=args.voice
            )
            
            with open(output_file, "wb") as f:
                f.write(audio_data)
            
            print(f"  成功: {output_file.name}")
            
        except Exception as e:
            print(f"  失败: {e}")
    
    print(f"\n批量处理完成，输出目录: {output_dir}")

def fallback_merge(client, ssml_text, args):
    """
    分段合并回退方案
    解析SSML，按不同音色分段合成，然后合并
    """
    if not AudioMerger or not DialogueFormatter:
        raise RuntimeError("回退方案需要 audio_merger 和 dialogue_formatter 模块")
    
    # 解析SSML获取分段
    formatter = DialogueFormatter()
    segments = formatter.parse_ssml_segments(ssml_text)
    
    if not segments:
        raise RuntimeError("无法从SSML解析出语音分段")
    
    print(f"分段合成: {len(segments)} 个片段")
    
    audio_files = []
    temp_dir = Path("temp_audio")
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # 逐个合成
        for i, (text, voice_name, voice_id) in enumerate(segments, 1):
            print(f"  片段 {i}: 音色={voice_name}({voice_id}), 文本='{text[:50]}...'")
            
            # 合成该片段
            audio_data = client.synthesize_text(
                text, spd=args.spd, pit=args.pit,
                vol=args.vol, aue=args.aue, per=voice_id
            )
            
            # 保存临时文件
            temp_file = temp_dir / f"segment_{i}.mp3"
            with open(temp_file, "wb") as f:
                f.write(audio_data)
            
            audio_files.append(str(temp_file))
        
        # 合并音频
        merger = AudioMerger()
        merged_audio = merger.merge_audio_files(audio_files, pause_ms=args.pause)
        
        return merged_audio
        
    finally:
        # 清理临时文件
        for temp_file in temp_dir.glob("segment_*.mp3"):
            try:
                temp_file.unlink()
            except OSError:
                pass  # Cleanup failure is non-critical
        
        try:
            temp_dir.rmdir()
        except OSError:
            pass  # Cleanup failure is non-critical

if __name__ == "__main__":
    main()