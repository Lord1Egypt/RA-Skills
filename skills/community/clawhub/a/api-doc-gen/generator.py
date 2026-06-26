"""
API Doc Generator Core
从代码自动生成 API 文档，支持 Markdown / OpenAPI 3.0 / Postman Collection
"""

import re
import json
import uuid
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# ============= 内置响应模板 =============

RESPONSE_TEMPLATES = {
    "success": {
        "description": "成功响应",
        "schema": {
            "code": {"type": "integer", "example": 0},
            "message": {"type": "string", "example": "操作成功"},
            "data": {"type": "object", "example": {}}
        }
    },
    "created": {
        "description": "创建成功",
        "schema": {
            "code": {"type": "integer", "example": 0},
            "message": {"type": "string", "example": "创建成功"},
            "data": {"type": "object", "example": {"id": 1}}
        }
    },
    "bad_request": {
        "description": "参数错误",
        "schema": {
            "code": {"type": "integer", "example": 400},
            "message": {"type": "string", "example": "参数错误"},
            "data": {"type": "null", "example": None}
        }
    },
    "unauthorized": {
        "description": "未授权",
        "schema": {
            "code": {"type": "integer", "example": 401},
            "message": {"type": "string", "example": "未授权"},
            "data": {"type": "null", "example": None}
        }
    },
    "forbidden": {
        "description": "禁止访问",
        "schema": {
            "code": {"type": "integer", "example": 403},
            "message": {"type": "string", "example": "禁止访问"},
            "data": {"type": "null", "example": None}
        }
    },
    "not_found": {
        "description": "资源不存在",
        "schema": {
            "code": {"type": "integer", "example": 404},
            "message": {"type": "string", "example": "资源不存在"},
            "data": {"type": "null", "example": None}
        }
    },
    "server_error": {
        "description": "服务器错误",
        "schema": {
            "code": {"type": "integer", "example": 500},
            "message": {"type": "string", "example": "服务器错误"},
            "data": {"type": "null", "example": None}
        }
    }
}

# ============= 类型推断引擎 =============

PYTHON_TYPE_TO_JSON = {
    "str": "string",
    "int": "integer",
    "float": "number",
    "bool": "boolean",
    "list": "array",
    "dict": "object",
    "bytes": "string",
    "None": "null",
    "Optional[str]": "string",
    "Optional[int]": "integer",
    "Optional[float]": "number",
    "Optional[list]": "array",
    "Optional[dict]": "object",
    "Optional[bool]": "boolean",
    "List[str]": "array",
    "List[int]": "array",
    "List[float]": "array",
    "List[dict]": "array",
    "List[object]": "array",
    "Dict[str, Any]": "object",
    "Dict[str, str]": "object",
    "Dict[str, int]": "object",
    "datetime": "string",
    "date": "string",
    "UUID": "string",
}

PYTHON_FORMAT_HINTS = {
    "email": "email",
    "phone": "tel",
    "url": "url",
    "uri": "url",
    "date": "date",
    "datetime": "date-time",
    "uuid": "uuid",
    "ip": "ipv4",
    "password": "password",
}


def infer_type_from_annotation(annotation: str) -> Tuple[str, Optional[str]]:
    """从 Python 类型注解推断 JSON Schema 类型"""
    raw_type = annotation.strip()
    json_type = PYTHON_TYPE_TO_JSON.get(raw_type, "string")
    fmt = None
    for hint, f in PYTHON_FORMAT_HINTS.items():
        if hint.lower() in raw_type.lower():
            fmt = f
            break
    return json_type, fmt


def infer_type_from_name(param_name: str) -> Tuple[str, Optional[str]]:
    """从参数名推断类型"""
    name_lower = param_name.lower()
    if "email" in name_lower:
        return "string", "email"
    if "phone" in name_lower or "mobile" in name_lower or "tel" in name_lower:
        return "string", "tel"
    if "url" in name_lower or "link" in name_lower:
        return "string", "url"
    if "date" in name_lower or "time" in name_lower or "_at" in name_lower or name_lower.endswith("at"):
        return "string", "date-time"
    if "id" in name_lower and ("user" in name_lower or "product" in name_lower or "order" in name_lower):
        return "integer", None
    if "id" in name_lower:
        return "integer", None
    if "count" in name_lower or "num" in name_lower or "page" in name_lower:
        return "integer", None
    if "price" in name_lower or "amount" in name_lower or "total" in name_lower or "fee" in name_lower:
        return "number", None
    if "is_" in name_lower or "has_" in name_lower or "enable" in name_lower:
        return "boolean", None
    if "desc" in name_lower or "content" in name_lower or "text" in name_lower or "msg" in name_lower:
        return "string", None
    return "string", None


def parse_python_docstring(docstring: str) -> Dict[str, Any]:
    """解析 Python docstring，提取参数和描述"""
    result = {"description": "", "params": {}}
    if not docstring:
        return result

    lines = docstring.strip().split("\n")
    current_param = None
    param_desc_lines = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith("=") or line.startswith("---"):
            continue
        if line.startswith("Args:") or line.startswith("Parameters:"):
            continue
        param_match = re.match(r"(\w+)\s*[(:]\s*(.*)", line)
        if param_match:
            if current_param:
                result["params"][current_param] = " ".join(param_desc_lines).strip()
            current_param = param_match.group(1)
            param_desc_lines = [param_match.group(2)] if param_match.group(2) else []
        elif current_param and line:
            param_desc_lines.append(line)

    if current_param:
        result["params"][current_param] = " ".join(param_desc_lines).strip()

    # 提取首行作为描述
    desc_lines = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("Args") or line.startswith("Parameters") or line.startswith("Returns"):
            continue
        if ":" in line and re.match(r"^\w+:", line):
            break
        desc_lines.append(line)
        if len(desc_lines) >= 3:
            break

    result["description"] = " ".join(desc_lines).strip()
    return result


def parse_jsdoc_comment(comment: str) -> Dict[str, Any]:
    """解析 JSDoc 注释"""
    result = {"description": "", "params": {}, "returns": None}

    desc_match = re.search(r"\*\s*(.+?)(?=\n\s*\*\s*@|\Z)", comment, re.DOTALL)
    if desc_match:
        result["description"] = desc_match.group(1).replace("*", "").strip()

    param_matches = re.findall(r"@param\s+\{([^}]+)\}\s+(\w+)(?:\s+-\s+)?(.+)?", comment)
    for ptype, pname, pdesc in param_matches:
        result["params"][pname] = {"type": ptype.strip(), "description": (pdesc or "").strip()}

    return_match = re.search(r"@returns?\s+\{([^}]+)\}(?:\s+-\s+)?(.+)?", comment)
    if return_match:
        result["returns"] = {"type": return_match.group(1).strip(), "description": (return_match.group(2) or "").strip()}

    return result


def extract_python_functions(code: str) -> List[Dict[str, Any]]:
    """从 Python 代码中提取函数/方法定义"""
    endpoints = []

    # 匹配装饰器路由
    route_decorators = [
        (r"@(app|router)\.(get|post|put|patch|delete|options|head)\s*\(\s*['\"]([^'\"]+)['\"]", "rest"),
        (r"@app\.route\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*methods\s*=\s*\[([^\]]+)\]", "flask"),
        (r"@(app|router)\.(get|post|put|patch|delete)\s*\(\s*['\"]([^'\"]+)['\"]", "rest"),
        (r"@(app)\.(get|post|put|patch|delete)\s*\(\s*['\"]([^'\"]+)['\"]", "rest"),
        (r"@(app)\.route\s*\(\s*['\"]([^'\"]+)['\"]", "flask_route"),
    ]

    lines = code.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # 检查装饰器
        http_method = None
        path = None
        framework = "generic"

        for pattern, ftype in route_decorators:
            m = re.match(pattern, line)
            if m:
                if ftype == "rest":
                    http_method = m.group(2).upper()
                    path = m.group(3)
                    framework = "fastapi_or_flask"
                elif ftype == "flask":
                    path = m.group(1)
                    methods_str = m.group(2).replace("'", "").replace('"', "")
                    http_method = methods_str.split(",")[0].strip().upper()
                    framework = "flask"
                elif ftype == "flask_route":
                    path = m.group(1)
                    framework = "flask"
                    http_method = "GET"
                break

        if path:
            func_name = ""
            params = {}
            description = ""
            returns = None
            responses = {}

            # 找函数名
            j = i + 1
            while j < len(lines):
                func_line = lines[j].strip()
                if func_line.startswith("async def ") or func_line.startswith("def "):
                    m = re.match(r"(?:async\s+)?def\s+(\w+)\s*\((.*?)\)(?:\s*->\s*(.+?))?:", func_line)
                    if m:
                        func_name = m.group(1)
                        arg_str = m.group(2)
                        ret_annotation = m.group(3)

                        # 解析参数
                        if arg_str.strip():
                            for arg in arg_str.split(","):
                                arg = arg.strip()
                                if not arg:
                                    continue
                                # 先提取默认值
                                default_val = None
                                if "=" in arg:
                                    eq_parts = arg.split("=")
                                    arg = eq_parts[0].strip()
                                    default_val = eq_parts[1].strip()
                                # 去除类型注解
                                type_part = ""
                                if ":" in arg:
                                    colon_idx = arg.index(":")
                                    type_part = arg[colon_idx+1:].strip()
                                    arg = arg[:colon_idx].strip()
                                pname = arg
                                if default_val is not None:
                                    ptype, pfmt = infer_type_from_annotation(type_part) if type_part else infer_type_from_annotation("Optional[str]")
                                    params[pname] = {"required": False, "default": default_val, "type": ptype, "format": pfmt, "description": ""}
                                else:
                                    ptype, pfmt = infer_type_from_annotation(type_part) if type_part else infer_type_from_annotation("str")
                                    params[pname] = {"required": True, "type": ptype, "format": pfmt, "description": ""}

                        if ret_annotation:
                            rtype, rfmt = infer_type_from_annotation(ret_annotation.strip())
                            returns = {"type": rtype, "format": rfmt}
                    break
                j += 1

            # 收集文档字符串
            docstring_lines = []
            docstring_started = False
            j = i + 1
            while j < len(lines):
                func_line = lines[j]
                stripped = func_line.strip()
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    if not docstring_started:
                        docstring_started = True
                        if stripped.endswith('"""') or stripped.endswith("'''"):
                            docstring_lines.append(stripped[3:-3])
                            break
                        else:
                            docstring_lines.append(stripped[3:])
                    else:
                        docstring_lines.append(stripped[:-3])
                        break
                elif docstring_started:
                    docstring_lines.append(func_line.strip())
                j += 1

            if docstring_lines:
                doc_info = parse_python_docstring("\n".join(docstring_lines))
                description = doc_info["description"]
                for pname, pdesc in doc_info["params"].items():
                    if pname in params:
                        params[pname]["description"] = pdesc

            # 默认响应
            if http_method in ("POST", "PUT", "PATCH"):
                responses = {"200": RESPONSE_TEMPLATES["success"].copy(), "400": RESPONSE_TEMPLATES["bad_request"].copy(), "500": RESPONSE_TEMPLATES["server_error"].copy()}
            elif http_method == "GET":
                responses = {"200": RESPONSE_TEMPLATES["success"].copy(), "400": RESPONSE_TEMPLATES["bad_request"].copy(), "404": RESPONSE_TEMPLATES["not_found"].copy()}
            else:
                responses = {"200": RESPONSE_TEMPLATES["success"].copy(), "400": RESPONSE_TEMPLATES["bad_request"].copy()}

            endpoints.append({
                "path": path,
                "method": http_method,
                "framework": framework,
                "function": func_name,
                "description": description,
                "parameters": params,
                "requestBody": None,
                "responses": responses,
                "returns": returns
            })

            if "request" in str(params).lower() or http_method in ("POST", "PUT", "PATCH"):
                pass

        i += 1

    return endpoints


def extract_js_endpoints(code: str) -> List[Dict[str, Any]]:
    """从 JavaScript/Node.js 代码中提取路由"""
    endpoints = []
    method_map = {"GET": "get", "POST": "post", "PUT": "put", "DELETE": "delete", "PATCH": "patch"}

    route_patterns = [
        (r"router\.(get|post|put|delete|patch)\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*(\w+)", "express"),
        (r"app\.(get|post|put|delete|patch)\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*(\w+)", "express"),
        (r"@Get\(['\"]([^'\"]+)['\"]\)", "nestjs_get"),
        (r"@Post\(['\"]([^'\"]+)['\"]\)", "nestjs_post"),
        (r"@Put\(['\"]([^'\"]+)['\"]\)", "nestjs_put"),
        (r"@Delete\(['\"]([^'\"]+)['\"]\)", "nestjs_delete"),
        (r"@Patch\(['\"]([^'\"]+)['\"]\)", "nestjs_patch"),
    ]

    for pattern, ftype in route_patterns:
        for m in re.finditer(pattern, code):
            if ftype == "express":
                method = m.group(1).upper()
                path = m.group(2)
                handler = m.group(3)
            elif ftype.startswith("nestjs"):
                method_map = {"nestjs_get": "GET", "nestjs_post": "POST", "nestjs_put": "PUT", "nestjs_delete": "DELETE", "nestjs_patch": "PATCH"}
                method = method_map.get(ftype, "GET")
                path = m.group(1)
                handler = ""
            else:
                continue

            js_doc = ""
            pos = m.end()
            lines = code[pos:pos+500].split("\n")
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("/**"):
                    js_doc += stripped + "\n"
                elif js_doc and stripped.startswith("*"):
                    js_doc += stripped + "\n"
                elif js_doc and not stripped.startswith("*") and stripped != "":
                    break

            doc_info = parse_jsdoc_comment(js_doc)

            endpoints.append({
                "path": path,
                "method": method,
                "framework": "express" if "express" in ftype else "nestjs",
                "function": handler,
                "description": doc_info["description"],
                "parameters": {},
                "requestBody": None,
                "responses": {"200": RESPONSE_TEMPLATES["success"].copy(), "400": RESPONSE_TEMPLATES["bad_request"].copy()},
                "returns": doc_info["returns"]
            })

    return endpoints


def extract_generic_functions(code: str, language: str = "python") -> List[Dict[str, Any]]:
    """从通用代码中提取函数定义"""
    if language == "python":
        endpoints = []
        for m in re.finditer(r"(?:async\s+)?def\s+(\w+)\s*\((.*?)\)(?:\s*->\s*(.+?))?:", code):
            func_name = m.group(1)
            arg_str = m.group(2)
            ret_annotation = m.group(3)

            params = {}
            if arg_str.strip():
                for arg in arg_str.split(","):
                    arg = arg.strip()
                    if not arg:
                        continue
                    # 先提取默认值（可能含在类型注解中，如 "prefix: str = 'Hello'"）
                    default_val = None
                    if "=" in arg:
                        eq_parts = arg.split("=")
                        arg = eq_parts[0].strip()
                        default_val = eq_parts[1].strip()

                    # 去除类型注解
                    type_part = ""
                    if ":" in arg:
                        colon_idx = arg.index(":")
                        type_part = arg[colon_idx+1:].strip()
                        arg = arg[:colon_idx].strip()

                    pname = arg
                    if default_val is not None:
                        ptype, pfmt = infer_type_from_annotation(type_part) if type_part else infer_type_from_annotation("Optional[str]")
                        params[pname] = {"required": False, "default": default_val, "type": ptype, "format": pfmt, "description": ""}
                    else:
                        ptype, pfmt = infer_type_from_annotation(type_part) if type_part else infer_type_from_annotation("str")
                        params[pname] = {"required": True, "type": ptype, "format": pfmt, "description": ""}

            rtype, rfmt = infer_type_from_annotation(ret_annotation.strip()) if ret_annotation else ("void", None)

            # 找文档字符串
            pos = m.end()
            doc_info = {"description": "", "params": {}}
            snippet = code[pos:pos+300]
            dm = re.search(r'"""\s*(.+?)"""', snippet, re.DOTALL)
            if dm:
                doc_info = parse_python_docstring(dm.group(1))
                for pname, pdesc in doc_info["params"].items():
                    if pname in params:
                        params[pname]["description"] = pdesc

            endpoints.append({
                "path": f"/{func_name}",
                "method": "AUTO",
                "framework": "generic",
                "function": func_name,
                "description": doc_info["description"],
                "parameters": params,
                "requestBody": None,
                "responses": {"200": RESPONSE_TEMPLATES["success"].copy()},
                "returns": {"type": rtype, "format": rfmt}
            })
        return endpoints
    return []


# ============= 文档生成器 =============

def generate_openapi(endpoints: List[Dict], title: str = "API Documentation", version: str = "1.0.0") -> Dict:
    """生成 OpenAPI 3.0 文档"""
    spec = {
        "openapi": "3.0.3",
        "info": {
            "title": title,
            "version": version,
            "description": f"Auto-generated API documentation. Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "contact": {}
        },
        "paths": {},
        "components": {
            "schemas": {}
        }
    }

    for ep in endpoints:
        path = ep["path"]
        if path not in spec["paths"]:
            spec["paths"][path] = {}

        method = ep["method"].lower() if ep["method"] != "AUTO" else "get"

        operation = {
            "summary": ep.get("description", ep.get("function", "")) or ep["function"],
            "description": ep.get("description", "") or ep["function"],
            "operationId": ep.get("function", f"{method}_{path.replace('/', '_')}"),
            "tags": [ep.get("framework", "General")],
            "responses": {}
        }

        # Parameters
        params = []
        required_params = []
        for pname, pdef in ep.get("parameters", {}).items():
            pitem = {
                "name": pname,
                "in": "query",
                "description": pdef.get("description", ""),
                "required": pdef.get("required", True),
                "schema": {"type": pdef.get("type", "string")}
            }
            if pdef.get("format"):
                pitem["schema"]["format"] = pdef["format"]
            if pdef.get("default"):
                pitem["schema"]["default"] = pdef["default"]
            params.append(pitem)
            if pdef.get("required", True):
                required_params.append(pname)

        if params:
            operation["parameters"] = params

        # Responses
        for status_code, resp_def in ep.get("responses", {}).items():
            operation["responses"][status_code] = {
                "description": resp_def.get("description", ""),
                "content": {
                    "application/json": {
                        "schema": resp_def.get("schema", {"type": "object"})
                    }
                }
            }

        spec["paths"][path][method] = operation

    return spec


def generate_openapi_yaml(spec: Dict) -> str:
    """将 OpenAPI dict 转换为 YAML 格式"""
    import yaml
    return yaml.dump(spec, allow_unicode=True, sort_keys=False, default_flow_style=False)


def generate_markdown(endpoints: List[Dict], title: str = "API Documentation") -> str:
    """生成 Markdown 格式 API 文档"""
    if not endpoints:
        return f"# {title}\n\n> Auto-generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n# ⚠️ No API endpoints found\n\nNo API endpoints or functions could be detected in the provided code.\n"

    md = []
    md.append(f"# {title}\n")
    md.append(f"> Auto-generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    md.append("")

    # 目录
    md.append("## 📑 Table of Contents\n")
    for i, ep in enumerate(endpoints):
        method_badge = method_badge_md(ep.get("method", "AUTO"))
        md.append(f"- [{method_badge} {ep['path']}](#{ep['path'].replace('/', '')})")
    md.append("")

    # 按路径分组
    current_path = None
    for ep in endpoints:
        path = ep["path"]
        if path != current_path:
            md.append(f"## {path}\n")
            current_path = path

        method = ep.get("method", "AUTO")
        badge = method_badge_md(method)

        md.append(f"### {badge} {path}\n")
        md.append(f"**Function:** `{ep.get('function', 'N/A')}`\n")
        if ep.get("description"):
            md.append(f"**Description:** {ep['description']}\n")

        # Parameters
        params = ep.get("parameters", {})
        if params:
            md.append("\n**Parameters:**\n")
            md.append("| Name | Type | Required | Default | Description |")
            md.append("|------|------|----------|---------|-------------|")
            for pname, pdef in params.items():
                ptype = pdef.get("type", "string")
                required = "✅" if pdef.get("required", True) else "❌"
                default = pdef.get("default", "-")
                desc = pdef.get("description", "-")
                md.append(f"| `{pname}` | {ptype} | {required} | {default} | {desc} |")

        # Responses
        md.append("\n**Responses:**\n")
        md.append("| Status | Description |")
        md.append("|--------|-------------|")
        for status, resp in ep.get("responses", {}).items():
            md.append(f"| {status} | {resp.get('description', '')} |")

        md.append("\n---\n")

    return "\n".join(md)


def method_badge_md(method: str) -> str:
    badges = {
        "GET": "🟢 GET",
        "POST": "🔵 POST",
        "PUT": "🟡 PUT",
        "PATCH": "🟠 PATCH",
        "DELETE": "🔴 DELETE",
        "OPTIONS": "⚪ OPTIONS",
        "AUTO": "⚪ AUTO"
    }
    return badges.get(method.upper(), f"⚪ {method}")


def generate_postman_collection(endpoints: List[Dict], name: str = "API Collection") -> Dict:
    """生成 Postman Collection"""
    collection_id = str(uuid.uuid4())
    collection = {
        "info": {
            "name": name,
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
            "_uid": collection_id
        },
        "item": []
    }

    # 按路径前缀分组
    groups: Dict[str, List] = {}
    for ep in endpoints:
        parts = ep["path"].strip("/").split("/")
        group_name = parts[0] if parts else "General"
        if group_name not in groups:
            groups[group_name] = []
        groups[group_name].append(ep)

    for group_name, eps in groups.items():
        folder = {
            "name": group_name,
            "item": []
        }
        for ep in eps:
            item = {
                "name": f"{ep.get('method', 'GET')} {ep['path']}",
                "request": {
                    "method": ep.get("method", "GET"),
                    "header": [],
                    "url": {
                        "raw": "{{base_url}}" + ep["path"],
                        "host": ["{{base_url}}"],
                        "path": ep["path"].strip("/").split("/")
                    },
                    "description": ep.get("description", "")
                },
                "response": []
            }

            # 添加 query params
            params = []
            for pname, pdef in ep.get("parameters", {}).items():
                params.append({
                    "key": pname,
                    "value": pdef.get("default", ""),
                    "description": pdef.get("description", "")
                })
            if params:
                item["request"]["url"]["query"] = params

            folder["item"].append(item)

        collection["item"].append(folder)

    return collection


# ============= 主入口 =============

def analyze_code(code: str, language: str = "auto", framework: str = "auto") -> List[Dict]:
    """分析代码，提取 API 端点或函数"""
    if language == "auto":
        if re.search(r"@(app|router)\.(get|post|put|patch|delete)", code):
            language = "python"
        elif re.search(r"router\.(get|post|put|delete)", code):
            language = "javascript"
        elif re.search(r"def\s+\w+\s*\(", code):
            language = "python"
        elif re.search(r"function\s+\w+\s*\(", code):
            language = "javascript"
        else:
            language = "python"

    if framework == "auto":
        if language == "python":
            if re.search(r"FastAPI|fastapi", code):
                framework = "fastapi"
            elif re.search(r"Flask|flask", code):
                framework = "flask"
            elif re.search(r"Django|django", code):
                framework = "django"
            else:
                framework = "generic"
        else:
            framework = "express"

    if language == "python":
        if re.search(r"@(app|router)\.", code):
            endpoints = extract_python_functions(code)
        else:
            endpoints = extract_generic_functions(code, "python")
    elif language == "javascript":
        endpoints = extract_js_endpoints(code)
    else:
        endpoints = extract_generic_functions(code, language)

    return endpoints


def generate_docs(code: str, output_format: str = "markdown",
                  title: str = "API Documentation",
                  language: str = "auto",
                  framework: str = "auto") -> str:
    """生成 API 文档主入口"""
    endpoints = analyze_code(code, language, framework)

    if not endpoints:
        return "# ⚠️ No API endpoints found\n\nNo API endpoints or functions could be detected in the provided code."

    if output_format == "openapi":
        spec = generate_openapi(endpoints, title)
        return json.dumps(spec, ensure_ascii=False, indent=2)
    elif output_format == "openapi-yaml":
        spec = generate_openapi(endpoints, title)
        return generate_openapi_yaml(spec)
    elif output_format == "postman":
        collection = generate_postman_collection(endpoints, title)
        return json.dumps(collection, ensure_ascii=False, indent=2)
    else:
        return generate_markdown(endpoints, title)


def batch_generate(file_paths: List[str], output_format: str = "markdown",
                   language: str = "auto", framework: str = "auto",
                   output_dir: str = ".") -> Dict[str, str]:
    """批量处理多个文件"""
    results = {}
    for path in file_paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
            content = generate_docs(code, output_format, framework=framework, language=language)
            base = path.replace("/", "_").replace("\\", "_").replace(".py", "").replace(".js", "")
            output_file = f"{output_dir}/{base}_doc.{'md' if output_format == 'markdown' else 'json'}"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)
            results[path] = output_file
        except Exception as e:
            results[path] = f"ERROR: {str(e)}"
    return results
