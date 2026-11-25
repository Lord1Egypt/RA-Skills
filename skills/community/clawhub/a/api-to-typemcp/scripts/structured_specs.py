"""Strict OpenAPI 3.x and Swagger 2.0 normalization for local supplied files."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from manifest import MANIFEST_SCHEMA, MANIFEST_VERSION, add_digest
from policy import classify_method


class StructuredSpecError(ValueError):
    """A user-safe unsupported or malformed structured specification error."""


_SUPPORTED_METHODS = ("get", "head", "options", "post", "put", "patch", "delete")
_UNSUPPORTED_METHOD_KEYS = frozenset({"trace", "connect"})
_OPERATION_ID = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,127}$")
_PATH_TEMPLATE = re.compile(
    r"^/(?:[^/?#{}]+|\{[A-Za-z][A-Za-z0-9_.-]{0,127}\})*"
    r"(?:/(?:[^/?#{}]+|\{[A-Za-z][A-Za-z0-9_.-]{0,127}\})*)*$"
)
_TEMPLATE_VAR = re.compile(r"\{([A-Za-z][A-Za-z0-9_.-]{0,127})\}")
_JSON_TYPES = frozenset({"string", "number", "integer", "boolean", "array", "object"})
_OPENAPI_AUTH_TYPES = frozenset({"apiKey", "http", "oauth2", "openIdConnect"})
_SWAGGER_AUTH_TYPES = frozenset({"basic", "apiKey", "oauth2"})
_AUTH_SCHEME_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,127}$")
_MAX_STRUCTURE_DEPTH = 64
_MAX_STRUCTURE_NODES = 10_000


def _check_encodable(value: str) -> None:
    """Reject strings that cannot round-trip through UTF-8 (e.g. lone surrogates)."""
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise StructuredSpecError("specification contains invalid Unicode text") from exc


def _validate_untrusted_structure(
    value: Any,
    *,
    seen: set[int] | None = None,
    depth: int = 0,
    nodes: list[int] | None = None,
) -> None:
    """Bound an untrusted parsed tree before normalization or deterministic sorting.

    PyYAML aliases may share Python objects or form recursive graphs. Identity
    tracking prevents alias fan-out from being repeatedly traversed, while depth
    and node caps fail closed for structurally oversized documents. Every string
    (value and mapping key) is checked for UTF-8 encodability so lone surrogates
    cannot reach canonical JSON encoding.
    """
    if depth > _MAX_STRUCTURE_DEPTH:
        raise StructuredSpecError("specification nesting exceeds the safe limit")
    if isinstance(value, str):
        _check_encodable(value)
        return
    if not isinstance(value, (dict, list)):
        return
    seen = set() if seen is None else seen
    nodes = [0] if nodes is None else nodes
    identity = id(value)
    if identity in seen:
        return
    seen.add(identity)
    nodes[0] += 1
    if nodes[0] > _MAX_STRUCTURE_NODES:
        raise StructuredSpecError("specification structure exceeds the safe limit")
    if isinstance(value, dict):
        for key, nested in value.items():
            if not isinstance(key, str):
                raise StructuredSpecError("specification object keys must be strings")
            _check_encodable(key)
            if key == "$ref":
                raise StructuredSpecError("$ref is not supported for local normalization")
            _validate_untrusted_structure(nested, seen=seen, depth=depth + 1, nodes=nodes)
    else:
        for nested in value:
            _validate_untrusted_structure(nested, seen=seen, depth=depth + 1, nodes=nodes)


def _safe_base_url(raw: object) -> str:
    if not isinstance(raw, str) or not raw:
        return ""
    try:
        parsed = urlsplit(raw)
        port = parsed.port
    except ValueError as exc:
        raise StructuredSpecError("base URL is malformed") from exc
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
        raise StructuredSpecError("base URL must be an http(s) URL without credentials")
    netloc = parsed.hostname
    if port:
        netloc += f":{port}"
    path = parsed.path.rstrip("/")
    return urlunsplit((parsed.scheme, netloc, path, "", ""))


def _swagger_base_url(document: dict[str, Any]) -> str:
    host = document.get("host")
    if not isinstance(host, str) or not host or any(char in host for char in "@/?#"):
        raise StructuredSpecError("Swagger host must be a hostname")
    schemes = document.get("schemes", ["https"])
    if not isinstance(schemes, list) or not schemes or schemes[0] not in {"http", "https"}:
        raise StructuredSpecError("Swagger schemes must begin with http or https")
    base_path = document.get("basePath", "")
    if not isinstance(base_path, str) or (base_path and not base_path.startswith("/")):
        raise StructuredSpecError("Swagger basePath must be an absolute path")
    return _safe_base_url(f"{schemes[0]}://{host}{base_path}")


def _safe_descriptor(raw: object) -> str:
    """Return an approved constant provenance label without local filenames."""
    allowed = frozenset({
        "local-structured-spec",
        "local-markdown-document",
        "local-html-document",
        "swagger-ui-config",
    })
    if not isinstance(raw, str) or raw not in allowed:
        raise StructuredSpecError("source descriptor is invalid")
    return raw


def _required_flag(value: object) -> bool:
    if not isinstance(value, bool):
        raise StructuredSpecError("required must be a boolean")
    return value


def _parameters(values: object, swagger: bool) -> list[dict[str, Any]]:
    if values is None:
        return []
    if not isinstance(values, list):
        raise StructuredSpecError("parameters must be an array")
    normalized: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for parameter in values:
        if not isinstance(parameter, dict):
            raise StructuredSpecError("parameter must be an object")
        name, location = parameter.get("name"), parameter.get("in")
        if not isinstance(name, str) or not name or not isinstance(location, str) or location not in {"path", "query", "header", "cookie", "body"}:
            raise StructuredSpecError("parameter name or location is invalid")
        if (name, location) in seen:
            raise StructuredSpecError("duplicate parameter")
        seen.add((name, location))
        if location == "body":
            continue
        schema = parameter.get("schema", {}) if not swagger else {"type": parameter.get("type", "string")}
        if not isinstance(schema, dict):
            raise StructuredSpecError("parameter schema must be an object")
        schema_type = schema.get("type", "string")
        if not isinstance(schema_type, str) or schema_type not in _JSON_TYPES:
            raise StructuredSpecError("parameter schema type is unsupported")
        item = {"name": name, "in": location, "required": _required_flag(parameter.get("required", False)), "type": schema_type}
        normalized.append(item)
    return sorted(normalized, key=lambda item: (item["in"], item["name"]))


def _request_body(operation: dict[str, Any], swagger: bool) -> dict[str, Any] | None:
    if swagger:
        bodies = [item for item in operation.get("parameters", []) if isinstance(item, dict) and item.get("in") == "body"]
        if not bodies:
            return None
        if len(bodies) != 1:
            raise StructuredSpecError("operation has multiple body parameters")
        schema = bodies[0].get("schema")
        if not isinstance(schema, dict):
            raise StructuredSpecError("body parameter schema must be an object")
        schema_type = schema.get("type", "object")
        if not isinstance(schema_type, str) or schema_type not in _JSON_TYPES:
            raise StructuredSpecError("body parameter schema type is unsupported")
        return {"required": _required_flag(bodies[0].get("required", False)), "contentType": "application/json", "type": schema_type}
    body = operation.get("requestBody")
    if body is None:
        return None
    if not isinstance(body, dict) or not isinstance(body.get("content"), dict) or not body["content"]:
        raise StructuredSpecError("requestBody must have content")
    content_type = sorted(body["content"])[0]
    media = body["content"][content_type]
    if not isinstance(media, dict) or not isinstance(media.get("schema", {}), dict):
        raise StructuredSpecError("requestBody media schema must be an object")
    schema_type = media.get("schema", {}).get("type", "object")
    if not isinstance(schema_type, str) or schema_type not in _JSON_TYPES:
        raise StructuredSpecError("requestBody media schema type is unsupported")
    return {"required": _required_flag(body.get("required", False)), "contentType": content_type, "type": schema_type}


def _responses(values: object) -> list[dict[str, str]]:
    if not isinstance(values, dict) or not values:
        raise StructuredSpecError("operation responses must be an object")
    result: list[dict[str, str]] = []
    for status, response in values.items():
        if not isinstance(status, str) or not re.fullmatch(r"(?:[1-5]\d\d|default)", status) or not isinstance(response, dict):
            raise StructuredSpecError("response is invalid")
        result.append({"status": status, "summary": f"HTTP {status} response"})
    return sorted(result, key=lambda response: response["status"])


def _authentication(document: dict[str, Any], swagger: bool) -> list[dict[str, str]]:
    """Normalize security scheme names and types; never include secrets or values."""
    if swagger:
        definitions = document.get("securityDefinitions")
        allowed_types = _SWAGGER_AUTH_TYPES
    else:
        components = document.get("components")
        definitions = components.get("securitySchemes") if isinstance(components, dict) else None
        allowed_types = _OPENAPI_AUTH_TYPES
    if definitions is None:
        return []
    if not isinstance(definitions, dict):
        raise StructuredSpecError("security definitions must be an object")
    result: list[dict[str, str]] = []
    for name in sorted(definitions):
        definition = definitions[name]
        if not isinstance(name, str) or not _AUTH_SCHEME_NAME.fullmatch(name):
            raise StructuredSpecError("security scheme name is invalid")
        if not isinstance(definition, dict):
            raise StructuredSpecError("security scheme must be an object")
        scheme_type = definition.get("type")
        if not isinstance(scheme_type, str) or scheme_type not in allowed_types:
            raise StructuredSpecError("security scheme type is unsupported")
        entry: dict[str, str] = {"name": name, "type": scheme_type}
        if scheme_type == "apiKey":
            location = definition.get("in")
            if not isinstance(location, str) or location not in {"header", "query"}:
                raise StructuredSpecError("apiKey scheme must specify in as header or query")
            entry["in"] = location
            param_name = definition.get("name")
            if not isinstance(param_name, str) or not param_name:
                raise StructuredSpecError("apiKey scheme must specify a parameter name")
            entry["parameterName"] = param_name
        elif scheme_type == "http":
            scheme = definition.get("scheme")
            if not isinstance(scheme, str) or scheme not in {"basic", "bearer"}:
                raise StructuredSpecError("http scheme must specify basic or bearer")
            entry["scheme"] = scheme
        # oauth2, openIdConnect, basic: name and type only — no URLs, flows, or values.
        result.append(entry)
    return result


def _validate_path_template(path: str, parameters: list[dict[str, Any]]) -> None:
    """Ensure every template variable has a matching required path parameter."""
    template_vars = sorted(set(_TEMPLATE_VAR.findall(path)))
    path_params = [p for p in parameters if p["in"] == "path"]
    declared = {p["name"] for p in path_params}
    for var in template_vars:
        if var not in declared:
            raise StructuredSpecError(f"path template variable {{{var}}} has no declared path parameter")
    for param in path_params:
        if not param["required"]:
            raise StructuredSpecError(f"path parameter {param['name']} must be required")
        if param["name"] not in template_vars:
            raise StructuredSpecError(f"path parameter {param['name']} does not match any template variable")


def build_manifest(document: dict[str, Any], descriptor: str) -> dict[str, Any]:
    """Validate and normalize one OpenAPI 3.x or Swagger 2.0 document."""
    _validate_untrusted_structure(document)
    if isinstance(document.get("openapi"), str) and document["openapi"].startswith("3."):
        kind, swagger = "openapi", False
        servers = document.get("servers", [])
        if not isinstance(servers, list) or not servers or not isinstance(servers[0], dict):
            raise StructuredSpecError("OpenAPI document must declare a server")
        base_url = _safe_base_url(servers[0].get("url"))
    elif document.get("swagger") == "2.0":
        kind, swagger = "swagger", True
        base_url = _swagger_base_url(document)
    else:
        raise StructuredSpecError("only OpenAPI 3.x and Swagger 2.0 are supported")

    authentication = _authentication(document, swagger)

    paths = document.get("paths")
    if not isinstance(paths, dict) or not paths:
        raise StructuredSpecError("specification paths must be a non-empty object")
    operations: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for path in sorted(paths):
        item = paths[path]
        if not isinstance(path, str) or not _PATH_TEMPLATE.fullmatch(path) or not isinstance(item, dict):
            raise StructuredSpecError("path item is invalid")
        for key in item:
            if key in _UNSUPPORTED_METHOD_KEYS:
                raise StructuredSpecError(f"HTTP method {key.upper()} is not supported for manifest generation")
        common_parameters = item.get("parameters", [])
        for method in _SUPPORTED_METHODS:
            operation = item.get(method)
            if operation is None:
                continue
            if not isinstance(operation, dict):
                raise StructuredSpecError("operation must be an object")
            operation_id = operation.get("operationId")
            if not isinstance(operation_id, str) or not _OPERATION_ID.fullmatch(operation_id) or operation_id in seen_ids:
                raise StructuredSpecError("operationId must be unique and stable")
            seen_ids.add(operation_id)
            operation_parameters = operation.get("parameters", [])
            if not isinstance(common_parameters, list) or not isinstance(operation_parameters, list):
                raise StructuredSpecError("parameters must be an array")
            parameters = _parameters(common_parameters + operation_parameters, swagger)
            _validate_path_template(path, parameters)
            raw_evidence = operation.get("x-api-to-typemcp-evidence")
            document_source = descriptor in {"local-markdown-document", "local-html-document"}
            if document_source and (
                isinstance(raw_evidence, dict)
                and isinstance(raw_evidence.get("line"), int)
                and raw_evidence["line"] > 0
                and raw_evidence.get("confidence") == "explicit"
            ):
                # Reconstruct evidence only from normalized operation fields;
                # never persist arbitrary supplied prose or extension snippets.
                evidence = {
                    "source": "document",
                    "line": raw_evidence["line"],
                    "snippet": f"{method.upper()} {path}",
                }
                confidence: str | None = "explicit"
            else:
                evidence = {"source": "structured-spec"}
                confidence = None
            item_value: dict[str, Any] = {
                "operationId": operation_id,
                "method": method.upper(),
                "path": path,
                "parameters": parameters,
                "requestBody": _request_body(operation, swagger),
                "responses": _responses(operation.get("responses")),
                "evidence": evidence,
                "confidence": confidence,
                "status": "ready",
                "policy": classify_method(method),
            }
            operations.append(item_value)
    if not operations:
        raise StructuredSpecError("specification contains no supported operations")
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "version": MANIFEST_VERSION,
        "protocol": "http",
        "source": {"kind": kind, "descriptor": _safe_descriptor(descriptor)},
        "baseUrl": base_url,
        "authentication": authentication,
        "operations": operations,
    }
    return add_digest(manifest)
