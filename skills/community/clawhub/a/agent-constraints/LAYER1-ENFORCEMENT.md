# 第 1 层：确定性执行

hooks 与权限规则由客户端强制执行，与模型的决定无关。**凡是不能失败的约束都属于这一层。**

以下语法均取自 Claude Code 官方文档。其他 agent 的机制不同，不要照搬。

**检查器不是执行门。** linter、formatter、类型系统和测试只有接入 CI required check、pre-commit、PostToolUse 或 Stop hook 后，才构成第 1 层约束。单独存在的配置只能判定结果，不能保证它会被运行。怎么接见下一节。

---

## 把检查器接成执行门

检查器（linter / formatter / 类型检查 / 测试）判定结果，门决定它会不会被运行、以及不过时会发生什么。同一个检查器可以接进多道门，**门越晚，反馈越慢但越难绕过**。

| 门 | 什么时候跑 | 绕不绕得过 | 适合 |
|---|---|---|---|
| `PostToolUse` hook | 每次 Write/Edit 之后 | agent 绕不过；人手改文件绕得过 | 快的检查：format、lint 单文件、类型检查 |
| `Stop` hook | agent 想结束回合时 | 连续 8 次阻止后强制结束，**不是绝对保证** | 交付门：全量测试、构建 |
| pre-commit | `git commit` 时 | `--no-verify` 一个参数就绕过；克隆后不装就不存在 | 提交前的快速拦截，**不能当红线** |
| CI required check | push / PR 时 | 设为 required 后合不进去，**唯一挡得住人的一道** | 真正的红线 |

**选门的两个判据**：

1. **失败成本**——错误合进主干才发现的代价有多大。代价高的必须有 CI required check 兜底，前面几道只是让反馈来得早一点。
2. **执行时机**——检查跑多久。秒级的放 `PostToolUse`，分钟级的别放，那会让每次编辑都卡住；放 `Stop` 或 CI。

同一条规则接多道门不是浪费：`PostToolUse` 让 agent 当场自己修，CI required check 保证漏了也进不去。

### pre-commit

`.pre-commit-config.yaml` + `pre-commit install`。**注意它有两个天然缺口**：hook 装在本地 `.git/hooks/`，克隆仓库的人不跑 `install` 就等于没有；`git commit --no-verify` 无条件跳过。所以它是「早点发现」的工具，红线要另外放 CI。

```yaml
repos:
  - repo: local
    hooks:
      - id: tests
        name: tests
        entry: sh tests/run.sh
        language: system
        pass_filenames: false
```

### CI required check

**光有 workflow 不算门。** workflow 跑红了、PR 照样能合，那它还是检查器。要变成门，得在仓库设置里把这个 check 标成 required：

- GitHub：Settings → Branches → Branch protection rule → Require status checks to pass，勾上 job 名（**是 job 名，不是 workflow 名**）
- 这一步**在 workflow 文件里配不了**，必须在仓库设置或 API 里做。写完 CI 就说"接上执行门了"是这里最常见的错。

给 agent 用的仓库还要注意：workflow 只在 push / PR 时跑，**agent 在本地干的活它一概看不到**。要在会话内就拦住，还得配 `PostToolUse` 或 `Stop` hook。

---

## 权限规则

写在 `settings.json` 的 `permissions` 下，三个数组：`allow`、`deny`、`ask`。

```json
{
  "permissions": {
    "allow": ["Bash(npm run *)", "Bash(git commit *)"],
    "deny":  ["Bash(git push *)", "Edit(/migrations/**)"]
  }
}
```

生效位置（后者覆盖前者的范围）：`~/.claude/settings.json`（个人全局）、`.claude/settings.json`（项目共享）、`.claude/settings.local.json`（个人本地，应 gitignore）、managed policy（组织级，不可被覆盖）。

### Bash 规则

`*` 匹配任意文本（含空格）。**`*` 必须放在子命令之后**——Claude Code 把第一个 `*` 之前的内容按字面匹配：

| 写法 | 含义 |
|---|---|
| `Bash(git log *)` | 只放行 `git log` 系列 |
| `Bash(git *)` | 放行**所有** git 命令 |
| `Bash(npm run build)` | 只精确匹配这一条，`npm run build --watch` 不匹配 |

allow 规则里 `*` 出现在子命令之前（如 `Bash(git * main)`）会在启动时告警。

### 文件路径规则

**只有 `Edit(...)` 和 `Read(...)` 两种会被文件权限检查真正读取。**

写 `Write(docs/**)`、`NotebookEdit(...)`、`Glob(...)` 的路径规则，Claude Code 会接受但**永不consult**，只在启动时告警。用 `Edit(docs/**)` 代替 `Write(docs/**)`，用 `Read(docs/**)` 代替 `Glob(docs/**)`。

`Read` 的 deny 规则会连带挡住同路径的 Edit 和 Write（**但不含 NotebookEdit**——要完全禁改，额外加一条 `Edit` deny）。

路径用 gitignore 语法，四种锚定方式：

| 写法 | 锚点 | 例 |
|---|---|---|
| `//path` | 文件系统根 | `Read(//Users/alice/secrets/**)` |
| `~/path` | home 目录 | `Read(~/Documents/*.pdf)` |
| `/path` | **settings 文件所在的那个作用域**，不是文件系统根 | `Edit(/src/**/*.ts)` → `<主工作目录>/src/**/*.ts` |
| `path` 或 `./path` | 当前目录 | `Read(*.env)` |

> 单个前导斜杠**不是**绝对路径。`/Users/alice/file` 锚在 settings 作用域，绝对路径要写 `//Users/alice/file`。

深度语义在 allow 与 deny 之间不同：

- **allow 规则**：`Edit(src/**)` 只匹配 `<cwd>/src`。要匹配任意深度得写 `Edit(**/src/**)`。
- **deny / ask 规则**：`Read(secrets/**)` 匹配当前目录下**任意深度**名为 `secrets` 的目录。

裸文件名按 gitignore 语义匹配任意深度：`Read(.env)` 等价于 `Read(**/.env)`。

### 按参数匹配

deny 和 ask 规则可以匹配顶层输入参数：`Agent(model:opus)`、`Bash(run_in_background:true)`。

**但匹配不到工具的主内容字段**——Bash 的 `command`、Read/Edit/Write 的 `file_path`、Grep/Glob 的 `path`、WebFetch 的 `url`。写 `Bash(command:rm *)` 会被**忽略并在启动时告警**（因为复合命令能绕过它），要写 `Bash(rm *)`。

### 权限规则管不到的地方

Read/Edit 的 deny 规则作用于内置文件工具，以及 Claude Code 能识别的 Bash 文件命令（`cat`、`head`、`tail`、`sed`）。**它挡不住任意子进程**——一个自己 open 文件的 Python 或 Node 脚本不受约束。需要 OS 级隔离就开 sandbox。

---

## Hooks

写在 `settings.json` 的 `hooks` 下。常用事件：

| 事件 | 时机 | 能否阻止 |
|---|---|---|
| `PreToolUse` | 工具调用执行前 | **能** |
| `PostToolUse` | 工具调用成功后 | 不能（已执行），但能把信息回传给 Claude |
| `Stop` | Claude 结束回合时 | **能**（阻止结束，继续对话） |
| `UserPromptSubmit` | 提交 prompt、Claude 处理前 | — |
| `SessionStart` | 会话开始或恢复 | — |
| `InstructionsLoaded` | CLAUDE.md 或 `.claude/rules/*.md` 被加载时（`session_start`、`nested_traversal`、`path_glob_match`、`include`、`compact` 五种 reason） | — |

（完整事件表还包括 `PermissionRequest`、`PostToolUseFailure`、`SubagentStop`、`PreCompact`、`SessionEnd` 等，需要时查官方文档。）

### 通用结构

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/lint.sh",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

matcher 语法：`"*"` 或省略 = 全匹配；`"Bash"` 精确；`"Edit|Write"` 多选；也支持 JavaScript 正则如 `"mcp__.*"`。**`Stop` 不支持 matcher**，每次都触发，配置直接是扁平数组。

handler 的 `type` 除 `command` 外还有 `http`、`mcp_tool`、`prompt`、`agent`。

### 阻止动作

**退出码 2 是主要机制。** 阻止原因取自 stderr。

| 事件 | 退出码 2 的效果 |
|---|---|
| `PreToolUse` | 阻止工具调用 |
| `PostToolUse` | 工具已执行、不可撤销；stderr 展示给 Claude |
| `Stop` | 阻止结束，继续对话 |

也可以用 JSON 输出精确控制：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "该目录禁止修改，请改为新增迁移文件"
  }
}
```

`permissionDecision` 取 `"allow"` / `"deny"` / `"ask"`。Stop 事件不用 `hookSpecificOutput`，用顶层的 `decision` 和 `reason`：

```json
{
  "decision": "block",
  "reason": "测试未全绿，继续修复"
}
```

`decision` 是顶层的遗留字段，取值 `approve` / `block`；`PostToolUse`、`Stop`、`UserPromptSubmit` 用 `"block"`，`block` 时 `reason` 必填——它是交给 Claude 看的续跑理由。**不写 `decision` 就是不阻止**，别写 `"decision": "continue"`，那不是有效值。（`PreToolUse` 上这个字段已废弃，改用 `hookSpecificOutput.permissionDecision`。）

另有一组并行的通用字段：`continue` 默认 `true`，设成 `false` 让 Claude Code 整个停下来；`stopReason` 是 `continue` 为 false 时展示的信息。两者别混用：要它继续干活用 `decision: "block"`，要它彻底停用 `continue: false`。

退出码与 JSON 的优先级：退出码 2 无条件阻止；退出码 0 且 JSON 合法时由 JSON 决定；**退出码 0 且 JSON 非法或缺失时走正常权限流程，不会自动放行**；超时本身不阻止。

### 常用配方

**编辑后自动跑检查**——`PostToolUse` + matcher `Write|Edit`，脚本里跑 lint，失败时 `exit 2` 把错误交回 Claude 自行修复。

**结束前必须全绿**——`Stop` hook 跑测试，不通过 `exit 2`。注意 Claude Code 在**连续 8 次阻止后会强制结束回合**，所以这不是无限循环，但也意味着它不是绝对保证。

**动态拦截**——`PreToolUse` 读 stdin 的 JSON（含 `tool_name`、`tool_input`），按内容判断后 `exit 2`。比静态 deny 规则灵活，代价是要自己维护脚本。

### 写 hook 的原则

- **hook 是接住尾巴的，不是复述文件的。** 已经写在 AGENTS.md 里的话不要再用 hook 说一遍——要么让 hook 真的执行检查，要么删掉文件里那行。
- 优先用现成的退出码。让 linter/测试自己判定成败，hook 只负责调用和传递。
- `Stop` hook 会拖长每个回合，只用于真正的交付门禁。
- Claude 能替你写 hook。直接说"写一个在每次编辑后跑 eslint 的 hook"。
- **验证一律靠实测**：真的触发一次，看它有没有 fire。`/hooks`、`/doctor`、`/context` 这些只在交互式终端里能打开，其他客户端未必可用，不要把它们当作唯一验证手段。
