---
name: film-exposure-asymmetry
description: |
  用户在使用胶片拍摄、问"负片和反转片曝光有什么区别"、或面对高反差场景
  需要决定曝光策略时调用。纯数码摄影用户不适用（数码传感器宽容度特性不同）。
  Invoke when the user is shooting film, asks about the difference between negative
  and reversal film exposure, or needs to decide exposure strategy for high-contrast
  film scenes. Not applicable to pure digital photography (sensor latitude differs).
  关键 trigger / Key triggers: "负片曝光"、"反转片曝光"、"slide film exposure"、
  "negative film latitude"、"宁过勿欠"、"宁欠勿过"、
  "high contrast film exposure"、"film exposure strategy"、
  "overexpose or underexpose film"。
source_book: 《纽约摄影学院摄影教程》 美国纽约摄影学院
source_chapter: 第五章 p124-p132
tags: [exposure, film-latitude, negative, reversal-film, asymmetry]
related_skills: []
---

# 胶片曝光不对称法则

## R — 原文 (Reading)

> "对所有的负像胶片（包括黑白底片和彩色负片）来说，曝光过度的宽容度大于曝光不足的宽容度...彩色反转片正好相反！曝光不足的宽容度（约1.5挡）大于曝光过度的宽容度（约1挡）。"
>
> — 美国纽约摄影学院，第五章

---

## I — 方法论骨架 (Interpretation)

负片和反转片的曝光宽容度呈完全相反的不对称分布，这一法则直接决定高反差场景的曝光策略。负片（黑白底片和彩色负片）"宁过勿欠"——曝光过度宽容度约5-7挡，曝光不足宽容度仅约2挡（彩色负片约1挡）。因此高反差场景应以阴影区为基准设置曝光，宁可让强光区过曝也不要让阴影区欠曝。反转片（幻灯片）"宁欠勿过"——曝光不足宽容度约1.5挡，曝光过度宽容度仅约1挡，总宽容度约2.5挡远窄于负片。因此应以强光区为基准，宁可让阴影区欠曝也不要让强光区过曝。彩色反转片还可通过故意欠曝0.5挡来增加色彩饱和度。

---

## A1 — 书中的应用 (Past Application)

### 案例 1: 高反差场景负片曝光
- **问题**: 逆光人像（面部阴影f/2 + 明亮天空f/22），用Plus-X拍摄
- **方法论的使用**: 以阴影区f/2为基础，收缩2挡（Plus-X曝光不足宽容度）→ f/4。验证：阴影区欠2挡（在宽容度内），强光区f/22比f/4大5挡（在5挡过度宽容度内）。
- **结论**: 完美记录双方细节
- **结果**: 验证了负片"宁过勿欠"法则的实用性

### 案例 2: 彩色反转片增加饱和度
- **问题**: 如何让彩色反转片色彩更饱和
- **方法论的使用**: 故意使彩色反转片稍曝光不足约0.5挡（将ISO感光度按150%设置测光表，如ISO100按EI150设置）。
- **结论**: 轻微欠曝可增加色彩饱和度而不损失关键细节
- **结果**: 专业摄影师常用技巧

---

## A2 — 触发场景 (Future Trigger)

### 用户会在什么情境下需要这个 skill?
1. 使用胶片拍摄，不确定曝光应该偏向哪端
2. 问"负片和反转片曝光有什么不同"
3. 高反差胶片场景需要决定曝光策略
4. 想增加彩色反转片的色彩饱和度

### 语言信号
- "负片怎么曝光"
- "反转片/幻灯片曝光"
- "slide film exposure"
- "negative film latitude"
- "宁过勿欠"
- "high contrast film"

### 与相邻 skill 的区分
- 与 `light-meter-compensation` 的区别：本 skill 是胶片宽容度特性决定的曝光策略，light-meter-compensation 是测光操作方法。两者配合使用。
- 与 `exposure-dual-control` 的区别：本 skill 解决"偏向哪端曝光"，exposure-dual-control 解决"选什么参数组合"。

---

## E — 可执行步骤 (Execution)

当 skill 被激活后，agent 应按以下步骤执行：

1. **确认胶片类型**
   - 完成标准: 明确用户使用负片（黑白/彩色负片）还是反转片（幻灯片）
   - 判停条件: 若数码摄影→说明数码传感器宽容度特性不同，本法则不直接适用

2. **负片策略：宁过勿欠**
   - 完成标准: 以阴影区（最暗的重要区域）为基准设置曝光
   - 彩色负片: 对阴影区测光后收缩1挡光圈
   - 黑白负片: 对阴影区测光后收缩约2挡光圈
   - 可接受强光区过曝

3. **反转片策略：宁欠勿过**
   - 完成标准: 以强光区（最亮的重要区域）为基准设置曝光
   - 对强光区测光，如需看清细节则开大1挡光圈
   - 可接受阴影区欠曝变黑
   - 极力推荐分界曝光法（拍2-3张不同曝光）

4. **增加饱和度技巧（彩色反转片）**
   - 完成标准: 若用户想增加色彩饱和度，建议故意欠曝0.5挡
   - 方法: 将ISO按150%设置（ISO100→EI150）

---

## B — 边界 (Boundary)

### 不要在以下情况使用此 skill
- 数码摄影 → 数码传感器宽容度特性不同（现代微单约12-15挡，且对称性更好）
- 纯测光操作问题 → 应调用 light-meter-compensation
- 光圈快门创意选择 → 应调用 exposure-dual-control

### 作者在书中警告的失败模式
- 反转片总宽容度仅约2.5挡，曝光稍有偏差就可能毁坏影像
- 强迫显影可增加感光度但有代价（颗粒度、反差、偏色）

### 作者的盲点 / 时代局限
- 全书基于胶片时代，数码时代此法则的适用性大幅降低
- 现代彩色负片（如Portra）宽容度可达10挡以上，远超书中数据
- 数码RAW格式允许后期大幅调整曝光，削弱了"一次拍对"的紧迫性

---

## 相关 skills (阶段 3 填充)

- composes-with: light-meter-compensation（测光方法+曝光策略配合使用）
- contrasts-with: exposure-dual-control（曝光偏向策略 vs 参数创意选择）

---

## 审计信息

- **验证通过**: V1 ✓ / V2 ✓ / V3 ✓
- **测试通过率**: 待测试
- **蒸馏时间**: 2026-08-03
