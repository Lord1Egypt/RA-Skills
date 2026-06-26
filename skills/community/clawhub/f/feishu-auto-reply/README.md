# Feishu Auto Reply Bot 🤖

飞书消息自动回复机器人，根据自定义规则自动回复飞书消息。

## 功能特点
- ✅ 多种匹配方式：包含、完全匹配、正则匹配、开头匹配、结尾匹配
- ✅ 支持仅被@时回复
- ✅ 工作时间配置，非工作时间不回复
- ✅ 自定义回复模板
- ✅ 支持富文本消息回复
- ✅ 规则测试功能
- ✅ 简单易用的配置文件

## 安装
```bash
clawhub install feishu-auto-reply
```

## 快速开始

### 1. 生成配置文件
```bash
feishu-auto-reply init --output ./config.yaml
```

### 2. 编辑配置文件
```yaml
rules:
  - keyword: "你好"
    reply: "你好！我是自动回复机器人，有什么可以帮你的？"
    match: contains
    only_mention: false

  - regex: "^(请假|休假)"
    reply: "请假请直接联系人事部门，谢谢！"
    match: regex
    only_mention: true

working_hours:
  - "9:00-18:00"
  exclude_weekends: true
```

### 3. 测试规则
```bash
feishu-auto-reply test --message "你好，请问怎么请假？" --config ./config.yaml
```

### 4. 启动服务
```bash
feishu-auto-reply start --config ./config.yaml
```

## 匹配方式说明
| 匹配方式 | 说明 | 示例 |
|---------|------|------|
| `contains` | 消息包含关键词即匹配 | `keyword: "你好"` 匹配 "你好啊" |
| `exact` | 消息完全等于关键词才匹配 | `keyword: "你好"` 仅匹配 "你好" |
| `startsWith` | 消息以关键词开头 | `keyword: "请假"` 匹配 "请假申请" |
| `endsWith` | 消息以关键词结尾 | `keyword: "吗？"` 匹配 "在吗？" |
| `regex` | 正则表达式匹配 | `regex: "^[0-9]+$"` 匹配纯数字 |

## 权限要求
使用前需要确保飞书应用有以下权限：
- `im:message:read` - 读取消息
- `im:message:send` - 发送消息
- `im:chat:read` - 读取群组信息
- `im:user:read` - 读取用户信息

## 使用场景
1. 客服自动回复常见问题
2. 节假日自动回复通知
3. 非工作时间自动回复
4. 部门常用话术自动回复
5. 机器人客服系统

## 注意事项
- 自动回复服务需要保持后台运行
- 建议先在测试群中验证规则再正式使用
- 避免设置过于宽泛的规则导致误回复
- 大量消息场景建议添加限流机制

## 路线图
- [ ] 支持图片、文件等富媒体回复
- [ ] 支持多轮对话
- [ ] 支持AI智能回复
- [ ] 消息统计和分析功能
- [ ] web 管理界面

## 许可证
MIT
