import requests
import json
import os
import uuid
from pathlib import Path
from urllib.parse import urlparse
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from typing import Optional, Dict, Any, List

class BaseCommerceClient:
    """
    Universal Agentic Commerce client. Supports stateless token-based auth,
    cart management, product discovery, and multi-merchant credential isolation.

    Credentials are stored per-domain under:
      ~/.openclaw/credentials/agent-commerce-engine/<domain>/
    """
    def __init__(self, base_url: str, brand_id: str = None):
        self.base_url = base_url.rstrip('/')

        # Security: Enforce HTTPS for production endpoints
        if not self.base_url.startswith('https://') and not any(h in self.base_url for h in ['localhost', '127.0.0.1']):
            raise ValueError(f"Insecure URL blocked: Commerce API must use HTTPS. Provided: {self.base_url}")

        # Derive store_id from the URL domain (e.g., "shop.example.com")
        parsed = urlparse(self.base_url)
        self.store_id = parsed.hostname or "unknown"

        # DEPRECATED: brand_id is kept for backward compatibility.
        # Brand-specific skills may still pass it for display purposes.
        # Will be removed in a future major version.
        self.brand_id = brand_id or self.store_id

        # Credential storage: isolated per domain
        self.config_dir = Path.home() / ".openclaw" / "credentials" / "agent-commerce-engine" / self.store_id
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.creds_file = self.config_dir / "creds.json"
        self.visitor_file = self.config_dir / "visitor.json"

        # MIGRATION: If old flat-file credentials exist, migrate them to the new structure
        self._migrate_legacy_credentials(brand_id)

        self.session = self._setup_session()

    def _migrate_legacy_credentials(self, legacy_brand_id: str = None):
        """Migrate old flat-file credentials ({brand_id}_creds.json) to new per-domain subfolder."""
        if legacy_brand_id is None:
            return
        legacy_dir = self.config_dir.parent  # ~/.openclaw/credentials/agent-commerce-engine/
        legacy_creds = legacy_dir / f"{legacy_brand_id}_creds.json"
        legacy_visitor = legacy_dir / f"{legacy_brand_id}_visitor.json"
        if legacy_creds.exists() and not self.creds_file.exists():
            legacy_creds.rename(self.creds_file)
        if legacy_visitor.exists() and not self.visitor_file.exists():
            legacy_visitor.rename(self.visitor_file)

    def _setup_session(self):
        s = requests.Session()
        retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        s.mount("http://", adapter)
        s.mount("https://", adapter)
        
        # 注入 Visitor ID
        visitor_id = self._get_visitor_id()
        s.headers.update({"x-visitor-id": visitor_id})
        
        # 注入身份信息（Token）
        creds = self.load_credentials()
        if creds:
            s.headers.update({
                "x-user-account": str(creds.get("account", "")),
                "x-api-token": str(creds.get("token", ""))
            })
        return s

    def _get_visitor_id(self) -> str:
        if not self.visitor_file.exists():
            visitor_id = str(uuid.uuid4())
            with open(self.visitor_file, "w") as f:
                json.dump({"visitor_id": visitor_id}, f)
            return visitor_id
        try:
            with open(self.visitor_file, "r") as f:
                return json.load(f).get("visitor_id")
        except:
            return str(uuid.uuid4())

    def save_credentials(self, account, token):
        """保存 Token 而非密码"""
        with open(self.creds_file, "w") as f:
            json.dump({"account": account, "token": token}, f)
        os.chmod(self.creds_file, 0o600)
        # 更新当前会话
        self.session.headers.update({
            "x-user-account": account,
            "x-api-token": token
        })
        # 移除旧的密码头（如果存在）
        self.session.headers.pop("x-user-password", None)

    def load_credentials(self) -> Optional[Dict]:
        if self.creds_file.exists():
            try:
                with open(self.creds_file, "r") as f:
                    return json.load(f)
            except:
                return None
        return None

    def delete_credentials(self):
        if self.creds_file.exists():
            self.creds_file.unlink()
        self.session.headers.pop("x-user-account", None)
        self.session.headers.pop("x-api-token", None)
        self.session.headers.pop("x-user-password", None)

    def reset_visitor_id(self):
        """重置访客 ID，用于隔离不同会话的购物车内容"""
        if self.visitor_file.exists():
            self.visitor_file.unlink()
        visitor_id = str(uuid.uuid4())
        with open(self.visitor_file, "w") as f:
            json.dump({"visitor_id": visitor_id}, f)
        self.session.headers.update({"x-visitor-id": visitor_id})
        return visitor_id

    def request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        try:
            response = self.session.request(method, url, timeout=10, **kwargs)
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        try:
            data = response.json()
            if not isinstance(data, dict):
                data = {"result": data}
            if response.status_code >= 400:
                data.setdefault("success", False)
                data.setdefault("status_code", response.status_code)
                # Map common HTTP errors to standard codes if backend didn't provide one
                if "error" not in data:
                    code_map = {401: "AUTH_REQUIRED", 403: "ACTION_DENIED", 404: "PRODUCT_NOT_FOUND", 429: "RATE_LIMITED", 500: "INTERNAL_ERROR"}
                    data["error"] = code_map.get(response.status_code, "BAD_REQUEST")
            return data
        except:
            return {
                "success": False,
                "error": "INTERNAL_ERROR",
                "instruction": f"Server returned non-JSON response (HTTP {response.status_code}).",
                "status_code": response.status_code
            }

    # --- 身份验证增强 (Token/注册) ---

    def get_api_token(self, account, password):
        """用密码换取 API Token"""
        url = f"{self.base_url}/auth/token"
        try:
            response = self.session.post(url, json={"account": account, "password": password}, timeout=10)
            result = self._handle_response(response)
            if result.get("success") and result.get("token"):
                self.save_credentials(account, result["token"])
            return result
        except Exception as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}

    def send_verification_code(self, email: str, type: str = 'register'):
        auth_url = self.base_url.replace('/v1', '') if '/v1' in self.base_url else self.base_url
        url = f"{auth_url}/auth/send-code"
        try:
            response = self.session.post(url, json={"email": email, "type": type}, timeout=10)
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}

    def register(self, email: str, password: str, name: str = None, code: str = None, invite_code: str = None):
        auth_url = self.base_url.replace('/v1', '') if '/v1' in self.base_url else self.base_url
        url = f"{auth_url}/auth/register"
        payload = {
            "email": email,
            "password": password,
            "name": name,
            "emailCode": code,
            "inviteCode": invite_code,
            "visitorId": self._get_visitor_id()
        }
        try:
            response = self.session.post(url, json=payload, timeout=10)
            result = self._handle_response(response)
            if result.get("success") and result.get("token"):
                # 注册成功后自动保存 Token
                self.save_credentials(email, result["token"])
            return result
        except Exception as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}

    # --- 核心业务接口 ---
    
    def search_products(self, query: str, page: int = 1, limit: int = 50):
        return self.request("GET", "/products", params={"q": query, "page": page, "limit": limit})

    def list_products(self, page: int = 1, limit: int = 50):
        return self.request("GET", "/products", params={"page": page, "limit": limit})

    def get_product(self, slug: str):
        return self.request("GET", f"/products/{slug}")

    def get_profile(self):
        return self.request("GET", "/user/profile")

    def update_profile(self, data: Dict):
        return self.request("PUT", "/user/profile", json=data)

    def get_cart(self):
        return self.request("GET", "/cart")

    def modify_cart(self, action: str, product_slug: str, variant: str, quantity: int = 1):
        method = "POST" if action == "add" else "PUT"
        payload = {
            "product_slug": product_slug,
            "variant": variant,
            "quantity": quantity
        }

        return self.request(method, "/cart", json=payload)

    def remove_from_cart(self, product_slug: str, variant: str):
        payload = {
            "product_slug": product_slug,
            "variant": variant
        }
        
        return self.request("DELETE", "/cart", json=payload)

    def clear_cart(self):
        return self.request("DELETE", "/cart", json={"clear_all": True})

    def get_promotions(self):
        return self.request("GET", "/promotions")

    def get_brand_info(self, category: str):
        return self.request("GET", "/brand", params={"category": category})

    def list_orders(self):
        return self.request("GET", "/orders")

    def create_order(self, shipping: Dict):
        """
        Creates an order from the current shopping cart.
        Requires a shipping dictionary with necessary fields like name, phone, province, city, address.
        """
        payload = {"shipping": shipping}
        return self.request("POST", "/orders", json=payload)
