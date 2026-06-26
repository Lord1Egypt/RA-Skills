# DingTalk CLI Auto Skill

钉钉 CLI 自动化技能 - 基于钉钉官方 CLI 工具 (dws) 实现企业自动化功能。

## Description

本 Skill 封装了钉钉官方 CLI 工具 `dws` (DingTalk Workspace CLI)，提供以下企业自动化能力：

- 📨 **消息管理**: 发送文本/Markdown消息给联系人或群聊
- 📅 **日程管理**: 创建日程、查询空闲时段、查看日程列表
- ✅ **待办事项**: 创建、完成、删除、查询待办
- 👥 **通讯录**: 搜索联系人、查询部门成员
- 🤖 **机器人交互**: 发送群机器人消息

## Prerequisites

### 1. 安装 dws CLI

```bash
# Linux/macOS
curl -fsSL https://raw.githubusercontent.com/DingTalk-Real-AI/dingtalk-workspace-cli/main/scripts/install.sh | sh

# Windows PowerShell
irm https://raw.githubusercontent.com/DingTalk-Real-AI/dingtalk-workspace-cli/main/scripts/install.ps1 | iex
```

### 2. 钉钉开放平台配置

1. 访问 [钉钉开放平台](https://open.dingtalk.com/) 创建企业内部应用
2. 获取 `AppKey` 和 `AppSecret`
3. 配置应用权限：
   - 通讯录管理
   - 日程管理
   - 待办管理
   - 群机器人消息
4. 发布应用

### 3. 环境变量配置

```bash
export DWS_CLIENT_ID="your-app-key"
export DWS_CLIENT_SECRET="your-app-secret"
```

或使用 OpenClaw 环境配置：

```bash
openclaw config set dingtalk.app_key your-app-key
openclaw config set dingtalk.app_secret your-app-secret
```

### 4. 首次认证

```bash
dws auth login
```

按提示完成 OAuth 设备流认证。

## Tools

### 发送消息

#### `send_text_message`
发送文本消息给指定用户或群聊

```bash
# 给用户发送消息
node scripts/message.js send-text --user-id "user123" --content "Hello, this is a test message"

# 给群聊发送消息
node scripts/message.js send-text --chat-id "chat123" --content "Group notification"
```

#### `send_markdown_message`
发送 Markdown 格式消息

```bash
node scripts/message.js send-md --user-id "user123" --title "通知" --content "**重要提醒**：会议即将开始"
```

### 日程管理

#### `create_schedule`
创建日程/会议

```bash
node scripts/calendar.js create \
  --title "周例会" \
  --start "2026-04-03T14:00:00" \
  --end "2026-04-03T15:00:00" \
  --attendees "user1,user2,user3" \
  --location "会议室A"
```

#### `list_schedules`
查询日程列表

```bash
# 查询今天的日程
node scripts/calendar.js list --today

# 查询指定日期范围
node scripts/calendar.js list --start "2026-04-01" --end "2026-04-07"
```

#### `check_free_busy`
查询用户空闲时间

```bash
node scripts/calendar.js free-busy \
  --users "user1,user2" \
  --start "2026-04-03T09:00:00" \
  --end "2026-04-03T18:00:00"
```

### 待办事项

#### `create_todo`
创建待办事项

```bash
node scripts/todo.js create \
  --content "完成项目文档" \
  --due "2026-04-05T18:00:00" \
  --assignees "user1"
```

#### `list_todos`
查询待办列表

```bash
# 所有待办
node scripts/todo.js list

# 即将到期的待办
node scripts/todo.js list --due-within 3
```

#### `complete_todo`
完成待办

```bash
node scripts/todo.js complete --id "todo123"
```

#### `delete_todo`
删除待办

```bash
node scripts/todo.js delete --id "todo123"
```

### 通讯录

#### `search_contacts`
搜索联系人

```bash
# 按姓名搜索
node scripts/contact.js search --name "张三"

# 按部门搜索
node scripts/contact.js search --dept "技术部"
```

#### `get_department_members`
获取部门成员列表

```bash
node scripts/contact.js dept-members --dept-id "dept123"
```

### 机器人消息

#### `send_robot_message`
发送群机器人消息

```bash
node scripts/robot.js send \
  --webhook "https://oapi.dingtalk.com/robot/send?access_token=xxx" \
  --secret "SECxxx" \
  --content "机器人通知消息"
```

## Usage Examples

### 场景 1: 每日待办提醒

```bash
# 获取今日待办
node scripts/todo.js list --today

# 创建今日待办
node scripts/todo.js create --content "提交日报" --due "today 18:00"
```

### 场景 2: 会议通知

```bash
# 搜索参会人员
node scripts/contact.js search --name "张三"

# 检查空闲时间
node scripts/calendar.js free-busy --users "user1,user2" --duration 60

# 创建会议
node scripts/calendar.js create \
  --title "项目评审会" \
  --start "2026-04-03T14:00:00" \
  --duration 60 \
  --attendees "user1,user2"

# 发送会议提醒
node scripts/message.js send-md \
  --chat-id "chat123" \
  --title "会议提醒" \
  --content "**项目评审会** 将于14:00开始，请准时参加"
```

### 场景 3: 任务分派

```bash
# 查找成员
node scripts/contact.js search --name "李四"

# 创建并分派待办
node scripts/todo.js create \
  --content "完成API文档编写" \
  --assignees "user2" \
  --due "2026-04-05"

# 发送通知
node scripts/message.js send-text \
  --user-id "user2" \
  --content "你有一个新的待办任务：完成API文档编写，截止2026-04-05"
```

## API Reference

### 命令行参数规范

所有脚本遵循统一的参数规范：

| 参数 | 说明 | 示例 |
|------|------|------|
| `--user-id` | 用户ID | `user123` |
| `--chat-id` | 群聊ID | `chat456` |
| `--content` | 消息/内容 | `Hello World` |
| `--title` | 标题 | `会议通知` |
| `--start` | 开始时间 | `2026-04-03T14:00:00` |
| `--end` | 结束时间 | `2026-04-03T15:00:00` |
| `--duration` | 持续时间(分钟) | `60` |
| `--attendees` | 参会人(逗号分隔) | `user1,user2` |
| `--assignees` | 负责人(逗号分隔) | `user1` |
| `--due` | 截止日期 | `2026-04-05` 或 `today` |
| `--dept-id` | 部门ID | `dept123` |
| `--name` | 姓名 | `张三` |
| `--dept` | 部门名称 | `技术部` |
| `--webhook` | 机器人Webhook | `https://...` |
| `--secret` | 机器人密钥 | `SEC...` |

### 时间格式

- ISO 8601: `2026-04-03T14:00:00`
- 相对时间: `today`, `tomorrow`, `+3d` (3天后)
- 自然语言: `今天18:00`, `明天上午9点`

## Error Handling

### 常见错误

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 401 | 未认证或Token过期 | 执行 `dws auth login` |
| 403 | 权限不足 | 检查应用权限配置 |
| 404 | 用户/群聊不存在 | 检查ID是否正确 |
| 400 | 参数错误 | 检查参数格式 |
| 429 | 请求过于频繁 | 稍后重试 |

### 调试模式

添加 `--debug` 参数查看详细日志：

```bash
node scripts/message.js send-text --user-id "user123" --content "test" --debug
```

## Configuration

### OpenClaw 集成配置

在 OpenClaw 配置文件中添加：

```json
{
  "skills": {
    "dingtalk-cli-auto": {
      "app_key": "your-app-key",
      "app_secret": "your-app-secret",
      "default_chat_id": "your-default-chat-id"
    }
  }
}
```

### 环境变量

| 变量名 | 说明 | 必需 |
|--------|------|------|
| `DWS_CLIENT_ID` | 钉钉AppKey | 是 |
| `DWS_CLIENT_SECRET` | 钉钉AppSecret | 是 |
| `DINGTALK_DEFAULT_CHAT` | 默认群聊ID | 否 |
| `DINGTALK_DEBUG` | 调试模式 | 否 |

## Dependencies

- Node.js >= 18.0.0
- dws CLI >= 0.5.0

## Installation

```bash
# 克隆到技能目录
cd ~/clawd/skills
git clone <repo-url> dingtalk-cli-auto

# 安装依赖
cd dingtalk-cli-auto
npm install

# 配置认证
export DWS_CLIENT_ID="your-app-key"
export DWS_CLIENT_SECRET="your-app-secret"
dws auth login

# 测试
npm test
```

## Testing

运行测试用例：

```bash
# 全部测试
npm test

# 单模块测试
npm run test:message
npm run test:calendar
npm run test:todo
npm run test:contact
```

## Troubleshooting

### 问题：dws 命令未找到

**解决方案**：
```bash
# 确认安装路径
which dws

# 添加到 PATH
export PATH="$HOME/.local/bin:$PATH"

# 重新安装
curl -fsSL https://raw.githubusercontent.com/DingTalk-Real-AI/dingtalk-workspace-cli/main/scripts/install.sh | sh
```

### 问题：认证失败

**解决方案**：
```bash
# 清除缓存重新认证
dws auth logout
dws auth login

# 检查环境变量
echo $DWS_CLIENT_ID
echo $DWS_CLIENT_SECRET
```

### 问题：权限不足

**解决方案**：
1. 检查钉钉开放平台应用权限设置
2. 确认应用已发布
3. 确认用户在企业通讯录中

## Changelog

### v1.0.0 (2026-04-02)
- 初始版本发布
- 支持消息发送、日程管理、待办事项、通讯录查询
- 支持机器人消息发送

## License

MIT

## Credits

- [DingTalk Workspace CLI](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli) - 钉钉官方CLI工具
- [钉钉开放平台](https://open.dingtalk.com/) - 钉钉开放API
