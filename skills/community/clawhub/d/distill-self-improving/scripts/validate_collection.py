#!/usr/bin/env python3
"""只读校验 self-improving collection 的机器结构契约。"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import shutil
import stat
import sys
import tempfile
import unicodedata
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


CONTRACT_VERSION = "3"
GATE_ORDER = {"G1": 1, "G2": 2, "G3": 3, "G4": 4, "G5": 5, "G7": 7, "Q2": 8}
INVENTORY_HEADERS = ("path", "type", "size", "mtime", "status")
MANIFEST_HEADERS = (
    "path",
    "indexed",
    "read",
    "distilled",
    "skipped",
    "reason",
    "output_ids",
    "last_verified",
)
SCOPE_HEADERS = ("path", "group")
INVENTORY_STATUSES = ("exists", "missing", "unreadable", "restricted", "needs-review")
BOOLEAN_VALUES = ("true", "false")
PRIMARY_PREFIX = "distillation-file:"
GROUP_PATTERN = r"[a-z0-9]+(?:-[a-z0-9]+)*"
RESULT_NAME_PATTERN = rf"d-([0-9a-f]{{12}})-({GROUP_PATTERN})\.md"
DISTILLATION_METADATA = (
    "distillation_id",
    "source",
    "group",
    "file_type",
    "document_time",
    "evidence_time",
)
DISTILLATION_SECTIONS = (
    "一句话",
    "关键要点",
    "版本关系 / 不确定性",
    "证据 / 现场复核边界",
)
SUMMARY_SECTION_ALIASES = (
    ("项目 / 主题速览",),
    ("跨文件核心事实 / 技术结论", "跨文档核心事实 / 技术结论"),
    ("文档版本 / 主题脉络",),
    ("单文件蒸馏导航",),
    ("限制与需现场复核",),
)
TEMPLATE_MARKER_RE = re.compile(r"<[^>\r\n]{1,120}>")
SUMMARY_LINK_RE = re.compile(r"\[[^\]]+\]\((\.\./distillations/[^)]+\.md)\)")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")


ERRORS: dict[str, tuple[str, str]] = {
    "E_SCOPE_MISSING": ("G1", "从 G1 重新生成 scope.csv；不要从结果目录反推范围。"),
    "E_SCOPE_HEADER": ("G1", "按 describe 输出和 scope 模板重建表头。"),
    "E_SCOPE_DUPLICATE": ("G1", "按精确 path 去重并重新冻结范围。"),
    "E_SOURCE_PATH_INVALID": ("G1", "把 scope.path 修正为已确认原文件的绝对路径后重新冻结范围。"),
    "E_GROUP_INVALID": ("G1", "使用稳定的小写字母、数字和连字符 group。"),
    "E_INVENTORY_MISSING": ("G2", "从已冻结 scope 重建 inventory.csv。"),
    "E_INVENTORY_HEADER": ("G2", "按 describe 输出重建 inventory 表头。"),
    "E_INVENTORY_DUPLICATE": ("G2", "按精确 path 去重 inventory。"),
    "E_MANIFEST_MISSING": ("G2", "从已冻结 scope 重建 manifest.csv。"),
    "E_MANIFEST_HEADER": ("G2", "按 describe 输出重建 manifest 表头。"),
    "E_MANIFEST_DUPLICATE": ("G2", "按精确 path 去重 manifest。"),
    "E_SCOPE_INVENTORY_DIFF": ("G2", "以 scope 为上游声明修正 inventory 集合。"),
    "E_SCOPE_MANIFEST_DIFF": ("G2", "以 scope 为上游声明修正 manifest 集合。"),
    "E_CSV_ROW": ("G2", "修正缺列、多列或空 path 的 CSV 行。"),
    "E_FIELD_REQUIRED": ("G2", "由负责当前字段的 Gate 写入非空值后重验。"),
    "E_STATUS_INVALID": ("G2", "只使用 describe 输出的 inventory status。"),
    "E_BOOLEAN_INVALID": ("G2", "只使用小写 true 或 false。"),
    "E_INDEXED_FALSE": ("G2", "manifest 中已物化的每行都必须由 G2 写 indexed=true。"),
    "E_SIZE_INVALID": ("G2", "写入非负十进制文件字节数。"),
    "E_SIZE_MISMATCH": ("G2", "以当前原文件实际字节数修正 inventory.size 后重验。"),
    "E_MTIME_INVALID": ("G2", "写入可解析的 ISO-8601 mtime。"),
    "E_LAST_VERIFIED": ("G2", "写入合法 YYYY-MM-DD 日期。"),
    "E_SOURCE_STATUS_MISMATCH": ("G2", "回查原路径并修正 status 或现场元数据。"),
    "E_SOURCE_NOT_FILE": ("G2", "确认 scope 仅含原文件；目录另走受控范围导航。"),
    "E_REASON_REQUIRED": ("G3", "为 read=false 或 skipped=true 的行写具体 reason。"),
    "E_STATE_INVALID": ("G3", "修正 read/distilled/skipped 的互斥和依赖关系。"),
    "E_G3_INCOMPLETE": ("G3", "重读或重提取原文件；临时故障保持未完成，不得伪装成 skip。"),
    "E_G4_INCOMPLETE": ("G4", "逐文件完成独立蒸馏或合法 skip，再运行批次校验。"),
    "E_OUTPUT_PRIMARY_COUNT": ("G4", "每个 distilled 行只保留一个 distillation-file 主输出。"),
    "E_OUTPUT_PATH_UNSAFE": ("G4", "使用 collection/distillations/<group>/<file>.md 内的相对主输出。"),
    "E_OUTPUT_MISSING": ("G4", "从原文件或未改写的已核验证词重新生成派生结果；不要修改证词。"),
    "E_OUTPUT_REUSED": ("G4", "为每个精确 source 生成独立主输出。"),
    "E_ORPHAN_OUTPUT": ("G4", "回到 scope/manifest 核对孤儿来源；没有删除授权时不要擅自删除。"),
    "E_REPARSE_POINT": ("G4", "停止跟随链接，改用范围内 regular 文件并重验。"),
    "E_DISTILLATION_METADATA": ("G4", "按单文件模板补齐结构字段后从原文件重新核验。"),
    "E_DISTILLATION_SOURCE_MISMATCH": ("G4", "回到 G1-G3 核实精确 path；不要改写原始读取或提取证词。"),
    "E_DISTILLATION_GROUP_MISMATCH": ("G4", "以 scope.csv 的 group 修正派生结果和输出路径。"),
    "E_DISTILLATION_ID_MISMATCH": ("G4", "让 distillation_id 与稳定文件名 stem 一致。"),
    "E_DISTILLATION_FILENAME": ("G4", "按 d-<path-hash12>-<ascii-slug>.md 命名。"),
    "E_DISTILLATION_HASH": ("G4", "按 describe 的精确 source 规范化与 SHA-256 规则重命名。"),
    "E_DISTILLATION_HASH_VERSION": ("G4", "正常模式必须使用 portable-v1；只有显式只读 legacy 模式允许既有结果缺字段。"),
    "E_DISTILLATION_SECTION": ("G4", "按单文件模板补齐必需章节。"),
    "E_DISTILLATION_SENTENCE": ("G4", "从原文件重新形成非模板、非路径复述的一句话；结构通过不代表事实正确。"),
    "E_DISTILLATION_POINTS": ("G4", "从原文件重新形成至少两个非模板要点；不要修改提取证词。"),
    "E_TEMPLATE_MARKER": ("G4", "用实际派生内容替换模板标记并重新读回原文件。"),
    "E_SUMMARY_MISSING": ("G5", "仅在显式要求时，为至少含两个独立结果的 group 建立项目/主题综合。"),
    "E_SUMMARY_SECTION": ("G5", "按项目/主题综合模板补齐必需章节。"),
    "E_SUMMARY_GROUP": ("G5", "让 summary 的 group 精确匹配 scope.csv。"),
    "E_SUMMARY_DUPLICATE_GROUP": ("G5", "每个 group 只保留一份权威 summary。"),
    "E_SUMMARY_LINK_MISSING": ("G5", "补齐本组所有独立结果链接；不能用综合正文替代。"),
    "E_SUMMARY_LINK_EXTRA": ("G5", "移除跨组或非 manifest 主输出链接。"),
    "E_SUMMARY_LINK_DUPLICATE": ("G5", "同一 summary 中每个结果只链接一次。"),
    "E_SUMMARY_INLINE_BODY": ("G5", "summary 只保留跨文件综合和链接，不内嵌单文件正文。"),
    "E_COLLECTION_README_MISSING": ("G7", "补齐 collection README 契约入口后重跑最终回归。"),
    "E_ENCODING": ("G7", "将派生文本转为严格 UTF-8 后重验；不要改写原始证词。"),
    "E_BOM": ("G7", "移除派生文本的 UTF-8 BOM。"),
    "E_TRAILING_WHITESPACE": ("G7", "移除派生文本行尾空白。"),
    "E_SOURCE_QUERY_MISSING": ("Q2", "报告目标未命中并回退只读原文件，不扫描其他范围。"),
}

LIMITATIONS = (
    "PASS 只证明机器结构与映射，不证明原文件支持正文结论。",
    "脚本只能拒绝模板标记、缺段和过短文本，不能判断事实真伪或业务价值。",
    "脚本不证明 skip 的语义理由永久有效，也不证明敏感信息已被完全清除。",
    "内容 identity 可比性需要调用方另行记录原文件哈希、读取工具和运行条件。",
    "默认 G5 只校验已存在 summary；只有显式 require-summary 才要求多结果组建立综合。",
)


@dataclass(frozen=True)
class Failure:
    gate: str
    code: str
    path: str
    expected: Any
    actual: Any
    remediation: str


class UsageOrReadError(Exception):
    pass


class Validator:
    def __init__(
        self,
        collection: Path,
        scope_path: Path,
        gate: str,
        source: str | None,
        legacy_read_only: bool = False,
        require_summary: bool = False,
    ):
        self.collection = collection
        self.scope_path = scope_path
        self.gate = gate
        self.source = source
        self.legacy_read_only = legacy_read_only
        self.require_summary = require_summary
        self.legacy_scope_used = False
        self.failures: list[Failure] = []
        self._failure_keys: set[str] = set()
        self.counts: dict[str, int] = {}

    def fail(
        self,
        code: str,
        path: str | Path,
        expected: Any,
        actual: Any,
        gate_override: str | None = None,
    ) -> None:
        gate, remediation = ERRORS[code]
        gate = gate_override or gate
        item = Failure(gate, code, str(path), expected, actual, remediation)
        key = json.dumps(asdict(item), ensure_ascii=False, sort_keys=True, default=str)
        if key not in self._failure_keys:
            self._failure_keys.add(key)
            self.failures.append(item)

    def check(self) -> dict[str, Any]:
        self._validate_collection_root()
        inventory = self._load_inventory()
        manifest = self._load_manifest()
        scopes = self._load_scope(manifest)
        self.counts.update(scope=len(scopes), inventory=len(inventory), manifest=len(manifest))

        if self.source is not None:
            self._check_source_query(scopes, inventory, manifest)
            return self._report("source")

        self._check_sets(scopes, inventory, manifest)
        self._check_inventory(inventory)
        manifest_state = self._check_manifest(manifest)
        if self._gate_at_least("G3"):
            self._check_g3(manifest_state)
        outputs: dict[str, str] = {}
        if self._gate_at_least("G4"):
            outputs = self._check_g4(scopes, manifest, manifest_state)
        if self._gate_at_least("G5"):
            self._check_g5(scopes, outputs)
        if self._gate_at_least("G7"):
            read_text_required(
                self.collection / "README.md",
                "E_COLLECTION_README_MISSING",
                self.fail,
            )
        return self._report("collection")

    def _report(self, mode: str) -> dict[str, Any]:
        ordered = sorted(
            self.failures,
            key=lambda x: (
                GATE_ORDER.get(x.gate, 99),
                x.code,
                x.path.casefold(),
                json.dumps(x.actual, ensure_ascii=False, sort_keys=True, default=str),
            ),
        )
        self.counts["failures"] = len(ordered)
        return {
            "contract_version": CONTRACT_VERSION,
            "status": "pass" if not ordered else "fail",
            "mode": mode,
            "gate": "Q2" if mode == "source" else self.gate,
            "counts": dict(sorted(self.counts.items())),
            "failures": [asdict(item) for item in ordered],
            "limitations": list(LIMITATIONS),
        }

    def _gate_at_least(self, value: str) -> bool:
        return GATE_ORDER[self.gate] >= GATE_ORDER[value]

    def _validate_collection_root(self) -> None:
        if not self.collection.exists() or not self.collection.is_dir():
            raise UsageOrReadError(f"collection 不存在或不是目录: {self.collection}")
        if is_reparse(self.collection):
            self.fail("E_REPARSE_POINT", self.collection, "regular directory", "reparse")

    def _load_scope(self, manifest: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
        if not self.scope_path.exists() and self.legacy_read_only:
            self.legacy_scope_used = True
            self.counts["legacy_read_only"] = 1
            rows: dict[str, dict[str, str]] = {}
            for path, row in manifest.items():
                primaries = [item for item in split_output_ids(row.get("output_ids", "")) if item.startswith(PRIMARY_PREFIX)]
                group = "skipped"
                if len(primaries) == 1:
                    rel = primaries[0][len(PRIMARY_PREFIX) :]
                    group = rel.split("/", 1)[0]
                rows[path] = {"path": path, "group": group}
            return rows
        rows = load_csv(
            self.scope_path,
            SCOPE_HEADERS,
            "E_SCOPE_MISSING",
            "E_SCOPE_HEADER",
            "E_SCOPE_DUPLICATE",
            self.fail,
        )
        for path, row in rows.items():
            if not is_absolute_source(path):
                self.fail("E_SOURCE_PATH_INVALID", path, "absolute source path", path)
            group = row.get("group", "")
            if not re.fullmatch(GROUP_PATTERN, group):
                self.fail("E_GROUP_INVALID", path, GROUP_PATTERN, group)
        return rows

    def _load_inventory(self) -> dict[str, dict[str, str]]:
        return load_csv(
            self.collection / "inventory.csv",
            INVENTORY_HEADERS,
            "E_INVENTORY_MISSING",
            "E_INVENTORY_HEADER",
            "E_INVENTORY_DUPLICATE",
            self.fail,
        )

    def _load_manifest(self) -> dict[str, dict[str, str]]:
        return load_csv(
            self.collection / "manifest.csv",
            MANIFEST_HEADERS,
            "E_MANIFEST_MISSING",
            "E_MANIFEST_HEADER",
            "E_MANIFEST_DUPLICATE",
            self.fail,
        )

    def _check_sets(
        self,
        scopes: dict[str, dict[str, str]],
        inventory: dict[str, dict[str, str]],
        manifest: dict[str, dict[str, str]],
    ) -> None:
        scope_set = set(scopes)
        inv_set = set(inventory)
        man_set = set(manifest)
        if scope_set != inv_set:
            self.fail(
                "E_SCOPE_INVENTORY_DIFF",
                self.collection / "inventory.csv",
                sorted(scope_set),
                {"missing": sorted(scope_set - inv_set), "extra": sorted(inv_set - scope_set)},
            )
        if scope_set != man_set:
            self.fail(
                "E_SCOPE_MANIFEST_DIFF",
                self.collection / "manifest.csv",
                sorted(scope_set),
                {"missing": sorted(scope_set - man_set), "extra": sorted(man_set - scope_set)},
            )

    def _check_inventory(self, inventory: dict[str, dict[str, str]]) -> None:
        for path, row in inventory.items():
            if not row.get("type", "").strip():
                self.fail("E_FIELD_REQUIRED", path, "non-empty type", row.get("type", ""))
            size: int | None = None
            try:
                size = int(row.get("size", ""))
                if size < 0:
                    raise ValueError
            except ValueError:
                self.fail("E_SIZE_INVALID", path, "non-negative integer", row.get("size", ""))
            if not parse_iso_datetime(row.get("mtime", "")):
                self.fail("E_MTIME_INVALID", path, "ISO-8601 datetime", row.get("mtime", ""))
            status_value = row.get("status", "")
            if status_value not in INVENTORY_STATUSES:
                self.fail("E_STATUS_INVALID", path, list(INVENTORY_STATUSES), status_value)
                continue
            source_path = Path(path)
            lexists = os.path.lexists(source_path)
            if status_value == "exists" and not lexists:
                self.fail("E_SOURCE_STATUS_MISMATCH", path, "path exists", "missing")
            if status_value == "missing" and lexists:
                self.fail("E_SOURCE_STATUS_MISMATCH", path, "path missing", "exists")
            if lexists:
                bad = first_reparse_component(source_path)
                if bad is not None:
                    self.fail("E_REPARSE_POINT", bad, "regular path", "reparse")
                elif source_path.exists() and not source_path.is_file():
                    self.fail("E_SOURCE_NOT_FILE", path, "regular file", "not-file")
                elif status_value == "exists" and size is not None and source_path.stat().st_size != size:
                    self.fail("E_SIZE_MISMATCH", path, source_path.stat().st_size, size)

    def _check_manifest(
        self,
        manifest: dict[str, dict[str, str]],
        required_gate: str | None = None,
    ) -> dict[str, dict[str, Any]]:
        gate = required_gate or self.gate
        require_g3 = GATE_ORDER[gate] >= GATE_ORDER["G3"]
        require_g4 = GATE_ORDER[gate] >= GATE_ORDER["G4"]
        result: dict[str, dict[str, Any]] = {}
        for path, row in manifest.items():
            parsed: dict[str, Any] = dict(row)
            valid: dict[str, bool] = {}
            for field in ("indexed", "read", "distilled", "skipped"):
                raw = row.get(field, "").strip()
                applicable = field == "indexed" or (field in {"read", "skipped"} and require_g3) or (field == "distilled" and require_g4)
                if not applicable:
                    parsed[field] = None
                    valid[field] = True
                    continue
                if raw not in BOOLEAN_VALUES:
                    field_gate = "G2" if field == "indexed" else "G3" if field in {"read", "skipped"} else "G4"
                    self.fail("E_BOOLEAN_INVALID", path, list(BOOLEAN_VALUES), {field: raw}, field_gate)
                    valid[field] = False
                else:
                    parsed[field] = raw == "true"
                    valid[field] = True
            if valid.get("indexed") and not parsed["indexed"]:
                self.fail("E_INDEXED_FALSE", path, True, False)
            if require_g3 and valid.get("read") and valid.get("skipped") and (
                not parsed["read"] or parsed["skipped"]
            ) and not row.get("reason", "").strip():
                self.fail("E_REASON_REQUIRED", path, "non-empty reason", "")
            if require_g4 and all(valid.get(field) for field in ("read", "distilled", "skipped")) and parsed["distilled"] and (
                not parsed["read"] or parsed["skipped"]
            ):
                self.fail(
                    "E_STATE_INVALID",
                    path,
                    "distilled=true => read=true and skipped=false",
                    {k: parsed[k] for k in ("read", "distilled", "skipped")},
                )
            if require_g4 and valid.get("skipped") and valid.get("distilled") and parsed["skipped"] and parsed["distilled"]:
                self.fail("E_STATE_INVALID", path, "distilled/skipped mutually exclusive", "both true")
            if not valid_date(row.get("last_verified", "")):
                self.fail("E_LAST_VERIFIED", path, "YYYY-MM-DD", row.get("last_verified", ""))
            result[path] = parsed
        self.counts["read"] = sum(1 for row in result.values() if row.get("read") is True)
        self.counts["distilled"] = sum(1 for row in result.values() if row.get("distilled") is True)
        self.counts["skipped"] = sum(1 for row in result.values() if row.get("skipped") is True)
        return result

    def _check_g3(self, manifest_state: dict[str, dict[str, Any]]) -> None:
        for path, row in manifest_state.items():
            if not isinstance(row.get("read"), bool) or not isinstance(row.get("skipped"), bool):
                continue
            if not row["read"] and not row["skipped"]:
                self.fail("E_G3_INCOMPLETE", path, "read=true or legal skipped=true", "unresolved")

    def _check_g4(
        self,
        scopes: dict[str, dict[str, str]],
        manifest: dict[str, dict[str, str]],
        manifest_state: dict[str, dict[str, Any]],
        scan_all: bool = True,
    ) -> dict[str, str]:
        outputs: dict[str, str] = {}
        output_owners: dict[str, list[str]] = {}
        for path, state in manifest_state.items():
            if not isinstance(state.get("distilled"), bool) or not isinstance(state.get("skipped"), bool):
                continue
            if not state["distilled"] and not state["skipped"]:
                self.fail("E_G4_INCOMPLETE", path, "distilled=true or skipped=true", "neither")
            output_ids = split_output_ids(manifest.get(path, {}).get("output_ids", ""))
            primaries = [item for item in output_ids if item.startswith(PRIMARY_PREFIX)]
            if state["distilled"]:
                if len(primaries) != 1:
                    self.fail("E_OUTPUT_PRIMARY_COUNT", path, 1, len(primaries))
                    continue
                primary = primaries[0]
                rel = primary[len(PRIMARY_PREFIX) :]
                safe = safe_output_path(self.collection, rel)
                if safe is None:
                    self.fail("E_OUTPUT_PATH_UNSAFE", path, "<group>/<file>.md", rel)
                    continue
                collection_rel = f"distillations/{rel}"
                output_owners.setdefault(collection_rel, []).append(path)
                outputs[path] = collection_rel
                if not os.path.lexists(safe):
                    self.fail("E_OUTPUT_MISSING", safe, "regular Markdown", "missing")
                    continue
                bad = first_reparse_within(self.collection, safe)
                if bad is not None:
                    self.fail("E_REPARSE_POINT", bad, "regular path", "reparse")
                    continue
                if not safe.is_file():
                    self.fail("E_OUTPUT_MISSING", safe, "regular Markdown", "not-file")
                    continue
                group = scopes.get(path, {}).get("group", "")
                self._check_distillation(safe, path, group)
            elif primaries:
                self.fail("E_OUTPUT_PRIMARY_COUNT", path, 0, len(primaries))

        for rel, owners in output_owners.items():
            if len(owners) > 1:
                self.fail("E_OUTPUT_REUSED", rel, "one source", sorted(owners))

        if scan_all:
            actual_files = set(iter_regular_markdown(self.collection / "distillations", self.fail))
            expected_files = set(outputs.values())
            for rel in sorted(actual_files - expected_files):
                self.fail("E_ORPHAN_OUTPUT", rel, "manifest primary output", "orphan")
            for rel in sorted(expected_files - actual_files):
                self.fail("E_OUTPUT_MISSING", rel, "regular Markdown", "missing")
            self.counts["distillation_files"] = len(actual_files)
        else:
            self.counts["distillation_files"] = len(outputs)
        return outputs

    def _check_distillation(self, path: Path, source: str, group: str) -> None:
        text = read_text_checked(path, self.fail)
        if text is None:
            return
        if TEMPLATE_MARKER_RE.search(text):
            self.fail("E_TEMPLATE_MARKER", path, "no template markers", "marker found")
        metadata = parse_metadata(text)
        for field in DISTILLATION_METADATA:
            if not metadata.get(field, "").strip():
                self.fail("E_DISTILLATION_METADATA", path, f"non-empty {field}", metadata.get(field, ""))
        if metadata.get("source") != f"file:{source}":
            self.fail("E_DISTILLATION_SOURCE_MISMATCH", path, f"file:{source}", metadata.get("source", ""))
        if metadata.get("group") != group:
            self.fail("E_DISTILLATION_GROUP_MISMATCH", path, group, metadata.get("group", ""))
        hash_version = metadata.get("source_hash_version", "").strip()
        if self.legacy_read_only:
            if hash_version not in {"", "portable-v1"}:
                self.fail("E_DISTILLATION_HASH_VERSION", path, "portable-v1 or absent in explicit legacy mode", hash_version)
        elif hash_version != "portable-v1":
            self.fail("E_DISTILLATION_HASH_VERSION", path, "portable-v1", hash_version or "absent")
        match = re.fullmatch(RESULT_NAME_PATTERN, path.name)
        if not match:
            self.fail("E_DISTILLATION_FILENAME", path, RESULT_NAME_PATTERN, path.name)
        else:
            if hash_version == "portable-v1":
                expected_hash = source_hash12(source)
                if match.group(1) != expected_hash:
                    self.fail("E_DISTILLATION_HASH", path, expected_hash, match.group(1))
            if metadata.get("distillation_id") != path.stem:
                self.fail("E_DISTILLATION_ID_MISMATCH", path, path.stem, metadata.get("distillation_id", ""))
        sections = parse_sections(text)
        for section in DISTILLATION_SECTIONS:
            if section not in sections or not sections[section].strip():
                self.fail("E_DISTILLATION_SECTION", path, f"non-empty section: {section}", "missing/empty")
        sentence = compact_text(sections.get("一句话", ""))
        if len(sentence) < 12 or sentence in {source, Path(source).name}:
            self.fail("E_DISTILLATION_SENTENCE", path, "at least 12 non-template characters", sentence)
        points = [
            line[2:].strip()
            for line in sections.get("关键要点", "").splitlines()
            if line.startswith("- ") and line[2:].strip()
        ]
        if len(points) < 2 or any(len(point) < 8 for point in points[:2]):
            self.fail("E_DISTILLATION_POINTS", path, "at least two points with 8+ characters", points)

    def _check_g5(self, scopes: dict[str, dict[str, str]], outputs: dict[str, str]) -> None:
        expected_by_group: dict[str, set[str]] = {}
        scope_groups = {row.get("group", "") for row in scopes.values()}
        for source, output in outputs.items():
            expected_by_group.setdefault(scopes.get(source, {}).get("group", ""), set()).add(output)

        summaries: dict[str, tuple[Path, list[str]]] = {}
        summary_dir = self.collection / "summaries"
        if summary_dir.exists() and is_reparse(summary_dir):
            self.fail("E_REPARSE_POINT", summary_dir, "regular directory", "reparse")
        elif summary_dir.exists():
            for summary_path in sorted(summary_dir.glob("*.md"), key=lambda p: p.name.casefold()):
                if is_reparse(summary_path) or not summary_path.is_file():
                    self.fail("E_REPARSE_POINT", summary_path, "regular Markdown", "reparse/not-file")
                    continue
                text = read_text_checked(summary_path, self.fail)
                if text is None:
                    continue
                missing_sections = [list(aliases) for aliases in SUMMARY_SECTION_ALIASES if not any(f"## {heading}" in text for heading in aliases)]
                if missing_sections:
                    self.fail("E_SUMMARY_SECTION", summary_path, [list(v) for v in SUMMARY_SECTION_ALIASES], missing_sections)
                if "## 一句话" in text or "## 关键要点" in text or "<a id=\"doc-" in text:
                    self.fail("E_SUMMARY_INLINE_BODY", summary_path, "links and cross-file synthesis only", "per-file body marker")
                metadata = parse_metadata(text)
                links = SUMMARY_LINK_RE.findall(text)
                linked_groups = {
                    PurePosixPath(link[len("../distillations/") :]).parts[0]
                    for link in links
                    if PurePosixPath(link[len("../distillations/") :]).parts
                }
                group = metadata.get("group", "")
                if self.legacy_scope_used:
                    if len(linked_groups) > 1:
                        self.fail("E_SUMMARY_GROUP", summary_path, "links from one output group", sorted(linked_groups))
                        continue
                    if len(linked_groups) == 1:
                        group = next(iter(linked_groups))
                    else:
                        group = f"legacy-empty:{summary_path.stem}"
                elif group not in scope_groups:
                    self.fail("E_SUMMARY_GROUP", summary_path, sorted(scope_groups), group)
                    continue
                if group in summaries:
                    self.fail("E_SUMMARY_DUPLICATE_GROUP", summary_path, "one summary", group)
                    continue
                summaries[group] = (summary_path, links)

        for group, (summary_path, links) in sorted(summaries.items()):
            expected = expected_by_group.get(group, set())
            normalized = [link[len("../") :] for link in links]
            counts = Counter(normalized)
            duplicates = sorted(link for link, count in counts.items() if count > 1)
            if duplicates:
                self.fail("E_SUMMARY_LINK_DUPLICATE", summary_path, [], duplicates)
            actual = set(normalized)
            missing = sorted(expected - actual)
            extra = sorted(actual - expected)
            expected_links = {"links": sorted(expected), "missing": [], "extra": []}
            actual_links = {"links": sorted(actual), "missing": missing, "extra": extra}
            if missing:
                self.fail("E_SUMMARY_LINK_MISSING", summary_path, expected_links, actual_links)
            if extra:
                self.fail("E_SUMMARY_LINK_EXTRA", summary_path, expected_links, actual_links)
            for rel in sorted(actual):
                target = safe_collection_relative(self.collection, rel)
                if target is None or not target.is_file() or first_reparse_within(self.collection, target) is not None:
                    self.fail("E_SUMMARY_LINK_EXTRA", summary_path, "existing regular result link", rel)
        if self.require_summary:
            for group, expected in sorted(expected_by_group.items()):
                if len(expected) >= 2 and group not in summaries:
                    self.fail("E_SUMMARY_MISSING", group, "one summary for a multi-result group", "missing")
        self.counts["summaries"] = len(summaries)

    def _check_source_query(
        self,
        scopes: dict[str, dict[str, str]],
        inventory: dict[str, dict[str, str]],
        manifest: dict[str, dict[str, str]],
    ) -> None:
        source = self.source or ""
        if source not in scopes or source not in inventory or source not in manifest:
            self.fail(
                "E_SOURCE_QUERY_MISSING",
                source,
                "one matching row in scope/inventory/manifest",
                {"scope": source in scopes, "inventory": source in inventory, "manifest": source in manifest},
            )
            return
        self._check_inventory({source: inventory[source]})
        state = self._check_manifest({source: manifest[source]}, required_gate="G4")
        row = state.get(source, {})
        if row.get("distilled") is True:
            self._check_g4({source: scopes[source]}, {source: manifest[source]}, state, scan_all=False)
        elif row.get("skipped") is not True:
            self.fail("E_G4_INCOMPLETE", source, "distilled=true or skipped=true", "neither")


def machine_contract() -> dict[str, Any]:
    return {
        "contract_version": CONTRACT_VERSION,
        "files": {
            "scope.csv": list(SCOPE_HEADERS),
            "inventory.csv": list(INVENTORY_HEADERS),
            "manifest.csv": list(MANIFEST_HEADERS),
        },
        "enums": {
            "inventory.status": list(INVENTORY_STATUSES),
            "manifest.booleans": list(BOOLEAN_VALUES),
            "gate": ["G2", "G3", "G4", "G5", "G7"],
        },
        "modes": {
            "legacy_read_only": "explicitly allows missing scope.csv and missing source_hash_version for unchanged legacy results",
            "require_summary": "requires one summary only for groups with at least two independent results",
        },
        "writers": {
            "scope.path/group": "G1",
            "inventory.* and manifest.indexed=true": "G2",
            "manifest.read/skipped/reason": "G3",
            "manifest.distilled/output_ids and distillation files": "G4",
            "summaries and links": "G5",
        },
        "gate_required_manifest_fields": {
            "G2": ["indexed", "last_verified"],
            "G3": ["indexed", "read", "skipped", "reason-when-unread-or-skipped", "last_verified"],
            "G4": ["indexed", "read", "distilled", "skipped", "output_ids-when-distilled", "last_verified"],
        },
        "distillation": {
            "primary_prefix": PRIMARY_PREFIX,
            "filename": RESULT_NAME_PATTERN,
            "metadata": list(DISTILLATION_METADATA),
            "source_hash_version": {
                "normal": ["portable-v1"],
                "legacy_read_only": ["portable-v1", "absent"],
            },
            "sections": list(DISTILLATION_SECTIONS),
            "minimum_sentence_characters": 12,
            "minimum_points": 2,
            "minimum_point_characters": 8,
        },
        "summary_sections": [list(value) for value in SUMMARY_SECTION_ALIASES],
        "limitations": list(LIMITATIONS),
    }


def load_csv(
    path: Path,
    headers: tuple[str, ...],
    missing_code: str,
    header_code: str,
    duplicate_code: str,
    fail,
) -> dict[str, dict[str, str]]:
    if not path.exists():
        fail(missing_code, path, "regular CSV", "missing")
        return {}
    if is_reparse(path) or not path.is_file():
        fail("E_REPARSE_POINT", path, "regular CSV", "reparse/not-file")
        return {}
    text = read_text_checked(path, fail)
    if text is None:
        return {}
    reader = csv.DictReader(io.StringIO(text, newline=""))
    actual_headers = tuple(reader.fieldnames or ())
    if actual_headers != headers:
        fail(header_code, path, list(headers), list(actual_headers))
        return {}
    rows: dict[str, dict[str, str]] = {}
    for number, row in enumerate(reader, start=2):
        if None in row or any(value is None for value in row.values()):
            fail("E_CSV_ROW", f"{path}:{number}", list(headers), row)
            continue
        normalized = {key: value for key, value in row.items()}
        key = normalized.get("path", "")
        if not key:
            fail("E_CSV_ROW", f"{path}:{number}", "non-empty path", key)
            continue
        if key in rows:
            fail(duplicate_code, key, "unique path", f"duplicate at line {number}")
            continue
        rows[key] = normalized
    return rows


def read_text_checked(path: Path, fail) -> str | None:
    if not path.exists():
        return None
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise UsageOrReadError(f"无法读取 {path}: {exc}") from exc
    if data.startswith(b"\xef\xbb\xbf"):
        fail("E_BOM", path, "UTF-8 without BOM", "BOM")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail("E_ENCODING", path, "strict UTF-8", str(exc))
        return None
    bad_lines = [number for number, line in enumerate(text.splitlines(), start=1) if re.search(r"[ \t]+$", line)]
    if bad_lines:
        fail("E_TRAILING_WHITESPACE", path, [], bad_lines[:20])
    return text


def read_text_required(path: Path, missing_code: str, fail) -> str | None:
    if not path.exists():
        fail(missing_code, path, "regular UTF-8 file", "missing")
        return None
    if is_reparse(path) or not path.is_file():
        fail("E_REPARSE_POINT", path, "regular file", "reparse/not-file")
        return None
    return read_text_checked(path, fail)


def parse_metadata(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("## "):
            break
        match = re.match(r"^- ([a-z_]+):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip()
    return values


def parse_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections.setdefault(current, [])
        elif current is not None:
            sections[current].append(line)
    return {key: "\n".join(value).strip() for key, value in sections.items()}


def compact_text(value: str) -> str:
    return " ".join(part.strip() for part in value.splitlines() if part.strip())


def split_output_ids(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def normalize_source(source: str) -> str:
    normalized = unicodedata.normalize("NFC", source).replace("\\", "/")
    if re.match(r"^[A-Za-z]:/", normalized):
        normalized = normalized[0].upper() + normalized[1:]
    return normalized


def source_hash12(source: str) -> str:
    normalized = normalize_source(source)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:12]


def is_absolute_source(source: str) -> bool:
    return bool(source.startswith("/") or re.match(r"^[A-Za-z]:[\\/]", source) or source.startswith("\\\\"))


def safe_output_path(collection: Path, value: str) -> Path | None:
    if "\\" in value:
        return None
    pure = PurePosixPath(value)
    if pure.is_absolute() or len(pure.parts) != 2 or any(part in {"", ".", ".."} for part in pure.parts):
        return None
    if not re.fullmatch(GROUP_PATTERN, pure.parts[0]) or not re.fullmatch(RESULT_NAME_PATTERN, pure.parts[1]):
        return None
    return safe_collection_relative(collection, f"distillations/{value}")


def safe_collection_relative(collection: Path, value: str) -> Path | None:
    if "\\" in value:
        return None
    pure = PurePosixPath(value)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        return None
    candidate = collection.joinpath(*pure.parts)
    try:
        candidate.absolute().relative_to(collection.absolute())
    except ValueError:
        return None
    return candidate


def iter_regular_markdown(root: Path, fail) -> Iterable[str]:
    if not root.exists():
        return []
    if is_reparse(root):
        fail("E_REPARSE_POINT", root, "regular directory", "reparse")
        return []
    values: list[str] = []
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        kept_dirs: list[str] = []
        for name in sorted(dirs, key=str.casefold):
            child = current_path / name
            if is_reparse(child):
                fail("E_REPARSE_POINT", child, "regular directory", "reparse")
            else:
                kept_dirs.append(name)
        dirs[:] = kept_dirs
        for name in sorted(files, key=str.casefold):
            if not name.endswith(".md"):
                continue
            child = current_path / name
            if is_reparse(child) or not child.is_file():
                fail("E_REPARSE_POINT", child, "regular Markdown", "reparse/not-file")
                continue
            rel = child.relative_to(root.parent).as_posix()
            values.append(rel)
    return values


def is_reparse(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
        return False
    attribute = getattr(info, "st_file_attributes", 0)
    flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    return stat.S_ISLNK(info.st_mode) or bool(flag and attribute & flag)


def first_reparse_component(path: Path) -> Path | None:
    current = path.absolute()
    chain = list(reversed((current, *current.parents)))
    for candidate in chain:
        if os.path.lexists(candidate) and is_reparse(candidate):
            return candidate
    return None


def first_reparse_within(root: Path, path: Path) -> Path | None:
    try:
        relative = path.absolute().relative_to(root.absolute())
    except ValueError:
        return path
    current = root
    if is_reparse(current):
        return current
    for part in relative.parts:
        current = current / part
        if os.path.lexists(current) and is_reparse(current):
            return current
    return None


def parse_iso_datetime(value: str) -> bool:
    if not value:
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def valid_date(value: str) -> bool:
    if not DATE_RE.fullmatch(value):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def format_report(report: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return
    print(f"status={report['status']} mode={report.get('mode', '')} gate={report.get('gate', '')}")
    counts = " ".join(f"{key}={value}" for key, value in report.get("counts", {}).items())
    if counts:
        print(counts)
    for item in report.get("failures", []):
        print(
            f"[{item['code']}] gate={item['gate']} path={item['path']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False)} "
            f"actual={json.dumps(item['actual'], ensure_ascii=False)}"
        )
        print(f"  remediation: {item['remediation']}")
    for limitation in report.get("limitations", []):
        print(f"limitation: {limitation}")


def describe(as_json: bool) -> int:
    contract = machine_contract()
    if as_json:
        print(json.dumps(contract, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"contract_version={CONTRACT_VERSION}")
        for name, headers in contract["files"].items():
            print(f"{name}: {','.join(headers)}")
        print(f"inventory.status: {'|'.join(INVENTORY_STATUSES)}")
        print(f"manifest.booleans: {'|'.join(BOOLEAN_VALUES)}")
        print(f"result filename: {RESULT_NAME_PATTERN}")
        for field, writer in contract["writers"].items():
            print(f"writer {field}: {writer}")
        for limitation in LIMITATIONS:
            print(f"limitation: {limitation}")
    return 0


def explain(code: str, as_json: bool) -> int:
    if code not in ERRORS:
        raise UsageOrReadError(f"未知错误码: {code}")
    gate, remediation = ERRORS[code]
    payload = {"code": code, "gate": gate, "remediation": remediation}
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"code={code} gate={gate}\nremediation={remediation}")
    return 0


def print_source_hash(source: str, as_json: bool) -> int:
    payload = {
        "version": "portable-v1",
        "source": source,
        "normalized": normalize_source(source),
        "source_hash12": source_hash12(source),
    }
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(payload["source_hash12"])
    return 0


def build_fixture(root: Path) -> tuple[Path, str, Path]:
    source_dir = root / "source"
    source_dir.mkdir(parents=True)
    source_file = source_dir / "guide.txt"
    source_file.write_text("alpha source evidence\n", encoding="utf-8", newline="\n")
    source = str(source_file.resolve())
    collection = root / "collection"
    (collection / "distillations" / "alpha").mkdir(parents=True)
    (collection / "summaries").mkdir()
    result_name = f"d-{source_hash12(source)}-guide.md"
    result_rel = f"alpha/{result_name}"
    result = collection / "distillations" / "alpha" / result_name
    stamp = datetime.fromtimestamp(source_file.stat().st_mtime).astimezone().isoformat(timespec="seconds")
    (collection / "README.md").write_text("# Collection\n", encoding="utf-8", newline="\n")
    (collection / "scope.csv").write_text(f"path,group\n{csv_quote(source)},alpha\n", encoding="utf-8", newline="\n")
    (collection / "inventory.csv").write_text(
        f"{','.join(INVENTORY_HEADERS)}\n{csv_quote(source)},text,{source_file.stat().st_size},{stamp},exists\n",
        encoding="utf-8",
        newline="\n",
    )
    (collection / "manifest.csv").write_text(
        f"{','.join(MANIFEST_HEADERS)}\n{csv_quote(source)},true,true,true,false,,{PRIMARY_PREFIX}{result_rel},2026-08-18\n",
        encoding="utf-8",
        newline="\n",
    )
    result.write_text(
        "\n".join(
            (
                f"# 单文件蒸馏 {result.stem}",
                "",
                f"- distillation_id: {result.stem}",
                "- source_hash_version: portable-v1",
                f"- source: file:{source}",
                "- group: alpha",
                "- file_type: text",
                "- document_time: 2026-08-18",
                "- evidence_time: 2026-08-18",
                "",
                "## 一句话",
                "该指南定义了稳定的本地处理边界与核验顺序。",
                "",
                "## 关键要点",
                "",
                "- 处理前必须先确认原始文件身份与可读状态。",
                "- 每份派生结果都要保留精确来源并逐项回查。",
                "",
                "## 版本关系 / 不确定性",
                "当前只有一个版本，后续变化需要重新读取原文件。",
                "",
                "## 证据 / 现场复核边界",
                "",
                "- 本次由当前原文件直接读取并形成派生结果。",
                "- 回答易变事实前仍需回到原文件现场复核。",
                "",
            )
        ),
        encoding="utf-8",
        newline="\n",
    )
    (collection / "summaries" / "alpha.md").write_text(
        "\n".join(
            (
                "# Alpha 项目 / 主题综合",
                "",
                "- group: alpha",
                "- scope: fixture",
                "- source_root: fixture",
                "- file_distillations: 1",
                "- evidence_time: 2026-08-18",
                "- sensitivity: normal",
                "",
                "## 项目 / 主题速览",
                "",
                "- 本组用于验证确定性结构契约。",
                "",
                "## 跨文件核心事实 / 技术结论",
                "",
                "- 唯一文件形成唯一派生结果。",
                "",
                "## 文档版本 / 主题脉络",
                "",
                "- 当前只有一个已验证版本。",
                "",
                "## 单文件蒸馏导航",
                "",
                f"- [{result.stem}](../distillations/{result_rel}) — guide.txt",
                "",
                "## 限制与需现场复核",
                "",
                "- 结构通过不证明正文事实正确。",
                "",
            )
        ),
        encoding="utf-8",
        newline="\n",
    )
    return collection, source, result


def csv_quote(value: str) -> str:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="")
    writer.writerow([value])
    return stream.getvalue()


def run_check(
    collection: Path,
    source: str | None = None,
    gate: str = "G7",
    legacy_read_only: bool = False,
    require_summary: bool = False,
) -> dict[str, Any]:
    return Validator(
        collection,
        collection / "scope.csv",
        gate,
        source,
        legacy_read_only,
        require_summary,
    ).check()


def self_test(as_json: bool, temp_root: Path | None = None) -> int:
    tests: list[dict[str, str]] = []

    def record(name: str, status_value: str, detail: str = "") -> None:
        tests.append({"name": name, "status": status_value, "detail": detail})

    def expect_code(name: str, mutate, code: str) -> None:
        case = root / name
        shutil.copytree(base, case)
        mutate(case)
        report = run_check(case)
        codes = {item["code"] for item in report["failures"]}
        record(name, "pass" if report["status"] == "fail" and code in codes else "fail", f"codes={sorted(codes)}")

    with tempfile.TemporaryDirectory(prefix="collection-validator-", dir=temp_root) as temp:
        root = Path(temp)
        base, source, result = build_fixture(root / "base")
        positive = run_check(base)
        record("positive", "pass" if positive["status"] == "pass" else "fail", str(positive["failures"]))
        source_query = run_check(base, source=source)
        record("source-query", "pass" if source_query["status"] == "pass" else "fail", str(source_query["failures"]))

        g2_pending = root / "g2-empty-downstream"
        shutil.copytree(base, g2_pending)
        clear_manifest_fields(g2_pending, ("read", "distilled", "skipped", "reason", "output_ids"))
        g2_report = run_check(g2_pending, gate="G2")
        record("g2-empty-downstream", "pass" if g2_report["status"] == "pass" else "fail", str(g2_report["failures"]))

        g3_pending = root / "g3-distilled-pending"
        shutil.copytree(base, g3_pending)
        clear_manifest_fields(g3_pending, ("distilled", "output_ids"))
        g3_report = run_check(g3_pending, gate="G3")
        record("g3-distilled-pending", "pass" if g3_report["status"] == "pass" else "fail", str(g3_report["failures"]))
        g4_pending_report = run_check(g3_pending, gate="G4")
        g4_pending_codes = {item["code"] for item in g4_pending_report["failures"]}
        record(
            "g4-rejects-empty-distilled",
            "pass" if g4_pending_report["status"] == "fail" and "E_BOOLEAN_INVALID" in g4_pending_codes else "fail",
            f"codes={sorted(g4_pending_codes)}",
        )

        no_summary = root / "single-result-no-summary"
        shutil.copytree(base, no_summary)
        next((no_summary / "summaries").glob("*.md")).unlink()
        no_summary_report = run_check(no_summary, gate="G5")
        no_summary_required_report = run_check(no_summary, gate="G5", require_summary=True)
        record(
            "single-result-no-summary",
            "pass" if no_summary_report["status"] == "pass" and no_summary_required_report["status"] == "pass" else "fail",
            f"default={no_summary_report['status']} required={no_summary_required_report['status']}",
        )

        expect_code(
            "duplicate-path",
            lambda c: append_text(c / "scope.csv", f"{csv_quote(source)},alpha\n"),
            "E_SCOPE_DUPLICATE",
        )
        expect_code(
            "scope-set-diff",
            lambda c: append_text(c / "scope.csv", f"{csv_quote(str(root / 'missing.txt'))},alpha\n"),
            "E_SCOPE_INVENTORY_DIFF",
        )
        expect_code(
            "manifest-set-diff",
            lambda c: write_rows_without_data(c / "manifest.csv", MANIFEST_HEADERS),
            "E_SCOPE_MANIFEST_DIFF",
        )
        expect_code("missing-output", lambda c: next((c / "distillations" / "alpha").glob("*.md")).unlink(), "E_OUTPUT_MISSING")
        expect_code(
            "orphan-output",
            lambda c: (c / "distillations" / "alpha" / "d-000000000000-orphan.md").write_text("orphan\n", encoding="utf-8"),
            "E_ORPHAN_OUTPUT",
        )
        expect_code(
            "source-mismatch",
            lambda c: replace_text(
                next((c / "distillations" / "alpha").glob("*.md")),
                f"- source: file:{source}",
                f"- source: file:{root / 'wrong.txt'}",
            ),
            "E_DISTILLATION_SOURCE_MISMATCH",
        )
        expect_code(
            "group-mismatch",
            lambda c: replace_text(next((c / "distillations" / "alpha").glob("*.md")), "- group: alpha", "- group: beta"),
            "E_DISTILLATION_GROUP_MISMATCH",
        )
        expect_code("portable-hash-mismatch", change_result_hash, "E_DISTILLATION_HASH")
        expect_code(
            "missing-hash-version-normal",
            lambda c: remove_line(
                next((c / "distillations" / "alpha").glob("*.md")),
                "- source_hash_version: portable-v1",
            ),
            "E_DISTILLATION_HASH_VERSION",
        )
        legacy_hash_case = root / "missing-hash-version-legacy"
        shutil.copytree(base, legacy_hash_case)
        remove_line(
            next((legacy_hash_case / "distillations" / "alpha").glob("*.md")),
            "- source_hash_version: portable-v1",
        )
        legacy_hash_report = run_check(legacy_hash_case, legacy_read_only=True)
        record(
            "missing-hash-version-legacy",
            "pass" if legacy_hash_report["status"] == "pass" else "fail",
            str(legacy_hash_report["failures"]),
        )
        expect_code(
            "unknown-hash-version",
            lambda c: replace_text(
                next((c / "distillations" / "alpha").glob("*.md")),
                "- source_hash_version: portable-v1",
                "- source_hash_version: future-v2",
            ),
            "E_DISTILLATION_HASH_VERSION",
        )
        expect_code("size-mismatch", change_inventory_size, "E_SIZE_MISMATCH")
        missing_link_case = root / "summary-missing-link"
        shutil.copytree(base, missing_link_case)
        result_rel = result.relative_to(base / "distillations").as_posix()
        replace_text(
            missing_link_case / "summaries" / "alpha.md",
            f"](../distillations/{result_rel})",
            "]",
        )
        missing_link_report = run_check(missing_link_case)
        missing_link_failure = next(
            (item for item in missing_link_report["failures"] if item["code"] == "E_SUMMARY_LINK_MISSING"),
            None,
        )
        expected_output = f"distillations/{result_rel}"
        missing_link_ok = bool(
            missing_link_failure
            and missing_link_failure["expected"] != missing_link_failure["actual"]
            and missing_link_failure["actual"]
            == {"links": [], "missing": [expected_output], "extra": []}
        )
        record(
            "summary-missing-link",
            "pass" if missing_link_ok else "fail",
            json.dumps(missing_link_failure, ensure_ascii=False, sort_keys=True),
        )
        expect_code(
            "invalid-boolean",
            lambda c: replace_text(c / "manifest.csv", ",true,true,true,false,", ",TRUE,true,true,false,"),
            "E_BOOLEAN_INVALID",
        )
        expect_code(
            "invalid-status",
            lambda c: replace_text(c / "inventory.csv", ",exists\n", ",available\n"),
            "E_STATUS_INVALID",
        )
        expect_code("bom", lambda c: add_bom(c / "scope.csv"), "E_BOM")
        expect_code("trailing-whitespace", lambda c: append_text(c / "README.md", "bad  \n"), "E_TRAILING_WHITESPACE")
        expect_code(
            "path-traversal",
            lambda c: replace_primary(c / "manifest.csv", "distillation-file:../escape.md"),
            "E_OUTPUT_PATH_UNSAFE",
        )
        expect_code(
            "template-marker",
            lambda c: replace_text(
                next((c / "distillations" / "alpha").glob("*.md")),
                "该指南定义了稳定的本地处理边界与核验顺序。",
                "<该文件内容特异的一句话>",
            ),
            "E_TEMPLATE_MARKER",
        )
        expect_code(
            "missing-points",
            lambda c: remove_line(
                next((c / "distillations" / "alpha").glob("*.md")),
                "- 每份派生结果都要保留精确来源并逐项回查。",
            ),
            "E_DISTILLATION_POINTS",
        )

        reparse_case = root / "reparse"
        shutil.copytree(base, reparse_case)
        link = next((reparse_case / "distillations" / "alpha").glob("*.md"))
        target = reparse_case / "link-target.md"
        shutil.copy2(link, target)
        link.unlink()
        try:
            os.symlink(target, link)
        except OSError as exc:
            record("reparse", "skip", f"platform cannot create symlink: {exc}")
        else:
            report = run_check(reparse_case)
            codes = {item["code"] for item in report["failures"]}
            record("reparse", "pass" if "E_REPARSE_POINT" in codes else "fail", f"codes={sorted(codes)}")

    failed = [item for item in tests if item["status"] == "fail"]
    payload = {
        "status": "pass" if not failed else "fail",
        "tests": tests,
        "counts": dict(Counter(item["status"] for item in tests)),
    }
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"status={payload['status']} " + " ".join(f"{k}={v}" for k, v in sorted(payload["counts"].items())))
        for item in tests:
            print(f"[{item['status']}] {item['name']} {item['detail']}")
    return 0 if not failed else 1


def append_text(path: Path, value: str) -> None:
    path.write_text(path.read_text(encoding="utf-8") + value, encoding="utf-8", newline="\n")


def replace_text(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"self-test fixture missing text: {old}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")


def remove_line(path: Path, value: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    if value not in lines:
        raise RuntimeError(f"self-test fixture missing line: {value}")
    lines.remove(value)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def add_bom(path: Path) -> None:
    path.write_bytes(b"\xef\xbb\xbf" + path.read_bytes())


def write_rows_without_data(path: Path, headers: tuple[str, ...]) -> None:
    path.write_text(",".join(headers) + "\n", encoding="utf-8", newline="\n")


def replace_primary(path: Path, value: str) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"distillation-file:[^,\r\n]+", value, text, count=1)
    path.write_text(text, encoding="utf-8", newline="\n")


def change_result_hash(collection: Path) -> None:
    old = next((collection / "distillations" / "alpha").glob("*.md"))
    new = old.with_name("d-000000000000-guide.md")
    old_name = old.name
    text = old.read_text(encoding="utf-8").replace(f"- distillation_id: {old.stem}", f"- distillation_id: {new.stem}")
    old.unlink()
    new.write_text(text, encoding="utf-8", newline="\n")
    replace_text(collection / "manifest.csv", old_name, new.name)
    replace_text(collection / "summaries" / "alpha.md", old_name, new.name)


def change_inventory_size(collection: Path) -> None:
    path = collection / "inventory.csv"
    rows = list(csv.reader(io.StringIO(path.read_text(encoding="utf-8"), newline="")))
    rows[1][2] = str(int(rows[1][2]) + 1)
    stream = io.StringIO(newline="")
    csv.writer(stream, lineterminator="\n").writerows(rows)
    path.write_text(stream.getvalue(), encoding="utf-8", newline="\n")


def clear_manifest_fields(collection: Path, fields: tuple[str, ...]) -> None:
    path = collection / "manifest.csv"
    rows = list(csv.reader(io.StringIO(path.read_text(encoding="utf-8"), newline="")))
    indexes = {name: rows[0].index(name) for name in fields}
    for row in rows[1:]:
        for index in indexes.values():
            row[index] = ""
    stream = io.StringIO(newline="")
    csv.writer(stream, lineterminator="\n").writerows(rows)
    path.write_text(stream.getvalue(), encoding="utf-8", newline="\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    describe_parser = sub.add_parser("describe", help="打印校验器实际采用的机器契约")
    describe_parser.add_argument("--json", action="store_true")
    check_parser = sub.add_parser("check", help="只读校验 collection 或单一 source")
    check_parser.add_argument("--collection", required=True, type=Path)
    check_parser.add_argument("--scope", type=Path, help="默认使用 collection/scope.csv")
    check_parser.add_argument("--gate", choices=("G2", "G3", "G4", "G5", "G7"), default="G7")
    check_parser.add_argument("--source", help="只校验该精确 source 的 Q2 关系")
    check_parser.add_argument(
        "--legacy-read-only",
        action="store_true",
        help="显式只读核验旧集合；可用共同台账补缺 scope，并允许未声明 hash 版本的未改旧结果",
    )
    check_parser.add_argument(
        "--require-summary",
        action="store_true",
        help="仅要求有至少两个独立结果的 group 建 summary；默认只校验已存在 summary",
    )
    check_parser.add_argument("--json", action="store_true")
    explain_parser = sub.add_parser("explain", help="查询一个失败码的 Gate 和安全修复方向")
    explain_parser.add_argument("code")
    explain_parser.add_argument("--json", action="store_true")
    self_test_parser = sub.add_parser("self-test", help="在隔离临时目录运行正例和负例")
    self_test_parser.add_argument("--json", action="store_true")
    self_test_parser.add_argument("--temp-root", type=Path, help="可选的受控临时父目录；测试结束自动清理")
    hash_parser = sub.add_parser("hash", help="计算新结果使用的 portable-v1 source_hash12")
    hash_parser.add_argument("source")
    hash_parser.add_argument("--json", action="store_true")
    return parser


def configure_standard_streams() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if not callable(reconfigure):
            continue
        try:
            reconfigure(encoding="utf-8", errors="backslashreplace")
        except (AttributeError, OSError, ValueError):
            pass


def main(argv: list[str] | None = None) -> int:
    configure_standard_streams()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "describe":
            return describe(args.json)
        if args.command == "explain":
            return explain(args.code, args.json)
        if args.command == "self-test":
            temp_root = args.temp_root.expanduser().absolute() if args.temp_root else None
            if temp_root is not None and (not temp_root.is_dir() or is_reparse(temp_root)):
                raise UsageOrReadError(f"self-test 临时父目录不可用: {temp_root}")
            return self_test(args.json, temp_root)
        if args.command == "hash":
            return print_source_hash(args.source, args.json)
        collection = args.collection.expanduser().absolute()
        scope_path = (args.scope.expanduser().absolute() if args.scope else collection / "scope.csv")
        report = Validator(
            collection,
            scope_path,
            args.gate,
            args.source,
            args.legacy_read_only,
            args.require_summary,
        ).check()
        format_report(report, args.json)
        return 0 if report["status"] == "pass" else 1
    except UsageOrReadError as exc:
        payload = {"status": "error", "error": str(exc), "exit_code": 2}
        as_json = bool(getattr(args, "json", False))
        if as_json:
            print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), file=sys.stderr)
        else:
            print(f"error: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        payload = {"status": "error", "error": str(exc), "exit_code": 2}
        as_json = bool(getattr(args, "json", False))
        if as_json:
            print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), file=sys.stderr)
        else:
            print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
