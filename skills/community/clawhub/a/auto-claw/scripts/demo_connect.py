# -*- coding: utf-8 -*-
"""
Auto-Claw Demo脚本

演示功能：
1. 初始化配置和日志
2. 模拟Vault获取WordPress凭据
3. 创建Gate Pipeline
4. 连接测试WordPress站点
5. 执行一个简单的读操作

运行方式：
    cd /path/to/auto-claw
    poetry run python scripts/demo_connect.py

依赖：
    - config/ 目录下的配置
    - lib/ 目录下的各模块
"""
import sys
import os

# 将项目根目录加入Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings
from lib.audit.logger import AuditLogger
from lib.vault.manager import VaultManager
from lib.pipeline.gate import GatePipeline, Operation, OperationType
from lib.wordpress.client import WordPressClient


def main():
    """主函数"""
    print("=" * 60)
    print("Auto-Claw Demo - WordPress连接测试")
    print("=" * 60)
    
    # 1. 初始化审计日志
    print("\n[1] 初始化审计日志...")
    audit = AuditLogger(settings)
    audit.log("demo", "start", {"message": "Demo script started"})
    print("✓ 审计日志已启用")
    
    # 2. 初始化Vault管理器
    print("\n[2] 初始化Vault管理器...")
    vault = VaultManager(settings, audit)
    print(f"✓ Vault模式: {'启用' if settings.vault.enabled else '禁用 (使用环境变量)'}")
    
    # 3. 演示从Vault获取密钥
    print("\n[3] 演示密钥获取...")
    # 尝试从环境变量获取（演示用）
    demo_password = vault.get("password", "demo")
    if demo_password:
        print(f"✓ 从Vault获取到密码")
    else:
        # 回退到环境变量
        demo_password = os.getenv("WP_DEMO_PASSWORD", "demo_password_not_set")
        print(f"✓ 从环境变量获取 (fallback): {demo_password[:4]}***")
    
    # 4. 初始化Gate Pipeline
    print("\n[4] 初始化Gate Pipeline...")
    pipeline = GatePipeline(settings, audit)
    print(f"✓ Pipeline已创建")
    print(f"  - 需要审批: {settings.pipeline.require_approval}")
    print(f"  - 自动重试: {settings.pipeline.auto_retry}")
    
    # 5. 创建WordPress客户端
    print("\n[5] 创建WordPress客户端...")
    
    # 从配置获取站点信息
    if settings.sites:
        site = settings.sites[0]
        print(f"  站点名称: {site.name}")
        print(f"  站点URL: {site.url}")
        
        # 使用环境变量中的凭据（演示用）
        username = os.getenv("WP_DEMO_USERNAME", "demo_user")
        password = os.getenv("WP_DEMO_PASSWORD", "demo_password")
        
        wp_client = WordPressClient(site.url, username, password, audit)
    else:
        # 创建一个模拟客户端（无真实站点时）
        print("⚠ 未配置WordPress站点，创建模拟客户端...")
        site_url = os.getenv("WP_DEMO_URL", "https://demo.wordpress.com")
        wp_client = WordPressClient(
            site_url,
            os.getenv("WP_DEMO_USERNAME", "demo"),
            os.getenv("WP_DEMO_PASSWORD", "demo"),
            audit
        )
    
    # 6. 通过Pipeline执行操作
    print("\n[6] 通过Gate Pipeline执行操作...")
    
    # 创建一个读取操作
    read_op = Operation(
        op_type=OperationType.READ,
        actor="demo_script",
        resource=f"site:{site.name if settings.sites else 'demo'}",
        action="get_posts"
    )
    
    # 定义执行器
    def read_posts_executor(op: Operation):
        return wp_client.get_posts({"per_page": 5})
    
    # 通过Pipeline执行
    result = pipeline.execute(read_op, executor=read_posts_executor)
    
    print(f"\n操作结果:")
    print(f"  - 决策: {result.decision.value}")
    print(f"  - 执行: {'成功' if result.executed else '失败'}")
    print(f"  - 耗时: {result.duration_ms}ms")
    
    if result.error:
        print(f"  - 错误: {result.error}")
    elif result.result:
        posts = result.result if isinstance(result.result, list) else []
        print(f"  - 获取文章数: {len(posts)}")
    
    # 7. 尝试写入操作（会被Gate拦截）
    print("\n[7] 测试写入操作（会被Gate拦截）...")
    
    write_op = Operation(
        op_type=OperationType.WRITE,
        actor="demo_script",
        resource=f"site:{site.name if settings.sites else 'demo'}",
        action="create_post",
        params={"dry_run": True}
    )
    
    def create_post_executor(op: Operation):
        return wp_client.create_post(
            title="Auto-Claw Demo Post",
            content="这是通过Auto-Claw自动创建的文章",
            status="draft"
        )
    
    write_result = pipeline.execute(write_op, executor=create_post_executor)
    print(f"  - 决策: {write_result.decision.value}")
    print(f"  - 执行: {'成功' if write_result.executed else '失败'}")
    if write_result.decision.value == "need_approval":
        print("  - 说明: 写入操作需要人工审批（Gate设计）")
    
    # 8. 查看审计日志
    print("\n[8] 审计日志摘要...")
    entries = audit.query(limit=10)
    print(f"今日日志条目数: {len(entries)}")
    for entry in entries[-3:]:
        print(f"  [{entry.timestamp}] {entry.module}:{entry.action}")
    
    print("\n" + "=" * 60)
    print("Demo完成！")
    print("=" * 60)
    
    # 清理
    audit.close()


if __name__ == "__main__":
    main()
