# 评估规则定义

三层评估漏斗：代码校验优先，LLM 语义评估兜底。

## 层级总览

| 层级 | 执行者 | 性质 | 适用场景 |
|------|--------|------|----------|
| Tier 1 | scripts/validate_*.py | 确定性，无 LLM | 结构完整性、字段完整性、字数区间 |
| Tier 2 | scripts/validate_*.py | 确定性，无 LLM | 约束满足、关键词存在、结构硬约束 |
| Tier 3 | LLM (prompts/evaluator.md) | 语义判断 | 连贯性、专业度、幻觉检测、忠实度 |

## 执行顺序

`Tier 1 → Tier 2 → Tier 3`，前一层失败则跳过后续。

## Tier 1 规则

### validate_contract.py (Step 3)

| 检查项 | 失败描述 |
|--------|----------|
| placeholders 非空 | "未识别任何占位符" |
| id 唯一 | "占位符 id 重复: {duplicates}" |
| para_index 有效 | "para_index=X 不存在于 raw_structure" |
| table_index+row+col 有效 | "表格位置 (T,R,C) 不存在于 raw_structure" |

### validate_content.py (Step 6)

| 检查项 | 失败描述 |
|--------|----------|
| 占位符全部填充 | "占位符 {id} 未填充" |
| 字数区间 | "占位符 {id} 字数 {n} < 最小 {min}" 或 "> 最大 {max}" |
| 原文泄漏 | "占位符 {id} 内容含模板原文提示性文字" |

### validate_format.py (Step 9)

| 检查项 | 失败描述 |
|--------|----------|
| 段落数一致 | "段落数不匹配: 模板 X vs 生成 Y" |
| 表格数一致 | "表格数不匹配" |
| 表格行列数一致 | "表格 {i} 行/列数不匹配" |
| 静态文本未改动 | "静态文本被改动: 期望含 '...'，实际 '...'" |
| 样式一致 | "段落 {i} 样式不匹配" |

## Tier 2 规则

### validate_contract.py

| 检查项 | 失败描述 |
|--------|----------|
| is_placeholder 已标记 | "占位符 {id} 缺少 is_placeholder 字段" |
| is_static 已标记 | "占位符 {id} 缺少 is_static 字段" |
| 约束可追溯 | "约束关键词 [...] 未在 original_text 中出现，疑似擅自生成" |

### validate_content.py

| 检查项 | 失败描述 |
|--------|----------|
| required_keywords 存在 | "占位符 {id} 缺少关键词: [...]" |

## Tier 3 规则（LLM 评估）

由 `prompts/evaluator.md` 加载的评估角色执行，输出：

```json
{
  "passed": bool,
  "failed_checks": [{"check": "...", "fix_hint": "..."}]
}
```

### 评估维度

| 维度 | 说明 |
|------|------|
| 内容与参考资料一致 | 生成内容是否有参考资料支持 |
| 表述专业 | 措辞是否符合同类文档惯例（如申报书用"拟开展"，教案用"将引导学生"） |
| 幻觉检测 | 内容中是否有参考资料不支持的信息 |
| 语义连贯性 | 段落间、表格单元格间逻辑是否连贯 |
| 占位符原文不泄漏 | 生成内容是否混入"请填写"等指令性文字 |

## 反馈格式（统一）

```json
{
  "passed": false,
  "tier_failed": 2,
  "failed_checks": [
    {
      "check": "placeholder_p3_empty",
      "fix_hint": "占位符 p3 未填充，需依据参考资料撰写课程目标"
    }
  ]
}
```

- `passed: true` → 直接进入下一步
- `passed: false` → 宿主智能体按 `fix_hint` 修改后直接进入下一步（不重新评估）

## 单次评估原则

每个校验点只评一次。未通过则修改后直接进入下一步，不循环评估。理由：
- 避免无限循环
- 修改后的内容会进入后续校验点继续把关
- LLM 评估的成本与延迟需控制
