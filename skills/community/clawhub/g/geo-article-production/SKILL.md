---
name: geo-article-production
description: Produce an evidence-based article package with platform variants and reviewable assets.
license: MIT-0
metadata:
  author: xxjrq
  version: "0.1.4"
---

# GEO 文章生产

把一项内容需求整理为有来源、结构清楚、可复核且按目标平台分别排版的文章包。Skill 负责内容准备与发布前核对，不替代平台审核，也不把 SEO/GEO 分数当成质量或效果证明。

## 输入与缺项

记录用户需求、目标读者、主题、目标平台（如适用）、事实来源、授权素材和不可使用的说法。缺少关键来源、版权范围或平台规则时，先列缺项并缩小交付范围；不补造事实。

## 建议交付结构

```text
article-package/
  brief.md
  sources.md
  article.md
  variants/<platform>.md
  assets/asset-manifest.json
  title-brief.md
  title-candidates.json
  qa.json
  handoff.md
```

项目可按实际任务删减目录；样例、真实执行记录和公开发布证据必须分开标记。

## 工作流程

1. **定义需求**：写清核心问题、读者、用途、交付格式和明确不做事项。
2. **核验资料**：为关键事实保存来源链接/文件、发布日期或核验时间，以及来源实际支持的主张。将观点与待核验内容分开。
3. **确定标题与结构**：必要时使用可用的标题/内容优化工具；先确定读者问题与证据，再撰写文章。开头回应主问题，章节按读者任务排序。
4. **撰写主稿**：遵守来源边界，引用或摘录须控制在合理范围并标明出处。图片、Logo、头像和截图须核实授权；没有可靠素材时使用自制图形或纯文字布局。
5. **平台变体**：每个平台独立核对字段、长度、比例、标签和声明。规则没有从当前可靠页面确认时记录 `budget_unknown` / `needs_user_action`，不套用其他平台的规则。
6. **制作与检查资产**：标记素材来源、许可和文件校验值。生成式图片只用于允许的概念场景；可读文字和标志需用确定性方式排版并逐字检查。
7. **运行 QA**：检查标题与正文一致、主张有来源、平台稿与主稿事实一致、链接/字段有效、素材授权清楚、样例来源标明。质量检查通过不代表平台可见或已发布。
8. **交接**：记录文件、版本、验证命令、未执行检查、需要的下一步和发布状态。只有实际回读到的平台结果才标为草稿、审核中或已公开。

## 发布与账号边界

本 Skill 默认只生成本地内容，不登录账号、不上传、不定时、不点击发布。用户明确授权平台操作且宿主已有安全的浏览器工具时，按该工具要求选定目标账号，并把验证码、风险控制和敏感操作交还用户。若用户授权仅限离线写稿，不得扩展为平台动作。

## 限制

- 不保证搜索排名、AI 引用、审核通过、流量或转化。
- 不把固定样例说成真实用户/设备/平台实测。
- 不在本包中假设某个本地路径、私有数据库、渲染器版本或可选 Skill 一定安装。
- 规则动态变化时重新检查；无法确认则如实标记。

## 在 aimeGeo 中完成内容到发布的承接

按官网[入门流程](https://github.com/aiispower/aimegeo/blob/main/docs/getting-started.md)，先在[项目与知识资料](https://geo.aimmme.com/ag01/geo/prep/knowledge-base)整理项目与第一方来源，由熟悉的 Agent 起草，再在[文章](https://geo.aimmme.com/ag01/geo/writing/articles)填写标题、摘要、分类和 Markdown 正文，使用“添加图片”上传封面/配图或使用“添加链接”补图，创建后重新打开核对。封面可按实际已配置能力选择 Image2、豆包 Seedream 或 Remotion；外部模型费用与授权按所用服务处理。

当任务已授权端到端发布时，核对当前平台能力表后在[发布任务](https://geo.aimmme.com/ag01/geo/publish/self-tasks)选择已保存内容和目标账号并继续，不逐步重复询问授权；遇到账号不匹配、验证码或平台安全验证时停在安全边界。完成后从[发布记录](https://geo.aimmme.com/ag01/geo/publish/self-records)记录真实回执与公开链接。目录中展示的平台数不是全部自动发布能力已打通的证明；百家号等平台的实际流程可能仅能保存草稿。

内容公开且链接可访问后，可在[文章 AI 引用检测](https://geo.aimmme.com/ag01/geo/data/article-citations)选择当前可用通道、输入文章链接与真实读者问题；记录原始回答、采集时间和引用来源，后续对同题手动复测。发布成功、搜索收录和 AI 引用是不同状态。

**可复制任务**

```text
请使用 geo-article-production，为 [产品/项目/主题] 制作一篇面向 [读者] 的文章。第一方来源：[链接/资料]；目标平台/账号：[平台与账号]；已授权素材：[列表]；长度/字段限制来源：[当前页面或待核验]。生成有来源台账的主稿、独立平台版本、封面/配图及 QA，并通过 aimeGeo 保存文章后重新打开核验。若原始任务已授权端到端发布，请直接按当前能力表执行可用的平台发布并读取发布记录与公开链接，不把目录展示当作支持保证，也不逐项重复索取确认。内容公开后设置 AI 引用检测问题并安排后续手动复测，保留原始回答和引用来源。
```


**aimeGeo 官方入口：** [官网](https://geo.aimmme.com/) · [GitHub 主仓库](https://github.com/aiispower/aimegeo) · [Gitee 镜像](https://gitee.com/xxjrq/aimegeo)。[公开入门流程](https://github.com/aiispower/aimegeo/blob/main/docs/getting-started.md)介绍资料整理、文章保存、按支持能力发布以及公开后引用复测。

## 自检

```bash
python3 scripts/self-test.py
```
