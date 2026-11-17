"""Parse macOS .sdef XML files into structured data for CLI generation."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

# Skip sdef files larger than this to avoid memory explosion
MAX_SDEF_BYTES = 1_000_000  # 1MB


@dataclass
class SdefParam:
    name: str
    type: str
    description: str
    optional: bool
    is_direct: bool


@dataclass
class SdefCommand:
    name: str
    cli_name: str
    func_name: str
    description: str
    suite_name: str
    parameters: list[SdefParam]
    direct_parameter: SdefParam | None
    result_type: str | None
    is_standard_suite: bool
    hidden: bool


@dataclass
class SdefProperty:
    name: str
    cli_name: str
    func_name: str
    type: str
    description: str
    access: str
    class_name: str
    hidden: bool


@dataclass
class SdefEnumeration:
    name: str
    values: list[tuple[str, str]]


@dataclass
class SdefInfo:
    app_name: str
    sdef_path: str
    commands: list[SdefCommand] = field(default_factory=list)
    properties: list[SdefProperty] = field(default_factory=list)
    enumerations: list[SdefEnumeration] = field(default_factory=list)


STANDARD_COMMAND_NAMES = frozenset({
    "open", "close", "save", "print", "quit", "count",
    "delete", "duplicate", "exists", "make", "move", "run",
})


def _to_cli_name(name: str) -> str:
    return name.strip().replace(" ", "-").lower()


def _to_func_name(name: str) -> str:
    return name.strip().replace(" ", "_").replace("-", "_").lower()


def _parse_direct_parameter(elem: ET.Element) -> SdefParam | None:
    dp = elem.find("direct-parameter")
    if dp is None:
        return None

    # Type can be an attribute or a child <type> element
    dp_type = dp.get("type", "")
    if not dp_type:
        type_child = dp.find("type")
        if type_child is not None:
            dp_type = type_child.get("type", "")
            if type_child.get("list") == "yes":
                dp_type = f"list of {dp_type}"

    optional = dp.get("optional", "no") == "yes"
    return SdefParam(
        name="direct",
        type=dp_type,
        description=dp.get("description", ""),
        optional=optional,
        is_direct=True,
    )


def _parse_parameters(elem: ET.Element) -> list[SdefParam]:
    params = []
    for p in elem.findall("parameter"):
        params.append(SdefParam(
            name=p.get("name", ""),
            type=p.get("type", ""),
            description=p.get("description", ""),
            optional=p.get("optional", "no") == "yes",
            is_direct=False,
        ))
    return params


def _is_standard_suite(suite_elem: ET.Element) -> bool:
    code = suite_elem.get("code", "")
    return code in ("****", "????")


def _parse_commands(suite: ET.Element, suite_name: str, standard: bool) -> list[SdefCommand]:
    commands = []
    for cmd in suite.findall("command"):
        name = cmd.get("name", "")
        hidden = cmd.get("hidden", "no") == "yes"

        # Result type
        result_elem = cmd.find("result")
        result_type = result_elem.get("type") if result_elem is not None else None

        is_std = standard or (name.lower() in STANDARD_COMMAND_NAMES and standard)

        commands.append(SdefCommand(
            name=name,
            cli_name=_to_cli_name(name),
            func_name=_to_func_name(name),
            description=cmd.get("description", ""),
            suite_name=suite_name,
            parameters=_parse_parameters(cmd),
            direct_parameter=_parse_direct_parameter(cmd),
            result_type=result_type,
            is_standard_suite=is_std,
            hidden=hidden,
        ))
    return commands


def _parse_properties(
    elem: ET.Element, class_name: str, hidden_parent: bool = False
) -> list[SdefProperty]:
    props = []
    for prop in elem.findall("property"):
        prop_hidden = prop.get("hidden", "no") == "yes" or hidden_parent

        # Access: if not specified, default to "rw"
        access = prop.get("access", "rw")

        # Type can be attribute or child <type> element
        prop_type = prop.get("type", "")
        if not prop_type:
            type_child = prop.find("type")
            if type_child is not None:
                prop_type = type_child.get("type", "")

        name = prop.get("name", "")
        props.append(SdefProperty(
            name=name,
            cli_name=_to_cli_name(name),
            func_name=_to_func_name(name),
            type=prop_type,
            description=prop.get("description", ""),
            access=access,
            class_name=class_name,
            hidden=prop_hidden,
        ))
    return props


def _parse_enumerations(suite: ET.Element) -> list[SdefEnumeration]:
    enums = []
    for enum in suite.findall("enumeration"):
        values = []
        for enumerator in enum.findall("enumerator"):
            values.append((enumerator.get("name", ""), enumerator.get("code", "")))
        enums.append(SdefEnumeration(
            name=enum.get("name", ""),
            values=values,
        ))
    return enums


MAX_INHERITED_PROPERTIES = 5000  # Cap to prevent memory explosion


def _resolve_inheritance(
    properties: list[SdefProperty],
    inheritance: dict[str, str],
) -> list[SdefProperty]:
    """Copy parent class properties to child classes via inheritance chain."""
    # Build lookup: class_name -> set of property names already defined
    existing = {}
    for p in properties:
        existing.setdefault(p.class_name, set()).add(p.name)

    # Build lookup: class_name -> list of properties
    props_by_class: dict[str, list[SdefProperty]] = {}
    for p in properties:
        props_by_class.setdefault(p.class_name, []).append(p)

    # Resolve full inheritance chain for each class (with cycle guard)
    def ancestors(cls: str) -> list[str]:
        chain = []
        visited: set[str] = set()
        while cls in inheritance:
            parent = inheritance[cls]
            if parent in visited:
                break  # cycle guard
            visited.add(parent)
            chain.append(parent)
            cls = parent
        return chain

    inherited = []
    for cls in inheritance:
        for ancestor in ancestors(cls):
            for p in props_by_class.get(ancestor, []):
                if p.name not in existing.get(cls, set()):
                    inherited.append(SdefProperty(
                        name=p.name,
                        cli_name=p.cli_name,
                        func_name=p.func_name,
                        type=p.type,
                        description=p.description,
                        access=p.access,
                        class_name=cls,
                        hidden=p.hidden,
                    ))
                    existing.setdefault(cls, set()).add(p.name)
                    if len(inherited) >= MAX_INHERITED_PROPERTIES:
                        return properties + inherited

    return properties + inherited


def parse_sdef(sdef_path: str, app_name: str, *, max_bytes: int = MAX_SDEF_BYTES) -> SdefInfo:
    """Parse an sdef file and return structured info.

    Args:
        sdef_path: Path to the .sdef file.
        app_name: Display name of the application (e.g. "Music").
        max_bytes: Maximum file size in bytes. Files larger than this raise ValueError.

    Returns:
        SdefInfo with parsed commands, properties, and enumerations.

    Raises:
        ValueError: If the sdef file exceeds max_bytes.
    """
    path = Path(sdef_path)
    file_size = path.stat().st_size
    if file_size > max_bytes:
        raise ValueError(
            f"{app_name} sdef too large ({file_size:,} bytes > {max_bytes:,} limit)"
        )

    xml_string = path.read_text(encoding="utf-8")

    # Strip DOCTYPE (including multi-line with internal subset [...])
    xml_string = re.sub(r"<!DOCTYPE[^[>]*(?:\[.*?\])?\s*>", "", xml_string, flags=re.DOTALL)

    root = ET.fromstring(xml_string)

    info = SdefInfo(app_name=app_name, sdef_path=sdef_path)

    # Track class inheritance: child -> parent
    inheritance: dict[str, str] = {}

    for suite in root.findall("suite"):
        suite_name = suite.get("name", "")
        standard = _is_standard_suite(suite)

        # Commands
        info.commands.extend(_parse_commands(suite, suite_name, standard))

        # Enumerations
        info.enumerations.extend(_parse_enumerations(suite))

        # Properties from <class> elements
        for cls in suite.findall("class"):
            class_name = cls.get("name", "")
            class_hidden = cls.get("hidden", "no") == "yes"
            info.properties.extend(_parse_properties(cls, class_name, class_hidden))

            # Record inheritance
            parent = cls.get("inherits")
            if parent:
                inheritance[class_name] = parent

        # Properties from <class-extension> elements
        for ext in suite.findall("class-extension"):
            class_name = ext.get("extends", "")
            info.properties.extend(_parse_properties(ext, class_name))

    # Resolve inheritance so child classes include parent properties
    info.properties = _resolve_inheritance(info.properties, inheritance)

    return info
