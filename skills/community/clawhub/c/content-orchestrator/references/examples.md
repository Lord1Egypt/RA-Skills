# content-orchestrator 使用示例

> 来源: SKILL.md + pipeline_state.py测试用例

## 示例1: 创建端到端管线

```python
from skills.content_orchestrator.scripts.pipeline_state import create_pipeline

pipeline = create_pipeline(
    title="夏日饮品推广视频",
    pipeline_type="E2E-DAILY",
    tenant_id="tenant_001",
    items_count=3,
    source="manual"
)
# 返回: {"id": "CP-20260728-abc123", "title": "...", "steps": [...], ...}
```

## 示例2: 更新步骤状态

```python
from skills.content_orchestrator.scripts.pipeline_state import update_step

result = update_step(
    pipeline_id="CP-20260728-abc123",
    step_name="hotspot",
    status="completed",
    progress="发现3个热点话题",
    output={"topics": ["夏日饮品", "健康饮食", "DIY制作"]}
)
```

## 示例3: 重试失败步骤

```python
from skills.content_orchestrator.scripts.pipeline_state import redo_step

result = redo_step(
    pipeline_id="CP-20260728-abc123",
    step_name="material_gen",  # 必须为failed状态
    clear_checkpoint=True
)
# 返回: {"success": True, "data": {"reset_steps": ["material_gen", "qa", "publish", ...], "preserved_steps": ["hotspot", "copywrite"]}}
```

## 示例4: 查询活跃管线

```python
from skills.content_orchestrator.scripts.pipeline_state import list_active_pipelines

active = list_active_pipelines(tenant_id="tenant_001")
# 返回: 当前有未完成步骤的管线列表
```
