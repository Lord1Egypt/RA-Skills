# Research Envelope Template

这是一个标准的 ResearchEnvelope 模板，用于并行研究任务。

---

## 基本信息

```yaml
research_envelope:
  task_id: "rt001"
  research_question: "[具体的研究问题，例如：Rust 在 2024 年的生态成熟度如何？]"
  research_dimension: "ecosystem-mapping"  # 从 methodology atlas 选择

  # 角色分配
  researcher_role: "ecosystem-analyst"  # source-scout, timeline-analyst, competitive-analyst, user-signal-analyst, dissent-reviewer, decision-analyst
  verifier_role: "evidence-verifier"
```

---

## 输入输出

```yaml
  # 输入制品
  input_artifacts:
    - artifact_name: "research_plan.md"
      artifact_path: "research_plan.md"
      required: true

    - artifact_name: "prior_evidence_ledger.json"
      artifact_path: "evidence_ledger.json"
      required: false

  # 输出制品
  output_artifacts:
    - "ecosystem_map.md"
    - "evidence_ledger_delta.json"
```

---

## 证据质量门禁

```yaml
  evidence_quality_gates:
    - gate: "source_reliability"
      threshold: "至少 3 个独立来源"
      quantitative_threshold:
        metric: "independent_sources_count"
        value: 3

    - gate: "recency"
      threshold: "证据不超过 1 年"
      quantitative_threshold:
        metric: "max_age_months"
        value: 12

    - gate: "completeness"
      threshold: "覆盖研究对象的 5 个主要领域"
      quantitative_threshold:
        metric: "coverage_percentage"
        value: 80

    - gate: "independence"
      threshold: "来源独立性验证通过"
```

---

## 研究范围

```yaml
  research_scope:
    time_range: "2023-2024"
    geographic_scope: "全球"
    industry_focus: "系统编程、Web 后端、嵌入式"
```

---

## 依赖与循环

```yaml
  # 任务依赖（如果此任务依赖其他任务完成）
  dependency_ids: []  # 例如：["rt000_source_scout"]

  # 最大重试次数
  max_cycles: 3
```

---

## 冲突解决策略

```yaml
  conflict_resolution_policy:
    strategy: "evidence-conflict-resolution-protocol"
    auto_resolve: true
    escalate_threshold: "无法自动解决的核心冲突"
```

---

## 人工升级策略

```yaml
  human_escalation_policy:
    escalate_on:
      - "max_cycles_reached"
      - "unresolvable_conflict"
      - "insufficient_evidence"
      - "quality_gate_failed"

    escalation_message: "研究任务 rt001 需要人工判断：[具体原因]"
```

---

## 元数据

```yaml
  metadata:
    created_at: "2025-06-14T10:00:00Z"
    created_by: "lead-integrator"
    research_sprint_id: "rs001"
    priority: "high"  # critical, high, medium, low
```

---

## 常见研究维度配置

### 1. 生态地图研究（Ecosystem Mapping）

```yaml
research_dimension: "ecosystem-mapping"
researcher_role: "ecosystem-analyst"

evidence_quality_gates:
  - gate: "completeness"
    threshold: "覆盖核心组件、框架、工具、社区"
  - gate: "source_reliability"
    threshold: "至少 3 个独立来源"
  - gate: "recency"
    threshold: "最近 6 个月"
```

### 2. 时间线分析（Historical Lineage）

```yaml
research_dimension: "historical-lineage"
researcher_role: "timeline-analyst"

evidence_quality_gates:
  - gate: "source_reliability"
    threshold: "官方文档或权威媒体"
  - gate: "completeness"
    threshold: "覆盖关键里程碑"
```

### 3. 竞品分析（Competitive Analysis）

```yaml
research_dimension: "competitive-analysis"
researcher_role: "competitive-analyst"

evidence_quality_gates:
  - gate: "completeness"
    threshold: "至少对比 3 个直接竞品"
  - gate: "independence"
    threshold: "来源不能全部来自单一厂商"
```

### 4. 用户信号分析（User Signal Analysis）

```yaml
research_dimension: "user-signal-analysis"
researcher_role: "user-signal-analyst"

evidence_quality_gates:
  - gate: "source_reliability"
    threshold: "多渠道验证（Reddit + GitHub + 论坛）"
  - gate: "completeness"
    threshold: "正面和负面反馈都覆盖"
```

### 5. 反方证据（Red Team Dissent）

```yaml
research_dimension: "red-team-dissent"
researcher_role: "dissent-reviewer"

evidence_quality_gates:
  - gate: "independence"
    threshold: "独立来源，非利益相关方"
  - gate: "completeness"
    threshold: "至少找到 3 类反对证据"
```

---

## 使用示例

### 示例 1：快速产品研究

```yaml
research_envelope:
  task_id: "rt_supabase_001"
  research_question: "Supabase 是否适合作为我们的后端？"
  research_dimension: "competitive-analysis"
  researcher_role: "competitive-analyst"
  verifier_role: "evidence-verifier"

  evidence_quality_gates:
    - gate: "completeness"
      threshold: "与 Firebase、AWS Amplify 对比"
    - gate: "source_reliability"
      threshold: "至少 2 个独立评测"

  research_scope:
    time_range: "2024"
    geographic_scope: "全球"
    industry_focus: "SaaS 后端"

  max_cycles: 2
```

### 示例 2：深度公司研究

```yaml
research_envelope:
  task_id: "rt_openai_timeline"
  research_question: "OpenAI 2023-2025 年的战略转变路径"
  research_dimension: "historical-lineage"
  researcher_role: "timeline-analyst"
  verifier_role: "evidence-verifier"

  evidence_quality_gates:
    - gate: "source_reliability"
      threshold: "官方声明 + 权威媒体"
    - gate: "completeness"
      threshold: "覆盖产品、融资、组织、争议 4 个维度"

  research_scope:
    time_range: "2023-01 to 2025-06"
    geographic_scope: "全球"

  max_cycles: 3

  conflict_resolution_policy:
    auto_resolve: true
    escalate_threshold: "商业战略判断的核心冲突"
```

---

## 注意事项

1. **research_question 必须具体**：不要"研究 AI"，而是"研究 GPT-4 在代码生成任务上的表现"

2. **evidence_quality_gates 要可验证**：避免主观标准，使用可量化的门禁

3. **max_cycles 建议范围**：
   - 简单研究：1-2 cycles
   - 中等复杂度：2-3 cycles
   - 复杂研究：3-5 cycles
   - 超过 5 cycles 说明研究问题需要拆分

4. **dependency_ids 使用场景**：
   - user-signal-analyst 依赖 ecosystem-analyst（需要先知道生态结构）
   - decision-analyst 依赖所有其他 analysts（需要综合所有证据）

5. **conflict_resolution_policy**：
   - 事实类研究：auto_resolve = true
   - 战略判断类研究：auto_resolve = false，更多依赖人工

---

## 参考文档

- [multi-agent-protocol.md](../references/multi-agent-protocol.md)
- [research-methodology-atlas.md](../references/research-methodology-atlas.md)
- [conflict-resolution-report.schema.json](../references/conflict-resolution-report.schema.json)
