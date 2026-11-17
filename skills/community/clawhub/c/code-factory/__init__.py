"""
Code Factory — 代码交付工厂 (v1.0)

将自然语言需求自动转化为可交付的完整项目资产。

分层架构：
- contracts/   — 数据契约层（输入/输出 Schema）
- layers/      — 核心执行层（7 个步骤模块 + 编排器）
- middlewares/  — 横切关注点（熔断、事务、防腐、副作用追踪）
- templates/   — 模板资产（项目结构、README、manifest 等）
- tests/       — 技能自身测试套件

使用：
    from contracts.input_schema import ProjectRequest
    from layers.orchestrator import Orchestrator

    req = ProjectRequest(project_name="my_tool", description="...")
    orch = Orchestrator(req)
    result = orch.run()
"""

__version__ = "1.0.0"
