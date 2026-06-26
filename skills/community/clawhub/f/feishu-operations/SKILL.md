---
name: feishu-operations
description: 提供飞书全平台操作指导和团队协作技巧；当用户需要学习飞书功能、解决使用问题或提升协作效率时使用
---

# 飞书操作全指南

## 任务目标
- 本Skill用于：指导用户熟练使用飞书各项功能，掌握团队协作技巧
- 能力包含：消息沟通、文档协作、多维表格、日程管理、权限设置、团队工作流优化
- 触发条件：用户询问飞书功能、操作步骤、协作技巧或遇到使用问题

## 核心功能导航
根据用户需求，提供以下模块的详细指导：

### 沟通协作
- **单聊/群聊**：消息发送、@提醒、消息管理、群聊创建与设置
- **富文本消息**：格式化、表情、文件、链接、@功能
- **消息类型**：文本、图片、文件、链接、语音、视频、位置
- **群聊管理**：群公告、群公告、成员管理、消息免打扰、置顶

### 文档协作
- **云文档**：创建、编辑、格式化、评论、历史版本、协作编辑
- **多维表格**：数据录入、字段类型、视图、筛选、排序、公式、统计
- **知识库**：文档组织、权限管理、搜索、模板使用

### 日程与会议
- **日历**：日程创建、邀请、提醒、重复事件、订阅
- **视频会议**：发起会议、屏幕共享、录制、会议纪要、会议记录
- **快速会议**：即时会议、预约会议、会议链接分享

### 文件管理
- **云盘**：文件上传、下载、文件夹组织、搜索、分享、权限
- **文件协作**：在线预览、评论、版本管理、协作编辑

### 权限与安全
- **权限体系**：查看、编辑、管理、所有者权限详解
- **权限设置**：文档、表格、文件夹权限配置
- **安全设置**：二次验证、登录保护、水印设置

### 效率工具
- **快捷键**：全平台快捷键大全
- **搜索技巧**：消息、文档、联系人高级搜索
- **机器人**：消息通知、工作流、自动化
- **集成**：第三方应用接入

## 使用指引
根据用户提问类型，智能体将：

1. **操作步骤查询**
   - 识别用户需要使用的功能模块
   - 提供清晰的步骤说明（分步骤、配示例）
   - 说明注意事项和常见误区

2. **问题解决**
   - 分析问题现象和可能原因
   - 提供排查步骤和解决方案
   - 说明如何避免类似问题

3. **协作优化**
   - 理解团队场景和需求
   - 推荐最佳实践和工作流
   - 提供权限设计和组织建议

4. **功能推荐**
   - 根据使用场景推荐合适功能
   - 对比不同功能的适用场景
   - 提供组合使用方案

## 资源索引
根据用户需求，智能体将读取相应的参考文档：

### 入门基础
- [references/getting-started.md](references/getting-started.md) - 飞书基础入门、界面介绍、核心概念

### 沟通功能
- [references/messaging.md](references/messaging.md) - 消息功能详解（单聊、群聊、富文本）
- [references/group-chat.md](references/group-chat.md) - 群聊管理与设置

### 文档与表格
- [references/documents.md](references/documents.md) - 云文档创建、编辑、协作
- [references/bitable.md](references/bitable.md) - 多维表格使用指南
- [references/wiki.md](references/wiki.md) - 知识库管理

### 日程与会议
- [references/calendar.md](references/calendar.md) - 日历功能详解
- [references/meetings.md](references/meetings.md) - 视频会议功能

### 文件管理
- [references/files.md](references/files.md) - 云盘与文件管理

### 权限与安全
- [references/permissions.md](references/permissions.md) - 权限体系详解

### 团队协作
- [references/collaboration.md](references/collaboration.md) - 团队协作最佳实践
- [references/workflow.md](references/workflow.md) - 团队工作流设计

### 效率提升
- [references/shortcuts.md](references/shortcuts.md) - 快捷键与技巧
- [references/automation.md](references/automation.md) - 自动化与机器人
- [references/integration.md](references/integration.md) - 第三方应用集成

### 问题解决
- [references/troubleshooting.md](references/troubleshooting.md) - 常见问题解决
- [references/faq.md](references/faq.md) - 高频问题FAQ

## 典型使用场景

### 场景1：新建项目团队
```
用户：如何为项目创建飞书协作空间？
智能体：
1. 参考 collaboration.md 了解团队协作空间设计
2. 参考 group-chat.md 创建项目群聊
3. 参考 documents.md 创建项目文档
4. 参考 permissions.md 设置权限
5. 参考 calendar.md 建立项目日历
```

### 场景2：多人协作文档
```
用户：如何在飞书中让多人一起编辑文档？
智能体：
1. 参考 documents.md 了解文档协作功能
2. 说明评论和修订功能的使用
3. 指导如何设置协作权限
4. 提供协作编辑的最佳实践
```

### 场景3：数据管理
```
用户：如何用飞书多维表格管理项目任务？
智能体：
1. 参考 bitable.md 创建多维表格
2. 设计字段类型（任务名、负责人、状态、截止日期）
3. 设置视图（按负责人分组、按状态筛选）
4. 使用公式计算进度
5. 参考 automation.md 设置自动化提醒
```

## 注意事项
- 根据用户具体问题选择合适的参考文档
- 提供实际可操作的步骤，避免理论空谈
- 说明操作的前提条件和注意事项
- 对于复杂功能，提供分阶段指导
- 推荐相关的快捷键和效率技巧
