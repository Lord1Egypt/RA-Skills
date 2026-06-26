# OpenClaw部署指南

## 简介

OpenClaw是一个智能体框架，支持多智能体协作、7×24小时运行。本指南基于视频第5、6、7集内容整理。

---

## 安装方式

### Windows安装

**前置要求**：
- Node.js >= 22
- PowerShell（管理员模式）

```bash
# PowerShell管理员模式执行
iwr https://raw.githubusercontent.com/openclaw/openclaw/main/install.ps1 -UseBasicParsing | iex
```

**安装引导流程**：
1. 同意风险提示（必须同意才能继续）
2. 选择 Quick Start 快速安装
3. 配置大模型（推荐Kimi K2.5或阿里通义）
4. 跳过渠道配置（后续手动配置飞书）
5. 等待安装完成

### Linux服务器安装

```bash
# 方式一：npm全局安装
npm install -g openclaw
openclaw gateway start

# 方式二：官方一键脚本
curl -fsSL https://openclaw.sh/install.sh | bash

# 方式三：无影云桌面（可视化Linux）
# 参考官方MumeCloud部署教程
```

### Mac安装

```bash
# 使用npm安装
npm install -g openclaw

# 启动Gateway
openclaw gateway start
```

---

## 大模型配置

### 推荐模型

| 模型 | 特点 | 费用 |
|------|------|------|
| Kimi K2.5 | 代码生成强 | 按量计费 |
| 阿里通义 | 性价比高 | 多种套餐 |
| 智谱 | 中文优化 | 按次计费 |

### 配置方法

在OpenClaw配置界面或配置文件中填写：
- API Key
- Base URL（如有特殊配置）
- 模型名称

---

## 飞书机器人配置

### 完整流程

#### 1. 创建飞书应用

1. 登录飞书开放平台：https://open.feishu.cn/app
2. 点击「创建企业自建应用」
3. 填写应用名称和描述
4. 添加「机器人」能力

#### 2. 获取凭证

在应用基础信息中获取：
- `App ID`
- `App Secret`

#### 3. 配置权限

权限管理 → 批量导入权限（参考下方JSON）：

```json
{
  "permissions": [
    "im:message",
    "im:message.group_at_msg",
    "im:chat.access_event.bot",
    "im:chat.access_event.observer",
    "docx:document"
  ]
}
```

#### 4. 安装飞书插件

```bash
# 在OpenClaw安装目录执行
git clone https://github.com/openclaw/feishu-plugin.git
cd feishu-plugin
npm install

# 安装node SDK
# 在OpenClaw根目录执行
npm install @openclaw/feishu-sdk
```

#### 5. 配置插件（三条命令）

```bash
# 配置App ID
openclaw config set channel.feishu.appId <YOUR_APP_ID>

# 配置App Secret
openclaw config set channel.feishu.appSecret <YOUR_APP_SECRET>

# 启动连接
openclaw channel connect
```

#### 6. 配置事件回调

1. 进入应用 → 事件与回调 → 添加事件
2. 配置回调长连接URL
3. 开启「使用长连接」选项

#### 7. 发布版本

1. 创建版本 → 填写版本信息
2. 提交审核（企业自建应用自动通过）
3. 在飞书中打开应用即可使用

---

## Gateway管理

```bash
# 查看状态
openclaw gateway status

# 启动
openclaw gateway start

# 停止
openclaw gateway stop

# 重启
openclaw gateway restart
```

---

## 工作区结构

```
~/.openclaw/
├── openclaw.js          # 主配置文件
├── skills/              # 技能目录
├── extensions/          # 扩展插件
├── workspace/           # 工作区
│   └── agents/          # 智能体工作空间
└── data/                # 数据存储
```

---

## 常见问题

### 问题1：PowerShell安装提示权限不足
- 必须使用「管理员模式」打开PowerShell
- Windows搜索PowerShell → 右键 → 以管理员运行

### 问题2：安装过程中网络超时
- 插件安装可能需要访问GitHub
- 网络不佳时可多试几次
- 或配置代理

### 问题3：飞书连接失败
- 确认App ID和App Secret正确
- 检查飞书应用是否已发布
- 确认事件回调已正确配置
