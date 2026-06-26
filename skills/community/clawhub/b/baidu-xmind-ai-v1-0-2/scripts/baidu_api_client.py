#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度智能文档分析平台 - 统一API客户端

支持文档抽取、文档解析、文档比对、合同审查、文档格式转换
"""

import os
import json
import time
import base64
import requests
from typing import Dict, Optional, Any
from pathlib import Path


class BaiduDocAIClient:
    """百度智能文档分析平台API客户端"""
    
    # API基础URL
    API_URLS = {
        "extract": "https://aip.baidubce.com/rest/2.0/brain/online/v1",
        "parse": "https://aip.baidubce.com/rest/2.0/brain/online/v2",
        "parse_vl": "https://aip.baidubce.com/rest/2.0/brain/online/v2",
        "compare": "https://aip.baidubce.com/file/2.0/brain/online/v1",
        "contract_review": "https://aip.baidubce.com/file/2.0/brain/online/v1",
        "convert": "https://aip.baidubce.com/rest/2.0/ocr/v1"
    }
    
    # API端点
    API_ENDPOINTS = {
        "extract": {"submit": "extract/task", "query": "extract/query_task"},
        "parse": {"submit": "parser/task", "query": "parser/task/query"},
        "parse_vl": {"submit": "paddle-vl-parser/task", "query": "paddle-vl-parser/task/query"},
        "compare": {"submit": "textdiff/create_task", "query": "textdiff/query_task"},
        "contract_review": {"submit": "textreview/task", "query": "textreview/task/query"},
        "convert": {"submit": "doc_convert/request", "query": "doc_convert/get_request_result"}
    }
    
    TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"
    POLL_INTERVAL = 5
    POLL_TIMEOUT = 600
    
    def __init__(self, api_key: str = None, secret_key: str = None):
        """初始化客户端"""
        self.api_key = api_key or os.environ.get("BAIDU_DOC_AI_API_KEY")
        self.secret_key = secret_key or os.environ.get("BAIDU_DOC_AI_SECRET_KEY")
        
        if not self.api_key or not self.secret_key:
            raise ValueError(
                "请配置百度文档AI凭证！\n"
                "方式1: 设置环境变量\n"
                "  export BAIDU_DOC_AI_API_KEY=您的API_KEY\n"
                "  export BAIDU_DOC_AI_SECRET_KEY=您的SECRET_KEY\n\n"
                "方式2: 创建配置文件 ~/.baidu_doc_ai_config\n"
                "  [credentials]\n"
                "  api_key = 您的API_KEY\n"
                "  secret_key = 您的SECRET_KEY"
            )
        
        self.access_token = None
    
    def _get_access_token(self) -> str:
        """获取access_token"""
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key
        }
        response = requests.post(self.TOKEN_URL, data=params, timeout=10)
        result = response.json()
        
        if "access_token" not in result:
            raise Exception(f"获取access_token失败: {result}")
        
        self.access_token = result["access_token"]
        return self.access_token
    
    @staticmethod
    def file_to_base64(file_path: str) -> str:
        """文件转base64"""
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    
    def _submit_task(self, api_type: str, data: Dict) -> str:
        """提交任务"""
        if not self.access_token:
            self._get_access_token()
        
        base_url = self.API_URLS[api_type]
        endpoint = self.API_ENDPOINTS[api_type]["submit"]
        url = f"{base_url}/{endpoint}?access_token={self.access_token}"
        
        response = requests.post(url, data=data, timeout=30)
        result = response.json()
        
        if result.get("error_code"):
            raise Exception(f"提交任务失败 ({result.get('error_code')}): {result.get('error_msg', 'Unknown error')}")
        
        # 不同的API返回不同的task_id字段名
        if "result" in result and "task_id" in result["result"]:
            return result["result"]["task_id"]
        elif "result" in result and "taskId" in result["result"]:
            return result["result"]["taskId"]
        else:
            return list(result.values())[0]
    
    def _query_task(self, api_type: str, task_id: str) -> Dict:
        """查询任务"""
        if not self.access_token:
            self._get_access_token()
        
        base_url = self.API_URLS[api_type]
        endpoint = self.API_ENDPOINTS[api_type]["query"]
        url = f"{base_url}/{endpoint}?access_token={self.access_token}"
        
        # 不同的API使用不同的查询参数
        if api_type in ["compare", "contract_review"]:
            # 这些API需要 multipart/form-data 格式
            # 使用 (None, value) 格式发送字符串作为multipart/form-data
            response = requests.post(url, files={"taskId": (None, task_id)}, timeout=30)
        elif api_type == "convert":
            response = requests.post(url, params={"request_id": task_id}, data={"data": task_id}, timeout=30)
        else:
            response = requests.post(url, data={"task_id": task_id}, timeout=30)
        
        return response.json()
    
    def _poll_result(self, api_type: str, task_id: str) -> Dict:
        """轮询结果"""
        initial_delay = {"contract_review": 60}.get(api_type, 5)
        time.sleep(initial_delay)
        
        start_time = time.time()
        while time.time() - start_time < self.POLL_TIMEOUT:
            result = self._query_task(api_type, task_id)
            
            # 处理不同的响应格式
            if api_type == "convert":
                if result.get("ret_code") == 1:
                    return result
                elif result.get("error_code"):
                    raise Exception(f"查询任务失败 ({result.get('error_code')}): {result.get('error_msg', 'Unknown')}")
            else:
                status = result.get("result", {}).get("status", "")
                if status == "success":
                    return result
                elif status == "failed":
                    error_msg = result.get("result", {}).get("task_error", "Unknown error")
                    raise Exception(f"任务失败: {error_msg}")
            
            time.sleep(self.POLL_INTERVAL)
        
        raise Exception(f"轮询超时（{self.POLL_TIMEOUT}秒）")
    
    # ==================== 文档抽取 ====================
    def extract(self, **kwargs) -> Dict:
        """文档抽取"""
        data = {}
        
        if kwargs.get("file_data"):
            data["file_data"] = kwargs["file_data"]
        elif kwargs.get("file_url"):
            data["file_url"] = kwargs["file_url"]
        else:
            raise ValueError("必须提供 file_url 或 file_data")
        
        if kwargs.get("manifest"):
            data["manifest"] = json.dumps(kwargs["manifest"])
        elif kwargs.get("fields"):
            data["manifest"] = json.dumps(kwargs["fields"])
        
        if kwargs.get("manifest_version_id"):
            data["manifest_version_id"] = kwargs["manifest_version_id"]
        if kwargs.get("remove_duplicates"):
            data["remove_duplicates"] = "true"
        if kwargs.get("page_range"):
            data["page_range"] = kwargs["page_range"]
        if kwargs.get("extract_seal"):
            data["extract_seal"] = "true"
        if kwargs.get("erase_watermark"):
            data["erase_watermark"] = "true"
        if kwargs.get("doc_correct"):
            data["doc_correct"] = "true"
        
        task_id = self._submit_task("extract", data)
        return self._poll_result("extract", task_id)
    
    # ==================== 文档解析 ====================
    def parse(self, **kwargs) -> Dict:
        """文档解析"""
        data = {}
        
        if kwargs.get("file_data"):
            data["file_data"] = kwargs["file_data"]
        elif kwargs.get("file_url"):
            data["file_url"] = kwargs["file_url"]
        else:
            raise ValueError("必须提供 file_url 或 file_data")
        
        if kwargs.get("file_name"):
            data["file_name"] = kwargs["file_name"]
        else:
            raise ValueError("必须提供 file_name")
        
        # 可选参数
        optional_params = [
            "recognize_formula", "analysis_chart", "angle_adjust",
            "parse_image_layout", "language_type", "switch_digital_width",
            "html_table_format"
        ]
        for param in optional_params:
            if kwargs.get(param):
                data[param] = kwargs[param]
        
        if kwargs.get("return_doc_chunks"):
            data["return_doc_chunks"] = json.dumps(kwargs["return_doc_chunks"])
        
        task_id = self._submit_task("parse", data)
        return self._poll_result("parse", task_id)
    
    # ==================== 文档解析VL ====================
    def parse_vl(self, **kwargs) -> Dict:
        """文档解析VL"""
        data = {}
        
        if kwargs.get("file_data"):
            data["file_data"] = kwargs["file_data"]
            if kwargs.get("file_name"):
                data["file_name"] = kwargs["file_name"]
        elif kwargs.get("file_url"):
            data["file_url"] = kwargs["file_url"]
            if not kwargs.get("file_name"):
                raise ValueError("使用 file_url 时必须提供 file_name")
            data["file_name"] = kwargs["file_name"]
        else:
            raise ValueError("必须提供 file_url 或 file_data")
        
        # 可选参数
        bool_params = ["analysis_chart", "merge_tables", "relevel_titles", 
                       "recognize_seal", "return_span_boxes"]
        for param in bool_params:
            if kwargs.get(param):
                data[param] = "true"
        
        task_id = self._submit_task("parse_vl", data)
        return self._poll_result("parse_vl", task_id)
    
    # ==================== 文档比对 ====================
    def compare(self, **kwargs) -> Dict:
        """文档比对"""
        files = {}
        params = {}
        
        if kwargs.get("base_file_data"):
            files["base_file"] = ("base.pdf", kwargs["base_file_data"], "application/pdf")
        if kwargs.get("compare_file_data"):
            files["compare_file"] = ("compare.pdf", kwargs["compare_file_data"], "application/pdf")
        
        bool_params = ["seal_recognition", "hand_writing_recognition",
                       "font_family_recognition", "font_size_recognition",
                       "full_width_half_width_recognition"]
        for param in bool_params:
            if kwargs.get(param):
                params[param] = "true"
        
        task_id = self._submit_task("compare", {**params, **files})
        return self._poll_result("compare", task_id)
    
    # ==================== 合同审查 ====================
    def contract_review(self, **kwargs) -> Dict:
        """合同审查"""
        files = {}
        params = {"template_name": kwargs.get("template_name", "Sales_PartyA_V2")}
        
        if kwargs.get("file_data"):
            files["files"] = ("contract.pdf", kwargs["file_data"], "application/pdf")
        
        if kwargs.get("comment_risk_level"):
            params["comment_risk_level"] = kwargs["comment_risk_level"]
        
        task_id = self._submit_task("contract_review", {**params, **files})
        return self._poll_result("contract_review", task_id)
    
    # ==================== 文档格式转换 ====================
    def convert(self, **kwargs) -> Dict:
        """文档格式转换"""
        data = {}
        
        if kwargs.get("file_data"):
            data["file_data"] = kwargs["file_data"]
        elif kwargs.get("file_url"):
            data["file_url"] = kwargs["file_url"]
        else:
            raise ValueError("必须提供 file_url 或 file_data")
        
        task_id = self._submit_task("convert", data)
        return self._poll_result("convert", task_id)
