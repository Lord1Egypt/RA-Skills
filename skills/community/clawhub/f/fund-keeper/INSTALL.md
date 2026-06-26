# Fund Keeper Release Package

**版本**: v2.4.0
**发布日期**: 2026-03-07

---

## 📦 安装包内容

```
fund-keeper-release/
├── funds/                      # 数据目录（示例文件）
│   ├── my-funds.md            # 持仓文件（模板）
│   ├── config.json            # 配置文件（默认值）
│   └── sip-plan.json          # 定投计划（空）
├── fund_keeper.py             # 主程序
├── fund_stats.py              # 收益统计模块
├── stock_data.py              # 股票数据模块
├── check_gold.py              # 黄金基金监控
├── ocr_fast.py                # OCR 快速识别
├── ocr_simple.py              # OCR 简单识别
├── search_fund.py             # 基金搜索
├── SKILL.md                   # 技能说明
├── README.md                  # 使用说明
├── CHANGELOG_v2.3.md          # v2.3 更新日志
└── CHANGELOG_v2.4.md          # v2.4 更新日志
```

---

## 🚀 安装步骤

### 1. 安装 Python 依赖

```bash
pip install akshare pandas requests easyocr
```

### 2. 复制文件到 OpenClaw 技能目录

```bash
# 将 fund-keeper-release 文件夹复制到
# C:\Users\Administrator\.openclaw\workspace\skills\fund-keeper
```

### 3. 初始化持仓文件

编辑 `funds/my-funds.md` 添加你的持仓，或使用 OCR 功能：

```bash
py fund_keeper.py ocr --image <支付宝/天天基金截图>
```

### 4. 测试安装

```bash
py fund_keeper.py portfolio
py fund_keeper.py stats
```

---

## 📊 功能特性

### v2.4 新增
- ✅ 股票行情查询（新浪财经数据源）
- ✅ 涨幅榜/跌幅榜
- ✅ 股票 - 基金联动分析

### v2.3 新增
- ✅ 收益统计与可视化
- ✅ 定投计划管理

### v2.2 新增
- ✅ 多数据源交叉验证
- ✅ 股票 - 基金联动

### v2.0-v2.1
- ✅ 实时估值获取
- ✅ 买卖建议
- ✅ OCR 识图添加基金

---

## 🎯 常用命令

```bash
# 持仓查询
py fund_keeper.py portfolio

# 收益统计
py fund_keeper.py stats

# 投资建议
py fund_keeper.py advice
py fund_keeper.py advice --fund 000218

# 配置管理
py fund_keeper.py config
py fund_keeper.py config --set profit_target_percent=10
py fund_keeper.py config --set stop_loss_percent=15
py fund_keeper.py config --reset

# 股票查询
py fund_keeper.py stock --code 000001
py fund_keeper.py stock --gainers
py fund_keeper.py stock --losers

# 定投管理
py fund_keeper.py sip --list
py fund_keeper.py sip --add --fund 011608 --amount 500 --day 15

# OCR 识图
py fund_keeper.py ocr --image screenshot.png
```

---

## 📁 数据目录说明

### `funds/my-funds.md`
你的基金持仓文件，格式：

```markdown
| 基金代码 | 基金名称 | 持有金额 (元) | 持有收益 | 备注 |
|---------|---------|-------------|---------|------|
| 000218 | 国泰黄金 ETF 联接 A | 5892.02 | +49.01 | 黄金 |
```

### `funds/config.json`
配置参数：

```json
{
  "alert_threshold": 3.0    // 涨跌幅提醒阈值 (%)
}
```

**重要**：止盈、止损、定投日等参数在添加基金时单独设置，没有默认值。

### `funds/sip-plan.json`
定投计划配置（自动生成）

---

## ⚠️ 注意事项

1. **首次运行**：需要安装 Python 依赖
2. **OCR 功能**：首次使用会下载 OCR 模型（约 100MB）
3. **实时数据**：仅在交易日 9:30-15:00 更新
4. **编码问题**：Windows 建议使用 UTF-8 编码

---

## 📞 支持

如有问题，请查看：
- `SKILL.md` - 详细技能说明
- `CHANGELOG_v2.4.md` - 更新日志
- `README.md` - 原始说明

---

**版本**: v2.4.0 | **作者**: tangepier-crypto
