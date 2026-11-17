"""verify_permission 单元测试 — 覆盖权限校验服务逻辑"""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from capabilities.verify_permission.service import verify_permission
from _errors import AuthError, ServiceError


class VerifyPermissionServiceTest(unittest.TestCase):
    """verify_permission service 层逻辑"""

    @patch("capabilities.verify_permission.service.api_post")
    def test_basic_vendor(self, mock_post):
        """基础版：isAi=false, digitalModel=false"""
        mock_post.return_value = {"isAi": False, "digitalModel": False, "faceFix": False}
        result = verify_permission()
        mock_post.assert_called_once_with("/api/alibaba.1688.image.generate.vertify.permission/1.0.0", {})
        self.assertFalse(result["isAi"])
        self.assertFalse(result["digitalModel"])

    @patch("capabilities.verify_permission.service.api_post")
    def test_premium_vendor(self, mock_post):
        """高级版全权限：isAi=true, digitalModel=true"""
        mock_post.return_value = {"isAi": True, "digitalModel": True, "faceFix": False}
        result = verify_permission()
        self.assertTrue(result["isAi"])
        self.assertTrue(result["digitalModel"])

    @patch("capabilities.verify_permission.service.api_post")
    def test_premium_no_digital_model(self, mock_post):
        """高级版无数字模特：isAi=true, digitalModel=false"""
        mock_post.return_value = {"isAi": True, "digitalModel": False, "faceFix": False}
        result = verify_permission()
        self.assertTrue(result["isAi"])
        self.assertFalse(result["digitalModel"])

    @patch("capabilities.verify_permission.service.api_post")
    def test_ak_missing_raises(self, mock_post):
        """AK 未配置：api_post 抛 AuthError"""
        mock_post.side_effect = AuthError("AK 未配置")
        with self.assertRaises(AuthError):
            verify_permission()

    @patch("capabilities.verify_permission.service.api_post")
    def test_abnormal_response_raises(self, mock_post):
        """网关返回非 dict：抛 ServiceError"""
        mock_post.return_value = "not a dict"
        with self.assertRaises(ServiceError):
            verify_permission()

if __name__ == "__main__":
    unittest.main()
