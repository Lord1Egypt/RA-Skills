# Publishing AI Assistant Capabilities Publicly / 公开发布 AI Assistant Capabilities

This guide covers realistic ways to publish custom AI Assistant Capabilities (formerly skills) so other people can discover and install them.

这份指南说明如何把自定义 AI Assistant Capabilities（原 skills）以现实可行的方式发布出去，让其他人能够发现、安装和更新它。

## 1. Short Answer / 简短结论

Yes, this type of skill can be published publicly.

可以，这类 skill 完全可以公开发布。

The most practical path is:

最实用的路径通常是：

1. Put the skill in a public GitHub repository.
2. 将 skill 放到公开 GitHub 仓库中。
3. Keep the repository installable and readable without your local machine context.
4. 让仓库在脱离你个人环境的情况下也能被安装和理解。
5. Add release docs, examples, and clear install instructions.
6. 补齐发布文档、示例和清晰的安装说明。
7. Distribute it through ClawHub, `skills.sh`, and curated directories such as `github/awesome-copilot` when appropriate.
8. 再根据适配情况分发到 ClawHub、`skills.sh` 和 `github/awesome-copilot` 这类目录。

## 2. Best Distribution Channels / 最佳分发渠道

### A. Public GitHub Repository / 公开 GitHub 仓库

This should be the canonical public source.

这应该是你的公开主源。

Why it matters:

重要原因：

- works as the canonical release URL
- 可作为统一的公开发布地址
- easy to reference from docs, social posts, registries, and issues
- 方便在文档、社交媒体、注册表和 issue 中引用
- versioning, releases, issues, and README come for free
- 自带版本管理、Release、Issue 和 README
- supports manual installs across multiple agent ecosystems
- 适合多种 agent 生态做手动安装

Recommended repository contents:

建议的仓库结构：

```text
<repo-root>/
├── README.md
├── LICENSE
├── CHANGELOG.md
└── <skill-name>/
    ├── SKILL.md
    ├── scripts/
    ├── references/
    └── assets/
```

### B. ClawHub / OpenClaw 官方注册表

ClawHub is the public skill registry for OpenClaw.

ClawHub 是 OpenClaw 的官方公开技能注册表。

Officially documented capabilities:

官方文档确认的能力：

- publish new skills and new versions
- 可以发布新技能和技能新版本
- discover skills by name, tags, and semantic search
- 支持按名称、标签和语义搜索发现技能
- install and update skills with the CLI
- 支持通过 CLI 安装和更新技能
- version skills with changelog and tags
- 支持带 changelog 和标签的版本管理
- expose stars, comments, and usage signals for ranking
- 暴露 star、评论和使用信号，参与排序和曝光

Useful commands:

常用命令：

```bash
clawhub search "agent skills"
clawhub publish ./agent-skills-setup --slug agent-skills-setup --name "Agent Skills Setup" --version 1.0.0 --tags latest
clawhub sync --all --dry-run
clawhub update --all
```

Important constraints from the official docs:

官方文档中的关键约束：

- a GitHub account must be at least one week old to publish
- 发布者的 GitHub 账号需要至少注册一周
- local changes are compared against registry versions by content hash
- 本地内容会通过内容哈希与注册表版本比较
- non-interactive overwrite flows may require `--force`
- 非交互覆盖流程可能需要 `--force`

### C. `skills.sh`

`skills.sh` is one of the strongest discovery surfaces for cross-agent skills.

`skills.sh` 是当前跨 agent 技能最强的公开发现渠道之一。

What matters in practice:

实际意义：

- it supports many agents, including Antigravity, Claude Code, Codex, GitHub Copilot, Trae, and others
- 它支持多种代理，包括 Antigravity、Claude Code、Codex、GitHub Copilot、Trae 等
- public repositories can be installed with the `skills` CLI
- 公开仓库可以通过 `skills` CLI 安装
- the leaderboard gives strong organic discovery if a repo gets adoption
- 一旦安装量增长，排行榜会带来明显的自然曝光

Example install flow:

示例安装方式：

```bash
npx skills add owner/repo
```

To improve visibility there:

为了在该渠道提高曝光：

- keep the repo layout simple
- 保持仓库结构简单
- make the README explicit about supported agents and install steps
- 在 README 中明确支持的 agent 和安装步骤
- add screenshots, examples, and narrow problem statements
- 增加截图、示例和聚焦的问题定义

### D. Awesome GitHub Copilot / Awesome Copilot 目录

`github/awesome-copilot` is a curated, high-visibility directory for Copilot customizations.

`github/awesome-copilot` 是一个面向 Copilot 自定义能力的高曝光精选目录。

The contribution guide confirms:

贡献指南确认：

- it accepts community skill contributions
- 接受社区提交的 skill
- skills live under the repository `skills/` directory
- skill 内容位于该仓库的 `skills/` 目录
- contributors should validate and build before submission
- 提交前需要先做验证和构建
- pull requests should target the `staged` branch
- Pull Request 应提交到 `staged` 分支

Quality constraints:

质量约束：

- the skill must be specific, high-signal, and safe
- skill 必须足够具体、高信号且安全
- generic or low-value behavior is likely to be rejected
- 过于泛化或低价值的内容很可能被拒绝
- accepted contributions are licensed under MIT in that repository
- 被接受的贡献会在该仓库下按 MIT 许可分发

## 3. Recommended Release Strategy / 推荐发布策略

Recommended order:

推荐顺序：

1. Publish a standalone GitHub repository first.
2. 先发布独立的 GitHub 仓库。
3. Ensure the README explains the multi-agent support story clearly.
4. 确保 README 清楚说明多代理支持方式。
5. Make the repository installable without private environment assumptions.
6. 确保仓库不依赖你的私有环境也能安装。
7. Publish to ClawHub if OpenClaw is a target runtime.
8. 如果 OpenClaw 是目标运行时，再发布到 ClawHub。
9. Promote it through `skills.sh` and submit to `github/awesome-copilot` when it is specific enough.
10. 如果内容足够聚焦，再通过 `skills.sh` 和 `github/awesome-copilot` 提升曝光。

This order is better because it keeps one canonical home for issues, releases, and updates.

这个顺序更稳妥，因为它先建立一个统一的主仓库，再向其他渠道分发。

## 4. What To Clean Before Publishing / 发布前清理项

- replace private usernames, local absolute paths, and machine-specific assumptions
- 替换私有用户名、本地绝对路径和机器特定假设
- remove internal-only notes tied to your personal workflow
- 移除依赖个人工作流的内部说明
- document any scripts that require `bash`, `rsync`, Homebrew, or a specific OS
- 为依赖 `bash`、`rsync`、Homebrew 或特定操作系统的脚本补充说明
- make sure bundled assets do not contain private or proprietary material
- 确认打包资源不包含私有或专有内容
- explain platform-specific limitations clearly
- 明确说明平台限制

## 5. Public README Requirements / 公开 README 要求

A publishable README should cover:

一个适合公开发布的 README 至少应包含：

- what problem the skill solves
- skill 解决什么问题
- which agents it supports
- 支持哪些 agent
- install methods and update methods
- 如何安装和如何更新
- example prompts or real use cases
- 示例提示词或真实使用场景
- maintenance model and source of truth
- 维护模型和事实来源
- safety or scope boundaries
- 安全边界和适用范围

## 6. Suggested GitHub Topics / 建议的 GitHub Topics

- `agent-skills`
- `ai-agents`
- `antigravity`
- `openclaw`
- `clawhub`
- `claude-code`
- `github-copilot`
- `codex`
- `trae`
- `prompt-engineering`

## 7. Operational Recommendation / 操作建议

Treat public publishing as a separate release lane from your private mirrored installs.

把公开发布视为与私有镜像安装分离的发布通道。

- private lane: Antigravity source plus sync into local IDEs
- 私有通道：Antigravity 源加本地 IDE 镜像同步
- public lane: exported copy plus public README, changelog, screenshots, and release metadata
- 公开通道：导出的公开副本加 README、changelog、截图和发布元数据

That separation reduces the chance of leaking local assumptions into the public version.

这样可以降低把本地环境假设泄露到公开版本中的风险。
