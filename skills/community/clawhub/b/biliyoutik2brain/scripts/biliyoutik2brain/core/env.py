"""
环境感知模块 (v3.0)

自动检测当前运行在哪个 AI Agent 平台上，输出环境画像。
无需任何配置，零依赖启动。

检测逻辑:
  - 文件系统特征 (配置文件/目录/二进制路径)
  - 环境变量 (平台专属变量)
  - 硬件特征 (CPU型号/内存)
  - Python包特征 (已安装的包)

输出: EnvProfile, ASRCapability, LLMCapability
"""

import os, platform, sys, subprocess, time, shutil
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum


# ═══════════════════════════════════════════════════════════════
#  数据类型
# ═══════════════════════════════════════════════════════════════

class AgentType(Enum):
    WORKBUDDY_CLOUD  = "workbuddy_cloud"
    WORKBUDDY_LOCAL  = "workbuddy_local"
    OPENCLAW_PIP     = "openclaw_pip"
    OPENCLAW_DOCKER  = "openclaw_docker"
    OPENCLAW_SOURCE  = "openclaw_source"
    HERMES           = "hermes"
    GENERIC          = "generic"


class ASREngine(Enum):
    FASTER_WHISPER  = "faster_whisper"
    BAILIAN          = "bailian"          # 百炼ASR (DashScope)
    OPENAI_WHISPER   = "openai_whisper"
    NONE             = "none"


class LLMBackend(Enum):
    DEEPSEEK        = "deepseek"
    OPENAI          = "openai"
    OLLAMA          = "ollama"
    VLLM            = "vllm"
    NONE            = "none"


@dataclass
class ASRCapability:
    """当前环境可用的 ASR 引擎列表"""
    engines: List[ASREngine] = field(default_factory=list)
    default_engine: ASREngine = ASREngine.NONE
    gpu_available: bool = False
    max_realtime_factor: float = 1.0    # 转录速度 / 视频时长


@dataclass
class LLMCapability:
    """当前环境可用的 LLM 后端列表"""
    backends: List[LLMBackend] = field(default_factory=list)
    default_backend: LLMBackend = LLMBackend.NONE
    is_paid: bool = True
    max_tokens_per_call: int = 4096


@dataclass
class EnvProfile:
    """环境画像 — 所有模块的决策依据"""
    agent_type: AgentType
    cpu_cores: int
    ram_gb: float
    gpu_available: bool
    gpu_name: str = ""
    os_type: str = ""           # Windows / Linux / macOS
    home_dir: str = ""
    storage_path: str = ""      # 技能输出存储路径
    asr: ASRCapability = field(default_factory=ASRCapability)
    llm: LLMCapability = field(default_factory=LLMCapability)
    profile_summary: str = ""   # 一行总结


# 缓存: 只检测一次
_cached_profile: Optional[EnvProfile] = None


# ═══════════════════════════════════════════════════════════════
#  检测函数
# ═══════════════════════════════════════════════════════════════

def _get_cpu_cores() -> int:
    """获取 CPU 核心数"""
    try:
        return os.cpu_count() or 2
    except Exception:
        return 2


def _get_ram_gb() -> float:
    """获取内存大小 (GB)"""
    try:
        # 优先用 psutil (最可靠)
        import psutil
        return psutil.virtual_memory().total / (1024 ** 3)
    except ImportError:
        pass

    try:
        if sys.platform == "win32":
            # 用 wmic 取 TotalPhysicalMemory
            result = subprocess.run(
                ["wmic", "ComputerSystem", "get", "TotalPhysicalMemory"],
                capture_output=True, text=True, timeout=10
            )
            for line in result.stdout.splitlines():
                val = line.strip()
                if val.isdigit():
                    return int(val) / (1024 ** 3)
        else:
            with open("/proc/meminfo") as f:
                for line in f:
                    if "MemTotal" in line:
                        kb = int(line.split()[1])
                        return kb / (1024 ** 2)
    except Exception:
        pass
    return 4.0  # 保守估算


def _get_gpu_info() -> Tuple[bool, str]:
    """检测 GPU"""
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            return True, result.stdout.strip().split("\n")[0]
    except Exception:
        pass
    return False, ""


def _detect_agent_type() -> AgentType:
    """自动检测当前运行平台"""
    home = os.path.expanduser("~")

    # ── WorkBuddy 检测 ──
    workbuddy_paths = [
        os.path.join(home, ".workbuddy"),
        os.path.join(home, "AppData", "Roaming", "WorkBuddy"),
    ]
    for p in workbuddy_paths:
        if os.path.exists(p):
            # 判断云端还是本地
            host_type = os.environ.get("WORKBUDDY_HOST_TYPE", "")
            if host_type == "cloud":
                return AgentType.WORKBUDDY_CLOUD
            # 本地特征: 有 NUC 路径、大内存等
            if _get_ram_gb() > 8:
                return AgentType.WORKBUDDY_LOCAL
            return AgentType.WORKBUDDY_CLOUD  # 默认云端

    # ── OpenClaw 检测 ──
    openclaw_pip = False
    openclaw_source = os.path.exists(os.path.join(home, "openclaw"))
    openclaw_docker = os.path.exists("/.dockerenv") and openclaw_source
    try:
        import importlib
        if importlib.util.find_spec("openclaw"):
            openclaw_pip = True
    except Exception:
        pass

    if openclaw_docker:
        return AgentType.OPENCLAW_DOCKER
    if openclaw_pip:
        return AgentType.OPENCLAW_PIP
    if openclaw_source:
        return AgentType.OPENCLAW_SOURCE

    # ── Hermes 检测 ──
    if os.environ.get("HERMES_HOME"):
        return AgentType.HERMES
    hermes_path = os.path.join(home, ".hermes")
    if os.path.exists(hermes_path):
        return AgentType.HERMES

    return AgentType.GENERIC


def _detect_asr_capability() -> ASRCapability:
    """检测可用的 ASR 引擎"""
    cap = ASRCapability()

    # faster-whisper (本地)
    try:
        import importlib
        if importlib.util.find_spec("faster_whisper"):
            cap.engines.append(ASREngine.FASTER_WHISPER)
    except Exception:
        pass

    # 百炼ASR (DashScope)
    if os.environ.get("DASHSCOPE_API_KEY"):
        cap.engines.append(ASREngine.BAILIAN)

    # OpenAI Whisper
    if os.environ.get("OPENAI_API_KEY"):
        cap.engines.append(ASREngine.OPENAI_WHISPER)

    # GPU 加速
    cap.gpu_available, _ = _get_gpu_info()

    # 默认引擎选择
    if ASREngine.FASTER_WHISPER in cap.engines:
        cap.default_engine = ASREngine.FASTER_WHISPER
        cap.max_realtime_factor = 3.0 if cap.gpu_available else 1.0
    elif ASREngine.BAILIAN in cap.engines:
        cap.default_engine = ASREngine.BAILIAN
    else:
        cap.default_engine = ASREngine.FASTER_WHISPER  # 乐观假设已安装

    return cap


def _detect_llm_capability() -> LLMCapability:
    """检测可用的 LLM 后端"""
    cap = LLMCapability()

    # DeepSeek
    if os.environ.get("DEEPSEEK_API_KEY"):
        cap.backends.append(LLMBackend.DEEPSEEK)

    # OpenAI 兼容
    if os.environ.get("OPENAI_API_KEY"):
        cap.backends.append(LLMBackend.OPENAI)

    # Ollama (本地)
    try:
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, timeout=3
        )
        if result.returncode == 0:
            cap.backends.append(LLMBackend.OLLAMA)
    except Exception:
        pass

    # vLLM (本地)
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:8000/health"],
            capture_output=True, text=True, timeout=3
        )
        if "ok" in result.stdout.lower():
            cap.backends.append(LLMBackend.VLLM)
    except Exception:
        pass

    # 默认后端
    if LLMBackend.OPENAI in cap.backends or LLMBackend.DEEPSEEK in cap.backends:
        cap.default_backend = LLMBackend.DEEPSEEK if LLMBackend.DEEPSEEK in cap.backends else LLMBackend.OPENAI
        cap.is_paid = True
    elif LLMBackend.OLLAMA in cap.backends:
        cap.default_backend = LLMBackend.OLLAMA
        cap.is_paid = False
    elif LLMBackend.VLLM in cap.backends:
        cap.default_backend = LLMBackend.VLLM
        cap.is_paid = False
    else:
        cap.default_backend = LLMBackend.DEEPSEEK  # 乐观假设有配置

    return cap


def _get_storage_path(agent_type: AgentType, home: str) -> str:
    """根据平台决定存储路径"""
    if agent_type in (AgentType.WORKBUDDY_CLOUD, AgentType.WORKBUDDY_LOCAL):
        return os.path.join(home, "openclaw", "workspace", "storage")
    if agent_type == AgentType.OPENCLAW_SOURCE:
        return os.path.join(home, "openclaw", "workspace", "storage")
    if agent_type == AgentType.OPENCLAW_DOCKER:
        return os.path.join(home, "openclaw", "workspace", "storage")
    if agent_type == AgentType.OPENCLAW_PIP:
        return os.path.join(home, "openclaw", "workspace", "storage")
    if agent_type == AgentType.HERMES:
        return os.path.join(home, ".hermes", "storage")
    # Generic
    return os.path.join(home, ".biliyoutik2brain", "storage")


# ═══════════════════════════════════════════════════════════════
#  公共 API
# ═══════════════════════════════════════════════════════════════

def detect() -> EnvProfile:
    """检测当前环境，返回画像（幂等，首次调用后缓存）"""
    global _cached_profile
    if _cached_profile:
        return _cached_profile

    home = os.path.expanduser("~")
    cpu = _get_cpu_cores()
    ram = _get_ram_gb()
    gpu, gpu_name = _get_gpu_info()
    agent = _detect_agent_type()
    asr = _detect_asr_capability()
    llm = _detect_llm_capability()
    storage = _get_storage_path(agent, home)

    profile = EnvProfile(
        agent_type=agent,
        cpu_cores=cpu,
        ram_gb=round(ram, 1),
        gpu_available=gpu,
        gpu_name=gpu_name,
        os_type=platform.system().lower(),
        home_dir=home,
        storage_path=storage,
        asr=asr,
        llm=llm,
        profile_summary=(
            f"[{agent.value}] CPU:{cpu}C RAM:{ram:.1f}GB "
            f"GPU:{'Yes' if gpu else 'No'} "
            f"ASR:{asr.default_engine.value} "
            f"LLM:{llm.default_backend.value}"
        ),
    )

    _cached_profile = profile
    return profile


def get_cached() -> Optional[EnvProfile]:
    """获取缓存的画像（不重新检测）"""
    return _cached_profile


def print_profile():
    """打印环境画像（诊断用）"""
    p = detect()
    print("=" * 60)
    print("  BiliYouTik2Brain 环境画像")
    print("=" * 60)
    print(f"  平台       : {p.agent_type.value}")
    print(f"  OS         : {p.os_type}")
    print(f"  CPU        : {p.cpu_cores} 核")
    print(f"  内存       : {p.ram_gb:.1f} GB")
    print(f"  GPU        : {'Yes - ' + p.gpu_name if p.gpu_available else 'No'}")
    print(f"  存储       : {p.storage_path}")
    print(f"  ASR 引擎   : {', '.join(e.value for e in p.asr.engines)}")
    print(f"  默认 ASR   : {p.asr.default_engine.value}")
    print(f"  LLM 后端   : {', '.join(b.value for b in p.llm.backends)}")
    print(f"  默认 LLM   : {p.llm.default_backend.value} ({'付费' if p.llm.is_paid else '免费'})")
    print(f"  总结       : {p.profile_summary}")
    print("=" * 60)


# ═══════════════════════════════════════════════════════════════
#  EnvironmentContext — 全局环境上下文（移植自 environment.py）
#  贯穿 L1-L6 所有环节的动态运行参数
# ═══════════════════════════════════════════════════════════════

@dataclass
class EnvironmentContext:
    """贯穿 L1-L6 所有环节的全局环境上下文"""

    # ── 静态环境 ──
    os_name: str = ""
    os_version: str = ""
    python_version: str = ""
    cpu_cores: int = 1
    total_ram_gb: float = 0.0

    ffmpeg_available: bool = False
    ffmpeg_path: str = ""
    yt_dlp_available: bool = False
    yt_dlp_version: str = ""
    opencc_available: bool = False
    tesseract_available: bool = False
    has_gpu: bool = False

    # ── 动态环境 ──
    cpu_usage_percent: float = 0.0
    ram_available_gb: float = 0.0
    disk_free_gb: float = 0.0
    network_bandwidth_mbps: float = 0.0
    network_latency_ms: float = 0.0

    # ── 代理状态 ──
    proxy_available: bool = False
    proxy_name: str = ""        # "direct" / "clash-verge" / "mihomo" / "v2ray"
    proxy_port: int = 0

    # ── LLM API 状态 ──
    llm_available: bool = False
    llm_model: str = ""
    llm_latency_ms: float = 0.0

    # ── 时间戳 ──
    detected_at: str = ""

    # ── 动态参数（基于环境自动计算） ──
    max_download_concurrency: int = 2
    max_light_concurrency: int = 4
    whisper_model: str = "base"
    enable_ocr: bool = True
    enable_bleep: bool = True
    download_timeout_s: int = 120
    retry_count: int = 3
    ocr_frame_count: int = 20
    degrade_ocr_frames: bool = False

    # ── 元信息 ──
    warnings: list = field(default_factory=list)
    errors: list = field(default_factory=list)

    def is_healthy(self) -> bool:
        """环境是否满足最低运行要求"""
        return len(self.errors) == 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def summary(self) -> str:
        """人类可读的环境摘要"""
        lines = [
            f"OS: {self.os_name} {self.os_version}",
            f"Python: {self.python_version}",
            f"CPU: {self.cpu_cores}核 (负载 {self.cpu_usage_percent:.0f}%)",
            f"RAM: {self.ram_available_gb:.1f}/{self.total_ram_gb:.1f}GB 可用",
            f"磁盘: {self.disk_free_gb:.1f}GB 可用",
            f"FFmpeg: {'Yes' if self.ffmpeg_available else 'No'} {self.ffmpeg_path[:40] if self.ffmpeg_path else ''}",
            f"yt-dlp: {'Yes' if self.yt_dlp_available else 'No'} {self.yt_dlp_version}",
            f"opencc: {'Yes' if self.opencc_available else 'No'}",
            f"tesseract: {'Yes' if self.tesseract_available else 'No'}",
            f"模型: {self.whisper_model} | 下载并发: {self.max_download_concurrency} | 重试: {self.retry_count}次",
        ]
        if self.llm_model:
            if self.llm_latency_ms < 0:
                lines.append(f"LLM: X {self.llm_model} 不可用")
            elif self.llm_latency_ms > 3000:
                lines.append(f"LLM: ! {self.llm_model} {self.llm_latency_ms:.0f}ms (慢)")
            else:
                lines.append(f"LLM: OK {self.llm_model} {self.llm_latency_ms:.0f}ms")
        if self.proxy_available:
            lines.append(f"代理: OK {self.proxy_name or 'direct'}")
        else:
            lines.append(f"代理: X (YouTube 不可达)")
        if self.warnings:
            lines.append(f"! {len(self.warnings)}条告警")
        if self.errors:
            lines.append(f"X {len(self.errors)}条阻断错误")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
#  静态环境检测
# ═══════════════════════════════════════════════════════════════

def _detect_static() -> dict:
    """检测静态环境（OS、工具链版本），结果可缓存"""
    result = {
        "os_name": platform.system(),
        "os_version": platform.release(),
        "python_version": platform.python_version(),
        "cpu_cores": os.cpu_count() or 1,
    }

    # 总内存
    try:
        if sys.platform == "win32":
            result2 = subprocess.run(
                ["wmic", "ComputerSystem", "get", "TotalPhysicalMemory"],
                capture_output=True, text=True, timeout=10
            )
            for line in result2.stdout.splitlines():
                val = line.strip()
                if val.isdigit():
                    result["total_ram_gb"] = int(val) / (1024 ** 3)
                    break
            else:
                result["total_ram_gb"] = 4.0
        else:
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        result["total_ram_gb"] = int(line.split()[1]) / 1024 / 1024
                        break
    except Exception:
        result["total_ram_gb"] = 4.0

    # ffmpeg
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        result["ffmpeg_available"] = True
        result["ffmpeg_path"] = ffmpeg_path
    else:
        result["ffmpeg_available"] = False
        result["ffmpeg_path"] = ""

    # yt-dlp
    ytdlp_path = shutil.which("yt-dlp")
    if ytdlp_path:
        result["yt_dlp_available"] = True
        try:
            out = subprocess.run([ytdlp_path, "--version"], capture_output=True, text=True, timeout=5)
            result["yt_dlp_version"] = out.stdout.strip()[:32]
        except Exception:
            result["yt_dlp_version"] = "unknown"
    else:
        result["yt_dlp_available"] = False
        result["yt_dlp_version"] = ""

    # opencc
    result["opencc_available"] = shutil.which("opencc") is not None

    # OCR（PaddleOCR）
    try:
        import importlib
        if importlib.util.find_spec("paddleocr"):
            result["tesseract_available"] = True
    except Exception:
        result["tesseract_available"] = False

    # GPU
    result["has_gpu"], _ = _get_gpu_info()

    return result


# ═══════════════════════════════════════════════════════════════
#  动态环境检测
# ═══════════════════════════════════════════════════════════════

def _detect_dynamic() -> dict:
    """检测动态环境（CPU、内存、磁盘），每次任务重新采样"""
    result = {}

    # CPU 使用率
    try:
        import psutil
        result["cpu_usage_percent"] = psutil.cpu_percent(interval=0.5)
    except ImportError:
        try:
            if sys.platform != "win32":
                with open("/proc/stat") as f:
                    cpu_line = f.readline()
                parts = cpu_line.split()
                if len(parts) >= 5:
                    idle = int(parts[4])
                    total = sum(int(x) for x in parts[1:])
                    result["cpu_usage_percent"] = 100.0 - (idle / max(total, 1) * 100)
                else:
                    result["cpu_usage_percent"] = 50.0
            else:
                result["cpu_usage_percent"] = 50.0
        except Exception:
            result["cpu_usage_percent"] = 50.0

    # 可用内存
    try:
        if sys.platform == "win32":
            import psutil
            result["ram_available_gb"] = psutil.virtual_memory().available / (1024 ** 3)
        else:
            with open("/proc/meminfo") as f:
                meminfo = f.read()
            for line in meminfo.split("\n"):
                if line.startswith("MemAvailable:"):
                    result["ram_available_gb"] = int(line.split()[1]) / 1024 / 1024
                    break
            else:
                free = cached = 0
                for line in meminfo.split("\n"):
                    if line.startswith("MemFree:"):
                        free = int(line.split()[1])
                    elif line.startswith("Cached:"):
                        cached = int(line.split()[1])
                result["ram_available_gb"] = (free + cached) / 1024 / 1024
    except Exception:
        result["ram_available_gb"] = result.get("total_ram_gb", 4.0) * 0.5

    # 磁盘空间
    try:
        workspace = os.path.expanduser("~/.biliyoutik2brain")
        target = workspace if os.path.exists(workspace) else os.path.expanduser("~")
        if sys.platform == "win32":
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(target), None, None, ctypes.pointer(free_bytes)
            )
            result["disk_free_gb"] = free_bytes.value / (1024 ** 3)
        else:
            stat = os.statvfs(target)
            result["disk_free_gb"] = (stat.f_frsize * stat.f_bavail) / (1024 ** 3)
    except Exception:
        result["disk_free_gb"] = 10.0

    # 网络延迟
    result["network_latency_ms"] = _ping_latency()
    result["network_bandwidth_mbps"] = 0.0

    # 代理连通性
    pa, pn, pp = _check_proxy()
    result["proxy_available"] = pa
    result["proxy_name"] = pn
    result["proxy_port"] = pp

    # LLM API 速度测试
    llm = _llm_speed_test()
    result["llm_available"] = llm["llm_available"]
    result["llm_latency_ms"] = llm["llm_latency_ms"]
    result["llm_model"] = llm["llm_model"]

    return result


# ═══════════════════════════════════════════════════════════════
#  代理检测 — 结果导向：只关心 YouTube 能不能通
# ═══════════════════════════════════════════════════════════════

# 已知代理工具及其常见端口（按探测顺序）
_KNOWN_PROXIES = {
    "clash-verge": {"ports": [7890, 7897], "win32": "clash-verge.exe", "unix": "clash-verge"},
    "mihomo":      {"ports": [9981, 7890],      "win32": "mihomo.exe",      "unix": "mihomo"},
    "v2ray":       {"ports": [10809, 1080],      "win32": "v2ray.exe",       "unix": "v2ray"},
    "clash":       {"ports": [7890],              "win32": "clash.exe",       "unix": "clash"},
}


def _test_youtube() -> bool:
    """直接测试 YouTube 连通性（不走代理）"""
    import urllib.request
    from .anti_crawl_middleware import _create_insecure_ssl_context
    ctx = _create_insecure_ssl_context()
    try:
        req = urllib.request.Request("https://www.youtube.com", method="HEAD")
        resp = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=ctx)
        ).open(req, timeout=5)
        return resp.status in (200, 301, 302, 307, 308)
    except Exception:
        return False


def _probe_port(port: int) -> bool:
    """测某个端口是否提供 HTTP 代理（通过代理访问 YouTube）"""
    import urllib.request
    from .anti_crawl_middleware import _create_insecure_ssl_context
    proxy_url = f"http://127.0.0.1:{port}"
    ctx = _create_insecure_ssl_context()
    try:
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({"http": proxy_url, "https": proxy_url}),
            urllib.request.HTTPSHandler(context=ctx)
        )
        req = urllib.request.Request("https://www.youtube.com", method="HEAD")
        resp = opener.open(req, timeout=3)
        return resp.status in (200, 301, 302, 307, 308)
    except Exception:
        return False


def _find_proxy() -> tuple:
    """扫描代理工具 → 端口 → 探活。

    Returns:
        (available: bool, proxy_name: str, port: int)
    """
    for name, cfg in _KNOWN_PROXIES.items():
        # 先扫端口（最快）
        for port in cfg["ports"]:
            if _probe_port(port):
                return True, name, port
        # 端口不通，查进程是否存在（可能代理刚启动还没就绪）
        proc_name = cfg["win32"] if sys.platform == "win32" else cfg["unix"]
        alive = False
        try:
            if sys.platform == "win32":
                out = subprocess.run(
                    ["tasklist", "/FI", f"IMAGENAME eq {proc_name}"],
                    capture_output=True, text=True, timeout=3
                )
                alive = proc_name.lower() in out.stdout.lower()
            else:
                out = subprocess.run(
                    ["pgrep", "-f", proc_name], capture_output=True, text=True, timeout=2
                )
                alive = bool(out.stdout.strip())
        except Exception:
            pass
        if alive:
            time.sleep(2)
            for port in cfg["ports"]:
                if _probe_port(port):
                    return True, name, port
    return False, "", 0


def _check_proxy(auto_heal: bool = True) -> tuple:
    """代理检测 — 结果导向，不管工具只管通路。

    策略：
    1. YouTube 直连 → 说明网络本身没问题，不管代理
    2. YouTube 不通 → 扫描已知代理端口找出可用的
    3. 都没有 → 尝试拉起 mihomo/Clash（如果脚本存在）
    4. 还不行 → 报告不可用

    Returns:
        (available: bool, proxy_name: str, port: int)
    """
    # 1. 直连能通 → 万事大吉
    if _test_youtube():
        return True, "direct", 0

    # 2. 扫描已知代理
    ok, name, port = _find_proxy()
    if ok:
        return True, name, port

    # 3. 都没有 → 警告（不阻塞）
    return False, "", 0


# ═══════════════════════════════════════════════════════════════
#  网络延迟检测
# ═══════════════════════════════════════════════════════════════

def _ping_latency() -> float:
    """快速检测网络延迟（百度 DNS，超时2秒）"""
    try:
        if sys.platform == "win32":
            out = subprocess.run(
                ["ping", "-n", "1", "-w", "2000", "180.101.50.242"],
                capture_output=True, text=True, timeout=3
            )
            for line in out.stdout.split("\n"):
                if "time=" in line.lower() or "time<" in line.lower():
                    import re
                    m = re.search(r"time[=<]\s*(\d+)", line, re.IGNORECASE)
                    if m:
                        return float(m.group(1))
        else:
            out = subprocess.run(
                ["ping", "-c", "1", "-W", "2", "180.101.50.242"],
                capture_output=True, text=True, timeout=3
            )
            for line in out.stdout.split("\n"):
                if "time=" in line:
                    parts = line.split("time=")
                    if len(parts) > 1:
                        ms_str = parts[1].split()[0]
                        return float(ms_str)
    except Exception:
        pass
    return 500.0


# ═══════════════════════════════════════════════════════════════
#  LLM API 速度探测
# ═══════════════════════════════════════════════════════════════

def _llm_speed_test() -> dict:
    """轻量级 LLM 速度探测（一次极简请求测延迟）"""
    try:
        from .secrets import get_llm_config
    except ImportError:
        return {"llm_available": False, "llm_latency_ms": -1, "llm_model": ""}

    key, base, model = get_llm_config()
    if not (key and base and model):
        return {"llm_available": False, "llm_latency_ms": 0, "llm_model": ""}

    start = time.time()
    try:
        import requests
        resp = requests.post(
            f"{base}/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": "1+1="}],
                "max_tokens": 5
            },
            timeout=10
        )
        elapsed_ms = (time.time() - start) * 1000
        return {
            "llm_available": resp.status_code == 200,
            "llm_latency_ms": elapsed_ms if resp.status_code == 200 else -1,
            "llm_model": model,
        }
    except Exception:
        return {"llm_available": False, "llm_latency_ms": -1, "llm_model": model}


# ═══════════════════════════════════════════════════════════════
#  自动计算最优运行参数
# ═══════════════════════════════════════════════════════════════

def _compute_params(static: dict, dynamic: dict) -> dict:
    """基于静态+动态环境，自动计算最优运行参数"""
    cpu = dynamic.get("cpu_usage_percent", 50)
    ram = dynamic.get("ram_available_gb", 4)
    lat = dynamic.get("network_latency_ms", 200)
    cores = static.get("cpu_cores", 2)

    params = {}

    # 下载并发数
    if lat > 500:
        params["max_download_concurrency"] = 1
    elif lat > 200:
        params["max_download_concurrency"] = max(1, min(2, cores // 2))
    else:
        params["max_download_concurrency"] = max(2, min(4, cores))

    # 轻活并发
    params["max_light_concurrency"] = max(2, params["max_download_concurrency"] * 2)

    # Whisper 模型
    if ram < 2:
        params["whisper_model"] = "tiny"
    elif ram < 4 or cpu > 80:
        params["whisper_model"] = "base"
    else:
        params["whisper_model"] = "base"

    # OCR
    if cpu > 80 or ram < 2 or not static.get("tesseract_available", False):
        params["enable_ocr"] = False
    else:
        params["enable_ocr"] = True

    # BLEEP
    params["enable_bleep"] = cpu < 85

    # 超时
    if lat > 500:
        params["download_timeout_s"] = 300
        params["retry_count"] = 5
    elif lat > 200:
        params["download_timeout_s"] = 180
        params["retry_count"] = 4
    else:
        params["download_timeout_s"] = 120
        params["retry_count"] = 3

    # OCR 抽帧
    if ram < 4 or cpu > 60:
        params["ocr_frame_count"] = 10
        params["degrade_ocr_frames"] = True
    else:
        params["ocr_frame_count"] = 20
        params["degrade_ocr_frames"] = False

    return params


# ═══════════════════════════════════════════════════════════════
#  缓存
# ═══════════════════════════════════════════════════════════════

_cache_static: Optional[dict] = None
_cache_static_ts: float = 0.0
STATIC_CACHE_TTL = 3600  # 静态环境缓存1小时


# ═══════════════════════════════════════════════════════════════
#  get_environment_context — 供 downstream 模块获取细粒度环境信息
# ═══════════════════════════════════════════════════════════════

def get_environment_context(force: bool = False) -> EnvironmentContext:
    """检测环境，返回 EnvironmentContext（面向 L1-L6 的动态运行参数）

    Args:
        force: 强制刷新，忽略静态缓存
    """
    global _cache_static, _cache_static_ts

    now = time.time()

    # 静态环境（缓存1小时）
    if _cache_static is None or force or (now - _cache_static_ts > STATIC_CACHE_TTL):
        _cache_static = _detect_static()
        _cache_static_ts = now

    # 动态环境（每次采样）
    dynamic = _detect_dynamic()

    # 合并计算参数
    params = _compute_params(_cache_static, dynamic)

    # 构建上下文
    ctx = EnvironmentContext(
        os_name=_cache_static.get("os_name", ""),
        os_version=_cache_static.get("os_version", ""),
        python_version=_cache_static.get("python_version", ""),
        cpu_cores=_cache_static.get("cpu_cores", 1),
        total_ram_gb=_cache_static.get("total_ram_gb", 0),
        ffmpeg_available=_cache_static.get("ffmpeg_available", False),
        ffmpeg_path=_cache_static.get("ffmpeg_path", ""),
        yt_dlp_available=_cache_static.get("yt_dlp_available", False),
        yt_dlp_version=_cache_static.get("yt_dlp_version", ""),
        opencc_available=_cache_static.get("opencc_available", False),
        tesseract_available=_cache_static.get("tesseract_available", False),
        has_gpu=_cache_static.get("has_gpu", False),
        cpu_usage_percent=dynamic.get("cpu_usage_percent", 50),
        ram_available_gb=dynamic.get("ram_available_gb", 2),
        disk_free_gb=dynamic.get("disk_free_gb", 5),
        network_bandwidth_mbps=dynamic.get("network_bandwidth_mbps", 0),
        network_latency_ms=dynamic.get("network_latency_ms", 200),
        proxy_available=dynamic.get("proxy_available", False),
        proxy_name=dynamic.get("proxy_name", ""),
        proxy_port=dynamic.get("proxy_port", 0),
        detected_at=time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(now)),
        max_download_concurrency=params.get("max_download_concurrency", 2),
        max_light_concurrency=params.get("max_light_concurrency", 4),
        whisper_model=params.get("whisper_model", "base"),
        enable_ocr=params.get("enable_ocr", True),
        enable_bleep=params.get("enable_bleep", True),
        download_timeout_s=params.get("download_timeout_s", 120),
        retry_count=params.get("retry_count", 3),
        ocr_frame_count=params.get("ocr_frame_count", 20),
        degrade_ocr_frames=params.get("degrade_ocr_frames", False),
        llm_available=dynamic.get("llm_available", False),
        llm_model=dynamic.get("llm_model", ""),
        llm_latency_ms=dynamic.get("llm_latency_ms", 0),
    )

    # 阻断性检查
    if not ctx.yt_dlp_available:
        ctx.errors.append("yt-dlp 未安装，无法下载视频")
    if not ctx.ffmpeg_available:
        ctx.warnings.append("ffmpeg 未安装，部分格式转换受限")
    if not ctx.opencc_available:
        ctx.warnings.append("opencc 未安装，繁体转简体将跳过")
    if not ctx.proxy_available:
        ctx.warnings.append(
            "YouTube 不可达，且未检测到可用代理（已扫描 clash-verge/mihomo/v2ray），外网下载可能失败"
        )
    if ctx.disk_free_gb < 1:
        ctx.errors.append(f"磁盘空间不足 ({ctx.disk_free_gb:.1f}GB)，至少需要 1GB")
    if ctx.ram_available_gb < 0.5:
        ctx.errors.append(f"可用内存不足 ({ctx.ram_available_gb:.1f}GB)，至少需要 0.5GB")
    if not ctx.llm_available:
        ctx.warnings.append(f"LLM {ctx.llm_model or '未知'} 不可用，enhance 阶段将跳过")
    elif ctx.llm_latency_ms > 5000:
        ctx.warnings.append(f"LLM {ctx.llm_model} 响应过慢 ({ctx.llm_latency_ms:.0f}ms)，enhance 可能超时")

    return ctx
