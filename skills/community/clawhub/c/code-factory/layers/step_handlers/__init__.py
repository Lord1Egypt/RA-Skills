"""
步骤处理器（Step Handlers）—— 每个步骤一个独立处理器。

从 Orchestrator 拆分出来，实现真正的单一职责。
每个处理器包含：
- execute()：执行步骤逻辑
- compensate()：Saga 补偿函数（可选）
"""
