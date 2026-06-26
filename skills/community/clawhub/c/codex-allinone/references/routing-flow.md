# 路由决策手册

> 这份文件给 Skill 自己看,告诉它在什么状态下做什么。

## v7 架构核心(必须先理解)

Codex CLI 0.130+ 默认发 OpenAI **Responses 协议**,而多数第三方服务只懂 **Chat 协议**。
本 skill 的解决方案:用本机 `codex-relay` 进程做协议翻译,每个 profile 独占一个端口。

| Profile | 端口 | 上游 | 协议适配 |
|---------|------|------|---------|
| agentplan | 4446 | https://ark.cn-beijing.volces.com/api/plan/v3 | relay 翻译 (Responses → Chat) |
| kimi | 4447 | https://api.moonshot.cn/v1 | relay 翻译 |
| deepseek | 4448 | https://api.deepseek.com/v1 | relay 翻译 |
| arkv3 | — | https://ark.cn-beijing.volces.com/api/v3 | **直连**(原生支持 Responses) |
| custom | 4449 或直连 | 用户提供 | **自动探测**(404 → relay;否则直连) |

custom 路径的探测逻辑见 `scripts/relay-helper.sh#probe_responses_support`,
对用户给的 base_url 发一个 `POST /responses`,根据 HTTP code 决定是否需要 relay。

## 状态机

```
                    ┌─────────────────────────┐
                    │ 用户触发 codex-allinone  │
                    └─────────────┬───────────┘
                                  ▼
                       bash scripts/doctor.sh
                                  │
                 ┌────────────────┼────────────────────┐
                 ▼                ▼                    ▼
         Codex 未安装       版本过旧              已安装且满足要求
                 │                │                    │
                 └────────┬───────┘                    │
                          ▼                            │
                 scripts/install.sh                    │
                          │                            │
                          └──────────┬─────────────────┘
                                     ▼
                            config_state == ?
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        ▼                            ▼                            ▼
    "clean"                  "managed-by-skill"             "user-managed"
   全新环境                  本 skill 之前配过               用户手动配过
        │                            │                            │
        ▼                            ▼                            ▼
  【路径 ①】                   【路径 ②】                    【路径 ③】
  首次配置                    正常使用                      兼容性检查
        │                            │                            │
        │                            │                     is_healthy ?
        │                            │                     ├─ 通过 → 转路径 ②
        │                            │                     └─ 不通 → 告知用户问题
        │                            │                              ├─ 选 A 重配 → 路径 ①
        │                            │                              └─ 选 B 自修 → 退出
        │                            │
        ├─ 选 A AgentPlan             ├─ ensure-relay.sh(确保服务就绪)
        │  → setup-agentplan.sh      │
        │                            ├─ codex exec --skip-git-repo-check "用户需求"
        └─ 选 B 第三方                │
           → 二级菜单                 ├─ 用户说"切换"
           → setup-thirdparty.sh     │  → switch-profile.sh
                                     │
                                     └─ 用户报错
                                        → 参考 troubleshooting.md
```

## 与用户对话的措辞模板

### 主菜单(仅全新环境触发)

> 你想用哪种模型来驱动 Codex?
>
> **A. 火山方舟 AgentPlan**(推荐)
> - 套餐内额度,无需额外付费
> - `ark-code-latest` 智能路由,可在 AgentPlan 控制台切换 Kimi K2 / Doubao / DeepSeek / GLM
> - 你需要:**AgentPlan 控制台**分配的"专属 Key"(注意不是普通 API Key 管理里的)
>
> **B. 第三方 Key**(已有 Kimi / DeepSeek / 自购方舟 Key,或公司自建网关等)
> - 自由选模型
> - 你需要:对应服务的 API Key
>
> 请回复 **A** 或 **B**。

### 二级菜单(选了 B 之后)

> 你的 Key 是哪家的?
>
> 1. **Kimi (Moonshot)** — 默认模型 `kimi-k2-turbo-preview`
>    需要:Kimi 平台的 API Key
>
> 2. **DeepSeek** — 默认模型 `deepseek-chat`
>    需要:DeepSeek 平台的 API Key
>
> 3. **火山方舟普通 v3 Key** — 默认 `doubao-seed-1-6-250615`
>    需要:火山方舟控制台 → API Key 管理里的普通 Key(注意:这跟 AgentPlan 的"专属 Key"不一样)
>
> 4. **自定义 OpenAI 兼容端点** — 任何符合 OpenAI Chat Completions 协议的服务
>    需要你**同时提供三样东西**:
>    - **API Key**(如 `sk-xxx`)
>    - **模型名**(如 `qwen-max` / `glm-4.6` / `yi-large` / 公司网关里的 model id)
>    - **Base URL**(如 `https://dashscope.aliyuncs.com/compatible-mode/v1`,通常以 `/v1` 结尾)
>
>    适用场景:通义千问、智谱 GLM、Yi、百川、LiteLLM、vLLM、Ollama、公司自建网关等。
>    ⚠️ 沙箱在境内 IDC,境外服务(OpenAI / Anthropic 官方等)通常连不上。
>
> 请回复数字。

### 兼容性检查不通过时

> 检测到你已有的 codex 配置存在以下问题:
>
> 1. {issues[0]}
> 2. {issues[1]}
>    ...
>
> 你希望:
>
> **A. 让本 skill 帮你重新配置**(推荐)
>    - 会先把你现有的 config.toml 备份,你随时可以恢复
>    - 然后重新选择 AgentPlan / 第三方 Key
>
> **B. 我自己去修改**
>    - 退出本 skill,你手动修改 config.toml
>    - 改完后再次触发 skill 会自动重新检查
>
> 请回复 **A** 或 **B**。

### 正常使用时的调用方式

用户说编程需求时,先确保服务就绪,再执行:

```bash
bash scripts/ensure-relay.sh
cd ~ && codex exec --skip-git-repo-check "用户的完整需求原文"
```

> 说明:
> - `ensure-relay.sh` 会读取当前 active-profile,自动启动对应端口的 relay。arkv3 直连模式以及 custom 直连模式会立即退出,不耗时
> - 端口分配:agentplan=4446 / kimi=4447 / deepseek=4448 / custom=4449 / arkv3=直连
> - `cd ~` 是因为 codex 默认要求在 git 目录中运行,沙箱家目录通常不是 git 仓库
> - `--skip-git-repo-check` 跳过这个限制

### 切换模型服务

用户说"切换"/"换一家"/"切到 Kimi" 时:
- 没指定具体哪家 → `bash scripts/switch-profile.sh`(列出已配置的选项)
- 指定了 → `bash scripts/switch-profile.sh <名称>`

如果用户之前是手动配置的(`config_state == "user-managed"`),切换前提醒:
"切换会覆盖你现有的 config.toml(会先备份),确认吗?"

## 禁止事项

- ❌ 用户没有选择之前不能自动运行配置脚本
- ❌ 不能自动猜测 Key,必须让用户主动粘贴
- ❌ 不能连接 OpenAI 官方服务(沙箱在境内 IDC,网络不通)
- ❌ 没有备份的情况下不能覆盖用户的配置文件
- ❌ 不能在日志或屏幕上打印完整的 Key
- ❌ 配置已就绪时不能反复询问用户"是否要切换"— 静默执行即可
- ❌ 兼容性检查通过时不能打扰用户 — 直接进入正常使用
