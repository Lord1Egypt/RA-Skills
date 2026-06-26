---
name: flight-price-monitor
description: flight price monitor, airfare price alert, fare tracking, cheap flight China, round-trip one-way, price drop notification, scheduled flight search, FlyAI CLI, search-flight, bookable links.
metadata:
  version: 1.0.1
  agent:
    type: tool
    runtime: node
    context_isolation: execution
    parent_context_access: read-only
  openclaw:
    emoji: "📉"
    priority: 90
    requires:
      bins:
        - node
    intents:
      - flight_price_monitor
      - flight_price_alert
      - fare_alert
      - fliggy_flight_search
      - find_skill_flight_price
    patterns:
      - "(机票.*(监控|提醒|低价|阈值|订阅|定时|比价|追踪))"
      - "(监控|追踪|订阅).*(机票|航班|票价|价格)"
      - "(查|搜|看|比).*(机票|航班).*(价格|多少钱|便宜|低价)"
      - "(往返|单程).*(机票|票)"
      - "(低于|不到|以内).*[0-9０-９]+.*(元|块).*(机票|票|提醒)"
      - "(飞猪|Fliggy).*(机票|票价).*(监控|提醒|比价|查价)"
      - "(find[- ]skill|哪个skill|推荐.*skill|有什么skill|适合.*skill|搜.*skill).*(机票|航班|票价|监控|低价|比价|飞猪)"
      - "(flight|airfare).*(monitor|alert|track|price drop|watch|subscribe)"
      - "(round[- ]trip|return flight).*(price|search|monitor)"
      - "(cheap|lowest).*(flight|airfare|ticket).*(china|domestic|Fliggy)?"
---

# 飞猪机票价格监控

面向 **飞猪渠道** 的机票：**单程 / 往返** 查价、可选 **低价阈值提醒**、**定时重复拉价**，以及把多次结果写入 **`memory/flight-monitor/`** 做简单趋势归纳。

实现方式：通过 **FlyAI CLI** 调用飞猪 MCP 的 **`search-flight`**，得到结构化报价与预订链接；**不**依赖浏览器自动化、页面快照或登录态抓数。

---

## 快速开始

### 环境与命令

```bash
npm i -g @fly-ai/flyai-cli
flyai search-flight --help

# 默认无key，可选配置：
flyai config set FLYAI_API_KEY "your-key"
```

### 一键查询机票

```
查一下北京到三亚 3 月 25 日的机票价格
查询杭州到西安 3 月 26 日，低于 500 元的机票
帮我看看上海飞成都，下周六的往返票
```

### 设置价格监控

```
帮我监控北京到三亚 3 月 25 日机票，每天查一次，低于 1500 提醒我
监控杭州到西安 3 月 26 日，每 6 小时查一次，低于 500 通知我
监控深圳飞东京 4 月 1 日，每天早晚各查一次
```

### 管理监控任务

```
查看我所有的机票监控任务
暂停北京到三亚的监控
删除杭州到西安的监控任务
显示北京到三亚的价格趋势
```

**说明**：任务列表依赖运行环境是否持久化定时任务；若无内置注册表，引导用户查看 `memory/flight-monitor/` 下的历史与自建说明（可在同目录另存一份「监控登记」Markdown）。

---

## 核心功能

### 1. 机票价格查询

- **单程**：出发地、目的地、出发日期；可选直飞、时段、预算上限；排序默认 **低价优先**。
- **往返**：增加返程日期，或使用 CLI 文档中的 **出发日期范围 / 返程范围** 参数（以 `--help` 为准）。
- **城市**：优先使用用户提供的 **中文城市名**；若仅提供 IATA 城市码，对照 **`references/airport-codes.md`** 再填入命令（以 CLI 是否接受为准）。

### 2. 价格监控

- 收集 **频率**（如每天固定时刻、每 N 小时）与可选 **阈值**（低于 X 元则强调提醒）。
- 在支持 **`cron.add`** 的环境：注册任务，`payload` 中写清航线、日期、往返、阈值、历史文件路径；示例见 **`references/cron-payload-examples.md`**。
- 其它环境：用系统 **crontab**、CI、或外部调度执行同一逻辑：**执行检索 → 解析 → 追加历史 → 判断是否提醒**。

### 3. 价格历史记录

- 建议路径：`memory/flight-monitor/{航线}-{出发日期}.md`，文件名避免空格（用 `-` 连接）。
- 每次巡检在表格中追加：**记录日期、时间、最低价、代表航班、相对上次涨跌**。
- 模板见 **`references/price-history-template.md`**。

---

## 使用参数

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| 出发地 | ✅ | 城市名或代码 | 北京 / BJS |
| 目的地 | ✅ | 城市名或代码 | 三亚 / SYX |
| 出发日期 | ✅ | `YYYY-MM-DD` | 2026-03-25 |
| 返回日期 | ❌ | 往返时需要 | 2026-03-30 |
| 监控频率 | 监控时 ✅ | 多久查一次 | 每天 9:00 / 每 6 小时 |
| 低价阈值 | ❌ | 低于多少提醒 | ¥1500 |
| 监控截止 | ❌ | 何时停止监控 | 监控到 3 月 18 日 |

---

## 技术实现

**所有 flag 以本机 `flyai search-flight --help` 为准**；与 `references/search-flight-params.md` 不一致时 **以终端为准**。

### 查询流程

1. **组参**：`--origin`、`--destination`、`--dep-date`；往返加 `--back-date`（或文档中的范围类参数）。
2. **检索**：执行命令；低价优先用 `--sort-type 3`；预算上限用 `--max-price`；只要直飞用 `--journey-type 1`。
3. **解析**：成功时 stdout 为单行 JSON；`status !== 0` 时结合 stderr 向用户说明原因。
4. **取价**：在 `data.itemList` 中解析 `adultPrice`（去掉货币符号再比数值），得到最低价及对应 `journeys`、预订跳转字段。
5. **阈值判断**：⚠️ **重要：严格按数值比较**
   - 提取最低价数字（如 3590）和阈值数字（如 1500）
   - **只有当 `最低价 < 阈值` 时才触发低价提醒**
   - 例如：3590 > 1500，应显示"当前 ¥3,590 高于阈值 ¥1,500"
   - 例如：1200 < 1500，才显示"🚨 低价提醒：¥1,200 低于阈值 ¥1,500"
   - **禁止错误描述**："3590 低于 1500" 是数学错误！
6. **历史**：监控场景将本条追加到 `memory/flight-monitor/...md`。
7. **展示字段**：返回里若有准点率、机型等额外字段，可在表格「备注」列择要展示；**无则不要编造**。

### Cron / 定时任务（OpenClaw 等）

常见形态示例（具体 API 以当前运行环境文档为准）：

```javascript
cron.add({
  name: "机票监控 - {航线}",
  schedule: { kind: "cron", expr: "0 9 * * *", tz: "Asia/Shanghai" },
  payload: {
    kind: "agentTurn",
    message: "（写全：航线、日期、是否往返、阈值、如何执行检索与写历史文件）"
  },
  sessionTarget: "isolated"
})
```

`message` 范例见 **`references/cron-payload-examples.md`**。

---

## 输出格式（用户可见）

**不要**在向用户正文里出现：`flyai`、`search-flight`、`stdout`、`JSON`、`jq`、`itemList`、`jumpUrl` 等实现词。可用「根据当前可查的实时报价」等自然表述。

### 查询结果（建议）

```markdown
## 机票查询结果

**航线：** 北京 → 三亚
**日期：** 2026-03-25（周三）

### 最低价航班

| 航班 | 价格 | 时间 | 备注 |
|------|------|------|------|
| 川航 3U3113 | ¥320 | 21:55-01:55+1 | 直飞（若适用） |

### 价格趋势
（若历史文件已有多日记录则按日罗列；否则说明本次为单次查询、尚无累计曲线。）

### 订票链接
[立即预订](<从结果中取得的链接>)
```

### 低价提醒（建议）

```markdown
🚨 低价提醒

北京 → 三亚 3 月 25 日
当前价：¥320（低于你的阈值 ¥1500）
航班：川航 3U3113 21:55-01:55+1

[立即预订](链接)
```

### ⚠️ 阈值判断示例（防止错误）

**✅ 正确示例：**
- 当前价 ¥1200，阈值 ¥1500 → "🚨 低价提醒：¥1200 低于阈值 ¥1500"
- 当前价 ¥3590，阈值 ¥1500 → "当前 ¥3590，高于阈值 ¥1500"

**❌ 错误示例（禁止）：**
- 当前价 ¥3590，阈值 ¥1500 → "大幅低于阈值 ¥1500"（数学错误！）
- 当前价 ¥2000，阈值 ¥1500 → "低价提醒"（2000 > 1500，不是低价）

若返回含可展示图片字段，可单独一行附图；**无则省略**。

---

## 使用场景

1. **提前规划**：远期出发日 + 较低巡检频率。
2. **错峰对比**：用户指定多日或多段日期时，分别检索后对比最低价（或一次使用 CLI 支持的日期范围）。
3. **商务约束**：叠加出发/到达时段、总时长等参数（见 `references/search-flight-params.md`）。
4. **临期出行**：近日/当日出发 + 阈值筛选。

---

## 配置要求

- **Node** 与全局包 **`@fly-ai/flyai-cli`**。
- 网络可达 FlyAI / 飞猪 MCP 服务端点；按环境配置 **API Key**（若必需）。
- **无需**为抓价而维护浏览器 Profile 或飞猪网页登录态。

---

## 注意事项

1. **时效**：报价反映查询时刻，与下单瞬间可能不一致。
2. **余票**：低价舱售罄快，以预订页为准。
3. **频率**：避免过高频请求；遵守服务条款与合理爬取/调用习惯。
4. **城市与日期**：核对起降地与 `YYYY-MM-DD`，避免跨日红线航班误解。
5. **诚实**：接口报错、鉴权失败、无结果时如实说明，**禁止虚构**价格、航班与链接。
6. **验证码**：本路径不经浏览器，一般不遇网页滑块；若遇 API 级限制，告知用户稍后再试或检查配额/Key。
7. **⚠️ 阈值逻辑**：**必须正确比较数字大小**！3590 > 1500，不要说成"低于"！只有实际价格小于阈值才是低价提醒。

---

## 监控频率建议

| 距出行时间 | 建议频率 | 说明 |
|------------|----------|------|
| 提前 1 个月+ | 每天 1 次 | 波动相对平缓 |
| 提前 2 周 | 每 12 小时 | 开始加密关注 |
| 提前 1 周 | 每 6 小时 | 波动加大 |
| 提前 3 天 | 每 3 小时 | 临期涨价风险高 |

---

## 相关链接

- 飞猪机票：<https://www.fliggy.com/jipiao/>
- FlyAI：<https://open.fly.ai/>
- OpenClaw 文档（若使用 `cron.add` 等能力）：<https://docs.openclaw.ai>

---

## 本包 References

| 文件 | 内容 |
|------|------|
| `references/search-flight-params.md` | CLI 参数速查 |
| `references/price-history-template.md` | 历史 Markdown 模板 |
| `references/cron-payload-examples.md` | 定时 payload 示例 |
| `references/airport-codes.md` | 常用城市三字码 |

---

**维护**：飞猪 MCP / CLI 升级可能导致字段或 flag 变化；以本机 `flyai search-flight --help` 与实跑 JSON 为准，必要时更新 `references/`。