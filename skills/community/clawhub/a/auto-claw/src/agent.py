"""
WordPress Agent — Auto-Claw 核心大脑
连接 Vault + Gate Pipeline + WordPress Client
"""
import os
import time
import hashlib
import requests
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass, field
try:
    from .audit import AuditLogger
    from .vault import VaultManager
    from .pipeline import GatePipeline, Operation, RiskLevel
    from .wordpress import WordPressClient
except ImportError:
    from audit import AuditLogger  # noqa: F401
    from vault import VaultManager  # noqa: F401
    from pipeline import GatePipeline, Operation, RiskLevel  # noqa: F401
    from wordpress import WordPressClient  # noqa: F401

@dataclass
class HealthReport:
    site: str
    connected: bool
    version: str = ""
    db_version: str = ""
    php_version: str = ""
    plugins: List[Dict] = field(default_factory=list)
    themes: List[Dict] = field(default_factory=list)
    admin_count: int = 0
    post_count: int = 0
    has_updates: bool = False
    security_score: int = 0  # 0-100
    recommendations: List[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "site": self.site,
            "connected": self.connected,
            "version": self.version,
            "db_version": self.db_version,
            "php_version": self.php_version,
            "plugins": self.plugins,
            "themes": self.themes,
            "admin_count": self.admin_count,
            "post_count": self.post_count,
            "has_updates": self.has_updates,
            "security_score": self.security_score,
            "recommendations": self.recommendations,
        }

class WordPressAgent:
    """
    Auto-Claw WordPress 运营 Agent

    使用方式：
        agent = WordPressAgent(site_id="prod-site-1")
        agent.connect()
        report = agent.health_check()
        result = agent.create_post("标题", "内容")
    """

    def __init__(
        self,
        site_id: str,
        ssh_host: str = None,
        ssh_user: str = None,
        ssh_key: str = None,
        web_root: str = None,
        php_bin: str = None,
        vault_mode: str = None,
        approval_callback: Callable[[Operation], bool] = None,
        webhook_url: str = None,
    ):
        self.site_id = site_id
        self.webhook_url = webhook_url or os.environ.get("APPROVAL_WEBHOOK_URL")
        
        # 初始化组件
        self.audit = AuditLogger()
        self.vault = VaultManager(mode=vault_mode)
        
        # Gate Pipeline with optional webhook approval
        self.pipeline = GatePipeline(self.audit, approval_callback=approval_callback)
        
        # 连接参数（优先级：传入参数 > Vault > 环境变量）
        self.ssh_host = ssh_host or self._vault_get("ssh_host") or os.environ.get("WP_SSH_HOST")
        self.ssh_user = ssh_user or self._vault_get("ssh_user") or os.environ.get("WP_SSH_USER")
        self.ssh_key = ssh_key or self._vault_get("ssh_key") or os.environ.get("WP_SSH_KEY")
        self.web_root = web_root or self._vault_get("web_root") or os.environ.get("WP_WEB_ROOT")
        self.php_bin = php_bin or os.environ.get("WP_PHP_BIN", "/www/server/php/82/bin/php")
        
        self.wp: Optional[WordPressClient] = None
        self._connected = False
        
        self.audit.log("agent", "init", details={"site_id": site_id, "host": self.ssh_host})

    def _vault_get(self, key: str) -> Optional[str]:
        return self.vault.get_secret(f"secret/wordpress/{self.site_id}", key)

    def connect(self) -> bool:
        """连接 WordPress 站点"""
        if not self.ssh_host or not self.web_root:
            self.audit.log("agent", "connect_failed", details={"reason": "missing_config"})
            return False
        
        self.audit.log("agent", "connect", details={"host": self.ssh_host, "user": self.ssh_user})
        
        try:
            self.wp = WordPressClient(
                ssh_host=self.ssh_host,
                ssh_user=self.ssh_user,
                ssh_key=self.ssh_key,
                web_root=self.web_root,
                php_bin=self.php_bin,
            )
            self._connected = self.wp.test_connection()
        except Exception as e:
            self.audit.log("agent", "connect_error", details={"error": str(e)})
            self._connected = False
        
        self.audit.log("agent", "connect_result", details={"connected": self._connected})
        return self._connected

    def health_check(self) -> HealthReport:
        """全面健康检查"""
        report = HealthReport(site=self.site_id, connected=self._connected)
        
        if not self._connected:
            report.recommendations.append("站点未连接，请先调用 connect()")
            return report
        
        self.audit.log("agent", "health_check", details={"site": self.site_id})
        
        try:
            # 核心信息
            core = self.wp.get_core_info()
            report.version = core.get("version", "")
            report.db_version = core.get("db_version", "")
            
            # 插件
            report.plugins = self.wp.get_plugins()
            
            # 主题
            report.themes = self.wp.get_themes()
            
            # 管理员
            report.admin_count = self.wp.get_admin_users()
            
            # 文章数
            posts = self.wp.get_posts(limit=100)
            report.post_count = len(posts)
            
            # 更新检查
            updates = self.wp.check_updates()
            report.has_updates = updates.get("has_plugin_updates", False) or updates.get("has_core_update", False)
            
            # 安全评分
            report.security_score = self._calc_security_score(report)
            
            # 建议
            report.recommendations = self._generate_recommendations(report)
            
        except Exception as e:
            self.audit.log("agent", "health_check_error", details={"error": str(e)})
            report.recommendations.append(f"健康检查出错: {e}")
        
        self.audit.log("agent", "health_check_complete", details={
            "version": report.version,
            "security_score": report.security_score,
            "recommendations": len(report.recommendations)
        })
        
        return report

    def _calc_security_score(self, report: HealthReport) -> int:
        score = 100
        
        # 管理员过多
        if report.admin_count > 3:
            score -= 20
        elif report.admin_count > 2:
            score -= 10
        
        # 有待更新
        if report.has_updates:
            score -= 15
        
        # 无插件
        if len(report.plugins) == 0:
            score -= 10  # 缺少基本防护
        
        return max(0, score)

    def _generate_recommendations(self, report: HealthReport) -> List[str]:
        recs = []
        if report.admin_count > 2:
            recs.append(f"⚠️ 管理员用户 {report.admin_count} 人，建议审查是否必需")
        if report.has_updates:
            recs.append("🔔 有可用更新，建议尽快更新插件/核心")
        if len(report.plugins) == 0:
            recs.append("🔒 建议安装安全插件（如 Wordfence）")
        if report.security_score < 70:
            recs.append(f"🔴 安全评分偏低 ({report.security_score}/100)，建议全面审查")
        if not recs:
            recs.append("✅ 站点状态良好，无紧急问题")
        return recs

    # ===== 内容管理 =====

    def create_post(self, title: str, content: str, status: str = "draft", author: str = "autoclaw") -> dict:
        """创建文章（走 Gate Pipeline）"""
        if not self._connected:
            return {"error": "Not connected. Call connect() first."}
        
        # 1. 创建操作请求
        op = self.pipeline.new_operation(
            "write", "create_post",
            f"site:{self.site_id}",
            {"title": title, "content_length": len(content), "author": author}
        )
        
        # 2. Gate Pipeline 审批
        decision = self.pipeline.request(op)
        
        if decision.decision == "deny":
            self.audit.log("agent", "post_create_denied", details={"op_id": op.id})
            return {"error": "Blocked by Gate Pipeline", "reason": decision.reason, "op_id": op.id}
        
        if decision.decision == "need_approval":
            # 尝试发 webhook 审批请求
            if self.webhook_url:
                self._send_approval_request(op, title, content)
            return {"error": "Waiting for approval", "op_id": op.id, "reason": decision.reason}
        
        # 3. 执行
        self.audit.log("agent", "post_create_execute", details={"op_id": op.id, "title": title})
        result = self.wp.create_post(title, content, status, author)
        
        self.audit.log("agent", "post_create_result", details={
            "op_id": op.id,
            "result": "success" if "error" not in result else "failed",
            "post_id": result.get("ID", "unknown")
        })
        
        return result

    def _send_approval_request(self, op: Operation, title: str, content: str):
        """发送审批请求到 webhook"""
        if not self.webhook_url:
            return
        try:
            import json as json_mod
            payload = {
                "op_id": op.id,
                "action": op.action,
                "type": op.type,
                "title": title,
                "content_preview": content[:200],
                "approve_url": f"{self.webhook_url}/approve?op_id={op.id}",
                "deny_url": f"{self.webhook_url}/deny?op_id={op.id}",
            }
            requests.post(self.webhook_url, json=payload, timeout=10)
        except Exception as e:
            self.audit.log("agent", "webhook_error", details={"error": str(e)})

    def get_posts(self, limit: int = 10) -> List[dict]:
        """获取文章列表（只读，直接执行）"""
        if not self._connected:
            return [{"error": "Not connected"}]
        
        op = self.pipeline.new_operation("read", "get_posts", f"site:{self.site_id}")
        decision = self.pipeline.request(op)
        
        if decision.decision == "deny":
            return [{"error": "Blocked", "reason": decision.reason}]
        
        return self.wp.get_posts(limit)

    def approve_operation(self, op_id: str) -> bool:
        """人工审批操作"""
        self.audit.log("agent", "manual_approve", details={"op_id": op_id})
        # 生产环境：从存储中恢复 pending 状态并批准
        return True

    def get_recent_logs(self, limit: int = 50) -> List[dict]:
        """获取最近审计日志"""
        return self.audit.query(limit=limit)
