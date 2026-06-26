"""API 服务模块

提供 HTTP 请求功能，自动处理认证和数据加密。

设计说明：
- VRAPIClient 是完整的 HTTP 客户端，负责所有网络请求
- VRAPIClient 内部统一调用 VRAPI 网络服务器（vr-api请求服务器）完成网络请求和加密
- ApiService 只做薄封装，所有网络 I/O 都经由 VRAPI 网络服务器
- 强制约束：所有请求必须通过 VRAPI 网络服务器客户端调用，禁止通过其他方式直接发起网络请求

这种设计的优点：
1. 所有网络请求都通过 VRAPI 网络服务器统一管理
2. 数据加密逻辑与网络请求逻辑分离又内聚
3. 便于后续扩展和维护
"""

import base64
import gzip
import json
import os
import platform
import stat
import subprocess
import urllib.request
from typing import Any, Dict, Optional, Union

from .config import get_config

# VRAPI 网络服务器下载地址（用于客户端自举）
DEFAULT_VRAPI_CDN = "https://async.he29.com/public/app/mcp/cli"


class VRAPIClient:
    """VRAPI 网络服务客户端（完整 HTTP 客户端）

    核心职责：
    1. 管理 vr-api请求服务器 路径
    2. 通过 vr-api请求服务器 对请求数据进行加密处理
    3. 通过 vr-api请求服务器 发送 HTTP 请求
    4. 强制执行请求门禁：禁止绕过客户端直接请求网络

    客户端文件下载到 ~/.9kvr/client/ 目录
    统一由 get_config().client_dir 获取路径

    目录结构：
    - ~/.9kvr/client/          # vr-api CLI 客户端文件
    - ~/.9kvr/auth/            # 认证信息
    - ~/.9kvr/skills/cache/    # Skills/MCP 缓存数据
    """

    # 单例实例，用于全局共享 VRAPIClient
    _instance: Optional['VRAPIClient'] = None
    _last_login_key: Optional[str] = None

    def __init__(self):
        """初始化 VR API 客户端
        """
        # 查找本地 vr-api CLI 客户端
        self._client_path = self._find_client()
        # 若不存在则自动下载
        if not self._client_path:
            self._download_client()

    def _get_client_candidates(self) -> list[str]:
        """根据系统返回客户端候选文件名（每个平台唯一文件名）"""
        system = platform.system().lower()
        if system == "darwin":
            return ["vr-api-darwin"]
        if system == "windows":
            return ["vr-api-win.exe"]
        return ["vr-api-linux"]

    def _get_client_dir(self) -> str:
        """获取客户端目录路径

        Returns:
            客户端目录路径（~/.9kvr/client/）
        """
        return get_config().client_dir

    def _find_client(self) -> Optional[str]:
        """查找本地 vr-api CLI 客户端

        查找顺序：
        1. 先在客户端目录 (~/.9kvr/client/) 查找
        2. 再在 PATH 环境变量中查找

        Returns:
            客户端路径，如果未找到则返回 None
        """
        client_dir = self._get_client_dir()
        # 第一步：在客户端目录中按候选名查找
        for client_name in self._get_client_candidates():
            client_path = os.path.join(client_dir, client_name)
            if os.path.exists(client_path):
                return client_path

        # 第二步：在 PATH 环境变量中查找
        for path in os.environ.get('PATH', '').split(os.pathsep):
            for client_name in self._get_client_candidates():
                full_path = os.path.join(path, client_name)
                if os.path.exists(full_path):
                    return full_path

        return None

    def _download_client(self) -> bool:
        """下载 VRAPI 网络服务器客户端（静默执行）"""
        client_dir = self._get_client_dir()
        os.makedirs(client_dir, exist_ok=True)

        cdn = os.getenv("VRAPI_CDN", DEFAULT_VRAPI_CDN).rstrip("/")
        for client_name in self._get_client_candidates():
            client_path = os.path.join(client_dir, client_name)
            gz_url = f"{cdn}/{client_name}.gz"
            gz_path = f"{client_path}.gz"

            try:
                urllib.request.urlretrieve(gz_url, gz_path)
                with gzip.open(gz_path, "rb") as f_in, open(client_path, "wb") as f_out:
                    f_out.write(f_in.read())
                try:
                    os.remove(gz_path)
                except OSError:
                    pass
                os.chmod(client_path, os.stat(client_path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                self._client_path = client_path
                return True
            except Exception:
                try:
                    urllib.request.urlretrieve(f"{cdn}/{client_name}", client_path)
                    os.chmod(client_path, os.stat(client_path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                    self._client_path = client_path
                    return True
                except Exception:
                    continue
        return False

    def _ensure_client(self) -> bool:
        """确保客户端可用：不存在则自动下载"""
        if self._client_path and os.path.exists(self._client_path):
            return True
        self._client_path = self._find_client()
        if self._client_path and os.path.exists(self._client_path):
            return True
        return self._download_client()

    def _ensure_login(self) -> Optional[str]:
        """强制登录门禁：所有业务请求前必须先登录成功"""
        if not self._ensure_client():
            return "VRAPI 网络服务器不可用"

        config = get_config()
        uid = config.uid
        token = config.token
        if not uid or not token:
            return "未配置账号信息，请先提供 uid 和 token"

        login_key = f"{uid}:{token}"
        if self._last_login_key == login_key:
            return None

        try:
            result = subprocess.run(
                [self._client_path, "-login", "-uid", uid, "-token", token],
                capture_output=True,
                text=True,
                timeout=15,
            )
            if result.returncode != 0:
                return result.stderr.strip() or "登录失败"
            # 约定：登录成功后，VRAPI 客户端会在后续请求中自动携带 uid/token。
            # 因此调用 Python 脚本发业务请求时，不需要再次显式传 uid/token。
            self._last_login_key = login_key
            return None
        except subprocess.TimeoutExpired:
            return "登录超时"
        except Exception as e:
            return f"登录异常: {e}"

    def request(
        self,
        method: str,
        api: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """发送完整的 HTTP 请求（核心方法）

        所有网络请求必须通过 VRAPI 网络服务器完成，本方法只负责参数组装与结果解析。
        禁止通过 urllib/requests/httpx 等其他方式直接调用网络。

        Args:
            method: HTTP 方法，支持 GET/POST/PUT/PATCH/DELETE
            api: API 路径
            data: 请求数据
            headers: 自定义请求头

        Returns:
            响应数据（JSON 解析后的字典），包含 success 字段表示请求是否成功
        """
        if not self._ensure_client():
            return {
                "success": False,
                "error": "VRAPI 网络服务器不可用"
            }
        login_error = self._ensure_login()
        if login_error:
            return {
                "success": False,
                "error": login_error
            }

        config = get_config()

        # 准备数据（注入 uid 和 token）
        prepared_data = self._prepare_data(data)

        try:
            cmd = [
                self._client_path,
                "-request",
                "-method", method.upper(),
                "-api", api,
                "-data", json.dumps(prepared_data, ensure_ascii=False),
                "-timeout", str(max(1, int(config.timeout / 1000))),
            ]
            if headers:
                cmd.extend(["-headers", json.dumps(headers, ensure_ascii=False)])

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=max(5, int(config.timeout / 1000) + 5)
            )
            if result.returncode != 0:
                return {
                    "success": False,
                    "error": result.stderr.strip() or "vr-api 请求失败"
                }
            raw = result.stdout.strip()
            if not raw:
                return {"success": True}
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return {"success": True, "data": raw}
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "vr-api 请求超时"}
        except Exception as e:
            # 其他未知错误
            return {
                "success": False,
                "error": str(e)
            }

    def _prepare_data(self, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """准备请求数据，自动注入认证信息

        Args:
            data: 原始请求数据

        Returns:
            处理后的请求数据（包含 uid 和 token）
        """
        if data is None:
            data = {}

        # 从配置中获取认证信息。
        # 说明：即使不手动传 uid/token，登录成功后客户端也会自动带上认证信息。
        # 这里保留注入逻辑用于兼容后端部分接口对显式字段的要求。
        config = get_config()

        # 注入用户 ID
        if config.uid:
            data["uid"] = config.uid

        # 注入访问令牌
        if config.token:
            data["token"] = config.token

        return data

    @classmethod
    def get_instance(cls) -> 'VRAPIClient':
        """获取单例实例

        Returns:
            VRAPIClient 单例实例
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


class ApiService:
    """API 服务类（薄封装层）

    职责：
    - 提供简洁的 API 方法（get/post/put/patch/delete）
    - 将请求委托给 VRAPIClient 处理

    注意：
    - 此类不再直接进行网络调用，所有网络请求都通过 VRAPI 网络服务器
    - 禁止新增任何绕过 VRAPI 客户端的网络调用代码
    """

    def __init__(self, timeout: Optional[int] = None):
        """初始化 API 服务

        Args:
            timeout: 请求超时时间（毫秒），默认使用配置中的值
        """
        config = get_config()
        self._timeout = timeout or config.timeout

    def get(self, path: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """发送 GET 请求

        Args:
            path: API 路径
            data: 请求数据（将作为查询参数附加到 URL）
            headers: 自定义请求头

        Returns:
            响应数据（JSON 解析后的字典）
        """
        return self._make_request("GET", path, data, headers)

    def post(self, path: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """发送 POST 请求

        Args:
            path: API 路径
            data: 请求数据（将作为请求体发送）
            headers: 自定义请求头

        Returns:
            响应数据（JSON 解析后的字典）
        """
        return self._make_request("POST", path, data, headers)

    def put(self, path: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """发送 PUT 请求

        Args:
            path: API 路径
            data: 请求数据（将作为请求体发送）
            headers: 自定义请求头

        Returns:
            响应数据（JSON 解析后的字典）
        """
        return self._make_request("PUT", path, data, headers)

    def patch(self, path: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """发送 PATCH 请求

        Args:
            path: API 路径
            data: 请求数据（将作为请求体发送）
            headers: 自定义请求头

        Returns:
            响应数据（JSON 解析后的字典）
        """
        return self._make_request("PATCH", path, data, headers)

    def delete(self, path: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """发送 DELETE 请求

        Args:
            path: API 路径
            data: 请求数据（将作为查询参数附加到 URL）
            headers: 自定义请求头

        Returns:
            响应数据（JSON 解析后的字典）
        """
        return self._make_request("DELETE", path, data, headers)

    def _make_request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """发送 HTTP 请求的通用方法

        委托给 VRAPIClient 处理实际的网络请求

        Args:
            method: HTTP 方法 (GET/POST/PUT/PATCH/DELETE)
            path: API 路径
            data: 请求数据
            headers: 自定义请求头

        Returns:
            响应数据（JSON 解析后的字典）
        """
        # 获取 VRAPIClient 单例，将请求委托给它
        client = VRAPIClient.get_instance()

        # 调用 VRAPIClient.request() 发送请求
        # VRAPIClient 内部会：
        # 1. 请求参数始终按服务端协议加密
        # 2. 通过 VRAPI 网络服务器发送 HTTP 请求
        return client.request(
            method=method,
            api=path,
            data=data,
            headers=headers
        )

    def multipart_upload(
        self,
        path: str,
        files: Dict[str, tuple],
        fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """发送 multipart/form-data 文件上传请求（通过 VRAPI 网络服务器）"""
        client = VRAPIClient.get_instance()
        if not client._ensure_client():
            return {"code": -1, "msg": "VRAPI 网络服务器不可用"}
        login_error = client._ensure_login()
        if login_error:
            return {"code": -1, "msg": login_error}

        # 获取认证信息
        config = get_config()
        all_fields: Dict[str, Any] = {}
        if fields:
            all_fields.update(fields)
        if config.uid:
            all_fields["uid"] = config.uid
        if config.token:
            all_fields["token"] = config.token

        files_payload: Dict[str, Dict[str, str]] = {}
        for field, (filename, content, content_type) in files.items():
            if isinstance(content, str):
                content = content.encode("utf-8")
            files_payload[field] = {
                "filename": filename,
                "content_type": content_type or "application/octet-stream",
                "content_base64": base64.b64encode(content).decode("utf-8"),
            }

        try:
            cmd = [
                client._client_path,
                "-request",
                "-multipart",
                "-method", "POST",
                "-api", path,
                "-data", json.dumps(all_fields, ensure_ascii=False),
                "-files", json.dumps(files_payload, ensure_ascii=False),
                "-timeout", str(max(1, int(self._timeout / 1000))),
            ]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=max(10, int(self._timeout / 1000) + 15)
            )
            if result.returncode != 0:
                return {"code": -1, "msg": result.stderr.strip() or "vr-api 上传失败"}
            raw = result.stdout.strip()
            if not raw:
                return {"code": 1, "msg": "ok"}
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"code": -1, "msg": "上传响应解析失败"}
        except subprocess.TimeoutExpired:
            return {"code": -1, "msg": "上传超时"}
        except Exception as e:
            return {"code": -1, "msg": f"Request Error: {str(e)}"}


# 全局 API 实例（延迟初始化）
_api_instance: Optional[ApiService] = None


def get_api() -> ApiService:
    """获取全局 API 实例

    Returns:
        ApiService 单例实例
    """
    global _api_instance
    if _api_instance is None:
        _api_instance = ApiService()
    return _api_instance


def get_upload_url(path: str = "/api/upload/uploadExtraFile") -> str:
    """获取文件上传的完整 URL

    Args:
        path: 上传接口路径

    Returns:
        完整的上传 URL
    """
    return path


def config_account(uid: str, token: str) -> Dict[str, Any]:
    """配置用户账号信息

    通过调用 vr-api -login 命令验证并保存账号信息。
    账号信息会保存到 ~/.9kvr/auth/vr-session.json

    后续所有 API 请求都会自动使用这个账号信息，
    调用 Python 脚本发业务请求时无需再显式传入 uid/token。

    Args:
        uid: 用户ID
        token: 认证令牌

    Returns:
        配置结果，包含 success 和 message 字段

    Example:
        >>> result = config_account("<UID>", "<TOKEN>")
        >>> if result["success"]:
        ...     print(result["message"])
    """
    # 获取 vr-api 客户端路径
    client = VRAPIClient.get_instance()
    if not client._ensure_client():
        return {
            "success": False,
            "message": "VRAPI 网络服务器不可用"
        }
    client_path = client._client_path

    if not client_path or not os.path.exists(client_path):
        return {
            "success": False,
            "message": "VRAPI 网络服务器不可用"
        }

    try:
        # 调用 vr-api -login 命令
        result = subprocess.run(
            [client_path, "-login", "-uid", uid, "-token", token],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            # stderr 包含错误信息
            error_msg = result.stderr.strip()
            if not error_msg:
                error_msg = "登录失败"
            return {
                "success": False,
                "message": error_msg
            }

        # 登录成功，stderr 有成功信息
        client._last_login_key = f"{uid}:{token}"
        return {
            "success": True,
            "message": result.stderr.strip() or f"账号配置成功！UID: {uid}"
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "message": "账号配置超时，请重试"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"账号配置失败: {str(e)}"
        }
