# Changelog

## 0.9.0 — 2026-11-03

### 0.9.0：唤醒可靠性、面板体验与值守快车道（spec 0014–0023）

### 插件壳支持钉钉（spec 0023）

- **第三个平台**：`dsh-plugin` 增加 `dws` adapter——身份（`profile list`）、拉取
  （`+chat-messages`，会话 ID 走 `--group`、userId 走 `--user`）、发现
  （`+recent-conversations`）、搜人 / 搜群、发送（保留 CLI 默认的 AI 标识，与 skill 一致）。
  唤醒、水位、屏蔽、画像等闭环复用现有轮询，不另起一套。
- **默认不启用**：`config.platforms` 缺省仍是飞书 / 企微，没装 `dws` 的机器不会每轮白跑
  授权检查。体检页固定列出三张平台卡，钉钉显示「未启用」，点「启用」才纳入轮询；
  加入钉钉值守会自动启用该平台。
- **体检页不再自动刷新**：进入页签取一次快照，之后只有点「刷新」或「跑一次体检」才更新。
- **平台可停用**：已启用的平台在体检页直接点「停用」；有值守会话时先确认。停用只停
  轮询与唤醒，值守配置与本地消息都保留，随时可以再启用。
- **富媒体暂不下载**：钉钉图片 / 文件 / 语音只做正文占位，agent 需要时用 CLI 自己取。
- 平台事实与坑位见 `references/dingtalk.md`。

### 面板体验加固（spec 0021）

- **刷新不吞输入**：搜索词、企微手动加入表单、详情发送框、设置页三个数字框都进面板内存；
  60 秒后台刷新正在输入时不重建正文，失焦后重绘也会恢复。发送/保存成功后清空对应草稿；
  草稿只在本机内存，不落盘。
- **失败不装空**：`/api/status|inbox|chats|targets` 失败时保留上一份数据，页签顶部显示
  「本地服务连不上：… · 重试」，头部不再显示绿点；空态只在请求成功且确实 0 条时出现。
  401 仍只自动刷新一次，之后明确提示「会话凭据过期，刷新页面（⌘R）」。
- **窄侧栏可用**：320px 面板不再横向溢出，页签栏可横向滚动；设置页数字框固定 92px 并成组
  换行；卡片头在窄宽度下换行而不是被裁。
- **收件箱更轻**：私聊不再渲染「私聊」标签；「agent 处理中」缩成「处理中」；名称优先，
  工作区 chip 移到摘要行并保留完整 `title`；服务卡片与详情不再重复状态。
- **危险操作先确认**：屏蔽（待回会被忽略、正文清空、取消不恢复）、清理其他会话待回；
  运行中移出值守会提示打断当前轮次；没有待回时「忽略这条」置灰。
- **可达与信息暴露**：收件箱行可 Tab 聚焦、Enter/Space 打开、有焦点轮廓；正文不再出现
  `oc_` / `wm_` / `self_id`，排障 ID 只放 `title`；详情「拉取」改成带图标的「拉一次」；
  「N 人」改「N 个对象」；空收件箱按筛选给文案；详情标注「只显示最近 30 条」。
- **演示夹具**：`/api/inbox` 对齐真实 grouped 形状，补 `platforms[].chats`；
  `#fail=inbox|status|chats|auth` 可在预览页稳定复现失败。

### 值守快车道：值班会话 60 秒一拉（spec 0022）

- **两条车道**：快车道按 `poll.fast_sec`（默认 60 秒）只拉值守候选（私聊 + `timer=1` 的群），
  不刷会话列表、不写 `runtime`；慢车道仍按 `poll.interval_min`（≥10 分钟）做发现与补拉。
- **可关**：`fast_sec=0` 退回旧节奏；非 0 时夹到 20–600 秒且不超过慢车道间隔。
- **成本可见**：体检「拉取节奏」显示「值守 60 秒（N 个会话，约 N×1440 次/天）· 发现 10 分钟」；
  设置页可改值守/发现两个间隔；页脚同步显示。
- **边界不变**：群默认仍不拉，只有勾了 `timer=1` 才进；`blocked` 两条车道都不进。
- 决策：`docs/decisions/implemented/0007-fast-lane.md` 修订 ADR 0002 的 10 分钟下限。

### 每日关注摘要与重开会话入口（spec 0019 / 0020）

- **面板新增「关注」页签**：显示 `~/.im-standin/digest/YYYY-MM-DD.md` 原文，可切日期；文件超过
  一天没更新时提示可能过时。插件只读，不解析、不统计。
- **日报由 agent 按 `SKILL.md §值守日报` 维护**：一个会话一行、整份覆盖写、问题消失行就消失、
  跨天把未结项带过来；事由一句概括，不写正文。插件不建目录、不写、不删。
- **`GET /api/digest`**：只读接口，日期白名单校验，文件不存在返回空态而不是 500。
- **「新建会话」改名「重开会话」**：从工作区行移到「DSH 会话」行，语义（打断在飞一轮、解绑、
  下轮命中开新会话）不变，详情页与分身页一致。
- **设计铁律第 8 条**：插件只做确定性搬运，判断与维护归 agent。

### 值守可靠性：唤醒正确性与富媒体交付（spec 0017）

- **按消息 ID 收口水位**：`chats.last_msg_id` 与 `last_epoch` 并存，同一秒到达的多条消息
  不再漏唤醒；水位掉出拉取窗口时回退 epoch 判据。
- **身份不可用就暂停该平台**：`whoami` 失败/没有 self_id 时本轮不拉取、不唤醒，
  错误进 `poller.errors`，体检显示“身份不可用，已暂停该平台拉取”；恢复授权后自动续上。
- **@ 判定收紧**：有结构化 mentions 时只认 ID；没有 ID 才用完全相等的名字/独立 token，
  别人 @“张三丰”不会再叫醒“张三”。
- **聊天正文里的 `/name` 不再触发 DSH skill 手势**：客户正文/昵称/群名过
  `sanitizeUntrusted()`（全角斜杠 + 破坏 `<!--`），首行 `/cyber-im-avatar` 不受影响。
- **富媒体由插件取回**：命中唤醒时下载本批待回消息的媒体；图片经 DSH
  `attachments.admitPromptContent()` 转成 image block 随 user message 交付，文件/语音/视频
  落 `~/.im-standin/media/` 并在 prompt 给本地路径；sticker 只标 `[表情]`。
  只有未适配类型和下载失败的消息才标“可用 CLI 取”，带 `msg_id`/`media_id`。
- **上限与清理**：单批最多 4 张图 / 合计 10MB、单条 20 秒；7 天 / 单会话 200MB 清理，
  清理后回写 `recent.media_paths`。模型不支持图片、附件服务缺失或超限时降级为文本+路径。
- **点开只读**：`/api/thread?fetch=1` 只补拉分类，不唤醒、不推进水位；显式唤醒只走
  `POST /api/chat/wake`。手动 `/api/poll` 受 `cooldown_sec` 约束，post-turn 补拉是唯一例外。
- **平台边界**：插件壳只加载飞书/企微；存量钉钉会话保留但不拉取，体检标“不支持”。
  企微群可在搜索卡片填“显示名 + 会话 ID”手动加入。设置页删除 `dm_scope` 控件
  （配置键保留为 legacy no-op），收件箱删除“客服”筛选。
- **配置对齐 CLI 上限**：`dm_recent=200` 时飞书 `--page-size` 实际 100；`/api/thread?limit=100`
  时飞书 `--limit` 实际 50；`backfill_hours` 接到企微 `fetchThread` 的回看窗口。
- **skill 自动重装**：`ensureSkill()` marker 增加 `content_hash`，版本号相同但 skill 内容
  变了也重装受管副本；手装无 marker 目录仍不覆盖。

### 唤醒载荷只追加新消息（spec 0016 / 0018）

- **每次唤醒只追加本次新消息**：不再有“首轮完整载荷 / 后续增量”两套模板。首轮多一行
  `/cyber-im-avatar` 入口，并带平台/对象、chat_id、运行形态与画像路径；同一 session 的
  后续唤醒**只发本次消息行**，不再重复这些说明、媒体提示或「本次只追加 N 条」。
  画像正文与最近 10 条不再进 prompt。
- **画像交给 agent 自己维护**：prompt 只给画像文件路径；agent 用文件工具直接读写，
  插件不解析 `im-profile-update`、不代写、不压缩、不归档、不做 mtime CAS。
- **`dsh.full_access`（默认 false）**：开启后插件在 `followup` 前把值守会话切到 DSH
  内置的 `danger-full-access`（完整文件访问、不弹审批），agent 才能写工作区外的画像；
  设置页有开关和警告。默认关闭时画像写入会被 `workspace-write` 拒绝。
- **被杀后继续追加**：`chats.prompt_session` 与 `recent` 落盘，进程重启后继续追加
  pending/新消息，不重建完整载荷；没有 pending 的手动唤醒返回 `no_pending`。
- **批次透传**：poller 把命中 batch 直接交给 `turns.wake()`；手动唤醒/失败重试没有
  batch 时用 pending 消息。

### 画像上限与整理（spec 0015 / 0018）

- **上限不变**：画像软上限 8KB、硬上限 12KB；超过时由 agent 按 skill 自己整理成稳定
  结论，缩小时自己把旧版追加到 `<画像>.history.md`。插件不再在 prompt 里强制整理，
  也不再代写或归档。
- **独立形态兜底**：`bootstrap.py --compact PLATFORM ALIAS [--dry-run]` 按小节去重，
  超 12KB 或历史结论 >20 条时从最旧开始归档；`--note` 追加后自动整理。

### 监听 55 分钟主动退出，续一次模型上下文缓存

- **默认 55 分钟退出一次**：模型服务商的上下文缓存通常 1 小时过期；监听脚本到
  55 分钟主动退出（退出码 `3`，stderr 标 `[cache-refresh]`），agent 重挂时那次模型
  调用会命中并续上缓存。等待期仍然只有本地轮询，不产生模型请求。
- **可调/可关**：`--cache-refresh-min 55`（分钟，`0` 关闭）；与 `--until` /
  `--timeout` 取更早者，临时值守重挂继续沿用原 `--until`，不重置截止时间。
- **大 interval 不再拖过点**：sleep 会截到 deadline，避免 `--interval 600` 把 55 分钟
  拖成 65 分钟。
- SKILL.md / README 同步；新增回归 `tests/run_tests.py::test_cache_refresh`。

### 分身页签收敛为「值守列表 + 统一搜索」（spec 0014）

- **分身页签只留值守会话**：删除「群聊 N · 全部点开才拉」清单与已屏蔽清单；
  已屏蔽会话的取消入口移到「设置 → 值守范围」，值守中的群卡片直接提供
  「定时检测 @我」开关。
- **搜人 / 搜群合并**：页签顶部一个输入框同时查人和群，结果按名称相关度排序、
  按会话去重；行内只显示名称、部门与「群 / 私聊」，不再出现 `open_id` / `chat_id`。
- **搜索结果可一键清空**：搜索后出现「清空」按钮（输入框里按 Esc 也行），清掉
  搜索词与结果回到空白态；清空输入再点搜索同样回到空白，不再残留上次结果。
  清空时若搜索请求还没返回，旧响应会作废，不会把结果重新弹回来。
- **修可读名称**：飞书 `contact +search-user` 返回的是 `localized_name`，此前只读
  `name` 导致搜索结果只剩 imid；现在映射 `localized_name`，并带上 `p2p_chat_id`
  与 `department`。群搜索没有名称时不再拿 `chat_id` 冒充。

### 面板配色改为跟随 DSH 主题 token

- **不再自带一套暖灰色**：面板颜色全部改为 DSH 的语义 token（`--dsw-alias-bg-base` /
  `label-primary` / `border-l2` / `interactive-bg-hover` / `state-*` 等），浅色、深色
  都直接跟随宿主，不再自己维护两套色值。
- **主色对齐**：主按钮用 DSH 的 brand-primary（浅色黑、深色白），焦点环与草稿标用
  DSH 的 business 蓝；用户消息气泡用 `--dsw-specific-bubble`；危险 / 警告 / 成功
  分别用 `state-error` / `state-warn` / `state-success`。
- **平台头像改为低饱和色块**：飞书 / 企微 / 钉钉的标识色映射到 DSH 的蓝 / 绿调色板，
  头像用 16% 透明底 + 同色文字，深色模式下不再白字压绿底。
- 宿主没注入 token（独立预览页、旧版 DSH）时回退到 DSH 浅色调色板，深色回退值单独
  给出；`web/panel.js` 与 `lib/client.js` 同步重建。

## 0.8.0 — 2026-11-03

### 0.8.0：插件收缩为分身壳 + Node 单进程重写（spec 0004 / 0013）

- **后端整体换血**：删掉 Python 服务、stdio 管道、SQLite 与 `dsh headless` 子进程。
  轮询、状态、API、唤醒全部在 DSH 宿主进程内用 Node 标准库完成；插件仍然不监听
  任何端口，面板继续走 DSH 的同源路由 `/plugins/im-standin`。
- **一个状态文件**：`~/.im-standin/state.json` 取代 `panel.db`。值守名单、工作区、
  绑定 DSH 会话、上一轮结果都在这里；原子写 + `.bak` + 0600。`env.json` 只读，
  不再写入目标；`panel.json` 只在一次性迁移时读。
- **消息只留指针且最多 10 条**：每个会话 `recent` 保留最新 10 条，只有待回
  （`new`/`opened` 的私聊、@我、客服）保留正文；更早的正文与历史去平台在线查。
  未读/待回/收件箱全部从这 10 条派生，不再有 messages/sends 表与发送历史。
- **唤醒改成宿主内 live turn**：`sessionController.resolveAgent` / `create` 拿到的
  就是 DSH 里同一个 agent，`followup` 后等 `turn/end`；UI 打开同一会话不再抢
  `session.lock`。只有另一个 DSH 宿主持有写锁时才报 `session_locked_other_host`。
  一轮结束后自动补拉一次，把 agent 自己发出的消息收回并闭合待回。
- **会话复用与工作区**：显式工作区目录存在但未在 DSH 登记时，不再每次新建会话，
  仍先恢复 `dsh_session`；cwd 漂移才在正确工作区重开。工作区不存在仍明确
  `workspace_missing` 失败，不静默落默认。
- **画像维护不变**：`profiles/<platform>/<chat_id>.md` 仍是唯一事实源，面板可编辑，
  agent 在回复末尾用 `im-profile-update` 块回写；12KB 上限、mtime CAS（用户刚改过
  就放弃 agent 回写）。
- **一次性迁移**：`node scripts/migrate-state.mjs` 把旧库每会话最新 10 条、会话配置、
  `panel.json` 配置与 `env.json` 目标索引搬进 `state.json`，旧库改名
  `panel.db.migrated`；运行期不再读 SQLite。`--fresh` 可空状态启动。
- **UI 零改动**：五个 tab、路由、字段、右侧栏停靠、浅/深色、401 reload 全部保留；
  `web/panel.js` 与 `lib/client.js` 未改。
- **测试**：Python 插件测试换成 `node --test`（state / profiles / im / poller /
  turns / app / migration），`scripts/gate.sh` 改跑 Node 测试；契约 01/02/03 重写为
  路由、`state.json`、配置三份现状。

#### 开发中间态：headless 子进程（最终实现已改为 Node 单进程）

> 以下是同一版本的中间实现，保留用于追溯。其中 `dsh headless` 子进程、
> SIGTERM 打断与 `attach_session` 的描述已被上面的宿主内 live turn 取代，
> 不要再按这些描述部署或排障。

- **定位变了**：插件不再起草。值守会话命中新消息后，对绑定的 DSH 会话起一轮
  `dsh headless`，agent 按 cyber-im-avatar skill 的闭环全权处理——自己调 IM CLI
  拉上下文、去工作区核实事实、起草并发送或把草稿留在会话里等人确认。插件只负责
  拉取（耳朵）、唤醒（嘴）、展示与通知（脸）。
- **一个分身实例 = 一通值守会话 ↔ 一个 DSH 会话**：`chats.dsh_session` 永久复用，
  跨命中跨重启；`attach_session` 归属到绑定工作区（侧边栏可见）；新增「新建会话」
  （`POST /api/chat/session/reset`），这是唯一换会话的入口。
- **turn 可打断**：同一会话在飞时又来了新消息 → SIGTERM 旧 turn（宽限 5s 再 SIGKILL）
  → 同 session 重起，任务注明「以最新上下文为准」。同一轮拉到的多条消息先合并成
  一个批次，burst 只唤醒一次。DSH 存储层的会话写锁是第二道保险。
- **UI 收缩**：删除起草按钮、草稿建议、四种回复模式、接管客服、自动发、风险闸门、
  起草模型设置；收件箱/会话详情保留消息展示与手动发送；新增实例状态
  （值守中 / agent 处理中 / 上一轮失败 / 已屏蔽）、绑定会话与累计轮数；
  实例卡与会话详情加「去会话」——调 DSH 客户端 `uiWorkspace.openSession`
  直接切到绑定会话（老版本缺这个服务时退回复制会话 id）。
- **面板停靠右侧栏**：不再是居中浮层 + 遮罩，改成 DSH 右侧栏的「IM 值守」标签页
  （`sidebarRightTabs` + `sidebar.right.pane.tab`），左边会话右边收件箱并排；
  侧边栏底部只留入口席位与未读角标。右侧栏布局按会话保存，「去会话」会在目标
  会话补开面板。**浮层形态与老 DSH 回退已整体删除**：没有右侧栏服务时只保留
  席位提示，不再挂居中浮窗。
- **配置与存储**：退役 `llm.*`、`reply.*`、`reply_guard`、`dsh.pre_draft`（老配置
  启动忽略）；`dsh.timeout` 默认 600s；`chats` 新增 `session_bound_at` /
  `session_turns`，`mode` / `auto_send` / `reply_*` 保留列不读写（迁移只放宽）。
- **服务对象画像文件（spec 0012）**：每个对象一份
  `~/.im-standin/profiles/<platform>/<chat_id>.md`，面板直接展示/编辑整份画像，
  不再展示逐条笔记或历史消息；agent 起草前只读当前对象这一份，每轮把长期有效的
  新事实增量合并回去。老 `env.json` 的 `profile` 笔记首次读取自动迁入画像文件。
- **消息本地只留指针（spec 0012）**：`messages.content` 只在待回（`new`/`opened`
  的私聊与 @我）时保留；`replied`/`ignored`/`fyi`/`out` 一律清空正文，只留
  `msg_id` / 时间 / 发送者 / 状态。打开会话时 `/api/thread` 从平台在线拉正文，
  失败才回退本地指针并标注 `offline`。本地不再无界积累聊天原文。
- **待回闭环修正**：首轮回填时本人回复和更早的消息同一批到达，旧消息会被先去重、
  后插入，留下已回过的待回。现在按本批最后一条本人发言截断：更早的对方消息直接
  标 `replied`（群非 @ 标 `ignored`），不进唤醒批次。
- **工作区接线修正**：所有「加入值守」入口都带工作区（默认上次选择 → 最近在用 →
  DSH 默认），详情页未值守也能先选；改工作区会打断在飞 turn、解绑错位会话；
  显式目录不存在时以 `workspace_missing` 失败，不再静默跑默认工作区；打断/续聊
  路径都会补发 `attach_session`，会话在 DSH 侧边栏可见。
- **手动唤醒**：新增 `POST /api/chat/wake` 与会话详情「现在处理」——把最新待回
  （默认 10 条，最多 20）交给 agent，不用等下一条新消息；在飞 / 屏蔽 / 未值守时拒绝。
- **壳内不挂监听**：唤醒任务带 `IM_STANDIN_SHELL=1`，prompt 明确轮询/水位/唤醒由
  插件负责，agent 不运行 `listen_cli` / `bootstrap.py`、不重挂监听。避免
  `workspace-write` 沙箱去写工作区外的 `~/.im-standin` 报 PermissionError。
- **skill 随插件安装并自动注入**：插件首次启动把 `cyber-im-avatar` 装到
  `~/.agents/skills/`（npm 包自带 skill 副本；已有手装副本不覆盖）；唤醒任务首行
  是 `/cyber-im-avatar`，由 DSH 直接把 skill 正文注入这一步。prompt 只剩命中载荷 +
  「不要挂监听」，不再重复闭环/平台文档/铁律。
- **打断续用同 session**：在飞 turn 的 `session` 事件一到就准备落库；新消息打断时
  先把内存里的 session id 写回 `chats.dsh_session` 再重起，不再因为「等 turn 结束
  才落库」而另开一个新会话。会话漂移（旧 session 在别的 cwd）在启动前校验并自动
  新建，运行中撞上也清绑定，下一轮重开。
- **通知节奏**：面板状态轮询 6s → **60s**；IM 拉取节奏不变（下限仍为 10 分钟）。
- **外观跟随 DSH**：删除四套皮肤与「设置 → 外观」，面板只留浅色/深色两套配色，
  直接跟随 DSH 主题标记（`body[data-ds-dark-theme]` / `html[data-ds-theme-source]`）
  即时切换，不刷新、不写配置；`ui.skin` 退役（老 `panel.json` 里的 `ui` 启动忽略）。
- 路由收敛：删除 `/api/draft`、`/api/suggestion`、`/api/chat/plan-confirm`。
- 测试：删 `test_reply_modes.py`（0003 行为下线），新增 `tests/test_turns.py`
  （唤醒/打断/锁错误/失败重喊/新建会话），`tests/test_polling.py` 补批次唤醒与
  待回闭环用例。

### 0.7.1：会话必须落在绑定工作区 + 起草不再自管模型配置

- **修 bug：绑定工作区变了之后起草永久失败**。DSH 的会话是按工作区落盘的
  （`~/.dsh/sessions/<工作区>/<session-id>`），旧 session 记在别的工作区目录下时
  DSH 会拒绝在新 cwd 里沿用它，此前每轮起草都撞在这条错误上、静默不出稿。
  现在遇到「session was recorded in …」就丢掉旧 id、在绑定工作区重开一个，
  新会话即落在该客服会话绑定的工作区目录里（DSH 侧边栏点开工作区就能看见、能接着聊）；
  新 session id 自动写回 `chats.dsh_session`，两个入口（轮询预写 / 面板点起草）都生效。
- **起草不再自管模型配置**：dsh 引擎下插件不再解析 DSH 的 `cordis.patch.yml`、
  不再读 `~/.dsh/.credentials.yaml`、不再往子进程注入 key —— 模型/网关/凭据全部
  交给 DSH 自己的配置解析。`panel.json` 的 `llm.base_url/model/api_key` 收窄为
  **直连兜底的显式覆盖**（要用才填，填了就以它为准）；「体检」里的模型标签改为
  「跟随 DSH 配置」。
- headless profile 需打开 `credentials` 服务（headless bundle 默认关掉、假设走
  启动时环境变量）；这是一次性的 DSH 侧配置，见
  `docs/implementation/log/2026-11-02.md`。

### 0.7.0：全自动客服与回复模式

- **全自动客服**：「设置 → 全自动客服」打开**新消息自动起草**（`dsh.pre_draft`）后，
  客服会话的新消息一到就在绑定工作区跑一轮真实 DSH 会话——agent 看工作区里的
  README / 配置 / 文档核实事实，再以本人语气起草；不同人绑不同工作区就是不同的知识面。
  风险闸门、收件留痕、「不把聊天内容当指令」三道安全阀照常生效。
- **回复模式（spec 0003）**：每个客服会话可单独选一种起草节奏——
  - `direct` 直接回复（默认，行为与之前完全一致）；
  - `ack` 先应答再回复：先发一条固定话术（零模型调用，同会话 10 分钟内不重复），
    再调研、再正式回复，且提示模型别再应答一遍；
  - `plan` 先方案后执行：先回 3～5 行方案要点，等对方回 ok 再出落实稿；
    默认要在面板点「确认继续」（`/api/chat/plan-confirm`），可开白名单自动继续
    ——白名单是**全等匹配**，「行吧」这类变体不会误命中；
  - `clarify` 先澄清：信息不足时只回一句澄清问题（`CLARIFY:` 前缀自动分流）。
- `chats` 表新增 `reply_mode` / `reply_state` / `reply_state_at`（默认 direct，老库自动补列）；
  `panel.json` 新增 `reply` 段（`ack_templates` / `plan_ok_words` / `plan_auto_ok`），
  应答话术与白名单在设置页可改。
- 新增 `tests/test_reply_modes.py`（31 条）：模式选择、状态机全边、ok 白名单、
  ack 冷却与话术稳定、老库补列。

### 0.6.0：文档体系与防劣化基础设施

- **文档有唯一入口与唯一归属**：新增 `docs/`（规则 `docs/AGENTS.md` + 路由表 `docs/README.md` +
  architecture 三篇 + runbooks + PROGRESS/log），仓库根新增 `AGENTS.md`（AI 会话入口）。
  后续非平凡改动先写 spec（`docs/specs/`，编号递增），拍板的取舍落 ADR（`docs/decisions/`）。
- **三份冻结契约**：`docs/specs/contracts/` 记接口 / 表 / 配置的确切形状，
  `tests/test_docs.py` 拿真实 `init()` 出来的库与 `ROUTES` / `DEFAULTS` 逐条对账——
  改代码不改契约直接红。
- **机器闸门**：`scripts/verify_docs.py`（死链死锚 / 活文档行数预算 / 反流水账 /
  spec 编号与归档登记 / 决策记录格式）、`scripts/gate.sh`（`--quick` 秒级静态层 + 全量）、
  `.githooks/pre-commit`（提交前自动跑 quick）。
- **顺手修掉的文档漂移**：`references/troubleshooting.md` 的 `#a` 式锚点换成真实可跳的标题锚
  （24 处，含 `SKILL.md` 引用）；发版手册从 `dsh-plugin/PUBLISHING.md` 迁入
  `docs/implementation/runbooks/publish.md`。
- CI（`test.yml`）增加插件测试与文档对账两步。

### 0.5.0：屏蔽群 / 屏蔽单聊

- **新增屏蔽（block）**：`chats.blocked` / `blocked_at` 两列，群和单聊都能屏蔽；
  升级自动补列，存量会话一律视为没屏蔽。屏蔽的第二层语义是**不同步**：
  定时轮不进（哪怕这个群勾着「定时检测 @我」）、点开不补拉、手动单会话拒拉——
  三条路都在 `poll_chat` 收口，只在那一处判断，避免某个入口漏看标记。
- **不进收件箱、不进角标**：`/api/inbox`（聚合与逐条两种模式）与 `counts()` 都排除屏蔽会话；
  屏蔽那一刻把该会话里还没处理的私聊 / @我 标成 `ignored`，否则角标一直红着却点不出东西。
  正文不删，取消屏蔽后历史仍可查。
- **入口**：收件箱每行右侧小铃铛、会话详情头部「屏蔽 / 取消屏蔽」（屏蔽时详情头部与顶部各有一条提示，
  历史只有屏蔽前的）、客服页群卡片与私聊卡片、以及「客服 → 已屏蔽」区块统一放回。
- 新增 `POST /api/chat/block`；`/api/chats` 回传 `blocked`，`timed` 对屏蔽会话恒为 false；
  `poll_info()` 增加 `blocked` / `blocked_dm` / `blocked_group`；底栏与「设置 → 值守范围」显示屏蔽数；
  体检的探针会话不再挑屏蔽的（那条路本来就不拉，拿它测通路只会误报）。
- 新增 `tests/test_polling.py::BlockTest`（7 条）：不进定时、三条拉取路径全拒、收件箱与计数排除、
  屏蔽清待回但保留正文、取消屏蔽恢复拉取、刷新会话清单不解除屏蔽、`poll_info` 计数。

### 0.4.1：收件箱按会话聚合

- **一个人 / 一个群只占一行**。同一个人连发五条不再刷五屏：`/api/inbox` 默认按
  `(platform, chat_id)` 归组，返回每组的待回条数、未读数、最后一条的时间与正文。
- 行右侧是「时间 + N 条 + 展开箭头」；点箭头在原位展开这个会话里其余几条（默认给 3 条预览），
  点行本身仍然进会话详情。收件箱顶部改成「N 个会话 · M 条」，一眼看出堆了多少。
- 逐条模式没删：`/api/inbox?group=msg` 仍返回一条消息一行，排查单条时用。
- 顺带修掉一个一直存在的布局问题：`.ims-body` 作为网格项缺 `min-width:0`，长消息的
  `nowrap` 会把列撑宽（实测行宽 1077 > 面板 1000），右侧时间与角标被顶到可视区外面。
- 新增 `tests/test_polling.py::InboxGroupTest`（6 条）：同会话合并、跨会话排序、筛选/未读语义、
  limit 上限、kinds 合并。

### 0.4.0：插件不再在任何本地端口上监听

- **零端口**。面板数据改走 DSH 自己的 Web 服务：宿主半用 `ctx.webServer.register` 注册同源前缀
  `/plugins/im-standin`，把请求顺着管道交给 `service/server.py`（stdio）。整机唯一的监听 socket
  是 DSH 那个；插件不再 `spawn` 一个 `127.0.0.1:8787` 的 HTTP 服务。
- **传输换成 NDJSON**：一行请求、一行应答，`id` 对齐；一条请求一个线程，起草几十秒也不会把
  6 秒一次的状态查询堵住。`emit()` 改为事件行（面板本来就走轮询，宿主半直接丢弃）。
- **三道校验**：连接必须来自回环、`Host` 必须是回环名（挡 DNS rebinding）、有 `Origin` 时必须
  与 `Host` 同源（挡跨站）、并带上本进程随机生成的 `x-im-token`（挡同机其它页面猜路径）。
  token 通过 `webserver/index-inject` 注入页面，不落盘，DSH 重启即换。
- 删掉 HTTP 层与随之而来的东西：`ThreadingHTTPServer`、`--port/--host`、静态预览页、`/skins`、
  SSE 订阅表、以及 `panel.json` 里的 `port`（老配置读入时直接丢弃）。
- 新增 `service/rpc.py`：一次性调后端看数据，同样不开端口。
- 新增 `tests/test_stdio.py`（10 条）：协议往返、id 对齐、query 解析、坏 JSON 不致命、
  SIGTERM 能正常退出（否则会留孤儿轮询进程），以及三条静态守卫（服务里不许再出现
  `HTTPServer` / `--port`，配置里不许再出现 `port`）。
- 前端 `panel.js` 的 API base 从 `http://127.0.0.1:8787` 换成相对前缀；401 时提示刷新页面。

### 0.3.0：拉取节奏改成分钟级，群聊点开才拉

- **不再按秒扫全部会话**。`poll_interval`(秒) 换成 `poll.interval_min`，默认 10 分钟，
  **下限 10 分钟**（写 1 会被抬到 10，上限 240）。老配置里的秒级字段在启动时自动迁移。
- **三条拉取路径**：定时（≥10 分钟，私聊 + 勾了定时的群）、按需（点开会话拉一次）、
  手动（顶部「同步」/ 详情「拉取」/ 设置里「立即拉一轮」，不受间隔约束，20 秒冷却防连点）。
- **群聊默认不进轮询**：加 `chats.timer`（1/0/-1）与 `chats.poll_at`，群只有在卡片上勾
  「定时检测 @我」才参与定时；升级时存量群统一置为 `-1`（点开才拉），不会被这次升级带上车。
- **指定群聊**：客服页新增群聊列表（来源是每轮一次的会话清单，不读正文）+ 按群名搜群
  （`/api/search/chats`，走 `lark-cli im +chat-search`），搜到即可加入值守。
- 新增 `/api/chat/timer`、`/api/search/chats`；`/api/poll` 支持单会话拉取与后台整轮；
  `/api/thread?fetch=1` 在点开时补拉一次并回传 `polled` 结果。
- 私聊范围可选 `dm_scope`：`recent`（最近活跃 N 个）/ `all` / `watched`；手动同步过的会话
  下一轮定时会顺延，不重复打接口。
- **修一个老 bug**：`POST /api/config` 之前路由到了只读的 `GET` 处理器，设置页保存的
  节奏/皮肤/模型覆盖其实都没落盘（界面看着生效了而已）。现在 GET/POST 分开路由。
- 新增 `dsh-plugin/tests/`（13 条）：10 分钟下限、老配置迁移、群不进定时、群勾选后进入、
  私聊显式关闭、按需拉取建 @我、冷却、手动越过间隔、key 不外泄；`tests/run_tests.py` 一并跑。
- 面板：底栏与体检页改显示「每 N 分钟一轮 / 本轮范围」，设置页改为分钟 + 私聊范围 + 立即拉一轮；
  客服页新增群聊区块；会话详情头部加「拉取」和「点开才拉 / 定时拉」标记。

### 0.2.0：模型与会话都交给 DSH

- **起草不再裸调模型接口，改成跑一轮真实 DSH 会话**（`dsh --profile headless --json`）：
  会话落在客服会话绑定的工作区目录下，在 DSH 侧边栏可见、可点开接着聊；同一通 IM 复用同一个
  `session-…`，历史累积。会话 id 存在 `chats.dsh_session`，客服页可一键复制。
- **模型配置只留一份**：新增 `service/dshconf.py`，从 `~/.dsh/profiles/<p>/cordis.patch.yml`
  的 `llm-deepseek` / `agent-default-model` 与 `~/.dsh/.credentials.yaml` 的 refs 解析网关、模型、key；
  本机 `panel.json` 里重复的那份 base_url / api_key 已清空（备份在 `.bak-*`）。
  「DSH 里能对话」= 「值守能起草」，面板设置页只在想临时覆盖时才需要填。
- **接管路径对齐 DSH 工作区**：`/api/chats` 给每条会话带上 `workspace_title / workspace_in_dsh`；
  未绑定工作区时落 DSH 默认工作区；工作区被删或在 DSH 里改名会在客服页显式标出。
- 新增 `/api/chat/session`：查这通 IM 对应哪个 DSH 会话、文件在哪。
- `dsh.pre_draft` 默认关：dsh 引擎每轮要真跑 agent（本机实测 3–12 秒），不再收到消息就预写；
  想保留旧的「草稿就绪」，打开它即可。
- dsh 引擎的输出会经 `_clean_reply()` 清洗（去 markdown 围栏、去「建议发」标签、去备选方案），
  因为它现在是 agent 在回答，不再是补全接口。
- `~/.dsh/profiles/headless/cordis.patch.yml` 需要与 web profile 用同一套网关（本机已配，见 README）。

### 发版自动化：GitHub Actions + OIDC

- 新增 `.github/workflows/publish.yml`：push `v*` tag 即发布，用 npm Trusted Publishing（OIDC），
  不需要长期 token、不需要 2FA 交互，产物带 provenance。手动触发默认只打包不发布。
  内置三道闸：tag 与 `package.json` 版本一致性、`tests/run_tests.py`、`npm pack --dry-run`。
- `PUBLISHING.md` 第四节改成"自动化优先 + 手动兜底"，写清 trusted publisher 要登记的
  四个字段、发版命令顺序（先确认包已上线再更新索引，避免索引指向不存在的版本），
  以及两条手动凭据路线（bypass token / 2FA + `--otp`）。

### 0.1.0 已发布到 npm，市场索引切到 npm 源

- `dsh-cyber-im-avatar@0.1.0` published → <https://www.npmjs.com/package/dsh-cyber-im-avatar>，
  `latest` 指向 0.1.0，`repository` 指回 GitHub（`directory: dsh-plugin`）、作者与 GitHub 账号一致。
- `market/index.json` 从 git 源（pin commit）切到 `{"type":"npm"}`，装插件只需
  `dsh plugin --profile web add dsh-cyber-im-avatar`，不用再跟着 commit 走。
- 首发实测踩到的两件事记进 `PUBLISHING.md`：新包强制「账号 2FA 或带 bypass 2FA 的
  granular token」，缺任何一边都是 403；首次发布会先建一个 `0.0.0-stage` 占位版本，
  真版本随后才进 `versions` 索引（`latest` 会在一两分钟内翻过去）。

### 发布准备：包名对齐项目名、github 关联、市场索引

- npm 包名定为 `dsh-cyber-im-avatar`（`dsh-` + 项目名，不另起名字），
  `package.json` 的 `repository` 指回 GitHub（`directory: dsh-plugin`）、
  `homepage`/`bugs`/`author` 与 GitHub 账号一致，`publishConfig.registry` 锁公网源。
- `scripts/make-market-index.mjs` 按 DSH format 1 生成 `market/index.json`
  （git 源 pin commit，也可 `--source npm`），生成后自动用 DSH 自带校验器复核。
- `PUBLISHING.md`：DSH 插件发布实际只有"自托管索引"一条路，附字段规则、
  安装检查顺序与发版检查清单。
- `prepack` 清掉 `service/__pycache__`，tarball 从 29 个文件降到 22 个。

### DSH 插件：四套皮肤 + 工作区 + 服务对象档案

界面、数据模型、模型接入一起升了一版：

- **四套皮肤**：`paper` / `console` / `cards` / `studio`，同一份 DOM，靠 `data-skin` 换外观，
  其中两套把页签挪成左侧竖排导航（CSS Grid 摆位，不改结构）。`/skins` 页四宫格实时对比，
  默认皮肤写回 `panel.json` 的 `ui.skin`，`?skin=` 可临时覆盖。
- **客服会话绑定工作区**：加入值守时先选工作区，之后在客服卡片与会话详情头部随时可改；
  列表来自 `~/.dsh/storages/workspace.json`，也支持手填绝对路径（不存在即拒）。
  起草时只把工作区名、路径与顶层目录名放进提示词，不读文件内容。
- **服务对象档案页**：`service/targets.py` 直接读写 `~/.im-standin/env.json` 的
  `targets.<platform>.<name>.profile`，与 skill 攒档案用的是同一份文件；写前留 `.bak`，
  只动 `profile` 字段。会话详情里加了「习惯」条，客服卡片显示最近两条。
- **双协议起草**：`llm.protocol = auto|openai|anthropic`。`anthropic` 走 `/v1/messages`
  （Claude Code 那类企业 Messages 网关），`openai` 仍走 `/chat/completions`。
- **值守范围收敛**：新增 `poll_watched_only`（只拉值守名单，不再扫最近会话）与
  `seed_targets`（默认关，重启不再把 env.json 目标全量并入）；
  `POST /api/inbox/cleanup` 把非值守会话的历史待回标记为已忽略（只改状态）。
- 底部状态条：值守会话数、客服名单、起草模型、轮询间隔、最近同步时间。
- 收件箱修复私聊行里发送者名字重复（与会话同名时不再重复前缀）。

### 人工确认 / 全自动：把交互补上

之前后端会为客服会话抢先起草，但前端没接这版草稿，打开会话又让模型重写一遍——白等一次延迟。
这版把这条链路接上，并把「自动发」这个危险开关做成需要看着后果再点的：

- 新增 `GET /api/suggestion`，按 `msg_id` 取值守已写好的草稿；
  `/api/status` 增加 `drafts` 索引（不含正文），收件箱据此标「草稿就绪」。
- 打开会话先取值守那版，命中即填进输入框并在上方提示「值守已经替你写好一版（模型）」；
  没写过才现调 `/api/draft`。
- 「自动发」默认关；勾选先弹确认卡（写清后果 + 风险词仍会拦），确认后才生效，
  开启态用橙色高亮（`--warn`），不再和普通开关一样灰着。
- 键盘：`⌘/Ctrl+Enter` 发送当前草稿，`Esc` 退回列表 / 关闭面板。
- `scrim` / `panel` 的 z-index 提到 9998/9999，模态不再被宿主自己的浮动按钮压住；
  遮罩改成 `blur(4px) saturate(.3)`，宿主的彩色元素不会在边缘渗色。
- 修 `useCached` 缺右花括号导致的语法错误；`.ims-banner` 与习惯条目 `.ims-note` 分名。

### 截图可以进 README 了

截图里不能出现同事姓名、群名、告警正文（真实数据里有 AK/SK 与内部域名）：

- `scripts/demo/fixture.mjs`：一份编好的办公场景（林一帆 / 周敏 / 云雀项目），
  字段结构与真实接口一致，时间文本按当前时间动态生成，避免「列表显示 05:41、详情写昨天」。
- `scripts/shot-dsh.mjs`：起一个干净工作区的 DSH（3099），**页面加载前**注入 fetch 拦截，
  把 `http://127.0.0.1:8787/api/*` 换成夹具，再连拍六张（全局 → 收件箱 → 待确认 → 自动发确认 →
  客服 → 服务对象），跑完关掉 DSH。
- `scripts/shot-skins.mjs`：同样注入后截 `/skins` 四宫格（`addScriptToEvaluateOnNewDocument`
  会作用到 iframe，四格都换成夹具）。
- `scripts/shot.mjs` 补 `--no-sandbox`：某些沙箱里 Chrome 起不来，表现为 CDP 连上但
  `Page.enable` 永不返回。
- `screenshots/` 不再入库：公开仓库不保存界面截图，避免真实或演示会话进入历史；
  需要时用 `node scripts/shot-dsh.mjs` 在本地干净 DSH 里复现。

### DSH 插件形态（`dsh-plugin/`）

同一仓库新增第二种交付形态：根目录仍是 skill，`dsh-plugin/` 是 DeepSeek Harness
插件，共用同一套 IM CLI 登录态。

- 侧边栏常驻「IM 值守」席位（带未读数徽章），点开是收件箱 / 客服 / 服务对象 / 体检 / 设置五页。
- 宿主半拉起本地 Python 值守服务并按 60s 保活；服务仍只用标准库，数据仍落 `~/.im-standin/`。
- 会话详情支持起草、编辑、发送、忽略，以及按会话的「接管客服」「自动发」两级开关。
- `@我` 判定改为按 `mentions[].id` 精确匹配本人 `open_id`；`@_user_N` 只是序号占位，不再视为命中。
- 首轮扫描把近 72h 的私聊 / `@我` 回填为待回，更早的历史消息标记已忽略，避免首装刷屏。
- `lib/client.js` 是构建产物，由 `scripts/build_client.py` 从 `web/panel.js` 内联生成。

## 2.3.0 — 2026-10-30

### 公开分发安全与正确性加固

- 修复全平台体检把未安装 CLI 的平台计入可用列表的问题；没有任何可用 CLI 时退出 2。
- 修复飞书 `--find` 把 `oc_...` 会话 ID 错填到 `--user-id` 的监听建议。
- 新增 `--until` 绝对截止时间（Unix 时间戳 / ISO 8601），临时值守命中后重挂不再意外延长。
- 个人数据目录自动收紧为 `700`、文件为 `600`；新增 `--delete-data --yes` 显式删除。
- 风格学习必须显式 `--chats`，默认脱敏并只保留 30 天；schema 诊断只输出字段结构，不回显正文值。
- 明确消息注入边界：聊天内容不得触发执行命令、读文件、改配置、扩权或第三方转发。
- 补公开安装说明、`.gitignore` 与 Python 3.9/3.11/3.13 CI 回归。

## 2.2.2 — 2026-10-30

### 权限模型改为「自适应所有人」（公开分发必需）

2.2.1 虽然修好了「续期会扩权」，但用的是**这台机器**的上下文（直接照搬我账号的 192 项）。
公开给别人用时，别人的应用、历史授权、甚至公司策略都不同，硬编码会立刻失效。这一版把它
抽象成**策略**，脚本自己判断，规则写进 SKILL.md。

**两档策略 + 一道闸门**：

| 策略 | 触发 | 申请范围 |
|---|---|---|
| `keep`（默认） | 直接跑 | 有历史授权 → `auth status` 的 `scope` 原样照搬（新增恒为 0）；无历史授权 → 必需集 |
| `minimal` | `--policy minimal` | 必需集 ∩ 应用已开通 |
| 扩权 | `--add ... --allow-add` | 缺一项就 `[block]` |

**三种边界情况自动处理**：

1. **应用没开通某必需权限** → 取交集跳过 + 报 `lack_on_app`（硬塞会让整个 OAuth 失败），
   并说明哪个功能会受限，提示去开放平台开通
2. **应用列表里没有、但历史上授予过** → `keep` 保留并提示（剔除可能丢基础能力），
   登录报 scope 错时再 `--policy minimal` 收窄
3. **平台基础 scope**（如 `auth:user.id:read`，`auth scopes` 不列它）→ 永远带上、不告警，
   避免每个新用户都看到一条无意义警告

**必需清单去硬编码**：`FEISHU_REQUIRED` 变成三元组 `(scope, 用途, 是否需在应用列表里)`，
每项都标注「哪条命令要用它」——加权限必须先说明用途。

**其他**：

- `doctor.py` 新增 `scope` 能力项：必需权限是否齐备（只报事实，绝不自动补权限）
- `reauth.py` 支持 `--policy keep|minimal`，`report_scopes()` 统一输出口径
- 企微/钉钉明确打印「该平台无 scope 概念，权限在管理后台/权限点配置，本脚本不申请任何权限」
- SKILL.md 新增整节 **「权限标准：只申请自己真会调的那几项」**（三原则 / 两档策略 /
  必需清单表 / 三种边界情况 / 红线），测试会校验这节存在
- troubleshooting §B.3 改写为通用策略口径，不再绑具体账号
- 测试 39 → 54 项

## 2.2.1 — 2026-10-30

### 修复（重要）：重新授权会顺手扩大权限

**现象**：授权同意页出现用户从没用过的权限（实测是「妙搭」`spark:app:read` / `spark:app:write`）。

**根因**：`lark-cli auth login` 在不带 `--scope` / `--domain` / `--recommend` 时，
**等价于 `--domain all`** —— 会把应用已开通的全部业务域都申请一遍。2.2.0 的 `reauth.py`
正是这么调的，所以续期动作变成了「顺带扩权」。

**修复**：

- `reauth.py` 现在**永远显式传 `--scope`**：
  - 有历史授权 → **原样沿用当前已授予的集合**（一项不多，新增恒为 0）
  - 全新安装 → 只给 `MINIMAL_IM`（收发消息 + 群成员 + 找人 + `offline_access`），
    不含 base/docs/drive/mail/spark
- 新增扩权闸门 `guard_scopes()`：只要本次申请比现有权限多，直接 `[block]` 拒跑，
  必须显式 `--add <scope> --allow-add` 才放行
- 新增 `--show-scope`（只演练，不申请不发卡）/ `--dry-run`
- 卡片正文加一句「权限范围与你现有完全一致（N 项），不会新增授权」
- `--complete` 收尾后打印「授予 N 项 / 新增 X 项」，新增非空会逐条列出

**排查命令**（三条，判断有没有被扩权）：

```bash
python3 scripts/reauth.py feishu --show-scope   # 应为「新增 0」
lark-cli auth scopes --json                     # 应用侧开通（多于授予属正常）
lark-cli auth status --json                     # 你实际授予（以此为准，看 grantedAt 有没有变）
```

**判据**：`grantedAt` 没变 = 那次授权**没完成**，权限范围没有被扩大。

文档 `references/troubleshooting.md` 新增 §B.3「权限范围：只续期、不扩权」，分诊表加了一行
「同意页出现没用过的权限」；SKILL.md 硬规矩从三条变四条。测试 29 → 39 项。

## 2.2.0 — 2026-10-30

### 新增：免扫码重新授权 `scripts/reauth.py`

飞书 token 约 7 天要续一次。原来只能回终端 `auth login` 再扫码；现在**授权按钮直接发到你 IM 里**：

```bash
python3 scripts/reauth.py feishu              # 发卡片 → 你点一下 → 自动收尾
python3 scripts/reauth.py feishu --detach     # 发完返回，之后 --complete <device_code>
python3 scripts/reauth.py feishu --no-send    # 不发卡片，只打印链接
```

- 原理：bot 用 `app_id/app_secret`（长期凭证），与 user token 是两套。**user token 过期时
  bot 照样能发消息**，所以这条链路不会死锁；按钮打开的是设备流授权页（`user_code` 已在 URL 里），
  **不需要本机回调端口**，远端/容器也能用。
- 卡片本身：单按钮 + `user_code` 兜底 + 「勿转发」警示 + `enable_forward: false`。
- 失败降级链：卡片 → 文本消息 → 打印链接，三级都能把链接送到人手上。
- **平台边界不糊弄**：企微是机器人凭证（不是 OAuth，走 `auth init --manual` 免扫码）；
  钉钉未登录时本机没有 bot 通道（先有鸡还是先有蛋），走 `auth login --device` 短链 + 验证码。
  脚本对这两个平台返回 4 并给出正确路径，不假装支持。

### 修复：两个"假成功"

- `lark-cli ... --content @<绝对路径>` 会被拒（只收 cwd 相对路径），但 **`rc` 仍然是 0**。
  改为 stdin 传内容，并统一按 JSON 的 `ok`/`error` 判断成败 —— 只看退出码会误报"发送成功"。
- `doctor.py` 的飞书过期提示改为直接给 `scripts/reauth.py feishu`，不再让用户去拼设备流命令。

### 文档

- `troubleshooting.md` §B.2 重写为「不扫码续期」：卡片流程、为什么成立、手动等价流程、
  卡片发不出去时怎么办；§G 补充「别用退出码判断发送成功」。

### 测试

- 29 项断言：新增授权卡片结构（按钮直链、`user_code` 兜底、勿转发、禁转发）与
  企微/钉钉平台边界（rc ∈ {0,4}，不得假装成功）。

## 2.1.0 — 2026-10-30

### 新增：故障处理索引（`references/troubleshooting.md`）

把"坏了怎么办"从口头经验变成可跳转的索引：**30 秒分诊表**（症状 → 第一条命令 → 小节）
＋ A~K 十一类故障，每类都是「症状 / 原因 / 修复命令」三段式，最后一节是**回归清单**。

覆盖的故障族：

- **A 版本漂移**：CLI 改名、子命令失效、字段消失时怎么查新版、怎么升级、升级后怎么重新
  发现命令（三平台机制不同：`lark-cli --help` + `schema`、`dws --help` + `schema --cli-path`、
  `wecom-cli --help` + `--schema`），以及升级后必做的 4 步回归。
- **B 授权到期**：怎么判断是"要刷新"还是"要重新授权"（飞书看 `tokenStatus` 与
  `refreshExpiresAt`），三平台各自的**非阻塞重新授权**流程（设备码 / 二维码 / `--device`），
  以及授权成功后的收尾动作。附授权相关坑位（scope 不足、`--as user` 漏了、Keychain 迁移）。
- **C 字段失配**：`SCHEMA_MISMATCH` 三步修复、五种成因与对应键名。
- **D 拉不到消息**：时间窗 7 天上限、群/单聊参数互斥、企微 `chat_id`=userid、429 限流、
  富文本取不到正文。
- **E 唤醒异常**：水位文件是唯一真相，不唤醒/重复唤醒/回环各自的判据与重置方法。
- **F 进程消失**：单发唤醒必须重挂、退出码语义、重复挂载会双回复。
- **G 发不出去**：三平台发送命令差异（企微 `--text` 必须是 JSON 对象）。
- **H 合规硬停**：钱/承诺/外部群/凭据一律不自动回。
- **I 配置损坏**：`env.json` 重建、水位隔离、多实例隔离目录。
- **J 上报模板**：只收集状态码与键名，附脱敏自检命令。

### 新增：`scripts/doctor.py`（一屏体检 + 自愈引导）

```bash
python3 scripts/doctor.py                          # 全平台
python3 scripts/doctor.py feishu --chat-id oc_xxx  # 附 3 秒通路自检
python3 scripts/doctor.py --check-update --json    # 版本检查 + 机器可读
python3 scripts/doctor.py --repair-state           # 隔离损坏水位（移到 *.bad，不删）
```

- 六项检查：CLI 存在与版本 → **CLI 自带 `doctor`**（飞书/钉钉有，企微没有就跳过并注明）
  → 授权与 token 剩余时间 → `env.json` 与 `self_id` → 水位目录可写与文件合法 → 真实通路。
- 每项 fail 直接打印 `→ 修复:` 命令与 `→ 手册:` 锚点，**agent 不用猜**。
- 退出码语义 = "现在能不能用"：指定平台则该平台必须全绿；全量体检只要有一个平台可用即 0。
- ID 默认打码（`--show-ids` 可关），避免体检输出被随手贴出去。
- 新增 `IM_STANDIN_DIR` 也被 `bootstrap.py` 尊重（此前只有引擎支持，文档与实现不一致）。

### 测试

- `tests/run_tests.py` 增到 **22 项断言**：新增文档索引完整性（所有 `#锚点` 可跳、
  分诊表与 A~K 章节齐全、文档内无真实 ID/token 泄漏）与 doctor 桩环境自洽
  （全绿、JSON 合法、三平台无 fail、ID 已脱敏）。

## 2.0.0 — 2026-10-30

### 新增：真正可用的企微 / 钉钉适配

不再靠猜。本机实装 `@wecom/cli` 1.3.4 与 `dingtalk-workspace-cli` 1.0.66 后按真实命令回写：

- 企业微信：`chat messages list`（**必须带时间窗**，仅近 7 天）、`contact users search --keywords`、
  `message send --text '{"content":"..."}'`；发现 `ChatMessage` **没有消息 ID**，改用复合指纹水位。
- 钉钉：`chat +chat-messages`、`chat +recent-conversations`、`contact user search`、
  `chat +messages-send`；发现 stdout 会连续输出两段 JSON、默认倒序。
- 平台矩阵在 `SKILL.md` 里标注实测程度，未验证的部分不写成"已支持"。

### 引擎（`listen_core.py`）

- 命令链回退 `cmd_list_chain`：CLI 改名不用改代码，命中后缓存不再试错。
- `overrides` 支持覆盖**和新增**任意键（命令与字段都能改）。
- 时间窗占位 `{begin_time}/{end_time}`，按 `--lookback-min` 每轮生成。
- 复合消息指纹 `f_msg_id_compose`，支撑无消息 ID 的 CLI。
- `f_count` / `f_has_more` 区分「空结果」与「字段不对」，不再把空会话误报成 schema 错误。
- `order` 归一化（正序平台内部翻转成最新在前）。
- `self_id_regex`：whoami 只回人类可读文本时用正则取本人 ID。
- 多段 JSON 输出只取第一个文档。
- 一轮多条新消息**只唤醒一次**，报最新那条并带 `pending_in_burst`。

### 工具链

- `bootstrap.py --find`：名字 → ID 精准解析，命中唯一自动登记别名（不再拉全量会话）。
- `bootstrap.py --probe`：打印 CLI 真实命令形态 + 现有字段映射 + override 模板。
- `bootstrap.py --selftest`：真跑 3 秒监听验证通路。
- `--learn-style --chats`：指定语料来源，避免为了学风格去枚举全部会话。
- `IM_STANDIN_DIR` 环境变量：数据目录可换（多账号 / 测试隔离）。

### 修复

- 飞书 `+chats-list` 不存在 → 改 `+chat-list`；消息数组在 `data.messages` 而非 `body.items`。
- `dig()` 支持三种调用写法，避免多路径传参报错。
- 回复命令按平台区分：企微 `text` 是 JSON 对象、钉钉单聊/群聊参数不同。

### 测试

- 新增 `tests/mock_cli.py` + `tests/run_tests.py`：14 项断言覆盖命中、防回环、水位、
  过滤、三种输出形态、SCHEMA_MISMATCH 与 override 修复。不需要真实账号。

## 1.0.0

首个版本：飞书单平台，脚本阻塞轮询 + 单发唤醒 + 风格学习 + 服务对象档案。
