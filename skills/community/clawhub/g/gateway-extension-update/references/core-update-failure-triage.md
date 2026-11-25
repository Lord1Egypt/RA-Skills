# 核心版本更新失败（npm global-install-failed）逐字段读法与命令集

用于：主人收到「Gateway restart update error (npm) / background auto-update / global-install-failed」，或自动更新任务反复报同一错。
**先读 `openclaw-extension-update/SKILL.md` 的前置事实**（两份安装根的分离、engines.node 门槛、证据落点、health 首行的运行时归属），本文件给逐字段读法与命令集。

## 1. 失败证据落点

```
~/.openclaw/logs/support/openclaw-update-failure-<uuid>.json     # 每次失败一个
~/.openclaw/logs/support/openclaw-triage-prompt-<ts>-<pid>.md  # 同批次的体检提示 + doctor 发现
~/.openclaw/logs/support/openclaw-diagnostics-<ts>-<pid>.zip    # 脱敏诊断包
```

失败 JSON 字段地图（顶层 `result`）：

| 字段 | 读它做什么 |
|---|---|
| `reason` | 归因大类：`global-install-failed`（npm 装包阶段挂）/ `preflight-node-runtime-incompatible`（装之前就被 node 门槛拦） |
| `root` | 更新器**打的**安装根（本次是 `~/.npm-global/lib/node_modules/openclaw`） |
| `recovery.version` | 服务已回退/保留在的版本（本次 2026.10.5） |
| `recovery.serviceRestartSafe` | 是否可以安全重启服务（true 才能让主人重启） |
| `steps[].name` | 挂在哪一步：`package-install` / `package-install-omit-optional` / `preflight-node-runtime-incompatible` |
| `steps[].stderrTail` | 根因原文（**这里才有真正的错误正文**，顶层 `error` 字段是同一段话的前缀） |
| `steps[].failureFacts[]` | 结构化事实，字段 `check`/`code`/`message`/`affectedKey`（`affectedKey: engines.node` 直接指认门槛字段） |

**读法**：先看 `reason` 定大类 → 看 `steps[].stderrTail` 拿根因原文 → 用 `root` + `recovery.version` 建立「两份安装」的对照。

## 2. 两份安装根对账（决定要不要再修）

更新器打的根与服务实际跑的根**可以不是同一份**。逐个取版本：

```bash
# 更新器打的根
cat ~/.npm-global/lib/node_modules/openclaw/package.json     # .version

# 服务实际跑的根：先看 ExecStart 指向哪
systemctl --user status openclaw-gateway.service --no-pager
# 输出里 Main PID 后面那行就是实际命令，含 node 绝对路径与脚本绝对路径
cat <ExecStart 里那个 openclaw 目录>/package.json           # .version
```

对账结论三种：
- **服务已是目标版本** ⇒ 本次失败是更新器在同步一份**没人用的孤儿根**；不需要重跑 update，处置对象是孤儿根或更新器的目标根设置。
- **服务是旧版** ⇒ 真没升上，根因看 `stderrTail`：`engines.node` 门槛 ⇒ 更新器用的 node 不合规（本次 `/usr/bin/node` v24.21.0 < 门槛 `>=24.22.1 <25 || >=26.12.1`，而服务跑 nvm v26.12.1）⇒ **重跑必然同错**。
- **两份版本一致但都不是目标版** ⇒ 更新链路整体未生效，另查更新器配置与网络。

```bash
# 服务实际用的 node（从 ExecStart 或 health 首行取）
<node 绝对路径> --version
which node                    # 交互 shell 的默认 node，常与服务的不同
```

## 3. 判断「更新其实成功了」

`openclaw health --json` 首行会报运行时归属：

```
openclaw: Retrying with "<node 绝对路径>" (managed Gateway service; current Node failed runtime admission).
```

⇒ 交互 shell 的 node 未通过 admission，真实服务用的是另一份。**这句直接给出「该用哪份 node 跑升级」**，不用自己拼 ExecStart。

## 4. 双向验证（两份都要，只报一条不算修好）

```bash
openclaw health --json     # 取 ok、plugins.errors、channels.*.connected
openclaw status --all      # 取版本面与各通道面
systemctl --user status openclaw-gateway.service --no-pager   # 取 active (running) 与 Main PID 的实际路径
```

判据：`health` 的 `ok:true` **单独一条不算成功** —— 顶层 ok 不覆盖插件加载错误与通道断连，须另附 `status --all` 与版本对账。

## 5. 处置方向（给主人选，不擅自改安装布局）

- **孤儿根**：`~/.npm-global/lib/node_modules/openclaw` 与 `~/.npm-global/bin/openclaw` 软链属于无人使用的一份（本次实测 2026.10.5，服务在 nvm 的 2026.10.7）。删除/改链前要看 `~/.npm-global/bin` 下还有没有别的 CLI（arkcli / clawhub / clawdhub / inkos / mcporter / agent-browser 等）依赖这个 npm prefix。
- **更新器用合规 node**：让更新链路用服务那份 node（其版本已满足门槛），而不是系统 `/usr/bin/node`。
- **先关自动更新止血**：把 `update.auto.enabled` 关掉（用 `openclaw config patch --dry-run` 先试、落盘后回读），避免每次后台尝试都留一份失败记录；改配置面交 `openclaw-config-audit`。
- **不要做的**：反复重跑 `openclaw update` / `npm install -g openclaw`（撞同一堵墙）；为了让 `npm install -g` 过关而手改已装包的 `package.json` engines。

## 6. 顺带可报的 Doctor 项

体检提示里常同时带这两类与更新无关但同批暴露的问题，**分别交付、别混成一条**：
- `gateway.bind=loopback` —— 仅本机绑定（要公网可达才需改）。
- `openclaw.json` 含明文密钥字段 ⇒ 迁 SecretRef（走 `openclaw-config-audit` 的明文密钥迁移口径）。
