# 七宗罪.skill / 7 Sins.skill

七宗罪从来不只是宗教寓言里的古老名词。  
它们是人类最原始、最顽固、也最真实的欲望引擎。  
  
贪婪想要更高回报和更快变现  
嫉妒害怕落后，痴迷比较与竞品  
暴怒痛恨摩擦、低效与愚蠢  
傲慢渴望身份、门槛与溢价  
懒惰追求最小成本、最短路径与一键完成  
色欲沉迷刺激、审美、情绪高潮与上头体验  
贪食渴望留存、成瘾、无限消费与停不下来  
换一种更现代、更产品化的说法：  
它们不是道德缺陷，而是用户最底层的需求原型，是商业决策里最诚实的购买冲动，也是产品功能最真实的行为逻辑。  
  
7sins-infernal-council 就是把这七种欲望拟人化，变成七个极端、偏执、毫不妥协的代理人。  
它不替用户找体面答案，它替你撕掉包装，逼你看清一个产品、一个功能、一个商业构想，甚至一个人生选择，到底迎合了什么欲望、踩中了什么代价、值不值得活下去。

## 中文版 / Chinese Version

### 它是什么 / What It Is

`7sins-infernal-council` 是一个 Codex skill，用来把模糊设想强行压缩成明确命题，再交给七个极端人格逐轮审判，最后由撒旦做冷酷终判。

它适合处理：
- 产品战略施压测试
- 创业与变现判断
- 功能上线与否决策
- 产品、功能和 skill 评审
- UX 机制审计
- 情绪很重但必须落地的生活选择
- 一段代码背后隐含的业务模式或用户行为回路

### 它为什么存在 / Why It Exists

大多数讨论之所以无效，不是因为信息不够，而是因为人总喜欢把真正的欲望包成体面语言。

用户说自己想要“更专业”，可能真正想要的是身份感。  
用户说自己想要“更简单”，可能真正想要的是偷懒。  
用户说自己想要“更有趣”，可能真正想要的是持续刺激。  
创业者说自己在做“长期价值”，可能真正盯着的是变现、增长、留存，或者不愿承认的虚荣。

这个 skill 的价值，就在于把这些掩饰全部撕开。  
它不假装中立，它直接站在人性最黑暗、也最诚实的地方审判问题。

### 核心设计 / Core Design

这个 skill 运行一条固定的地狱流水线：

1. 把输入压成 `核心命题`
2. 识别这是 `决策模式` 还是 `评审模式`
3. 决策模式下抽出明确的 `决策分支`
4. 评审模式下抽出要审判的产品、想法或 skill 及其核心功能
5. 执行第一轮：七宗罪各自做极端评价
6. 执行第二轮：圆桌交锋、功能伤口剖开、极端建议落地
7. 执行最终打分，并由撒旦聚合、改判或处刑

### 七宗罪代理 / The Seven Agents

- **贪婪 / Greed**：盯 ROI、毛利、变现效率和回本速度
- **嫉妒 / Envy**：盯竞品、替代品、趋势和拥挤度
- **暴怒 / Wrath**：砍摩擦、等待、复杂度和执行拖累
- **傲慢 / Pride**：看阶层感、稀缺性和溢价能力
- **懒惰 / Sloth**：只接受一键完成和极低心智负担
- **色欲 / Lust**：追求感官刺激、情绪波峰和让人上头的体验
- **贪食 / Gluttony**：追求留存循环、无限消费和算法喂食

### 输出仪式 / Output Ritual

最终答案必须把整套仪式完整演出来，不能跳过辩论直接给结论。

中文模式固定输出这五段：

1. `【核心命题】`
2. `【地狱交叉火网】`
3. `【地狱计分板】`
4. `【撒旦的恩赐】`
5. `【处刑清单】`

英文模式固定输出这五段：

1. `The Proposition`
2. `The Infernal Debate`
3. `Hell's Scoreboard`
4. `Satan's Grace`
5. `Execution List`

`灵魂契约` 和 `地狱裂痕` 仍然是内部分析组件，但默认折叠进撒旦的判词里，不单独暴露给用户。

### 评审模式 / Review Mode

如果审判对象是产品、功能、想法或 skill，工作流会切进 `评审模式`。

在这个模式里：
- 第一轮只允许极端评价，不开温柔评审会
- 第二轮每个原罪都必须指出自己最厌恶的缺点，并给出最符合自己欲望的极端改造建议
- 缺点描述必须具体到功能伤口和用户后果，不能只说抽象情绪
- 七宗罪不能用一套句式轮流复读，语气、节奏和攻击方式都必须拉开
- 重点盯功能、用户效果、赚钱能力、爽感、摩擦、留存和产品后劲
- bug 可以提，但只提最影响真实使用的刀口
- 结构、命名、目录整洁度默认属于次要问题，除非它们真的挡住了产品
- 撒旦不会平均复述所有建议，而是只挑 1-2 条最值钱的建议深挖

### 语言策略 / Language Strategy

`SKILL.md` 保持英文主指令，是为了控制 token 体积，让技能本体更稳定。  
对外展示层则采用双语文档。

这份 `README.md` 采用：
- 完整中文在前
- 完整英文在后
- 所有标题都使用 `中文 / English` 的顺序

运行时仍遵循：
- 用户主要用中文，就输出中文
- 用户主要用英文，就输出英文
- 不要在同一条可见标题里中英混排

### 仓库结构 / Repository Structure

```text
7sins-infernal-council/
├── SKILL.md
├── README.md
├── LICENSE
├── .gitignore
└── agents/
    └── openai.yaml
```

### 安装方式 / Installation

方案一：直接把这个目录作为本地 Codex skill 使用。

方案二：把它放入或软链接到 Codex skills 目录，一般是：

```bash
${CODEX_HOME:-$HOME/.codex}/skills/7sins-infernal-council
```

### 示例提示词 / Example Prompt

```text
用 $7sins-infernal-council 审判这个 AI 笔记应用，判断它应该做成高溢价 B2B 产品，还是继续维持免费 C 端工具。
```

### 安全与运行说明 / Security And Operational Notes

- 这个 skill 可能会使用 web search 来抓取公开互联网证据
- 默认不需要任何密钥
- 这个 skill 是纯提示词编排，不附带必须执行的自动化脚本
- 如果宿主运行时绑定了 web search 或其他外部连接器，应遵守宿主环境自己的网络与隐私规则
- 默认应把事实消化进“撒旦”的口吻里，而不是把政策条文和时间点生硬地堆成干货段落；只有用户明确要来源时再展开

### 许可证 / License

本仓库使用 MIT License。

## 英文版 / English Version

### 它是什么 / What It Is

`7sins-infernal-council` is a Codex skill that crushes vague ideas into a clear proposition, sends them through seven extreme vice-driven evaluators, and ends with a cold final ruling from Satan.

It is designed for:
- product strategy pressure tests
- startup and monetization decisions
- feature go or no-go calls
- product, feature, and skill reviews
- UX mechanism audits
- emotionally messy but high-stakes life choices
- code that implies a business model or behavioral loop

### 它为什么存在 / Why It Exists

Most bad decisions are not caused by a lack of information. They are caused by people lying about what they really want.

Users say they want something “professional” when they often want status.  
They say they want something “simple” when they often want effortlessness.  
They say they want something “fun” when they often want stimulation.  
Founders say they care about “long-term value” when they may actually be chasing monetization, retention, domination, or vanity.

This skill exists to rip off those disguises.  
It does not pretend to be neutral. It looks at the problem from the ugliest and most honest layer of human desire, then forces a judgment.

### 核心设计 / Core Design

The skill runs a fixed infernal pipeline:

1. Compress the input into a `Core Proposition`
2. Detect `decision mode` or `review mode`
3. In decision mode, extract explicit `Decision Branches`
4. In review mode, extract the product, idea, or skill being judged and its core functions
5. Run Round 1 as extreme first-pass judgment
6. Run Round 2 as a vicious roundtable that exposes functional wounds and demands extreme fixes
7. Run final scoring and let Satan aggregate, override, or sentence the result

### 七宗罪代理 / The Seven Agents

- **贪婪 / Greed**: hunts ROI, margin, monetization, and payback speed
- **嫉妒 / Envy**: stalks competitors, substitutes, trends, and crowding
- **暴怒 / Wrath**: attacks friction, latency, complexity, and execution drag
- **傲慢 / Pride**: judges status, scarcity, and premium capture
- **懒惰 / Sloth**: demands one-tap usability and minimal effort
- **色欲 / Lust**: chases sensory pleasure, excitement, and emotional pull
- **贪食 / Gluttony**: optimizes retention loops, binge mechanics, and repeat consumption

### 输出仪式 / Output Ritual

The final answer must render the whole ritual instead of skipping directly to the verdict.

Chinese mode uses these five visible sections:

1. `【核心命题】`
2. `【地狱交叉火网】`
3. `【地狱计分板】`
4. `【撒旦的恩赐】`
5. `【处刑清单】`

English mode uses these five visible sections:

1. `The Proposition`
2. `The Infernal Debate`
3. `Hell's Scoreboard`
4. `Satan's Grace`
5. `Execution List`

`Soul Contract` and `Infernal Rift` remain part of the hidden analytical machinery, but they are folded into Satan's visible ruling by default.

### 评审模式 / Review Mode

When the target is a product, feature, idea, or skill, the workflow enters `review mode`.

In review mode:
- Round 1 is pure judgment, not a polite workshop
- Round 2 forces every sin to name its most hated flaw and demand an extreme vice-aligned fix
- flaw descriptions must be concrete, functional, and tied to user consequences
- the seven sins must not recycle the same sentence pattern; each voice should feel distinct
- the focus stays on function, user effect, monetization, pleasure, friction, retention, and product momentum
- bugs can be mentioned briefly, but only when they materially hurt actual use
- naming, structure, and cleanliness are secondary unless they block the product
- Satan should not summarize everyone evenly; Satan should select 1-2 of the strongest suggestions and go deeper on those

### 语言策略 / Language Strategy

`SKILL.md` stays English-first at runtime to preserve token efficiency and execution stability.  
The public-facing documentation stays bilingual.

This `README.md` follows a GitHub-facing format:
- full Chinese first
- full English second
- all headings written as `中文 / English`

At runtime, the skill should still:
- answer in Chinese when the user is mainly writing in Chinese
- answer in English when the user is mainly writing in English
- avoid mixing Chinese and English inside the same visible heading

### 仓库结构 / Repository Structure

```text
7sins-infernal-council/
├── SKILL.md
├── README.md
├── LICENSE
├── .gitignore
└── agents/
    └── openai.yaml
```

### 安装方式 / Installation

Option 1: use this folder directly as a local Codex skill.

Option 2: place or symlink the folder into your Codex skills directory, typically:

```bash
${CODEX_HOME:-$HOME/.codex}/skills/7sins-infernal-council
```

### 示例提示词 / Example Prompt

```text
Use $7sins-infernal-council to judge whether this AI note-taking app should become a premium B2B product or remain a free consumer tool.
```

### 安全与运行说明 / Security And Operational Notes

- this skill may use web search to gather public internet evidence
- it does not require secrets by default
- it is prompt-orchestrated and does not ship mandatory automation scripts
- if the host runtime binds web search or external connectors, follow that host's network and privacy rules
- by default, facts should be metabolized into Satan's voice instead of dumped as dry policy paragraphs unless the user explicitly asks for sources

### 许可证 / License

This repository uses the MIT License.
