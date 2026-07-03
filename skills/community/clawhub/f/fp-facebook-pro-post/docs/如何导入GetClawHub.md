# 如何把这个 Skill 导入 GetClawHub

约 5 分钟。

## 第一步：打开文件
打开 `skill/SKILL.md`，找到 `## System Prompt（整段复制到 GetClawHub）`。

## 第二步：新建 Skill
GetClawHub → 左侧 Skills → 「+ New Skill」

## 第三步：填字段
| GetClawHub 字段 | 值 |
|----------------|-----|
| Skill Name | `fp_facebook_pro_post` |
| Display Name | FB 专业内容生成 |
| Description | （复制 frontmatter 的 description） |
| System Prompt | `## System Prompt` 下全部内容 |
| Model | `claude-sonnet-4-6` |
| Temperature | `0.7` |
| Max Tokens | `800` |

## 第四步：测试
用 `examples/example_facebook_posts.md` 里任一类型测试，例如：
```
类型：B
素材：Ordered a starter for my old Bobcat, showed up in 2 days and fit perfect. — Dave R.
```
检查输出的 quote 是否≤15词、格式是否对。

## 第五步：检查
用 `reference/输出质量checklist.md` 抽查。

---

## 怎么用（日常）
1. 想发 FB → 确定类型（A科普/B客评/C KOL/D热点）
2. 准备素材 → 输入 Skill
3. 拿到正文+hashtag+配图建议 → 微调 → 发布

## 配合其他 Skill
- 发完 FB → 用 `fp_x_sync` 一键改写成 X 版本同步
- Blog 上线 → 用 `fp_blog_to_social` 出 FB 版（和本 Skill 互补）
