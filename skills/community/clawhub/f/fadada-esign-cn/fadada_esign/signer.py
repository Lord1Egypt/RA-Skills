#!/usr/bin/env python3
"""
签署人信息模型
"""

from typing import Optional, Dict, Any


class Signer:
    """
    签署人信息
    
    支持个人签署和企业签署
    """
    
    def __init__(
        self,
        name: str,
        mobile: str,
        actor_id: str = "signer1",
        actor_type: str = "person",
        permissions: list = None,
        notification: Dict[str, Any] = None,
        id_number: Optional[str] = None,
        email: Optional[str] = None
    ):
        """
        初始化签署人
        
        Args:
            name: 签署人姓名/企业名称
            mobile: 手机号（用于接收签署通知）
            actor_id: 签署人标识（默认 signer1）
            actor_type: 签署人类型（person/corp）
            permissions: 权限列表（默认 ["sign"]）
            notification: 通知配置（默认短信通知）
            id_number: 身份证号（可选）
            email: 邮箱（可选）
        """
        self.name = name
        self.mobile = mobile
        self.actor_id = actor_id
        self.actor_type = actor_type
        self.permissions = permissions or ["sign"]
        self.id_number = id_number
        self.email = email
        
        # 默认通知配置
        self.notification = notification or {
            "sendNotification": True,
            "notifyWay": "mobile",
            "notifyAddress": mobile
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为API请求格式"""
        actor = {
            "actorId": self.actor_id,
            "actorType": self.actor_type,
            "actorName": self.name,
            "permissions": self.permissions,
            "notification": self.notification
        }
        
        if self.id_number:
            actor["idNumber"] = self.id_number
        if self.email:
            actor["email"] = self.email
            
        return {"actor": actor}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Signer":
        """从字典创建Signer对象"""
        actor = data.get("actor", data)
        return cls(
            name=actor.get("actorName") or actor.get("name"),
            mobile=actor.get("notification", {}).get("notifyAddress") or actor.get("mobile"),
            actor_id=actor.get("actorId", "signer1"),
            actor_type=actor.get("actorType", "person"),
            permissions=actor.get("permissions", ["sign"]),
            notification=actor.get("notification"),
            id_number=actor.get("idNumber"),
            email=actor.get("email")
        )


class CorpSigner(Signer):
    """企业签署人"""
    
    def __init__(
        self,
        corp_name: str,
        mobile: str,
        open_corp_id: Optional[str] = None,
        actor_id: str = "signer1",
        **kwargs
    ):
        """
        初始化企业签署人
        
        Args:
            corp_name: 企业名称
            mobile: 经办人手机号
            open_corp_id: 企业OpenID（可选，如已绑定）
            actor_id: 签署人标识
        """
        super().__init__(
            name=corp_name,
            mobile=mobile,
            actor_id=actor_id,
            actor_type="corp",
            **kwargs
        )
        self.open_corp_id = open_corp_id
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为API请求格式"""
        data = super().to_dict()
        if self.open_corp_id:
            data["actor"]["openId"] = self.open_corp_id
        return data
