# 复盘触发机制

约束的触发条件是「**第二次**犯同一个错」——这本质上是跨会话的，单个会话内看不出来。
所以这里不做实时判断，只做**记录 + 定期复盘**。

## 装法

1. 放置脚本（用户级）：

   ```sh
   mkdir -p ~/.claude/hooks
   cp log-session.sh ~/.claude/hooks/
   chmod +x ~/.claude/hooks/log-session.sh
   ```

2. 在 `~/.claude/settings.json` 里注册。两个要点：**`command` 用绝对路径**（`~` 的展开行为未经验证），
   以及**把下面的 `hooks` 键合并进已有的 settings.json，不要整个覆盖**——那个文件里通常还有
   你的 `permissions`、`env` 等配置，覆盖掉会一起丢失。已经有 `hooks` 键的话，
   只把 `SessionEnd` 数组加进去。

   ```json
   {
     "hooks": {
       "SessionEnd": [
         {
           "hooks": [
             {
               "type": "command",
               "command": "/Users/<你>/.claude/hooks/log-session.sh",
               "timeout": 10
             }
           ]
         }
       ]
     }
   }
   ```

   省略 `matcher` 表示全部匹配。只想记特定结束原因时，`matcher` 支持
   `"clear"`、`"resume"`、`"logout"`、`"prompt_input_exit"`、`"other"`。

3. **验证（实测，不要跳过）**：开一个会话再退出，检查
   `~/.claude/constraint-review.log` 是否多了一行。

   这一步不能省。省略 `matcher` 依据的是「省略即全匹配」的通用规则，
   但只有真的跑一次才知道它在你的版本上确实触发了。
   在交互式终端里还可以用 `/hooks` 看已注册的 hook，其他客户端未必能打开这个面板。

日志位置可用 `CLAUDE_CONSTRAINTS_LOG` 环境变量改。

## 这个日志记什么

制表符分隔的五列：时间、工作目录、结束原因、session_id、transcript 路径。

**只记指针，不做内容提取。** transcript 的 JSONL 结构未公开，脚本里解析它会在版本变动时
静默失效。复盘时由 agent 去读这些文件更稳，也更聪明。

## 另一个信号源：auto memory

Claude Code 的 auto memory 本来就在记「你给 Claude 的纠正」，存在
`~/.claude/projects/<project>/memory/` 下，frontmatter 里 `type: feedback` 的那些文件。

这是**已经存在的、经过消化的**信号，比原始 transcript 好读。复盘时两个都看：

- 会话日志 → 哪些会话值得回看，以及总量趋势
- auto memory 的 feedback 文件 → 已经被识别出来的纠正

auto memory 可能被关掉（`autoMemoryEnabled: false` 或
`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`），所以两者互为补充，不要只依赖其一。

## 诚实的边界

**记录 hook 的调用是第 1 层**：客户端对这项配置的触发是确定性的。

脚本依赖 Python 3。**每次运行都会把日志文件 `chmod 600`**——不只是新建时，已存在的日志也会被收紧，因为里面有 cwd 和 transcript 路径。如果你有意把它设成别的权限，这个脚本会覆盖掉。

状态持久化是尽力而为：记录可能因依赖、权限或磁盘失败；错误打到 stderr，可见但不阻止会话退出。

**复盘这一环是第 4 层**，仍然依赖人或 agent 的判断——它不会自己发生，需要你定期发起
（建议每周，或每积累 15–20 个会话一次）。想让它自动发生，就再加一个定时任务去调用复盘流程。

这个分工是刻意的：能确定性执行的部分交给 hook，需要判断的部分不假装它是自动的。
