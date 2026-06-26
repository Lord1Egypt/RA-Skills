# 定级报告标准模板

## 模式A：简历审计报告（仅简历）

```markdown
# AI人才简历审计报告

## 基本信息
- 评估时间: {timestamp}
- 数据来源: {file_list}
- 候选人编号: {candidate_id}
- 审计模式: 仅简历审计

---

## 一、简历漏洞穿透审计

### 1.1 高阶含金量审计
- 疑点数量: {count}
- 具体疑点:
  {#each audit.high_value_issues}
  - {issue_description} [风险等级: {risk_level}]
  {/each}
- 审计结论: {conclusion}

### 1.2 高势能低细节断层
- 断层数量: {count}
- 具体断层:
  {#each audit.detail_gaps}
  - **段落**: {paragraph}
  - **问题**: {gap_description}
  - **建议追问**: {suggested_question}
  {/each}

### 1.3 因果链断裂检测
- 断裂数量: {count}
- 具体断裂:
  {#each audit.causality_gaps}
  - **声称**: {claim}
  - **缺失**: {missing_link}
  {/each}

### 1.4 AI生成痕迹识别
- 痕迹数量: {count}
- 具体痕迹:
  {#each audit.ai_patterns}
  - {pattern_type}: {evidence}
  {/each}

### 1.5 逻辑一致性校验
- 不一致数量: {count}
- 具体问题:
  {#each audit.consistency_issues}
  - {issue_description}
  {/each}

---

## 二、综合审计结论

| 指标 | 结果 |
|------|------|
| 高阶含金量 | {status} |
| 细节断层 | {status} |
| 因果链 | {status} |
| AI痕迹 | {status} |
| 逻辑一致性 | {status} |
| **综合结论** | **{overall_conclusion}** |

---

## 三、定制化测谎面试题

{#each lie_detection_questions}
### {question_type}：{question_title}
{question_content}
{/each}

---

## 四、审计备注
- 审计可信度: {confidence}
- 关键风险提示: {key_risks}
- 建议后续动作: {next_steps}
```

---

## 模式B：完整定级报告（简历 + 面试记录）

```markdown
# AI人才完整定级报告

## 基本信息
- 候选人ID: {candidate_id}
- 评估时间: {timestamp}
- 数据来源: {file_list}
- 评估模式: 完整定级

---

## 一、简历审计结果

### 1.1 审计摘要
- 审计结论: {audit.conclusion}
- 高嫌疑指标: {audit.high_suspicion_count}
- 中嫌疑指标: {audit.medium_suspicion_count}

### 1.2 关键疑点
{#each audit.key_suspicions}
- [{severity}] {description}
{/each}

---

## 二、面试交叉验证

### 2.1 测谎题覆盖情况
| 测谎题 | 是否问到 | 验证结果 | 备注 |
|--------|---------|---------|------|
{#each cross_validation.items}
| {question_summary} | {asked} | {result} | {notes} |
{/each}

### 2.2 疑点处理统计
- 已确认（存疑）: {confirmed_count}
- 已排除: {excluded_count}
- 待验证: {pending_count}

---

## 三、六维度评估

| 维度 | 得分 | 评估依据 | 认知深度 |
|------|------|---------|---------|
| AI流利度 | {score} | {evidence} | {cognitive_level} |
| 人机判断力 | {score} | {evidence} | {cognitive_level} |
| 架构设计力 | {score} | {evidence} | {cognitive_level} |
| 混合编排力 | {score} | {evidence} | {cognitive_level} |
| 认知深度 | {score} | {evidence} | {cognitive_level} |
| 问题建模能力 | {score} | {evidence} | {cognitive_level} |

**能力平均分**: {average_score}

---

## 四、加权计算

| 因子 | 等级 | 系数 | 依据 |
|------|------|------|------|
| 环境复杂度 | {level} | {coefficient} | {reason} |
| 个人杠杆率 | {level} | {coefficient} | {reason} |
| 成长速度 | {level} | 调整{adjustment} | {reason} |

**计算公式**:
```
({average_score} × {env_coefficient} × {leverage_coefficient}) + {growth_adjustment} = {weighted_score}
加权后得分: {weighted_score} × 4 = {final_score}
```

---

## 五、定级结果

| 项目 | 内容 |
|------|------|
| **最终级别** | **L{level}** |
| 级别名称 | {level_name} |
| P序列参考 | {p_level} |
| 级别定义 | {level_definition} |

{#if is_potential}
### 潜力标注
- 类型: 潜力型
- 突出维度: {outstanding_dimension}
- 建议: {recommendation}
{/if}

{#if is_weakness}
### 短板标注
- 类型: 短板型
- 薄弱维度: {weak_dimension}
- 建议: {recommendation}
{/if}

{#if is_downgraded}
### 降级说明
- 原始级别: L{original_level}
- 降级原因: {downgrade_reason}
{/if}

{#if needs_confidence_note}
### 置信度说明（v3.2 一致性检验）
> 综合得分 {final_score} 属于极端区间（≥13 或 ≤7），需说明置信度：
- 评估置信度: {confidence_level}
- 关键证据来源: {evidence_sources}
- 不确定性说明: {uncertainty_notes}
- 对标参考案例: {calibration_case}（见 references/calibration-cases.md）
{/if}

{#if has_dimension_gap}
### 非均衡型标注
- 最高维度: {max_dimension} ({max_score})
- 最低维度: {min_dimension} ({min_score})
- 分差: {gap} ≥ 2，需说明: {explanation}
{/if}

---

## 六、风险提示

### 高风险项
{#each risks.high}
- {description}
{/each}

### 中风险项
{#each risks.medium}
- {description}
{/each}

### 建议验证点
{#each risks.verify}
- {action}
{/each}

---

## 七、数据质量评估

| 维度 | 评分(1-5) | 说明 |
|------|-----------|------|
| 简历完整度 | {score} | {note} |
| 面试记录质量 | {score} | {note} |
| 评估可信度 | {score} | {note} |

---

## 八、附录

### 评估配置
- 使用配置: {config_version}
- 权重设置: {weights}

### 评估时间线
- 开始时间: {start_time}
- 结束时间: {end_time}
- 总耗时: {duration}
```

---

## 模式C：面试认知复盘报告（v3.3 Pro 新增）

```markdown
# 面试认知复盘报告

## 基本信息
- 候选人ID: {candidate_id}
- 面试日期: {interview_date}
- 数据来源: {source_type}（飞书妙记转录 / 手动记录 / 面试官笔记）
- 转录质量: {transcript_quality}（高/中/低）
- 面试时长: {duration}
- 分析时间: {timestamp}

> ⚠️ 免责声明：本分析基于{source_type}文本，可能存在口语转写误差。所有矛盾和认知判断需结合面试官实际观察综合判断。

---

## 一、矛盾检测结果

| # | 矛盾类型 | 描述 | 置信度 | 建议动作 |
|---|---------|------|--------|---------|
| 1 | {type} | {description} | 高/中/低 | {action} |

### 矛盾统计
- 高置信度矛盾: {high_count}（需追问验证）
- 中置信度矛盾: {medium_count}（建议追问）
- 低置信度矛盾: {low_count}（内部参考）
- 总计: {total_count}

---

## 二、认知行为解析

| 维度 | 状态 | 证据摘要 |
|------|------|---------|
| 问题拆解 | 持续出现/偶尔出现/未观察到/反向出现 | {evidence} |
| 抽象能力 | 持续出现/偶尔出现/未观察到/反向出现 | {evidence} |
| 逻辑一致性 | 持续出现/偶尔出现/未观察到/反向出现 | {evidence} |
| 真实性纹理 | 持续出现/偶尔出现/未观察到/反向出现 | {evidence} |
| 不确定性处理 | 持续出现/偶尔出现/未观察到/反向出现 | {evidence} |
| 修正能力 | 持续出现/偶尔出现/未观察到/反向出现 | {evidence} |
| Ownership | 持续出现/偶尔出现/未观察到/反向出现 | {evidence} |
| AI协同 | 持续出现/偶尔出现/未观察到/反向出现 | {evidence} |

---

## 三、深挖追问建议

基于矛盾引擎和认知解析发现，建议以下追问：

### 追问 1：{topic}
**触发原因**: {trigger}
**问题**: "{question}"
**期望深度**: 第{level}层（{level_name}）

{#each follow_up_questions}
### 追问 {index}：{topic}
**触发原因**: {trigger}
**问题**: "{question}"
**期望深度**: 第{level}层（{level_name}）
{/each}

---

## 四、认知画像

| 维度 | 特征 | 证据 |
|------|------|------|
| 决策风格 | {style} | {evidence} |
| 思维结构 | {structure} | {evidence} |
| AI协同习惯 | {ai_pattern} | {evidence} |
| 复杂度承载 | {complexity} | {evidence} |
| Ownership | {ownership} | {evidence} |
| 风险偏好 | {risk} | {evidence} |
| 修正能力 | {correction} | {evidence} |
| 真实性风险 | {authenticity} | {evidence} |

### 画像可信度
- 数据质量: {data_quality}
- 可信度: {confidence}
- 说明: {note}

---

## 五、与定级的关联（可选）

> 认知复盘是六维度打分的辅助证据，不直接改变定级结果。

| 认知发现 | 可能影响的定级维度 | 建议 |
|---------|-------------------|------|
| {finding} | {dimension} | {recommendation} |

---

## 六、总结

**核心发现**: {key_finding}
**最大风险**: {biggest_risk}
**最大亮点**: {biggest_strength}
**建议后续动作**: {next_steps}
```