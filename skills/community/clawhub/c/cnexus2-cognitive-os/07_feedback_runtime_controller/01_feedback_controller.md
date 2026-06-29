# 01_feedback_controller — 反馈控制器规格

**层级：L3（治理/演化/反馈系统）**
**输入源：** FailureReport（来自 06 失败分析器）
**权限：** 只读 FailureReport、只读 L1/L2 输出——**无直接修改当前运行状态的权限**

---

## 一、职责

反馈控制器分析失败分析器的报告，生成 **revision_proposal**（修订提案）。

提案只以 L0 词汇表描述。提案不包含 L1/L2/L3 实现细节。

**反馈控制器的输出结果是下一轮循环的输入参数，而不是对当前运行状态的直接修改。**

## 二、反馈的物理路径

```
反馈控制器 → 生成 revision_proposal → 写入 Block Store（特定标记的 proposal block）
  → 下一轮循环的 OBSERVE 步在正常流程中读取这些 Block
  → COGNIZE 步将其作为 recall_items 之一纳入上下文
  → DECIDE 步可以据此调整策略
```

**反馈绝不直接注入当前 State。**

## 三、Revision Proposal 的格式

```
RevisionProposal = {
  proposal_id: str,               # UUID
  source: str,                    # "failure_analysis" / "periodic_review"
  proposed_changes: list[{
    target: str,                  # "L0" / "L1_reducer_XX" / "L2_threshold" / "L3_config"
    change_type: str,             # "threshold_adjust" / "behavior_modify" / "data_correct"
    current_value: str,           # 当前值的描述（用 L0 词汇表）
    proposed_value: str,          # 建议值（用 L0 词汇表）
    rationale: str,               # 理由（用 L0 词汇表）
    confidence: float,            # [0.0, 1.0] 反馈控制器对该提案的自信度
  }],
  supporting_evidence: str,       # 来自 Trace 的证据摘要（L0 词汇表内描述）
  conflicts_with: list[str],      # 与此提案冲突的其他活跃提案
  status: str,                    # "pending" / "in_review" / "accepted" / "rejected"
  timestamp: float,
}
```

### 3.1 提案的验证管道

```
每个 RevisionProposal 在提交前通过验证管道：
  
  1. 词汇表检查
     proposed_changes[].target 和 proposed_value 中的所有术语
     必须属于 _global_registry/GLOBAL_SEMANTIC_REGISTRY.md 的注册表
  
  2. 语义范围检查
     提议修改的 target 必须与 proposal 的 source 在同一层或上层
     L3 不能提议修改 L1 的 reducer 实现细节
  
  3. 一致性检查
     提案不违反 L0 任何护栏（01_layer_invariance_axioms.md 的 3 条）
     提案不违反 P1 > P2 > P3 优先级
  
  4. 影响评估
     提案对系统稳态的影响应在可控范围内
     影响评估不涉及数值计算，只在 L0 词汇表层面描述
```

### 3.2 提案的知识沉淀

```
通过 Proposal Validation Pipeline 的提案：
  1. 写入 Block Store（label = "archival"，标记为 proposal block）
  2. 等待下一次迭代的 COGNIZE 步读取
  3. 如果连续 3 轮迭代后提案未被任何 DECIDE 采用 → 自动过期
  
  人工介入的唯一途径：
  如果 L3 标记了 proposal.status = "human_review_required"（通常当
  confidence < 0.5 且涉及 L0 词汇表边界调整时）
```

## 四、反馈控制器的冷隔离

```
反馈控制器强制执行冷隔离：
  - 不提供对 State 的写访问
  - 不提供对 L1 reducer 状态的写访问
  - 不提供对 L2 断言阈值的写访问（只读 degradation history）
  - 不修改任何正在运行的 Trace
  
  反馈控制器的输出只通过 Block Store（proposal blocks）传递给下一轮
```

## 五、不在本文件范围内

| 概念 | 所属位置 |
|------|---------|
| Proposal 的人工审批界面 | L3 实现（Web UI 或外部工具） |
| 提案过期的时间窗口具体值 | L3 配置 |
| proposal block 的具体存储字段 | L1 05_memory_lifecycle archival |
| _global_registry 的登记更新流程 | _global_registry/GLOBAL_SEMANTIC_REGISTRY.md |
