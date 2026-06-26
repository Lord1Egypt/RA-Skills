"""
API Doc Generator — 单元测试
"""

import pytest
import json
import yaml
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generator import (
    analyze_code,
    generate_docs,
    generate_openapi,
    generate_markdown,
    generate_postman_collection,
    extract_python_functions,
    extract_generic_functions,
    infer_type_from_name,
    infer_type_from_annotation,
    parse_python_docstring,
    RESPONSE_TEMPLATES,
)


# ============= 辅助函数测试 =============

class TestInferType:
    """类型推断测试"""

    def test_infer_email(self):
        ptype, fmt = infer_type_from_name("user_email")
        assert ptype == "string"
        assert fmt == "email"

    def test_infer_phone(self):
        ptype, fmt = infer_type_from_name("phone_number")
        assert ptype == "string"
        assert fmt == "tel"

    def test_infer_id(self):
        ptype, fmt = infer_type_from_name("user_id")
        assert ptype == "integer"

    def test_infer_price(self):
        ptype, fmt = infer_type_from_name("total_price")
        assert ptype == "number"

    def test_infer_bool(self):
        ptype, fmt = infer_type_from_name("is_active")
        assert ptype == "boolean"

    def test_infer_date(self):
        ptype, fmt = infer_type_from_name("created_at")
        assert ptype == "string"
        assert fmt == "date-time"

    def test_infer_plain_string(self):
        ptype, fmt = infer_type_from_name("username")
        assert ptype == "string"
        assert fmt is None


class TestInferAnnotation:
    """Python类型注解推断测试"""

    def test_str_annotation(self):
        ptype, fmt = infer_type_from_annotation("str")
        assert ptype == "string"

    def test_int_annotation(self):
        ptype, fmt = infer_type_from_annotation("int")
        assert ptype == "integer"

    def test_float_annotation(self):
        ptype, fmt = infer_type_from_annotation("float")
        assert ptype == "number"

    def test_bool_annotation(self):
        ptype, fmt = infer_type_from_annotation("bool")
        assert ptype == "boolean"

    def test_list_annotation(self):
        ptype, fmt = infer_type_from_annotation("list")
        assert ptype == "array"

    def test_optional_str(self):
        ptype, fmt = infer_type_from_annotation("Optional[str]")
        assert ptype == "string"

    def test_list_str(self):
        ptype, fmt = infer_type_from_annotation("List[str]")
        assert ptype == "array"


class TestDocstringParser:
    """文档字符串解析测试"""

    def test_parse_simple_docstring(self):
        doc = '''获取用户列表
        Returns:
            list: 用户列表
        '''
        result = parse_python_docstring(doc)
        assert "获取用户列表" in result["description"]

    def test_parse_params(self):
        doc = '''创建用户
        Args:
            name: 用户名
            email: 邮箱地址
        '''
        result = parse_python_docstring(doc)
        assert "name" in result["params"]
        assert result["params"]["name"] == "用户名"

    def test_empty_docstring(self):
        result = parse_python_docstring("")
        assert result["description"] == ""
        assert result["params"] == {}


# ============= Flask 路由提取测试 =============

class TestFlaskRoutes:
    """Flask 路由提取测试"""

    def test_extract_get_route(self):
        code = '''
from flask import Flask
app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def get_users():
    """获取用户列表"""
    return {'code': 0, 'data': []}
'''
        endpoints = extract_python_functions(code)
        assert len(endpoints) >= 1

    def test_extract_post_route(self):
        code = '''
from flask import Flask
app = Flask(__name__)

@app.route('/api/users', methods=['POST'])
def create_user():
    """创建用户"""
    return {'code': 0}
'''
        endpoints = extract_python_functions(code)
        # 应该提取到 POST /api/users
        post_routes = [ep for ep in endpoints if ep.get("method") == "POST"]
        assert len(post_routes) >= 1

    def test_extract_multiple_routes(self):
        code = '''
from flask import Flask, request
app = Flask(__name__)

@app.route('/users', methods=['GET'])
def list_users():
    return []

@app.route('/users', methods=['POST'])
def create_user():
    return {}

@app.route('/users/<int:uid>', methods=['GET'])
def get_user(uid):
    return {}

@app.route('/users/<int:uid>', methods=['PUT'])
def update_user(uid):
    return {}

@app.route('/users/<int:uid>', methods=['DELETE'])
def delete_user(uid):
    return {}
'''
        endpoints = extract_python_functions(code)
        paths = [ep["path"] for ep in endpoints]
        methods = [ep["method"] for ep in endpoints]
        assert "/users" in paths
        assert "GET" in methods
        assert "POST" in methods
        assert "PUT" in methods
        assert "DELETE" in methods


# ============= 通用函数提取测试 =============

class TestGenericFunctions:
    """通用函数提取测试"""

    def test_extract_plain_function(self):
        code = '''
def hello(name: str) -> str:
    """Say hello to user"""
    return f"Hello {name}"
'''
        endpoints = extract_generic_functions(code, "python")
        assert len(endpoints) == 1
        assert endpoints[0]["function"] == "hello"
        assert endpoints[0]["method"] == "AUTO"

    def test_extract_multiple_functions(self):
        code = '''
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

def multiply(x: float, y: float) -> float:
    """Multiply two numbers"""
    return x * y
'''
        endpoints = extract_generic_functions(code, "python")
        assert len(endpoints) == 2
        func_names = [ep["function"] for ep in endpoints]
        assert "add" in func_names
        assert "multiply" in func_names

    def test_function_with_default_params(self):
        code = '''
def greet(name: str, prefix: str = "Hello") -> str:
    """Greet user with prefix"""
    return f"{prefix} {name}"
'''
        endpoints = extract_generic_functions(code, "python")
        assert len(endpoints) == 1
        params = endpoints[0]["parameters"]
        assert "prefix" in params
        assert params["prefix"]["required"] is False


# ============= 文档生成测试 =============

class TestOpenAPIGenerate:
    """OpenAPI 文档生成测试"""

    def test_generate_openapi_basic(self):
        code = '''
from flask import Flask
app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello():
    """Hello endpoint"""
    return {'message': 'hello'}
'''
        endpoints = extract_python_functions(code)
        spec = generate_openapi(endpoints, title="Test API", version="1.0.0")
        assert spec["openapi"] == "3.0.3"
        assert spec["info"]["title"] == "Test API"
        assert "/api/hello" in spec["paths"]
        assert "get" in spec["paths"]["/api/hello"]

    def test_openapi_json_valid(self):
        code = '''
def foo(x: int) -> str:
    """Foo function"""
    return str(x)
'''
        endpoints = extract_generic_functions(code, "python")
        spec = generate_openapi(endpoints, title="Test")
        json_str = json.dumps(spec, ensure_ascii=False)
        parsed = json.loads(json_str)
        assert parsed["openapi"] == "3.0.3"

    def test_openapi_yaml_valid(self):
        from generator import generate_openapi_yaml
        code = '''
def bar() -> None:
    """Bar function"""
    pass
'''
        endpoints = extract_generic_functions(code, "python")
        spec = generate_openapi(endpoints)
        yaml_str = generate_openapi_yaml(spec)
        parsed = yaml.safe_load(yaml_str)
        assert parsed["openapi"] == "3.0.3"


class TestMarkdownGenerate:
    """Markdown 文档生成测试"""

    def test_generate_markdown_basic(self):
        code = '''
def hello(name: str) -> str:
    """Say hello"""
    return f"Hello {name}"
'''
        endpoints = extract_generic_functions(code, "python")
        md = generate_markdown(endpoints, title="Test API")
        assert "# Test API" in md
        assert "hello" in md

    def test_markdown_no_endpoints(self):
        md = generate_markdown([], title="Empty")
        assert "No API endpoints found" in md


class TestPostmanGenerate:
    """Postman Collection 生成测试"""

    def test_generate_postman_basic(self):
        code = '''
from flask import Flask
app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def get_users():
    return []
'''
        endpoints = extract_python_functions(code)
        collection = generate_postman_collection(endpoints, name="Test Collection")
        assert collection["info"]["name"] == "Test Collection"
        assert "item" in collection

    def test_postman_json_valid(self):
        code = '''
def test():
    """Test function"""
    pass
'''
        endpoints = extract_generic_functions(code, "python")
        collection = generate_postman_collection(endpoints)
        json_str = json.dumps(collection, ensure_ascii=False)
        parsed = json.loads(json_str)
        assert "info" in parsed
        assert "item" in parsed


# ============= 端到端测试 =============

class TestEndToEnd:
    """端到端测试"""

    def test_flask_full_pipeline(self):
        code = '''
from flask import Flask, request
app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def list_users():
    """获取用户列表"""
    return {'code': 0, 'data': []}

@app.route('/api/users', methods=['POST'])
def create_user():
    """创建新用户
    Args:
        name: 用户名
        email: 邮箱
    """
    return {'code': 0, 'data': {'id': 1}}, 201
'''
        # Markdown
        md = generate_docs(code, "markdown", framework="flask")
        assert "/api/users" in md
        assert "GET" in md or "🟢" in md

        # OpenAPI
        oa = generate_docs(code, "openapi", framework="flask")
        spec = json.loads(oa)
        assert "/api/users" in spec["paths"]

        # Postman
        pm = generate_docs(code, "postman", framework="flask")
        collection = json.loads(pm)
        assert len(collection["item"]) > 0

    def test_auto_language_detection(self):
        code = '''
from flask import Flask
app = Flask(__name__)
@app.route('/test', methods=['GET'])
def test(): pass
'''
        endpoints = analyze_code(code, language="auto", framework="auto")
        assert len(endpoints) >= 1

    def test_batch_like_single_file(self):
        code = '''
def func_a(): pass
def func_b(): pass
'''
        eps = analyze_code(code, language="python")
        assert len(eps) == 2


# ============= 响应模板测试 =============

class TestResponseTemplates:
    """响应模板测试"""

    def test_templates_exist(self):
        assert "success" in RESPONSE_TEMPLATES
        assert "created" in RESPONSE_TEMPLATES
        assert "bad_request" in RESPONSE_TEMPLATES
        assert "unauthorized" in RESPONSE_TEMPLATES
        assert "server_error" in RESPONSE_TEMPLATES

    def test_success_template_has_schema(self):
        t = RESPONSE_TEMPLATES["success"]
        assert "schema" in t
        assert "code" in t["schema"]
        assert "message" in t["schema"]
        assert "data" in t["schema"]

    def test_all_status_codes(self):
        for name, template in RESPONSE_TEMPLATES.items():
            assert "description" in template
            assert "schema" in template
