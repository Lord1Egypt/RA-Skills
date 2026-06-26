---
name: cid-tracking
version: 1.0.0
description: 国内二类电商 CID 投流追踪技能，支持抖音巨量引擎、快手磁力引擎、腾讯广点通。提供 Click ID 生成、转化回传、ROI 分析、数据看板、异常监控功能，输出专业 Excel 报表。Use when: (1) 管理多平台广告投流数据，(2) 生成 CID 追踪报表，(3) 分析广告 ROI 和转化效果，(4) 监控异常广告计划，(5) 自动化日报周报。
---

# CID 投流追踪技能

专为国内二类电商设计的 CID（Click ID）投流追踪技能，支持抖音巨量引擎、快手磁力引擎、腾讯广点通三大广告平台。

## 核心功能

### ✅ Click ID 生成
- 为每次广告点击生成唯一标识符
- 支持批量生成和单个生成
- CID 格式符合各平台规范

### ✅ 转化回传
- 订单数据回传到广告平台
- 支持自定义转化事件
- 回传状态追踪和重试机制

### ✅ ROI 分析
- 多平台数据聚合分析
- 实时计算投入产出比
- 按计划/创意/时段维度拆解

### ✅ 数据看板
- 日报/周报自动生成
- 关键指标可视化
- 趋势分析和对比

### ✅ 异常监控
- 消耗异常预警
- 转化率波动检测
- 低 ROI 计划自动标记

## 支持平台

| 平台 | API 文档 | 状态 |
|------|----------|------|
| 抖音巨量引擎 | https://oceanengine.github.io/open-platform/ | ✅ |
| 快手磁力引擎 | https://mp.weixin.qq.com/ | ✅ |
| 腾讯广点通 | https://e.qq.com/dev/ | ✅ |

## 快速开始

### 1. 配置 API 凭证

在 `config.json` 中配置各平台凭证：

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
    "secret_key": "密钥"
  }
}
```

### 2. 生成 CID 追踪链接

```bash
python scripts/cid_generator.py --platform oceanengine --campaign_id 12345
```

### 3. 获取广告数据

```bash
python scripts/data_fetcher.py --platform all --date yesterday
```

### 4. 生成 Excel 报表

```bash
python scripts/report_generator.py --output daily_report.xlsx --date 2026-03-21
```

### 5. 监控异常

```bash
python scripts/anomaly_detector.py --threshold 1.5
```

## 脚本说明

| 脚本 | 功能 | 输入 | 输出 |
|------|------|------|------|
| `cid_generator.py` | 生成 CID 追踪链接 | 广告计划 ID | 追踪 URL 列表 |
| `data_fetcher.py` | 获取各平台广告数据 | 平台、日期范围 | JSON 数据 |
| `conversion_tracker.py` | 转化数据回传 | 订单数据 | 回传结果 |
| `roi_analyzer.py` | ROI 分析计算 | 消耗 + 转化数据 | 分析结果 |
| `report_generator.py` | 生成 Excel 报表 | 聚合数据 | .xlsx 文件 |
| `anomaly_detector.py` | 异常检测预警 | 历史数据 | 预警列表 |

## Excel 报表结构

生成的报表包含以下工作表：

1. **汇总看板** - 核心指标总览
2. **分平台数据** - 各平台详细数据
3. **计划明细** - 广告计划级别数据
4. **异常监控** - 异常计划列表
5. **趋势图表** - 消耗/转化趋势图

## 依赖

```bash
pip install openpyxl pandas requests matplotlib
```

## 使用示例

### 示例 1：生成日报

```bash
python scripts/report_generator.py \
  --output reports/daily_20260321.xlsx \
  --date 2026-03-21 \
  --platforms oceanengine,kuaishou,tencent
```

### 示例 2：回传转化

```bash
python scripts/conversion_tracker.py \
  --platform oceanengine \
  --event purchase \
  --cid CID123456 \
  --value 299.00
```

### 示例 3：检测异常

```bash
python scripts/anomaly_detector.py \
  --min-roi 1.5 \
  --max-cpa 100 \
  --notify wechat
```

## 注意事项

1. **API 限流** - 各平台有调用频率限制，建议设置合理的请求间隔
2. **数据延迟** - 广告平台数据通常有 2-4 小时延迟
3. **CID 有效期** - 生成的 CID 链接通常 30 天有效
4. **转化归因** - 默认 7 天点击归因窗口

## 故障排查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| API 调用失败 | 凭证过期 | 刷新 access_token |
| 数据为空 | 日期范围无数据 | 检查日期参数 |
| Excel 生成失败 | 依赖缺失 | `pip install -r requirements.txt` |
| CID 无效 | 格式错误 | 检查平台 CID 规范 |

## 参考资料

- [巨量引擎 API 文档](references/oceanengine_api.md)
- [磁力引擎 API 文档](references/kuaishou_api.md)
- [广点通 API 文档](references/tencent_api.md)
- [CID 追踪最佳实践](references/cid_best_practices.md)
