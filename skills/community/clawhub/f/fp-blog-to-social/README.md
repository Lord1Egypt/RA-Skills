# fp_blog_to_social — Blog 一文多发 Skill（炼化版 v1.0）

一个可直接导入 GetClawHub 的 Skill，把一篇 FridayParts Blog 文章一键拆解为 **Facebook、Instagram、X、TikTok** 四个平台的内容，每个平台都是对应的原生风格。

**这是最高 ROI 的 Skill** —— Blog 每周 4-5 篇，每篇拆解从 20-40 分钟降到 60 秒。

---

## 📦 文件库结构

```
fp-blog-skill/
├── README.md                       ← 本文件
├── skill/
│   └── SKILL.md                    ← Skill 本体（导入这个）
├── examples/
│   └── example_blog_to_social.md   ← 2个真实样例（故障类+对比类）
├── reference/
│   └── 平台风格checklist.md         ← 四平台输出抽查清单
└── docs/
    └── 如何导入GetClawHub.md         ← 5分钟导入教程
```

---

## 🚀 怎么用（3 步）

1. **导入**：照 `docs/如何导入GetClawHub.md`，把 `skill/SKILL.md` 导入 GetClawHub。
2. **测试**：用 `examples/` 的主题跑一遍，对照样例看四平台输出质量。
3. **验证**：用 `reference/平台风格checklist.md` 抽查，过了就投产。

---

## ✨ 解决什么问题

| | 之前 | 之后 |
|---|------|------|
| 流程 | 每篇 Blog 为 4 个平台各写一遍 | 复制标题+摘要 → 一键四平台 |
| 耗时 | 20-40 分钟/篇 | 60 秒/篇 |
| 一致性 | 各平台容易脱节 | 核心信息一致，风格各异 |

---

## 🎯 关键设计：四平台真正差异化

不是把同一段复制四遍，而是按平台调性改写：

| 平台 | 开头 | 长度 | 特点 |
|------|------|------|------|
| Facebook | 问句切入 | 长（科普） | 完整解释 + 官网引导，3-4 hashtag |
| Instagram | 钩子+emoji | 短 | 情绪化、节奏快，8 hashtag |
| X | 直接进主题 | 中 | 符号清单、信息密集，2-3 hashtag |
| TikTok | 制造张力的一句话 | 极短 | 只为前 3 秒留人 |

---

## 🔬 技术类内容自动"留余地"

当 Blog 是 How-to 或故障类内容时，社媒文案也会避免误导——和 `fp_youtube_script` 用同一套准确性逻辑：

- 故障归因用 "can / may / could be"，不写死成 "always / the only"
- 例：coolant temp 灯 → "could be low coolant or a stuck thermostat"（留余地）
  而不是 "means your thermostat is broken"（绝对化）

见 `examples/` 里 CAT 警告灯样例的实际表述。

---

## 📝 关于运营 SOP

SKILL.md 预留了三个可扩展占位区：
- `[品牌词规范]`、`[Hashtag偏好]`、`[CTA规范]`

拿到运营 SOP 后填进去即可，无需重写。

---

## ⚙️ 配置参数

| 参数 | 值 |
|------|-----|
| Model | claude-sonnet-4-6 |
| Temperature | 0.65 |
| Max Tokens | 1500 |

---

## 🔗 在工作流里的位置

- Blog 上线 → 本 Skill 拆四平台 → 各平台发布
- 进阶：搭 Chain，输入 Blog URL 自动抓正文 → 本 Skill → 四平台内容
- 配合 `fp_x_sync`、`fp_instagram_emotion` 等做二次精修
