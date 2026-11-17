from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from dirstat_skill.models import AnalysisFinding, NormalizedNode
from dirstat_skill.risk import classify_path


ANALYSIS_SECTIONS: list[tuple[str, str, str]] = [
    ("Dominant Space", "dominant space", "Shows the paths that explain most space under the configured dominant-space threshold."),
    ("Path Safety", "path safety", "Shows paths whose location changes their risk posture even before deeper inspection."),
    ("Nearby References", "nearby references", "Shows paths with local evidence pointing to nearby configs, manifests, or workflow references."),
    ("Signature Heuristics", "signature heuristics", "Shows paths matched by obvious signatures such as cache, temp, trash, or incomplete-download patterns."),
    ("Probable Duplicates", "probable duplicates", "Shows large assets that look duplicated by basename, size, and extension across different directories."),
    ("Protected Huge Hotspots", "protected huge hotspots", "Shows very large protected areas that matter for visibility but should stay handled carefully."),
]
LARGE_ASSET_EXTENSIONS = {".gguf", ".safetensors", ".ckpt", ".bin", ".pth", ".pt", ".onnx"}


@dataclass(frozen=True)
class TopLists:
    top_dirs: list[NormalizedNode]
    top_files: list[NormalizedNode]


def build_top_lists(nodes: list[NormalizedNode], min_bytes: int, top_n: int) -> TopLists:
    dirs = [node for node in nodes if node.is_dir and node.dsize >= min_bytes]
    files = [node for node in nodes if not node.is_dir and node.dsize >= min_bytes]
    top_dirs = sorted(dirs, key=lambda node: node.dsize, reverse=True)[:top_n]
    top_files = sorted(files, key=lambda node: node.dsize, reverse=True)[:top_n]
    return TopLists(top_dirs=top_dirs, top_files=top_files)


def select_dominant_candidates(
    nodes: list[NormalizedNode],
    root_path: str,
    dominant_percent: float,
    min_candidate_bytes: int,
) -> list[NormalizedNode]:
    node_by_key = {_path_key(node.path): node for node in nodes}
    children_by_parent = _build_children_index(nodes)
    root = node_by_key[_path_key(root_path)]
    selected = _select_from_node(
        node=root,
        children_by_parent=children_by_parent,
        dominant_percent=dominant_percent,
        min_candidate_bytes=min_candidate_bytes,
    )
    return _dedupe_nodes(selected)


def select_dominant_candidates_for_roots(
    nodes: list[NormalizedNode],
    dominant_percent: float,
    min_candidate_bytes: int,
) -> list[NormalizedNode]:
    children_by_parent = _build_children_index(nodes)
    node_keys = {_path_key(node.path) for node in nodes}
    roots = [node for node in nodes if _parent_key(node.path) not in node_keys]
    selected: list[NormalizedNode] = []
    for root in sorted(roots, key=lambda node: node.dsize, reverse=True):
        selected.extend(
            _select_from_node(
                node=root,
                children_by_parent=children_by_parent,
                dominant_percent=dominant_percent,
                min_candidate_bytes=min_candidate_bytes,
            )
        )
    return _dedupe_nodes(selected)


def build_analysis_findings(
    selected_nodes: list[NormalizedNode],
    all_nodes: list[NormalizedNode],
    protected_prefixes: list[str],
    inspection_prefixes: list[str],
    nearby_reference_extensions: list[str],
    max_nearby_reference_files: int,
    dominant_percent: float,
    min_candidate_bytes: int,
) -> list[AnalysisFinding]:
    findings: list[AnalysisFinding] = []
    for node in selected_nodes:
        findings.append(
            _build_primary_finding(
                node=node,
                protected_prefixes=protected_prefixes,
                inspection_prefixes=inspection_prefixes,
                nearby_reference_extensions=nearby_reference_extensions,
                max_nearby_reference_files=max_nearby_reference_files,
                dominant_percent=dominant_percent,
            )
        )
    findings.extend(
        _build_probable_duplicate_findings(
            nodes=all_nodes,
            protected_prefixes=protected_prefixes,
            dominant_percent=dominant_percent,
            min_candidate_bytes=min_candidate_bytes,
        )
    )
    findings.extend(
        _build_protected_hotspot_findings(
            nodes=all_nodes,
            protected_prefixes=protected_prefixes,
            dominant_percent=dominant_percent,
            min_candidate_bytes=min_candidate_bytes,
        )
    )
    return _dedupe_findings(findings)


def render_review_report(root_path: str, findings: list[AnalysisFinding]) -> str:
    configured_dominant_percent = findings[0].configured_dominant_percent if findings else 0.0
    lines = [
        "# Review Report",
        "",
        "> READ-ONLY ANALYSIS ONLY",
        "> DirStat_Skill never changes files automatically. It only explains what a human should review.",
        "",
        f"- root: `{root_path}`",
        f"- total_findings: {len(findings)}",
        f"- configured_dominant_percent: `{configured_dominant_percent}`",
        "",
        "## How To Read This",
        "",
        "- Start from `dominant space` to see where the volume is concentrated.",
        "- Use `path safety` and `protected huge hotspots` to understand sensitive areas.",
        "- Treat `probable duplicates` as a strong suspicion, not as byte-level proof.",
        "- Treat `nearby references` as contextual evidence, not as certainty of active use.",
        "",
    ]
    for title, analysis_kind, explanation in ANALYSIS_SECTIONS:
        lines.append(f"## {title}")
        lines.append("")
        lines.append(explanation)
        lines.append("")
        section_findings = [item for item in findings if item.analysis_kind == analysis_kind]
        if not section_findings:
            lines.append("- none")
            lines.append("")
            continue
        for finding in section_findings:
            lines.append(f"### `{finding.path}`")
            lines.append("")
            lines.append(f"- size_bytes: `{finding.dsize}`")
            lines.append(f"- size_human: `{_human_size(finding.dsize)}`")
            lines.append(f"- attention_level: `{finding.attention_level}`")
            lines.append(f"- review_reason: {finding.review_reason}")
            lines.append(f"- evidence: {finding.evidence}")
            lines.append(f"- confidence: `{finding.dependency_check_confidence}`")
            if finding.group_key:
                lines.append(f"- group_key: `{finding.group_key}`")
            lines.append(f"- selection_source: `{finding.selection_source}`")
            lines.append("")
    lines.extend(
        [
            "## Limits",
            "",
            "- `probable duplicates` uses fast structural signals by default, not full-content hashing.",
            "- `protected huge hotspots` are visibility findings, not an invitation to act blindly.",
            "- low-confidence findings still need human judgment.",
            "",
        ]
    )
    return "\n".join(lines)


def write_review_candidates_csv(
    output_path: Path,
    findings: list[AnalysisFinding],
) -> None:
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "path",
                "dsize",
                "is_dir",
                "analysis_kind",
                "attention_level",
                "review_reason",
                "evidence",
                "dependency_check_confidence",
                "selection_source",
                "group_key",
                "configured_dominant_percent",
            ],
        )
        writer.writeheader()
        for finding in findings:
            writer.writerow(finding.__dict__)


def _build_children_index(nodes: list[NormalizedNode]) -> dict[str | None, list[NormalizedNode]]:
    children_by_parent: dict[str | None, list[NormalizedNode]] = {}
    for node in nodes:
        children_by_parent.setdefault(_parent_key(node.path), []).append(node)
    return children_by_parent


def _select_from_node(
    node: NormalizedNode,
    children_by_parent: dict[str | None, list[NormalizedNode]],
    dominant_percent: float,
    min_candidate_bytes: int,
) -> list[NormalizedNode]:
    if not node.is_dir or node.dsize < min_candidate_bytes:
        return [node]
    children = [
        child
        for child in sorted(
            children_by_parent.get(_path_key(node.path), []),
            key=lambda item: item.dsize,
            reverse=True,
        )
        if child.dsize >= min_candidate_bytes
    ]
    if not children:
        return [node]
    total_child_size = sum(child.dsize for child in children)
    if total_child_size <= 0:
        return [node]
    selected_children: list[NormalizedNode] = []
    cumulative = 0
    for child in children:
        selected_children.append(child)
        cumulative += child.dsize
        if cumulative / total_child_size >= dominant_percent:
            break
    if (
        len(selected_children) == len(children)
        and len(children) > 1
        and all(child.is_dir for child in children)
    ):
        return [node]
    selected: list[NormalizedNode] = []
    for child in selected_children:
        if child.is_dir:
            selected.extend(
                _select_from_node(
                    node=child,
                    children_by_parent=children_by_parent,
                    dominant_percent=dominant_percent,
                    min_candidate_bytes=min_candidate_bytes,
                )
            )
        else:
            selected.append(child)
    return selected or [node]


def _build_primary_finding(
    node: NormalizedNode,
    protected_prefixes: list[str],
    inspection_prefixes: list[str],
    nearby_reference_extensions: list[str],
    max_nearby_reference_files: int,
    dominant_percent: float,
) -> AnalysisFinding:
    attention_level = classify_path(
        node.path,
        protected_prefixes,
        inspection_prefixes,
    )
    nearby_refs = _find_nearby_references(
        node.path,
        nearby_reference_extensions=nearby_reference_extensions,
        max_nearby_reference_files=max_nearby_reference_files,
    )
    analysis_kind = _primary_analysis_kind(
        path=node.path,
        attention_level=attention_level,
        nearby_refs=nearby_refs,
    )
    review_reason = _review_reason(node=node, attention_level=attention_level, analysis_kind=analysis_kind)
    evidence, confidence = _evidence_and_confidence(
        node=node,
        attention_level=attention_level,
        nearby_refs=nearby_refs,
    )
    return AnalysisFinding(
        path=node.path,
        dsize=node.dsize,
        is_dir=node.is_dir,
        analysis_kind=analysis_kind,
        attention_level=attention_level,
        review_reason=review_reason,
        evidence=evidence,
        dependency_check_confidence=confidence,
        selection_source="dominant_subtree" if node.is_dir else "dominant_leaf",
        group_key="",
        configured_dominant_percent=dominant_percent,
    )


def _build_probable_duplicate_findings(
    nodes: list[NormalizedNode],
    protected_prefixes: list[str],
    dominant_percent: float,
    min_candidate_bytes: int,
) -> list[AnalysisFinding]:
    groups: dict[tuple[str, int, str], list[NormalizedNode]] = {}
    for node in nodes:
        if node.is_dir or node.dsize < min_candidate_bytes:
            continue
        suffix = Path(node.name).suffix.lower()
        if suffix not in LARGE_ASSET_EXTENSIONS:
            continue
        if _matched_protected_prefix(node.path, protected_prefixes):
            continue
        groups.setdefault((node.name.lower(), node.dsize, suffix), []).append(node)

    findings: list[AnalysisFinding] = []
    for (name, dsize, _suffix), group in groups.items():
        directories = {str(Path(node.path).parent).lower() for node in group}
        if len(group) < 2 or len(directories) < 2:
            continue
        group_key = f"duplicate:{name}:{dsize}"
        evidence = f"same basename and same size across {len(group)} directories"
        for node in sorted(group, key=lambda item: item.path.lower()):
            findings.append(
                AnalysisFinding(
                    path=node.path,
                    dsize=node.dsize,
                    is_dir=node.is_dir,
                    analysis_kind="probable duplicates",
                    attention_level="review carefully",
                    review_reason="large asset appears structurally duplicated across different directories",
                    evidence=evidence,
                    dependency_check_confidence="medium",
                    selection_source="duplicate_cluster",
                    group_key=group_key,
                    configured_dominant_percent=dominant_percent,
                )
            )
    return findings


def _build_protected_hotspot_findings(
    nodes: list[NormalizedNode],
    protected_prefixes: list[str],
    dominant_percent: float,
    min_candidate_bytes: int,
) -> list[AnalysisFinding]:
    protected_nodes = [
        node
        for node in nodes
        if node.dsize >= min_candidate_bytes and _matched_protected_prefix(node.path, protected_prefixes)
    ]
    findings: list[AnalysisFinding] = []
    for node in sorted(protected_nodes, key=lambda item: item.dsize, reverse=True)[:10]:
        matched_prefix = _matched_protected_prefix(node.path, protected_prefixes) or "protected"
        findings.append(
            AnalysisFinding(
                path=node.path,
                dsize=node.dsize,
                is_dir=node.is_dir,
                analysis_kind="protected huge hotspots",
                attention_level="keep protected",
                review_reason="protected runtime-owned area contributes significant space and should be understood explicitly",
                evidence=f"matched protected prefix `{matched_prefix}` with `{_human_size(node.dsize)}`",
                dependency_check_confidence="high",
                selection_source="protected_hotspot",
                group_key=f"hotspot:{matched_prefix}",
                configured_dominant_percent=dominant_percent,
            )
        )
    return findings


def _review_reason(node: NormalizedNode, attention_level: str, analysis_kind: str) -> str:
    normalized = _path_key(node.path)
    if normalized.endswith((".filepart", ".part", ".partial")):
        return "incomplete download pattern surfaced by the dominant-space walk"
    if _has_cache_temp_trash_signature(normalized):
        return "cache, temp, or trash path surfaced by the dominant-space walk"
    if analysis_kind == "nearby references":
        return "path surfaced with nearby contextual references worth reading before drawing conclusions"
    if attention_level == "keep protected":
        return "protected system or runtime-owned path that should be interpreted carefully"
    if normalized.endswith((".gguf", ".safetensors", ".ckpt", ".bin", ".pth")):
        return "user-owned model asset surfaced by the dominant-space walk"
    if node.is_dir:
        return "directory dominates parent space under the dominant-space walk"
    return "file surfaced by the dominant-space walk"


def _primary_analysis_kind(
    path: str,
    attention_level: str,
    nearby_refs: list[str],
) -> str:
    normalized = _path_key(path)
    if _is_signature_path(normalized):
        return "signature heuristics"
    if nearby_refs:
        return "nearby references"
    if attention_level == "keep protected":
        return "path safety"
    return "dominant space"


def _evidence_and_confidence(
    node: NormalizedNode,
    attention_level: str,
    nearby_refs: list[str],
) -> tuple[str, str]:
    normalized = _path_key(node.path)
    if attention_level == "keep protected":
        return "matched protected path prefix", "high"
    if _has_cache_temp_trash_signature(normalized):
        return "matched cache or temp path signature", "high"
    if normalized.endswith((".filepart", ".part", ".partial")):
        return "matched partial-download suffix", "high"
    if nearby_refs:
        return f"nearby references found in {', '.join(nearby_refs)}", "medium"
    if Path(node.name).suffix.lower() in LARGE_ASSET_EXTENSIONS:
        return "selected by dominant-space walk among large user-owned assets", "low"
    return "selected by dominant-space walk with no nearby references found", "low"


def _find_nearby_references(
    path: str,
    nearby_reference_extensions: list[str],
    max_nearby_reference_files: int,
) -> list[str]:
    candidate_path = Path(path)
    try:
        exists = candidate_path.exists()
    except OSError:
        return []
    if not exists:
        return []
    search_dirs: list[Path] = []
    try:
        current = candidate_path if candidate_path.is_dir() else candidate_path.parent
    except OSError:
        return []
    for _ in range(3):
        if current in search_dirs:
            break
        search_dirs.append(current)
        if current.parent == current:
            break
        current = current.parent
    basename = candidate_path.name.lower()
    matches: list[str] = []
    for directory in search_dirs:
        try:
            entries = sorted(directory.iterdir(), key=lambda item: item.name.lower())
        except OSError:
            continue
        for entry in entries:
            try:
                is_file = entry.is_file()
            except OSError:
                continue
            if not is_file:
                continue
            if entry.suffix.lower() not in nearby_reference_extensions:
                continue
            try:
                content = entry.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if basename in content.lower():
                matches.append(entry.name)
            if len(matches) >= max_nearby_reference_files:
                return matches
    return matches


def _is_signature_path(normalized: str) -> bool:
    return normalized.endswith((".filepart", ".part", ".partial", ".tmp", ".cache")) or _has_cache_temp_trash_signature(
        normalized
    )


def _has_cache_temp_trash_signature(normalized: str) -> bool:
    if any(fragment in normalized for fragment in ("/appdata/local/temp", "/tmp", "/var/tmp")):
        return True
    segments = [segment for segment in normalized.split("/") if segment]
    return any(
        segment in {"trash", ".trash", ".cache"}
        or segment.endswith("_cache")
        for segment in segments
    )


def _matched_protected_prefix(path: str, protected_prefixes: list[str]) -> str | None:
    normalized_path = _path_key(path)
    for prefix in protected_prefixes:
        normalized_prefix = _path_key(prefix)
        if normalized_path == normalized_prefix or normalized_path.startswith(f"{normalized_prefix}/"):
            return prefix
    return None


def _path_key(path: str) -> str:
    normalized = path.replace("\\", "/").rstrip("/").lower()
    if not normalized and path.startswith("/"):
        return "/"
    return normalized


def _parent_key(path: str) -> str | None:
    normalized = _path_key(path)
    if not normalized:
        return None
    if normalized == "/":
        return None
    if len(normalized) == 2 and normalized[1] == ":":
        return None
    if normalized.startswith("/") and normalized.count("/") == 1:
        return "/"
    parent = normalized.rsplit("/", 1)[0] if "/" in normalized else ""
    if not parent:
        return None
    return parent


def _dedupe_nodes(nodes: list[NormalizedNode]) -> list[NormalizedNode]:
    deduped: list[NormalizedNode] = []
    seen: set[str] = set()
    for node in nodes:
        key = _path_key(node.path)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(node)
    return deduped


def _dedupe_findings(findings: list[AnalysisFinding]) -> list[AnalysisFinding]:
    deduped: list[AnalysisFinding] = []
    seen: set[tuple[str, str, str]] = set()
    for finding in findings:
        key = (finding.analysis_kind, _path_key(finding.path), finding.group_key)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(finding)
    return deduped


def _human_size(size_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = float(size_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size_bytes} B"

