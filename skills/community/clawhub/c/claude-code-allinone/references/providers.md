# 模型供应商参考 — 引导用户选择 / 收集 Key

> 这份文档给主对话 Agent 看:用户问"我应该选哪个"或"这个 Key 怎么搞"时,从这里抄答案。

## 核心原则:默认 AgentPlan,不主动列菜单

减少用户感知是本 skill 的核心设计。**首次配置时一律默认走 AgentPlan**,只让用户粘贴一次 Key。**只有**用户主动表达"我有自己的 Anthropic 兼容网关 / 自定义 base_url / 别的 Key"等语义时,才进入 custom 分支。

⛔ 禁止主动给用户列 A/B 菜单。这会增加感知,违背"无感配置"原则。

---

## A. 火山方舟 AgentPlan(默认 / 无需询问)

**这是首次配置的默认路径。** 不要问用户"要选 A 还是 B",直接说:

> "准备给你配置 Claude Code,使用火山方舟 AgentPlan(套餐内额度,ark-code-latest 智能路由)。请粘贴 AgentPlan 控制台分配的专属 Key:"

- **base_url**: `https://ark.cn-beijing.volces.com/api/plan`
- **协议**: 原生 Anthropic Messages 协议(Claude Code 直连即可)
- **模型名**: `ark-code-latest`(智能路由,后端自动分发到 Kimi K2 / Doubao / DeepSeek / GLM 等)
- **Key 来源**:登录 [AgentPlan 控制台](https://www.volcengine.com/) → 找到"AgentPlan 专属 Key"页面 → 复制
- **优点**:
  - 套餐内额度,不需要单独付费
  - 智能路由,后端帮你选最合适的模型
  - 境内 IDC 直连,延迟低
- **限制**:
  - Key 必须是 AgentPlan 控制台分配的"专属 Key",不能用普通 v3 API Key
  - 不支持自定义 temperature / top_p

### 配置命令
```bash
bash scripts/setup-agentplan.sh "<AgentPlan 专属 Key>"
```

### 引导话术(默认场景,**不**给 A/B 菜单)
```
准备给你配置 Claude Code,使用火山方舟 AgentPlan(套餐内额度,ark-code-latest 智能路由)。

请粘贴你的 AgentPlan 专属 Key:

📋 怎么获取 Key?
   1. 登录火山方舟控制台
   2. 进入 AgentPlan 模块
   3. 找到"专属 Key"或"分配 Key"页面
   4. 复制里面的 Key

⚠️ 注意:这个 Key 跟普通的"API Key 管理"里的 Key 不是一回事,
   AgentPlan 必须用专属 Key,普通 Key 会报 401。
```

---

## B. 自定义 Anthropic 兼容网关(仅用户主动要求时)

**触发条件**:用户语句里出现以下任一(或类似)语义,才进入这条分支。否则一律默认 AgentPlan,不询问。

- "我有自己的 / 我们公司的 / 我们自建的 网关 / base_url / 端点"
- "我有别的 Anthropic 兼容 Key"
- "用 claude-code-router / kimi-router / Bedrock / Vertex 出来的端点"
- "不用 AgentPlan,我有自己的 Key"
- 用户**直接给出**了 base_url + Key + model 三件套

⛔ 用户没说这些,**不要主动**问"要不要用自定义网关"。

- **base_url**: 由用户提供
- **协议**: 必须实现 Anthropic Messages 协议(`POST /v1/messages`)
- **模型名**: 由用户提供
- **典型场景**:
  - 公司自建的 Anthropic 协议网关
  - 第三方厂商提供的 Anthropic 兼容端点
  - 自部署的 Anthropic 协议代理(claude-code-router 等)
- **不适用场景**:
  - OpenAI 协议端点(请去 codex-allinone)
  - 普通 Chat Completions 接口(本 skill 不做协议转换)

### 配置命令
```bash
bash scripts/setup-custom.sh "<base_url>" "<Key>" "<model>"
```

### 引导话术
```
请按顺序提供 3 个信息:

1. base_url(网关地址,不含 /v1 后缀)
   示例: https://my-gateway.example.com

2. API Key
   示例: sk-xxxxxxxxxxxxxxxx

3. 模型名(网关上能识别的)
   示例: claude-3-5-sonnet-20241022 / kimi-k2 / 自定义名

可以一次贴出来,格式:
  base_url=...
  key=...
  model=...
```

setup-custom.sh 会自动:
- 探测 `<base_url>/v1/messages` 是否可达 (curl POST 一次, 返回 200/400/422 视为通)
- 把占位符 `__BASE_URL__` / `__MODEL__` 替换到 profile 文件
- 备份旧 settings.json 后写入新内容

---

## 不支持的供应商(本 skill 不做)

| 供应商 | 协议 | 应该用什么 |
|---|---|---|
| OpenAI 官方 | OpenAI Chat | codex-allinone(OpenAI 协议)|
| 火山方舟 v3 普通 Key | OpenAI Chat | codex-allinone arkv3 模式 |
| Kimi (Moonshot) | OpenAI Chat | codex-allinone kimi 模式 |
| DeepSeek | OpenAI Chat | codex-allinone deepseek 模式 |
| Anthropic 官方 (anthropic.com) | Anthropic | 境内 IDC 网络不通,无法使用 |
| AWS Bedrock | Anthropic via AWS | (后续版本可能支持)|
| Google Vertex | Anthropic via GCP | (后续版本可能支持)|

---

## Key 安全说明

setup 脚本会把 Key 存到 3 个位置(全部在用户家目录,不出沙箱):

1. `~/.bashrc` 的 `export ARK_API_KEY=...` 或 `export CUSTOM_ANTHROPIC_KEY=...`
   - 用途:沙箱重启后自动恢复环境变量
   - 权限:跟 `.bashrc` 一致(通常 644,但内容只在用户家目录)

2. `~/.claude/.token`
   - 用途:settings.json 的 `apiKeyHelper: "cat ~/.claude/.token"` 会读这个
   - 权限:600(仅当前用户可读)

3. `~/.claude/profiles/<name>.json` 不含 Key,只含 base_url / model 等
   - profile 文件不存 Key,切换 profile 时 .token 文件由 switch 脚本同步

⛔ Skill 永远不会把 Key 上传到任何外部服务,也不会在日志里打印完整 Key。
