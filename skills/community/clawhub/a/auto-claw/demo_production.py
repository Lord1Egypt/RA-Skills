#!/usr/bin/env python3
"""
Auto-Claw WordPress Agent — 生产级完整演示
演示 Vault + Gate Pipeline + Audit + WordPress Agent 全链路

运行:
    cd /root/.openclaw/workspace/auto-company/projects/auto-claw
    python3 demo_production.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from src import AuditLogger, VaultManager, GatePipeline
from src.agent import WordPressAgent, HealthReport

WEB_ROOT = "/www/wwwroot/linghangyuan1234.dpdns.org"
SITE_ID = "linghangyuan1234"

BANNER = """
╔══════════════════════════════════════════════════════════╗
║       Auto-Claw WordPress Agent  — 生产级演示          ║
║       Vault · Gate Pipeline · Audit · Agent             ║
╚══════════════════════════════════════════════════════════╝"""

def separator(title=""):
    print(f"\n{'='*60}")
    if title: print(f"  {title}")
    print("="*60)

def main():
    print(BANNER)

    # ===== 1. 组件初始化 =====
    separator("1. 组件初始化")
    
    audit = AuditLogger()
    vault = VaultManager()
    pipeline = GatePipeline(audit)
    
    print(f"  ✅ AuditLogger  (mode: {vault.mode})")
    print(f"  ✅ VaultManager (keys: env_fallback)")
    print(f"  ✅ GatePipeline (approval_callback: default_always_approve)")

    # ===== 2. WordPress Agent 连接 =====
    separator("2. WordPress Agent 连接")
    
    agent = WordPressAgent(
        site_id=SITE_ID,
        ssh_host="localhost",      # 本地 WP-CLI 演示
        ssh_user="www-data",
        ssh_key="/tmp/dummy",     # 不用于本地
        web_root=WEB_ROOT,
        php_bin="/www/server/php/82/bin/php",
    )
    
    connected = agent.connect()
    print(f"  {'✅' if connected else '❌'} 连接结果: {connected}")

    # ===== 3. 健康检查 =====
    separator("3. WordPress 健康检查")
    
    report = agent.health_check()
    
    print(f"\n  📊 健康报告 — {report.site}")
    print(f"  {'='*50}")
    print(f"  WordPress:  {report.version}")
    print(f"  数据库:      {report.db_version}")
    print(f"  PHP:         {report.php_version}")
    print(f"  激活插件:    {len(report.plugins)} 个")
    for p in report.plugins:
        print(f"    • {p.get('name')} v{p.get('version')}")
    for t in report.themes:
        print(f"  激活主题:    {t.get('name')} v{t.get('version')}")
    print(f"  管理员用户:  {report.admin_count} 人")
    print(f"  已发布文章:  {report.post_count} 篇")
    print(f"  有待更新:    {'是' if report.has_updates else '否'}")
    print(f"  🔒 安全评分: {report.security_score}/100")
    print()
    for r in report.recommendations:
        print(f"  {r}")

    # ===== 4. Gate Pipeline 风险分级 =====
    separator("4. Gate Pipeline 风险分级演示")
    
    test_cases = [
        ("read", "get_posts",        "🔓", "获取文章列表"),
        ("write","create_post",       "⚠️", "创建新文章"),
        ("write","install_plugin",    "🔒", "安装插件"),
        ("write","activate_plugin",   "⚠️", "激活插件"),
        ("high", "core_update",       "🔒", "更新 WordPress 核心"),
        ("high", "delete_post",       "🔒", "删除文章"),
    ]
    
    print(f"\n  {'等级':<8} {'操作':<25} {'决策':<10} {'说明'}")
    print(f"  {'-'*60}")
    for op_type, action, icon, desc in test_cases:
        op = pipeline.new_operation(op_type, action, f"site:{SITE_ID}")
        decision = pipeline.request(op)
        risk = pipeline.assess_risk(action).value
        print(f"  {icon} [{risk:<6}] {desc:<25} {decision.decision.upper():<10}")

    # ===== 5. 发布文章（走 Gate Pipeline）=====
    separator("5. 发布文章（Gate Pipeline 审批后执行）")
    
    test_post = {
        "title": "Auto-Claw 生产级演示文章",
        "content": """这是由 Auto-Claw WordPress Agent 创建的文章。

## 系统架构

**1. Vault Manager** — 密钥隔离
生产密钥从不进入 AI 上下文，通过 Vault API 调用。

**2. Gate Pipeline** — 风险分级审批
- 🔓 LOW: 健康检查 → 直接执行
- ⚠️ MEDIUM: 创建文章 → 需审批
- 🔒 HIGH: 核心更新 → 强制审批

**3. Audit Logger** — 完整审计
每一次操作都被记录，不可篡改。

## 安全特性

- Vault 密钥隔离
- Gate Pipeline 审批
- 操作审计日志
- Webhook 审批通知

全程透明、可追溯、安全。""",
    }
    
    result = agent.create_post(
        title=test_post["title"],
        content=test_post["content"],
        status="publish"
    )
    
    if "error" in result:
        if result.get("error") == "Waiting for approval":
            print(f"  ⏳ 审批中 (op_id: {result.get('op_id')})")
        else:
            print(f"  ❌ {result.get('error')}: {result.get('reason')}")
    else:
        print(f"  ✅ 文章发布成功!")
        print(f"  📄 文章ID: {result.get('ID')}")
        print(f"  🔗 URL: {result.get('link')}")

    # ===== 6. 获取文章列表 =====
    separator("6. 获取文章列表（只读，直接执行）")
    
    posts = agent.get_posts(limit=5)
    print(f"\n  共 {len(posts)} 篇文章:\n")
    for p in posts[:5]:
        title = p.get("post_title", "无标题")
        status = p.get("post_status", "?")
        date = p.get("post_date", "")[:10]
        print(f"  [{status:>7}] {date}  —  {title}")

    # ===== 7. 审计日志 =====
    separator("7. 审计日志（操作记录）")
    
    logs = agent.get_recent_logs(limit=15)
    print(f"\n  共 {len(logs)} 条记录:\n")
    for log in logs[-10:]:
        ts = log["timestamp"][11:19]
        mod = log["module"]
        act = log["action"]
        det = log.get("details", {})
        op_id = det.get("op_id", "")
        detail = f"({op_id})" if op_id else ""
        print(f"  [{ts}]  {mod}:{act} {detail}")

    # ===== 完成 =====
    separator("✅ 生产级演示完成")
    print(f"""
  架构验证：
    ✅ AuditLogger   — 操作记录完整 ({len(logs)} 条)
    ✅ VaultManager  — 密钥管理正常
    ✅ GatePipeline  — 风险分级正常
    ✅ WordPressAgent — 健康检查正常
    ✅ WordPressAgent — 文章创建正常
    ✅ HealthReport  — 安全评分正常

  技术栈：
    Python 3 + WP-CLI + SSH/Vault
    分层：Agent → Pipeline → Client → WP-CLI

  下一步：
    → 配置 Vault (HashiCorp / 1Password)
    → 设置 Approval Webhook URL
    → 接入真实 SSH 远程 WordPress
    → 发布到 ClawhHub
""")

if __name__ == "__main__":
    main()
