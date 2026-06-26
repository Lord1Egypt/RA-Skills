# 飞书消息推送配置

## 概述
飞书消息推送功能用于将每日天气和新闻内容发送到指定的飞书用户。

## 基本用法
```bash
openclaw message send --channel feishu --target "用户ID" --message "消息内容"
```

### 参数说明
- `--channel feishu`: 指定飞书通道
- `--target "用户ID"`: 目标用户ID
- `--message "消息内容"`: 要发送的消息内容

## 用户ID获取
飞书用户ID通常以"ou_"开头，例如：
- `ou_3a0705a4c7b5f068fff0b2b719d37978`

## 消息格式
支持Markdown格式的消息内容，包括：
- 标题：使用🌅等emoji
- 分割线：使用---或空行
- 列表：使用-或1.
- 链接：直接粘贴URL

## 错误处理
### 常见错误
1. **命令未找到**
   ```
   ⚠️ openclaw命令未找到，无法发送消息
   ```
   解决方案：确保openclaw已正确安装并配置

2. **权限错误**
   ```
   ❌ 权限不足，无法发送消息
   ```
   解决方案：检查飞书应用权限配置

3. **网络连接问题**
   ```
   🔌 网络连接失败
   ```
   解决方案：检查网络连接和防火墙设置

### 调试方法
1. **测试消息发送**
   ```bash
   openclaw message send --channel feishu --target "用户ID" --message "测试消息"
   ```

2. **检查日志**
   ```bash
   tail -f /home/alanchan/.openclaw/workspace/daily_push.log
   ```

3. **验证配置**
   ```bash
   # 检查openclaw是否可用
   which openclaw
   openclaw --help
   ```

## 日志记录
所有推送操作都会记录到日志文件：
```
/home/alanchan/.openclaw/workspace/daily_push.log
```

日志格式：
```
2026-02-25 07:30:00 - 推送内容已生成并发送到飞书
```

## 备用方案
如果openclaw不可用，可以：
1. 输出消息内容到控制台
2. 保存到文件供后续处理
3. 使用其他消息推送方式