# Roundtable Release Planning Discussion

**Date**: 2026-05-23  
**Discussion ID**: `rt_xxxxxxxx`  
**WebViewer**: `http://0.0.0.0:8206/r/COVUagOC9zBn5ByxHTyEMiI7`  
**Conclusion doc**: `roundtable/docs/discussions/rt_xxxxxxxx_roundtable-release-plan.md`

## Configuration

```python
roundtable_init(
    topic="关于 roundtable 发布到各大 skill 平台以及开源的相关事宜",
    context="roundtable 技能是一个实现多 Agent 圆桌讨论的技术方案...",
    participants=[
        {"profile": "bingge", "role": "产品总监", "perspective": "产品规划与市场策略", "display_name": "饼哥"},
        {"profile": "pixiel", "role": "设计师", "perspective": "用户体验与开源社区呈现", "display_name": "像素姐"},
        {"profile": "mafei", "role": "开发者", "perspective": "技术实现与工程可行性", "display_name": "码飞"},
    ],
    max_rounds=3,
    notifications={
        "enabled": True,
        "channels": [{"platform": "feishu", "chat_id": "oc_your_company_group_id"}],
        "events": ["round_start", "speech", "round_end", "concluded"]
    },
    web=True
)
```

## Workflow Used

**Hybrid approach** (delegate_task for reasoning + Direct Core API for recording):
1. Coordinator opened Round 1 via Direct Core API
2. Each participant: `delegate_task` → extract summary → `core.speak()` to record
3. Coordinator summarized between rounds via `core.speak(participant="coordinator")`
4. Notifications sent to company group after each round via `send_message`

## Key Results

### Round 1 — 版本号、发布平台、许可证、准备时间
- **饼哥**: 版本 0.1.0，首选 Hermes Skill Hub，Apache 2.0，技术准备 2 天
- **像素姐**: 社区图标准备 1 天，品牌标识明确，开源文档站计划
- **码飞**: GitLab → Hermes Skill Hub，自动化 CI/CD 测试，安全审查步骤

### Round 2 — 细化计划与执行标准
- **饼哥**: 详细时间表（D0-D2），Apache 2.0 明确，平台发布清单
- **像素姐**: 社区图标交付物清单，开源文档站最小功能集
- **码飞**: CI/CD pipeline 配置，安全审查自动化步骤

### Round 3 — 最终确认与行动项分配
- **饼哥**: 每个角色具体行动项，验收标准，发布流程 checklist
- **像素姐**: 社区图标交付时间，品牌指南文档
- **码飞**: 开发任务分配，技术债务清理，发布自动化

## Consensus Achieved

| 决策项 | 结论 |
|--------|------|
| 版本号 | 0.1.0 |
| 发布平台 | 首选 Hermes Skill Hub，后续考虑 PyPI/ClawHub |
| 许可证 | Apache 2.0 |
| 技术准备时间 | 2 天 |
| 发布日期 | D3（5/26） |

## Action Items by Role

### 饼哥（产品）
- D0: 起草 v0.1.0 发布公告
- D1: 准备发布 checklist，确认所有技术准备完成
- D2: 最终审核，准备发布流程

### 像素姐（设计）
- D0: 设计社区图标初稿
- D1: 完善品牌标识，准备开源文档站设计
- D2: 交付所有设计资产

### 码飞（开发）
- D0: 设置 CI/CD pipeline，安全审查自动化
- D1: 代码清理，文档完善，测试覆盖
- D2: 最终技术审核，发布准备

## Lessons Learned

1. **Hybrid workflow is optimal**: delegate_task for reasoning + Direct Core API for recording is the most reliable pattern
2. **Notifications must be in init config**: If not passed in `roundtable_init`, no notifications are sent
3. **WebViewer must be opened manually**: Direct Core API doesn't trigger browser open — must manually share URL and run `open`
4. **Conclusion doc must be written BEFORE `roundtable_end`**: `end()` only accepts brief text, not full documents
5. **3 rounds is optimal for product/design/dev discussions**: Allows initial exploration → detailed planning → final action items
