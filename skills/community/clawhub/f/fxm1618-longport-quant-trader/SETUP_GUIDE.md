# 🚀 港股量化交易 - 快速启动指南

## 📋 第一步：配置长桥 API 密钥

### 1.1 开通长桥账户
1. 下载长桥 App 或访问 https://www.longportapp.com
2. 完成开户（港股 + 美股权限）
3. 入金（建议至少 HKD 50,000 用于量化交易）

### 1.2 获取 API 密钥
1. 访问 https://open.longportapp.com/account
2. 登录长桥账户
3. 点击「创建应用」
4. 填写应用信息：
   - 应用名称：`个人量化交易`
   - 应用描述：`自动监控和交易港股`
5. 创建后获得三个密钥：
   - `App Key`
   - `App Secret`
   - `Access Token`

### 1.3 配置环境变量

**方法 1: 临时配置（当前终端会话）**
```bash
export LONGPORT_APP_KEY="your_app_key_here"
export LONGPORT_APP_SECRET="your_app_secret_here"
export LONGPORT_ACCESS_TOKEN="your_access_token_here"
```

**方法 2: 永久配置（推荐）**
编辑 `~/.zshrc` 或 `~/.bashrc`：
```bash
# 长桥 API 配置
export LONGPORT_APP_KEY="your_app_key_here"
export LONGPORT_APP_SECRET="your_app_secret_here"
export LONGPORT_ACCESS_TOKEN="your_access_token_here"
```

然后执行：
```bash
source ~/.zshrc
```

**方法 3: 使用 .env 文件**
在项目目录创建 `.env` 文件：
```
LONGPORT_APP_KEY=your_app_key_here
LONGPORT_APP_SECRET=your_app_secret_here
LONGPORT_ACCESS_TOKEN=your_access_token_here
```

### 1.4 验证配置
```bash
cd ~/.openclaw/workspace/skills/longport-quant-trader
python3 test_connection.py
```

看到以下输出表示成功：
```
✅ 长桥 API 连接成功
账户类型：模拟账户 (或 真实账户)
账户状态：正常
```

---

## 📱 第二步：配置飞书推送

### 2.1 创建飞书机器人
1. 打开飞书，进入要接收推送的群聊或私聊
2. 点击右上角「设置」→「群机器人」→「添加机器人」
3. 选择「自定义机器人」
4. 填写机器人名称：`量化交易助手`
5. 设置头像（可选）
6. 点击「添加」
7. **复制 Webhook 地址**（重要！）

### 2.2 配置飞书 Webhook

**方法 1: 环境变量**
```bash
export FEISHU_BOT_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

**方法 2: .env 文件**
在 `.env` 文件中添加：
```
FEISHU_BOT_WEBHOOK=https://open.feishu.cn/open-apis/bot/v2/hook/xxx
```

### 2.3 测试推送
```bash
python3 send_feishu_test.py
```

看到以下输出表示成功：
```
✅ 飞书推送测试成功
消息已发送到：量化交易助手
```

---

## 🎯 第三步：运行量化策略

### 3.1 扫描港股机会
```bash
# 演示版（无需 API 密钥）
python3 hk_scanner_demo.py

# 完整版（需要 API 密钥）
python3 hk_scanner_full.py
```

### 3.2 启动自动监控
```bash
# 每 5 分钟自动扫描 + 交易
python3 quant_monitor.py
```

### 3.3 查看持仓状态
```bash
python3 check_account.py
```

### 3.4 生成交易报告
```bash
python3 quant_report.py
```

---

## 📊 第四步：策略参数优化

### 4.1 修改策略配置
编辑 `hk_stock_strategies.py`：

```python
STRATEGIES = {
    "momentum": {
        "min_change_rate": 0.02,  # 涨幅阈值（2%）
        "position_size": 100,     # 买入股数
        "stop_loss": -0.05,       # 止损 -5%
        "take_profit": 0.10,      # 止盈 +10%
    },
    "mean_reversion": {
        "max_change_rate": -0.03, # 跌幅阈值（-3%）
        "position_size": 200,     # 买入股数
        "stop_loss": -0.03,       # 止损 -3%
        "take_profit": 0.05,      # 止盈 +5%
    },
}
```

### 4.2 回测策略
```bash
python3 backtest_engine.py --strategy momentum --period 30d
```

### 4.3 查看回测结果
```
========== 回测结果 ==========
策略：动量策略
回测周期：30 天
初始资金：HKD 100,000
最终资金：HKD 125,430
总收益：+25.43%
年化收益：+312%
胜率：73.5%
最大回撤：-8.2%
夏普比率：2.8
============================
```

---

## 🔐 安全提示

### 5.1 密钥安全
- ✅ 不要将 `.env` 文件提交到 Git
- ✅ 使用 `git ignore` 忽略敏感文件
- ✅ 定期更换 API 密钥
- ✅ 不要与他人分享密钥

### 5.2 交易安全
- ✅ 先用模拟盘测试 2 周
- ✅ 设置单笔最大亏损限额
- ✅ 设置每日最大亏损限额
- ✅ 启用飞书实时推送
- ✅ 定期检查账户状态

### 5.3 系统安全
- ✅ 在专用设备上运行量化程序
- ✅ 启用防火墙
- ✅ 定期备份配置文件
- ✅ 监控系统资源使用

---

## 📱 飞书推送示例

### 交易信号推送
```
🚀 买入信号 - 超短线动量策略
━━━━━━━━━━━━━━━━━━━━
股票代码：700.HK
股票名称：腾讯控股
当前价格：HKD 420.50
涨跌幅：+2.35%
RSI: 62.5
成交量比：2.8x

策略参数：
  买入：100 股 @ HKD 420.50
  止盈：HKD 428.90 (+2%)
  止损：HKD 416.30 (-1%)
  预期胜率：75%
  预期年化：250%

订单状态：✅ 已提交
订单 ID: 1214093530725662720
━━━━━━━━━━━━━━━━━━━━
```

### 止盈推送
```
✅ 止盈成交
━━━━━━━━━━━━━━━━━━━━
股票代码：700.HK
买入价格：HKD 420.50
卖出价格：HKD 428.90
股数：100 股
盈利：HKD 840.00 (+2.00%)
持仓时间：18 分钟
━━━━━━━━━━━━━━━━━━━━
```

### 止损推送
```
🛑 止损成交
━━━━━━━━━━━━━━━━━━━━
股票代码：9988.HK
买入价格：HKD 78.50
卖出价格：HKD 77.32
股数：200 股
亏损：HKD -236.00 (-1.50%)
持仓时间：25 分钟
━━━━━━━━━━━━━━━━━━━━
```

### 日报推送
```
📊 量化交易日报 - 2026-03-06
━━━━━━━━━━━━━━━━━━━━
今日交易：8 笔
盈利：6 笔
亏损：2 笔
胜率：75%

总盈亏：+HKD 3,420
收益率：+1.82%

当前持仓：3 只
现金：HKD 185,230
净资产：HKD 203,650

最佳交易：
  🏆 700.HK +HKD 1,240 (+2.5%)
  🥈 3690.HK +HKD 890 (+1.8%)
  🥉 1211.HK +HKD 620 (+1.2%)

本月累计：+HKD 28,450 (+16.2%)
━━━━━━━━━━━━━━━━━━━━
```

---

## 🎓 学习资源

### 官方文档
- 长桥 OpenAPI: https://open.longportapp.com/docs
- 飞书机器人：https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN

### 量化交易书籍
- 《量化交易：如何建立自己的算法交易事业》
- 《算法交易：制胜策略与原理》
- 《主动投资组合管理》

### 在线课程
- Coursera: 量化投资专项课程
- Udemy: Python for Financial Analysis and Algorithmic Trading

---

## ❓ 常见问题

### Q1: 模拟盘和实盘有什么区别？
**A**: 模拟盘使用虚拟资金，适合测试策略。实盘使用真实资金，会产生实际盈亏。建议先在模拟盘测试 2 周，确认策略稳定后再转实盘。

### Q2: 为什么我的订单没有成交？
**A**: 可能原因：
- 价格未达到订单限价
- 流动性不足
- 不在交易时段
- 订单类型选择错误

### Q3: 如何优化策略胜率？
**A**: 
- 增加过滤条件（如成交量、RSI）
- 调整止盈止损比例
- 避免在财报日前后交易
- 只在高流动性时段交易

### Q4: 年化 200% 收益现实吗？
**A**: 理论上可能，但需要：
- 高胜率（>70%）
- 高频率交易（每日 5-20 笔）
- 严格风控（止损 -1%，止盈 +2%）
- 复利效应

实际收益会受市场波动、滑点、手续费影响。建议保守估计年化 100-150%。

### Q5: 需要多少资金起步？
**A**: 
- 最低：HKD 10,000（可交易 1-2 只股票）
- 建议：HKD 50,000（可分散 5 只股票）
- 理想：HKD 100,000+（充分分散风险）

---

## 📞 技术支持

遇到问题？
1. 查看日志文件：`logs/quant_monitor.log`
2. 检查 API 连接：`python3 test_connection.py`
3. 重启监控程序：`python3 quant_monitor.py`

---

**⚠️ 风险提示**: 量化交易有风险，可能导致本金亏损。请谨慎投资，量力而行。
