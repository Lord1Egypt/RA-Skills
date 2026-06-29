# 如何把这个 Skill 导入 GetClawHub

约 5 分钟。

## 第一步：打开文件
打开 `skill/SKILL.md`，找到 `## System Prompt（整段复制到 GetClawHub）`。

## 第二步：新建 Skill
GetClawHub → 左侧 Skills → 「+ New Skill」

## 第三步：填字段
| GetClawHub 字段 | 值 |
|----------------|-----|
| Skill Name | `fp_community_insight` |
| Display Name | 社区热点痛点分析 |
| Description | （复制 frontmatter 的 description） |
| System Prompt | `## System Prompt` 下全部内容 |
| Model | `claude-sonnet-4-6` |
| Temperature | `0.6` |
| Max Tokens | `2000` |

> ⚠️ 完整粘贴 System Prompt，尤其是"合规与安全标注"部分——
> DPF delete 在美国违法，这部分漏了可能产出违规选题。

## 第四步：准备输入数据
两种方式：
1. **自动**：跑 `fp_weekly_crawl.sh`（在 fp-skills 库里）抓 Reddit/论坛，
   把输出的 jsonl 数据粘进来
2. **手动**：复制一批热帖的标题 + 评论摘要粘进来（起步阶段可用）

## 第五步：测试
用 `examples/example_community_insight.md` 里的输入跑一遍，对照输出看质量。

## 第六步：检查
用 `reference/输出质量checklist.md` 抽查，重点看：
- 选题是否具体可用
- DPF 等合规话题是否标注了风险

---

## 怎么用（每周流程）
1. 周一：跑 Agent-Reach 抓 Reddit + 论坛
2. 把数据粘进本 Skill → 得到痛点报告 + 选题
3. 周二选题会：用报告定本周内容方向
4. 把选好的选题复制给：
   - `fp_youtube_script`（做视频脚本）
   - `fp_blog_to_social`（做文章+四平台）
   - `fp_facebook_pro_post`（做FB科普）

一条"挖痛点 → 出内容 → 分发"的闭环就跑起来了。
