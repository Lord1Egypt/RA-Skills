<!--
文件：SAMPLE_RECORD.md
核心功能：提供 AKM Fashion 的英文脱敏样本，展示输入快照、结构化记录、决策输出与变化原因。
输入：真实穿搭使用记录的轻脱敏重写版。
输出：供 GitHub、ClawHub 或审阅者快速理解 Fashion skill 工作流的公开样本。
-->

# Fashion Sample Record

## Input Snapshot

- Primary scene: city commuting plus semi-formal daytime meetings
- Body context: wants cleaner vertical lines, avoids silhouettes that widen the waist visually
- Functional constraints: needs comfortable movement, weather adaptability, and practical pocket use
- Current wardrobe reality: several usable dark trousers, limited lightweight outerwear, too many low-signal tops
- Anti-preferences: avoids loud logos, sloppy streetwear proportions, and costume-like formalwear
- Purchase tolerance: low-volume buying, prefer targeted gap-filling over broad shopping

## Structured Record

```yaml
Profile:
  ScenePriority:
    1: commuting
    2: semi-formal meetings
    3: casual social use
  BodyContext:
    desired_signal:
      - cleaner vertical proportion
      - sharper but not rigid silhouette
    avoid:
      - waist-widening layers
      - bulky low-structure tops
  WardrobeAssets:
    strong_items:
      - dark tapered trousers
      - simple leather shoes
      - neutral knit basics
    weak_items:
      - lightweight outer layer for transitional weather
      - high-signal meeting top layer
  FunctionalNeeds:
    - comfortable movement
    - weather adaptability
    - practical pocket utility
  AntiPatterns:
    - oversized streetwear drag
    - loud branding
    - ceremonial formality
  PurchaseTolerance:
    strategy: low-volume targeted additions
```

## Decision Output

```yaml
SceneJudgment: wardrobe-is-usable-but-top-layer-weak
OutfitRecommendation:
  - dark tapered trousers
  - clean neutral knit or structured polo
  - lightweight dark overshirt or unstructured jacket
  - simple leather shoes
WhyThisWorks:
  - keeps vertical line clean
  - stays meeting-appropriate without looking overdressed
  - preserves movement comfort for commuting
GapAnalysis:
  - missing one reliable lightweight outer layer that can bridge commute and meeting scenes
PurchasePriority:
  1: dark lightweight overshirt or soft-structured jacket
  2: one sharper neutral top with better neckline presence
MissingInputs: []
```

## Why This Output Changed

The decision did not start from generic "smart casual" advice.
It changed because the valid solution had to satisfy five concrete constraints at once:

1. commute and meeting scenes had to coexist
2. body line concerns ruled out bulky layering
3. current wardrobe assets limited what could be recommended immediately
4. function mattered alongside aesthetics
5. purchase tolerance favored one precise addition over a full refresh

The result is not moodboard language.
It is a wardrobe decision shaped by profile, assets, and scene logic.
