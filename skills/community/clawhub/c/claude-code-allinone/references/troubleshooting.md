# 故障排查 — 看 doctor.sh 的 issues / 看 claude code 报错信息,对照下表给用户处方

> v3.1 现网验证后总结的踩坑清单。每条都给出"原因 → 处方"。

## 按现象索引

### 1. `command not found: claude`

**原因**:npm 全局 bin 不在 PATH。

**处方**:
```bash
bash scripts/install.sh   # install 会自动写 PATH 到 .bashrc
source ~/.bashrc
```

### 2. doctor.sh 显示 `claude_outdated=true`

**原因**:claude code 版本 < 2.1.0,部分参数(如 `--permission-mode plan`)不存在。

**处方**:
```bash
bash scripts/install.sh   # 会自动升级到最新
```

### 3. `Onboarding has not been completed`

**原因**:`~/.claude.json` 缺少 `hasCompletedOnboarding: true`,Claude Code 在非交互模式 (`-p`) 下会直接 abort。

**处方**:
```bash
bash scripts/ensure-onboarding.sh   # 幂等设置,可反复跑
```

每次 setup-* 脚本都会自动跑这一步,正常情况下用户碰不到。

### 4. `ANTHROPIC_AUTH_TOKEN is not set` / `401 Unauthorized`

**原因**:Key 没生效。可能的具体场景:
- `~/.claude/.token` 文件不存在或为空
- 当前 shell 没 source `~/.bashrc`(环境变量没生效)
- 用户用了错误的 Key (AgentPlan 专属 Key vs 普通 v3 Key 混淆)

**处方**:
```bash
# 看 token 文件
ls -la ~/.claude/.token
wc -c < ~/.claude/.token   # 应该非 0

# 看当前激活 profile 是哪个
cat ~/.claude/active-profile

# 重跑对应 setup
bash scripts/setup-agentplan.sh "<正确的 AgentPlan Key>"
# 或
bash scripts/setup-custom.sh "<base_url>" "<Key>" "<model>"
```

### 5. `403 Forbidden` / 模型在某些 base_url 下不存在

**原因**:base_url 与 Key 不匹配,或者 model 名错误。

**处方**:
- AgentPlan 路径必须 model = `ark-code-latest`
- 自定义网关的 model 名必须是网关那边能识别的(常见误区:把 `claude-3-5-sonnet` 缩写成 `sonnet`)

```bash
# 看当前 settings.json
cat ~/.claude/settings.json
```

### 6. ArkClaw / OpenClaw 沙箱里 claude 一直挂死,无任何输出

**原因**:十有八九是主对话 Agent 调用 Skill 时叠加了 `pty: true`,导致 `</dev/null` 隔离失效,claude 在等 stdin。

**处方**(给主对话 Agent 看):
- 调用 run.sh 时 **不要** 在执行器里启用 PTY
- 直接用 bash 执行 `bash /path/to/skill/scripts/run.sh "<需求>"`,不要走伪终端通道
- run.sh 内部已经做好了 `nohup setsid + </dev/null + log file + 110s 超时` 三件套

如果你不是用 Skill 调用,而是手工跑 claude:
```bash
# 错误示范
claude -p "改个东西"   # 在某些 sandbox 里会等 stdin,挂死

# 正确示范
nohup setsid claude -p "改个东西" --allowedTools "Read,Edit,Write,Bash" </dev/null > /tmp/claude.log 2>&1 &
sleep 60
cat /tmp/claude.log
```

### 7. claude 报 `Input must be provided through stdin or as a prompt argument`

**原因**:你忘了 `-p`,或者 PTY 模式让 claude 以为要从 stdin 读。

**处方**:
- 必须用 `-p "<prompt>"` 传需求(而不是 echo "..." | claude)
- Skill 调用方禁止 PTY

### 8. claude 报 `unknown permission-mode: accept`

**原因**:用了不存在的 mode 值。

**合法值**:`acceptEdits | auto | bypassPermissions | default | dontAsk | plan`

**处方**:本 skill 只用 `plan` (review 模式) 和 `--allowedTools` (build 模式),不要自己改其他 mode。

### 9. build 模式跑完没改文件

**可能原因**:
- 用户的 prompt 里没有"修改"语义,claude 自己也判定不需要改
- `--allowedTools` 白名单不够(比如要装 npm 包但白名单里没 Bash)
- 工作目录不是预期目录

**处方**:
```bash
# 显式指定工作目录
bash scripts/run.sh --cwd /path/to/repo --mode build "明确说要改什么"

# 看完整日志
ls -lt ~/.claude-runs | head -5
cat ~/.claude-runs/run-build-XXX.log
```

### 10. review 模式 claude 输出了改文件的代码块,但没真改

**这是预期行为**:`--permission-mode plan` 就是只读分析,只输出方案/diff,不真去改。
如果用户想动手,改用 build 模式:
```bash
bash scripts/run.sh --mode build "<需求>"
```

### 11. `~/.claude/settings.json` 被覆盖,我之前的自定义配置丢了

**原因**:setup-* / switch-profile.sh 会覆盖 settings.json。但脚本会先备份。

**处方**:
```bash
ls -lt ~/.claude/settings.json.bak.*
# 找到最近的备份,人工合并你需要的字段
```

### 12. 切换 profile 后还是用旧的 base_url

**原因**:settings.json 没真的被替换,或者主进程里有 cached 环境变量。

**处方**:
```bash
# 看当前 settings.json 实际内容
cat ~/.claude/settings.json

# 看 active-profile marker
cat ~/.claude/active-profile

# 重跑 switch
bash scripts/switch-profile.sh agentplan
```

### 13. 沙箱重启后挂了

**原因**:某些 Key 没持久化(只在当前 shell 环境)。

**处方**:本 skill 的 setup-* 脚本会写 `export ARK_API_KEY="..."` 到 ~/.bashrc。`~/.claude/.token` 文件也是磁盘持久的。`source ~/.bashrc` 即恢复。如果还不行:
```bash
grep -E '(ANTHROPIC|ARK_API_KEY|CUSTOM_ANTHROPIC_KEY)' ~/.bashrc
ls -la ~/.claude/{.token,settings.json,active-profile}
```

### 14. doctor.sh 显示 `claude_installed=false` 但你确定装过

**原因**:npm 全局 bin 不在当前 shell 的 PATH。

**处方**:
```bash
ls $HOME/.npm-global/bin/claude   # 看实际位置
export PATH="$HOME/.npm-global/bin:$PATH"
which claude
```

### 15. `failed to load skill ... missing YAML frontmatter`

**原因**:同目录下有其他 Skill 的 SKILL.md 格式错了(不影响本 skill 自身)。

**处方**:可忽略;或者把那个有问题的 skill 目录删了。

## 兜底:把 doctor.sh 完整输出贴给我

如果上面都对不上,让用户:
```bash
bash scripts/doctor.sh
```
把完整 JSON 贴回来,Skill 根据 issues 数组逐项处理。
