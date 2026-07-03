# fp_facebook_pro_post — FB 专业内容生成 Skill（炼化版 v1.0）

一个可直接导入 GetClawHub 的 Skill，生成 FridayParts Facebook 帖子，四种类型一键切换：**行业科普、客户好评、KOL推广、热点营销**。

---

## 📦 文件库结构

```
fp-facebook-skill/
├── README.md                        ← 本文件
├── skill/
│   └── SKILL.md                     ← Skill 本体（导入这个）
├── examples/
│   └── example_facebook_posts.md    ← 四种类型各一条真实样例
├── reference/
│   └── 输出质量checklist.md          ← 输出抽查清单
└── docs/
    └── 如何导入GetClawHub.md          ← 5分钟导入教程
```

---

## 🚀 怎么用（3 步）
1. **导入**：照 `docs/如何导入GetClawHub.md`，把 `skill/SKILL.md` 导入。
2. **测试**：用 `examples/` 任一类型跑一遍。
3. **验证**：用 `reference/输出质量checklist.md` 抽查。

---

## ✨ 四种类型

| 类型 | 用途 | 关键规则 |
|------|------|---------|
| A 科普 | 行业知识 | 问句开头，技术内容留余地 |
| B 客评 | Google Review 转背书 | quote ≤15词（硬规则） |
| C KOL | 合作视频配文 | KOL故事+点出FP配件 |
| D 热点 | 节点借势 | 结尾提问引互动 |

每条输出：正文 + Hashtag + 配图建议。

---

## 🎯 两个内置硬规则
1. **客评 quote ≤15 个英文单词** —— 超了自动转述，避免大段照搬
2. **技术类内容留余地** —— 故障原因用 often/may，不绝对化（和内容线其他 Skill 一致）

---

## 📝 微调（后续）
SKILL.md 预留占位区，想调直接改，不用重写：
- `[风格偏好]` —— 想更糙的工地口吻 / 更克制专业
- `[品牌词规范]`、`[固定CTA话术]`、`[优先Hashtag]`

---

## ⚙️ 配置参数
| 参数 | 值 |
|------|-----|
| Model | claude-sonnet-4-6 |
| Temperature | 0.7 |
| Max Tokens | 800 |

---

## 🔗 配合其他 Skill
- 发完 FB → `fp_x_sync` 同步成 X 版本
- Blog 上线 → `fp_blog_to_social` 出 FB 版（互补）
