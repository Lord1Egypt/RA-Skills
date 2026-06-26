# Setup 流程指南

> Setup 流程的完整步骤,供 Agent 对话引导使用。

## 核心原则

- **多 Provider 优于单 Provider** — 引导用户尽可能提供多个 Key

## 命令执行约束

> **CLI 路径:** 下文所有命令中的 `<skill_dir>` 指技能安装目录。默认路径为 `~/.openclaw/skills/free-model-router`，具体路径取决于当前 OpenClaw 变种的安装目录和技能名称（例如 `~/.kimi-openclaw/skills/free-model-router`）。

**禁止复合命令:** OpenClaw 的 exec 工具不支持 `cd ... && node ...` 或 `bash -c "..."` 等复合命令。所有命令必须使用直接调用格式 `node <skill_dir>/scripts/free-model-cli.js <command>`。如需切换目录,应使用 OpenClaw 的 `workingDirectory` 参数指定。

## 第一步:运行 setup

```bash
node <skill_dir>/scripts/free-model-cli.js setup
```

setup 自动完成:
1. 启动 Router 服务(如果未运行)
2. 注册 API Key、拉取 providers/models、自动选择主备模型
   - **幂等性**:仅对尚未设置主模型的 provider 自动选择,保留用户手动配置
3. 向 openclaw.json 写入 `free-model-router` provider(仅此一次,已存在则跳过)
4. 输出 cron 任务注册指令

> **已安装检测**:如果 Router 已运行且 OpenClaw 已配置,setup 会输出当前状态摘要而非重新配置。

## 第二步:注册定时任务

根据 setup 输出的指令,使用 OpenClaw 内置 cron 工具注册:

> **幂等提示:** 注册前先用 `cron list` 检查任务是否已存在。如果任务已存在且配置相同,跳过即可。

**任务 A:事件通知检查(每 30 分钟)**
```
cron add
  name: free-model-router-event-check
  schedule: */30 * * * *
  instruction: 读取 <DATA_DIR>/events.json 中 status=pending 且 shouldNotify=true 的事件。如有待推送事件,向用户推送后标记 status=notified;如无待推送事件,保持静默,不输出任何内容
```

**任务 B:每日状态汇报(每天 9:00)**
```
cron add
  name: free-model-router-daily-status
  schedule: 0 9 * * *
  instruction: 读取 <DATA_DIR>/router-config.json 中各 provider 的主备模型和运行状态,向用户汇报
```

> 如果 cron 不可用,提示用户重新注册定时任务。
> 如果任务已存在,Agent 应跳过注册或仅更新指令内容,不创建重复任务。

## 第三步:展示 Provider 列表,引导设置 API Key

> **幂等提示:** 如果已有 Provider 配置了 API Key,第三步可以跳过或仅引导添加新的 Provider。

```bash
node <skill_dir>/scripts/free-model-cli.js providers
```

根据服务器返回的 providers 数据,向用户展示状态和注册网址:

```
支持的免费模型 Provider:

{遍历 providers 数组,对每个 provider 显示:}
✓ {name} — 已配置 API Key
  网址: {url}

? {name} — 未配置 API Key({freeQuota})
  网址: {url}
  注册指引: {keyGuide}

建议多配置几个 Provider,提升稳定性。
请回复需要配置的 Provider 和对应的 API Key
```

> **重要:** Provider 列表、网址、注册指引均由 model-server 动态返回,不要写死数据。展示时必须包含:
> - `url` - 注册网址
> - `freeQuota` - 免费额度说明
> - `keyGuide` - API Key 获取指引(如果有)

收到 Key 后调用:
```bash
node <skill_dir>/scripts/free-model-cli.js providerApiKey <provider> <key>
```

## 第四步:询问用户将 free-model-router 设为OpencClaw的主模型还是备用模型

> **此步骤在至少一个 Provider 的 API Key 设置完成后执行。**

向用户询问:

```
free-model-router 已配置完成。
请选择 free-model-router 在 OpenClaw 中的角色:

选项 A:设为主模型(推荐) — 所有请求默认走免费模型路由,原主模型自动降为备用
选项 B:设为备用模型 — 仅当原主模型不可用时使用免费模型路由

请回复 "主模型" 或 "备用模型"
```

收到用户选择(未选择时默认设为备用模型)后调用:
```bash
node <skill_dir>/scripts/free-model-cli.js configureModelRole <primary|fallback>
```

- 设为主模型后,`agents.defaults.model.primary` 将变为 `free-model-router/model-router`,原主模型自动移入 `fallbacks`
- 设为备用模型后,`free-model-router/model-router` 将添加到 `agents.defaults.model.fallbacks` 列表末尾

## 第五步:展示各 Provider 主备模型

```bash
node <skill_dir>/scripts/free-model-cli.js models
```

向用户展示各 provider 的主备模型选择:

```
{遍历已配置的 providers:}
{providerName}:
  主模型: {primaryModel}
  备模型: {fallbackModels}
```

用户可选择切换主模型:
```bash
node <skill_dir>/scripts/free-model-cli.js switchProviderPrimaryModel <provider> <modelId>
```

## 第六步:完成

```
全部完成!
Router 已启动: http://127.0.0.1:5678
OpenClaw 已配置: free-model-router → 本地 Router
主模型: xxx / 备模型: xxx, xxx
事件通知: 每 30 分钟 / 状态汇报: 每天 9:00 / 故障切换: 自动

所有模型切换在 Router 层透明完成,不再修改 openclaw.json。
```
