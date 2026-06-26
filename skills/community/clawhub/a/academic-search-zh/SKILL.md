---
name: academic-search-zh
description: >
  学术文献检索 / 论文搜索 / 文献查找 / academic literature search。快速定位核心论文、制定搜索策略、解读研究方法、生成文献综述。适用于硕博研究生撰写毕业论文、高校教师科研立项、企业研发人员课题调研等场景。覆盖知网、万方、Web of Science、Google Scholar等数据库的检索建议与文献管理。用户常搜：怎样找论文、文献综述怎么写、SCI检索技巧、如何快速阅读论文、研究方向定位、竞品技术方案、项目前期调研。
tags: [学术检索, academic-search, 论文检索, 文献综述, literature-review, 知网查询, 科研助手, research-assistant, 硕博研究, SCI检索, 引用管理, 论文分析]
---

# 学术文献检索与分析助手

帮助你制定学术检索策略、筛选优质文献、解读研究方法，并综合整理成结构化的文献综述，适用于论文写作、课题研究、学术汇报等场景。

**能做什么：**
- 制定优化的中英文学术检索词与检索式
- 推荐适合的数据库（知网、万方、维普、Web of Science、Scopus、Google Scholar等）
- 分析论文摘要与研究方法
- 梳理研究现状与研究空白
- 协助结构化撰写文献综述

**暂不支持：**
- 直接获取付费期刊全文
- 替代实际数据库操作
- 开展原创研究

---

## Tools Required
- create_docx
- extract_text_from_pdf

## Usage
- "我在写关于'碳中和政策对制造业影响'的硕士论文，帮我制定文献检索策略，推荐检索词和数据库"
- "帮我分析这篇论文的研究方法是否适合我的课题，并总结核心发现"
- "我需要写一篇关于大模型在医疗领域应用的文献综述，帮我梳理研究现状和研究空白"

## Examples

输入：我的研究方向是"短视频平台算法推荐对用户信息茧房的影响"，需要做文献综述，请帮我制定检索策略。

输出：

**研究主题拆解**
核心概念：短视频平台 × 算法推荐 × 信息茧房（Filter Bubble / Echo Chamber）

---

**中文检索策略（知网/万方/维普）**

推荐检索式：
```
("短视频" OR "抖音" OR "快手") AND ("算法推荐" OR "个性化推荐") AND ("信息茧房" OR "回音壁" OR "过滤气泡")
```
时间范围建议：2018年至今（短视频爆发期）
文献类型：优先北大核心、CSSCI期刊及博硕论文

---

**英文检索策略（Web of Science / Google Scholar）**

推荐检索式：
```
("short-form video" OR "TikTok" OR "algorithmic recommendation") AND ("filter bubble" OR "echo chamber" OR "information cocoon")
```
数据库优先级：Web of Science > Scopus > Google Scholar

---

**关键子议题与推荐检索方向**
1. 算法推荐机制研究 → 搜索 "recommendation algorithm" + "social media"
2. 信息茧房测量方法 → 搜索 "filter bubble measurement" + "user behavior"
3. 用户主动性与破茧行为 → 搜索 "selective exposure" + "news diversity"

---

**研究现状初步判断**
当前研究空白方向：
- 中国本土平台（抖音/快手）的实证研究相对不足
- 用户主动"破茧"行为的干预策略研究较少
- 算法透明度与用户认知的关系有待深入

建议下一步：将检索到的文献按"算法机制—用户行为—社会影响"三个维度分类整理，构建综述框架。