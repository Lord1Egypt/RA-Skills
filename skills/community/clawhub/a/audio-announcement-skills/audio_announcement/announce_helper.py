#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音播报助手 - 跨平台简化集成
自动选择最佳播报方案（pygame 优先，fallback 到 shell 脚本）

版本: 2.2.0
"""

import os
import sys
import subprocess
import threading
import json
import logging
import time
import tempfile
import hashlib
import shutil
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from functools import wraps

# 配置日志
def setup_logging(level=logging.INFO):
    """配置结构化日志"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

logger = logging.getLogger(__name__)

__version__ = "2.2.0"

# 用户配置目录
CONFIG_DIR = Path.home() / ".config" / "audio-announcement"
CONFIG_FILE = CONFIG_DIR / "config.json"

# 缓存目录
CACHE_DIR = Path.home() / ".cache" / "audio-announcement"
TEMP_DIR = Path(tempfile.gettempdir()) / "audio-announcement"

# ============ 模块级常量 ============

# 语言 → edge-tts 音色映射
VOICES: Dict[str, str] = {
    "zh": "zh-CN-XiaoxiaoNeural",
    "en": "en-US-JennyNeural",
    "ja": "ja-JP-NanamiNeural",
    "ko": "ko-KR-SunHiNeural",
    "es": "es-ES-ElviraNeural",
    "fr": "fr-FR-DeniseNeural",
    "de": "de-DE-KatjaNeural",
}

# 播报类型 → 语音前缀
SPEAK_PREFIXES: Dict[str, str] = {
    "task": "任务: ",
    "complete": "完成: ",
    "error": "警告: ",
    "receive": "",
}

# 播报类型 → 日志前缀（降级为纯日志时使用）
LOG_PREFIXES: Dict[str, str] = {
    "receive": "[RECV]",
    "task": "[TASK]",
    "complete": "[DONE]",
    "error": "[ERR]",
}

def retry(max_attempts=3, delay=1, backoff=2):
    """重试装饰器（用于网络调用）"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts:
                        wait = delay * (backoff ** (attempt - 1))
                        logger.warning(f"第{attempt}次尝试失败: {e}，{wait}秒后重试...")
                        time.sleep(wait)
                    else:
                        logger.error(f"重试{max_attempts}次后仍失败")
            raise last_exception
        return wrapper
    return decorator

@dataclass
class AnnouncementConfig:
    """播报配置（带验证）"""
    enabled: bool = True
    default_lang: str = "zh"
    volume: float = 0.25  # 默认 25% 音量
    async_default: bool = True
    cache_enabled: bool = True
    log_level: str = "INFO"  # 提高默认日志级别
    prefer_pygame: bool = True
    fallback_to_shell: bool = True
    
    # v2.1.0 新增字段
    max_cache_files: int = 100  # LRU 缓存限制
    voice_override: Optional[str] = None  # 自定义音色
    retry_attempts: int = 3  # 网络重试次数
    
    def __post_init__(self):
        """配置验证"""
        assert 0.0 <= self.volume <= 1.0, f"音量必须在 0-1 之间，当前: {self.volume}"
        assert self.log_level in ["DEBUG", "INFO", "WARNING", "ERROR"], f"无效的日志级别: {self.log_level}"
        assert 1 <= self.max_cache_files <= 1000, "max_cache_files 范围 1-1000"
    
    @classmethod
    def load(cls) -> "AnnouncementConfig":
        """从配置文件加载（带容错）"""
        config_data = {}
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"配置文件 JSON 解析失败: {e}，使用默认配置")
                return cls()
            except Exception as e:
                logger.warning(f"加载配置失败: {e}，使用默认配置")
                return cls()
        
        # 过滤未知字段（向前兼容）
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in config_data.items() if k in valid_fields}
        
        return cls(**filtered_data)
    
    def save(self):
        """保存配置到文件"""
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.__dict__, f, indent=2, ensure_ascii=False)
            logger.debug(f"配置已保存: {CONFIG_FILE}")
        except Exception as e:
            logger.error(f"保存配置失败: {e}")
    
    def update(self, **kwargs):
        """动态更新配置（热重载）"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                logger.debug(f"配置更新: {key} = {value}")
            else:
                logger.warning(f"忽略未知配置项: {key}")
        self.save()

# 全局配置
_config = AnnouncementConfig.load()
setup_logging(getattr(logging, _config.log_level))

# ============ 统计与监控 ============
class StatsCollector:
    """运行时统计收集器"""
    def __init__(self):
        self.lock = threading.Lock()
        self.total_announcements = 0
        self.success_count = 0
        self.failure_count = 0
        self.start_time = time.time()
    
    def record(self, success: bool):
        with self.lock:
            self.total_announcements += 1
            if success:
                self.success_count += 1
            else:
                self.failure_count += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        uptime = time.time() - self.start_time
        success_rate = (self.success_count / self.total_announcements * 100) if self.total_announcements > 0 else 0
        
        return {
            "total_announcements": self.total_announcements,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "success_rate": f"{success_rate:.1f}%",
            "uptime_seconds": int(uptime),
            "cache_size_mb": self._get_cache_size_mb(),
            "cache_file_count": self._get_cache_file_count()
        }
    
    def _get_cache_file_count(self) -> int:
        cache_path = Path(CACHE_DIR)
        if cache_path.exists():
            return len(list(cache_path.glob("*.mp3")))
        return 0
    
    def _get_cache_size_mb(self) -> float:
        cache_path = Path(CACHE_DIR)
        if cache_path.exists():
            total = sum(f.stat().st_size for f in cache_path.glob("*.mp3") if f.is_file())
            return round(total / 1024 / 1024, 2)
        return 0.0

_stats = StatsCollector()

# ============ 辅助函数 ============
def ensure_dirs():
    """确保目录存在"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

def get_cache_key(text: str, voice: str) -> str:
    """生成缓存键（MD5）"""
    key_str = f"{text}-{voice}"
    return hashlib.md5(key_str.encode('utf-8')).hexdigest()

def safe_path_str(path: Path) -> str:
    """安全路径字符串（处理中文和空格）"""
    return str(path.resolve())

@retry(max_attempts=3, delay=1, backoff=2)
def generate_audio(text: str, voice: str, output_file: str) -> bool:
    """
    使用 edge-tts 生成音频（带重试）
    
    Args:
        text: 文本内容
        voice: 音色 ID
        output_file: 输出 MP3 文件路径
    
    Returns:
        bool: 生成是否成功
    """
    cache_key = get_cache_key(text, voice)
    cached_file = CACHE_DIR / f"{cache_key}.mp3"
    
    # 检查缓存
    if cached_file.exists():
        logger.debug(f"使用缓存: {cached_file.name}")
        shutil.copy2(cached_file, output_file)
        return True
    
    logger.info(f"生成语音: {text[:40]}...")
    
    # 使用 python -m edge_tts（不依赖 PATH）
    cmd = [
        sys.executable, "-m", "edge_tts",
        "--text", text,
        "--voice", voice,
        "--write-media", output_file
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=30
        )
        
        if result.returncode == 0 and Path(output_file).exists() and Path(output_file).stat().st_size > 0:
            # 保存到缓存
            shutil.copy2(output_file, cached_file)
            logger.debug("语音生成成功")
            return True
        else:
            logger.error(f"edge-tts 失败: {result.stderr.strip() or '未知错误'}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("edge-tts 超时（30秒）")
        return False
    except Exception as e:
        logger.error(f"生成音频异常: {e}")
        raise  # 触发重试

def cleanup_temp_files(keep_count: int = 50):
    """LRU 缓存清理（保留最新的 N 个文件）"""
    try:
        cache_files = list(CACHE_DIR.glob("*.mp3"))
        if len(cache_files) > keep_count:
            # 按修改时间排序
            sorted_files = sorted(cache_files, key=lambda f: f.stat().st_mtime, reverse=True)
            old_files = sorted_files[keep_count:]
            for f in old_files:
                f.unlink(missing_ok=True)
            logger.debug(f"清理了 {len(old_files)} 个旧缓存文件")
    except Exception as e:
        logger.warning(f"缓存清理失败: {e}")

def cleanup_temp_files_async(file_path: Path):
    """异步删除单个临时文件"""
    def _delete():
        try:
            time.sleep(2)  # 等待播放器释放文件
            file_path.unlink(missing_ok=True)
        except Exception as e:
            logger.debug(f"异步清理失败（可忽略）: {e}")
    t = threading.Thread(target=_delete, daemon=True)
    t.start()

def play_pygame_safe(audio_file: str, volume: float) -> bool:
    """
    安全播放（pygame 方案）
    
    Args:
        audio_file: MP3 文件路径
        volume: 音量 0.0-1.0
    
    Returns:
        bool: 播放是否成功
    """
    try:
        import pygame
        
        # 初始化 mixer（更大缓冲区减少卡顿）
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        
        # 设置音量
        pygame.mixer.music.set_volume(volume)
        
        # 加载并播放
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        
        logger.debug(f"pygame 播放开始 (音量: {volume*100:.0f}%)")
        
        # 等待播放完成
        while pygame.mixer.music.get_busy():
            time.sleep(0.05)
        
        logger.debug("pygame 播放完成")
        return True
        
    except Exception as e:
        logger.error(f"pygame 播放失败: {e}")
        return False

def play_fallback_system(audio_file: str) -> bool:
    """
    降级方案：使用系统播放器
    
    Args:
        audio_file: MP3 文件路径
    
    Returns:
        bool: 播放是否成功
    """
    if sys.platform == "win32":
        logger.error("Windows 平台无 pygame 时无法播放，请安装: pip install pygame")
        return False
    
    # macOS/Linux 使用系统播放器
    players = {
        "darwin": ["afplay"],  # macOS
        "linux": ["mpg123", "ffplay", "aplay"]  # Linux 多种后备
    }
    
    platform_key = sys.platform
    if platform_key == "darwin":
        player_cmd = ["afplay"]
    elif platform_key == "linux":
        # 尝试找到可用的播放器
        player_cmd = None
        for p in ["mpg123", "ffplay", "aplay"]:
            if shutil.which(p):
                player_cmd = [p]
                break
        if not player_cmd:
            logger.error("未找到可用的系统播放器（mpg123/ffplay/aplay）")
            return False
    else:
        logger.error(f"不支持的平台: {sys.platform}")
        return False
    
    try:
        result = subprocess.run(
            player_cmd + [audio_file],
            capture_output=True,
            timeout=60
        )
        if result.returncode == 0:
            logger.debug(f"系统播放器成功: {player_cmd[0]}")
            return True
        else:
            logger.error(f"系统播放失败: {result.stderr.decode(errors='ignore')}")
            return False
    except Exception as e:
        logger.error(f"系统播放异常: {e}")
        return False

def announce(type_: str, message: str, lang: Optional[str] = None, 
             async_: Optional[bool] = None, timeout: int = 30) -> bool:
    """
    执行语音播报（多层降级策略）
    
    播放优先级：
    1. pygame（推荐，跨平台一致）
    2. shell 脚本（macOS/Linux 系统播放器）
    3. 仅日志（最后手段，不中断主流程）
    
    Args:
        type_: 播报类型 ("receive" / "task" / "complete" / "error")
        message: 播报内容（建议 ≤20 字，口语化）
        lang: 语言代码 ("zh"/"en"/"ja"/"ko"/"es"/"fr"/"de")
        async_: 是否异步（None 使用配置）
        timeout: 超时时间（秒）
    
    Returns:
        bool: 播报是否成功（False 仅表示播放失败，不影响主流程）
    """
    global _config
    
    # 禁用状态
    if not _config.enabled:
        return True
    
    # 参数处理
    lang = lang or _config.default_lang
    async_ = async_ if async_ is not None else _config.async_default
    
    # 音色选择
    voice = _config.voice_override or VOICES.get(lang, VOICES["zh"])
    
    # 拼接前缀 + 消息
    full_message = SPEAK_PREFIXES.get(type_, "") + message
    
    # 生成临时文件
    timestamp = int(time.time() * 1000)
    temp_file = TEMP_DIR / f"announce_{os.getpid()}_{timestamp}.mp3"
    
    try:
        # 步骤1: 生成音频（带重试）
        if not generate_audio(full_message, voice, safe_path_str(temp_file)):
            logger.error("音频生成失败，尝试降级方案...")
            return _fallback_announce(type_, message, lang)
        
        # 步骤2: 播放（多层降级）
        success = _play_with_fallback(safe_path_str(temp_file), _config.volume)
        
        if not success:
            logger.warning("所有播放方案失败，转为日志模式")
            return _fallback_announce(type_, message, lang)
        
        # 成功：异步清理临时文件
        if not async_:
            cleanup_temp_files_async(temp_file)
        else:
            # 异步模式下延迟清理
            threading.Thread(
                target=lambda: (time.sleep(10), temp_file.unlink(missing_ok=True)),
                daemon=True
            ).start()
        
        _stats.record(True)
        return True
        
    except Exception as e:
        logger.error(f"播报异常: {e}", exc_info=True)
        _stats.record(False)
        # 异常时也尝试降级
        return _fallback_announce(type_, message, lang)

def _play_with_fallback(audio_file: str, volume: float) -> bool:
    """
    多层播放降级策略
    
    优先级：
    1. pygame（配置启用且可用）
    2. 系统播放器（非 Windows）
    3. 仅日志（静默失败）
    """
    # 方案1: pygame
    if _config.prefer_pygame and _has_pygame():
        logger.debug("尝试 pygame 播放...")
        if play_pygame_safe(audio_file, volume):
            return True
        logger.warning("pygame 播放失败，尝试降级方案...")
    
    # 方案2: 系统播放器（仅非 Windows）
    if _config.fallback_to_shell and sys.platform != "win32":
        logger.debug("尝试系统播放器...")
        if play_fallback_system(audio_file):
            return True
        logger.warning("系统播放器也失败")
    
    return False

def _fallback_announce(type_: str, message: str, lang: str) -> bool:
    """
    最终降级：仅输出日志（不中断主流程）
    
    Args:
        type_: 播报类型
        message: 消息内容
        lang: 语言
    
    Returns:
        bool: 总是 True（静默处理）
    """
    prefix = LOG_PREFIXES.get(type_, "[LOG]")
    logger.info(f"{prefix}: {message} (语音播放失败，已降级为日志)")
    return True  # 静默成功，不影响主流程

def _has_pygame() -> bool:
    """检查 pygame 是否可用"""
    try:
        import pygame
        return True
    except ImportError:
        return False

def reload_config():
    """热重载配置文件（无需重启）"""
    global _config
    old_config = _config
    _config = AnnouncementConfig.load()
    # 更新日志级别
    setup_logging(getattr(logging, _config.log_level))
    logger.info("配置已重载（热重载）")
    return _config

# ============ 快捷函数 ============
def receive(msg: str, lang: Optional[str] = None, async_: Optional[bool] = None) -> bool:
    """收到消息"""
    return announce("receive", msg, lang=lang, async_=async_)

def task(msg: str, lang: Optional[str] = None, async_: Optional[bool] = None) -> bool:
    """任务进行中"""
    return announce("task", msg, lang=lang, async_=async_)

def complete(msg: str, lang: Optional[str] = None, async_: Optional[bool] = None) -> bool:
    """任务完成"""
    return announce("complete", msg, lang=lang, async_=async_)

def error(msg: str, lang: Optional[str] = None, async_: Optional[bool] = None) -> bool:
    """错误警告"""
    return announce("error", msg, lang=lang, async_=async_)

# ============ 环境自检 ============
class EnvironmentChecker:
    """环境自检工具（启动时自动运行）"""
    
    @staticmethod
    def check_all() -> Dict[str, Any]:
        """全面环境检查"""
        issues = []
        warnings = []
        results = {
            "python_version": None,
            "pygame_version": None,
            "edge_tts_available": False,
            "config_writable": False,
            "cache_writable": False,
            "audio_device_ok": False,
            "platform": sys.platform,
            "issues": issues,
            "warnings": warnings
        }
        
        # 1. Python 版本
        py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        results["python_version"] = py_version
        if sys.version_info < (3, 9):
            issues.append(f"Python 版本过低: {py_version} (推荐 3.9+)")
        
        # 2. pygame 检测
        try:
            import pygame
            results["pygame_version"] = pygame.version.ver
        except ImportError:
            issues.append("pygame 未安装（Windows 必须安装: pip install pygame）")
        except Exception as e:
            warnings.append(f"pygame 版本检测异常: {e}")
        
        # 3. edge-tts 可用性（快速检查）
        try:
            result = subprocess.run(
                [sys.executable, "-m", "edge_tts", "--help"],
                capture_output=True,
                timeout=5,
                encoding='utf-8',
                errors='replace'
            )
            results["edge_tts_available"] = result.returncode == 0
            if not results["edge_tts_available"]:
                warnings.append("edge-tts 模块响应异常")
        except FileNotFoundError:
            issues.append("edge-tts 未安装（必需: pip install edge-tts）")
        except subprocess.TimeoutExpired:
            warnings.append("edge-tts 响应超时（可能网络异常）")
        except Exception as e:
            warnings.append(f"edge-tts 检测失败: {e}")
        
        # 4. 配置目录权限
        config_dir = Path.home() / ".config" / "audio-announcement"
        try:
            config_dir.mkdir(parents=True, exist_ok=True)
            test_file = config_dir / ".write_test"
            test_file.write_text("test", encoding='utf-8')
            test_file.unlink()
            results["config_writable"] = True
        except PermissionError:
            issues.append("配置目录不可写（权限不足）")
        except Exception as e:
            warnings.append(f"配置目录访问异常: {e}")
        
        # 5. 缓存目录权限
        cache_dir = Path.home() / ".cache" / "audio-announcement"
        try:
            cache_dir.mkdir(parents=True, exist_ok=True)
            test_file = cache_dir / ".write_test"
            test_file.write_bytes(b"test")
            test_file.unlink()
            results["cache_writable"] = True
        except PermissionError:
            warnings.append("缓存目录不可写（可能影响缓存功能）")
        except Exception as e:
            warnings.append(f"缓存目录访问异常: {e}")
        
        # 6. 音频设备检测（仅 pygame 可用时）
        if results["pygame_version"]:
            try:
                import pygame
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
                pygame.mixer.quit()
                results["audio_device_ok"] = True
            except Exception as e:
                warnings.append(f"音频设备初始化失败: {e}")
                results["audio_device_ok"] = False
        
        return results
    
    @staticmethod
    def log_check_results(results: Dict[str, Any]):
        """记录检查结果"""
        logger.info("=== 环境自检结果 ===")
        logger.info(f"  平台: {results['platform']}")
        logger.info(f"  Python: {results['python_version']}")
        logger.info(f"  pygame: {results['pygame_version'] or '未安装'}")
        logger.info(f"  edge-tts: {'可用' if results['edge_tts_available'] else '不可用'}")
        logger.info(f"  配置目录: {'可写' if results['config_writable'] else '不可写'}")
        logger.info(f"  缓存目录: {'可写' if results['cache_writable'] else '不可写'}")
        logger.info(f"  音频设备: {'正常' if results['audio_device_ok'] else '异常'}")
        
        if results["issues"]:
            logger.error("【严重问题】")
            for issue in results["issues"]:
                logger.error(f"  [FAIL] {issue}")
        
        if results["warnings"]:
            logger.warning("【警告】")
            for warning in results["warnings"]:
                logger.warning(f"  [WARN]️ {warning}")
        
        if not results["issues"] and not results["warnings"]:
            logger.info("[OK] 环境检查通过，所有功能正常")

# ============ 高级助手类 ============
class AnnouncementHelper:
    """高级助手：提供更多控制和查询"""
    
    def __init__(self):
        self.config = _config
        # 启动时自动环境自检（提升日志级别以确保可见）
        old_level = logger.level
        logger.setLevel(logging.INFO)
        env_results = EnvironmentChecker.check_all()
        EnvironmentChecker.log_check_results(env_results)
        logger.setLevel(old_level)
        
        # 如果有严重问题，记录到统计但不阻止使用
        if env_results["issues"]:
            _stats.record(False)  # 记录一次失败，提醒用户
    
    def announce(self, type_: str, message: str, lang: Optional[str] = None, 
                 async_: Optional[bool] = None) -> bool:
        """使用当前配置播报"""
        return announce(type_, message, lang=lang, async_=async_)
    
    def is_enabled(self) -> bool:
        return self.config.enabled
    
    def enable(self):
        self.config.enabled = True
        self.config.save()
        logger.info("播报已启用")
    
    def disable(self):
        self.config.enabled = False
        self.config.save()
        logger.info("播报已禁用")
    
    def set_volume(self, volume: float):
        """设置音量（0.0-1.0）并立即生效"""
        self.config.volume = max(0.0, min(1.0, volume))
        self.config.save()
        logger.info(f"音量设置为: {volume*100:.0f}%")
    
    def set_language(self, lang: str):
        """设置默认语言"""
        if lang in ["zh", "en", "ja", "ko", "es", "fr", "de"]:
            self.config.default_lang = lang
            self.config.save()
            logger.info(f"默认语言设置为: {lang}")
        else:
            logger.warning(f"不支持的语言: {lang}")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取使用统计（合并配置统计和运行时统计）"""
        cache_stats = {
            "cache_size_mb": _stats._get_cache_size_mb(),
            "cache_file_count": _stats._get_cache_file_count(),
        }
        runtime_stats = _stats.get_stats()
        config_stats = {
            "enabled": self.config.enabled,
            "volume": self.config.volume,
            "default_lang": self.config.default_lang,
            "async_default": self.config.async_default,
            "prefer_pygame": self.config.prefer_pygame,
            "pygame_available": _has_pygame(),
            "platform": sys.platform,
            "log_level": self.config.log_level
        }
        return {**config_stats, **runtime_stats, **cache_stats}
    
    def clear_cache(self, keep_count: int = 50):
        """清理缓存文件"""
        cleanup_temp_files(keep_count)
        logger.info(f"缓存已清理（保留最新 {keep_count} 个）")
    
    def reload_config(self):
        """热重载配置文件"""
        reload_config()
        self.config = _config
        logger.info("配置已热重载")

# ============ 测试入口 ============
if __name__ == "__main__":
    setup_logging(logging.INFO)
    
    print(f"[Beep · 小喇叭 v{__version__}]")
    print(f"平台: {sys.platform}")
    print(f"pygame 可用: {_has_pygame()}")
    print(f"配置: {_config}")
    
    helper = AnnouncementHelper()
    
    print("\n=== 开始稳定性测试 ===")
    
    # 测试1: 基本播报
    print("\n1. 基础播报测试...")
    receive("系统启动测试")
    task("正在执行任务")
    complete("任务完成")
    error("错误测试")
    
    # 测试2: 统计查看
    print("\n2. 统计信息:")
    stats = helper.get_stats()
    for k, v in stats.items():
        print(f"   {k}: {v}")
    
    # 测试3: 配置热重载
    print("\n3. 配置热重载测试...")
    print(f"   当前音量: {helper.config.volume}")
    helper.set_volume(0.2)
    print(f"   新音量: {helper.config.volume}")
    helper.reload_config()
    print(f"   重载后音量: {helper.config.volume}")
    
    print("\n[OK] 测试完成")

# ============ 集成验证 ============

def verify_integration() -> bool:
    """
    一键集成验证：检查环境 + 播放所有类型测试语音
    
    Returns:
        bool: 所有检查是否通过
    """
    all_passed = True
    
    SEP = "=" * 60
    
    print(SEP)
    print("Beep · 小喇叭  [Integration Verify]  v" + __version__)
    print(SEP)
    
    # 1. 依赖检查
    print("\n[1/5] Dependencies")
    try:
        import pygame
        print(f"  [OK] pygame {pygame.version.ver}")
    except ImportError:
        print("  [FAIL] pygame not installed (pip install pygame)")
        all_passed = False
    
    try:
        import edge_tts
        print(f"  [OK] edge-tts installed")
    except ImportError:
        print("  [FAIL] edge-tts not installed (pip install edge-tts)")
        all_passed = False
    
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"  [OK] Python {py_ver}")
    
    # 2. 配置检查
    print("\n[2/5] Configuration")
    config_path = CONFIG_FILE
    if config_path.exists():
        try:
            with open(config_path, encoding='utf-8') as f:
                cfg = json.load(f)
            print(f"  [OK] Config file exists")
            print(f"       volume: {cfg.get('volume', 'N/A')}")
            print(f"       language: {cfg.get('default_lang', 'N/A')}")
            print(f"       async: {cfg.get('async_default', 'N/A')}")
        except Exception as e:
            print(f"  [WARN] Config parse error: {e}")
    else:
        print(f"  [WARN] Config not found, using defaults")
    
    # 3. 环境自检（复用 EnvironmentChecker）
    print("\n[3/5] Environment Check")
    try:
        env = EnvironmentChecker.check_all()
        issues = env.get("issues", [])
        warnings_list = env.get("warnings", [])
        
        if issues:
            for issue in issues:
                print(f"  [FAIL] {issue}")
                all_passed = False
        if warnings_list:
            for w in warnings_list:
                print(f"  [WARN] {w}")
        
        if not issues and not warnings_list:
            print(f"  [OK] All checks passed")
    except Exception as e:
        print(f"  [FAIL] Environment check error: {e}")
        all_passed = False
    
    # 4. 功能测试（播放 4 种类型）
    print("\n[4/5] Voice Test")
    tests = [
        ("receive", receive),
        ("task", task),
        ("complete", complete),
        ("error", error),
    ]
    
    for name, func in tests:
        try:
            print(f"  Testing {name}...", end=" ", flush=True)
            func(f"测试{name}类型")
            print("[OK]")
        except Exception as e:
            print(f"[FAIL] {e}")
            all_passed = False
    
    # 5. 系统状态
    print("\n[5/5] System Status")
    cache_path = CACHE_DIR
    if cache_path.exists():
        cache_files = list(cache_path.glob("*.mp3"))
        total_size = sum(f.stat().st_size for f in cache_files)
        print(f"  [OK] Cache: {len(cache_files)} files ({total_size / 1024 / 1024:.2f} MB)")
    
    print(f"  [OK] Version: {__version__}")
    print(f"  [{'OK' if all_passed else 'FAIL'}] Integration: {'READY' if all_passed else 'ISSUES FOUND'}")
    
    print(SEP)
    if all_passed:
        print("All checks passed! Beep is ready to use.")
    else:
        print("Some checks failed. See above for details.")
    print(SEP)
    
    return all_passed

