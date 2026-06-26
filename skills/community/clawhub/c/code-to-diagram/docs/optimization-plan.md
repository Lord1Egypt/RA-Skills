# code-to-diagram 优化方案

> 参考项目：[fireworks-tech-graph](https://github.com/yizhiyanhua-ai/fireworks-tech-graph)

## 当前项目 vs fireworks-tech-graph 对比

| 维度 | code-to-diagram (当前) | fireworks-tech-graph (参考) |
|------|----------------------|---------------------------|
| 渲染引擎 | Mermaid CLI (mmdc) | 纯 SVG 内联生成 |
| 视觉风格 | 1 种（暗色主题） | 7 种（Flat Icon / Blueprint / Glassmorphism 等） |
| 图表类型 | Mermaid 支持的标准类型 | 14+ 种，含完整 UML |
| 领域知识 | 无内置模式 | AI/Agent 领域模式（RAG、Multi-Agent 等） |
| 图形语义 | 无 | 形状语义（六边形=Agent，圆柱=向量库等） |
| 箭头语义 | 无 | 颜色/虚线编码含义 |
| 产品图标 | 无 | 40+ 品牌图标 |
| 输出格式 | .mmd + .md + .png | .svg + .png |
| 测试 | 无 | 回归测试 fixtures |
| 依赖 | 需要 mmdc (Puppeteer/Chrome) | 需要 librsvg |

## 可融合的优化方向

### 1. 多风格系统（最高价值）

当前只有一种暗色主题。可以引入风格选择机制：

- **Dark Terminal** — 适合 GitHub README（当前已有类似风格）
- **Flat Icon** — 白底，适合文档/博客/演示文稿
- **Blueprint** — 蓝底网格线，适合技术架构文档
- **Notion Clean** — 极简白底，适合 Notion 嵌入
- **Glassmorphism** — 毛玻璃效果，适合现代感展示

通过 `--theme` 参数扩展，Claude 可根据用户场景自动选择风格。

### 2. AI/Agent 领域模式内置

fireworks-tech-graph 内置了大量 AI 系统模式，这对 Claude Code 用户非常有价值：

- **RAG Pipeline** — Query → Embed → VectorSearch → Retrieve → LLM
- **Agentic RAG** — 加入 Agent 循环 + 工具调用
- **Multi-Agent** — Orchestrator → SubAgent×N → Aggregator
- **Memory Architecture** — Sensory → Working → Episodic → Semantic → Procedural
- **Tool Call Flow** — LLM → Tool Selector → Execution → Parser → LLM

可以在 SKILL.md 中加入这些模式的 Mermaid 模板，让 Claude 生成图表时有参考蓝本。

### 3. 语义图形体系

引入形状与含义的对应关系：

- **LLM/模型** → 双边框圆角矩形
- **Agent/编排器** → 六边形
- **向量数据库** → 圆柱体
- **工具/函数** → 带齿轮的矩形
- **决策点** → 菱形
- **用户** → 圆形

这让生成的图表具有一致的视觉语言，不同图表之间可以互相对照。

### 4. 箭头语义系统

为不同类型的数据流使用不同的线条样式：

- **主数据流** → 2px 实线
- **内存写入** → 虚线
- **异步/事件** → 点线
- **反馈/循环** → 曲线

Mermaid 支持 `-.->` / `==>` / `-->` 等箭头样式，可以直接映射。

### 5. 产品图标支持

fireworks-tech-graph 内置 40+ 品牌图标（OpenAI、Anthropic、LangChain、Pinecone、AWS 等）。虽然 Mermaid 原生不支持图标，但可以：

- 在 Mermaid 节点标签中使用 emoji 或 Unicode 符号作为简化替代
- 或者考虑混合方案：关键架构图用纯 SVG 生成（借鉴 fireworks-tech-graph 的方式），普通流程图继续用 Mermaid

### 6. 双引擎方案（进阶）

保留 Mermaid 作为通用引擎，同时引入纯 SVG 生成能力：

- **Mermaid 引擎** — 适合流程图、时序图、状态图等标准图表（快速、简单）
- **SVG 引擎** — 适合架构图、AI 系统图等需要精细控制的图表（精美、可定制）

Claude 根据图表类型自动选择引擎。

### 7. 测试与质量保障

- 添加 regression fixtures（参考 fireworks-tech-graph 的 `fixtures/` 目录）
- 添加 SVG 验证脚本
- 每种风格/类型组合都有基准输出

### 8. 轻量化依赖

fireworks-tech-graph 用 `rsvg-convert`（librsvg）替代 Puppeteer/Chrome，这明显更轻量：

- mmdc 需要 Puppeteer → 需要 Chrome → 几百 MB
- rsvg-convert 只需要 librsvg → 几 MB

如果引入 SVG 引擎，可以用 rsvg-convert 做 PNG 导出，大幅降低安装成本。

## 建议优先级

| 优先级 | 优化项 | 理由 |
|--------|--------|------|
| P0 | 多风格系统 | 用户场景差异大，一种风格无法覆盖 |
| P0 | AI/Agent 领域模式 | 目标用户群（Claude Code 用户）的核心需求 |
| P1 | 语义图形+箭头体系 | 提升图表专业度和一致性 |
| P1 | 纯 SVG 引擎（双引擎） | 摆脱 Mermaid 限制，支持精细定制 |
| P2 | 产品图标库 | 架构图的视觉识别度 |
| P2 | 测试 fixtures | 保障质量稳定 |
| P3 | rsvg-convert 替代 | 减少依赖体积 |
