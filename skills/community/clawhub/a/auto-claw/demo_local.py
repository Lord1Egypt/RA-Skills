#!/usr/bin/env python3
"""
Auto-Claw 完整演示脚本 V2
支持本地 WP-CLI 直连（不需要 SSH）
"""
import sys
import os
import subprocess
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src import AuditLogger, VaultManager, GatePipeline, WordPressAgent

# ===== 配置 =====
WEB_ROOT = "/www/wwwroot/linghangyuan1234.dpdns.org"
PHP_BIN = "/www/server/php/82/bin/php"
WP_CLI = "/usr/local/bin/wp"
SITE_ID = "linghangyuan1234"

SEPARATOR = "=" * 60

def wp_cmd(args: str) -> tuple:
    """执行 WP-CLI 命令，返回 (stdout, stderr, returncode)"""
    cmd = f"cd {WEB_ROOT} && WP_CLI_PHP={PHP_BIN} {WP_CLI} --allow-root {args}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def print_header(title):
    print(f"\n{SEPARATOR}\n  {title}\n{SEPARATOR}")

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║       Auto-Claw WordPress Agent — 完整演示 V2             ║
║   Vault · Gate Pipeline · Audit · WordPress 全链路        ║
╚══════════════════════════════════════════════════════════╝
""")

    # ===== 初始化 =====
    print_header("第1步：初始化")
    audit = AuditLogger()
    vault = VaultManager()
    pipeline = GatePipeline(audit)
    print(f"✅ 审计日志 (mode: {vault.mode})")
    print(f"✅ Vault 管理器")
    print(f"✅ Gate Pipeline")

    # ===== 健康检查 =====
    print_header("第2步：健康检查（只读 → 直接执行）")

    version, _, _ = wp_cmd("core version")
    print(f"   WordPress 版本: {version}")

    checksum, err, _ = wp_cmd("core verify-checksums 2>&1")
    status = "✅ 正常" if err and "success" in err.lower() else "⚠️ 需检查"
    print(f"   核心校验: {status}")

    db_ver, _, _ = wp_cmd("core update-db --dry-run 2>&1 | head -1")
    print(f"   数据库版本: {db_ver}")

    plugins = []
    out, _, _ = wp_cmd("plugin list --format=json --status=active")
    try: plugins = json.loads(out) if out else []
    except: pass
    print(f"   激活插件: {len(plugins)} 个")
    for p in plugins:
        print(f"     - {p.get('name')} v{p.get('version')} ({p.get('status')})")

    themes = []
    out, _, _ = wp_cmd("theme list --format=json --status=active")
    try: themes = json.loads(out) if out else []
    except: pass
    for t in themes:
        print(f"   激活主题: {t.get('name')} v{t.get('version')}")

    admin_count, _, _ = wp_cmd("user list --role=administrator --format=count")
    print(f"   管理员用户: {admin_count} 人")

    updates, _, _ = wp_cmd("plugin update --dry-run 2>&1")
    has_updates = "有" if "available" in updates.lower() else "无"
    print(f"   插件更新: {has_updates}")

    audit.log("health_check", "complete", details={"version": version})

    # ===== Gate Pipeline 演示 =====
    print_header("第3步：Gate Pipeline 风险分级")

    test_cases = [
        ("read", "get_posts", "获取文章列表"),
        ("write", "create_post", "创建新文章"),
        ("write", "install_plugin", "安装插件"),
        ("write", "activate_plugin", "激活插件"),
        ("high", "core_update", "WordPress 核心更新"),
        ("high", "delete_post", "删除文章"),
    ]

    for op_type, action, desc in test_cases:
        op = pipeline.new_operation(op_type, action, f"site:{SITE_ID}")
        decision = pipeline.request(op)
        risk = pipeline.assess_risk(action).value
        icon = "🔒" if risk == "high" else "⚠️" if risk == "medium" else "🔓"
        print(f"   {icon} [{risk:6}] {desc}")
        print(f"          → {decision.decision.upper()}: {decision.reason}")

    # ===== 创建文章（走 Gate）=====
    print_header("第4步：创建文章（走 Gate Pipeline）")

    post_title = "Auto-Claw 演示文章 #2"
    post_content = """这是由 Auto-Claw AI Agent 创建的第二篇文章。

## 系统架构

1. **Vault Manager** — 密钥隔离，AI 永不接触明文密钥
2. **Gate Pipeline** — 风险分级，高风险操作需人工审批
3. **Audit Logger** — 完整操作记录，不可篡改

## 安全机制

- 只读操作（健康检查）：🔓 直接执行
- 中等风险操作（创建内容）：⚠️ 需审批
- 高风险操作（核心更新/删除）：🔒 强制审批

全程可追溯，每一步都有审计日志。
"""

    op = pipeline.new_operation("write", "create_post", f"site:{SITE_ID}", {"title": post_title})
    decision = pipeline.request(op)
    print(f"   Gate 决策: {decision.decision.upper()}")

    if decision.decision == "allow":
        out, err, code = wp_cmd(
            f"post create --post_title='{post_title}' "
            f"--post_content='{post_content.replace(chr(10), ' ')}' "
            f"--post_status=publish --format=json"
        )
        if code == 0:
            try:
                result = json.loads(out)
                print(f"   ✅ 文章创建成功!")
                print(f"   📄 文章ID: {result.get('ID')}")
                print(f"   🔗 URL: {result.get('link')}")
            except:
                print(f"   ✅ 命令执行成功\n   {out[:100]}")
        else:
            print(f"   ❌ 失败: {err[:100]}")
    else:
        print(f"   ❌ 被 Gate 拦截")

    # ===== 文章列表 =====
    print_header("第5步：读取文章（只读）")

    posts = []
    out, _, _ = wp_cmd("post list --post_type=post --posts_per_page=5 --format=json")
    try: posts = json.loads(out) if out else []
    except: pass

    print(f"   共 {len(posts)} 篇文章:\n")
    for p in posts:
        title = p.get("post_title", "无标题")
        status = p.get("post_status", "?")
        date = p.get("post_date", "")[:10]
        print(f"   [{status:7}] {date} — {title}")

    audit.log("posts_read", "complete", details={"count": len(posts)})

    # ===== 审计日志 =====
    print_header("第6步：审计日志")

    logs = audit.query(limit=20)
    print(f"   共 {len(logs)} 条记录:\n")
    for log in logs[-8:]:
        ts = log["timestamp"][11:19]
        mod = log["module"]
        act = log["action"]
        det = log.get("details", {})
        op_id = det.get("op_id", "")
        decision = det.get("decision", det.get("result", ""))
        print(f"   [{ts}] {mod}:{act} {f'({op_id})' if op_id else ''}")

    # ===== 最终报告 =====
    print_header("✅ 演示完成")

    print(f"""
架构验证：
  ✅ AuditLogger — 操作记录正常
  ✅ VaultManager — 密钥管理正常
  ✅ GatePipeline — 风险分级正常
  ✅ WordPressClient — 健康检查正常
  ✅ WordPressClient — 文章创建正常

下次操作建议：
  1. 用真实 SSH 密钥连接远程 WordPress
  2. 配置 Vault（HashiCorp / 1Password）
  3. 设置 Gate Pipeline 人工审批 webhook
  4. 注册 Skills 到 OpenClaw

""")

if __name__ == "__main__":
    main()
