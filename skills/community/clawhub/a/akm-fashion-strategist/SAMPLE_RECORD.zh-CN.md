<!--
文件：SAMPLE_RECORD.zh-CN.md
核心功能：提供 AKM Fashion 的中文脱敏样本，展示输入快照、结构化记录、决策输出与变化原因。
输入：真实穿搭使用记录的轻脱敏重写版。
输出：供 GitHub 中文页、ClawHub 溯源码或内部审阅者快速理解 Fashion skill 工作流的公开样本。
-->

# Fashion 脱敏样本

## 输入快照

- 主场景：城市通勤 + 半正式白天会面
- 体型语境：希望视觉纵向更利落，避免显腰宽的轮廓
- 功能约束：需要活动舒适、天气适配、口袋实用
- 现有衣橱现实：深色裤装可用项不少，轻薄外层偏弱，低信号上装偏多
- 反偏好：避免大 logo、松垮街头比例、戏服感正装
- 采购容忍度：低频购买，优先精准补缺而不是大规模换新

## 结构化记录

```yaml
Profile:
  ScenePriority:
    1: 通勤
    2: 半正式会面
    3: 日常社交
  BodyContext:
    desired_signal:
      - 纵向更干净
      - 轮廓利落但不僵硬
    avoid:
      - 放大腰部的叠穿
      - 低结构、显拖沓的上装
  WardrobeAssets:
    strong_items:
      - 深色锥形裤
      - 简洁皮鞋
      - 中性色针织基础层
    weak_items:
      - 适合过渡天气的轻外层
      - 更适合会面场景的高信号上装
  FunctionalNeeds:
    - 行动舒适
    - 天气适配
    - 口袋实用
  AntiPatterns:
    - 过度宽松街头拖垮比例
    - 高调品牌标识
    - 仪式感过强的正装
  PurchaseTolerance:
    strategy: 低频精准补件
```

## 决策输出

```yaml
SceneJudgment: 衣橱可用，但外层偏弱
OutfitRecommendation:
  - 深色锥形裤
  - 干净的中性色针织或结构化 Polo
  - 轻薄深色 overshirt 或无衬结构夹克
  - 简洁皮鞋
WhyThisWorks:
  - 保持纵向比例干净
  - 对会面场景足够得体，又不显过度正式
  - 通勤时仍保留活动舒适度
GapAnalysis:
  - 缺少一件能同时覆盖通勤与会面场景的稳定轻外层
PurchasePriority:
  1: 深色轻薄 overshirt 或软结构夹克
  2: 一件领口存在感更强的中性色上装
MissingInputs: []
```

## 为什么输出变了

这个决策不是从“smart casual 怎么穿”这种泛化建议开始的。
它之所以改变，是因为有效方案必须同时满足五个具体约束：

1. 通勤和会面场景要共存
2. 体型线条问题排除了厚重膨胀式叠穿
3. 现有衣橱资产限制了立刻可推荐的组合
4. 功能性和审美必须同时满足
5. 采购容忍度决定了优先补一个关键缺口，而不是整体翻新

最后产出的不是 moodboard 式语言，而是由画像、资产和场景逻辑共同约束出的衣橱决策。
