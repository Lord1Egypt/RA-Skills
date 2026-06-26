---
name: exam-rescue-html
description: >
  读取 knowledge_map.json，生成三分区考前抢救清单 HTML：
  核心公式速记 / 高频考点清单 / 高频错点清单，以卡片形式呈现，支持打印。
  全程零等待，自动完成内容生成、模板填充、文件写入。
license: MIT
---

# ⚡️ 静默执行协议

**[SYSTEM CRITICAL]**

1. **Do not ask for confirmation to proceed.**
2. **全流程一次完成。** 生成三类卡片内容 → 写 JSON → 填模板 → 写 HTML → 引导。
3. **不向用户输出中间生成过程。** 不输出"正在处理第X个考点…"之类提示。
4. **All errors are silent fallback.** 遇到问题静默处理，不暴露给用户。

---

# Skill：exam-rescue-html

## 1. 触发条件

- **自动触发**：exam-question-generator 完成后，用户说「继续」
- **用户触发**：用户说「生成抢救清单」或「最后冲刺」或「重新生成」

---

## 2. 执行流程

```
Step 1   确认 .exam-session/knowledge_map.json 存在且有效
Step 2   读取 {baseDir}/references/content-rules.md（三类卡片生成规则）

Step 3   生成「核心公式速记」（formula_cards）：
           从 knowledge_map.points 中找含公式/定理/法则/定律的考点
           调用 knowledge-base 技能的 note_retrieve 接口检索原文
           为每条生成：name + formula + condition（可选）+ memory_hook（可选）

Step 4   生成「高频考点清单」（hotspot_cards）：
           筛选 importance ≥ 0.75 的考点，按 importance 降序，最多 20 个
           调用 knowledge-base 技能的 note_retrieve 接口检索原文
           为每条生成：name + core_note（≤2句话）

Step 5   生成「高频错点清单」（mistake_cards）：
           取 is_weak_point = true 的考点，补充知识库返回含"误区/注意/陷阱"的考点
           调用 knowledge-base 技能的 note_retrieve 接口检索原文
           为每条生成：name + wrong（❌开头）+ right（✅开头）+ tip（可选）

Step 6   写入 .exam-session/rescue_notes.json（格式见"输出格式"）
Step 7   读取 {baseDir}/assets/template.html
Step 8   为三类卡片各自生成 HTML 片段（格式见"模板填充规范"）
Step 9   将 template.html 中所有 {{占位符}} 替换为实际值，得到完整 HTML
Step 10  将完整 HTML 字符串写入 exam-rescue-YYYYMMDD.html（写到工作区根目录）
Step 11  发送引导消息
```

---

## 3. 输出格式

写入 `.exam-session/rescue_notes.json`：

```json
{
  "rescue": {
    "exam_type": "string",
    "exam_date": "YYYY-MM-DD",
    "days_remaining": 0,
    "target_score": "string",
    "generated_at": "YYYY-MM-DD",
    "formula_count": 0,
    "hotspot_count": 0,
    "mistake_count": 0,
    "formula_cards": [
      {
        "id": "f_001",
        "name": "公式/定理名",
        "formula": "公式内容（数学用 $LaTeX$，其他学科用文字）",
        "condition": "适用条件 | null",
        "memory_hook": "口诀 | null"
      }
    ],
    "hotspot_cards": [
      {
        "id": "h_001",
        "name": "考点名",
        "importance": 0.92,
        "is_weak_point": false,
        "core_note": "≤2句核心要点"
      }
    ],
    "mistake_cards": [
      {
        "id": "m_001",
        "name": "错点名称",
        "wrong": "❌ 常见错误理解",
        "right": "✅ 正确做法",
        "tip": "辨别提示 | null"
      }
    ]
  }
}
```

---

## 4. 模板填充规范

**输出路径**：`exam-rescue-YYYYMMDD.html`（工作区根目录）

**模板占位符**：

| 占位符 | 取值 |
|--------|-----|
| `{{exam_type}}` | rescue.exam_type |
| `{{days_remaining}}` | rescue.days_remaining |
| `{{target_score}}` | rescue.target_score |
| `{{formula_count}}` | rescue.formula_count |
| `{{hotspot_count}}` | rescue.hotspot_count |
| `{{mistake_count}}` | rescue.mistake_count |
| `{{formula_cards_html}}` | 所有公式卡片 HTML 拼接 |
| `{{hotspot_cards_html}}` | 所有考点卡片 HTML 拼接 |
| `{{mistake_cards_html}}` | 所有错点卡片 HTML 拼接 |

**HTML 片段格式**：

```html
<!-- 公式卡片 -->
<div class="formula-card">
  <div class="formula-name">{name}</div>
  <div class="formula-body">{formula}</div>
  <!-- condition 不为 null 时输出 -->
  <div class="formula-condition">适用：{condition}</div>
  <!-- memory_hook 不为 null 时输出 -->
  <span class="formula-hook">🔑 {memory_hook}</span>
</div>

<!-- 考点卡片（importance≥0.8→imp-dot high；0.6-0.79→mid；<0.6→low） -->
<!-- is_weak_point=true 时加 class="hotspot-card is-weak" -->
<div class="hotspot-card is-weak">
  <div class="hotspot-header">
    <span class="hotspot-name">{name}</span>
    <span class="imp-dot high"></span>
    <!-- is_weak_point=true 时才输出 weak-tag -->
    <span class="weak-tag">⚠️ 薄弱</span>
  </div>
  <div class="hotspot-note">{core_note}</div>
</div>

<!-- 错点卡片 -->
<div class="mistake-card">
  <div class="mistake-name">{name}</div>
  <div class="mistake-wrong">{wrong}</div>
  <div class="mistake-right">{right}</div>
  <!-- tip 不为 null 时输出 -->
  <div class="mistake-tip">💡 {tip}</div>
</div>
```

**分区隐藏规则**：某类卡片数量为 0 时，在 HTML 中完整省略该 `<div class="section">` 块（不输出空分区）。

---

## 5. 引导消息

写入 HTML 成功后立即发送：

```
你的考前抢救清单已生成 ✅

📐 核心公式速记 {formula_count} 条
🎯 高频考点清单 {hotspot_count} 个
⚠️ 高频错点清单 {mistake_count} 个

右上角有打印按钮，考前1小时翻看效果最佳。

接下来：
• 说「重新生成」→ 重新生成抢救清单
• 说「重新出题」→ 回到模拟题
```

---

## 6. 错误处理

| 场景 | 处理 |
|------|------|
| knowledge_map.json 不存在 | 提示"请先运行考前冲刺分析"，不继续 |
| 筛选后考点数 < 5 | 触发降级条件，降至 importance ≥ 0.6 |
| 某类卡片数量为 0 | 省略该分区，其余正常生成 |
| 某考点知识库无内容返回 | 仅凭 point.name 生成，继续 |
| rescue_notes.json 写入失败 | 存入会话上下文，继续执行 Step 7-11 |
| template.html 读取失败 | 终止并提示"skill 文件缺失，请检查安装" |

---

## 7. Anti-Patterns（严禁）

```
❌ 生成过程中询问"要包含哪些考点？"
❌ 将清单内容以 Markdown 文字直接输出给用户——必须按模板填充规范生成 HTML
❌ 输出 .md 文件作为产物，最终产物必须是 exam-rescue-YYYYMMDD.html（根目录）
❌ 不读取 assets/template.html 直接自行构造 HTML 结构——必须基于 template.html 填充占位符
❌ 将引导消息嵌入 HTML 文件——引导消息只能在聊天对话中以纯文本发送
❌ 向用户展示 rescue_notes.json 原始内容
❌ 某类卡片为空时输出空白分区——直接省略该 section 块
❌ wrong / right 字段写成解释而非对比——必须形成"错误理解 vs 正确做法"的直接对比
```

---

## 8. 用户操作响应

| 用户说 | 处理 |
|--------|------|
| 「重新生成」 | 重新执行 Step 3-11，覆盖旧文件 |
| 「重新出题」 | 触发 exam-question-generator |
| 其他 | 重新展示引导消息选项 |

---

## 9. 验证矩阵

| 场景 | 预期行为 | 禁止行为 |
|------|---------|---------|
| 正常流程 | 三分区卡片→JSON→HTML→引导 | 中间确认 |
| 无公式类考点（纯文科） | 省略公式分区，其余正常 | 输出空公式分区 |
| 无薄弱点 | 省略错点分区或仅用RAG线索补充 | 强行输出空分区 |
| 考点数 < 5 | 自动降级至 importance ≥ 0.6 | 提示用户"考点不足" |
| 知识库某考点无返回 | 仅凭考点名生成，继续其余 | 跳过或报错 |
| 用户说"重新生成" | 覆盖旧文件，重新执行 | 询问是否确认 |
