---
name: community-group-buying-supply-chain
description: 社区团购供应链与采购管理全链路技能包。涵盖供应商开发、资质审核、评分卡、采购谈判、仓储管理、配送履约及配套工具。适用于平台采购负责人、供应链管理者。
version: 1.0.0
created_at: 2026-04-14
license: MIT
github_url: null
---

# 模块四：供应链与采购

> **模块边界说明**
> 本模块聚焦"货从哪来"，即供应商开发、采购谈判、仓储管理、物流配送。
> 选品决策 → 模块一（选品策略）
> 团长运营 → 模块二（团长运营）
> 获客留存 → 模块三（获客与留存）
> 营销促销 → 模块六（营销与促销）
> 各模块边界独立，不重叠。

---

## 知识库

### 4.1 供应链在社区团购中的核心地位

```
社区团购的竞争，本质是供应链的竞争：

  美团优选 → 美团配送体系支撑
  多多买菜 → 拼多多农产品供应链支撑
  兴盛优选 → 湖南本地供应链支撑

没有供应链优势，一切获客/运营手段都是空中楼阁。

供应链三大核心指标：
  1. 成本：进价 vs 市场价，差距越大利润空间越大
  2. 稳定：能不能持续供货，断货是最大风险
  3. 品质：货质量稳定，不出食品安全事故
```

---

### 4.2 供应商分级体系

供应商按贡献和稳定性分为四级，每级有明确量化指标：

```
供应商分级量化标准：

┌─────────────────────────────────────────────────────────────────────────────┐
│  级别    占比      月供货额      准时率      损耗率      账期      管理      │
│ ─────────────────────────────────────────────────────────────────────       │
│  S级    5-10%    ≥ ¥100万     ≥ 98%      ≤ 5%       T+14     月度战略会  │
│  A级    15-20%   ¥30-100万    ≥ 95%      ≤ 8%       T+7      季度Review  │
│  B级    50-60%   ¥5-30万      ≥ 90%      ≤ 12%      单次结   月度数据审 │
│  C级    10-15%   < ¥5万       ≥ 85%      ≤ 15%      现结     单次评估   │
└─────────────────────────────────────────────────────────────────────────────┘

---

S级：战略供应商
  → 占比：5-10%（每品类保留1-2个）
  → 核心指标：月供货额 ≥ ¥100万，准时率 ≥ 98%，损耗率 ≤ 5%
  → 特征：独家合作/产地直采/品牌联名，有行业稀缺性
  → 待遇：账期优先（T+14）/ 专人对接 / 联合营销基金
  → 管理：月度战略会议，共同制定季度销售计划，优先新品首发

A级：核心供应商
  → 占比：15-20%
  → 核心指标：月供货额 ¥30-100万，准时率 ≥ 95%，损耗率 ≤ 8%
  → 特征：稳定供货 / 质量合格 / 价格有竞争优势
  → 待遇：账期正常（T+7）/ 标准对接 / 营销资源倾斜
  → 管理：季度 Review，S/A级供应商占比目标 20-30%，末尾10%降级或淘汰

B级：常规供应商
  → 占比：50-60%（平台主力层）
  → 核心指标：月供货额 ¥5-30万，准时率 ≥ 90%，损耗率 ≤ 12%
  → 特征：按需供货 / 配合度高 / 品类常见
  → 待遇：单次结算 / 平台规则统一约束
  → 管理：月度数据Review，连续2个季度不达标降为C级

C级：应急供应商
  → 占比：10-15%
  → 核心指标：月供货额 < ¥5万，准时率 ≥ 85%，损耗率 ≤ 15%
  → 特征：临时补货 / 季节性商品 / 新品测试供应商
  → 待遇：现结（无账期）/ 无优先权
  → 管理：单次合作评估，试销通过可升级B级

---

升级路径：
  C级 → B级：连续2个季度月供货额 ≥ ¥5万 + 准时率 ≥ 90% → 自动升级
  B级 → A级：年供货额累计 ≥ ¥300万 + 准时率 ≥ 95% + 损耗率 ≤ 8% → 采购决策会评审
  A级 → S级：年供货额累计 ≥ ¥1000万 + 战略价值评估 → 高管战略会审定
```

---

### 4.3 采购定价策略

```
采购定价三角：

        供货价
        （供应商）
           △
           │
     市场价 ─┴─ 账期

理想状态：供货价 < 市场价 30% + 账期 ≥ T+7

---

定价策略（三种）：

策略1：源头直采（成本最低）
  → 产地合作社/工厂直接谈，跳过中间商
  → 适合：大宗农产品（蔬菜/水果/肉类）
  → 成本优势：15-40%

策略2：产地批发（成本适中）
  → 产地批发市场集中采购
  → 适合：季节性商品（粽子/月饼/年货）
  → 成本优势：10-25%

策略3：品牌经销商（成本较高）
  → 通过区域经销商拿货
  → 适合：标品（饮料/零食/日用品）
  → 成本优势：5-15%，但品质稳定
```

#### 定价策略场景化应用

| 品类 | 推荐策略 | 核心要点 | 议价优先级 |
|------|---------|---------|-----------|
| 大宗农产品（叶菜/茄果） | 源头直采 | 锁定合作社，签长期框架协议 | 供货价 > 账期 |
| 季节性农产品（草莓/樱桃） | 产地批发 | 提前锁货，分批交货降低风险 | 损耗责任 > 价格 |
| 品牌标品（饮料/方便面） | 品牌经销商 | 拿区域独家，经销商返点谈返利 | 账期 + 返点 |
| 白牌标品（纸巾/日化） | 1688工厂 | 按单采购，MOQ从低开始测试 | 价格 > MOQ |
| 进口商品 | 口岸进口商 | 批量采购谈折扣，账期45天内 | 资金占用成本 |

#### 各平台账期参考

| 平台 | 账期 | 说明 |
|------|------|------|
| 美团优选 | T+7 至 T+14 | 账期最长，但规则严，罚款多 |
| 多多买菜 | T+5 至 T+10 | 账期短，供应商需谨慎让利 |
| 兴盛优选 | T+7 | 账期稳定，供应商信任度高，愿意让利 8-12% |
| 淘菜菜 | T+7 至 T+10 | 中等账期，考核准时交货率 |

---

### 4.4 供应商议价技巧

```
供应商谈判三步法：

第一步：摸底（不先开口）
  → 让供应商先报价，摸清对方底价
  → 了解供应商当前库存积压情况（急于出货 = 可压价）
  → 询问其他平台合作价格（货比三家）

第二步：压价（有理有据）
  → 出示竞品报价（最低价参考）
  → 承诺采购量换取折扣（量换价原则）
  → 账期换价格：接受更短账期 → 换取更低供货价
    例：T+14 → T+7，价格可降 2-3%

第三步：锁定（落袋为安）
  → 合同写明价格有效期（避免随行就市涨价）
  → 谈最惠客户条款：若给其他平台更低价格，需同步给本平台
  → 谈保底采购量：若承诺月销10万，供应商需给最优惠价格

压价目标参考（vs 市场价）：
  农产品源头直采：25-40%
  农产品批发：15-25%
  白牌标品：15-20%
  品牌标品：5-12%
  账期压缩换价：每压缩7天，价格可降1-2%
```

---

### 4.5 各平台供应链对比

#### 美团优选
```
供应链模式：平台主导型
核心特点：
  → 平台统一采购，供应商只管送货到仓
  → 自有配送体系（美团配送）降低物流成本
  → 供应商话语权弱，平台规则严

供应商结构：
  → 全国性供应商：占 60%（统一采购）
  → 区域性供应商：占 30%（区域补货）
  → 独家供应商：占 10%（差异化商品）

账期：T+7 至 T+14（行业较长）
核心优势：配送体系成熟，损耗率低（5-7%）
```

#### 多多买菜
```
供应链模式：农产品上行型
核心特点：
  → 聚焦农产品，产地直采比例高（40%+）
  → 供应商门槛低，白牌供应商为主
  → 平台规模大，议价能力强

供应商结构：
  → 产地合作社：占 40%（农产品）
  → 白牌工厂：占 35%（标品）
  → 品牌商：占 25%（少量）

账期：T+5 至 T+10（相对较短）
核心优势：农产品价格极低，但损耗率偏高（7-10%）
```

#### 兴盛优选
```
供应链模式：区域深耕型
核心特点：
  → 供应商本地化，减少长途运输
  → 区域小型工厂/合作社为主
  → 供应链稳定，不受全国波动影响

供应商结构：
  → 本地供应商：占 65%（本地小型工厂/合作社）
  → 区域品牌商：占 25%
  → 全国供应商：占 10%（补充品）

账期：T+7（稳定，供应商信任度高）
核心优势：损耗率最低（4-6%），供应链本地化
```

---

## 方法论

### 4.6 供应商开发 SOP

```
供应商开发五步法：

Step 1：源头锁定
  ┌─────────────────────────────────────────────┐
  │  品类          优先渠道                       │
  │  ─────────────────────────────────          │
  │  农产品        一亩田 / 惠农网 / 产地合作社    │
  │  食品标品      1688工厂店 / 糖酒会 / 中食展   │
  │  品牌商品      区域经销商 / 品牌方直接对接      │
  │  进口商品      口岸进口商 / 跨境供应链          │
  └─────────────────────────────────────────────┘

Step 2：资质审核（必须全部通过）

  必要资质（缺一不可）：
  ├── 营业执照（有效期内）
  ├── 食品经营许可证（预包装/散装/生产许可证）
  ├── 产品检测报告（近3个月内，批批检测）
  ├── 商标注册证或授权书（品牌商品必须）
  └── 法人身份证

  加分资质：
  ├── ISO 9001（质量管理）
  ├── ISO 22000（食品安全管理）
  ├── 绿色/有机食品认证
  └── 出口食品备案

  ⚠️ 注意：资质造假 = 直接永久黑名单，报警处理

Step 3：样品测试
  → 要求提供 3-5 件样品
  → 评估维度：
  │   外观（颜色/大小/完整度）
  │   口感（生鲜必须试吃）
  │   包装（是否适合配送/保质期）
  │   性价比（ vs 市场同类品）

Step 4：商务谈判
  核心条款：
  ├── 进价：目标低于市场价 20%+
  ├── 账期：目标 T+7 以上
  ├── MOQ：最低起订量，越低越好
  ├── 退换货：滞销品/尾货处理机制
  ├── 营销分摊：爆品推广费用谁出
  └── 独家：差异化商品是否愿意独家

Step 5：合同签署
  合同必须包含：
  ├── 商品清单 + 价格表（有效期明确）
  ├── 质量标准（外观/口感/包装/检测要求）
  ├── 交货地点/时间/验收标准
  ├── 付款账期和方式
  ├── 质量保证 + 违约金条款
  ├── 退换货处理流程
  └── 违约责任界定

  合同有效期：通常 3-6 个月，到期重新谈判
```

---

### 4.7 供应商评分卡（正式版）

供应商评估五维度（总分100分）：

| 维度 | 权重 | 评估要点 |
|------|------|---------|
| 价格竞争力 | 25% | 进价 vs 市场价、MOQ灵活度、账期接受度 |
| 质量稳定性 | 25% | 来料合格率、抽检通过率、资质齐全度 |
| 交货能力 | 20% | 准时交货率、交货速度、缺货处理 |
| 服务配合 | 15% | 响应速度、投诉处理、退换货配合 |
| 合作意愿 | 15% | 配合积极性、营销支持、独家合作可能 |

评级标准：

| 评级 | 总分区间 | 管理策略 |
|------|---------|---------|
| S | ≥ 90 | 战略合作，优先供货，专人对接 |
| A | 80-89 | 核心合作，标准管理，季度Review |
| B | 70-79 | 常规合作，月度数据Review |
| C | 60-69 | 观察合作，连续2个C则降级或淘汰 |
| D | < 60 | 淘汰，6个月内不合作 |

---

### 4.8 仓储管理体系

```
仓储模式选择：

中心仓模式（CDC）：
  → 全国/区域设大仓，供应商送货到大仓
  → 平台负责分拣 → 网格仓 → 团长自提点
  优点：规模化成本低，适合标准化商品
  缺点：层级多，损耗和时效难控

前置仓模式（PC）：
  → 大仓分拨到各社区前置仓
  → 覆盖 3-5 公里范围，当日达
  优点：时效快，用户体验好
  缺点：成本高，需要密集覆盖

店仓一体：
  → 团长店面既是销售点又是仓储点
  → 用户下单 → 团长从店内取货
  优点：零额外仓储成本，适合小社区
  缺点：品类受限，库存有限

各平台仓储模式：
  美团优选：中心仓 + 网格仓（2级），次日达
  多多买菜：中心仓直发（1级），次日达
  兴盛优选：区域仓 + 自提点（2级），部分当日达
  淘菜菜：中心仓 + 前置仓（2级），当日达为主
```

#### 仓储损耗控制

```
损耗控制关键节点：

节点1：入库验收（减少 2-3% 损耗）
  → 抽检比例：批次 > 100件抽 10%，< 100件抽 5%
  → 外观不合格品当场退换，不入库

节点2：分拣包装（减少 1-2% 损耗）
  → 分拣人员培训标准化，减少人为损耗
  → 包装材料：抗压纸箱 + 保鲜膜（生鲜）

节点3：在库管理（减少 1-2% 损耗）
  → 遵循"先进先出"原则
  → 临期品：提前 3 天预警，优先推送销售
  → 温控：生鲜冷藏 0-4℃，冻品 <-18℃

节点4：出库配送（减少 1-2% 损耗）
  → 配送路径优化，减少搬运次数
  → 到团长时间：生鲜 < 24小时，标品 < 48小时

行业损耗率参考：
  蔬菜品类：5-8%（优秀） / 8-12%（一般）
  水果品类：3-6%（优秀） / 6-10%（一般）
  肉禽水产：2-5%（优秀） / 5-8%（一般）
  标品（包装食品）：<1%
```

---

## 工具集

### Tool 1: 供应商评分卡（完整版）

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
供应商评分卡（完整版）
五维度评估：价格竞争力 / 质量稳定性 / 交货能力 / 服务配合 / 合作意愿
输出：S/A/B/C/D 五级评级 + 改进建议 + 历史评分追踪
"""

from dataclasses import dataclass, field
from typing import List, Dict
import json
from datetime import datetime


@dataclass
class SupplierEvaluation:
    """供应商评估数据"""
    name: str
    category: str  # 品类

    # 价格竞争力（25分）
    price_advantage: float = 0.0    # 相对市场价优势 0-10
    moq_flexibility: float = 0.0    # MOQ灵活度 0-5
    payment_terms: float = 0.0      # 账期接受度 0-10

    # 质量稳定性（25分）
    quality_consistency: float = 0.0  # 来料合格率 0-10
    inspection_pass_rate: float = 0.0  # 抽检通过率 0-10
    cert_completeness: float = 0.0  # 资质齐全度 0-5

    # 交货能力（20分）
    on_time_delivery: float = 0.0  # 准时交货率 0-10
    delivery_speed: float = 0.0    # 交货速度 0-5
    shortage_handling: float = 0.0  # 缺货处理 0-5

    # 服务配合（15分）
    response_speed: float = 0.0    # 响应速度 0-5
    complaint_handling: float = 0.0  # 投诉处理 0-5
    return_cooperation: float = 0.0  # 退换货配合 0-5

    # 合作意愿（15分）
    cooperation_enthusiasm: float = 0.0  # 配合积极性 0-5
    marketing_support: float = 0.0   # 营销支持 0-5
    exclusivity_potential: float = 0.0  # 独家合作潜力 0-5

    # 历史记录
    history: List[Dict] = field(default_factory=list)

    def calculate_scores(self) -> Dict:
        """计算各维度得分和总分"""
        price_score = (
            (self.price_advantage / 10) * 15 +
            (self.moq_flexibility / 5) * 5 +
            (self.payment_terms / 10) * 5
        )

        quality_score = (
            self.quality_consistency * 2.5 +
            self.inspection_pass_rate * 1.0 +
            self.cert_completeness * 1.0
        )

        delivery_score = (
            self.on_time_delivery * 2.0 +
            self.delivery_speed * 1.0 +
            self.shortage_handling * 1.0
        )

        service_score = (
            self.response_speed * 1.0 +
            self.complaint_handling * 1.0 +
            self.return_cooperation * 1.0
        )

        willingness_score = (
            self.cooperation_enthusiasm * 1.0 +
            self.marketing_support * 1.0 +
            self.exclusivity_potential * 1.0
        )

        total = price_score + quality_score + delivery_score + service_score + willingness_score

        return {
            "价格竞争力（25分）": round(price_score, 1),
            "质量稳定性（25分）": round(quality_score, 1),
            "交货能力（20分）": round(delivery_score, 1),
            "服务配合（15分）": round(service_score, 1),
            "合作意愿（15分）": round(willingness_score, 1),
            "总分（100分）": round(total, 1),
        }

    def get_grade(self) -> str:
        """评级"""
        scores = self.calculate_scores()
        total = scores["总分（100分）"]
        if total >= 90:
            return "S"
        elif total >= 80:
            return "A"
        elif total >= 70:
            return "B"
        elif total >= 60:
            return "C"
        else:
            return "D"

    def get_improvement_suggestions(self) -> List[str]:
        """生成改进建议"""
        suggestions = []
        checks = [
            ("价格竞争力", self.price_advantage, 10, "价格优势"),
            ("MOQ灵活度", self.moq_flexibility, 5, "MOQ"),
            ("账期接受度", self.payment_terms, 10, "账期"),
            ("质量稳定性", self.quality_consistency, 10, "质量"),
            ("来料合格率", self.inspection_pass_rate, 10, "合格率"),
            ("资质齐全度", self.cert_completeness, 5, "资质"),
            ("准时交货率", self.on_time_delivery, 10, "交货"),
            ("交货速度", self.delivery_speed, 5, "速度"),
            ("缺货处理", self.shortage_handling, 5, "缺货"),
            ("响应速度", self.response_speed, 5, "响应"),
            ("投诉处理", self.complaint_handling, 5, "投诉"),
            ("退换货配合", self.return_cooperation, 5, "退换"),
            ("配合积极性", self.cooperation_enthusiasm, 5, "积极性"),
            ("营销支持", self.marketing_support, 5, "营销"),
            ("独家合作潜力", self.exclusivity_potential, 5, "独家"),
        ]

        for name, score, max_score, label in checks:
            pct = score / max_score
            if pct < 0.5:
                suggestions.append(f"[WARNING] {name}：{score}/{max_score}，需重点改进（<50%）")
            elif pct >= 0.9:
                suggestions.append(f"[OK] {name}：{score}/{max_score}，优秀（>90%）")

        return suggestions

    def to_dict(self, include_suggestions: bool = True) -> Dict:
        scores = self.calculate_scores()
        result = {
            "供应商名称": self.name,
            "品类": self.category,
            "评级": self.get_grade(),
            "总分": f"{scores['总分（100分）']}/100",
            "维度得分": {
                k: f"{v}/权重满分"
                for k, v in scores.items()
            },
            "详细得分": {
                "价格竞争力（25分）": scores["价格竞争力（25分）"],
                "质量稳定性（25分）": scores["质量稳定性（25分）"],
                "交货能力（20分）": scores["交货能力（20分）"],
                "服务配合（15分）": scores["服务配合（15分）"],
                "合作意愿（15分）": scores["合作意愿（15分）"],
            },
        }
        if include_suggestions:
            result["改进建议"] = self.get_improvement_suggestions()
        return result


def compare_suppliers(suppliers: List[SupplierEvaluation]) -> List[Dict]:
    """供应商横向对比排序"""
    results = []
    for s in suppliers:
        d = s.to_dict(include_suggestions=False)
        d["总分数值"] = float(d["总分"].split("/")[0])
        d["评级"] = s.get_grade()
        results.append(d)

    results.sort(key=lambda x: x["总分数值"], reverse=True)

    for i, r in enumerate(results):
        r["排名"] = i + 1
        r.pop("总分数值", None)

    return results


def run():
    print("=" * 60)
    print("供应商评分卡")
    print("=" * 60)

    name = input("供应商名称：").strip() or "测试供应商"
    category = input("品类：").strip() or "时令水果"

    print("\n--- 价格竞争力（25分）---")
    try:
        pa = float(input("  价格优势（0-10）：").strip() or "7")
    except ValueError:
        pa = 7
    try:
        moq = float(input("  MOQ灵活度（0-5）：").strip() or "3")
    except ValueError:
        moq = 3
    try:
        pt = float(input("  账期接受度（0-10）：").strip() or "6")
    except ValueError:
        pt = 6

    print("\n--- 质量稳定性（25分）---")
    try:
        qc = float(input("  质量稳定性（0-10）：").strip() or "8")
    except ValueError:
        qc = 8
    try:
        ip = float(input("  来料合格率（0-10）：").strip() or "8")
    except ValueError:
        ip = 8
    try:
        cc = float(input("  资质齐全度（0-5）：").strip() or "4")
    except ValueError:
        cc = 4

    print("\n--- 交货能力（20分）---")
    try:
        otd = float(input("  准时交货率（0-10）：").strip() or "8")
    except ValueError:
        otd = 8
    try:
        ds = float(input("  交货速度（0-5）：").strip() or "4")
    except ValueError:
        ds = 4
    try:
        sh = float(input("  缺货处理（0-5）：").strip() or "3")
    except ValueError:
        sh = 3

    print("\n--- 服务配合（15分）---")
    try:
        rs = float(input("  响应速度（0-5）：").strip() or "4")
    except ValueError:
        rs = 4
    try:
        ch = float(input("  投诉处理（0-5）：").strip() or "3")
    except ValueError:
        ch = 3
    try:
        rc = float(input("  退换货配合（0-5）：").strip() or "3")
    except ValueError:
        rc = 3

    print("\n--- 合作意愿（15分）---")
    try:
        ce = float(input("  配合积极性（0-5）：").strip() or "4")
    except ValueError:
        ce = 4
    try:
        ms = float(input("  营销支持（0-5）：").strip() or "2")
    except ValueError:
        ms = 2
    try:
        ep = float(input("  独家合作潜力（0-5）：").strip() or "3")
    except ValueError:
        ep = 3

    supplier = SupplierEvaluation(
        name=name,
        category=category,
        price_advantage=pa,
        moq_flexibility=moq,
        payment_terms=pt,
        quality_consistency=qc,
        inspection_pass_rate=ip,
        cert_completeness=cc,
        on_time_delivery=otd,
        delivery_speed=ds,
        shortage_handling=sh,
        response_speed=rs,
        complaint_handling=ch,
        return_cooperation=rc,
        cooperation_enthusiasm=ce,
        marketing_support=ms,
        exclusivity_potential=ep,
    )

    result = supplier.to_dict()

    print(f"\n{'='*60}")
    print(f"【{result['供应商名称']}】（{result['品类']}）")
    print(f"评级：{result['评级']}   总分：{result['总分']}")
    print(f"\n各维度得分：")
    for k, v in result["详细得分"].items():
        print(f"  {k}：{v}")

    print(f"\n改进建议：")
    for s in result["改进建议"]:
        print(f"  {s}")


if __name__ == "__main__":
    run()
```

### Tool 2: 采购成本计算器

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
采购成本计算器
输入：供应商报价 + 市场价 + 账期 + 损耗率
输出：真实采购成本 + 利润空间分析
"""


def calculate_procurement_cost(
    supplier_price: float,       # 供应商报价（元）
    market_price: float,         # 市场价（元）
    payment_days: int,           # 账期（天）
    loss_rate: float,            # 损耗率（0-1）
    logistics_cost: float = 0.0,  # 物流成本（元）
    platform_margin: float = 0.15,  # 平台抽佣率
    leader_margin: float = 0.12,   # 团长佣金率
):
    """
    计算真实采购成本和利润空间

    Returns:
        dict: 成本分析报告
    """
    # 基础成本
    base_cost = supplier_price + logistics_cost

    # 损耗摊销
    loss_cost = base_cost * loss_rate

    # 真实成本（加损耗）
    true_cost = base_cost + loss_cost

    # 资金占用成本（账期成本）
    # 年化资金成本按 5% 计算
    daily_financing_rate = 0.05 / 365
    financing_cost = base_cost * daily_financing_rate * payment_days

    # 真实采购成本
    total_procurement_cost = true_cost + financing_cost

    # 价格优势
    price_advantage_pct = (market_price - supplier_price) / market_price * 100

    # 毛利空间
    target_selling_price = market_price * 0.85  # 定价为市场价85%
    gross_profit = target_selling_price - total_procurement_cost
    gross_margin = gross_profit / target_selling_price * 100

    # 盈亏平衡售价
    breakeven = total_procurement_cost / (1 - platform_margin - leader_margin)

    return {
        "基础采购成本": round(base_cost, 2),
        "损耗摊销": round(loss_cost, 2),
        "资金占用成本（账期）": round(financing_cost, 2),
        "真实采购成本": round(total_procurement_cost, 2),
        "价格优势": f"{price_advantage_pct:.1f}%（vs 市场价）",
        "目标售价（市场价85%）": round(target_selling_price, 2),
        "毛利空间": round(gross_profit, 2),
        "毛利率": f"{gross_margin:.1f}%",
        "盈亏平衡售价": round(breakeven, 2),
        "是否可行": "✅ 可行" if gross_margin >= 15 else "⚠️ 毛利偏低" if gross_margin >= 10 else "❌ 毛利不足",
    }


def run():
    print("=" * 55)
    print("采购成本计算器")
    print("=" * 55)

    try:
        sp = float(input("供应商报价（元）：").strip() or "8.5")
    except ValueError:
        sp = 8.5

    try:
        mp = float(input("市场价（元）：").strip() or "12.0")
    except ValueError:
        mp = 12.0

    try:
        days = int(input("账期（天）：").strip() or "7")
    except ValueError:
        days = 7

    try:
        loss = float(input("损耗率（如 0.05 表示 5%）：").strip() or "0.06")
    except ValueError:
        loss = 0.06

    try:
        logistics = float(input("物流成本（元，可直接回车跳过）：").strip() or "0")
    except ValueError:
        logistics = 0

    result = calculate_procurement_cost(sp, mp, days, loss, logistics)

    print(f"\n{'='*55}")
    print("采购成本分析报告")
    print(f"{'='*55}")

    print(f"\n成本明细：")
    print(f"  基础采购成本：{result['基础采购成本']:.2f} 元")
    print(f"  损耗摊销：{result['损耗摊销']:.2f} 元")
    print(f"  资金占用成本：{result['资金占用成本（账期）']:.2f} 元")
    print(f"  真实采购成本：{result['真实采购成本']:.2f} 元")

    print(f"\n利润分析：")
    print(f"  {result['价格优势']}")
    print(f"  目标售价（85折）：{result['目标售价（市场价85%）']:.2f} 元")
    print(f"  毛利空间：{result['毛利空间']:.2f} 元")
    print(f"  毛利率：{result['毛利率']}")
    print(f"  盈亏平衡售价：{result['盈亏平衡售价']:.2f} 元")
    print(f"\n结论：{result['是否可行']}")


if __name__ == "__main__":
    run()
```

### Tool 3: 库存周转分析器

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
库存周转分析器
输入：SKU库存数据 + 销售数据
输出：周转天数/呆滞品预警/补货建议
"""


def calculate_turnover_metrics(
    sku: str,
    current_stock: float,      # 当前库存（件/千克）
    daily_avg_sales: float,    # 日均销量
    lead_time: int,            # 补货周期（天）
    min_stock_days: int = 3,  # 最低库存天数（触发补货预警）
    max_stock_days: int = 14,  # 最高库存天数（呆滞预警）
):
    """
    计算库存周转指标

    Returns:
        dict: 周转分析报告
    """
    if daily_avg_sales <= 0:
        return {
            "SKU": sku,
            "当前库存": f"{current_stock:.0f}",
            "日均销量": "0（无销量）",
            "库存天数": "N/A",
            "月周转次数": "N/A",
            "库存状态": "⚠️ 无销量",
            "补货建议": "无销量商品，建议下架或重新推广",
            "补货点": "0 件",
            "安全库存": "0 件",
            "建议补货量": "0 件",
        }

    stock_days = current_stock / daily_avg_sales  # 库存天数
    turnover_rate = 30 / stock_days if stock_days > 0 else float("inf")  # 月周转次数

    # 补货点（ROQ公式简化版）
    reorder_point = daily_avg_sales * lead_time
    safety_stock = daily_avg_sales * min_stock_days
    reorder_quantity = daily_avg_sales * (max_stock_days - min_stock_days)

    # 状态判断
    if stock_days < min_stock_days:
        status = "🔴 紧急补货"
        action = f"立即补货！当前库存仅够 {stock_days:.1f} 天"
    elif stock_days < lead_time:
        status = "🟠 即将断货"
        action = f"需在 {stock_days:.0f} 天内补货，建议量 {reorder_quantity:.0f} 件"
    elif stock_days <= max_stock_days:
        status = "🟢 正常"
        action = f"库存正常，当前库存够用 {stock_days:.1f} 天"
    else:
        status = "🟡 呆滞预警"
        action = f"库存过多（够用 {stock_days:.1f} 天），减少进货，优先清库存"

    return {
        "SKU": sku,
        "当前库存": f"{current_stock:.0f}",
        "日均销量": f"{daily_avg_sales:.1f}",
        "库存天数": f"{stock_days:.1f} 天",
        "月周转次数": f"{turnover_rate:.1f} 次",
        "库存状态": status,
        "补货建议": action,
        "补货点": f"{reorder_point:.0f} 件",
        "安全库存": f"{safety_stock:.0f} 件",
        "建议补货量": f"{reorder_quantity:.0f} 件",
    }


def batch_analysis(data: list):
    """批量分析多个SKU"""
    results = []
    for item in data:
        r = calculate_turnover_metrics(**item)
        results.append(r)

    # 分类统计
    status_count = {"紧急补货": 0, "即将断货": 0, "正常": 0, "呆滞预警": 0, "无销量": 0}
    for r in results:
        for k in status_count:
            if k in r.get("库存状态", ""):
                status_count[k] += 1

    return {
        "明细": results,
        "汇总": status_count,
        "呆滞品": [r for r in results if "呆滞" in r.get("库存状态", "")],
        "断货预警": [r for r in results if "断货" in r.get("库存状态", "") or "紧急" in r.get("库存状态", "")],
    }


def run():
    print("=" * 55)
    print("库存周转分析器")
    print("=" * 55)

    sku = input("SKU名称：").strip() or "测试SKU"

    try:
        stock = float(input("当前库存（件）：").strip() or "200")
    except ValueError:
        stock = 200

    try:
        sales = float(input("日均销量（件）：").strip() or "30")
    except ValueError:
        sales = 30

    try:
        lead = int(input("补货周期（天）：").strip() or "3")
    except ValueError:
        lead = 3

    result = calculate_turnover_metrics(sku, stock, sales, lead)

    print(f"\n{'='*55}")
    print(f"【{result['SKU']}】库存分析报告")
    print(f"{'='*55}")
    print(f"\n基础数据：")
    print(f"  当前库存：{result['当前库存']} 件")
    print(f"  日均销量：{result['日均销量']} 件/天")
    print(f"  库存天数：{result['库存天数']}")
    print(f"  月周转次数：{result['月周转次数']}")

    print(f"\n状态：{result['库存状态']}")
    print(f"建议：{result['补货建议']}")
    print(f"\n补货参数：")
    print(f"  补货点：{result['补货点']} 件")
    print(f"  安全库存：{result['安全库存']} 件")
    print(f"  建议补货量：{result['建议补货量']} 件")


if __name__ == "__main__":
    run()
```

---

## 案例库

### 案例1：多多买菜农产品供应链损耗控制

```
问题：农产品损耗率高，拖累利润

原因分析：
  1. 包装简陋：田间纸箱直接运输，磕碰损耗大
  2. 链路太长：产地 → 大仓 → 网格仓 → 团长，损耗逐级累积
  3. 分拣粗糙：来不及精细分拣，好坏混装

改进措施：
  1. 产地预冷：蔬菜采摘后 2 小时内入冷库
  2. 标准化包装：托盘+保鲜膜，减少磕碰
  3. 精准订单：减少"卖不完"的浪费

数据对比：
  改进前：损耗率 12-15%
  改进后（2023年）：损耗率 6.5-8%
  节省成本：约节省 2-4% 的 GMV，相当于数千万元
```

### 案例2：兴盛优选本地供应商深度绑定

```
成功点：本地供应商长期合作，供应链极其稳定

具体做法：
  1. 合同一年一签，账期稳定，供应商信任平台
  2. 提前付款：优质供应商可申请预付款（5-10%）
  3. 联合营销：平台出补贴，供应商出折扣，合作推广新品
  4. 技术赋能：给供应商提供库存管理系统（免费）

数据支撑：
  供应商稳定性：95%（年流失率 < 5%）
  准时交货率：98%（行业最高）
  采购成本：比美团低 8-12%（账期更稳定，供应商愿意让利）

核心逻辑：
  → 账期稳定 = 供应商愿意让利
  → 预付款 = 供应商全力配合
  → 数字化赋能 = 供应商效率提升 = 成本下降
```

### 案例3：美团优选中心仓到网格仓的损耗控制

```
成功点：两级仓配体系，平衡成本与效率

体系设计：
  中心仓（CDC）：
  → 接收全国/区域供应商的大批量货物
  → 进行质量抽检、分拣、归类
  → 发往各城市的网格仓

  网格仓（Grid）：
  → 覆盖半径 10-20 公里
  → 从中心仓接收货物，再次分拣
  → 直接配送到团长自提点

数据支撑：
  两级体系 vs 一级体系（直接到团）：
  成本：低 15-20%（规模效应）
  时效：慢 12-24 小时
  损耗：高 2-3%（多一次装卸）
  结论：适合规模化的标准品，生鲜不建议超过两级
```

### 案例4：某平台"伪造有机认证"供应商事故的教训

```
背景：2021年某中型平台（年GMV约2亿）供应商审核漏洞导致事故

事件经过：
  Step 1：供应商入驻
    → 某农业合作社入驻，声称有"有机食品认证"
    → 资质审核时：上传了模糊的证书扫描件
    → 审核人员：仅检查"有证书"，未核实真实性
    → 入驻完成，开始供货

  Step 2：销售扩张
    → 打着"有机蔬菜"旗号，定价高于普通蔬菜 30%
    → 平台默许其使用"有机"标签进行营销
    → 3个月内月销量突破 ¥80 万

  Step 3：东窗事发
    → 监管部门抽查：农药残留超标
    → 进一步调查：该供应商的有机认证已于半年前被吊销
    → 消费者投诉：多位家长反映孩子食用后出现不适

事故处置：
  直接损失：
    → 商品下架 + 召回：约 ¥120 万（含运输/处理）
    → 用户赔偿：约 ¥85 万（含医疗费/退款）
    → 监管罚款：¥200 万 + 整改通知
    → 平台声誉：百度搜索指数下跌 35%（持续2个月）

  根因分析：
    → 资质审核形同虚设（仅检查"有/无"，未验证真实性）
    → 有机认证查询网站未核实（cqc.org.cn可免费查证）
    → 商品页面违规使用"有机"标签（违反《广告法》）
    → 采购人员与供应商存在利益关联（未发现）

整改措施：
  1. 资质核查升级：
    → 所有证书必须在发证机构官网实时查验
    → 有机认证：必须在"食品农产品认证信息系统"（food.cnca.gov.cn）核查
    → 建立证书有效期自动预警（提前30天提醒续期）

  2. 采购合规制度：
    → 采购人员轮岗制度（每年轮岗，防止利益关联）
    → 供应商入库须经两人以上交叉审核
    → 建立供应商黑名单共享机制（行业互通）

  3. 商品页面合规：
    → "有机"等标签必须有对应认证证书才可使用
    → 法律合规部门定期抽检商品页面文案

核心教训：
  → 供应商资质审核不能走过场，必须100%核实
  → 有机/绿色等标签是敏感词汇，滥用违反《广告法》
  → 认证造假成本低，必须主动核实，不能仅依赖证书照片
  → 采购腐败是供应链最大风险之一，必须有制衡机制
```

### 案例5：某平台"核心供应商断供危机"

```
背景：某中型平台（年GMV约5亿）因单一供应商依赖引发断供危机

事件经过：
  → 某肉类供应商A（月供货额约¥200万，占品类40%）
  → 因与平台发生账期纠纷（延迟付款15天）
  → 供应商A停止供货，同时断供另两家同类平台（集体行动）

应急处理：
  48小时内：
    → 启动备用供应商紧急补货（但备用供应商月供能力仅¥80万，不足部分缺货）
    → 平台CEO亲自出面与供应商A协商，达成部分恢复供货协议
    → 用户端：已下单用户全额退款，额外补偿¥10无门槛券

损失估算：
  → GMV损失：缺货期间日均损失约¥35万（断供7天 ≈ ¥245万）
  → 补偿成本：退款+优惠券 ≈ ¥18万
  → 紧急采购溢价：临时找备用供应商，采购成本增加约8%（≈¥16万）
  → 声誉损失：部分用户转向竞品（无法精确量化）

根因分析：
  ① 同品类供应商数量不足：最大供应商占比40%（红线应≤30%）
  ② 没有备用供应商：紧急时无可用替代
  ③ 账期管理不善：延迟付款触发供应商集体行动
  ④ 合同条款缺失：没有"供应商断供应急"条款

整改措施：
  ① 同品类备份供应商≥2家，单一供应商占比≤30%
  ② 账期到期前3天自动提醒，到期日必须付款（不可延误）
  ③ 合同中增加"断供应急条款"：供应商断供需提前30天通知
  ④ 建立供应商关系预警机制：账期逾期超7天自动升级

核心教训：
  → 供应商依赖是最大的供应链风险
  → 账期准时支付是供应商关系的基本尊重
  → 备用供应商必须提前培育，不能等危机时再找
```

---

## 附录：供应链检查清单

```
月度供应链健康检查：

□ 1. 供应商稳定性：月流失供应商是否 < 5%？
□ 2. S/A级供应商占比：是否达到 20-30%？
□ 3. 采购成本：主要 SKU 采购价 vs 市场价是否有优势？
□ 4. 账期健康：是否在 T+7 以上？（供商抱怨 = 预警）
□ 5. 资质合规：S/A级供应商资质是否 100% 有效？
□ 6. 损耗率：各品类损耗率是否在目标范围内？
□ 7. 库存周转：呆滞品（>30天未动销）是否 < 5% SKU？
□ 8. 补货预警：是否每日检查断货风险 SKU？
□ 9. 新品测试：试销新品是否有数据复盘（7天/30天）？
□ 10. 黑名单：是否有新增黑名单供应商？

红线预警：
  → 食品安全事故（任意一起 = 全平台下架）
  → 供应商集体断货（ > 3 家 = 供应链危机）
  → 损耗率突然上升 > 3% = 需立即排查原因
```
