# CLI 参考 — Codex CLI 正确用法

> 基于 `codex --help` 和 `codex exec --help` 官方输出

---

## ⚠️ PTY 模式必须

Codex 是交互式 CLI，**必须用 PTY wrapper**，否则输出损坏或卡死。

**macOS PTY wrapper：**
```bash
script -q /dev/null <command>
```

**正确示例：**
```bash
script -q /dev/null env OPENAI_API_KEY_0011AI="<key>" codex --full-auto exec "<task>"
```

---

## ⚠️ Git Repo 必须（可跳过）

Codex 默认要求在 git 目录下运行。可用 `--skip-git-repo-check` 跳过。

```bash
codex exec --skip-git-repo-check "..."
```

---

## exec 核心参数

| 参数 | 效果 |
|------|------|
| `exec "prompt"` | 一次性执行，退出 |
| `--cd <DIR>` | **指定工作目录**（ Codex 会 cd 进入再操作） |
| `--full-auto` | 等价于 `-a on-request --sandbox workspace-write` |
| `--dangerously-bypass-approvals-and-sandbox` | 跳过所有确认 + sandbox（真正的 yolo）|
| `--sandbox <mode>` | `read-only` \| `workspace-write` \| `danger-full-access` |
| `--skip-git-repo-check` | 跳过 git 仓库检查 |
| `--add-dir <DIR>` | 在工作区之外增加可写目录 |
| `-o <FILE>` / `--output-last-message <FILE>` | 将最后一条消息写入文件 |
| `--json` | 输出 JSONL 格式的事件流 |
| `--ephemeral` | 不持久化 session 文件到磁盘 |
| `--model <model>` | 指定模型，如 `o3`、`o4-mini` |
| `--search` | 启用实时网络搜索 |
| `--resume` | 恢复之前的 session |
| `-i <FILE>` / `--image <FILE>` | 附加图片（多模态输入）|

### sandbox 模式

| 模式 | 说明 |
|------|------|
| `read-only` | 只读，不能写文件 |
| `workspace-write` | 允许在工作区写文件 |
| `danger-full-access` | 无限制，危险 |

### 审批模式（`-a / --ask-for-approval`）

| 模式 | 说明 |
|------|------|
| `untrusted` | 只运行受信任命令（ls、cat 等），其他提示用户 |
| `on-request` | 模型自行决定何时请求审批 |
| `never` | 从不请求审批，非交互运行使用此模式 |

---

## 工作目录指定

**用 `--cd <DIR>` 指定工作目录：**

```bash
codex --cd /path/to/project exec "重构这个模块"
```

Codex 会自动 cd 进入该目录并以它为工作区根目录。

---

## 任务参数安全转义

使用 Python `shlex.quote()` 转义，防止 `$` `` ` `` `"` 等字符破坏命令：

```python
import shlex
task_safe = shlex.quote(task)
```

---

## codex-call.sh 实际实现

```bash
# PTY wrapper + 后台 &
(
    CODEX_CMD="script -q /dev/null env OPENAI_API_KEY_0011AI=\"$KEY\" \
        codex --full-auto exec \
        --cd \"$WORKDIR\" \
        -o \"$SUMMARY_FILE\" \
        -- \"$TASK\""
    bash -c "$CODEX_CMD" >/dev/null 2>&1 &
    PID=$!
    echo "$PID" > "$LOCK_FILE"
) &

# 主进程立即返回 {"task_id":"...","pid":...}
```

---

## 交互模式 vs exec 模式

| 特性 | `codex`（交互） | `codex exec`（非交互） |
|------|----------------|----------------------|
| session 持久化 | ✅ 自动保存 | ❌（用 `--ephemeral` 可禁用） |
| 恢复 session | `codex resume` | `codex exec --resume` |
| 适合场景 | 探索性开发 | 脚本化任务 |
| TTY 要求 | ✅ 需要 | ❌ 不需要 |

---

## 已知限制

| 问题 | 说明 |
|------|------|
| `codex exec` 不支持 `--session-id` | session 持久化走 `codex resume` |
| `--resume` 需要 session 文件 | session 文件默认保存在 `~/.codex/sessions/` |
| 每次 exec 都是新 session | 无法携带上一次对话的上下文（用 `exec --resume` 补救）|

---

## 好的提示词示例

```
帮我写一个 Python 爬虫，爬取豆瓣 Top250，要求：
1. 使用 requests + BeautifulSoup
2. 支持翻页
3. 保存 CSV
4. 加请求间隔防封
```

越具体，Codex 执行越准确。

---

*来源：`codex --help` + `codex exec --help`（2026-04-05）*
