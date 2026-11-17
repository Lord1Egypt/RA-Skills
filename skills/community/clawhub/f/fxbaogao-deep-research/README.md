# fxbaogao-deep-research

`fxbaogao-deep-research` 是一个面向发现报告（fxbaogao）的 Codex/Claude Skill 和本地工具集，用于把行业、公司或主题研究整理成可追溯、可复核、可交付的研报研究工作区。

它的核心方法是“先想后搜”：先定义研究边界并拆解 MECE 子问题，再调用发现报告接口检索、筛选、精读和交叉验证，最后输出结构化调研报告。

## 适合场景

- 行业、公司、产业链或主题的系统研究。
- 从大量研报中筛选核心材料，而不是只返回搜索结果。
- 需要保留报告 ID、阅读链接、事实卡片和推导过程。
- 需要区分 paragraph 摘要、正文摘录和 PDF 原文精读。

## 能力组成

| 模块 | 说明 |
| --- | --- |
| `SKILL.md` | Skill 入口，定义触发场景、路由规则和硬性约束 |
| `references/api-usage.md` | 发现报告搜索、段落、下载接口说明 |
| `references/research-playbook.md` | 多篇研报深度研究方法 |
| `references/report-reader-playbook.md` | 单篇报告精读方法 |
| `assets/workspace_templates/` | 研究工作区 Markdown 模板 |

## 环境要求

- 支持 Skill 的 Codex / Claude 客户端。
- 有效的发现报告 API key。开通请咨询[发现报告客服（工作日9:00-18:00）](https://www.fxbaogao.com/seo/kefu)。

配置 API key：

```bash
export FXBAOGAO_API_KEY=<your_api_key>
```

## 安装

```bash
git clone git@github.com:fxbaogao/fxbaogao-deep-research.git
cd fxbaogao-deep-research
```

作为本地 Skill 使用时，把整个目录放到客户端的 skills 目录；例如 Claude：

```bash
cp -r fxbaogao-deep-research ~/.claude/skills/
```

Codex 或其它客户端请按其实际 skill 目录配置。

## 使用方式

自然语言触发：

```text
深度调研 光模块行业竞争格局与增长驱动
基于发现报告研究 荣耀终端股份有限公司竞争力
精读报告 5339478，并提炼关键事实和风险
```

多篇深度研究会先输出研究边界、核心问题和 3-7 个 MECE 子问题搜索矩阵，再进入检索。
单篇报告精读会直接走 `references/report-reader-playbook.md`，不会默认创建完整多篇研究工作区。


## 输出工作区

完整多篇研究需要落盘时，默认使用如下结构：

```text
workspace/topic-<主题>-<日期>/
├── REPORT_READER_精读分析.md
├── FINAL_调研报告.md
└── intermediate/
    ├── 00_问题拆解.md
    ├── 01_资料来源.md
    ├── 02_事实卡片.md
    ├── 03_对比框架.md
    └── 04_推导过程.md
```

模板在 `assets/workspace_templates/`。具体写法以 `references/research-playbook.md` 为准。

## 关键约束

- 调用搜索接口前，先产出研究边界和 MECE 子问题搜索矩阵。
- 所有发现报告资料必须保留报告 ID 和官网阅读链接：`https://www.fxbaogao.com/view?id=<reportId>`。
- paragraph 回包只适合快速初筛和轻量研究。
- 正式研究、原文引用、关键数据核验必须下载 PDF 并基于 PDF 原文核对。
- 不伪造作者、机构、日期、摘要、页码或数据口径。

## 文档导航

- API 调用：`references/api-usage.md`
- 多篇研究流程：`references/research-playbook.md`
- 单篇报告精读：`references/report-reader-playbook.md`
- 工作区模板：`assets/workspace_templates/`

## 常见问题

**没有 API key 能用吗？**

不能。搜索、段落和下载接口都需要有效的 `FXBAOGAO_API_KEY`。

**paragraph 和 PDF 精读怎么选？**

快速初筛或轻量研究用 paragraph。正式研究、原文引用和关键数据核验用 PDF 原文。

**可以只研究一篇报告吗？**

可以。给出报告 ID、PDF 或明确报告标题时，Skill 会走单篇精读流程，不默认执行完整多篇研究。

**这和直接搜索发现报告有什么区别？**

本项目不是只返回搜索结果，而是先拆解研究问题，再按子问题检索、筛选核心报告、沉淀事实卡片和推导过程，最终形成可复核报告。

## 致谢

本项目部分思路参考 [deep-research](https://github.com/wshuyi/deep-research)。
