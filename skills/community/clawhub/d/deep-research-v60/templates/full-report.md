# {{research_domain}} 深度研究报告

> **版本**：v6.0 Universal  
> **生成时间**：{{date}}  
> **方法论**：配置驱动 + 数据源自适应 + 三层输出

---

## 方法论说明

- **检索策略**：{{search_strategy}}
- **数据来源**：{{source_breakdown}}
- **提取逻辑**：通用 Prompt + 领域配置
- **全文比例**：{{full_text_ratio}}%

---

## 已验证结论（基于全文/高完整度摘要）

{{#each verified_sections}}
### {{title}}

**来源**：{{sources}}  
**证据**：{{evidence_summary}}  
**业务意义**：{{business_implication}}

{{/each}}

---

## 待验证线索（基于摘要/低完整度来源）

{{#each pending_sections}}
### {{title}}

**来源**：{{sources}}  
**当前证据**：{{abstract_evidence}}  
**缺失指标**：{{missing_metrics}}  
**验证路径**：{{verification_path}}

{{/each}}

---

## 战略建议（分层级）

### 短期（本周）
{{#each short_term}}
- {{action}} (依据：{{source}})
{{/each}}

### 中期（本月）
{{#each mid_term}}
- {{action}} (待验证：{{metrics}})
{{/each}}

### 长期（季度+）
{{#each long_term}}
- {{action}} (需更多证据)
{{/each}}

---

## 附录：完整卡片索引

| 卡片 | 主题 | 数据级别 | 关键指标 | 链接 |
|------|------|----------|----------|------|
{{#each cards}}
| {{id}} | {{topic}} | {{data_level}} | {{key_metrics}} | [🔗]({{url}}) |
{{/each}}

---

**报告版本**：v6.0 Universal  
**溯源验证**：✅ 所有数据可溯源到卡片
