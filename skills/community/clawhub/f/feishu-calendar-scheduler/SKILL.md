---
name: feishu-calendar-scheduler
description: 飞书智能日历调度器 - 自动推荐最佳会议时间，批量管理日程，生成会议报表
homepage: https://clawhub.com/skills/feishu-calendar-scheduler
metadata:
  {
    "openclaw": {
      "emoji": "📅",
      "requires": { "tools": ["feishu_calendar_event", "feishu_calendar_calendar"] },
      "price": {
        "monthly": 99,
        "currency": "CNY",
        "trialDays": 7
      }
    },
  }
---

# 飞书智能日历调度器

为企业提供智能会议时间推荐和批量日程管理服务。

## 功能特点

### 🕒 智能时间推荐
- 基于规则的时间推荐算法
- 避开已知繁忙时段
- 考虑时区和工作日设置
- 多参会人时间协调

### 📊 批量会议管理
- 批量创建、修改、取消会议
- 自动发送会议邀请
- 参会人状态跟踪
- 会议模板管理

### 📈 报表分析
- 会议参与率统计
- 时间利用率分析
- 效率改进建议
- 导出 Excel/PDF 报告

### 🔗 集成扩展
- 与飞书文档、多维表格集成
- 支持自定义工作流
- API 接口调用
- 第三方系统集成

## 安装使用

### 安装要求
- OpenClaw 已配置飞书插件
- 用户拥有飞书日历访问权限

### 快速开始
```bash
# 通过 ClawHub 安装
clawhub install feishu-calendar-scheduler

# 或手动安装到 skills 目录
```

### 基础使用
```bash
# 推荐会议时间
openclaw skill feishu-calendar-scheduler recommend \
  --start "2026-03-17T09:00:00+08:00" \
  --end "2026-03-17T18:00:00+08:00" \
  --duration 60 \
  --attendees "ou_xxx,ou_yyy"

# 批量创建会议
openclaw skill feishu-calendar-scheduler batch-create \
  --template "周会模板" \
  --start-date "2026-03-17" \
  --weeks 4 \
  --attendees "团队全员"

# 生成会议报表
openclaw skill feishu-calendar-scheduler report \
  --month 2026-03 \
  --output excel
```

## 定价策略

### 免费试用
- 7天免费试用期
- 最多10个会议
- 基础功能

### 专业版 ¥99/月
- 无限会议数量
- 所有智能功能
- 高级报表
- 技术支持

### 企业版 ¥499/月
- 多团队管理
- API 访问权限
- 定制化开发
- 优先支持

## 技术架构

- **核心引擎**：基于规则的时间调度算法
- **数据存储**：飞书多维表格 + 本地缓存
- **用户界面**：命令行 + 飞书机器人
- **部署方式**：OpenClaw 插件形式

## 开发计划

### v1.0（当前）
- 基础时间推荐
- 简单会议管理
- 命令行界面

### v1.1（1个月后）
- 飞书机器人集成
- 图形化配置界面
- 更多报表类型

### v1.2（2个月后）
- API 开放接口
- 第三方系统集成
- 高级算法优化

## 支持与帮助

- 文档：https://docs.clawhub.com/skills/feishu-calendar-scheduler
- 支持：support@clawhub.com
- 社区：https://discord.com/invite/clawd

## 许可证
商业许可证 - 需要购买订阅后使用

---

**开始7天免费试用**：安装后自动开始试用期，试用期满后需要购买订阅。