# A股早盘提醒

每个A股开盘日 9:45 通过飞书发送当日开盘情况总结。

## 触发条件

- 时间：每交易日 9:45（周一至周五）
- 时区：Asia/Shanghai
- 注意：节假日需额外判断

## 内容

- 上证指数、深证成指、创业板指
- 沪深300指数
- 涨跌分布统计
- 热门板块 Top 5
- 成交额
- 操作建议

## 实现

使用腾讯股票 API 获取实时数据：
- 指数: `https://qt.gtimg.cn/q={code}`

## 发送

通过 OpenClaw 飞书通道发送给用户。

## 使用方法

```bash
# 仅生成报告
node scripts/morning-summary.mjs

# 生成并发送到飞书
node scripts/morning-summary.mjs --send
```

## Cron 定时任务

设置每天 9:45 执行（OpenClaw 会自动判断是否为交易日）：

```bash
openclaw cron add "45 9 * * 1-5" --skill a-stock-morning -- --send
```
