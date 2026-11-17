# 协作工作流

## 与其他 SKILL 的详细协作流程

### 1. solution-architect → report-builder（上游→本 SKILL）

solution-architect 产出详案（30-80页 md）后，可作为 report-builder 的输入：

```
solution-architect 产出详案
    ↓
report-builder Step 1: 信息提取
    ↓
从详案中提取关键结论/数据/决策点
    ↓
report-builder Step 2-5: 分层→转译→叙事→校验
    ↓
输出高管报告
```

**调用方式：** Agent 在完成 solution-architect 任务后，自动或手动触发 report-builder。

**数据传递：** 详案的 md 文件路径作为 report-builder 的输入参数。

### 2. digital-research → report-builder

需要行业数据/竞品数据时，委托 digital-research 抓取：

```
Agent: "需要获取竞品XYZ的定价策略数据"
    ↓
digital-research: web_search + web_fetch → 结构化数据
    ↓
注入 report-builder 的信息提取层
```

**触发条件：** 报告中出现 `<!-- TODO: 待调研补充 -->` 标记时自动触发。

### 3. plantuml-generator → report-builder

需要架构图/流程图嵌入报告时：

```
Agent: "需要一张系统架构图展示三层架构"
    ↓
plantuml-generator: 生成 .puml → 渲染为 .png
    ↓
嵌入报告的"附录"部分
    ↓
markdown-to-html: 转换时包含图片引用
```

### 4. report-builder → markdown-to-html（本 SKILL → 下游）

报告定稿后，调用 markdown-to-html 生成 HTML 版本：

```
report-builder: 报告定稿（校验通过，A级）
    ↓
markdown-to-html: 转换 md → html
    ↓
输出到报告目录：01-{名称}-v{版本}.html
```

**触发条件：** validate.py 评分 A 级 + 用户确认定稿。

**执行方式：**

```bash
cd reports/{报告名称}/
python3 /path/to/markdown-to-html/scripts/markdown_to_html.py \
  01-{名称}-v{版本}.md -o 01-{名称}-v{版本}.html
```

---

## 标准化输入接口

report-builder 接收的输入格式：

### 输入类型 1：完整详案文件

```
输入：/path/to/detailed-plan.md
受众：CEO / CFO / Board / Steering Committee
决策上下文：[他们已知什么，需要做什么决策]
约束：500词上限 / 中文 / 需含财务测算
```

### 输入类型 2：结构化摘要输入

```json
{
  "title": "数字化转型方案",
  "conclusions": ["结论1", "结论2"],
  "key_findings": [
    {"finding": "发现1", "data": "支撑数据", "confidence": "HIGH"}
  ],
  "implications": [
    {"area": "收入", "impact": "影响描述"},
    {"area": "成本", "impact": "影响描述"}
  ],
  "recommendations": [
    {"action": "行动", "owner": "负责人", "timeline": "Q3 2026"}
  ],
  "risks": [{"risk": "风险", "mitigation": "缓解"}]
}
```

### 输入类型 3：对话式输入

```
Agent 与用户对话收集信息 → 结构化后进入流水线
```

---

## 输出产物清单

| 产物 | 文件 | 何时生成 |
|------|------|---------|
| 高管报告 | `01-{名称}-v{版本}.md` | init.py 或 bump.py |
| HTML 版本 | `01-{名称}-v{版本}.html` | 定稿时调用 markdown-to-html |
| 校验报告 | `01-{名称}-v{版本}-validation.json` | validate.py |
| 密度分析 | stdout（或 JSON） | density.py |
| 版本历史 | `VERSION.md` | 每次 bump.py |
| 报告索引 | `README.md` | init.py 或 bump.py |
