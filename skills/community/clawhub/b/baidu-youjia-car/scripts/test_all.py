#!/usr/bin/env python3
"""
test_all.py — 百度有驾汽车查询 Skill 集成测试

测试覆盖：
- Key 解析链（参数 → 环境变量 → .env → ~/.youjia/key.json）
- send_code / create_key / save_config 脚本（单元测试）
- YoujiaClient 基本功能
"""

import os
import sys
import json
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# 添加 scripts 目录到 path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import youjia_client
from youjia_client import (
    YoujiaClient,
    YoujiaError,
    _load_env_file,
    _load_local_key,
    _resolve_key,
    save_key_to_dotenv,
)

import send_code
import create_key
import save_config


# ============================================================
# 1. .env 解析测试
# ============================================================

class TestEnvFileParsing(unittest.TestCase):
    """测试 .env 文件解析（_load_env_file）"""

    def test_load_env_file_normal(self):
        """正常解析 KEY=VALUE 格式"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("YOUJIA_API_KEY=sk-test123\n")
            f.write("OTHER_VAR=value\n")
            f.write("# comment line\n")
            f.write("\n")
            f.write('QUOTED_VAR="quoted value"\n')
            env_path = f.name

        try:
            result = _load_env_file(env_path)
            self.assertEqual(result.get("YOUJIA_API_KEY"), "sk-test123")
            self.assertEqual(result.get("OTHER_VAR"), "value")
            self.assertEqual(result.get("QUOTED_VAR"), "quoted value")
        finally:
            os.unlink(env_path)

    def test_load_env_file_not_exists(self):
        """文件不存在时返回空 dict"""
        result = _load_env_file("/nonexistent/.env")
        self.assertEqual(result, {})

    def test_load_env_file_malformed(self):
        """畸形的 .env 行被安全忽略"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("NO_EQUALS\n")
            f.write("=empty_key\n")
            env_path = f.name

        try:
            result = _load_env_file(env_path)
            self.assertNotIn("NO_EQUALS", result)
            self.assertNotIn("", result)
        finally:
            os.unlink(env_path)


# ============================================================
# 2. 本地 Key 加载测试
# ============================================================

class TestLocalKeyLoading(unittest.TestCase):
    """测试 ~/.youjia/key.json 加载（_load_local_key）"""

    def setUp(self):
        """创建临时 key.json"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.youjia_dir = os.path.join(self.temp_dir.name, ".youjia")
        os.makedirs(self.youjia_dir, exist_ok=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def _write_key_json(self, data):
        path = os.path.join(self.youjia_dir, "key.json")
        with open(path, "w") as f:
            json.dump(data, f)
        return path

    @patch("os.path.expanduser")
    def test_load_dict_format(self, mock_expanduser):
        """dict 格式：{"phone": {"key": "sk-xxx"}}"""
        mock_expanduser.return_value = self.temp_dir.name
        self._write_key_json({"13800138000": {"key": "sk-dict-key", "applied_at": "2026-01-01"}})
        key, source = _load_local_key()
        self.assertEqual(key, "sk-dict-key")
        self.assertEqual(source, "local_key")

    @patch("os.path.expanduser")
    def test_load_no_key_field(self, mock_expanduser):
        """dict 中每个 phone 无 key 字段 → 返回 None"""
        mock_expanduser.return_value = self.temp_dir.name
        self._write_key_json({"13800138000": {"applied_at": "2026-01-01"}})
        key, source = _load_local_key()
        self.assertIsNone(key)

    @patch("os.path.expanduser")
    def test_load_no_file(self, mock_expanduser):
        """key.json 不存在 → 返回 None"""
        mock_expanduser.return_value = self.temp_dir.name
        key, source = _load_local_key()
        self.assertIsNone(key)
        self.assertEqual(source, "none")

    @patch("os.path.expanduser")
    def test_load_empty_dict(self, mock_expanduser):
        """空 dict → 返回 None"""
        mock_expanduser.return_value = self.temp_dir.name
        self._write_key_json({})
        key, source = _load_local_key()
        self.assertIsNone(key)


# ============================================================
# 3. Key 解析链测试
# ============================================================

class TestKeyResolution(unittest.TestCase):
    """测试 Key 解析链优先级"""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        # 清除环境变量
        self._saved_env = os.environ.pop("YOUJIA_API_KEY", None)

    def tearDown(self):
        self.temp_dir.cleanup()
        if self._saved_env:
            os.environ["YOUJIA_API_KEY"] = self._saved_env
        else:
            os.environ.pop("YOUJIA_API_KEY", None)

    def test_resolve_argument_first(self):
        """传入参数优先级最高"""
        key, source = _resolve_key("sk-arg")
        self.assertEqual(key, "sk-arg")
        self.assertEqual(source, "argument")

    def test_resolve_env_var(self):
        """环境变量次优先"""
        os.environ["YOUJIA_API_KEY"] = "sk-env"
        key, source = _resolve_key(None)
        self.assertEqual(key, "sk-env")
        self.assertEqual(source, "env")

    def test_resolve_no_key(self):
        """无任何配置时返回 None"""
        key, source = _resolve_key(None)
        self.assertIsNone(key)
        self.assertEqual(source, "none")


# ============================================================
# 4. YoujiaClient 测试
# ============================================================

class TestYoujiaClient(unittest.TestCase):
    """测试 YoujiaClient 核心功能"""

    def test_client_with_explicit_key(self):
        """显式传 key 创建 client"""
        c = YoujiaClient(key="sk-explicit")
        self.assertEqual(c.key, "sk-explicit")
        self.assertEqual(c.key_source, "argument")

    def test_client_no_key(self):
        """无 key 时初始化成功但 key 为 None"""
        with patch.object(youjia_client, "_resolve_key", return_value=(None, "none")):
            c = YoujiaClient()
            self.assertIsNone(c.key)

    def test_ask_price_no_key_raises(self):
        """无 key 时调用 ask_price 抛出 YoujiaError"""
        with patch.object(youjia_client, "_resolve_key", return_value=(None, "none")):
            c = YoujiaClient()
            with self.assertRaises(YoujiaError) as ctx:
                c._get("/test", {"query": "test"})
            self.assertEqual(ctx.exception.code, -1)
            self.assertIn("未检测到 API Key", ctx.exception.message)

    def test_format_for_reply_empty(self):
        """空数据返回空字符串"""
        result = YoujiaClient.format_for_reply({})
        self.assertEqual(result, "")

    def test_format_for_reply_basic(self):
        """基本格式化输出"""
        data = {
            "Result": {
                "car_info": {
                    "brand_name": "奥迪",
                    "series_name": "奥迪A4L",
                    "model_name": "奥迪A4L 40TFSI",
                    "manufacturer_price": "32.18万",
                },
                "city_name": "北京",
            }
        }
        result = YoujiaClient.format_for_reply(data)
        self.assertIn("奥迪", result)
        self.assertIn("奥迪A4L", result)
        self.assertIn("北京", result)


# ============================================================
# 5. send_code 脚本测试
# ============================================================

class TestSendCode(unittest.TestCase):
    """测试 send_code 脚本逻辑"""

    @staticmethod
    def _mock_response(body_bytes):
        """创建支持 context manager 协议的 mock response"""
        mock = MagicMock()
        mock.read.return_value = body_bytes
        mock.__enter__.return_value = mock
        mock.__exit__.return_value = None
        return mock

    def test_send_code_response_parsing(self):
        """正常响应解析"""
        mock_body = json.dumps({
            "ResultCode": "0",
            "Result": True,
            "ResultMsg": "ok",
            "QueryID": "1234567890"
        }).encode("utf-8")
        resp = self._mock_response(mock_body)
        with patch("urllib.request.urlopen", return_value=resp):
            result = send_code.send_code("13800138000")
            self.assertEqual(result["error"], 0)
            self.assertEqual(result["query_id"], "1234567890")

    def test_send_code_error_response(self):
        """错误响应解析"""
        mock_body = json.dumps({
            "ResultCode": "50001",
            "Result": False,
            "ResultMsg": "手机号格式不正确"
        }).encode("utf-8")
        resp = self._mock_response(mock_body)
        with patch("urllib.request.urlopen", return_value=resp):
            result = send_code.send_code("13800138000")
            self.assertNotEqual(result["error"], 0)
            self.assertEqual(result["msg"], "手机号格式不正确")


# ============================================================
# 6. create_key 脚本测试
# ============================================================

class TestCreateKey(unittest.TestCase):
    """测试 create_key 脚本逻辑"""

    @staticmethod
    def _mock_response(body_bytes):
        """创建支持 context manager 协议的 mock response"""
        mock = MagicMock()
        mock.read.return_value = body_bytes
        mock.__enter__.return_value = mock
        mock.__exit__.return_value = None
        return mock

    def test_create_key_success(self):
        """成功返回 key"""
        mock_body = json.dumps({
            "ResultCode": "0",
            "Result": {"key_id": "sk-test-key", "app_ids": None},
            "ResultMsg": "ok",
            "QueryID": "1234567890"
        }).encode("utf-8")
        resp = self._mock_response(mock_body)
        with patch("urllib.request.urlopen", return_value=resp):
            result = create_key.create_key("13800138000", "123456")
            self.assertEqual(result["error"], 0)
            self.assertEqual(result["key"], "sk-test-key")

    def test_create_key_wrong_code(self):
        """验证码错误 53008"""
        mock_body = json.dumps({
            "ResultCode": "53008",
            "Result": False,
            "ResultMsg": "验证码错误"
        }).encode("utf-8")
        resp = self._mock_response(mock_body)
        with patch("urllib.request.urlopen", return_value=resp):
            result = create_key.create_key("13800138000", "000000")
            self.assertEqual(result["error"], 53008)
            self.assertEqual(result["msg"], "验证码错误")


# ============================================================
# 7. save_config 脚本测试
# ============================================================

class TestSaveConfig(unittest.TestCase):
    """测试 save_config 脚本逻辑"""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.youjia_dir = os.path.join(self.temp_dir.name, ".youjia")
        os.makedirs(self.youjia_dir, exist_ok=True)
        self.skill_root = tempfile.TemporaryDirectory()
        self.env_path = os.path.join(self.skill_root.name, ".env")
        self._saved_env = os.environ.pop("YOUJIA_API_KEY", None)

    def tearDown(self):
        self.temp_dir.cleanup()
        self.skill_root.cleanup()
        if self._saved_env is not None:
            os.environ["YOUJIA_API_KEY"] = self._saved_env
        else:
            os.environ.pop("YOUJIA_API_KEY", None)

    def _read_key_json(self):
        path = os.path.join(self.youjia_dir, "key.json")
        with open(path, "r") as f:
            return json.load(f)

    def _read_dotenv(self):
        with open(self.env_path, "r", encoding="utf-8") as f:
            return f.read()

    def _patch_paths(self):
        """同时 mock key.json 路径与 skill .env 路径。"""
        return (
            patch("save_config.get_config_path",
                  return_value=os.path.join(self.youjia_dir, "key.json")),
            patch("save_config.get_skill_env_path", return_value=self.env_path),
        )

    def test_save_new_key(self):
        """新建 key 记录，并覆盖环境变量 / .env"""
        p1, p2 = self._patch_paths()
        with p1, p2:
            result = save_config.save_config("13800138000", "sk-new")
        self.assertTrue(result["write_success"])
        self.assertTrue(result["is_new"])
        self.assertTrue(result["env_updated"])
        records = self._read_key_json()
        self.assertIn("13800138000", records)
        self.assertEqual(records["13800138000"]["key"], "sk-new")
        self.assertEqual(os.environ.get("YOUJIA_API_KEY"), "sk-new")
        self.assertIn("YOUJIA_API_KEY=sk-new", self._read_dotenv())

    def test_reuse_existing_key(self):
        """复用已有 key 时仍覆盖环境变量 / .env"""
        p1, p2 = self._patch_paths()
        with p1, p2:
            save_config.save_config("13800138000", "sk-same")
            result = save_config.save_config("13800138000", "sk-same")
        self.assertTrue(result["write_success"])
        self.assertFalse(result["is_new"])
        self.assertTrue(result["env_updated"])
        self.assertEqual(os.environ.get("YOUJIA_API_KEY"), "sk-same")

    def test_update_key(self):
        """同手机号不同 key → 视为新建，并覆盖旧环境变量"""
        p1, p2 = self._patch_paths()
        with p1, p2:
            # 先写入旧 key 到环境与 .env
            with open(self.env_path, "w", encoding="utf-8") as f:
                f.write("YOUJIA_API_KEY=sk-old\nOTHER=keep\n")
            os.environ["YOUJIA_API_KEY"] = "sk-old"

            save_config.save_config("13800138000", "sk-old")
            result = save_config.save_config("13800138000", "sk-new")

        self.assertTrue(result["write_success"])
        self.assertTrue(result["is_new"])
        self.assertTrue(result["env_updated"])
        records = self._read_key_json()
        self.assertEqual(records["13800138000"]["key"], "sk-new")
        self.assertEqual(os.environ.get("YOUJIA_API_KEY"), "sk-new")
        dotenv = self._read_dotenv()
        self.assertIn("YOUJIA_API_KEY=sk-new", dotenv)
        self.assertIn("OTHER=keep", dotenv)
        self.assertNotIn("YOUJIA_API_KEY=sk-old", dotenv)

    def test_overwrite_local_env_preserves_other_vars(self):
        """overwrite_local_env 只覆盖 YOUJIA_API_KEY，保留其他变量"""
        with open(self.env_path, "w", encoding="utf-8") as f:
            f.write("FOO=bar\nYOUJIA_API_KEY=sk-old\n")
        with patch("save_config.get_skill_env_path", return_value=self.env_path):
            result = save_config.overwrite_local_env("sk-fresh")
        self.assertTrue(result["env_updated"])
        self.assertEqual(os.environ.get("YOUJIA_API_KEY"), "sk-fresh")
        dotenv = self._read_dotenv()
        self.assertIn("FOO=bar", dotenv)
        self.assertIn("YOUJIA_API_KEY=sk-fresh", dotenv)


# ============================================================
# 8. YoujiaError 异常测试
# ============================================================

class TestYoujiaError(unittest.TestCase):
    """测试 YoujiaError 异常类"""

    def test_error_creation(self):
        """异常创建和属性访问"""
        e = YoujiaError(404, "Not Found", "/api/test", {"raw": "data"})
        self.assertEqual(e.code, 404)
        self.assertEqual(e.message, "Not Found")
        self.assertEqual(e.api, "/api/test")
        self.assertEqual(e.raw, {"raw": "data"})
        self.assertIn("[", str(e))

    def test_error_with_negative_code(self):
        """code 为负数"""
        e = YoujiaError(-1, "Unknown", "/api", {})
        self.assertEqual(e.code, -1)


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]] + sys.argv[1:], verbosity=2)
