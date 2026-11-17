# 重活外派 · 随时应答 —— 快速上手

> **一句话**：让 AI 助手不再被重活占死。规则块一页写清纪律，落地脚本一行命令装到本机，体检脚本告诉你装没装上。

**平台无关**：规则块与平台无关；落地器只在**有实测把握**的两个落点直接写文件（Hermes 的 `SOUL.md`、Claude Code 的 `~/.claude/CLAUDE.md`），其余平台导出一份可粘贴的规则块。

---

## 30 秒安装（三步）

```bash
# 1) 先预演：只报告，不动文件（默认就是预演）
python3 scripts/provision_agent_responsiveness.py

# 2) 确认无误后写入（自动备份原文件；幂等，重复跑不会重复写）
python3 scripts/provision_agent_responsiveness.py --apply

# 3) 体检：规则块在不在、是不是最新
python3 scripts/audit_agent_responsiveness.py
```

装完**重启**对应的 Agent 进程 / 网关（指令文件通常只在启动时读一次）。

---

## 探测不到我的平台怎么办？

不猜、不编路径。改用**可粘贴规则块**这条路：

```bash
python3 scripts/provision_agent_responsiveness.py --apply --export
# 生成 ./agent-ops-rules.md
```

把 `agent-ops-rules.md` 的内容整块粘到你的**系统提示 / 自定义指令 / 项目规则**里，效果等同：
- Codex / Cursor / WorkBuddy：粘到各自的全局指令或项目规则配置；
- 任意自建 Agent：粘到 system prompt；
- 任何看起来更简单的地方：直接把它当成一段"必须优先遵守"的指令文本。

---

## 它会往我的文件里写什么？

一个被标记包裹的规则块：

```markdown
<!-- agent-ops-rules:v1 -->
## ⚡ 重活外派 · 随时应答（作业纪律）
...（六条纪律）...
<!-- /agent-ops-rules -->
```

全文见 `templates/agent-ops-rules.md`。落地器的安全约定（脚本里写死）：

- **默认预演**：不加 `--apply` 绝不写盘；
- **自动备份**：写入前生成 `<文件名>.bak-agent-ops-<时间戳>`；
- **幂等**：有标记就比对内容——一致跳过、不一致只替换标记区块；
- **不覆盖你的内容**：只在文件顶部插入（跳过 frontmatter），不删任何原文；
- **纯标准库**：Windows / macOS / Linux 通用，无需装任何依赖。

---

## 它解决什么 / 不解决什么

| ✅ 它解决 | ❌ 它不解决 |
|---|---|
| 重活占住主脑、用户等不到回话 | 模型本身的速度——纪律不提升单点能力 |
| 插话被排队、长命令期间完全插不进去 | 需要用户拍板的决策（那本来就该用户定） |
| "装了但没人知道装没装上" | 跨会话常驻任务（用定时任务 / 后台进程） |
| 多实例 / 多 profile 逐个人工改的重复劳动 | 平台不提供的功能（探测不到就导出粘贴块） |

---

## 文件说明

- `SKILL.md`——完整方法论：病根、三件事、落地器/体检脚本用法、平台适配层、坑、验收清单。
- `templates/agent-ops-rules.md`——规则块全文（脚本的数据来源，也可直接手工粘贴）。
- `scripts/provision_agent_responsiveness.py`——跨平台幂等落地器（默认 dry-run）。
- `scripts/audit_agent_responsiveness.py`——跨平台体检；探测不到平台时如实报「未检测到支持的平台」。
- `references/hermes-implementation.md`——**示例实现（Hermes）**：真实键名、坑与验证口径（其他平台可忽略）。

---

## 关于作者

作者：**九品锦锂e**，长期做「一个主助手 + 多个后台子代理干活」的工程化落地，本技能是其中沉淀下来的纪律与工具。
联系方式见 `SKILL.md` 文末「关于作者」一节。
