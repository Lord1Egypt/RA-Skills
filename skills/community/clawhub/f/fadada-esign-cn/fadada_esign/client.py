#!/usr/bin/env python3
"""
法大大电子签客户端 - FASC API 5.0

核心功能：
- 获取AccessToken
- 上传文件
- 创建签署任务
- 获取签署链接
- 查询签署状态
- 下载已签署文档
"""

import os
import json
import hashlib
import hmac
import time
import uuid
import requests
from typing import Optional, Dict, Any, List
from pathlib import Path

from .exceptions import FaDaDaError, FaDaDaAuthError, FaDaDaAPIError, FaDaDaFileError
from .signer import Signer


class FaDaDaClient:
    """
    法大大电子签客户端 (FASC API 5.0)
    
    使用示例：
        >>> from fadada_esign import FaDaDaClient, Signer
        >>> client = FaDaDaClient(
        ...     app_id="your_app_id",
        ...     app_secret="your_app_secret",
        ...     open_corp_id="your_corp_id"
        ... )
        >>> signer = Signer(name="张三", mobile="13800138000")
        >>> result = client.send_document(
        ...     file_path="/path/to/contract.pdf",
        ...     signers=[signer],
        ...     task_subject="合同签署"
        ... )
        >>> print(result["sign_url"])
    """
    
    # API 端点
    PROD_URL = "https://api.fadada.com/api/v5"
    SANDBOX_URL = "https://testapi.fadada.com/api/v5"
    
    def __init__(
        self,
        app_id: str,
        app_secret: str,
        open_corp_id: str,
        server_url: Optional[str] = None,
        sandbox: bool = False
    ):
        self.app_id = app_id
        self.app_secret = app_secret
        self.open_corp_id = open_corp_id
        
        if server_url:
            self.server_url = server_url.rstrip("/")
        elif sandbox:
            self.server_url = self.SANDBOX_URL
        else:
            self.server_url = self.PROD_URL
            
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0
        
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/x-www-form-urlencoded"
        })
    
    @staticmethod
    def _sort_parameters(params: Dict[str, Any]) -> str:
        """按 key ASCII 排序并拼接成字符串"""
        sorted_params = sorted([
            (k, str(v)) for k, v in params.items() 
            if v is not None and v != ""
        ])
        return "&".join([f"{k}={v}" for k, v in sorted_params])
    
    def _generate_signature(self, param_str: str, timestamp: str) -> str:
        """FASC 5.0 签名算法（两步 HMAC-SHA256）"""
        sign_text = hashlib.sha256(param_str.encode("utf-8")).hexdigest()
        secret_signing = hmac.new(
            self.app_secret.encode("utf-8"),
            timestamp.encode("utf-8"),
            hashlib.sha256
        ).digest()
        signature = hmac.new(
            secret_signing,
            sign_text.encode("utf-8"),
            hashlib.sha256
        ).hexdigest().lower()
        return signature
    
    def _build_headers(
        self,
        access_token: Optional[str] = None,
        biz_content: Optional[str] = None
    ) -> tuple[Dict[str, str], str]:
        """构建请求头"""
        timestamp = str(int(time.time() * 1000))
        nonce = uuid.uuid4().hex[:32]
        
        sign_params = {
            "X-FASC-App-Id": self.app_id,
            "X-FASC-Sign-Type": "HMAC-SHA256",
            "X-FASC-Timestamp": timestamp,
            "X-FASC-Nonce": nonce,
            "X-FASC-Api-SubVersion": "5.1"
        }
        
        if access_token:
            sign_params["X-FASC-AccessToken"] = access_token
        
        if biz_content:
            sign_params["bizContent"] = biz_content
        
        param_str = self._sort_parameters(sign_params)
        signature = self._generate_signature(param_str, timestamp)
        
        headers = {
            "X-FASC-App-Id": self.app_id,
            "X-FASC-Sign-Type": "HMAC-SHA256",
            "X-FASC-Sign": signature,
            "X-FASC-Timestamp": timestamp,
            "X-FASC-Nonce": nonce,
            "X-FASC-Api-SubVersion": "5.1",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        if access_token:
            headers["X-FASC-AccessToken"] = access_token
        
        data = {}
        if biz_content:
            data["bizContent"] = biz_content
            
        return headers, data
    
    def _request(
        self,
        endpoint: str,
        biz_content: Optional[Dict] = None,
        access_token: Optional[str] = None,
        method: str = "POST"
    ) -> Dict[str, Any]:
        """发起 API 请求"""
        url = f"{self.server_url}{endpoint}"
        
        if access_token is None and endpoint != "/service/get-access-token":
            access_token = self._get_access_token()
        
        biz_content_str = None
        if biz_content:
            biz_content_str = json.dumps(biz_content, separators=(",", ":"), ensure_ascii=False)
        
        headers, data = self._build_headers(access_token, biz_content_str)
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers, params=data, timeout=30)
            else:
                response = self.session.post(url, headers=headers, data=data, timeout=30)
            
            response.raise_for_status()
            result = response.json()
            
            code = result.get("code")
            if code not in [100000, "100000"]:
                msg = result.get("msg", "Unknown error")
                raise FaDaDaAPIError(msg, code=code, response=result)
            
            return result.get("data", {})
            
        except requests.RequestException as e:
            raise FaDaDaError(f"Request failed: {e}")
    
    def _get_access_token(self) -> str:
        """获取 Access Token（带缓存）"""
        if self._access_token and time.time() < self._token_expires_at:
            return self._access_token
        
        result = self._request(
            "/service/get-access-token",
            biz_content={"grantType": "client_credential"},
            access_token=None
        )
        
        self._access_token = result.get("accessToken")
        expires_in = int(result.get("expiresIn", 7200))
        self._token_expires_at = time.time() + expires_in - 300
        
        return self._access_token
    
    # ==================== 文件操作 ====================
    
    def upload_file(self, file_path: str) -> str:
        """
        上传文件并返回 fileId
        
        Args:
            file_path: 本地文件路径
            
        Returns:
            fileId: 文件ID，用于后续创建签署任务
        """
        if not os.path.exists(file_path):
            raise FaDaDaFileError(f"File not found: {file_path}")
        
        # 1. 获取上传地址
        upload_data = self._request(
            "/file/get-upload-url",
            biz_content={"fileType": "doc"}
        )
        
        upload_url = upload_data.get("uploadUrl")
        fdd_file_url = upload_data.get("fddFileUrl")
        
        # 2. 上传文件到 OSS
        try:
            with open(file_path, 'rb') as f:
                response = requests.put(upload_url, data=f, timeout=60)
            
            if response.status_code != 200:
                raise FaDaDaFileError(f"Upload failed: HTTP {response.status_code}")
        except Exception as e:
            raise FaDaDaFileError(f"Upload error: {e}")
        
        # 3. 处理文件获取 fileId
        file_name = os.path.basename(file_path)
        file_format = file_name.split('.')[-1].lower() if '.' in file_name else 'pdf'
        
        process_data = self._request(
            "/file/process",
            biz_content={
                "fddFileUrlList": [{
                    "fileType": "doc",
                    "fddFileUrl": fdd_file_url,
                    "fileName": file_name,
                    "fileFormat": file_format
                }]
            }
        )
        
        file_id_list = process_data.get("fileIdList", [])
        if not file_id_list:
            raise FaDaDaAPIError("Failed to get fileId")
        
        return file_id_list[0].get("fileId")
    
    # ==================== 签署任务 ====================
    
    def create_sign_task(
        self,
        task_subject: str,
        file_id: str,
        signers: List[Signer],
        doc_id: str = "doc1",
        auto_start: bool = True,
        auto_finish: bool = True
    ) -> str:
        """
        创建签署任务
        
        Args:
            task_subject: 任务主题
            file_id: 文件ID
            signers: 签署人列表
            doc_id: 文档ID（默认 doc1）
            auto_start: 是否自动开始
            auto_finish: 是否自动结束
            
        Returns:
            signTaskId: 签署任务ID
        """
        # 构建文档列表
        docs = [{
            "docId": doc_id,
            "docName": task_subject,
            "docFileId": file_id
        }]
        
        # 构建签署人列表
        actors = [signer.to_dict() for signer in signers]
        
        result = self._request(
            "/sign-task/create",
            biz_content={
                "initiator": {
                    "idType": "corp",
                    "openId": self.open_corp_id
                },
                "signTaskSubject": task_subject,
                "signDocType": "contract",
                "autoStart": auto_start,
                "autoFinish": auto_finish,
                "docs": docs,
                "actors": actors
            }
        )
        
        return result.get("signTaskId")
    
    def get_sign_url(self, sign_task_id: str, actor_id: str = "signer1") -> str:
        """
        获取签署链接
        
        Args:
            sign_task_id: 签署任务ID
            actor_id: 签署人ID（默认 signer1）
            
        Returns:
            签署链接URL
        """
        result = self._request(
            "/sign-task/actor/get-url",
            biz_content={
                "signTaskId": sign_task_id,
                "actorId": actor_id
            }
        )
        
        return result.get("actorSignTaskUrl")
    
    def query_task_detail(self, sign_task_id: str) -> Dict[str, Any]:
        """
        查询签署任务详情
        
        Args:
            sign_task_id: 签署任务ID
            
        Returns:
            任务详情
        """
        return self._request(
            "/sign-task/app/get-detail",
            biz_content={"signTaskId": sign_task_id}
        )
    
    def get_download_url(self, sign_task_id: str) -> str:
        """
        获取已签署文档下载链接
        
        Args:
            sign_task_id: 签署任务ID
            
        Returns:
            下载链接
        """
        result = self._request(
            "/sign-task/owner/get-download-url",
            biz_content={
                "ownerId": {
                    "idType": "corp",
                    "openId": self.open_corp_id
                },
                "signTaskId": sign_task_id,
                "fileType": "doc"
            }
        )
        
        return result.get("downloadUrl")
    
    # ==================== 一键式API ====================
    
    def send_document(
        self,
        file_path: str,
        signers: List[Signer],
        task_subject: Optional[str] = None,
        return_result: bool = True
    ) -> Dict[str, Any]:
        """
        一键发送文档签署（完整流程）
        
        自动完成：上传文件 → 创建任务 → 获取签署链接
        
        Args:
            file_path: 文件路径
            signers: 签署人列表
            task_subject: 任务主题（默认使用文件名）
            return_result: 是否返回完整结果
            
        Returns:
            {
                "sign_task_id": "任务ID",
                "sign_url": "签署链接",
                "task_subject": "任务主题",
                "file_path": "文件路径",
                "signers": [签署人信息]
            }
        """
        if not task_subject:
            task_subject = os.path.basename(file_path)
        
        # 1. 上传文件
        file_id = self.upload_file(file_path)
        
        # 2. 创建签署任务
        sign_task_id = self.create_sign_task(
            task_subject=task_subject,
            file_id=file_id,
            signers=signers
        )
        
        # 3. 获取签署链接（取第一个签署人）
        sign_url = None
        if signers:
            sign_url = self.get_sign_url(sign_task_id, signers[0].actor_id)
        
        result = {
            "sign_task_id": sign_task_id,
            "sign_url": sign_url,
            "task_subject": task_subject,
            "file_path": file_path,
            "signers": [
                {
                    "name": s.name,
                    "mobile": s.mobile,
                    "actor_id": s.actor_id
                }
                for s in signers
            ]
        }
        
        return result
    
    def send_to_single_signer(
        self,
        file_path: str,
        signer_name: str,
        signer_mobile: str,
        task_subject: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        发送给单个签署人（最简API）
        
        Args:
            file_path: 文件路径
            signer_name: 签署人姓名
            signer_mobile: 签署人手机号
            task_subject: 任务主题（可选）
            
        Returns:
            签署任务结果
        """
        signer = Signer(name=signer_name, mobile=signer_mobile)
        return self.send_document(
            file_path=file_path,
            signers=[signer],
            task_subject=task_subject
        )
