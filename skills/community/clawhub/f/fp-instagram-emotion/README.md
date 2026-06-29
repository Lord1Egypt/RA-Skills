# fp_instagram_emotion — INS 情绪内容 Skill（含 Meme，炼化版 v1.0）

一个可直接导入 GetClawHub 的 Skill，生成 FridayParts Instagram 情绪驱动内容，主力是**机械圈 Meme**，另含展会动态、KOL Reel 文案。

**核心：用机械师真实痛点做梗，不是泛泛的情绪。**

---

## 📦 文件库结构

```
fp-instagram-skill/
├── README.md                        ← 本文件
├── skill/
│   └── SKILL.md                     ← Skill 本体（导入这个）
├── examples/
│   └── example_instagram_meme.md    ← 3个Meme样例 + 梗强弱评估 ★
├── reference/
│   └── 输出质量checklist.md          ← 输出抽查清单
└── docs/
    └── 如何导入GetClawHub.md          ← 5分钟导入教程
```

---

## 🚀 怎么用（3 步）
1. **导入**：照 `docs/如何导入GetClawHub.md`，把 `skill/SKILL.md` 导入。
2. **测试**：用 `examples/` 的 Meme 输入跑，对照梗评估看效果。
3. **验证**：用 `reference/输出质量checklist.md` 抽查梗强弱。

---

## 🎯 三种内容类型

| 类型 | 用途 |
|------|------|
| Meme（主力） | Drake / This is Fine / Distracted Boyfriend / Two Buttons 模板 |
| 展会动态 | 参展现场感内容 |
| KOL Reel | 合作视频竖屏文案 |

---

## ✨ 关键设计：会判断"梗到不到位"

Skill 的 System Prompt 内置了做梗的判断标准：
- **强梗** = 戳机械师独有的痛（设备专挑工期坏、OEM报价一堆零）
- **弱梗** = 泛泛情绪（被新机器吸引——换别的行业也成立）

`examples/` 里跑了3个真实 Meme 并标了强弱：
- This is Fine（设备专挑工期坏）→ ✅✅ 最强
- Drake（OEM高价）→ ✅ 到位
- Distracted Boyfriend（被新机器吸引）→ ⚠️ 稍弱

这帮你校准 Skill 输出的方向。

---

## 📝 微调（后续）
SKILL.md 预留占位区：
- `[梗的尺度]` —— 想更糙的工地黑话 / 更克制干净
- `[禁用梗]` —— 不能碰的话题
- `[已用过的Meme]` —— 避免重复模板

> 你之前说"后续应该可以微调"——就是改这三个占位区，不用动主体。

---

## ⚙️ 配置参数
| 参数 | 值 |
|------|-----|
| Model | claude-sonnet-4-6 |
| Temperature | 0.85（Meme 需要创意，比其他 Skill 高） |
| Max Tokens | 800 |

---

## 💡 一个判断技巧
如果生成的 Meme 换成别的行业也成立，说明不够"机械圈"，让它重做一个更戳痛点的。
