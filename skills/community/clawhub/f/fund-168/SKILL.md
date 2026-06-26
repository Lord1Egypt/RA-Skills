---
name: fund-168
description: |
  基金监控技能。管理自选基金列表，监控场外基金、ETF基金的压力位和支撑位。
  支持添加/删除自选基金，自动计算压力位 (智能判断：若 20 日均线×1.05 大于当前价格则输出该值，否则输出当前净值×1.05) 和支撑位 (智能判断：若 20 日均线×0.95 小于当前价格则输出该值，否则输出当前净值×0.95)。
  支持独立任务模式（task参数）：每只基金创建独立定时任务，间隔1分钟逐个执行，避免API并发限制。
  支持涨跌幅告警：当日涨跌幅超阈值时主动推送。
  支持持仓盈亏追踪：记录成本价，自动计算浮动盈亏。
  支持备份导出（backup）：将所有任务明细导出为CSV/XLSX表格到本地C盘，方便归档与查看。
  支持多渠道推送：企业微信/钉钉/飞书/邮件。
  支持系统自检：检查API连通性、数据目录、cron状态。
  支持自定义均线周期（5/10/20/30/60日）。
  支持Watchlist导入导出。
  使用场景：基金监控、自选基金管理、净值提醒、技术分析辅助、盈亏追踪。
  触发词：基金监控、自选基金、压力位、支撑位、fund-005、添加基金、删除基金、监控时间、task、backup、备份、导出、涨跌幅、告警、盈亏、持仓、自检
---

# Fund-005 - 基金监控技能

## 概述

本技能用于监控自选基金的净值动态，自动计算压力位和支撑位，并在指定时间进行监控提醒。提供独立任务模式、涨跌幅告警、持仓盈亏追踪、备份导出等完整功能。

## 核心功能

### 1. 自选基金管理
- 添加自选基金（支持场外基金、ETF基金）
- 删除自选基金
- 查看自选基金列表
- 导入/导出自选基金列表（JSON格式）

### 2. 技术分析
- **压力位**：智能判断
  - 若（20 日均线 × 1.05）> 当前价格，输出（20 日均线 × 1.05）
  - 若（20 日均线 × 1.05）≤ 当前价格，输出（当前净值 × 1.05）
- **支撑位**：智能判断
  - 若（20日均线 × 0.95）< 当前价格，输出（20日均线 × 0.95）
  - 若（20日均线 × 0.95）≥ 当前价格，输出（当前净值 × 0.95）
- 所有数值保留四位小数（基金净值精度更高）
- 支持自定义均线周期（5/10/20/30/60日），默认20日

### 3. 独立任务模式（task参数）
- 每只基金创建独立的定时监控任务（cron job）
- 任务按间隔1分钟逐个启动，避免并发请求API被限流
- 支持单只基金独立添加/删除任务
- 支持批量为所有自选基金创建任务
- 支持查看当前所有任务状态

### 4. 涨跌幅告警
- 设置涨跌幅阈值（如 ±3%），触发时主动推送告警
- 支持按基金单独设置阈值，也支持全局默认阈值
- 盘中估值触发和收盘确认触发两种模式

### 5. 持仓盈亏追踪
- 记录每只基金的买入成本价和持有份额
- 监控报告中自动计算浮动盈亏（金额+百分比）
- 支持多次买入的成本均价计算

### 6. 备份导出（backup）
- 将所有任务明细导出为CSV或XLSX表格
- 默认导出到 `C:\fund_monitor_backup\` 目录
- 支持自定义导出路径
- 文件名自动加时间戳，防止覆盖；XLSX文件自动加 `月日` 中文前缀

### 7. 多渠道推送
- 企业微信Webhook（默认）
- 钉钉机器人Webhook
- 飞书机器人Webhook
- 邮件（SMTP）
- 支持同时推送多个渠道

### 8. 系统自检
- 检查API数据源连通性
- 检查数据目录权限
- 检查cron任务运行状态
- 检查依赖库是否安装

## 快速开始

### 基础使用流程

```bash
# 1. 添加自选基金
python fund_monitor_wechat.py add 000001 华夏成长混合 场外基金
python fund_monitor_wechat.py add 510300 沪深300ETF ETF基金

# 2. 设置企业微信推送
python fund_monitor_wechat.py webhook https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY

# 3. 创建独立监控任务
python fund_monitor_wechat.py task batch 14:30 1

# 4. 立即执行监控测试
python fund_monitor_wechat.py monitor --wechat
```

### 命令速查

| 命令类别 | 常用命令 |
|---------|---------|
| 自选基金管理 | `add`, `remove`, `list`, `watchlist export/import` |
| 任务管理 | `task add`, `task batch`, `task list`, `task remove` |
| 监控执行 | `monitor`, `monitor-single`, `times` |
| 涨跌幅告警 | `alert threshold`, `alert set`, `alert list` |
| 持仓盈亏 | `hold add`, `hold remove`, `hold list` |
| 推送设置 | `push add`, `webhook`, `push list` |
| 备份导出 | `backup`, `backup list` |
| 系统管理 | `doctor`, `--version` |

## 详细使用指南

### 自选基金管理

#### 添加自选基金

```bash
# 语法：python fund_monitor_wechat.py add <基金代码> <基金名称> <基金类型>
python fund_monitor_wechat.py add 000001 华夏成长混合 场外基金
python fund_monitor_wechat.py add 510300 沪深300ETF ETF基金
python fund_monitor_wechat.py add 110022 易方达消费行业 场外基金
```

#### 删除自选基金

```bash
# 语法：python fund_monitor_wechat.py remove <基金代码>
python fund_monitor_wechat.py remove 000001
```

#### 查看自选基金列表

```bash
python fund_monitor_wechat.py list
```

#### 导入导出Watchlist

```bash
# 导出为JSON（默认）
python fund_monitor_wechat.py watchlist export

# 指定导出路径
python fund_monitor_wechat.py watchlist export --path D:\watchlist_backup.json

# 导入（默认追加模式，不覆盖已有基金）
python fund_monitor_wechat.py watchlist import watchlist_backup.json

# 覆盖模式（清空后导入）
python fund_monitor_wechat.py watchlist import watchlist_backup.json --overwrite
```

### 自定义均线周期

默认使用20日均线，可按需调整为5/10/30/60日：

```bash
# 全局默认改为10日均线
python fund_monitor_wechat.py ma period 10

# 为单只基金指定均线周期
python fund_monitor_wechat.py ma set 000001 30
python fund_monitor_wechat.py ma set 510300 5

# 查看当前均线配置
python fund_monitor_wechat.py ma list
```

#### 均线周期与压力/支撑位的关系

```
MA周期越短 → 对近期价格越敏感 → 压力/支撑位波动更大
MA周期越长 → 趋势越平滑 → 压力/支撑位更稳定

建议：
- 场外基金（波动小）：20日或30日
- ETF基金（波动大）：10日或20日
- 短线操作：5日或10日
- 长线持有：30日或60日
```

### 独立任务模式（task参数）

#### 为单只基金创建独立监控任务

```bash
# 语法：task add <基金代码> [监控时间] [间隔分钟数]
# 默认监控时间 14:30，间隔 1 分钟

python fund_monitor_wechat.py task add 000001
python fund_monitor_wechat.py task add 510300
python fund_monitor_wechat.py task add 110022
```

以上命令会创建3个独立cron任务，分别在：
- `000001` → 14:30 执行
- `510300` → 14:31 执行（+1分钟）
- `110022` → 14:32 执行（+2分钟）

#### 指定自定义监控时间与间隔

```bash
# 语法：task add <基金代码> <起始时间> <间隔分钟数>

python fund_monitor_wechat.py task add 000001 10:00 1
python fund_monitor_wechat.py task add 510300 10:00 1
# 结果：000001 在 10:00 执行，510300 在 10:01 执行
```

#### 批量为所有自选基金创建任务

```bash
# 语法：task batch <起始时间> <间隔分钟数>
# 为 watchlist.json 中所有基金逐个创建独立任务

python fund_monitor_wechat.py task batch 14:30 1
```

输出示例：
```
📋 批量创建任务：共 3 只基金
────────────────────────────────────────────────────
  ✅ 000001 华夏成长混合     → 14:30
  ✅ 510300 沪深300ETF      → 14:31
  ✅ 110022 易方达消费行业   → 14:32
────────────────────────────────────────────────────
end
```

#### 任务管理命令

```bash
# 删除单只基金的任务
python fund_monitor_wechat.py task remove 000001

# 删除所有任务
python fund_monitor_wechat.py task clear

# 暂停某只基金的监控（不删除，保留配置）
python fund_monitor_wechat.py task disable 000001

# 重新启用
python fund_monitor_wechat.py task enable 000001

# 查看当前所有任务
python fund_monitor_wechat.py task list
```

任务列表输出示例：
```
📋 基金监控任务列表
────────────────────────────────────────────────────
  000001 华夏成长混合     14:30 每日 ✅
  510300 沪深300ETF      14:31 每日 ✅
  110022 易方达消费行业   14:32 每日 ✅
────────────────────────────────────────────────────
  📋 共 3 个任务，间隔 1 分钟
────────────────────────────────────────────────────
end
```

### 备份导出（backup）

#### 导出所有任务明细为CSV表格

```bash
# 默认导出到 C:\fund_monitor_backup\ 目录，文件名自动加时间戳
python fund_monitor_wechat.py backup

# 指定导出格式（csv / xlsx）
python fund_monitor_wechat.py backup --format xlsx

# 指定自定义导出路径
python fund_monitor_wechat.py backup --path D:\my_backups
```

#### 导出内容

每行对应一只基金的任务明细，包含以下列：

| 列名 | 说明 | 示例 |
|------|------|------|
| 序号 | 任务执行顺序 | 1 |
| 基金代码 | 6位基金代码 | 000001 |
| 基金名称 | 基金全称 | 华夏成长混合 |
| 基金类型 | 场外基金 / ETF基金 | 场外基金 |
| 监控时间 | 该任务的执行时间 | 14:30 |
| 间隔(分钟) | 相对前一任务的间隔 | 1 |
| 是否启用 | 任务状态 | 是 |
| 最新净值 | 最近一次监控的净值 | 1.4512 |
| 压力位 | 计算得出的压力位 | 1.5234 |
| 支撑位 | 计算得出的支撑位 | 1.3789 |
| 更新时间 | 最后一次数据更新时间 | 2026-03-24 14:31 |

#### 查看备份历史

```bash
# 列出 C:\fund_monitor_backup\ 下所有备份文件
python fund_monitor_wechat.py backup list
```

输出示例：
```
📁 备份文件列表：C:\fund_monitor_backup\
────────────────────────────────────────────────────
  fund_tasks_2026-03-24_143000.csv       2.3 KB
  3月23日_fund_tasks.xlsx                8.1 KB
  fund_tasks_2026-03-22_143000.csv       2.1 KB
  3月22日_fund_tasks.xlsx                8.0 KB
────────────────────────────────────────────────────
  📋 共 4 个备份文件
────────────────────────────────────────────────────
end
```

### 传统批量监控（兼容旧版）

```bash
# 查看监控配置
python fund_monitor_wechat.py times

# 添加监控时间
python fund_monitor_wechat.py addtime 14:30
python fund_monitor_wechat.py addtime 10:00

# 删除监控时间
python fund_monitor_wechat.py removetime 14:30

# 立即执行全部监控
python fund_monitor_wechat.py monitor

# 执行监控并发送到企业微信
python fund_monitor_wechat.py monitor --wechat
```

### 企业微信推送设置

```bash
python fund_monitor_wechat.py webhook https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
```

### 多渠道推送设置

#### 钉钉机器人

```bash
python fund_monitor_wechat.py push add dingtalk https://oapi.dingtalk.com/robot/send?access_token=xxx
python fund_monitor_wechat.py push add dingtalk https://oapi.dingtalk.com/robot/send?access_token=xxx --secret SECxxx
```

#### 飞书机器人

```bash
python fund_monitor_wechat.py push add feishu https://open.feishu.cn/open-apis/bot/v2/hook/xxx
```

#### 邮件（SMTP）

```bash
python fund_monitor_wechat.py push add email --smtp smtp.qq.com --port 465 --from xxx@qq.com --to receiver@qq.com --password xxx
```

#### 查看/删除推送渠道

```bash
python fund_monitor_wechat.py push list       # 查看所有渠道
python fund_monitor_wechat.py push remove dingtalk  # 删除钉钉渠道
```

### 涨跌幅告警

#### 设置全局默认阈值

```bash
# 涨跌幅超过 ±3% 时告警（默认）
python fund_monitor_wechat.py alert threshold 3

# 改为 ±5%
python fund_monitor_wechat.py alert threshold 5
```

#### 为单只基金设置单独阈值

```bash
# 000001 涨跌幅超过 ±2% 就告警
python fund_monitor_wechat.py alert set 000001 2

# 510300（波动大的ETF）设为 ±1%
python fund_monitor_wechat.py alert set 510300 1
```

#### 查看/删除告警阈值

```bash
python fund_monitor_wechat.py alert list          # 查看所有阈值
python fund_monitor_wechat.py alert remove 000001 # 删除单独设置，恢复默认
```

#### 告警触发模式

```bash
# 盘中估值触发（实时，可能有误差）
python fund_monitor_wechat.py alert mode realtime

# 收盘确认触发（准确，但延迟到收盘后，默认）
python fund_monitor_wechat.py alert mode close
```

#### 告警报告示例

```
⚠️ 涨跌幅告警 [2026-03-24 14:15]
────────────────────────────────────────────────────
  【易方达消费行业】110022
    估算涨幅：+3.52%  🔔 超过阈值 ±3%
    最新估值：2.1234
    昨日收盘：2.0510
    压 力 位：2.1567
    支 撑 位：1.9523
    重点关注：1.95
────────────────────────────────────────────────────
end
```

### 持仓盈亏追踪

#### 记录持仓成本

```bash
# 买入记录：基金代码 成本价 份额
python fund_monitor_wechat.py hold add 000001 1.3500 10000
python fund_monitor_wechat.py hold add 000001 1.4200 5000   # 多次买入，自动计算均价

# 删除持仓
python fund_monitor_wechat.py hold remove 000001

# 查看持仓列表
python fund_monitor_wechat.py hold list
```

#### 持仓报告示例

```
💰 持仓盈亏报告 [2026-03-24 14:30]
────────────────────────────────────────────────────
  【华夏成长混合】000001
    持仓均价：1.3733
    持有份额：15000
    最新净值：1.4512
    浮动盈亏：+1168.50 (+5.67%)
    压 力 位：1.5234
    支 撑 位：1.3789
    重点关注：1.38

  ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
  总持仓成本：20600.00
  总 市 值：21768.00
  总浮动盈亏：+1168.00 (+5.67%)
────────────────────────────────────────────────────
end
```

### 系统自检

```bash
python fund_monitor_wechat.py doctor
```

输出示例：
```
🏥 系统自检报告 [2026-03-24 14:30]
────────────────────────────────────────────────────
  ✅ Python版本：3.10.0
  ✅ requests库：已安装 (2.31.0)
  ✅ openpyxl库：已安装 (3.1.2)
  ✅ 数据目录：data/ 可读写
  ✅ 日志目录：data/logs/ 可读写
  ✅ 天天基金API：连通正常 (120ms)
  ✅ DoctorXiong API：连通正常 (200ms)
  ⚠️ 腾讯财经API：响应较慢 (1500ms)
  ✅ watchlist.json：格式正确，3只基金
  ✅ config.json：格式正确
  ✅ cron任务：3个运行中，0个异常
  ✅ 企业微信Webhook：可达
  ⚠️ 备份目录：不存在（首次backup时自动创建）

  📋 总结：10项通过 / 2项警告 / 0项异常
────────────────────────────────────────────────────
end
```

### 版本信息

```bash
python fund_monitor_wechat.py --version
```

输出示例：
```
fund-005 v2.1.0
基金监控技能 · 多源API降级 · 独立任务模式 · 涨跌幅告警 · 持仓盈亏追踪
```

## 数据存储

### 配置文件

| 文件 | 用途 |
|------|------|
| `data/watchlist.json` | 自选基金列表 |
| `data/config.json` | 监控配置、任务配置、备份配置 |
| `data/push_channels.json` | 多渠道推送配置 |
| `data/alert_config.json` | 涨跌幅告警阈值配置 |
| `data/holdings.json` | 持仓成本与份额数据 |
| `data/holidays.json` | 法定节假日日期列表 |
| `data/workdays.json` | 调休补班日期列表 |
| `data/logs/YYYY-MM-DD.log` | 每日运行日志 |

### 监控配置示例

`data/config.json`:

```json
{
  "monitor_times": ["14:30"],
  "webhook_url": "",
  "default_ma_period": 20,
  "alert": {
    "default_threshold": 3,
    "mode": "close"
  },
  "backup": {
    "format": "csv",
    "path": "C:\\fund_monitor_backup",
    "auto_backup": false,
    "auto_backup_schedule": "weekly"
  },
  "tasks": {
    "000001": {
      "time": "14:30",
      "interval_min": 1,
      "order": 0,
      "enabled": true,
      "cron_id": "fund-task-000001",
      "last_nav": 1.4512,
      "last_date": "2026-03-24",
      "last_pressure": 1.5234,
      "last_support": 1.3789
    }
  }
}
```

## 技术实现

### 多源API降级策略

采用三梯队API自动降级，按优先级依次尝试：

#### 第一梯队：天天基金（主用）
- 实时估值：`http://fundgz.1234567.com.cn/js/{code}.js`
- 历史净值：`http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={code}&page=1&per=20`
- 基金信息：`http://fund.eastmoney.com/js/{code}.js`

#### 第二梯队：备用API（天天基金不可用时降级）
- 实时净值：`https://api.doctorxiong.club/v1/fund?code={code}`
- 历史净值：`https://api.doctorxiong.club/v1/fund/netWorth?code={code}`
- 基金搜索：`https://api.doctorxiong.club/v1/fund/search?keyword={keyword}`

#### 第三梯队：兜底API
- 基金实时数据：`https://qt.gtimg.cn/q=ff{code}`（腾讯财经）
- ETF行情：`https://hq.sinajs.cn/list=ff_{code}`（新浪财经）

### 依赖清单

| 库名 | 用途 | 是否必需 |
|------|------|----------|
| `requests` | HTTP请求 | ✅ 必需 |
| `json` | 数据解析（标准库） | ✅ 必需 |
| `re` | JSONP正则提取（标准库） | ✅ 必需 |
| `csv` | CSV导出（标准库） | ✅ 必需 |
| `openpyxl` | XLSX导出 | ⚡ 仅XLSX需要 |
| `smtplib` | 邮件发送（标准库） | ⚡ 仅邮件推送需要 |

安装命令：
```bash
pip install requests
pip install openpyxl  # 仅需XLSX导出时安装
```

### 计算公式

- MA20 = 最近20个交易日净值平均值
- 压力位：
  - 若 (MA20 × 1.05) > 当前净值：压力位 = MA20 × 1.05
  - 若 (MA20 × 1.05) ≤ 当前净值：压力位 = 当前净值 × 1.05
- **支撑位**：
  - 若 (MA20 × 0.95) < 当前净值：支撑位 = MA20 × 0.95
  - 若 (MA20 × 0.95) ≥ 当前净值：支撑位 = 当前净值 × 0.95

### 输出格式规范

所有终端和推送输出遵循统一格式规范：

```
┌─ 标题行 ──────────────────────────────────────────┐
│ Emoji + 报告名 + [日期 时间]                        │
├─ 分隔线 ──────────────────────────────────────────┤
│ 固定52个 ─ 字符，所有报告统一使用                      │
├─ 内容区 ──────────────────────────────────────────┤
│ 缩进：首级2空格，次级4空格                            │
│ 冒号对齐：中文冒号后对齐数值                            │
│ Emoji状态标记：                                      │
│   ✅ 正常    ⚠️ 警告    ❌ 异常    📊 数据           │
│   📋 列表    ⏰ 时间    💰 金额    🔔 告警           │
├─ 汇总行 ──────────────────────────────────────────┤
│ 可选，多只基金时显示汇总                               │
└────────────────────────────────────────────────────┘
```

#### 格式细则

| 项目 | 规范 | 示例 |
|------|------|------|
| 分隔线 | 固定52个 `─` | `────────────────────────────────────────────────────` |
| 时间格式 | `YYYY-MM-DD HH:MM` | `2026-03-24 14:31` |
| 净值精度 | 保留4位小数 | `1.4512` |
| 百分比 | 带正负号，保留2位小数 | `+3.52%` / `-1.20%` |
| 金额精度 | 保留2位小数 | `+1168.50` |
| 重点关注 | 支撑位保留2位小数，紧跟支撑位下方显示 | `重点关注：3.55` |
| 缩进 | 标题2空格，明细4空格 | 见下方示例 |
| 结尾标记 | 所有报告统一加 `end` | — |

### 监控报告示例（单只基金任务推送）

```
📊 基金监控 [2026-03-24 14:31]
────────────────────────────────────────────────────
  【华夏成长混合】000001
    最新净值：1.4512
    压 力 位：1.5234
    支 撑 位：1.3789
    重点关注：1.38
────────────────────────────────────────────────────
end
```

## 注意事项

1. **基金代码格式**：
   - 场外基金：6位数字（如000001）
   - ETF基金：6位数字（如510300）

2. **交易日**：周末和节假日可能无法获取完整数据，task模式默认仅工作日执行

3. **API降级**：脚本内置三梯队API自动降级（天天基金 → DoctorXiong → 腾讯/新浪），无需手动切换。若全部不可用会跳过该基金并记录日志

4. **数据目录**：可通过环境变量 `LOOK_FUND_DATA_DIR` 自定义

5. **任务间隔**：建议间隔至少1分钟，避免天天基金API限流

6. **任务数量**：单用户建议不超过20个并发任务

7. **备份导出**：
   - CSV格式无需额外依赖，XLSX格式需安装`openpyxl`库
   - 默认导出到 `C:\fund_monitor_backup\`（Windows），其他系统请用 `--path` 指定路径
   - Linux/Mac示例：`python fund_monitor_wechat.py backup --path ~/fund_backup`

8. **task vs 批量监控**：
   - `task` 模式：每只基金独立任务，间隔执行，互不影响，单只失败不影响其他
   - `monitor` 批量模式：一次性查所有基金，适合快速查看

9. **涨跌幅告警**：
   - 盘中估值模式可能有误差（±0.5%），收盘确认模式更准确
   - 建议设置合理的阈值，过低会导致频繁告警

10. **持仓盈亏**：
    - 成本价和份额由用户手动录入，脚本不对接券商API
    - 多次买入自动计算加权均价：`均价 = Σ(价格×份额) / 总份额`

11. **多渠道推送**：
    - 同一条监控消息会推送到所有已启用的渠道
    - 钉钉机器人需配置加签密钥（`--secret`），否则消息可能被拦截

12. **均线周期**：
    - 切换均线周期后，压力位/支撑位会立即按新周期重新计算
    - 均线数据不足时（如设60日但只有30个交易日），用可用数据计算并提示

## 完整命令参考

### 自选基金管理

| 命令 | 说明 |
|------|------|
| `add <代码> <名称> <类型>` | 添加自选基金 |
| `remove <代码>` | 删除自选基金 |
| `list` | 查看自选基金列表 |
| `watchlist export [--path]` | 导出自选基金列表 |
| `watchlist import <文件> [--overwrite]` | 导入自选基金列表 |

### 任务管理

| 命令 | 说明 |
|------|------|
| `task add <代码> [时间] [间隔]` | 为单只基金创建监控任务 |
| `task batch <时间> <间隔>` | 批量创建所有基金的监控任务 |
| `task remove <代码>` | 删除单只基金的任务 |
| `task clear` | 删除所有任务 |
| `task enable <代码>` | 启用某只基金的任务 |
| `task disable <代码>` | 禁用某只基金的任务（保留配置） |
| `task list` | 查看所有任务状态 |

### 监控执行

| 命令 | 说明 |
|------|------|
| `times` | 查看监控时间配置 |
| `addtime <HH:MM>` | 添加监控时间点 |
| `removetime <HH:MM>` | 删除监控时间点 |
| `monitor` | 立即执行全部监控 |
| `monitor --wechat` | 执行监控并推送企业微信 |
| `monitor-single <代码>` | 监控单只基金 |

### 均线配置

| 命令 | 说明 |
|------|------|
| `ma period <天数>` | 设置全局默认均线周期 |
| `ma set <代码> <天数>` | 为单只基金指定均线周期 |
| `ma list` | 查看当前均线配置 |

### 涨跌幅告警

| 命令 | 说明 |
|------|------|
| `alert threshold <%>` | 设置全局涨跌幅阈值 |
| `alert set <代码> <%>` | 为单只基金设置单独阈值 |
| `alert remove <代码>` | 删除单只基金的单独阈值 |
| `alert mode <realtime/close>` | 设置告警触发模式 |
| `alert list` | 查看所有告警阈值 |

### 持仓盈亏

| 命令 | 说明 |
|------|------|
| `hold add <代码> <成本价> <份额>` | 记录买入成本 |
| `hold remove <代码>` | 删除持仓记录 |
| `hold list` | 查看持仓盈亏 |

### 推送渠道

| 命令 | 说明 |
|------|------|
| `webhook <URL>` | 设置企业微信Webhook（快捷方式） |
| `push add <类型> <URL> [options]` | 添加推送渠道 |
| `push remove <类型>` | 删除推送渠道 |
| `push list` | 查看所有推送渠道 |

### 备份导出

| 命令 | 说明 |
|------|------|
| `backup [options]` | 导出任务明细表格 |
| `backup list` | 查看历史备份文件 |

### 系统

| 命令 | 说明 |
|------|------|
| `doctor` | 系统自检 |
| `--version` | 查看版本信息 |

## 资源

### scripts/
本技能包含可执行脚本：

- `fund_monitor_wechat.py` - 基金监控主脚本
  - 完整实现所有基金监控功能
  - 支持独立任务模式、涨跌幅告警、持仓盈亏追踪
  - 多渠道推送：企业微信、钉钉、飞书、邮件
  - 备份导出：CSV/XLSX格式
  - 系统自检功能

### references/
参考文档和API信息：

- `api_endpoints.md` - 所有可用API端点列表
- `calculation_methods.md` - 压力位/支撑位计算方法详解
- `workflow_diagrams.md` - 工作流程图

### assets/
配置模板和示例文件：

- `config_template.json` - 配置文件模板
- `watchlist_example.json` - 自选基金列表示例
- `backup_template.csv` - 备份文件模板

