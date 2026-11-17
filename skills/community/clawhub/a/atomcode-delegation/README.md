# AtomCode Delegation Skill

通过 [AtomCode CLI](https://atomgit.com/atomcode) 无头模式委派独立代码任务，支持单任务/批量并发、监控、超时、续会话。

## 核心能力

| 能力 | 说明 |
|------|------|
| 单任务委派 | 通过 prompt-file 精准下发任务，后台执行 |
| 批量并发 | ≤4 任务并行，PID 追踪，独立超时守护 |
| 续会话 | `atomcode -c` 续接中断任务，不丢失上下文 |
| 超时保护 | 后台 watchdog 进程，自动 kill 防止卡死 |
| 结果验证 | `[done]` marker + git diff + 语法检查三重确认 |

## 支持 Provider

| Provider | 模型 | 上下文窗口 | 场景 |
|----------|------|-----------|------|
| `AtomGit-deepseek-v4-flash` | deepseek-v4-flash | 1,000,000 | 代码修改、bug fix、重构（默认） |
| `AtomGit-GLM-5.2` | GLM-5.2 | 200,000 | 复杂架构设计、多文件协调 |
| `AtomGit-Qwen3-VL-8B` | Qwen3-VL-8B | 64,000 | 图像理解、视觉分析 |

## 快速开始

```bash
# 前置检查
command -v atomcode >/dev/null 2>&1 || { echo "ERROR: atomcode not found"; exit 1; }

# 准备 prompt
cat > /tmp/prompts/fix_bug.txt << 'PROMPT'
# 修复 auth.py token 过期判断
## 修改要求
1. read auth.py 确认当前实现
2. 修改 check_token(): 比较 current_time 与 token.expires_at
## 验证
python3 -c "import ast; ast.parse(open('auth.py').read())"
PROMPT

# 执行任务
atomcode -C "$HOME/code/my-project" \
  --prompt-file /tmp/prompts/fix_bug.txt \
  -y --dev \
  --provider AtomGit-deepseek-v4-flash \
  --max-turns 12
```

## 批量并行

```bash
for tid in fix_auth refactor_db add_test update_docs; do
  atomcode -C "$WORKDIR" \
    --prompt-file "/tmp/prompts/${tid}.txt" \
    -y --dev \
    --provider AtomGit-deepseek-v4-flash \
    --max-turns 12 \
    > "/tmp/atomcode-tasks/${tid}.log" 2>&1 &
  echo "$tid → PID=$!"
done
```

## 安装

### ClawHub（推荐）
```bash
openclaw skills install @vincentlau2046-sudo/atomcode-delegation
```

### Git
```bash
git clone https://github.com/vincentlau2046-sudo/atomcode-delegation.git
cp atomcode-delegation/SKILL.md ~/.openclaw/workspace/skills/atomcode-delegation/
```

## 仓库

| 平台 | 地址 |
|------|------|
| GitHub | <https://github.com/vincentlau2046-sudo/atomcode-delegation> |
| AtomGit | <https://atomgit.com/vincentlau2046/atomcode-delegation> |
| ClawHub | <https://clawhub.ai/vincentlau2046-sudo/atomcode-delegation> |
