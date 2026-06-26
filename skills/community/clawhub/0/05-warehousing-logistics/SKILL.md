---
name: community-group-buying-warehousing-logistics
description: 社区团购仓储与物流履约全链路技能包。涵盖配送模式选择、仓配体系设计、时效管理、成本控制及配套工具。适用于平台运营负责人、物流管理者。
version: 1.0.0
created_at: 2026-04-14
license: MIT
github_url: null
---

# 模块五：仓储与物流

> **模块边界说明**
> 本模块聚焦"货怎么到团长"，即仓到团的配送履约时效与成本控制。
> 选品决策 → 模块一（选品策略）
> 供应链采购 → 模块四（供应链与采购）
> 团长运营 → 模块二（团长运营）
> 获客留存 → 模块三（获客与留存）
> 营销促销 → 模块六（营销与促销）
> 各模块边界独立，不重叠。

---

## 知识库

### 5.1 社区团购仓配体系概述

```
仓配体系是社区团购的"命脉"：

  平台下单 → 仓储分拣 → 物流配送 → 团长自提 → 用户提货

时效要求：
  次日达：当日 23:00 前下单，次日 16:00 前到团长
  当日达：当日 10:00 前下单，当日 20:00 前到团长（部分平台）

仓配成本结构（占 GMV 3-8%）：
  仓储成本：约 1-2%（含分拣/打包/存储）
  配送成本：约 2-5%（取决于距离和密度）
  损耗摊销：约 0.5-1%（已入库损耗）
  退货成本：约 0.2-0.5%（退团/拒收处理）

核心矛盾：
  覆盖越广 → 配送成本越高
  时效越快 → 仓储压力越大
  密度越高 → 单均成本越低
```

---

### 5.2 配送模式选择

#### 自建配送 vs 第三方配送

| 维度 | 自建配送 | 第三方配送 |
|------|---------|-----------|
| 适用规模 | 日均 50 万单以上 | 日均 50 万单以下 |
| 初期投入 | 高（车辆/人员/系统） | 低（按单结算） |
| 管控力度 | 强，可精细化考核 | 弱，依赖第三方 |
| 配送质量 | 稳定可控 | 参差不齐 |
| 成本 | 规模大后成本更低 | 单均 0.5-2 元溢价 |
| 弹性 | 差，大促期间运力紧张 | 好，可弹性扩缩 |

```
各平台配送模式：
  美团优选：自建为主（美团配送），部分区域外包
  多多买菜：第三方众包（蜂鸟/美团众包），成本优先
  兴盛优选：自建 + 区域物流合作，深度管控
  淘菜菜：阿里系菜鸟整合，资源整合型
```

#### 冷链配送要求

| 品类 | 温度要求 | 包装要求 | 最长在途时间 |
|------|---------|---------|------------|
| 冷冻品（冰淇淋/冻肉） | <-18℃ | 泡沫箱+干冰 | < 24h |
| 冷藏品（乳制品/熟食） | 0-4℃ | 冷链箱+冰袋 | < 12h |
| 蔬菜/水果（夏季） | 8-12℃ | 透气包装+冰袋 | < 6h |
| 标品（常温） | 常温 | 纸箱/编织袋 | < 48h |

---

### 5.3 仓配体系层级设计

```
一级仓配（单品均GMV > 500万）：
  产地/工厂 → CDC中心仓 → 团长
  优点：链路最短，成本最低
  缺点：覆盖有限，只适合高密度区域

二级仓配（标准模式）：
  产地/工厂 → CDC中心仓 → 网格仓(Grid) → 团长
  优点：规模化与覆盖平衡
  缺点：多一次装卸，损耗增加 2-3%

三级仓配（早期/低密度区域）：
  产地/工厂 → CDC → 城市仓 → 网格仓 → 团长
  缺点：链路太长，损耗和时效都差，已逐步淘汰
```

#### 各平台仓配体系

| 平台 | 仓配层级 | 配送频次 | 覆盖半径 |
|------|---------|---------|---------|
| 美团优选 | CDC + Grid（2级） | 每日一配 | 10-20km/网格仓 |
| 多多买菜 | CDC直发（1级为主） | 每日一配 | 20-30km |
| 兴盛优选 | 区域仓 + 自提点（2级） | 每日两配 | 5-10km |
| 淘菜菜 | CDC + 前置仓（2级） | 每日两配 | 3-5km |

---

### 5.4 配送时效管理

```
时效标准（从出仓到团长）：

  次日达标准：
    T日 23:00 前下单 → T+1日 16:00 前到团
    用户感受：16小时窗口

  当日达标准：
    T日 10:00 前下单 → T日 20:00 前到团
    用户感受：10小时窗口

时效管控三要素：
  1. 揽收时效：出仓时间 vs 计划出仓时间（误差 < 30分钟）
  2. 运输时效：平均配送时长（按距离分区管控）
  3. 到团时效：实际到团 vs 承诺到团（达成率 > 98%）

时效预警机制：
  超时率 > 2% → 橙色预警（排查原因）
  超时率 > 5% → 红色预警（启动应急配送）
  客诉率 > 1% → 启动专项整改
```

---

### 5.5 配送成本控制

```
配送成本构成（元/单）：

  基础配送费：0.8-1.5（含 3 公里内）
  超出里程费：0.2-0.5 / 公里
  特殊品类费：0.5-1.0（冷链/大件）
  上楼/团长处堆放费：0.1-0.3

行业参考成本（2023年数据）：
  美团优选：1.2-1.8 元/单（规模效应）
  多多买菜：1.0-1.5 元/单（密度高，成本低）
  兴盛优选：0.8-1.2 元/单（区域深耕，密度极高）
  淘菜菜：1.5-2.0 元/单（当日达要求更高）

成本优化路径：
  路径优化：AI路线规划，减少配送里程 10-15%
  集单配送：同方向订单合并，减少行驶距离
  团长密度提升：网格仓覆盖团长密度 > 30/仓 → 单均降 0.3-0.5 元
  合理排线：每车配送团点 15-25 个为最优
```

---

## 方法论

### 5.6 新仓选址评估 SOP

```
新仓选址五步法：

Step 1：需求预测
  → 基于历史单量预测未来 3-6 个月日均单量
  → 考虑季节性波动（大促/节假日 + 30-50%）
  → 参考公式：所需面积 = 日均单量 × 0.003 ㎡（含通道）

Step 2：候选区域筛选
  ┌─────────────────────────────────────────────┐
  │  考量维度        权重      评估要点            │
  │  ─────────────────────────────────          │
  │  交通便利性      20%      高速/主干道出入口    │
  │  团长密度        25%      半径 15km 内团长数   │
  │  租金成本        20%      元/㎡/月，押一付三   │
  │  电力/消防       15%      380V 电力/丙二消防   │
  │  扩展空间        10%      未来 3 年扩展可能性  │
  │  周边环境        10%      禁止有污染型企业     │
  └─────────────────────────────────────────────┘

Step 3：竞品物流调研
  → 调研同类平台仓库位置（避免贴身竞争）
  → 调研第三方云仓资源（弹性扩容选项）
  → 了解当地物流人力市场（司机/分拣工资水平）

Step 4：盈亏测算
  → 单均物流成本 = 月固定成本 / 月均单量
  → 固定成本：租金 + 人工 + 设备摊销 + 水电
  → 临界单量：固定成本 / (配送收入 - 变动成本)
  → 新仓盈亏平衡点：通常需要日均 > 3000 单

  案例：某二线城市新仓选址测算
  ┌─────────────────────────────────────────────────────┐
  │ 候选区域：城东工业园（距核心区 12km）              │
  │ 候选区域：城西社区（距核心区 8km）                  │
  │                                                     │
  │ 城东方案：                                         │
  │   租金：15元/㎡/月 × 1000㎡ = 1.5万/月             │
  │   人工：12人 × 5000元 = 6.0万/月                   │
  │   设备摊销：2.0万/月                               │
  │   水电/其他：0.5万/月                              │
  │   月固定成本合计：10.0万                           │
  │   月配送单量预测：8万单（月均日2500单，旺季3500）   │
  │   单均变动成本：1.2元（第三方配送）                 │
  │   月变动成本：8万 × 1.2 = 9.6万                   │
  │   月总成本：10.0 + 9.6 = 19.6万                   │
  │   单均物流成本：19.6万 ÷ 8万 = 2.45元/单          │
  │   ⚠️ 高于行业均值（1.2-1.8元），风险较大          │
  │                                                     │
  │ 城西方案：                                         │
  │   租金：28元/㎡/月 × 800㎡ = 2.24万/月            │
  │   人工：10人 × 5000元 = 5.0万/月                  │
  │   设备摊销：1.5万/月                               │
  │   水电/其他：0.5万/月                              │
  │   月固定成本合计：9.24万                           │
  │   月配送单量预测：12万单（社区密度高，预测更乐观）   │
  │   单均变动成本：1.0元（密度高，议价能力强）         │
  │   月变动成本：12万 × 1.0 = 12.0万                 │
  │   月总成本：9.24 + 12.0 = 21.24万                 │
  │   单均物流成本：21.24万 ÷ 12万 = 1.77元/单        │
  │   ✅ 在行业合理区间（1.5-2.0元），可接受           │
  └─────────────────────────────────────────────────────┘

Step 5：试运营验证
  → 先用临时仓/云仓试运营 1 个月
  → 验证时效达成率、损耗率、团长满意度
  → 数据达标后再签正式租赁
```

---

### 5.7 配送效率提升方法

```
配送效率提升四步法：

第一步：数据底数摸清
  → 记录每条线路的实际配送时长/里程/单量
  → 统计每个配送员日均单量（基准线）
  → 分析超时/投诉的集中时段和区域

第二步：路线优化（减少 10-15% 里程）
  → 使用地图 API（高德/腾讯）做路径规划
  → 按地理位置分单：东西向/南北向分开配送
  → 优先配送时效要求高的团点（当日达优先）
  → 避开早晚高峰：生鲜早班 5:00-9:00 配送

第三步：团点合并（提升团长密度）
  → 统计网格仓下团长分布密度
  → 淘汰低密度区域（半径内 < 15 个活跃团长）
  → 引导低密度区域团长合并提货点

第四步：绩效考核设计
  → 时效达成率（占 40%）：准时到团率 > 98%
  → 单量完成率（占 30%）：无差错完成配送任务
  → 货损率（占 20%）：配送途中损耗 < 0.3%
  → 团长满意度（占 10%）：定期调研评分

行业参考：配送员日均单量
  密集区域（>20团/线路）：80-120 单/天
  中等密度（10-20团/线路）：50-80 单/天
  低密度（<10团/线路）：30-50 单/天
```

---

### 5.8 配送异常处理话术

```
五种常见配送异常及处理：

异常1：团长联系不上/团长临时不在
  处理：联系备用团长（提前报备名单）
  话术：
    "您好，配送司机到达【团点名称】，团长电话无人接听，
     请协助联系或安排人员接货。如10分钟内无法联系，
     将货物暂存司机车上，等待后续处理。"

异常2：团长拒收（货损/数量不对）
  处理：先核实再处理，不与团长争论
  话术：
    "您好，请您先帮忙签收并在配送单上注明异常情况
     （货损照片已发群），我们将在2小时内补货或退款，
     不会影响您的佣金。"

异常3：配送途中交通事故
  处理：启动备用车辆/延迟补发
  话术：
    "【团长群公告】因配送车辆发生交通事故，
     团点【XX】预计延迟2小时到达，请各位团长提前通知用户，
     延迟到团的订单将额外补偿10元优惠券。"

异常4：用户漏取/未提货
  处理：次日优先配送，不计入损耗
  话术：
    "【团长】未提货用户请在群内@未取用户，
     仍未取货的，商品由团长代售（按团购价结算），
     不计入平台损耗。"

异常5：冷链断链（温度超标）
  处理：整批次召回，不计成本
  话术：
    "【紧急】团点【XX】冷链异常，批次【XXX】全部下架，
     严禁销售。配送员将上门回收，请团长切勿私自处理。
     回收完成后将补发新货。"
```

---

### 5.9 特殊品类配送管理

```
生鲜配送关键控制点：

叶菜类（青菜/菠菜/白菜）：
  → 采摘后 2 小时内预冷至 4℃ 以下
  → 使用透气保鲜袋+冰袋包装
  → 到团后团长需立即放入冷柜
  → 损耗率：配送途中 1-3%

茄果类（番茄/黄瓜/茄子）：
  → 室温配送即可，避免冷藏（会产生冷害）
  → 包装用纸格隔离，减少磕碰
  → 损耗率：配送途中 0.5-2%

水产类（鱼/虾/蟹）：
  → 使用充氧包装+冰袋
  → 活鲜配送：到团存活率目标 > 95%
  → 死亡拒收：需提前与团长确认验收标准
  → 损耗率：配送途中 2-5%（含死亡损耗）

大件/重货（整箱饮料/整袋米）：
  → 单独配送路线，不与生鲜混装
  → 需提前与团长确认存放空间
  → 配送费用单独计费（+ 0.5-1.0 元/单）
```

---

## 工具集

### Tool 1: 配送成本计算器

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配送成本计算器
输入：日均单量 + 配送模式 + 仓储面积 + 人员配置
输出：单均物流成本 + 盈亏平衡分析 + 优化建议
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class LogisticsCostCalculator:
    """物流成本计算"""

    daily_orders: float          # 日均单量
    avg_order_value: float      # 客单价（元）
    storage_area: float         # 仓储面积（㎡）
    storage_rent: float         # 仓储租金（元/㎡/月）
    staff_count: int            # 仓储人员数量
    staff_salary: float         # 人均月工资（元）
    vehicle_count: int           # 配送车辆数量
    vehicle_monthly_cost: float # 车辆月成本（含折旧/油/司机）
    third_party_cost_per_order: float = 0.0  # 第三方配送单价（元/单）
    use_third_party: bool = False  # 是否使用第三方

    def calculate(self) -> Dict:
        # 固定成本（月）
        rent_cost = self.storage_area * self.storage_rent
        labor_cost = self.staff_count * self.staff_salary
        vehicle_cost = self.vehicle_count * self.vehicle_monthly_cost
        fixed_cost = rent_cost + labor_cost + vehicle_cost

        # 变动成本（月）
        monthly_orders = self.daily_orders * 30
        if self.use_third_party:
            variable_cost = monthly_orders * self.third_party_cost_per_order
        else:
            # 自建配送的变动成本（油费/过路费/小件损耗）估 0.3 元/单
            variable_cost = monthly_orders * 0.3

        # 总成本
        total_cost = fixed_cost + variable_cost

        # 单均成本
        cost_per_order = total_cost / monthly_orders
        logistics_cost_ratio = cost_per_order / self.avg_order_value * 100

        # 盈亏平衡分析（假设每单收取平台配送费）
        platform_delivery_fee = self.avg_order_value * 0.05  # 假设配送费占客单价 5%
        break_even_orders = fixed_cost / (platform_delivery_fee - 0.3) if platform_delivery_fee > 0.3 else float('inf')

        # 成本占比分析
        cost_breakdown = {
            "仓储租金": f"{rent_cost/total_cost*100:.1f}%",
            "人工成本": f"{labor_cost/total_cost*100:.1f}%",
            "车辆成本": f"{vehicle_cost/total_cost*100:.1f}%",
            "变动配送": f"{variable_cost/total_cost*100:.1f}%",
        }

        # 优化建议
        suggestions = []
        if cost_per_order > 2.0:
            suggestions.append("⚠️ 单均成本偏高（>2元），建议提升团长密度或优化路线")
        if self.daily_orders < 3000 and not self.use_third_party:
            suggestions.append("⚠️ 日均单量低于 3000，建议前期使用第三方弹性配送")
        if self.storage_area / self.daily_orders > 0.005:
            suggestions.append("⚠️ 仓储面积利用率偏低，考虑缩减面积降固定成本")
        if labor_cost / total_cost > 0.4:
            suggestions.append("⚠️ 人工成本占比 > 40%，考虑自动化分拣设备")
        if cost_per_order <= 1.2:
            suggestions.append("✅ 单均成本处于行业优秀水平（<1.2元）")

        return {
            "日均单量": f"{self.daily_orders:.0f} 单",
            "月均单量": f"{monthly_orders:.0f} 单",
            "月固定成本": f"¥{fixed_cost:,.0f}",
            "月变动成本": f"¥{variable_cost:,.0f}",
            "月总成本": f"¥{total_cost:,.0f}",
            "单均物流成本": f"¥{cost_per_order:.2f}",
            "物流成本占客单价比": f"{logistics_cost_ratio:.1f}%",
            "盈亏平衡日均单量": f"{break_even_orders:.0f} 单（当前）" if break_even_orders != float('inf') else "无法计算",
            "成本占比": cost_breakdown,
            "优化建议": suggestions,
        }


def run():
    print("=" * 55)
    print("配送成本计算器")
    print("=" * 55)

    try:
        daily = float(input("日均单量：").strip() or "5000")
    except ValueError:
        daily = 5000

    try:
        aov = float(input("客单价（元）：").strip() or "35")
    except ValueError:
        aov = 35

    try:
        area = float(input("仓储面积（㎡）：").strip() or "800")
    except ValueError:
        area = 800

    try:
        rent = float(input("仓储租金（元/㎡/月）：").strip() or "25")
    except ValueError:
        rent = 25

    try:
        staff = int(input("仓储人员数量：").strip() or "15")
    except ValueError:
        staff = 15

    try:
        salary = float(input("人均月工资（元）：").strip() or "5000")
    except ValueError:
        salary = 5000

    try:
        vehicles = int(input("配送车辆数量：").strip() or "8")
    except ValueError:
        vehicles = 8

    try:
        vcost = float(input("车辆月成本（元/辆）：").strip() or "6000")
    except ValueError:
        vcost = 6000

    use_3rd = input("使用第三方配送？(y/N)：").strip().lower() == 'y'
    third_cost = 0.0
    if use_3rd:
        try:
            third_cost = float(input("第三方配送单价（元/单）：").strip() or "1.3")
        except ValueError:
            third_cost = 1.3

    calc = LogisticsCostCalculator(
        daily_orders=daily,
        avg_order_value=aov,
        storage_area=area,
        storage_rent=rent,
        staff_count=staff,
        staff_salary=salary,
        vehicle_count=vehicles,
        vehicle_monthly_cost=vcost,
        third_party_cost_per_order=third_cost,
        use_third_party=use_3rd,
    )

    result = calc.calculate()

    print(f"\n{'='*55}")
    print("物流成本分析报告")
    print(f"{'='*55}")
    print(f"\n单量数据：")
    print(f"  {result['日均单量']}  {result['月均单量']}")

    print(f"\n成本明细：")
    print(f"  月固定成本：{result['月固定成本']}")
    print(f"  月变动成本：{result['月变动成本']}")
    print(f"  月总成本：{result['月总成本']}")

    print(f"\n单均成本：")
    print(f"  单均物流成本：{result['单均物流成本']}")
    print(f"  物流成本占客单价比：{result['物流成本占客单价比']}")
    print(f"  盈亏平衡：{result['盈亏平衡日均单量']}")

    print(f"\n成本占比：")
    for k, v in result['成本占比'].items():
        print(f"  {k}：{v}")

    print(f"\n优化建议：")
    for s in result['优化建议']:
        print(f"  {s}")


if __name__ == "__main__":
    run()
```

### Tool 2: 配送时效监控表

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配送时效监控表
输入：每日配送数据（出仓时间/到团时间/团点数）
输出：时效达成率/超时原因分析/改进建议
"""

from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime, timedelta


@dataclass
class DeliveryRecord:
    """单条配送记录"""
    route_id: str
    warehouse_out_time: str   # "05:30"
    planned_arrival: str       # "14:00"
    actual_arrival: str        # "14:32"
    order_count: int
    late_reason: str = ""      # 超时原因


def parse_time(t_str: str) -> datetime:
    today = datetime.today()
    parts = t_str.split(":")
    return today.replace(hour=int(parts[0]), minute=int(parts[1]), second=0)


def analyze_delivery(record: DeliveryRecord) -> Dict:
    """分析单条配送记录"""
    planned = parse_time(record.planned_arrival)
    actual = parse_time(record.actual_arrival)

    delay_minutes = (actual - planned).total_seconds() / 60

    # 状态判断
    if delay_minutes <= 0:
        status = "✅ 准时"
        delay_level = 0
    elif delay_minutes <= 30:
        status = "🟡 轻微迟到"
        delay_level = 1
    elif delay_minutes <= 60:
        status = "🟠 中度迟到"
        delay_level = 2
    else:
        status = "🔴 严重迟到"
        delay_level = 3

    # 原因分析（根据常见原因映射）
    reason_map = {
        "早高峰": "交通拥堵",
        "爆单": "单量超负荷",
        "团长联系不上": "团长配合差",
        "路线绕路": "路线规划差",
        "车故障": "车辆问题",
        "天气": "不可抗力",
    }
    auto_reason = reason_map.get(record.late_reason, record.late_reason or "未知")

    return {
        "路线ID": record.route_id,
        "计划到团": record.planned_arrival,
        "实际到团": record.actual_arrival,
        "延迟": f"+{delay_minutes:.0f}分钟" if delay_minutes > 0 else "准时",
        "状态": status,
        "单量": f"{record.order_count} 单",
        "可能原因": auto_reason,
        "delay_level": delay_level,
    }


def daily_summary(records: List[DeliveryRecord]) -> Dict:
    """每日配送汇总"""
    analyses = [analyze_delivery(r) for r in records]

    total = len(analyses)
    on_time = sum(1 for a in analyses if a["delay_level"] == 0)
    slight = sum(1 for a in analyses if a["delay_level"] == 1)
    moderate = sum(1 for a in analyses if a["delay_level"] == 2)
    severe = sum(1 for a in analyses if a["delay_level"] == 3)

    on_time_rate = on_time / total * 100 if total > 0 else 0
    delay_rate = (slight + moderate + severe) / total * 100 if total > 0 else 0

    # 原因统计
    reason_count = {}
    for a in analyses:
        if a["delay_level"] > 0:
            reason = a["可能原因"]
            reason_count[reason] = reason_count.get(reason, 0) + 1

    # 改进建议
    suggestions = []
    if on_time_rate < 95:
        suggestions.append(f"⚠️ 时效达成率 {on_time_rate:.1f}% 未达标（目标 > 98%）")
    if severe > 0:
        suggestions.append(f"🔴 存在 {severe} 条严重迟到，需专项整改")
    if reason_count:
        top_reason = max(reason_count, key=reason_count.get)
        suggestions.append(f"超时主因：{top_reason}（{reason_count[top_reason]}次），需针对性优化")

    return {
        "总路线数": total,
        "准时": f"{on_time} 条（{on_time_rate:.1f}%）",
        "轻微迟到": f"{slight} 条",
        "中度迟到": f"{moderate} 条",
        "严重迟到": f"{severe} 条",
        "时效达成率": f"{on_time_rate:.1f}%",
        "超时原因分布": reason_count,
        "改进建议": suggestions,
        "明细": analyses,
    }


def run():
    print("=" * 55)
    print("配送时效监控表")
    print("=" * 55)

    n = int(input("输入今日配送路线数量：").strip() or "3")
    records = []

    print(f"\n请依次输入 {n} 条路线数据：")
    for i in range(1, n + 1):
        print(f"\n--- 路线 {i} ---")
        route_id = input(f"路线ID（如R001）：").strip() or f"R{i:03d}"
        out_time = input("出仓时间（HH:MM，如05:30）：").strip() or "05:30"
        planned = input("计划到团时间（HH:MM，如14:00）：").strip() or "14:00"
        actual = input("实际到团时间（HH:MM，如14:30）：").strip() or "14:00"
        orders = int(input("配送单量：").strip() or "40")
        reason = input("迟到原因（可回车跳过）：").strip()

        records.append(DeliveryRecord(route_id, out_time, planned, actual, orders, reason))

    result = daily_summary(records)

    print(f"\n{'='*55}")
    print("配送汇总")
    print(f"{'='*55}")
    print(f"  总路线数：{result['总路线数']}")
    print(f"  准时：{result['准时']}")
    print(f"  轻微迟到：{result['轻微迟到']}")
    print(f"  中度迟到：{result['中度迟到']}")
    print(f"  严重迟到：{result['严重迟到']}")
    print(f"  时效达成率：{result['时效达成率']}")

    if result['超时原因分布']:
        print(f"\n超时原因分布：")
        for k, v in result['超时原因分布'].items():
            print(f"  {k}：{v} 次")

    print(f"\n改进建议：")
    for s in result['改进建议']:
        print(f"  {s}")


if __name__ == "__main__":
    run()
```

### Tool 3: 团长提货点布局优化器

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
团长提货点布局优化器
输入：团长坐标 + 单量数据 + 仓库位置
输出：网格仓覆盖建议 + 合并方案 + 密度热力图
"""

import math
from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class TeamLeader:
    """团长数据"""
    id: str
    name: str
    lat: float  # 纬度
    lon: float  # 经度
    daily_orders: int    # 日均单量
    active_days: int     # 月活跃天数
    distance: float = 0.0  # 与仓库距离（公里），在optimize_coverage中自动计算


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """计算两点间球面距离（公里）"""
    R = 6371  # 地球半径
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat/2)**2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c


def optimize_coverage(
    leaders: List[TeamLeader],
    warehouse_lat: float,
    warehouse_lon: float,
    max_coverage_km: float = 15.0,
    min_leaders_per_grid: int = 10,
) -> Dict:
    """
    网格仓覆盖优化

    Args:
        leaders: 团长列表
        warehouse_lat/lon: 仓库位置
        max_coverage_km: 最大覆盖半径
        min_leaders_per_grid: 每个网格仓最少团长数
    """
    # 过滤活跃团长（月活跃 > 15天）
    active = [l for l in leaders if l.active_days >= 15]
    total_leaders = len(active)
    total_orders = sum(l.daily_orders for l in active)

    # 按单量排序
    active.sort(key=lambda x: x.daily_orders, reverse=True)

    # 计算每个团长到仓库的距离
    for l in active:
        l.distance = haversine(warehouse_lat, warehouse_lon, l.lat, l.lon)

    # 分组：按距离分区
    zones = {"核心区": [], "扩展区": [], "边缘区": []}
    for l in active:
        if l.distance <= 5:
            zones["核心区"].append(l)
        elif l.distance <= 10:
            zones["扩展区"].append(l)
        elif l.distance <= max_coverage_km:
            zones["边缘区"].append(l)

    # 合并建议
    merge_suggestions = []
    if len(active) < min_leaders_per_grid:
        merge_suggestions.append(
            f"⚠️ 团长总数 {len(active)} 低于最低要求 {min_leaders_per_grid}，"
            "建议暂不设网格仓，使用第三方配送直发"
        )

    # 单量密度分析
    density_by_zone = {}
    for zone, leaders_list in zones.items():
        if leaders_list:
            avg_orders = sum(l.daily_orders for l in leaders_list) / len(leaders_list)
            density_by_zone[zone] = {
                "团长数": len(leaders_list),
                "日均单量": sum(l.daily_orders for l in leaders_list),
                "平均单量": f"{avg_orders:.1f}",
                "单量占比": f"{sum(l.daily_orders for l in leaders_list)/total_orders*100:.1f}%",
            }

    # 网格仓选址建议（选择核心区中心位置）
    grid_suggestions = []
    if zones["核心区"]:
        center_lat = sum(l.lat for l in zones["核心区"]) / len(zones["核心区"])
        center_lon = sum(l.lon for l in zones["核心区"]) / len(zones["核心区"])
        grid_suggestions.append({
            "位置": "核心区",
            "建议坐标": f"({center_lat:.4f}, {center_lon:.4f})",
            "覆盖团长": len(zones["核心区"]),
            "预计日均单量": sum(l.daily_orders for l in zones["核心区"]),
        })
    if zones["扩展区"]:
        grid_suggestions.append({
            "位置": "扩展区",
            "建议坐标": f"({sum(l.lat for l in zones['扩展区'])/len(zones['扩展区']):.4f}, "
                       f"{sum(l.lon for l in zones['扩展区'])/len(zones['扩展区']):.4f})",
            "覆盖团长": len(zones["扩展区"]),
            "预计日均单量": sum(l.daily_orders for l in zones["扩展区"]),
        })

    return {
        "总活跃团长数": total_leaders,
        "日均总单量": total_orders,
        "密度分析": density_by_zone,
        "网格仓选址建议": grid_suggestions,
        "合并建议": merge_suggestions,
    }


def run():
    print("=" * 55)
    print("团长提货点布局优化器")
    print("=" * 55)
    print("（演示模式：输入 5 个团长模拟数据）\n")

    # 模拟团长数据（假设仓库在 [31.2304, 121.4737] 上海人民广场附近）
    warehouse = (31.2304, 121.4737)

    demo_leaders = [
        TeamLeader("TL001", "张团长", 31.2280, 121.4750, 45, 28),
        TeamLeader("TL002", "李团长", 31.2350, 121.4800, 38, 25),
        TeamLeader("TL003", "王团长", 31.2400, 121.4700, 52, 30),
        TeamLeader("TL004", "刘团长", 31.2500, 121.4900, 22, 18),
        TeamLeader("TL005", "陈团长", 31.2200, 121.4600, 30, 20),
    ]

    result = optimize_coverage(demo_leaders, warehouse[0], warehouse[1])

    print(f"数据概览：")
    print(f"  活跃团长总数：{result['总活跃团长数']} 个")
    print(f"  日均总单量：{result['日均总单量']} 单")

    print(f"\n密度分析（按距离分区）：")
    for zone, data in result['密度分析'].items():
        print(f"  【{zone}】")
        print(f"    团长数：{data['团长数']}")
        print(f"    日均单量：{data['日均单量']}")
        print(f"    平均单量：{data['平均单量']}/天")
        print(f"    单量占比：{data['单量占比']}")

    print(f"\n网格仓选址建议：")
    for s in result['网格仓选址建议']:
        print(f"  {s['位置']}：坐标 {s['建议坐标']}")
        print(f"    覆盖团长：{s['覆盖团长']} 个")
        print(f"    预计日均：{s['预计日均单量']} 单")

    print(f"\n合并建议：")
    for s in result['合并建议']:
        print(f"  {s}")


if __name__ == "__main__":
    run()
```

### Tool 4: 配送异常预测表

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配送异常预测表
输入：天气/交通/节日/历史数据
输出：各路线异常风险评分 + 预警级别
"""


def predict_delivery_risk(
    route_id: str,
    distance_km: float,
    is_holiday: bool,
    is_weekend: bool,
    weather: str,         # "晴" / "雨" / "暴雨" / "雪"
    historical_delay_rate: float,  # 历史延迟率（0-1）
    holiday_season: bool,  # 春节/国庆等长假期
) -> dict:
    """
    预测配送路线异常风险

    Args:
        route_id: 路线ID
        distance_km: 配送距离（公里）
        is_holiday: 是否节假日
        is_weekend: 是否周末
        weather: 天气状况
        historical_delay_rate: 该路线历史延迟率
        holiday_season: 是否春节/国庆等大假期
    """
    # 风险因子评分
    risk_factors = {}

    # 距离因子：> 20km 高风险
    if distance_km > 20:
        risk_factors["长距离配送"] = 3  # 高风险
    elif distance_km > 10:
        risk_factors["中距离配送"] = 2  # 中风险
    else:
        risk_factors["短距离配送"] = 1  # 低风险

    # 天气因子
    weather_scores = {
        "晴": 0, "多云": 0, "阴": 1,
        "雨": 2, "暴雨": 4, "雪": 4, "大雾": 3,
    }
    weather_risk = weather_scores.get(weather, 1)
    risk_factors[f"天气：{weather}"] = weather_risk

    # 时间因子
    if holiday_season:
        risk_factors["节假日长假期"] = 4
    elif is_holiday:
        risk_factors["普通节假日"] = 2
    elif is_weekend:
        risk_factors["周末"] = 1

    # 历史延迟因子
    if historical_delay_rate > 0.15:
        risk_factors["历史高延迟"] = 3
    elif historical_delay_rate > 0.05:
        risk_factors["历史中延迟"] = 2
    else:
        risk_factors["历史低延迟"] = 0

    # 总风险评分（满分10）
    total_score = sum(risk_factors.values())

    # 风险级别
    if total_score >= 8:
        level = "[RED] 高风险"
        action = "建议更换配送时间或启用备用车辆"
    elif total_score >= 5:
        level = "[ORANGE] 中风险"
        action = "建议提前出发，增加30分钟 buffer"
    elif total_score >= 2:
        level = "[YELLOW] 低风险"
        action = "正常执行，关注天气变化"
    else:
        level = "[GREEN] 正常"
        action = "无特殊风险，正常执行"

    return {
        "路线ID": route_id,
        "配送距离": f"{distance_km}km",
        "风险因子": risk_factors,
        "风险评分": f"{total_score}/10",
        "风险级别": level,
        "建议行动": action,
    }


def run():
    print("=" * 55)
    print("配送异常预测表")
    print("=" * 55)

    n = int(input("输入要预测的路线数量：").strip() or "2")

    for i in range(1, n + 1):
        print(f"\n--- 路线 {i} ---")
        route_id = input("路线ID：").strip() or f"R{i:03d}"
        distance = float(input("配送距离（km）：").strip() or "15")
        weather = input("天气（晴/雨/暴雨/雪）：").strip() or "晴"
        hist_rate = float(input("历史延迟率（0.1 = 10%）：").strip() or "0.05")
        is_weekend = input("是否周末（y/N）：").strip().lower() == 'y'
        is_holiday = input("是否节假日（y/N）：").strip().lower() == 'y'
        holiday_season = input("是否春节/国庆长假（y/N）：").strip().lower() == 'y'

        result = predict_delivery_risk(
            route_id, distance, is_holiday, is_weekend,
            weather, hist_rate, holiday_season
        )

        print(f"\n  风险级别：{result['风险级别']}")
        print(f"  风险评分：{result['风险评分']}")
        print(f"  风险因子：{result['风险因子']}")
        print(f"  建议：{result['建议行动']}")


if __name__ == "__main__":
    run()
```

---

### 5.10 仓配盈亏平衡分析

```
仓配盈亏平衡核心公式：

固定成本 = 仓租 + 人工 + 设备摊销 + 水电 + 管理费
变动成本 = 单均配送费 + 单均损耗摊销 + 单均退货处理费

月总仓配成本 = 固定成本 + 变动成本 × 月订单量

盈亏平衡点（月订单量）= 固定成本 / (单均配送收入 - 单均变动成本)

---

仓配收入来源（平台视角）：
  → 供应商仓租/仓储服务费（可选）
  → 配送服务费（向供应商收取，约客单价 3-5%）
  → 货值损耗补贴（由供应商承担）

单均边际贡献 = 配送收入 - 变动成本
  （必须 > 0 才能覆盖固定成本）

---

仓配运营决策参考表：

月固定成本估算（示例，二线城市网格仓）：
  仓租：¥15-25元/㎡/月 × 200㎡ = ¥3,000-5,000/月
  人工：3人 × ¥5,000/月 = ¥15,000/月
  设备摊销：¥2,000/月（货架/叉车/打包机）
  水电管理：¥2,000/月
  月固定成本合计：约 ¥22,000-24,000/月

盈亏平衡测算：
  假设：单均配送收入 ¥1.5，单均变动成本 ¥0.8
  单均边际贡献 = ¥1.5 - ¥0.8 = ¥0.7
  月固定成本 ¥23,000
  盈亏平衡月订单量 = ¥23,000 / ¥0.7 ≈ 32,857 单/月
  日均盈亏平衡 ≈ 1,095 单/天

行业实际参考：
  ┌─────────────────────────────────────────────────────────────┐
  │ 仓型          日均单量    月固定成本    单均配送收入         │
  │ ─────────────────────────────────────────────────────       │
  │ 网格仓         >5000      ¥8-12万      ¥1.2-1.5/单         │
  │ 中心仓         >20000     ¥25-40万     ¥1.0-1.3/单         │
  │ 前置仓（PC）   >3000      ¥12-18万     ¥2.5-4.0/单（赔钱） │
  └─────────────────────────────────────────────────────────────┘

决策边界：
  日均单量 > 盈亏平衡点 → 仓配体系可持续扩
  日均单量 < 盈亏平衡点 × 0.7 → 立即优化（缩仓/降人工/提效率）
  日均单量 < 盈亏平衡点 × 0.5 → 战略性撤退或关仓

扩仓决策触发条件（必须同时满足）：
  ① 当前仓日均单量 > 盈亏平衡点 × 1.5（稳健扩仓）
  ② 区域内团长密度持续提升（>20个/仓）
  ③ 竞对未在该区域形成垄断
```
```

---

## 案例库

### 案例1：多多买菜"拼多多式"物流降本

```
问题：农产品单均价值低，物流成本占比高

背景：
  拼多多农产品客单价约 25-30 元
  物流成本每下降 0.1 元 = 利润率提升 0.4%
  规模化后物流成本优化空间巨大

具体措施：
  1. 路线合并：同一方向订单集中配送，减少行驶里程 15%
  2. 集单集运：多个团点合并到同一辆车，降低单车单趟成本
  3. 众包配送：使用蜂鸟/美团众包，弹性扩缩，无需养固定配送员
  4. 网格仓下沉：在低线城市设网格仓，缩短配送半径

数据效果（2019-2022年）：
  物流成本从 2.5 元/单 → 1.3 元/单（下降 48%）
  损耗率从 12-15% → 7-9%（冷链标准化）
  时效：从 48 小时 → 24 小时达团率提升至 92%

核心逻辑：
  → 密度效应：团长越多，单均配送成本越低
  → 规模效应：单量越大，单均固定成本越低
  → 路径优化：算法规划路线，减少空驶率
```

### 案例2：兴盛优选"当日两配"的高密度打法

```
问题：如何做到比竞争对手更快的时效体验

策略：每日两配，提高提货密度

上午配送（满足早市需求）：
  00:00 供应商送货到仓
  01:00-05:00 分拣完成
  05:00-10:00 第一批配送
  10:00 前到团 → 用户上午可提货

下午配送（满足追加需求）：
  10:00-12:00 下午订单分拣
  12:00-18:00 第二批配送
  18:00-20:00 到团 → 用户晚间可提货

数据效果（2021年数据）：
  当日达率：95%（行业最高）
  用户复购率：78%（高频次购物习惯养成）
  客诉率：< 0.5%（到团及时，用户体验好）

关键成功因素：
  1. 供应商配合：愿意凌晨送货到仓
  2. 团长配合：愿意早开门晚关门（6:00-22:00）
  3. 密度足够：每条线路团点 > 20 个，车辆满载率高
  4. 流程标准化：两配之间严格隔离，不混装
```

### 案例3：淘菜菜"即时配送"模式的差异化探索

```
背景：淘菜菜（阿里）试图以"即时配送"差异化竞争

策略：借鉴盒马/天猫超市，前置仓发货，最快2小时达

仓配体系：
  前置仓（PC）：覆盖 3-5 公里，SKU 精选 500-800 个
  配送：绑定蜂鸟骑手，实现 2-4 小时达
  自提为主，部分支持送货上门（+2元服务费）

时效对比：
  淘菜菜：2-4 小时达（最快）
  兴盛优选：当日达（早市+午市两配）
  美团/多多：次日达（行业主流）

数据表现（2021年）：
  用户满意度：92%（时效体验好）
  单均配送成本：3.5-4.5 元/单（是美团的2倍）
  订单密度：日均 2000-3000 单/前置仓（低于盈亏平衡 5000 单）
  亏损率：每单亏损 1.5-2.0 元

失败原因：
  1. 社区团购用户价格敏感：愿意等次日达，不愿付即时配送溢价
  2. 单均配送成本过高：2-4 元/单 vs 美团的 1.2-1.8 元/单
  3. 前置仓 SKU 有限：500-800 SKU 满足不了家庭一站式购物
  4. 与美团/多多正面竞争：规模不如多多，价格不如美团

教训总结：
  → 社区团购的核心竞争力是"性价比"，不是"即时性"
  → 次日达模式在低线城市完全足够
  → 即时配送适合高线城市高收入人群，不适合下沉市场
```

### 案例4：美团优选Grid仓的精细化运营

```
成功点：网格仓（Grid仓）标准化管理，降低履约成本

Grid仓定位：
  → 位于社区 10-15 公里范围内
  → 覆盖 50-100 个团长自提点
  → 日均单量 5000-10000 单/仓
  → 人员配置：8-15 人（含分拣/配送管理）

Grid仓标准化 SOP：
  1. 入库：08:00 前供应商送达，扫码入库
  2. 分拣：08:00-11:00 完成分拣，按线路码放
  3. 配送：11:00-16:00 完成所有团点配送
  4. 结算：当日 20:00 前确认配送完成，系统结算

考核指标（网格仓长）：
  时效达成率（占 40%）：16:00 前到团率 > 98%
  货损率（占 30%）：< 0.5%
  成本控制（占 20%）：单均成本 < 目标值
  团长满意度（占 10%）：评分 > 4.5/5

成本参考（2022年华南地区）：
  网格仓固定成本：约 ¥8-12 万/月
  单均配送成本：¥0.8-1.2 元/单（含仓储）
 盈亏平衡：日均 > 5000 单
```

### 案例5：某平台"低密度区域网格仓关停危机"

```
背景：某平台在低人口密度区域过早建设网格仓，导致持续亏损被迫关停

事件经过：
  → 进入新省份时，在某县级市场开设网格仓
  → 该区域日均单量仅 800 单（远低于 5000 单盈亏平衡线）
  → 网格仓固定成本 ¥8万/月，持续亏损 6 个月
  → 累计损失：¥8万×6月 = ¥48万（不含机会成本）

问题诊断：
  ① 选址评估不足：仅看"市场潜力"，未验证"短期单量支撑"
  ② 乐观预期：认为3个月可达到盈亏平衡，实际远未达标
  ③ 缺乏退出机制：发现亏损后未及时关停，持续失血
  ④ 政治考量：当地负责人不想承认失败，拖延决策

处置过程：
  第1-2月：观察期，发现单量无明显增长
  第3-4月：尝试补贴拉单，但成本更高（补贴+运营 > 收益）
  第5月：区域负责人终于上报亏损情况
  第6月：决定关停，但已损失约¥40万

损失估算：
  固定成本：¥8万/月 × 6月 = ¥48万
  补贴拉单额外成本：约¥8万
  关停后重新进入成本：重新建设约¥15万（场地/设备/人员）
  总损失：约¥71万 + 延误当地市场3-6个月

核心教训：
  → 网格仓开设前必须做"试运营验证"：日均单量≥3000才可建仓
  → 设定明确止损线：连续3个月低于盈亏平衡50%则启动关停评估
  → 选负责人时，"不承认失败"的倾向是危险信号
  → 新市场开拓应"小步快跑"，先验证再放大
```

### 案例6：某平台"冷链断链导致整批酸奶报废"

```
失败背景：2023年夏季，平台销售低温酸奶，因冷链车故障导致500箱酸奶报废

事故经过：
  ① 事件发生：
    → 夏季高温天，冷藏车运输途中故障（冷机损坏）
    → 司机未及时发现，车内温度升至30℃（标准≤8℃）
    → 到仓后验收：500箱酸奶温度超标，全部拒收

  ② 损失估算：
    → 商品成本：500箱 × ¥80/箱 = ¥4万
    → 报废成本：全额损失
    → 额外成本：紧急调货 + 延期配送 + 用户补偿 ≈ ¥1.5万
    → 总计直接损失：约¥5.5万

  ③ 根因分析：
    → 冷链车老旧：车队平均车龄5年，冷机故障率偏高
    → 监控缺失：车辆无实时温度监控，到仓才发现问题
    → 应急缺失：司机无备用方案（可联系备用车辆或及时转运）

  ④ 处理过程：
    → 仓管拒收后，联系供应商协调退货
    → 用户补偿：已下单用户全额退款 + ¥5无门槛券
    → 承运商追责：按合同条款，承运商承担商品损失

整改措施：
  ① 冷链车加装实时温度监控设备（GPS+温度传感器，数据同步到后台）
  ② 设定温度告警阈值：车内温度>12℃自动告警，>15℃触发应急程序
  ③ 司机应急培训：温度异常时立即停车+联系调度+启动备用方案
  ④ 建立承运商考核机制：冷链断链超2次，终止合作

核心教训：
  → 冷链是生鲜品类的生命线，实时监控比事后补救重要100倍
  → 报废成本由承运商承担，但商誉损失和用户流失是平台承担
  → 夏季是冷链事故高发期，必须提前做车辆检修和应急演练
```

---

## 附录：配送履约检查清单

```
月度配送履约健康检查：

□ 1. 时效达成率：16:00 前到团率是否 > 98%？
□ 2. 配送破损率：是否 < 0.5%？（含团长拒收）
□ 3. 单均配送成本：是否在目标范围内（< ¥1.5 元/单）？
□ 4. 车辆满载率：是否 > 75%？（未满载需优化线路）
□ 5. 团长投诉率：是否 < 1%？
□ 6. 异常件处理：超时/破损/错发是否 24 小时内处理？
□ 7. 冷链合规：冷藏/冷冻品是否全程温控合规？
□ 8. 配送员管理：是否每日进行安全培训？
□ 9. 新团长布点：新开团长是否完成配送测试？
□ 10. 大促预案：大促期间（双11/过年）是否有专项履约方案？

红线预警：
  → 时效达成率连续 3 天 < 95% = 红色预警，立即排查
  → 单均配送成本突然上涨 > 20% = 需查原因（油价/线路/密度）
  → 团长集中投诉（> 5 例/天）= 客服专项跟进
  → 冷链断链（温度超标）= 该批次商品全部召回，不计成本
```
