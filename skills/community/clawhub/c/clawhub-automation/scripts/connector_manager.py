"""
Connector Manager - 生态连接器管理器
管理微信、钉钉、飞书、WPS等平台的接口对接
"""

import json
import time
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum


class PlatformType(Enum):
    """平台类型"""
    WECHAT = "wechat"           # 微信
    DINGTALK = "dingtalk"       # 钉钉
    FEISHU = "feishu"           # 飞书
    WPS = "wps"                 # WPS
    TENCENT_DOC = "tencent_doc" # 腾讯文档
    ALIYUN_DRIVE = "aliyun_drive" # 阿里云盘


class AuthStatus(Enum):
    """授权状态"""
    UNAUTHORIZED = "unauthorized"  # 未授权
    AUTHORIZING = "authorizing"    # 授权中
    AUTHORIZED = "authorized"      # 已授权
    EXPIRED = "expired"            # 已过期


@dataclass
class PlatformAuth:
    """平台授权信息"""
    platform: str
    status: AuthStatus
    access_token: str = ""
    refresh_token: str = ""
    expires_at: float = 0.0
    scope: List[str] = field(default_factory=list)
    auth_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PlatformConnector:
    """平台连接器"""
    platform: str
    name: str
    description: str
    supported_actions: List[str]
    auth_required: bool = True
    auth_url: str = ""
    api_base: str = ""
    status: str = "active"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'platform': self.platform,
            'name': self.name,
            'description': self.description,
            'supported_actions': self.supported_actions,
            'auth_required': self.auth_required,
            'auth_url': self.auth_url,
            'status': self.status
        }


class ConnectorManager:
    """
    生态连接器管理器
    
    Features:
    - 多平台连接器管理
    - 授权状态管理
    - 统一接口调用
    """
    
    def __init__(self):
        """初始化连接器管理器"""
        self.connectors: Dict[str, PlatformConnector] = {}
        self.auths: Dict[str, PlatformAuth] = {}
        self.action_handlers: Dict[str, Callable] = {}
        
        # 注册默认连接器
        self._register_default_connectors()
    
    def _register_default_connectors(self):
        """注册默认平台连接器"""
        # 微信连接器
        self.register_connector(PlatformConnector(
            platform=PlatformType.WECHAT.value,
            name="微信",
            description="微信个人/企业号接口",
            supported_actions=[
                'send_message',
                'receive_message',
                'send_file',
                'receive_file',
                'get_contacts'
            ],
            auth_required=True,
            auth_url="https://open.weixin.qq.com/connect/oauth2/authorize",
            api_base="https://api.weixin.qq.com"
        ))
        
        # 钉钉连接器
        self.register_connector(PlatformConnector(
            platform=PlatformType.DINGTALK.value,
            name="钉钉",
            description="钉钉企业接口",
            supported_actions=[
                'send_message',
                'send_work_notice',
                'create_approval',
                'get_user_info',
                'create_calendar_event'
            ],
            auth_required=True,
            auth_url="https://oapi.dingtalk.com/connect/oauth2/sns_authorize",
            api_base="https://oapi.dingtalk.com"
        ))
        
        # 飞书连接器
        self.register_connector(PlatformConnector(
            platform=PlatformType.FEISHU.value,
            name="飞书",
            description="飞书企业接口",
            supported_actions=[
                'send_message',
                'create_document',
                'create_spreadsheet',
                'create_task',
                'send_notification'
            ],
            auth_required=True,
            auth_url="https://open.feishu.cn/open-apis/authen/v1/index",
            api_base="https://open.feishu.cn"
        ))
        
        # WPS连接器
        self.register_connector(PlatformConnector(
            platform=PlatformType.WPS.value,
            name="WPS",
            description="WPS办公接口",
            supported_actions=[
                'create_document',
                'edit_document',
                'create_spreadsheet',
                'create_presentation'
            ],
            auth_required=True,
            auth_url="https://open.wps.cn/oauth2/authorize",
            api_base="https://open.wps.cn"
        ))
        
        # 腾讯文档连接器
        self.register_connector(PlatformConnector(
            platform=PlatformType.TENCENT_DOC.value,
            name="腾讯文档",
            description="腾讯文档接口",
            supported_actions=[
                'create_document',
                'create_spreadsheet',
                'create_collection',
                'import_file'
            ],
            auth_required=True,
            auth_url="https://docs.qq.com/oauth2/authorize",
            api_base="https://docs.qq.com/api"
        ))
        
        # 阿里云盘连接器
        self.register_connector(PlatformConnector(
            platform=PlatformType.ALIYUN_DRIVE.value,
            name="阿里云盘",
            description="阿里云盘存储接口",
            supported_actions=[
                'upload_file',
                'download_file',
                'list_files',
                'create_folder',
                'share_file'
            ],
            auth_required=True,
            auth_url="https://auth.aliyundrive.com/oauth2/authorize",
            api_base="https://openapi.aliyundrive.com"
        ))
    
    def register_connector(self, connector: PlatformConnector):
        """
        注册平台连接器
        
        Args:
            connector: 平台连接器实例
        """
        self.connectors[connector.platform] = connector
    
    def get_connector(self, platform: str) -> Optional[PlatformConnector]:
        """
        获取平台连接器
        
        Args:
            platform: 平台标识
            
        Returns:
            PlatformConnector or None
        """
        return self.connectors.get(platform)
    
    def list_connectors(self) -> List[PlatformConnector]:
        """列出所有连接器"""
        return list(self.connectors.values())
    
    def get_auth_url(self, platform: str, redirect_uri: str = "") -> str:
        """
        获取平台授权URL
        
        Args:
            platform: 平台标识
            redirect_uri: 回调地址
            
        Returns:
            str: 授权URL
        """
        connector = self.get_connector(platform)
        if not connector:
            return ""
        
        # 构建授权URL（简化版）
        auth_url = connector.auth_url
        if redirect_uri:
            auth_url += f"?redirect_uri={redirect_uri}"
        
        return auth_url
    
    def authorize(self, platform: str, auth_code: str) -> PlatformAuth:
        """
        完成平台授权
        
        Args:
            platform: 平台标识
            auth_code: 授权码
            
        Returns:
            PlatformAuth: 授权信息
        """
        # 模拟授权流程
        auth = PlatformAuth(
            platform=platform,
            status=AuthStatus.AUTHORIZED,
            access_token=f"token_{platform}_{int(time.time())}",
            refresh_token=f"refresh_{platform}_{int(time.time())}",
            expires_at=time.time() + 7200,  # 2小时过期
            scope=['read', 'write']
        )
        
        self.auths[platform] = auth
        return auth
    
    def get_auth_status(self, platform: str) -> AuthStatus:
        """
        获取平台授权状态
        
        Args:
            platform: 平台标识
            
        Returns:
            AuthStatus: 授权状态
        """
        if platform not in self.auths:
            return AuthStatus.UNAUTHORIZED
        
        auth = self.auths[platform]
        
        # 检查是否过期
        if auth.expires_at < time.time():
            auth.status = AuthStatus.EXPIRED
        
        return auth.status
    
    def revoke_auth(self, platform: str) -> bool:
        """
        撤销平台授权
        
        Args:
            platform: 平台标识
            
        Returns:
            bool: 是否成功
        """
        if platform in self.auths:
            del self.auths[platform]
            return True
        return False
    
    def execute_action(
        self,
        platform: str,
        action: str,
        params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        执行平台操作
        
        Args:
            platform: 平台标识
            action: 操作类型
            params: 操作参数
            
        Returns:
            Dict: 执行结果
        """
        connector = self.get_connector(platform)
        if not connector:
            return {'success': False, 'error': f'平台 {platform} 未注册'}
        
        if action not in connector.supported_actions:
            return {'success': False, 'error': f'操作 {action} 不被支持'}
        
        # 检查授权状态
        if connector.auth_required:
            auth_status = self.get_auth_status(platform)
            if auth_status != AuthStatus.AUTHORIZED:
                return {
                    'success': False,
                    'error': f'平台 {platform} 未授权或授权已过期',
                    'auth_status': auth_status.value
                }
        
        # 执行操作（模拟）
        return {
            'success': True,
            'platform': platform,
            'action': action,
            'params': params or {},
            'result': f"{platform}.{action}_executed"
        }
    
    def refresh_token(self, platform: str) -> bool:
        """
        刷新平台访问令牌
        
        Args:
            platform: 平台标识
            
        Returns:
            bool: 是否成功
        """
        if platform not in self.auths:
            return False
        
        auth = self.auths[platform]
        
        # 模拟刷新
        auth.access_token = f"token_{platform}_{int(time.time())}"
        auth.expires_at = time.time() + 7200
        auth.status = AuthStatus.AUTHORIZED
        
        return True
    
    def get_supported_platforms(self) -> List[str]:
        """获取支持的平台列表"""
        return list(self.connectors.keys())
    
    def is_action_supported(self, platform: str, action: str) -> bool:
        """
        检查操作是否被支持
        
        Args:
            platform: 平台标识
            action: 操作类型
            
        Returns:
            bool: 是否支持
        """
        connector = self.get_connector(platform)
        if not connector:
            return False
        return action in connector.supported_actions