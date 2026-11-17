# -*- coding: utf-8 -*-
"""输入适配：把 Skill 收到的各种"网络来源"统一成 Core 能吃的对象。

Skill 的调用方是 Agent，它会自然地传各种形态：

* ``"examples/example.toml"``            —— 文件路径
* ``'[network]\\nid = "x"\\n...'``        —— TOML 文本
* 已经读好的 TOML 字典
* 已经解析好的 :class:`~fluid_network.models.Network`
* 上一轮 ``analyze_scenario`` 返回的 AnalysisResult（dict）

这一层只做**识别与转换**，不做任何校验或计算 —— 校验交给 Core，
这样错误信息的来源始终唯一。
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Mapping

from ..exceptions import ConfigError, ParseError, ValidationError
from ..models import Network, Scenario
from ..parser import FluidConfigParser

__all__ = [
    "NetworkSource",
    "ResolvedNetwork",
    "resolve_network_source",
    "looks_like_toml",
    "looks_like_path",
    "adapt_toml_document",
]


class ResolvedNetwork:
    """一次网络来源解析的结果。"""

    __slots__ = ("network", "scenarios", "source_kind", "source_ref")

    def __init__(self, network: Network, scenarios: tuple[Scenario, ...],
                 source_kind: str, source_ref: str) -> None:
        self.network = network
        self.scenarios = scenarios
        self.source_kind = source_kind    # "path" | "toml" | "document" | "network"
        self.source_ref = source_ref      # 供 Agent 回显，如文件路径

    def scenario(self, scenario_id: str) -> Scenario | None:
        for item in self.scenarios:
            if item.id == scenario_id:
                return item
        return None

    @property
    def scenario_ids(self) -> list[str]:
        return [s.id for s in self.scenarios]


# 类型别名，供 Schema 与签名使用
NetworkSource = Any


# --------------------------------------------------------------------------- #
# 形态判定
# --------------------------------------------------------------------------- #
def looks_like_toml(value: str) -> bool:
    """判断一段文本是不是 TOML 内容（而不是路径）。

    判据是"有没有段落头或键值行" —— 路径里不会出现 ``[section]`` 或
    ``key = value``（``=`` 在合法路径里极罕见，且路径不含换行）。
    """
    if "\n" not in value:
        return False
    stripped = value.lstrip()
    if stripped.startswith("[") or stripped.startswith("#"):
        return True
    for line in stripped.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line and not line.startswith("/"):
            return True
    return False


def looks_like_path(value: str) -> bool:
    """判断一段文本像不像文件路径。"""
    if "\n" in value:
        return False
    if len(value) > 512:
        return False
    if value.endswith(".toml"):
        return True
    # Windows 盘符、POSIX 绝对路径、相对路径
    return bool(
        os.path.isabs(value)
        or value.startswith("./")
        or value.startswith("../")
        or (len(value) > 2 and value[1] == ":")
        or "/" in value
        or "\\" in value
    )


# --------------------------------------------------------------------------- #
# 主入口
# --------------------------------------------------------------------------- #
def resolve_network_source(
    source: NetworkSource,
    *,
    parser: FluidConfigParser | None = None,
) -> ResolvedNetwork:
    """把任意形态的来源解析成 :class:`ResolvedNetwork`。

    抛出的都是 Core 的异常（:class:`ConfigError` / :class:`ParseError` /
    :class:`ValidationError`），由 Skill 层统一转成 :class:`SkillResult`。
    """
    parser = parser or FluidConfigParser()

    # 已经解析好的 Network（可能是 (Network, scenarios) 二元组）
    if isinstance(source, Network):
        return ResolvedNetwork(source, (), "network", source.id)

    if isinstance(source, (tuple, list)) and len(source) == 2 and isinstance(source[0], Network):
        network, scenarios = source
        return ResolvedNetwork(network, tuple(scenarios), "network", network.id)

    # 字典：可能是 TOML 文档，也可能是上一轮的 AnalysisResult
    if isinstance(source, Mapping):
        if _looks_like_analysis_result(source):
            raise ConfigError(
                "传入的是 AnalysisResult，不是网络定义。"
                "要基于已有结果继续分析，请把它交给 explain_load / compare_scenarios / render_report。"
            )
        network, scenarios = parser.parse(dict(source), source="<document>")
        return ResolvedNetwork(network, tuple(scenarios), "document", "<document>")

    if isinstance(source, str):
        return _resolve_string(source, parser)

    raise ConfigError(
        f"无法识别的网络来源类型 {type(source).__name__}；"
        "支持：TOML 文本、TOML 文件路径、已解析的 Network、或 TOML 字典"
    )


def _resolve_string(value: str, parser: FluidConfigParser) -> ResolvedNetwork:
    text = value.strip()
    if not text:
        raise ConfigError("网络来源为空字符串")

    # 1) 先按路径试 —— 文件存在才算数（避免把 TOML 文本误判成路径）
    if looks_like_path(text):
        path = Path(text)
        if path.is_file():
            network, scenarios = parser.load(path)
            return ResolvedNetwork(network, tuple(scenarios), "path", str(path))
        # 明确像路径又不存在 —— 报"文件不存在"比"TOML 语法错误"有用得多
        if text.endswith(".toml") or (not looks_like_toml(text)):
            raise ConfigError(
                f"配置文件不存在：{text}",
                diagnostic=_missing_file_diagnostic(text),
            )

    # 2) 当作 TOML 文本
    if not looks_like_toml(text):
        raise ConfigError(
            "无法识别网络来源：既不是存在的文件路径，也不像 TOML 内容。"
            'TOML 至少应包含 "[network]" 段落。',
        )
    network, scenarios = parser.loads(text, source="<inline toml>")
    return ResolvedNetwork(network, tuple(scenarios), "toml", "<inline toml>")


def _missing_file_diagnostic(path: str):
    from ..diagnostics import Diagnostic

    return Diagnostic(
        code="network_file_not_found",
        message=f"配置文件不存在：{path}",
        location=path,
        suggestion="检查路径是否正确；或直接把 TOML 文本作为 network_source 传入",
        context={"path": path},
    )


def _looks_like_analysis_result(value: Mapping) -> bool:
    """AnalysisResult 有 ``schema_version`` + ``loads`` + ``paths``，网络定义没有。"""
    return "schema_version" in value and "loads" in value and "paths" in value


def adapt_toml_document(doc: Mapping[str, Any]) -> dict:
    """复制一份 TOML 文档，避免调用方传入的对象被后续步骤改动。"""
    return {k: v for k, v in doc.items()}
