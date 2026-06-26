# CID 投流追踪技能 - 快速开始指南

## ✅ 技能已创建完成！

**技能位置:** `C:\Users\Administrator\.openclaw\workspace\skills\cid-tracking`

## 📦 技能结构

```
cid-tracking/
├── SKILL.md                  # 技能描述
├── README.md                 # 完整文档
├── requirements.txt          # Python 依赖
├── config.example.json       # 配置模板
├── scripts/
│   ├── cid_generator.py      # CID 生成器
│   ├── data_fetcher.py       # 数据获取器
│   ├── conversion_tracker.py # 转化回传器
│   ├── roi_analyzer.py       # ROI 分析器
│   ├── report_generator.py   # Excel 报表生成器
│   └── anomaly_detector.py   # 异常检测器
└── references/
    ├── oceanengine_api.md    # 巨量引擎 API 参考
    ├── kuaishou_api.md       # 快手 API 参考
    ├── tencent_api.md        # 广点通 API 参考
    └── cid_best_practices.md # CID 最佳实践
```

## 🚀 5 分钟快速上手

### 1️⃣ 安装依赖

```bash
cd skills/cid-tracking
pip install -r requirements.txt
```

### 2️⃣ 配置 API 凭证

```bash
cp config.example.json config.json
# 编辑 config.json，填写你的平台凭证
```

### 3️⃣ 生成 CID 追踪链接

```bash
python scripts/cid_generator.py -p oceanengine -c 123456 -u "https://your-landing-page.com" -n 10
```

### 4️⃣ 生成测试报表（无需 API）

使用已创建的测试数据：

```bash
python scripts/report_generator.py -i test_data.json -o daily_report.xlsx -d 2026-03-21
```

打开 `daily_report.xlsx` 查看效果！

## 📊 Excel 报表示例

生成的报表包含 4 个工作表：

1. **汇总看板** - 核心指标一览
   - 总消耗、总转化、总展示、总点击
   - CTR、CVR、CPC、CPA、ROI

2. **分平台数据** - 平台对比
   - 抖音、快手、腾讯各平台数据
   - 自动计算各平台 ROI

3. **计划明细** - 详细数据
   - 每个广告计划的完整数据
   - 按消耗排序

4. **异常监控** - 自动预警
   - ROI < 1.5 的计划（红色标记）
   - CPA > 100 的计划
   - 零转化但高消耗的计划

## 🔄 典型工作流

### 每日自动化

```bash
# 1. 获取昨天数据（需要配置 API 凭证）
python scripts/data_fetcher.py -p all -s yesterday -e yesterday -o data.json

# 2. 生成日报
python scripts/report_generator.py -i data.json -o reports/daily_$(date +%Y%m%d).xlsx

# 3. 检测异常
python scripts/anomaly_detector.py -i data.json --min-roi 1.5 --max-cpa 100 -a alert.txt

# 4. 发送预警
cat alert.txt | send-to-wechat  # 或其他通知方式
```

### 转化回传

```bash
# 订单支付成功后回传
python scripts/conversion_tracker.py \
  -p oceanengine \
  -c CID123456789 \
  -e purchase \
  -v 299.00 \
  -o ORDER_20260321_001
```

## 🎯 核心功能

| 功能 | 脚本 | 说明 |
|------|------|------|
| CID 生成 | `cid_generator.py` | 批量生成追踪链接 |
| 数据获取 | `data_fetcher.py` | 从平台 API 拉取数据 |
| 转化回传 | `conversion_tracker.py` | 回传订单数据 |
| ROI 分析 | `roi_analyzer.py` | 多维度分析 |
| Excel 报表 | `report_generator.py` | 专业报表生成 |
| 异常检测 | `anomaly_detector.py` | 自动预警 |

## ⚙️ 配置说明

### config.json

```json
{
  "oceanengine": {
    "app_id": "你的应用 ID",
    "access_token": "访问令牌"
  },
  "kuaishou": {
    "app_id": "你的应用 ID",
    "access_token": "访问令牌"
  },
  "tencent": {
    "account_id": "账户 ID",
    "secret_id": "密钥 ID",
    "secret_key": "密钥"
  },
  "report": {
    "output_dir": "./reports",
    "include_charts": true
  },
  "anomaly": {
    "min_roi": 1.5,
    "max_cpa": 100
  }
}
```

## 📝 常用命令

### CID 生成

```bash
# 单个 CID
python scripts/cid_generator.py -p oceanengine -c 123456 -u "https://example.com"

# 批量生成 100 个
python scripts/cid_generator.py -p oceanengine -c 123456 -u "https://example.com" -n 100 -o cids.json

# 快手平台
python scripts/cid_generator.py -p kuaishou -c 789012 -u "https://example.com"
```

### 数据分析

```bash
# ROI 分析（按平台分组）
python scripts/roi_analyzer.py -i data.json -g platform -o roi.json

# ROI 分析（按计划分组）
python scripts/roi_analyzer.py -i data.json -g campaign -t 20

# 异常检测
python scripts/anomaly_detector.py -i data.json --min-roi 1.5 --max-cpa 100
```

## 🛠️ 故障排查

### 问题：找不到模块

```bash
pip install -r requirements.txt --upgrade
```

### 问题：API 认证失败

检查 `config.json` 中的凭证是否正确，确保：
- app_id 正确
- access_token 未过期
- 账号有 API 权限

### 问题：Excel 生成失败

检查是否有写入权限，确保输出目录存在。

## 📚 参考资料

- [完整文档](README.md)
- [巨量引擎 API](references/oceanengine_api.md)
- [快手 API](references/kuaishou_api.md)
- [广点通 API](references/tencent_api.md)
- [CID 最佳实践](references/cid_best_practices.md)

## 💡 下一步

1. **申请 API 权限** - 访问各平台开放平台
2. **配置凭证** - 编辑 `config.json`
3. **测试流程** - 使用 `test_data.json` 测试报表
4. **接入生产** - 配置定时任务自动运行

## 🤝 需要帮助？

查看详细文档：`README.md`

---

**祝你使用愉快！** 🎉
