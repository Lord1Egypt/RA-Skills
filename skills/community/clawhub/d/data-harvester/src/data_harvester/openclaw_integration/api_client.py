"""
OpenClaw API客户端
用于与OpenClaw平台通信
"""

import logging
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

from ..exceptions import IntegrationError, AuthenticationError, RateLimitError, TimeoutError

logger = logging.getLogger(__name__)


@dataclass
class OpenClawAPIResponse:
    """OpenClaw API响应"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    status_code: int = 200
    headers: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    @classmethod
    def from_response(cls, response: requests.Response) -> "OpenClawAPIResponse":
        """从requests响应创建"""
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            response_data = {"text": response.text}
        
        return cls(
            success=response.ok,
            data=response_data if response.ok else None,
            error=None if response.ok else response_data.get("error", response.text),
            status_code=response.status_code,
            headers=dict(response.headers),
            timestamp=datetime.now()
        )


class OpenClawAPIClient:
    """OpenClaw API客户端"""
    
    DEFAULT_TIMEOUT = 30  # 默认超时时间（秒）
    DEFAULT_RETRIES = 3   # 默认重试次数
    
    def __init__(self, base_url: str, api_key: str, timeout: int = DEFAULT_TIMEOUT):
        """
        初始化API客户端
        
        Args:
            base_url: OpenClaw API基础URL
            api_key: API密钥
            timeout: 请求超时时间（秒）
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        
        # 设置默认请求头
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "OpenClaw-DataHarvester/1.0.0"
        })
        
        logger.debug(f"OpenClaw API客户端初始化: {base_url}")
    
    def register_skill(self, skill_manifest: Dict[str, Any]) -> Dict[str, Any]:
        """
        注册技能到OpenClaw平台
        
        Args:
            skill_manifest: 技能清单
            
        Returns:
            注册结果
            
        Raises:
            IntegrationError: 注册失败
        """
        endpoint = f"{self.base_url}/api/v1/skills/register"
        
        try:
            response = self._request_with_retry(
                "POST",
                endpoint,
                json=skill_manifest
            )
            
            if not response.success:
                raise IntegrationError(f"技能注册失败: {response.error}")
            
            logger.info(f"技能注册成功: {skill_manifest.get('name')}")
            return response.data
            
        except Exception as e:
            logger.error(f"技能注册失败: {e}")
            raise IntegrationError(f"技能注册失败: {e}") from e
    
    def update_skill(self, skill_id: str, skill_manifest: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新技能信息
        
        Args:
            skill_id: 技能ID
            skill_manifest: 更新的技能清单
            
        Returns:
            更新结果
        """
        endpoint = f"{self.base_url}/api/v1/skills/{skill_id}"
        
        try:
            response = self._request_with_retry(
                "PUT",
                endpoint,
                json=skill_manifest
            )
            
            if not response.success:
                raise IntegrationError(f"技能更新失败: {response.error}")
            
            logger.info(f"技能更新成功: {skill_id}")
            return response.data
            
        except Exception as e:
            logger.error(f"技能更新失败: {e}")
            raise IntegrationError(f"技能更新失败: {e}") from e
    
    def get_skill_info(self, skill_id: str) -> Dict[str, Any]:
        """
        获取技能信息
        
        Args:
            skill_id: 技能ID
            
        Returns:
            技能信息
        """
        endpoint = f"{self.base_url}/api/v1/skills/{skill_id}"
        
        try:
            response = self._request_with_retry("GET", endpoint)
            
            if not response.success:
                raise IntegrationError(f"获取技能信息失败: {response.error}")
            
            return response.data
            
        except Exception as e:
            logger.error(f"获取技能信息失败: {e}")
            raise IntegrationError(f"获取技能信息失败: {e}") from e
    
    def list_skills(self, category: Optional[str] = None, 
                   author: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        列出技能
        
        Args:
            category: 按分类过滤
            author: 按作者过滤
            
        Returns:
            技能列表
        """
        endpoint = f"{self.base_url}/api/v1/skills"
        params = {}
        
        if category:
            params["category"] = category
        if author:
            params["author"] = author
        
        try:
            response = self._request_with_retry("GET", endpoint, params=params)
            
            if not response.success:
                raise IntegrationError(f"列出技能失败: {response.error}")
            
            return response.data.get("skills", [])
            
        except Exception as e:
            logger.error(f"列出技能失败: {e}")
            raise IntegrationError(f"列出技能失败: {e}") from e
    
    def install_skill(self, skill_id: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        安装技能
        
        Args:
            skill_id: 技能ID
            config: 技能配置
            
        Returns:
            安装结果
        """
        endpoint = f"{self.base_url}/api/v1/skills/{skill_id}/install"
        
        try:
            response = self._request_with_retry(
                "POST",
                endpoint,
                json=config or {}
            )
            
            if not response.success:
                raise IntegrationError(f"技能安装失败: {response.error}")
            
            logger.info(f"技能安装成功: {skill_id}")
            return response.data
            
        except Exception as e:
            logger.error(f"技能安装失败: {e}")
            raise IntegrationError(f"技能安装失败: {e}") from e
    
    def uninstall_skill(self, skill_id: str) -> Dict[str, Any]:
        """
        卸载技能
        
        Args:
            skill_id: 技能ID
            
        Returns:
            卸载结果
        """
        endpoint = f"{self.base_url}/api/v1/skills/{skill_id}/uninstall"
        
        try:
            response = self._request_with_retry("POST", endpoint)
            
            if not response.success:
                raise IntegrationError(f"技能卸载失败: {response.error}")
            
            logger.info(f"技能卸载成功: {skill_id}")
            return response.data
            
        except Exception as e:
            logger.error(f"技能卸载失败: {e}")
            raise IntegrationError(f"技能卸载失败: {e}") from e
    
    def execute_skill_operation(self, skill_id: str, operation: str, 
                               params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        执行技能操作
        
        Args:
            skill_id: 技能ID
            operation: 操作名称
            params: 操作参数
            
        Returns:
            操作结果
        """
        endpoint = f"{self.base_url}/api/v1/skills/{skill_id}/execute/{operation}"
        
        try:
            response = self._request_with_retry(
                "POST",
                endpoint,
                json=params or {}
            )
            
            if not response.success:
                raise IntegrationError(f"执行技能操作失败: {response.error}")
            
            logger.debug(f"技能操作执行成功: {skill_id}/{operation}")
            return response.data
            
        except Exception as e:
            logger.error(f"执行技能操作失败: {e}")
            raise IntegrationError(f"执行技能操作失败: {e}") from e
    
    def get_skill_metrics(self, skill_id: str, period: str = "day") -> Dict[str, Any]:
        """
        获取技能指标数据
        
        Args:
            skill_id: 技能ID
            period: 统计周期（hour, day, week, month）
            
        Returns:
            指标数据
        """
        endpoint = f"{self.base_url}/api/v1/skills/{skill_id}/metrics"
        params = {"period": period}
        
        try:
            response = self._request_with_retry("GET", endpoint, params=params)
            
            if not response.success:
                raise IntegrationError(f"获取技能指标失败: {response.error}")
            
            return response.data
            
        except Exception as e:
            logger.error(f"获取技能指标失败: {e}")
            raise IntegrationError(f"获取技能指标失败: {e}") from e
    
    def get_platform_stats(self) -> Dict[str, Any]:
        """获取平台统计信息"""
        endpoint = f"{self.base_url}/api/v1/platform/stats"
        
        try:
            response = self._request_with_retry("GET", endpoint)
            
            if not response.success:
                raise IntegrationError(f"获取平台统计失败: {response.error}")
            
            return response.data
            
        except Exception as e:
            logger.error(f"获取平台统计失败: {e}")
            raise IntegrationError(f"获取平台统计失败: {e}") from e
    
    def search_skills(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        搜索技能
        
        Args:
            query: 搜索关键词
            limit: 结果数量限制
            
        Returns:
            技能列表
        """
        endpoint = f"{self.base_url}/api/v1/skills/search"
        params = {"q": query, "limit": limit}
        
        try:
            response = self._request_with_retry("GET", endpoint, params=params)
            
            if not response.success:
                raise IntegrationError(f"搜索技能失败: {response.error}")
            
            return response.data.get("results", [])
            
        except Exception as e:
            logger.error(f"搜索技能失败: {e}")
            raise IntegrationError(f"搜索技能失败: {e}") from e
    
    def upload_skill_package(self, package_path: str) -> Dict[str, Any]:
        """
        上传技能包
        
        Args:
            package_path: 技能包路径
            
        Returns:
            上传结果
        """
        endpoint = f"{self.base_url}/api/v1/skills/upload"
        
        try:
            with open(package_path, "rb") as f:
                files = {"package": f}
                response = self._request_with_retry("POST", endpoint, files=files)
            
            if not response.success:
                raise IntegrationError(f"技能包上传失败: {response.error}")
            
            logger.info(f"技能包上传成功: {package_path}")
            return response.data
            
        except Exception as e:
            logger.error(f"技能包上传失败: {e}")
            raise IntegrationError(f"技能包上传失败: {e}") from e
    
    def check_health(self) -> bool:
        """检查API健康状态"""
        endpoint = f"{self.base_url}/api/v1/health"
        
        try:
            response = self._request_with_retry("GET", endpoint, timeout=5)
            return response.success and response.data.get("status") == "healthy"
            
        except Exception:
            return False
    
    def _request_with_retry(self, method: str, url: str, 
                           retries: int = DEFAULT_RETRIES, 
                           **kwargs) -> OpenClawAPIResponse:
        """
        带重试的请求
        
        Args:
            method: HTTP方法
            url: 请求URL
            retries: 重试次数
            **kwargs: 请求参数
            
        Returns:
            API响应
            
        Raises:
            AuthenticationError: 认证失败
            RateLimitError: 速率限制
            TimeoutError: 请求超时
            IntegrationError: 其他API错误
        """
        last_exception = None
        
        for attempt in range(retries + 1):
            try:
                # 设置超时
                if "timeout" not in kwargs:
                    kwargs["timeout"] = self.timeout
                
                # 发送请求
                response = self.session.request(method, url, **kwargs)
                
                # 处理响应
                api_response = OpenClawAPIResponse.from_response(response)
                
                # 处理特定错误
                if response.status_code == 401:
                    raise AuthenticationError("API认证失败")
                elif response.status_code == 429:
                    raise RateLimitError("API速率限制")
                elif response.status_code >= 500:
                    logger.warning(f"服务器错误 {response.status_code}, 重试 {attempt + 1}/{retries + 1}")
                    if attempt < retries:
                        continue
                    else:
                        raise IntegrationError(f"服务器错误: {response.status_code}")
                
                return api_response
                
            except AuthenticationError as e:
                logger.error(f"认证失败: {e}")
                raise
            except RateLimitError as e:
                logger.warning(f"速率限制: {e}")
                raise
            except Timeout as e:
                last_exception = e
                logger.warning(f"请求超时，重试 {attempt + 1}/{retries + 1}")
                if attempt < retries:
                    continue
                else:
                    raise TimeoutError(f"请求超时: {e}") from e
            except ConnectionError as e:
                last_exception = e
                logger.warning(f"连接错误，重试 {attempt + 1}/{retries + 1}")
                if attempt < retries:
                    continue
                else:
                    raise IntegrationError(f"连接错误: {e}") from e
            except RequestException as e:
                last_exception = e
                logger.warning(f"请求异常，重试 {attempt + 1}/{retries + 1}: {e}")
                if attempt < retries:
                    continue
                else:
                    raise IntegrationError(f"请求失败: {e}") from e
        
        # 所有重试都失败
        raise IntegrationError(f"请求失败，所有重试都失败: {last_exception}")
    
    def close(self):
        """关闭客户端"""
        self.session.close()
        logger.debug("OpenClaw API客户端已关闭")
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()