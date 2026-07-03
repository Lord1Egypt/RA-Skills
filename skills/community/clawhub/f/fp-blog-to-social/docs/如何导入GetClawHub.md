# 如何把这个 Skill 导入 GetClawHub

约 5 分钟。

## 第一步：打开文件
打开 `skill/SKILL.md`，找到 `## System Prompt（整段复制到 GetClawHub）` 那一段。

## 第二步：新建 Skill
GetClawHub → 左侧 Skills → 「+ New Skill」

## 第三步：填字段
| GetClawHub 字段 | 值 |
|----------------|-----|
| Skill Name | `fp_blog_to_social` |
| Display Name | Blog 一文多发 |
| Description | （复制 frontmatter 的 description） |
| System Prompt | `## System Prompt` 下全部内容 |
| Model | `claude-sonnet-4-6` |
| Temperature | `0.65` |
| Max Tokens | `1500` |

> ⚠️ System Prompt 要完整粘贴，尤其是四个平台的格式规范和技术准确性规范。

## 第四步：测试
用 `examples/` 里的测试输入跑一遍：
```
标题：CAT 警告灯含义解读
摘要：解释 CAT 设备常见的几个警告灯（机油压力、冷却液温度、电池/充电系统），
每个灯亮起时该先检查什么，什么情况要立即停机，什么情况可以继续观察。
```
对照 `examples/example_blog_to_social.md` 看输出是否接近。

## 第五步：检查
用 `reference/平台风格checklist.md` 抽查四个平台输出。

---

## 怎么用（日常）
1. Blog 新文章上线 → 复制标题 + 摘要（200字内）
2. 粘进这个 Skill → 拿到四平台内容
3. 用 checklist 快速过一遍 → 微调 → 发布
4. 一篇 Blog 60 秒变四平台内容

## 配合 Chain 使用（进阶）
所有 Skill 跑稳后，可在 GetClawHub 搭 Chain：
输入 Blog URL → 自动抓正文 → 本 Skill → 四平台内容 → （可选）配图 → 发布
