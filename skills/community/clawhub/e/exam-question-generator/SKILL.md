---
name: exam-question-generator
description: >
  读取 knowledge_map.json，按三套差异化规则生成模拟题（基础巩固/综合能力/冲刺模拟），
  AI 生成题目内容写入 questions.json，运行脚本渲染三 Tab 独立 HTML，
  生成后引导用户选择下一步。
license: MIT
---

# Skill：exam-question-generator

## 1. 触发条件

- **自动触发**：exam-mindmap-generator 完成后，用户说「继续」
- **用户触发**：用户说「重新出题」时，重新执行 Step 3-9

---

## 2. 执行流程

```
Step 1   确认 .exam-session/knowledge_map.json 存在且有效
Step 2   读取 {baseDir}/references/question-formats.md（题型组成 + 来源策略）
Step 3   读取 {baseDir}/references/difficulty-rules.md（三套难度规则）
Step 4   调用 /knowledge-base 技能（note_retrieve）：对每个考点拉取知识库原文上下文
           查询词："{point.name} {point.evidence[0]}"（逐考点查询）
Step 5   按规格生成三套全部题目（格式见"题目生成规范"）
Step 6   写入 .exam-session/questions.json（格式见"输出格式"）
Step 7   读取 {baseDir}/assets/template.html
Step 8   为三套题目各自生成 HTML 卡片片段（格式见"模板填充规范"）
Step 9   将 template.html 中所有 {{占位符}} 替换为实际值，得到完整 HTML
Step 10  将完整 HTML 字符串写入 exam-questions-YYYYMMDD.html（写到工作区根目录）
Step 11  发送引导消息
```

---

## 3. 题目生成规范

### 3.1 考点处理顺序

按 knowledge_map.points 的 importance 降序处理：

| importance 范围 | 出现套次 |
|----------------|---------|
| ≥ 0.8          | 套1 + 套2 + 套3 |
| 0.6 – 0.79     | 套1 + 套2 |
| < 0.6          | 仅套1 |

`is_weak_point = true` → 在套1额外增加 1 道 tf，专门考查该考点的最常见误区。

### 3.2 题目来源判断（C方案）

```
检查 point.evidence 是否含"真题"/"历年"/"模拟题"：
  是 → source_type = "adapted"：RAG 拉取原文 → 改编措辞/数据，保留核心考查点
  否 → source_type = "generated"：基于 point.name + RAG 上下文 AI 生成
```

### 3.3 难度执行

严格遵守 difficulty-rules.md：

| 套次 | 题干风格 | 干扰项设计 | 简答要求 |
|------|---------|-----------|---------|
| 套1 基础 | 直白，无歧义 | 明显错误 | 定义/列举 |
| 套2 综合 | 场景化，需应用 | 近义混淆 | 分析/比较 |
| 套3 冲刺 | 含陷阱，仿真 | 似对实错 | 跨考点综合 |

### 3.4 答案格式规范

- **mc**：answer = 单字母，如 `"B"`
- **mma**：answer = 字母连排，如 `"ACD"`（无空格无标点）
- **tf**：answer = `"正确"` 或 `"错误"`
- **sa**：answer = 分点换行文本，格式：`"1. 要点一\n2. 要点二\n3. 要点三"`

### 3.5 explanation 深度要求（对应 Q5:B）

- mc/mma：逐选项说明对错，重点解释干扰项为何错
- tf：给出完整判断逻辑链，非仅写"对/错"
- sa：列出 2–4 个关键词和给分参考点

---

## 4. 输出格式

写入 `.exam-session/questions.json`：

```json
{
  "questions": {
    "exam_type": "string",
    "exam_date": "YYYY-MM-DD",
    "days_remaining": 0,
    "target_score": "string",
    "generated_at": "YYYY-MM-DD",
    "sets": [
      {
        "set_id": "set1",
        "label": "套1 · 基础巩固",
        "difficulty": "basic",
        "total_score": 100,
        "total_questions": 20,
        "time_minutes": 60,
        "questions": [
          {
            "id": "q_s1_001",
            "type": "mc",
            "source_point_id": "kp_001",
            "source_point_name": "string",
            "source_type": "generated",
            "content": "题目内容",
            "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
            "answer": "B",
            "explanation": "逐项解析...",
            "knowledge_ref": "kp_001",
            "score": 2
          }
        ]
      },
      { "set_id": "set2", "label": "套2 · 综合能力", "difficulty": "intermediate", "total_score": 100, "total_questions": 20, "time_minutes": 90, "questions": [] },
      { "set_id": "set3", "label": "套3 · 冲刺模拟", "difficulty": "advanced",     "total_score": 100, "total_questions": 20, "time_minutes": 90, "questions": [] }
    ]
  }
}
```

**字段说明**：
- `type`："mc" | "mma" | "tf" | "sa"
- `options`：mc/mma 有值（字符串数组），tf/sa 为 null
- `answer`：见 3.4 格式规范
- `knowledge_ref`：对应 knowledge_map 中的 `point.id`

---

## 5. 模板填充规范

**输出路径**：`exam-questions-YYYYMMDD.html`（工作区根目录）

**模板占位符**：

| 占位符 | 取值 |
|--------|-----|
| `{{exam_type}}` | knowledge_map.exam_type |
| `{{days_remaining}}` | knowledge_map.days_remaining |
| `{{target_score}}` | knowledge_map.target_score |
| `{{set1_label}}` | `套1 · 基础巩固（{N}题）` |
| `{{set2_label}}` | `套2 · 综合能力（{N}题）` |
| `{{set3_label}}` | `套3 · 冲刺模拟（{N}题）` |
| `{{set1_questions}}` | 套1所有题目卡片的 HTML 拼接 |
| `{{set2_questions}}` | 套2所有题目卡片的 HTML 拼接 |
| `{{set3_questions}}` | 套3所有题目卡片的 HTML 拼接 |
| `{{set1_stats}}` | `{N}题 · 100分 · 60分钟` |
| `{{set2_stats}}` | `{N}题 · 100分 · 90分钟` |
| `{{set3_stats}}` | `{N}题 · 100分 · 90分钟` |

**题目卡片 HTML 片段格式**（每道题生成一个 `<div class="q-card">` 块，拼接后填入对应占位符）：

```html
<!-- mc / mma 题 -->
<div class="q-card">
  <div class="q-header">
    <div class="q-num">{题号}</div>
    <span class="q-badge {type}">{类型中文：单选/多选/判断/简答}</span>
    <span class="q-score">{score}分</span>
    <span class="q-point">{source_point_name}</span>
  </div>
  <div class="q-content">{content}</div>
  <div class="options">
    <div class="option">A. {选项}</div>
    <div class="option">B. {选项}</div>
    <div class="option">C. {选项}</div>
    <div class="option">D. {选项}</div>
  </div>
  <button class="toggle-btn" onclick="toggleAnswer(this)">查看答案 ▼</button>
  <div class="answer-wrap">
    <div class="answer-line">答案：<strong>{answer}</strong></div>
    <div class="explanation">{explanation}</div>
    <span class="ref-chip">考点：{source_point_name}</span>
  </div>
</div>

<!-- tf / sa 题（无 options 区块）-->
<div class="q-card">
  <div class="q-header">
    <div class="q-num">{题号}</div>
    <span class="q-badge {type}">{类型中文}</span>
    <span class="q-score">{score}分</span>
    <span class="q-point">{source_point_name}</span>
  </div>
  <div class="q-content">{content}</div>
  <button class="toggle-btn" onclick="toggleAnswer(this)">查看答案 ▼</button>
  <div class="answer-wrap">
    <div class="answer-line">答案：<strong>{answer}</strong></div>
    <div class="explanation">{explanation}</div>
    <span class="ref-chip">考点：{source_point_name}</span>
  </div>
</div>
```

---

## 6. 引导消息

写入 HTML 成功后立即发送（变量从 Step 9 实际写入数据取值）：

```
你的3套专属模拟题已生成 ✅

套1 基础巩固：{set1_count}题 · 100分 · 建议60分钟
套2 综合能力：{set2_count}题 · 100分 · 建议90分钟
套3 冲刺模拟：{set3_count}题 · 100分 · 建议90分钟

要生成考前1小时抢救清单吗？（含核心公式速记 / 高频考点 / 高频错点，支持打印）
```

---

## 7. 错误处理

| 场景 | 处理 |
|------|------|
| knowledge_map.json 不存在 | 提示"请先运行考前冲刺分析"，不继续 |
| 某考点知识库无上下文返回 | 告知用户该考点无匹配资料，仅凭考点名称生成，继续其余考点 |
| questions.json 写入失败 | 将数据存入会话上下文，继续执行 Step 7-11 |
| template.html 读取失败 | 终止并提示"skill 文件缺失，请检查安装" |

---

## 8. Anti-Patterns（严禁）

```
❌ 生成过程中输出"我正在出套1的单选题，请稍候…"
❌ 每套生成完毕后询问"是否继续生成套2？"
❌ 简答题 explanation 只写"详见教材"或"理解即可"
❌ 多选题 answer 含空格或标点（正确格式："ACD"，错误格式："A, C, D"）
❌ 向用户展示 questions.json 的原始内容
❌ 脚本报错后不处理直接崩溃，应告知用户具体失败原因
❌ 将题目内容以 Markdown 文字直接输出给用户——必须按模板填充规范生成 HTML，最终产物只有 HTML 文件
❌ 输出 .md 文件作为产物，最终产物必须是 .exam-output/exam-questions-YYYYMMDD.html
❌ 不读取 assets/template.html 直接自行构造 HTML 结构——必须基于 template.html 填充占位符
❌ 将引导消息（"下一步操作"、"接下来"等文字）嵌入 HTML 文件——引导消息只能在聊天对话中以纯文本发送
```

---

## 9. 用户操作响应

| 用户回复 | 处理 |
|---------|------|
| 「要」/「生成」/「好」/「继续」/「是」 | 触发 exam-rescue-html |
| 「不要」/「不用」/「不」 | 回复"好的，需要时随时说「生成抢救清单」" |
| 「重新出题」 | 重新执行 Step 4-10，覆盖旧文件 |
| 其他 | 重新展示引导消息 |

---

## 10. 验证矩阵

| 场景 | 预期行为 | 禁止行为 |
|------|---------|---------|
| 正常流程 | 三套各20题→JSON→HTML→引导 | 分步确认 |
| 含真题证据的考点 | source_type="adapted"，改编措辞 | 直接复制原文 |
| is_weak_point 考点 | 套1额外多一道tf | 仅按常规题数出题 |
| importance<0.6 的考点 | 仅在套1出题 | 出现在套2/套3 |
| 用户说"重新出题" | 重新执行，覆盖旧文件 | 询问是否确认 |
| 用户说"要/继续" | 触发 exam-rescue-html | 再展示题目内容 |
| 用户说"不要" | 礼貌回复，不继续 | 强行触发下一步 |
| questions.json 写入失败 | 降级存会话→继续渲染 | 报错终止 |
