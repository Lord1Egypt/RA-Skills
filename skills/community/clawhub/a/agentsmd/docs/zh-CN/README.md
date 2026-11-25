简体中文 | [English](../../README.md)

# agentsmd

**你踩过的坑，AI 不再踩第二遍。**

[![GitHub stars](https://img.shields.io/github/stars/kelegele/agentsmd-skill?style=flat-square)](https://github.com/kelegele/agentsmd-skill/stargazers)
[![skills.sh installs](https://skills.sh/b/kelegele/agentsmd-skill?style=flat-square)](https://www.skills.sh/kelegele/agentsmd-skill)
![Agent Skill](https://img.shields.io/badge/格式-Agent_Skills-blue?style=flat-square)
![Claude Code](https://img.shields.io/badge/支持-Claude_Code-purple?style=flat-square)
![Codex](https://img.shields.io/badge/支持-Codex-black?style=flat-square)
![Cursor](https://img.shields.io/badge/支持-Cursor-gray?style=flat-square)

把这次会话里踩的坑、纠正过的错交给 AI，说一句「把教训固化进 AGENTS.md」，它会把它们蒸馏成一行行可执行的规矩，写进项目根目录的 AGENTS.md。此后每个新会话——无论 Claude Code、Codex 还是 Cursor——开工前自动读取，照办。

> 这个 skill 来自我自己一次次重复的「调教」。每次开发，总有一些东西想固化下来：这个项目怎么构建、哪些边界不能碰、代码要守什么规范。它们不写进 AGENTS.md，就得每次开新会话重新教一遍 agent——同样的错它犯三遍，我纠正三遍，时间全耗在这上面。
>
> 后来成了习惯：每当有通用的规范或规则要存，我就让 agent 写进 AGENTS.md。日子久了又冒出新麻烦——文件一攒就攒成常识大全，越写越肥，肥到最后连真正的规矩都被淹没在里面。
>
> 于是我想到：固化这件事本身，为什么不交给 skill？从此我只要说一句「把这次的教训固化进 AGENTS.md」，收集、蒸馏、合并、核验它全包，我只负责批准。然后，就有了这个 skill。

## 30 秒开始

```bash
npx skills add kelegele/agentsmd-skill
```

装好后，对 AI 说：

> 用 agentsmd 把这次的教训固化进 AGENTS.md

不想动手装？直接把仓库地址发给你的 agent：

> 帮我安装这个 skill：https://github.com/kelegele/agentsmd-skill ，装好后告诉我怎么用。

## 它能帮你做什么？

| 你手里的东西 | 它会怎么处理 |
|---|---|
| 这次会话踩的坑、纠正过的错、重复过的偏好 | 过三关准入（会再遇到 + 违反有实际损失 + 一行说得清），泛化成通用规则、压成一行祈使句写入 AGENTS.md |
| 一份越写越肥的 AGENTS.md | 五道合并闸门：等价丢弃 / 重叠合并 / 特例泛化 / 矛盾取新 / 过时删除，禁止无条件追加 |
| 接近 120 行上限 | 仍有价值的内容迁 `docs/<主题>.md`，原位留一行引用——删的是冗余，不是记忆 |
| 一个还没有 AGENTS.md 的新项目 | 扫描目录结构、README 与构建/CI 配置按实际生成；每条命令实跑或逐一核对，跑不通的不写入 |
| 只属于某个子目录的教训 | 下沉为该子目录的局部 AGENTS.md，根文件只留全局适用内容 |
| 纯文档 / 数据的 work 目录（报告库、协作目录） | 自动切换适配：扫文档结构与命名惯例替代构建配置，规则偏向口径、归档与交付规范，归集脱离固定三桶，按 work 类型自定文件夹分类 |
| 散落在根目录的文档与数据文件 | 先查代码引用再出方案：文档归 `docs/<主题>/`、数据归 `data/<主题>/`，批准后移动并修复所有引用断链 |
| Hermes / OpenClaw 等 personal agent 的记忆、TODO / CHANGELOG | 借宿主自己的记忆机制沉淀项目记忆——按宿主格式、先查重、批准后写入，不另起炉灶；无记忆机制则静默跳过 |

## 为什么不是「让 AI 自己写一份」？

每个新会话 AI 都从零开始：你纠正过的错它今天照犯，教训散落在几十个会话记录里，换会话、换工具全部蒸发。让它自己写规范？它给你堆一份 500 行的「最佳实践」——一半是常识，一半是没跑通就写进去的命令，文件越肥，越没人当真。

agentsmd 反其道而行：**每条规则一句话**、**总长硬上限 120 行**、**命令逐条核验**、**落盘前必须经你批准**。规范是宪法，不是垃圾场。

## 怎么说，比较容易一次做好？

**固化本次教训**（最常见）：

> 把这次踩的坑固化成项目规则

**瘦身一份已经很肥的规范**：

> 更新项目规范：把这次的教训按合并决策表整合进去，超 120 行就先删后加

**新项目初始化**：

> 项目还没有 AGENTS.md，用 agentsmd 生成首版，命令都要实跑核验

**work 目录（纯文档 / 数据协作目录）**：

> 沉淀这个协作目录的工作规范，顺手把散落的报告、数据、参考资料归整一下

**顺手归档**：

> 把教训写进 AGENTS.md，顺便把根目录散落的文档和数据归整一下

## 从会话到规范，它做七件事

1. **收集教训**：提取你指出的错误、实际踩的坑、重复出现（≥2 次）的偏好、验证有效的做法；一次性细节与通用常识直接排除。
2. **蒸馏规则**：泛化 → 压成一行 → 归入最贴近的章节；三关准入，缺一丢弃。
3. **读取现状**：已有 AGENTS.md 就逐条建立现有规则清单；没有就先判定 coding / work 场景再生成首版——coding 逐条核验命令，work 核对文中引用路径。
4. **有机合并**：新规则过五道闸门后才可能写入；接近 120 行先删后加，有价值内容迁 `docs/`。
5. **确认写入**：提交完整改动方案（新增 / 合并 / 删除 / 迁移 / 行数），你批准后才动文件。
6. **同步记忆与进度**：借宿主的壳，不另起炉灶——agent 有记忆机制就按其格式沉淀项目记忆，有 TODO / CHANGELOG 就同步更新；不造私有记忆格式，装到哪个 agent 都融入其生态。
7. **文档与数据归集**（可选）：先查引用再出方案——文档归 `docs/`、数据归 `data/` 为缺省；work 场景自定贴合 work 类型的分类，批准后写入 AGENTS.md 固化；批准后移动并修复断链。

## 最后你会得到什么？

- 一份 **≤120 行**、章节贴合项目实际、无占位空条的 `AGENTS.md`
- 迁移到 `docs/` 的参考内容，与根文件里的一行引用
- 更新后的 agent 项目记忆与进度文件
- 归档整洁、无断链的目录布局（缺省 `docs/`、`data/`、`references/`；work 场景为贴合 work 类型的自定分类）

## 安装

### Claude Code / Codex / Cursor（git clone）

```bash
git clone https://github.com/kelegele/agentsmd-skill.git ~/.claude/skills/agentsmd   # 全局
git clone https://github.com/kelegele/agentsmd-skill.git .claude/skills/agentsmd    # 仅当前项目
```

### 手动复制（任意 agent）

把仓库复制到目标 agent 的技能目录，目录名须为 `agentsmd`：

| Agent | 全局技能目录 |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| 跨 agent 通用 | `~/.agents/skills/` |
| WorkBuddy | `~/.workbuddy/skills/` |

### WorkBuddy URL 导入

左侧栏 **技能 → 添加技能 → 通过 URL 导入**，粘贴 `https://github.com/kelegele/agentsmd-skill`，确认启用。

### 技能市场安装

```bash
clawhub install agentsmd   # ClawHub（OpenClaw 生态：openclaw skills install agentsmd）
```

也可在 [LobeHub Skills Marketplace](https://lobehub.com/skills/kelegele-agentsmd-skill) 一键安装。

> 注：部分 agent 需重启或新开对话才能加载新技能。

## 更新

按当初的安装方式对应操作（各版本变更内容见 [CHANGELOG](../../CHANGELOG.md)）：

**npx skills 安装**：用 CLI 自带的更新命令

```bash
npx skills update agentsmd   # 只更新 agentsmd；不带名字则更新全部
```

**git clone 安装**：进入克隆目录拉取最新

```bash
git -C ~/.claude/skills/agentsmd pull   # 全局安装的路径；项目内安装换成对应目录
```

**手动复制**：重新把仓库内容覆盖复制到技能目录。

**WorkBuddy URL 导入**：重新走一遍「技能 → 添加技能 → 通过 URL 导入」。

> 注：更新后部分 agent 需重启或新开对话才能加载新版。

## FAQ

**会让 AI 堆一堆通用常识吗？**
不会。写入前过三关准入门槛，「禁止为了看起来完整堆砌通用常识」写死在工作流里。

**规范里的命令跑不通怎么办？**
首版每条命令必须实跑确认，或与构建 / CI 配置逐一核对，跑不通、核对不上的一律不写入。

**文件会不会越用越大？**
不会。硬上限 120 行，新规则必须过合并闸门，「只增不减」被工作流直接禁止。

**换个 agent 还能用吗？**
能。AGENTS.md 遵循 [agents.md](https://agents.md/) 开源规范，Claude Code / Codex / Cursor / Gemini CLI / OpenCode / WorkBuddy 读同一份。

**Hermes / OpenClaw 这类 personal agent 能用吗？**
能。skill 是纯 Markdown，无构建无依赖、不绑定 CLI；agent 有记忆机制就按其格式沉淀记忆（先查重、批准后写入），没有就静默跳过。

**非代码目录能用吗？**
能。判定为 work 场景后自动切换适配：扫描对象换成文档结构与命名惯例，规则章节偏向口径、归档与交付，归集脱离固定 `docs/ data/ references/` 三桶——agent 按工作类型自定文件夹分类（仍须批准，批准后写入 AGENTS.md 固化），AGENTS.md 格式不变。

**会不经我同意改文件吗？**
不会。所有写入——AGENTS.md、记忆、进度文件、移动文档——先出方案、批准后才执行。

## 仓库结构

```
agentsmd/
├── SKILL.md                     # 核心工作流（7 步）
├── references/
│   └── agents-md-spec.md        # agents.md 规范要点摘要
└── assets/
    ├── AGENTS-template.md       # 章节参考骨架（标准 + 可选章节）
    └── AGENTS-example.md        # agents.md 官方真实成稿示例
```

> 以上为 skill 包本体，安装时复制的只是这些。仓库另含项目协作用文件（HANDOVER.md、docs/、scripts/、.zcode/ 等，中文版文档在 [docs/zh-CN/](.)），不属于 skill 安装内容。

## 相关项目

- [project-handoff-skill](https://github.com/kelegele/project-handoff-skill)——换一个 agent 接着干，不用从头再讲一遍。agentsmd 管「怎么干」，project-handoff 管「干到哪」。
- 博客文章：[设计哲学](https://www.kelegele.com/blog/agents-md-lessons-without-bloat) · [迭代复盘](https://www.kelegele.com/blog/agentsmd-skill-iteration-retrospective) · [使用指南](https://www.kelegele.com/blog/agentsmd-scene-guide)

## 反馈

遇到问题或有想法，欢迎 [提 issue](https://github.com/kelegele/agentsmd-skill/issues)。更多项目见作者站点 [kelegele.com](https://kelegele.com)。
