# OpenClaw Agent Skill 安装指南

## 安装方式

### 方式 1: 直接安装到 OpenClaw Skills 目录

```bash
# 克隆到 OpenClaw skills 目录
git clone https://github.com/EaveLuo/1panel-skill.git ~/.openclaw/skills/1panel

# 进入目录
cd ~/.openclaw/skills/1panel

# 安装依赖
npm install

# 构建
npm run build
```

### 方式 2: 通过 npm 安装（推荐）

```bash
# 全局安装
npm install -g 1panel-skill

# 创建软链接到 OpenClaw skills 目录
ln -s $(npm root -g)/1panel-skill ~/.openclaw/skills/1panel
```

## 配置

在 OpenClaw 配置中添加环境变量：

```bash
# ~/.bashrc 或 ~/.zshrc
export ONEPANEL_API_KEY="your-1panel-api-key"
export ONEPANEL_HOST="localhost"
export ONEPANEL_PORT="8080"
export ONEPANEL_PROTOCOL="http"
```

## 获取 API Key

1. 登录 1Panel Web 界面
2. 进入: 个人资料 → API
3. 生成或复制 API Key

## 使用方法

OpenClaw 会自动识别 SKILL.md 中的命令。

示例对话:

```
用户: 列出我的 1Panel 容器
Agent: 我来帮您查看容器列表...
      [执行: node {baseDir}/scripts/1panel.mjs containers]

用户: 停止容器 abc123
Agent: 正在停止容器...
      [执行: node {baseDir}/scripts/1panel.mjs stop abc123]

用户: 查看系统状态
Agent: 正在获取系统信息...
      [执行: node {baseDir}/scripts/1panel.mjs system]
```

## 目录结构

```
~/.openclaw/skills/1panel/
├── SKILL.md              # Skill 定义文档
├── scripts/
│   └── 1panel.mjs        # CLI 入口
├── dist/                 # 编译输出
│   ├── index.js          # 库入口
│   ├── client.js         # OnePanelClient
│   ├── api/              # API 模块
│   └── tools/            # Tools 模块
├── src/                  # 源代码
├── package.json
└── README.md
```

## 可用命令

| 命令 | 说明 |
|------|------|
| `containers` | 列出所有容器 |
| `container <id>` | 查看容器详情 |
| `start <id>` | 启动容器 |
| `stop <id>` | 停止容器 |
| `restart <id>` | 重启容器 |
| `images` | 列出镜像 |
| `websites` | 列出网站 |
| `databases` | 列出数据库 |
| `files <path>` | 列出文件 |
| `system` | 系统信息 |
| `dashboard` | 仪表盘信息 |

## 高级用法

### 在 OpenClaw 中使用库 API

```typescript
import { OnePanelClient } from '{baseDir}/dist/index.js';

const client = new OnePanelClient({
  host: 'localhost',
  port: 8080,
  apiKey: process.env.ONEPANEL_API_KEY,
  protocol: 'http'
});

// 使用高阶方法
const containers = await client.listContainers();
const websites = await client.listWebsites();

// 或使用底层 API
const containers = await client.containers.list();
const websites = await client.websites.list();
```

### 使用 Tools 层

```typescript
import { containerTools, handleContainerTool } from '{baseDir}/dist/tools/index.js';

// 获取工具定义
console.log(containerTools);

// 执行工具
const result = await handleContainerTool(client, 'list_containers', {});
```

## 故障排除

### 401 错误 - API Key 错误

```
{"code":401,"message":"API 接口密钥错误"}
```

解决: 检查 ONEPANEL_API_KEY 环境变量是否正确设置

### 连接错误

```
Error: connect ECONNREFUSED
```

解决: 检查 ONEPANEL_HOST 和 ONEPANEL_PORT 是否正确

### 模块找不到

```
Error: Cannot find module
```

解决: 运行 `npm run build` 确保 dist 目录存在

## 更新

```bash
cd ~/.openclaw/skills/1panel
git pull
npm install
npm run build
```

## 卸载

```bash
rm -rf ~/.openclaw/skills/1panel
```
