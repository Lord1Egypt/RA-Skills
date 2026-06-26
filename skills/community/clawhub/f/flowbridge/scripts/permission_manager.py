"""
Permission Manager - 权限管理器
企业级权限管控与合规审计
"""

import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class UserRole(Enum):
    """用户角色"""
    ADMIN = "admin"          # 管理员
    MEMBER = "member"        # 普通成员
    GUEST = "guest"          # 访客


class ApprovalStatus(Enum):
    """审批状态"""
    PENDING = "pending"      # 待审批
    APPROVED = "approved"    # 已批准
    REJECTED = "rejected"    # 已拒绝


@dataclass
class User:
    """用户"""
    id: str
    name: str
    role: UserRole
    team_id: str = ""
    permissions: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)


@dataclass
class WorkflowApproval:
    """流程审批"""
    id: str
    workflow_id: str
    workflow_name: str
    applicant: str
    status: ApprovalStatus
    reason: str = ""
    approver: str = ""
    comment: str = ""
    created_at: float = field(default_factory=time.time)
    processed_at: Optional[float] = None


@dataclass
class AuditRecord:
    """审计记录"""
    id: str
    user_id: str
    action: str
    resource_type: str
    resource_id: str
    details: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    ip_address: str = ""
    user_agent: str = ""


class PermissionManager:
    """
    权限管理器
    
    Features:
    - 用户角色管理
    - 权限分级控制
    - 流程审批管理
    - 审计日志记录
    """
    
    def __init__(self):
        """初始化权限管理器"""
        self.users: Dict[str, User] = {}
        self.approvals: Dict[str, WorkflowApproval] = {}
        self.audit_logs: List[AuditRecord] = []
        
        # 权限定义
        self.permissions = {
            'workflow:create': '创建工作流',
            'workflow:edit': '编辑工作流',
            'workflow:delete': '删除工作流',
            'workflow:approve': '审批工作流',
            'workflow:execute': '执行工作流',
            'team:manage': '管理团队',
            'audit:view': '查看审计日志'
        }
        
        # 角色权限映射
        self.role_permissions = {
            UserRole.ADMIN: list(self.permissions.keys()),
            UserRole.MEMBER: [
                'workflow:create',
                'workflow:edit',
                'workflow:execute'
            ],
            UserRole.GUEST: [
                'workflow:execute'
            ]
        }
    
    def create_user(
        self,
        user_id: str,
        name: str,
        role: UserRole = UserRole.MEMBER,
        team_id: str = ""
    ) -> User:
        """
        创建用户
        
        Args:
            user_id: 用户ID
            name: 用户名称
            role: 角色
            team_id: 团队ID
            
        Returns:
            User: 用户对象
        """
        permissions = self.role_permissions.get(role, [])
        
        user = User(
            id=user_id,
            name=name,
            role=role,
            team_id=team_id,
            permissions=permissions
        )
        
        self.users[user_id] = user
        
        # 记录审计日志
        self._log_audit(
            user_id=user_id,
            action='user:create',
            resource_type='user',
            resource_id=user_id,
            details={'name': name, 'role': role.value}
        )
        
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """获取用户"""
        return self.users.get(user_id)
    
    def check_permission(self, user_id: str, permission: str) -> bool:
        """
        检查用户权限
        
        Args:
            user_id: 用户ID
            permission: 权限标识
            
        Returns:
            bool: 是否有权限
        """
        user = self.get_user(user_id)
        if not user:
            return False
        
        # 管理员拥有所有权限
        if user.role == UserRole.ADMIN:
            return True
        
        return permission in user.permissions
    
    def assign_role(self, user_id: str, role: UserRole) -> bool:
        """
        分配角色
        
        Args:
            user_id: 用户ID
            role: 新角色
            
        Returns:
            bool: 是否成功
        """
        user = self.get_user(user_id)
        if not user:
            return False
        
        old_role = user.role
        user.role = role
        user.permissions = self.role_permissions.get(role, [])
        
        # 记录审计日志
        self._log_audit(
            user_id=user_id,
            action='user:assign_role',
            resource_type='user',
            resource_id=user_id,
            details={'old_role': old_role.value, 'new_role': role.value}
        )
        
        return True
    
    def submit_approval(
        self,
        workflow_id: str,
        workflow_name: str,
        applicant: str,
        reason: str = ""
    ) -> WorkflowApproval:
        """
        提交审批申请
        
        Args:
            workflow_id: 工作流ID
            workflow_name: 工作流名称
            applicant: 申请人
            reason: 申请理由
            
        Returns:
            WorkflowApproval: 审批记录
        """
        approval_id = f"approval_{len(self.approvals)}"
        
        approval = WorkflowApproval(
            id=approval_id,
            workflow_id=workflow_id,
            workflow_name=workflow_name,
            applicant=applicant,
            status=ApprovalStatus.PENDING,
            reason=reason
        )
        
        self.approvals[approval_id] = approval
        
        # 记录审计日志
        self._log_audit(
            user_id=applicant,
            action='approval:submit',
            resource_type='workflow',
            resource_id=workflow_id,
            details={'approval_id': approval_id, 'reason': reason}
        )
        
        return approval
    
    def process_approval(
        self,
        approval_id: str,
        approver: str,
        approved: bool,
        comment: str = ""
    ) -> bool:
        """
        处理审批申请
        
        Args:
            approval_id: 审批ID
            approver: 审批人
            approved: 是否批准
            comment: 审批意见
            
        Returns:
            bool: 是否成功
        """
        approval = self.approvals.get(approval_id)
        if not approval:
            return False
        
        # 检查审批人权限
        if not self.check_permission(approver, 'workflow:approve'):
            return False
        
        approval.status = ApprovalStatus.APPROVED if approved else ApprovalStatus.REJECTED
        approval.approver = approver
        approval.comment = comment
        approval.processed_at = time.time()
        
        # 记录审计日志
        self._log_audit(
            user_id=approver,
            action='approval:process',
            resource_type='workflow',
            resource_id=approval.workflow_id,
            details={
                'approval_id': approval_id,
                'decision': 'approved' if approved else 'rejected',
                'comment': comment
            }
        )
        
        return True
    
    def get_pending_approvals(self, approver: str = None) -> List[WorkflowApproval]:
        """
        获取待审批列表
        
        Args:
            approver: 审批人（用于权限检查）
            
        Returns:
            List[WorkflowApproval]: 待审批列表
        """
        if approver and not self.check_permission(approver, 'workflow:approve'):
            return []
        
        return [
            a for a in self.approvals.values()
            if a.status == ApprovalStatus.PENDING
        ]
    
    def _log_audit(
        self,
        user_id: str,
        action: str,
        resource_type: str,
        resource_id: str,
        details: Dict[str, Any] = None
    ):
        """记录审计日志"""
        record = AuditRecord(
            id=f"audit_{len(self.audit_logs)}",
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {}
        )
        
        self.audit_logs.append(record)
    
    def get_audit_logs(
        self,
        user_id: str = None,
        action: str = None,
        resource_type: str = None,
        start_time: float = None,
        end_time: float = None
    ) -> List[AuditRecord]:
        """
        查询审计日志
        
        Args:
            user_id: 用户ID筛选
            action: 操作类型筛选
            resource_type: 资源类型筛选
            start_time: 开始时间
            end_time: 结束时间
            
        Returns:
            List[AuditRecord]: 审计日志列表
        """
        logs = self.audit_logs
        
        if user_id:
            logs = [log for log in logs if log.user_id == user_id]
        
        if action:
            logs = [log for log in logs if log.action == action]
        
        if resource_type:
            logs = [log for log in logs if log.resource_type == resource_type]
        
        if start_time:
            logs = [log for log in logs if log.timestamp >= start_time]
        
        if end_time:
            logs = [log for log in logs if log.timestamp <= end_time]
        
        return logs
    
    def export_audit_logs(self, filepath: str = None) -> str:
        """
        导出审计日志
        
        Args:
            filepath: 导出路径
            
        Returns:
            str: 导出文件路径
        """
        if not filepath:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = f"audit_logs_{timestamp}.json"
        
        data = [
            {
                'id': log.id,
                'user_id': log.user_id,
                'action': log.action,
                'resource_type': log.resource_type,
                'resource_id': log.resource_id,
                'details': log.details,
                'timestamp': log.timestamp
            }
            for log in self.audit_logs
        ]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def is_sensitive_action(self, action: str, params: Dict) -> bool:
        """
        检查是否为敏感操作
        
        Args:
            action: 操作类型
            params: 操作参数
            
        Returns:
            bool: 是否敏感
        """
        sensitive_actions = [
            'workflow:delete',
            'user:delete',
            'team:delete',
            'data:export'
        ]
        
        # 检查操作类型
        if action in sensitive_actions:
            return True
        
        # 检查是否涉及敏感数据
        sensitive_keywords = ['password', 'token', 'secret', 'key', 'private']
        for keyword in sensitive_keywords:
            if keyword in json.dumps(params).lower():
                return True
        
        return False
    
    def require_additional_auth(self, user_id: str, action: str) -> bool:
        """
        检查是否需要额外授权
        
        Args:
            user_id: 用户ID
            action: 操作类型
            
        Returns:
            bool: 是否需要额外授权
        """
        user = self.get_user(user_id)
        if not user:
            return True
        
        # 敏感操作需要额外授权
        if action in ['team:delete', 'user:delete']:
            return True
        
        # 管理员不需要额外授权
        if user.role == UserRole.ADMIN:
            return False
        
        return False