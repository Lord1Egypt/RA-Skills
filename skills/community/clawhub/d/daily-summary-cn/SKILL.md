---
name: daily-summary
description: 每日工作总结自动生成。根据聊天记录和浏览器历史生成一句话工作总结，定时发送飞书。
---

# Daily Summary - 每日工作总结

自动生成简洁的每日工作总结，通过飞书发送。

## 功能

- 读取本地聊天记录（memory 文件）
- 读取浏览器历史（Chrome/Edge）
- 生成一句话工作总结
- 每天定时发送飞书

## 使用方法

### 定时任务（自动）

设置每天 17:30 自动生成：
```bash
openclaw cron add --schedule "30 17 * * 1-5" --message "生成今日工作总结" --channel feishu
```

### 手动生成

```bash
python skills/daily-summary/scripts/generate.py
```

## 配置

### 浏览器历史路径

- Chrome: `%LOCALAPPDATA%\Google\Chrome\User Data\Default\History`
- Edge: `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\History`

### 飞书发送

需要配置飞书机器人：
```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "your-app-id",
      "appSecret": "your-app-secret"
    }
  }
}
```

## 输出格式

一句话总结今日完成的主要任务，简洁明了。

示例：
> 今日完成：部署本地模型、安装飞书 skills、创建每日工作总结定时任务、发布 daily-summary skill
