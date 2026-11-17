<!--
forklift-benchmark-v2 / knowledge/standards.md
forklift embodied-intelligence benchmark — regulatory & standards knowledge base
covers: GB/T 43756, GB/T 44679, GB/T 43657, ISO 23308, ISO 3691-1, TSG 11
bilingual (中文 / English)
-->
# 叉车标准与法规知识库 / Forklift Standards & Regulations Knowledge Base

> 用途:为叉车具身智能 Benchmark 提供法规、标准、约束条款基线。
> 基准:2024-2026 国标 + ISO 2020-2024 体系 + 中国特种设备法规。
> 范围:聚焦 6 大核心标准 + 1 部特种设备监察规程,每条标注对 Benchmark 的影响。

---

## 1. GB/T 43756-2024《叉车设计规范》

| 字段 | 内容 |
|------|------|
| 标准号 / Standard No. | GB/T 43756-2024 |
| 中文名 / Chinese Name | 叉车设计规范 |
| 英文名 / English Name | Forklift — Design specification |
| 颁布年份 / Issued | 2024 |
| 实施日期 / Effective | 2024-10-01 |
| 性质 / Type | 推荐性国家标准(GB/T) |
| 页数 / Pages | 144 |
| 起草单位 / Drafters | 安徽合力、北京起重运输机械研究院、杭叉、林德(中国)等 |
| 归口 / SAC TC | SAC/TC 332(全国工业车辆标准化技术委员会) |
| 状态 / Status | 现行 / Current |

### 核心约束条款 / Key Constraint Clauses

1. **适用范围 / Scope** — 平衡重式、前移式、侧面式、插腿式、托盘堆垛车、三向堆垛式共 6 类车辆的设计要求。
2. **结构设计 / Structure** — 门架强度、护顶架、驾驶室、座椅、安全带固定点。
3. **机械传动 / Mechanical Drive** — 变速箱、驱动桥、转向桥、制动系统的设计余量。
4. **电气系统 / Electrical** — 电压等级(常见 24V/48V/80V/96V/144V)、绝缘等级、IP 防护等级。
5. **液压系统 / Hydraulic** — 工作压力、软管爆破系数(≥4 倍工作压力)、液压油清洁度。
6. **安全装置 / Safety Devices** — 门架前倾/后倾限位、起升限位、超载保护(部分车型强制)、驻车制动。

### 对 Benchmark 的影响 / Impact on Benchmark
- **运动学包络 / Kinematic envelope** — 门架前倾/后倾角度、起升高度、下降速度须受标准约束,Benchmark 仿真器须在动作空间内做硬性裁剪。
- **稳定性验证 / Stability** — 仿真场景须按 GB/T 5141(平衡重式)/ GB/T 5142(前移式)做稳定性试验,失稳工况记为 fail。
- **属具接口 / Attachment interface** — 货叉挂钩尺寸、属具液压快换接头须按本标准中"属具连接"章节设计。
- **安全联锁 / Safety interlock** — 起升超限、急停、护顶架、座椅开关等可在 Benchmark 中设置为事件触发器。

---

## 2. GB/T 44679-2024《叉车禁用与报废技术规范》

| 字段 | 内容 |
|------|------|
| 标准号 | GB/T 44679-2024 |
| 中文名 | 叉车禁用与报废技术规范 |
| 英文名 | Forklift — Prohibition and scrapping technical specification |
| 实施日期 | 2025-04-01 |
| 性质 | 推荐性国家标准 |

### 核心约束条款 / Key Clauses
1. **禁用条件 / Prohibition conditions** — 检验不合格、未注册登记、未持证操作、超过设计使用年限仍带病作业。
2. **报废条件 / Scrapping conditions**:
   - 平衡重式叉车使用年限一般不超过 **12 年**(按工况可调整);
   - 锂电池循环寿命 < 80% 标称容量、铅酸电池严重硫化;
   - 货叉磨损 > 10% 厚度、链条延伸率 > 3%、门架变形超差;
   - 制动性能不达标、转向间隙超标。
3. **报废流程 / Scrapping process** — 检测 → 评估 → 备案 → 注销使用登记 → 拆解。

### 对 Benchmark 的影响
- **残值/老化仿真 / Aging simulation** — Benchmark 可模拟"老旧叉车"工况:链条松、货叉磨、刹车弱、转向间隙大。
- **任务拒绝 / Task rejection** — 当 Agent 派遣了一辆"接近报废"状态的叉车,场景应给出"该车建议报废,不可用于本任务"提示。
- **数据集划分 / Dataset split** — 训练集中"健康车"占主体,测试集中应包含 5-10% 老旧车场景,考察 Agent 识别与告警能力。

---

## 3. GB/T 43657-2024《工业车辆能效 试验方法》(系列)

### 3.1 GB/T 43657.1-2024 总则

| 字段 | 内容 |
|------|------|
| 标准号 | GB/T 43657.1-2024 |
| 中文名 | 工业车辆能效 试验方法 第1部分:总则 |
| 英文名 | Energy efficiency of industrial trucks — Test methods — Part 1: General |
| 实施日期 | 2024-10-01 |
| 性质 | 推荐性国家标准 |
| 等同采用 / IDT | ISO 23308-1:2020 |
| 起草单位 | 杭叉、合力、林德、诺力、中力、凡己科技等 |

### 3.2 GB/T 43657.2-2024 操作者控制车辆

| 字段 | 内容 |
|------|------|
| 标准号 | GB/T 43657.2-2024 |
| 范围 | 操作者控制的自行式车辆、牵引车、载运车(对应 ISO 23308-2:2020) |
| 试验循环 | 标准 VDI 循环 — 起升 + 行驶 + 转向 + 下降 + 倒退,合计 60s/循环 |

### 3.3 GB/T 43657.3-2024 集装箱搬运车

| 字段 | 内容 |
|------|------|
| 标准号 | GB/T 43657.3-2024 |
| 范围 | 集装箱搬运车(对应 ISO 23308-3:2020) |
| 专项 | 满载/空载集装箱堆垛循环 |

### 核心约束 / Key Clauses
1. **测试条件**:环境温度 20±5°C,锂电池 SOC 20%-80% 区间,载荷为额定载荷的 **60% ± 5%**(典型工况)。
2. **能耗指标**:
   - Wh/循环(每标准循环消耗电量)
   - kWh/h(每小时能耗)
   - 整车能量利用率(行驶+起升+液压+充电损耗)
3. **充电效率** — 需同时记录充电机效率与电池充放电效率。

### 对 Benchmark 的影响
- **能耗奖励设计 / Energy reward** — Benchmark 可根据 ISO 23308 标准循环计算 Agent 的能耗得分。
- **电池建模 / Battery modeling** — SOC、温度、循环次数、容量衰减需符合该标准。
- **充电桩交互 / Charger interaction** — Agent 决策去哪个充电桩、用什么功率,均需在该体系下评估。

---

## 4. ISO 23308(国际)

| 字段 | 内容 |
|------|------|
| 标准号 | ISO 23308-1/2/3:2020 |
| 英文名 | Energy efficiency of industrial trucks — Test methods |
| 状态 | 现行 / Current |
| 中国对应 | GB/T 43657.1/2/3-2024(IDT 全部) |
| 适用范围 | 自行式工业车辆使用阶段能耗 |

### 关键概念 / Key Concepts
- **使用阶段能耗(Use-phase energy)** — 不含原材料、制造的隐含能。
- **标准循环(Standard cycle)** — 包含 5 个动作:起升、行驶、转向、下降、倒退。
- **测试载荷(60% ± 5%)** — 实际工作典型载荷,而非满载。

### 对 Benchmark 的影响
- **基准对比 / Baseline comparison** — Benchmark 可将 Agent 决策与 ISO 23308 标准循环对比,生成"超标率"指标。
- **跨平台一致 / Cross-platform consistency** — 国际/国内标准 IDT 对应,保证 Benchmark 在出口场景(欧洲 CE 认证)中同样适用。

---

## 5. ISO 3691-1(国际) / GB 10827.1-2014(国标)

| 字段 | 内容 |
|------|------|
| 标准号(国际) | ISO 3691-1:2011(最新修订 2015 版) |
| 标准号(国标) | GB 10827.1-2014(IDT 2011 版) |
| 中文名 | 工业车辆安全要求和验证 第1部分:自行式工业车辆(除无人驾驶、伸缩臂、载运车) |
| 英文名 | Safety requirements and verification — Part 1: Self-propelled industrial trucks |
| 性质(国标) | 强制性国家标准(GB) |

### 核心约束条款 / Key Clauses
1. **结构完整性 / Structural integrity** — 护顶架、门架、货叉、链条、制动器、转向系统的设计要求。
2. **稳定性 / Stability** — 纵向、横向稳定性,载荷曲线下任何工况不得失稳。
3. **操作系统 / Operating systems** — 制动、加速、转向、起升、下降、前倾、后倾的人机工程学要求。
4. **电气 / Electrical** — 绝缘、接地、漏电保护、电池连接。
5. **照明与信号 / Lighting & signals** — 前灯、转向灯、倒车蜂鸣器(>3 km/h 倒车必须)、蓝色警示灯(选配)。
6. **可听报警 / Audible warning** — 倒车蜂鸣 ≥ 90 dB(A) @ 1m。
7. **保护装置 / Protective devices** — 紧急断电(急停)、超载限制器、起升限位器。

### 对 Benchmark 的影响
- **安全事件触发 / Safety event triggers** — Benchmark 中"超载起升""失稳操作""未系安全带""未鸣笛倒车"等均可记为安全违规。
- **声光合规 / Acoustic-optical compliance** — 仿真中可检测 Agent 是否在倒车时启动蜂鸣器。
- **急停链路 / E-stop chain** — Agent 决策遇到紧急障碍时须调用急停,Benchmark 验证急停时延 ≤ 200ms。

---

## 6. TSG 11-2020《场(厂)内专用机动车辆安全技术监察规程》

| 字段 | 内容 |
|------|------|
| 规程号 | TSG 11-2020 |
| 中文名 | 场(厂)内专用机动车辆安全技术监察规程 |
| 英文名 | Safety Technical Supervision Regulation for Special Motor Vehicles In-plant(In-site) |
| 发布部门 | 国家市场监督管理总局 |
| 性质 | 部门规范性文件,强制性 |
| 关联目录 | 列入《特种设备目录》(2023 版)场(厂)内专用机动车辆 |

### 核心约束 / Key Clauses
1. **使用登记 / Registration** — 叉车投入使用前必须办理使用登记,获得使用登记证。
2. **定期检验 / Periodic inspection** — 每年至少一次全面检验(由特种设备检验检测机构出具报告)。
3. **作业人员 / Operators** — 必须取得"场(厂)内专用机动车辆作业人员证",即 N1 / N2 驾照:
   - **N1** — 平衡重式叉车;
   - **N2** — 其他类型(前移式、侧面式、插腿式、牵引车等)。
4. **报废注销 / Deregistration** — 达到报废条件,向登记部门办理注销。
5. **事故报告 / Incident reporting** — 发生事故 30 分钟内上报,启动应急预案。
6. **保险 / Insurance** — 鼓励投保特种设备责任险。

### 对 Benchmark 的影响
- **资质校验 / Qualification check** — Benchmark 派遣 Agent 时,需校验"操作员证"是否匹配车型与吨位。
- **年检事件 / Annual inspection event** — 仿真环境可注入"年检到期"事件,考察 Agent 是否触发报检流程。
- **违章计分 / Penalty scoring** — 安全违规、超载、违停等按规程计分,与 N1/N2 驾照挂钩。

---

## 7. 标准对照速查表 / Standards Cross-Reference

| 主题 | 中国 GB | 国际 ISO | 欧盟 EN | 备注 |
|------|------|------|------|------|
| 设计总则 | GB/T 43756-2024 | — | EN ISO 3691-1(结构部分) | 144 页设计规范 |
| 报废 | GB/T 44679-2024 | — | — | 2025-04-01 起 |
| 能效总则 | GB/T 43657.1-2024 | ISO 23308-1:2020 | EN 16796-2:2016(对位) | IDT |
| 能效-操作者 | GB/T 43657.2-2024 | ISO 23308-2:2020 | EN 16796-2:2016 | IDT |
| 能效-集装箱 | GB/T 43657.3-2024 | ISO 23308-3:2020 | — | IDT |
| 通用安全 | GB 10827.1-2014 | ISO 3691-1:2011 | EN ISO 3691-1 | 强制 |
| 伸缩臂 | GB/T 10827.2-2021 | ISO 3691-2:2016 | — | 推荐 |
| 无人驾驶 | (待转) | ISO 3691-4:2020 | EN ISO 3691-4 | AGV 适用 |
| 术语分类 | GB/T 6104.1-2018 | ISO 5053-1:2015 | — | I/II/III/IV/V |
| 属具设计 | GB/T 46909-2025 | — | — | 货叉/夹抱器等 |
| 操作手册 | GB/T 43923-2024 | — | — | 培训用 |
| 检查维护 | GB/T 44361-2024 | — | — | 维保用 |
| 特种设备 | TSG 11-2020 | — | — | 强制性规程 |

---

## 8. 强制性 vs 推荐性 / Mandatory vs Voluntary

- **强制性(GB/TSG)** — 涉及人身安全、节能、环保、监管,必须执行;不达标不得出厂、销售、运行。
  - 范例:GB 10827.1-2014(安全)、GB 38031-2025(动力电池安全)、TSG 11(监察规程)。
- **推荐性(GB/T)** — 技术指南,鼓励采用,无强制约束。
  - 范例:GB/T 43756(设计)、GB/T 44679(报废)、GB/T 43657(能效)。

---

## 9. 查询渠道 / Lookup Channels

| 渠道 / Channel | URL | 用途 |
|------|------|------|
| 国家标准全文公开系统 | openstd.samr.gov.cn | GB 标准在线阅读/购买 |
| 工标网 | www.csres.com | GB/行业/团标检索 |
| ISO Online | www.iso.org/standard | ISO 原文(付费) |
| 欧盟 CEN | standards.cencenelec.eu | EN 标准 |
| 国家市场监督管理总局 | www.samr.gov.cn | TSG 法规 |
| 中叉网标讯 | www.chinaforklift.com | 行业标准动态 |

---

## 10. Benchmark 集成建议 / Benchmark Integration Recommendations

1. **合规检查器(Compliance Checker)** — 在仿真器中实现一个 `compliance.py` 模块,加载 6 大标准,实时检测 Agent 决策。
2. **计分函数(Score Function)** — 借鉴 ISO 23308 标准循环 + ISO 3691 安全规则,综合"能耗 + 安全 + 效率 + 寿命"四维度评分。
3. **事件触发器(Event Triggers)** — 注入"超载""失稳""未鸣笛""未持证""年检到期"等事件,考察 Agent 应对。
4. **跨标对比 / Cross-Standard Validation** — 同一场景在 GB 43657 / ISO 23308 / EN 16796 三个口径下对比,识别不一致点。
5. **版本演进追踪 / Version Evolution** — 标准每年更新,Benchmark 须支持配置版本号,测试 Agent 对新标的鲁棒性。

---

> **版权 / Copyright**:本文件基于杨鹏飞 / 微信公众号「叉车技术老炮」维护的叉车专家技能 (forklift-expert)整理,遵循 CC BY-NC 4.0 + 严禁商用附加条款。
