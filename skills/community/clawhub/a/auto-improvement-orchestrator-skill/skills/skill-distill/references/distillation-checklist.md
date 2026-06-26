# 蒸馏决策与检查清单

## 蒸馏决策矩阵

| 重叠程度 | 源 skill 数量 | 建议 |
|---------|-------------|------|
| >70% 重叠 | 2 个 | 蒸馏为 1 个，删除源 |
| >70% 重叠 | 3+ 个 | 蒸馏为 1 个，删除源 |
| 30-70% 重叠 | 2 个 | 蒸馏为 1 个 + references，保留源作为补充 |
| 30-70% 重叠 | 3+ 个 | 蒸馏核心交集为 1 个，保留差异大的源 |
| <30% 重叠 | 任意 | 不蒸馏，考虑用 rules-distill 提取共性到 rules |

## 内容分层策略

### SKILL.md body 应包含

- 流程/workflow（用户每次执行都需要的步骤）
- 核心规则（高频应用的约束，如 Tier 1 模式列表）
- 快速参考表（最常查的决策表）
- example/anti-example（最典型的 1-2 对）
- 评分/质量标准（如果有）

### references/ 应包含

- 完整规则目录（所有模式的详细说明和示例）
- 场景特定指南（如中文写作特有模式、学术写作规则）
- 对比示例集（多组 before/after）
- 来源标注和学术引用

### 丢弃标准

- AI 模型已知的通用知识（如"用主动语态"不需要解释什么是主动语态）
- 纯装饰性内容（如 emoji 指南、格式美化建议）
- 和蒸馏目标无关的内容（如 slopbuster 的 code 和 academic 模式，对 text-only 蒸馏无用）

## 来源追溯模板

在蒸馏版 SKILL.md 的开头标注：

```markdown
蒸馏自 `source-A`、source-B、source-C 的核心规则。
```

在 references/ 文件中标注每个 section 的来源：

```markdown
> 来源：source-A (writing-patterns.md) + source-B (rules/text-content.md)。
```

## 蒸馏后检查清单

- [ ] SKILL.md body ≤ 500 行
- [ ] 每个源 skill 的独特贡献有对应
- [ ] example/anti-example 成对出现
- [ ] triggers 不和其他 skill 冲突
- [ ] frontmatter description 包含"蒸馏自"来源标注
- [ ] learner 评分 accuracy ≥ 0.80
- [ ] 用户确认了冲突解决方案
- [ ] 源 skill 的处理方式已决定（保留/删除/降级）
