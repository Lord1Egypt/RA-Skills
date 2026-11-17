#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""飞书写前幂等护栏（2026-11-13，ct-literature）。

背景：飞书 searchlog 实测 30 天 650 行中 264 行（40.6%）是同一次逻辑调用
在 <2s（p50=385ms / p75=531ms / max=1933ms）内重复写入的第二行，日双写率
多日精确 50%。根因之一是 11-11 引入的 request_id 从未真正送达云端
（详见 references/coze_fix_spec_feishu_write_idempotency.md）。

本模块提供**客户端兜底**：在发出飞书写入前，按「业务载荷指纹 + 时间窗」做一次
原子 claim，窗口内重复载荷直接跳过，不依赖 Coze 端是否已实现幂等去重。

边界（必须明确）：
  · 仅同机同共享目录有效；多机 / 多端点 / 云端节点内部重复写无效，
    仍需 Coze 端按 (skillname, request_id) 幂等 upsert 根治；
  · fail-open：目录不可写 / 锁超时 / ledger 损坏 → 一律返回允许写，
    护栏永不阻断主业务链路；
  · 业务载荷指纹**必须排除 request_id**：两次重复 run 各自 uuid4，
    把 ID 算进指纹会让护栏形同虚设；
  · 排他锁 + 原子写：避免两个进程同时检查通过而双双放行。

可逆开关：
  CT_LIT_WRITE_GUARD=0            关闭护栏（恢复旧行为）
  CT_LIT_WRITE_GUARD_WINDOW=秒    调整去重时间窗（默认 5.0）
  CT_LIT_WRITE_GUARD_DIR=路径     自定义 ledger 目录
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
import threading
import time

_SCHEMA = "v1"
_DEFAULT_WINDOW = 5.0
_MAX_ENTRIES = 256
_LOCK_WAIT_MAX = 2.0
_LEDGER_NAME = "feishu_write_ledger.json"
_LOCK_NAME = "feishu_write_ledger.lock"

_local_lock = threading.Lock()


def _shared_dir() -> str:
    override = os.environ.get("CT_LIT_WRITE_GUARD_DIR", "").strip()
    if override:
        return os.path.abspath(os.path.expanduser(override))
    # 复用 search_cache 的用户级共享目录约定（单一真源，不另造一套路径规则）
    try:
        from adapters import search_cache
        return os.path.dirname(
            os.path.join(os.path.expanduser("~"), search_cache._SHARED_REL))
    except Exception:
        return os.path.join(os.path.expanduser("~"), ".cache", "ct-literature")


def disabled() -> bool:
    return os.environ.get("CT_LIT_WRITE_GUARD", "").strip().lower() in (
        "0", "false", "no", "off")


def _window() -> float:
    try:
        return max(0.0, float(
            os.environ.get("CT_LIT_WRITE_GUARD_WINDOW", "") or _DEFAULT_WINDOW))
    except (TypeError, ValueError):
        return _DEFAULT_WINDOW


def _fingerprint(skillname: str, payload: str) -> str:
    raw = "%s|%s|%s" % (_SCHEMA, skillname or "", payload or "")
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


def _acquire_lock(path: str):
    """排他锁文件（O_CREAT|O_EXCL）；超时返回 None，由调用方 fail-open。"""
    deadline = time.time() + _LOCK_WAIT_MAX
    while time.time() < deadline:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            try:
                os.write(fd, str(os.getpid()).encode("ascii"))
            finally:
                os.close(fd)
            return True
        except FileExistsError:
            # 陈旧锁（进程崩溃遗留）：超过 30s 强制清理，避免永久死锁
            try:
                if time.time() - os.path.getmtime(path) > 30:
                    os.unlink(path)
                    continue
            except OSError:
                pass
            time.sleep(0.02)
        except OSError:
            return None
    return None


def _atomic_write(path: str, data: dict) -> None:
    d = os.path.dirname(path)
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".ledger_", dir=d)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def claim(payload: str, skillname: str = "ct-literature",
          window_sec: float = None):
    """原子「检查 + 登记」一次写入意图。

    Args:
        payload: 业务载荷字符串（**调用方须先剔除 request_id 等每次运行都变的字段**）。
        skillname: 技能名，参与指纹，避免跨技能误抑制。
        window_sec: 去重时间窗；None = 读环境变量 / 默认 5.0s。

    Returns:
        (allowed: bool, reason: str)。allowed=False 表示时间窗内已有同载荷写入，
        调用方应跳过本次飞书写入。任何异常一律 fail-open 返回 (True, "guard_*")。
    """
    if disabled():
        return True, "guard_disabled"
    w = window_sec if window_sec is not None else _window()
    if w <= 0:
        return True, "guard_window_zero"
    key = _fingerprint(skillname, payload)
    now = time.time()
    try:
        d = _shared_dir()
        ledger_path = os.path.join(d, _LEDGER_NAME)
        lock_path = os.path.join(d, _LOCK_NAME)
        os.makedirs(d, exist_ok=True)
        with _local_lock:
            if _acquire_lock(lock_path) is None:
                return True, "guard_lock_timeout"
            try:
                data = {"schema": _SCHEMA, "entries": {}}
                try:
                    with open(ledger_path, "r", encoding="utf-8") as f:
                        loaded = json.load(f)
                    if isinstance(loaded, dict) and loaded.get("schema") == _SCHEMA:
                        data = loaded
                except (OSError, ValueError):
                    pass  # 损坏 / 首次运行 → 重建
                entries = {}
                for k, v in (data.get("entries") or {}).items():
                    try:
                        ts = float(v)
                    except (TypeError, ValueError):
                        continue
                    if now - ts <= w:
                        entries[k] = ts
                if key in entries:
                    return False, "duplicate_in_window"
                if len(entries) >= _MAX_ENTRIES:
                    for k in sorted(entries, key=entries.get)[:len(entries) - _MAX_ENTRIES + 1]:
                        entries.pop(k, None)
                entries[key] = now
                data["entries"] = entries
                try:
                    _atomic_write(ledger_path, data)
                except OSError:
                    return True, "guard_write_failed"
                return True, "claimed"
            finally:
                try:
                    os.unlink(lock_path)
                except OSError:
                    pass
    except Exception:
        return True, "guard_unavailable"


def release(payload: str, skillname: str = "ct-literature") -> None:
    """撤销一次 claim（飞书写入失败时调用，允许时间窗内重试）。

    与 claim 对称；任何异常静默忽略（fail-open，护栏永不阻断主链路）。
    """
    if disabled():
        return
    key = _fingerprint(skillname, payload)
    try:
        d = _shared_dir()
        ledger_path = os.path.join(d, _LEDGER_NAME)
        lock_path = os.path.join(d, _LOCK_NAME)
        with _local_lock:
            if _acquire_lock(lock_path) is None:
                return
            try:
                try:
                    with open(ledger_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except (OSError, ValueError):
                    return
                entries = data.get("entries") or {}
                if key in entries:
                    entries.pop(key, None)
                    data["entries"] = entries
                    _atomic_write(ledger_path, data)
            finally:
                try:
                    os.unlink(lock_path)
                except OSError:
                    pass
    except Exception:
        return


def _selftest():
    import shutil
    tmp = tempfile.mkdtemp(prefix="ct_lit_guard_")
    prev = {k: os.environ.get(k) for k in
            ("CT_LIT_WRITE_GUARD_DIR", "CT_LIT_WRITE_GUARD", "CT_LIT_WRITE_GUARD_WINDOW")}
    os.environ["CT_LIT_WRITE_GUARD_DIR"] = tmp
    os.environ.pop("CT_LIT_WRITE_GUARD", None)
    os.environ.pop("CT_LIT_WRITE_GUARD_WINDOW", None)
    try:
        ok, why = claim('{"topic":"A","hits":3}', "ct-literature")
        assert (ok, why) == (True, "claimed"), (ok, why)
        ok, why = claim('{"topic":"A","hits":3}', "ct-literature")
        assert ok is False and why == "duplicate_in_window", (ok, why)
        ok, why = claim('{"topic":"B","hits":3}', "ct-literature")
        assert ok is True, (ok, why)
        # 不同技能不得互相抑制
        ok, why = claim('{"topic":"A","hits":3}', "ct-safety")
        assert ok is True, (ok, why)
        # 窗口过期后可再次写入
        ok, _ = claim('{"topic":"C"}', "ct-literature", window_sec=0.05)
        assert ok is True
        ok, _ = claim('{"topic":"C"}', "ct-literature", window_sec=0.05)
        assert ok is False
        time.sleep(0.08)
        ok, _ = claim('{"topic":"C"}', "ct-literature", window_sec=0.05)
        assert ok is True
        # 关闭开关 → 恒允许
        os.environ["CT_LIT_WRITE_GUARD"] = "0"
        ok, why = claim('{"topic":"A","hits":3}', "ct-literature")
        assert (ok, why) == (True, "guard_disabled"), (ok, why)
        os.environ.pop("CT_LIT_WRITE_GUARD", None)
        # 写入失败后 release 撤销登记，窗口内仍可重试
        ok, _ = claim('{"topic":"E"}', "ct-literature")
        assert ok is True
        release('{"topic":"E"}', "ct-literature")
        ok, _ = claim('{"topic":"E"}', "ct-literature")
        assert ok is True
        # 载荷含不同 request_id 时必须由调用方剔除；此处模拟「已剔除」的稳定性
        ok, _ = claim('{"topic":"D"}', "ct-literature")
        assert ok is True
        ok, _ = claim('{"topic":"D"}', "ct-literature")
        assert ok is False
        print("feishu_write_guard selftest: ALL PASSED")
    finally:
        for k, v in prev.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    _selftest()
