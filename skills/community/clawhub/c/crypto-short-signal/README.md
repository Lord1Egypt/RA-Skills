# 加密货币做空信号生成器

**版本**: 2.0.0 (两层架构)  
**作者**: Denny Huang  
**收费**: 0.001 USDT/次  
**平台**: SkillPay + ClawHub

---

## 🏗️ 架构说明

### 公开层 (ClawHub)
```
index.js
├── SkillPay 收费接口
├── 基础验证
└── 调用付费层 API
```

### 付费层 (SkillPay Cloud)
```
api.js
├── API Key (保密)
├── 代币数据库 (保密)
└── 核心分析逻辑 (保密)
```

---

## 📖 功能说明

### 核心功能
1. 查询代币解锁时间
2. 分析解锁前后价格走势
3. 生成做空信号（时间 + 目标 + 止损）
4. 风险评估报告

### 支持代币
- ZRO (LayerZero)
- BARD (Lombard)
- STABLE (Stable)
- 其他低流通高 FDV 代币

---

## 🚀 快速开始

### 安装
```bash
# OpenClaw 一键安装
openclaw skill install crypto-short-signal
```

### 使用
```bash
# 查询单个代币
openclaw crypto-short-signal --token ZRO

# 批量查询
openclaw crypto-short-signal --tokens ZRO,BARD,STABLE

# 生成做空信号
openclaw crypto-short-signal --signal ZRO
```

---

## 💰 收费说明

- **单次查询**: 0.001 USDT
- **批量查询**: 0.005 USDT (5 个代币)
- **做空信号**: 0.001 USDT

**支付方式**: BNB Chain USDT (SkillPay)

---

## 📊 输出示例

### 基础查询
```
代币：ZRO (LayerZero)
解锁时间：2026-03-20
解锁量：32.6M ZRO (3.26%)
解锁压力：高
流通率：20.26%
FDV/MCAP: 4.94x
```

### 做空信号
```
代币：ZRO
做空时间：2026-03-13 至 03-18
目标价格：$1.65 (-10%)
止损价格：$2.00 (+10%)
胜率：78%
预期收益：-5.97%
```

---

## ⚠️ 风险提示

- 仅供参考，不构成投资建议
- 加密货币波动大，请谨慎操作
- 用户自负盈亏
- 历史数据不代表未来表现

---

## 🔗 相关链接

- SkillPay: https://skillpay.me/
- ClawHub: https://clawhub.ai/
- OpenClaw: https://openclaw.ai/

---

**更新时间**: 2026-03-05
