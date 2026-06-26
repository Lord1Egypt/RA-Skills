# A股收盘报告

每个A股交易日 15:10 通过飞书发送当日收盘情况总结，包含主力资金状况。

## 触发条件

- 时间：每交易日 15:10（周一至周五）
- 时区：Asia/Shanghai
- 注意：节假日需额外判断

## 内容

- 上证指数、深证成指、创业板指、沪深300 涨跌幅
- 涨跌分布统计（上涨/下跌/平盘）
- **主力资金状况**（重点）
  - 主力资金净流入/净流出
  - 主力资金净流入板块 Top 5
  - 主力资金净流出板块 Top 5
- 热门板块
- 成交额
- 操作建议

## 实现

使用东方财富股票 API 获取实时数据：
- 指数: `https://push2.eastmoney.com/api/qt/ulist.np/get`
- 行业资金流向: `https://push2.eastmoney.com/api/qt/clist/get` (fid=f62 主力资金)
- 涨跌统计: `https://push2.eastmoney.com/api/qt/ulist.np/get` (f104/f105/f106)

## 发送

通过 OpenClaw 飞书通道发送给用户。

## 使用方法

```bash
# 仅生成报告
node scripts/closing-summary.mjs

# 生成并发送到飞书
node scripts/closing-summary.mjs --send
```

## Cron 定时任务

设置每天 15:10 执行（OpenClaw 会自动判断是否为交易日）：

```bash
openclaw cron add "10 15 * * 1-5" --skill a-stock-evening -- --send
```
