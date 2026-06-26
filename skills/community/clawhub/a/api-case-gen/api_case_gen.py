"""
API Test Case Generator — from OpenAPI specs to test design matrices.

Analyzes service files, recursively expands models, extracts constraints
(schema + description heuristic + fallback hints), detects cross-field
dependencies, and generates prioritized test case matrices with response
assertions, auth/pagination coverage, and CRUD lifecycle chains.
"""

from __future__ import annotations

import json
import logging
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

log = logging.getLogger("api-case-gen")

# ---------------------------------------------------------------------------
#  Exit codes
# ---------------------------------------------------------------------------

EXIT_OK = 0
EXIT_BAD_ARGS = 1
EXIT_PARSE_ERROR = 2

# Well-known path parameters that don't need individual invalid-value tests
_COMMON_PATH_PARAMS = {"regionId", "az"}

# Pagination parameter names (matched case-insensitively)
_PAGINATION_NAMES_LOWER = {"pagenumber", "pageno", "pagesize", "pagelimit", "page", "size"}

# ---------------------------------------------------------------------------
#  Configuration
# ---------------------------------------------------------------------------


@dataclass
class AnalysisConfig:
    repo_root: str = ""
    output_format: str = "both"  # markdown | yaml | both
    priority_levels: list[str] = field(default_factory=lambda: ["P0", "P1", "P2"])
    extract_description_constraints: bool = True
    confidence_threshold: str = "medium"  # low | medium | high
    max_model_depth: int = 8
    include_internal_apis: bool = True
    env_mapping: dict[str, str] = field(default_factory=dict)
    defaults: dict[str, Any] = field(default_factory=dict)
    id_prefix: str = ""
    ref_version_dirs: list[str] = field(default_factory=lambda: ["v1", "v2"])
    internal_api_key: str = "x-jdcloud-internal"
    # Slim mode: reduce low-value test cases
    slim_path_params: bool = True   # max 1 invalid path param case per op
    slim_empty_string: bool = True  # empty-string only for required fields

    @classmethod
    def from_file(cls, path: str) -> "AnalysisConfig":
        p = Path(path)
        if not p.exists():
            log.warning("Config file not found: %s — using defaults", path)
            return cls()
        with open(p, encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}
        analysis = raw.get("analysis", {})
        gen = raw.get("generation", {})
        slim = raw.get("slim", {})
        return cls(
            repo_root=raw.get("repo_root", ""),
            output_format=raw.get("output", {}).get("format", "both"),
            priority_levels=gen.get("priority_levels", ["P0", "P1", "P2"]),
            extract_description_constraints=analysis.get("extract_description_constraints", True),
            confidence_threshold=analysis.get("confidence_threshold", "medium"),
            max_model_depth=analysis.get("max_model_depth", 8),
            include_internal_apis=analysis.get("include_internal_apis", True),
            env_mapping=raw.get("env_mapping", {}),
            defaults=raw.get("defaults", {}),
            id_prefix=gen.get("id_prefix", ""),
            ref_version_dirs=analysis.get("ref_version_dirs", ["v1", "v2"]),
            internal_api_key=analysis.get("internal_api_key", "x-jdcloud-internal"),
            slim_path_params=slim.get("path_params", True),
            slim_empty_string=slim.get("empty_string", True),
        )


# ---------------------------------------------------------------------------
#  Constraint extraction — extensible pattern registry
# ---------------------------------------------------------------------------

CONFIDENCE_ORDER = {"high": 3, "medium": 2, "low": 1}

# Each entry: (compiled_regex, constraint_kind, handler, confidence)
# handler: "groups" → use group(1), group(2); "group1" → use group(1)
DESC_PATTERNS: list[tuple[str, str, str, str]] = [
    # Range: 取值范围[1, 100] / (1~100) / 1-100之间
    (r"(?:取值)?范围\s*[\[（(]\s*(\d+)\s*[,，\s~\-]+\s*(\d+)\s*[\]）)]", "range", "groups", "high"),
    (r"(\d+)\s*(?:到|至|~|-)\s*(\d+)\s*(?:之间|个|位|字符)", "range", "groups", "high"),
    # Max: 不大于N / <=N / 不超过N位 / 最多N个 / N以内
    (r"(?:不[大超]于|<=?)\s*(\d+)", "maxLength_or_maximum", "group1", "high"),
    (r"(?:最[大长多]|上限)\s*(\d+)", "maxLength_or_maximum", "group1", "high"),
    (r"不能超过\s*(\d+)", "maxLength_or_maximum", "group1", "high"),
    (r"(\d+)\s*(?:位|个|字符|字节)\s*(?:以内|以下|之内)", "maxLength_or_maximum", "group1", "high"),
    # Min: 不小于N / >=N / 至少N
    (r"(?:不[小少]于|>=?)\s*(\d+)", "minLength_or_minimum", "group1", "high"),
    (r"(?:至少|最[小短少])\s*(\d+)", "minLength_or_minimum", "group1", "high"),
    # Default: 默认N / 默认为N / 默认值N
    (r"默认\s*(?:值\s*)?(?:为\s*)?[\"']?(\S+?)[\"']?(?:[，,。；;）)\s]|$)", "default", "group1", "high"),
    # Pattern hints
    (r"以([a-zA-Z\u4e00-\u9fff]+)开头", "pattern_hint", "group1", "medium"),
    (r"只支持([\w\u4e00-\u9fff、/]+)", "pattern_hint", "group1", "medium"),
    (r"只[能允]许([\w\u4e00-\u9fff、/]+)", "pattern_hint", "group1", "medium"),
    # Boolean constraint from description
    (r"true\s*(?:为|表示).*?false\s*(?:为|表示)", "boolean_semantics", "group0", "medium"),
    (r"false\s*(?:为|表示).*?true\s*(?:为|表示)", "boolean_semantics", "group0", "medium"),
]

# Enum extraction patterns — broader than brackets-only
ENUM_PATTERNS: list[re.Pattern] = [
    # [A,B,C] or (A/B/C) or 【A、B】
    re.compile(
        r"[\[（(【]"
        r"([A-Za-z0-9_|]+(?:[,，/、|][A-Za-z0-9_|]+)+)"
        r"[\]）)】]"
    ),
    # 可选值：A、B、C  or  取值为：A, B
    re.compile(
        r"(?:可选值|支持的值|取值)\s*[：:]\s*"
        r"([A-Za-z0-9_]+(?:[,，、/|]\s*[A-Za-z0-9_]+)+)"
    ),
]

# Fallback hint keywords — detect potentially-constrained fields
HINT_KEYWORDS: list[tuple[str, str]] = [
    (r"\d+", "含数字（可能是范围/长度/个数）"),
    (r"必填|必传|不[可能]为空", "含必填提示"),
    (r"仅[当在]|只[有在当]|只有.*时", "含条件依赖"),
    (r"格式|日期|时间|yyyy|timestamp", "含格式约束"),
    (r"唯一|不重复|不允许重复", "含唯一性约束"),
    (r"依赖|关联|配合|联动", "含字段关联"),
    (r"JSON|BASE64|编码|序列化", "含编码/格式要求"),
    (r"可选值[：:]|支持的值[为：:]|取值[为：:]", "含枚举值（非标准格式）"),
    (r"[大小长短]于|超过|不超|上限|下限|至少|最多", "含边界约束"),
    (r"正[整]数|非负|正数|自然数", "含数值约束"),
    (r"文件|xlsx|csv|上传", "含文件类型约束"),
]


@dataclass
class FieldInfo:
    name: str
    path: str  # dot-separated (e.g. "spec.vpcId")
    field_type: str = ""
    required: bool = False
    description: str = ""
    enum: list[str] = field(default_factory=list)
    constraints: list[dict[str, Any]] = field(default_factory=list)
    items_type: str = ""
    ref: str = ""
    default: Any = None
    unextracted_hints: list[str] = field(default_factory=list)


def check_unextracted_hints(desc: str, existing_constraints: list[dict]) -> list[str]:
    """Detect fields whose description likely contains unextracted constraints.

    Only flags fields where regex extracted few constraints relative to
    the number of hint signals in the description.
    """
    if not desc:
        return []
    meaningful_kinds = {c.get("kind") for c in existing_constraints} - {"default"}
    hints: list[str] = []
    for pattern, label in HINT_KEYWORDS:
        if re.search(pattern, desc, re.IGNORECASE):
            hints.append(label)
    # Flag only if hints significantly outnumber extracted constraints
    if len(hints) >= 2 and len(meaningful_kinds) < max(len(hints) - 1, 1):
        return hints
    return []


def _meets_threshold(confidence: str, threshold: str) -> bool:
    return CONFIDENCE_ORDER.get(confidence, 0) >= CONFIDENCE_ORDER.get(threshold, 0)


def extract_schema_constraints(prop_def: dict, field_type: str = "string") -> list[dict[str, Any]]:
    """Extract constraints from schema-level keys (highest confidence).

    Reads: maxLength, minLength, minimum, maximum, exclusiveMinimum,
    exclusiveMaximum, pattern, format, minItems, maxItems, uniqueItems.
    """
    results: list[dict[str, Any]] = []
    _SCHEMA_KEYS = {
        "maxLength": "maxLength",
        "minLength": "minLength",
        "minimum": "minimum",
        "maximum": "maximum",
        "exclusiveMinimum": "exclusiveMinimum",
        "exclusiveMaximum": "exclusiveMaximum",
        "minItems": "minItems",
        "maxItems": "maxItems",
    }
    for yaml_key, kind in _SCHEMA_KEYS.items():
        val = prop_def.get(yaml_key)
        if val is not None and isinstance(val, (int, float)):
            results.append({"kind": kind, "value": val, "source": "schema", "confidence": "high"})

    pattern = prop_def.get("pattern")
    if pattern and isinstance(pattern, str):
        results.append({"kind": "pattern", "value": pattern, "source": "schema", "confidence": "high"})

    fmt = prop_def.get("format")
    if fmt and isinstance(fmt, str):
        results.append({"kind": "format", "value": fmt, "source": "schema", "confidence": "high"})

    if prop_def.get("uniqueItems") is True:
        results.append({"kind": "uniqueItems", "value": True, "source": "schema", "confidence": "high"})

    return results


def extract_desc_constraints(desc: str, field_type: str = "string") -> list[dict[str, Any]]:
    """Extract implicit constraints from a description string using pattern registry."""
    if not desc:
        return []
    results: list[dict[str, Any]] = []

    for pattern, kind, handler, confidence in DESC_PATTERNS:
        m = re.search(pattern, desc)
        if not m:
            continue
        if handler == "groups" and kind == "range":
            lo, hi = int(m.group(1)), int(m.group(2))
            if field_type in ("integer", "number"):
                results.append({"kind": "minimum", "value": lo, "source": "description", "confidence": confidence})
                results.append({"kind": "maximum", "value": hi, "source": "description", "confidence": confidence})
            else:
                results.append({"kind": "minLength", "value": lo, "source": "description", "confidence": confidence})
                results.append({"kind": "maxLength", "value": hi, "source": "description", "confidence": confidence})
        elif handler == "group1":
            val = m.group(1)
            if kind == "maxLength_or_maximum":
                k = "maximum" if field_type in ("integer", "number") else "maxLength"
                results.append({"kind": k, "value": int(val), "source": "description", "confidence": confidence})
            elif kind == "minLength_or_minimum":
                k = "minimum" if field_type in ("integer", "number") else "minLength"
                results.append({"kind": k, "value": int(val), "source": "description", "confidence": confidence})
            elif kind == "default":
                results.append({"kind": "default", "value": val, "source": "description", "confidence": confidence})
            elif kind == "pattern_hint":
                results.append({"kind": "pattern_hint", "value": val, "source": "description", "confidence": confidence})

    for enum_re in ENUM_PATTERNS:
        em = enum_re.search(desc)
        if em:
            raw = em.group(1)
            values = [v.strip() for v in re.split(r"[,，/、|]", raw) if v.strip()]
            if len(values) >= 2:
                results.append({"kind": "enum", "value": values, "source": "description", "confidence": "medium"})
            break

    return results


def extract_all_constraints(prop_def: dict, desc: str, field_type: str) -> list[dict[str, Any]]:
    """Three-layer extraction: schema → description → (fallback handled separately).

    Schema constraints take precedence; description constraints only added
    for kinds not already covered by schema.
    """
    schema_cs = extract_schema_constraints(prop_def, field_type)
    desc_cs = extract_desc_constraints(desc, field_type)
    schema_kinds = {c["kind"] for c in schema_cs}
    # Deduplicate: don't add desc constraint if schema already has that kind
    merged = list(schema_cs)
    for dc in desc_cs:
        if dc["kind"] not in schema_kinds:
            merged.append(dc)
    return merged


# ---------------------------------------------------------------------------
#  Model resolver — with pluggable cross-module strategy
# ---------------------------------------------------------------------------


class ModelResolver:
    """Resolve $ref across multi-file specs, tracking the resolved file path."""

    def __init__(self, repo_root: str, *, version_dirs: list[str] | None = None) -> None:
        self._root = Path(repo_root) if repo_root else None
        self._version_dirs = version_dirs or ["v1", "v2"]
        self._cache: dict[str, dict] = {}

    def _load(self, yaml_path: Path) -> dict:
        key = str(yaml_path.resolve())
        if key not in self._cache:
            if yaml_path.exists():
                try:
                    with open(yaml_path, encoding="utf-8") as f:
                        self._cache[key] = yaml.safe_load(f) or {}
                except yaml.YAMLError as e:
                    log.error("YAML parse error in %s: %s", yaml_path, e)
                    self._cache[key] = {}
            else:
                log.debug("File not found: %s", yaml_path)
                self._cache[key] = {}
        return self._cache[key]

    def resolve_ref(self, ref: str, context_file: Path) -> tuple[dict, str, Path]:
        """Resolve a $ref string relative to context_file.

        Cross-module refs (e.g. ../../module/model/File.yaml) are resolved
        by searching <repo_root>/<module>/<version_dir>/model/<File>.yaml.

        Returns: (resolved_definition, definition_name, resolved_file_path)
        """
        if "#" in ref:
            file_part, fragment = ref.split("#", 1)
        else:
            file_part, fragment = ref, ""

        if file_part:
            target_path = (context_file.parent / file_part).resolve()
        else:
            target_path = context_file.resolve()

        # Cross-module fallback: ../../module/model/File.yaml → <root>/module/v1/model/File.yaml
        if not target_path.exists() and self._root and file_part:
            real_parts = [p for p in Path(file_part).parts if p != ".."]
            if len(real_parts) >= 2:
                module = real_parts[0]
                rest = Path(*real_parts[1:])
                for vdir in self._version_dirs:
                    candidate = self._root / module / vdir / rest
                    if candidate.exists():
                        target_path = candidate.resolve()
                        log.debug("Cross-module resolved: %s → %s", ref, target_path)
                        break

        spec = self._load(target_path)
        parts = [p for p in fragment.strip("/").split("/") if p]
        obj = spec
        for part in parts:
            if isinstance(obj, dict):
                obj = obj.get(part, {})
            else:
                return {}, parts[-1] if parts else "", target_path
        return (obj if isinstance(obj, dict) else {}), (parts[-1] if parts else ""), target_path

    def expand_model(
        self,
        model: dict,
        context_file: Path,
        *,
        depth: int = 0,
        max_depth: int = 8,
        visited: set[str] | None = None,
    ) -> dict:
        """Recursively expand all $ref in a model definition.

        Each resolved $ref switches context_file to the file where the
        definition was found, so nested relative $refs resolve correctly.
        """
        if depth > max_depth:
            return model
        if visited is None:
            visited = set()

        result = dict(model)
        properties = result.get("properties", {})
        expanded_props = {}

        for prop_name, prop_def in properties.items():
            if not isinstance(prop_def, dict):
                expanded_props[prop_name] = prop_def
                continue

            prop_copy = dict(prop_def)

            if "$ref" in prop_copy:
                ref_key = prop_copy["$ref"]
                if ref_key in visited:
                    prop_copy["_circular"] = True
                else:
                    visited.add(ref_key)
                    resolved, _, resolved_file = self.resolve_ref(ref_key, context_file)
                    if resolved:
                        resolved = self.expand_model(
                            resolved, resolved_file,
                            depth=depth + 1, max_depth=max_depth, visited=visited,
                        )
                        prop_copy.update(resolved)
                    prop_copy.pop("$ref", None)

            if "items" in prop_copy and isinstance(prop_copy["items"], dict):
                items = prop_copy["items"]
                if "$ref" in items:
                    ref_key = items["$ref"]
                    if ref_key not in visited:
                        visited.add(ref_key)
                        resolved, _, resolved_file = self.resolve_ref(ref_key, context_file)
                        if resolved:
                            resolved = self.expand_model(
                                resolved, resolved_file,
                                depth=depth + 1, max_depth=max_depth, visited=visited,
                            )
                            prop_copy["items"] = resolved

            expanded_props[prop_name] = prop_copy

        result["properties"] = expanded_props
        return result


# ---------------------------------------------------------------------------
#  Data models
# ---------------------------------------------------------------------------


@dataclass
class BodyModel:
    """A resolved body parameter model with its expanded properties."""
    name: str
    param_name: str
    required: bool
    description: str
    model: dict

@dataclass
class CrossConstraint:
    """A constraint between two or more parameters."""
    kind: str  # conditional_required | mutual_exclusive | value_dependency | format_dependency
    fields: list[str]
    condition: str
    description: str
    confidence: str = "medium"

@dataclass
class OperationAnalysis:
    operation_id: str
    method: str
    path: str
    description: str
    internal: bool
    path_params: list[str]
    parameters: list[FieldInfo]
    body_models: list[BodyModel]
    response_fields: dict[str, Any]
    error_codes: list[str]
    cross_constraints: list[CrossConstraint]

    @property
    def body_model(self) -> dict | None:
        return self.body_models[0].model if self.body_models else None

    @property
    def body_model_name(self) -> str:
        return self.body_models[0].name if self.body_models else ""

@dataclass
class ServiceAnalysis:
    file_name: str
    title: str
    description: str
    base_path: str
    operations: list[OperationAnalysis]


# ---------------------------------------------------------------------------
#  Service analyzer
# ---------------------------------------------------------------------------


class ServiceAnalyzer:
    """Analyze a single service YAML file (Swagger 2.0 + OpenAPI 3.x)."""

    def __init__(self, resolver: ModelResolver, config: AnalysisConfig) -> None:
        self._resolver = resolver
        self._config = config

    def analyze(self, service_path: str | Path) -> ServiceAnalysis:
        service_path = Path(service_path)
        try:
            with open(service_path, encoding="utf-8") as f:
                spec = yaml.safe_load(f)
        except (OSError, yaml.YAMLError) as e:
            log.error("Failed to parse %s: %s", service_path, e)
            return ServiceAnalysis(
                file_name=service_path.name,
                title=service_path.stem,
                description=f"Parse error: {e}",
                base_path="",
                operations=[],
            )

        if not isinstance(spec, dict):
            log.error("Invalid spec format in %s", service_path)
            return ServiceAnalysis(
                file_name=service_path.name, title=service_path.stem,
                description="Invalid format", base_path="", operations=[],
            )

        is_oas3 = str(spec.get("openapi", "")).startswith("3")
        info = spec.get("info", {})
        base_path = spec.get("basePath", "")
        if is_oas3:
            servers = spec.get("servers", [])
            if servers and isinstance(servers[0], dict):
                base_path = servers[0].get("url", "")

        # OAS3: inline definitions for requestBody / components.schemas
        oas3_schemas = {}
        if is_oas3:
            oas3_schemas = (spec.get("components") or {}).get("schemas") or {}

        operations: list[OperationAnalysis] = []

        for path_key, methods in (spec.get("paths") or {}).items():
            if not isinstance(methods, dict):
                continue
            full_path = base_path + path_key
            path_params = re.findall(r"\{(\w+)\}", full_path)

            for method_name, op in methods.items():
                if method_name not in ("get", "post", "put", "delete", "patch"):
                    continue
                if not isinstance(op, dict):
                    continue

                is_internal = bool(
                    self._config.internal_api_key
                    and op.get(self._config.internal_api_key, False)
                )
                if not self._config.include_internal_apis and is_internal:
                    continue

                if is_oas3:
                    params, body_models = self._analyze_params_oas3(
                        op.get("parameters", []),
                        op.get("requestBody", {}),
                        service_path, oas3_schemas,
                    )
                    response_fields, error_codes = self._analyze_responses_oas3(
                        op.get("responses", {}), oas3_schemas,
                    )
                else:
                    params, body_models = self._analyze_params(
                        op.get("parameters", []), service_path,
                    )
                    response_fields, error_codes = self._analyze_responses(op.get("responses", {}))

                cross_constraints = self._detect_cross_constraints(params, body_models)

                operations.append(OperationAnalysis(
                    operation_id=op.get("operationId", f"{method_name}_{path_key}"),
                    method=method_name.upper(),
                    path=full_path,
                    description=op.get("description", op.get("summary", "")),
                    internal=is_internal,
                    path_params=path_params,
                    parameters=params,
                    body_models=body_models,
                    response_fields=response_fields,
                    error_codes=error_codes,
                    cross_constraints=cross_constraints,
                ))

        return ServiceAnalysis(
            file_name=service_path.name,
            title=info.get("title", service_path.stem),
            description=info.get("description", ""),
            base_path=base_path,
            operations=operations,
        )

    def _analyze_params(
        self, params: list[dict], context_file: Path,
    ) -> tuple[list[FieldInfo], list[BodyModel]]:
        fields: list[FieldInfo] = []
        body_models: list[BodyModel] = []

        for p in params:
            if not isinstance(p, dict):
                continue

            fi = FieldInfo(
                name=p.get("name", ""),
                path=p.get("name", ""),
                field_type=p.get("type", ""),
                required=p.get("required", False),
                description=p.get("description", ""),
                enum=p.get("enum", []),
                default=p.get("default"),
            )

            if p.get("type") == "array" and isinstance(p.get("items"), dict):
                fi.items_type = p["items"].get("type", "")
                ref = p["items"].get("$ref", "")
                if ref:
                    fi.ref = ref

            if p.get("in") == "body":
                schema = p.get("schema", {})
                ref = schema.get("$ref", "")
                if ref:
                    fi.ref = ref
                    resolved, name, resolved_file = self._resolver.resolve_ref(ref, context_file)
                    if resolved:
                        expanded = self._resolver.expand_model(
                            resolved, resolved_file,
                            max_depth=self._config.max_model_depth,
                        )
                        body_models.append(BodyModel(
                            name=name,
                            param_name=p.get("name", ""),
                            required=p.get("required", False),
                            description=p.get("description", ""),
                            model=expanded,
                        ))
                    else:
                        log.warning("Unresolved body $ref: %s in %s", ref, context_file)
                elif schema.get("type") == "array" and schema.get("items", {}).get("$ref"):
                    item_ref = schema["items"]["$ref"]
                    resolved, name, resolved_file = self._resolver.resolve_ref(item_ref, context_file)
                    if resolved:
                        expanded = self._resolver.expand_model(
                            resolved, resolved_file,
                            max_depth=self._config.max_model_depth,
                        )
                        body_models.append(BodyModel(
                            name=name,
                            param_name=p.get("name", ""),
                            required=p.get("required", False),
                            description=p.get("description", ""),
                            model={"type": "array", "items_model": expanded, "properties": expanded.get("properties", {})},
                        ))
                fi.field_type = "object"

            if self._config.extract_description_constraints:
                fi.constraints = extract_all_constraints(p, fi.description, fi.field_type)
                fi.unextracted_hints = check_unextracted_hints(fi.description, fi.constraints)

            fields.append(fi)

        return fields, body_models

    def _analyze_params_oas3(
        self, params: list[dict], request_body: dict | None,
        context_file: Path, schemas: dict,
    ) -> tuple[list[FieldInfo], list[BodyModel]]:
        """OAS3 parameter + requestBody analysis."""
        fields: list[FieldInfo] = []
        body_models: list[BodyModel] = []

        for p in params:
            if not isinstance(p, dict):
                continue
            schema = p.get("schema", {})
            fi = FieldInfo(
                name=p.get("name", ""),
                path=p.get("name", ""),
                field_type=schema.get("type", p.get("type", "")),
                required=p.get("required", False),
                description=p.get("description", ""),
                enum=schema.get("enum", p.get("enum", [])),
                default=schema.get("default", p.get("default")),
            )
            if self._config.extract_description_constraints:
                fi.constraints = extract_all_constraints(schema, fi.description, fi.field_type)
                fi.unextracted_hints = check_unextracted_hints(fi.description, fi.constraints)
            fields.append(fi)

        if request_body and isinstance(request_body, dict):
            content = request_body.get("content", {})
            json_schema = (content.get("application/json") or {}).get("schema", {})
            ref = json_schema.get("$ref", "")
            if ref:
                if ref.startswith("#/components/schemas/"):
                    name = ref.rsplit("/", 1)[-1]
                    resolved = schemas.get(name, {})
                    if resolved:
                        expanded = self._resolver.expand_model(
                            dict(resolved), context_file,
                            max_depth=self._config.max_model_depth,
                        )
                        body_models.append(BodyModel(
                            name=name, param_name="body",
                            required=request_body.get("required", False),
                            description=request_body.get("description", ""),
                            model=expanded,
                        ))
                else:
                    resolved, name, resolved_file = self._resolver.resolve_ref(ref, context_file)
                    if resolved:
                        expanded = self._resolver.expand_model(
                            resolved, resolved_file,
                            max_depth=self._config.max_model_depth,
                        )
                        body_models.append(BodyModel(
                            name=name, param_name="body",
                            required=request_body.get("required", False),
                            description=request_body.get("description", ""),
                            model=expanded,
                        ))
            elif json_schema.get("properties"):
                body_models.append(BodyModel(
                    name="RequestBody", param_name="body",
                    required=request_body.get("required", False),
                    description=request_body.get("description", ""),
                    model=json_schema,
                ))

        return fields, body_models

    @staticmethod
    def _analyze_responses_oas3(
        responses: dict, schemas: dict,
    ) -> tuple[dict[str, Any], list[str]]:
        result_fields: dict[str, Any] = {}
        error_codes: list[str] = []

        for code, resp in responses.items():
            code_str = str(code)
            if not isinstance(resp, dict):
                continue
            if code_str.startswith("2"):
                content = resp.get("content", {})
                json_schema = (content.get("application/json") or {}).get("schema", {})
                ref = json_schema.get("$ref", "")
                props = json_schema.get("properties", {})
                if ref and ref.startswith("#/components/schemas/"):
                    name = ref.rsplit("/", 1)[-1]
                    resolved = schemas.get(name, {})
                    props = resolved.get("properties", {}) if resolved else {}
                for k, v in props.items():
                    if isinstance(v, dict):
                        result_fields[k] = {
                            "type": v.get("type", ""),
                            "description": v.get("description", ""),
                        }
            elif code_str.startswith(("4", "5")):
                error_codes.append(code_str)

        return result_fields, error_codes

    @staticmethod
    def _detect_cross_constraints(
        params: list[FieldInfo], body_models: list[BodyModel],
    ) -> list[CrossConstraint]:
        """Detect inter-parameter constraints from descriptions."""
        constraints: list[CrossConstraint] = []
        all_descs: list[tuple[str, str]] = []

        for p in params:
            if p.description:
                all_descs.append((p.name, p.description))
        for bm in body_models:
            for pname, pdef in (bm.model.get("properties") or {}).items():
                if isinstance(pdef, dict) and pdef.get("description"):
                    all_descs.append((f"{bm.name}.{pname}", pdef["description"]))
                    for npname, npdef in (pdef.get("properties") or {}).items():
                        if isinstance(npdef, dict) and npdef.get("description"):
                            all_descs.append((f"{bm.name}.{pname}.{npname}", npdef["description"]))

        cond_pattern = re.compile(
            r"(?:仅当|仅在|只有|只在|当|在)\s*(\w+)\s*[=为是]\s*(\w+)\s*时"
            r".*?(?:有效|生效|必填|此参数|该参数)", re.DOTALL,
        )
        cond_pattern2 = re.compile(
            r"(\w+)\s*(?:为|=)\s*(\w+)\s*时\s*(?:必填|有效|生效|此参数)",
        )
        mutual_pattern = re.compile(r"([\w_]+)\s*或\s*([\w_]+)\s*(?:2种|两种)")
        value_dep_pattern = re.compile(
            r"(?:当)?(\w+)\s*(?:为|=)\s*(\w+)\s*时\s*(?:取值|值)\s*(?:为|范围)?\s*(?:[：:]?\s*)?"
            r"[\[（(]?\s*(\d+)\s*[~\-,，\s]+\s*(\d+)\s*[\]）)]?",
        )

        for fname, desc in all_descs:
            m = cond_pattern.search(desc)
            if not m:
                m = cond_pattern2.search(desc)
            if m:
                dep_field, dep_value = m.group(1), m.group(2)
                constraints.append(CrossConstraint(
                    kind="conditional_required",
                    fields=[fname, dep_field],
                    condition=f"{dep_field}={dep_value}",
                    description=f"{fname} 仅在 {dep_field}={dep_value} 时有效/必填",
                    confidence="medium",
                ))

            for vm in value_dep_pattern.finditer(desc):
                dep_field, dep_value = vm.group(1), vm.group(2)
                lo, hi = vm.group(3), vm.group(4)
                constraints.append(CrossConstraint(
                    kind="value_dependency",
                    fields=[fname, dep_field],
                    condition=f"当 {dep_field}={dep_value} 时 {fname} 取值 [{lo}, {hi}]",
                    description=f"{fname} 的范围依赖 {dep_field} 的值",
                    confidence="high",
                ))

            mm = mutual_pattern.search(desc)
            if mm:
                constraints.append(CrossConstraint(
                    kind="mutual_exclusive",
                    fields=[fname],
                    condition=f"取值为 {mm.group(1)} 或 {mm.group(2)}",
                    description=desc[:80],
                    confidence="low",
                ))

            if re.search(r"格式\s*[\"']?yyyy", desc, re.I):
                constraints.append(CrossConstraint(
                    kind="format_dependency",
                    fields=[fname],
                    condition="格式: yyyy-MM-dd",
                    description=f"{fname} 需要日期格式 yyyy-MM-dd",
                    confidence="high",
                ))

        return constraints

    @staticmethod
    def _analyze_responses(responses: dict) -> tuple[dict[str, Any], list[str]]:
        result_fields: dict[str, Any] = {}
        error_codes: list[str] = []

        for code, resp in responses.items():
            code_str = str(code)
            if code_str.startswith("2"):
                schema = resp.get("schema", {}) if isinstance(resp, dict) else {}
                result = schema.get("properties", {}).get("result", {})
                if isinstance(result, dict) and result.get("properties"):
                    for k, v in result["properties"].items():
                        result_fields[k] = {
                            "type": v.get("type", ""),
                            "description": v.get("description", ""),
                        }
            elif code_str.startswith(("4", "5")):
                error_codes.append(code_str)

        return result_fields, error_codes


# ---------------------------------------------------------------------------
#  Test case generator
# ---------------------------------------------------------------------------


@dataclass
class TestCase:
    case_id: str
    priority: str
    category: str
    scenario: str
    input_summary: str
    expected: str
    operation_id: str
    method: str
    path: str


class CaseGenerator:
    """Generate test cases from operation analysis using strategy pattern."""

    def __init__(self, config: AnalysisConfig) -> None:
        self._config = config
        self._counter: dict[str, int] = {}
        self._auth_emitted = False

    def reset(self) -> None:
        """Reset stateful counters (call before each independent analysis run)."""
        self._counter.clear()
        self._auth_emitted = False

    def _next_id(self, prefix: str) -> str:
        self._counter[prefix] = self._counter.get(prefix, 0) + 1
        return f"{prefix}_{self._counter[prefix]:03d}"

    def generate(self, op: OperationAnalysis) -> list[TestCase]:
        cases: list[TestCase] = []
        prefix = self._config.id_prefix or _op_id_to_prefix(op.operation_id)
        all_fields = self._collect_all_fields(op)

        if "P0" in self._config.priority_levels:
            cases.extend(self._p0_normal_flow(op, prefix))
            cases.extend(self._p0_missing_required(op, prefix))
            cases.extend(self._p0_auth(op, prefix))

        if "P1" in self._config.priority_levels:
            cases.extend(self._p1_boundary(op, prefix, all_fields))
            cases.extend(self._p1_enum(op, prefix, all_fields))
            cases.extend(self._p1_type_mismatch(op, prefix, all_fields))
            cases.extend(self._p1_pagination(op, prefix, all_fields))

        if "P2" in self._config.priority_levels:
            cases.extend(self._p2_business(op, prefix))

        if not cases:
            log.warning("Zero cases generated for %s — possible parse failure", op.operation_id)

        return cases

    # -- P0 strategies --

    def _p0_normal_flow(self, op: OperationAnalysis, prefix: str) -> list[TestCase]:
        resp_assertion = _build_response_assertions(op)
        return [TestCase(
            case_id=self._next_id(prefix), priority="P0", category="正常流",
            scenario=f"正常{_method_verb(op.method)} — 所有必填参数填有效值",
            input_summary=_summarize_required(op),
            expected=f"200, {resp_assertion}",
            operation_id=op.operation_id, method=op.method, path=op.path,
        )]

    def _p0_missing_required(self, op: OperationAnalysis, prefix: str) -> list[TestCase]:
        cases: list[TestCase] = []
        for f in self._collect_required(op):
            cases.append(TestCase(
                case_id=self._next_id(prefix), priority="P0", category="必填缺失",
                scenario=f"缺失必填参数 {f.name}",
                input_summary=f"{f.name}=null 或不传",
                expected="400 INVALID_ARGUMENT",
                operation_id=op.operation_id, method=op.method, path=op.path,
            ))
        return cases

    def _p0_auth(self, op: OperationAnalysis, prefix: str) -> list[TestCase]:
        """One global 401 case — auth is gateway-level, no need per-endpoint."""
        if self._auth_emitted:
            return []
        self._auth_emitted = True
        return [TestCase(
            case_id=self._next_id(prefix), priority="P0", category="未认证",
            scenario="不携带认证信息（无 Token/AK）— 网关层统一校验",
            input_summary="请求不带 Authorization header",
            expected="401 Unauthorized",
            operation_id=op.operation_id, method=op.method, path=op.path,
        )]

    # -- P1 strategies --

    def _p1_boundary(self, op: OperationAnalysis, prefix: str, all_fields: list[FieldInfo] | None = None) -> list[TestCase]:
        cases: list[TestCase] = []
        for f in (all_fields or self._collect_all_fields(op)):
            seen_kinds: set[str] = set()
            for c in f.constraints:
                kind, val = c.get("kind", ""), c.get("value")
                if not _meets_threshold(c.get("confidence", "low"), self._config.confidence_threshold):
                    continue
                if kind in seen_kinds:
                    continue
                seen_kinds.add(kind)

                if kind == "maxLength" and isinstance(val, (int, float)):
                    cases.append(TestCase(
                        case_id=self._next_id(prefix), priority="P1", category="字符串超长",
                        scenario=f"{f.name} 超过最大长度 {val}",
                        input_summary=f"{f.name}={int(val) + 1}字符",
                        expected="400",
                        operation_id=op.operation_id, method=op.method, path=op.path,
                    ))
                elif kind == "minLength" and isinstance(val, (int, float)) and val > 0:
                    cases.append(TestCase(
                        case_id=self._next_id(prefix), priority="P1", category="字符串过短",
                        scenario=f"{f.name} 低于最小长度 {val}",
                        input_summary=f"{f.name}={int(val) - 1}字符",
                        expected="400",
                        operation_id=op.operation_id, method=op.method, path=op.path,
                    ))
                elif kind in ("maximum", "exclusiveMaximum") and isinstance(val, (int, float)):
                    over = val if kind == "exclusiveMaximum" else val + 1
                    cases.append(TestCase(
                        case_id=self._next_id(prefix), priority="P1", category="数值上越界",
                        scenario=f"{f.name} 超过最大值 {val}",
                        input_summary=f"{f.name}={over}",
                        expected="400",
                        operation_id=op.operation_id, method=op.method, path=op.path,
                    ))
                elif kind in ("minimum", "exclusiveMinimum") and isinstance(val, (int, float)):
                    under = val if kind == "exclusiveMinimum" else val - 1
                    cases.append(TestCase(
                        case_id=self._next_id(prefix), priority="P1", category="数值下越界",
                        scenario=f"{f.name} 低于最小值 {val}",
                        input_summary=f"{f.name}={under}",
                        expected="400",
                        operation_id=op.operation_id, method=op.method, path=op.path,
                    ))
                elif kind == "maxItems" and isinstance(val, (int, float)):
                    cases.append(TestCase(
                        case_id=self._next_id(prefix), priority="P1", category="数组超限",
                        scenario=f"{f.name} 超过最大元素数 {val}",
                        input_summary=f"{f.name}=[{int(val) + 1} items]",
                        expected="400",
                        operation_id=op.operation_id, method=op.method, path=op.path,
                    ))
                elif kind == "pattern" and isinstance(val, str):
                    cases.append(TestCase(
                        case_id=self._next_id(prefix), priority="P1", category="正则不匹配",
                        scenario=f"{f.name} 不匹配 pattern /{val[:30]}/",
                        input_summary=f'{f.name}="!!!invalid!!!"',
                        expected="400",
                        operation_id=op.operation_id, method=op.method, path=op.path,
                    ))
                elif kind == "format" and isinstance(val, str):
                    fmt_examples = {
                        "date-time": "not-a-datetime",
                        "date": "not-a-date",
                        "email": "not-an-email",
                        "uri": "not-a-uri",
                        "uuid": "not-a-uuid",
                        "ipv4": "999.999.999.999",
                        "ipv6": "not-ipv6",
                    }
                    bad_val = fmt_examples.get(val, f"invalid-{val}")
                    cases.append(TestCase(
                        case_id=self._next_id(prefix), priority="P1", category="格式校验",
                        scenario=f"{f.name} 不符合 format={val}",
                        input_summary=f'{f.name}="{bad_val}"',
                        expected="400",
                        operation_id=op.operation_id, method=op.method, path=op.path,
                    ))

            # Slim mode: empty-string only for required fields
            emit_empty = not self._config.slim_empty_string or f.required
            if f.field_type == "string" and not f.enum and emit_empty:
                cases.append(TestCase(
                    case_id=self._next_id(prefix), priority="P1", category="空值",
                    scenario=f"{f.name} 传空字符串",
                    input_summary=f'{f.name}=""',
                    expected="400",
                    operation_id=op.operation_id, method=op.method, path=op.path,
                ))

            if f.field_type == "array" and (f.required or not self._config.slim_empty_string):
                cases.append(TestCase(
                    case_id=self._next_id(prefix), priority="P1", category="空数组",
                    scenario=f"{f.name} 传空数组",
                    input_summary=f"{f.name}=[]",
                    expected="400 或正常处理",
                    operation_id=op.operation_id, method=op.method, path=op.path,
                ))

        return cases

    def _p1_enum(self, op: OperationAnalysis, prefix: str, all_fields: list[FieldInfo] | None = None) -> list[TestCase]:
        cases: list[TestCase] = []
        for f in (all_fields or self._collect_all_fields(op)):
            enum_values = f.enum
            if not enum_values:
                for c in f.constraints:
                    if c.get("kind") == "enum" and isinstance(c.get("value"), list):
                        if _meets_threshold(c.get("confidence", "low"), self._config.confidence_threshold):
                            enum_values = c["value"]
                            break

            if enum_values:
                cases.append(TestCase(
                    case_id=self._next_id(prefix), priority="P1", category="枚举遍历",
                    scenario=f"{f.name} 遍历所有有效枚举值",
                    input_summary=f"逐一传入: {', '.join(str(v) for v in enum_values)}",
                    expected="均 200",
                    operation_id=op.operation_id, method=op.method, path=op.path,
                ))
                cases.append(TestCase(
                    case_id=self._next_id(prefix), priority="P1", category="枚举非法值",
                    scenario=f"{f.name} 传入不在枚举中的值",
                    input_summary=f'{f.name}="INVALID_ENUM_VALUE"',
                    expected="400",
                    operation_id=op.operation_id, method=op.method, path=op.path,
                ))

        return cases

    def _p1_type_mismatch(self, op: OperationAnalysis, prefix: str, all_fields: list[FieldInfo] | None = None) -> list[TestCase]:
        cases: list[TestCase] = []
        for f in (all_fields or self._collect_all_fields(op)):
            if f.field_type == "integer":
                cases.append(TestCase(
                    case_id=self._next_id(prefix), priority="P1", category="类型错误",
                    scenario=f"{f.name} 传字符串值（应为 integer）",
                    input_summary=f'{f.name}="abc"',
                    expected="400",
                    operation_id=op.operation_id, method=op.method, path=op.path,
                ))
            elif f.field_type == "boolean":
                cases.append(TestCase(
                    case_id=self._next_id(prefix), priority="P1", category="类型错误",
                    scenario=f"{f.name} 传非布尔值",
                    input_summary=f'{f.name}="maybe"',
                    expected="400",
                    operation_id=op.operation_id, method=op.method, path=op.path,
                ))
        return cases

    def _p1_pagination(self, op: OperationAnalysis, prefix: str, all_fields: list[FieldInfo] | None = None) -> list[TestCase]:
        """Generate pagination boundary tests for list-type endpoints."""
        cases: list[TestCase] = []
        fields = all_fields or self._collect_all_fields(op)
        page_fields = [f for f in fields if f.name.lower() in _PAGINATION_NAMES_LOWER]
        if not page_fields:
            return cases

        has_page_num = any(f.name.lower() in ("pagenumber", "pageno", "page") for f in page_fields)
        has_page_size = any(f.name.lower() in ("pagesize", "pagelimit", "size") for f in page_fields)

        if has_page_num:
            cases.append(TestCase(
                case_id=self._next_id(prefix), priority="P1", category="分页边界",
                scenario="pageNumber=0（通常最小为1）",
                input_summary="pageNumber=0",
                expected="400 或返回第一页",
                operation_id=op.operation_id, method=op.method, path=op.path,
            ))
            cases.append(TestCase(
                case_id=self._next_id(prefix), priority="P2", category="分页边界",
                scenario="pageNumber=999999（超出实际页数）",
                input_summary="pageNumber=999999",
                expected="200, 返回空列表",
                operation_id=op.operation_id, method=op.method, path=op.path,
            ))
        if has_page_size:
            cases.append(TestCase(
                case_id=self._next_id(prefix), priority="P1", category="分页边界",
                scenario="pageSize=0",
                input_summary="pageSize=0",
                expected="400 或返回默认条数",
                operation_id=op.operation_id, method=op.method, path=op.path,
            ))
            cases.append(TestCase(
                case_id=self._next_id(prefix), priority="P2", category="分页边界",
                scenario="pageSize 超过系统上限（如10000）",
                input_summary="pageSize=10000",
                expected="400 或截断至最大值",
                operation_id=op.operation_id, method=op.method, path=op.path,
            ))
        return cases

    # -- P2 strategies --

    def _p2_business(self, op: OperationAnalysis, prefix: str) -> list[TestCase]:
        cases: list[TestCase] = []

        if op.method in ("POST", "PUT"):
            cases.append(TestCase(
                case_id=self._next_id(prefix), priority="P2", category="幂等性",
                scenario="相同参数重复调用",
                input_summary="连续两次相同请求",
                expected="第二次 409 或幂等 200",
                operation_id=op.operation_id, method=op.method, path=op.path,
            ))

        # Slim: at most 1 invalid path param case (skip well-known ones)
        if self._config.slim_path_params:
            unique_params = [pp for pp in op.path_params if pp not in _COMMON_PATH_PARAMS]
            if unique_params:
                pp = unique_params[0]
                cases.append(TestCase(
                    case_id=self._next_id(prefix), priority="P2", category="路径参数无效",
                    scenario=f"路径参数 {pp} 传不存在的值",
                    input_summary=f'{pp}="non-existent-id"',
                    expected="404",
                    operation_id=op.operation_id, method=op.method, path=op.path,
                ))
        else:
            for pp in op.path_params:
                cases.append(TestCase(
                    case_id=self._next_id(prefix), priority="P2", category="路径参数无效",
                    scenario=f"路径参数 {pp} 传不存在的值",
                    input_summary=f'{pp}="non-existent-id"',
                    expected="404",
                    operation_id=op.operation_id, method=op.method, path=op.path,
                ))

        for cc in op.cross_constraints:
            if cc.kind == "conditional_required":
                cases.append(TestCase(
                    case_id=self._next_id(prefix), priority="P1", category="条件必填",
                    scenario=f"满足条件 {cc.condition} 但缺失 {cc.fields[0]}",
                    input_summary=f"设置 {cc.condition}，不传 {cc.fields[0]}",
                    expected="400",
                    operation_id=op.operation_id, method=op.method, path=op.path,
                ))
                cases.append(TestCase(
                    case_id=self._next_id(prefix), priority="P1", category="条件必填-反向",
                    scenario=f"不满足条件时传入 {cc.fields[0]}（应被忽略或拒绝）",
                    input_summary=f"条件不满足时仍传 {cc.fields[0]}",
                    expected="200（忽略）或 400",
                    operation_id=op.operation_id, method=op.method, path=op.path,
                ))
            elif cc.kind == "value_dependency":
                cases.append(TestCase(
                    case_id=self._next_id(prefix), priority="P1", category="值依赖-越界",
                    scenario=f"在 {cc.condition} 下传越界值",
                    input_summary=cc.condition + " → 传超出范围的值",
                    expected="400",
                    operation_id=op.operation_id, method=op.method, path=op.path,
                ))
            elif cc.kind == "format_dependency":
                cases.append(TestCase(
                    case_id=self._next_id(prefix), priority="P1", category="格式校验",
                    scenario=f"{cc.fields[0]} 传入非法日期格式",
                    input_summary=f'{cc.fields[0]}="not-a-date"',
                    expected="400",
                    operation_id=op.operation_id, method=op.method, path=op.path,
                ))

        return cases

    # -- Field collection --

    @staticmethod
    def _collect_required(op: OperationAnalysis) -> list[FieldInfo]:
        result = [p for p in op.parameters if p.required and p.path not in ("regionId", "instanceId")]
        for bm in op.body_models:
            for rname in bm.model.get("required", []):
                result.append(FieldInfo(
                    name=f"{bm.name}.{rname}",
                    path=f"{bm.name}.{rname}",
                    required=True,
                ))
        return result

    @staticmethod
    def _collect_all_fields(op: OperationAnalysis) -> list[FieldInfo]:
        """Collect all fields from params + all body models, recursively."""
        fields = [p for p in op.parameters if p.name not in ("regionId", "instanceId")]
        for bm in op.body_models:
            _flatten_model_fields(bm.model, prefix=bm.name, fields=fields, max_depth=4)
        return fields


def _flatten_model_fields(
    model: dict, prefix: str, fields: list[FieldInfo],
    *, max_depth: int = 4, depth: int = 0,
) -> None:
    """Recursively flatten model properties into FieldInfo list."""
    if depth > max_depth:
        return
    properties = model.get("properties", {})
    required_set = set(model.get("required", []))

    for pname, pdef in properties.items():
        if not isinstance(pdef, dict):
            continue

        field_path = f"{prefix}.{pname}" if prefix else pname
        ftype = pdef.get("type", "")
        desc = pdef.get("description", "")
        enum_vals = pdef.get("enum", [])
        items_type = ""
        if isinstance(pdef.get("items"), dict):
            items_type = pdef["items"].get("type", "")

        fi = FieldInfo(
            name=pname, path=field_path, field_type=ftype,
            required=pname in required_set,
            description=desc, enum=enum_vals, items_type=items_type,
        )
        fi.constraints = extract_all_constraints(pdef, desc, ftype)
        fi.unextracted_hints = check_unextracted_hints(desc, fi.constraints)
        fields.append(fi)

        if pdef.get("properties") and depth < max_depth:
            _flatten_model_fields(
                pdef, prefix=field_path, fields=fields,
                max_depth=max_depth, depth=depth + 1,
            )
        if isinstance(pdef.get("items"), dict) and pdef["items"].get("properties") and depth < max_depth:
            _flatten_model_fields(
                pdef["items"], prefix=f"{field_path}[]", fields=fields,
                max_depth=max_depth, depth=depth + 1,
            )


# ---------------------------------------------------------------------------
#  Helpers
# ---------------------------------------------------------------------------


def _op_id_to_prefix(op_id: str) -> str:
    parts = re.findall(r"[A-Z][a-z]+|[a-z]+|[A-Z]+", op_id)
    if len(parts) <= 2:
        return op_id[:8].upper()
    return "".join(p[0].upper() for p in parts[:4])


def _method_verb(method: str) -> str:
    return {"GET": "查询", "POST": "创建", "PUT": "更新", "DELETE": "删除", "PATCH": "修改"}.get(method, "操作")


def _summarize_required(op: OperationAnalysis) -> str:
    required = [p.name for p in op.parameters if p.required and p.name not in ("regionId", "instanceId")]
    for bm in op.body_models:
        required.extend(bm.model.get("required", []))
    if not required:
        return "无必填参数（仅路径参数）"
    return f"必填: {', '.join(required[:6])}" + ("..." if len(required) > 6 else "")


def _build_response_assertions(op: OperationAnalysis) -> str:
    """Build response assertions with key field != null checks."""
    parts: list[str] = []
    if op.response_fields:
        key_fields = list(op.response_fields.keys())[:5]
        for k in key_fields:
            parts.append(f"{k} != null")
    if not parts:
        parts.append("requestId != null")
    return "assert: " + ", ".join(parts)


# ---------------------------------------------------------------------------
#  CRUD lifecycle detection
# ---------------------------------------------------------------------------

_CRUD_VERBS = {
    "create": "create",
    "add": "create",
    "new": "create",
    "describe": "read",
    "get": "read",
    "list": "read",
    "query": "read",
    "update": "update",
    "modify": "update",
    "edit": "update",
    "delete": "delete",
    "remove": "delete",
    "destroy": "delete",
}


def _singularize(noun: str) -> str:
    """Best-effort English singular: Instances→Instance, Addresses→Address, Statuses→Status."""
    if noun.endswith("ses") and len(noun) > 4:
        # "Addresses" → "Address", "Statuses" → "Status"
        return noun[:-2]
    if noun.endswith("ies") and len(noun) > 4:
        return noun[:-3] + "y"
    if noun.endswith("s") and not noun.endswith("ss"):
        return noun[:-1]
    return noun


def detect_crud_chains(
    all_operations: list[OperationAnalysis],
) -> list[dict[str, Any]]:
    """Detect CRUD lifecycle chains across operations.

    Groups operations by resource noun and returns chains like:
    [{"resource": "Instance", "create": "createInstance", "read": "describeInstance",
      "update": "modifyInstance", "delete": "deleteInstance"}]
    """
    resource_ops: dict[str, dict[str, str]] = {}

    for op in all_operations:
        op_id = op.operation_id
        lower = op_id.lower()
        matched_verb = ""
        matched_crud = ""
        for verb, crud_type in _CRUD_VERBS.items():
            if lower.startswith(verb):
                matched_verb = verb
                matched_crud = crud_type
                break

        if not matched_crud:
            continue

        noun = op_id[len(matched_verb):]
        if not noun:
            continue
        base_noun = _singularize(noun) if matched_crud == "read" else noun

        if base_noun not in resource_ops:
            resource_ops[base_noun] = {}
        # Prefer create/delete over read/update for same slot
        if matched_crud not in resource_ops[base_noun]:
            resource_ops[base_noun][matched_crud] = op_id

    chains: list[dict[str, Any]] = []
    for resource, ops in resource_ops.items():
        if len(ops) >= 2 and ("create" in ops or "delete" in ops):
            chain: dict[str, Any] = {"resource": resource}
            chain.update(ops)
            chains.append(chain)

    return chains


# ---------------------------------------------------------------------------
#  Markdown output
# ---------------------------------------------------------------------------


def render_markdown(
    service: ServiceAnalysis,
    cases_by_op: dict[str, list[TestCase]],
    crud_chains: list[dict[str, Any]] | None = None,
) -> str:
    lines: list[str] = []
    lines.append(f"# {service.title} 接口测试设计\n")
    lines.append(f"> {service.description}\n")
    lines.append(f"> basePath: `{service.base_path}`\n")

    if crud_chains:
        lines.append("## CRUD 生命周期链\n")
        lines.append("以下资源具备完整或部分 CRUD 链，建议按链顺序执行端到端测试：\n")
        lines.append("| 资源 | Create | Read | Update | Delete |")
        lines.append("|------|--------|------|--------|--------|")
        for chain in crud_chains:
            lines.append(
                f"| {chain['resource']} "
                f"| {chain.get('create', '-')} "
                f"| {chain.get('read', '-')} "
                f"| {chain.get('update', '-')} "
                f"| {chain.get('delete', '-')} |"
            )
        lines.append("")

    for op in service.operations:
        lines.append(f"## {op.operation_id} ({op.method} {op.path})\n")
        lines.append(f"{op.description}\n")

        if op.internal:
            lines.append("> 内部接口 (internal)\n")

        all_fields = CaseGenerator._collect_all_fields(op)

        lines.append("### 参数约束摘要\n")
        lines.append("| 参数 | 类型 | 必填 | 约束 | 来源 |")
        lines.append("|------|------|------|------|------|")
        for f in all_fields:
            lines.append(f"| {f.name} | {f.field_type} | {'✓' if f.required else '✗'} | {_format_constraints(f)} | {_constraints_source(f)} |")

        if op.response_fields:
            lines.append("\n### 响应字段\n")
            lines.append("| 字段 | 类型 | 说明 |")
            lines.append("|------|------|------|")
            for fname, finfo in op.response_fields.items():
                lines.append(f"| {fname} | {finfo.get('type', '')} | {finfo.get('description', '')} |")

        if op.error_codes:
            lines.append(f"\n### 错误码: {', '.join(op.error_codes)}\n")

        if op.cross_constraints:
            lines.append("\n### 参数间约束\n")
            lines.append("| 类型 | 关联字段 | 约束条件 | 说明 | 置信度 |")
            lines.append("|------|---------|---------|------|--------|")
            kind_labels = {
                "conditional_required": "条件必填",
                "value_dependency": "值依赖",
                "mutual_exclusive": "互斥",
                "format_dependency": "格式依赖",
            }
            for cc in op.cross_constraints:
                label = kind_labels.get(cc.kind, cc.kind)
                lines.append(f"| {label} | {', '.join(cc.fields)} | {cc.condition} | {cc.description[:60]} | {cc.confidence} |")

        if len(op.body_models) > 1:
            lines.append(f"\n### Body 参数模型（{len(op.body_models)} 个）\n")
            for bm in op.body_models:
                req_tag = " (必填)" if bm.required else ""
                lines.append(f"- **{bm.param_name}** → `{bm.name}`{req_tag}: {bm.description[:80]}")

        review_fields = [f for f in all_fields if f.unextracted_hints]
        if review_fields:
            lines.append("\n### 待 AI 审查（正则未能提取的潜在约束）\n")
            lines.append("以下字段的 description 含约束线索但脚本未能结构化提取，需人工/AI 补充用例：\n")
            lines.append("| 字段 | 类型 | 线索 | Description |")
            lines.append("|------|------|------|-------------|")
            for f in review_fields:
                hints_str = "; ".join(f.unextracted_hints[:3])
                desc_short = f.description.replace("\n", " ")[:80]
                lines.append(f"| {f.path} | {f.field_type} | {hints_str} | {desc_short} |")

        op_cases = cases_by_op.get(op.operation_id, [])
        if op_cases:
            lines.append("\n### 测试用例\n")
            lines.append("| ID | 优先级 | 场景 | 输入要点 | 预期结果 |")
            lines.append("|----|--------|------|---------|----------|")
            for tc in op_cases:
                lines.append(f"| {tc.case_id} | {tc.priority} | {tc.scenario} | {tc.input_summary} | {tc.expected} |")

        lines.append("")

    return "\n".join(lines)


def _format_constraints(f: FieldInfo) -> str:
    parts: list[str] = []
    if f.enum:
        parts.append(f"enum: [{', '.join(str(v) for v in f.enum)}]")
    for c in f.constraints:
        kind, val = c.get("kind", ""), c.get("value", "")
        src = c.get("source", "")
        tag = "S" if src == "schema" else ""
        if kind == "enum":
            parts.append(f"[{', '.join(str(v) for v in val)}]")
        elif kind in ("maxLength", "maximum", "exclusiveMaximum"):
            parts.append(f"≤{val}{tag}")
        elif kind in ("minLength", "minimum", "exclusiveMinimum"):
            parts.append(f"≥{val}{tag}")
        elif kind == "maxItems":
            parts.append(f"maxItems={val}")
        elif kind == "minItems":
            parts.append(f"minItems={val}")
        elif kind == "pattern":
            parts.append(f"pattern=/{val[:20]}/")
        elif kind == "format":
            parts.append(f"fmt={val}")
        elif kind == "uniqueItems":
            parts.append("uniqueItems")
        elif kind == "default":
            parts.append(f"默认={val}")
        elif kind == "pattern_hint":
            parts.append(f"以{val}开头")
    if not parts and f.description:
        return f.description.split("；")[0].split("\n")[0][:50]
    return "; ".join(parts) if parts else "-"


def _constraints_source(f: FieldInfo) -> str:
    sources = set()
    if f.enum:
        sources.add("schema")
    for c in f.constraints:
        sources.add(c.get("source", "description"))
    return "/".join(sorted(sources)) if sources else "schema"


# ---------------------------------------------------------------------------
#  YAML output (mqapitest compatible)
# ---------------------------------------------------------------------------


def render_yaml_case(tc: TestCase, env_mapping: dict[str, str]) -> dict:
    path = tc.path
    for var, replacement in env_mapping.items():
        path = path.replace(f"{{{var}}}", replacement)

    step: dict[str, Any] = {"name": tc.scenario, "method": tc.method, "path": path}

    assertions: list[dict] = []
    if "401" in tc.expected:
        assertions.append({"field": "status_code", "operator": "==", "value": 401})
    elif "200" in tc.expected:
        assertions.append({"field": "status_code", "operator": "==", "value": 200})
        # Parse response field assertions from expected (e.g. "assert: foo != null, bar != null")
        m = re.search(r"assert:\s*(.+)", tc.expected)
        if m:
            for part in m.group(1).split(","):
                part = part.strip()
                if "!= null" in part:
                    fname = part.replace("!= null", "").strip()
                    assertions.append({"field": f"body.result.{fname}", "operator": "!=", "value": None})
    elif "400" in tc.expected:
        assertions.append({"field": "status_code", "operator": "==", "value": 400})
    elif "404" in tc.expected:
        assertions.append({"field": "status_code", "operator": "==", "value": 404})
    elif "409" in tc.expected:
        assertions.append({"field": "status_code", "operator": "in", "value": [200, 409]})
    step["assertions"] = assertions

    return {
        "test_id": tc.case_id,
        "description": tc.scenario,
        "priority": tc.priority,
        "tags": [tc.category, tc.operation_id],
        "steps": [step],
    }


# ---------------------------------------------------------------------------
#  Orchestrator
# ---------------------------------------------------------------------------


class APICaseGenerator:
    """Top-level orchestrator: parse → expand → extract → generate → output."""

    def __init__(self, config: AnalysisConfig | None = None) -> None:
        self._config = config or AnalysisConfig()
        self._resolver = ModelResolver(
            self._config.repo_root,
            version_dirs=self._config.ref_version_dirs,
        )
        self._analyzer = ServiceAnalyzer(self._resolver, self._config)
        self._case_gen = CaseGenerator(self._config)

    def analyze_service(self, service_path: str) -> tuple[ServiceAnalysis, dict[str, list[TestCase]]]:
        analysis = self._analyzer.analyze(service_path)
        cases_by_op: dict[str, list[TestCase]] = {}
        for op in analysis.operations:
            cases_by_op[op.operation_id] = self._case_gen.generate(op)
        return analysis, cases_by_op

    def analyze_product(self, product_dir: str) -> list[tuple[ServiceAnalysis, dict[str, list[TestCase]]]]:
        self._case_gen.reset()
        product_path = Path(product_dir)
        service_dir = product_path / "service"
        if not service_dir.exists():
            for candidate in product_path.iterdir():
                if candidate.is_dir() and (candidate / "service").exists():
                    service_dir = candidate / "service"
                    break

        if not service_dir.exists():
            log.error("No service/ directory found in %s", product_dir)
            return []

        results = []
        for svc_file in sorted(service_dir.glob("*.yaml")):
            try:
                result = self.analyze_service(str(svc_file))
                results.append(result)
            except Exception as e:
                log.error("Failed to analyze %s: %s", svc_file, e)
        return results

    def get_all_operations(
        self, results: list[tuple[ServiceAnalysis, dict[str, list[TestCase]]]],
    ) -> list[OperationAnalysis]:
        ops: list[OperationAnalysis] = []
        for analysis, _ in results:
            ops.extend(analysis.operations)
        return ops

    def write_markdown(
        self,
        result: tuple[ServiceAnalysis, dict[str, list[TestCase]]],
        output_dir: str,
        crud_chains: list[dict[str, Any]] | None = None,
    ) -> Path:
        analysis, cases_by_op = result
        md = render_markdown(analysis, cases_by_op, crud_chains=crud_chains)
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{analysis.file_name.replace('.yaml', '')}_cases.md"
        out_file.write_text(md, encoding="utf-8")
        return out_file

    def write_yaml(
        self,
        result: tuple[ServiceAnalysis, dict[str, list[TestCase]]],
        output_dir: str,
    ) -> list[Path]:
        analysis, cases_by_op = result
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        written: list[Path] = []

        for op_id, cases in cases_by_op.items():
            if not cases:
                continue
            yaml_cases = [render_yaml_case(tc, self._config.env_mapping) for tc in cases]
            out_file = out_dir / f"{op_id}_cases.yaml"
            with open(out_file, "w", encoding="utf-8") as f:
                yaml.dump(yaml_cases, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            written.append(out_file)

        return written

    def print_coverage(
        self,
        results: list[tuple[ServiceAnalysis, dict[str, list[TestCase]]]],
        crud_chains: list[dict[str, Any]] | None = None,
    ) -> None:
        total_ops = 0
        total_cases = 0
        by_priority: dict[str, int] = {}
        by_category: dict[str, int] = {}
        total_fields = 0
        fields_with_constraints = 0
        fields_needing_review = 0
        review_items: list[tuple[str, str, str]] = []

        for analysis, cases_by_op in results:
            total_ops += len(analysis.operations)
            for op in analysis.operations:
                all_fields = CaseGenerator._collect_all_fields(op)
                for f in all_fields:
                    if f.description:
                        total_fields += 1
                    if f.constraints or f.enum:
                        fields_with_constraints += 1
                    if f.unextracted_hints:
                        fields_needing_review += 1
                        review_items.append((op.operation_id, f.path, f.description[:60]))

            for op_id, cases in cases_by_op.items():
                total_cases += len(cases)
                for tc in cases:
                    by_priority[tc.priority] = by_priority.get(tc.priority, 0) + 1
                    by_category[tc.category] = by_category.get(tc.category, 0) + 1

        print(f"\n{'='*50}")
        print("  Coverage Report")
        print(f"{'='*50}")
        print(f"  Operations: {total_ops}")
        print(f"  Test cases: {total_cases}")
        print(f"  Avg per op: {total_cases / max(total_ops, 1):.1f}\n")

        print("  By priority:")
        for p in sorted(by_priority):
            print(f"    {p}: {by_priority[p]}")

        print("\n  By category:")
        for cat in sorted(by_category, key=lambda x: -by_category[x]):
            print(f"    {cat}: {by_category[cat]}")

        extraction_pct = fields_with_constraints * 100 // max(total_fields, 1)
        print(f"\n  Constraint extraction (script only):")
        print(f"    Fields with description:  {total_fields}")
        print(f"    Script extracted:         {fields_with_constraints} ({extraction_pct}%)")
        print(f"    Pending AI review:        {fields_needing_review}")
        no_constraint = total_fields - fields_with_constraints - fields_needing_review
        print(f"    Likely no constraint:     {max(no_constraint, 0)}")
        print(f"  ─────────────────────────────────────")
        print(f"  ★ Phase 5: AI 需逐字段阅读 description 补全约束")
        print(f"    目标: Pending AI review → 0")

        if crud_chains:
            print(f"\n  CRUD chains detected: {len(crud_chains)}")
            for chain in crud_chains:
                ops = [f"{k}={v}" for k, v in chain.items() if k != "resource"]
                print(f"    {chain['resource']}: {', '.join(ops)}")

        if review_items:
            print(f"\n  {'='*50}")
            print("  Fields pending AI review (Phase 5)")
            print(f"  {'='*50}")
            for op_id, fpath, desc in review_items[:10]:
                print(f"    {op_id}.{fpath}")
                print(f"      {desc}")
            if len(review_items) > 10:
                print(f"    ... and {len(review_items) - 10} more (run fallback for full list)")
        print()


# ---------------------------------------------------------------------------
#  Fallback report builder
# ---------------------------------------------------------------------------


def build_fallback_report(
    results: list[tuple[ServiceAnalysis, dict[str, list[TestCase]]]],
) -> str:
    lines: list[str] = []
    lines.append("# Fallback Review Report\n")
    lines.append("Fields whose description contains constraint hints that regex could not extract.")
    lines.append("Review each original description and supplement missing: enum values, ranges, formats, conditional deps, mutual exclusions.\n")
    lines.append("---\n")

    total = 0
    for analysis, cases_by_op in results:
        svc_items: list[tuple[str, FieldInfo]] = []
        for op in analysis.operations:
            for f in CaseGenerator._collect_all_fields(op):
                if f.unextracted_hints:
                    svc_items.append((op.operation_id, f))

        if not svc_items:
            continue

        lines.append(f"## {analysis.title} ({analysis.file_name})\n")
        for op_id, f in svc_items:
            total += 1
            hints = ", ".join(f.unextracted_hints[:4])
            desc_clean = f.description.replace("\n", " ").strip()
            lines.append(f"### {op_id} — `{f.path}` ({f.field_type})\n")
            lines.append(f"- **Hints**: {hints}")
            lines.append(f"- **Original description**: {desc_clean}")
            existing = _format_constraints(f) if f.constraints else "none"
            lines.append(f"- **Extracted constraints**: {existing}")
            lines.append(f"- **To check**: [ ] enum  [ ] range  [ ] format/encoding  [ ] conditional dep  [ ] mutual exclusive\n")

    lines.insert(3, f"**{total}** fields pending review.\n")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
#  LLM auto-supplement prompt builder
# ---------------------------------------------------------------------------


def build_llm_supplement_prompt(
    results: list[tuple[ServiceAnalysis, dict[str, list[TestCase]]]],
) -> str:
    """Build a structured prompt for LLM to supplement unextracted constraints.

    Output: JSON-parseable prompt that an LLM can respond to with structured
    test cases for each flagged field.
    """
    fields_to_review: list[dict[str, str]] = []

    for analysis, _ in results:
        for op in analysis.operations:
            for f in CaseGenerator._collect_all_fields(op):
                if not f.unextracted_hints:
                    continue
                fields_to_review.append({
                    "operation_id": op.operation_id,
                    "method": op.method,
                    "path": op.path,
                    "field_path": f.path,
                    "field_type": f.field_type,
                    "required": str(f.required),
                    "description": f.description,
                    "hints": ", ".join(f.unextracted_hints),
                    "existing_constraints": json.dumps(
                        [{"kind": c["kind"], "value": c["value"]} for c in f.constraints],
                        ensure_ascii=False,
                    ),
                })

    if not fields_to_review:
        return "No fields require AI review."

    prompt_parts: list[str] = [
        "You are an API testing expert. For each field below, the regex-based",
        "constraint extractor could not fully parse the description. Analyze the",
        "original description and output supplementary test cases.\n",
        "## Instructions\n",
        "For each field, output a JSON object with:",
        "- `field_path`: the field's dot-separated path",
        "- `operation_id`: the operation ID",
        "- `missing_constraints`: array of {kind, value, reason}",
        "- `test_cases`: array of {id, priority, scenario, input, expected}\n",
        "Priority: P0 (basic validation), P1 (boundary/edge), P2 (business logic)",
        "Constraint kinds: enum, range, format, conditional, file_type, encoding, unique\n",
        "## Fields to review\n",
        "```json",
        json.dumps(fields_to_review, indent=2, ensure_ascii=False),
        "```\n",
        "## Output format\n",
        "Return a JSON array of review results, one per field. Example:",
        "```json",
        json.dumps([{
            "field_path": "spec.name",
            "operation_id": "createFoo",
            "missing_constraints": [{"kind": "range", "value": "1-64 chars", "reason": "description says '不超过64个字符'"}],
            "test_cases": [
                {"id": "[AI] CF_R01", "priority": "P1", "scenario": "name exceeds 64 chars", "input": "name=65字符", "expected": "400"},
            ],
        }], indent=2, ensure_ascii=False),
        "```",
    ]
    return "\n".join(prompt_parts)


def parse_llm_supplement_response(response_text: str) -> list[dict]:
    """Parse LLM JSON response into structured supplement results."""
    json_match = re.search(r"```(?:json)?\s*\n(.*?)\n```", response_text, re.DOTALL)
    raw = json_match.group(1) if json_match else response_text
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return data
        return [data]
    except json.JSONDecodeError as e:
        log.error("Failed to parse LLM response as JSON: %s", e)
        return []


def merge_supplement_to_markdown(md_path: str, supplements: list[dict]) -> int:
    """Merge LLM-supplemented test cases back into a Markdown test report.

    Appends [AI-review] cases to the matching operation's test case table.
    Returns the number of cases merged.
    """
    path = Path(md_path)
    if not path.exists():
        log.error("Markdown file not found: %s", md_path)
        return 0

    content = path.read_text(encoding="utf-8")
    merged = 0

    for item in supplements:
        op_id = item.get("operation_id", "")
        test_cases = item.get("test_cases", [])
        if not op_id or not test_cases:
            continue

        marker = f"## {op_id} ("
        if marker not in content:
            log.warning("Operation %s not found in %s", op_id, md_path)
            continue

        # Find the last row of this operation's test case table
        # Pattern: look for the table under this operation
        op_start = content.index(marker)
        # Find next operation or end of file
        next_op = content.find("\n## ", op_start + len(marker))
        section = content[op_start:next_op] if next_op != -1 else content[op_start:]

        # Find last table row in the section
        table_rows = [i for i, line in enumerate(section.split("\n")) if line.startswith("|") and not line.startswith("|--")]
        if not table_rows:
            continue

        lines = content.split("\n")
        # Calculate absolute line position
        section_start_line = content[:op_start].count("\n")
        insert_after = section_start_line + table_rows[-1]

        new_rows: list[str] = []
        for tc in test_cases:
            tc_id = tc.get("id", f"[AI-review] {op_id}")
            prio = tc.get("priority", "P1")
            scenario = tc.get("scenario", "")
            inp = tc.get("input", "")
            exp = tc.get("expected", "")
            new_rows.append(f"| {tc_id} | {prio} | {scenario} | {inp} | {exp} |")
            merged += 1

        for i, row in enumerate(new_rows):
            lines.insert(insert_after + 1 + i, row)
        content = "\n".join(lines)

    path.write_text(content, encoding="utf-8")
    return merged


# ---------------------------------------------------------------------------
#  CLI
# ---------------------------------------------------------------------------


def _infer_repo_root(args: object) -> str:
    """Auto-detect repo root from service/product-dir path.

    For multi-file specs like JCloud (<repo>/<module>/v1/service/Xxx.yaml),
    walk up from the given path until we find a directory containing 2+
    subdirectories that each have a versioned subdir (v1/, v2/, etc.).
    """
    seed = Path(getattr(args, "service", "") or getattr(args, "product_dir", "") or "")
    if not seed.exists():
        return ""
    seed = seed.resolve()
    candidate = seed if seed.is_dir() else seed.parent
    for _ in range(6):
        candidate = candidate.parent
        if not candidate or candidate == candidate.parent:
            break
        versioned = [d for d in candidate.iterdir()
                     if d.is_dir() and any((d / v).is_dir() for v in ("v1", "v2", "v3"))]
        if len(versioned) >= 2:
            log.info("Auto-detected repo root: %s", candidate)
            return str(candidate)
    return ""


def main():
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    parser = argparse.ArgumentParser(
        description="API Test Case Generator — from OpenAPI specs to test design matrices",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    sub = parser.add_subparsers(dest="command")

    # -- analyze --
    p_analyze = sub.add_parser("analyze", help="Analyze a single service file")
    p_analyze.add_argument("--service", "-s", required=True, help="Service YAML path")
    p_analyze.add_argument("--repo-root", "-r", default="", help="Multi-file spec repo root")
    p_analyze.add_argument("--output", "-o", default="./cases", help="Output directory")
    p_analyze.add_argument("--format", "-f", default="both", choices=["markdown", "yaml", "both"])
    p_analyze.add_argument("--config", "-c", help="Config file path")
    p_analyze.add_argument("--no-slim", action="store_true", help="Disable slim mode (emit all cases)")

    # -- analyze-all --
    p_all = sub.add_parser("analyze-all", help="Analyze all services in a product directory")
    p_all.add_argument("--product-dir", "-d", required=True, help="Product v1/ directory")
    p_all.add_argument("--repo-root", "-r", default="", help="Multi-file spec repo root")
    p_all.add_argument("--output", "-o", default="./cases", help="Output directory")
    p_all.add_argument("--format", "-f", default="both", choices=["markdown", "yaml", "both"])
    p_all.add_argument("--config", "-c", help="Config file path")
    p_all.add_argument("--no-slim", action="store_true", help="Disable slim mode")

    # -- coverage --
    p_cov = sub.add_parser("coverage", help="Print coverage statistics")
    p_cov.add_argument("--product-dir", "-d", required=True)
    p_cov.add_argument("--repo-root", "-r", default="")
    p_cov.add_argument("--config", "-c", help="Config file path")

    # -- fallback --
    p_fb = sub.add_parser("fallback", help="Output fallback review report for fields needing AI review")
    p_fb.add_argument("--product-dir", "-d", required=True, help="Product v1/ directory")
    p_fb.add_argument("--repo-root", "-r", default="", help="Multi-file spec repo root")
    p_fb.add_argument("--output", "-o", default="", help="Output file path (stdout if empty)")
    p_fb.add_argument("--config", "-c", help="Config file path")

    # -- auto-supplement --
    p_supp = sub.add_parser("auto-supplement", help="Generate LLM prompt for automated constraint supplementation")
    p_supp.add_argument("--product-dir", "-d", required=True, help="Product v1/ directory")
    p_supp.add_argument("--repo-root", "-r", default="", help="Multi-file spec repo root")
    p_supp.add_argument("--output", "-o", default="", help="Output file (stdout if empty)")
    p_supp.add_argument("--config", "-c", help="Config file path")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger("api-case-gen").setLevel(logging.DEBUG)

    if not args.command:
        parser.print_help()
        sys.exit(EXIT_BAD_ARGS)

    config = AnalysisConfig.from_file(args.config) if getattr(args, "config", None) else AnalysisConfig()
    if hasattr(args, "repo_root") and args.repo_root:
        config.repo_root = args.repo_root
    elif not config.repo_root:
        config.repo_root = _infer_repo_root(args)
    if hasattr(args, "format"):
        config.output_format = args.format
    if getattr(args, "no_slim", False):
        config.slim_path_params = False
        config.slim_empty_string = False

    gen = APICaseGenerator(config)

    if args.command == "analyze":
        if not Path(args.service).exists():
            log.error("Service file not found: %s", args.service)
            sys.exit(EXIT_PARSE_ERROR)

        result = gen.analyze_service(args.service)
        analysis, cases_by_op = result
        total = sum(len(c) for c in cases_by_op.values())
        print(f"Done: {analysis.title} — {len(analysis.operations)} operations, {total} cases")

        crud = detect_crud_chains([op for op in analysis.operations])
        if config.output_format in ("markdown", "both"):
            md_path = gen.write_markdown(result, args.output, crud_chains=crud)
            print(f"  Markdown: {md_path}")
        if config.output_format in ("yaml", "both"):
            yaml_paths = gen.write_yaml(result, args.output)
            print(f"  YAML: {len(yaml_paths)} files → {args.output}")

    elif args.command == "analyze-all":
        if not Path(args.product_dir).exists():
            log.error("Product directory not found: %s", args.product_dir)
            sys.exit(EXIT_PARSE_ERROR)

        results = gen.analyze_product(args.product_dir)
        if not results:
            log.error("No service files found")
            sys.exit(EXIT_PARSE_ERROR)

        all_ops = gen.get_all_operations(results)
        crud_chains = detect_crud_chains(all_ops)

        for analysis, cases_by_op in results:
            total = sum(len(c) for c in cases_by_op.values())
            print(f"  {analysis.file_name}: {len(analysis.operations)} ops, {total} cases")

            if config.output_format in ("markdown", "both"):
                gen.write_markdown((analysis, cases_by_op), args.output, crud_chains=crud_chains)
            if config.output_format in ("yaml", "both"):
                gen.write_yaml((analysis, cases_by_op), args.output)

        gen.print_coverage(results, crud_chains=crud_chains)

    elif args.command == "coverage":
        results = gen.analyze_product(args.product_dir)
        all_ops = gen.get_all_operations(results)
        crud_chains = detect_crud_chains(all_ops)
        gen.print_coverage(results, crud_chains=crud_chains)

    elif args.command == "fallback":
        results = gen.analyze_product(args.product_dir)
        report = build_fallback_report(results)
        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(report, encoding="utf-8")
            print(f"Fallback report written: {out_path}")
        else:
            print(report)

    elif args.command == "auto-supplement":
        results = gen.analyze_product(args.product_dir)
        prompt = build_llm_supplement_prompt(results)
        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(prompt, encoding="utf-8")
            print(f"LLM supplement prompt written: {out_path}")
            print(f"  Feed this to your LLM and pass the response to `parse_llm_supplement_response()`")
        else:
            print(prompt)


if __name__ == "__main__":
    main()
