# 钉钉 CLI 自动化技能

基于钉钉官方 CLI 工具 (dws) 实现的企业自动化 OpenClaw Skill。

## 功能特性

- 📝 **消息发送** - 支持文本、Markdown 消息发送给用户或群聊
- 📅 **日程管理** - 创建、查询、更新、删除日程
- ✅ **待办事项** - 创建、完成、删除、查询待办
- 👥 **通讯录** - 搜索联系人、查询部门成员、获取用户详情
- 🤖 **机器人** - 发送群机器人消息、模板消息

## 快速开始

### 1. 安装 dws CLI

```bash
# Linux/macOS
curl -fsSL https://raw.githubusercontent.com/DingTalk-Real-AI/dingtalk-workspace-cli/main/scripts/install.sh | sh

# 验证安装
dws --version
```

### 2. 钉钉开放平台配置

1. 访问 [钉钉开放平台](https://open.dingtalk.com/)
2. 创建企业内部应用
3. 获取 `AppKey` 和 `AppSecret`
4. 配置必要权限（通讯录、日程、待办）
5. 发布应用

### 3. 配置认证

```bash
# 设置环境变量
export DWS_CLIENT_ID="your-app-key"
export DWS_CLIENT_SECRET="your-app-secret"

# 登录认证
dws auth login
```

### 4. 在 OpenClaw 中使用

```bash
# 发送消息
node scripts/message.js send-text --user-id "user123" --content "Hello"

# 查询待办
node scripts/todo.js list

# 创建日程
node scripts/calendar.js create --title "会议" --start "today 14:00" --duration 60
```

## 目录结构

```
dingtalk-cli-auto/
├── SKILL.md           # Skill 说明文档
├── index.js           # 统一入口
├── package.json       # npm 配置
├── .env.example       # 环境变量示例
│
├── lib/               # 核心库
│   ├── dws.js         # DWS 客户端封装
│   ├── message.js    # 消息客户端
│   ├── calendar.js   # 日程客户端
│   ├── todo.js       # 待办客户端
│   └── contact.js    # 通讯录客户端
│
├── scripts/           # 命令行脚本
│   ├── message.js    # 消息发送
│   ├── calendar.js   # 日程管理
│   ├── todo.js       # 待办管理
│   ├── contact.js    # 通讯录
│   └── robot.js      # 机器人消息
│
└── test/              # 测试
    └── run-all.js    # 测试入口
```

## 编程使用

```javascript
const { MessageClient, TodoClient, CalendarClient } = require('./dingtalk-cli-auto');

// 发送消息
const msgClient = new MessageClient();
await msgClient.sendText('user123', null, 'Hello World');

// 创建待办
const todoClient = new TodoClient();
await todoClient.create({
  content: '完成报告',
  due: 'tomorrow',
  priority: 'high'
});

// 查询日程
const calClient = new CalendarClient();
const events = await calClient.list({ today: true });
```

## 环境变量

| 变量 | 说明 | 必需 |
|------|------|------|
| `DWS_CLIENT_ID` | 钉钉 AppKey | 是 |
| `DWS_CLIENT_SECRET` | 钉钉 AppSecret | 是 |
| `DINGTALK_DEFAULT_CHAT` | 默认群聊 ID | 否 |
| `DINGTALK_DEBUG` | 调试模式 | 否 |

## 许可

MIT