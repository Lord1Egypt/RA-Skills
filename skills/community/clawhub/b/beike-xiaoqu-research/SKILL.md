---
name: beike-xiaoqu-research
description: 通过 mcp-chrome 插件抓取贝壳找房数据，支持两种模式：(1) 单小区深度四步研究（详情/在售/成交）；(2) 按地区批量发现并筛选符合条件的小区，再对候选清单做 PAL MCP 多模型 consensus 综合评估。适用场景：查贝壳小区信息、按区域发现候选小区、多模型评估买房方案。需要用户已安装 mcp-chrome 插件（端口 12306）+ mcporter 已配置 pal server。
---

# 贝壳找房小区研究工具 v2.2

## I/O 契约（输入 / 输出 / 错误）

> **Agent 调用此 Skill 前必读**，确保参数与返回结构符合预期。

### 模式 A：单小区深度研究

**输入参数（环境变量 / 脚本参数）**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `$1` (NAME) | string | 必填 | 小区名（中文），用于 `rs{小区名}` 搜索 |
| `$2` (CITY) | string | `sh` | 城市前缀 |
| `$3` (OUTDIR) | string | `/tmp/beike` | 输出目录 |
| `BEIKE_HEADLESS` | env | `0` | 设为 `1` 则 headless 模式，验证码时 exit 4 不挂起 |

**成功输出（OUTDIR 下生成以下文件）**

```json
{
  "status": "ok",
  "mode": "single_xiaoqu",
  "xiaoqu_name": "东方花园三期",
  "xiaoqu_id": "5011102207315",
  "files": {
    "xiaoqu_json": "{OUTDIR}/东方花园三期_xiaoqu.json",
    "ershou_json": "{OUTDIR}/东方花园三期_ershou.json",
    "chengjiao_json": "{OUTDIR}/东方花园三期_chengjiao.json"
  }
}
```

`*_xiaoqu.json` 字段 Schema：

```json
{
  "avg_price": 78000,
  "building_type": "板楼",
  "total_units": "320户",
  "total_buildings": "8栋",
  "green_rate": "35%",
  "far": "1.8",
  "ownership": "商品房",
  "built_year": "2008-2012",
  "mgmt_fee": "2.5元/月/㎡",
  "mgmt_company": "绿城物业",
  "developer": "绿城集团",
  "followers": "125",
  "on_sale": "5",
  "sold_90d": "2",
  "views_30d": "38",
  "metros": ["🚇9号线 七宝站 688m"],
  "_parse_source": "css+innerText"
}
```

### 模式 B：区域批量发现

**输入参数**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `$1` (BOARDS) | string | 必填 | 逗号分隔板块，如 `qibao,gumei` |
| `$2` (CITY) | string | `sh` | 城市前缀 |
| `$3` (OUTDIR) | string | `/tmp/beike_discover` | 输出目录 |
| `--district` | flag | `minhang` | 区域路径段，如 `pudong` |
| `--no-detail` | flag | off | 仅发现，不抓详情 |
| `--consensus` | flag | off | 发现后接 PAL MCP 评估 |
| `BEIKE_HEADLESS` | env | `0` | headless 模式 |

**成功输出**

```json
{
  "status": "ok",
  "mode": "region_discover",
  "city": "sh",
  "district": "minhang",
  "boards": ["qibao", "gumei"],
  "total_candidates": 8,
  "candidates": [
    {
      "name": "好世鹿鸣苑",
      "board": "qibao",
      "price": 68000,
      "year": "2010-2012",
      "on_sale": 5,
      "sold_90d": 2,
      "metro": "1号线 莘庄站 688m",
      "xiaoqu_id": "5011000015858"
    }
  ],
  "csv_file": "{OUTDIR}/candidates_2026-03-23.csv"
}
```

### 错误状态码

| exit code | status 字符串 | 说明 |
|-----------|--------------|------|
| `0` | `ok` | 成功 |
| `1` | `dependency_missing` | mcp-chrome 未启动 / 依赖缺失 |
| `2` | `captcha_detected` | 验证码（交互模式，等待用户处理） |
| `3` | `parse_failed` | 关键字段解析失败（贝壳结构变更） |
| `4` | `captcha_headless` | headless 模式遇验证码，无法处理 |

---

## 两种工作模式

| 模式 | 触发场景 | 脚本 |
|------|---------|------|
| **A. 单小区深度研究** | "查XX小区的信息"、"看东方花园三期" | `fetch_xiaoqu.sh` |
| **B. 区域批量发现** | "找七宝/古美附近符合条件的小区"、"帮我发现候选小区" | `region_discover.sh` |

两种模式最终都可接 **PAL MCP Consensus 评估**（`consensus_analyze.py`）。

---

## 前置检查

### 1. mcp-chrome 连接

```bash
curl -s http://127.0.0.1:12306/mcp -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"agent","version":"1.0"}}}' \
  | grep -o '"name":"ChromeMcpServer"' && echo "✅ 已连接" || echo "❌ 请检查插件"
```

获取 SESSION_ID（动态获取，不要写死）：

```bash
SESSION_ID=$(curl -s -i -X POST "http://127.0.0.1:12306/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"agent","version":"1.0"}}}' \
  | grep -i "mcp-session-id:" | awk '{print $2}' | tr -d '\r\n ')
```

### 2. PAL MCP 可用性（Consensus 模式需要）

```bash
mcporter list pal 2>&1 | grep -q "chat" && echo "✅ PAL MCP 正常" || echo "❌ 请检查 ~/.mcporter/mcporter.json"
```

---

## 贝壳 URL 规则

```
# 城市前缀：sh=上海 bj=北京 sz=深圳 gz=广州

# 区域列表（发现小区）
按板块：   https://{city}.ke.com/xiaoqu/minhang/{板块拼音}/
全区：     https://{city}.ke.com/xiaoqu/{区拼音}/

# 常用上海板块
七宝=qibao  古美=gumei  金汇=jinhui  龙柏=longbai
莘庄=xinzhuang  漕河泾=caoheqing  虹桥=hongqiao

# 单小区操作
详情页：   https://{city}.ke.com/xiaoqu/{小区ID}/
在售：     https://{city}.ke.com/ershoufang/rs{小区名}/
成交：     https://{city}.ke.com/chengjiao/rs{小区名}/
```

---

## 模式 A：单小区深度研究（四步）

### Step 1 – 查小区 ID

```bash
navigate → ershoufang/rs{小区名}/
wait 7s
JS: return Array.from(document.querySelectorAll('a'))
      .find(a => a.href.includes('/xiaoqu/') && /\/\d+\//.test(a.href))?.href || ''
# 取 URL 中的数字部分即为小区 ID
```

### Step 2 – 小区详情页

```bash
navigate → xiaoqu/{小区ID}/
wait 7s
JS: return document.body.innerText
→ parse_beike.py xiaoqu
```

**关键解析注意**：
- 贝壳使用 `\xa0`（非断行空格），正则需用 `[\s\xa0]*` 代替普通空格
- 字段格式：`字段名\n值`（换行分隔，非同行）
- 在售套数：格式为 `N套\n在售二手房`

### Step 3 – 在售二手房

```bash
navigate → ershoufang/rs{小区名}/
wait 7s
JS: return document.body.innerText
→ parse_beike.py ershou
```

### Step 4 – 成交记录

```bash
navigate → chengjiao/rs{小区名}/
wait 7s  # 此页最易触发验证码，建议在 Step 2/3 之间 sleep 10s
JS: return document.body.innerText
→ parse_beike.py chengjiao
```

---

## 模式 B：区域批量发现

### B1 – 读取板块小区列表

```bash
navigate → https://sh.ke.com/xiaoqu/minhang/{板块拼音}/
wait 7s
JS: return document.body.innerText
→ parse_beike.py region_list  # 输出符合条件的小区列表 JSON
```

**列表页格式**（已验证）：

```
小区名                     ← 行 i-1
 90天成交X套               ← 行 i（标志行）
 闵行\xa0板块\xa0 /\xa0年份 ← 行 i+1
近地铁XX站（可选）
均价元/m2
月份参考均价
N套
在售二手房
```

**筛选条件**（可通过参数调整）：
- 建成年份最新年 ≥ 2005（次新）
- 均价 40,000–110,000 元/㎡
- 在售套数 ≥ 2
- 排除：别墅、公寓、大厦、写字楼

### B2 – 批量抓取详情

对筛选出的候选小区，循环执行步骤 A1–A2（详情页），每个小区间 sleep 10s 降低验证码风险。

一键脚本：

```bash
bash scripts/region_discover.sh qibao,gumei,jinhui sh /tmp/result/
# 参数: 板块列表(逗号分隔)  城市  输出目录
```

---

## 验证码处理协议

```
检测：grep -q "请在下图\|请按语序" page.txt

触发后：
1. 立即停止 → 告知用户 "⚠️ Chrome 有验证码，请手动完成点选"
2. 等待用户确认
3. 直接重读当前页（不重新 navigate）
4. 验证通过后继续
```

---

## PAL MCP Consensus 评估（可选最终步骤）

收集好各小区 JSON 数据后，调用 `consensus_analyze.py` 让多个 AI 模型从不同维度评分：

```bash
python3 scripts/consensus_analyze.py \
  --data-dir /tmp/result/ \
  --requirements "三房120㎡以上, 预算1300万以内, 有产权车位, 地铁1km以内, 2005年后" \
  --models "gemini-3-pro-preview,auto" \
  --output /tmp/result/consensus_report.md
```

**Consensus 流程**：
1. 汇总所有小区数据为结构化摘要
2. 构造统一评估 prompt（含需求条件）
3. 模型1（偏保守/价格导向）评分 + 理由
4. 模型2（偏流动性/投资导向）评分 + 理由
5. 综合两个视角输出最终排名推荐

---

## 分析维度参考

| 维度 | 关注点 | 权重 |
|------|-------|------|
| **流动性** | 90天成交套数 + 成交周期 | ★★★★★ |
| **价格匹配** | 120㎡三房总价是否在预算内 | ★★★★★ |
| **车位** | 成交记录中车位条数；在售"产权车位"提及 | ★★★★☆ |
| **地铁距离** | 最近站 < 1km 优先 | ★★★★☆ |
| **建筑年代** | 2008+ 为次新，板楼优于塔楼 | ★★★☆☆ |
| **容积率** | < 2.0 为低密度 | ★★★☆☆ |
| **物业品质** | 绿城/仁恒/万科 > 普通 | ★★☆☆☆ |
| **学区** | 若有孩子计划，需额外查证 | ★★★☆☆ |
