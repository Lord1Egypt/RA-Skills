# BSC Dev Monitor Skill - 定价更新

## 💰 新价格

**每次调用**: 0.01 USDT
**计费模式**: 按次收费

## 📝 更新内容

### 已更新文件

1. **SKILL.md**
   - 价格：0.001 → 0.01 USDT
   - 收费模式：简化为按次收费

2. **index.js**
   - SKILLPAY_CONFIG.price：0.001 → 0.01
   - billingMode：per_detection → per_call
   - 支付描述简化

### 收费说明

- **每次监控请求收费 0.01 USDT**
- **无论是否有检测结果**
- **简单明了的按次计费**

## ✅ 测试状态

```
✅ 价格更新: 完成
✅ 代码测试: 通过
✅ 支付链接: 正常
```

## 🚀 部署

价格已更新，可以直接部署到 ClawHub：

```bash
cd /root/.openclaw/workspace/bsc-dev-monitor-skill
./deploy.sh
```

---

**更新时间**: 2026-03-05
**新价格**: 0.01 USDT / 次
