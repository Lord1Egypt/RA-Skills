# GLOSSARY — cite-holmes 正词表

> cite-holmes 的领域词汇纪律：报告、文档、JSON 字段与对话使用同一套词。
> **有主见**：同一概念只认一个正词，其余写法进 _Avoid_——报告语言与你的语言永远对得齐。
> 纯词汇表：零实现细节（实现看 `references/verification-details.md`，判定看 `--explain`）。

## 判定（五种状态，报告与 JSON 的 `verdict` 字段）

**verified**:
来源存在、层级权威、注册库登记元数据与声称一致——可支撑正文结论。
_Avoid_: 通过、可信、真实、success、ok

**partial**:
可达但有降级因素（社区层级/字段缺失/元数据存疑/撤稿/语义否定）——降级使用。
_Avoid_: 存疑引用、半可信、warning

**unreachable**:
本次抓取失败（着陆页 404/超时/反爬——传输层拿不到页面）——不等于不存在，转人工复核；
注意与「注册库查询确凿查无」区分，后者归 invalid。
_Avoid_: 死链、失败引用、broken

**invalid**:
标识符不存在、指向错误论文或拼接伪造——机械层确凿判死，不得引用。
_Avoid_: 假引用（口语可用但报告不用）、错误引用、reject

**unverified**:
未执行检查（离线模式或跳过）——联网重跑才有真实判定。
_Avoid_: 未验、pending、unchecked

## 核验对象与结构

**claim-triplet**:
语义层最小验证单元：主语–关系–宾语，把"这段是否被支撑"拆到"哪半句有问题"。
_Avoid_: 三元组校验、assertion triple

**in-text 标记**:
正文里的引用记号（[12] / [1-4] / (Smith, 2023) / doi.org 链接）——`--check-document` 的解析对象。
_Avoid_: 行内引用、citation marker（中文语境用标记）

**锚词率**:
引用句与被引标题的内容词重合度——低只代表"疑似错配，人工复核"，不是判定。
_Avoid_: 匹配率、相似度（相似度专指标题比对值）

## 评分与台账

**CiteScore**:
整份清单的 0–100 置信度分（A–D 级），报告头部第一眼数字。
_Avoid_: 置信分、健康分、health score

**BLUF 报头**:
报告开头的双读者结构：机器可解析 YAML（verdict/key_numbers/blocker/next_action）+ 人类 5 行 TL;DR。
_Avoid_: 摘要头、front block

**工作底稿**:
`--export auditjson` 产出的逐项检查明细——每条判定的可追溯证据链。
_Avoid_: 审计日志、debug 信息

## v3.10+ 信号（线索与提示，均非判定）

**克隆引用对**:
同一标题挂多个不同 DOI、或同一 DOI 挂不同标题——成对警示，至少一个标识有误。
_Avoid_: 重复引用（那是 mark_duplicates 的真重复合并）、duplicate

**跨语言桥接**:
中文原题对英文登记名时的三级核验（双语 original-title → DOI 落地页 → OpenAlex）——命中升 verified，未命中维持 partial。
_Avoid_: 翻译比对、多语言匹配

**清单画像**:
整批参考文献表的统计指纹筛查（标识符近邻簇/年份集中/信源集中/裸条目）——旗标是人工抽查建议。
_Avoid_: 批量检测、画像评分（画像无评分）

**预印本升级提示**:
arXiv 引用已登记正式发表时的注记（附期刊版 DOI）——提交前完成版本升级。
_Avoid_: 版本警告、preprint alarm

**导出完整度**:
verified 条目可从注册库 CSL 回填的导出字段计分（0–100）——告诉你差哪些字段。
_Avoid_: 质量分、字段分

## 错误码（`error_codes` 字段，12 类，机器可读）

错误码是五态之上的**原因细分**（如 E_DOI_NOT_FOUND / E_TITLE_MISMATCH / E_CROSS_LANG），
人话翻译见 `--explain N` 输出。
_Avoid_: 错误类型、异常码

## 环境与模式

**注册库**:
官方学术数据源：DOI.org、Crossref、PubMed E-utilities、arXiv API、OpenAlex、Semantic Scholar、Retraction Watch、Wayback。
_Avoid_: 数据库（太泛）、第三方源（S2/OpenAlex 是确认源，注册库是判定源）

**网络降级**:
批内多个主机传输连续失败后的快速诚实跳过模式——一次快速诚实的通过胜过几分钟干等。
_Avoid_: 离线模式（--offline 是主动选择，降级是被动保护）

**注册库预检**:
`--preflight`：跑批前看各官方源可达性状态。
_Avoid_: 健康检查（那是 --doctor 的环境自检）
