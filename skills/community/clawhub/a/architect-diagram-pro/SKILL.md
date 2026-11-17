---
name: architect-diagram-pro
version: 1.0.0
displayName: 架构图生成
description: 本地优先的架构图与结构图生成工具。当用户要求画架构图、系统图、模块图、流程图、时序图、状态机、网络拓扑图、ER图、数据流图、微服务/云原生架构图、甘特图，或提到"画个图""架构图""系统图""模块图""拓扑图""时序图""draw/diagram/flowchart/architecture"时触发。纯本地渲染，无需云端、无需 node、无需 API Key；支持自包含 HTML 与内联 SVG 双输出，内置类型边界、间距可读性与出错重试。
agent_created: true
metadata:
  category: tools
  tags:
    - architecture
    - diagram
    - visualization
    - svg
    - html
    - flowchart
---

# 架构图生成

## 概述
在本地生成架构图与结构图，纯本地、零外部依赖、数据不出本机。四层设计：**语义层**（规划画什么、为什么画）→ **护栏层**（边界与防错）→ **模板层**（暖色自包含 HTML）→ **生成层双轨**（HTML / 内联 SVG）。

## 核心强制规则（始终生效，无需读取外部文件）
以下为最低兜底规范，即使未加载 references 也必须遵守：

- **画布与布局**：SVG 宽固定 680，viewBox `0 0 680 <h>`；优先网格/列布局，列间距 ≥40，同层节点间距 ≥16，文字与边框 padding ≥12。
- **文字安全**：文字与连线净空 ≥8px；箭头端点周围 10px 半径内禁止放置文字；连线不得横穿文字。
- **箭头文字避让**：箭头连线必须避开文字；无法避开时，将连线偏移 `dy=-10` 或 `dx=10`，或在文字下方先垫一个白底矩形再写字。
- **类型边界**：支持系统/微服务/分层架构、网络拓扑、业务流程、数据流、时序、状态机、ER、类图、甘特。暂不支持统计图（饼/柱/折线）、3D/地图、思维导图、PNG/PDF 直出、反向工程（由图生成代码）。遇到不支持的类型：**先说明「不支持 + 原因 + 替代方案」，再等用户确认**，不硬画。
- **坐标先行**：生成代码前，必须先做坐标/结构规划（见工作流第 2 步 Mental Sandbox）。
- **自检与重试**：输出前逐条核对上方规则；出错按「现象 → 原因 → 修复 → 重试校验」处理，修复后必须重新自检再交付。

## 工作流（六步）

1. **澄清**（意图/类型/输出形态不清时，用 ≤3 选项提问，勿啰嗦）：
   - 输出形态：自包含 HTML ｜ 内联 SVG ｜ Mermaid 代码块？
   - 图类型：是哪一类？（有歧义时复述确认，如「你说的是业务流程图，对吗？」）
   - 范围：整体还是某模块？节点建议 ≤20，超出先提议拆分。

2. **语义规划（三不变式 + Mental Sandbox）**：
   - **解引用一切**：用户给的文件路径/专有名词，先读取并拍平为自包含语义文本，禁止「仅列词成框」。
   - **论证而非展示**：每条关系必须可复述为明确语句（如「A 依赖 B」），禁止用「元素靠得近」替代关系定义。
   - **一图一主题**：先定抽象层级（宏观/中观/微观），再定粒度；装不下必须拆分。
   - **坐标预演（必须先做）**：写代码前先用纯文本输出结构/坐标规划，例如：
     > 画布 680×420。L1 接入层(y=40)：API 网关(100,60)。L2 应用层(y=160)：订单服务(80,180)、支付服务(300,180)。L3 数据层(y=300)：主库(80,320)、缓存(300,320)。连线：网关→订单→支付；订单→主库/缓存。图例在底部。
     确认无坐标冲突、无文字压线风险后再写代码。

3. **能力边界预检**：对照 `references/capability-matrix.md`；落在 ❌ 区先说「不支持 + 原因 + 替代」再等确认。

4. **选轨道**：概览/要分享 → HTML；精细/多类型/对话直看 → 内联 SVG；进文档 → Mermaid。涉及多视图拆分时走第 5 步确认门。

5. **生成**：
   - HTML 轨道：基于 `assets/template.html` 的 CSS 类与 theme 生成单文件，零外部 CDN（仅系统字体）。
   - SVG 轨道：先 `read_me(["diagram"])` 加载设计模块（含 HTML 交互控件才追加 `"interactive"`），再 `show_widget` 传原始 SVG；用 CSS 类 + `<defs>/<use>` 复用降低 token。
   - Mermaid：输出对应语法代码块。
   - **确认门（多视图/大幅调整前阻塞）**：先输出推荐方案（拆分机制 + 各视图焦点/层级 + 理由）并等用户明确确认，未确认不落笔。优先用 **scenarios**：单数据源 + 高亮目标链路、淡化无关，优于复制多份完整图。

6. **自检与重试**：逐条核对「核心强制规则」；任一项不过先改再发。出错按四段式回复，修复后重新自检并交付。

## 输出轨道要点
- **HTML 轨道**：单个 `.html`，暖色极简（背景 #edebe1、卡片 #f5f3eb、顶部 3px 色条），hover 上浮 + 渐入，响应式 768px 以下纵向；文件名建议 `{project}-architecture.html`。
- **SVG 轨道**：`<svg>` 开头，禁 `<!DOCTYPE>/<html>/<head>/<body>`；箭头用 `<marker>`（朝右 + `orient="auto"`，`markerWidth/Height ≥ viewBox 宽高`）；中文 `font-family="sans-serif"`；复杂图拆多张 `show_widget`。

## 资源索引（按需加载）
- `references/three-invariants.md` — 三不变式与展示意图边界
- `references/capability-matrix.md` — 类型边界 ✅/❌ 与硬规则
- `references/clarification-gate.md` — 澄清三问 + 确认门 + scenarios 高亮
- `references/svg-efficient-template.md` — Token 高效 SVG 复用模板
- `references/arrow-text-clearance.md` — 文字避让（防压字）规范
- `references/architecture-layout.md` — 分层架构布局规范
- `references/diagram-types.md` — 各类型：最佳实践 → 反模式 → 骨架
- `references/html-template-guide.md` — HTML 模板使用与扩展
- `references/self-check-and-errors.md` — 渲染前自检 + 四段式出错与重试
- `references/faq.md` — 范围与异常排查

## 安全边界
- 仅读取用户显式指定的输入文件；不遍历用户目录或无关配置。
- 产物生成在用户工作区内；不要求联网鉴权或配置任何 API Key。
- 路径限制在当前工作区，超出则拒绝并说明。
