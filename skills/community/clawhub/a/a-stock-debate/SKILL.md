---
name: stock-debate
description: A股多空辩论深度分析 - 多空研究员对抗辩论式个股深度研究，输出结构化投资简报
tags: [A股, 深度分析, 多空辩论, 投资, 个股研究]
---

# A股多空辩论深度分析 Skill V2.1

## 触发条件

用户说出以下任一表述时触发：
- 「深度辩论分析 XXX」
- 「多空分析 XXX」
- 「辩论分析 XXX」

其中 XXX 为股票代码、名称或简称。

## 数据架构

| 数据类型 | 来源 | 代理 | 备注 |
|---------|------|------|------|
| 实时行情 | 腾讯财经 | ❌ 直连 | 海外稳定可用 |
| K线历史 | 腾讯财经 | ❌ 直连 | 日/周/月，前复权 |
| 资金流向 | 东方财富 datacenter | ✅ 代理 | 需mihomo运行 |
| 财务指标 | Tushare | ❌ 直连 | 已配置token |

### 代理配置
- 工具：mihomo (Clash Meta)，端口 HTTP 7890
- 代理地址从环境变量 `STOCK_PROXY` 读取（默认 `http://127.0.0.1:7890`）
- 启动命令：`/tmp/mihomo_bin -f /tmp/mihomo_config.yaml -d /tmp/mihomo_data`
- 配置文件：`/tmp/mihomo_config.yaml`（从订阅生成）

### LLM API 配置
- base URL：`https://open.bigmodel.cn/api/paas/v4`
- API Key：从环境变量 `GLM_API_KEY` 读取
- 模型：glm-4-flash（基本面/技术面）、glm-5（辩论/决策）

## 执行流程

### 第1步：启动代理（按需，采集完必须关闭）

> ⚠️ **重要**：代理仅在获取东方财富数据时启动，采集完成后**必须立即关闭**，避免影响服务器其他使用场景（新加坡 IP 直连）。

```bash
# 启动代理（如未运行）
stock_start_proxy() {
    pgrep -f mihomo_bin > /dev/null && return
    nohup /tmp/mihomo_bin -f /tmp/mihomo_config.yaml -d /tmp/mihomo_data > /tmp/mihomo.log 2>&1 &
    sleep 2
    curl -s --connect-timeout 5 --proxy ${STOCK_PROXY:-http://127.0.0.1:7890} https://httpbin.org/ip | grep -q origin || echo "PROXY_DOWN"
}

# 关闭代理（采集完成后必须调用）
stock_stop_proxy() {
    pkill -f mihomo_bin 2>/dev/null
    sleep 1
}

# 使用方式：
stock_start_proxy
# ... 执行数据采集 ...
stock_stop_proxy
```

### 第2步：数据采集

通过 exec 执行以下 Python 脚本，采集个股行情、财务和资金数据。将 `{CODE}` 替换为实际股票代码（如 `600519`）。

```python
import requests, json, datetime, os

code = "{CODE}"
proxy = os.environ.get("STOCK_PROXY", "http://127.0.0.1:7890")
proxies = {"http": proxy, "https": proxy}

# 市场前缀
prefix = "sh" if code.startswith("6") else "sz"

# === 1. 实时行情（腾讯财经 - 直连，海外稳定） ===
try:
    r = requests.get(f"https://qt.gtimg.cn/q={prefix}{code}", timeout=10)
    r.encoding = 'gbk'
    parts = r.text.split('~')
    current = {
        "名称": parts[1], "代码": code,
        "最新价": float(parts[3]), "涨跌幅": float(parts[32]),
        "今开": float(parts[5]), "最高": float(parts[33]),
        "最低": float(parts[34]), "昨收": float(parts[4]),
        "成交量": int(parts[6]), "成交额": float(parts[37]),
        "换手率": float(parts[38]) if parts[38] else None,
        "市盈率": float(parts[39]) if parts[39] else None,
        "总市值": round(float(parts[45]) / 10000, 2) if parts[45] else None,
        "流通市值": round(float(parts[46]) / 10000, 2) if parts[46] else None,
        "60日最高": float(parts[41]) if parts[41] else None,
        "60日最低": float(parts[42]) if parts[42] else None,
    }
    print(f"实时行情: {current['名称']} {current['最新价']}元 PE{current['市盈率']} 市值{current['总市值']}亿")
except Exception as e:
    print(f"实时行情失败: {e}")
    current = {"代码": code, "名称": "未知"}

# === 2. 近60日K线（腾讯财经 - 直连） ===
kline_data = []
try:
    end_date = datetime.date.today().strftime("%Y-%m-%d")
    start_date = (datetime.date.today() - datetime.timedelta(days=90)).strftime("%Y-%m-%d")
    r = requests.get(
        f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get",
        params={"param": f"{prefix}{code},day,{start_date},{end_date},60,qfq"},
        timeout=10
    )
    d = r.json()["data"][f"{prefix}{code}"]
    for item in d.get("qfqday", [])[-60:]:
        kline_data.append({
            "日期": item[0], "开盘": float(item[1]), "收盘": float(item[2]),
            "最高": float(item[3]), "最低": float(item[4]),
            "成交量": float(item[5]),
        })
    if len(kline_data) >= 2:
        current["60日涨跌幅"] = round((kline_data[-1]["收盘"] / kline_data[0]["收盘"] - 1) * 100, 2)
    print(f"K线: {len(kline_data)}条 60日涨跌: {current.get('60日涨跌幅')}%")
except Exception as e:
    print(f"K线失败: {e}")

# === 3. 资金流向（东方财富 datacenter - 需代理） ===
fund_flow = []
try:
    secid = f"{'1' if code.startswith('6') else '0'}.{code}"
    r = requests.get(
        "https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get",
        params={"secid": secid, "fields1": "f1,f2,f3", "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65", "lmt": 10, "klt": 101},
        proxies=proxies, timeout=15
    )
    for line in r.json()["data"]["klines"][:10]:
        parts = line.split(",")
        fund_flow.append({
            "日期": parts[0], "主力净流入": float(parts[1]),
            "超大单净流入": float(parts[2]), "大单净流入": float(parts[3]),
            "中单净流入": float(parts[4]), "小单净流入": float(parts[5]),
        })
    print(f"资金流向: {len(fund_flow)}条")
except Exception as e:
    print(f"资金流向失败: {e}")

# === 4. 财务指标（AkShare - 直连） ===
financials = {}
try:
    import akshare as ak
    fin = ak.stock_financial_analysis_indicator(symbol=code, start_year="2023")
    if fin is not None and len(fin) > 0:
        for _, row in fin.tail(2).iterrows():
            period = str(row.get("日期", ""))
            financials[period] = {
                "每股收益": row.get("摊薄每股收益(元)"),
                "净资产收益率": row.get("净资产收益率(%)"),
                "销售净利率": row.get("销售净利率(%)"),
                "销售毛利率": row.get("销售毛利率(%)"),
                "营收增长率": row.get("主营业务收入增长率(%)"),
                "净利润增长率": row.get("净利润增长率(%)"),
                "资产负债率": row.get("资产负债率(%)"),
                "流动比率": row.get("流动比率"),
            }
        print(f"财务指标: {list(financials.keys())}")
except Exception as e:
    print(f"财务指标失败: {e}")

print(json.dumps({"current": current, "kline_60d": kline_data, "fund_flow_10d": fund_flow, "financials": financials}, ensure_ascii=False, default=str))
```

### 第 2.5 步：关闭代理（必须）

> ⚠️ **重要**：数据采集完成后**必须立即关闭代理**，避免影响服务器其他使用场景。

```bash
stock_stop_proxy
echo "代理已关闭，出口 IP 已恢复新加坡直连"
```


### 第3步：基本面分析

将采集到的 `current`、`financials` 数据喂给 GLM（glm-4-flash），生成基本面摘要。

**Prompt：**
```
你是一位资深A股基本面研究员。基于以下财务数据，进行基本面分析。

数据：
{current_data}
{financial_data}

要求：
1. 营收和利润趋势（同比、环比）
2. 盈利能力评估（ROE、净利率、毛利率）
3. 估值水平（PE、PB与行业对比）
4. 财务健康度（资产负债、现金流）
5. 给出基本面评分（1-10分，10为最优）

用数据说话，每个结论必须有数据支撑。
```

### 第4步：技术面分析

将 `kline_60d` 和 `fund_flow_10d` 数据喂给 GLM（glm-4-flash），生成技术面摘要。

**Prompt：**
```
你是一位A股技术分析师。基于以下数据，进行技术面分析。

近60日K线数据：
{kline_data}

近10日资金流向：
{fund_flow_data}

要求：
1. 趋势判断（短期/中期/长期）
2. 均线系统状态（MA5/10/20/60排列）
3. 成交量分析（放量/缩量、量价配合）
4. 关键支撑位和压力位
5. 资金流向解读（主力动向）
6. 技术面评分（1-10分，10为最强）

每个结论必须有具体价格和数值支撑。
```

### 第5步：多空辩论（核心）

使用 glm-5 进行深度推理。分三阶段完成：

#### 阶段A：多头研究员建仓

```
你是一位看多研究员。你的任务是为该股票找到至少5条看多论据。

## 标的基本信息
{basic_info}

## 基本面分析
{fundamental_analysis}

## 技术面分析
{technical_analysis}

## 要求
1. 列出至少5条看多论据，每条必须：
   - 有明确的数据/数字支撑
   - 说明逻辑链条（为什么这个因素利好）
   - 给出该论据的置信度（高/中/低）
2. 识别1-2个你可能遗漏的风险
3. 给出你的目标价区间和逻辑
```

#### 阶段B：空头研究员建仓

```
你是一位看空研究员。你的任务是为该股票找到至少5条看空论据。

## 标的基本信息
{basic_info}

## 基本面分析
{fundamental_analysis}

## 技术面分析
{technical_analysis}

## 要求
1. 列出至少5条看空论据，每条必须：
   - 有明确的数据/数字支撑
   - 说明逻辑链条（为什么这个因素利空）
   - 给出该论据的严重程度（高/中/低）
2. 不要敷衍，要找到真正的风险点
3. 给出你认为的合理估值下限和逻辑
```

#### 阶段C：2轮辩论

**第1轮 - 多头反驳空头：**
```
你是多头研究员。空头提出了以下观点，请逐一反驳：

## 空头观点
{bear_thesis}

## 原始数据
{data_summary}

要求：
1. 逐条反驳空头论据，用数据说话
2. 承认空头说得对的地方（如果有）
3. 补充多头的新论据（如果有的话）
```

**第1轮 - 空头反驳多头：**
```
你是空头研究员。多头提出了以下观点，请逐一反驳：

## 多头观点
{bull_thesis}

## 原始数据
{data_summary}

要求：
1. 逐条反驳多头论据，用数据说话
2. 承认多头说得对的地方（如果有）
3. 补充空头的新风险点（如果有的话）
```

**第2轮 - 双方收尾反驳：**（同理，交换反驳对方第1轮的反驳，但更精炼）

> ⚠️ **Token控制**：辩论阶段用 glm-5，但每轮 prompt 控制在 3000 字以内。可将数据摘要化后传入，避免传完整原始数据。

### 第6步：综合决策

使用 glm-5 汇总所有分析。

```
你是一位经验丰富的A股交易员。请基于以下多空辩论结果，给出操作建议。

## 标的：{stock_name}（{stock_code}），当前价 {current_price}

## 多头观点摘要
{bull_summary}

## 空头观点摘要
{bear_summary}

## 辩论核心分歧点
{key_debates}

## 要求
给出明确的可执行建议：
1. 操作方向：买入 / 持有 / 卖出 / 观望
2. 仓位建议：占总资金比例（如 20%）
3. 目标价：基于数据推算
4. 止损价：基于技术面关键位
5. 时间框架：短线（1-2周）/ 中线（1-3月）/ 中长线（3-6月）
6. 置信度：高/中/低
7. 一句话总结理由

如果信息不足以决策，明确说明缺什么。
```

### 第7步：风险提示

从空头论据和辩论中提炼 3-5 个关键风险点，格式：

```
⚠️ **关键风险提示**
1. 【风险类型】具体描述 + 影响程度
2. ...
```

## 输出格式模板

```
# ⚔️ 多空辩论深度分析报告

## 📊 标的基本信息
| 项目 | 数值 |
|------|------|
| 名称 | {name} |
| 代码 | {code} |
| 当前价 | {price} |
| 60日涨跌 | {chg_60d} |
| 市盈率 | {pe} |
| 总市值 | {market_cap} |

---

## 📈 多头观点

### 多头论据
1. **[论据标题]** {论据内容}（置信度：{高/中/低}）
2. ...

### 多头反驳记录
- 对空头论据X的反驳：...

---

## 📉 空头观点

### 空头论据
1. **[论据标题]** {论据内容}（严重程度：{高/中/低}）
2. ...

### 空头反驳记录
- 对多头论据X的反驳：...

---

## ⚔️ 辩论核心分歧点

| 分歧点 | 多头立场 | 空头立场 | 裁定 |
|--------|---------|---------|------|
| {issue1} | ... | ... | {偏向多方/偏向空方/持平} |
| ... | ... | ... | ... |

---

## 🎯 综合操作建议

| 项目 | 建议 |
|------|------|
| 操作方向 | {买入/持有/卖出/观望} |
| 建议仓位 | {XX%} |
| 目标价 | {price}（{逻辑}） |
| 止损价 | {price}（{关键位}） |
| 时间框架 | {短线/中线/中长线} |
| 置信度 | {高/中/低} |
| 理由 | {一句话} |

---

## ⚠️ 风险提示
1. ...
2. ...

---
*报告生成时间：{datetime} | 数据来源：腾讯财经+东方财富 | 本报告仅供参考，不构成投资建议*
```

## 注意事项

1. **数据真实性**：所有论据必须基于实际采集数据，禁止编造数字
2. **Token预算**：整个流程控制在 3 万 token 以内，数据传入 LLM 前先摘要化
3. **模型选择**：数据采集用 Python，基本面/技术面初判用 glm-4-flash，辩论和决策用 glm-5
4. **执行顺序**：严格按 7 步顺序执行，不可跳步
5. **辩论质量**：空头不能敷衍，必须找到真正的风险；多头不能只说好的，要承认不确定性
6. **免责声明**：报告末尾必须包含「不构成投资建议」的声明
