---
name: deal-hunter-alert-claw
description: |
  商业捡漏预警虾 — 商业信息差的极速捕手。监控多平台（闲鱼、链家、阿里拍卖、政府采购网等），第一时间发现低价房产、优质二手货、招标机会，并推送飞书预警。

  当以下情况时使用此 Skill：
  (1) 用户要求监控某平台的低价商品、房产或招标信息
  (2) 用户要求设置价格预警阈值（如"低于市场价30%就通知我"）
  (3) 用户提到"捡漏"、"低价房产"、"法拍房"、"急售"、"二手好货"、"招标信息"、"商机预警"、"信息差"、"抢先"、"套利"、"优质标的"、"域名抢注"、"股权转让"、"政府采购"、"闲置好物"
  (4) 用户说"帮我盯着XXX"、"发现低价XXX立刻告诉我"、"监控XXX平台"
  (5) 需要对发现的标的进行快速估值和风险评估
---

# 商业捡漏预警虾

## 核心工作流

### 第一步：理解监控需求

从用户输入中提取：
- **平台**：闲鱼/转转/链家/贝壳/阿里拍卖/政府采购网等（见支持平台列表）
- **筛选条件**：关键词、价格上限/下限、地区、折扣阈值
- **通知方式**：默认飞书推送

如果用户未指定平台，根据标的类型推断：
- 二手数码/奢侈品 → 闲鱼 + 转转
- 二手房/急售 → 链家 + 贝壳
- 法拍房 → 阿里拍卖 + 京东拍卖
- 招标项目 → 政府采购网 + 招标平台

### 第二步：构建监控规则

将用户需求转换为规则 JSON：

```json
{
  "platform": "xianyu",
  "keyword": "iPhone 15 Pro",
  "price_max": 5000,
  "price_min": 1000,
  "min_discount_pct": 20,
  "city": "上海",
  "notify_channel": "feishu"
}
```

多条规则时使用数组：
```json
[
  {"platform": "lianjia", "city": "beijing", "district": "朝阳区", "price_max": 500, "min_discount_pct": 20},
  {"platform": "paimai", "city": "beijing", "district": "海淀区", "price_max": 500, "min_discount_pct": 30}
]
```

### 第三步：执行扫描

```bash
# 单条规则（快速测试）
python3 ~/.openclaw/skills/deal-hunter-alert-claw/scripts/monitor.py \
  --rule '{"platform":"xianyu","keyword":"iPhone 15","price_max":5000}'

# 规则文件（多平台监控）
python3 ~/.openclaw/skills/deal-hunter-alert-claw/scripts/monitor.py \
  --config ~/.openclaw/workspace/deal-hunter-data/rules.json

# JSON 输出（便于后续处理）
python3 ~/.openclaw/skills/deal-hunter-alert-claw/scripts/monitor.py \
  --rule '...' --output json
```

### 第四步：估值与风险评估

脚本自动完成，但对于重要标的需人工复核：
- 读取 `references/valuation-models.md` 进行估值判断
- 读取 `references/risk-signals.md` 识别风险信号
- 高风险标的自动过滤，中风险标的附加提示后推送

### 第五步：推送飞书预警

扫描完成后，将结果格式化并通过飞书推送给用户：

```
🦞 捡漏预警 | 闲鱼
📌 iPhone 15 Pro 256G 深空黑 九成新
💰 价格：4200元
📊 市场价：7999元 | 折扣：47.5%
🔗 https://2.taobao.com/item/xxx
⚡ 注意：换过电池，注意续航
```

### 第六步：持续监控设置（可选）

如果用户需要持续监控，建议通过 OpenClaw cron 定时执行：
- 二手商品：每5-15分钟一次
- 房产/法拍：每30分钟一次
- 招标信息：每天2-4次（工作日）

告知用户设置方式：`/cron add "*/15 * * * *" "扫描闲鱼iPhone 15"`

---

## 支持平台

| 平台标识 | 平台名称 | 适用场景 |
|---------|---------|---------|
| `xianyu` | 闲鱼 | 二手商品 |
| `zhuanzhuan` | 转转 | 二手商品 |
| `lianjia` | 链家 | 二手房/急售 |
| `ke` | 贝壳 | 二手房/急售 |
| `paimai` | 阿里拍卖 | 法拍房/资产 |
| `jd_auction` | 京东拍卖 | 法拍房/资产 |
| `ccgp` | 政府采购网 | 招标 |
| `bidding` | 招标投标平台 | 招标 |

---

## 参考资料

- **估值方法**：`references/valuation-models.md` — 房产/二手商品/招标的快速估值模型
- **平台规则**：`references/platform-rules.md` — 各平台采集策略、字段结构、反爬策略
- **风险识别**：`references/risk-signals.md` — 各类标的的风险信号库

> ⚠️ 当前脚本为示例实现，返回模拟数据。实际部署时需在 `scripts/monitor.py` 中替换各平台的真实采集逻辑（HTTP 请求或 Selenium）。

---

## 与其他虾协作

- 发现优质标的后 → 调用 **strategy-advisor-claw** 评估是否值得投入
- 多渠道推送 → 调用 **cross-platform-messenger-claw** 同时推送到微信/短信
- 历史数据分析 → 调用 **auto-data-analysis-claw** 优化监控规则
