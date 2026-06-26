"""
demo.py - M-A3 多Agent记忆层使用示例

演示完整的记忆层使用流程。
"""

from __future__ import annotations

import sys
sys.path.insert(0, ".")

from agent_cluster.memory import (
    MemoryRouter,
    MemoryScope,
    MemoryType,
    MemoryImportance,
)
from agent_cluster.memory.memory_integration import (
    AgentMemoryGlue,
    SessionRecovery,
    CollaborationMemory,
    OrchestratorMemoryMixin,
)


def demo_basic():
    """基础使用演示"""
    print("\n" + "=" * 60)
    print("M-A3 多Agent记忆层 - 基础使用演示")
    print("=" * 60)
    
    # 1. 初始化记忆路由
    mr = MemoryRouter()
    
    # 2. 私有记忆
    print("\n[1] Agent 私有记忆")
    
    inventory_memory = mr.get_private("inventory")
    
    # 记忆偏好
    inventory_memory.memorize_preference("总是优先查询华东仓库")
    
    # 记忆知识
    inventory_memory.memorize_knowledge(
        "SKU001 是爆款，平均日销量 50 件，补货周期 3 天",
        importance=MemoryImportance.HIGH,
        tags=["sku001", "inventory"],
    )
    
    # 提炼规则
    inventory_memory.memorize_rule(
        "当库存 < 安全库存 × 1.5 时，自动触发补货提醒",
        reason="避免断货影响销售",
    )
    
    # 召回
    rules = inventory_memory.recall_rules()
    print(f"  提炼的规则数量: {len(rules)}")
    for r in rules[:2]:
        print(f"  - {r.content[:60]}")
    
    # 3. 共享知识池
    print("\n[2] 共享知识池")
    
    # 库存Agent发布库存事实
    fact_id = mr.shared.publish_fact(
        content='{"SKU001": {"qty": 100, "warehouse": "华东", "last_update": "2026-04-14"}}',
        author_agent_id="inventory",
        tags=["inventory", "sku001"],
        summary="SKU001 当前库存 100 件",
    )
    print(f"  发布库存事实: {fact_id[:20]}...")
    
    # 财务Agent查询共享知识
    finance_result = mr.shared.query_knowledge(
        query_text="库存",
        caller_agent_id="finance",
        limit=10,
    )
    print(f"  财务Agent查询到相关知识: {finance_result.total} 条")
    
    # 4. 会话同步
    print("\n[3] 会话记忆同步")
    
    # 创建协作会话
    session = mr.session.create_session(
        task_id="task_procurement_001",
        root_agent_id="orchestrator",
        title="SKU001 补货采购任务",
        participants=["orchestrator", "inventory", "finance", "procurement"],
    )
    print(f"  会话创建: {session.session_id[:20]}...")
    print(f"  参与者: {session.participants}")
    
    # 记录会话事件
    mr.session.log_event(
        session_id=session.session_id,
        agent_id="inventory",
        event_type="task_start",
        content="开始检查 SKU001 库存",
    )
    
    # 广播决策
    mr.session.broadcast_decision(
        session_id=session.session_id,
        agent_id="finance",
        decision="批准补货，预算 ¥5000",
        reason="库存低于安全水位",
    )
    
    # 查询会话事件
    events = mr.session.get_events(session.session_id)
    print(f"  会话事件数: {len(events)}")
    for e in events[:3]:
        print(f"  - [{e.event_type}] {e.agent_id}: {e.content[:40]}")
    
    # 5. 跨Agent同步
    print("\n[4] 跨Agent知识同步")
    
    sync_result = mr.sync_across_agents(
        content="SKU001 爆款预警：当前库存仅够 2 天销售，请尽快补货",
        from_agent_id="inventory",
        to_agent_ids=["procurement", "finance", "logistics"],
        reason="库存预警",
        session_id=session.session_id,
    )
    print(f"  同步结果: {list(sync_result.keys())}")
    
    # 6. 构建Agent上下文
    print("\n[5] 构建Agent上下文")
    
    ctx = mr.build_agent_context(
        agent_id="procurement",
        task_query="SKU001 补货",
    )
    print(f"  上下文长度: {len(ctx)} 字符")
    if ctx:
        print(f"  前100字: {ctx[:100]}")
    
    # 7. 统一读写 API
    print("\n[6] 统一读写 API")
    
    entry_id = mr.memorize(
        content="采购单 PO-2026-0414-001 已创建，供货商：供应商A",
        agent_id="procurement",
        scope=MemoryScope.SHARED,
        memory_type=MemoryType.FACT,
        importance=MemoryImportance.HIGH,
        tags=["purchase_order", "po-001"],
        related_agent_ids=["finance", "inventory"],
    )
    print(f"  写入记忆: {entry_id[:20]}...")
    
    # 查询
    recall_result = mr.recall(
        agent_id="finance",
        query_text="SKU001",
        scope="shared",
        limit=10,
    )
    print(f"  召回结果: {recall_result.total} 条")


def demo_agent_glue():
    """Agent记忆胶水演示"""
    print("\n" + "=" * 60)
    print("Agent 记忆胶水演示")
    print("=" * 60)
    
    # 为采购Agent安装记忆能力
    procurement_memory = AgentMemoryGlue(agent_id="procurement")
    
    # 记忆偏好
    procurement_memory.remember_preference("首选供应商", "供应商A")
    
    # 记忆知识
    procurement_memory.remember_knowledge(
        "供应商A 交货周期 5 天，供应商B 交货周期 3 天（加急费 10%）",
        tags=["supplier", "lead_time"],
    )
    
    # 提炼规则
    procurement_memory.remember_rule(
        "单次采购金额 > ¥10000 需要财务审批",
    )
    
    # 使用装饰器自动记忆任务结果
    @procurement_memory.memorize_outcome
    def create_purchase_order(sku, qty, supplier):
        return {"status": "success", "po_id": "PO-001", "amount": qty * 100}
    
    result = create_purchase_order("SKU001", 100, "供应商A")
    print(f"\n  任务执行结果: {result}")
    
    # 召回近期任务
    history = procurement_memory.recall(limit=5)
    print(f"  近期记忆: {len(history)} 条")


def demo_collaboration():
    """协同记忆演示"""
    print("\n" + "=" * 60)
    print("协同记忆演示")
    print("=" * 60)
    
    collab = CollaborationMemory(primary_agent_id="orchestrator")
    
    # 启动多Agent协作
    session_id = collab.start_collaboration(
        task_id="task_monthly_report",
        participants=["finance", "procurement", "inventory", "sales"],
        title="月度经营报告生成",
    )
    print(f"\n  协作会话: {session_id[:20]}...")
    
    # 共享中间结果
    inventory_data = '{"revenue": 500000, "cost": 300000, "margin": 40}'
    collab.share_intermediate_result(
        session_id=session_id,
        agent_id="inventory",
        result=f"销售数据：{inventory_data}",
        next_agent_id="finance",
    )
    
    # 记录决策
    collab.record_collaboration_decision(
        session_id=session_id,
        decision="本月毛利率目标 35%，若低于此值需启动成本优化流程",
        decided_by="finance",
        participants=["finance", "procurement", "sales"],
    )
    
    # 获取协作历史
    history = collab.get_collaboration_history(session_id, "procurement")
    print(f"  协作历史-决策数: {len(history.get('decisions', []))}")
    print(f"  协作历史-事件数: {len(history.get('events', []))}")


def demo_session_recovery():
    """会话恢复演示"""
    print("\n" + "=" * 60)
    print("会话恢复演示")
    print("=" * 60)
    
    recovery = SessionRecovery(agent_id="inventory")
    
    # 保存检查点
    task_state = {
        "current_step": 2,
        "total_steps": 5,
        "processed_skus": ["SKU001", "SKU002"],
        "pending_skus": ["SKU003", "SKU004"],
        "errors": [],
    }
    
    checkpoint_id = recovery.save_checkpoint(
        session_id="session_resume_demo",
        task_state=task_state,
        current_task="批量检查 SKU 库存",
    )
    print(f"\n  检查点保存: {checkpoint_id[:20]}...")
    
    # 模拟重启后加载
    loaded = recovery.load_checkpoint("session_resume_demo")
    print(f"  检查点加载: {'成功' if loaded else '失败'}")
    if loaded:
        print(f"  当前步骤: {loaded.get('current_step')}/{loaded.get('total_steps')}")
    
    # 完整会话恢复
    full_recovery = recovery.recover_session(
        session_id="session_resume_demo",
        requester_agent_id="inventory",
    )
    print(f"  完整恢复: {list(full_recovery.keys())}")


if __name__ == "__main__":
    demo_basic()
    demo_agent_glue()
    demo_collaboration()
    demo_session_recovery()
    print("\n✅ 所有演示完成！")
