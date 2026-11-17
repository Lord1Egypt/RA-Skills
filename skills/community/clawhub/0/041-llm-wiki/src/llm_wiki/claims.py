"""
论断(claim)级溯源校验

页面 frontmatter 可声明 claims 列表,把"页面说了什么"与"依据哪个来源"
绑定到论断粒度:

    claims:
      - text: "LoRA 将权重更新约束为低秩乘积"
        source: "sources/lora.pdf"     # 必须在本页 sources / sources_meta 中声明
        status: "accepted"             # accepted | provisional | contested | unsupported

校验规则(全部 advisory,不改变 lint 退出行为):
1. 每条 claim 必须有 text/source/status 三个字段
2. status 必须在词表内
3. source 必须是本页已声明的来源(sources 条目或 sources_meta 的
   title/source_alias/citation_key),防止引用未声明材料。
   注意:不检查文件是否存在于本地——sources/ 由用户管理且不入库,
   在克隆/CI 环境中缺失是正常状态,不是页面缺陷。
4. mature/evergreen 页面仍有 contested/unsupported 论断时给出提示
   ——"内容完整"的声明与未决论断矛盾
"""

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .agent_logger import get_logger

LOG = get_logger("claims")

CLAIM_STATUSES = ("accepted", "provisional", "contested", "unsupported")
_UNSETTLED = ("contested", "unsupported")
_MATURE = ("mature", "evergreen")


def _declared_sources(frontmatter: Mapping[str, Any]) -> set:
    """页面已声明的来源:sources 条目 + sources_meta 的 title/source_alias/citation_key。"""
    declared = {str(s) for s in frontmatter.get("sources", []) or []}
    for meta in frontmatter.get("sources_meta", []) or []:
        if isinstance(meta, dict):
            for key in ("title", "source_alias", "citation_key"):
                if meta.get(key):
                    declared.add(str(meta[key]))
    return declared


def validate_claims(page, project_root: Path | None = None) -> list[str]:
    """校验单个页面的 claims,返回问题描述列表(空列表 = 通过)。

    project_root 保留用于与未来需要本地文件系统的校验兼容。
    """
    frontmatter = page.frontmatter
    claims = frontmatter.get("claims")
    if claims is None:
        return []
    if not isinstance(claims, list):
        return [f"{page.title}: claims must be a list"]

    declared = _declared_sources(frontmatter)
    issues: list[str] = []

    for i, claim in enumerate(claims):
        label = f"{page.title} claim[{i}]"
        if not isinstance(claim, dict):
            issues.append(f"{label}: must be a mapping")
            continue

        missing = [k for k in ("text", "source", "status") if not claim.get(k)]
        if missing:
            issues.append(f"{label}: missing {', '.join(missing)}")
            continue

        status = str(claim["status"])
        if status not in CLAIM_STATUSES:
            issues.append(
                f"{label}: invalid status {status!r} (expected one of {', '.join(CLAIM_STATUSES)})"
            )

        source = str(claim["source"])
        if source not in declared:
            issues.append(f"{label}: cites undeclared source `{source}`")

    if not issues and claims:
        page_status = str(frontmatter.get("status", "draft"))
        unsettled = [c for c in claims if str(c.get("status")) in _UNSETTLED]
        if page_status in _MATURE and unsettled:
            issues.append(
                f"{page.title}: status={page_status} but {len(unsettled)} claim(s) "
                f"still contested/unsupported"
            )

    if issues:
        LOG.debug("claim issues on %s: %d", page.title, len(issues))
    return issues
