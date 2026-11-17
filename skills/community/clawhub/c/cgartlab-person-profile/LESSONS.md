# LESSONS — person-profile

> 通用人物档案 Skill：结构化创建 / 维护 / 校验人物档案（11 节模板 + 16 条写作硬规矩 + 5 级证据分级 + 全库校验脚本），每条事实可核验、每份档案可自我证伪。
> 本仓库从真实失误沉淀的「教训→规则」清单。**会话开始先全文阅读并遵循其中所有规则**；出现新失误按 §维护 追加。
> 权威依据：Anthropic Claude Code memory/best practices（<200 行、具体可验证、第二次犯同样错即写入）；社区 lessons.md 惯例（Boris Cherny，Anthropic）。
> 来源：本仓库 SKILL.md 的 Pitfalls / 硬规矩 + 已验证 fix 提交；预填为种子，后续由 Agent 在真实工作中增长。

## 维护
- **触发**：用户纠正 / Agent 自查到的失误 / 非显而易见的 gotcha。
- **格式**：`### <主题>` 下，每条 = 失误（具体场景）→ 规则（最小可执行指令），一行可验证。
- **只记项目特有、不可从代码推断的**；通用最佳实践不写；含糊措辞（"小心""注意"）删掉。
- **重复出现** → 升级进 `AGENTS.md` 硬规则；**月度审阅**裁剪过期项；目标 < 200 行。

## 立项与事实纪律

- 失误：不问定位就开工，起点数据全错（阮一峰档案：任务给的"2007 年创建博客 / 2014 年创刊周刊"，实际是 2003-12 和 2018-04-23）→ 规则：建档前必答 3 问（档案定位 / 信息源范围 / 交付形态），不问不开工（见 SKILL.md「[1] 立项澄清」）
- 失误：抓不到资料就凭记忆构造 URL → 规则：抓不到写「未取得」，绝不凭记忆构造 URL（见 SKILL.md「[2] 前置研究」）
- 失误：来源冲突时替老板择一 → 规则：两说并列，不择一（见 SKILL.md「Pitfalls」）
- 失误：只搜正面不搜反面，档案变宣传稿 → 规则：委派研究必须含「商业化与争议」线（见 SKILL.md「[2] 前置研究」）
- 失误：凭印象写 GitHub 数字 → 规则：必须走 API 拉，README 声明与 API 返回不一致时都列（见 SKILL.md「Pitfalls」）
- 失误：机构自述当事实用 → 规则：机构自述不能当事实；5 级证据身份分级写进可信度章节（见 SKILL.md「[2] 前置研究」）

## 结构与格式

- 失误：章节标题级别用了 `#` 或 `###` → 规则：11 节标题必须全为 `##`，名称与顺序不可增删改（见 SKILL.md「[3] 起草」）
- 失误：正文用破折号 / 商业黑话 / 模型路标词 → 规则：禁 `——`/`—`/`–`，禁闭环/赋能/抓手等，禁"值得注意的是/本质上/由此可见/总之"（见 SKILL.md「[3] 起草」）
- 失误：成稿残留模板 HTML 注释 → 规则：起草期可保留，落盘前删除（见 SKILL.md「特殊场景」）
- 失误：frontmatter 残留 `author: ChatGPT` → 规则：逐份扫，模板红线禁止（见 SKILL.md「Pitfalls」）
- 失误：历史档案商业黑话与破折号违规累积 → 规则：`scripts/validate_library.py` 全库校验，违规要修（commit 7afe39c）
- 失误：章节顺序靠记忆 → 规则：用 `required_sections` 列表按模板顺序校验（见 SKILL.md「Pitfalls」）
- 失误：长度不足 300 行就交 → 规则：质量底线 ≥ 300 行（不含 frontmatter），参考标杆 Dan Koe.md / 阮一峰.md（见 SKILL.md「[3] 起草」）

## 补链与校验

- 失误：补链凭空制造合作 / 影响关系 → 规则：查不到就写「无可核实交集」，否定结论要写（见 SKILL.md「[4] 补双向链」）
- 失误：批量改格式没跑校验 → 规则：先 dry-run 报告偏差 → 老板明确许可 → 执行 → 再校验 100% 通过 → 人工 spot-check 3-5 份（见 SKILL.md「[6] 格式统一校验」）
- 失误：校验器把书名号内的破折号误报为违规 → 规则：`check_prohibitions` 要识别 `《》`，书名内破折号不算违规（commit e230aa9）
- 失误：合并到 main 未确认 → 规则：老板未明确许可不合并（见 SKILL.md「Pitfalls」）

## 可移植性

- 失误：SKILL.md 写死 harness / 平台耦合、死引用、硬编码工具名 → 规则：移除平台耦合与死引用，保持可移植（commit c8bc96f）
- 失误：写了 `metadata.kind` 之外的跨平台字段不一致 → 规则：skill 目录契约字段要符合 catalog 规范（commit 4253c1b）

## 文档与真实文件一致性

- 失误：README 目录结构列了 `benchmarks/dan-koe.md`、`benchmarks/ruanyifeng.md`、`templates/person-fragment.md`、`assets/.gitkeep`，实际都不存在 → 规则：改文档前先 `find` 核验每个被引用的路径，引用了就必须让文件真实存在
- 失误：模板带 `## Evidence Ledger` 章节和 `living_person` / `notability` 字段，但知识库 30 份真实成稿都不用，模板跑 `validate_archive.py` 会报「非模板章节」→ 规则：模板结构必须从真实成稿提炼，不能凭空加章节或字段；模板要能通过它自己定义的校验
- 失误：README 写「27 份档案」「26 份档案」，知识库实际 30 份档案（33 个 md 含 2 个索引+1 个报告） → 规则：文档里的计数改成现场命令或最新核验值，不写记忆中的旧数

## CI 与发布

- 失误：publish.yml 在 `release: published` 时调用 `cgartlab/cgartlab-skills` 的 reusable workflow，但后者是 private 仓库，GitHub 不允许 public 仓库调用 private reusable workflow，导致 7 个 skill 仓库的 publish 全部 0s 失败、jobs 为空、`referenced_workflows: []` → 规则：public 仓库的 reusable workflow 必须放在 public 仓库；private 共享 workflow 只能被 private caller 调用。排查时先看 `jobs` 是否为空 + `referenced_workflows` 是否为空，这是解析期失败的信号。**最终解法（v0.2.2）：把发布逻辑内联到本仓库 `.github/actions/publish`，不再依赖跨仓库 reusable workflow**
- 失误：`dry-run: ${{ inputs.dry_run || false }}` 在 release 触发下 `inputs` 上下文不存在，但这不是本次根因（真正根因是 private reusable workflow）；规则：同类报错先排除权限/可见性，再怀疑表达式
- 失误：修知识库索引时用了 `git add <file>` 后直接 `git commit`，把用户已 staged 的其他删除一起提交 → 规则：仓库有其他未提交改动时，用 `git commit -- <path>` 只提交指定文件，或先 `git status` 确认 staged 内容
- 失误：`read_file` / `sed` 把 `${{ secrets.SKILLHUB_API_KEY }}` 显示成 `*** secrets.SKILLHUB_API_KEY }}`，被误判为 YAML 语法错误 → 规则：secrets 值在工具输出里会脱敏显示，不要据此判断文件损坏；用 `od -An -c` 看原始字节或 `git diff` 确认是否真有改动
- 失误：误判后仍用 patch 试图「修复」，patch 报 Non-exact match 但 `git diff` 为空（实际没改）→ 规则：patch 报非精确匹配时先 `git diff` 确认是否落盘，不要继续叠加修改
