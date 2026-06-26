"""
Unit Tests for FlowBridge
单元测试
"""

import unittest
import time
from unittest.mock import Mock, patch
import sys
import os

# 添加scripts到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.workflow_engine import WorkflowEngine, Workflow, WorkflowNode, NodeType, NodeStatus
from scripts.connector_manager import ConnectorManager, PlatformType, AuthStatus
from scripts.ai_flow_generator import AIFlowGenerator, IntentParseResult
from scripts.template_center import TemplateCenter, WorkflowTemplate
from scripts.execution_monitor import ExecutionMonitor, ExecutionStatus
from scripts.permission_manager import PermissionManager, UserRole, ApprovalStatus


class TestWorkflowEngine(unittest.TestCase):
    """工作流引擎测试"""
    
    def setUp(self):
        self.engine = WorkflowEngine()
    
    def test_create_workflow(self):
        """测试创建工作流"""
        workflow = self.engine.create_workflow(
            name="测试流程",
            description="测试描述"
        )
        
        self.assertIsNotNone(workflow)
        self.assertEqual(workflow.name, "测试流程")
        self.assertEqual(workflow.description, "测试描述")
        self.assertIn(workflow.id, self.engine.workflows)
    
    def test_add_node(self):
        """测试添加节点"""
        workflow = self.engine.create_workflow("测试流程")
        
        node_id = self.engine.add_node(
            workflow_id=workflow.id,
            name="触发节点",
            node_type=NodeType.TRIGGER,
            platform="wechat",
            action="message_received"
        )
        
        self.assertIn(node_id, workflow.nodes)
        self.assertEqual(workflow.nodes[node_id].name, "触发节点")
    
    def test_connect_nodes(self):
        """测试连接节点"""
        workflow = self.engine.create_workflow("测试流程")
        
        node1 = self.engine.add_node(
            workflow_id=workflow.id,
            name="节点1",
            node_type=NodeType.TRIGGER,
            platform="wechat",
            action="trigger"
        )
        
        node2 = self.engine.add_node(
            workflow_id=workflow.id,
            name="节点2",
            node_type=NodeType.ACTION,
            platform="aliyun_drive",
            action="upload"
        )
        
        self.engine.connect_nodes(workflow.id, node1, node2)
        
        self.assertIn(node2, workflow.nodes[node1].next_nodes)
    
    def test_run_workflow(self):
        """测试执行工作流"""
        workflow = self.engine.create_workflow("测试流程")
        
        # 添加节点
        trigger_id = self.engine.add_node(
            workflow_id=workflow.id,
            name="触发器",
            node_type=NodeType.TRIGGER,
            platform="wechat",
            action="trigger"
        )
        
        action_id = self.engine.add_node(
            workflow_id=workflow.id,
            name="动作",
            node_type=NodeType.ACTION,
            platform="aliyun_drive",
            action="upload"
        )
        
        self.engine.connect_nodes(workflow.id, trigger_id, action_id)
        
        # 执行
        result = self.engine.run(workflow.id)
        
        self.assertTrue(result.success)
        self.assertEqual(len(result.node_results), 2)


class TestConnectorManager(unittest.TestCase):
    """连接器管理器测试"""
    
    def setUp(self):
        self.manager = ConnectorManager()
    
    def test_get_connector(self):
        """测试获取连接器"""
        connector = self.manager.get_connector('wechat')
        
        self.assertIsNotNone(connector)
        self.assertEqual(connector.platform, 'wechat')
    
    def test_list_connectors(self):
        """测试列出连接器"""
        connectors = self.manager.list_connectors()
        
        self.assertGreater(len(connectors), 0)
        self.assertTrue(any(c.platform == 'wechat' for c in connectors))
    
    def test_authorize(self):
        """测试授权"""
        auth = self.manager.authorize('wechat', 'mock_code')
        
        self.assertEqual(auth.status, AuthStatus.AUTHORIZED)
        self.assertIsNotNone(auth.access_token)
    
    def test_get_auth_status(self):
        """测试获取授权状态"""
        # 未授权
        status = self.manager.get_auth_status('wechat')
        self.assertEqual(status, AuthStatus.UNAUTHORIZED)
        
        # 授权后
        self.manager.authorize('wechat', 'mock_code')
        status = self.manager.get_auth_status('wechat')
        self.assertEqual(status, AuthStatus.AUTHORIZED)
    
    def test_execute_action(self):
        """测试执行操作"""
        # 先授权
        self.manager.authorize('wechat', 'mock_code')
        
        result = self.manager.execute_action(
            platform='wechat',
            action='send_message',
            params={'to': 'user', 'content': 'hello'}
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['platform'], 'wechat')


class TestAIFlowGenerator(unittest.TestCase):
    """AI流程生成器测试"""
    
    def setUp(self):
        self.generator = AIFlowGenerator()
    
    def test_generate_workflow(self):
        """测试生成工作流"""
        instruction = "微信收到文件后自动同步到阿里云盘"
        
        workflow = self.generator.generate(instruction)
        
        self.assertIsNotNone(workflow)
        self.assertGreater(len(workflow.nodes), 0)
    
    def test_validate_instruction(self):
        """测试验证指令"""
        # 有效指令
        result = self.generator.validate_instruction(
            "微信收到文件后自动同步到阿里云盘"
        )
        self.assertTrue(result['valid'])
        
        # 无效指令
        result = self.generator.validate_instruction("同步文件")
        self.assertFalse(result['valid'])
    
    def test_suggest_optimization(self):
        """测试优化建议"""
        instruction = "微信收到文件后自动同步到阿里云盘"
        workflow = self.generator.generate(instruction)
        
        suggestions = self.generator.suggest_optimization(workflow)
        
        self.assertIsInstance(suggestions, list)


class TestTemplateCenter(unittest.TestCase):
    """模板中心测试"""
    
    def setUp(self):
        self.center = TemplateCenter()
        self.engine = WorkflowEngine()
    
    def test_get_template(self):
        """测试获取模板"""
        template = self.center.get_template('tpl_wechat_to_aliyun')
        
        self.assertIsNotNone(template)
        self.assertEqual(template.category, 'personal')
    
    def test_list_templates(self):
        """测试列出模板"""
        templates = self.center.list_templates(category='personal')
        
        self.assertGreater(len(templates), 0)
        self.assertTrue(all(t.category == 'personal' for t in templates))
    
    def test_search_templates(self):
        """测试搜索模板"""
        results = self.center.search_templates('文件')
        
        self.assertGreater(len(results), 0)
    
    def test_create_workflow_from_template(self):
        """测试从模板创建工作流"""
        workflow = self.center.create_workflow_from_template(
            template_id='tpl_wechat_to_aliyun',
            workflow_engine=self.engine
        )
        
        self.assertIsNotNone(workflow)
        self.assertGreater(len(workflow.nodes), 0)


class TestExecutionMonitor(unittest.TestCase):
    """执行监控器测试"""
    
    def setUp(self):
        self.monitor = ExecutionMonitor()
    
    def test_start_execution(self):
        """测试开始执行"""
        self.monitor.start_execution('exec_001', 'wf_001', '测试流程')
        
        self.assertIn('exec_001', self.monitor.executions)
        self.assertEqual(self.monitor.stats['total_executions'], 1)
    
    def test_log_node_execution(self):
        """测试记录节点执行"""
        self.monitor.start_execution('exec_001', 'wf_001', '测试流程')
        
        self.monitor.log_node_start('exec_001', 'node_1', '节点1', 'wechat', 'send')
        self.monitor.log_node_complete('exec_001', 'node_1', ExecutionStatus.SUCCESS)
        
        logs = self.monitor.get_execution_logs(execution_id='exec_001')
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].status, ExecutionStatus.SUCCESS)
    
    def test_get_statistics(self):
        """测试获取统计"""
        self.monitor.start_execution('exec_001', 'wf_001', '测试')
        self.monitor.complete_execution('exec_001', success=True)
        
        stats = self.monitor.get_statistics()
        
        self.assertIn('total_executions', stats)
        self.assertIn('success_rate', stats)


class TestPermissionManager(unittest.TestCase):
    """权限管理器测试"""
    
    def setUp(self):
        self.pm = PermissionManager()
    
    def test_create_user(self):
        """测试创建用户"""
        user = self.pm.create_user('user_001', '测试用户', UserRole.MEMBER)
        
        self.assertIsNotNone(user)
        self.assertEqual(user.name, '测试用户')
        self.assertEqual(user.role, UserRole.MEMBER)
    
    def test_check_permission(self):
        """测试检查权限"""
        admin = self.pm.create_user('admin_001', '管理员', UserRole.ADMIN)
        member = self.pm.create_user('member_001', '成员', UserRole.MEMBER)
        
        # 管理员有所有权限
        self.assertTrue(self.pm.check_permission('admin_001', 'workflow:delete'))
        
        # 成员权限受限
        self.assertTrue(self.pm.check_permission('member_001', 'workflow:create'))
        self.assertFalse(self.pm.check_permission('member_001', 'workflow:approve'))
    
    def test_approval_workflow(self):
        """测试审批流程"""
        admin = self.pm.create_user('admin_001', '管理员', UserRole.ADMIN)
        member = self.pm.create_user('member_001', '成员', UserRole.MEMBER)
        
        # 提交审批
        approval = self.pm.submit_approval('wf_001', '测试流程', 'member_001')
        self.assertEqual(approval.status, ApprovalStatus.PENDING)
        
        # 处理审批
        result = self.pm.process_approval(approval.id, 'admin_001', True, '同意')
        self.assertTrue(result)
        self.assertEqual(approval.status, ApprovalStatus.APPROVED)
    
    def test_audit_logging(self):
        """测试审计日志"""
        self.pm.create_user('user_001', '测试用户', UserRole.MEMBER)
        
        logs = self.pm.get_audit_logs(action='user:create')
        
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].action, 'user:create')


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_workflow_lifecycle(self):
        """测试完整工作流生命周期"""
        # 初始化组件
        engine = WorkflowEngine()
        templates = TemplateCenter()
        monitor = ExecutionMonitor()
        pm = PermissionManager()
        
        # 1. 创建用户
        user = pm.create_user('user_001', '测试用户', UserRole.ADMIN)
        
        # 2. 从模板创建工作流
        workflow = templates.create_workflow_from_template(
            template_id='tpl_wechat_to_aliyun',
            workflow_engine=engine
        )
        self.assertIsNotNone(workflow)
        
        # 3. 执行工作流
        result = engine.run(workflow.id)
        self.assertTrue(result.success)
        
        # 4. 验证执行日志
        self.assertEqual(workflow.total_runs, 1)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestWorkflowEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestConnectorManager))
    suite.addTests(loader.loadTestsFromTestCase(TestAIFlowGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestTemplateCenter))
    suite.addTests(loader.loadTestsFromTestCase(TestExecutionMonitor))
    suite.addTests(loader.loadTestsFromTestCase(TestPermissionManager))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)