# 飞书多 Agent 配置助手 🤖

> **交互式引导版本** - 逐步指导用户创建多个飞书 Bot，配置多 Agent 系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.0.4-blue.svg)](https://github.com/rfdiosuao/openclaw-skills)

---

## 📦 安装

```bash
# 从 GitHub 克隆
git clone https://github.com/rfdiosuao/openclaw-skills.git
cd openclaw-skills/feishu-multi-agent-manager

# 安装依赖
npm install

# 构建
npm run build
```

---

## 🚀 功能特性

### ✨ v2.0.4 新增功能（兼容飞书插件 2026.4.1）

1. **兼容飞书插件 2026.4.1** 🦞
   - 适配 OpenClaw 2026.3.31+
   - 支持话题模式独立上下文
   - 支持流式输出配置

2. **交互式配置向导** 🎯
   - 逐步引导用户完成配置
   - 询问用户要创建几个 Agent
   - 提供预设角色推荐方案

3. **飞书 Bot 创建教程** 📘
   - 详细的图文教程
   - 分步骤指导创建飞书应用
   - 包含检查清单和注意事项

4. **批量创建支持** 📦
   - 一次性创建多个 Agent
   - 自动验证每个凭证
   - 详细的成功/失败报告

5. **预设角色模板** 🎭
   - 6 个经典角色（大总管、开发、内容、运营、法务、财务）
   - 每个角色包含完整人设文件
   - 支持完全自定义

6. **诊断命令集成** 🔧
   - `/feishu start` - 检查插件状态
   - `/feishu doctor` - 深度诊断
   - `/feishu auth` - 批量授权

---

## 🎯 使用流程

### 步骤 1：启动配置向导

```typescript
await main(ctx, { action: 'start_wizard' });
```

**Bot 回复：**
```
🤖 欢迎使用飞书多 Agent 配置助手！

我将引导你完成多个 Agent 的配置流程。

## 📋 配置流程
1. 选择 Agent 数量 - 告诉我要创建几个 Agent
2. 选择 Agent 角色 - 从预设角色中选择或自定义
3. 创建飞书应用 - 我会提供详细的创建教程
4. 配置凭证 - 逐个输入每个 Bot 的 App ID 和 App Secret
5. 验证并生成 - 自动验证凭证并生成配置
6. 重启生效 - 重启 OpenClaw 使配置生效

## 🎯 预设角色推荐
| 角色 | 职责 | 表情 |
|------|------|------|
| main | 大总管 - 统筹全局、分配任务 | 🎯 |
| dev | 开发助理 - 代码开发、技术架构 | 🧑‍💻 |
| content | 内容助理 - 内容创作、文案撰写 | ✍️ |
| ops | 运营助理 - 用户增长、活动策划 | 📈 |
| law | 法务助理 - 合同审核、合规咨询 | 📜 |
| finance | 财务助理 - 账目统计、预算管理 | 💰 |

## 🚀 快速开始
**请告诉我：你想创建几个 Agent？**

例如：
- 3 个 - 我推荐：main（大总管）+ dev（开发）+ content（内容）
- 6 个 - 完整团队：全部 6 个角色
- 自定义 - 你自由选择角色

回复数字或"自定义"，我们开始吧！😊
```

---

### 步骤 2：选择 Agent 数量

**用户回复：** `6 个`

**Bot 回复：**
```
✅ 好的！我们将创建 6 个 Agent。

## 📋 推荐方案
推荐：完整 6 人团队 - main + dev + content + ops + law + finance

## 🎯 请选择配置方式

方式 1：使用预设角色
回复「预设」或「模板」，我会按推荐方案自动配置

方式 2：自定义角色
回复「自定义」，然后告诉我你想用哪 6 个角色

方式 3：完全自定义
回复「全新」，每个角色都由你自由定义

请选择（回复数字或关键词）：
```

---

### 步骤 3：查看飞书创建教程

```typescript
await main(ctx, { 
  action: 'show_tutorial',
  step: 1,
  agentName: '大总管'
});
```

**Bot 回复：**
```
## 📘 第 1 步：创建飞书应用「大总管」

### 步骤 1: 登录飞书开放平台
1. 访问 https://open.feishu.cn/
2. 使用你的飞书账号登录

### 步骤 2: 创建企业自建应用
1. 点击右上角「创建应用」
2. 选择「企业自建」
3. 输入应用名称：大总管
4. 点击「创建」

### 步骤 3: 获取应用凭证
1. 进入应用管理页面
2. 点击左侧「凭证与基础信息」
3. 复制 App ID（格式：cli_xxxxxxxxxxxxxxx）
4. 复制 App Secret（32 位字符串）
   - 如果看不到，点击「查看」或「重置」

### 步骤 4: 开启机器人能力
1. 点击左侧「功能」→「机器人」
2. ✅ 开启「机器人能力」
3. ✅ 开启「以机器人身份加入群聊」
4. 点击「保存」

### 步骤 5: 配置事件订阅
1. 点击左侧「功能」→「事件订阅」
2. 选择「长连接」模式（推荐）
3. 勾选以下事件：
   - ✅ im.message.receive_v1 - 接收消息
   - ✅ im.message.read_v1 - 消息已读（可选）
4. 点击「保存」

### 步骤 6: 配置权限
1. 点击左侧「功能」→「权限管理」
2. 搜索并添加以下权限：
   - ✅ im:message - 获取用户发给机器人的单聊消息
   - ✅ im:chat - 获取群组中发给机器人的消息
   - ✅ contact:user:readonly - 读取用户信息（可选）
3. 点击「申请」

### 步骤 7: 发布应用
1. 点击左侧「版本管理与发布」
2. 点击「创建版本」
3. 填写版本号：1.0.0
4. 点击「提交审核」（机器人类通常自动通过）
5. 等待 5-10 分钟生效

---

### ✅ 完成检查清单
- [ ] App ID 已复制（以 cli_ 开头）
- [ ] App Secret 已复制（32 位字符串）
- [ ] 机器人能力已开启
- [ ] 事件订阅已配置（长连接模式）
- [ ] 权限已申请（im:message, im:chat）
- [ ] 应用已发布

---

**准备好后，请回复以下信息：**

```
第 1 个 Bot 配置完成：
App ID: cli_xxxxxxxxxxxxxxx
App Secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

我会帮你验证并添加到配置中！👍
```

---

### 步骤 4：验证凭证

```typescript
await main(ctx, { 
  action: 'validate_credentials',
  appId: 'cli_xxx',
  appSecret: 'xxx'
});
```

**Bot 回复：**
```
✅ 凭证验证通过！

App ID: cli_xxx
App Secret: 12345678...（已隐藏）

准备添加到配置，请确认：
- 回复「确认」继续
- 回复「取消」放弃
- 回复「下一个」直接配置下一个
```

---

### 步骤 5：批量创建 Agent

```typescript
await main(ctx, {
  action: 'batch_create',
  agents: [
    {
      agentId: 'main',
      agentName: '大总管',
      appId: 'cli_main_xxx',
      appSecret: 'main_secret_xxx',
      isDefault: true
    },
    {
      agentId: 'dev',
      agentName: '开发助理',
      appId: 'cli_dev_xxx',
      appSecret: 'dev_secret_xxx'
    },
    {
      agentId: 'content',
      agentName: '内容助理',
      appId: 'cli_content_xxx',
      appSecret: 'content_secret_xxx'
    }
  ]
});
```

**Bot 回复：**
```
🎉 批量创建成功！

✅ 已创建 3 个 Agent：
1. main - ✅
2. dev - ✅
3. content - ✅

---

## 📝 下一步

### 1. 重启 OpenClaw
```bash
openclaw restart
```

### 2. 等待 Bot 上线
重启后等待 1-2 分钟，所有 Bot 会自动连接飞书

### 3. 测试 Bot
在飞书中搜索 Bot 名称，发送消息测试

### 4. 查看日志
```bash
tail -f /home/node/.openclaw/run.log
```

---

## 📚 配置详情

所有 Agent 的配置已保存到：
- 配置文件：/home/node/.openclaw/openclaw.json
- 工作区：/home/node/.openclaw/workspace/[agentId]/
- 人设文件：每个工作区包含 SOUL.md、AGENTS.md、USER.md

---

💡 提示：如果有任何 Bot 显示 offline，请检查飞书应用配置是否正确（凭证、事件订阅、权限）。

需要帮助请回复「帮助」或「排查」！
```

---

## 📋 API 参考

### `start_wizard` - 启动配置向导

**参数：** 无

**说明：** 启动交互式配置向导，引导用户完成整个流程

---

### `select_count` - 选择 Agent 数量

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `count` | string | ✅ | Agent 数量（1-10） |

**示例：**
```typescript
await main(ctx, { action: 'select_count', count: '6' });
```

---

### `show_tutorial` - 显示飞书创建教程

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `step` | string | ✅ | 第几步（1-6） |
| `agentName` | string | ✅ | Agent 名称 |

**示例：**
```typescript
await main(ctx, { 
  action: 'show_tutorial',
  step: '1',
  agentName: '大总管'
});
```

---

### `validate_credentials` - 验证凭证

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `appId` | string | ✅ | 飞书 App ID |
| `appSecret` | string | ✅ | 飞书 App Secret |

**示例：**
```typescript
await main(ctx, { 
  action: 'validate_credentials',
  appId: 'cli_xxx',
  appSecret: 'xxx'
});
```

---

### `batch_create` - 批量创建 Agent

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agents` | Array | ✅ | Agent 列表 |

**Agent 对象结构：**
```typescript
{
  agentId: string;        // Agent 唯一标识
  agentName: string;      // 显示名称
  appId: string;          // 飞书 App ID
  appSecret: string;      // 飞书 App Secret
  isDefault?: boolean;    // 是否为默认 Agent
  model?: string;         // 模型配置
}
```

**示例：** 见上方步骤 5

---

### `show_status` - 显示当前配置状态

**参数：** 无

**示例：**
```typescript
await main(ctx, { action: 'show_status' });
```

---

## 🎭 预设角色模板

### 6 个经典角色

| 角色 ID | 名称 | 职责 | 表情 |
|--------|------|------|------|
| **main** | 大总管 | 统筹全局、分配任务、跨 Agent 协调 | 🎯 |
| **dev** | 开发助理 | 代码开发、技术架构、运维部署 | 🧑‍💻 |
| **content** | 内容助理 | 内容创作、文案撰写、素材整理 | ✍️ |
| **ops** | 运营助理 | 用户增长、数据分析、活动策划 | 📈 |
| **law** | 法务助理 | 合同审核、合规咨询、风险规避 | 📜 |
| **finance** | 财务助理 | 账目统计、成本核算、预算管理 | 💰 |

每个角色包含：
- ✅ 完整的 SOUL.md 人设文件
- ✅ 核心职责说明
- ✅ 工作准则
- ✅ 协作方式

---

## 📝 使用场景

### 场景 1：快速搭建 3 人团队

**用户需求：** "我想创建 3 个 Agent"

**流程：**
1. 启动向导 → `start_wizard`
2. 选择数量 → `select_count` (count: "3")
3. 选择预设 → 自动推荐 main + dev + content
4. 逐个配置 → 显示教程 → 验证凭证
5. 批量创建 → `batch_create`
6. 重启生效

---

### 场景 2：完整 6 人团队

**用户需求：** "我要完整的 6 个角色"

**流程：**
1. 启动向导 → `start_wizard`
2. 选择数量 → `select_count` (count: "6")
3. 选择预设 → 自动配置全部 6 个角色
4. 批量配置 → 一次性提供 6 个凭证
5. 批量创建 → `batch_create`
6. 重启生效

---

### 场景 3：完全自定义

**用户需求：** "我要自定义 2 个特殊角色"

**流程：**
1. 启动向导 → `start_wizard`
2. 选择数量 → `select_count` (count: "2")
3. 选择自定义 → 用户提供角色名称和职责
4. 生成人设 → 自动生成 SOUL.md
5. 配置凭证 → 验证并创建
6. 重启生效

---

## 🔧 配置说明

### openclaw.json 结构

批量创建后，`openclaw.json` 会自动更新：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "custom/qwen3.5-plus"
      }
    },
    "list": [
      {
        "id": "main",
        "name": "大总管",
        "workspace": "/home/node/.openclaw/workspace/main",
        "default": true
      },
      {
        "id": "dev",
        "name": "开发助理",
        "workspace": "/home/node/.openclaw/workspace/dev"
      }
    ]
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "accounts": {
        "main": {
          "appId": "cli_main_xxx",
          "appSecret": "main_secret_xxx"
        },
        "dev": {
          "appId": "cli_dev_xxx",
          "appSecret": "dev_secret_xxx"
        }
      }
    }
  },
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "feishu",
        "accountId": "main"
      }
    },
    {
      "agentId": "dev",
      "match": {
        "channel": "feishu",
        "accountId": "dev"
      }
    }
  ],
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["main", "dev"]
    }
  }
}
```

---

## 🧪 测试

```bash
# 运行单元测试
npm test

# 运行并生成覆盖率报告
npm test -- --coverage
```

---

## 🐛 问题排查

### 问题 1：凭证验证失败

**错误：** `❌ App ID 必须以 cli_ 开头`

**解决：** 
- 检查 App ID 是否正确复制
- 确保以 `cli_` 开头
- 不要包含空格或换行

---

### 问题 2：Agent ID 已存在

**错误：** `❌ Agent ID "main" 已存在`

**解决：**
- 使用不同的 `agentId`
- 或删除现有 Agent 后重试

---

### 问题 3：Bot 显示 offline

**解决：**
```bash
# 1. 检查配置文件
cat /home/node/.openclaw/openclaw.json | jq '.channels.feishu.accounts'

# 2. 检查日志错误
grep -i "error\|fail" /home/node/.openclaw/run.log | tail -20

# 3. 测试飞书 API 连通性
curl -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"cli_xxx","app_secret":"xxx"}'
```

**可能原因：**
- ❌ AppID/AppSecret 填写错误
- ❌ 飞书应用未发布
- ❌ 事件订阅未配置
- ❌ 权限未开通

---

## 📝 更新日志

### v2.0.4 (2026-04-01) - 兼容飞书插件 2026.4.1
- ✅ **兼容飞书插件 2026.4.1** - 适配 OpenClaw 2026.3.31+
- ✅ **支持话题模式** - 集成 `threadSession` 配置
- ✅ **支持流式输出** - 集成 `streaming` 配置
- ✅ **诊断命令** - 集成 `/feishu start/doctor/auth`
- ✅ **更新安装说明** - 使用最新官方安装命令

### v2.0.2 (2026-03-26) - 动态路径 + 自动备份
- ✅ **动态路径获取** - 自动检测用户实际路径
- ✅ **配置前自动备份** - 修改 openclaw.json 前自动备份
- ✅ **自动复制认证配置** - 创建子 Agent 时自动复制 auth-profiles.json
- ✅ **配置验证** - 添加配置格式验证和错误提示

### v2.0.1 (2026-03-19) - 配置格式修复
- 🐛 **修复 accounts 配置格式** - 数组→对象格式
- ✅ **自动检测和转换** - 数组格式自动转换为对象格式
- ✅ **配置格式验证** - 添加初始化保护

### v2.0.0 (2026-03-09)
- ✨ **交互式配置向导** - 逐步引导用户完成配置
- ✨ **飞书创建教程** - 详细的图文教程
- ✨ **批量创建支持** - 一次性创建多个 Agent
- ✨ **预设角色模板** - 6 个经典角色
- ✨ **凭证验证** - 自动验证 AppID/AppSecret 格式
- ✨ **状态查询** - 显示当前配置状态

### v1.0.0 (2026-03-09)
- ✨ 初始版本
- ✅ 支持创建/列出/更新/删除 Agent

---

## 🔒 安全提示

1. **凭证安全**
   - App Secret 是敏感信息，请勿泄露
   - 不要将 `openclaw.json` 上传到公开仓库
   - 建议定期轮换飞书凭证（90 天）

2. **权限控制**
   - 飞书应用只需配置必要的权限
   - 推荐权限：`im:message`、`im:chat`、`contact:user:readonly`

3. **操作审计**
   - 所有 Agent 管理操作都会记录日志
   - 建议定期检查日志

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [多 Agent 路由文档](https://clawd.org.cn/concepts/multi-agent.html)
- [飞书开放平台](https://open.feishu.cn/)
- [GitHub 仓库](https://github.com/rfdiosuao/openclaw-skills)
- [ClawHub 技能市场](https://clawhub.ai)

---

**维护者：** [@rfdiosuao](https://github.com/rfdiosuao)  
**最后更新：** 2026-04-01

---

## ⚠️ 重要：工作区隔离说明

### 每个 Agent 拥有完全独立的工作区！

**路径规则：**
- ✅ **workspace:** `/home/node/.openclaw/workspace-[agentId]/`
- ✅ **agentDir:** `/home/node/.openclaw/agents/[agentId]/agent/`
- ✅ **sessions:** `/home/node/.openclaw/agents/[agentId]/sessions/`

**示例（6 个 Agent）：**
```
~/.openclaw/
├── workspace-main/           # main 的工作区
│   ├── SOUL.md
│   ├── USER.md
│   ├── AGENTS.md
│   └── memory/
├── workspace-dev/            # dev 的工作区（独立！）
│   ├── SOUL.md
│   ├── USER.md
│   ├── AGENTS.md
│   └── memory/
├── workspace-content/        # content 的工作区（独立！）
├── workspace-ops/
├── workspace-law/
├── workspace-finance/
└── agents/
    ├── main/
    │   ├── agent/           # main 的状态
    │   │   └── auth-profiles.json
    │   └── sessions/        # main 的会话
    ├── dev/
    │   ├── agent/           # dev 的状态（独立！）
    │   │   └── auth-profiles.json
    │   └── sessions/        # dev 的会话（独立！）
    └── ...
```

**为什么需要隔离？**
1. **记忆独立** - main 的记忆不会污染 dev 的记忆
2. **人设独立** - 每个 Agent 有自己的 SOUL.md
3. **会话独立** - 聊天历史分开存储
4. **认证独立** - 每个 Agent 绑定不同的飞书账号
5. **模型独立** - 可为不同 Agent 配置不同模型
