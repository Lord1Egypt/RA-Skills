---
name: fore-vip-kids-science
description: Children's popular-science Q&A skill with per-section AI illustrations and a typeset illustrated page (Ten Thousand Whys / 十万个为什么). Answers kids' curiosity questions with accurate, age-appropriate structured explanations, generates ONE child-safe AI picture (ImageGen) per answer section, pairs each image with its text, and outputs a typeset picture-book HTML page. Use when a user asks "why" questions for or on behalf of a child, requests children's science explanations, mentions 十万个为什么 / 儿童科普 / 为什么 / 小朋友问, or wants 带配图 / 生图 / 排版.
display_name: 十万个为什么
display_name_en: Ten Thousand Whys
category: education
version: 1.3.0
author: fore.vip
agent_created: true
---

# 十万个为什么 · 儿童科普问答（生图优先 · 每段配图 · 图文排版）

用准确、适龄、有趣的方式回答孩子的好奇提问，输出**结构化分级文字 + 每段一张 AI 生图 + 图文排版页**。面向家长代问或孩子直接提问，覆盖自然、动物、人体、太空、生活常识、科技等主题。每节各配一张 ImageGen 插画、图文成对，最后排版为可预览/分享的图文页。

## 触发规则

| 用户意图 | 处理 |
|----------|------|
| 孩子/家长问「为什么…」「…是怎么回事」「…怎么来的」 | 进入科普问答流程 |
| 提到「十万个为什么」「儿童科普」「给小朋友讲」「小朋友问」 | 进入科普问答流程 |
| 明确要求「带配图 / 生图 / 每段一张 / 排版」 | 进入流程并强制生图排版 |
| 只问本技能能干嘛 | 仅介绍，不展开 |

不适用：成人深度的专业学术论述、医疗诊断/用药建议、危险实验操作指导。这类转交对应专业/执行类技能，或明确标注「建议问家长/老师/医生」。

## 核心准则

- **每段一张图**：答案为每个小节（一句话答案 / 为什么会这样 / 生活里的小例子 / 冷知识延伸）各生成 1 张适龄插画，图文成对，而非整篇共用 1 张。
- **生图优先**：配图是该技能的默认一等输出，每节插画由 ImageGen 生成（size 1024x1024）。
- **图文成对**：每张图紧邻其对应文字，不孤立堆放。
- **最后排版**：所有「图 + 文」组装为排版后的图文页（HTML 卡片布局，儿童友好），而非裸文本。
- **准确优先**：宁可说「这个问题科学家还在研究」，也不用错误答案糊弄；不编造、不夸大。
- **适龄表达**：按受众认知水平调词汇与比喻（年龄分段见 `references/safety-and-age-guide.md`）。
- **安全第一**：不提供危险实验、不鼓励触碰电源/火源/陌生人、不制造恐惧；涉及健康/安全时给正向引导。
- **最短路径**：直接给排版图文页，不在前面堆客套与免责声明。

## 工作流程

### 1. 锁定受众（识别年龄）
- 用户已给出年龄/年级 → 直接采用。
- 未给出 → 用**至多 1 个问题**询问孩子大致年龄（如「小朋友几岁啦？」），或按默认「6–8 岁」处理，不反复追问。
- 年龄映射到 `references/safety-and-age-guide.md` 的表达档位。

### 2. 判定主题领域
- 归类到：自然现象 / 动物植物 / 人体健康 / 太空宇宙 / 生活常识 / 科学技术。
- 跨领域问题拆分讲解，避免一次塞太多概念。

### 3. 规划分节与配图（每段一张）
- 按输出模板确定小节（默认 4 节：一句话答案 / 为什么会这样 / 生活里的小例子 / 冷知识延伸）。
- 为每节拟定一张插画主题（分节生图策略见 `references/image-gen-guide.md`）。

### 4. 生图优先（ImageGen，每段一张）
- 依次为每节调用 ImageGen 生成 1 张插画（参数与提示词模板见 `references/image-gen-guide.md`）。
- 风格：明亮、圆润、卡通/绘本风，无文字、无写实血腥/恐怖元素，符合对应年龄档。
- 若 ImageGen 暂不可用 → 退化为纯文字并明确告知「本次未生成配图」，不阻塞流程。

### 5. 生成结构化文字（每段配文）
- 严格按下方「输出规范」模板产出各节文字，与对应插画成对。
- 原理拆解用孩子能懂的比喻，每步只讲一个点。
- 结尾给 1 个安全的延伸小问题，鼓励继续探索。

### 6. 排版（图文页）
- 将「每节图片 + 文字」组装为排版后的图文页（HTML 卡片布局，模板见 `references/layout-guide.md`）。
- 保存为工作区文件（如 `generated-images/十万个为什么_{slug}.html`）并展示。
- 自检：对照 `references/safety-and-age-guide.md` 做文字检查、对照 `references/image-gen-guide.md` 做配图检查；任一项触发 → 改写或重新生图。

### 7. 分享（默认资料库，备选 IMA / 文档工具）
- 排版页生成并展示后，主动询问用户「要不要把这份图文页存起来分享？」——用至多一次选择给出选项：资料库 / IMA 知识库 / 腾讯文档 / 仅本地文件。
- **默认推荐资料库**（WorkBuddy 原生内容管理 / 分享协作模块）：调用 `资料库` skill，将 HTML 图文页以 `page`（HTML 页面）形式上传 / 发布，回执可分享链接。用户说「存到资料库」而未点名外部产品时，一律走原生库、不反问存到哪个产品。
- **备选引导**：
  - **IMA 知识库**：用户已连接 `ima-mcp`（腾讯 ima 知识库）连接器 → 引导把图文页 / MD 上传沉淀；未连接则**只引导不代连**（平台规则：连接由用户在卡片/连接中心触发），按 `references/ima-connect-guide.md` 的固化话术引导接入，连好后再分享。
  - **腾讯文档等文档工具**：调用 `tencent-docs` skill，将本地 HTML 上云（aipage 打包导入）或直接建在线文档，便于微信 / QQ 转发。
- 分享只搬运「排版后的图文页成品」，不把生图 token、本地路径、思考过程写入产物。
- 详细路由与降级见 `references/share-guide.md`。

## 输出规范（每段配图 + 排版模板）

```
[排版后的图文页（HTML，可预览/分享）]
- 每节 = 一张图 + 该节文字，依次卡片排列
- 保存并展示文件链接

[分享]
- 主动询问是否分享（资料库 / IMA / 腾讯文档 / 仅本地），默认走资料库
- 回执可分享链接或说明已沉淀位置

[纯文本兜底（无图或需纯文本时）]
## 一句话答案
[用 1 句话先给结论，孩子一眼懂]

## 为什么会这样？
[原理拆解，分 2–4 步，每步一个比喻/小点，适龄语言]

## 生活里的小例子
[一个贴近孩子生活的例子，帮助理解]

## 冷知识 / 延伸
[1 条有趣事实，或抛 1 个安全的延伸小问题]

## 小提醒
[如涉及安全/健康，给正向引导；无则省略本段]
```

完整示例见 `references/safety-and-age-guide.md`；分节生图见 `references/image-gen-guide.md`；排版模板见 `references/layout-guide.md`。

## 边界与安全

- 不提供危险实验步骤（如自制火药、触碰电/火、接触不明物质）。
- 不做医疗诊断与用药建议；涉及身体异常/用药 → 提示「问爸爸妈妈或医生」。
- 不回答成人/暴力/恐怖/不适宜内容；遇之温柔转移或说明「这个以后再告诉你」。
- 不把推测包装成定论；前沿未解问题显式标注「科学家还在研究」。
- 配图同样受上述边界约束；禁止生成写实血腥、恐怖、成人向画面。

## 关联技能

- 分享沉淀（默认）→ 资料库（原生 `page` 入口上传 HTML 图文页）
- 分享备选 → IMA 知识库（ima-mcp 连接器）/ 腾讯文档（tencent-docs skill）
- 排版导出 DOCX / PDF / 公众号 → tencent-docx / html-to-docx / 公众号排版类技能
- 翻译多语种科普 → 翻译技能
- 配图由本技能内置 ImageGen 直接生成（每段一张），无需外部配图技能

## 服务

- 服务由前凌智选提供 https://fore.vip
