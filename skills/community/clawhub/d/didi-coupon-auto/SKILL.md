---
name: didi-coupon-auto
description: "自动领取滴滴出行优惠券。每天0点自动领取打车券包，支持网约车、顺风车、代驾等多种出行券。触发词: 领取滴滴优惠券, 运行滴滴领券技能, 设置每日自动领取滴滴, 滴滴打车券, didi coupon"
metadata:
  {
    "openclaw": {
      "emoji": "🚕",
      "requires": {
        "bins": ["node"],
        "runtimeNote": "需要 Node.js 和 OpenClaw 浏览器（CDP 端口 18800）。ws 模块由 OpenClaw workspace 的 node_modules 提供。"
      }
    }
  }
---

# 滴滴出行优惠券自动领取

每天 0:00 自动打开滴滴领券页，点击领取当日打车券包，输出**完整分组明细**（快车/顺风车/代驾/火车票/跨城等）。

首次运行需要在浏览器中登录滴滴账号；登录后 cookie 保留，后续全自动运行。

## 验证数据
- 17张券，最高立减合计 ¥219（2026-03-16 实测）
- 分组展示：快车 · 顺风车 · 火车票 · 代驾 · 跨城/包车 · 其他
- 耗时约 8s（API 拦截模式）

---

## 触发词

- "领取滴滴优惠券" / "滴滴领券"
- "运行滴滴领券技能" / "didi coupon"
- "设置每日自动领取滴滴"
- "打车有优惠券吗"

---

## 执行流程

### 步骤 1：启动浏览器

```
browser(action=status, profile=openclaw)
# 未运行则先 start
browser(action=start, profile=openclaw)
```

### 步骤 2：运行领券脚本

```bash
node skills/didi-coupon-auto/scripts/claim.mjs
```

### 步骤 3：处理结果

| 脚本输出 | 处理方式 |
|---------|---------|
| `需要登录` | 告知用户在浏览器手动登录滴滴，登录后重新运行 |
| `今日已领取` | 输出已有券包完整明细 |
| `领取完成！共 N 张` | 输出新领取券包完整明细 |

### 步骤 4：关闭浏览器

```
browser(action=stop, profile=openclaw)
```

---

## 输出格式

```
🚕 滴滴出行优惠券自动领取 v5
─────────────────────────────────────────────
🎫 共 17 张券，最高立减合计 ¥219
🚗 快车
    · 快车早高峰券  9.5折 最高抵扣10元
    · 快车晚高峰券  9.5折 最高抵扣10元
    · 宠物快车券  8折 最高抵扣10元
🤝 顺风车
    · 顺风车新客券  5折 最高抵扣10元
🚄 火车票
    · 火车票券  2元 满65元可用
    · 火车票券  6元 满12元可用
    · 火车票券  8元 满20元可用
🌙 代驾
    · 代驾折扣券  9折 最高抵扣5元
    · 代驾远途券  10元 满100元可用
    · 取送车代驾券  25元 立减25元
🛣 跨城/包车
    · 包车立减券  20元 立减20元
🎟 其他
    · 酒店优惠券  25元 满199元可用
    · 机票惊喜券  20元 满600元可用
    · 租车惊喜券  30元 满300元可用
    · 搬家立减券  20元 满200元可用
    · 单车折扣券  5折 最高抵扣3元
⏱  耗时 8688ms
```

---

## 定时任务（每天 0:05）

```json
{
  "name": "每日滴滴领券",
  "schedule": { "kind": "cron", "expr": "5 0 * * *", "tz": "Asia/Shanghai" },
  "payload": { "kind": "systemEvent", "text": "⏰ 定时提醒：领取滴滴优惠券" },
  "sessionTarget": "main",
  "delivery": { "mode": "none" }
}
```

> ⚠️ 必须使用 `sessionTarget: "main"` + `payload.kind: "systemEvent"`。
> 使用 `isolated` + `announce` 在无外部渠道（Telegram/Discord）时会报错：
> `Channel is required (no configured channels detected)`

---

## 页面状态说明

| 状态 | 识别关键词 | 处理 |
|------|----------|------|
| 未登录 | `登录领取` | 提示用户手动登录 |
| 可领取 | MPX 组件 `canClaim` | `autoGetCoupon()` / `click()` |
| 已领取 | `errno=3000030009` | 刷新页面拉取已有券列表 |
| 领取失败 | 其他 errno | 输出错误码 |

---

## 技术实现

- **CDP 直连**：WebSocket 连接浏览器调试端口（18800），无需 Playwright/Puppeteer
- **MPX 组件调用**：优先调用 `vm.autoGetCoupon()` / `vm.getCoupon()`，降级至 DOM 点击
- **API 拦截**：监听 `reward/receive` + `reward/list` 响应，直接解析券数据
- **日志**：结果写入 `logs/claim_YYYYMMDD.json`（.gitignore 已排除）

---

## 领券地址

```
https://vv.didi.cn/a8ZdG0j?source_id=88446DIDI88446tkmmchild1001&ref_from=dunion
```
覆盖：网约车 · 顺风车 · 特惠 · 代驾 · 火车票 · 跨城 · 包车 · 酒店 · 单车

---

> 📋 实测记录（2026-03-16）：
> - [x] 完整分组输出：去除 6 条截断限制，全部 17 张券逐条显示
> - [x] 按出行类型分组：快车/顺风车/火车票/代驾/跨城包车/其他
> - [x] 总价统计：累加所有面值（含折扣券最高抵扣值）
> - [x] 今日已领 17 张 / ¥219 / 耗时 8.7s
