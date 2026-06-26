---
name: exam-mindmap-generator
description: >
  接收 knowledge_map.json，生成三合一静态复习计划 HTML：
  知识结构图 + 薄弱点预警 + 复习计划，以卡片形式呈现，支持打印。
  生成后主动询问用户是否生成模拟题，等待用户决策。
license: MIT
---

# ⚡️ 静默执行协议

**[SYSTEM CRITICAL]**

1. **Do not ask for confirmation to proceed.**
2. **Generate the full output in one go.** 读取数据 → 生成三类内容 → 填充模板 → 写入 HTML → 发送引导消息。
3. **All errors are silent fallback.** 遇到问题静默处理，不报告给用户。
4. **生成 HTML 后立即发送引导消息，主动询问是否生成模拟题。**

---

# ⛔ 平台执行限制（最高优先级）

天禧 Claw 平台中 Claude **没有 shell / bash / terminal 工具**，**无法执行任何系统命令**。

- ❌ `node generate.js` → 禁止尝试
- ✅ **唯一合法产物生成方式**：读取 `{baseDir}/assets/template.html` → 填充全部 `{{占位符}}` → 用文件写入工具写出 HTML

---

# Skill：exam-mindmap-generator

## 1. 触发条件

- **自动触发**：`exam-sprint-pipeline` 完成 Phase 2 后调用（无需用户开口）
- **用户触发**：用户说"重新生成"时，重新执行全部步骤

---

## 2. 执行流程

```
Step 1   确认 .exam-session/knowledge_map.json 存在且有效
Step 2   读取 {baseDir}/references/node-rules.md（三分区生成规则）
Step 3   读取 {baseDir}/references/design-spec.md（视觉规范）
Step 4   读取 {baseDir}/assets/template.html

Step 5   根据 days_remaining 判断渲染模式（urgent ≤7 / standard 8-30 / relaxed >30）

Step 6   生成「知识结构图」(echarts_tree_data)：
           按 node-rules.md 规则，将所有类别和考点构建为 ECharts 树图 JSON 对象

Step 7   生成「薄弱点预警」(weak_points_html)：
           筛选 is_weak_point = true 的考点，按 importance 降序生成 wp-item HTML

Step 8   生成「复习计划」(study_plan_html)：
           按渲染模式和 node-rules.md 阶段规则，计算日期区间，生成 plan-phase HTML

Step 9   计算统计数据：total_points、weak_points_count、total_hours、plan_phases_count

Step 10  将 template.html 中所有 {{占位符}} 替换为实际值，得到完整 HTML

Step 11  将完整 HTML 字符串写入 exam-mindmap-YYYYMMDD.html（写到工作区根目录）

Step 12  发送引导消息（见"引导消息"节）
```

---

## 3. 模板填充规范

**输出路径**：`exam-mindmap-YYYYMMDD.html`（工作区根目录）

**模板占位符**：

| 占位符 | 取值来源 |
|--------|---------|
| `{{exam_type}}` | knowledge_map.exam_type |
| `{{days_remaining}}` | knowledge_map.days_remaining |
| `{{target_score}}` | knowledge_map.target_score |
| `{{total_points}}` | 展示的考点总数 |
| `{{weak_points_count}}` | is_weak_point=true 的考点数量 |
| `{{total_hours}}` | Σ 所有展示考点的计算时长（保留一位小数） |
| `{{plan_mode}}` | "⚡ 紧急冲刺" / "📘 标准复习" / "📅 充裕备考" |
| `{{plan_phases_count}}` | 复习计划阶段数 |
| `{{echarts_tree_data}}` | ECharts 树图 JSON 对象（直接嵌入 JS） |
| `{{weak_points_html}}` | 薄弱点预警卡片 HTML 拼接 |
| `{{study_plan_html}}` | 复习计划阶段 HTML 拼接 |

**各分区 HTML 片段格式**详见 `{baseDir}/references/node-rules.md`。

---

## 4. 引导消息

写入 HTML 成功后立即发送：

```
你的复习计划已生成 ✅

🗂️ 知识结构图：{total_points} 个考点，建议总时长 {total_hours}h
⚠️ 薄弱点预警：{weak_points_count} 个需重点攻克
📅 复习计划：{plan_phases_count} 个阶段

要基于这份计划生成专属模拟题吗？（3套，含基础/综合/冲刺）
```

---

## 5. 错误处理

| 场景 | 处理 |
|------|------|
| knowledge_map.json 不存在 | 提示"请先运行考前冲刺分析"，不继续 |
| days_remaining 字段缺失 | 默认按 standard 模式处理 |
| template.html 读取失败 | 终止并提示"skill 文件缺失，请检查安装" |
| 薄弱点为 0 | 输出提示块（见 node-rules.md），不输出空分区 |

---

## 6. 用户操作响应

| 用户回复 | 处理 |
|---------|------|
| 「要」/「生成」/「好」/「继续」/「是」 | 触发 exam-question-generator |
| 「不要」/「不用」/「不」 | 回复"好的，需要时随时说「生成模拟题」" |
| 「重新生成」 | 重新执行全部步骤，覆盖旧文件 |
| 其他 | 重新展示引导消息 |

---

## 7. Anti-Patterns（严禁）

```
❌ 将复习计划内容以 Markdown 文字直接输出给用户——最终产物只有 HTML 文件
❌ 输出 .md 文件——最终产物必须是 .exam-output/exam-mindmap-YYYYMMDD.html
❌ 不读取 assets/template.html 直接自行构造 HTML 结构
❌ 将引导消息嵌入 HTML 文件——引导消息只在聊天中发送
❌ 生成 HTML 后不发引导消息、沉默等待用户先开口
❌ 用 markmap / mermaid / D3 等外部库——模板已是纯静态 HTML，无需任何外部脚本
❌ 自行尝试运行 node generate.js 或任何 shell 命令
```

---

## 8. 验证矩阵

| 场景 | 预期行为 | 禁止行为 |
|------|---------|---------|
| 标准流程 | 三分区→HTML→引导询问 | 生成完直接沉默 |
| 无薄弱点 | 薄弱点区输出"暂无标注"提示块 | 输出空白区域 |
| 紧急模式 | 仅纳入 importance ≥ 0.8，逐日计划 | 展示全量考点 |
| 用户说"重新生成" | 覆盖旧文件，重新执行 | 询问是否确认 |
| 用户说"不要模拟题" | 礼貌回复，不继续 | 强行触发下一步 |
| 用户说"要" | 立即触发 exam-question-generator | 再次确认 |
