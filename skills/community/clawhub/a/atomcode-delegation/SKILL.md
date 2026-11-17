---
name: "atomcode-delegation"
description: "通过 atomcode CLI 无头模式委派独立代码任务，支持单任务/批量并发、监控、超时、续会话。"
---

# AtomCode Delegation Skill

> 通过 atomcode CLI 无头模式委派独立代码任务。

## 触发条件

当用户说以下关键词时激活：
- "用 atomcode 修..." / "atomcode 改..."
- "委派给 atomcode"
- "atomcode 任务"
- 批量代码修改任务需要并行执行

## 前置检查

```bash
command -v atomcode >/dev/null 2>&1 || { echo "ERROR: atomcode not found in PATH"; exit 1; }
mkdir -p /tmp/atomcode-tasks /tmp/prompts
```

## 核心命令

```bash
atomcode -C "<workdir>" \
  --prompt-file "<prompt_file>" \
  -y \
  --provider "<provider>" \
  --max-turns <N>
```

> **提示**：优先用 `--prompt-file` 而非 `-p "$(cat ...)"`：
> - 不丢失末尾换行、不触发 shell 分裂/通配符展开、不截断内容

### 参数速查

| 参数 | 必选 | 说明 |
|---|---|---|
| `-C <dir>` | ✅ | 工作目录（务必引号包裹） |
| `--prompt-file <path>` | ✅ | 从文件读取 prompt（推荐） |
| `-p <prompt>` | ✅ | 直接传 prompt 字符串（替代 `--prompt-file`） |
| `-y` | ✅ | 跳过权限确认（后台任务必加，否则挂起） |
| `--provider` | ✅ | 模型后端（见下方 Provider 选择） |
| `--max-turns` | ✅ | 回合限制（简单=12，复杂=20-30） |
| `--model` | 可选 | 覆盖 provider 中的 model 名称 |
| `--engine` | 可选 | 引擎选择：`v2`（默认）/ `v1`（legacy 回退） |
| `-c` | 可选 | 续接上一次中断的会话 |
| `--dev` | 推荐 | 禁用自动更新（批量任务推荐） |
| `-v` | 可选 | stderr 显示工具调用、token 用量、回合摘要 |
| `--no-telemetry` | 可选 | 禁用本次调用的遥测 |
| `--lang <lang>` | 可选 | 设置界面语言：`en` / `zh-CN` / `zh` |
| `--disable-tools <names>` | 可选 | 排除指定的工具（逗号分隔） |

### Provider 选择

> Provider 名称来自 `~/.atomcode/config.toml` 中 `[providers.*]` 的标识符。

| Provider | 模型 | 场景 |
|---|---|---|
| `AtomGit-deepseek-v4-flash` | deepseek-v4-flash | 代码修改、bug fix、重构（默认，100 万 token 窗口） |
| `AtomGit-GLM-5.2` | GLM-5.2 | 复杂架构设计、多文件协调（20 万 token） |
| `AtomGit-Qwen-Qwen3-VL-8B-Instruct` | Qwen/Qwen3-VL-8B-Instruct | 图像理解、视觉分析任务（6.4 万 token） |

## 标准流程

### 1. 准备 prompt

```bash
cat > "/tmp/prompts/<task_id>.txt" << 'PROMPT'
# 任务标题
## 背景
问题描述、涉及的代码位置、预期行为 vs 实际行为。
## 修改要求
1. 先 read 相关文件，理解当前实现
2. 具体修改内容（不要只说"修复 bug"，要说明改什么、怎么改）
3. 保持现有代码风格和注释
## 约束
- 不要新增不必要的依赖
- 不要修改未在要求中列出的文件
## 验证
python3 -c "import ast; ast.parse(open('<file>').read())"
PROMPT

if [ ! -s "/tmp/prompts/<task_id>.txt" ]; then
  echo "ERROR: prompt file is empty or was not written"; exit 1
fi
```

**Prompt 规范**：

| 原则 | 说明 |
|---|---|
| **角色设定** | prompt 开头给 agent 一个角色 |
| **先读后改** | 要求 agent 先 `read_file` 再着手修改 |
| **具体不要模糊** | ❌ "修复性能" → ✅ "将 list 推导替换为 generator" |
| **约束在前** | 明确"不改什么"比"改什么"更重要 |
| **验证命令附后** | 末尾嵌可运行的验证命令 |
| **--prompt-file 优先** | 比 `-p "$(cat ...)"` 更安全（无截断风险、保留末尾换行） |

### 2. 验证工作环境

```bash
if [ ! -d "<workdir>" ]; then
  echo "ERROR: workdir <workdir> does not exist"; exit 1
fi
cd "<workdir>"
git rev-parse --git-dir >/dev/null 2>&1 || echo "WARNING: not a git repo"
```

### 3. 启动任务

```bash
# 单任务 —— 保存 PID 以便监控和清理
LOG="/tmp/atomcode-tasks/<task_id>.log"
atomcode -C "<workdir>" \
  --prompt-file "/tmp/prompts/<task_id>.txt" \
  -y --dev \
  --provider AtomGit-deepseek-v4-flash \
  --max-turns 12 \
  > "$LOG" 2>&1 &
ATOMCODE_PID=$!

# 批量并行（≤4 并发保守；≤6 在 RAM ≥16GB 可尝试）
declare -A TASK_PIDS
for tid in r1 r2 r3 r4; do
  LOG="/tmp/atomcode-tasks/${tid}.log"
  atomcode -C "<workdir>" \
    --prompt-file "/tmp/prompts/${tid}.txt" \
    -y --dev \
    --provider AtomGit-deepseek-v4-flash \
    --max-turns 12 \
    > "$LOG" 2>&1 &
  TASK_PIDS[$tid]=$!
done
```

### 4. 监控完成

```bash
# 单个任务
wait $ATOMCODE_PID; EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ] && grep -q "\[done\]" "$LOG" 2>/dev/null; then
  echo "✅ completed"
elif [ $EXIT_CODE -eq 0 ]; then
  echo "⚠️ exit=0 but no [done] — check git diff for partial changes"
else
  echo "❌ FAILED (exit=$EXIT_CODE)"; tail -20 "$LOG"
fi

# 批量检查（精确 PID 匹配，避免 pgrep 子串竞态）
for tid in r1 r2 r3 r4; do
  PID=${TASK_PIDS[$tid]}
  LOG="/tmp/atomcode-tasks/${tid}.log"
  if kill -0 "$PID" 2>/dev/null; then
    echo "⏳ ${tid}: PID=$PID running ($(wc -l < "$LOG") lines)"
  else
    wait "$PID" 2>/dev/null; EC=$?
    if [ $EC -eq 0 ] && grep -q "\[done\]" "$LOG" 2>/dev/null; then
      echo "✅ ${tid}: $(grep '\[done\]' "$LOG" | tail -1)"
    elif [ $EC -eq 0 ]; then
      echo "⚠️ ${tid}: exit=0, no [done]"
    else
      echo "❌ ${tid}: exit=$EC"
    fi
  fi
done
```

**完成检测优先级**：
1. `[done]` marker **且** exit=0 → 确认完成
2. exit=0 但无 `[done]` → `--max-turns` 耗尽，检查 `git diff`
3. exit≠0 → 失败，查看日志尾部
4. 进程仍在运行 → 继续等待或触发超时

### 5. 超时处理

```bash
TIMEOUT=300
(
  sleep $TIMEOUT
  if kill -0 $ATOMCODE_PID 2>/dev/null; then
    echo "TIMEOUT: killing PID=$ATOMCODE_PID after ${TIMEOUT}s"
    kill -TERM $ATOMCODE_PID; sleep 5
    kill -0 $ATOMCODE_PID 2>/dev/null && kill -9 $ATOMCODE_PID
  fi
) &
WATCHDOG_PID=$!
# ⚠️ 任务完成后清理: wait $ATOMCODE_PID; kill $WATCHDOG_PID 2>/dev/null
```

### 6. 验证结果

```bash
cd "<workdir>"
python3 -c "
import ast, sys
for f in ['file1.py', 'file2.py']:
    try:
        ast.parse(open(f).read()); print(f'✅ {f}')
    except SyntaxError as e:
        print(f'❌ {f}: {e}'); sys.exit(1)
"
git diff --stat
```

## 失败处理

| 症状 | 原因 | 处理 |
|---|---|---|
| 进程卡住无输出 | 卡在 shell tool | `kill <PID>` 并重试，或加 `--engine v1` |
| 无 `[done]` 但 exit=0 | `--max-turns` 耗尽 | 检查 `git diff`；用 `-c` 续接继续 |
| 语法错误 | 输出不完整 | 手动修复或降低 `--max-turns` 重试 |
| token 超限 | 任务太复杂或 prompt 过长 | 拆分为更小的子任务 |
| v2 引擎异常 | 新版引擎 bug | 加 `--engine v1` 回退 legacy |
| atomcode 不可用 | 未安装或不在 PATH | 检查 `command -v atomcode` |
| prompt 为空 | heredoc 写入失败 | 检查文件权限、磁盘空间 |

## 注意事项

- **原子化**: 每个任务只改独立文件集，不互相依赖
- **max-turns 必填**: 防止无限循环
- **-y 务必加**: 后台任务无 stdin，不加 `-y` 会永久挂起
- **--dev 推荐**: 批量任务防自动更新打断
- **续会话用 -c**: `atomcode -C <dir> -c -y --max-turns 12` 续接中断任务
- **--prompt-file 优先**: 比 `-p "$(cat ...)"` 更安全
- **PID 追踪**: 始终保存 `$!`，不用 `pgrep` 子串匹配
- **引号保护**: 所有路径变量用双引号包裹
- **超时守护**: 后台任务务必配超时
- **清理**: `rm -f /tmp/atomcode-tasks/<task_id>.log /tmp/prompts/<task_id>.txt`

## End-to-End 示例

```bash
TASK_ID="fix_auth_bug"; WORKDIR="$HOME/code/my-project"
command -v atomcode >/dev/null || exit 1
mkdir -p /tmp/atomcode-tasks /tmp/prompts

cat > "/tmp/prompts/${TASK_ID}.txt" << 'PROMPT'
# 修复 auth.py token 过期判断
## 修改要求
1. read auth.py 确认当前实现
2. 修改 check_token(): 比较 current_time 与 token.expires_at
3. 输出 git diff --stat
## 验证
python3 -c "import ast; ast.parse(open('auth.py').read())"
PROMPT

[ -d "$WORKDIR" ] || exit 1
LOG="/tmp/atomcode-tasks/${TASK_ID}.log"
atomcode -C "$WORKDIR" --prompt-file "/tmp/prompts/${TASK_ID}.txt" -y --dev \
  --provider AtomGit-deepseek-v4-flash --max-turns 12 > "$LOG" 2>&1 &
PID=$!
(sleep 300; kill -TERM $PID 2>/dev/null; sleep 5; kill -9 $PID 2>/dev/null) &
WD_PID=$!
wait $PID; EXIT=$?; kill $WD_PID 2>/dev/null
if [ $EXIT -eq 0 ]; then
  echo "✅ $TASK_ID"; cd "$WORKDIR" && git diff --stat
else
  echo "❌ $TASK_ID: exit=$EXIT"; tail -10 "$LOG"
  echo "💡 续接: atomcode -C $WORKDIR -c -y --max-turns 8 --provider AtomGit-deepseek-v4-flash"
fi
rm -f "$LOG" "/tmp/prompts/${TASK_ID}.txt"
```
