---
name: sp-service-weather
description: 用户询问天气（今天天气怎么样、天气怎么样、某城市/某日期天气）、或查询天气服务订单/额度/调用明细时触发
metadata:
  env:
    CLAUDE_SKILL_DIR: "Skill 运行目录，由 Agent 自动注入，用于存放 sp-weather-config.json"
    SP_WEATHER_BASE: "天气服务 base URL（可选），默认为 https://www.dxmpay.com"
    SP_WEATHER_PASSWORD: "私钥保护密码（可选），未设置时 Skill 会通过对话向用户询问"
---

> ⚠️ **安装前须知**
>
> 1. **服务后端**：所有 API 调用（天气查询、用户注册、短链生成）均通过 `https://www.dxmpay.com`。如果您不信任该域名，请勿安装。
> 2. **域名范围说明**：本 Skill 的所有网络请求均限定在 `www.dxmpay.com` 域名下，包括天气查询、支付、短链生成接口。短链服务仅对 `https://www.dxmpay.com/` 开头的 URL 生成短链，其他域名的 URL 会被拒绝，不存在将任意外部链接发送至短链服务的风险。
> 3. **密钥对存储**：本 Skill 会在首次运行时生成 EC 密钥对，加密后保存至 `${CLAUDE_SKILL_DIR}/sp-weather-config.json`。密码通过对话获取，不写入任何文件。
> 4. **二维码文件写入**：生成的 PNG 文件默认写入当前工作目录，请注意文件残留，必要时手动清理。

# 天气服务 Skill (sp-service-weather)

本 Skill 通过天气服务 (`https://www.dxmpay.com`) 查询天气，并支持用户认证初始化、订单查询、额度查询等功能。

**脚本路径**: `scripts/sp-weather-cli.js`（相对于 skill 目录）
**运行方式**: `node scripts/sp-weather-cli.js <command> [options]`

---

## 触发条件

以下任意情况触发本 Skill：
- 用户询问天气：「今天天气怎么样」「北京天气」「明天上海天气」「天气怎么样」
- 用户查询订单：「查询天气服务订单」「查充值记录」
- 用户查询额度：「查询天气服务余额」「还有多少额度」
- 用户查询调用明细：「查看API调用记录」「查用量」

---

## 工作流程

### 第一步：确保私钥密码已就绪

**每次执行前必须先通过对话询问用户密码**：

> "执行天气查询需要您的私钥保护密码，请告知（密码不会被记录到任何文件）："

获取到密码后，后续所有 `node scripts/sp-weather-cli.js` 调用均需在命令前拼接环境变量：
```bash
export SP_WEATHER_PASSWORD=<用户输入的密码> && node scripts/sp-weather-cli.js <command>
```

> **注意**：密码仅在命令行内联使用，不写入任何文件，不输出到日志。

### 第二步：确保用户配置存在

**每次执行前必须先运行**：
```bash
node scripts/sp-weather-cli.js userConfig
```

- 返回 `"action": "exists"` → 配置已存在，直接进入第三步
- 返回 `"action": "created"` → 已自动生成 EC/secp256r1 密钥并保存到 `${SKILL_DIR}/sp-weather-config.json`，继续第三步
- 返回失败 → 告知用户错误信息,禁止把其他json配置文件拷贝过来重命名使用

### 第三步：根据用户意图执行对应命令

---

## 命令说明

### 1. 天气查询 `queryWeather`

**触发**：用户询问任何天气相关问题

**参数提取**：
- 从用户输入中提取**日期**，若无日期则使用当天日期（通过 `new Date().toISOString().split('T')[0]` 获取）
- 从用户输入中提取**城市名**；若用户未提供城市，**必须主动询问用户**直到获得城市名，不可使用默认值

**执行**：
```bash
node scripts/sp-weather-cli.js queryWeather --city <城市> --date <日期>
```

示例：
```bash
node scripts/sp-weather-cli.js queryWeather --city 北京 --date 2026-03-20
node scripts/sp-weather-cli.js queryWeather --city 上海
```

**处理结果**：
- `success: true` → 将 `data` 中的天气信息整理后展示给用户
- **当返回 `error: "FORBIDDEN"` 或 `detail` 包含"未购买"时**：
  1. 在本 Skill 内执行：
     ```bash
     node scripts/sp-weather-cli.js queryPurchaseDetail
     ```
  2. 从返回的 `data` 中提取字段，构造结构化 JSON：
     ```json
     {
       "productName":  "<data.productName>",
       "productDesc":  "<data.productDesc>",
       "price":        "<data.price>",
       "payUrl":       "<data.payUrl（必须为 https://www.dxmpay.com/ 开头）>",
       "pay_channels": "<data.pay_channels>",
     }
     ```
  3. 调用 `dxm-claw-pay` Skill，传入上述 JSON
     → 后续二维码生成（含 `--short-url` 短链）、话术引导均由 `dxm-claw-pay` 完成
- `needCity: true` → 询问用户城市名后重新执行

---

### 2. 查询充值订单列表 `queryOrders`

**触发**：用户查询充值记录、订单列表

```bash
node scripts/sp-weather-cli.js queryOrders
# 分页（可选）
node scripts/sp-weather-cli.js queryOrders --page 1 --page-size 20
```

**接口**：`GET /api/skill/orders?uid=<userId>&page=1&page_size=20`

---

### 3. 查询指定订单 `queryOrder`

**触发**：用户提供了具体订单号

```bash
node scripts/sp-weather-cli.js queryOrder --orderId SP202603192029449B6A4893
```

**接口**：`GET /api/skill/orders/<orderId>?uid=<userId>`

---

### 4. 查询天气服务额度 `queryQuota`

**触发**：用户询问余额、额度、还能用多少次

```bash
node scripts/sp-weather-cli.js queryQuota
```

**接口**：`GET /api/skill/quota?uid=<userId>&skill_id=skill_001`

---

### 5. 查询 API 调用明细 `queryCallLogs`

**触发**：用户查询调用记录、用量明细

```bash
node scripts/sp-weather-cli.js queryCallLogs
# 分页（可选）
node scripts/sp-weather-cli.js queryCallLogs --page 1 --page-size 20
```

**接口**：`GET /api/skill/call-logs?uid=<userId>&skill_id=skill_001&page=1&page_size=20`

### 6. 查询商品信息 `queryPurchaseDetail`

**触发**：余额不足时自动调用；或用户询问充值套餐、商品价格

```bash
node scripts/sp-weather-cli.js queryPurchaseDetail
```

**接口**：`GET /api/skill/purchase/detail?uid=<userId>&skill_id=skill_001`

**处理结果**：从返回的 `data` 中提取商品字段，构造结构化 JSON，调用 `dxm-claw-pay` Skill 完成二维码生成（`dxm-claw-pay` 内部使用 `--short-url` 生成短链）

---


---

## 配置文件说明

脚本自动将用户配置保存在 `${CLAUDE_SKILL_DIR}/sp-weather-config.json`，内容包括：
```json
{
  "userId": "userid",
  "publicKey": "-----BEGIN PUBLIC KEY-----\n...",
  "privateKey": "加密格式..."
}
```

密钥算法：EC / secp256r1（prime256v1），签名算法：SHA256withECDSA。

---

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SP_WEATHER_BASE` | 天气服务 base URL | `https://www.dxmpay.com`（天气查询与支付均通过此域名） |
| `SP_WEATHER_PASSWORD` | 私钥保护密码，未设置时 Skill 会通过对话向用户询问 | 无 |

---

## 故障排查

| 现象 | 处理 |
|------|------|
| `连接天气服务失败` | 确认服务 `https://www.dxmpay.com` 是否可达 |
| `余额不足` / `payRequired: true` | 扫码充值后重试 |
| 二维码不显示 | 手动打开 `payUrl` 完成支付；可安装 `brew install qrencode` 改善体验 |
| `用户配置不存在` | 先执行 `userConfig` 命令初始化 |
| `未知命令` | 检查命令名拼写，可用命令：`userConfig` / `queryWeather` / `queryOrders` / `queryOrder` / `queryQuota` / `queryPurchaseDetail` / `queryCallLogs` |

---

## 版本历史

- **v1.0.0**：初始版本，支持用户认证、天气查询、订单/额度/调用明细查询、二维码支付引导
