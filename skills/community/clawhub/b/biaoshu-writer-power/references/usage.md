# 执行细节（操作手册）

本文件是**执行任务时的完整操作指引**——做解读/制作/合规、生成报告、处理边界情形时按需查阅。接口总调度见 [api.md](api.md)，具体字段按场景读对应 API 分册。

## ⚠️ 输出约定（必须遵守，除非用户明确说不要）

运行 `zcm.py` 时**老老实实把脚本输出原样给用户看**，不得为了「省事/抽字段」把它藏起来：

1. **生成任务必须实时播报**：生成成品标书耗时长，禁止直接前台等待。必须先用 `generate ... --no-wait` 拿到 `job_id`，再立即启动 `progress-stream <job_id>`，把每次变化转述给用户（如「进度更新：标书正在生成中。已进入「生成正文」阶段（47%，32/80 节）。当前正在写「项目实施方案」。已用 6分钟。我会继续后台监听，完成后交付成品链接。」）。即使平台暂时没有返回百分比/章节，也要转述脚本每 5 秒输出的心跳句（如「进度更新：任务已开始运行，正在等待平台返回生成阶段进度。我会继续后台监听。」），让用户知道任务仍在跑。看到 `进度更新：`、`[完成]`、`[失败]` 这类行时直接转述或轻微润色，不要改写成“等待后台完成通知”。解读/抽包/合规也要照常展示百分比+阶段。**不要 `2>` 重定向、不要吞掉**。
2. **完整交付产物位置**：每次产出后，必须把以下信息明确告知用户：
   - 智能解读结果/报告（`*_智能解读.html` 等）
   - 成品标书默认给短时下载链接（含文件名、大小、有效期）；用户明确要本地文件时再下载为 `*_投标文件.docx`
   - 合规审查结果/报告（`*_合规审查.html` 等）

   脚本本身已打印这些信息（`generate` 默认打印下载链接；`result -o` 成功后打印本地全路径）；**别用 `>`/`2>` 把它们重定向掉**。若用 `--no-wait`，完成后须主动用 `download-url <job_id>` 补取成品链接，或在用户要求本地文件时用 `result <job_id> -o <路径>.docx` 下载。

   此外，解读/生成/合规/查重完成后脚本会打印一行 `💰 当前可用字数：X`——**照常转述给用户**，让其对可用字数与「够不够下一次」有数；查询失败时不打印，属正常，不必追问。

> 反例（禁止）：`python3 scripts/zcm.py generate <pid> > out.json 2> log` —— 这会同时藏掉进度和成品全路径。

3. **凭证/注册/绑定/字数类交互是例外，不要把命令与 exit 码原样抛给用户**：这类脚本报错（如 `register` 缺参的 exit 2、`非交互环境请传参…`）是给你（助手）看的提示，**不是给用户的**。你应当把它翻译成一句「用户下一步该提供什么」，并由你代跑命令——绝不要让用户自己去敲 `python3 scripts/zcm.py register`。详见「第 1 步：凭证」末尾的绑定/可用字数流程。

## 用法速查（完整流程）

```bash
python3 scripts/zcm.py login --app-key bk_live_xxx   # 1. 配凭证（自动生成 config.json；或 trial / 环境变量）
python3 scripts/zcm.py me                            #    连通 + 可用字数自检
python3 scripts/zcm.py interpret 招标文件.pdf --report html   # 2. 解读 → project_id（+解读报告）
python3 scripts/zcm.py packages <project_id>         # 3. 抽包（多包才需选包）
python3 scripts/zcm.py generate <project_id> --package-ids 11 --total-pages 80 --no-wait  # 4. 用户确认包和页数后生成
python3 scripts/zcm.py compliance <project_id> 投标文件.docx --report html --name 招标文件.pdf   # 5. 可选：标书审查
python3 scripts/zcm.py duplicate 投标A.docx 投标B.docx --tender-file 招标文件.pdf --legal-possession-attested --report html  # 6. 可选：标书查重（+查重报告）
```
招标文件支持 `.pdf/.doc/.docx`；标书审查和标书查重的投标文件支持 `.pdf/.doc/.docx`。全部自动轮询、实时播报后端进度。各步详解见下。

## 明确制作意图：自动全流程

用户上传/提供招标文件后，如果明确要求制作标书或投标文件（如「帮我做标书」「生成投标文件」「出一份响应文件」「直接做成标书」），视为已授权自动制作。无分包/单包时自动继续：interpret → packages → generate --no-wait → progress-stream → download-url；多包项目必须停下来让用户确认具体包，不默认全选。

- 分包：先照常执行 `packages`。`is_multi_package=false` 时生成传 `--no-package`；`is_multi_package=true` 时展示分包清单并暂停，让用户确认选哪些包后再生成；用户已在原始需求里指定包号/包名时按指定包执行。
- 页数：平台当前最大页数上限为 1200 页；用户已指定页数时按指定值执行，并用 `max_total_pages` 校验，超限必须拒绝；未指定页数时默认 200 页，默认生成200页的标书，并且生成命令带 `--total-pages 200` 与 `--max-total-pages`。对用户要明确说明：默认按 200 页生成，也可以指定 1 到 max_total_pages 范围内的页数。如果 `max_total_pages < 200`，不要提交 200 页；改为提示上限并让用户确认，或在用户明确允许自动按上限时使用 `--total-pages <max_total_pages>`。
- 例外：用户明确说「包和页数先列出来让我确认」「开始前先问我」「不要直接生成」时，按常规确认流程暂停。
- 进度：提交生成后立刻进入 `progress-stream`，持续转述阶段、百分比、当前章节、已用时间；即使只有心跳也要播报。完成后主动 `download-url` 取成品短时链接，用户要求本地文件时再下载。

## 目录
- [第 1 步：凭证](#第-1-步凭证)
- [第 2 步：智能解读](#第-2-步智能解读)
- [明确制作意图：自动全流程](#明确制作意图自动全流程)
- [第 3 步：抽取分包](#第-3-步抽取分包)
- [第 4 步：生成成品标书](#第-4-步生成成品标书)
- [第 5 步：标书审查](#第-5-步标书审查)
- [第 6 步：标书查重](#第-6-步标书查重)
- [报告生成与命名](#报告生成与命名)
- [版本检查排查](#版本检查排查)
- [关键约定](#关键约定)

---

## 第 1 步：凭证

凭证固定存在 **当前 skill 根目录的 `config.json`**。读取和写入都锁定这个文件，不读旧 `~/.zcm/` 目录，也不允许 `ZCM_CONFIG` 改到其他路径。

**只需 Api Key 一项**：

**配置方式（任选其一）**：
1. 直接创建 `config.json`（必须在当前 `biaoshu-writer-power/SKILL.md` 同级目录，按下面模板写入即可，`base`/`output_dir` 可选留空）：
   ```json
   {"app_key":"bk_live_xxxxx","base":"","output_dir":""}
   ```
   建好后 `chmod 600 config.json`（含真实 Key）。通常不用手写——方式 2~5 任一命令都会自动生成到**当前 skill 根目录**。
2. 用户把 Key 发你后，**先定位当前安装的 `biaoshu-writer-power/SKILL.md` 所在目录，再由你代跑** `login --app-key bk_live_xxx` 保存（自动建/更新同级 `config.json`，权限 600）——别把这条命令丢给用户自己敲。
3. 临时用环境变量：`export ZCM_APP_KEY=bk_live_xxx`（首次会自动落盘到当前 skill 根目录的 `config.json`，不是全局目录）。
4. 没 Key 想直接注册：向用户要手机号，由你代跑 `register --phone`（skill 内手机号+短信验证码换取 Api Key，自动保存）——见本节末尾「绑定手机号 / 可用字数不足」流程，别让用户自己敲命令。
5. 免费试用：`python3 scripts/zcm.py trial`（自动采集设备特征开通试用账号，赠 50,000 字；同设备重复执行幂等返回原 Key，不重复赠送）。

- **保存后转述位置**：凭证保存成功后（login / trial / register / 环境变量落盘任一方式），把脚本打印的**凭证文件（config.json）完整路径**转述给用户。
- 🔒 **发布安全**：`config.json` 含真实 Key——**绝不上传发布包/提交仓库**；发布包不含任何配置文件，模板结构见上方方式 1。不要使用 `~/.zcm/` 或 `ZCM_CONFIG` 保存本 skill 的 Api Key。
- **升级保留配置**：升级 skill 时，必须保留当前安装目录里的 `config.json` 和 `biaoshu-writer-power-files/`；只覆盖 `SKILL.md`、`scripts/`、`references/` 等内容文件。不要用会清空整个目录的安装方式直接覆盖当前目录；如安装器只能强制覆盖，先装到临时目录，再同步内容文件到原目录并排除 `config.json`。
- **用户完全没有任何 Key**（首次用）：三选一，均由你代跑——① 试用零输入自动开通（赠 50,000 字，绑手机号可升级为注册账号并继续补发 50,000 字，Key 不变）；② 向用户要手机号，你代跑 `register --phone` 在 skill 内注册；③ 用户已在官网有 Key——获取全路径：打开官网 https://biaoshu.zhiliaobiaoxun.com/?ch=s94 注册登录后，点**左侧菜单『Skill 接入 → 获取 Api Key』**在弹出面板中查看/复制 Key（首次打开自动生成）；让他把 Key 粘贴到对话里（如「我的 Api Key 是 bk_live_xxxxx，帮我保存一下」），由你代为保存（**别把 `login --app-key` 命令甩给用户**）。缺凭证时脚本会打印这些指引并退出（码 2）。
  - 注意：③ 仅限**从没有过 Key** 的场景。若用户**已有 Key** 只是可用字数不足，按下面「绑定手机号 / 可用字数不足」处理：绑定走 skill 内验证码流程，购买会员或字数包只给普通官网地址（可带 `ch` 渠道码）。
- 先 `python3 scripts/zcm.py me` 确认连通与可用字数（生成会消耗可用字数）。

### 绑定手机号 / 可用字数不足（由你代跑，别把命令丢给用户）

可用字数不足或想绑手机号升级为注册账号时，**你（助手）驱动整个流程，用户只需提供手机号与验证码**，Api Key 全程不变。对外不得展示任何携带 Api Key 的链接：

1. 先向用户要**手机号**（例：「请提供你的手机号，我来发送验证码」）。**不要**打印 `python3 scripts/zcm.py register` 让用户自己敲。
2. 你运行 `python3 scripts/zcm.py register --phone <手机号>` 触发发码，然后告诉用户「验证码已发送，请把收到的验证码发我」。
3. 拿到验证码后你运行 `python3 scripts/zcm.py register --phone <手机号> --code <验证码>` 完成绑定/注册（Api Key 不变；新手机号注册赠 5 万字，试用账号绑定手机号继续补发 5 万字）。
4. **绝不运行无参 `register`**（非交互会 exit 2）；也**别把 exit 码 / `非交互环境请传参…` 这类内部报错贴给用户**——只说下一步要什么。

- **用户不想在 skill 内绑定 / 想自助上网页**：只给普通官网地址（可带 `ch` 渠道码），让用户登录后按页面完成账户、会员或字数包操作；不要把 Api Key 拼进任何 URL，也不要转发平台返回的带凭证参数链接。
  ```
  https://biaoshu.zhiliaobiaoxun.com/?ch=s94
  ```
  `ch` 只用于渠道归因，不是用户凭证。
- 手机号已被注册过：返回老账号 Key 并切换，试用账号数据不迁移。

## 第 2 步：智能解读

唯一招标文件入口；只在这步传一次，后续全程复用 `project_id`。

```bash
python3 scripts/zcm.py interpret /path/招标文件.pdf      # 本地路径，或 http(s) URL
```
- 支持 `.pdf/.doc/.docx`，**≤ 50 MB**（超限脚本提前报错）。自动轮询，结束打印 `project_id`（**记下它**）+ **解读摘要**，默认不再向 WorkBuddy 打印完整 JSON，以免大结果拖慢展示；完整明细通过解读报告交付。
- **云端文件先下载到本地再处理**：传入 URL 时，脚本会先把文件下载到 `biaoshu-writer-power-files/_downloads/`（拿到真实文件名、绕开后端远程下载的 https/内网/大小限制），再按本地文件上传。文件名也据此自动命名报告。
- **直接把解读摘要展示给用户**——至少包含项目名称、`project_id`、控标建议/风险、合标项/废标红线/评分项等结构化条目数量，并交付 HTML 解读报告全路径；不要默认打印完整 `/result` JSON。只有后台排查或用户明确要原始 JSON 时，才加 `--full-json` 打印完整结果。字段口径见 [api-bid-workflow.md](api-bid-workflow.md)。
- 展示后**主动问是否生成解读报告**（见[报告生成与命名](#报告生成与命名)）。但用户已经明确要求制作标书或投标文件时，不在这里停顿，仍要自动生成 HTML 解读报告并继续抽包、生成成品标书。

## 第 3 步：抽取分包

```bash
python3 scripts/zcm.py packages <project_id>
```
- `is_multi_package=true` → 把返回的 `packages` 呈现给用户挑选，收集选中的 `package_ids`；即使用户已明确要求制作标书或投标文件，只要没有在原始需求里指定包，多包项目必须停下来让用户确认，不能默认全选。
- `is_multi_package=false` → 常规流程不询问包选择，直接进入页数确认；第 4 步自动传 `--no-package`。自动全流程下直接传 `--no-package` 继续生成。
- `max_total_pages` 是当前项目最大页数；平台当前最大页数上限为 1200 页。用户想指定页数时，以抽包结果里的上限为准，超过必须拒绝，不要提交生成；向用户提示可指定范围时使用“1 到 max_total_pages 页”。
- 页数确认时展示：系统建议页数、最大页数、预计消耗字数、当前可用字数。优先使用抽包结果里的 `suggested_estimated_words`；用户改页数时按 `total_pages * estimated_words_per_page * estimate_reserve_factor` 重新估算，并说明“预计消耗仅供参考，实际消耗以平台最终结算为准”。
- **确认门槛（有例外）**：常规解读后，如果用户尚未明确制作意图，抽包后必须暂停到页数确认；多包项目还必须先确认选哪些包。用户确认“生成多少页/使用系统建议页数”之前，不得进入第 4 步。但用户在上传/提供招标文件后已明确要求制作标书或投标文件时，无分包/单包时自动继续；多包项目必须停下来让用户确认具体包。未指定页数时默认 200 页，并校验 `max_total_pages`；同时告诉用户也可以指定 1 到 max_total_pages 范围内的页数。

## 第 4 步：生成成品标书

**生成成品标书按生成内容消耗可用字数**，耗时较长。默认不下载本地文件，完成后输出短时下载链接：
- 用户只要成品 → 不传 `-o`，脚本完成后打印文件名、大小、下载链接和有效期。
- 用户明确要本地文件 → `-o <路径>`；想长期固定本地输出目录 → `login --output-dir <目录>`。

```bash
python3 scripts/zcm.py generate <project_id> --package-ids 11,12 --total-pages 80 --max-total-pages 1200
# 非多包且用户未指定页数：python3 scripts/zcm.py generate <project_id> --no-package --total-pages 200 --max-total-pages 1200
# WorkBuddy/SkillHub 必须追加 --no-wait，并另起 progress-stream 实时播报
# 需要本地文件时：完成后再 result <job_id> -o 投标文件.docx
```
- 生成前脚本会强制校验：多包必须传用户已确认或已明确指定的 `--package-ids`，无分包/单项目自动传 `--no-package`；必须已确认页数或按明确制作意图使用默认 200 页（`--total-pages`）；必须带入抽包结果的 `--max-total-pages`；并且默认必须用 `--no-wait` 进入实时进度模式。
- 生成前脚本会按确认页数预估本次需要字数；用户页数超过 `max_total_pages` 会直接拒绝；不根据余额做字数不足示警，直接继续提交 Open API 生成任务。预估公式是 `total_pages * estimated_words_per_page * estimate_reserve_factor`，当前平台默认等价于 `页数 * 500 * 1.05`；预计消耗仅供参考，实际消耗以平台最终结算为准。
- 完成后默认打印**成品下载链接**；如用户明确要求本地文件，完成后再下载并打印**成品完整路径**+所在目录，**两项都告诉用户**。
- 成品下载链接有效期只以后端 `download-url` 返回的 `expires_in` 为准；skill 只能展示该值，不能单方面延长。若链接失效，用同一 `job_id` 重新获取下载链接；若要把“半小时/1 小时”统一改为 1 天，需要后端签发 token 的 TTL 改为 `86400` 秒。
- 后端会按「选包 → 抽需求 → 生成大纲 → 生成正文 → 抽取制式模板 → 导出」串行完成；页数规划会综合分包结构、技术/商务内容、表格和图表，`total_pages` 最高 1200。
- 制式表格/范本会尽量自动抽取或生成；无法确认的公司资料、日期、报价、签章等信息会保留为待填项，不要替用户编造。
- **跟用户解释字数计费时统一说**：智能解读免费，可用字数为 0 也能发起；标书制作、标书审查、标书查重按平台规则消耗可用字数。标书生成的预计消耗仅供参考，实际消耗以平台最终结算为准；生成前只做预估，不做字数不足示警，也不会因预估字数不足而拦截提交。抽包、任务查询、结果获取、知识库查询等辅助查询不作为独立成果单独计费。
- **生成中可用字数不足**：平台会停止继续写正文并可能返回 `insufficient_balance` / `insufficient_points`。skill 必须明确告诉用户“本次任务已停止，平台不会自动续跑”；如果 `download-url` 返回 `partial=true`，先交付半成品下载链接，展示已生成/总章节/缺失章节，并提示购买会员或字数包后用 `continue-generate <project_id> --outline-id <outline_id> --no-wait` 继续生成正文。不要重新解读、抽包或重建大纲。
- ⏱ **生成可能耗时 >10 分钟**（实测 30 页约 15 分钟）。固定流程：`generate <pid> ... --no-wait` 拿 `job_id` → `progress-stream <job_id>` 实时转述阶段/百分比/当前章节/已用时间 → 完成后 `download-url <job_id>` 取短时下载链接；用户明确要本地文件时再用 `result <job_id> -o <路径>.docx` 下载。万一监听中断，用同一 `job_id` 续查即可；半成品补写用 `continue-generate`，不要重发 generate。
- **默认页数口径**：常规流程继续展示系统建议页数、最大页数和预计消耗，让用户确认。自动制作流程下，用户明确要求制作标书或投标文件即视为同意默认生成200页的标书；未指定页数时默认 200 页，命令使用 `--total-pages 200` 和 `--max-total-pages`，不使用 `suggested_pages` 作为默认页数。提示用户时必须同时说明“也可以指定 1 到 max_total_pages 范围内的页数”。如果实际环境仍出现“单包项目明确要制作却停在页数确认”，优先检查用户安装的 WorkBuddy/Skill 是否不是 3.1.2+，或 WorkBuddy 是否没有按本手册执行。
- **进度细节来源**：`progress-stream` 只转述 `/jobs/{job_id}` 返回的 `progress.percent/stage/message/current_step/total_steps/current_step_label/elapsed_seconds/estimated_remaining_seconds`。后端不写这些字段时，skill 只能输出运行心跳，不能编造章节级进度。
- **内容完整性边界**：skill 不负责复刻生成算法，也不能只靠文案保证“内容完整”。后端应在标记 `succeeded` 前校验计划章节数、已生成章节数、空章节、模板占位符、待填项和导出 docx 结构；发现缺章节或结构异常时应自动补写，或把任务置为 failed 并返回明确原因，skill 再如实转述。
- **耗时排查口径**：如果 Open API / skill 生成明显慢于网页登录流程，先记录 `job_id`、页数、包号、提交/完成时间、进度阶段，再排查后端是否使用同一套生成 worker、模型、并发、缓存与模板填充策略；skill 侧不要靠重试或降级流程掩盖慢链路。

## 第 5 步：标书审查

要**两样输入，都要让用户提供**：
1. **招标文件**（`.pdf/.doc/.docx`）→ 经第 2 步解读产出 `project_id`；已解读则复用，不重传。
2. **投标文件**：**一份或多份** `.pdf/.doc/.docx`，被审查对象（本地路径或 http(s) URL），**支持多选，最多 100 份**；**每份 ≤ 1024 MB**，**总大小不超过 2GB**。

```bash
python3 scripts/zcm.py compliance <project_id> /path/投标A.docx /path/投标B.docx
# 暗标/电子标：加 --blind / --electronic
# 敏感单位名称：加 --sibling-unit-names "甲公司,乙设计院"
# 关闭语义审查：加 --no-semantic-review
```
- 投标文件传 URL 时，**同样先逐个下载到本地再上传**（落 `biaoshu-writer-power-files/_downloads/`）。
- 审查选项与平台一致：暗标、电子投标、敏感单位名称、语义审查开关。关闭语义审查时只能表述为“规则类检查结果”，不能说成完整语义审查。
- 标书审查按平台规则消耗可用字数；发起前会校验可用字数，不足时提示购买会员/字数包后重试。
- **直接把合规结果展示给用户**——含 `summary`（风险计数 + 一句话结论 + 语义审查状态）、`partial_summary`（阶段性/部分结果统计）、`scope_summary_lines`（检查范围）、`issues[]`（风险等级/招标依据/投标证据/修改建议）、`similarity_issues[]`（多文件雷同）、`manual_items[]`（人工核查清单）。优先讲高风险、结论与审查完整性。字段见 [api-compliance.md](api-compliance.md)。
- 若 `summary.conclusion_phase`、`summary.semantic_review` 或 `partial_summary` 表示语义审查处理中、部分完成或只完成规则检查，必须如实说明“当前为部分结果/语义审查未完整完成”，不要说成完整审查完成。
- `risk_level` 实测为 `high`/`review`/`tip`，脚本输出与报告**已自动转中文**（高风险/待复核/提示），直接用中文呈现。
- 未解读就调 → 409；投标文件缺失/类型不对 → 422（两份输入缺一不可）。
- 展示后**主动问是否生成合规报告**（见下）。

## 第 6 步：标书查重

用于比较不同主体投标文件之间的雷同/相似风险。它不是标书审查，也不判断投标文件是否合规；结果只作为提交前内部自查线索，不构成围标、串标或违法违规的法律认定。

固定按这 3 步走，缺一步都不要提交任务：

1. **先收集投标文件**：必须是 2-3 份投标文件。只有 1 份投标文件，或“1 份投标文件 + 1 份招标文件”，都不能发起查重；应提示用户再提供至少 1 份投标文件。
2. **再处理招标文件（可选）**：招标文件只能放到 `--tender-file`，用于排除招标原文造成的共同表述，不能放进投标文件列表里凑数。
3. **最后确认合法持有**：发起前必须先问并得到用户确认：「请确认你合法持有并有权处理本次上传的全部投标文件/招标文件。确认后我再发起标书查重。」

```bash
python3 scripts/zcm.py duplicate /path/A公司投标.docx /path/B公司投标.docx --legal-possession-attested --report html
# 可选关联招标文件，用于排除招标原文造成的共同表述：
python3 scripts/zcm.py duplicate /path/A公司投标.docx /path/B公司投标.docx /path/C公司投标.docx \
  --tender-file /path/招标文件.pdf --legal-possession-attested --report html
# 可选关闭维度：--no-image / --no-metadata / --no-semantic
# 默认排除招标文件原文共同表述；如用户明确要求不排除，可加 --include-tender-baseline
```

- 投标文件必须 **2-3 份**，支持 `.doc/.docx/.pdf`；单份 ≤ 1024 MB，总大小不超过 2GB。投标文件不足 2 份时直接补问，不要提交 API。
- 招标文件可选 **1 份**，支持 `.doc/.docx/.pdf`，≤ 50 MB；用于降低招标原文共同表述对相似度的干扰。
- **云端文件先下载到本地再处理**：传入 URL 时，脚本会先下载到 `biaoshu-writer-power-files/_downloads/`，再按本地文件上传。
- 标书查重按平台规则消耗可用字数；发起前会校验可用字数，不足时提示购买会员/字数包后重试。
- 查重维度：连续文本/段落结构、图片相似、文档元数据、主体线索、招标基线。
- 查重完成后展示 JSON 里的核心结论，并在用户需要或命令带 `--report html|docx|both` 时生成本地 HTML/Word 查重报告。必须输出报告绝对路径。
- 若任务失败返回 `bid_duplicate_failed`，优先转述平台返回的具体原因；错误详情通常会带 `run_id`、`duplicate_status`、`duplicate_error_message`，用于后台定位是哪次查重运行失败。
- 查重报告只呈现文件对风险率、证据片段、图片/元数据/主体线索异常、修改建议；不要输出“已串标/确认围标”等定性结论。

## 报告生成与命名

解读/合规/查重结果可渲染成报告（HTML / Word），零依赖：

```bash
# 随命令一步出（默认 html；要 Word：--report both）
python3 scripts/zcm.py interpret 招标文件.pdf --report html
python3 scripts/zcm.py compliance <pid> 投标.docx --report html --name 招标文件.doc
python3 scripts/zcm.py duplicate 投标A.docx 投标B.docx --legal-possession-attested --report html
# 按 job_id 补出
python3 scripts/zcm.py report --job <JOB_ID> --name 招标文件.pdf            # html
python3 scripts/zcm.py report --job <JOB_ID> --name 招标文件.pdf --format both  # +Word
python3 scripts/zcm.py report --job <JOB_ID> --service bid_duplicate --format html
```
- **默认只出 HTML**；用户明确要 Word 才 `docx`/`both`。
- 命名：`招标文件名_智能解读` / `招标文件名_合规审查` / `标书查重_时间戳`。取名优先级：`--name` > 结果自动识别（`original_filename` / `project_info.项目名称` / 本地缓存）> `标签_时间戳`。
  - `interpret` 自动用上传文件名；`generate` 自动用缓存名；**`compliance`/`report --job` 拿不到招标文件名时务必带 `--name`**，否则退化时间戳。`bid_duplicate` 不依赖招标文件名时默认使用时间戳命名。
- 报告内容依赖后端按对应 API 分册返回完整结果；合规 HTML 总览会展示检查范围、结论、语义审查状态和部分结果摘要；`/result` 只回句柄或字段空时，报告注明「无明细」而不报错。

## 版本检查排查

SkillHub 线启动时会每天最多自动检查一次版本更新：有本地凭证、平台 `/skill/version` 返回的 `latest` 大于本地 `SKILL_VERSION` 时，才会提示更新。失败、无凭证、平台未配置更高版本、本地已是同版本、或当天已经检查过，默认都不会打扰用户。

后台排查“为什么没提示更新”时，先确认三件事：
- 平台 `skill_setting.skill_version` 是否高于本地 `SKILL_VERSION`。
- 本地是否已安装同版本或更高版本。
- 当前 skill 目录的 `config.json` 是否已有当天 `last_version_check`。

需要立即复查时，可后台运行 `version-check` 子命令；它会绕过当天节流并输出检查结果。若仍无提示，多半是平台未返回 `latest`、网络不可达，或版本号不是 `MAJOR.MINOR.PATCH` 格式。

## 知识库取数（供本地待填项回填）

当需要用企业资料辅助**本地**待填项回填时，不改走生成主流程，而是单独查询开放 API：

```bash
python3 scripts/zcm.py knowledge-base
python3 scripts/zcm.py knowledge-base company_profile
python3 scripts/zcm.py knowledge-base qualifications --page 1 --page-size 50
python3 scripts/zcm.py knowledge-base performances --page 1 --page-size 50
python3 scripts/zcm.py knowledge-base financial_reports --page 1 --page-size 50
```

- 返回按类别分组的结构化 JSON；分页类默认前 **50** 条。
- **明确排除**：历史标书库、标书模板库。
- 字段含义、可否直接回填、敏感字段边界见 [knowledge-fields.md](knowledge-fields.md)。

## 经验沉淀与问题上报（后台命令，勿展示给用户）

经验沉淀（用户两问都同意后执行；长文本先写入临时文件走 --content-file）：

```bash
python3 scripts/zcm.py experience --type preference --stage write \
  --title "落款格式" --content "落款统一用公司全称"
# type: material=素材 preference=偏好 correction=纠错；stage: interpret/write/compliance
# 长文本：--content-file /tmp/exp.txt；可选 --project-id 关联项目
```

成功输出「已沉淀，累计 N 条」——向用户转述 N；`daily_quota_exceeded` → 转述「今日沉淀已达上限（每天最多 20 条）」。

问题上报（内容先展示给用户、同意后执行；自动附带 skill 版本与渠道码）：

```bash
python3 scripts/zcm.py feedback --category error --scene "生成标书" \
  --phenomenon "轮询中断报超时" --expectation "自动续轮询"
# category: misguide=跑偏 correction=用户纠正 error=报错 suggestion=建议
```

两条命令上报失败（网络/配额/Key 失效）时不阻断主流程：如实告知「本次未回传，稍后可再试」。

## 关键约定

- **必须输出完整路径**：解读报告 / 成品标书 / 合规报告生成后，把**每个文件的完整绝对路径**逐行告诉用户（脚本已用「已生成…/已下载…」打印绝对路径，照搬即可）——**不要只说落在某目录**。
- **进度播报（两阶段，必须这样做才能实时）**：Bash 工具不流式传输 stderr，`--no-wait` + `progress-stream` + Monitor 是唯一能让用户看到实时进度的方式。长任务（interpret / generate / compliance / duplicate）统一走以下三步：
  1. **提交**（同步，快）：加 `--no-wait`，Bash 运行后立即拿到 `job_id`。
  2. **实时监听**：`Bash(run_in_background=True)` 运行 `python3 scripts/zcm.py progress-stream <job_id>`，再用 Monitor 订阅该进程 stdout——每行状态变更即时通知 Claude，Claude 实时转达给用户（如「5% 准备文档」→「生成内容 47% · 正在写正文 32/80 节」→「导出 Word」→「完成」）。Monitor 的 description 用正常任务名，**不带「重试」等临时标签**——即使是 worker_lost 后重新提交的 job，新 job 已正常运行，描述应反映当前状态而非历史原因。后端暂未给出细分进度时，`progress-stream` 会立即输出监听开始，并每 5 秒输出排队/运行中心跳句；这些心跳句也必须转述，避免用户误以为卡死。运行环境已激活 `smartBidding311` 时，优先直接用该环境里的 `python` 启动监听；不要用 `conda run` 包裹 `progress-stream`，它可能缓冲 stdout，导致前台看不到实时行。
  3. **取结果 + 生成报告 + 输出路径**：Monitor 收到 `[完成]` 后必须主动补齐后处理，三类任务各有对应步骤：
     - `interpret`：`result <job_id>`（提取 project_id）→ `report --job <job_id> --format html`（生成解读报告）→ 输出报告全路径
     - `generate`：`download-url <job_id>`（获取短时下载链接）→ 输出文件名、大小、有效期和下载链接；用户明确要本地文件时再 `result <job_id> -o <路径>.docx`
     - `compliance`：`result <job_id>`（打合规摘要）→ `report --job <job_id> --format html`（生成合规报告）→ 输出报告全路径
     - `duplicate`：`result <job_id>`（打查重 JSON 摘要）→ `report --job <job_id> --service bid_duplicate --format html`（生成查重报告）→ 输出报告全路径；如果用户明确不要报告，则只输出文件对风险率、证据片段与修改建议，不输出本地报告路径
     
     > `--no-wait` 跳过了同步模式的后处理，**AI 必须手动补**，否则报告文件不会生成，用户看不到路径。
  > 仅在用户不需要看进度或调试时才用单命令前台运行（无 `--no-wait`）。`packages` / `me` 等快速命令无需两阶段。
- **断点续查**：`job <job_id>` 查状态、`result <job_id> [-o file]` 取结果、`cancel <job_id>` 取消。
- **幂等**：网络重试给提交命令加 `--idempotency-key <UUID>`，避免重复建任务/重复扣费。
- **续接已有 project**：用户解读后直接说「帮我生成」，沿用 `project_id` 从第 3 步继续，不重传。
- **错误处理**：脚本已把 401/402/404/422/429 转中文。常见——402 可用字数不足让用户购买会员或字数包；整层 404 多为开放 API 总开关未开，让管理员开启；429 退避重试。完整对照见 [api.md](api.md)，按任务场景继续读对应分册。
- **可用字数不足（402）**：开放 API / Skill 下，智能解读免费且可用字数为 0 也能发起；标书审查、标书查重仍会校验并按平台规则消耗可用字数；标书生成前只做预计消耗说明，不查余额、不做示警、不拒绝提交。未绑手机号时脚本先引导「绑定手机号升级注册账号并领取补发字数」（`register`，Api Key 不变）；已绑则给普通官网地址让用户登录后购买会员或字数包。不得展示任何携带 Api Key 的绑定/充值链接。
