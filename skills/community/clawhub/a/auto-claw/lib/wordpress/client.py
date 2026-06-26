# -*- coding: utf-8 -*-
"""
WordPress客户端

职责：
1. 与WordPress站点通信（REST API）
2. 封装常用操作（获取文章、发布评论、更新设置等）
3. 错误处理与重试

设计思路：
- 简单HTTP客户端 > 重量级SDK
- 先实现最小功能集，再逐步扩展
"""
import requests
from typing import Optional, Dict, Any, List
from urllib.parse import urljoin
from lib.audit.logger import AuditLogger


class WordPressClient:
    """
    WordPress REST API客户端
    
    使用WordPress REST API与站点通信
    支持 Basic Auth 和 Application Password 认证
    """
    
    def __init__(self, site_url: str, username: str, password: str, audit_logger: AuditLogger):
        self.site_url = site_url.rstrip("/")
        self.username = username
        self.password = password
        self.audit = audit_logger
        self._session = requests.Session()
        self._session.auth = (username, password)
        self._session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "Auto-Claw/1.0 (WordPress Operations Manager)"
        })
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """发送HTTP请求"""
        url = urljoin(self.site_url + "/", endpoint.lstrip("/"))
        self.audit.log("wordpress", "request", {
            "method": method,
            "url": url,
            "username": self.username
        })
        
        response = self._session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def get_posts(self, params: Optional[Dict] = None) -> List[Dict]:
        """
        获取文章列表
        
        Args:
            params: 查询参数 (per_page, page, status, search等)
            
        Returns:
            文章列表
        """
        default_params = {"per_page": 10, "page": 1}
        if params:
            default_params.update(params)
        
        data = self._request("GET", "/wp-json/wp/v2/posts", params=default_params)
        return data if isinstance(data, list) else data.get("data", [])
    
    def get_post(self, post_id: int) -> Dict:
        """获取单篇文章"""
        return self._request("GET", f"/wp-json/wp/v2/posts/{post_id}")
    
    def create_post(self, title: str, content: str, status: str = "draft", 
                    categories: Optional[List[int]] = None,
                    tags: Optional[List[int]] = None) -> Dict:
        """
        创建文章
        
        Args:
            title: 标题
            content: 内容
            status: 状态 (draft, publish, private)
            categories: 分类ID列表
            tags: 标签ID列表
        """
        payload = {
            "title": title,
            "content": content,
            "status": status
        }
        if categories:
            payload["categories"] = categories
        if tags:
            payload["tags"] = tags
        
        return self._request("POST", "/wp-json/wp/v2/posts", json=payload)
    
    def update_post(self, post_id: int, **kwargs) -> Dict:
        """更新文章"""
        return self._request("POST", f"/wp-json/wp/v2/posts/{post_id}", json=kwargs)
    
    def delete_post(self, post_id: int, force: bool = False) -> Dict:
        """
        删除文章
        
        Args:
            post_id: 文章ID
            force: 是否强制删除（绕过回收站）
        """
        return self._request("DELETE", f"/wp-json/wp/v2/posts/{post_id}", 
                            params={"force": force})
    
    def get_categories(self) -> List[Dict]:
        """获取分类列表"""
        data = self._request("GET", "/wp-json/wp/v2/categories", params={"per_page": 100})
        return data if isinstance(data, list) else []
    
    def get_tags(self) -> List[Dict]:
        """获取标签列表"""
        data = self._request("GET", "/wp-json/wp/v2/tags", params={"per_page": 100})
        return data if isinstance(data, list) else []
    
    def get_comments(self, post_id: Optional[int] = None) -> List[Dict]:
        """获取评论"""
        params = {}
        if post_id:
            params["post"] = post_id
        data = self._request("GET", "/wp-json/wp/v2/comments", params=params)
        return data if isinstance(data, list) else []
    
    def get_site_info(self) -> Dict:
        """获取站点信息"""
        return self._request("GET", "/wp-json/wp/v2/settings")
    
    def test_connection(self) -> bool:
        """
        测试连接是否正常
        
        Returns:
            True if connection successful
        """
        try:
            self.get_site_info()
            self.audit.log("wordpress", "connection_ok", {"site": self.site_url})
            return True
        except Exception as e:
            self.audit.log("wordpress", "connection_failed", {
                "site": self.site_url,
                "error": str(e)
            })
            return False
