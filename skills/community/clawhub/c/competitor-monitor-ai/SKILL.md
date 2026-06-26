---
name: competitor-monitor
description: 竞品数据定时监控Skill，定时访问指定电商或社交平台页面，抓取点赞、评论、销量等数据，检测数据异常波动（如出现爆款），自动截图并发送提醒通知。适用于竞品分析、市场监控、爆款发现等场景。
license: MIT
compatibility: 需要网络访问，需要Python 3.8+环境，需要Playwright或Selenium进行网页抓取
metadata:
  author: AI Assistant
  version: "1.0"
  category: data-monitoring
  language: zh-CN
---

# 竞品数据定时监控 Skill

## 用途

本 Skill 用于定时监控竞品在电商平台或社交平台的数据表现，帮助用户：
- 自动抓取竞品的点赞、评论、销量等关键数据
- 追踪数据变化趋势，生成可视化报表
- 检测数据异常波动（如出现爆款、数据暴增）
- 自动截图保存关键页面
- 及时发送提醒通知

## 适用平台

### 电商平台
- **淘宝/天猫**：商品销量、评价数、价格
- **京东**：商品销量、评价数、价格
- **拼多多**：销量、评价、价格
- **抖音电商**：销量、点赞、评论
- **小红书电商**：销量、点赞、收藏

### 社交平台
- **抖音**：视频点赞、评论、转发、播放量
- **小红书**：笔记点赞、收藏、评论
- **微博**：转发、评论、点赞
- **B站**：播放量、点赞、投币、收藏
- **快手**：点赞、评论、播放量

## 核心功能

### 1. 定时数据采集
- 支持自定义监控频率（每小时/每天/每周）
- 支持多平台同时监控
- 支持批量监控多个竞品链接

### 2. 数据抓取
- 自动抓取点赞数、评论数、销量等关键指标
- 支持JavaScript渲染页面
- 自动处理反爬机制

### 3. 异常检测
- 检测数据异常波动（如点赞数暴增）
- 识别潜在爆款
- 支持自定义异常阈值

### 4. 自动截图
- 异常时自动截图保存
- 支持全页面截图
- 截图带时间戳存档

### 5. 提醒通知
- 支持多种通知方式（邮件、微信、钉钉、飞书）
- 支持自定义提醒内容
- 支持异常摘要报告

## 工作流程

### 第一步：配置监控任务

创建监控配置文件 `config/monitor_tasks.json`：

```json
{
  "tasks": [
    {
      "id": "task_001",
      "name": "竞品A-抖音监控",
      "platform": "douyin",
      "url": "https://www.douyin.com/video/xxxxx",
      "schedule": "0 */2 * * *",
      "metrics": ["likes", "comments", "shares", "views"],
      "alert_threshold": {
        "likes": {"increase_percent": 50, "min_value": 1000},
        "comments": {"increase_percent": 30, "min_value": 100}
      }
    },
    {
      "id": "task_002",
      "name": "竞品B-小红书监控",
      "platform": "xiaohongshu",
      "url": "https://www.xiaohongshu.com/explore/xxxxx",
      "schedule": "0 */4 * * *",
      "metrics": ["likes", "collections", "comments"],
      "alert_threshold": {
        "likes": {"increase_percent": 100, "min_value": 500}
      }
    }
  ]
}
```

### 第二步：启动监控服务

```bash
# 启动监控服务
python scripts/monitor_service.py --config assets/config/monitor_tasks.json

# 后台运行
nohup python scripts/monitor_service.py --config assets/config/monitor_tasks.json > monitor.log 2>&1 &
```

### 第三步：异常检测与提醒

当检测到数据异常时：
1. 自动截图保存到 `assets/screenshots/`
2. 发送提醒通知
3. 记录异常日志

## 监控配置说明

### 配置文件结构

```json
{
  "tasks": [
    {
      "id": "任务ID",
      "name": "任务名称",
      "platform": "平台类型",
      "url": "监控页面URL",
      "schedule": "定时规则(cron格式)",
      "metrics": ["监控指标列表"],
      "selectors": {
        "likes": "点赞数CSS选择器",
        "comments": "评论数CSS选择器"
      },
      "alert_threshold": {
        "指标名": {
          "increase_percent": "增长率阈值(%)",
          "min_value": "最小触发值"
        }
      },
      "screenshot_on_alert": true,
      "notification": {
        "email": ["email@example.com"],
        "webhook": "https://oapi.dingtalk.com/robot/send?access_token=xxx"
      }
    }
  ],
  "global": {
    "data_retention_days": 30,
    "screenshot_retention_days": 7,
    "default_schedule": "0 */6 * * *"
  }
}
```

### 平台预设配置

Skill内置了常见平台的CSS选择器预设：

| 平台 | 点赞 | 评论 | 分享/转发 | 播放量/浏览 |
|------|------|------|-----------|-------------|
| 抖音 | .like-count | .comment-count | .share-count | .play-count |
| 小红书 | .like-count | .comment-count | .collect-count | - |
| 微博 | .like-count | .comment-count | .repost-count | .read-count |
| B站 | .like-count | .comment-count | .coin-count | .view-count |
| 淘宝 | - | .rate-count | - | .sell-count |

### 定时规则（Cron格式）

```
* * * * *
│ │ │ │ │
│ │ │ │ └─── 星期 (0-7, 0和7都是周日)
│ │ │ └───── 月份 (1-12)
│ │ └─────── 日期 (1-31)
│ └───────── 小时 (0-23)
└─────────── 分钟 (0-59)

示例：
0 */2 * * *    # 每2小时
0 9,18 * * *   # 每天9点和18点
0 */6 * * 1-5  # 工作日每6小时
```

## 异常检测规则

### 检测类型

1. **增长率检测**
   - 检测指标增长率是否超过阈值
   - 示例：点赞数2小时内增长超过50%

2. **绝对值检测**
   - 检测指标是否达到某个绝对值
   - 示例：评论数超过1000

3. **趋势检测**
   - 检测数据是否呈现异常趋势
   - 示例：连续3次采集数据持续上升

4. **爆款检测**
   - 综合多指标判断是否为爆款
   - 示例：点赞+评论+分享同时暴增

### 阈值配置示例

```json
{
  "alert_threshold": {
    "likes": {
      "increase_percent": 50,
      "min_value": 1000,
      "window": "2h"
    },
    "comments": {
      "increase_percent": 30,
      "min_value": 100
    },
    "views": {
      "increase_percent": 100,
      "min_value": 10000
    }
  },
  "burst_detection": {
    "enabled": true,
    "min_metrics": 2,
    "threshold": {
      "likes": 5000,
      "comments": 500,
      "shares": 1000
    }
  }
}
```

## 通知方式

### 邮件通知

```json
{
  "notification": {
    "email": {
      "smtp_server": "smtp.qq.com",
      "smtp_port": 587,
      "username": "your_email@qq.com",
      "password": "your_auth_code",
      "to": ["recipient@example.com"]
    }
  }
}
```

### 钉钉机器人

```json
{
  "notification": {
    "dingtalk": {
      "webhook": "https://oapi.dingtalk.com/robot/send?access_token=xxx",
      "secret": "your_secret"
    }
  }
}
```

### 飞书机器人

```json
{
  "notification": {
    "feishu": {
      "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
    }
  }
}
```

### 企业微信

```json
{
  "notification": {
    "wecom": {
      "webhook": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
    }
  }
}
```

## 数据存储

### 数据文件结构

```
assets/data/
├── raw/                    # 原始抓取数据
│   ├── task_001/
│   │   ├── 2024-01-15.json
│   │   └── 2024-01-16.json
│   └── task_002/
├── processed/              # 处理后数据
│   └── trends/
└── alerts/                 # 异常记录
    └── 2024-01-16.json
```

### 数据格式

```json
{
  "task_id": "task_001",
  "timestamp": "2024-01-16T10:00:00",
  "url": "https://...",
  "data": {
    "likes": 15234,
    "comments": 892,
    "shares": 3456,
    "views": 125000
  },
  "changes": {
    "likes": {"value": 1234, "percent": 8.8},
    "comments": {"value": 89, "percent": 11.1}
  },
  "alert_triggered": false
}
```

## 使用方法

### 快速开始

1. **复制配置文件**
```bash
cp assets/config/monitor_tasks.example.json assets/config/monitor_tasks.json
```

2. **编辑配置**
```bash
vim assets/config/monitor_tasks.json
```

3. **启动监控**
```bash
python scripts/monitor_service.py start
```

### 命令行工具

```bash
# 添加监控任务
python scripts/monitor_cli.py add --name "竞品A" --url "https://..." --platform douyin

# 列出所有任务
python scripts/monitor_cli.py list

# 手动执行一次监控
python scripts/monitor_cli.py run --task task_001

# 查看监控数据
python scripts/monitor_cli.py data --task task_001 --days 7

# 生成趋势报告
python scripts/monitor_cli.py report --task task_001 --output report.html

# 停止监控服务
python scripts/monitor_service.py stop
```

### 单次监控任务

```bash
# 单次抓取数据
python scripts/scraper.py --url "https://..." --platform douyin --output data.json

# 带截图
python scripts/scraper.py --url "https://..." --platform douyin --screenshot
```

## 技术实现

### 依赖安装

```bash
pip install playwright schedule pandas requests
playwright install chromium
```

### 核心模块

| 模块 | 功能 |
|------|------|
| `scraper.py` | 网页数据抓取 |
| `detector.py` | 异常检测算法 |
| `notifier.py` | 通知发送 |
| `scheduler.py` | 定时任务调度 |
| `storage.py` | 数据存储管理 |
| `monitor_service.py` | 监控服务主程序 |

## 注意事项

1. **合规性**：请遵守各平台的robots协议和使用条款
2. **频率控制**：避免过于频繁的抓取，建议间隔不小于1小时
3. **反爬处理**：部分平台可能有反爬机制，需要适当调整
4. **数据隐私**：注意保护抓取的数据，不要泄露敏感信息
5. **稳定性**：建议将监控服务部署在稳定的服务器上

## 文件结构

```
competitor-monitor/
├── SKILL.md                    # Skill主文件
├── README.md                   # 使用说明
├── INSTALL_GUIDE.md            # 安装指南
├── install.sh                  # 安装脚本
├── scripts/
│   ├── monitor_service.py      # 监控服务主程序
│   ├── monitor_cli.py          # 命令行工具
│   ├── scraper.py              # 数据抓取模块
│   ├── detector.py             # 异常检测模块
│   ├── notifier.py             # 通知模块
│   ├── scheduler.py            # 定时任务模块
│   ├── storage.py              # 数据存储模块
│   └── dashboard.py            # 数据可视化
├── assets/
│   ├── config/
│   │   ├── monitor_tasks.example.json  # 配置示例
│   │   └── platforms.json      # 平台预设配置
│   ├── screenshots/            # 截图存档
│   └── data/                   # 数据存档
└── references/
    └── PLATFORM_SELECTORS.md   # 平台选择器参考
```

## 示例场景

### 场景1：监控竞品抖音视频

```json
{
  "id": "douyin_001",
  "name": "竞品抖音视频监控",
  "platform": "douyin",
  "url": "https://www.douyin.com/video/1234567890",
  "schedule": "0 */2 * * *",
  "metrics": ["likes", "comments", "shares"],
  "alert_threshold": {
    "likes": {"increase_percent": 50, "min_value": 5000}
  },
  "screenshot_on_alert": true
}
```

### 场景2：监控小红书爆款笔记

```json
{
  "id": "xhs_001",
  "name": "小红书爆款监控",
  "platform": "xiaohongshu",
  "url": "https://www.xiaohongshu.com/explore/abcdef",
  "schedule": "0 */4 * * *",
  "metrics": ["likes", "collections", "comments"],
  "alert_threshold": {
    "likes": {"increase_percent": 100, "min_value": 1000},
    "collections": {"increase_percent": 80, "min_value": 500}
  },
  "burst_detection": {
    "enabled": true,
    "min_metrics": 2
  }
}
```

### 场景3：监控淘宝商品销量

```json
{
  "id": "taobao_001",
  "name": "竞品销量监控",
  "platform": "taobao",
  "url": "https://item.taobao.com/item.htm?id=123456",
  "schedule": "0 9,18 * * *",
  "metrics": ["sell_count", "rate_count", "price"],
  "alert_threshold": {
    "sell_count": {"increase_percent": 30, "min_value": 100}
  }
}
```
