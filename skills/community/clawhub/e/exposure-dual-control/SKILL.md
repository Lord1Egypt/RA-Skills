---
name: exposure-dual-control
description: |
  用户在纠结光圈和快门速度的选择、问"怎么设置曝光参数"、或想理解曝光的创造性效果时调用。
  不适用于测光表使用问题（应调用 light-meter-compensation）、胶片选择问题、或纯器材参数查询。
  Invoke when the user is deciding between aperture and shutter speed, asking about
  exposure settings, or wants to understand the creative effects of exposure.
  Not for light-meter usage (use light-meter-compensation), film selection, or
  pure gear spec queries.
  关键 trigger / Key triggers: "光圈快门怎么设"、"曝光参数"、"aperture shutter speed"、
  "景深怎么控制"、"运动模糊"、"exposure settings"、"how to set exposure"、
  "aperture vs shutter speed"。
source_book: 《纽约摄影学院摄影教程》 美国纽约摄影学院
source_chapter: 第二章 p020-p023, 第三章 p062-p068
tags: [exposure, aperture, shutter-speed, creative-control]
related_skills: []
---

# 曝光双变量决策法

## R — 原文 (Reading)

> "任何两只镜头，只要它们设定的f值相同，那么它们所传送的光量就是完全一样的...从一挡速度移动到下一挡更快的速度时，总是将曝光时间削减一半...正确的快门速度是能够获得所需效果的速度，快门速度将有助于表现作品的主题。"
>
> — 美国纽约摄影学院，第二章/第三章

---

## I — 方法论骨架 (Interpretation)

曝光的核心不是"让照片不黑不白"，而是两个创造性变量的组合决策。变量一：孔径（f值）——控制两个效果，一是进入相机的光量（f值越小光量越大），二是景深（f值越大景深越大，背景越清晰）。变量二：快门速度——也控制两个效果，一是曝光时间（速度越快光量越少），二是运动表现（速度越快越能凝固运动，速度越慢越能表现动感）。两个变量通过互易律相互补偿（开大一挡光圈=加快一挡快门，曝光量不变），但创造性效果截然不同。决策时先问"我需要多大景深"确定光圈，再问"我需要怎样的运动表现"确定快门，最后用互易律微调使曝光量正确。

---

## A1 — 书中的应用 (Past Application)

### 案例 1: 职业摄影师运用快门速度捕捉水
- **问题**: 如何用快门速度表现水的不同质感
- **方法论的使用**: 伊凡·马萨尔用高速快门停住水面一切运动呈现绝对安宁；彼得·西蒙用高速+逆光捕捉海浪喷溅的冰雕感；迈克尔·曼海姆用极慢快门让海水变成"安琪儿头发"。
- **结论**: 同一场景用不同快门速度可以创造完全不同的艺术效果
- **结果**: 证明了"正确的快门速度是能获得所需效果的速度"

### 案例 2: 中国象棋棋子景深实验
- **问题**: 直观展示光圈对景深的控制效果
- **方法论的使用**: 所有照片聚焦在"马"上，只改变孔径：f/2时只有"马"清晰；f/8时前面的"兵"和后面的"车"进入清晰范围；f/16时四个棋子都相当清晰。
- **结论**: 孔径是控制景深最直接的手段
- **结果**: 成为教学中的经典演示案例

---

## A2 — 触发场景 (Future Trigger)

### 用户会在什么情境下需要这个 skill?
1. 拍摄前纠结"用大光圈还是小光圈"、"用高速快门还是慢速快门"
2. 问"为什么同一场景不同参数拍出来感觉不同"
3. 想理解曝光的创造性效果（不只是技术正确）
4. 问"怎么拍出背景虚化的人像"或"怎么拍出流水的丝滑感"

### 语言信号
- "光圈快门怎么设？"
- "怎么控制景深？"
- "怎么拍出运动模糊/凝固运动？"
- "aperture vs shutter speed"
- "exposure settings for portrait/landscape"
- "bokeh background blur"

### 与相邻 skill 的区分
- 与 `depth-of-field-control` 的区别：本 skill 是曝光的全局决策框架（光圈+快门），depth-of-field-control 专门深入景深的三因素控制。
- 与 `light-meter-compensation` 的区别：本 skill 解决"选什么参数"，light-meter-compensation 解决"测光表读数不准怎么办"。
- 与 `shutter-speed-motion` 的区别：本 skill 是双变量全局框架，shutter-speed-motion 专门深入快门与运动表现的四因素决策。

---

## E — 可执行步骤 (Execution)

当 skill 被激活后，agent 应按以下步骤执行：

1. **确定景深需求**
   - 完成标准: 明确用户需要浅景深（背景虚化隔离主体）还是大景深（全景清晰）
   - 浅景深→选大孔径（小f值如f/1.4-f/2.8）；大景深→选小孔径（大f值如f/8-f/16）

2. **确定运动表现需求**
   - 完成标准: 明确用户需要凝固运动还是表现动感
   - 凝固运动→选高速快门（1/500秒以上）；表现动感→选慢速快门（1/60秒以下）或追随拍摄

3. **用互易律匹配曝光量**
   - 完成标准: 根据测光表读数或经验，调整光圈和快门使曝光量正确
   - 规则: 开大一挡光圈=加快一挡快门，曝光量不变
   - 判停条件: 若景深需求和运动需求冲突（如要浅景深但要慢速快门）→ 使用ND镜或提高ISO

4. **给出具体参数建议**
   - 完成标准: 给出至少一组具体的光圈+快门速度组合，并说明创造性效果

---

## B — 边界 (Boundary)

### 不要在以下情况使用此 skill
- 测光表读数不准/曝光补偿问题 → 应调用 light-meter-compensation
- 胶片/ISO选择问题 → 不涉及感光度选择
- 纯器材参数查询（如"f/2.8是什么意思"）→ 属于知识查询

### 作者在书中警告的失败模式
- 完全依赖程序曝光模式，放弃创造性控制
- 混淆镜头"快慢"（光量传送能力）与捕捉快速运动的能力

### 作者的盲点 / 时代局限
- 基于胶片时代，数码时代可通过后期调整部分弥补曝光偏差
- 未涉及数码传感器的ISO性能优势（高ISO噪点控制远优于胶片）

### 容易混淆的邻近方法论
- 互易律在极短/极长曝光下会失效（互易律失效），此时不能简单互换

---

## 相关 skills (阶段 3 填充)

- depends-on: light-meter-compensation（先正确测光，再选择参数）
- composes-with: depth-of-field-control（景深是三因素控制，光圈只是其中之一）
- composes-with: shutter-speed-motion（快门速度选择需考虑四因素）
- contrasts-with: auto-exposure-limitation（手动决策 vs 程序自动）

---

## 审计信息

- **验证通过**: V1 ✓ / V2 ✓ / V3 ✓
- **测试通过率**: 待测试
- **蒸馏时间**: 2026-08-03
