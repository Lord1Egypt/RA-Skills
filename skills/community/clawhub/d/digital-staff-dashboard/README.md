# Agent Dashboard v2.1 🚀

一个增强版的 OpenClaw Agent 可视化监控面板，支持自动查找 OpenClaw 安装目录、Token 成本计算、头像上传、**创建新 Agent** 和实时数据展示。

## ✨ 新特性

### 🆕 创建新 Agent
- **通过 Dashboard 创建 Agent**：点击「新建 Agent」按钮
- **配置 Agent 属性**：名称、角色、emoji、颜色主题
- **选择模型**：**自动读取 OpenClaw 配置的模型提供商和模型列表**
- **写入 OpenClaw 配置**：创建的 Agent 直接生效，可在 OpenClaw 中使用

**模型提供商自动同步：**
- Dashboard 自动读取 `~/.openclaw/openclaw.json` 中的模型配置
- 支持多个模型提供商（deepseek、moonshot、kimi-coding、zai、minimax 等）
- 创建 Agent 时自动复制对应的模型配置

### 🔍 自动查找 OpenClaw 安装目录
- 自动检测系统中多个可能的 OpenClaw 安装位置
- 支持环境变量 `OPENCLAW_HOME` 覆盖
- 智能选择包含最多 Agent 的目录作为主目录

### ⚙️ 可配置 Dashboard
- **自定义 Dashboard 名称和副标题**
- **Token 成本配置**：设置输入/输出/缓存 Token 的价格
- **自动刷新间隔**：可配置的实时数据更新频率
- **费用估算显示开关**

### 👤 头像上传功能
- 点击 Agent 头像即可上传自定义图片
- 支持拖拽上传
- 支持 PNG、JPG、GIF、WebP 格式
- 最大 5MB 文件限制
- 自动保存到项目目录

### 💰 Token 成本计算
- 自动计算每个 Agent 的 Token 使用成本
- 分别统计输入、输出和缓存 Token
- 显示总费用估算
- 支持自定义货币和价格

## 🚀 快速开始

### 安装依赖

```bash
cd workspace/agent-dashboard-v2
pip3 install -r requirements.txt --break-system-packages
```

### 启动服务

```bash
# 使用启动脚本
./start.sh

# 或直接启动
python3 dashboard_server.py
```

服务启动后，访问 **http://localhost:5177**

## 📁 项目结构

```
workspace/agent-dashboard-v2/
├── dashboard_server.py      # 主服务器
├── openclaw_finder.py       # OpenClaw 目录查找模块
├── openclaw_config.py       # OpenClaw 配置管理模块（新增）
├── config.py                # Dashboard 配置管理
├── start.sh                 # 启动脚本
├── requirements.txt         # Python 依赖
├── README.md               # 本文件
├── static/                 # 前端文件
│   ├── index.html          # 主页面
│   ├── css/style.css       # 样式文件
│   └── js/app.js           # 前端逻辑
└── data/                   # 数据目录
    ├── config.json         # Dashboard 配置
    └── avatars/            # 上传的头像
```

## 🆕 创建 Agent 流程

### 1. 打开 Dashboard
点击右上角的「**➕ 新建 Agent**」按钮

### 2. 填写 Agent 信息
- **Agent ID**：唯一标识（如 `my-assistant`）
- **显示名称**：展示在 Dashboard 上的名称
- **角色**：Agent 的角色描述
- **Emoji**：选择一个图标（如 🤖、💻、🎨）
- **颜色主题**：选择卡片的颜色风格
- **模型提供商**：从 OpenClaw 配置中选择
- **选择模型**：选择具体的 AI 模型
- **描述**：Agent 的详细描述
- **系统提示词**：设置 Agent 的系统行为

### 3. 创建完成
点击「创建 Agent」后：
- Agent 配置写入 `~/.openclaw/agents/{agent_id}/`
- Dashboard 自动刷新显示新 Agent
- Agent 可在 OpenClaw 中立即使用

### Agent 配置结构

创建的 Agent 目录结构：

```
~/.openclaw/agents/{agent_name}/
├── agent/
│   ├── metadata.json       # Dashboard 元数据（名称、角色、emoji等）
│   └── models.json         # 模型配置（API密钥、模型列表）
└── sessions/
    └── sessions.json       # 会话数据（自动创建）
```

## ⚙️ 配置说明

配置文件位于 `data/config.json`，首次启动会自动创建默认配置。

### 配置项说明

```json
{
  "dashboard_name": "Agent Dashboard",
  "dashboard_subtitle": "实时监控 Agent 状态",
  "refresh_interval": 30,
  "show_cost_estimates": true,
  "token_cost": {
    "input_price_per_1m": 2.0,
    "output_price_per_1m": 8.0,
    "cache_price_per_1m": 1.0,
    "currency": "CNY"
  },
  "agent_configs": {
    "main": {
      "name": "小七",
      "role": "主助手",
      "emoji": "🎯",
      "color": "main"
    }
  }
}


```
<img width="2505" height="1371" alt="截图 2026-03-28 16-41-28 (Edited)" src="https://github.com/user-attachments/assets/d9bc91e9-cac7-4133-bd9b-e46c749f46a7" />
## 🔌 API 端点

### Agent 管理（新增）
- `POST /api/agents` - 创建新 Agent
  ```json
  {
    "name": "my-agent",
    "display_name": "我的助手",
    "role": "助手",
    "emoji": "🤖",
    "color": "cyan",
    "description": "...",
    "system_prompt": "...",
    "model_provider": "deepseek",
    "model_id": "deepseek-chat"
  }
  ```
- `DELETE /api/agents/<name>` - 删除 Agent（移动到回收站）
- `GET /api/model-providers` - 获取可用的模型提供商列表

### 配置相关
- `GET /api/config` - 获取 Dashboard 配置
- `POST /api/config` - 更新 Dashboard 配置
- `POST /api/config/sync` - 手动同步 OpenClaw 配置

### Agent 相关
- `GET /api/agents` - 获取所有 Agent 列表
- `GET /api/agents/<name>/sessions` - 获取指定 Agent 的会话
- `GET /api/agents/<name>/avatar` - 获取 Agent 头像
- `POST /api/agents/<name>/avatar` - 上传 Agent 头像
- `GET|POST /api/agents/<name>/config` - 获取/更新 Agent 配置

### 统计相关
- `GET /api/stats` - 获取聚合统计（含成本）
- `GET /api/stats/cost-summary` - 获取成本汇总

### 系统信息
- `GET /api/system-info` - 获取 OpenClaw 安装信息

## 🎨 Agent 颜色主题

支持以下预设颜色：
- `main` - 蓝紫渐变
- `coder` - 青蓝渐变
- `brainstorm` - 橙粉渐变
- `writer` - 绿青渐变
- `investor` - 绿橙渐变
- `cyan` - 青色（默认）

## ⌨️ 快捷键

- `Esc` - 关闭弹窗
- `Ctrl+R` - 刷新数据

## 📝 数据来源

Dashboard 从以下路径读取数据：
- `~/.openclaw/agents/{agent}/sessions/sessions.json`
- `~/.openclaw/agents/{agent}/agent/metadata.json`（Dashboard 特有配置）
- `~/.openclaw/agents/{agent}/agent/models.json`（模型配置）

## 🔧 故障排除

### 找不到 OpenClaw 目录
设置环境变量：
```bash
export OPENCLAW_HOME=/path/to/.openclaw
python3 dashboard_server.py
```

### 端口被占用
修改 `data/config.json` 中的 `port` 配置项。

### 头像上传失败
检查 `data/avatars` 目录是否有写入权限。

### 创建 Agent 失败
- 检查 `~/.openclaw/agents/` 是否有写入权限
- Agent ID 只能包含小写字母、数字、连字符和下划线
- Agent ID 不能重复

### 模型提供商列表为空
- 检查 `~/.openclaw/openclaw.json` 是否存在且包含 `models.providers` 配置
- 确保 OpenClaw 已正确配置至少一个模型提供商
- 检查 Dashboard 服务器日志中是否有 API 错误信息
- 尝试重启 Dashboard 服务重新同步配置

## 🔄 与 OpenClaw 的集成

1. **启动同步**：Dashboard 启动时自动从 OpenClaw 读取 Agent 配置
2. **创建 Agent**：通过 Dashboard 创建的 Agent 直接写入 OpenClaw 目录
3. **配置同步**：Agent 的显示名称、角色等元数据保存在 OpenClaw 的 `metadata.json` 中
4. **模型配置**：自动从 OpenClaw 的全局配置中复制模型提供商配置

## 📄 许可证

MIT License
