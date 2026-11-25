"""Render TypeMCP stdio projects from approved manifests.

Every generated project depends only on the published ``@theorvane/type-mcp``
npm package (never ``file:``, ``git:``, or copied source).  Operation-specific
TypeScript is emitted programmatically with strict identifier escaping;
fixed-infrastructure files come from ``templates/typescript-stdio/``.
"""

from __future__ import annotations

import json
import re
import string
from pathlib import Path
from typing import Any, Callable

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates" / "typescript-stdio"

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def render_project(manifest: dict[str, Any], output_dir: Path) -> list[str]:
    """Render a complete TypeMCP stdio project into *output_dir*.

    Returns a sorted list of relative POSIX paths that were written.
    """
    project_name = _project_name(manifest)
    server_class = _pascal_case(project_name) + "Server"
    operations: list[dict[str, Any]] = manifest.get("operations", [])
    env_vars = _env_var_names(manifest)

    written: list[str] = []

    def write(rel: str, content: str) -> None:
        path = output_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append(rel)

    # --- Template-rendered files -------------------------------------------
    _tpl("package.json.tmpl", write, "package.json", {"PROJECT_NAME": project_name})
    _tpl("package-lock.json.tmpl", write, "package-lock.json", {"PROJECT_NAME": project_name})
    _tpl("tsconfig.json.tmpl", write, "tsconfig.json", {})
    _tpl("src/index.ts.tmpl", write, "src/index.ts", {"SERVER_CLASS": server_class})
    _tpl("src/api-client.ts.tmpl", write, "src/api-client.ts", {})
    _tpl("src/policy.ts.tmpl", write, "src/policy.ts", {})
    _tpl("README.md.tmpl", write, "README.md", {
        "PROJECT_NAME": project_name,
        "OPERATION_COUNT": str(len(operations)),
        "OPERATION_LIST": _operation_list_md(operations),
    })
    _tpl(".env.example.tmpl", write, ".env.example", {
        "ENV_VARS": "\n".join(env_vars),
    })

    # --- Programmatically generated files ----------------------------------
    write("src/operations.ts", _operations_ts(operations))
    write("src/schemas.ts", _schemas_ts(operations))
    write("src/server.ts", _server_ts(operations, server_class, project_name))
    write("test/policy.test.ts", _policy_test_ts())
    write("test/server.test.ts", _server_test_ts(server_class))

    # --- Manifest copy (canonical, secret-free) ----------------------------
    write(
        "api-to-typemcp.manifest.json",
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
    )

    return sorted(written)


# ---------------------------------------------------------------------------
# Template helpers
# ---------------------------------------------------------------------------


def _tpl(
    template_name: str,
    write: Callable[[str, str], None],
    rel_path: str,
    variables: dict[str, str],
) -> None:
    template_path = TEMPLATES_DIR / template_name
    text = template_path.read_text(encoding="utf-8")
    rendered = string.Template(text).safe_substitute(variables)
    write(rel_path, rendered)


# ---------------------------------------------------------------------------
# Naming / identifier helpers
# ---------------------------------------------------------------------------


def _project_name(manifest: dict[str, Any]) -> str:
    base_url = manifest.get("baseUrl", "")
    match = re.search(r"https?://([^/:]+)", base_url)
    if match:
        host = match.group(1).split(".")[0]
        name = _kebab_case(host) + "-mcp"
        if re.match(r"^[a-z]", name):
            return name
    return "generated-mcp-server"


def _kebab_case(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()
    return s or "generated"


def _pascal_case(name: str) -> str:
    parts = re.split(r"[-_]+", name)
    return "".join(p.capitalize() for p in parts if p) or "Generated"


# TypeScript reserved words that must not be emitted as identifiers.
_TS_RESERVED = frozenset({
    "abstract", "any", "as", "asserts", "async", "await", "bigint", "boolean",
    "break", "case", "catch", "class", "const", "continue", "debugger",
    "declare", "default", "delete", "do", "else", "enum", "export", "extends",
    "false", "finally", "for", "from", "function", "get", "if", "implements",
    "import", "in", "infer", "instanceof", "interface", "is", "keyof", "let",
    "module", "namespace", "never", "new", "null", "number", "object", "of",
    "package", "private", "protected", "public", "readonly", "require",
    "return", "set", "static", "string", "super", "switch", "symbol", "this",
    "throw", "true", "try", "type", "typeof", "undefined", "unique", "unknown",
    "var", "void", "while", "with", "yield",
})


def _safe_identifier(name: str) -> str:
    """Convert an arbitrary string to a valid TypeScript identifier."""
    ident = re.sub(r"[^a-zA-Z0-9_$]", "_", name)
    if ident and ident[0].isdigit():
        ident = f"_{ident}"
    ident = ident or "_unnamed"
    if ident in _TS_RESERVED:
        ident = f"_{ident}"
    return ident


def _unique_identifiers(names: list[str]) -> dict[str, str]:
    """Map raw names to collision-free TypeScript identifiers."""
    result: dict[str, str] = {}
    seen: set[str] = set()
    for name in names:
        base = _safe_identifier(name)
        candidate = base
        counter = 1
        while candidate in seen:
            candidate = f"{base}_{counter}"
            counter += 1
        seen.add(candidate)
        result[name] = candidate
    return result


# ---------------------------------------------------------------------------
# Zod type mapping
# ---------------------------------------------------------------------------

_ZOD_TYPES: dict[str, str] = {
    "string": "z.string()",
    "integer": "z.number().int()",
    "number": "z.number()",
    "boolean": "z.boolean()",
}


def _zod_type(param_type: str) -> str:
    return _ZOD_TYPES.get(param_type, "z.string()")


# ---------------------------------------------------------------------------
# Environment variable names
# ---------------------------------------------------------------------------


def _env_var_names(manifest: dict[str, Any]) -> list[str]:
    names = ["TYPE_MCP_BASE_URL", "TYPE_MCP_ALLOW_PROTECTED_OPERATIONS"]
    for scheme in manifest.get("authentication", []):
        raw = scheme.get("name", "") if isinstance(scheme, dict) else str(scheme)
        safe = _safe_identifier(raw).upper()
        names.append(f"TYPE_MCP_AUTH_{safe}")
    return names


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------


def _operation_list_md(operations: list[dict[str, Any]]) -> str:
    if not operations:
        return "_No operations._"
    lines: list[str] = []
    for op in operations:
        method = op.get("method", "?")
        path = op.get("path", "?")
        oid = op.get("operationId", "?")
        policy = op.get("policy", "?")
        lines.append(f"- `{method} {path}` — **{oid}** ({policy})")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Generated TypeScript — operations.ts
# ---------------------------------------------------------------------------


def _operations_ts(operations: list[dict[str, Any]]) -> str:
    lines = [
        "// Auto-generated by api-to-typemcp. Do not edit.",
        "",
        "export interface OperationDescriptor {",
        "  operationId: string;",
        "  method: string;",
        "  path: string;",
        '  policy: "read" | "protected-write" | "deny";',
        "}",
        "",
        "export const operations: OperationDescriptor[] = [",
    ]
    for op in operations:
        oid = json.dumps(op.get("operationId", ""))
        method = json.dumps(op.get("method", ""))
        path = json.dumps(op.get("path", ""))
        policy = json.dumps(op.get("policy", "deny"))
        lines.append(
            f"  {{ operationId: {oid}, method: {method}, path: {path}, policy: {policy} }},"
        )
    lines.append("];")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Generated TypeScript — schemas.ts
# ---------------------------------------------------------------------------


def _schemas_ts(operations: list[dict[str, Any]]) -> str:
    lines = [
        "// Auto-generated by api-to-typemcp. Do not edit.",
        "",
        'import { z } from "zod";',
        "",
    ]
    ids = _unique_identifiers([op.get("operationId", "") for op in operations])
    for op in operations:
        name = ids[op.get("operationId", "")]
        schema_name = f"{name}Input"
        lines.append(f"export const {schema_name} = z.object({{")
        for param in op.get("parameters", []):
            pname = _safe_identifier(param.get("name", ""))
            ptype = _zod_type(param.get("type", "string"))
            if not param.get("required", False):
                ptype += ".optional()"
            lines.append(f"  {pname}: {ptype},")
        body = op.get("requestBody")
        if body and body.get("type") == "object":
            lines.append("  body: z.record(z.string(), z.unknown()),")
        lines.append("});")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Generated TypeScript — server.ts
# ---------------------------------------------------------------------------


def _server_ts(
    operations: list[dict[str, Any]],
    server_class: str,
    project_name: str,
) -> str:
    ids = _unique_identifiers([op.get("operationId", "") for op in operations])
    schema_imports = ", ".join(
        f"{ids[op.get('operationId', '')]}Input" for op in operations
    )

    lines: list[str] = [
        "// Auto-generated by api-to-typemcp. Do not edit.",
        "",
        'import { McpServer, McpTool } from "@theorvane/type-mcp";',
        'import { z } from "zod";',
        'import { authorizeOperation } from "./policy.js";',
        'import { ApiClient } from "./api-client.js";',
        'import { operations } from "./operations.js";',
        f'import {{ {schema_imports} }} from "./schemas.js";',
        "",
        "// Tool result envelope",
        "const toolResult = z.object({",
        '  content: z.array(z.object({ type: z.literal("text"), text: z.string() })),',
        "});",
        "",
        f"@McpServer({{ name: {json.dumps(project_name)}, version: \"1.0.0\" }})",
        f"export class {server_class} {{",
        '  private client = new ApiClient(process.env.TYPE_MCP_BASE_URL ?? "");',
        "",
    ]

    for op in operations:
        name = ids[op.get("operationId", "")]
        oid = op.get("operationId", "")
        method = op.get("method", "")
        path = op.get("path", "")
        policy = op.get("policy", "deny")
        schema_name = f"{name}Input"
        desc = f"{method} {path}"

        lines.append(
            f"  @McpTool({{ name: {json.dumps(oid)}, description: {json.dumps(desc)}, input: {schema_name} }})"
        )
        lines.append(
            f"  async {name}(input: z.infer<typeof {schema_name}>) {{"
        )
        lines.append(
            f"    const op = operations.find((o) => o.operationId === {json.dumps(oid)});"
        )
        lines.append(f'    if (!op) throw new Error("Unknown operation: {oid}");')
        lines.append("    authorizeOperation(op.operationId, op.policy);")

        if policy == "deny":
            lines.append(
                f'    throw new Error("Operation {oid} is denied by policy.");'
            )
        else:
            path_expr = _path_expression(path, op.get("parameters", []))
            query_params = [
                p for p in op.get("parameters", []) if p.get("in") == "query"
            ]

            lines.append(
                f"    const result = await this.client.request({json.dumps(method)}, {path_expr}, {{"
            )
            if query_params:
                qparts = ", ".join(
                    f"{json.dumps(p.get('name', ''))}: String(input.{_safe_identifier(p.get('name', ''))} ?? \"\")"
                    for p in query_params
                )
                lines.append(f"      query: {{ {qparts} }},")
            if op.get("requestBody"):
                lines.append("      body: input.body,")
            lines.append("    });")
            lines.append(
                '    const text = typeof result === "string" ? result : JSON.stringify(result);'
            )
            lines.append(
                '    return toolResult.parse({ content: [{ type: "text" as const, text }] });'
            )

        lines.append("  }")
        lines.append("")

    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def _path_expression(path: str, parameters: list[dict[str, Any]]) -> str:
    """Return a TypeScript expression for the request path.

    If the path contains ``{param}`` templates, emit a template literal with
    ``encodeURIComponent`` wrapping.  Otherwise return a plain string literal.
    """
    path_params = [p for p in parameters if p.get("in") == "path"]
    if not path_params:
        return json.dumps(path)

    # Build a JS template literal: `/pets/${encodeURIComponent(String(input.petId))}`
    parts = path.split("{")
    result = "`" + parts[0]
    for part in parts[1:]:
        param_name, _, rest = part.partition("}")
        safe = _safe_identifier(param_name)
        result += "${encodeURIComponent(String(input." + safe + "))}" + rest
    result += "`"
    return result


# ---------------------------------------------------------------------------
# Generated TypeScript — test files
# ---------------------------------------------------------------------------


def _policy_test_ts() -> str:
    return "\n".join([
        "// Auto-generated by api-to-typemcp. Do not edit.",
        "",
        'import { describe, it, expect, afterEach } from "vitest";',
        'import { authorizeOperation } from "../src/policy.js";',
        "",
        'describe("authorizeOperation", () => {',
        "  afterEach(() => {",
        '    delete process.env.TYPE_MCP_ALLOW_PROTECTED_OPERATIONS;',
        "  });",
        "",
        '  it("allows read operations without env config", () => {',
        '    expect(() => authorizeOperation("listPets", "read")).not.toThrow();',
        "  });",
        "",
        '  it("denies operations with deny policy", () => {',
        '    expect(() => authorizeOperation("x", "deny")).toThrow(/denied/);',
        "  });",
        "",
        '  it("rejects wildcards in protected-write allowlist", () => {',
        '    process.env.TYPE_MCP_ALLOW_PROTECTED_OPERATIONS = "*";',
        '    expect(() => authorizeOperation("createPet", "protected-write")).toThrow(/[Ww]ildcard/);',
        "  });",
        "",
        '  it("allows exact operation IDs", () => {',
        '    process.env.TYPE_MCP_ALLOW_PROTECTED_OPERATIONS = "createPet";',
        '    expect(() => authorizeOperation("createPet", "protected-write")).not.toThrow();',
        "  });",
        "",
        '  it("rejects unknown operation IDs", () => {',
        '    process.env.TYPE_MCP_ALLOW_PROTECTED_OPERATIONS = "createPet";',
        '    expect(() => authorizeOperation("deletePet", "protected-write")).toThrow(/not in/);',
        "  });",
        "});",
        "",
    ])


def _server_test_ts(server_class: str) -> str:
    return "\n".join([
        "// Auto-generated by api-to-typemcp. Do not edit.",
        "",
        'import { describe, it, expect } from "vitest";',
        'import { readFileSync } from "node:fs";',
        "",
        'describe("Server source", () => {',
        '  it("exports the decorated server class", () => {',
        '    const source = readFileSync(new URL("../src/server.ts", import.meta.url), "utf8");',
        f'    expect(source).toContain("export class {server_class}");',
        '    expect(source).toContain("@McpServer");',
        "  });",
        "});",
        "",
    ])
