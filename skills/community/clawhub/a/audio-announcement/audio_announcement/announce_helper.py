#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音播报助手 - 跨平台简化集成
自动选择最佳播报方案（pygame 优先，fallback 到 shell 脚本）
"""

import os
import sys
import subprocess
import threading
import json
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)

# 包内脚本路径
try:
    from importlib.resources import files as pkg_files
    PACKAGE_DIR = pkg_files("audio_announcement")
    ANNOUNCE_PYGAME_SCRIPT = str(PACKAGE_DIR.joinpath("scripts", "announce_pygame.py"))
    ANNOUNCE_SH_SCRIPT = str(PACKAGE_DIR.joinpath("scripts", "announce.sh"))
except:
    # 回退：从当前模块位置计算
    script_dir = Path(__file__).parent / "scripts"
    ANNOUNCE_PYGAME_SCRIPT = str(script_dir / "announce_pygame.py")
    ANNOUNCE_SH_SCRIPT = str(script_dir / "announce.sh")

# 用户配置目录
CONFIG_DIR = Path.home() / ".config" / "audio-announcement"
CONFIG_FILE = CONFIG_DIR / "config.json"

@dataclass
class AnnouncementConfig:
    """播报配置"""
    enabled: bool = True
    default_lang: str = "zh"
    volume: float = 1.0
    async_default: bool = True   # 默认异步，减少阻塞
    cache_enabled: bool = True
    log_level: str = "WARNING"
    prefer_pygame: bool = True   # 优先使用 pygame 方案（跨平台一致体验）
    fallback_to_shell: bool = True  # 失败时回退到 shell 脚本
    
    @classmethod
    def load(cls) -> "AnnouncementConfig":
        """从配置文件加载，如果不存在则使用默认值"""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return cls(**data)
            except Exception as e:
                logger.warning(f"加载配置失败，使用默认值: {e}")
        return cls()
    
    def save(self):
        """保存配置到文件"""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, indent=2, ensure_ascii=False)

# 全局配置
_config = AnnouncementConfig.load()

def set_config(**kwargs):
    """更新配置并保存"""
    global _config
    for k, v in kwargs.items():
        if hasattr(_config, k):
            setattr(_config, k, v)
    _config.save()

def _has_pygame() -> bool:
    """检查 pygame 是否可用"""
    try:
        import pygame
        return True
    except ImportError:
        return False

def _run_pygame_script(type_, message, lang, async_, timeout):
    """使用 pygame 脚本播放"""
    if not os.path.exists(ANNOUNCE_PYGAME_SCRIPT):
        logger.warning(f"pygame 脚本不存在: {ANNOUNCE_PYGAME_SCRIPT}")
        return False
    
    cmd = [sys.executable, ANNOUNCE_PYGAME_SCRIPT, type_, message, lang]
    return _run_command(cmd, async_, timeout)

def _run_shell_script(type_, message, lang, async_, timeout):
    """使用 shell 脚本播放（macOS/Linux）"""
    if not os.path.exists(ANNOUNCE_SH_SCRIPT):
        logger.warning(f"shell 脚本不存在: {ANNOUNCE_SH_SCRIPT}")
        return False
    
    # shell 脚本需要可直接执行权限（在 Unix 系统上）
    if sys.platform != "win32":
        os.chmod(ANNOUNCE_SH_SCRIPT, 0o755)
    
    cmd = [ANNOUNCE_SH_SCRIPT, type_, message, lang]
    return _run_command(cmd, async_, timeout)

def _run_command(cmd, async_, timeout):
    """通用命令执行"""
    try:
        if async_:
            thread = threading.Thread(
                target=subprocess.run,
                args=(cmd,),
                kwargs={"capture_output": True, "timeout": timeout},
                daemon=True
            )
            thread.start()
            return True
        else:
            result = subprocess.run(cmd, capture_output=True, timeout=timeout)
            success = result.returncode == 0
            if not success:
                logger.warning(f"播报失败: {result.stderr.decode(errors='ignore')}")
            return success
    except Exception as e:
        logger.warning(f"播报异常: {e}")
        return False

def announce(type_, message, lang=None, async_=None, timeout=30):
    """
    执行语音播报（跨平台自动选择方案）
    
    自动选择逻辑：
    1. 如果 prefer_pygame=True 且 pygame 可用 → 使用 pygame 方案（推荐，体验一致）
    2. 否则使用 shell 脚本（macOS/Linux 用系统播放器，Windows 需要额外依赖）
    
    参数:
        type_: 播报类型 - "receive" / "task" / "complete" / "error"
        message: 播报内容（建议 ≤20 字，口语化）
        lang: 语言 - "zh" / "en" / "ja" / "ko" / "es" / "fr" / "de" (默认从配置读取)
        async_: 是否异步播放（默认从配置读取，通常为 True）
        timeout: 超时时间（秒）
    
    返回:
        bool: 播报是否成功
    """
    if not _config.enabled:
        return True  # 静默：如果禁用，视为成功
    
    if lang is None:
        lang = _config.default_lang
    if async_ is None:
        async_ = _config.async_default
    
    # 选择播放方案
    use_pygame = _config.prefer_pygame and _has_pygame()
    
    if use_pygame:
        logger.debug("使用 pygame 方案播放")
        success = _run_pygame_script(type_, message, lang, async_, timeout)
        if success or not _config.fallback_to_shell:
            return success
        logger.warning("pygame 方案失败，尝试 shell 方案...")
    
 # shell 方案（macOS/Linux）
    if sys.platform == "win32":
        logger.error("Windows 平台没有 pygame 时无法播放，请安装: pip install pygame")
        return False
    
    logger.debug("使用 shell 方案播放")
    return _run_shell_script(type_, message, lang, async_, timeout)

# 快捷函数
def receive(msg, lang=None): 
    return announce("receive", msg, lang=lang)

def task(msg, lang=None): 
    return announce("task", msg, lang=lang)

def complete(msg, lang=None): 
    return announce("complete", msg, lang=lang)

def error(msg, lang=None): 
    return announce("error", msg, lang=lang)

class AnnouncementHelper:
    """高级助手类，提供更多控制和状态查询"""
    
    def __init__(self):
        self.config = _config
    
    def is_enabled(self) -> bool:
        return self.config.enabled
    
    def enable(self):
        self.config.enabled = True
        self.config.save()
    
    def disable(self):
        self.config.enabled = False
        self.config.save()
    
    def set_volume(self, volume: float):
        """设置音量（0.0-1.0）"""
        self.config.volume = max(0.0, min(1.0, volume))
        self.config.save()
        # 注意：需要修改 announce_pygame.py 才能实时生效
    
    def get_stats(self) -> dict:
        """获取使用统计"""
        cache_dir = Path.home() / ".cache" / "audio-announcement"
        if cache_dir.exists():
            cache_files = list(cache_dir.glob("*.mp3"))
            return {
                "enabled": self.config.enabled,
                "cache_size_mb": sum(f.stat().st_size for f in cache_files if f.is_file()) / 1024 / 1024,
                "cache_file_count": len(cache_files),
                "prefer_pygame": self.config.prefer_pygame,
                "pygame_available": _has_pygame(),
                "platform": sys.platform
            }
        return {
            "enabled": self.config.enabled,
            "cache_size_mb": 0,
            "cache_file_count": 0,
            "prefer_pygame": self.config.prefer_pygame,
            "pygame_available": _has_pygame(),
            "platform": sys.platform
        }

if __name__ == "__main__":
    # 测试模式
    logging.basicConfig(level=logging.INFO)
    print(f"[audio-announcement 2.0.7] 跨平台测试模式")
    print(f"平台: {sys.platform}")
    print(f"pygame 可用: {_has_pygame()}")
    
    helper = AnnouncementHelper()
    print(f"配置: {helper.config}")
    
    print("\n开始测试...")
    receive("收到测试指令")
    task("正在执行任务")
    complete("任务完成")
    error("测试错误")
    
    print("\n统计:", helper.get_stats())
