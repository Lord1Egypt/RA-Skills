#!/usr/bin/env python3
"""
CDISC Library API 客户端封装
- 认证管理
- 请求缓存
- 速率限制
- 错误处理
"""

import os
import time
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

try:
    import requests
except ImportError:
    print("需要安装 requests: pip install requests")
    exit(1)


class CDISCClient:
    """CDISC Library API 客户端"""
    
    BASE_URL = "https://api.library.cdisc.org/api"
    CACHE_DIR = Path(__file__).parent / ".cache"
    CACHE_TTL = timedelta(hours=1)
    RATE_LIMIT_DELAY = 0.1  # 100ms
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化客户端
        
        Args:
            api_key: API Key，如不提供则从环境变量或 TOOLS.md 读取
        """
        self.api_key = api_key or self._load_api_key()
        if not self.api_key:
            raise ValueError(
                "未找到 API Key，请:\n"
                "1. 在 TOOLS.md 中添加 'CDISC API Key: xxx'\n"
                "2. 或设置环境变量 CDISC_API_KEY"
            )
        
        self.headers = {
            "api-key": self.api_key,
            "Accept": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self._last_request_time = 0
        
        # 创建缓存目录
        self.CACHE_DIR.mkdir(exist_ok=True)
    
    def _load_api_key(self) -> Optional[str]:
        """从环境变量或 TOOLS.md 加载 API Key"""
        # 优先环境变量
        if os.getenv("CDISC_API_KEY"):
            return os.getenv("CDISC_API_KEY")
        
        # 尝试从 TOOLS.md 读取
        tools_path = Path(__file__).parent.parent.parent / "TOOLS.md"
        if tools_path.exists():
            content = tools_path.read_text(encoding="utf-8")
            for line in content.split("\n"):
                # 支持格式：**API Key**: `xxx` 或 - API Key: xxx
                if "API Key" in line and "`" in line:
                    # 提取反引号中的内容
                    import re
                    match = re.search(r'`([a-zA-Z0-9]{32,})`', line)
                    if match:
                        return match.group(1)
                elif "API Key" in line and ":" in line:
                    key = line.split(":", 1)[1].strip().strip("`'\"")
                    if key and len(key) >= 32:
                        return key
        
        return None
    
    def _rate_limit(self):
        """速率限制"""
        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < self.RATE_LIMIT_DELAY:
            time.sleep(self.RATE_LIMIT_DELAY - elapsed)
        self._last_request_time = time.time()
    
    def _get_cache_path(self, endpoint: str) -> Path:
        """获取缓存文件路径"""
        safe_name = endpoint.replace("/", "_").replace("?", "_").replace("=", "_")
        return self.CACHE_DIR / f"{safe_name}.json"
    
    def _load_cache(self, endpoint: str) -> Optional[Any]:
        """加载缓存"""
        cache_path = self._get_cache_path(endpoint)
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 检查过期
            cached_at = datetime.fromisoformat(data["_cached_at"])
            if datetime.now() - cached_at > self.CACHE_TTL:
                cache_path.unlink()
                return None
            
            return data["_data"]
        except (json.JSONDecodeError, KeyError, OSError):
            return None
    
    def _save_cache(self, endpoint: str, data: Any):
        """保存缓存"""
        cache_path = self._get_cache_path(endpoint)
        cache_data = {
            "_cached_at": datetime.now().isoformat(),
            "_data": data
        }
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except OSError:
            pass  # 缓存失败不影响主流程
    
    def _get(self, endpoint: str, params: Optional[Dict] = None, use_cache: bool = True) -> Dict:
        """
        发送 GET 请求
        
        Args:
            endpoint: API 端点路径
            params: 查询参数
            use_cache: 是否使用缓存
        
        Returns:
            JSON 响应数据
        """
        # 检查缓存
        cache_key = f"{endpoint}?{json.dumps(params or {})}"
        if use_cache:
            cached = self._load_cache(cache_key)
            if cached:
                return cached
        
        # 速率限制
        self._rate_limit()
        
        # 发送请求
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # 保存缓存
            if use_cache:
                self._save_cache(cache_key, data)
            
            return data
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise ValueError("API Key 无效或已过期")
            elif e.response.status_code == 404:
                raise ValueError(f"资源不存在：{endpoint}")
            elif e.response.status_code == 429:
                raise ValueError("请求过于频繁，请稍后重试")
            else:
                raise ValueError(f"API 错误：{e.response.status_code}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"网络错误：{e}")
    
    # ==================== 产品相关 ====================
    
    def get_products(self) -> Dict:
        """获取所有产品类别"""
        return self._get("/mdr/products")
    
    def get_qrs_instruments(self) -> List[Dict]:
        """获取 QRS 量表列表"""
        data = self._get("/mdr/products/QrsInstrument")
        return data.get("_links", {}).get("instruments", [])
    
    # ==================== QRS 量表相关 ====================
    
    def get_instrument(self, instrument: str, version: str, expand: bool = False) -> Dict:
        """
        获取量表详情
        
        Args:
            instrument: 量表代码（如 AIMS01）
            version: 版本号（如 2-0）
            expand: 是否扩展关联实体
        """
        endpoint = f"/mdr/qrs/instruments/{instrument}/versions/{version}"
        params = {"expand": "true"} if expand else None
        return self._get(endpoint, params)
    
    def get_instrument_items(self, instrument: str, version: str) -> List[Dict]:
        """获取量表项目列表"""
        endpoint = f"/mdr/qrs/instruments/{instrument}/versions/{version}/items"
        data = self._get(endpoint)
        return data.get("_embedded", {}).get("qrsInstrumentItem", [])
    
    def get_instrument_response_groups(self, instrument: str, version: str) -> List[Dict]:
        """获取量表响应组"""
        endpoint = f"/mdr/qrs/instruments/{instrument}/versions/{version}/responseGroups"
        data = self._get(endpoint)
        return data.get("_embedded", {}).get("qrsResponseGroup", [])
    
    def get_root_instrument(self, instrument: str) -> Dict:
        """获取版本无关的量表根信息"""
        return self._get(f"/mdr/root/qrs/instruments/{instrument}")
    
    # ==================== ADaM 相关 ====================
    
    def get_adam_product(self, product: str) -> Dict:
        """获取 ADaM 产品详情"""
        return self._get(f"/mdr/adam/{product}")
    
    def get_adam_datastructures(self, product: str) -> List[Dict]:
        """获取 ADaM 数据结构列表"""
        data = self._get(f"/mdr/adam/{product}/datastructures")
        return data.get("_links", {}).get("dataStructures", [])
    
    def get_adam_varsets(self, product: str, datastructure: str) -> List[Dict]:
        """获取变量集列表"""
        endpoint = f"/mdr/adam/{product}/datastructures/{datastructure}/varsets"
        data = self._get(endpoint)
        return data.get("_embedded", {}).get("adamVarset", [])
    
    def get_adam_varset(self, product: str, datastructure: str, varset: str) -> Dict:
        """获取变量集详情"""
        endpoint = f"/mdr/adam/{product}/datastructures/{datastructure}/varsets/{varset}"
        return self._get(endpoint)
    
    # ==================== CDASH/SDTM 相关 ====================
    
    def get_cdash(self, version: str) -> Dict:
        """获取 CDASH 版本详情"""
        return self._get(f"/mdr/cdash/{version}")
    
    def get_cdash_domains(self, version: str) -> List[Dict]:
        """获取 CDASH 域列表"""
        data = self._get(f"/mdr/cdash/{version}/domains")
        return data.get("_embedded", {}).get("cdashDomain", [])
    
    def get_sdtmig(self, version: str) -> Dict:
        """获取 SDTMIG 版本详情"""
        return self._get(f"/mdr/sdtmig/{version}")
    
    def get_sdtmig_domains(self, version: str) -> List[Dict]:
        """获取 SDTMIG 域列表"""
        data = self._get(f"/mdr/sdtmig/{version}/domains")
        return data.get("_embedded", {}).get("sdtmDomain", [])
    
    # ==================== 受控术语相关 ====================
    
    def get_ct_packages(self) -> List[Dict]:
        """获取术语包列表"""
        data = self._get("/mdr/ct/packages")
        return data.get("_embedded", {}).get("ctPackage", [])
    
    def get_ct_codelists(self) -> List[Dict]:
        """获取代码列表列表"""
        data = self._get("/mdr/ct/codelists")
        return data.get("_embedded", {}).get("ctCodelist", [])
    
    def get_ct_codelist(self, codelist: str) -> Dict:
        """获取代码列表详情"""
        return self._get(f"/mdr/ct/codelists/{codelist}")
    
    def get_ct_terms(self, codelist: str) -> List[Dict]:
        """获取术语列表"""
        endpoint = f"/mdr/ct/codelists/{codelist}/terms"
        data = self._get(endpoint)
        return data.get("_embedded", {}).get("ctTerm", [])
    
    # ==================== 版本比较 ====================
    
    def compare_versions(self, product_type: str, product_id: str, v1: str, v2: str) -> Dict:
        """
        比较两个版本
        
        Args:
            product_type: 产品类型（qrs, adam, cdash, sdtmig）
            product_id: 产品 ID
            v1: 版本 1
            v2: 版本 2
        """
        endpoint = f"/mdr/compare/{product_type}/{product_id}/versions/{v1}/to/{v2}"
        return self._get(endpoint, use_cache=False)
    
    def compare_to_previous(self, product_type: str, product_id: str, version: str) -> Dict:
        """比较与上一版本的差异"""
        endpoint = f"/mdr/compare/{product_type}/{product_id}/versions/{version}/to/previous"
        return self._get(endpoint, use_cache=False)
    
    # ==================== 搜索 ====================
    
    def search_instruments(self, keyword: str) -> List[Dict]:
        """搜索量表（本地过滤）"""
        instruments = self.get_qrs_instruments()
        return [
            inst for inst in instruments
            if keyword.lower() in inst.get("title", "").lower()
            or keyword.upper() in inst.get("href", "").upper()
        ]
    
    def clear_cache(self):
        """清除缓存"""
        import shutil
        if self.CACHE_DIR.exists():
            shutil.rmtree(self.CACHE_DIR)
            self.CACHE_DIR.mkdir()


# ==================== 快捷测试 ====================

if __name__ == "__main__":
    # 测试连接
    client = CDISCClient()
    
    print("测试 CDISC API 连接...")
    try:
        products = client.get_products()
        print(f"✓ 连接成功！找到 {len(products.get('_links', {}))} 个产品类别")
    except ValueError as e:
        print(f"✗ 错误：{e}")
