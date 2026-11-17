---
name: "ctx-lockstep"
description: "管理 git/非 git 项目的长期上下文与断点恢复。触发场景：继续/恢复之前的项目、提交代码后更新项目进度、会话结束前保存项目状态、接手或纳管一个已有项目、为长期推进的任务建立项目档案。Manage long-term project context and session-resume checkpoints for git and non-git projects. Use when resuming a project, updating progress after commits, saving state before ending a session, adopting an existing project, or archiving a long-running task."
metadata: { "openclaw": { "emoji": "🗂️", "requires": { "bins": ["python3"] } } }
---

# Ctx-Lockstep — 项目上下文管理

- **GitHub**: https://github.com/holdyounger/ctx-lockstep
- **ClawHub**: https://clawhub.ai/skills/ctx-lockstep

基于**文件**的长期项目管理机制。核心特性：**项目状态收敛到项目内单目录 `<项目>/.ctx-lockstep/`**（尊重个人隐私与仓库整洁），**漂移检测由事件驱动机械完成**（git hook + mtime 扫描），不依赖心跳、不依赖模型自觉。

> 本文件的示例均为通用占位数据。真实项目登记在注册表，不写死在 skill 本体。

## 适用场景

- 共享主会话中同时推进**多个长期项目**
- 会话中断/归档后可靠恢复项目状态
- 把项目上下文与普通聊天分开
- 提交代码后进度跟进（drift 检测提醒固化）

## 与主会话的边界

本 skill 管理**项目上下文**，不假装把共享主会话变成隔离的原生项目会话。

## 核心原则

- 不依赖聊天记忆管理长期项目
- 恢复靠文件（`.ctx-lockstep/PROJECT.md`），不靠翻聊天记录
- **固化触发靠机制不靠自觉**：commit 事件机械留痕 + 进入项目时机械检测

## 项目结构（单目录收敛）

每个项目只有一个状态目录，可选 commit 或 gitignore（推荐 gitignore，属 agent 工具产物）：

```
<项目>/.ctx-lockstep/
├── PROJECT.md          # 唯一恢复入口：主线/断点/决策/索引/固化记录 三合一
├── checkpoints/        # 阶段快照（YYYY-MM-DD-主题.md）
└── commits.log         # git 项目: post-commit hook 自动追加；固化后清空
```

- 不再在项目根目录平铺 `00_*/01_*/99_*` 文件（v1 遗留，见下方迁移规则）
- `PROJECT.md` 头部 HTML 注释携带机器可读元数据：`last_checkpoint: <时间戳>`

## 双路径工作环境

同一项目在 Linux(含 WSL) 与 Windows 两端访问时：

- WSL/Linux 访问一律用 POSIX 路径（`/mnt/d/...`）
- `PROJECT.md` 元信息区同时记录 posix 与 win 双路径
- 注册表条目含 `posix_path` 与 `win_path`

## 项目注册表

- 路径：`~/.openclaw/workspace/.ctx-lockstep/projects-registry.json`
- 只记录已被用户确认纳入管理的项目：

```json
{
  "projects": [
    {
      "name": "project-a",
      "posix_path": "/mnt/d/workspace/project-a",
      "win_path": "D:\\workspace\\project-a",
      "note": "示例"
    }
  ]
}
```

## 进入 / 恢复项目流程

1. 读 workspace 级 `PROJECT_SYSTEM.md` 与注册表
2. 扫描已登记项目；有歧义时让用户确认
3. **漂移检测（机械步骤，必做）**：
   ```bash
   python3 {baseDir}/scripts/check_drift.py '<项目路径>'
   ```
   - git 项目 → 读 `.ctx-lockstep/commits.log` 积压（post-commit hook 写入）
   - 非 git 项目 → mtime 晚于 `last_checkpoint` 的文件扫描（近似值）
4. 读 `.ctx-lockstep/PROJECT.md`（恢复入口）
5. 需要时补读最新 `checkpoints/<最新>.md`
6. 输出：当前主线、已完成、当前断点、关键决策、推荐下一步
7. **若 drift > 0：先报告积压，建议先固化再继续**（此时会话已活跃，固化成本≈一次文件追加）

## 退出项目流程

- 用户退出后，后续消息不再默认属于该项目
- **收尾硬规则：本次会话若改过项目代码/文档，退出前必须固化**（把固化绑定到收尾动作，不靠事后想起）
- 普通事务不写入项目记录；后续消息疑似项目相关时提醒确认

## 固化（Checkpoint）流程

用户说"固化/更新恢复文件/保存断点/保存阶段进展"时**立即执行**。固化动作（轻量化）：

1. 更新 `.ctx-lockstep/PROJECT.md`：断点、决策、里程碑、固化记录；**更新头部 `last_checkpoint` 时间戳**
2. 阶段性大节点才写 `checkpoints/YYYY-MM-DD-主题.md` 快照（小步进度只改 PROJECT.md，不产生快照文件）
3. git 项目：**清空 `commits.log`**（积压归零）
4. 更新当日 workspace memory（可选）

主动建议固化的时机：完成关键文档后、断点明显变化后、新决策形成后、进入新阶段、会话将暂停前。**用户拒绝后本次会话不再催，但下次进入项目时 drift 检测仍会如实报告。**

## 项目接管 / 新项目初始化

```bash
python3 {baseDir}/scripts/init_project.py '<JSON>'
```

- 新项目：`{"projects_root": "...", "project_name": "..."}`（项目目录不存在时自动创建）
- **接管已有目录**：`{"existing_path": "/path/to/project"}`
- 公共参数：`create_workspace_rule`(默认 true)、`workspace_root`、`overwrite`

脚本行为：创建 `.ctx-lockstep/` 单目录结构 + 幂等安装 git post-commit hook + 非 git 项目给出 mtime 模式提示（**不擅自 git init**）。

## 漂移检测机制（对用户透明）

| 项目类型 | 事实来源 | 精度 |
|---------|---------|------|
| git 项目 | `.ctx-lockstep/commits.log`（hook 每次 commit 追加一行 JSON） | 精确（commit 级） |
| 非 git 项目 | mtime 扫描（排除 node_modules/build 等，阈值 = `PROJECT.md` 的 `last_checkpoint`） | 近似（文件级） |

- 检测脚本零依赖（纯 Python 标准库）、按需执行（只在进入项目时跑一次）、无常驻进程、无心跳
- hook 失败静默（绝不阻断用户提交）
- 若用户在 agent 之外手动 commit，hook 照样记录（事实层不受影响）

## 旧版结构迁移（旧项目接管）

发现项目根目录有 v1 平铺文件（`00_恢复入口.md`、`00_文档总索引与当前进度.md`、`01_项目会话与恢复机制说明.md`、`99_关键决策记录.md`）时：

1. 建议迁移到 `.ctx-lockstep/PROJECT.md` 单目录（内容合并：恢复原则→删（流程在 SKILL.md）；索引+断点+决策→合并进 PROJECT.md 对应章节）
2. 旧文件删除前征求用户确认（它们通常未 commit）
3. 跑 `init_project.py --existing_path` 补 hook 与目录

## 提示触发规则

- **强触发**：开始新项目 / 以后持续推进 / 给任务建项目管理 / 我已建好目录 / 恢复项目 / 继续之前的项目
- **中触发**（提示一次）：分阶段推进、需持续写文档、需 checkpoint
- **弱触发**（不提示）：一次性问答、临时排查、短脚本、单次查询。**新话题 ≠ 新项目**

## 反打扰规则

- 同一主题只提醒一次；用户拒绝后不短时间内重复催促
- 不擅自创建项目目录/git init，除非用户明确同意

## 脚本

- `scripts/init_project.py` — 初始化/接管（`.ctx-lockstep/` 结构 + hook）
- `scripts/check_drift.py` — 漂移检测（git/mtime 双模式）
