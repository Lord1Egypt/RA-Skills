# FlowBridge - 零代码跨生态自动化工具

一款让无代码基础的用户也能在3分钟内搭建跨平台自动化流程的工具，连接微信、钉钉、飞书、WPS等国内主流生态。

## 核心功能

### 1. 国内全生态接口对接
- 微信（个人/企业）
- 钉钉
- 飞书
- WPS
- 腾讯文档
- 阿里云盘

### 2. 零代码自动化流程配置
- 可视化拖拽配置
- 触发条件 + 操作动作 + 分支判断
- 单流程最多10个节点
- 支持保存、编辑、复制、删除

### 3. AI流程智能生成
- 自然语言指令识别
- 自动生成完整流程
- 流程优化建议
- 中文语义理解

### 4. 流程执行监控与异常兜底
- 实时监控执行状态
- 与重试降级Skill联动
- 执行日志记录
- 支持导出Excel/PDF

### 5. 模板中心
| 分类 | 模板数量 | 覆盖场景 |
|-----|---------|---------|
| 个人 | 4+ | 文件同步、聊天记录整理、自动记账、定时提醒 |
| 小微企业 | 4+ | 订单同步、审批归档、发票整理、员工通知 |
| 企业级 | 3+ | 跨平台同步、数据汇总、入职流程 |

### 6. 权限管控与合规审计
- 用户角色分级（管理员/成员/访客）
- 流程审批机制
- 完整审计日志
- 符合国内数据安全法规

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

### 基础用法 - 创建工作流

```python
from scripts.workflow_engine import WorkflowEngine, NodeType

# 创建引擎
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
    action="file_received"
)

# 添加动作节点
action_id = engine.add_node(
    workflow_id=workflow.id,
    name="上传到阿里云盘",
    node_type=NodeType.ACTION,
    platform="aliyun_drive",
    action="upload_file"
)

# 连接节点
engine.connect_nodes(workflow.id, trigger_id, action_id)

# 执行流程
result = engine.run(workflow.id)
print(f"执行结果: {'成功' if result.success else '失败'}")
```

### AI生成流程

```python
from scripts.ai_flow_generator import AIFlowGenerator

ai_gen = AIFlowGenerator()

# 自然语言指令生成流程
workflow = ai_gen.generate("微信收到文件后自动同步到阿里云盘")

# 获取优化建议
suggestions = ai_gen.suggest_optimization(workflow)
```

### 使用模板

```python
from scripts.template_center import TemplateCenter
from scripts.workflow_engine import WorkflowEngine

templates = TemplateCenter()
engine = WorkflowEngine()

# 从模板创建工作流
workflow = templates.create_workflow_from_template(
    template_id="tpl_wechat_to_aliyun",
    workflow_engine=engine
)

# 搜索模板
results = templates.search_templates("文件同步")
```

### 连接器管理

```python
from scripts.connector_manager import ConnectorManager

manager = ConnectorManager()

# 获取授权URL
auth_url = manager.get_auth_url('wechat')

# 完成授权
auth = manager.authorize('wechat', auth_code='xxx')

# 执行操作
result = manager.execute_action(
    platform='wechat',
    action='send_message',
    params={'to': 'user', 'content': 'Hello'}
)
```

### 执行监控

```python
from scripts.execution_monitor import ExecutionMonitor

monitor = ExecutionMonitor()

# 开始执行监控
monitor.start_execution('exec_001', 'wf_001', '测试流程')

# 记录节点执行
monitor.log_node_start('exec_001', 'node_1', '触发器', 'wechat', 'file_received')
monitor.log_node_complete('exec_001', 'node_1', ExecutionStatus.SUCCESS)

# 获取执行报告
report = monitor.get_execution_report('exec_001')

# 导出日志
filepath = monitor.export_logs(format='json')
```

### 权限管理

```python
from scripts.permission_manager import PermissionManager, UserRole

pm = PermissionManager()

# 创建用户
admin = pm.create_user('admin_001', '管理员', UserRole.ADMIN)
member = pm.create_user('member_001', '成员', UserRole.MEMBER)

# 检查权限
has_permission = pm.check_permission('member_001', 'workflow:create')

# 提交审批
approval = pm.submit_approval('wf_001', '重要流程', 'member_001')

# 处理审批
pm.process_approval(approval.id, 'admin_001', approved=True, comment='同意')
```

## 项目结构

```
flowbridge/
├── SKILL.md                 # Skill说明文档
├── README.md                # 完整文档
├── requirements.txt         # 依赖列表
├── config/
│   └── connectors.yaml      # 连接器配置
├── scripts/                 # 核心模块
│   ├── __init__.py
│   ├── workflow_engine.py   # 流程引擎
│   ├── connector_manager.py # 生态连接器
│   ├── ai_flow_generator.py # AI流程生成
│   ├── template_center.py   # 模板中心
│   ├── execution_monitor.py # 执行监控
│   └── permission_manager.py # 权限管理
├── examples/
│   └── basic_usage.py       # 7个使用示例
└── tests/
    └── test_automation.py   # 单元测试
```

## 运行测试

```bash
cd tests
python test_automation.py

# 预期输出:
# Ran 25+ tests in X.XXXs
# OK
```

## 运行示例

```bash
cd examples
python basic_usage.py
```

## API参考

### WorkflowEngine - 流程引擎

```python
# 创建工作流
workflow = engine.create_workflow(name, description)

# 添加节点
node_id = engine.add_node(
    workflow_id,
    name,
    node_type,      # TRIGGER, ACTION, CONDITION
    platform,       # wechat, dingtalk, feishu, etc.
    action,
    params={},
    is_critical=True
)

# 连接节点
engine.connect_nodes(workflow_id, from_node, to_node)

# 执行流程
result = engine.run(workflow_id, context={})

# 返回 ExecutionResult
result.success          # bool
result.node_results     # Dict
result.duration         # float
result.degraded         # bool
```

### ConnectorManager - 连接器管理器

```python
# 获取连接器
connector = manager.get_connector(platform)

# 获取授权URL
auth_url = manager.get_auth_url(platform, redirect_uri)

# 授权
auth = manager.authorize(platform, auth_code)

# 检查授权状态
status = manager.get_auth_status(platform)

# 执行操作
result = manager.execute_action(platform, action, params)

# 刷新令牌
success = manager.refresh_token(platform)
```

### AIFlowGenerator - AI流程生成器

```python
# 生成流程
workflow = generator.generate(instruction, workflow_name)

# 验证指令
validation = generator.validate_instruction(instruction)
# validation['valid']       # bool
# validation['missing_info'] # List[str]
# validation['suggestions']  # List[str]

# 获取优化建议
suggestions = generator.suggest_optimization(workflow)
```

### TemplateCenter - 模板中心

```python
# 获取模板
template = center.get_template(template_id)

# 列出模板
templates = center.list_templates(
    category='personal',        # personal/business/enterprise
    platforms=['wechat'],
    tags=['文件同步']
)

# 搜索模板
results = center.search_templates(keyword)

# 从模板创建工作流
workflow = center.create_workflow_from_template(
    template_id,
    workflow_engine,
    custom_params
)
```

### ExecutionMonitor - 执行监控器

```python
# 开始执行
monitor.start_execution(execution_id, workflow_id, workflow_name)

# 记录节点
monitor.log_node_start(execution_id, node_id, name, platform, action)
monitor.log_node_complete(execution_id, node_id, status, result, error)

# 完成执行
monitor.complete_execution(execution_id, success, error_message)

# 获取报告
report = monitor.get_execution_report(execution_id)

# 获取统计
stats = monitor.get_statistics()

# 导出日志
filepath = monitor.export_logs(format='json/csv', filepath='logs.json')
```

### PermissionManager - 权限管理器

```python
# 创建用户
user = pm.create_user(user_id, name, role, team_id)

# 检查权限
has_permission = pm.check_permission(user_id, permission)

# 分配角色
pm.assign_role(user_id, role)

# 提交审批
approval = pm.submit_approval(workflow_id, workflow_name, applicant, reason)

# 处理审批
pm.process_approval(approval_id, approver, approved, comment)

# 获取审计日志
logs = pm.get_audit_logs(user_id, action, resource_type)

# 导出审计日志
filepath = pm.export_audit_logs(filepath)
```

## 默认模板列表

### 个人场景
- `tpl_wechat_to_aliyun` - 微信文件自动同步到阿里云盘
- `tpl_chat_backup` - 聊天记录自动整理备份
- `tpl_expense_tracker` - 消费记录自动记账
- `tpl_daily_reminder` - 每日定时提醒

### 小微企业
- `tpl_order_to_sheet` - 微信订单自动同步到腾讯文档
- `tpl_approval_archive` - 钉钉审批自动归档
- `tpl_invoice_organize` - 发票自动整理
- `tpl_employee_notify` - 员工通知自动推送

### 企业级
- `tpl_cross_platform_sync` - 飞书任务同步到钉钉通知
- `tpl_data_summary` - 跨办公软件数据汇总
- `tpl_onboarding` - 员工入职流程自动化

## 与重试降级Skill联动

本Skill与 `clawhub-retry-fallback` Skill无缝集成：

```python
from scripts.workflow_engine import WorkflowEngine
from clawhub_retry_fallback.scripts.retry_handler import RetryHandler

# 初始化重试降级Skill
retry_handler = RetryHandler()

# 传递给流程引擎
engine = WorkflowEngine(retry_fallback_skill=retry_handler)

# 执行流程时自动使用重试降级能力
result = engine.run(workflow_id)
```

## 性能指标

| 指标 | 目标值 |
|-----|-------|
| 流程配置响应耗时 | ≤100ms |
| 流程执行响应耗时 | ≤500ms/节点 |
| 接口联动成功率 | ≥99% |
| 流程整体成功率 | ≥95% |
| 模块可用性 | ≥99.99% |

## 兼容性

- ✅ 与重试降级Skill无缝联动
- ✅ 兼容PC端、移动端
- ✅ 支持Chrome、Edge、Firefox
- ✅ 支持私有化部署

## 安全与合规

- 数据加密传输和存储
- 符合《个人信息保护法》《网络安全法》《数据安全法》
- 完整的审计日志
- 敏感操作拦截

## License

MIT License - ClawHub Platform