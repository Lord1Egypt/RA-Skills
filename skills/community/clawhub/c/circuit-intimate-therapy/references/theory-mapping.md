# Part 6:与亲密关系理论的对应

## 使用方式

按相关度从强到弱分三档,标出**概念→电路元件**的对应。

读取本份的典型场景:
- 用户从一个心理学理论提问,问"它在电路里对应什么"
- 用户从一个电路结构提问,问"它在 Miller/Gottman/Rusbult 哪一章"
- 用户准备讲座 / 写论文,需要一份对照速查表

不要全部展开;按用户问的章节挑出来。

---

## 第一档:核心同构

### ch11-conflict(冲突)

| 概念 | 电路对应 |
|---|---|
| **Gottman volatile** 多变型 | 串联 LC,小 R,Q 高 → 燃烧型 |
| **Gottman validator** 确认型 | 并联共轭 + 适度 R → 健康临界阻尼 |
| **Gottman avoider** 逃避型 | 大 R,小 L 小 C → 室友型,纯阻性扁平 |
| **Gottman hostile** 敌对型 | 不稳定根,DC 反向 → 振荡发散 |
| **Negative affect reciprocity** | 正反馈振荡:每次过零反向都被对方放大,Q 值越来越高 |
| **Demand/withdraw** | LC 振荡 + 半波整流二极管对 |
| **Triggering events** | 电压脉冲激发 LC 自由响应 |
| **Voice/Loyalty/Exit/Neglect** | 电流的四条出路 |

### ch13-dissolution(解体)

| 概念 | 电路对应 |
|---|---|
| **Vulnerability-Stress-Adaptation 模型(Karney & Bradbury)** | **RLC + V + 时间** —— 这个心理学模型本身就是系统响应论的口语版 |
| **Barrier model** | DC 偏置 + 反向二极管 |
| **Enduring dynamics** | 内在 L 值,不随事件改变 |
| **Emergent distress** | 振荡幅度增长直到 \|AC\| > \|DC\| |
| **Disillusionment** | DC 偏置随时间衰减 |

### ch06-interdependence(相互依赖)

Rusbult 投入模型核心量直接对应电路工作点描述:

| 概念 | 电路对应 |
|---|---|
| Comparison Level (CL) | 期望工作点电流 |
| CLalt 替代水平 | 外部电路电压 |
| Investment 投入 | L 增大 |
| Commitment 承诺 | DC 偏置 |
| Equity 公平 | 阻抗匹配 |
| Communal vs exchange | 不同电路拓扑 |

### ch14-maintenance-repair(维持和修复)

所有维持机制都是**主动调整 RLC + 二极管**:

| 维持机制 | 电路操作 |
|---|---|
| Cognitive interdependence | 串联改并联共轭("一模一样" → "互补不同") |
| Positive illusions | 整流二极管 + 稳压器,维护 DC 偏置 |
| Inattention to / derogation of alternatives | 关闭通向 CLalt 的旁路开关 |
| Sacrifice | 主动加 R / 单向二极管 |
| Accommodation | 负向脉冲到来时手动注入阻尼 |
| Michelangelo phenomenon | 双方相互调谐 L 值 |
| PREP / couple therapy | 整体电路重设计 |

### ch08-love(爱情)

Sternberg 三角理论 = 电路三大维度:

| 三角分量 | 电路对应 |
|---|---|
| **Intimacy** 亲密 | LC 谐振腔(内部能量交换的活跃度) |
| **Passion** 激情 | 振荡幅度 / Q 值 |
| **Commitment** 承诺 | DC 偏置 |

| 爱的类型 | 电路特征 |
|---|---|
| 浪漫之爱 | 高 Q + 中亲密 + 低 DC → 易过零反向 |
| 相伴之爱 | 中亲密 + 低 Q + 高 DC → 稳态低戏剧 |
| 完美之爱 | 三者都强(健康共轭 + 强 DC + 适度 Q) |

**Coolidge effect** = 电容饱和效应:同一电源充电久了梯度趋零,新源接入响应剧烈。

### ch01-building-blocks(关系构成)

依恋类型 = L 的特征分类:

| 依恋类型 | 电路特征 |
|---|---|
| Secure 安全型 | 健康 L + 适度阻尼 |
| Preoccupied 沉迷型 | 高 L 高 Q,焦虑振荡 |
| Dismissing 疏离型 | 大 R,主动断开 LC + 入向二极管 |
| Fearful 恐惧型 | 双稳态 LC,工作点跳变 |

- **Big Five 神经质** = Q 值的人格底色:|Z| 对压力的敏感度
- **Sociometer 自尊(Leary)** = photodiode + DC 偏置传感器

→ 推荐演示:`app04-attachment.html` 直接对比四种类型的波形

---

## 第二档:局部强相关

### ch03-attraction(吸引力)

| 概念 | 电路对应 |
|---|---|
| Similarity | 串联结构倾向 → "灵魂伴侣即燃烧" |
| Complementarity | **并联共轭**的前提 |
| Reactance / Romeo-Juliet effect | 电感反激 + Zener 击穿 |
| Mere exposure 曝光效应 | L 累积过程:重复通电使磁芯磁化 |

### ch05-communication(沟通)

| 概念 | 电路对应 |
|---|---|
| Responsiveness 应答性 | 并联共轭的实际运行机制 |
| Social penetration theory | 逐步建立 LC 容量 + 自我表露阈值 |
| Interpersonal gap 人际隔阂 | 阻抗失配,信号反射 |
| Active listening / validation | 桥式整流器 |
| Microexpressions | 次阈值漏电流 |

### ch10-stress-strain(压力与紧张)

| 概念 | 电路对应 |
|---|---|
| Reactive jealousy | 强迫响应:外部脉冲驱动 LC |
| Suspicious jealousy | LC 自激振荡(无外部输入,脑补能量循环) |
| Betrayal | 反极性大电流注入打穿 DC |
| Forgiveness | Zener + 通过 R 耗散反向电荷 |
| Truth bias | 输入端整流器 |
| Hurt feelings | 非对称二极管阈值 |

### ch07-friendship(友谊)

| 概念 | 电路对应 |
|---|---|
| Invisible support 无形支持 | 高 R 但隐藏阻尼 |
| Capitalization 资本化(Gable) | LED + photodiode 配对 |
| Dyadic withdrawal 二元退缩 | 高 Q LC 切断外部端口 |
| Socioemotional selectivity 社会情绪选择性 | 老年期主动调小带宽 |

---

## 第三档:局部接口

### ch04-social-cognition

- **Positive illusions / Self-fulfilling prophecy** = DC 偏置维护机制
- **Confirmation bias** = 高 Q 窄带滤波器 + 整流器
- **Self-serving bias** = 双向整流器
- **Reconstructive memory** = 时间维度整流器

### ch12-power-violence

- **I³ 模型(Instigation/Impellance/Inhibition)** = V / Z / R 三件套
- **Principle of lesser interest** = 高阻抗者主导回路
- **Intimate terrorism** = 低 Zener 阈值的故意设计
- **Situational couple violence** = 偶发瞬态雪崩

### ch02-research-methods、ch09-sexuality

主要不在动力学层面(测量学 / 具体行为内容),与电路结构接口较弱。
- 可以把测量学问题映射成"传感器精度"
- 把 sociosexual orientation 之类的稳态偏好映射成 DC 偏置基线
- 但不必强行套

---

## 反向速查:从电路到章节

| 电路结构 | 主要章节 |
|---|---|
| RLC 元件基础 | ch01, ch06, ch11 |
| DC 偏置 | ch06(commitment),ch08(三角),ch13(barrier),ch14(maintenance) |
| Z 向量 / 五种家庭 | ch11(Gottman) |
| 串/并联共轭 | ch03(complementarity),ch05(responsiveness),ch14 |
| 阻尼 | ch11(冲突收尾),ch10(应激恢复) |
| 单向二极管 | ch01(dismissing),ch11(stonewalling),ch12(权力不对称) |
| 阈值二极管 | ch05(self-disclosure),ch11(triggering events) |
| Zener | ch03(reactance),ch10(forgiveness/betrayal),ch12(intimate terrorism) |
| 整流 | ch04(社会认知),ch10(truth bias),ch14(positive illusions) |
| 半波整流回路 | ch11(demand-withdraw) |
| LED-photodiode | ch07(capitalization) |
| photodiode + DC | ch01(sociometer),ch10(ostracism) |
| VSA 时间演化 | ch13 |

---

## 理论文献基础(完整列表)

- **Karney & Bradbury (1995)** —— Vulnerability-Stress-Adaptation Model
- **Rusbult** —— Investment Model(commitment, satisfaction, alternatives, investment)
- **Gottman** —— 夫妻类型(volatile / validator / avoider / hostile)、四骑士、5:1 比例
- **Sternberg** —— 爱情三角理论(intimacy / passion / commitment)
- **Bartholomew & Horowitz** —— 依恋四类型
- **Murray** —— Positive Illusions
- **Leary & Baumeister** —— Sociometer Hypothesis
- **Bowen** —— Differentiation of Self
- **Christensen & Heavey** —— Demand/Withdraw Pattern
- **Gable** —— Capitalization
- **Bolger** —— Invisible Support
- **Finkel** —— I³ Model
- **Johnson** —— Intimate Terrorism vs. Situational Couple Violence
- **Miller** —— 《Intimate Relationships》(Ch. 1–14)
