# 别瞎说（BieXiaShuo）Skill 设计文档

## 1. Skill 基本信息

| 字段 | 值 |
|------|-----|
| 名称 | `biexishuo` |
| 描述 | 验证AI回答是否正确，基于多源交叉验证 |
| 触发词 | `/verify`、`/别瞎说`、`验证回答` |
| 参数 | `question`（必填）、`answer`（必填）、`reference`（可选） |

## 2. 目录结构

```
biexishuo/
├── SKILL.md          # Skill主文件（触发入口）
├── src/
│   ├── decompose.py  # 原子事实分解
│   ├── verify.py     # 交叉验证逻辑
│   └── score.py      # 综合评分
├── prompts/
│   ├── decompose.txt # 原子事实分解prompt
│   ├── verify.txt    # 单事实验证prompt
│   └── consistency.txt # 一致性检测prompt
└── tests/
    └── test_cases.json # 测试用例
```

## 3. 执行流程

```
用户输入 /verify
   │
   ├── 参数解析：question + answer + reference
   │
   ▼
┌──────────────────────────────────────┐
│ Step 1: 获取多源参考答案              │
│ 调用多个AI模型询问相同question         │
│ 得到 answers = [ans1, ans2, ans3]   │
└──────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────┐
│ Step 2: 原子事实分解                   │
│ 将 answer 分解为原子事实列表           │
│ facts = [fact1, fact2, ...]          │
└──────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────┐
│ Step 3: 逐事实验证                    │
│ 对每个fact，用多源答案交叉验证         │
│ 得到每个fact的verdict                 │
└──────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────┐
│ Step 4: 内部一致性检测                │
│ 检查answer自身是否自相矛盾            │
└──────────────────────────────────────┘
   │
   ▼
┌──────────────────────────────────────┐
│ Step 5: 综合评分                      │
│ 基于各fact的verdict计算总分          │
│ 输出最终报告                          │
└──────────────────────────────────────┘
```

## 4. Prompt 设计

### 4.1 原子事实分解 Prompt

```
你是一个事实分解专家。请将以下回答分解为独立的原子事实。
每个原子事实应该是一个可以被独立验证的陈述句。

回答：
{{ANSWER}}

输出格式（JSON）：
{
  "facts": [
    {"id": 1, "text": "事实陈述1"},
    {"id": 2, "text": "事实陈述2"},
    ...
  ]
}

规则：
1. 每个fact必须包含完整的主体、谓词和客体
2. 数字、日期、名称必须精确保留
3. 如果无法分解，返回原回答作为一个fact
```

### 4.2 单事实验证 Prompt

```
你是一个事实核查员。请判断待验证事实是否正确的。

参考来源：
{{REFERENCES}}

待验证事实：
{{FACT}}

请分析并输出JSON：
{
  "verdict": "true|false|uncertain",
  "confidence": 0.0-1.0,
  "reason": "判断理由"
}

规则：
- true：事实与参考来源一致
- false：事实与参考来源矛盾
- uncertain：无法从参考来源判断
```

### 4.3 一致性检测 Prompt

```
请检查以下回答是否存在自相矛盾的地方。

回答：
{{ANSWER}}

输出JSON：
{
  "consistent": true|false,
  "contradictions": [
    {"location": "位置描述", "description": "矛盾描述"}
  ]
}
```

## 5. 输出格式

```json
{
  "verdict": "partial",
  "score": 65,
  "summary": "回答部分正确，3个事实正确，2个事实错误，1个无法验证",
  "details": {
    "facts": [
      {"id": 1, "text": "...", "verdict": "true", "confidence": 0.95, "reason": "..."},
      {"id": 2, "text": "...", "verdict": "false", "confidence": 0.87, "reason": "..."}
    ],
    "consistency": {"consistent": true, "contradictions": []},
    "sources": ["gpt-4o", "claude-3.5", "gemini-2.0"]
  }
}
```

格式化的展示（给用户看的）：

```
🔍 验证结果：部分正确（65分）

✅ 正确的事实：
  • 长城汽车成立于1984年（置信度：95%）
  • 魏建军是现任董事长（置信度：92%）

❌ 错误的事实：
  • 长城汽车2023年销量200万辆（实际约123万辆，置信度：87%）

⚠️ 无法验证：
  • 魏建军持有公司45%股份（各来源未提及具体比例）

📊 一致性检测：通过（回答内部无矛盾）

📚 参考来源：GPT-4o、Claude 3.5、Gemini 2.0
```

## 6. 多源AI调用策略

方案A下，Skill需要调用多个AI模型获取参考答案。有两种实现方式：

### 方式一：通过WorkBuddy的LLM能力（推荐）

直接在Skill的python代码中，通过HTTP请求调用不同AI的API：
- OpenAI API（GPT）
- Anthropic API（Claude）
- Google API（Gemini）

需要配置各API Key（通过Skill的environment variables）

### 方式二：通过其他Skill

如果有封装好的AI调用Skill，可以依赖调用。但目前看起来没有。

## 7. 关键设计决策

| 决策点 | 选择 | 理由 |
|--------|------|------|
| 原子事实分解 | Prompt工程 | 不依赖FActScore，更轻量 |
| 事实验证 | 多源交叉 | 不依赖单一知识库 |
| 评分算法 | 加权平均 | 正确事实占比 × 置信度 |
| 参考来源 | 多AI答案 | 避免wiki爬虫的复杂性 |

## 8. MVP开发优先级

- [x] Task 1：环境检查
- [x] Task 2：开源调研
- [x] Task 3：需求与设计（本文档）
- [ ] Task 4：实现原子事实分解
- [ ] Task 5：实现多源答案获取
- [ ] Task 6：实现验证核心逻辑
- [ ] Task 7：编写SKILL.md与测试

---

_创建时间：2026-05-09_
