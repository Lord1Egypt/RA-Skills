---
name: agent-self-rollback
description: Deploy a self-rollback / snapshot mechanism for an AI agent's own memory files (identity SOUL.md, user profile USER.md, FACT.md, JOURNAL) and project files, so the agent can survive its own mistakes. Covers snapshotting, listing, restoring, and MD5 verify, plus self-discipline rules to write into the agent's own rules. Has a portable PowerShell script (snapshot/list/restore/verify). Use when the user asks for "agent rollback" "误操作回滚" "self-rollback mechanism" "protect my agent memory" "备份agent记忆" "快照回滚" or wants to harden an AI assistant against accidentally corrupting its own persistent memory. 关键词：误操作回滚、记忆保护、快照、self-rollback、agent memory backup、自毁预防。
version: "1.0.0"
---

# Agent Self-Rollback Mechanism（Agent 自身误操作回滚机制）

> 让 AI agent 拥有「后悔药」：即使把自己改坏了，也能从快照链里捞回来。
> Give an AI agent a "do-over": even if it corrupts its own memory, it can recover from a snapshot chain.

## 适用场景（When to use）

- 用户要求为 AI agent 建立 「自身的误操作回滚/备份机制」，保护 agent 的持久记忆文件（身份/人格/用户画像/事实库/事件日志）不被意外覆盖或写坏。
- 用户担心 **agent 误操作导致项目文件误改误删** 后无法恢复，需要一套快照方案。
- 任何「agent 有持久记忆 + 有文件写权限」的落地场景：Claude Code / CherryStudio / CodeBuddy / OpenClaw 等。

## 核心思想（Core idea）

三层防线，缺一不可：

1. **预防层（Rules）**：把自律规则写进 agent 自己的行为准则（SOUL.md 角色定义 或 AGENTS.md / 系统提示），让「改之前先存档」成为肌肉记忆。
2. **备份层（Snapshots）**：每次会话启动 / 修改关键文件之前，自动打时间戳快照。
3. **恢复层（Restore）**：发现记错/改坏 → `restore` 回滚；恢复前自动先存「当前状态」兜底，滚错了还能再滚回来。

## 部署步骤（Deploy steps）

### 1. 确认要保护的文件

典型 agent 记忆四件套（可自行增删）：

| 文件 | 内容 |
|---|---|
| `SOUL.md` | 身份、人格、说话风格 —— 改坏 = 性格崩了 |
| `USER.md` | 用户画像、偏好 —— 改坏 = 认错主人 |
| `memory\FACT.md` | 持久知识、决策 —— 改坏 = 知识断层 |
| `memory\JOURNAL.jsonl` | 事件日志（追加式）—— 一般不会坏，但要留档 |

可随时通过 `-Arg` 附加项目文件一起快照。

### 2. 放置脚本并配置

1. 拷贝 `scripts/rollback.ps1` 到一个**纯英文路径**（如 `D:\agent-tools\self-rollback\`）——中文路径在部分 Windows 环境的 PowerShell/CI 下有编码坑。
2. 编辑脚本顶部 `# config` 区块：
   - `$AgentDir` → agent 数据根目录绝对路径
   - `$CoreFiles` → 要保护的相对路径清单
   - 快照目录默认是脚本上一级 `snapshots\`，可改 `$SnapRoot`

### 3. 跑一次初始化快照

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File rollback.ps1 snapshot
```

应在 `snapshots\<时间戳>\` 生成：记忆文件 + `MANIFEST.txt` + `HASHES.md5` + `REASON.txt`。

### 4. 写入自律规则

把下面这段（按需改措辞）加入 agent 的行为准则（SOUL.md 安全护盾区 或 AGENTS.md）：

> 1. 每次会话启动先打一次快照。
> 2. 修改 SOUL.md / USER.md（身份/人格文件）之前必须先打快照。
> 3. 项目文件批量覆盖/删除前，用 `-Arg` 把关键路径一并快照，或改用 trash 类软删除。
> 4. 怀疑记忆被动过 → `verify`（MD5 对比）；确认改坏 → `restore`（先看清序号再输 yes）。
> 5. 每次会话结束，确认快照链存在。

### 5. 封装一键命令（可选）

提供 `snapshot.bat` / `restore.bat` 双击即用：

```bat
@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0rollback.ps1" snapshot
pause
```

## 命令速查（Commands）

| 命令 | 作用 |
|---|---|
| `snapshot` | 打快照，可选 `-Arg "path1,path2"` 附加项目文件 |
| `list` | 列全部快照，最近的是序号 0 |
| `restore [序号]` | 回滚到指定快照（先自动存 pre-restore 兜底，输 yes 确认） |
| `verify` | 对比当前文件与最近快照 MD5，标 UNCHANGED / CHANGED / MISSING |

## 铁律（Rules / Iron rules)

1. **恢复比备份更挑剔**：restore 会覆盖当前文件，必须先提示、必须再存一份 pre-restore 兜底、必须让用户输入 `yes` 二次确认。
2. **JOURNAL/日志类文件 verify 报 CHANGED 属正常**（每次都追加），不要误报警。
3. **快照目录只增不删**：所有快照都能查（list），磁盘吃紧手动清理旧档即可。
4. **脚本输出用英文，中文解说放文档**：Windows PowerShell 对 UTF-8 无 BOM 中文脚本易乱码；文档双语随意。
5. **路径用纯英文**：脚本所在路径、快照目录避免中文，防编码坑。
6. **凭证不落盘**：脚本里不要写死任何 API Key / token；认证一律环境变量或一次性 URL。
7. **建档时机**：修改任何「旧档」之前先存「新档」——形成「改前档 + 改后档」可回滚链。

## 自检清单（Checklist）

部署完成后逐项确认：

- [ ] `snapshot` 第一次运行成功，快照目录出现时间戳文件夹
- [ ] 快照内含全部核心文件 + `MANIFEST.txt` + `HASHES.md5` + `REASON.txt`
- [ ] `list` 能看到至少一条快照
- [ ] 随手改一个测试文件后 `verify` 能标出 CHANGED，改回来再 `verify` 是 UNCHANGED
- [ ] `restore` 前会打印 pre-restore 提示，且要求输入 `yes`
- [ ] 自律规则已写入 agent 行为准则（SOUL.md / AGENTS.md）

## 正误示例（Do / Don't）

**✅ 正确**
- 改 SOUL.md 前：先 `snapshot`，再编辑，改完再 `snapshot` —— 留「前档 + 后档」。
- 遇到记忆疑似被动：先 `verify` 看 MD5 差异，再决定回不回滚，不盲目恢复。
- restore 后立即再打一次快照，让回滚动作本身成为链上新节点。

**❌ 错误**
- 不存档就直接 Edit SOUL.md —— 改了才发现写错，旧版已无处可寻。
- 不加 pre-restore 兜底就覆盖当前状态恢复 —— 恢复目标选错时连错误现场都丢了。
- 看到 verify 的 JOURNAL 报 CHANGED 就惊慌回车 rollback —— 追加式日志本来就该变。

## 给维护者的建议（Maintainer notes）

- 快照目录可选放进 .gitignore；若 agent 数据已纳入版本控制，快照与版本控制二选一即可，勿重复。
- 大 agent（多会话并行）建议在「每次会话启动」和「每次会话结束」双节点快照，保证任意时点都有档可回。
- 若 agent 有跨机器同步（如 WebDAV/云盘），把 `snapshots\` 一并同步，「远程误删」也能找回历史。
- 版本迭代时在 REASON.txt 里写清原因（manual / pre-restore-* / 会话启动），list 一眼可读。

## 更新日志（Changelog）

- v1.0.0（2026-09-07）：初版。沉淀 self-rollback 部署流程：三层防线、可移植 rollback.ps1（snapshot/list/restore/verify + pre-restore 兜底）、自律规则模板、铁律与自检清单。来源于真实 Agent 误操作回滚机制的项目要求与实施经验，全部脱敏。