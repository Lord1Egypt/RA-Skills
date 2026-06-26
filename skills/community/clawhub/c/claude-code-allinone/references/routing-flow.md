# 路由流程参考 — Skill 内部决策路径详解

> 这份文档是给 Skill 调用方(主对话 Agent)看的:每次触发时该走哪条分支、判断的是什么、命中后跑哪个脚本。

## 顶层路由(三条路径)

每次 skill 被触发,**第一步**必须先跑 doctor.sh,根据它返回的 JSON 决定走哪一条。

```
bash scripts/doctor.sh > /tmp/cc_doctor.json
```

输出 JSON 关键字段:

| 字段 | 含义 |
|---|---|
| `claude_installed` | claude CLI 是否已装 |
| `claude_outdated`  | 装了但版本低于 2.1.0 |
| `config_state`     | `clean` / `managed-by-skill` / `user-managed` |
| `active_profile`   | 当前激活的 profile 名 (managed-by-skill 时) |
| `user_health`      | user-managed 时的健康检查结果 |
| `onboarding_complete` | `~/.claude.json` 是否已标记 onboarding 完成 |
| `token_set`        | `~/.claude/.token` 是否非空 |
| `issues[]`         | 问题列表(人话) |

### 路径 ① 首次配置 (config_state == "clean")

**核心原则:减少用户感知,默认走 AgentPlan,不主动列菜单。**

- 必要时跑 install.sh
- **默认直接走 AgentPlan**:只问用户一句"请粘贴 AgentPlan 专属 Key",拿到 Key 后跑 `setup-agentplan.sh`
- **仅当用户主动表达**"我有自己的 Anthropic 兼容网关 / 别的 base_url / 自定义模型 / 公司自建网关 / claude-code-router"等关键词时,才走 custom 分支(`setup-custom.sh`)
- ⛔ 用户没主动提"自定义"语义时,**禁止**主动给用户列 A/B 菜单 — 这违背"默认 AgentPlan,无感配置"原则
- setup 脚本会自动把 config_state 切到 managed-by-skill,转到路径 ②

### 自定义分支的触发关键词(仅供参考)

只有用户语句里出现以下任一(或类似)语义,才走 custom 分支:

- "我有自己的 / 我们公司的 / 我们自建的 网关 / base_url / 端点"
- "我有别的 Anthropic 兼容 Key"
- "用 claude-code-router / kimi-router / Bedrock / Vertex"
- "不用 AgentPlan,我有自己的 Key"
- 用户直接给出了 base_url + Key + model 三件套

否则一律默认 AgentPlan,不询问。

### 路径 ② 正常使用 (config_state == "managed-by-skill")

- 跑 ensure-onboarding.sh (幂等,几乎无开销)
- 跑 run.sh "<用户需求>"
- 把 run.sh 的输出原样回给用户
- ⛔ 不要解释流程,不要询问"是否切换",体验要等同于直接对话 claude code

### 路径 ③ 兼容性检查 (config_state == "user-managed")

读 `user_health.is_healthy`:

- `true`  → 当作正常使用,转到路径 ②
- `false` → 把 `user_health.issues[]` 展示给用户,询问是 A. 让本 skill 重配 还是 B. 自己修

---

## 二级路由 — review vs build 模式判定

run.sh 内部通过关键词扫描决定走哪个模式。

| 触发关键词 | 模式 | claude 参数 |
|---|---|---|
| review / Review / REVIEW / 评审 / 审查 / 分析 / 评估 / 检查 / lint / 只读 / read-only | review | `--permission-mode plan` |
| (其他所有情况) | build | `--allowedTools "Read,Glob,Grep,LS,Bash,Edit,Write"` |

也可以由 Agent 显式指定:
```bash
bash scripts/run.sh --mode review "审一下 utils.py"
bash scripts/run.sh --mode build  "把这个 bug 修了"
```

### 为什么要分模式?

| 场景 | 不分模式的后果 |
|---|---|
| 用户只想做 PR review | 默认 build 会真去改文件,造成误改 |
| 用户想动手实现 | 默认 plan 模式只输出方案不动手,用户要手动套一遍 |

review 模式的 `--permission-mode plan` 会让 claude 进入 "看,但不改" 状态。
build 模式的 `--allowedTools` 白名单是 v3.1 现网验证过的最小可用集合,既能完成大多数编程任务,也不会误用危险工具。

---

## 防挂死三件套(必须遵守)

run.sh 启动 claude 时严格遵循:

```bash
nohup setsid claude -p "..." </dev/null > "$LOG_FILE" 2>&1 &
CLAUDE_PID=$!

# 轮询 PID,超过 110s 主动 kill -9
elapsed=0
while kill -0 "$CLAUDE_PID" 2>/dev/null; do
  [ $elapsed -ge 110 ] && { kill -9 "$CLAUDE_PID"; break; }
  sleep 1; elapsed=$((elapsed+1))
done

cat "$LOG_FILE"
```

| 元素 | 作用 | 不能省 |
|---|---|---|
| `nohup setsid` | 完全脱离 controlling tty,不受父进程的信号影响 | 否则父 shell 退出会带走 claude |
| `</dev/null`   | claude 的 stdin 接到 /dev/null,绝不等待输入 | 否则 claude 会陷入"等用户回车"挂死 |
| `> log 2>&1`   | 所有输出落盘,后续 cat | 否则 buffer 满会 SIGPIPE 中断 |
| 110s 轮询超时 | 极限值,超过就 kill -9 取已生成内容 | 否则会无限挂起 |

### ⛔ 主对话 Agent 调用本 skill 时的禁忌

- **禁止叠加 `pty: true`**:许多沙箱执行器有"分配伪终端"开关,一旦打开,会把 stdin 重新接回新 PTY,直接破坏 `</dev/null` 隔离,导致 claude 等输入挂死
- **禁止用 `bypassPermissions`**:run.sh 的 `--allowedTools` 已经给出了安全的最小工具集,bypass 会失去白名单保护
- **禁止把 `--permission-mode` 改成 `acceptEdits` / `dontAsk`**:这些模式在沙箱非交互环境会触发未知行为

---

## profile 切换的内部机制

```
~/.claude/profiles/
├── agentplan.json      ← setup-agentplan 写入的模板副本
└── custom.json         ← setup-custom 写入的模板副本(已替换 __BASE_URL__/__MODEL__)

~/.claude/settings.json ← 当前激活 profile 的实际内容(由 setup/switch 复制写入)
~/.claude/.token        ← 当前激活 profile 的 Key (apiKeyHelper 读这个)
~/.claude/active-profile← 文本: 当前激活的 profile 名
```

切换 = 用 `~/.claude/profiles/<name>.json` 覆盖 `settings.json` + 同步 `.token` + 写 `active-profile`。

切换不需要重启任何服务(没有 relay),立刻生效。
