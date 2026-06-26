# Part 5:二极管 —— 非线性现象

## 使用方式

只用 RLC 的电路是**线性时不变(LTI)**的,强制现象满足正负对称和叠加性。但很多亲密关系现象**根本不对称、不线性** —— 这是只用 RLC 时显得别扭的地方。

二极管打破 LTI,引入四个新性质:**单向性、正向阈值、反向击穿、整流**。

读取本份的典型场景:
- 用户描述不对称现象(我付出他不接 / 他能伤我我不能伤他 / 他从不让步 / 他什么都吞)
- 询问 Stonewalling、Forgiveness、Reactance、Demand-Withdraw、Capitalization、Sociometer
- 询问积极错觉、验证性偏差、自我服务偏差、重构性记忆、truth bias

按需展开下面 4 个性质中的相关一两个,而非全部。

---

## 1. 单向性(forward conduction / reverse blocking)

二极管允许一个方向通过,阻断另一个方向。

| 现象 | 电路对应 |
|---|---|
| **回避型依恋(Dismissing)** | **入向阻断的二极管**:"我可以走出去关心你,但你的关心传不到我心里来" |
| **Stonewalling 筑墙(Gottman 四骑士)** | 反向截止极致状态:任何形式的输入都不通过 |
| **Sacrifice 牺牲意愿** | 单向能量传输,不预期回流。健康牺牲是**有 Zener 限位的二极管**;无限位的(IPV 受害者)会能量单流到耗尽 |
| **Sexual double standard 性双重标准** | 社会强加的二极管 |
| **Principle of lesser interest 较小利益原则** | 不对称二极管对:利益较小者控制电流方向 |

### 临床判别

问:"什么从对方传到你心里来,什么传不进来?反过来呢?"
→ 找到具体的**导通方向**和**截止方向**,就找到了二极管的极性。

---

## 2. 正向阈值(forward voltage drop)

二极管低于阈值不导通,跨过阈值才有电流 —— 这是 RLC 完全没有的"门槛"行为。

| 现象 | 电路对应 |
|---|---|
| **Social penetration theory 社会渗透** | 自我表露的导通阈值:轻度披露不触发互惠,只有跨过亲密阈值才开启互惠流动 |
| **Triggering events** | 冲突点火阈值:日常小摩擦在阈值下被吸收 |
| **Microexpressions 微表情** | **次阈值漏电流**:在 display rules 关门前的瞬间漏过去 |
| **Hurt feelings 感情创伤** | **非对称阈值**:负向输入的导通阈值远低于正向(损失厌恶在亲密关系里的版本) |

### 临床用途

- 找门槛:"是什么强度的事件之后他/你才真的有反应?"
- 找漏电流:"在他刻意冷静之前,有没有一闪而过的表情?"——这是临床常用的微表情侦测

---

## 3. 反向击穿(Zener / avalanche)

正常二极管反向不通,但反向电压超过阈值会击穿,反向大电流通过。Zener 二极管把击穿做成**可控的稳压器**。

| 现象 | 电路对应 |
|---|---|
| **Romeo-Juliet effect / Reactance** | **经典反向击穿**:父母用反向电压压制爱情,达到 Zener 阈值后反向激出更强烈的爱情 |
| **Forgiveness 宽恕** | **可控的反向通道**:并联一个 Zener,允许在特定条件下让反向电荷耗散,工作点回归 DC 偏置。**没有 Zener 的家庭遇背叛就直接击穿** |
| **Betrayal recovery** | Zener 阈值高低决定能否扛过反向冲击 |
| **Situational vs. Intimate terrorism** | 不同击穿模式:Situational 是偶发瞬态雪崩;Intimate terrorism 是被故意设计成低 Zener 阈值的电路 |

### Zener 阈值的两种失败

- **过低**:风一吹就击穿。轻微批评 / 拒绝 / 拒绝性接触都被解读为关系危机
- **过高**:扛住一切但永远不释放。背叛后强行"原谅"但没真正泄放,反向电荷累积,后期突然崩塌

健康的 Zener 阈值:能扛住日常冲击,在重大伤害时**主动激活**让能量受控泄放。

### 推荐演示

`app10-forgiveness-zener.html` —— 直接看背叛冲击下,Zener 阈值过低 / 过高 / 适中三种结果。

---

## 4. 整流(rectification, AC→DC)

二极管把双向变化的 AC 单向化,从振荡里**提取直流分量** —— 这是认知偏差的电路本质。

| 现象 | 电路对应 |
|---|---|
| **Positive illusions 积极错觉** | **半波整流器**:只让正向情绪事件进入长期记忆,负向被滤掉,从振荡日常里提取稳定正向 DC 偏置(Murray) |
| **Confirmation bias 验证性偏差** | 已有信念是 DC 偏置,新进来的 AC 证据被整流成支持原假设的 DC 增量 |
| **Self-serving bias 自我服务偏差** | **双向整流器**:成功正向通道导通,失败反向通道导通 |
| **Reconstructive memory 重构性记忆** | 时间维度的整流器 |
| **Truth bias 事实偏见** | 输入端整流器,信任低阈值、质疑高阈值 |

### 临床用途

健康关系**需要**适度的积极错觉(Murray):给 DC 偏置充电。完全无整流 = 抑郁性现实主义,DC 维持不住。

但被污染的整流器(强自我服务、强验证性)会让伴侣对同一事件得到完全相反的"客观回顾"——这是 attributional conflict 的电路根源。

---

## 二极管组合 = 复合现象

| 现象 | 电路结构 |
|---|---|
| **Demand/withdraw** | **半波整流回路**:A 的二极管"提出问题"方向导通,B 的二极管"回应"方向反向截止。能量推过来形不成完整回路 |
| **Capitalization 资本化(Gable)** | **LED + photodiode 配对**:分享方点亮(LED),响应方接收转化(photodiode)。一方失效全回路熄灭 |
| **Active listening / Validation** | **桥式整流器**:把对方 AC 情绪(无论正负)翻译成同向 DC 输出 —— 把"愤怒"和"悲伤"都变成连接信号 |

### Demand-Withdraw 推荐演示

`app08-demand-withdraw.html` —— 看 A 推 B 退,挫败电容慢慢充电直到击穿;偶尔"打开"B 的二极管(回应)可以重置回路。

### Capitalization 推荐演示

`app09-capitalization.html` —— 4 种响应风格(Active-Constructive / Active-Destructive / Passive-Constructive / Passive-Destructive)中只有 AC 让 LED-photodiode 回路真正点亮。

---

## Sociometer = photodiode

**Sociometer 自尊(Leary & Baumeister)** 字面上是 photodiode —— 把外部社会关系信号(光)转化为内部电流(自尊),维持自我电路 DC 偏置。

**孤独 / Ostracism** = photodiode 长期处于黑暗:外部无光照,内部 DC 偏置衰减,其他元件失去维持工作点的能力。

→ 这从电路上解释了**社会排斥与生理疼痛激活同一脑区**的现象 —— 都在维护"系统是否有外部能量供应"的同一个监测电路。

---

## RLC 进不去的领域,二极管刚好补上

| RLC 处理不了 | 二极管补上 |
|---|---|
| 不对称的依恋 / 付出 / 权力 | 单向性 |
| 积小不成多但跨阈值突变 | 正向阈值 |
| 反向爆发(逆反、击穿、宽恕) | Zener |
| 双向事实变单向叙事 | 整流 |
| 一推一退的循环卡死 | 半波整流对 |
| 外部认可如何变内部能量 | photodiode |

---

## 推荐演示总览

| 二极管类型 | App |
|---|---|
| 4 种 I-V 曲线总览 | `app07-diode-iv.html` |
| 单向阻断 + Demand-Withdraw 半波整流回路 | `app08-demand-withdraw.html` |
| LED + photodiode 配对 (Capitalization) | `app09-capitalization.html` |
| Zener (Forgiveness / Reactance / Betrayal) | `app10-forgiveness-zener.html` |
