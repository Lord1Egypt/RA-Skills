# 竞品数据定时监控 Skill

定时访问指定电商或社交平台页面，抓取点赞、评论、销量等数据，检测数据异常波动（如出现爆款），自动截图并发送提醒通知。

## 功能特点

- ⏰ **定时监控**：支持自定义监控频率（每小时/每天/每周）
- 📊 **数据抓取**：自动抓取点赞、评论、销量等关键指标
- 🔍 **异常检测**：检测数据暴增、骤降、持续趋势等异常
- 🔥 **爆款识别**：综合多指标判断是否为爆款
- 📸 **自动截图**：异常时自动截图保存
- 📢 **多平台通知**：支持邮件、钉钉、飞书、企业微信

## 支持平台

| 平台 | 支持指标 |
|------|----------|
| **抖音** | 点赞、评论、分享、播放量 |
| **小红书** | 点赞、收藏、评论 |
| **微博** | 转发、评论、点赞、阅读量 |
| **B站** | 播放量、点赞、投币、收藏、评论 |
| **快手** | 点赞、评论、播放量 |
| **淘宝/天猫** | 销量、评价数、价格 |
| **京东** | 评价数、价格 |
| **拼多多** | 销量、价格 |

## 快速开始

### 1. 安装依赖

```bash
pip install playwright schedule requests pandas
playwright install chromium
```

### 2. 配置监控任务

```bash
# 复制配置文件示例
cp assets/config/monitor_tasks.example.json assets/config/monitor_tasks.json

# 编辑配置
vim assets/config/monitor_tasks.json
```

### 3. 启动监控服务

```bash
# 启动定时监控服务
python scripts/monitor_service.py start --config assets/config/monitor_tasks.json

# 后台运行
nohup python scripts/monitor_service.py start > monitor.log 2>&1 &
```

### 4. 单次测试

```bash
# 执行一次监控任务
python scripts/monitor_service.py run --task douyin_001

# 抓取单个页面
python scripts/scraper.py --url "https://www.douyin.com/video/xxxxx" --platform douyin --screenshot
```

## 配置说明

### 任务配置

```json
{
  "id": "任务唯一ID",
  "name": "任务名称",
  "platform": "平台类型",
  "url": "监控页面URL",
  "schedule": "定时规则(cron格式)",
  "metrics": ["监控指标列表"],
  "alert_threshold": {
    "指标名": {
      "increase_percent": "增长率阈值(%)",
      "min_value": "最小触发值",
      "window": "历史数据窗口"
    }
  },
  "screenshot_on_alert": true,
  "notification": {
    "dingtalk": {...},
    "email": {...}
  }
}
```

### 定时规则（Cron格式）

| 规则 | 说明 |
|------|------|
| `0 */2 * * *` | 每2小时 |
| `0 */4 * * *` | 每4小时 |
| `0 9,18 * * *` | 每天9点和18点 |
| `0 */1 * * *` | 每小时 |
| `0 */6 * * 1-5` | 工作日每6小时 |

### 异常检测阈值

```json
{
  "alert_threshold": {
    "likes": {
      "increase_percent": 50,  // 增长率超过50%
      "min_value": 5000,       // 且当前值超过5000
      "window": 3              // 与最近3次数据比较
    }
  },
  "burst_detection": {
    "enabled": true,
    "min_metrics": 2,  // 至少2个指标同时触发
    "threshold": {
      "likes": 10000,
      "comments": 1000
    }
  }
}
```

## 通知配置

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

### 邮件

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

## 命令行工具

```bash
# 启动监控服务
python scripts/monitor_service.py start

# 执行一次监控
python scripts/monitor_service.py run
python scripts/monitor_service.py run --task task_id

# 生成监控报告
python scripts/monitor_service.py report
python scripts/monitor_service.py report --days 7 --output report.md

# 抓取单个页面
python scripts/scraper.py --url "https://..." --platform douyin --screenshot

# 测试异常检测
python scripts/detector.py

# 测试通知
python scripts/notifier.py
```

## 数据存储

```
assets/data/
├── raw/                    # 原始抓取数据
│   ├── task_001/
│   │   ├── 2024-01-15.jsonl
│   │   └── 2024-01-16.jsonl
│   └── task_002/
├── alerts/                 # 异常记录
│   └── 2024-01-16.jsonl
└── screenshots/            # 截图存档
    └── task_001_20240116_120000.png
```

## 异常检测类型

| 类型 | 说明 | 触发条件 |
|------|------|----------|
| **暴增 (SPIKE)** | 数据快速增长 | 增长率超过阈值 |
| **骤降 (DROP)** | 数据快速下降 | 下降率超过阈值 |
| **持续上升 (TREND_UP)** | 连续多次上升 | 连续N次增长 |
| **持续下降 (TREND_DOWN)** | 连续多次下降 | 连续N次下降 |
| **爆款 (BURST)** | 多指标同时爆发 | 多个指标同时超过阈值 |
| **阈值 (THRESHOLD)** | 超过绝对值阈值 | 达到设定的绝对值 |

## 文件结构

```
competitor-monitor/
├── SKILL.md                    # Skill主文件
├── README.md                   # 使用说明
├── scripts/
│   ├── monitor_service.py      # 监控服务主程序
│   ├── scraper.py              # 数据抓取模块
│   ├── detector.py             # 异常检测模块
│   └── notifier.py             # 通知模块
├── assets/
│   ├── config/
│   │   └── monitor_tasks.example.json
│   ├── data/                   # 数据存储
│   └── screenshots/            # 截图存储
└── references/
    └── PLATFORM_SELECTORS.md   # 平台选择器参考
```

## 注意事项

1. **合规性**：请遵守各平台的robots协议和使用条款
2. **频率控制**：避免过于频繁的抓取，建议间隔不小于1小时
3. **反爬处理**：部分平台可能有反爬机制
4. **数据隐私**：注意保护抓取的数据
5. **稳定性**：建议将监控服务部署在稳定的服务器上

## 许可证

MIT License
