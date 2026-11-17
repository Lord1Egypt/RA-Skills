# AGENTS.md — 跨 Agent 会话同步（给 AI agent 的操作手册）

本文件夹是一个自洽工具包：把 **codex / hermes / dsh(DeepSeek Harness) / zcode / workbuddy / workbuddy-ai(WorkBuddy AI 国际版，与国内版同一 agent 双发行版) / kilo(Kilo CLI，opencode 分支) / claude code / opencode / qoder / openclaw / cursor / trae / minimax(MiniMax Code) / mimo(MiMoCode CLI) / kimi(Kimi Work) / pi(Pi Agent) / gemini(Gemini CLI) / cline(Cline)** 十九家 AI agent
的会话记录归一到 **dsh** 继续对话，并可导出 Markdown 归档（另有 **2 张占位卡**：grok(Grok Build=~/.grok/sessions JSONL 三层)/copilot(GitHub Copilot=VS Code chatSessions)——均源码核验，路径探测与手动绑定已留，待实装接 reader）。

**家谱速览（2026-09-11 台账，webui 卡片数=21=本清单全集）**：
- **实装 reader 19 个**（含 workbuddy 国内/国际双源**各自一卡**）；
  **写入目标 12 家**：dsh、codex、claude、hermes、opencode、kilo(复用 opencodewrite)、
  workbuddy、workbuddy-ai(复用 workbuddywrite)、minimax、pi、gemini、cline；
  只读 7 家：zcode(写入已废弃)、openclaw、qoder、cursor、mimo、kimi、trae(见下)
- **grok / copilot：占位未实装**（探测/绑定就位，reader 待实装）
- **trae(CN)：明确不可读写**——正文库自加密阻断，仅整库快照备份/还原；
  会话提取不存在（status 显示 0 是真实状态，webui 卡带 🔒 阻断 tag）
- 防环、幂等、人在回路三道确认策略全源通用
**zcode 只出不进**（仅读取源；写入方向已移除——双端同对话易混乱，实测亦有兼容问题）。
你（AI agent）读完本文件即可安全操作，不需要其它上下文。

## 0. 环境准备（一次性）

```bash
cd "<项目目录>"        # 注意：路径含空格，必须带引号
python --version                 # 需要 3.10+
pip install zstandard            # 唯一第三方依赖（import zstandard 不报错即已装好）
```

Node 22 仅在运行 `tools/verify-dsh-backend.cmd`（dsh 原生后端强校验）时需要：先 `nvm use 22`，
或直接调用该 .cmd（它自动优先选 nvm 的 22.x）。

## 1. 第一条命令永远是自检

```bash
python sync.py selftest
```

它在沙箱（`.selftest/`）里完整跑一遍 dsh 写入→读回→增量→校验、归档渲染、webui 只读端点，
**不碰任何真实数据**。全绿（`SELFTEST PASSED`）才继续；有 FAIL 就停下排查（见 §6），
不要带病操作真实数据。

## 2. 日常操作（cookbook）

所有写命令**默认 dry-run**：先跑一遍看计划，确认后加 `--apply`。

**dsh 侧完整闭环（顺序不能乱）**：

```bash
python sync.py to-dsh --source all --scope inc --apply --budget 550000   # ① 导入（两道确认=参数；终端交互会弹菜单）
# ② 完全退出 dsh（含后台进程），然后（挂分组 + 回填侧栏标题缓存）：
python sync.py attach-dsh --apply                                           # ② 挂分组 + 回填侧栏标题缓存
# ③ 启动 dsh → import-* 会话出现在对应分组，可 resume 续聊
```

> 只做 ① 不做 ②，会话会堆在侧栏「未分组」。以后增量导入新会话后，同样要补一次 ②。

| 任务 | 命令 |
|---|---|
| 看各 agent 源概览 | `python sync.py status` |
| 只读可视化 dashboard（给人看） | `python sync.py web`（浏览器自动开 127.0.0.1:8321，`--port` 可改；三视图：总览 9 泳道时间轴/会话列表筛选/轮次时间条下钻；行级/详情可导出——`⬇ md`（人读 Markdown）与 `⬇ ir`（C 库同构 IR JSON，拷进 ~/.session-sync 即可 push 回写）；📥=agentsync 导入（列表/详情标题黄）、🤖=子代理、🗑=回收站徽章；源卡 stat 统一「导入 X + 原生 Y」；源卡标签可点——`可导出` 弹窗勾选会话整源下载（md/jsonl，原生口径），`可写入` 弹「让 agent 代跑」提示词可复制，`⚙`/「未找到·点击绑定」弹目录绑定（粘绝对路径，后端校验结构，存 ~/.session-sync/paths.json 优先于自动探测，空=解绑）；POST 仅此一个例外端点、其余 405、仅绑 127.0.0.1、实时读源无缓存。用户想看会话全景/排查时间分布时起给他；agent 自己分析数据不需要它。install 脚本装过后任意目录可直接 `session-sync web`，快捷 `ass web`） |
| 把某条会话带进 zcode 续聊（zcode 不可写库） | `python sync.py archive --source dsh --session <id子串> --apply` 导出单会话 Markdown → 用户贴进 zcode 新会话（上下文靠文档传递；项目级用 `local/zcode-交接摘要.md` 模式） |
| 导入到 dsh（计划→落盘） | `python sync.py to-dsh --source all --scope inc` 然后 `--apply --budget 550000`（终端跑自动弹两道确认；非交互必须显式两参，缺参拒绝） |
| 反向写入 codex / claude code / hermes / opencode / kilo / workbuddy / workbuddy-ai / minimax / pi / gemini / cline | `python sync.py to-codex\|to-claude\|to-hermes\|to-opencode\|to-kilo\|to-workbuddy\|to-workbuddy-ai\|to-minimax\|to-pi\|to-gemini\|to-cline --source all --scope inc --apply`（同款两道确认+历史拦截；非 dsh 目标 all 含 dsh 源；写入器在 agentsync/{codex,claude,hermes,opencode,workbuddy,minimax,pi,gemini,cline}write.py，**workbuddy-ai 复用 workbuddywrite；kilo 复用 opencodewrite（三表同构零改动，2026-09-11 探针真库验收）**；zcode 不可写；**minimax 写入须先完全退出 MiniMax Code**）。**十一目标已实测全通**（**workbuddy 系 2026-09-11 双向实测**：导入自动折叠每会话时间戳目录防劈分区（pg 会话例外，保持原目录——**两版「任务」栏均为 is_playground 标记位视图，双向均已实证**；playground/未分区会话读取需 --include-playground；写入器按会话原始 is_playground 自动归位）） |
| 规范库（A→C→B 架构） | `python sync.py pull --source all --scope inc`（各源→~/.session-sync，只读源安全免退出）→ `python sync.py push --target dsh\|codex\|claude\|hermes\|opencode\|kilo\|workbuddy\|workbuddy-ai\|minimax\|pi\|gemini\|cline --source all --scope inc --apply`（C→目标，幂等断点续推，中途换 agent 重跑即续；与直通 to-X 共享幂等 id，混用不重复） |
| 挂工作区分组 + 标题预投影 | **退出 dsh 后** `python sync.py attach-dsh --apply`（改 workspace.json + 回填 projcache title 行，均先备份） |
| 批量改标题 | 编辑 `titles.json`（{源ID: 新标题}）→ `python sync.py to-dsh --source all --scope all --apply --force --confirm-history --titles titles.json --budget 550000` → 重启 dsh |
| 只同步某个会话 | 加 `--session <源ID子串>`（如 `--session sess_07c4`） |
| 只同步某个工作区 | 加 `--cwd frontend`（子串匹配） |
| 只要最近数据 | 确认2 用 `--scope 7d`（按最后活跃时间，推荐）；旧参数 `--since 7` 按创建时间过滤，仍可用 |
| 超长会话防超上下文 | `to-dsh` 加 `--budget 200000`（三层裁剪保续聊） |
| Markdown 归档 | `python sync.py archive --source all --apply` → `archive/` |
| 清理孤儿/测试会话 | **退出 dsh 后** `python sync.py prune --apply`（dry-run 先看；孤儿=源已删的导入，junk=纯打招呼/冒烟；移入 `~/.trash-dsh` 可恢复，manifest.jsonl 有明细） |
| 校验已导入的 dsh 会话 | `python sync.py verify` |
| 一键收尾（不想逐条跑） | 退出 dsh 后 `python sync-finish.py`（先弹两道确认→prune+导入+挂载+校验；`--sources zcode --scope 7d` 参数即确认）；`--check` 只读预览 |
| 一键体检+自修复 | `python sync.py doctor`：zstandard 缺失自动装 → selftest → 存储探测 → 增量基准损坏备份重建 → dsh 导入校验（BAD 给修复命令不代写）→ skills 桥接/全局 shim 缺坏自动补 → **opencode 存量导入审计**（清单反推法：旁路清单上线前的老写入自动补登记，防跨家重复外流）。全程不动会话数据，有警告退出码 1 |
| 会话备份/还原 | `python sync.py backup [--source all] [--scope 7d\|30d\|all] [--with-imports] [--session 子串] [--list] [--source X --ts Y --delete]`：按口径（默认原生）与日期/点名快照会话 IR 到 C 库 `backups/<源>/<时间戳>/`，不碰源数据、不推进增量水位；`restore --source <源> --ts <戳> [--target] [--apply]` 幂等写回（默认目标=源本身，只读源须 `--target`）。**读取被阻断的源（trae）自动转原始库整份快照**：加密库文件（database.db+wal/shm）不解密直接拷进 C 库，还原=原位覆盖写回。webui：各源卡片「备份」tag（口径/日期 chips+会话勾选+快照行选目标还原；阻断源弹原始库快照模式，卡片带 🔒 加密阻断 tag）；**C 库卡片「备份」tag=全源快照总览**（源徽章+磁盘路径+还原+删除，📦 行=原始库快照） |
| 矩阵回归（真库读写闭环） | `python sync.py regtest`（dry-run 看计划）→ **退出全部目标应用**后 `python sync.py regtest --apply`。每格自动选该源「最新且已稳定」会话当探针（10 分钟内仍在更新的跳过），五步验证：缺基准先预置到探针时刻-1ms → 审计探针在增量候选 → 走 to-X 同一代码路径精准写 1 条 → 复跑验幂等 → 含导入口径读回；自家→自家格验证防回环拦截。`--sources`/`--targets` 缩圈；跑完 `web` 核对各目标「导入 N」 |
| dsh 原生后端强校验 | `tools\verify-dsh-backend.cmd`（Node 22） |

**同步语义**：幂等（重复跑自动去重）；增量（源会话长了再跑 `to-dsh` 只追加新轮次；
`--scope inc` 基准存于 `~/.dsh/sessions/.agentsync-state.json`，`--apply` 成功后推进，回看 15 分钟重叠）；
**人在回路**（to-dsh / sync-finish 先确认 ①来源区 ②数据量：交互弹菜单、非交互参数即确认缺参拒绝；
**历史全量二次拦截**：`--scope all` 或 inc 首跑在 `--apply` 时需交互 y/N 或人给的 `--confirm-history`，agent 不得自行拍板全量；
**大批量第三道**：候选 >15 交互弹会话勾选清单，非交互需 `--confirm-batch` 或缩小范围——绝不一股脑写入）；
导入会话按源工作区自动落分区。落盘后可见性：dsh 需 attach + 重启。
预期留在 dsh「未分组」的：源会话无 cwd（hermes 旧库）、cwd 目录已删除、临时目录、
cwd 嵌套在已有工作区路径下（dsh 启动会清理这类嵌套记录）。
**子代理会话默认排除**：dsh 每次 agent 委派各落一个会话目录（header `origin=subagent`，
侧栏隐藏但磁盘全在）；openclaw 子代理与主会话同库混存，靠首问 `[Subagent Context]`
标记区分——reader 层默认不返回它们（对齐 zcode parent_id / codex 过滤口径），
审计全量用 `read_dsh(root, include_subagents=True)` / `read_openclaw(home,
include_subagents=True)` 或 webui 展示口径（🤖 徽章）。
**归档会话默认排除同步**：zcode / hermes / workbuddy 的 UI 归档与 dsh 的 workspace.json
软删名单（`global.archivedSessionIds`）在 reader 层默认排除——归档=用户已不要，不再外流
其他目标；webui 展示与 `prune --pick` 用 `include_archived=True` 仍可见（🗑 徽章；卡片 🗑 数、
行级标记、workspace 名单三处同口径）。
**导入会话不回流（防环）**：codex/claude/hermes/workbuddy 四家写入器铸的 sessionId 是
uuid5、原生都不是 v5——reader 层按版本位默认跳过；**opencode 例外**（桌面版原生 id 也是
uuidv5，形状判别不可用）改旁路清单 `.agentsync-imports.json`（写入器登记、读取器排除）；
dsh 默认排除 `import-*` 会话（副本在 dsh，正主在原生源，当源外流=二次成环）。审计/展示口径
`include_imports=True`（webui 已内置，导入会话带 📥 徽章）。

## 3. 安全铁律

1. **永不写入 zcode 的存储**（2026-09-01 两次实验定论：全量追加=超上下文黑屏报废；裁剪版
   新建也黑屏且模型无历史——zcode v2 靠 `session_entry`/`session_input`/`turn_usage` 等
   注册表协同渲染与装配上下文，外部写 session/message/part 进不了读取路径。要带上下文进
   zcode 用交接摘要 markdown）。`agentsync/zcodewrite.py` 仅作历史参考。
2. 读取侧永远只读（sqlite `mode=ro`）；写 dsh 只新增 `import-*` 会话目录，不动原生会话。
3. 改 dsh 的 workspace.json/projcache（attach-dsh）必须在其完全退出后进行。
3. 对用户报结果时如实说明：写了多少、跳过多少、有无裁剪、哪些步骤被阻塞待用户配合。
5. **本机个人操作一律放 `local/`（已 gitignore）**：一次性执行脚本、含真实会话 id/标题/本机路径的
   清单与产物，绝不提交、绝不放进公共目录。只有对所有用户有用且无隐私的才进正式目录。
   临时验证脚本用 `.tmp-*` 前缀（同样被忽略，用完即删）。

## 4. 文档地图

| 文件 | 内容 |
|---|---|
| `AGENTS.md` | 本文件：操作手册（你是 agent 就看这个） |
| `SKILL.md` | 同样内容的 skill 封装（装到 `~/.agents/skills/session-sync/` 后可一句话触发） |
| `README.md` | 人类视角的项目说明、验证记录 |
| `docs/FORMATS.md` | 格式总览 + 归一化 IR + 索引（先看这个再进分册） |
| `docs/pitfalls.md` | **踩坑总录**（按家分组，全部已修进代码；排障先查这里） |
| `docs/agents/dsh.md` | dsh 深度规格：多帧 zstd、事件纪律、目录编码、workspace.json 分组挂载 |
| `docs/agents/qoder.md` | Qoder 深度规格：任务索引 vscdb + conversation-history 两跳、文件名截 8 位（读取源） |
| `docs/agents/openclaw.md` | OpenClaw 深度规格：reset 快照孤儿读取、toolResult 行配对、新旧双版本兼容（读取源） |
| `docs/agents/cursor.md` | Cursor 深度规格：globalStorage cursorDiskKV（composer+bubble 键前缀关联）、@路径标题剥离（读取源） |
| `docs/agents/trae.md` | Trae 深度规格：CN 版实机核验——正文库 ModularData/ai-agent/database.db 自加密读取阻断、无 cursorDiskKV（读取源，当前 0 会话为真实状态） |
| `docs/agents/minimax.md` | MiniMax Code 深度规格：v2 runtime-state.sqlite 注册表+消息行、引导壳无消息自然滤除、写入配方（读写源；占位说明在册尾） |
| `docs/agents/pi.md` | Pi Agent 深度规格：~/.pi/agent/sessions 事件流 JSONL、thinking/toolCall/toolResult 映射、写入配方（读写源；minimax 的 pi-agent 运行时同源） |
| `docs/agents/gemini.md` | Gemini CLI 深度规格：tmp/*/chats 的 $set 快照+裸消息行、流式碎片坑、写入配方（读写源） |
| `docs/agents/grok.md` | Grok Build 深度规格（占位）：~/.grok/sessions 三层 JSONL、uuidv7、foreign-sessions 竞品模块；已装未认证 |
| `docs/agents/mimo.md` | MiMo-Code（mimo CLI）深度规格：**实机已核验**（0.1.14）——库在 `~/.local/share/mimocode/mimocode.db`（XDG 四分区字面生效）、schema 同构 opencode、`ses_` 前缀 id 防环、首跑自动导入 claude 会话须排除（读取源，read_mimo 已实装） |
| `docs/agents/kimi.md` | Kimi Work（桌面版 Kimi 的 coding agent，内部引擎仍名 Kimi Code）深度规格：**实机已核验**——daimon runtime（OpenClaw 族）内嵌引擎，数据根 `<数据盘>:\KimiData`，wire.jsonl + conversations.sqlite + 日转录三口径、`ctitle-*` 副作用会话须排除（读取源，read_kimi 已实装） |
| `docs/agents/copilot.md` | GitHub Copilot 深度规格（占位）：VS Code chatSessions 布局、探测边界与 Cline 的区分 |
| `docs/agents/cline.md` | Cline 深度规格：扩展 globalStorage tasks/<ts>/ 的 ui_messages 事件流、api 历史反解 cwd、三件 JSON 写入配方+旁路清单（读写源） |
| `docs/agents/zcode.md` | zcode 深度规格：三表结构、message/part 模板、project_id（读取源；写入器已弃用存档） |
| `docs/agents/hermes.md` | hermes 深度规格：state.db 两表、三种 role 形态、已知边界 |
| `docs/agents/codex.md` | codex 深度规格：rollout JSONL、response_item 映射、subagent 过滤 |
| `docs/agents/workbuddy.md` | WorkBuddy（国内 + 国际 workbuddy-ai 双版）深度规格：db+JSONL 双层、读取规则、跨版本迁移边界（读写源，全链路实测） |
| `docs/agents/kilo.md` | Kilo CLI（opencode 分支）深度规格：kilo.db 三表同构、read_mimo 泛化复用、opencodewrite 零改动写入、bailian provider 配方（**读写源**，第 19 家） |
| `examples/` | 示例：真实命令输出转录 + 两条完整转换实例（源→dsh 事件日志 / 源→zcode 数据行） |
| `agentsync/` | Python 源码（readers 十九家读取 / dshwrite 写入+挂载 / confirm 人工确认 / syncstate 增量基准 / model IR / archive / validate / store C 库 / webui 只读 dashboard；zcodewrite 已废弃保留） |
| `tools/` | Node 22 的 dsh 原生后端校验脚本 |
| `reference/` | 参考仓库（dsh-chat-import 等；agentctxsync 在 `本地克隆的 agentctxsync 仓库`） |
| `archive/` | Markdown 归档输出目录 |

## 5. 维护：dsh / zcode 升级后怎么确认还兼容

1. `python sync.py selftest` —— 快速回归。
2. dsh 侧分区编码全量核对（应输出 mismatches 0）：
   ```bash
   python - <<'EOF'
   import sys, glob, os; sys.path.insert(0, '.')
   from agentsync.dshwrite import project_key
   from agentsync.readers import _zstd_decode_all, _parse_jsonl
   bad = total = 0
   for path in glob.glob(os.path.expanduser('~/.dsh/sessions/*/*/session.jsonl*')):
       folder = os.path.basename(os.path.dirname(os.path.dirname(path)))
       try:
           raw = open(path, 'rb').read()
           text = _zstd_decode_all(raw).decode('utf-8', 'replace') if path.endswith('.zstd') else raw.decode('utf-8', 'replace')
           h = next(o for o in _parse_jsonl(text) if o.get('type') == 'session')
       except Exception: continue
       total += 1
       if (project_key(h['cwd']) if h.get('cwd') else '_no-cwd') != folder: bad += 1
   print(f'checked {total}, mismatches {bad}')
   EOF
   ```
3. zcode 侧 project_id 全量核对（应输出 mismatches 0）：
   ```bash
   python - <<'EOF'
   import sys, sqlite3, os; sys.path.insert(0, '.')
   from agentsync.paths import zcode_project_id
   db = os.path.expanduser('~/.zcode/cli/db/db.sqlite').replace('\\', '/')
   con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
   bad = sum(1 for d, p in con.execute('SELECT DISTINCT directory, project_id FROM session') if zcode_project_id(d) != p)
   print('mismatches:', bad)
   EOF
   ```
4. 不兼容时的适配点：`agentsync/dshwrite.py`（事件/schema/编码）。规格基线见 `docs/FORMATS.md`
   （zcode 只读，其读取器 `readers.read_zcode` 若因结构变化失败，对照 `docs/agents/zcode.md` 修）。

## 6. 故障排查

| 症状 | 原因与处理 |
|---|---|
| `ModuleNotFoundError: zstandard` | `pip install zstandard` |
| 想清理历史导入进 zcode 的会话 | **至少清两个库**：① `cli/db.sqlite`（识别：`sess_` 前缀 + 总长 41 + uuid 版本位= '5'；除 part/message/session 外还有注册表族 session_entry/session_input/turn_usage 等 15 张关联表，全清单见 `docs/agents/zcode.md` §1.1）；② `v2/tasks-index.sqlite`（删 `task_id NOT IN (SELECT id FROM session)` 的僵尸行，否则 UI 残留 + `fault.subscribe.sessionNotFound`；另有 task_group_view_node_orders 等 3 表）。磁盘关联目录（agents/artifacts/exec/bash-startup/image-cache/rollout model-io）按同名 id 连删。两库先备份（2026-08-26 已清理 246 会话 + 199 僵尸 task，备份 `*.cleanup-bak-*`） |
| to-dsh 写出后 dsh 里看不到会话 | 重启 dsh / 新开会话列表；确认会话在 `~/.dsh/sessions/<工作区>/import-*/` 下 |
| `verify-dsh-backend` 报找不到包 | dsh 安装布局变化：`set AGENTSYNC_DSH_JSONL_PKG=<dsh-session-persistence-jsonl 目录>` 再跑 |
| hermes 旧会话落在 `_no-cwd` / 主目录 | 源数据本身没有 cwd，属预期行为 |
| 路径含空格导致命令报错 | Git Bash 下始终 `cd "<项目目录>"` 带引号 |
| dsh resume 超上下文 | 重导时加 `--budget 200000`（裁剪中间轮次保锚点+尾部） |
| 点开导入会话报 `SessionFormatUnsupportedError: ... session/imported ... not marked ignorable` | 旧版导入缺顶层 `ignorable:true` 标记：`python sync.py to-dsh --apply --force [--budget 550000]` 整体重写后重启 dsh（校验器已内置该规则，`verify` 不通过即未修复） |
| 导入会话标题显示成工作区名/全在「未分组」 | 两种原因：① 日志被判不可解析（ignorable 缺失）→ `to-dsh --force` 重写；② projcache 无 title 行（点开才有标题）→ 退出 dsh 后 `attach-dsh --apply` 回填 |
| 重写后仍在「未分组」 | 会话没挂进 workspace.json 的工作区记录：退出 dsh → `python sync.py attach-dsh --apply` → 重启。无 cwd 的源会话（hermes 旧库）按原生语义留在未分组 |
| attach 报「检测到 dsh 正在运行」 | 完全退出 dsh（含后台 node 进程）后重试；dsh 退出时会把内存中的 workspace 状态写回磁盘，运行中改必被覆盖 |
| dsh UI 归档数与 webui/实际对不上 | 历史删除会留死归档 id（`workspace.json` 的 `archivedSessionIds` 指向已删目录）。核实：名单 ∩ 磁盘目录；清死 id 需完全退出 dsh 后改（先备份）——2026-09-01 清 30 条 |
| dsh 启动报 `stored record … does not match its schema`（createdAt/updatedAt） | workspace.json 有记录缺 `createdAt/updatedAt`（ISO 字符串）——用 `storages/workspace.json.agentsync-bak-*` 恢复，或给缺字段记录补上两键；新代码已不会再产生这种记录 |
| attach 后个别会话仍在未分组 | 看 attach 输出的跳过原因：无 cwd / 目录已删 / 临时目录 / 嵌套在已有工作区路径下（dsh 会清理嵌套记录，工具保持一致不建） |
