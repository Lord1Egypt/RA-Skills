# 示例：分析单只股票

**用户请求**：「分析贵州茅台」

## 执行流程

```
1. 获取准确时间
2. python {skillDir}/scripts/setup_dependencies.py
3. ls -la (检查工作目录)
4. mkdir {OUTPUT_DIR}/financial_data/600519_SH
5. fetch realtime (600519.SH) → {OUTPUT_DIR}/financial_data/600519_SH/
6. fetch history 3y (600519.SH) → {OUTPUT_DIR}/financial_data/600519_SH/
7. fetch fundamental (600519.SH) → {OUTPUT_DIR}/financial_data/600519_SH/
8. calculate_indicators (all)
9. calculate_risk_metrics
10. list_dir (检查文件)
11. read_file × 3 (实时、指标、风险)
12. ⭐⭐ fetch_trending.py 获取全网热点（必须先于搜索执行！）
13. ⭐ macro_analysis.py --dashboard --trending-json（宏观数据+热点分类+关键词提取）
14. read_file macro_dashboard.json（重点关注 hot_keywords 部分）
15. ⭐ web_search × 3-4 (公司新闻、行业政策、财报、机构观点)
16. ⭐ web_search × 5-8 (地缘政治、中美关系、国内政策、央行操作等)
17. ⭐ web_search × N (基于 hot_keywords.dynamic_search_queries 的动态搜索)
18. 创建 research_materials.json（素材归档）
19. 深度思考（按思考路径模板推理）
20. 创建 ai_analysis.json + ai_deep_analysis.json（综合分析研判拆分为双文件）
21. generate_html_report --macro-json --ai-analysis-json --ai-deep-analysis-json
22. 检查报告质量，如需补充则 replace_in_file 修改
23. list_dir (展示文件清单)
```

## 具体命令

```bash
# 1. 安装依赖
python {skillDir}/scripts/setup_dependencies.py

# 2. 创建目录
mkdir -p {OUTPUT_DIR}/financial_data/600519_SH

# 3. 实时行情
python {skillDir}/scripts/fetch_stock_data.py \
  --symbol 600519.SH --type realtime \
  --output-dir {OUTPUT_DIR}/financial_data/600519_SH --format csv

# 4. 历史数据（3年）
python {skillDir}/scripts/fetch_stock_data.py \
  --symbol 600519.SH --type history --period 3y \
  --output-dir {OUTPUT_DIR}/financial_data/600519_SH --format csv

# 5. 基本面数据
python {skillDir}/scripts/fetch_stock_data.py \
  --symbol 600519.SH --type fundamental \
  --output-dir {OUTPUT_DIR}/financial_data/600519_SH --format csv

# 6. 技术指标
python {skillDir}/scripts/calculate_indicators.py \
  --input {OUTPUT_DIR}/financial_data/600519_SH/600519_SH_history.csv \
  --output {OUTPUT_DIR}/financial_data/600519_SH/600519_SH_indicators.csv \
  --indicator all

# 7. 风险指标
python {skillDir}/scripts/calculate_risk_metrics.py \
  --input {OUTPUT_DIR}/financial_data/600519_SH/600519_SH_history.csv \
  --output {OUTPUT_DIR}/financial_data/600519_SH/600519_SH_risk_metrics.json \
  --risk-free-rate 0.03

# 8. ⭐⭐ 全网时政热点采集（必须先于搜索执行！关键：必须先于搜索执行）
python {skillDir}/scripts/fetch_trending.py \
  --all --limit 20 \
  --output {OUTPUT_DIR}/financial_data/trending.json

# 9. ⭐ 宏观分析 + 热点分类 + 关键词提取（一步完成）
python {skillDir}/scripts/macro_analysis.py \
  --dashboard \
  --trending-json {OUTPUT_DIR}/financial_data/trending.json \
  --stock-name "贵州茅台" \
  --industry "白酒" \
  --reference-date {当前日期YYYY-MM-DD} \
  --news-max-age-days 30 \
  --output {OUTPUT_DIR}/financial_data/macro_dashboard.json

# 10. 读取 macro_dashboard.json，重点关注 hot_keywords 部分
# 查看 hot_keywords.dynamic_search_queries 获取动态搜索建议
# 查看 hot_keywords.coverage_gaps 获取覆盖盲区
# 查看 hot_keywords.impact_chains 获取事件→行业传导链

# 11. 创建素材归档文件（将所有收集信息结构化写入）
cat > {OUTPUT_DIR}/financial_data/research_materials.json << 'MATERIALS_EOF'
{
  "meta": {
    "target": "贵州茅台(600519.SH)",
    "industry": "白酒",
    "analysis_date": "{当前日期}",
    "materials_version": "1.0"
  },
  "data_files": {
    "realtime": "600519_SH/600519_SH_realtime.csv",
    "history": "600519_SH/600519_SH_history.csv",
    "fundamental": "600519_SH/600519_SH_fundamental.csv",
    "indicators": "600519_SH/600519_SH_indicators.csv",
    "risk_metrics": "600519_SH/600519_SH_risk_metrics.json",
    "macro_dashboard": "macro_dashboard.json",
    "trending": "trending.json"
  },
  "hot_keywords_summary": {
    "top_entities": ["从 hot_keywords.hot_entities 摘取 top 10"],
    "key_impact_chains": ["从 impact_chains 摘取 relevance=high 的"],
    "coverage_gaps": ["从 coverage_gaps 摘取"]
  },
  "news_intelligence": {
    "company_news": ["贵州茅台最新公告和新闻"],
    "industry_news": ["白酒行业政策和动态"],
    "geopolitical_events": ["地缘政治事件及对消费板块影响"],
    "macro_policy": ["宏观政策和央行动态"],
    "global_markets": ["全球市场走势"],
    "dynamic_hotspot_findings": ["动态搜索发现的重要信息"]
  },
  "trending_highlights": {
    "geopolitical": ["地缘政治类热点 top 5"],
    "national_policy": ["国家政策类热点 top 5"],
    "company_related": ["茅台相关热点"],
    "industry_related": ["白酒/消费行业热点"]
  }
}
MATERIALS_EOF

# 12. 创建 AI 综合分析 JSON（拆分为双文件：核心结论+事件影响 / 推理链路+多维分析）
cat > {OUTPUT_DIR}/financial_data/ai_analysis.json << 'EOF'
{
  "summary": "贵州茅台作为白酒龙头，品牌护城河深厚，当前估值处于历史中位数附近，建议逢低布局",
  "recommendation": "谨慎买入",
  "target_price": {"low": 1650, "mid": 1800, "high": 2000},
  "stop_loss": 1450,
  "news_intelligence": {
    "key_events": [
      {"event": "茅台2025年年报营收突破1500亿", "impact": "超预期增长印证品牌龙头地位", "direction": "利好"},
      {"event": "消费刺激政策持续加码", "impact": "直接利好高端消费品", "direction": "利好"}
    ],
    "geopolitical": [
      {"event": "中东局势持续紧张", "impact": "通过原油价格间接影响消费品成本，但影响有限", "direction": "中性"},
      {"event": "中美关系缓和信号", "impact": "利好市场风险偏好，提振消费板块估值", "direction": "利好"}
    ],
    "macro_policy": [
      {"event": "LPR持续下调，货币政策维持宽松", "impact": "降低贴现率，利好成长股估值修复", "direction": "利好"},
      {"event": "财政政策加大基建投入", "impact": "间接带动消费信心恢复", "direction": "利好"}
    ],
    "industry_dynamics": [
      {"event": "高端白酒市场集中度进一步提升", "impact": "龙头企业市占率持续扩大", "direction": "利好"}
    ],
    "company_specific": [
      {"event": "茅台推出新产品线", "impact": "拓展消费场景，但需关注品牌稀释风险", "direction": "利好"}
    ],
    "market_sentiment": [
      {"event": "北向资金连续3周净买入消费板块", "impact": "外资看好消费赛道，提供估值支撑", "direction": "利好"}
    ]
  },
  "impact_assessment": [
    {
      "event": "中东局势紧张",
      "transmission": "中东冲突 → 原油价格上涨 → 运输/包装成本上升 → 白酒成本微增(影响<1%)",
      "direction": "利空",
      "strength": "弱",
      "duration": "短期冲击"
    },
    {
      "event": "消费刺激政策加码",
      "transmission": "政策出台 → 居民消费意愿提升 → 高端白酒需求增加 → 茅台量价齐升",
      "direction": "利好",
      "strength": "强",
      "duration": "中期影响"
    },
    {
      "event": "LPR持续下调",
      "transmission": "降息 → 无风险利率下降 → 股票贴现率降低 → 成长股估值修复",
      "direction": "利好",
      "strength": "中",
      "duration": "长期趋势"
    }
  ]
}
EOF

cat > {OUTPUT_DIR}/financial_data/ai_deep_analysis.json << 'EOF'
{
  "thinking_trace": {
    "information_scan": "Top 10 关键信息：1.茅台2025年报营收增长15% 2.白酒消费政策利好 3.LPR持续下调 4.中东局势对消费品影响有限 5.北向资金持续流入 6.高端白酒集中度提升 7.新产品线扩展 8.社保基金增持 9.PMI回升至荣枯线以上 10.人民币汇率企稳",
    "impact_transmission": "中东局势→原油→消费品成本间接影响(弱) | 消费政策→白酒龙头直接利好(强) | LPR下调→估值修复(中) | 北向资金→估值支撑(中)",
    "cross_validation": "技术面超卖+基本面优秀→超卖修复机会 | 宏观宽松+消费复苏→估值修复支撑 | 市场情绪偏谨慎但基本面确定性强→存在预期差",
    "risk_matrix": "地缘冲突升级(低概率/中影响) | 消费下行(中概率/大影响) | 政策风险-限制三公消费(低概率/大影响) | 估值回调(中概率/中影响)",
    "decision_logic": "基于PE28倍历史分位45%+ROE32%+自由现金流强劲→估值合理偏低→逢低买入策略 | 催化剂：年报业绩+消费政策 | 最大风险：消费降级趋势"
  },
  "sections": [
    {"title": "技术面研判", "content": "均线系统：MA5(1520)与MA10(1535)形成短期死叉，但MA60(1580)仍有支撑...MACD：DIF(-8.2)与DEA(-5.1)均处于零轴下方，绿柱有收窄迹象...RSI：14日RSI为35.2，接近超卖区间...布林带：价格运行在中轨(1560)和下轨(1480)之间...KDJ：J值22.5，进入超卖区域...综合判断：技术面偏弱但超卖修复信号初现。"},
    {"title": "基本面与业绩分析", "content": "营收：2025年全年营收1500亿元，同比增长15.3%...净利润：归母净利润750亿，同比增长13.8%...ROE：加权ROE 32.5%，连续5年保持30%以上...现金流：经营现金流净额820亿，远超净利润...估值：当前PE(TTM)约28倍，处于近5年历史分位数45%..."},
    {"title": "行业与政策展望", "content": "行业景气度：高端白酒市场维持结构性繁荣...行业政策：消费升级政策整体利好品牌白酒...竞争格局：茅台市场地位稳固...催化剂：春节旺季、新产品线扩展..."},
    {"title": "宏观环境与热点事件影响", "content": "经济周期：当前处于弱复苏阶段...货币政策：LPR持续下调，利好消费股估值修复...\n【热点传导分析】根据热点关键词提取结果，当前中东局势对消费品行业影响有限（间接通过原油成本<1%），但国内消费政策持续利好是核心催化剂...\n【事件传导链】消费刺激政策→居民消费意愿↑→高端白酒需求↑→茅台量价齐升(强利好)\n中东紧张→原油↑→运输成本微增→白酒成本影响极小(弱利空)\nLPR下调→贴现率↓→成长股估值修复→茅台PE合理区间上移(中利好)"},
    {"title": "投资策略建议", "content": "投资评级：谨慎买入...目标价：保守1650/基准1800/乐观2000...买入策略：理想买入区间1450-1520元...止盈止损策略...仓位建议：总仓位不超过个人组合的15%..."}
  ]
}
EOF

# 13. 生成报告（含宏观分析 + AI综合分析双文件）
python {skillDir}/scripts/generate_html_report.py \
  --title '贵州茅台(600519)投资分析报告' \
  --data-dir {OUTPUT_DIR}/financial_data/600519_SH \
  --output {OUTPUT_DIR}/贵州茅台投资分析报告.html \
  --macro-json {OUTPUT_DIR}/financial_data/macro_dashboard.json \
  --ai-analysis-json {OUTPUT_DIR}/financial_data/ai_analysis.json \
  --ai-deep-analysis-json {OUTPUT_DIR}/financial_data/ai_deep_analysis.json
```

## 新闻搜索（基于热点关键词的动态搜索 + 常规搜索）

```typescript
// === 常规公司/行业搜索 ===
web_search({ searchTerm: '贵州茅台 最新新闻 2026', explanation: '获取公司最新动态' });
web_search({ searchTerm: '白酒行业 政策 监管 2026', explanation: '了解行业政策变化' });
web_search({ searchTerm: '贵州茅台 2025年财报 业绩', explanation: '获取最新财务表现' });
web_search({ searchTerm: '贵州茅台 机构评级 研报', explanation: '了解机构投资观点' });

// === 宏观与国际层面搜索 ===
web_search({ searchTerm: '地缘政治 台海 中东 俄乌 冲突 2026', explanation: '了解地缘政治风险' });
web_search({ searchTerm: '中美关系 贸易摩擦 关税 2026', explanation: '了解中美关系进展' });
web_search({ searchTerm: '国务院 产业政策 消费品 财政政策 2026', explanation: '了解国内政策变化' });
web_search({ searchTerm: '中国人民银行 MLF LPR 降准 降息 2026', explanation: '获取央行最新操作' });
web_search({ searchTerm: '美股 纳斯达克 全球市场 走势 2026', explanation: '了解全球市场走势' });
web_search({ searchTerm: '人民币汇率 北向资金 外资流向 2026', explanation: '了解外资动态' });

// === 动态热点搜索（基于 macro_dashboard.json 的 hot_keywords）===
// 示例：假设热点中出现了"伊朗"关键词
web_search({ searchTerm: '伊朗 最新 局势 影响 2026', explanation: '热点关键词"伊朗"在多条热搜中出现' });
// 示例：假设 coverage_gaps 中有"胡塞"
web_search({ searchTerm: '胡塞 最新动态 影响 2026', explanation: '覆盖盲区补充：胡塞武装最新动态' });
```

## 全网时政热点采集（必须先于搜索执行）

通过 `fetch_trending.py` 脚本直接从各平台公开接口采集热榜数据，**不局限于金融新闻**，覆盖地缘政治、国家政策、央行/银行活动、全球时事等：

**⚠️ 时效性要求**：热点数据必须当天或前一天获取，超过 48 小时需重新采集。

```bash
# 采集全部 13 平台热点
python {skillDir}/scripts/fetch_trending.py \
  --all --limit 20 \
  --output {OUTPUT_DIR}/financial_data/trending.json
```

采集后立即传入 `macro_analysis.py`，一步完成热点分类 + 关键词提取 + 动态搜索建议生成。

## 预期输出文件

```
{OUTPUT_DIR}/
├── financial_data/
│   ├── macro_dashboard.json              ← 宏观数据+热点分类+关键词提取+动态搜索建议
│   ├── trending.json                     ← 全网时政热点（fetch_trending.py 采集）
│   ├── research_materials.json           ← 素材归档
│   ├── ai_analysis.json                  ← AI 综合分析研判（核心结论+事件影响+新闻情报）
│   ├── ai_deep_analysis.json             ← AI 深度分析（推理链路+多维分析）
│   └── 600519_SH/
│       ├── 600519_SH_realtime.csv
│       ├── 600519_SH_history.csv
│       ├── 600519_SH_fundamental.csv
│       ├── 600519_SH_indicators.csv
│       └── 600519_SH_risk_metrics.json
└── 贵州茅台投资分析报告.html              ← 含宏观+关键事件影响+深度思考+AI综合分析区块
```

---

# 示例：深度分析单只股票（专业模式）

**用户请求**：「深度分析贵州茅台，做一个 DCF 估值」

## 执行流程

```
1-11. 同基础流程
12. ⭐⭐ fetch_trending.py 获取全网热点（必须先于搜索执行！）
13. ⭐ macro_analysis.py --dashboard --trending-json（宏观+热点分类+关键词提取）
14. read_file macro_dashboard.json（重点关注 hot_keywords）
15. ⭐ web_search × 3-4 (公司新闻、行业政策、财报、机构观点)
16. ⭐ web_search × 5-8 (地缘政治、中美关系、国内政策、央行操作等)
17. ⭐ web_search × N (基于 hot_keywords 的动态搜索)
18. 创建 research_materials.json（素材归档）
19. calculate_valuation --mode dcf (DCF 估值)
20. calculate_valuation --mode comps --peers "..." (可比公司分析)
21. 深度思考（按思考路径模板推理，含估值分析）
22. 创建 ai_analysis.json + ai_deep_analysis.json（综合分析研判拆分为双文件）
23. generate_html_report --valuation-json --comps-json --macro-json --ai-analysis-json --ai-deep-analysis-json
24. 检查报告质量，如需补充则 replace_in_file 修改
25. list_dir (展示文件清单)
```

## 新增命令（在基础流程基础上追加估值步骤，报告命令替换基础版）

```bash
# 10. DCF 估值分析
python {skillDir}/scripts/calculate_valuation.py \
  --symbol 600519.SH \
  --data-dir {OUTPUT_DIR}/financial_data/600519_SH \
  --output {OUTPUT_DIR}/financial_data/600519_SH/600519_SH_valuation.json \
  --mode dcf

# 11. 可比公司分析
python {skillDir}/scripts/calculate_valuation.py \
  --symbol 600519.SH \
  --data-dir {OUTPUT_DIR}/financial_data/600519_SH \
  --output {OUTPUT_DIR}/financial_data/600519_SH/600519_SH_comps.json \
  --mode comps \
  --peers "000858.SZ,000568.SZ,603369.SH"

# 12. 生成深度报告（替换基础流程的报告命令，只生成一份完整报告）
python {skillDir}/scripts/generate_html_report.py \
  --title '贵州茅台(600519)深度投资分析报告' \
  --data-dir {OUTPUT_DIR}/financial_data/600519_SH \
  --output {OUTPUT_DIR}/贵州茅台深度分析报告.html \
  --valuation-json {OUTPUT_DIR}/financial_data/600519_SH/600519_SH_valuation.json \
  --comps-json {OUTPUT_DIR}/financial_data/600519_SH/600519_SH_comps.json \
  --macro-json {OUTPUT_DIR}/financial_data/macro_dashboard.json \
  --ai-analysis-json {OUTPUT_DIR}/financial_data/ai_analysis.json \
  --ai-deep-analysis-json {OUTPUT_DIR}/financial_data/ai_deep_analysis.json
```

## 深度报告输出文件

```
{OUTPUT_DIR}/
├── financial_data/
│   ├── macro_dashboard.json              ← 宏观数据+热点分类+关键词提取
│   ├── trending.json                     ← 全网时政热点
│   ├── research_materials.json           ← 素材归档
│   ├── ai_analysis.json                  ← AI 综合分析研判（核心结论+事件影响+新闻情报）
│   ├── ai_deep_analysis.json             ← AI 深度分析（推理链路+多维分析）
│   └── 600519_SH/
│       ├── 600519_SH_realtime.csv
│       ├── 600519_SH_history.csv
│       ├── 600519_SH_fundamental.csv
│       ├── 600519_SH_indicators.csv
│       ├── 600519_SH_risk_metrics.json
│       ├── 600519_SH_valuation.json    ← DCF + 三表分析
│       └── 600519_SH_comps.json        ← 可比公司分析
└── 贵州茅台深度分析报告.html               ← 含估值+热点传导+深度思考+AI综合分析区块
```
