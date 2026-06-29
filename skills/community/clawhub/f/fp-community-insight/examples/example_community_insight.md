# 示例输出：社区热点痛点分析

用模拟 Agent-Reach 抓取的 Reddit 热帖数据跑的真实输出。

---

## 输入（模拟 Agent-Reach 抓取的热帖数据）

```
r/skidsteer: "Bobcat S650 overheating after 20 min, already replaced water pump"
  (87赞, 评论里多人说先查恒温器和散热器)
r/heavyequipment: "DEF system fault keeps coming back on my CAT, dealer wants $2k" (142赞)
r/Construction: "Hydraulic fluid leaking but can't find where, anyone dealt with this" (63赞)
r/mechanics: "What's the actual difference between OEM and aftermarket parts, worth the price?"
  (200+赞, 大量讨论)
r/kubota: "U35 won't regen, limp mode, DPF clogged" (54赞)
r/tractors: "John Deere fuel filter part number lookup is impossible" (78赞)
r/skidsteer: "Bobcat error code L7404, what does it mean" (41赞)
r/heavyequipment: "DPF delete vs cleaning, what do you guys do" (评论分歧大)
```

---

## 输出（Skill 生成）

### ① 本周热门话题 Top 5

**1. 设备过热，先换水泵却没解决（约2-3帖在讨论）**
典型帖："Bobcat S650 overheating after 20 min, already replaced water pump"
用户已经换了水泵但问题还在，评论区反复提醒先查恒温器、散热器、冷却液。这是个高频误判场景。

**2. 后处理系统故障(DEF/DPF/regen)反复出现（讨论量最大，3+帖）**
典型帖："DEF system fault keeps coming back"、"U35 won't regen, limp mode, DPF clogged"
用户被后处理系统折磨，经销商报价高($2k)，很多人想自己搞或考虑 DPF delete。情绪强烈（贵+反复+停机）。

**3. OEM vs 售后件值不值（单帖200+赞，讨论最热）**
典型帖："What's the actual difference between OEM and aftermarket parts, worth the price?"
这是机械师群体的长期争论，直接关系到 FridayParts 的核心卖点。

**4. 零件型号查询困难（2帖）**
典型帖："John Deere fuel filter part number lookup is impossible"
用户找不到正确的零件号，这是采购前的真实障碍。

**5. 故障代码看不懂（2帖）**
典型帖："Bobcat error code L7404, what does it mean"
用户遇到代码不知含义，需要解读。

### ② 高频用户痛点（按出现频率+情绪强度）

1. **后处理系统(DPF/DEF/regen)反复故障 + 维修贵** —— 出现最多，情绪最强
2. **过热问题误判**（以为是水泵，其实可能是恒温器/散热器）
3. **OEM vs 售后件该怎么选** —— 决策困惑，直接影响购买
4. **零件号查不到** —— 采购障碍
5. **故障代码不懂** —— 需要解读

### ③ FridayParts 可切入的内容机会（可直接做选题）

1. **【YouTube脚本】"换了水泵还过热？这3个地方先别漏"**
   回应痛点2，接你们已有的水泵恒温器脚本，可做系列。

2. **【YouTube脚本】"DPF 反复堵塞？清洗 vs 更换前你该知道的"**（合规：只讲清洗/维护，不碰删除）
   回应最热的痛点1，流量潜力大。

3. **【Blog + FB】"OEM vs 售后件：5个真实区别"**
   回应痛点3，正打 FridayParts 核心卖点，适合做权威科普。

4. **【Blog】"John Deere 零件号怎么查"系列**
   回应痛点4，FP 有零件查询能力，可引流到官网工具。

5. **【FB/INS 短科普】"Bobcat 常见故障代码速查"**
   回应痛点5，可做成系列卡片内容。

### ④ 趋势信号

- **后处理系统(DPF/DEF)相关讨论量明显上升**，且情绪负面（贵、反复、停机），是值得持续追踪的内容富矿。
- **DPF delete 话题分歧大** —— 用户在讨论，但 FridayParts 内容应聚焦合规的清洗/维护方向，不碰删除（合规风险）。

---

## 这版输出的几个亮点

| 特点 | 说明 |
|------|------|
| 不只罗列 | 把8条帖聚类成5个话题，按讨论量排序 |
| 痛点排序 | 按"频率+情绪强度"排，最痛的排最前 |
| 选题可直接用 | 每个选题像真标题，并标注适合哪个下游 Skill |
| 主动标合规 | DPF delete 标注"只讲维护不碰删除"（美国删除后处理系统违法） |
| 闭环衔接 | 选题1直接接已有的水泵恒温器 YouTube 脚本，形成系列 |

---

## 怎么接下游

把③里的选题复制给对应 Skill：
- 选题1、2 → 喂给 `fp_youtube_script`，做成完整视频脚本
- 选题3、4 → 喂给 `fp_blog_to_social`，做成 Blog + 四平台内容
- 选题5 → 喂给 `fp_facebook_pro_post`，做成 FB 科普

一条"社区挖痛点 → AI 出内容 → 多平台分发"的闭环就跑通了。
