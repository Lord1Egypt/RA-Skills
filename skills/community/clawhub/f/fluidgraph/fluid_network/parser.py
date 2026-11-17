# -*- coding: utf-8 -*-
"""TOML -> 数据模型的解析器。

职责边界
--------
parser **只负责把配置变成可信的对象**，不做任何物理计算。它承担四件事：

1. 读取 TOML（文件 / 字符串）；
2. 结构校验：必需字段齐全、没有拼错的未知字段；
3. 引用校验：``from``/``to`` 指向的节点存在、工况引用的阀门存在；
4. 汇总全部错误后一次性抛出，而不是遇到第一个错就中断 —— 配置错了就
   应该一次看全，而不是改一个跑一次。

字段级数值校验（正数、非空等）由 :mod:`fluid_network.models` 的 dataclass
负责，这里不重复实现。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, NoReturn

from .diagnostics import Diagnostic, DiagnosticCollector
from .exceptions import ConfigError, ParseError, ValidationError
from .models import Network, Node, NodeType, Pipe, Scenario, Valve

try:  # Python 3.11+ 内置
    import tomllib as _toml
except ModuleNotFoundError:  # pragma: no cover - 仅 Python <= 3.10 走这里
    try:
        import tomli as _toml  # type: ignore[no-redef]
    except ModuleNotFoundError as exc:  # pragma: no cover
        raise ImportError(
            "需要 TOML 解析库：Python 3.11+ 自带 tomllib；"
            "更低版本请先安装 tomli（pip install tomli）"
        ) from exc


# 各段落允许出现的键。多出来的键一律报错，避免"写了但没生效"的隐蔽 bug。
_NETWORK_KEYS = {"id", "name"}
_NODE_KEYS = {"id", "type", "pressure", "min_pressure", "min_flow", "required_flow", "supply_limit"}
_PIPE_KEYS = {"id", "from", "to", "resistance", "diameter", "length"}
_VALVE_KEYS = {"id", "from", "to"}
_SCENARIO_KEYS = {"id", "name", "valve_states", "failures", "actions"}

_KNOWN_SECTIONS = {"network", "nodes", "pipes", "valves", "scenarios"}


# --------------------------------------------------------------------------- #
# 结构化错误辅助
#
# 这些函数把"抛异常"和"结构化诊断"两件事绑在一起：既保留既有的
# try/except 使用方式，又让每个错误都带位置、字段与修复建议。
# --------------------------------------------------------------------------- #
def _edit_distance(a: str, b: str) -> int:
    """Levenshtein 距离 —— 用来给拼错的字段名推荐最接近的正确写法。"""
    if a == b:
        return 0
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        current = [i]
        for j, cb in enumerate(b, 1):
            current.append(min(
                previous[j] + 1,
                current[j - 1] + 1,
                previous[j - 1] + (ca != cb),
            ))
        previous = current
    return previous[-1]


def _fail(code: str, message: str, *, site: str = "", field: str = "",
          suggestion: str = "", **context) -> "NoReturn":
    """抛出一个携带结构化诊断的 ParseError。"""
    diagnostic = Diagnostic(
        code=code, message=message,
        location=(f"{site}.{field}" if site and field else site),
        field=field, suggestion=suggestion, context=context,
    )
    raise ParseError(str(diagnostic), diagnostic)


def _diagnostics_of(exc: Exception, site: str) -> list[Diagnostic]:
    """把捕获到的异常转成诊断，并补上它缺失的位置信息。

    元件解析时异常是从深层（models.py 的 dataclass 校验）冒上来的，
    那里只知道"某个节点"，不知道"它是 [[nodes]] 里的第几个"。
    这里统一把外层坐标补回去。
    """
    existing = getattr(exc, "diagnostics", None)
    if existing:
        return [
            d if d.location.startswith(site) else Diagnostic(
                code=d.code, message=d.message, location=f"{site}",
                field=d.field, suggestion=d.suggestion,
                severity=d.severity, context=d.context,
            )
            for d in existing
        ]

    diagnostic = getattr(exc, "diagnostic", None)
    if diagnostic is not None:
        return [diagnostic if diagnostic.location else Diagnostic(
            code=diagnostic.code, message=diagnostic.message, location=site,
            field=diagnostic.field, suggestion=diagnostic.suggestion,
            severity=diagnostic.severity, context=diagnostic.context,
        )]

    # 兜底：没有结构化信息的异常（理论上不该出现）
    return [Diagnostic(code="parse_error", message=str(exc), location=site)]



class FluidConfigParser:
    """把 TOML 解析成 :class:`Network` 与一组 :class:`Scenario`。

    典型用法::

        parser = FluidConfigParser()
        net, scenarios = parser.load("examples/example.toml")
        scenario = {s.id: s for s in scenarios}["normal"]
    """

    def __init__(self, *, strict: bool = True) -> None:
        # strict=True 时未知字段报错；置 False 可用于兼容旧配置。
        self.strict = strict

    # ------------------------------------------------------------------ #
    # 入口
    # ------------------------------------------------------------------ #
    def load(self, path: str | Path) -> tuple[Network, tuple[Scenario, ...]]:
        """从文件读取并解析。"""
        path = Path(path)
        if not path.exists():
            raise ConfigError(f"配置文件不存在：{path}")
        try:
            raw_bytes = path.read_bytes()
        except OSError as exc:
            raise ConfigError(f"无法读取配置文件 {path}：{exc}") from exc
        return self.loads(raw_bytes, source=str(path))

    def loads(self, data: str | bytes, *, source: str = "<string>") -> tuple[Network, tuple[Scenario, ...]]:
        """从字符串 / 字节解析。"""
        if isinstance(data, str):
            data = data.encode("utf-8")
        try:
            doc = _toml.loads(data.decode("utf-8"))
        except UnicodeDecodeError as exc:
            raise ConfigError(f"{source} 不是合法的 UTF-8 文件：{exc}") from exc
        except _toml.TOMLDecodeError as exc:
            raise ConfigError(f"{source} 不是合法的 TOML：{exc}") from exc
        return self.parse(doc, source=source)

    def parse(self, doc: Mapping[str, Any], *, source: str = "<dict>") -> tuple[Network, tuple[Scenario, ...]]:
        """解析已经读出来的 TOML 字典。"""
        if not isinstance(doc, Mapping):
            raise ConfigError(f"{source} 的顶层必须是 TOML 表，实际是 {type(doc).__name__}")

        if self.strict:
            unknown = sorted(set(doc) - _KNOWN_SECTIONS)
            if unknown:
                _fail("unknown_section",
                      f"存在未知的顶层段落：{', '.join(unknown)}",
                      site=source, field=unknown[0],
                      suggestion=f"删掉它们，或改用：{', '.join(sorted(_KNOWN_SECTIONS))}",
                      unknown_sections=unknown,
                      allowed_sections=sorted(_KNOWN_SECTIONS))

        network_doc = doc.get("network")
        if not isinstance(network_doc, Mapping):
            _fail("missing_network_section",
                  "缺少 [network] 段落（需要提供网络 id）",
                  site=source,
                  suggestion='在文件开头加上一个 [network] 段落并给它一个 id，例如：'
                             + chr(10) + '[network]' + chr(10) + 'id = "your-network-id"')

        self._check_keys(network_doc, _NETWORK_KEYS, "[network]")
        network_id = self._require_str(network_doc, "id", "[network]")
        network_name = self._optional_str(network_doc, "name", "", "[network]") or network_id

        node_docs = self._section_list(doc, "nodes", "[[nodes]]", source)
        pipe_docs = self._section_list(doc, "pipes", "[[pipes]]", source)
        valve_docs = self._section_list(doc, "valves", "[[valves]]", source)
        scenario_docs = self._section_list(doc, "scenarios", "[[scenarios]]", source)

        # -- 元件解析 -------------------------------------------------- #
        # 结构错误（缺字段 / 类型不对）先按元素逐个收集，能在一次运行里全部报出。
        collector = DiagnosticCollector()
        nodes = self._parse_each(node_docs, "[[nodes]]", self._parse_node, collector)
        pipes = self._parse_each(pipe_docs, "[[pipes]]", self._parse_pipe, collector)
        valves = self._parse_each(valve_docs, "[[valves]]", self._parse_valve, collector)
        if collector.has_errors:
            raise ValidationError.from_collector(
                f"{source} 中的元件定义有 {len(collector.errors)} 处问题", collector
            )

        # -- 跨对象校验（由 Network 的 __post_init__ 完成） ------------ #
        network = Network(
            id=network_id,
            name=network_name,
            nodes=tuple(nodes),
            pipes=tuple(pipes),
            valves=tuple(valves),
        )

        # -- 工况解析 + 引用校验 --------------------------------------- #
        scenarios, scenario_collector = self._parse_scenarios(scenario_docs, network)
        if scenario_collector.has_errors:
            raise ValidationError.from_collector(
                f"{source} 中的工况定义有 {len(scenario_collector.errors)} 处问题", scenario_collector
            )

        return network, tuple(scenarios)

    # ------------------------------------------------------------------ #
    # 元件解析
    # ------------------------------------------------------------------ #
    def _parse_node(self, doc: Mapping[str, Any], where: str) -> Node:
        self._check_keys(doc, _NODE_KEYS, where)
        node_id = self._require_str(doc, "id", where)
        raw_type = self._require_str(doc, "type", where)
        try:
            node_type = NodeType(raw_type.strip().lower())
        except ValueError:
            valid = [t.value for t in NodeType]
            _fail("invalid_node_type",
                  f"节点 '{node_id}' 的 type='{raw_type}' 无效",
                  site=where, field="type",
                  suggestion=f"把 type 改成以下之一：{', '.join(valid)}",
                  node_id=node_id, actual_value=raw_type, allowed_values=valid)

        return Node(
            id=node_id,
            type=node_type,
            pressure=doc.get("pressure"),
            min_pressure=doc.get("min_pressure"),
            min_flow=doc.get("min_flow"),
            required_flow=doc.get("required_flow"),
            supply_limit=doc.get("supply_limit"),
        )

    def _parse_pipe(self, doc: Mapping[str, Any], where: str) -> Pipe:
        self._check_keys(doc, _PIPE_KEYS, where)
        pipe_id = self._require_str(doc, "id", where)
        return Pipe(
            id=pipe_id,
            from_node=self._require_str(doc, "from", where),
            to_node=self._require_str(doc, "to", where),
            resistance=self._require_number(doc, "resistance", where),
            diameter=self._require_number(doc, "diameter", where),
            length=self._optional_number(doc, "length", where),
        )

    def _parse_valve(self, doc: Mapping[str, Any], where: str) -> Valve:
        self._check_keys(doc, _VALVE_KEYS, where)
        valve_id = self._require_str(doc, "id", where)
        return Valve(
            id=valve_id,
            from_node=self._require_str(doc, "from", where),
            to_node=self._require_str(doc, "to", where),
        )

    def _parse_scenarios(
        self, docs: list[tuple[Mapping[str, Any], str]], network: Network
    ) -> tuple[list[Scenario], DiagnosticCollector]:
        scenarios: list[Scenario] = []
        collector = DiagnosticCollector()
        seen: set[str] = set()

        for doc, where in docs:
            try:
                self._check_keys(doc, _SCENARIO_KEYS, where)
                scenario_id = self._require_str(doc, "id", where)
                if scenario_id in seen:
                    raise ValidationError(
                        f"工况 id '{scenario_id}' 重复",
                        diagnostics=[Diagnostic(
                            code="duplicate_scenario_id",
                            message=f"工况 id '{scenario_id}' 重复",
                            location=f"{where}.id", field="id",
                            suggestion=f"把其中一个工况的 id 改掉（'{scenario_id}' 已被占用）",
                            context={"scenario_id": scenario_id},
                        )],
                    )
                seen.add(scenario_id)

                raw_states = doc.get("valve_states", {})
                if not isinstance(raw_states, Mapping):
                    _fail("invalid_valve_states",
                  "valve_states 必须是表，例如 [scenarios.valve_states] 后跟 V1 = false",
                  site=where, field="valve_states",
                  suggestion="写成独立的表头：[scenarios.valve_states] 然后每行 V1 = true/false")

                for valve_id, state in raw_states.items():
                    if not any(v.id == valve_id for v in network.valves):
                        available = ", ".join(sorted(v.id for v in network.valves)) or "（无）"
                        raise ValidationError(
                            f"工况 '{scenario_id}' 引用了不存在的阀门 '{valve_id}'；可用阀门：{available}",
                            diagnostics=[Diagnostic(
                                code="unknown_valve_in_scenario",
                                message=f"工况 '{scenario_id}' 引用了不存在的阀门 '{valve_id}'",
                                location=f"{where}.valve_states.{valve_id}",
                                field="valve_states",
                                suggestion=f"把 '{valve_id}' 改成已定义的阀门，或先声明它；可用阀门：{available}",
                                context={"scenario_id": scenario_id, "valve_id": valve_id,
                                         "available_valves": sorted(v.id for v in network.valves)},
                            )],
                        )
                    if not isinstance(state, bool):
                        _fail("invalid_valve_state",
                              f"工况 '{scenario_id}' 中阀门 '{valve_id}' 的开关状态必须是布尔值，"
                              f"实际是 {type(state).__name__}",
                              site=f"{where}.valve_states", field=valve_id,
                              suggestion="TOML 中写 true / false（小写，不加引号）",
                              scenario_id=scenario_id, valve_id=valve_id)

                scenarios.append(
                    Scenario(
                        id=scenario_id,
                        name=self._optional_str(doc, "name", "", where) or scenario_id,
                        valve_states=raw_states,
                        failures=self._optional_dict_tuple(doc, "failures", scenario_id),
                        actions=self._optional_dict_tuple(doc, "actions", scenario_id),
                    )
                )
            except (ParseError, ValidationError) as exc:
                collector.extend(_diagnostics_of(exc, where))

        if not collector.has_errors and not scenarios:
            collector.error(
                "no_scenarios",
                "配置中没有定义任何 [[scenarios]]，无法确定计算工况",
                location="[[scenarios]]",
                suggestion='至少添加一个工况：' + chr(10) + '[[scenarios]]' + chr(10) + 'id = "normal"',
            )

        return scenarios, collector

    # ------------------------------------------------------------------ #
    # 通用辅助
    # ------------------------------------------------------------------ #
    @staticmethod
    def _parse_each(docs, where, fn, collector: DiagnosticCollector):
        """逐个解析元件，把失败转成诊断后继续 —— 一次收集全部问题。"""
        parsed = []
        for doc, site in docs:
            try:
                parsed.append(fn(doc, site))
            except (ParseError, ValidationError) as exc:
                collector.extend(_diagnostics_of(exc, site))
        return parsed

    @staticmethod
    def _section_list(doc: Mapping[str, Any], key: str, label: str, source: str) -> list[tuple[Mapping[str, Any], str]]:
        value = doc.get(key, [])
        if not isinstance(value, list):
            _fail("invalid_section_type",
                  f"{key} 必须是数组表（{label}），实际是 {type(value).__name__}",
                  site=source, field=key,
                  suggestion=f"把它写成 {label} 形式")
        for i, item in enumerate(value):
            if not isinstance(item, Mapping):
                _fail("invalid_section_entry", f"{label}[{i}] 必须是表",
                      site=f"{label}[{i}]",
                      suggestion=f"确认 {label}[{i}] 是标准的键值表（不是数组或标量）")
        return [(item, f"{label}[{i}]") for i, item in enumerate(value)]

    def _check_keys(self, doc: Mapping[str, Any], allowed: set[str], where: str) -> None:
        if not self.strict:
            return
        unknown = sorted(set(doc) - allowed)
        if unknown:
            # 拼写错误是最常见的原因，给出最接近的候选能省一轮往返
            best = min(unknown, key=lambda u: min(
                (_edit_distance(u, a), a) for a in allowed
            ))
            closest = min(allowed, key=lambda a: _edit_distance(best, a))
            distance = _edit_distance(best, closest)
            hint = (f"'{best}' 是不是想写 '{closest}'？"
                    if distance <= 3 else
                    f"可用字段：{', '.join(sorted(allowed))}")
            _fail("unknown_field",
                  f"存在未知字段：{', '.join(unknown)}",
                  site=where, field=best, suggestion=hint,
                  unknown_fields=unknown, allowed_fields=sorted(allowed))

    @staticmethod
    def _require_str(doc: Mapping[str, Any], key: str, where: str) -> str:
        if key not in doc:
            _fail("missing_required_field",
                  f"缺少必需字段 '{key}'",
                  site=where, field=key,
                  suggestion=f"在 {where} 里补上 {key} = \"...\"")
        value = doc[key]
        if not isinstance(value, str) or not value.strip():
            _fail("invalid_string",
                  f"字段 '{key}' 必须是非空字符串，实际是 {value!r}",
                  site=where, field=key,
                  suggestion=f"把 {key} 改成一个非空字符串（当前值 {value!r} 不是）",
                  actual_value=repr(value))
        return value.strip()

    @staticmethod
    def _optional_str(doc: Mapping[str, Any], key: str, default: str, where: str) -> str:
        if key not in doc:
            return default
        value = doc[key]
        if not isinstance(value, str):
            _fail("invalid_string", f"字段 '{key}' 必须是字符串，实际是 {value!r}",
                  site=where, field=key,
                  suggestion=f"给 {key} 加上引号，或直接删掉该字段使用默认值",
                  actual_value=repr(value))
        return value.strip() or default

    @staticmethod
    def _require_number(doc: Mapping[str, Any], key: str, where: str) -> float:
        if key not in doc:
            _fail("missing_required_field",
                  f"缺少必需字段 '{key}'",
                  site=where, field=key,
                  suggestion=f"在 {where} 里补上 {key}，且必须是正数")
        return FluidConfigParser._as_number(doc[key], key, where)

    @staticmethod
    def _optional_number(doc: Mapping[str, Any], key: str, where: str) -> float | None:
        if key not in doc:
            return None
        return FluidConfigParser._as_number(doc[key], key, where)

    @staticmethod
    def _as_number(value: Any, key: str, where: str) -> float:
        # 显式排除 bool —— Python 里 True 是 int 的子类，静默接受会很坑。
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            # 字符串数字是最常见的错误，单独给一条能直接照做的建议
            hint = ""
            if isinstance(value, str):
                try:
                    float(value)
                    hint = f"看起来是想写数字，去掉引号即可：{key} = {value}"
                except ValueError:
                    hint = f"把 {key} 改成一个数字"
            else:
                hint = f"把 {key} 改成一个数字（当前是 {type(value).__name__}）"
            _fail("invalid_number",
                  f"字段 '{key}' 必须是数字，实际是 {value!r}",
                  site=where, field=key, suggestion=hint, actual_value=repr(value))
        return float(value)

    @staticmethod
    def _optional_dict_tuple(doc: Mapping[str, Any], key: str, scenario_id: str) -> tuple[Mapping[str, Any], ...]:
        """读取预留的扩展字段（failures / actions），只保留不解释。

        一阶段求解器不会消费它们，但保留下来可以让场景描述在版本演进中不丢失。
        """
        value = doc.get(key, [])
        if isinstance(value, Mapping):  # 允许写成单张表
            value = [value]
        if not isinstance(value, list):
            _fail("invalid_section_type",
                  f"工况 '{scenario_id}' 的 '{key}' 必须是数组表或表",
                  site=f"[[scenarios]]", field=key,
                  suggestion=f"把 {key} 写成 [[scenarios.{key}]] 数组表形式")
        entries: list[Mapping[str, Any]] = []
        for i, item in enumerate(value):
            if not isinstance(item, Mapping):
                _fail("invalid_section_entry",
                      f"工况 '{scenario_id}' 的 '{key}' 第 {i} 项必须是表",
                      site=f"[[scenarios.{key}]][{i}]",
                      suggestion="每一项都应是键值表")
            entries.append(dict(item))
        return tuple(entries)


# --------------------------------------------------------------------------- #
# 模块级便捷函数
# --------------------------------------------------------------------------- #
def load_network(path: str | Path) -> tuple[Network, tuple[Scenario, ...]]:
    """读取 TOML 文件，返回 ``(Network, scenarios)``。"""
    return FluidConfigParser().load(path)


def load_scenarios(path: str | Path) -> dict[str, Scenario]:
    """读取 TOML 文件，返回 ``{scenario_id: Scenario}``。"""
    _, scenarios = load_network(path)
    return {s.id: s for s in scenarios}


__all__ = ["FluidConfigParser", "load_network", "load_scenarios"]
