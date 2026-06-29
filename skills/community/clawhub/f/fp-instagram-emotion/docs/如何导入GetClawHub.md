# 如何把这个 Skill 导入 GetClawHub

约 5 分钟。

## 第一步：打开文件
打开 `skill/SKILL.md`，找到 `## System Prompt（整段复制到 GetClawHub）`。

## 第二步：新建 Skill
GetClawHub → 左侧 Skills → 「+ New Skill」

## 第三步：填字段
| GetClawHub 字段 | 值 |
|----------------|-----|
| Skill Name | `fp_instagram_emotion` |
| Display Name | INS 情绪内容（含Meme） |
| Description | （复制 frontmatter 的 description） |
| System Prompt | `## System Prompt` 下全部内容 |
| Model | `claude-sonnet-4-6` |
| Temperature | `0.85`（Meme 需要创意） |
| Max Tokens | `800` |

## 第四步：测试
用 `examples/example_instagram_meme.md` 里的输入测试，例如：
```
类型：Meme
素材：又一根液压管在工期最紧时爆了
模板：This is Fine
```
对照样例看梗到不到位。

## 第五步：检查
用 `reference/输出质量checklist.md` 抽查，重点看"梗强弱判断"那条。

---

## 怎么用（日常）
1. 想发 Meme → 给场景 + 选模板（或让 Skill 自己挑）
2. 拿到图片文字建议 + caption + hashtag
3. 配图（用 meme 模板图 + 文字）→ 发布

## 一个判断技巧
如果生成的 Meme 换成别的行业也成立，说明不够"机械圈"，让它重做一个更戳痛点的。
