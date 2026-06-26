---
name: feishu-enhanced
description: 飞书增强套件 - 深度集成飞书文档、多维表格、消息和日历的自动化操作。适用于需要高效办公自动化的中文用户。
metadata:
  openclaw:
    requires:
      bins: ["curl", "jq"]
    install:
      - id: curl
        kind: binary
        binary: curl
        label: Install curl
      - id: jq
        kind: binary
        binary: jq
        label: Install jq for JSON processing
---

# 飞书增强套件 (Feishu Enhanced)

深度集成飞书API的增强技能套件，提供文档、多维表格、消息和日历的自动化操作能力。

## 功能特性

### 1. 智能文档操作
- 自动创建和更新飞书文档
- 批量文档内容提取和转换
- 文档模板快速应用

### 2. 多维表格高级功能
- 批量记录创建和更新
- 数据同步和备份
- 自动化报表生成

### 3. 消息自动化
- 定时消息发送
- 消息模板管理
- 群发通知

### 4. 日历集成
- 日程自动创建
- 会议提醒同步
- 日历数据分析

## 使用场景

- **日常办公**: 自动化日报、周报生成
- **数据管理**: 多维表格批量操作
- **团队协作**: 消息通知自动化
- **时间管理**: 日程智能提醒

## 依赖

- OpenClaw飞书扩展已配置
- 飞书应用已授权相应权限

## 配置

在 `TOOLS.md` 中添加飞书应用配置:

```markdown
### Feishu Config
- App ID: your_app_id
- App Secret: your_app_secret
- Default Folder Token: your_folder_token
```

## 注意事项

1. 确保飞书应用已获得必要的API权限
2. 批量操作时注意API调用频率限制
3. 敏感数据建议先备份再操作

---

**版本**: 1.0.0
**作者**: @lijie
**分类**: 办公自动化 / 飞书集成
