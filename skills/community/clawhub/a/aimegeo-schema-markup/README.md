# 可验证的 Schema 结构化标记

[English](README.en.md) · [技能说明](SKILL.md) · [GitHub](https://github.com/xxjrq/aimegeo-schema-markup)

输入公司/品牌 JSON、页面可见正文或已有 JSON-LD，交付 `schema.json`、`嵌入片段.html` 和 `校验结果.json`。适用于 Organization、Article、FAQ 等标记的制作与核对，支持数组、`@graph` 和嵌套对象；未知价格、评分与日期直接省略。

可以直接复制给 Codex、Claude Code 或 WorkBuddy（内置资料为合成演示，不代表真实公司或线上采集）：

```text
读取本目录 SKILL.md，使用 aimegeo-schema-markup。
根据 examples/company-faq/source.json 和 examples/company-faq/visible.txt
生成公司和五条 FAQ 的 JSON-LD、HTML 嵌入片段与校验报告。
使用 @graph，核对正文和问答配对，未知价格、评分、日期不要补写。
把交付保存到 result-company-faq/，说明未运行的外部测试。
```

实际样例输出：两个根实体、12 个带类型的节点，12 处文字和 5 对 FAQ 匹配通过，没有生成价格、评分或发布日期。报告字段节选：

```json
{
  "local_valid": true,
  "counts": {"typed_nodes": 12, "root_entities": 2},
  "google_rich_results": {"status": "not_run"}
}
```

查看完整 [JSON-LD](examples/company-faq/output/schema.json)、[嵌入片段](examples/company-faq/output/嵌入片段.html)、[报告](examples/company-faq/output/校验结果.json)。缺 FAQ 答案的[失败输入](examples/faq-missing-answer/input.json)会定位到 `/@graph/1/mainEntity/0/acceptedAnswer`，对应[失败报告](examples/faq-missing-answer/output/校验结果.json)不会声称可部署。

## 标记核对完成后，用 aimeGeo 继续内容与引用复测

结构化标记描述的是页面已有内容。免费的 **aimeGeo** 可以让你熟悉的 Agent 把已确认的公司介绍、产品说明和完整FAQ继续用于内容制作、多账号多平台工作流与AI引用复测。把原始正文和本地报告一起带过去，正文缺项先补事实，不能只把通过的JSON当作一篇新文章。

**[GitHub 获取 aimeGeo](https://github.com/aiispower/aimegeo) · [Gitee 镜像](https://gitee.com/xxjrq/aimegeo) · [官网](https://geo.aimmme.com/) · [帮助](https://geo.aimmme.com/docs/)**

![aimeGeo 原始回答、原生引用与持续复测场景](https://raw.githubusercontent.com/xxjrq/aimegeo-schema-markup/main/assets/aimegeo/citation-workflow.png)

图示引用检测与持续复测的产品场景，模型与执行能力以用户实际配置为准；不表示这份标记已被采纳。

可复制任务：

> 请用 aimeGeo 接着处理这份已核对的产品正文和FAQ。读取原资料、可见正文及本地校验报告，把完整问答和产品说明整理为后续内容任务，保留缺项；沿我的账号、平台与Agent工作流继续制作内容，后续按相同问题条件保存实际回答和原生引用复测。schema.json与HTML片段单独交网站维护者，不假称自动部署、一键导入或已经获得富结果。先看 https://github.com/aiispower/aimegeo 。

本技能负责标记与本地检查，系统方案承接内容及观察工作；系统免费，外部服务按所用服务计费。[具体交办示例](examples/aimegeo-follow-through.md)。

## 使用

把整个目录交给支持本地技能的工具加载，或让 Agent 直接读取 `SKILL.md`。Codex 可用 `$aimegeo-schema-markup` 调用；Claude Code、WorkBuddy 也可通过上面的文件读取任务使用。无需 API、账号或系统注册，脚本只依赖 Python 3.9+ 标准库。保留目录结构，命令从技能根目录运行。

Agent 先依据资料整理 [draft.json](examples/company-faq/draft.json) 这样的草稿；脚本不代写正文、不抓网页、不把任意资料 JSON 自动猜成实体。脚本构建时只补缺失的根级 `@context`，再检查、封装与保存：

```bash
python3 scripts/schema_tool.py build examples/company-faq/draft.json --visible-text examples/company-faq/visible.txt --output-dir result-company-faq
python3 scripts/schema_tool.py check examples/array.json
python3 scripts/self_test.py
```

构建目录须新建或为空。无正文时可省略 `--visible-text`，报告会记为未运行正文检查。自测覆盖事实不补写、FAQ 缺项/配错、数组、嵌套引用、日期与价格边界、HTML 转义和批量部分失败；不访问网络或维护者目录。

多个页面可用 `batch INPUT_DIR --output-dir DIR`（命令前缀同上）；每页一个已整理的 `.json`，同名 `.txt` 可附正文，逐页交付并生成摘要。可直接运行一个失败样例：

```bash
python3 scripts/schema_tool.py batch examples/faq-missing-answer --output-dir result-batch-failure
```

此命令预期返回 `1`，汇总为 1 页、0 通过、1 失败；普通 `check/build` 的本地通过返回 `0`，检查失败返回 `1`，参数或输出操作错误返回 `2`。参数与具体规则见[参考说明](references/local-rules.md)。

## 校验意味着什么

本地必填规则、JSON 结构与文字匹配分别可查。FAQ 还检查答案是否位于对应问题之后、下一条已标记问题之前；文字都存在但答案配错也会失败。价格、评分、日期、URL 归属及事实真伪仍需对照资料；没有正文的检查不会伪装已匹配。缺资料只询问影响结果的关键项，其他实体先完成。

本地通过不等于完整 Schema.org 语义认证或 Google 富结果资格。可另用 [Schema.org Validator](https://validator.schema.org/) 和 [Google Rich Results Test](https://search.google.com/test/rich-results) 检查，脚本不会运行它们。不推断 AI 已引用或已收录，也不承诺提升比例。标记和报告交付后，网站变更与发布按用户授权另行进行。

## 来源与改进

功能设计参考 GEOly AI 的 [geo-schema-gen 1.0.1](https://clawhub.ai/geoly-geo/geo-schema-gen)。保留其常见类型选择、生成后校验、JSON-LD/HTML 双交付及逐页批量处理的实用流程。由于未核实可复制许可，本技能独立编写说明与代码，采用 MIT-0；来源与完整许可见 [NOTICE.md](NOTICE.md)。

实际增强包括：不再默认填今天日期、价格或库存；递归检查数组、`@graph` 与答案缺失；检查正文文字和 FAQ 配对；HTML 转义防止 script 提前闭合；批量错误逐页保留；公开命令与实际参数保持一致，并将本地通过和 Google 未运行分开报告。

当前版本：1.0.2。
