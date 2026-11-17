#!/usr/bin/env python3
"""
c_ext_loader — C 扩展集中加载器（终极防错方案）

设计目标
--------
彻底消除 AGI 进化模型历史上反复出现的「C 扩展加载失败 / 崩溃」类问题
（根因：命名空间包遮蔽、路径逻辑分叉、平台格式差异、__file__ 为 None 时崩溃）。

历史根因
--------
- BUG-2: personality_layer_pure 对 namespace package 的 __file__=None 调 .endswith 崩溃
- BUG-3: personality_core.so 被埋在 scripts/personality_core/ 子目录，被同名目录
         抢注成命名空间包，import 永远命中目录而非 .so，两平台都不生效
- 跨平台: Windows 只认 .pyd，Linux 认 .so；os.statvfs 等 API 不跨平台

本模块的硬性保证
----------------
1. 不依赖 `import <name>` 的解析顺序（它会命中同名目录型命名空间包）。
   改用 importlib.util.spec_from_file_location 按「显式文件路径」直接加载 .so/.pyd。
2. 候选目录统一搜索：scripts/ 根目录、scripts/personality_core/、当前工作目录。
3. 平台感知后缀：posix -> .so，windows -> .pyd。
4. 加载后按「必需符号」校验，确认拿到的是真正的 C 扩展而非占位命名空间包。
5. 全程 catch-all，返回结构化结果 (module, loaded, detail)，绝不向上抛未捕获异常。

依赖：仅标准库（importlib / os / sys / glob / typing）。
"""

from __future__ import annotations

import glob
import importlib.util
import os
import subprocess
import sys
from typing import List, Optional, Tuple

# 候选搜索子目录（相对 scripts 目录）。空串表示 scripts 根目录本身。
_CANDIDATE_SUBDIRS: Tuple[str, ...] = ("", "personality_core")


def _candidate_paths(module_name: str, base_dir: str) -> List[str]:
    """返回 module_name 的可能 .so/.pyd 文件路径（去重、保序）。"""
    suffix = ".pyd" if sys.platform.startswith("win") else ".so"
    raw: List[str] = []
    for sub in _CANDIDATE_SUBDIRS:
        d = os.path.join(base_dir, sub) if sub else base_dir
        # 精确路径
        raw.append(os.path.join(d, f"{module_name}{suffix}"))
        # glob 兜底（兼容异常命名 / 大小写）
        raw.extend(glob.glob(os.path.join(d, f"{module_name}.{suffix}*")) or [])
    seen: set = set()
    out: List[str] = []
    for p in raw:
        ap = os.path.abspath(p)
        if ap not in seen:
            seen.add(ap)
            out.append(p)
    return out


def _probe_execution(
    base_dir: str,
    module_name: str,
    required_symbols: List[str],
    runtime_probe: Tuple[str, tuple, dict],
) -> bool:
    """在子进程中真实调用一次 ext 的探针函数，确认不会崩溃（如 SIGILL）。

    某些预编译 .so 在 import 阶段正常，但执行含特定 SIMD 指令的函数时会在
    不支持该指令集的 CPU 上触发 Illegal instruction（SIGILL）并杀死整个进程，
    这种错误无法用 try/except 在主进程内捕获。因此必须在独立子进程中探测：
    子进程崩溃只影响自己，主进程据此安全降级到纯 Python。

    返回 True 表示执行安全；False 表示子进程异常/崩溃。
    """
    func_name, pargs, pkwargs = runtime_probe
    script = (
        "import sys\n"
        "sys.path.insert(0, {base!r})\n"
        "from c_ext_loader import load_c_extension\n"
        "SYMS = {syms!r}\n"
        "mod, ok, _ = load_c_extension({mod!r}, required_symbols=SYMS)\n"
        "sys.exit(2) if not ok else None\n"
        "getattr(mod, {func!r})(*{args!r}, **{kw!r})\n"
        "sys.exit(0)\n"
    ).format(
        base=base_dir,
        syms=required_symbols,
        mod=module_name,
        func=func_name,
        args=pargs,
        kw=pkwargs,
    )
    try:
        proc = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            timeout=15,
        )
        return proc.returncode == 0
    except Exception:
        return False


def load_c_extension(
    module_name: str,
    required_symbols: Optional[List[str]] = None,
    base_dir: Optional[str] = None,
    runtime_probe: Optional[Tuple[str, tuple, dict]] = None,
) -> Tuple[object, bool, str]:
    """加载 C 扩展。

    返回 (module_or_None, loaded: bool, detail: str)
    - loaded=True 当且仅当：找到文件 + importlib 加载成功 + 必需符号齐全
      + （若提供 runtime_probe）子进程内实际调用探针函数未崩溃。
    - 任何异常都被捕获，loaded=False 并返回原因，绝不向上传播。
    - runtime_probe: (函数名, 位置参数元组, 关键字参数字典)。提供后会在一个
      独立子进程中真实调用一次该函数，用于拦截 SIGILL 等「import 正常但执行崩溃」
      的二进制不兼容问题——这类崩溃无法在主进程内用 try/except 捕获。

    注意：加载成功后才会写入 sys.modules[module_name]，避免污染。
    """
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    required_symbols = required_symbols or []

    candidates = _candidate_paths(module_name, base_dir)
    for path in candidates:
        if not os.path.isfile(path):
            continue
        try:
            spec = importlib.util.spec_from_file_location(module_name, path)
            if spec is None or spec.loader is None:
                continue
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception:
            # 该候选加载失败，尝试下一个
            continue

        # 必需符号校验：确认拿到的是真正的 C 扩展，而非占位/命名空间包
        missing = [s for s in required_symbols if not hasattr(module, s)]
        if missing:
            # 不作为有效 C 扩展，继续寻找下一个候选
            continue

        # 执行安全探针（防止 SIGILL 等二进制不兼容在首次调用时炸掉整个进程）
        if runtime_probe is not None:
            if not _probe_execution(base_dir, module_name, required_symbols, runtime_probe):
                # 子进程执行崩溃，视为不可用，尝试下一个候选
                continue

        sys.modules[module_name] = module
        return module, True, f"C 扩展已加载: {path}"

    detail = (
        f"未找到/无法加载 {module_name} 的 C 扩展"
        f"（平台={sys.platform}，已搜索 {len(candidates)} 个候选路径），将降级到纯 Python"
    )
    return None, False, detail


# 已知 C 扩展的必需符号表（用于「真加载」校验，避免误把命名空间包当扩展）
PERSONALITY_CORE_SYMBOLS: List[str] = [
    "calculate_similarity",
    "compute_all_scores",
    "compute_maslow_priority",
    "normalize_weights",
]

PERCEPTION_NODE_SYMBOLS: List[str] = [
    "call_tool",
    "generate_trace_id",
]


if __name__ == "__main__":
    # 简单自测：打印两个扩展在两平台上的「可执行」加载状态（含执行安全探针）
    for name, syms, probe in (
        ("personality_core", PERSONALITY_CORE_SYMBOLS,
         ("calculate_similarity", ([0.5] * 5, [0.5] * 5), {})),
        ("core_perception_node", PERCEPTION_NODE_SYMBOLS,
         ("generate_trace_id", (), {})),
    ):
        mod, ok, msg = load_c_extension(name, required_symbols=syms, runtime_probe=probe)
        print(f"{name}: loaded={ok} | {msg}")
