"""
声明式能力契约

每个 agent-bridge 命令声明自己的 read/write 范围、网络需求与 dry-run
支持。默认契约在本模块定义;config.yaml 的 `capabilities` 段只能收紧
(禁用命令、缩小 write_scope),不能放宽——放宽尝试会被拒绝。

这与 AGENTS.md 的行为规则互为冗余:协议文档约束 Agent 意图,
契约在工具入口做机器强制。
"""

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from .agent_logger import get_logger

LOG = get_logger("capabilities")


class CapabilityError(Exception):
    """能力契约校验失败"""


@dataclass(frozen=True)
class Capability:
    """单条命令的能力声明。write_scope 为仓库根相对的前缀列表。"""

    command: str
    write_scope: tuple[str, ...] = ()
    network: bool = False
    dry_run: bool = False
    enabled: bool = True
    description: str = ""


CAPABILITIES: dict[str, Capability] = {
    "check": Capability("check", description="Environment self-check"),
    "status": Capability("status", description="Wiki overview"),
    "lint": Capability("lint", description="Wiki health check"),
    "link": Capability("link", description="Relation discovery"),
    "query": Capability("query", description="Semantic query"),
    "relink": Capability(
        "relink",
        write_scope=("wiki/",),
        dry_run=True,
        description="Batch relation discovery and page backlink updates",
    ),
    "merge": Capability(
        "merge",
        write_scope=("wiki/",),
        dry_run=True,
        description="Safe single-page content merge",
    ),
    "index": Capability(
        "index",
        write_scope=("wiki/.cache/",),
        description="Build/update embedding index cache",
    ),
    "hot": Capability("hot", description="Bounded recent-activity context"),
    "apply-bundle": Capability(
        "apply-bundle",
        write_scope=("wiki/", "log.md"),
        dry_run=True,
        description="Atomic multi-file transaction bundle",
    ),
    "zotero-plan": Capability(
        "zotero-plan",
        write_scope=("temp/",),
        description="Read-only Zotero sync planner; manifest only under temp/",
    ),
    "zotero-local-auth": Capability(
        "zotero-local-auth",
        write_scope=("var/",),
        network=True,
        description="Authorize direct Zotero 10 local API writes",
    ),
    "zotero-refresh": Capability(
        "zotero-refresh",
        write_scope=("var/", "temp/"),
        network=True,
        description="Zotero metadata enrichment via MCP and external providers",
    ),
    "zotero-writeback": Capability(
        "zotero-writeback",
        write_scope=("temp/",),
        network=True,
        description="Restricted local Zotero managed-tag and reviewed-relation write-back",
    ),
    "zotero-relocate": Capability(
        "zotero-relocate",
        write_scope=("temp/", "sources/zotero/"),
        network=True,
        dry_run=True,
        description="Controlled Zotero attachment relocation with verified local metadata updates",
    ),
    "zotero-ingest-verify": Capability(
        "zotero-ingest-verify",
        write_scope=("temp/",),
        description="Collection ingest allocation, provenance, and page verification",
    ),
    "zotero-heal": Capability(
        "zotero-heal",
        write_scope=("temp/", "wiki/", "log.md"),
        dry_run=True,
        description="Stale Zotero binding detection and in-place frontmatter rebinding",
    ),
    "zotero-alias": Capability(
        "zotero-alias",
        description="Render a sanitized sources/zotero alias from a wildcard template",
    ),
    "init": Capability(
        "init",
        description="Scaffold a new knowledge-base directory",
    ),
    "ingest": Capability(
        "ingest",
        description="Guidance for source material ingestion",
    ),
}


def get_capability(command: str, config: dict[str, Any] | None = None) -> Capability:
    """解析命令的有效契约:默认声明 + config 收紧覆盖。"""
    overrides = (config or {}).get("capabilities", {})
    for name in overrides:
        if name not in CAPABILITIES:
            raise CapabilityError(f"unknown command in capabilities config: {name}")

    if command not in CAPABILITIES:
        raise CapabilityError(f"unknown command: {command}")

    cap = CAPABILITIES[command]
    override = overrides.get(command)
    if not override:
        return cap

    if override.get("enabled") is False:
        cap = replace(cap, enabled=False)

    if "write_scope" in override:
        narrowed = tuple(str(p) for p in override["write_scope"])
        for entry in narrowed:
            if not _covered_by(entry, cap.write_scope):
                raise CapabilityError(
                    f"capabilities.{command}.write_scope may only narrow the default "
                    f"{cap.write_scope}; `{entry}` would widen it"
                )
        cap = replace(cap, write_scope=narrowed)

    return cap


def check_enabled(command: str, config: dict[str, Any] | None = None) -> None:
    cap = get_capability(command, config)
    if not cap.enabled:
        raise CapabilityError(f"Command `{command}` is disabled by capabilities config")


def check_write_paths(
    command: str,
    paths,
    config: dict[str, Any] | None = None,
) -> None:
    """要求所有写入路径都落在命令的 write_scope 内,否则 fail closed。"""
    cap = get_capability(command, config)
    check_enabled(command, config)
    for raw in paths:
        rel = Path(raw).as_posix()
        if not _covered_by(rel, cap.write_scope):
            raise CapabilityError(
                f"Path `{rel}` is outside `{command}` write_scope "
                f"{cap.write_scope or '(read-only command)'}"
            )
    if paths:
        LOG.debug(
            "write paths within scope for %s: %s", command, [str(p) for p in paths]
        )


def _covered_by(path: str, prefixes: tuple[str, ...]) -> bool:
    """path 是否等于某个前缀文件,或位于某个前缀目录下。"""
    for prefix in prefixes:
        prefix = prefix.rstrip("/")
        if path == prefix or path.startswith(prefix + "/"):
            return True
    return False
