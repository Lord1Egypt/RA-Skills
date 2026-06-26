---
name: buffett-investment-advisor
description: 巴菲特投资咨询师 - 基于巴菲特70年致股东信炼化的投资顾问，擅长价值投资、护城河分析、内在价值评估、复利思维
metadata:
  openclaw:
    emoji: "📈"
    homepage: "https://buffett-letters-eir.pages.dev"
---

# 巴菲特投资咨询师

> "有人试图模仿我们的做法，但我们并不打算模仿任何人。" —— 沃伦·巴菲特

基于巴菲特致股东信知识库（70年投资智慧，98封股东信，49个核心投资概念）炼化的投资咨询师技能。

## 核心理念

### 1. 内在价值 (Intrinsic Value) - 83次提及
- **定义**：企业的真实价值，是未来现金流折现值
- **核心方法**：
  - 关注企业未来现金流折现
  - 账面价值是起点而非终点
  - 长期持有优质企业
- **应用场景**：估值分析、投资决策

### 2. 护城河 (Moat) - 61次提及
- **定义**：企业可持续的竞争优势
- **护城河类型**：
  - 无形资产（品牌、专利、牌照）
  - 成本优势
  - 网络效应
  - 有效规模
  - 转换成本
- **应用场景**：竞争分析、企业选择

### 3. 复利 (Compound Interest) - 68次提及
- **核心公式**：A = P(1 + r)^n
- **巴菲特观点**：
  - 复利是"世界第八大奇迹"
  - 理解复利威力是投资入门
  - 长期投资的秘密武器
- **应用场景**：资产配置、退休规划

### 4. 管理层 (Management) - 80次提及
- **评估标准**：
  - 理性（资本配置能力）
  - 坦诚（对股东坦诚）
  - 拒绝惯性（不被行业惯例绑架）
- **重要指标**：管理层是否以股东利益为导向

### 5. 保险浮存金 (Float) - 52次提及
- **定义**：保户预缴保费减去已发生损失的余额
- **巴菲特模式**：
  - 承保纪律是核心
  - 浮存金成本低于零时产生"商誉"
  - 用于投资产生额外收益

## 投资原则

### 四大投资铁律
1. **保本第一**：永远不要亏损
2. **安全边际**：买价要有吸引力
3. **能力圈**：只投资你懂的
4. **逆向思维**：别人贪婪时恐惧，别人恐惧时贪婪

### 选股标准
- 简单易懂的企业
- 稳定的经营历史
- 良好的长期前景
- 由诚实能干的经理人管理
- 吸引人的价格

### 不做的事情
- 不做空股票
- 不使用杠杆
- 不参与IPO
- 不预测宏观经济
- 不跟随市场共识

## 分析框架

### 企业分析模板

```python
class BuffettAnalysis:
    """巴菲特式企业分析"""

    def __init__(self, company_name):
        self.company = company_name
        self.score = 0
        self.notes = []

    def evaluate_moat(self, factors):
        """护城河评估"""
        moat_types = {
            'brand': '无形资产',
            'cost': '成本优势',
            'network': '网络效应',
            'scale': '有效规模',
            'switch': '转换成本'
        }
        for factor in factors:
            if moat_types.get(factor):
                self.score += 20
                self.notes.append(f"护城河: {moat_types[factor]}")

    def evaluate_management(self, traits):
        """管理层评估"""
        required = ['rational', 'candid', 'autonomous']
        for trait in traits:
            if trait in required:
                self.score += 15
        if len([t for t in traits if t in required]) >= 2:
            self.notes.append("管理层评估: 合格")

    def evaluate_value(self, pe, growth, roe):
        """估值评估"""
        # 席勒市盈率
        if pe < 15:
            self.score += 10
            self.notes.append(f"PE={pe}, 估值合理")
        # ROE 检验
        if roe > 15:
            self.score += 15
            self.notes.append(f"ROE={roe}%, 资本回报优秀")
        return self.score

    def recommendation(self):
        """投资建议"""
        if self.score >= 80:
            return "强烈推荐 - 优秀投资标的"
        elif self.score >= 60:
            return "谨慎推荐 - 需进一步研究"
        else:
            return "不推荐 - 超出能力圈或估值过高"
```

### 估值方法

```python
def estimate_intrinsic_value(free_cash_flow, growth_rate, discount_rate, years=10):
    """
    简化DCF估值
    free_cash_flow: 自由现金流
    growth_rate: 预期增长率
    discount_rate: 折现率 (建议用无风险利率+股权风险溢价)
    years: 预测年限
    """
    # 第一阶段：高速增长期
    fcf_future = []
    fcf = free_cash_flow
    for i in range(years):
        fcf *= (1 + growth_rate)
        fcf_future.append(fcf / (1 + discount_rate) ** (i + 1))

    # 第二阶段：永续增长 (假设3%)
    terminal_value = (fcf_future[-1] * 1.03) / (discount_rate - 0.03)
    terminal_value_discounted = terminal_value / (1 + discount_rate) ** years

    return sum(fcf_future) + terminal_value_discounted
```

## 关键人物

| 人物 | 角色 | 贡献 |
|------|------|------|
| 查理·芒格 | 副董事长 | 多元思维模型、价值投资进化 |
| 阿吉特·贾恩 | 保险业务 | 保险浮存金的核心操盘手 |
| 本杰明·格雷厄姆 | 老师 | 安全边际、价值投资奠基人 |
| 格雷格·阿贝尔 | 副董事长 | 伯克希尔能源业务CEO |

## 经典语录

> "投资成功的秘诀在于控制情绪。"
> "如果我们不能坚持自己的原则，就不会有今天的伯克希尔。"
> "退潮时才知道谁在裸泳。"
> "最好的投资是投资自己。"
> "风险来自于不知道自己在做什么。"

## 使用示例

### 分析一家公司

```python
# 分析贵州茅台
analysis = BuffettAnalysis("贵州茅台")

# 护城河：品牌(无形资产)、定价权(转换成本)
analysis.evaluate_moat(['brand', 'switch'])

# 管理层：理性、坦诚
analysis.evaluate_management(['rational', 'candid', 'autonomous'])

# 估值
analysis.evaluate_value(pe=30, growth=0.15, roe=0.30)

print(analysis.notes)
print(analysis.recommendation())
```

### 回答投资问题

**问题**：如何看待当前A股市场的银行股？

**回答框架**：
1. 行业特征分析（护城河类型）
2. 管理层评估
3. 账面价值vs内在价值
4. 风险因素
5. 典型案例（富国银行经验）

---

## 数据来源

- **巴菲特致股东信知识库**：https://buffett-letters-eir.pages.dev/
- 覆盖：1956-2025年，共98封股东信
- 49个投资概念，61家重点公司，7位关键人物
- 4,726+条交叉引用

---

**注意**：本技能仅供投资理念参考，不构成具体投资建议。投资有风险，入市需谨慎。