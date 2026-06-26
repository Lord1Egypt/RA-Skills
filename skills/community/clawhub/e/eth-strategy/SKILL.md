---
name: eth-strategy
slug: eth-strategy
version: 1.0.2
description: |
  对 ETH/USDT 进行全方位技术分析，输出方向（多/空）、进场、止损、分批止盈点位。
  使用的分析手段包括：缠论结构、MACD、EMA、MA、KDJ、BOLL、RSI、ADX、
  各种 K 线形态（裸K、吞没、锤子等）、大单成交量（筹码区）以及
  简易的散户情绪/做市商猎杀区判定。
---

# ETH Strategy Skill

## 使用方式
在 OpenClaw 中运行：
openclaw exec eth-strategy <pair>

示例：
openclaw exec eth-strategy ETH/USDT

默认 pair 为 ETH/USDT，如果想分析其他交易对（如 BTC/USDT），只需把参数改成对应的符号即可。

## 依赖
- pandas
- pandas-ta
- ccxt
- numpy
