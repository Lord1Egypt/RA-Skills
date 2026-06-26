# Roundtable 静态介绍页设计方案

> 设计师：像素姐 🎨  
> 依据：`docs/product/static-intro-page-prd.md` v1.0  
> 交付目标：为 Vercel 静态 Landing Page 提供可开发落地的视觉、布局、交互与响应式规范。

---

## 1. 设计定位

Roundtable 的介绍页不做喧闹的 AI 营销页，而要像一个“可信的开源开发者工具入口”：第一眼清楚、第二眼专业、继续阅读时能感到它真的理解多 Agent 协作的复杂性。

核心视觉句子：

> 在深色终端般的空间里，一张有秩序的圆桌正在把分散观点收敛成可追溯决策。

### 设计关键词

- 专业：开发者工具感，强调可靠、轻量、可嵌入。
- 结构化：用圆桌、轮次、状态轨道、结论面板表达讨论协议层。
- 克制但有记忆点：沿用 Roundtable Tokyo Night 品牌色，并借鉴 Linear 式暗色精密感。
- 中英兼容：中文解释价值，英文 headline / badge / CTA 方便开源传播。

### 视觉参考转译

- Roundtable 既有品牌：Tokyo Night 蓝紫渐变、六节点圆桌、中心共识点。
- Linear / Vercel 类开发者工具：深色原生画布、细边框、低噪声卡片、代码块优先。
- 避免：大面积彩虹渐变、泛 SaaS 图标堆叠、假数据大屏、过度玻璃拟态。

---

## 2. 页面信息架构

页面采用单页 Landing Page，从“理解产品”到“确认适配”再到“立即行动”。建议模块顺序如下：

| 顺序 | 模块 | 目标 | 关键内容 |
|---|---|---|---|
| 1 | Hero | 10 秒理解 | 产品名、定位、安装命令、CTA、可信标签 |
| 2 | Pain Points | 解释为什么需要 | 多 Agent 会说话但不会开会、难复盘、难沉淀 |
| 3 | Capabilities | 证明它能做什么 | discussion lifecycle、ordered speaking、convergence tracking、meeting notes |
| 4 | Workflow | 展示讨论协议 | init → speak in turns → track → summarize → conclude |
| 5 | Code Snippet | 让开发者可行动 | `pip install agent-roundtable` 与 `from roundtable import RoundtableCore` |
| 6 | Use Cases | 自我匹配 | 产品决策、技术评审、代码 Review、需求澄清、多 Agent 工作流 |
| 7 | Channels | 生态入口 | GitHub、PyPI、Hermes Skill Hub、OpenClaw Skill Hub 状态 |
| 8 | Final CTA / Footer | 完成转化 | 再次安装、GitHub、README / Docs |

信息节奏原则：

1. 首屏不讲完整 API，只回答“这是什么、为什么值得试、怎么开始”。
2. 中段用卡片和流程图降低阅读成本，避免 PRD 式长段落。
3. 安装命令与 GitHub CTA 至少出现两次：Hero 一次，底部一次。
4. 所有未上线渠道必须有 Coming soon / Planned 状态，不使用空链接误导用户。

---

## 3. 视觉系统

### 3.1 色彩

沿用 Roundtable Tokyo Night，并稍微压低背景亮度，让首屏更像开发者工具官网。

| Token | 色值 | 用途 |
|---|---|---|
| `--rt-bg` | `#08090f` | 页面主背景，接近 Linear 式深黑 |
| `--rt-bg-soft` | `#10131d` | 次级背景、导航底 |
| `--rt-surface` | `rgba(255,255,255,0.035)` | 卡片、代码块外壳 |
| `--rt-surface-strong` | `rgba(255,255,255,0.07)` | 重点卡片、hover |
| `--rt-border` | `rgba(192,202,245,0.12)` | 默认细边框 |
| `--rt-border-strong` | `rgba(122,162,247,0.36)` | 活跃、强调边框 |
| `--rt-text` | `#f1f5ff` | 标题与主要文本 |
| `--rt-text-soft` | `#a9b1d6` | 正文、副说明 |
| `--rt-muted` | `#6f789d` | metadata、弱化文本 |
| `--rt-blue` | `#7aa2f7` | 主强调、链接、主 CTA |
| `--rt-purple` | `#bb9af7` | 品牌渐变、共识中心 |
| `--rt-cyan` | `#7dcfff` | 技术标签、信息提示 |
| `--rt-green` | `#9ece6a` | Available、consensus |
| `--rt-yellow` | `#e0af68` | Planned / in progress |
| `--rt-red` | `#f7768e` | disagreement、风险提示 |

使用比例：背景 70%，文字与边框 20%，蓝紫主强调 8%，语义状态色 2%。这个配色我觉得可以调一下呢～如果后续页面接入真实截图，蓝紫强调可以再降低 10%，避免和截图抢视觉。

### 3.2 字体

- 主字体：`Inter`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, sans-serif。
- 代码字体：`JetBrains Mono`, `SFMono-Regular`, Consolas, monospace。
- H1：56–72px 桌面，40px 平板，34px 移动；字重 600，letter-spacing -0.04em。
- H2：34–44px 桌面，28px 移动；字重 560，letter-spacing -0.03em。
- Body：16–18px，line-height 1.65。
- Badge / metadata：12–13px，字重 600，英文可 uppercase。

### 3.3 间距与圆角

- 栅格：8px 基础栅格。
- 页面最大宽度：1180px。
- Section 垂直间距：桌面 112px，移动 72px。
- 卡片内边距：桌面 24–32px，移动 18–22px。
- 圆角：按钮 12px，卡片 20px，大型代码面板 28px。
- 触控：所有按钮与可点击卡片最小高度 44px。

---

## 4. 组件规范

### 4.1 顶部导航

- 左侧：Roundtable 圆桌符号 + wordmark。
- 中间：Overview、Workflow、Install、Channels。
- 右侧：GitHub ghost button、Get Started primary button。
- 桌面 sticky，背景 `rgba(8,9,15,0.72)` + blur；移动端保留 logo 与两枚核心 CTA，隐藏次级导航。

### 4.2 Hero

布局：桌面左右双栏，左侧文案，右侧“圆桌讨论仪表板”示意。移动端上下结构。

Hero 必备元素：

- H1：`多 Agent 圆桌讨论引擎`
- 英文辅助：`Structured roundtable discussions for AI Agent teams`
- 副标题：强调按轮次发言、追踪共识分歧、生成结构化会议记录。
- CTA：`快速开始` / `View GitHub`
- 安装命令卡：`pip install agent-roundtable`
- 信任标签：Python 3.10+、Apache-2.0、Zero external dependencies、SQLite。

右侧视觉建议：

- 中央圆桌：6 个角色节点围绕中心 convergence 点。
- 右侧 mini panel：展示 consensus、disagreement、summary 三类输出。
- 底部状态条：`round 2/3`、`convergence 0.82`、`meeting notes ready`。

### 4.3 痛点卡片

三张卡片一行，移动端单列：

1. 多 Agent 会说话，但不会“开会”
2. 讨论过程难复盘
3. 结论难沉淀到工作流

每张卡片使用小型 terminal prompt 或 quote 片段，避免普通图标卡片太泛。

### 4.4 能力卡片

四张卡片：Create Discussion、Speak in Turns、Track Convergence、Summarize Decisions。每张卡片由编号、短标题、1 句解释、输出对象组成。

### 4.5 Workflow 时间线

采用横向流程线，移动端改为纵向：

`init(topic, participants)` → `round based speaking` → `status + convergence` → `summary + conclusion`

每个节点都有输入 / 状态 / 输出，帮助开发者理解它是“协议层”而非聊天 UI。

### 4.6 Code Snippet

代码面板需要两层：

- 上层 Bash 安装命令，突出包名 `agent-roundtable`。
- 下层 Python 示例，突出导入名 `roundtable`。

增强项：复制按钮，JS 失败时不影响阅读。复制成功可把按钮文案改为 `Copied` 1.5 秒。

### 4.7 Channel Badges

渠道卡片包含：名称、用途、状态、链接状态。

| 渠道 | 状态建议 | 视觉 |
|---|---|---|
| GitHub | Available | 绿色点 + 可点击 |
| PyPI | Coming soon / Available 视发布状态 | 黄色或绿色 |
| Hermes Skill Hub | Planned / Coming soon | 紫色弱化 |
| OpenClaw Skill Hub | Planned / Coming soon | 蓝色弱化 |

不要把未上线渠道做成高亮主 CTA，避免用户误以为已经可用。

---

## 5. 响应式与交互规则

### 5.1 断点

| 断点 | 规则 |
|---|---|
| `<= 480px` | 单列布局，H1 34px，代码块横向可滚动但页面不可横向滚动 |
| `481–767px` | 单列，卡片间距 16px，Hero 视觉压缩为简化圆桌 |
| `768–1023px` | Hero 双栏可保留但比例改为 1fr / 0.9fr，能力卡片 2 列 |
| `>= 1024px` | 完整 12 栏视觉，Hero 约 54/46 分栏，卡片 3–4 列 |

### 5.2 可访问性

- 正文对比度不低于 WCAG AA。
- 交互元素有 `:focus-visible` 状态，focus ring 使用蓝紫光晕。
- 动效遵守 `prefers-reduced-motion`，关闭循环呼吸与浮动动画。
- H1 只出现一次；section title 使用 H2。
- 代码内容必须是真实文本，不作为图片展示。

### 5.3 动效

动效要像“会议正在呼吸”，不要像广告页。建议：

- Hero 圆桌中心轻微 pulse：3.6s infinite。
- 角色节点轻微错峰闪烁：表示轮次发言。
- 卡片 hover：边框亮度 + 背景透明度提升，不大幅位移。
- CTA hover：按钮从蓝到蓝紫渐变，并增加 1 层细微外发光。

---

## 6. SEO / OG 规范

- Title：`Roundtable - Multi-Agent Discussion Engine`
- Description：`Roundtable is a multi-agent discussion engine for structured debates, consensus tracking, and decision-ready meeting notes. Install with pip install agent-roundtable.`
- Keywords：`multi-agent, AI agents, roundtable, consensus tracking, meeting notes, Python package, agent-roundtable`
- OG title：`Roundtable - Multi-Agent Discussion Engine`
- OG description：`让多个 AI Agent 像开圆桌会议一样讨论、追踪共识分歧并沉淀结构化会议记录。`
- OG image：优先使用后续从 `static-intro-page-preview.html` 截出的 1200×630 分享图，或现有 `docs/design/social-preview.html` 体系。

---

## 7. 开发交付提示

### 推荐文件结构

```text
docs/design/static-intro-page-design.md      # 本设计规范
docs/design/static-intro-page-preview.html   # 静态预览稿，可本地打开
```

如果后续进入真实页面开发，可把 HTML 预览拆为：

```text
app/page.tsx 或 index.html
public/roundtable-logo.svg
styles/tokens.css
```

### 链接策略

- GitHub / README 可使用真实仓库链接。
- PyPI / Skill Hub 未确认前保留 `aria-disabled="true"` 或 Coming soon 文案。
- 页面内 CTA 可先锚点跳转到 `#install`，不依赖后端。

---

## 8. 设计验收清单

- [x] 覆盖 Hero、feature cards、workflow、code snippet、channel badges、CTA、footer。
- [x] 定义视觉方向：专业、现代、有记忆点，适合 AI Agent / 开源工具 / 开发者产品。
- [x] 给出色彩、字体、间距、响应式规则。
- [x] 安装命令为 `pip install agent-roundtable`，导入名为 `roundtable`。
- [x] 未上线渠道有 Coming soon / Planned 状态建议。
- [x] HTML 预览为单文件、无需外链资源、可本地打开。
- [x] 移动端按 375px 无横向滚动设计。

细节决定品质感。这个页面的重点不是堆信息，而是让用户的眼睛在 10 秒内找到答案：Roundtable 不是“更多聊天”，而是让 Agent 讨论可以收敛的协议层。
