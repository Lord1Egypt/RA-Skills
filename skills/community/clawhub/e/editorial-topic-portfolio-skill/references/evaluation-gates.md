# Evaluation Gates

## Gate order

硬门禁优先于评分。任何 BLOCK 不得由其他维度高分抵消。

### G0 Input

检查标题、日期、主题类型、核心假设、来源、状态和关联内容。缺失字段标记 `NEEDS_INPUT`。

### G1 Fact and status

区分讨论、草案、通过、生效、执行案例；区分新闻发布、Preview、GA、roadmap；区分融资额、估值、累计融资和交易对价。

结果：`PASS` / `BLOCK_FACT` / `HOLD_EVIDENCE`。

### G2 Timeliness

- 事件型：24—72 小时窗口，过期后必须有新的判断增量。
- 政策型：写作前重核状态，不能把讨论写成执行。
- 趋势型：至少跨时间验证，不用单日平台数据推导全球趋势。
- 框架型：时效低，但要有案例和反方。
- 观察型：必须有触发条件和复核日期。

结果：`PASS` / `BLOCK_STALE` / `HOLD_TRIGGER`。

### G3 Originality

分别搜索中文、英文的主题、同义判断、分析框架、标志性表达、反方和历史反例。

结果：

- `PASS_INCREMENT`：有明确新框架、新证据或新连接。
- `MERGE_COVERED`：适合并入已有文章。
- `BLOCK_SATURATED`：核心论点和结构均已充分覆盖。

### G4 Argument capacity

判断一条选题是否能支撑长文：核心判断、证据链、反方、边界和足够材料是否同时存在。

结果：`LONGFORM` / `SHORT_NOTE` / `MERGE` / `BLOCK_THIN`。

### G5 Position and confidentiality

检查 AI 主线、研究者姿态、合集定位、个人内容边界、公司资料和投资敏感信息。

结果：`PASS` / `BLOCK_BOUNDARY` / `PRIVATE_ONLY`。

## Gate output

每条选题必须输出：

```yaml
gates:
  G0: PASS
  G1: PASS
  G2: PASS
  G3: PASS_INCREMENT
  G4: LONGFORM
  G5: PASS
final_gate: PASS | HOLD | MERGE | BLOCK
block_reason: ""
required_evidence: []
trigger_condition: ""
recheck_date: ""
```
