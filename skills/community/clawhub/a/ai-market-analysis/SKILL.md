---
name: AI-market-analysis
description: 市场与行业分析框架：提供宏观经济、市场策略、固定收益及各大行业（如半导体、医药、房地产、军工等）的通用分析框架。当用户需要分析特定行业或宏观市场，或者询问"XX行业的分析框架是什么"时触发。
agent_created: true
---

# Market Analysis Skills

本技能包含多种宏观经济、投资策略及各大行业的标准分析框架。当用户需要了解如何分析某个行业、市场趋势或投资策略时，请根据用户的具体需求，读取对应的参考文件。

## 🎯 核心原则

1.  **读取对应框架**：在回答用户关于特定行业或宏观经济的分析方法时，**必须**首先读取对应的 `.md` 参考文件。
2.  **通用化应用**：在应用这些框架时，需结合当前的实际市场环境和公司情况进行分析。
3.  **结构化输出**：参考框架的结构，为用户提供清晰、有条理的分析报告（如：核心逻辑、供需分析、竞争格局、关键指标等）。
4. **指标通过技能查询**：查看用户是否有东方财富妙想、NEO Data、iFind、Wind、同花顺等Skills，如有通过Skills获取数据
5. **信息检索**:检查信息调用腾讯新闻、公众号文章查询、WebSearch等Skills，多方数据源确认

## 📖 参考文件读取路由 (Reference File Reading Protocol)

请根据用户询问的主题（如果用户询问公司，需要将公司对应到具体的行业上进行分析），使用 `read_file` 工具读取 `references/` 目录下的相应文件：

### 宏观与策略 (Macro & Strategy)
*   **宏观经济分析 (Macro Economy)** -> 读取 `references/macro-economy.md`
*   **策略研究框架 (Strategy)** -> 读取 `references/strategy.md`
*   **固定收益/债市 (Fixed Income)** -> 读取 `references/fixed-income.md`
*   **金融工程 (Financial Engineering)** -> 读取 `references/financial-engineering.md`
*   **长股选股策略 (Long-term Strategy)** -> 读取 `references/long-term-strategy.md`

### 科技与制造 (Tech & Manufacturing)
*   **半导体行业 (Semiconductor)** -> 读取 `references/semiconductor.md`
*   **半导体设备与材料 (Semiconductor Equipment & Materials)** -> 读取 `references/semiconductor-equipment.md`
*   **人工智能 (Artificial Intelligence)** -> 读取 `references/artificial-intelligence.md`
*   **互联网行业 (Internet)** -> 读取 `references/internet.md`
*   **光伏行业 (Photovoltaics)** -> 读取 `references/photovoltaics.md`
*   **机械行业 (Machinery)** -> 读取 `references/machinery.md` 或 `references/machinery-2.md`
*   **国防军工 (Defense & Military)** -> 读取 `references/defense.md` 或 `references/military.md`
*   **汽车行业 (Automobiles)** -> 读取 `references/automobiles.md`
*   **新材料 (New Materials)** -> 读取 `references/new-materials.md`

### 医药与健康 (Healthcare)
*   **医药行业整体 (Pharmaceuticals)** -> 读取 `references/pharmaceuticals.md`
*   **创新药产业链 (Innovative Drugs)** -> 读取 `references/innovative-drugs.md`
*   **生物制药产业链上游 (Biopharma Upstream)** -> 读取 `references/biopharma-upstream.md`
*   **医疗器械 (Medical Devices)** -> 读取 `references/medical-devices.md`
*   **体外诊断 (IVD Medical Devices)** -> 读取 `references/ivd-medical-devices.md`
*   **医疗服务 (Medical Services)** -> 读取 `references/medical-services.md`
*   **创新疫苗 (Vaccines)** -> 读取 `references/vaccines.md`

### 消费与服务 (Consumer & Services)
*   **食品饮料 (Food & Beverage)** -> 读取 `references/food-and-beverage.md`
*   **商贸零售 (Retail)** -> 读取 `references/retail.md` 或 `references/retail-2.md`
*   **跨境电商 (Cross-border E-commerce)** -> 读取 `references/cross-border-ecommerce.md`
*   **家电行业 (Home Appliances)** -> 读取 `references/home-appliances.md` 或 `references/home-appliances-2.md`
*   **纺织服装 (Textiles & Apparel)** -> 读取 `references/textiles-and-apparel.md`
*   **农业与宠物消费 (Agriculture & Pets)** -> 读取 `references/agriculture.md`
*   **交运行业 (Transportation)** -> 读取 `references/transportation.md`

### 周期与金融地产 (Cyclical, Financials & Real Estate)
*   **房地产 (Real Estate)** -> 读取 `references/real-estate.md`
*   **物管及商管 (Property Management)** -> 读取 `references/property-management.md`
*   **银行业 (Banking)** -> 读取 `references/banking.md` 或 `references/banking-2.md`
*   **建材行业 (Construction Materials)** -> 读取 `references/construction-materials.md`
*   **钢铁行业 (Steel)** -> 读取 `references/steel.md`
*   **化工行业 (Chemicals)** -> 读取 `references/chemicals.md`
*   **有色金属 (Non-ferrous Metals)** -> 读取 `references/non-ferrous-metals.md`
*   **天然气行业 (Natural Gas)** -> 读取 `references/natural-gas.md`
*   **公用及环保 (Public Utilities & Environment)** -> 读取 `references/public-utilities.md`

## 🛠️ 建议工作流 (Suggested Workflow)

1.  **需求分析**：明确用户询问的特定行业或宏观分析主题。
2.  **匹配框架**：在路由表中找到对应的 `.md` 文件并完整读取。
3.  **提炼核心**：从读取的框架中提取该行业的核心驱动因素、关键指标（如：开工率、库存、政策周期等）和商业模式。
4.  **结合现状（可选）**：如果用户提供了当前市场的具体数据或特定公司的财报，将数据带入框架进行解读。
5.  **输出报告**：按照逻辑清晰的层级（如：宏观环境 -> 行业供需 -> 产业链价值分布 -> 投资策略建议）向用户输出分析结果。
