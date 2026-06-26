#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audio Announcement Player - PyGame Version (v2.2.0)
使用 pygame.mixer 播放，高质量、低延迟

强制播报规则（每次交互必须遵守）:
- 类型: receive, task, complete, error
- 原则: 简洁≤20字 | 口语化 | 不带名称 | 信息丰富
- 示例:
    receive: "收到上传指令"
    task: "准备发布到GitHub"
    complete: "上传完成"
    error: "网络连接失败"

详细规则见: skills/beep-skills/SKILL.md
"""

import os
import sys
import subprocess
import tempfile
import hashlib
import shutil
import time
import threading
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# 配置（会从配置文件覆盖）
CACHE_DIR = Path.home() / ".cache" / "audio-announcement"
TEMP_DIR = Path(tempfile.gettempdir()) / "audio-announcement"
MAX_RETRIES = 3
KEEP_TEMP_FILES = False  # v2.1.0: 改为 False，自动清理
VOLUME = 0.1  # 默认音量（会被配置文件覆盖）

def load_config():
    """加载配置文件（支持热重载）"""
    global VOLUME
    config_path = Path.home() / ".config" / "audio-announcement" / "config.json"
    
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                VOLUME = config.get('volume', 0.1)
                logger.debug(f"配置加载成功: volume={VOLUME}")
        except json.JSONDecodeError as e:
            logger.error(f"配置文件 JSON 解析失败: {e}")
        except Exception as e:
            logger.warning(f"加载配置失败，使用默认音量: {e}")
    else:
        logger.info(f"配置文件不存在，使用默认音量: {VOLUME*100:.0f}%")

def ensure_dirs():
    """确保目录存在"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

def get_cache_key(text: str, voice: str) -> str:
    """生成缓存键（MD5）"""
    key_str = f"{text}-{voice}"
    return hashlib.md5(key_str.encode('utf-8')).hexdigest()

def cleanup_old_cache(keep_count: int = 100):
    """LRU 缓存清理（保留最新的 N 个文件）"""
    try:
        cache_files = list(CACHE_DIR.glob("*.mp3"))
        if len(cache_files) > keep_count:
            # 按修改时间排序（最新的在前）
            sorted_files = sorted(cache_files, key=lambda f: f.stat().st_mtime, reverse=True)
            old_files = sorted_files[keep_count:]
            for f in old_files:
                f.unlink(missing_ok=True)
            logger.debug(f"清理了 {len(old_files)} 个旧缓存文件")
    except Exception as e:
        logger.warning(f"缓存清理失败: {e}")

def generate_audio(text: str, voice: str, output_file: str) -> bool:
    """
    生成 MP3（增强版：重试、错误处理、编码容错）
    
    Returns:
        bool: 成功 True，失败 False
    """
    logger.info(f"生成语音: {text[:50]}...")
    
    cache_key = get_cache_key(text, voice)
    cached_file = CACHE_DIR / f"{cache_key}.mp3"
    
    # 检查缓存
    if cached_file.exists():
        logger.debug("使用缓存文件")
        try:
            shutil.copy2(cached_file, output_file)
            return True
        except Exception as e:
            logger.warning(f"缓存复制失败，重新生成: {e}")
    
    # 重试生成
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # 使用 python -m edge_tts（不依赖 PATH）
            cmd = [
                sys.executable, "-m", "edge_tts",
                "--text", text,
                "--voice", voice,
                "--write-media", output_file
            ]
            
            logger.debug(f"尝试生成 ({attempt}/{MAX_RETRIES})...")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',  # 编码容错
                timeout=30,
                cwd=Path.cwd()  # 明确工作目录
            )
            
            if result.returncode == 0 and Path(output_file).exists():
                file_size = Path(output_file).stat().st_size
                if file_size > 1000:  # 至少 1KB
                    # 保存到缓存
                    try:
                        shutil.copy2(output_file, cached_file)
                        logger.debug(f"生成成功，缓存已保存")
                    except Exception as e:
                        logger.warning(f"缓存保存失败: {e}")
                    return True
                else:
                    logger.warning(f"生成文件太小 ({file_size} bytes)，可能损坏")
            else:
                logger.warning(f"edge-tts 失败: {result.stderr.strip() or 'unknown error'}")
        
        except subprocess.TimeoutExpired:
            logger.error(f"生成超时（30秒）")
        except FileNotFoundError:
            logger.critical("edge-tts 模块未找到，请安装: pip install edge-tts")
            return False  # 不可恢复错误
        except Exception as e:
            logger.error(f"生成异常: {e}")
        
        if attempt < MAX_RETRIES:
            wait_time = 2 ** attempt  # 指数退避
            logger.info(f"等待 {wait_time} 秒后重试...")
            time.sleep(wait_time)
    
    logger.error("语音生成失败（已达最大重试次数）")
    return False

def play_pygame(audio_file: str) -> bool:
    """
    使用 pygame 播放（增强版：错误处理、资源清理）
    
    Returns:
        bool: 成功 True，失败 False
    """
    try:
        import pygame
        
        # 初始化 mixer
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        except Exception as e:
            logger.error(f"pygame mixer 初始化失败: {e}")
            return False
        
        # 设置音量（全局 VOLUME）
        pygame.mixer.music.set_volume(VOLUME)
        
        # 加载音频
        try:
            pygame.mixer.music.load(audio_file)
        except Exception as e:
            logger.error(f"加载音频失败: {e}")
            return False
        
        # 播放
        try:
            pygame.mixer.music.play()
        except Exception as e:
            logger.error(f"播放失败: {e}")
            return False
        
        logger.debug(f"pygame 播放开始 (音量: {VOLUME*100:.0f}%)")
        
        # 等待播放完成
        while pygame.mixer.music.get_busy():
            time.sleep(0.05)
        
        logger.debug("pygame 播放完成")
        return True
        
    except ImportError:
        logger.error("pygame 未安装，请运行: pip install pygame")
        return False
    except Exception as e:
        logger.error(f"pygame 播放异常: {e}")
        return False

def announce(type_: str, message: str, lang: str = "zh") -> bool:
    """
    播报主函数（独立脚本版本）
    
    注意：此函数为独立脚本设计，不依赖 announce_helper.py 的复杂逻辑
    适合作为独立进程运行
    """
    # 音色映射
    VOICES = {
        "zh": "zh-CN-XiaoxiaoNeural",
        "en": "en-US-JennyNeural",
        "ja": "ja-JP-NanamiNeural",
        "ko": "ko-KR-SunHiNeural",
        "es": "es-ES-ElviraNeural",
        "fr": "fr-FR-DeniseNeural",
        "de": "de-DE-KatjaNeural",
    }
    voice = VOICES.get(lang, VOICES["zh"])
    
    # 消息前缀
    PREFIXES = {
        "task": "任务: ",
        "complete": "完成: ",
        "error": "警告: ",
    }
    full_message = PREFIXES.get(type_, "") + message
    
    # 准备临时文件
    ensure_dirs()
    timestamp = int(time.time() * 1000)
    temp_mp3 = TEMP_DIR / f"announce_{os.getpid()}_{timestamp}.mp3"
    
    try:
        # 步骤1: 生成音频
        if not generate_audio(full_message, voice, str(temp_mp3)):
            logger.error("音频生成失败")
            return False
        
        # 步骤2: 播放
        if not play_pygame(str(temp_mp3)):
            logger.error("pygame 播放失败")
            # Windows 没有 pygame 无法降级
            if sys.platform == "win32":
                return False
            # 尝试系统播放器（macOS/Linux）
            logger.info("尝试系统播放器...")
            return fallback_play(str(temp_mp3))
        
        return True
        
    except Exception as e:
        logger.error(f"播报异常: {e}")
        return False
    finally:
        # 清理临时文件
        if not KEEP_TEMP_FILES:
            try:
                if temp_mp3.exists():
                    temp_mp3.unlink()
            except Exception:
                pass

def fallback_play(audio_file: str) -> bool:
    """降级方案：使用系统播放器"""
    if sys.platform == "win32":
        logger.error("Windows 平台需要 pygame，请安装: pip install pygame")
        return False
    
    players = {
        "darwin": ["afplay"],
        "linux": ["mpg123", "ffplay", "aplay", "cvlc"]
    }
    
    platform_key = sys.platform
    if platform_key == "darwin":
        player_cmd = ["afplay"]
    elif platform_key == "linux":
        for player in ["mpg123", "ffplay", "aplay", "cvlc"]:
            if shutil.which(player):
                player_cmd = [player]
                break
        else:
            logger.error("未找到系统播放器（mpg123/ffplay/aplay/cvlc）")
            return False
    else:
        logger.error(f"不支持的平台: {sys.platform}")
        return False
    
    try:
        result = subprocess.run(
            player_cmd + [audio_file],
            capture_output=True,
            timeout=60,
            encoding='utf-8',
            errors='replace'
        )
        if result.returncode == 0:
            logger.debug(f"系统播放成功: {player_cmd[0]}")
            return True
        else:
            logger.error(f"系统播放失败: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"系统播放异常: {e}")
        return False

def cleanup_temp_files_async(file_path: Path):
    """异步清理临时文件"""
    def _cleanup():
        time.sleep(10)
        try:
            file_path.unlink(missing_ok=True)
        except Exception:
            pass
    threading.Thread(target=_cleanup, daemon=True).start()

# ============ 主程序 ============
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 加载配置
    load_config()
    ensure_dirs()
    
    # 参数检查
    if len(sys.argv) < 3:
        print("用法: python announce_pygame.py <type> <message> [lang]", file=sys.stderr)
        print("示例: python announce_pygame.py complete '任务完成' zh", file=sys.stderr)
        print("\n可用类型: receive, task, complete, error", file=sys.stderr)
        sys.exit(1)
    
    type_ = sys.argv[1]
    message = sys.argv[2]
    lang = sys.argv[3] if len(sys.argv) > 3 else "zh"
    
    # 执行播报
    logger.info(f"开始播报: [{type_}] {message} (lang={lang})")
    success = announce(type_, message, lang)
    
    if success:
        logger.info("播报完成")
        sys.exit(0)
    else:
        logger.error("播报失败")
        sys.exit(1)
