#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ct-advisor 常驻编排服务（L1, 2026-09-25）

目的：把 run_orchestrate 所需的全部重模块（adapters / refine_answer / handle_need_tool /
route_tool / orchestrate 等，冷导入合计约 24s）在进程启动期一次性预热，此后每个 /ask 请求
直接复用 sys.modules 缓存，使单次问答的本地开销从 ~24s 降到接近 0（仅首启与空闲超时重置时付费）。

安全边界：
  - 仅监听 127.0.0.1（回环），外部不可达，不接受任何代码执行或文件副作用。
  - 仅暴露 /health、/ask、/shutdown 三个端点；/ask 只接受 {payload, config} 并返回
    run_orchestrate 的**明文**结果（v1.3.20 起内部无编码包裹），与 entry.py 内联路径
    输出完全一致——HARD GATE 与输出契约不变。
  - 空闲超时自动退出（默认 600s），避免孤儿进程常驻。
"""
from __future__ import annotations
import json
import os
import sys
import time
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
for _p in (SCRIPT_DIR, SKILL_ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

PORT = int(os.environ.get("CT_ADVISOR_PORT", "18771"))
# 空闲窗口（2026-10-16）：原 600s 对「间隔十几分钟问一次」的真实用法偏短，
# 每次都要重新冷编译重模块（7-20s）。放宽到 3600s，仍保留自动退出的兜底。
IDLE_TIMEOUT = int(os.environ.get("CT_ADVISOR_IDLE", "3600"))

_last_request = [time.time()]
__version__ = "1.3.0"          # 技能版本，供 /version 探针
# 代码版本指纹（2026-10-16）：scripts/*.py + adapters/**/*.py 的 mtime 最大值。
# 此前只记录 orchestrate.py，导致「单独更新 serve.py / adapters」时 entry.py 的
# 版本探针不触发，旧服务静默继续跑旧代码（实测确认的盲区）。
CODE_FP = [0.0]
ORCH_MTIME = [0]                # 兼容旧客户端：orchestrate.py 的 mtime


def _warmup():
    """一次性预热重模块。个别失败不应阻断启动（首个 /ask 内会再次导入）。"""
    import importlib
    for mod in ("route", "route_tool", "adapters", "refine_answer",
                "handle_need_tool", "orchestrate"):
        try:
            importlib.import_module(mod)
        except Exception as e:  # noqa: BLE001
            sys.stderr.write(f"[serve] 预热 {mod} 失败: {e}\n")
    sys.stderr.write("[serve] 预热完成\n")
    # 采集代码版本指纹（2026-10-16）：覆盖 scripts/*.py + adapters/**/*.py，
    # 供 entry 的版本探针比较——任一相关 .py 被更新都会触发服务重启。
    try:
        import code_fingerprint as _cf
        CODE_FP[0] = _cf.collect()
    except Exception:
        CODE_FP[0] = 0.0
    # 兼容字段：旧版 entry.py 只认 orchestrate_mtime
    try:
        import orchestrate as _orch
        ORCH_MTIME[0] = os.path.getmtime(_orch.__file__)
    except Exception:
        ORCH_MTIME[0] = 0


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):
        pass

    def _send(self, code, body: bytes, ctype="text/plain; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        try:
            self.wfile.write(body)
        except Exception:
            pass

    def _touch(self):
        _last_request[0] = time.time()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            self._touch()
            self._send(200, b"ok")
        elif path == "/shutdown":
            self._send(200, b"shutting down")
            threading.Thread(target=lambda: (time.sleep(0.1), os._exit(0)),
                             daemon=True).start()
        elif path == "/version":
            self._touch()
            body = json.dumps({
                "version": __version__,
                "code_fingerprint": CODE_FP[0],
                "orchestrate_mtime": ORCH_MTIME[0],
                "port": PORT,
            }).encode("utf-8")
            self._send(200, body, "application/json")
        else:
            self._send(404, b"not found")

    def do_POST(self):
        path = urlparse(self.path).path
        self._touch()
        if path != "/ask":
            self._send(404, b"not found")
            return
        try:
            length = int(self.headers.get("Content-Length", "0") or "0")
            raw = self.rfile.read(length) if length else b""
            data = json.loads(raw.decode("utf-8"))
            payload = data["payload"]
            config = data.get("config", os.path.join(SKILL_ROOT, "config.json"))
        except Exception as e:  # noqa: BLE001
            self._send(400, f"bad request: {e}".encode("utf-8"))
            return
        try:
            from orchestrate import run_orchestrate
            out = run_orchestrate(payload, config)
            self._send(200, out.encode("utf-8"))
        except Exception as e:  # noqa: BLE001
            # 2026-10-16 修复（重复调用风险）：此前返回 HTTP 500，而客户端
            # （adapters/local_service_client.server_ask）对 HTTPError 的处理是
            # 「回退内联再跑一次」——若异常发生在 Coze 调用之后，就会**真的再调
            # 一次 Coze**，正是本次优化的目标缺陷。改为在服务端就地渲染成合法答案
            # （明文；标记/checksum 由 entry 出口补），以 HTTP 200 返回，客户端不再
            # 回退，杜绝重复执行。
            out = ("⚠️ 技能编排过程出现内部错误，无法生成答案。\n\n"
                   f"{type(e).__name__}: {e}\n\n"
                   "请稍后重试；若持续出现，请把本条提示反馈给技能维护者。")
            self._send(200, out.encode("utf-8"))


class _QuietServer(ThreadingHTTPServer):
    """吞掉 keep-alive 连接被客户端正常关闭时的噪音 traceback（2026-10-16）。

    HTTP/1.1 keep-alive 下，客户端读完响应即关闭连接，服务端接着读下一行请求
    会拿到 ConnectionAbortedError(10053)；默认 handle_error 会把它连同整段
    traceback 打到 stderr。既然 stderr 现在落盘到 config/serve.log，这类纯噪音
    会污染日志可读性，故在此静默（真错误照常走 super()）。
    """

    def handle_error(self, request, client_address):
        exc = sys.exc_info()[1]
        if isinstance(exc, (ConnectionAbortedError, ConnectionResetError,
                            BrokenPipeError, TimeoutError)):
            return
        super().handle_error(request, client_address)


def _idle_watchdog():
    while True:
        time.sleep(15)
        if time.time() - _last_request[0] > IDLE_TIMEOUT:
            sys.stderr.write("[serve] 空闲超时，退出\n")
            os._exit(0)


def _redirect_stderr_to_log() -> None:
    """把服务端 stderr 落盘到 config/serve.log（2026-10-16）。

    start_server() 以 stderr=DEVNULL 拉起本服务，服务进程内的全部诊断
    （预热耗时 / answer-cache hit / [ct-advisor][ERR] 错误信号）都会丢失。
    这里自行重定向到日志文件，保证信号可追溯；超过 1 MB 时截断。
    """
    try:
        from pathlib import Path as _P
        log_dir = _P(SKILL_ROOT) / "config"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / "serve.log"
        try:
            if log_path.exists() and log_path.stat().st_size > 1024 * 1024:
                log_path.write_text("", encoding="utf-8")
        except Exception:
            pass
        fh = open(log_path, "a", encoding="utf-8", buffering=1)
        os.dup2(fh.fileno(), 2)
        sys.stderr = fh
    except Exception:
        pass


def main():
    _redirect_stderr_to_log()
    _warmup()
    try:
        server = _QuietServer(("127.0.0.1", PORT), Handler)
    except OSError as e:
        sys.stderr.write(f"[serve] 端口 {PORT} 绑定失败（可能被旧服务占用）: {e}\n")
        sys.exit(1)
    sys.stderr.write(f"[serve] 监听 127.0.0.1:{PORT}\n")
    threading.Thread(target=_idle_watchdog, daemon=True).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
