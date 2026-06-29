# 如何把这个 Skill 导入 GetClawHub

约 5 分钟。

## 第一步：打开文件
打开 `skill/SKILL.md`，找到 `## System Prompt（整段复制到 GetClawHub）`。

## 第二步：新建 Skill
GetClawHub → 左侧 Skills → 「+ New Skill」

## 第三步：填字段
| GetClawHub 字段 | 值 |
|----------------|-----|
| Skill Name | `fp_competitor_weekly` |
| Display Name | 竞品周报生成 |
| Description | （复制 frontmatter 的 description） |
| System Prompt | `## System Prompt` 下全部内容 |
| Model | `claude-sonnet-4-6` |
| Temperature | `0.5`（数据分析要稳定准确） |
| Max Tokens | `2000` |

## 第四步：准备两份数据
1. **Socialinsider**：每周一导出竞品 IG/TT/FB 数据，选 CSV 格式
2. **Agent-Reach**：跑爬虫抓竞品 YouTube 数据（fp-skills 库里的脚本）

## 第五步：测试
用 `examples/example_competitor_weekly.md` 里的输入跑一遍，对照输出看质量。
输入时把 A（Socialinsider）和 B（YouTube）两部分都粘进去。

## 第六步：检查
用 `reference/输出质量checklist.md` 抽查，重点看：
- 是不是读出了结论（不是念数据）
- 行动建议能不能直接执行

---

## 怎么用（每周流程）
1. 周一 10:00：Socialinsider 导出 IG/TT/FB CSV
2. 周一同时：Agent-Reach 抓竞品 YouTube 数据
3. 把两份数据都粘进本 Skill → 得到竞品周报
4. 周二选题会：用周报里的"行动建议"定本周内容方向

## 配合其他 Skill
- 周报里发现的爆款形式（如修复连载）→ 可作为 fp_youtube_script 的选题方向
- 周报里的"FB别投入"等结论 → 指导 fp_x_sync / fp_blog_to_social 的平台分配
