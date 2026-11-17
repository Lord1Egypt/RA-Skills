# -*- coding: utf-8 -*-
"""构建时通用工具 —— 从 `generate_site.py` 主入口下沉，守住「主入口 ≤500 行」硬上限。

内容：
  * ``_CountingWriter``   —— 包裹 stdout，统计本次运行的 ⚠️/❌ 并收集告警原文
  * ``_parse_csv_arg``    —— CLI 逗号串 -> 列表
  * ``_parse_num_arg``    —— CLI 逗号串 -> float 列表（含非数字则告警并回退 None）
  * ``load_json_strict``  —— 读 JSON，失败即 parser.error（核心输入）
  * ``load_json_soft``    —— 读 JSON，失败告警并降级（可选输入）
  * ``bounded_int``       —— argparse type= 回调，拒绝越界整数
  * ``resolve_search_sources`` —— --keyword-search-sources 的「文件路径 / 内联 JSON」双语义解析
  * ``write_run_log``     —— 写 <output>.run.log（失败只告警，不掩盖已成功的生成）

设计说明：
  这些工具与「生成引擎」的业务逻辑无关，属纯 CLI/IO 适配层，故独立成模块。
  旧的下划线前缀命名沿用迁移前的写法，保持既有调用点零改动；新增函数一律用公共名。
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


class _CountingWriter:
    """P1#12：统计 ⚠️/❌ 并收集告警原文，供末尾 print_user_hints() 翻译成人话。"""

    def __init__(self, stream):
        self._stream = stream
        self.warns = 0
        self.errors = 0
        self.messages: list[str] = []

    def write(self, s: str) -> int:
        if "⚠️" in s:
            self.warns += s.count("⚠️")
            self.messages.append(s.strip())
        if "❌" in s:
            self.errors += s.count("❌")
            self.messages.append(s.strip())
        return self._stream.write(s)

    def flush(self):
        return self._stream.flush()


def _parse_csv_arg(s: str):
    """CLI 逗号字符串 -> 列表；空串返回 None。"""
    return [x.strip() for x in s.split(",")] if s else None


def _parse_num_arg(s: str):
    """CLI 逗号字符串 -> float 列表；含非数字告警并回退 None。"""
    if not s:
        return None
    try:
        return [float(x) for x in s.split(",")]
    except ValueError:
        print(f"  ⚠️ 图表数据解析失败(含非数字): {s} — 将回退估算值")
        return None


def load_json_strict(parser, path, label: str):
    """读取 CLI 指定的 JSON 文件；失败即 ``parser.error``（退出码 2）。

    用于「读不到就不能继续」的核心输入（新闻 JSON / 洞察 JSON 等）：
    文件不存在（``OSError``）与语法错误（``json.JSONDecodeError``）统一转成人话，
    不再让裸 traceback 冒到用户面前，也避免同类输入有的地方包错、有的地方不包。
    """
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        parser.error(f"{label} 不是合法 JSON：{path} —— {e}")
    except OSError as e:
        parser.error(f"{label} 读取失败：{path} —— {e}")


def load_json_soft(path, label: str, default=None):
    """读取 JSON 文件；失败打印 ⚠️ 并返回 ``default``（不中断生成）。

    用于「缺了也能降级」的可选输入（自定义排行榜 / 受众结论等）。
    返回 ``None`` 表示读取失败或文件内容就是 ``null``——调用方需自行决定
    是否覆盖已有值（参见 generate_site.py 中受众结论的处理）。
    """
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"  ⚠️ {label} 读取失败：{e}")
        return default


def bounded_int(minimum: int, maximum: int | None = None, name: str = "参数"):
    """构造 argparse ``type=`` 回调：拒绝越界整数，错误信息带范围提示。

    负数 workers 会让 ThreadPoolExecutor 直接报错、0 会静默不干活，
    故在解析阶段就拦下（与 ``--date`` 的即时校验保持同一风格）。
    """
    def _parse(raw: str) -> int:
        try:
            value = int(raw)
        except ValueError:
            raise argparse.ArgumentTypeError(f"{name} 需为整数，收到 {raw!r}")
        if value < minimum or (maximum is not None and value > maximum):
            rng = f"≥ {minimum}" if maximum is None else f"{minimum} ~ {maximum}"
            raise argparse.ArgumentTypeError(f"{name} 需在 {rng} 范围内，收到 {value}")
        return value

    return _parse


def resolve_search_sources(parser, spec: str) -> str:
    """解析 ``--keyword-search-sources``：是文件路径就读文件，否则视为内联 JSON。

    两种来源都在此处校验（合法 JSON + 非空 ``{name: url}`` 对象），
    避免非法输入被推迟到渲染中途才以裸 traceback 形式暴露。
    返回可直接注入模板的 JSON 字符串。
    """
    raw = spec
    if spec:
        try:
            as_path = Path(spec)
            if as_path.exists():
                raw = as_path.read_text(encoding="utf-8").strip()
        except OSError:
            pass  # 超长内联串会被当成非法文件名——按内联 JSON 继续校验
    try:
        parsed = json.loads(raw)
    except (json.JSONDecodeError, TypeError) as e:
        parser.error(f"--keyword-search-sources 需为 JSON 文件路径或 JSON 字符串：{e}")
    if not isinstance(parsed, dict) or not parsed:
        parser.error("--keyword-search-sources 需为非空的 {name: url} JSON 对象")
    return raw


def write_run_log(output: str, count: int, counter) -> str:
    """把本次运行的告警/错误计数写入 ``<output>.run.log``（供无人值守复盘）。

    写日志失败不应掩盖「HTML 已成功生成」这一事实，故只告警不抛。
    返回实际写入路径；失败返回 ``""``。
    """
    run_log = Path(output).with_suffix(".run.log")
    try:
        run_log.write_text(
            f"ai-weekly generate run @ {datetime.now().astimezone().isoformat(timespec='seconds')}\n"
            f"output: {output}\n"
            f"news: {count}\n"
            f"warnings: {counter.warns}\n"
            f"errors: {counter.errors}\n",
            encoding="utf-8",
        )
    except OSError as e:
        print(f"  ⚠️ 运行日志写入失败：{e}（报告已生成，可忽略）")
        return ""
    return str(run_log)


__all__ = [
    "_CountingWriter", "_parse_csv_arg", "_parse_num_arg",
    "load_json_strict", "load_json_soft", "bounded_int",
    "resolve_search_sources", "write_run_log",
]
