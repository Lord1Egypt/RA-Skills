# DCF 估值工具 (dcf-valuation-skill)

十年DCF估值 AI Agent Skill，支持**传统DCF（Gordon永续模型）**和**段永平式PE退出法**两种估值方法并行计算。

---

## 功能特性

- **双模式并行**：同时输出传统DCF和段永平式PE退出法结果
- **三情景分析**：保守 / 中性 / 乐观三种假设
- **定性+定量**：内置完整的公司定性问题框架（商业模式四问、行业周期判断、财务质量检查）
- **自动文件生成**：分析结果自动保存为 Markdown 文件
- **飞书集成**：可选同步到飞书云文档（需配置 folder_token）

---

## 适用场景

当用户提到以下关键词时触发本 Skill：
> 估算DCF、DCF估值、内在价值、十年估值、自由现金流折现、PE退出、段永平式估值

**适合分析的公司类型：**
- ✅ 高确定性、高分红优质企业（茅台、片仔癀、长江电力）
- ✅ 成熟稳定、现金流可预测的龙头
- ✅ 周期型公司（需配合行业周期判断）

**慎用的公司类型：**
- ⚠️ 严重亏损或无现金流公司（DCF参数极难设定）
- ⚠️ 强周期且当前处于周期底部（净利率中枢难以判断）

---

## 安装方式

### 方式一：克隆 GitHub 仓库

```bash
# 克隆仓库
git clone https://github.com/ianzheng001/dcf-valuation-skill.git

# 复制到 Agent skills 目录
cp -r dcf-valuation-skill ~/.agents/skills/dcf

# 重启 Agent 即可生效
openclaw gateway restart
```

### 方式二：从 .skill 文件安装

```bash
openclaw skills install ./dcf-valuation-skill/dcf-valuation.skill
```

### 方式三：从 clawhub.ai 安装（推荐）

```bash
openclaw skills install dcf-valuation-skill
```

### 方式四：从 Claude Code 安装

[Claude Code](https://github.com/anthropics/claude-code) 的 skill 安装方式：

```bash
# 克隆仓库到 Claude Code 的 skills 目录
mkdir -p ~/.claude-agents/skills
cd ~/.claude-agents/skills
git clone https://github.com/ianzheng001/dcf-valuation-skill.git dcf

# 重启 Claude Code 即可生效
```

---

## 使用方法

### 在对话中触发

直接告诉 Agent 公司名即可：

```
/dcf 帮我估算泸州老窖的内在价值
/dcf 贵州茅台
/dcf 分析贝泰妮的十年估值
```

## 核心参数说明

### 传统DCF 参数

| 参数 | 说明 | 建议值 |
|------|------|--------|
| `base_revenue` | 基准年营收（亿） | 最新年报数据 |
| `base_profit` | 基准年净利润（亿） | 最新年报数据 |
| `net_cash` | 净现金 = 货币资金 - 有息负债 | 最新财报 |
| `total_shares` | 总股本（亿股） | F10 数据 |
| `discount_rate` | 折现率（保守9-10%，中性8-9%，乐观7-8%） | 含股权风险溢价 |
| `terminal_growth` | 永续增长率（3-4%） | 不宜高于GDP增速太多 |
| `fcf_ratio` | FCF/净利润 比例 | 资本开支大的公司取值更低 |

### 段永平式PE退出法 参数

| 参数 | 说明 | 建议值 |
|------|------|--------|
| `profit_growth` | 未来10年净利润增速数组 | 根据行业判断 |
| `exit_pe` | 10年后给多少倍PE | 保守15x，中性20x，乐观25x |
| `discount_rate` | 机会成本折现率 | 1.5%（国债利率）或3%（稳健） |
| `dividend_ratio` | 分红比例 | 高分红公司取70-80% |

---

## 两种方法对比

| | 传统DCF | 段永平PE退出法 |
|---|---------|---------------|
| **折现率** | 7-10%（含股权风险溢价） | 1.5-3%（机会成本） |
| **终值处理** | Gordon永续（占总价值60-80%） | 10年后净利润×PE（可控） |
| **本质** | 数学模型 | 商业判断 |
| **适合企业** | 任何企业 | 高确定性+稳定分红 |
| **风险** | 永续增长率微调导致结果剧变 | 10年增速+PE主观 |

---

## 定性分析框架

分析一家公司时，回答四个核心问题：

### 1. 商业模式（这钱是怎么赚的？）
- 核心收入来源是什么？一次性还是持续性的？
- **提价权**：能否在不丢失客户的情况下提价？
- **扩张成本**：想赚更多钱需要投入多少额外资本？

### 2. 行业空间（天花板在哪里？）
- 行业总规模多大？增速多少？
- 渗透率处于什么阶段？（早期/中期/后期）

### 3. 竞争格局（谁赢谁输？）
- 主要竞争对手是谁？各自优劣势？
- 行业集中度在提升还是下降？

### 4. 财务质量（钱是否真实？）
- 经营现金流/净利润 > 80%？
- 净现金是否为正？

---

## 输出示例

分析完成后，输出包含：

**定性综合判断**：星级评分 + 一句话总结

**传统DCF三情景**：内在价值、每股价值、市值/内在价值比

**段永平PE退出三情景**：内在价值、10年后净利润、隐含年化回报

**综合判断**：两种方法对照、安全边际、主要风险

---

## 项目结构

```
dcf-valuation-skill/
├── SKILL.md                    # Agent Skill 核心文件
├── dcf-valuation.skill         # 打包后的分发文件
├── references/
│   └── qualitative.md          # 定性分析完整框架
└── scripts/
    └── dcf_calc.py            # DCF计算脚本
```

---

## 数据来源要求

> ⚠️ **重要**：必须使用最新年报数据
>
> 分析前会校验数据时效性，若发现已有旧报告使用了更旧的年份，会提示数据已过时。

推荐数据获取渠道：
- 东方财富 F10（`emweb.securities.eastmoney.com`）
- 新浪财经（`finance.sina.com.cn`）
- 公司最新年报（巨潮资讯网）

---

## 免责声明

DCF 估值结果仅供参考，不构成投资建议。

估值参数（折现率、增速、净利率中枢等）均为主观假设，不同参数会导致结果差异巨大。

投资决策请咨询专业投资顾问。

---

## 贡献与反馈

- GitHub Issues: https://github.com/ianzheng001/dcf-valuation-skill/issues
- 欢迎提交 PR 改进分析框架或修复计算逻辑

---

## License

MIT License