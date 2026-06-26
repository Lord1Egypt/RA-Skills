# 示例：对比分析多只股票

**用户请求**：「对比分析贵州茅台和五粮液」

## 执行流程

```
1. 获取准确时间
2. python {skillDir}/scripts/setup_dependencies.py
3. ls -la (检查工作目录)
4. mkdir {OUTPUT_DIR}/financial_data/600519_SH + mkdir {OUTPUT_DIR}/financial_data/000858_SZ
5-7. fetch realtime/history/fundamental (600519.SH) × 3
8-10. fetch realtime/history/fundamental (000858.SZ) × 3
11-12. calculate_indicators × 2
13-14. calculate_risk_metrics × 2
15. list_dir (检查文件)
16. read_file × 6
17. ⭐⭐ fetch_trending.py 获取全网热点（必须先于搜索执行！）
18. ⭐ macro_analysis.py --dashboard --trending-json（宏观+热点分类+关键词提取）
19. read_file macro_dashboard.json（重点关注 hot_keywords）
20. ⭐ web_search × 4-6 (两只股票的新闻、行业政策)
21. ⭐ web_search × 3-5 (宏观政策、国际局势、全球市场、大宗商品、汇率资金)
22. ⭐ web_search × N (基于 hot_keywords 的动态搜索)
23. 创建 research_materials.json（素材归档）
24. 深度思考 + 对比分析
25. 创建 ai_analysis.json + ai_deep_analysis.json（综合分析研判拆分为双文件）
26. generate_html_report --macro-json --ai-analysis-json --ai-deep-analysis-json (分别生成或合并报告)
27. list_dir (展示清单)
```

## 全网时政热点采集（必须先于搜索执行）

```bash
# 采集全部 13 平台热点
python {skillDir}/scripts/fetch_trending.py \
  --all --limit 20 \
  --output {OUTPUT_DIR}/financial_data/trending.json

# 宏观分析 + 热点分类 + 关键词提取
python {skillDir}/scripts/macro_analysis.py \
  --dashboard \
  --trending-json {OUTPUT_DIR}/financial_data/trending.json \
  --stock-name "贵州茅台" \
  --industry "白酒" \
  --reference-date {当前日期YYYY-MM-DD} \
  --output {OUTPUT_DIR}/financial_data/macro_dashboard.json
```

将采集的热点数据传入宏观分析，脚本会自动分类为 13 个类别并提取热点关键词、生成动态搜索建议和事件→行业传导链。

## 对比分析要点

- **收益率对比**：年化收益率、累计收益率
- **风险对比**：波动率、最大回撤、夏普比率
- **估值对比**：PE、PB 相对高低
- **技术面对比**：均线排列、MACD/RSI 信号
- **基本面对比**：ROE、营收增长率、净利润增长率
- **热点对比**：行业地位、政策影响差异
- **宏观背景**：经济周期阶段、行业轮动建议、国际局势影响
- **热点事件传导**：基于 impact_chains 分析不同事件对两只股票的差异化影响

---

# 示例：对比分析 ETF

**用户请求**：「对比分析消费ETF(159928)和军工ETF(512660)」

## 注意事项

- ETF代码使用6位纯数字（如 `159928`、`512660`），**不加 `.SH`/`.SZ` 后缀**
- ETF 的 fundamental 数据会返回说明信息（ETF 无传统财务指标）
- 对比重点：历史收益率、波动率、夏普比率、最大回撤
- ⭐ **必须搜索行业热点**：行业政策、订单情况、资金流向

## ETF 新闻搜索示例

```typescript
// 公司/行业层面搜索
web_search({ searchTerm: '消费板块 行业趋势 政策 2026', explanation: '了解消费行业整体动态' });
web_search({ searchTerm: '军工行业 订单 国防预算 2026', explanation: '了解军工板块催化剂' });

// 宏观与国际层面搜索
web_search({ searchTerm: '中国宏观经济 GDP CPI PMI 2026', explanation: '了解宏观经济数据走向' });
web_search({ searchTerm: '全球地缘政治 中美关系 贸易 2026', explanation: '评估国际局势对行业影响' });
web_search({ searchTerm: '北向资金 外资流向 A股 2026', explanation: '了解资金面变化' });

// 动态热点搜索（基于 hot_keywords）
// 根据 macro_dashboard.json 中的 hot_keywords.dynamic_search_queries 执行
```

## 港股分析注意

- 港股代码**必须是5位数字**：`00700.HK`（腾讯）、`01810.HK`（小米）
- 4位代码（`0700`）会导致查询失败，必须补齐为5位
- 港股不支持 fundamental/financial 数据
