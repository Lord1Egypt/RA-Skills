"""BabelDOC / pdf2zh-next 子进程封装（AGPL 隔离 + 崩溃隔离双目的）。

铁律：绝不 import 引擎源码，只以子进程调用官方 CLI `pdf2zh_next`；
引擎以独立 pip 包安装（uv tool install pdf2zh-next），本仓库零 vendor。
"""

from __future__ import annotations

import glob
import os
import shutil
import subprocess
import time
from dataclasses import dataclass, field

DEFAULT_WATERMARK_MODE = "no_watermark"
MIN_TIMEOUT_S = 180
MAX_TIMEOUT_S = 600
PER_PAGE_BUDGET_S = 15


class EngineNotFoundError(FileNotFoundError):
    pass


@dataclass
class EngineResult:
    ok: bool
    returncode: object = None
    dual_path: str = None
    mono_path: str = None
    stderr_tail: str = ""
    duration_s: float = 0.0
    timed_out: bool = False
    command: list = field(default_factory=list)

    def to_dict(self, hide_key: bool = True) -> dict:
        cmd = list(self.command)
        if hide_key:
            cmd = ["<redacted>" if v == "--openai-api-key" else
                   ("<redacted-key>" if cmd[i - 1] == "--openai-api-key" else v)
                   for i, v in enumerate(cmd)]
        return {
            "ok": self.ok, "returncode": self.returncode,
            "dual_path": self.dual_path, "mono_path": self.mono_path,
            "stderr_tail": self.stderr_tail, "duration_s": round(self.duration_s, 1),
            "timed_out": self.timed_out, "command": cmd,
        }


def find_engine_bin(explicit: str = None) -> str:
    """pdf2zh_next 可执行文件发现：显式 > env > PATH > 开发树 .venv。"""
    candidates = [
        explicit,
        os.environ.get("DOC_HOLMES_PDF2ZH_BIN"),
        shutil.which("pdf2zh_next"),
        os.path.join(os.path.expanduser("~"), ".local", "bin", "pdf2zh_next"),
    ]
    repo_root = os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    for exe in (os.path.join(repo_root, ".venv", "bin", "pdf2zh_next"),
                os.path.join(repo_root, ".venv", "Scripts", "pdf2zh_next.exe")):
        candidates.append(exe)
    for cand in candidates:
        if cand and os.path.isfile(cand) and os.access(cand, os.X_OK):
            return cand
    raise EngineNotFoundError(
        "未找到 pdf2zh_next 引擎。安装方式任选其一：\n"
        "  uv tool install --python 3.12 pdf2zh-next\n"
        "  pip install pdf2zh-next\n"
        "或用环境变量 DOC_HOLMES_PDF2ZH_BIN 指定完整路径。")


def build_command(pdf: str, outdir: str, base_url: str, api_key: str, model: str,
                  *, lang_in: str = "en", lang_out: str = "zh",
                  pages: str = None, no_dual: bool = False, no_mono: bool = False,
                  qps: int = 4, watermark_mode: str = DEFAULT_WATERMARK_MODE,
                  openai_timeout: int = 180, engine_bin: str = None,
                  extra_args: list = None) -> list:
    cmd = [
        find_engine_bin(engine_bin), pdf,
        "--openai",
        "--openai-model", model,
        "--openai-base-url", base_url,
        "--openai-api-key", api_key,
        "--openai-timeout", str(openai_timeout),
        "--lang-in", lang_in,
        "--lang-out", lang_out,
        "--watermark-output-mode", watermark_mode,
        "--qps", str(qps),
        "--output", outdir,
    ]
    if pages:
        cmd += ["--pages", pages]
    if no_dual:
        cmd.append("--no-dual")
    if no_mono:
        cmd.append("--no-mono")
    if extra_args:
        cmd += list(extra_args)
    return cmd


OUTPUT_RE = None  # 惰性编译见 discover_outputs


def discover_outputs(outdir: str, pdf: str, not_before: float = 0.0):
    """pdf2zh_next 产物命名：<stem>.<mode>.<lang>.dual.pdf / .mono.pdf。

    精确 stem 边界匹配（report.pdf 不得命中 report_v2 的产物），
    not_before 限定本次运行的产物窗口（共享 outdir 时防误归属/误回滚）。
    """
    import re
    stem = os.path.splitext(os.path.basename(pdf))[0]
    pat = re.compile(re.escape(stem) + r"\..+\.(dual|mono)\.pdf$", re.I)
    dual = mono = None
    try:
        names = os.listdir(outdir)
    except OSError:
        return None, None
    for name in names:
        m = pat.match(name)
        if not m:
            continue
        full = os.path.join(outdir, name)
        if not os.path.isfile(full) or os.path.getmtime(full) < not_before:
            continue
        if m.group(1).lower() == "dual":
            if dual is None or os.path.getmtime(full) > os.path.getmtime(dual):
                dual = full
        else:
            if mono is None or os.path.getmtime(full) > os.path.getmtime(mono):
                mono = full
    return dual, mono


def classify_failure(timed_out: bool, returncode, stderr_tail: str) -> str:
    if timed_out:
        return "timeout"
    if returncode is None:
        return "spawn_error"
    if isinstance(returncode, int) and returncode < 0:
        return "killed_signal_%d" % (-returncode)
    tail = (stderr_tail or "").lower()
    if "out of memory" in tail or " oom" in tail or "outofmemory" in tail:
        return "likely_oom"
    if any(k in tail for k in ("api key", "unauthorized", "invalid api", "401",
                               "403", "quota", "rate limit", "authentication")):
        return "api_auth_or_quota"
    if returncode not in (0,):
        return "engine_error_rc%s" % returncode
    return ""


def translate_pdf(pdf: str, outdir: str, base_url: str, api_key: str, model: str,
                  *, page_count: int = None, timeout_s: int = None, **kw) -> EngineResult:
    """同步翻译单个 PDF；超时 kill 进程组（POSIX），连孙进程一起清，绝不挂死调用方。"""
    if timeout_s is None:
        pages = page_count or 10
        timeout_s = min(max(MIN_TIMEOUT_S, PER_PAGE_BUDGET_S * pages), MAX_TIMEOUT_S)
    os.makedirs(outdir, exist_ok=True)
    cmd = build_command(pdf, outdir, base_url, api_key, model, **kw)
    t0 = time.time()
    rc = None
    err_tail = ""
    timed_out = False
    window = t0 - 1  # 产物发现窗口：只认本次运行开始后的文件
    # POSIX 下以独立进程组启动：超时 killpg 连孙进程一起清（评审 P2，实测孤儿继续烧配额）
    popen_kwargs = {}
    if os.name == "posix":
        popen_kwargs["start_new_session"] = True
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, **popen_kwargs)
        try:
            out, err = proc.communicate(timeout=timeout_s)
            rc = proc.returncode
            err_tail = (err or "") + (out or "")
            err_tail = err_tail[-2000:]
        except subprocess.TimeoutExpired:
            timed_out = True
            if os.name == "posix":
                try:
                    os.killpg(os.getpgid(proc.pid), 9)
                except (ProcessLookupError, PermissionError):
                    proc.kill()
            else:
                proc.kill()
            try:
                out, err = proc.communicate(timeout=15)
            except Exception:
                out, err = "", ""
            err_tail = ((err or "") + (out or ""))[-2000:]
    except FileNotFoundError:
        raise
    except Exception as exc:
        rc = -1
        err_tail = "spawn/communicate error: %r" % (exc,)
        err_tail = ((exc.stderr or b"").decode("utf-8", "ignore")
                    if isinstance(exc.stderr, bytes) else (exc.stderr or ""))[-2000:]
    duration = time.time() - t0
    if api_key:
        err_tail = err_tail.replace(api_key, "<redacted-key>")
    dual, mono = discover_outputs(outdir, pdf, not_before=window)
    ok = (not timed_out) and rc == 0 and bool(dual or mono)
    if not ok and not timed_out:
        fail_class = classify_failure(False, rc, err_tail) or "no_output"
        err_tail = ("[%s] " % fail_class) + err_tail
    return EngineResult(ok=ok, returncode=rc, dual_path=dual, mono_path=mono,
                        stderr_tail=err_tail.strip(), duration_s=duration,
                        timed_out=timed_out, command=cmd)
