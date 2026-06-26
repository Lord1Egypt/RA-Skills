# DataWorks 智能监控技能

## 📊 功能概述

自动监控 DataWorks 任务运行情况，提供智能分析和告警。

## 🚀 快速开始

### 1. 配置项目信息

在 `TOOLS.md` 中添加 DataWorks 配置。

### 2. 运行监控

```bash
# TH 项目
python3 dataworks_th_smart_monitor.py

# 或指定日期
python3 dataworks_th_smart_monitor.py --date 2026-03-01
```

### 3. 查看报告

- JSON 报告：`dataworks_th_smart_report.json`
- 文本报告：`dataworks_th_smart_report.txt`

## 📋 报告内容

### 基础统计
- 任务总数
- 成功/失败/运行中数量
- 未运行任务数量

### 运行时长分析
- 平均运行时长
- 时长异常任务列表（超过平均 2 倍）

### 失败分析
- 失败原因归类
- 告警分级统计（P0/P1/P2）
- 失败任务详情

## 🎯 告警分级

### P0 - 严重（立即处理）
- 数据源连接失败
- 内存不足/OOM
- 磁盘满
- 权限拒绝

### P1 - 重要（工作时间处理）
- 字段类型不匹配
- 语法错误
- 表不存在
- 分区错误

### P2 - 一般（可自动重试）
- 超时
- 网络问题
- 临时错误

## 📅 定时执行

建议配置 cron 任务：

```bash
# 每天上午 9 点执行
0 9 * * * cd /path/to/workspace && python3 dataworks_th_smart_monitor.py
```

## 🔧 扩展

### 添加 PH 项目支持

复制脚本并修改配置：

```python
# dataworks_ph_smart_monitor.py
PROJECT_ID = "xxx"  # PH 项目 ID
ACCESS_KEY_ID = "xxx"
ACCESS_KEY_SECRET = "xxx"
```

### 集成飞书通知

在脚本末尾添加飞书消息发送：

```python
import requests

def send_feishu_notification(text):
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
    requests.post(webhook_url, json={"msg_type": "text", "content": {"text": text}})
```

## 📊 示例输出

```
📊 TH DataWorks 智能监控日报 (2026-03-01)
项目：sg_th_ard_bi (ID: 33012)
======================================================================

📋 任务统计
  总计：700 | 成功：586 | 失败：0 | 运行中：0

⏱️  运行时长分析
  平均时长：2.21 分钟
  ⚠️  时长异常任务 (10 个):
    - tmp_route: 17.2 分钟 (平均的 7.8 倍)

✅ 无失败任务！
```

## 🛠️ 维护

- 定期检查 API 配额
- 更新告警关键词
- 调整时长阈值
