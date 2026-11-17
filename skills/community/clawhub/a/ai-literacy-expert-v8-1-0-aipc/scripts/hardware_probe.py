"""
hardware_probe.py - V7-AIPC 鑷姩纭欢鎺祴锛歂PU/iGPU/CPU 鏅鸿兘璋冨害 + 涓?work_summary 鑱斿姩

璁捐鐩爣锛?
  - 鍦?init_text_pipeline 鍓嶅厛鎺祴 NPU / iGPU / CPU 鍙敤鎬?
  - 鏍规嵁 npu-scheduling-guide 搂1.2 浠诲姟鍒嗛厤鐭樀杩斿洖鏈浼樿澶?
  - 閬垮厤纭紪鐮?--device CLI 鍙傛暟锛堢敤鎴锋棤闇鍏冲績纭欢锛?

璋冨害绛栫暐锛堟潵婧?npu-scheduling-guide.md 搂1.2锛夛細
  LLM 鏂囨湰鎺悊锛?.5B DeepSeek-R1锛夛細CPU + iGPU 寮傛瀯锛堥閫?GPU锛?
  绔簯鍗忓悓 NPU 浠诲姟锛歂PU 浼樺厛锛圤CR/ASR/TTS锛?

杩斿洖鍊硷細
  ProbeResult(device: str, npu: bool, igpu: bool, cpu: bool, source: str)
  - device: 鎺崘璁惧锛圢PU | GPU | CPU锛?
  - npu/igpu/cpu: 鍚勮澶囧彲鐢?
  - source: 鎺祴鏉簮锛坥penvino | static | default锛?
"""
from __future__ import annotations
__version__ = "8.1.0-aipc"  # V8.1-AIPC: 每次工作自动输出本地/云端对比 + 全互动控件完整性门控

import os
import sys
from dataclasses import dataclass
from typing import Optional

# 寮哄埗 UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from log_util import get_logger

log = get_logger("hardware_probe")


@dataclass
class ProbeResult:
    """硬件探测结果."""
    device: str       # 鎺崘璁惧
    npu: bool
    igpu: bool
    cpu: bool
    source: str       # 鎺祴鏉簮
    error: Optional[str] = None  # 鎺祴澶辫触鍘熷洜


def _probe_via_openvino() -> Optional[ProbeResult]:
    """通过 OpenVINO Core.available_devices 探测硬件."""
    try:
        import openvino as ov  # type: ignore
        core = ov.Core()
        available = set(core.available_devices)
        # NPU 鍦?OpenVINO 涓互 "NPU" 鏍囪瘑
        npu_ok = any("NPU" in d.upper() for d in available)
        # iGPU 鍦?OpenVINO 涓互 "GPU" 鎴?"GPU.X" 鏍囪瘑
        igpu_ok = any(d.upper().startswith("GPU") for d in available)
        cpu_ok = "CPU" in available

        # 鎸?npu-scheduling-guide 搂1.2 閫夋嫨鏈浼樿澶?
        if npu_ok and igpu_ok:
            device = "GPU"  # 1.5B 鎺悊锛欳PU+iGPU 寮傛瀯浼樺厛
        elif igpu_ok:
            device = "GPU"
        elif npu_ok:
            device = "NPU"  # 绾?NPU 澶囬?
        else:
            device = "CPU"  # 鍏滃簳

        log.info(f"[probe] OpenVINO 鎺祴: available={available} -> device={device}")
        return ProbeResult(
            device=device, npu=npu_ok, igpu=igpu_ok, cpu=cpu_ok,
            source="openvino",
        )
    except ImportError as e:
        log.warn(f"[probe] openvino 鏈畨瑁? {e}")
        return None
    except Exception as e:
        log.warn(f"[probe] OpenVINO 鎺祴澶辫触: {e}")
        return None


def _probe_via_subprocess() -> Optional[ProbeResult]:
    """閫氳繃瀛愯繘绋?check_platform.ps1 鎺祴纭欢锛圵indows锛夈?"""
    import subprocess
    import platform
    if platform.system() != "Windows":
        return None
    try:
        # 璋冪敤 check_platform.ps1 鑾峰彇纭欢淇伅
        ps_script = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "scripts", "check_platform.ps1"
        )
        if not os.path.exists(ps_script):
            return None
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
             "-File", ps_script, "--probe-only"],
            capture_output=True, text=True, timeout=15,
        )
        output = (result.stdout or "").lower()
        npu_ok = "npu" in output and ("available" in output or "ok" in output)
        igpu_ok = ("igpu" in output or "xe-lpg" in output or "arc" in output)
        cpu_ok = True  # CPU 姘歌繙鍙敤
        if not (npu_ok or igpu_ok):
            return None
        if igpu_ok:
            device = "GPU"
        elif npu_ok:
            device = "NPU"
        else:
            device = "CPU"
        return ProbeResult(
            device=device, npu=npu_ok, igpu=igpu_ok, cpu=cpu_ok,
            source="powershell",
        )
    except Exception as e:
        log.warn(f"[probe] PowerShell 鎺祴澶辫触: {e}")
        return None


def _probe_static() -> ProbeResult:
    """闈欐佹帰娴嬶紙鍏滃簳锛夛細鏍规嵁鐜鍙橀噺鍒畾銆?"

    鐜鍙橀噺锛?
      AI_LITERACY_DEVICE: 鏄惧紡鎸囧畾璁惧
      AI_LITERACY_NO_NPU: 鏍囪 NPU 涓嶅彲鐢?
      AI_LITERACY_NO_IGPU: 鏍囪 iGPU 涓嶅彲鐢?
    """
    explicit = os.environ.get("AI_LITERACY_DEVICE", "").strip().upper()
    if explicit in ("NPU", "GPU", "CPU"):
        log.info(f"[probe] 闈欐佹帰娴嬶細AI_LITERACY_DEVICE={explicit}")
        return ProbeResult(
            device=explicit,
            npu=explicit == "NPU" and not os.environ.get("AI_LITERACY_NO_NPU"),
            igpu=explicit == "GPU" and not os.environ.get("AI_LITERACY_NO_IGPU"),
            cpu=True,
            source="static",
        )
    # 兜底: 默认 GPU (1.5B 文本推理首选 iGPU 异构)
    log.info("[probe] 静态探测: 默认 GPU (1.5B 文本推理推荐)")
    return ProbeResult(
        device="GPU",
        npu=not os.environ.get("AI_LITERACY_NO_NPU"),
        igpu=not os.environ.get("AI_LITERACY_NO_IGPU"),
        cpu=True,
        source="default",
    )


def probe_hardware() -> ProbeResult:
    """探测硬件并返回最优推荐设备.

    优先级:
      1. OpenVINO Core.available_devices(最准确)
      2. PowerShell check_platform.ps1 --probe-only(Windows 备选)
      3. 静态探测(环境变量 / 默认 GPU)
    """
    log.info("[probe] 开始硬件探测...")
    result = _probe_via_openvino()
    if result is not None:
        return result
    result = _probe_via_subprocess()
    if result is not None:
        return result
    return _probe_static()


def auto_select_device(prefer: str = "GPU") -> str:
    """自动选择最优设备 (probe + prefer 偏好).

    Args:
        prefer: 偏好设备 ("NPU" | "GPU" | "CPU"), 默认 "GPU"

    Returns:
        设备字符串 ("NPU" | "GPU" | "CPU").
    """
    result = probe_hardware()
    # prefer 浼樺厛锛堝 NPU 鍙敤涓?prefer=NPU 鍒欓?NPU锛?
    if prefer == "NPU" and result.npu:
        return "NPU"
    if prefer == "GPU" and result.igpu:
        return "GPU"
    if prefer == "CPU":
        return "CPU"
    # 鍚垯鐢?probe 鐨勬帹鑽?
    return result.device


if __name__ == "__main__":
    # CLI: python hardware_probe.py
    result = probe_hardware()
    print(f"device: {result.device}")
    print(f"NPU:    {'yes' if result.npu else 'no'}")
    print(f"iGPU:   {'yes' if result.igpu else 'no'}")
    print(f"CPU:    {'yes' if result.cpu else 'no'}")
    print(f"source: {result.source}")
    if result.error:
        print(f"error:  {result.error}")

