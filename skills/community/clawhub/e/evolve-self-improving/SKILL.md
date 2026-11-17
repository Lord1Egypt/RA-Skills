---
name: evolve-self-improving
description: 在当前对话中自动发现 corrections、feature requests、knowledge gaps 和 errors 四类学习信号，并评估其中已经验证、以后可复用的事实、规则、做法和踩坑；用户无需先说“记住”。适用于“不对，实际应该……/that is outdated”“还能不能……/I wish it could……”“原文或现场和理解不符”“命令非零、异常栈、意外输出、超时或连接失败”，也适用于主动要求记住、复盘、纠正、归档或删除。自动发现只启动评估：明确纠正、稳定能力期望、证据闭环或已收敛诊断满足写入条件才保存；临时诉求、猜测、原始报错和未定位事件不写，也不会后台监听或自行改变行为。
---

# 维护本机知识与经验

## When to use

- **Corrections / 纠正**：出现“不对、实际应该、你说错了、已过时、that is wrong、actually、outdated”等明确修正。自动开始核对；只有用户明确确认或当前权威证据直接闭环才写，未收敛争议不写。
- **Feature requests / 能力期望**：出现“还能不能、我希望、有没有办法、为什么不能、could it、I wish、why can't”等需求。只沉淀跨会话稳定的能力期望、工作偏好或边界，不把本轮追加任务、一次性愿望或未决方案写成认知。
- **Knowledge gaps / 知识缺口**：用户给出此前未知事实，引用文档已过时，或 API、代码、配置、现场行为与既有理解不符。必须完成来源、反证和适用边界闭环后才写；只有差异现象时不写。
- **Errors / 错误**：非零退出、异常栈、意外输出、超时、连接失败或重复故障。至少收敛出可复用的诊断路径、根因、修复条件或防复发护栏才写；原始报错和未定位事件不入库。
- 用户主动话术：“记住这条规则”“把这次踩坑沉淀下来”“复盘一下哪些做法值得保留”“这条旧结论已经错了，请纠正”“归档这个经验”“忘掉我指定的这条记录”。
- 不触发：普通任务完成、未定位的一般错误、猜测、单次临时状态、仅查看或批量处理文件、仅定位项目路径。没有稳定内容时不写。

## Workflow

1. **准备并捕获。** 数据根使用 `~/.agent-knowledge/`。根不存在时，只初始化本流程需要的 `knowledge/{current,archive}/`、`experience/{current,archive}/`、四个空 `INDEX.md`、最小 README 和 `maintenance.md`，不创建其他索引或状态。识别 correction、feature-request、knowledge-gap、error 或主动记忆信号，记录待评估结论、原始证据、适用范围和复核方式；这些词可作为 tags，但不新增类别字段。检查：来源应可回查且结论不是猜测；不通过则不写，必要时最多问一个自然问题。
2. **判断资格和分类。** 稳定条目必须同时满足：有原文件、命令回读、现场或明确确认支持；跨会话仍有意义，易变值只保存权威入口和核验方法；可在相同条件下复用；scope 和不适用边界清楚；已脱敏且能明确归为事实或方法。稳定事实、定义、职责、入口和约束归 knowledge；方法、条件、失败模式和护栏归 experience。检查：五项必须全部成立；不通过则说明为什么未沉淀。
3. **去重、冲突、复现和纠正。** 先读 knowledge/experience 两个 current INDEX，用 title、scope、tags、source 简写和特异概括缩小候选，再比较候选正文的 id、标题、scope、source 和语义；纠错追溯时定向读取 archive INDEX。INDEX 缺失或失配时停止写入，先由本流程重建并验证。等价条目不新增：若后续独立事件与既有条目的问题模式、scope 和实质结论一致，并有新的可回查 source，则在 `recurrence/<entry-id>.md` 追加一条复现证据；同一会话的重复表述、命令重试、连续错误输出、普通读取或引用不计复现。新增复现时结合现场分析它为何再次发生，例如此前未被召回、适用边界判断不准、现场条件已经变化或原结论存在缺口；只把有证据的原因写入该行 `summary`。若新证据足以改变既有经验，则按原有结构修正其适用边界、失败边界、回查方法或实质结论；原因未收敛时只保留复现事实，不强行改写经验。未收敛冲突可同时保留并写明差异；明确证伪时先写带 `supersedes` 的新 current，读回后再把旧条目移入同类 archive。检查：复现 source 不重复，不丢有效 source，经验修正均有新证据支持；不通过则保留原状。
4. **原子写入并读回。** 每条一个 Markdown，knowledge 的 id 使用 `k-` 前缀，experience 使用 `e-` 前缀，文件名等于 id；必填字段恰为 `id/title/scope/tags/learned_at/source`，可选 `supersedes`。使用同目录临时文件写完整内容，校验后原子替换：

   ```markdown
   ---
   id: k-YYYYMMDD-HHmmss-short-slug
   title: 简短标题
   scope: global
   tags: [topic]
   learned_at: YYYY-MM-DD
   source: conversation:<opaque-ref>
   ---
   正文写结论、适用边界和复核方式。
   ```

   正文有效字符不是 token 或英文 word：取第二个 `---` 后的 Markdown，去除空白、标题/列表/引用/代码围栏等控制符、强调或行内代码控制符和链接目标 URL，保留链接文字、正文文字与正文标点，再按 Unicode code point 计数；区间含 300 和 400。knowledge 正文覆盖稳定事实或定义、适用边界、使用方式、回查方法；experience 覆盖适用条件、问题或风险、推荐做法、失败边界、回查方法。禁止用重复句、无意义模板、URL、代码或标点凑字。

   复现记录每个条目最多一个文件，文件名等于 entry id；首次沉淀不算复现，无文件即为 0 次：

   ```markdown
   # e-YYYYMMDD-HHmmss-short-slug 复现记录

   | observed_at | source | scope | signal | summary |
   |---|---|---|---|---|
   | 2026-08-20 | conversation:<opaque-ref> | dataset | correction | 新的独立事件再次证明同一问题模式 |
   ```

   `signal` 只使用 `correction/feature-request/knowledge-gap/error`。每次新增、修改、纠正、复现、归档、移动或删除后，使用随包 `scripts/validate_entries.py render-index --directory <目录>` 生成受影响目录的完整 INDEX 临时文本；条目、复现记录与 INDEX 都校验后再原子替换并读回。检查：运行 `check --file <条目>` 和 `check --root ~/.agent-knowledge/`，确认正文 300–400、复现文件逐行有据且 source 唯一、INDEX 次数和最近日期由证据计算、四索引双射；不通过则恢复本项写前条目、复现记录和索引，不把部分成功说成完成。
5. **自然维护并报告。** 每次被调用时读取 `maintenance.md`；距 `last_reviewed_at` 满 7 天才检查 current 的来源、重复、冲突、过时风险和敏感泄漏，全部成功后写回日期。删除只在用户明确指定条目或范围时执行，先验证目标位于拥有目录且不是链接。检查：逐项读回新增、修改、归档或删除结果；不通过则保留已成功项，用普通话说明权限、磁盘或格式故障和剩余项，不把部分成功说成全部完成。

## Tools and data sources

- 只读原文件、当前代码、配置、命令回读和运行现场；写入范围仅为 `knowledge/`、`experience/`、按需创建的 `recurrence/`、根最小 README 与 `maintenance.md`。
- 使用宿主原生安全文件 API、固定字符串搜索和 Markdown/frontmatter 解析器；随包标准库工具只读校验或把 INDEX 文本输出到 stdout，不直接修改知识库，也不依赖网络、服务或后台任务。
- `source` 可为非空列表；确认只能追加，不能替换原始文件或现场证据。

## Gotchas

- `current` 只表示允许检索的线索，不表示已经验证；`archive` 只供追溯，默认不检索。不要增加 candidate、status、confidence、访问次数或普通使用次数。复现次数只是有独立证据的再次发生记录，不证明正确，也不自动改变排序或 current/archive；复现分析不生成防复发契约，不限制 Agent 结合当前现场自行判断，也不自动下沉为 Skill、项目规则或执行门禁。
- `scope` 选择已明确的最窄范围；易变事实不保存成长期现值。凭据、隐私、客户原文、长会话和未脱敏内容不写入。
- 小修可原位更新；实质纠正必须先保住完整新旧内容再归档。模糊的“忘记”不能扩大成广泛删除。
- 一项失败不回滚其他已验证项；不确定时宁可不写，也不伪造 source 或强行消解冲突。
- 自动触发不等于自动保存：四类信号分别通过确认、稳定性、证据闭环或根因/护栏门槛后才写。
