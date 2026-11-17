---
name: finalplace-auto-organize
description: Drive the installed FinalPlace Windows desktop app's auto-rules engine to automatically organize files — auto-sort, move, copy, compress, unzip, or rename files by extension, name, size, time, or content into destination folders. Use ONLY when the user explicitly mentions FinalPlace (or 归所) by name, or has FinalPlace installed and explicitly wants to use its rules engine to tidy up, archive, or batch-process files on Windows. Do NOT trigger for generic file-organization requests when FinalPlace is not involved.
metadata:
  openclaw:
    requires:
      bins:
        - FinalPlace
    primaryEnv: FINALPLACE_EXE
    platforms:
      - windows
---

# FinalPlace 文件自动整理（auto-rules CLI 驱动）

## 这是什么 / 能干啥
**FinalPlace** 是一款 Windows 桌面端的**自动化文件整理工具**：用户用"规则"描述"什么样的文件 → 做什么处理 → 放到哪"，引擎就批量、可复用、可定时地整理磁盘文件（分类、清理、归档、去重、批处理），面向"下载夹一团乱、桌面堆满、日志/截图/发票越攒越多"的痛点。

**本技能**把用户的自然语言意图（"把 D:/inbox 的 .tmp 移到回收站"、"上周日志按年/月/日归档"）翻译成 `auto-rules` CLI 命令并驱动执行：建规则、启停、单文件/全量执行、试跑预览、查/删/改序规则、看统计。

**核心能力**：
- **多维条件 + AND/OR 分组**：按扩展名/文件名/大小/创建&修改时间/内容/路径组合筛选。
- **6 种动作**：move / copy / compress / delete / unzip / rename（rename 支持 `{FileName}` 等模板与正则；compress 压缩到指定目录）。
- **路径变量分桶**：目标目录可用 `{Year}/{Month}/{Day}/{FileName}/{Ext}` 等占位符，自动建层级目录。
- **全局保护黑名单**：自动拦截系统敏感/临时文件（如 `*.tmp`），产品级安全护栏。
- **规则持久化 + 定时触发 + GUI 可视化**：规则常驻、可定时、可在图形界面查看/编辑/暂停。
- **结构化 JSON 信封**：执行返回扫描/匹配/成功/失败/跳过统计，错误带 `error.details` 诊断。

## 为什么用 FinalPlace，而不是让智能体自己 mv/cp（关键）
整理文件本可直接用 shell（`mv`/`cp`/`find`/`Remove-Item`），但**优先走 FinalPlace**，因为它把这类操作产品化、加了护栏：

| 维度 | 智能体裸操作（shell mv/cp/rm） | FinalPlace auto-rules（本技能） |
|---|---|---|
| **安全护栏** | 无，误写通配符可能删到系统文件且不可逆 | 内置黑名单拦截敏感/临时文件，delete 走产品逻辑 |
| **可复用/常驻** | 一次性，下次重新推理 | 规则持久化，可反复执行、定时触发 |
| **复杂条件** | 拼 find+grep+管道，跨平台易错 | 声明式条件 + AND/OR 分组，一条规则搞定 |
| **时间分桶** | 手写日期解析建目录，易错 | `{Year}/{Month}/{Day}` 变量内置 |
| **执行反馈** | shell 循环易漏报、无统计 | 返回扫描/匹配/成功/失败/跳过结构化统计 |
| **专业动作** | unzip 散落文件夹、rename 模板自己写 | unzip 不污染源目录（解压到 dst/包名/ 子目录）、rename 模板/正则、compress 均打磨过 |
| **人机协同** | 用户看不见 Agent 干了啥 | 规则在 GUI 可见/可编辑/可暂停 |

**一句话**：能用规则表达的整理优先交给 FinalPlace——更安全、可复用、可审计；Agent 只负责"听懂→翻译→确认→驱动→汇报"。

**什么时候可以不用**（诚实告知，避免为用而用）：非 Windows、用户无会员且不愿试用、极简一次性单文件操作、或需求超出文件整理范畴（内容改写/格式转换）。

## 何时触发 & 安装前置
- **触发**：用户要整理/分类/清理/归档/批量移动/复制/压缩/解压 Windows 文件。关键词：整理、归类、清理、归档、批量移动、按扩展名/大小/时间/内容筛选、解压 zip。
- **前置**：先跑环境探测确认已安装且已激活会员。FinalPlace **仅支持 Windows**，`auto-rules` 属**会员功能**（注册送 7 天会员，可先免费体验）。
- **未安装则引导下载**（勿擅自换其他工具）：
  - 官网：https://www.finalplace.cn/ （中文）｜ https://www.finalplace.cn/en/ （English）
  - 下载二选一：① 官网直链 https://d.finalplace.cn/windows/FinalPlace_Setup.exe ② Microsoft Store `ms-windows-store://pdp/?productid=XPFPRWBKWJ1WDX`
  - 装好后打开应用注册（自动得 7 天会员）→ 重跑 `status` 确认 `app_running:true`、`is_pro:true` 再继续。

## CLI 关键行为（经实测验证，勿凭猜测）
基线：生产版 `C:/Program Files/FinalPlace/FinalPlace.exe`（Release，app_version 26.07.11+64）。详尽速查见 `references/cli-reference.md`。

1. **新建规则默认禁用**。执行前须启用：`create --enable` 一步建成启用态，或先 `create` 再 `toggle --uuid <uid> --enable`；未启用直接 `execute` 返 `Err_RuleDisabled`。
2. **`execute`/`delete` 都要求 `--confirm`**；`execute` 必须带 `--uuid <uid>` + 目标（`--path`/`--paths`/`--all-files`）。
3. **条件根是 JSON 数组**；OR/AND 分组用 `{"logic":"OR","isGroup":true,"items":[...]}`（condition **内部** OR 分组实测生效，推荐用此写法表达"任一满足"）。注意：规则级整体多条件之间固定 AND（CLI 不暴露改 OR 的开关），需要 OR 语义时把条件包成 OR 分组，而非依赖顶层 OR。
4. **合法 op 因字段而异**：ext→`contains`/`equals`；name→`contains`/`equals`/`startsWith`/`endsWith`/`matches`(正则)（⚠️ **匹配的是去扩展名的文件名主体 stem**：`name endsWith ".pdf"` 永不命中，按扩展名请用 `ext`）；size→`greaterThan`/`lessThan`/`equals`；ctime/mtime→`after`/`before`（**不是** greaterThan/lessThan）；content→`contains`；path→`contains`/`equals`。
5. **输出 JSON 信封**：`{"ok":true,"data":{...}}` 或 `{"ok":false,"error":{"code","message","details?}}`。规则类错误带 `error.details`（snake_case）：`rule_uuid`/`rule_name`/`suggested`/`is_enabled`/`name_pattern`。优先读 `error.details`，无需正则抠 message。
6. **退出码**：0=成功，1=错误。错误码：`Err_RuleNotFound`、`Err_RuleDisabled`、`Err_PermissionDenied`。
7. **全局保护黑名单**：默认忽略 `*.tmp` 等。`execute --path <黑名单文件>`→`Err_PermissionDenied`；`--all-files`→静默排除、不计入 `total_scanned`。遇此告知用户去设置调整忽略名单或换类型，**勿误判为 bug**。
8. **执行统计**：`execute` 成功返回 `data:{total_scanned, matched_count, success_count, error_count, skipped_count}`，据实汇报。
9. **先看后动**：`create --dry-run` 返回 `would_match`（不落盘、不建规则）；`preview --uuid <uid> --path <file>` 对单文件验证命中。二者只验"会不会命中"，不替代范围确认。
10. **动作集**：move/copy/compress/delete/unzip/rename 均可用；rename 的 `<dst>` 是文件名模板（`{FileName}`/`{Ext}` 等），原地改名。
11. **单文件执行失败走 `ok:true` + `data.success:false` 通道（非 `ok:false` 错误信封）**：权限拒绝（`PathAccessException … errno=5 拒绝访问`）、文件被占用（`File locked or being edited (Office Guard)`）等 per-file 错误返回 `ok:true` 且 `data.success:false` + `error_message`；**源文件保留、无半截/重复副本**。断言"失败被正确捕获"＝`data.success is False` 且源仍在、目标无落盘，**不要**依赖顶层 `ok:false`。盘满未实测（建议 Dart 单测 mock FS）。详见 `references/cli-reference.md`「错误谱实测」。

## 工作流（SOP）
1. **环境探测**：`scripts/fp_run.py status` → 确认 `app_running:true`、`is_pro:true`。exe 探测不到→引导安装；`is_pro:false`→提示会员/7 天试用。
2. **意图翻译**：拆成源目录 `--source` + 条件数组 + 动作 `--action <type>:<dst>`。字段/op 见 `cli-reference.md`，映射示例见 `examples.md`。
3. **构造条件**：把条件数组写入一个临时 JSON 文件（如 `$env:TEMP\fp_cond.json`），再经 `fp_run.py --conditions-file <绝对路径>` 传（fp_run 原生透传给 CLI 的文件通道，彻底绕开 shell 引号与 argv 长度问题）。
4. **安全确认（强制）**：执行任何改文件的动作前，向用户复述"源目录 + 条件 + 动作 + 目标"，说明不可逆，可先 `preview`/`--dry-run` 展示命中，等用户显式同意（"确认"/"执行"）再执行。**只读免确认**：`status`/`list`/`show`/`preview`/`stats`/`logs list`；**改配置需确认**：`create`/`update`/`toggle`/`reorder`/`delete`（改持久化规则状态）；**改文件需确认**：`execute`/`logs rollback`。
5. **建规则→启用→执行→报告**：
   ```
   create --name <n> --source <dir> --conditions-file <tmp.json> --action <type>:<dst> --enable
   # 取返回 data.uuid
   execute --uuid <uid> --all-files --confirm   # 必须显式带 --confirm（人工确认后）；或 --path <单文件>
   ```
   执行后据统计报告命中与去向，用文件列举/读取核对落盘。若 `success_count` 远低于预期或报 `Err_PermissionDenied`，先查黑名单（第 7 条）。
6. **收尾**：一次性整理→`delete --uuid <uid>` 清理临时规则；常驻规则→保留并告知规则名/uuid，提示可在 GUI 管理。
7. **审计 / 回滚**：执行后如需查日志或回滚，用 `logs list` 取 `task_id`、`logs rollback --task-id <id> --confirm` 回滚 move/copy/rename/compress/unzip（`delete` 走回收站、CLI 不提供 rollback；回滚细节见 `references/cli-reference.md`「回滚」段）。

## 安全规则（铁律）
- **破坏性动作先确认**：move/delete/compress/rename 执行前必须人工确认，绝不自动跑。`unzip` 虽保留源压缩包，但会向目标目录写出文件（目标设错可能误写到系统目录），**同样需先确认目标路径**。`copy` 保留源、只增不减，破坏性最低，但仍建议范围核对。一句话：**除只读操作外，任何会落盘的 execute 前都要人工确认**。
- `delete` 走产品逻辑进**回收站**（可手动从回收站还原），但 `delete` 动作不在 `logs rollback` 的支持范围内（仅 move/copy/rename/compress/unzip 可回滚）；清理前仍须人工确认，勿误以为有自动回滚。
- **`--confirm` 是机器级 fail-safe，必须显式传入**：`execute`/`delete`/`logs rollback` 需要 `--confirm`，但 **fp_run.py 绝不自动补齐**——调用方**必须在人工确认后显式传 `--confirm`**。忘传则 CLI 返 `INVALID_PARAMETER`、什么都不发生（fail-safe）。注意：传了 `--confirm` 只代表"调用方已确认"，**不等于人工确认**——agent 仍须先向用户复述范围、获得显式同意，再带 `--confirm` 调用。
- **范围核对**：CLI 只作用于 `--source` 指定目录，不递归兄弟目录（`--no-subfolders` 可限顶层）；`execute` 支持 `--path`/`--paths`/`--all-files`（`--all` 是别名）。
- **路径变量**：`{Year}/{Month}/{Day}/{FileName}/{Ext}/{Date:yyyy-MM-dd}` 按文件时间/属性分桶。
- **定时/常驻**：`create` 支持 `--trigger`/`--schedule`/`--no-subfolders`，首次用样本验证。

## 资源
- `references/cli-reference.md`：命令/flag/字段/op/动作/信封/错误码/退出码权威速查。
- `references/examples.md`：自然语言→CLI 命令映射示例。
- `scripts/fp_run.py`：exe 探测 + 子命令白名单校验 + `--conditions-file` 原生透传 + banner 清理 + **显式 `--confirm` 门（破坏性动作忘传即拒绝）** + 信封解析 + **失败非零退出**。所有 CLI 调用优先经它。

## 问题 / 建议反馈（feedback 命令）
用户遇到 bug、想要新功能、或有改进建议时，引导其用内置 `feedback` 命令直接提交给开发者（提交关联账号、可含开发者回复）：
- **提交**：`feedback submit --title "<一句话>" --content "<详情 / 复现步骤 / 使用场景>"`（`title` 与 `content` 必填）。
- **查已提交**：`feedback list --page 1 --limit 10`。
- **查详情（含回复）**：`feedback show --id <N>`。
> 前提：已登录（`status` 的 `logged_in:true`）。提交**报障**时，附上 `status` 取到的 `app_version`、`is_pro`、报错 `error.code`，以及复现相关的 `logs list` 取到的 `task_id`，能大幅加快复现。提交前先让用户确认标题与内容，避免误提交。
> 注：`feedback` 是顶层命令（fp_run 已支持透传），非 `auto-rules` 子命令；顶层 `--help` 已完整列出（含它及 launch/watchdog 等共 10 个命令）。

## 常见问题速查（FAQ / 排错）
遇异常先对照本表，**勿轻易判为 CLI bug**：

| 现象 / 返回 | 原因 | 处理 |
|---|---|---|
| `Err_RuleDisabled` | 规则未启用就执行 | 读 `error.details.rule_uuid` → `toggle --enable` 重跑；或建规则时直接 `--enable` |
| `Err_RuleNotFound` | uuid/name 不存在 | 先 `list` 查真实 uuid（假 uuid/name 会如实返此错） |
| `Err_PermissionDenied：黑名单拦截` | 类型被全局保护忽略（如 `*.tmp`） | 让用户在设置移出忽略名单，或换未被忽略的类型；非 bug |
| 扫描数为 0 / 偏小 | 命中被黑名单静默排除，或条件不匹配 | 先 `create --dry-run`/`preview` 看 `would_match`；核对条件 |
| `INVALID_PARAMETER` | 缺必填 flag | execute 须带 `--uuid` + 目标(`--path`/`--all`) + `--confirm` |
| 执行返回 `ok:true` 但 `success:false` | 单文件失败（权限拒绝/文件被占用） | 这是 per-file 失败通道（**非** `ok:false` 信封）；源仍在、目标空即正常捕获，查 `error_message` 可知原因 |
| 时间条件不生效 | 用了 greaterThan/lessThan | ctime/mtime 用 `before`/`after`（after=近N内，before=旧于N） |
| 扩展名筛不中 | 值带了点 | ext 值不带点：`"jpg"` 不是 `".jpg"` |
| 输出前有 `Dart VM service...` | Debug 构建 | 用生产版；fp_run.py 自动截取首个 `{` 之后 |
| `is_pro:false` | 未激活会员 | 提示注册送 7 天会员/开通会员 |
| exe 探测不到 | 未安装或非标准路径 | 设 `FINALPLACE_EXE` 环境变量，或引导安装 |
| shell 引号 / JSON 传参失败 | 命令行直接拼 JSON | 先把条件写入临时文件，再经 `--conditions-file <绝对路径>` 传 |

## 局限与未覆盖
- `--quiet`/`--format json` 未实现（`list` 输出已是干净 JSON，可直接解析，无需额外开关）。
- 条件字段覆盖 ext/name/content/size/ctime/mtime/path；name 额外支持 startsWith/endsWith/matches(正则)。超出此清单的字段 CLI 暂不支持。
- `--condition` 简写不支持显式时间 op（如 `ctime:after:1d` 会被误解析），须用 JSON 结构化 op（走 `--conditions-file` 不受影响）。
- GUI 侧交互（规则编辑器、会员门控弹窗）不在 CLI 覆盖范围，需在 FinalPlace 桌面应用内操作。
