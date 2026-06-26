"""e签宝 API 客户端封装。

用法（由 Agent 通过 Bash 调用）:
    python3 esign_api.py upload <file_path>
    python3 esign_api.py search_keyword <file_id> <keyword>
    python3 esign_api.py create_flow <json_config_path>
    python3 esign_api.py sign_url <sign_flow_id> <operator_id>
    python3 esign_api.py query_flow <sign_flow_id>
    python3 esign_api.py revoke_flow <sign_flow_id> <reason>
    python3 esign_api.py download_docs <sign_flow_id> [output_dir]
    python3 esign_api.py verify <file_id_or_path> [sign_flow_id]
"""
import base64
import hashlib
import hmac
import json
import os
import sys
import tempfile
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# 凭证加载优先级：
# 1. ~/.config/esign-contract/.env（推荐，路径固定，不受 Skill 安装目录影响）
# 2. 系统环境变量（ESIGN_APP_ID / ESIGN_APP_SECRET / ESIGN_BASE_URL）
# 不再依赖 Skill 目录下的 .env，避免相对路径因安装/执行目录不确定而失效
_CONFIG_DIR = Path.home() / ".config" / "esign-contract"
_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
load_dotenv(_CONFIG_DIR / ".env")


def _atomic_write_json(path: str, data: dict):
    """原子写入 JSON 文件：先写临时文件，再 os.replace 替换，避免并发读到半写入数据。"""
    dir_name = os.path.dirname(path) or "."
    fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


class ESignAPIError(Exception):
    """e签宝 API 调用错误。"""
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"e签宝 API 错误 [{code}]: {message}")


class ESignClient:
    """e签宝 API 客户端，支持签名鉴权和 Token 鉴权两种方式。"""

    def __init__(self, **kwargs):
        self.app_id = kwargs.get("app_id") or os.environ["ESIGN_APP_ID"]
        self.app_secret = kwargs.get("app_secret") or os.environ["ESIGN_APP_SECRET"]
        self.base_url = kwargs.get("base_url") or os.environ.get(
            "ESIGN_BASE_URL", "https://openapi.esign.cn"
        )
        self.base_url = self.base_url.rstrip("/")
        self._token_cache_path = kwargs.get("token_cache_path") or str(
            _CONFIG_DIR / "token_cache.json"
        )
        # 鉴权方式：auto（默认，先签名后 token）、signature、token
        self._auth_mode = kwargs.get("auth_mode") or os.environ.get(
            "ESIGN_AUTH_MODE", "auto"
        )

    # ── HmacSHA256 签名鉴权 ──────────────────────────────────────

    @staticmethod
    def _content_md5(body: bytes) -> str:
        if not body:
            return ""
        return base64.b64encode(hashlib.md5(body).digest()).decode()

    def _sign(self, method: str, path: str, content_type: str, content_md5: str) -> str:
        accept = "*/*"
        parts = [method.upper(), accept, content_md5, content_type, ""]
        string_to_sign = "\n".join(parts) + "\n" + path
        signature = hmac.new(
            self.app_secret.encode(), string_to_sign.encode(), hashlib.sha256
        ).digest()
        return base64.b64encode(signature).decode()

    def _signature_headers(self, method: str, path: str, body: bytes = b"") -> dict:
        content_type = "application/json; charset=UTF-8" if body else ""
        content_md5 = self._content_md5(body)
        sig = self._sign(method, path, content_type, content_md5)
        headers = {
            "X-Tsign-Open-App-Id": self.app_id,
            "X-Tsign-Open-Ca-Signature": sig,
            "Accept": "*/*",
        }
        if content_md5:
            headers["Content-MD5"] = content_md5
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    # ── OAuth Token 鉴权 ─────────────────────────────────────────

    def _get_token(self) -> str:
        cached = self._read_token_cache()
        if cached:
            return cached
        return self._fetch_new_token()

    def _read_token_cache(self):
        try:
            with open(self._token_cache_path, "r") as f:
                data = json.load(f)
            if data.get("expires_at", 0) > time.time() + 300:
                return data["token"]
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            pass
        return None

    def _fetch_new_token(self) -> str:
        resp = requests.get(
            f"{self.base_url}/v1/oauth2/access_token",
            params={
                "appId": self.app_id,
                "secret": self.app_secret,
                "grantType": "client_credentials",
            },
        )
        result = resp.json()
        if result.get("code") != 0:
            raise ESignAPIError(result.get("code"), result.get("message", "获取 token 失败"))
        token = result["data"]["token"]
        expires_in = int(result["data"]["expiresIn"])
        # expiresIn 是毫秒时间戳
        expires_at = expires_in / 1000 if expires_in > 1e12 else time.time() + expires_in
        _atomic_write_json(self._token_cache_path, {"token": token, "expires_at": expires_at})
        return token

    def _token_headers(self, body: bytes = b"") -> dict:
        headers = {
            "X-Tsign-Open-App-Id": self.app_id,
            "X-Tsign-Open-Token": self._get_token(),
        }
        if body:
            headers["Content-Type"] = "application/json; charset=UTF-8"
        return headers

    # ── 统一请求 ─────────────────────────────────────────────────

    def _request(self, method: str, path: str, **kwargs) -> dict:
        url = f"{self.base_url}{path}"
        body = b""
        if "json" in kwargs:
            json_data = kwargs.pop("json")
            if json_data is not None:
                body = json.dumps(json_data, ensure_ascii=False).encode("utf-8")
                kwargs["data"] = body

        modes = (
            ["signature", "token"] if self._auth_mode == "auto"
            else [self._auth_mode]
        )

        last_error = None
        for mode in modes:
            if mode == "signature":
                headers = self._signature_headers(method, path, body)
            else:
                headers = self._token_headers(body)

            for attempt in range(3):
                resp = requests.request(method, url, headers=headers, timeout=30, **kwargs)
                if resp.status_code == 429:
                    time.sleep(2 ** attempt)
                    continue
                result = resp.json()
                if result.get("code") == 401 and mode == "signature" and len(modes) > 1:
                    last_error = result
                    break  # 签名鉴权失败，尝试 token
                if result.get("code") != 0:
                    raise ESignAPIError(result.get("code"), result.get("message", "未知错误"))
                # 签名鉴权成功，锁定模式
                if self._auth_mode == "auto" and mode == "signature":
                    self._auth_mode = "signature"
                elif self._auth_mode == "auto" and mode == "token":
                    self._auth_mode = "token"
                return result.get("data", {})
            else:
                if mode == modes[-1]:
                    raise ESignAPIError(-1, "请求超过重试次数限制")

        raise ESignAPIError(
            last_error.get("code") if last_error else -1,
            last_error.get("message", "鉴权失败") if last_error else "鉴权失败",
        )

    # ── File Operations ───────────────────────────────────────────

    def upload_file(self, file_path: str) -> str:
        """上传本地文件到 e签宝，返回 fileId。"""
        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")

        file_size = p.stat().st_size
        if file_size > 50 * 1024 * 1024:
            print(json.dumps({"warning": f"文件较大（{file_size // 1024 // 1024}MB），上传可能需要较长时间"}),
                  file=sys.stderr)
        content_type_map = {
            ".pdf": "application/pdf",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".doc": "application/msword",
            ".odt": "application/vnd.oasis.opendocument.text",
        }
        content_type = content_type_map.get(p.suffix.lower(), "application/octet-stream")

        # 计算文件 MD5
        file_bytes = p.read_bytes()
        file_md5 = base64.b64encode(hashlib.md5(file_bytes).digest()).decode()

        # Step 1: 获取上传地址
        upload_params = {
            "fileName": p.name,
            "fileSize": file_size,
            "contentType": content_type,
            "contentMd5": file_md5,
        }
        # 非 PDF 文件需要服务端转换为 PDF
        if p.suffix.lower() != ".pdf":
            upload_params["convertToPDF"] = True
        data = self._request("POST", "/v3/files/file-upload-url", json=upload_params)
        file_id = data["fileId"]
        upload_url = data["fileUploadUrl"]

        # Step 2: PUT 文件到上传地址
        resp = requests.put(
            upload_url,
            data=file_bytes,
            headers={
                "Content-Type": content_type,
                "Content-MD5": file_md5,
            },
            timeout=60,
        )
        if resp.status_code not in (200, 201):
            raise ESignAPIError(-1, f"文件上传失败，HTTP {resp.status_code}")

        return file_id

    def search_keyword(self, file_id: str, keyword: str) -> list:
        """检索文件中关键字的坐标位置。

        V3 接口路径: POST /v3/files/{fileId}/keyword-positions
        注意: 返回坐标为关键字第一个字的左下角位置。
        返回: keywordPositions[].positions[].coordinates[].{positionX, positionY}
        """
        data = self._request("POST", f"/v3/files/{file_id}/keyword-positions", json={
            "keywords": [keyword],
        })
        keyword_positions = data.get("keywordPositions", [])
        matched_positions = []
        for item in keyword_positions:
            if not item.get("searchResult"):
                continue
            if not item.get("positions"):
                continue
            matched_positions.append(item)
        return matched_positions

    @staticmethod
    def calc_seal_position(keyword_x: float, keyword_y: float,
                           keyword_len: int = 5, font_size: float = 12,
                           seal_width: float = 159, seal_height: float = 159) -> dict:
        """根据关键字坐标计算签章定位坐标。

        关键字坐标（keyword API 返回）是第一个字左下角位置，PDF 坐标系（Y 从底部往上）。
        signFieldPosition 的坐标也是 PDF 坐标系，positionY 为签章区域的底边 Y。
        需要偏移使签章居中覆盖关键字区域。

        Args:
            keyword_x: 关键字第一个字左下角 X
            keyword_y: 关键字第一个字左下角 Y（PDF 坐标，从页面底部起算）
            keyword_len: 关键字字符数（用于计算关键字宽度）
            font_size: 关键字字号（pt）
            seal_width: 签章宽度（pt, 默认159≈56mm）
            seal_height: 签章高度（pt, 默认159≈56mm）

        Returns:
            {"positionX": float, "positionY": float} 签章定位坐标
        """
        keyword_width = keyword_len * font_size
        # X: 签章左边紧贴关键字右侧
        seal_x = keyword_x + keyword_width
        # Y: 签章垂直居中对齐关键字文本中心
        seal_y = keyword_y + font_size / 2 - seal_height / 2
        return {"positionX": round(seal_x, 2), "positionY": round(seal_y, 2)}

    def create_sign_flow(self, flow_config: dict) -> str:
        """基于文件发起签署流程，返回 signFlowId。"""
        data = self._request(
            "POST", "/v3/sign-flow/create-by-file", json=flow_config
        )
        return data["signFlowId"]

    def get_sign_url(self, sign_flow_id: str, operator_account: str,
                      org_info: dict = None) -> dict:
        """获取签署页面链接。

        Args:
            sign_flow_id: 签署流程ID
            operator_account: 经办人手机号/邮箱
            org_info: 企业信息（可选），格式 {"orgName": "xxx"} 或 {"orgId": "xxx"}
        """
        body = {
            "needLogin": True,
            "urlType": 2,
            "operator": {
                "psnAccount": operator_account,
            },
        }
        if org_info:
            body["organization"] = org_info
        return self._request(
            "POST",
            f"/v3/sign-flow/{sign_flow_id}/sign-url",
            json=body,
        )

    def query_flow(self, sign_flow_id: str) -> dict:
        """查询签署流程详情。"""
        return self._request("GET", f"/v3/sign-flow/{sign_flow_id}/detail")

    def revoke_flow(self, sign_flow_id: str, reason: str) -> dict:
        """撤销签署流程。

        仅签署中的流程可撤销，撤销后流程终止变为已撤销状态。
        注意：签署方已完成签字盖章后撤销需获得全部已完成盖章签署方同意。

        Args:
            sign_flow_id: 签署流程ID
            reason: 撤销原因
        """
        return self._request(
            "POST",
            f"/v3/sign-flow/{sign_flow_id}/revoke",
            json={"revokeReason": reason},
        )

    def download_flow_documents(self, sign_flow_id: str, output_dir: str = "") -> list:
        """下载签署完成的文件。

        前提：流程状态必须为已完成（signFlowStatus=2）。
        先获取下载地址，再下载文件到本地。

        Args:
            sign_flow_id: 签署流程ID
            output_dir: 输出目录，默认使用系统临时目录（tempfile.gettempdir()）

        Returns:
            list: 下载的文件信息 [{"fileId": ..., "fileName": ..., "filePath": ...}]
        """
        # Step 1: 检查流程状态
        detail = self.query_flow(sign_flow_id)
        status = detail.get("signFlowStatus")
        status_desc = detail.get("signFlowDescription", "")
        if status != 2:
            raise ESignAPIError(
                -1,
                f"流程当前状态为「{status_desc}」（status={status}），仅已完成的流程可下载签署文件",
            )

        # Step 2: 获取下载地址
        data = self._request(
            "GET",
            f"/v3/sign-flow/{sign_flow_id}/file-download-url",
        )
        files = data.get("files", [])
        if not files:
            raise ESignAPIError(-1, "未找到可下载的签署文件")

        # Step 3: 下载文件到本地
        if not output_dir:
            output_dir = tempfile.gettempdir()
        os.makedirs(output_dir, exist_ok=True)
        downloaded = []
        for f in files:
            file_name = f.get("fileName", f"signed_{f.get('fileId', 'unknown')}.pdf")
            download_url = f.get("downloadUrl") or f.get("fileDownloadUrl")
            if not download_url:
                continue
            file_path = os.path.join(output_dir, file_name)
            resp = requests.get(download_url, timeout=60)
            if resp.status_code != 200:
                raise ESignAPIError(-1, f"文件下载失败: {file_name}，HTTP {resp.status_code}")
            with open(file_path, "wb") as out:
                out.write(resp.content)
            downloaded.append({
                "fileId": f.get("fileId"),
                "fileName": file_name,
                "filePath": file_path,
                "fileSize": len(resp.content),
            })

        return downloaded

    def query_file_status(self, file_id: str) -> dict:
        """查询文件上传状态。"""
        return self._request("GET", f"/v3/files/{file_id}")

    def verify_signature(self, file_id: str, sign_flow_id: str = None) -> dict:
        """核验合同文件签名有效性。

        解析 PDF 文件中签署者数字证书信息，验证内容或签名是否被篡改。

        Args:
            file_id: 待验签的文件 ID（若为本地文件，需先通过 upload 获取 fileId）
            sign_flow_id: 签署流程 ID（可选，指定后可关联流程验证）

        Returns:
            dict: 验签结果，包含签名信息、证书信息、篡改检测结果等
        """
        body = {}
        if sign_flow_id:
            body["signFlowId"] = sign_flow_id
        return self._request("POST", f"/v3/files/{file_id}/verify", json=body if body else None)


_FLOW_HISTORY_PATH = str(_CONFIG_DIR / "flow_history.json")


def save_flow_record(sign_flow_id: str, contract_name: str, parties: list):
    """记录签署流程到本地历史。

    parties 支持两种格式（向后兼容）：
    - 字符串列表: ["甲方名称", "乙方名称"]  → 自动转为 {"name": x, "role": ""}
    - 结构化列表: [{"name": "张三", "role": "甲方", "phone": "138xxx"}]
    """
    from datetime import datetime

    normalized = []
    for p in parties:
        if isinstance(p, str):
            normalized.append({"name": p, "role": "", "phone": ""})
        elif isinstance(p, dict):
            normalized.append({
                "name": p.get("name", ""),
                "role": p.get("role", ""),
                "phone": p.get("phone", ""),
            })
        else:
            normalized.append({"name": str(p), "role": "", "phone": ""})

    history = _load_flow_history()
    history["flows"].append({
        "signFlowId": sign_flow_id,
        "contractName": contract_name,
        "parties": normalized,
        "createdAt": datetime.now().isoformat(),
    })
    _atomic_write_json(_FLOW_HISTORY_PATH, history)


def list_flow_records() -> list:
    """列出所有签署流程历史记录。"""
    return _load_flow_history().get("flows", [])


def _load_flow_history() -> dict:
    try:
        with open(_FLOW_HISTORY_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"flows": []}


# ── CLI Entry Point ───────────────────────────────────────────

def _cli():
    """命令行入口，供 Agent 通过 Bash 调用。"""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "用法: python3 esign_api.py <command> [args...]"}))
        sys.exit(1)

    client = ESignClient()
    cmd = sys.argv[1]

    try:
        if cmd == "upload":
            file_path = sys.argv[2]
            file_id = client.upload_file(file_path)
            print(json.dumps({"fileId": file_id}))

        elif cmd == "search_keyword":
            file_id, keyword = sys.argv[2], sys.argv[3]
            result = client.search_keyword(file_id, keyword)
            print(json.dumps({"keywordPositions": result}, ensure_ascii=False))

        elif cmd == "create_flow":
            config_path = sys.argv[2]
            with open(config_path, "r") as f:
                config = json.load(f)
            flow_id = client.create_sign_flow(config)
            print(json.dumps({"signFlowId": flow_id}))

        elif cmd == "sign_url":
            flow_id, operator_account = sys.argv[2], sys.argv[3]
            org_info = None
            if len(sys.argv) > 4:
                org_info = json.loads(sys.argv[4])
            result = client.get_sign_url(flow_id, operator_account, org_info)
            print(json.dumps(result, ensure_ascii=False))

        elif cmd == "query_flow":
            flow_id = sys.argv[2]
            result = client.query_flow(flow_id)
            print(json.dumps(result, ensure_ascii=False))

        elif cmd == "file_status":
            file_id = sys.argv[2]
            result = client.query_file_status(file_id)
            print(json.dumps(result, ensure_ascii=False))

        elif cmd == "save_flow":
            flow_id, name = sys.argv[2], sys.argv[3]
            # Support JSON array for structured parties: '[{"name":"x","role":"甲方","phone":"138xxx"}]'
            if len(sys.argv) == 5 and sys.argv[4].startswith('['):
                parties = json.loads(sys.argv[4])
            else:
                parties = sys.argv[4:]
            save_flow_record(flow_id, name, parties)
            print(json.dumps({"saved": True}))

        elif cmd == "list_flows":
            flows = list_flow_records()
            print(json.dumps({"flows": flows}, ensure_ascii=False))

        elif cmd == "revoke_flow":
            flow_id = sys.argv[2]
            reason = sys.argv[3] if len(sys.argv) > 3 else "用户主动撤销"
            result = client.revoke_flow(flow_id, reason)
            print(json.dumps({"revoked": True, "signFlowId": flow_id, **result}, ensure_ascii=False))

        elif cmd == "download_docs":
            flow_id = sys.argv[2]
            output_dir = sys.argv[3] if len(sys.argv) > 3 else tempfile.gettempdir()
            files = client.download_flow_documents(flow_id, output_dir)
            print(json.dumps({"files": files}, ensure_ascii=False))

        elif cmd == "verify":
            file_id_or_path = sys.argv[2]
            sign_flow_id = sys.argv[3] if len(sys.argv) > 3 else None
            # 如果传入的是文件路径，先上传获取 fileId
            if os.path.exists(file_id_or_path):
                file_id = client.upload_file(file_id_or_path)
            else:
                file_id = file_id_or_path
            result = client.verify_signature(file_id, sign_flow_id)
            print(json.dumps(result, ensure_ascii=False))

        else:
            print(json.dumps({"error": f"未知命令: {cmd}"}))
            sys.exit(1)

    except ESignAPIError as e:
        print(json.dumps({"error": e.message, "code": e.code}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    _cli()
