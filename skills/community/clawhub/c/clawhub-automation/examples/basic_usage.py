"""
ClawHub Automation Skill - 使用示例
零代码跨生态自动化使用示例
"""

import sys
import os

# 添加scripts到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.workflow_engine import WorkflowEngine, Workflow, NodeType
from scripts.connector_manager import ConnectorManager, PlatformType
from scripts.ai_flow_generator import AIFlowGenerator
from scripts.template_center import TemplateCenter
from scripts.execution_monitor import ExecutionMonitor
from scripts.permission_manager import PermissionManager, UserRole


def example_1_basic_workflow():
    """示例1: 基础工作流创建与执行"""
    print("=" * 60)
    print("示例1: 基础工作流创建与执行")
    print("=" * 60)
    
    # 创建工作流引擎
    engine = WorkflowEngine()
    
    # 创建工作流
    workflow = engine.create_workflow(
        name="微信文件自动备份",
        description="微信收到文件后自动备份到阿里云盘"
    )
    
    # 添加触发节点
    trigger_id = engine.add_node(
        workflow_id=workflow.id,
        name="微信收到文件",
        node_type=NodeType.TRIGGER,
        platform="wechat",
        action="file_received",
        params={"file_types": ["*"]}
    )
    
    # 添加动作节点
    action_id = engine.add_node(
        workflow_id=workflow.id,
        name="上传到阿里云盘",
        node_type=NodeType.ACTION,
        platform="aliyun_drive",
        action="upload_file",
        params={"folder": "/backup/wechat"}
    )
    
    # 连接节点
    engine.connect_nodes(workflow.id, trigger_id, action_id)
    
    print(f"✓ 工作流创建成功: {workflow.name}")
    print(f"  ID: {workflow.id}")
    print(f"  节点数: {len(workflow.nodes)}")
    print()


def example_2_ai_generate():
    """示例2: AI生成流程"""
    print("=" * 60)
    print("示例2: AI生成流程")
    print("=" * 60)
    
    ai_gen = AIFlowGenerator()
    
    # 自然语言指令生成流程
    instructions = [
        "微信收到文件后自动同步到阿里云盘",
        "钉钉审批完成后自动归档到云盘并发送通知",
        "每天定时整理聊天记录并备份到腾讯文档"
    ]
    
    for instruction in instructions:
        print(f"\n指令: {instruction}")
        
        # 验证指令
        validation = ai_gen.validate_instruction(instruction)
        if not validation['valid']:
            print(f"  ! 指令不完整: {validation['missing_info']}")
            print(f"  建议: {validation['suggestions']}")
            continue
        
        # 生成流程
        workflow = ai_gen.generate(instruction)
        
        print(f"  ✓ 生成工作流: {workflow.name}")
        print(f"    节点: {list(workflow.nodes.keys())}")
        
        # 获取优化建议
        suggestions = ai_gen.suggest_optimization(workflow)
        if suggestions:
            print(f"    优化建议:")
            for s in suggestions:
                print(f"      - {s['message']}")
    print()


def example_3_template_usage():
    """示例3: 使用模板"""
    print("=" * 60)
    print("示例3: 使用模板中心")
    print("=" * 60)
    
    template_center = TemplateCenter()
    engine = WorkflowEngine()
    
    # 列出所有模板
    print("\n【个人场景模板】")
    personal_templates = template_center.list_templates(category='personal')
    for tpl in personal_templates[:3]:
        print(f"  - {tpl.name}: {tpl.description}")
    
    print("\n【小微企业模板】")
    business_templates = template_center.list_templates(category='business')
    for tpl in business_templates[:3]:
        print(f"  - {tpl.name}: {tpl.description}")
    
    # 搜索模板
    print("\n【搜索'文件'相关模板】")
    results = template_center.search_templates("文件")
    for tpl in results:
        print(f"  - {tpl.name}")
    
    # 从模板创建工作流
    print("\n【从模板创建工作流】")
    workflow = template_center.create_workflow_from_template(
        template_id="tpl_wechat_to_aliyun",
        workflow_engine=engine
    )
    
    if workflow:
        print(f"  ✓ 创建工作流: {workflow.name}")
        print(f"    节点数: {len(workflow.nodes)}")
    print()


def example_4_connector_management():
    """示例4: 连接器管理"""
    print("=" * 60)
    print("示例4: 连接器管理")
    print("=" * 60)
    
    manager = ConnectorManager()
    
    # 列出所有连接器
    print("\n【支持的平台】")
    for connector in manager.list_connectors():
        print(f"  - {connector.name}: {len(connector.supported_actions)} 个操作")
    
    # 获取授权URL
    print("\n【微信授权URL】")
    auth_url = manager.get_auth_url('wechat', redirect_uri='https://example.com/callback')
    print(f"  {auth_url[:80]}...")
    
    # 模拟授权
    print("\n【模拟授权】")
    auth = manager.authorize('wechat', auth_code='mock_auth_code_123')
    print(f"  ✓ 授权状态: {auth.status.value}")
    print(f"    Token: {auth.access_token[:20]}...")
    
    # 检查授权状态
    status = manager.get_auth_status('wechat')
    print(f"    状态检查: {status.value}")
    
    # 执行操作
    print("\n【执行操作】")
    result = manager.execute_action(
        platform='wechat',
        action='send_message',
        params={'to': 'user123', 'content': 'Hello'}
    )
    print(f"  ✓ 执行结果: {result}")
    print()


def example_5_execution_monitoring():
    """示例5: 执行监控"""
    print("=" * 60)
    print("示例5: 执行监控")
    print("=" * 60)
    
    monitor = ExecutionMonitor()
    
    # 模拟执行监控
    execution_id = "exec_001"
    workflow_id = "wf_001"
    workflow_name = "测试流程"
    
    # 开始执行
    monitor.start_execution(execution_id, workflow_id, workflow_name)
    
    # 记录节点执行
    import time
    
    monitor.log_node_start(execution_id, 'node_1', '触发器', 'wechat', 'file_received')
    time.sleep(0.1)
    monitor.log_node_complete(execution_id, 'node_1', ExecutionStatus.SUCCESS)
    
    monitor.log_node_start(execution_id, 'node_2', '上传文件', 'aliyun_drive', 'upload_file')
    time.sleep(0.1)
    monitor.log_node_complete(execution_id, 'node_2', ExecutionStatus.SUCCESS)
    
    # 完成执行
    monitor.complete_execution(execution_id, success=True)
    
    # 获取执行报告
    print("\n【执行报告】")
    report = monitor.get_execution_report(execution_id)
    if report:
        print(f"  工作流: {report['workflow_name']}")
        print(f"  状态: {report['status']}")
        print(f"  耗时: {report['duration']:.3f}秒")
        print(f"  节点数: {report['node_count']}")
    
    # 获取统计
    print("\n【执行统计】")
    stats = monitor.get_statistics()
    print(f"  总执行: {stats['total_executions']}")
    print(f"  成功: {stats['successful']}")
    print(f"  成功率: {stats['success_rate']}")
    print()


def example_6_permission_management():
    """示例6: 权限管理"""
    print("=" * 60)
    print("示例6: 权限管理")
    print("=" * 60)
    
    pm = PermissionManager()
    
    # 创建用户
    print("\n【创建用户】")
    admin = pm.create_user('user_001', '管理员', UserRole.ADMIN, 'team_001')
    member = pm.create_user('user_002', '普通成员', UserRole.MEMBER, 'team_001')
    guest = pm.create_user('user_003', '访客', UserRole.GUEST, 'team_001')
    
    print(f"  ✓ 管理员: {admin.name}, 权限数: {len(admin.permissions)}")
    print(f"  ✓ 成员: {member.name}, 权限数: {len(member.permissions)}")
    print(f"  ✓ 访客: {guest.name}, 权限数: {len(guest.permissions)}")
    
    # 检查权限
    print("\n【权限检查】")
    print(f"  管理员创建工作流: {pm.check_permission('user_001', 'workflow:create')}")
    print(f"  成员创建工作流: {pm.check_permission('user_002', 'workflow:create')}")
    print(f"  访客创建工作流: {pm.check_permission('user_003', 'workflow:create')}")
    print(f"  成员审批工作流: {pm.check_permission('user_002', 'workflow:approve')}")
    
    # 提交审批
    print("\n【流程审批】")
    approval = pm.submit_approval(
        workflow_id='wf_001',
        workflow_name='重要业务流程',
        applicant='user_002',
        reason='需要部署到生产环境'
    )
    print(f"  ✓ 提交审批: {approval.id}")
    print(f"    状态: {approval.status.value}")
    
    # 处理审批
    result = pm.process_approval(
        approval_id=approval.id,
        approver='user_001',
        approved=True,
        comment='同意部署'
    )
    print(f"  ✓ 审批处理: {'成功' if result else '失败'}")
    print(f"    最终状态: {pm.approvals[approval.id].status.value}")
    
    # 审计日志
    print("\n【审计日志】")
    logs = pm.get_audit_logs(user_id='user_001')
    print(f"  管理员操作记录: {len(logs)} 条")
    print()


def example_7_integration():
    """示例7: 综合使用"""
    print("=" * 60)
    print("示例7: 综合使用 - 完整场景")
    print("=" * 60)
    
    # 初始化所有组件
    engine = WorkflowEngine()
    connectors = ConnectorManager()
    ai_gen = AIFlowGenerator()
    templates = TemplateCenter()
    monitor = ExecutionMonitor()
    pm = PermissionManager()
    
    print("\n【场景: 小微企业自动化办公】")
    
    # 1. 创建企业用户
    admin = pm.create_user('admin_001', '企业管理员', UserRole.ADMIN, 'company_001')
    print(f"1. 创建管理员: {admin.name}")
    
    # 2. 从模板创建工作流
    workflow = templates.create_workflow_from_template(
        template_id='tpl_order_to_sheet',
        workflow_engine=engine
    )
    print(f"2. 从模板创建工作流: {workflow.name if workflow else '失败'}")
    
    # 3. AI优化流程
    if workflow:
        suggestions = ai_gen.suggest_optimization(workflow)
        print(f"3. AI优化建议: {len(suggestions)} 条")
        for s in suggestions:
            print(f"   - {s['message']}")
    
    # 4. 提交审批
    if workflow:
        approval = pm.submit_approval(
            workflow_id=workflow.id,
            workflow_name=workflow.name,
            applicant='admin_001'
        )
        print(f"4. 提交审批: {approval.id}")
    
    # 5. 模拟执行
    if workflow:
        result = engine.run(workflow.id, context={'message': '测试订单'})
        print(f"5. 执行结果: {'成功' if result.success else '失败'}")
        print(f"   耗时: {result.duration:.3f}秒")
        print(f"   降级执行: {result.degraded}")
    
    print("\n✓ 综合场景演示完成")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("ClawHub 零代码跨生态自动化 Skill")
    print("使用示例")
    print("=" * 60 + "\n")
    
    examples = [
        ("基础工作流", example_1_basic_workflow),
        ("AI生成流程", example_2_ai_generate),
        ("模板中心", example_3_template_usage),
        ("连接器管理", example_4_connector_management),
        ("执行监控", example_5_execution_monitoring),
        ("权限管理", example_6_permission_management),
        ("综合使用", example_7_integration),
    ]
    
    print(f"共有 {len(examples)} 个示例\n")
    print("-" * 60)
    
    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\n✗ 示例 '{name}' 执行出错: {e}\n")
        print("-" * 60)
    
    print("\n" + "=" * 60)
    print("所有示例执行完成!")
    print("=" * 60)