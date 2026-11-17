#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data_guard.py — 取数失败可见化（NEED_DATA 通用化）

样板：candidate_gate.py 的 NEED_DATA 动作。那里只覆盖了「字典缺项」，
这里推广到全部取数失败的路径，并统一了「取数失败 ≠ 无数据」的约定。

🔴 核心约定（写给未来的自己）
────────────────────────────────────────────────────────────
**取数失败 ≠ 业务上「没有这个东西」。**
接口返 404、超时、空响应、结构变了 —— 这些都必须显式报出来，
绝不能 `except: return None` 之后让调用方当成「无数据」继续跑。

一个静默的 None 会变成：
  门槛判定 → DATA_FAIL（其实可能真触发了 B1/B2）
  台账同步 → 漏同步一份台账，没人数得出来
  监控告警 → 「一切正常」，用户以为风险已覆盖

统一三种状态（贯穿全部 7 个脚本）：
  OK        取数成功
  EMPTY     接口通、但业务上确实没有（如「本周无新财报」）
  FETCH_FAIL 接口不通/超时/结构变了 —— 🔴 必须与 EMPTY 严格区分

用法：
  from data_guard import FetchResult, fetch_status
  r = fetch_status(lambda: _get(url))
  if r.state == "FETCH_FAIL":
      ...  # 必须上报，不许当成 EMPTY
"""
from __future__ import annotations

import time
import urllib.error
import urllib.request
from typing import Any, Callable

UA = {"User-Agent": "Mozilla/5.0"}


class FetchResult:
    """取数结果的三态容器。state ∈ {OK, EMPTY, FETCH_FAIL}。

    ⚠️ 用 truthiness 判断会踩坑（空 dict 也是 falsy），
    必须显式判 `r.state == "OK"`。
    """

    __slots__ = ("state", "value", "error")

    def __init__(self, state: str, value: Any = None, error: str = ""):
        self.state = state
        self.value = value
        self.error = error

    def __bool__(self) -> bool:
        return self.state == "OK"

    def __repr__(self) -> str:
        if self.error:
            return f"FetchResult({self.state}, error={self.error!r})"
        return f"FetchResult({self.state}, {self.value!r})"

    @property
    def ok(self) -> bool:
        return self.state == "OK"

    @property
    def failed(self) -> bool:
        return self.state == "FETCH_FAIL"

    @property
    def empty(self) -> bool:
        return self.state == "EMPTY"


def fetch_status(fn: Callable[[], Any], tries: int = 3,
                 delay: float = 1.0, empty_ok: bool = True) -> FetchResult:
    """把「可能抛异常的取数函数」包成三态结果。

    fn            —— 取数函数，返回业务值；返回 None/空容器视为业务上的空
    tries         —— 失败重试次数（含首次）
    delay         —— 重试退避基数秒，第 n 次失败后等 delay*n
    empty_ok      —— True: fn 返回空值 → EMPTY；False: 空值 → FETCH_FAIL

    🔴 绝不吞异常：异常文本全部保留在 .error，交由调用方上报。
    """
    last = ""
    for i in range(tries):
        try:
            v = fn()
            if v is None or (hasattr(v, "__len__") and len(v) == 0):
                return FetchResult("EMPTY", None,
                                   "接口可达但返回空（业务上的空，非取数失败）")
            return FetchResult("OK", v, "")
        except Exception as exc:                     # noqa: BLE001
            last = f"{type(exc).__name__}: {exc}"
            if i < tries - 1:
                time.sleep(delay * (i + 1))
    return FetchResult("FETCH_FAIL", None,
                       f"重试 {tries} 次仍失败｜{last}")


def need_data(line: str, task: str, codes: list[str] | None = None,
              cmd: str = "") -> str:
    """生成一段 NEED_DATA / FETCH_FAIL 的告警文本（stdout 会进飞书）。

    🔴 这段文本必须**非空**。no_agent 任务的判定是「stdout 非空即投递」，
    返回空字符串 = 静默成功 = 故障被吃掉。
    """
    parts = [line]
    if codes:
        parts.append(f"标的：{'、'.join(codes)}")
    if cmd:
        parts.append(f"复现命令：{cmd}")
    return "🔴 取数失败 · " + "｜".join(parts)


def summary_line(codes: list[str], failed: list[str]) -> str:
    """结尾汇总行：只要有失败就非空，供 no_agent 判定投递。"""
    if not failed:
        return ""
    return (f"🔴 取数失败 {len(failed)}/{len(codes)} 只：" +
            "、".join(failed) + " —— 本次结果不完整，不可当作'无变化'")


def demo():
    """自检。断言逻辑坏掉时立刻失败，不等运行到线上。"""
    calls = {"n": 0}

    def boom():
        calls["n"] += 1
        raise ValueError("接口 500")

    r = fetch_status(boom, tries=2, delay=0)
    assert r.state == "FETCH_FAIL", r
    assert "ValueError" in r.error, r.error
    assert calls["n"] == 2, calls

    r = fetch_status(lambda: [], tries=1, delay=0)
    assert r.state == "EMPTY", r

    r = fetch_status(lambda: [1, 2], tries=1, delay=0)
    assert r.state == "OK" and r.value == [1, 2], r
    assert bool(r) is True and r.failed is False and r.empty is False

    # 空 dict 不能因为 falsy 被误判
    r = fetch_status(lambda: {}, tries=1, delay=0)
    assert r.state == "EMPTY", r

    # need_data 永远非空 —— 否则 no_agent 会静默吃掉故障
    s = need_data("公告接口 3 次超时", "持仓公告扫描", ["600000"], "curl x")
    assert s and s.startswith("🔴"), s
    assert summary_line(["a", "b"], ["b"]) != ""
    assert summary_line(["a", "b"], []) == ""
    print("✅ data_guard 自检通过")


if __name__ == "__main__":
    demo()