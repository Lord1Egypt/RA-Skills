# +connect 详细参考

> **前置：** 先读 [`../SKILL.md`](../SKILL.md)。本文件只补充上面没写的细节。

## Agent 必读要点（不要跳过）

1. 子命令穷举：`(空)` / `list` / `uninstall`。**不存在** install / setup / sync / remove。`--path` 是 flag，不是子命令。
2. 默认行为 = 安装；不要写 `arkcli +connect install`。
3. 安装走 **authoritative catalog update**：当前 CLI catalog 的每个精确名称一律覆盖现有同名目录；旧 manifest 中已退出 catalog 的名称一律删除。
4. 其他不同名且从未被 manifest 管理的目录默认保留。目录摘要不阻断安装，但 `uninstall` 默认仍只删除摘要未变化的 managed skills。
5. `--path <skills-dir>` 表示"指定的 skills 目录"，不是项目根目录。相对路径按当前 `PWD` 解析，绝对路径原样使用。
6. `--path` 模式是隔离操作：只在该目录收敛当前 catalog 与旧 manifest，并保留其他不同名条目；不扫描 agent、不清 legacy 私有目录、不删除 `byted-ark-*` conflicting skills、不 patch Claude/opencode 等 harness 配置。
7. `list` 是只读，不需要认证；其他子命令也不需要认证。
8. 多个 agent 共享同一 skills 目录时，按路径自动去重，只更新一次。Codex / Pi 统一安装到 `~/.agents/skills`；legacy 私有目录只删除带旧 manifest 的 owned Skills，或与当前官方树逐字节一致的迁移副本，未知/修改过的同前缀条目保留。
9. `npm install` 触发的 postinstall 在交互式终端上**自动**跑 `+connect`，不再问 `[y/N]`；CI / 非交互终端静默跳过；详见下文「postinstall 行为」。

## 行为细节

1. 扫描 40+ 个已知 agent 的 skills 目录路径（如 `~/.claude/skills/`、`~/.cursor/skills/`）
2. 父目录存在即判定为"已检测到"
3. 对每个检测到的 agent：先把当前 catalog 写入隐藏 staging，再把当前 catalog 名称和旧 manifest 名称一起备份，原子收敛 Skills 和 manifest；任一步失败都回滚
4. 按 `skillsDir` 去重

共享安装目录只计为一个目标；同时存在 Codex / Pi 这类 agent 自己的检测目录时，
展示名称优先使用该独立信号，避免仅因 `~/.agents` 已存在而把目标误标成 Cline。

当前 catalog 是安装后的权威状态：同名目录无论来源和内容都由当前版本覆盖，旧
manifest 记录但已退出 catalog 的名称会删除。其他既不在当前 catalog、也不在旧
manifest 的不同名目录保持不变。旧 BytePlus `arkcli-managed-agent` 因此自然退休，
canonical `arkcli-agent` 正常安装，不需要单独的产品或摘要特判。

`--path` 模式跳过上面的 agent 扫描：

1. 解析 `<skills-dir>`：相对路径基于当前 `PWD`，绝对路径保持原样
2. 创建目标目录
3. 覆盖当前 catalog 的全部精确同名目录，删除旧 manifest 中已退出 catalog 的名称；其他不同名条目保持不动
4. 把当前 Skills 写入目标目录，并原子更新 `.arkcli-managed-skills.json`

示例：

```bash
cd /path/to/repo
arkcli +connect --path .claude/skills
arkcli +connect uninstall --path .claude/skills
```

落盘结构：

```text
/path/to/repo/.claude/skills/arkcli-chat/SKILL.md
/path/to/repo/.claude/skills/arkcli-gen/SKILL.md
/path/to/repo/.claude/skills/.arkcli-managed-skills.json
...
```

## 输出示例

手动运行 `arkcli +connect`：
```
Detected N agent(s): claude-code cursor gemini-cli
Installing M skill(s)...

  updated 3 managed + installed M → claude-code (~/.claude/skills)
  installed M → cursor (~/.cursor/skills)

Done. Installed M skill(s) × N agent(s) = total.
```

npm postinstall 自动安装：
```
✓ 已将 ArkCLI Skills 安装到 N 个 AI Agent（claude-code/ codex/ opencode）。
  如需移除 ArkCLI 安装的 Skills：arkcli +connect uninstall
```

安装到指定目录：
```
Installing M skill(s) to /path/to/repo/.claude/skills...

  updated K managed + installed M → /path/to/repo/.claude/skills

Done. Installed M skill(s).
```

卸载：
```
Uninstalling skills from N agent(s)...

  removed K skill(s) from claude-code (~/.claude/skills)

Done. Removed total skill(s) total.
```

从指定目录卸载：
```
  removed K skill(s) from /path/to/repo/.claude/skills

Done. Removed K skill(s) total.
```

注意：默认卸载里的 K 只包含 manifest 记录且摘要未变化的 managed Skills。只有用户明确确认并追加 `--purge-prefix` 时，才删除目标中的所有 `ark-` / `arkcli-` 前缀目录或软链。

## postinstall 行为

`npm install` arkcli 时触发 `scripts/postinstall.js`，该脚本：

1. 检查逃生阀：`ARKCLI_SKIP_POSTINSTALL=1` 或 `CI=true` 直接跳过
2. 校验 platform/arch + binary 是否存在；不在支持名单或文件缺失（例如 `--ignore-scripts`）静默跳过
3. 尝试打开 `/dev/tty` 双向 fd；拿不到（管道、Windows 等无 controlling tty 场景）静默跳过
4. 直接以 `+connect` 启动平台对应的 binary，stdout/stderr 接到 tty；成功时只展示唯一安装目标数、对应 Agent 名称和安全卸载命令，不逐目录展开进度明细。自动路径使用同一 authoritative catalog 事务，绝不隐式启用 `--purge-prefix`
5. 任何失败一律 `exit 0`，不阻断 npm 主链；想完全静音设 `ARKCLI_SKIP_POSTINSTALL=1`

## 常见提示与错误

| 消息 | 类型 | 原因 | 处理 |
|------|------|------|------|
| `No AI agents detected` | warning（正常退出） | 本机没有支持的 agent | 先装一个 agent（如 Claude Code）再跑 `+connect` |
| `No skills embedded in this binary` | warning | 编译时未嵌入 skills | `make build` 重新编译 |
| `embedded skills filesystem not initialised` | error | 内嵌文件系统未初始化 | 重新编译二进制 |
| `mkdir ... permission denied` | error | skills 目录无写权限 | 检查目标目录权限 |
| `copy ...: not a directory` | error | 指定目录中存在同名普通文件，无法覆盖成 skill 目录 | 手动移走该文件后重试 |
| `managed Skill ... was modified` | uninstall error | 默认卸载发现目录摘要已变化 | 默认保留该目录；只有明确要求全前缀清理时才确认使用 `--purge-prefix` |

`arkcli-managed-agent` 不是当前可安装 Skill 名。若它由旧 manifest 管理，下一次安装
会按统一 catalog 收敛规则删除它，并在 manifest 和磁盘只保留 `arkcli-agent`。

## 参考

- [arkcli-connect](../SKILL.md) -- skill 入口
- [arkcli-shared](../../arkcli-shared/SKILL.md) -- 共享认证与全局参数
