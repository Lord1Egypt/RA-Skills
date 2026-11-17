# Verification Report Template

这是一个标准的 VerificationReport 模板，由 Evidence-Verifier 使用。

---

## 基本信息

```yaml
verification_report:
  task_id: "rt001"
  verifier_role: "evidence-verifier"
  cycle_number: 1  # 第几轮验证
```

---

## 判决（必填）

```yaml
  verdict: "pass"  # pass | fail | hold

  # pass: 证据充分、来源可信、符合质量门禁
  # fail: 证据不足、来源可疑、违反质量门禁，需要 retry
  # hold: 证据有冲突、需要补充来源、需要人工判断
```

---

## 验证维度（必填）

```yaml
  verified_dimensions:

    # 来源可靠性
    source_reliability:
      status: "pass"  # pass | fail | hold
      note: "3 个独立来源，符合门禁要求"
      score: 8.5  # 0-10 分，可选

    # 时效性
    recency:
      status: "pass"
      note: "所有证据均为 2024 年"
      oldest_evidence_date: "2024-01-15"

    # 完整性
    completeness:
      status: "fail"
      note: "仅覆盖 Web 框架和 WASM，缺少嵌入式、CLI 工具、数据处理"
      coverage_percentage: 40  # 0-100%

    # 独立性
    independence:
      status: "hold"
      note: "发现 2 条证据追溯到同一来源，需 Conflict Arbiter 介入"
      independent_sources_count: 2

    # 佐证性
    corroboration:
      status: "pass"
      note: "关键主张有 2+ 独立来源佐证"
```

---

## 证据分类

```yaml
  # 确认有效的证据 ID
  confirmed_evidence_ids:
    - "e101"
    - "e103"
    - "e105"

  # 拒绝的证据 ID（需说明原因）
  rejected_evidence_ids: []

  # 标记需进一步验证的证据 ID
  flagged_evidence_ids:
    - "e102"  # 来源可靠性存疑
    - "e104"  # 与其他证据冲突
```

---

## 证据缺口

```yaml
  evidence_gaps:
    - "企业采用数据"
    - "嵌入式领域深度分析"
    - "CLI 工具生态"
    - "数据处理框架"
```

---

## 冲突汇总（如果有冲突）

```yaml
  conflict_summary:
    conflicts:
      - conflict_id: "c001"
        severity: "medium"  # low | medium | high | critical
        auto_resolvable: false
        reason: "需要更多独立来源验证 Rocket vs Actix-web 的流行度"

    total_conflicts: 1
    auto_resolvable_count: 0
```

---

## 返工指导（verdict = fail 时必填）

```yaml
  retry_patch:
    priority_tasks:
      - "补充嵌入式领域证据"
      - "查找企业采用案例"
      - "验证 Rocket vs Actix-web 的独立评测"

    search_hints:
      - "搜索 'Rust embedded ecosystem 2024'"
      - "搜索 'Rust enterprise adoption case study'"
      - "搜索 'Actix-web vs Rocket benchmark 2024'"

    focus_areas:
      - "嵌入式领域"
      - "企业采用"
      - "CLI 工具生态"

    avoid:
      - "不要再引用社交媒体作为唯一来源"
      - "不要使用 2023 年之前的数据"
```

---

## 置信度影响

```yaml
  confidence_impact: "从 medium 降至 low（因完整性不足）"
```

---

## 推荐行动

```yaml
  recommendation: "需补充 3 个领域的证据后重新验证"
```

---

## 验证证据（可选）

```yaml
  verification_evidence:
    - dimension: "source_reliability"
      evidence: "检查了 3 个来源的域名权威性和发布记录"
      reference: "source-strategy.md"

    - dimension: "independence"
      evidence: "追溯到 e102 和 e104 来源于同一篇博客的转载"
      reference: "upstream_source_id 字段"
```

---

## 元数据

```yaml
  metadata:
    verified_at: "2025-06-14T11:30:00Z"
    verification_duration_ms: 45000  # 验证耗时（毫秒）
```

---

## 常见判决模式

### 模式 1：Pass（验证通过）

```yaml
verification_report:
  verdict: "pass"

  verified_dimensions:
    source_reliability: {status: "pass", note: "3 个独立权威来源"}
    recency: {status: "pass", note: "所有证据为近 6 个月"}
    completeness: {status: "pass", note: "覆盖所有要求的维度"}
    independence: {status: "pass", note: "来源独立性确认"}

  confirmed_evidence_ids: ["e101", "e102", "e103", "e104", "e105"]
  evidence_gaps: []

  confidence_impact: "保持 high"
  recommendation: "证据充分，可进入合并阶段"
```

### 模式 2：Fail（需返工）

```yaml
verification_report:
  verdict: "fail"

  verified_dimensions:
    source_reliability: {status: "fail", note: "仅有社交媒体来源"}
    recency: {status: "pass"}
    completeness: {status: "fail", note: "仅覆盖 30% 的要求维度"}

  confirmed_evidence_ids: []
  rejected_evidence_ids: ["e101", "e102"]

  evidence_gaps:
    - "官方文档证据"
    - "权威媒体报道"
    - "技术博客深度分析"

  retry_patch:
    priority_tasks:
      - "查找官方文档"
      - "搜索权威媒体报道"
    search_hints:
      - "搜索 '[产品名] official documentation'"
      - "搜索 '[产品名] TechCrunch | The Verge'"

  confidence_impact: "从 medium 降至 very_low"
  recommendation: "需重新收集证据，避免使用社交媒体作为主要来源"
```

### 模式 3：Hold（需冲突解决或补充信息）

```yaml
verification_report:
  verdict: "hold"

  verified_dimensions:
    source_reliability: {status: "pass"}
    recency: {status: "pass"}
    completeness: {status: "pass"}
    independence: {status: "hold", note: "发现证据冲突"}

  confirmed_evidence_ids: ["e101", "e103"]
  flagged_evidence_ids: ["e102", "e104"]

  conflict_summary:
    conflicts:
      - conflict_id: "c001"
        severity: "high"
        auto_resolvable: false
        reason: "两个高可信来源给出矛盾结论，无法自动判断"
    total_conflicts: 1

  confidence_impact: "从 high 降至 medium"
  recommendation: "触发 Conflict Arbiter 进行冲突仲裁"
```

---

## 验证清单

### Verifier 在验证时必须检查：

- [ ] 每条证据都有 source_title、source_url、accessed_at
- [ ] 来源可靠性符合 source-strategy.md 的分级标准
- [ ] 证据时效性在 research_scope.time_range 内
- [ ] 关键主张有独立来源佐证（检查 upstream_source_id）
- [ ] 覆盖 research_envelope 中要求的所有维度
- [ ] 识别并记录所有证据冲突
- [ ] 如果 verdict = fail，必须提供 retry_patch
- [ ] 如果发现冲突，必须提供 conflict_summary

---

## 判决决策树

```
┌─ 所有维度都 pass？
│  └─ YES → verdict = "pass"
│  └─ NO → 继续
│
├─ 有冲突且无法自动解决？
│  └─ YES → verdict = "hold"
│  └─ NO → 继续
│
└─ 有维度 fail？
   └─ YES → verdict = "fail" + retry_patch
```

---

## 注意事项

1. **verdict 必须基于证据，不能基于偏好**
2. **如果 verdict = fail，retry_patch 是必须的**
3. **如果发现冲突，必须记录在 conflict_summary 中**
4. **confidence_impact 要明确说明"从什么到什么"**
5. **rejected_evidence_ids 必须说明拒绝原因**

---

## 参考文档

- [multi-agent-protocol.md](../references/multi-agent-protocol.md)
- [claim-citation-protocol.md](../references/claim-citation-protocol.md)
- [source-strategy.md](../references/source-strategy.md)
