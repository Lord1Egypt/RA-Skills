# CID 投流追踪技能

专为**国内二类电商**设计的 CID（Click ID）投流追踪技能，支持抖音巨量引擎、快手磁力引擎、腾讯广点通三大广告平台。

## 🎯 功能特性

| 功能 | 说明 | 状态 |
|------|------|------|
| Click ID 生成 | 为每次广告点击生成唯一标识符 | ✅ |
| 转化回传 | 将订单数据回传到广告平台 | ✅ |
| ROI 分析 | 多维度投入产出比计算 | ✅ |
| Excel 报表 | 专业美观的日报/周报 | ✅ |
| 异常监控 | 低 ROI、高 CPA 自动预警 | ✅ |

## 📦 安装

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API 凭证

复制配置文件并填写你的平台凭证：

```bash
cp config.example.json config.json
```

编辑 `config.json`：

```json
{
  "oceanengine": {
    "app_id": "你的巨量引擎应用 ID",
    "access_token": "访问令牌"
  },
  "kuaishou": {
    "app_id": "你的磁力引擎应用 ID",
    "access_token": "访问令牌"
  },
  "tencent": {
    "account_id": "广点通账户 ID",
    "secret_id": "密钥 ID",
    "secret_key": "密钥"
  }
}
```

## 🚀 快速开始

### 生成 CID 追踪链接

```bash
# 抖音平台
python scripts/cid_generator.py -p oceanengine \
  -c 123456 \
  -u https://your-landing-page.com

# 快手平台
python scripts/cid_generator.py -p kuaishou \
  -c 789012 \
  -u https://your-landing-page.com

# 批量生成 100 个
python scripts/cid_generator.py -p oceanengine \
  -c 123456 \
  -u https://your-landing-page.com \
  -n 100 \
  -o cids.json
```

### 获取广告数据

```bash
# 获取昨天的数据
python scripts/data_fetcher.py -p all \
  -s 2026-03-20 -e 2026-03-20 \
  -o ads_data.json
```

### 生成 Excel 报表

```bash
python scripts/report_generator.py \
  -i ads_data.json \
  -o reports/daily_20260321.xlsx \
  -d 2026-03-21
```

### ROI 分析

```bash
python scripts/roi_analyzer.py \
  -i ads_data.json \
  -g platform \
  -o roi_analysis.json
```

### 异常检测

```bash
python scripts/anomaly_detector.py \
  -i ads_data.json \
  --min-roi 1.5 \
  --max-cpa 100 \
  -o anomalies.json \
  -a alert.txt
```

### 转化回传

```bash
# 回传一笔订单
python scripts/conversion_tracker.py \
  -p oceanengine \
  -c CID123456789 \
  -e purchase \
  -v 299.00 \
  -o ORDER_20260321_001
```

## 📊 Excel 报表结构

生成的报表包含 4 个工作表：

1. **汇总看板** - 核心指标总览（消耗、转化、CTR、CVR、ROI 等）
2. **分平台数据** - 抖音/快手/腾讯对比
3. **计划明细** - 每个广告计划的详细数据
4. **异常监控** - 低 ROI、高 CPA 计划列表

## 🔄 自动化工作流

### 每日定时任务（建议使用 OpenClaw cron）

```bash
# 1. 获取昨天数据
python scripts/data_fetcher.py -p all -s yesterday -e yesterday -o data.json

# 2. 生成日报
python scripts/report_generator.py -i data.json -o reports/daily.xlsx

# 3. 检测异常
python scripts/anomaly_detector.py -i data.json -a alert.txt

# 4. 发送预警（集成微信/钉钉）
cat alert.txt | send-to-wechat
```

## ⚠️ 注意事项

1. **API 凭证** - 需要先在各自平台申请 API 权限
   - 巨量引擎：https://ad.oceanengine.com/open-platform
   - 磁力引擎：https://mp.kuaishou.com/
   - 广点通：https://e.qq.com/dev/

2. **数据延迟** - 广告平台数据通常有 2-4 小时延迟

3. **API 限流** - 建议设置合理的请求间隔，避免触发限流

4. **转化归因** - 默认 7 天点击归因窗口，可根据实际情况调整

## 🛠️ 脚本说明

| 脚本 | 功能 | 主要参数 |
|------|------|----------|
| `cid_generator.py` | 生成 CID 追踪链接 | `-p` 平台，`-c` 计划 ID，`-u` 落地页，`-n` 数量 |
| `data_fetcher.py` | 获取广告数据 | `-p` 平台，`-s` 开始日期，`-e` 结束日期 |
| `conversion_tracker.py` | 转化回传 | `-p` 平台，`-c` CID，`-e` 事件，`-v` 价值 |
| `roi_analyzer.py` | ROI 分析 | `-i` 输入，`-g` 分组维度，`-t` Top N |
| `report_generator.py` | Excel 报表 | `-i` 输入，`-o` 输出，`-d` 日期 |
| `anomaly_detector.py` | 异常检测 | `-i` 输入，`--min-roi`，`--max-cpa` |

## 📝 常见问题

### Q: 如何获取 API 凭证？
A: 各平台开放平台申请：
- 巨量引擎：登录后台 → 开发工具 → API 管理
- 磁力引擎：营销平台 → 开发者中心
- 广点通：腾讯广告平台 → API 接入

### Q: ROI 计算准确吗？
A: 当前使用估算公式：`ROI = (转化数 × 客单价) / 消耗`
默认客单价 200 元，可根据实际情况修改脚本中的参数。

### Q: 如何对接自己的订单系统？
A: 修改 `conversion_tracker.py`，添加自己的订单数据源，调用回传 API 即可。

## 📄 许可证

MIT-0

## 👥 支持

如有问题，请提交 Issue 或联系开发者。
