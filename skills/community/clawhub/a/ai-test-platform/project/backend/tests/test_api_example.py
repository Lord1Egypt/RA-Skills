"""
API 接口测试示例

使用 pytest + requests 测试 AI 生成接口
"""

import pytest
import requests
import time

BASE_URL = "http://localhost:8000"


class TestAuthAPI:
    """授权接口测试"""

    def test_create_auth_code(self):
        """测试创建授权码"""
        url = f"{BASE_URL}/api/admin/create_auth"
        data = {
            "permission": "all",
            "max_days": 365,
            "max_count": 100
        }

        response = requests.post(url, json=data)
        assert response.status_code == 200

        result = response.json()
        assert "encrypted_code" in result
        assert result["permission"] == "all"

        # 保存授权码用于后续测试
        self.auth_code = result["encrypted_code"]
        return self.auth_code


class TestGenerateAPI:
    """AI生成接口测试"""

    @pytest.fixture(scope="class")
    def auth_code(self):
        """获取授权码"""
        url = f"{BASE_URL}/api/admin/create_auth"
        data = {
            "permission": "all",
            "max_days": 365,
            "max_count": 100
        }

        response = requests.post(url, json=data)
        result = response.json()
        return result["encrypted_code"]

    def test_generate_test_case(self, auth_code):
        """测试生成测试用例"""
        url = f"{BASE_URL}/api/generate/case"
        headers = {"Authorization": f"Bearer {auth_code}"}
        data = {
            "document_content": "用户登录功能：用户输入正确的用户名和密码后，系统应该允许登录。",
            "requirements": "重点关注安全性测试"
        }

        response = requests.post(url, data=data, headers=headers)
        assert response.status_code == 200

        result = response.json()
        assert "task_id" in result
        assert result["status"] == "processing"

        # 等待生成完成
        task_id = result["task_id"]
        self._wait_for_task_completion(task_id, auth_code)

    def test_generate_api_script(self, auth_code):
        """测试生成API脚本"""
        url = f"{BASE_URL}/api/generate/api"
        headers = {"Authorization": f"Bearer {auth_code}"}
        data = {
            "document_content": "API接口：GET /api/users - 获取用户列表",
            "api_info": "返回JSON格式的用户列表"
        }

        response = requests.post(url, data=data, headers=headers)
        assert response.status_code == 200

        result = response.json()
        assert "task_id" in result

        # 等待生成完成
        task_id = result["task_id"]
        self._wait_for_task_completion(task_id, auth_code)

    def test_generate_ui_script(self, auth_code):
        """测试生成UI脚本"""
        url = f"{BASE_URL}/api/generate/ui"
        headers = {"Authorization": f"Bearer {auth_code}"}
        data = {
            "document_content": "登录页面：用户输入用户名、密码，点击登录按钮",
            "ui_info": "使用Chrome浏览器测试"
        }

        response = requests.post(url, data=data, headers=headers)
        assert response.status_code == 200

        result = response.json()
        assert "task_id" in result

        # 等待生成完成
        task_id = result["task_id"]
        self._wait_for_task_completion(task_id, auth_code)

    def _wait_for_task_completion(self, task_id, auth_code, timeout=60):
        """等待任务完成"""
        url = f"{BASE_URL}/api/generate/progress/{task_id}"
        start_time = time.time()

        while time.time() - start_time < timeout:
            response = requests.get(url)
            result = response.json()

            if result["status"] == "completed":
                print(f"\n任务完成: {result}")
                return result
            elif result["status"] == "failed":
                raise Exception(f"任务失败: {result['message']}")

            time.sleep(2)  # 每2秒查询一次

        raise Exception("任务超时")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
