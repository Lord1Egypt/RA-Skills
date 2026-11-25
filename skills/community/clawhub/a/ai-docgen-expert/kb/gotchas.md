---
type: cross-cutting
name: gotchas
domain: ai-docgen
skill_name: ai-docgen-expert
version: 2
updated: 2026-11-18
subdomains: [doc-taxonomy, api-doc-gen, code-comment, adr-changelog, ai-docgen-workflow, ai-doc-verification, doc-governance, doc-quality]
counts: 19
---

# ai-docgen 全领域坑点 Top 速查（gotchas）

跨 8 个子领域蒸馏的高频坑点清单。

**Top 判定标准（满足其一才入本表）**：

- a) 跨 ≥2 子领域的共性坑；
- b) P0 级——文档事实错误误导用户 / 文档体系崩坏 / 门禁失效；
- c) 静默失效类（无报错但文档已失效）且单领域高频。

不达标的坑点留在各子领域 kb「高频坑点」小节，不入 Top。每条：编号 + 一句话描述 + 详情引用（kb 文件 + 法则编号）；法则编号均为子域编号（DT/AD/CC/AC/AW/AV/DG/DQ）。

## 事实与幻觉类

### [G-1] 无源编造事实数据

签名/参数名/默认值/错误码/版本号/日期/贡献者全是事实数据，无源时以「同类典型形态」补全，编造与事实同形输出、读者无法分流（跨 api-doc-gen/adr-changelog/code-comment/doc-taxonomy，P0）。

详情: kb/api-doc-gen.md §高频坑点（AD-2）；kb/adr-changelog.md §高频坑点（AC-11）；kb/code-comment.md §高频坑点（CC-2）；kb/doc-taxonomy.md §高频坑点（DT-12）

### [G-2] 交叉引用与链接幻觉

`详见 §3.2` 指向不存在章节、`docs/api.md` 目标未创建、`{@link Foo}` 指向不存在的导出、`Closes #123` issue 不存在——引用是「合理想象」而非存在性验证，读者点击 404（跨 4 子域，P0）。

详情: kb/doc-taxonomy.md §高频坑点（DT-12）；kb/api-doc-gen.md §高频坑点（AD-2）；kb/code-comment.md §高频坑点（CC-2）；kb/adr-changelog.md §高频坑点（AC-9）；kb/ai-doc-verification.md §高频坑点（AV-4）

### [G-3] why/决策/动机编造

注释编决策理由、无输入生成完整 ADR forces、explanation 编设计动机——why 是最高价值层同时是模型最无知层，「社区最优解释」冒充项目私有事实（跨 code-comment/adr-changelog/doc-taxonomy，P0）。

详情: kb/code-comment.md §高频坑点（CC-2）；kb/adr-changelog.md §高频坑点（AC-5）；kb/doc-taxonomy.md §最佳实践·场景 5（DT-12）

### [G-4] 编造内容与事实内容同形输出

无置信度分层：幻觉段落与源驱动段落口吻完全相同，审校者无法定位高风险声明（跨 api-doc-gen/code-comment/ai-docgen-workflow，静默失效）。

详情: kb/api-doc-gen.md §高频坑点（AD-2）；kb/ai-docgen-workflow.md §法则（AW-6 来源分级）；kb/code-comment.md §高频坑点（CC-2）

### [G-5] 版本/框架先验误配

旧版语法（React 16 写法/旧版 Node API）输出到新版项目，「v2 起」实际 v2.3 起——版本先验有半衰期，训练截止后的变更一无所知（跨 api-doc-gen/doc-governance，P0）。

详情: kb/api-doc-gen.md §高频坑点（AD-2）；kb/doc-governance.md §高频坑点（DG-6 版本标注进 CI 对账）

## 结构混写类

### [G-6] 类型混写崩塌（blur）

单文档内教程腔+参考腔+解释腔混排，AI 侧成因是逐段局部合理、整体类型漂移；长文档前半守型后半回归默认模板（跨 doc-taxonomy/doc-quality，P0——文档体系崩坏）。

详情: kb/doc-taxonomy.md §高频坑点·Top 1（DT-3/DT-1）；kb/doc-quality.md §法则（DQ-10 判型先于治理）

### [G-7] AI 腔：低信息密度的高完成感

总结癖/对称癖/免责癖/空洞强调十特征；腔在骨架（每节总结、万物三点式）不止在词汇，逐句去腔结构残留则治理无效（跨 doc-quality/ai-docgen-workflow/doc-governance，高频）。

详情: kb/doc-quality.md §高频坑点（DQ-8/DQ-9）；kb/ai-docgen-workflow.md §法则（AW-7 风格锚先行）；kb/doc-governance.md §法则（DG-7/DG-11 组织声音）

### [G-8] 结构幻觉：虚构章节与类目

文档结尾必附凑数 FAQ 三条、虚构 Troubleshooting 三段式、自创 changelog 类目 `Improved`——模板先验压倒实际需要与既有规范（跨 doc-taxonomy/adr-changelog）。

详情: kb/doc-taxonomy.md §高频坑点（DT-10/DT-12）；kb/adr-changelog.md §高频坑点（AC-6 类目以官方六类为准）

### [G-9] 受众混淆与受众漂移

changelog 写成开发者叙述、release notes 写成 commit 复读、文档中途从新手假设滑到专家假设——载体分工与读者假设双双失守（跨 adr-changelog/doc-taxonomy）。

详情: kb/adr-changelog.md §高频坑点（AC-6/AC-10）；kb/doc-taxonomy.md §法则（DT-9 读者假设显式）

## 漂移与失效类

### [G-10] 代码-文档同步漂移

改代码不动旧注释、`@example` 调用三版本前已改名的方法、行为变更后示例输出还是旧字段——注释与示例是 review 盲区，漂移静默发生（跨 code-comment/api-doc-gen/ai-docgen-workflow，静默失效）。

详情: kb/code-comment.md §高频坑点（CC-6）；kb/api-doc-gen.md §高频坑点·Top 2（AD-7）；kb/ai-docgen-workflow.md §法则（AW-1 触发链）

### [G-11] 示例复制即报错

`// ... 其余配置` 省略号、import 缺失、版本沉默假设——示例从未被运行验证（死示例），信任级失效（跨 doc-quality/api-doc-gen，P0）。

详情: kb/doc-quality.md §高频坑点·深度展开 1（DQ-4 示例五性）；kb/api-doc-gen.md §法则（AD-7 示例最小可运行）

### [G-12] 图腐烂

架构图停留在旧架构、二进制图变更不进 diff 无人知晓——图比无图更糟（主动误导）；架构变更无「图更新」触发（doc-quality，静默失效 + 单领域高频）。

详情: kb/doc-quality.md §高频坑点·深度展开 2（DQ-5）

### [G-13] 链接检查把 403 反爬当 BROKEN

`npmjs.com`/`w3.org → 403` 全量报断链淹没真 404，团队因误报关闭整个检查——门禁失效（跨 ai-doc-verification/ai-docgen-workflow）。

详情: kb/ai-doc-verification.md §高频坑点·Top 1（AV-3 三态分类）；kb/ai-docgen-workflow.md §法则（AW-9 外链三态处理）

### [G-14] 覆盖率 Goodhart 与幸存者偏差

注释覆盖率 100% 全是 `// the x` 垃圾凑数；分母来自文档侧致 50 个公共 API 不在分子分母里——度量成为目标后为度量优化取代为质量优化（跨 ai-doc-verification/doc-governance，静默失效）。

详情: kb/ai-doc-verification.md §高频坑点（AV-5 度量配对 + 代码侧分母）；kb/doc-quality.md §法则（DQ-7 Goodhart 防御）

## 流程与门禁类

### [G-15] 零审校直出

AI 生成直接 commit/publish，幻觉长驱直入；「看起来很好」的生成质量让审校显得多余——恰恰是最危险时（跨 ai-docgen-workflow/ai-doc-verification/doc-governance，P0 + 静默失效）。

详情: kb/ai-docgen-workflow.md §高频坑点·坑 1（AW-4/AW-6）；kb/ai-doc-verification.md §法则（AV-8 验收必须外部）；kb/doc-governance.md §法则（DG-10 发布即担责）

### [G-16] AI 加持的大爆炸重写

「一周用 AI 重写全站」开工——风格漂移 + 错误模式全量复制 + 新旧断档三害并发，AI 让大爆炸「更可行」从而更诱人（跨 ai-docgen-workflow/doc-governance，P0——文档体系崩坏）。

详情: kb/ai-docgen-workflow.md §高频坑点·坑 2（AW-2/AW-7）；kb/doc-governance.md §法则（DG-3 演进禁大爆炸）

### [G-17] ADR/追加型历史被原地改写

「更新 ADR-0007」时把原决策内容改成新决策——历史被摧毁；根因是把 ADR 当活文档（文档站思维）而非追加型历史（跨 adr-changelog/ai-docgen-workflow/doc-governance，P0）。

详情: kb/adr-changelog.md §高频坑点·Top 2（AC-4 supersede 流程）；kb/ai-docgen-workflow.md §法则（AW-11 历史记录修改过人工门）；kb/doc-governance.md §法则（DG-10）

### [G-18] 批次错误自相关不扩抽

抽 10 篇发现 2 篇幻觉仍放行同批 90 篇；AI 错误在批次内同模式，发现一处即整批扩抽信号——抽样发现率被当常数（跨 ai-doc-verification/ai-docgen-workflow）。

详情: kb/ai-doc-verification.md §法则（AV-7 发现即扩抽）；kb/ai-docgen-workflow.md §法则（AW-7 批间 checkpoint）

## 台账与生命周期类

### [G-19] 活台账写完即僵尸

台账类活文档（风险登记册/状态报告/检查表/威胁模型）AI 一次生成「完美的初始台账」——状态列全 open、无下次复审日期、缓解措施「持续关注」——写完即过时且看起来不需要更新；活文档缺状态机、复审日期与更新触发机制，静默失效（跨 proj-docs/doc-templates/doc-governance，静默失效 + P0——风险治理空转）。

详情: kb/proj-docs.md §法则（PJ-12 风险登记册活文档：状态机+复审日期+可执行缓解；PJ-14 威胁模型更新触发——OWASP 官方点名「新功能发布/安全事件/架构变更」三触发）；kb/doc-templates.md §法则（PT-13 runbook 保鲜）；kb/doc-governance.md §法则（DG 生命周期处置）

---

未入 Top 的坑点（不达标判定示例）：「锚点 slug 规则平台差异」（单领域、非 P0、可报错——留 kb/ai-doc-verification.md）；「文件头 boilerplate 过长」（单领域、显性可察觉——留 kb/code-comment.md）；「日期格式混乱」（官方已点名、单领域、显性——留 kb/adr-changelog.md）；「过度披露」（治理权衡类非失效类——留 kb/doc-governance.md）。

## 对账记录

| 轮次 | 结果 | 日期 |
|---|---|---|
| 第 2 轮（refresh 补锚） | 豁免——本轮为溯源升级（Conventional Commits 1.0.0 / SemVer 2.0.0 / CODEOWNERS / Google Markdown style / Diátaxis colophon 五锚），未产生达 Top 判定标准的新坑点；CODEOWNERS「最后匹配优先」「OR 审批」等平台语义已写入 kb/doc-governance.md 概念表与冲突消解 #9（单域、显性可查，不入 Top） | 2026-11-17 |
| 第 5 轮（doc-templates 扩展子域） | 豁免——候选「模板八股化」「判据空转」经 Top 判定标准核对不达标：前者单子域（doc-templates）且显性可察觉；后者虽属静默失效类但跨子域证据不足（DG 门禁判定已 lint 化、AV 评审清单域内覆盖），且已由 LAW-17 与 kb/ai-mistakes.md doc-templates 分节覆盖，不重复入 Top；G-1~18 与新子域坑点查重无冲突——PT 域「硬事实编造」为 G-1 在模板场景的实例化，已由 PT-1 域层防御 | 2026-11-17 |
| 第 6 轮（proj-docs 扩展子域） | 新增 G-19（活台账写完即僵尸）——满足判定标准 a+c：跨 proj-docs（风险登记册/威胁模型/检查表）/doc-templates（runbook 保鲜）/doc-governance（生命周期处置）三子域成立，静默失效类（无报错但台账已失效）且台账族生成高频（AI 一次生成完美初始台账的偏置），OWASP 威胁建模页官方点名更新触发事件；候选「规格填充行为」豁免——为 G-1 在规格/断点/SLA 场景的实例化，已由 PT-1/PJ 域层防御；候选「理想态偏科」豁免——由升格的 LAW-18（正常/异常路径并重）承担，不入坑点表 | 2026-11-18 |
| 第 7 轮（refresh 补锚对账） | 豁免——本轮为溯源升级（MADR 官方 spec 站 adr.github.io/madr/ + api-extractor.com 三页两锚补抓），无达 Top 判定标准的新坑点候选；「报告变更漏提交则 PR validation 失败」（api-extractor 官方素材）为工具链机制非 AI 坑点，已写入 kb/api-doc-gen.md 冲突消解 #8（单域显性可查，不入 Top）；G-1~19 与补锚素材核对无冲突 | 2026-11-18 |

## 来源索引

- 来源主体：9 个子领域 kb「高频坑点（速查）」小节的 Top 汇总（Top 判定标准见文首；G-19 为第 6 轮从 proj-docs 子域坑点跨域检验升格，proj-docs 不另设 gotchas 候选池）；每条的「详情」行指向对应 kb 文件与法则编号，此处不重复。
- 官方背书锚（个别坑点）：G-6 混写崩塌官方术语 blur [官方文档](https://diataxis.fr/map/)；G-8 changelog 官方类目与 G-9 commit 复读官方反模式 [官方文档](https://keepachangelog.com/en/1.1.0/)；G-13 三态分类中的 BLOCKED 态为本库 spot_check 内源实践锚；G-15/G-16 的审校与文档修剪纪律同向 [官方文档](https://google.github.io/styleguide/docguide/best_practices.html)；G-19 威胁模型更新触发事件 [官方文档](https://owasp.org/www-community/Threat_Modeling)。
- 其余坑点源自 9 个子领域的模型萃取层，标注 [模型经验]，未经官方文档逐条验证。
