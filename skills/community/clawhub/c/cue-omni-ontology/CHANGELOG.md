# Changelog

### 0.3.18 — 2026-11-03（本格仅刷新在架新鲜度、无能力变更、无接口变更）

### 0.3.17 — 2026-11-02（本格仅刷新在架时间戳与收录新鲜度，无能力变更、无接口变更）

### 0.3.16 — 2026-10-29（指路补齐解析腿那一页：两枚说明面把「怎么连」与「不连会少什么」都写了，缺的只是官方配置页入口；本包只把解析腿列为对外取证腿，所以不给数据腿页，非能力面变更）
- 改因：两枚说明面早就写着这条腿的用法与判据——中文说明面第 45 行「真实解析复用官方 cue-omni-reader……按其 setup 连接 MCP 并配置凭据」、第 47 行把已连判据按路分写并写明不连的代价（页锚与逐字定位缺位、来源记录只能到文件级），英文说明面同两处同形。但对官方配置页的引用改前只在两枚技能面在场，两枚说明面各 0 枚：面名册现读 README.md 0∥0、README.en.md 0∥0，尺当场打「⚠ 面不齐：README.en.md/README.md 指路 0 枚」——读者知道差哪一层却不知道去哪补。
- 改法（只补指路、原句一字未动；腿的取舍由面文定，不硬塞没写过的腿）：两枚说明面在「配置凭据」那句之后各接一句解析腿官方配置页指针 https://cuecue.cn/hub/omni-reader，并把「不连会少什么」指回本面下面那一段的原话、不复写。**不给数据腿那一页**：本件面文从没把结构化披露或横向深研列为取证腿，替它补一页就是造一条没写过的腿——依据写到这里为止。另有一格撤换（随本票做完、版号不再前进）：这两枚说明面初稿带着一句自指计数句，宣称全包扫某两枚工具名的枚数为零，而那句话自己就在被扫的面里，写下即让它为假，还把内部审计动作放进成品面；现在撤成依据句，成品面不再出现那种「现扫 N 枚」的形制。
- 现测（先证靶在场，再改，再复跑）：改前那一拍跑在版本库取回的只读副本上（面名册逐枚 0∥0、那条「面不齐」报警全句在场）→ 改后四面各 0∥1、包级 解析腿页 4 枚，「面不齐」报警句不在场；行长度 中文说明面第 45 行 310→460 字符、英文说明面第 45 行 538→1024 字符（页 URL 整串 https://cuecue.cn/hub/omni-reader 现读起列 333∥615；本票撤句前该两行各为 503∥1086，撤句后重读一次，长度以本条为准）。撤句后对两枚说明面逐式各扫那两枚工具名＝0 枚，全包 .md 非留痕位命中 0 行；旧病灶形复扫改前改后都 面 0∥行 0∥次 0；本条顶条区自扫 面 0∥行 0∥次 0。仓内各闸与出包读数以各闸自报行为准，本条不复写。
- 本票射程：指路只补两枚说明面（中文说明面、英文说明面）——两枚技能面本来就有解析腿那一页，本票未动；随包 references 十枚不落。
- 未动：知识契约与判定规则、包内工具脚本与离线测试、页锚与哈希口径、首屏文案、两枚说明面各自那行安装式（现扫各 1 枚，本票未改）。故本票不触发重验旧靶。
- 号序与槽位：0.3.15 → 0.3.16（指路补齐＝patch，非能力面变更）。本包版本位三处——两枚技能面的版本位加随包件内的版本位（那行注释本来就写着升号必须同改这两处）；现扫三枚同值，旧串全包残留 0 枚（留痕位除外）。

### 0.3.15 — 2026-10-29（按路分写解析可用的验收判据：四面那句把 URL 路与 Bridge 路压成同一条验收动作，remote-only 那面照它做不成；非能力面变更）
- 改因：与同批 omni2docx 那一枚同源（6.1 第十批 Major 10-C，结论「不签 LGTM；blocker 0／major 2／minor 0」，判定窗 HEAD `fa6d62abb01972b15bf03eb599030dd23d943444`）。产品仓边界句同法逐字复跑、带列号不截断：`cue-skills/cue-omni-reader/README.md:13`（行长 409）列 386 与 `cue-omni-reader/SKILL.md:21`（行长 244）列 209 都明写 remote-only **cannot read local files**；`README.md:17`∥`SKILL.md:76` 列 1 起写明 remote-only 恰好三枚 `parse`／`get_parse_status`／`cancel_parse`。⇒ 本包四面在列完两路名集之后，又把「一次真实本地文件 parse」写成端到端可用的共同必要条件——上一票修好了名集那半，这半仍合着一条尺。
- 改法（中英同射程）：那半句换成按路分写，串与同批 omni2docx 逐字相同、逐字取 Lead 点形（本票票面「点形＝你的 §四 a」），一字未改，英文只随句位首字母大写。落点与改后读数（面∥行∥改后行长∥新式串「真实 URL ∥ real URL parse」起列）：SKILL.md:43∥824∥645；SKILL.en.md:29∥1738∥1316；README.md:47∥512∥407；README.en.md:47∥1172∥928。
- 复验（与同批那条共用的尺，两把都跑）：票面判据①那条旧式串（`真实本地文件.{0,24}parse` ∥ `real local-file parse`）改后本包仍命中 4 行——按路分写必须写「本地文件那一腿…真实本地文件跑一次 parse」，这条尺照字面过不了，如实报数不自改判据。分辨力在缺陷式 `端到端[^。]{0,40}真实本地文件|end-to-end[^.]{0,60}real local-file parse`：本包改前（HEAD）4 行 → 改后 0 行；新式尺 `URL 那一腿要拿一枚真实 URL 跑一次 parse|the URL route is verified by one real URL parse`：改前 0 行 → 改后 4 行。两包合计 9 → 0 与 0 → 9（另一包读数写在它自己的顶条里）。
- 未动：六段流程、判定与 schema、两支自测（`scripts/test_ontology.py`∥`scripts/test_numeric.py`）、产物形制、README 两面「装本件自己」的安装式（README.md:42／README.en.md:42）、上一票新增的三态分写与按路名集、以及那句「两文口径一致」——都不改窄也不删除。判定与 schema 一字未动，故本票不触发重验旧靶。
- 号序与槽位：0.3.14 → 0.3.15（对外承诺句射程修正＝patch，非能力面变更）。本包三枚版本字面同批推进（`SKILL.md:13`／`SKILL.en.md:5`／`scripts/ontology.py:27` 的 `VERSION`，那行注释原文「升号必须同改这两处（包内产物与自报行都取这一枚）」）；`grep -rn '^version:' cue-omni-ontology | grep -v fixtures/` 现读 2 枚，加脚本常量共 3 枚，合成靶不在本包。

### 0.3.14 — 2026-10-29（对外承诺句射程修正：入口与判据那几句把「装好 skill／已配凭据／通道已连」压成一件；非能力面变更）
- 改因：第九批复查对外承诺句后落的一枚 major（改的是面文射程，不改判定），与同批 omni2docx 那一枚同源。本包面文原来写「装完再列一次工具，返回里认得到 parse／get_parse_status／read_result 这几枚才算已连」——①它把三种独立状态压成一句「已连」，装 skill 只证文件到位，不产生连接；②名集按产品仓 `cue-omni-reader/SKILL.md:76` 原文是两路两数：remote-only 恰好 `parse`／`get_parse_status`／`cancel_parse` 三枚，Bridge 再加 `read_result`／`read_outline`／`discard_result`／`save_result` 共七枚，我们那三枚的凑法既不等于 remote-only 全集（缺 cancel_parse）也不等于 Bridge 全集；③`cue-omni-reader/README.md:66` 明写只有跑一次真实本地文件 parse 才证数据路端到端可用，工具在场不证它。产品仓 `README.md:66` 另写明 URL 那腿无需本机安装、本地文件那腿需 audited Bridge 与最小根授权，`SKILL.md:22` 补 doctor 与宿主 reload/reconnect——本票三处逐字在盘上复跑过（只读）。
- 落点：4 枚面、6 处行（行号现读 SKILL.md 43／45，SKILL.en.md 29／31，README.md 47，README.en.md 47）。其中 README 两面那两条是上一票没在射程内的同族句，本票按 token 复扫补上，只改新段会在同包留下互斥承诺。
- 改法（中英同射程）：①三态分写——装好 skill ≠ 已配凭据 ≠ 通道已连，句形取同族母本 `journal-draft/README.md:153`（那枚面在冻结名单内，本票一字未动，只引句形）；②已连判据按路分写、方向从「在场才算连上」改成「连上之后应能在宿主列出的工具里看到这些名字」，3 枚与 7 枚并列，不再用固定数判两路；③端到端降成一句实话——名字在场只证被暴露，端到端要真实本地文件 parse 一次，本包不自证也不代跑；④「不装不报错」加前提限定（不调用解析腿、且已有可贴的文本或文件与 Python 3.10+），并把零凭据演示定位成证本包工具链、不证通道。
- 指路（新增，可数）：两面 SKILL 的入口段加解析腿官方配置页 `https://cuecue.cn/hub/omni-reader` 与凭据页 `https://cuecue.cn/hub/api-key`（盘上出处同批记在 omni2docx 那条里）；本包只依赖解析腿，`hub/mcp` 保持 0 枚、不塞。
- 未动：六段流程、判定与 schema、两支自测、产物形制、README 里「装本件自己」的安装式（README.md:42／README.en.md:42）一字未改；那句「两文口径一致」没改窄也没放宽——两面各自补齐同一射程的段，它是随改动成真。
- 号序与槽位：0.3.13 → 0.3.14（对外承诺句射程修正＝patch，非能力面变更）。本包三枚版本字面同批推进（SKILL.md:13／SKILL.en.md:5／scripts/ontology.py 的 VERSION，那行注释自写「升号必须同改这两处」），改后三处同读 0.3.14、旧值在非 CHANGELOG 面残留 0 枚。

### 0.3.13 — 2026-10-28（英文面补上对应入口段：那句「两文口径一致」就地成真，没有把承诺改小）
- 改因：上一票给中文 SKILL 面补了入口段，英文面没有对应物——它只有 `## First useful result`（零凭据演示那一节），段内不含已连判据、也不含带代价的降级句。两种数法当场分得开：按收窄式（first use 后不接 ful、where to connect、enable the channel、CUE_API_KEY、npx skills add、sign up）现读中文面真入口 1 枚∥英文面 0 枚；把串放宽成「First use」就会把 `First useful result` 误读成入口段——那是上一拍票面读数出错的地方，本条按收窄式记值。裁语是补英文面对应段，不改窄也不放宽 `SKILL.md` 第 27 行那句「两文口径一致」：承诺成真比把承诺改小对读者更负责。
- 改法：`SKILL.en.md` 在 `## First useful result` 之前加一段 `## First use: connect the parsing channel`，两行与中文面同射程——Where to connect（真解析用宿主里那枚官方 cue-omni-reader MCP，本包不代装也不代连；装完在宿主里再列一次工具，走 JSON-RPC 的 tools/list 握手，那份返回里认得到 parse／get_parse_status／read_result 才算连上；凭据留在你自己的凭据设施，本包脚本不读 CUE_API_KEY、不在聊天里索取 key，只在回读 artifact 分片时按 CUE_OMNI_BRIDGE 起那枚桥，key 归通道自己的环境）；No install, no error（装了却列不到那几枚名字就是没连上，本件随即只接你贴进来的文本，**what you lose is page anchors, verbatim locators, and source records above file level**；解析消耗以服务端返回为准，本件不代估也不代付；没连上不等于不能用，但下一节那条零凭据演示是另一条路径——虚构材料、不联网、不调解析 API，别把它的产出读成通道已连）。
- 取词与现值：句子从本包 README.en.md 第 47 行那枚现有句（Connectivity test 那段）与脚本现值取，不翻译中文面句形、不新造承诺。脚本现值同上一票复扫：scripts 内 CUE_API_KEY 字面 0 处、真网络调用 0 处、只读 CUE_OMNI_BRIDGE 一枚（`omni_source.py:45`，类注释原话写着本模块从不读取、打印或转手 key）。新段里没有价格承诺，也没有未开放域与第三方同类实践点名。
- 三面一字未动（边界写着重复即红）：中文 SKILL 面除本批那一枚版本字面外零改动；README.md／README.en.md 的入口段仍各 1 枚、两面一字未增未减。
- 号序与槽位：0.3.12 → 0.3.13（补英文面对应段＝patch；判定、schema、产物形制与两支自测脚本一字未动，故本票不触发「加/改判据必重验旧靶」）。三枚版本字面同批推进（SKILL.md、SKILL.en.md、scripts/ontology.py 的 VERSION），改后同读 0.3.13。
- 现测（读数在各尺自报行；出包字节数与 sha 按 K-66 在所有写盘与执行都结束之后再取，记在回执——写进本条它自己就会变，故此处不复数）：首屏尺 rc=0 且丙降级无代价行=0、安装式对表 rc=0、lint --strict rc=0、卫生闸 rc=0 且成品面 ERROR 与基线同值、两支包内自测各 rc=0、出包与发布物闸各 rc=0，且从 zip 内读回英文面新段在场、三枚版本字面同值。

### 0.3.12 — 2026-10-28（SKILL 面补一段入口：连通道那两行此前只在 README 两面有，而技能加载只读 SKILL 这一面）
- 改因：入口串（首次使用／去哪连／已连判据／不装不报错）此前在本包是 SKILL.md 0 枚、README.md 1 枚、README.en.md 1 枚。README 那两行写得再对，agent 加载技能时读的是 SKILL.md 这一面——缺的就是第三面上那一步：往哪儿连、怎么算连上、没连上掉哪一层。与本包 0.3.11 那拍（把已连判据从首屏绕开句改成正文真形）同源，只是这次缺的面不是行。
- 改法：SKILL.md 在「先交付一个有用结果」之前加一段「## 首次使用：连上解析通道」，两行——一行去哪连（解析这一腿复用官方 cue-omni-reader 的 MCP，本包不自动安装也不代连；装完在宿主里再列一次工具，走 MCP 的 tools/list 握手，那份返回里认得到 parse／get_parse_status／read_result 这几枚才算已连；凭据由用户在自己的凭据设施里配置，本包脚本不读 key、不在聊天里索取 key，只在回读 artifact 分片时按 CUE_OMNI_BRIDGE 起那枚桥，key 归通道自己的环境），一行不装不报错并**把缺的那一层写进同一句**（列不到那几枚名字就是没连上，本件随即只走「你把文本贴进来」那条路，缺的是页锚与逐字定位那一层，来源记录只能到文件级）。取词全部来自本包 README 已有的那枚入口句与脚本现值，不新造承诺：本包不自动安装或配置 Omni、解析消耗以服务端返回为准、本件不代估也不代付（无价格承诺，唯一相关的一串在否定位）；并明确写开「没连上」与「下一节那条零凭据演示」是两条路径，别把演示产出当成已连通道的读数。
- README 两面没补第二遍（票面边界：重复即红），本票三面入口枚数现读＝SKILL.md 1 枚、README.md 1 枚、README.en.md 1 枚。
- 号序与槽位：0.3.11 → 0.3.12（补入口段＝patch；判定、schema、产物形制与脚本判据一字未动）。版本位所在三枚字面同批改（SKILL.md／SKILL.en.md／scripts/ontology.py 的 VERSION 常量）——这是本包既有形制（ontology.py 那行的注释自己写着「升号必须同改这两处」），也是与本票「只动 SKILL 面文」边界的一处必要偏离，理由与读数一并报出；SKILL.en.md 只改那一枚版本字面，其面文没有新增段落，所以英文面的入口仍是你早先看到的那一枚，本票没在英文面补第二遍。

- 现测（零凭据那两条路各自真跑）：`python3 -B scripts/ontology.py demo --out <一枚不存在的全新目录>` 退码 0、产物 16 枚（含 brief/brief.html 与 brief/brief.md 两枚在场）、自报 synthetic=True 且 api_calls=0；同一条命令在 `socket.connect`／`create_connection` 换成遇调即抛并记次的拦尺下跑，出网尝试计数 0——面文那句「演示不联网、不调解析 API」与实现同形。反手一格也实测到了：`--out` 交一枚**已存在**的目录时本件退码 2（要全新工作目录），所以那行命令原文照 README 的写法留给用户自己填新路径，我没在 SKILL 面把它写成可直接复跑的固定路径。包内两支自测 `scripts/test_ontology.py`、`scripts/test_numeric.py` 各 rc=0（带 PYTHONDONTWRITEBYTECODE 跑，没给包新增字节码）；仓级 lint --strict、卫生闸、首屏尺（名册=24 不合=0、丙降级无代价行=0）、安装式对表（形制点名 0 处）、场景图、形状尺、出包与发布物闸各 rc=0，数取各尺自报行。
- 我没动也没自扩的一格（只报不改，处置由裁语定）：`SKILL.md` 第 27 行那句「本文件即主入口（中文主）；英文对应版见 `SKILL.en.md`，两文口径一致」在本票之前就是这样，而英文面没有这一段的对应物（边界写着只动本包 SKILL.md＋顶条，README 与英文面都不在这一票的射程里）。现读逐面列清：中文 SKILL 面新段 1 枚（行号 41）；英文 SKILL 面只有 `## First useful result`（第 27 行，对应中文面「先交付一个有用结果」那节，内容是把零凭据演示交给用户，不含 tools/list 已连判据、也不含带代价的降级句——按串扫它会命中「First use」，那是标题巧合，别把它读成本段的对应物）；README 两面各 1 枚（`## 第一次试用：无需 API key`／`## First try: no API key`）。所以那句「两文口径一致」比这个现值宽一格。要么下一票把英文面对应段补上（同号槽同批），要么把那句收成实现射程内的说法；两种都不该由我在这一票里顺手做掉。

### 0.3.11 — 2026-10-22（解析腿的已连判据进正文：走宿主 MCP 的 tools/list 握手，本面不假装有一条 curl）
- 改因：首屏那一眼给用户的是「可以不开通通道」的绕开理由，而真正跑得起来的通道正路命令不在这面上；正文另有绕开句只说「不装不报错」，没在同一句里写清缺的是什么。
- 改法：依赖那一节补上这条腿的已连判据：宿主列工具走的是 MCP 的 tools/list 握手，那份返回里认得到 parse／get_parse_status／read_result（转换件另带 read_outline）才算已连；列不到名字就是没连，本件走哪条降级路、缺的是哪一层都写在同句里。这几枚的解析腿不在这张目录里，没有 curl 可以替代它，本面不假装有一条。
- 射程（现数，不按记忆）：成品面改动 2 枚（口径＝本包被改面逐枚现列：README.md／README.en.md）；版本位所在文件 3 枚（口径＝含旧号的非 CHANGELOG 件逐枚现扫，落笔后残留 0；锁位 SKILL.en.md 与 scripts/ontology.py 里那枚版本锁——后者初版漏了，是复扫逮出来的，就地补一行「与 SKILL.md 成对」的标注）；闸与夹具一字未动，scripts/ontology.py 只改那枚版本锁那一行、判定逻辑一字未动。
- 现测：首屏探针末行「名册=18 不合=0｜甲命中行=0 乙缺枚数=0 丙降级无代价行=0」，本枚不在不合名册内；lint --strict rc=0、末行「summary: 18 skill(s), 0 error(s), 0 warning(s)」；卫生闸 rc=0、末行「summary: 面 180，ERROR 0，WARN 233」；面尺从仓外那一层跑 rc=0、末行「面数=23 不合=0」。
- 未动：SKILL.md 的判定与契约段、inputs／produces／consumes 那批声明键、两面 README 的其余段落、闸与夹具、CHANGELOG 历史条目（不回改）。
- 号序：0.3.10 → 0.3.11（成品面指路与代价句更正＝patch）。

### 0.3.10 — 2026-10-21（新建 metadata.openclaw 一层并声明运行前置 bins）
- 改因：本面此前没有 metadata 这一层（现读：改前该文件 frontmatter 内无 metadata 键），而渠道抽取器认的运行前置层是 metadata.openclaw（别名两支亦可）——所以这一层在盘上原本不存在，不是挂错了层。本包也不引用那枚可选凭据（现读 0 枚件、0 次），故只声明前置、不补凭据项：硬编一条就是假阳。
- 改法：新建 metadata.openclaw 一层，其下 requires 声明 bins 为 python3（依据＝面内命令块以 python3 起，现读 SKILL.md 那段）；env 与 primaryEnv 两支都不写；面内 inputs／produces／legs 那批场景图声明键与两面 README 未碰。叙事勘正：本条首写把这一改动讲成了对既有声明的搬迁，与同条后一半自相矛盾——真实动作是新建，按实况改写；事实与读数不变，版本位不因此再进一枚（当前条勘正，历史条目不回改）。
- 射程（现数，不按记忆）：声明层改动＝SKILL.md 一枚（本面）；版本位所在文件 3 枚＝SKILL.en.md、SKILL.md、scripts/ontology.py（本包若有多处锁，枚数由这一行现读给出，不手抄）；其余件零改动（本件按「含旧号的非 CHANGELOG 件」逐枚现扫，落笔后残留 0）。
- 现测：渠道面件尺（只读、零网络）对本枚判 ok，全仓末行「名册=18 不合=0 计划位=有」退码 0；卫生闸末行「summary: 面 180，ERROR 0，WARN 233」；面尺末行「面数=23 不合=0」；本包入口自测退码 0、末行「OK」；场景图读数与本批开工时逐字节同＝是。
- 未动：面文其余段落、闸与夹具、包内代码判定、CHANGELOG 历史条目（不回改）。
- 号序：0.3.9 → 0.3.10（面件结构变更＝patch）。新条目反引号 0 枚、美元号 0 枚（本条现读：含反引号的行 0 行／出现次数 0 次）。

### 0.3.9 — 2026-10-19（补一条 bool 坏形：数值字段喂 True 必须仍被拒，且这条能抓到排除式被摘）

- 病灶：对外承诺说数值字段须为有限数，实现里那条排除 bool 的式子（`_num` 中的 `not isinstance(x, bool)`）没有任何用例守着——把它摘掉，测试套件照跑照绿（现测：HEAD 那版加摘掉排除式 → Ran 8 tests／OK，退码 0）。承诺失去实证，属覆盖面缺口不是判定错。
- 改法：在既有的那组坏形表里加一条——把数值字段换成 `True`，断言仍发 Invalid 且报文点名「value must be a finite number」。判定阈值与码集一字未动，只补用例。
- 反证成对（靶本＝整包副本，仓内件零改动）：①加完这条后跑套件 → Ran 8 tests／OK，退码 0，双跑剥耗时后逐字节同；②在同一副本里摘掉 `_num` 的排除式（生效自证：该串在场枚数 1→0）再跑 → 退码 1，FAIL 行点名 subTest「[value must be a finite number]」，FAILED (failures=1)。这条不是装饰：排除式没被执行到就红。
- 版本位：0.3.8 → 0.3.9（覆盖面补强＝patch，判定不变）。三枚字面同步（SKILL.md、SKILL.en.md、scripts/ontology.py 的版本常量各一枚——本包有一道一致性锁把三者钉在一起，漏一枚入口就红），旧值非 CHANGELOG 面残留 0；新条目无美元号（本文件现读 0 行 0 次）；反引号仅作 markdown 排版、不是病灶串，本顶条现读出现次数 8 次、含反引号的行 3 行（病灶句、改法句、反证句各占一行）。

### 0.3.8 — 2026-10-19（音视频回测那套腿档字母就地定义，与来源可信级分开）

- 改的一处：references/av-backtest.md 的 Layers of evidence 节顶部补一行定义——L1–L4 是回测腿档（URL 侧整片可读性／本地整档字节一致／本地有界片段进链／在 L3 产物上跑完整链），本文件是本仓这套字母的唯一定义处，别包不引用它；同时写明它与本仓别处用作来源可信级的 L1/L2/L3 无关（那三级指来源，不是腿档）。
- 为什么只在这一处加：清点显示本包其余面对这套字母命中 0，脚本代码命中 0 枚——不存在需要同步的第二面，也不涉及机检字面。
- 未动：判定逻辑、各道闸与阈值、夹具与样例、README 双语与 SKILL 双语的其余句子；本票不加判据也不放宽判据（新增 0／放宽 0）。
- 版本位：0.3.7 → 0.3.8（术语定义补齐＝patch）。三枚字面同步（SKILL.md、SKILL.en.md、ontology.py 的版本常量各一枚），常量之外的代码一字未改；旧值非 CHANGELOG 面残留 0；新条目无反引号、美元号与流水号。
### 0.3.7 — 2026-10-14（码内版本常量与面版本位同步）

- 同步三枚锁位：`SKILL.md` 与 `SKILL.en.md` 的 version 0.3.6→0.3.7，`scripts/ontology.py` 的 `VERSION` 0.3.5→0.3.7。此前码内常量落后一版，包内自带的「版本单源」断言（`test_ontology.py` 逐面把 `VERSION` 与两份 frontmatter 的 version 对拍）因此判红——那是断言在报真事，不是断言写错。
- 面内其余文字零改动；判定逻辑、阈值与退出码未动，旧值在非 CHANGELOG 面残留 0 枚。
- 复验（取脚本自报行）：`python3 -B -m unittest discover -s scripts -p 'test_*.py'` 在仓内与解包件两态均退码 0，自报「Ran 74 tests」＋「OK」；成品面逐面现跑全「PASS 五禁零命中、指路可跟随」。
- 版本位：0.3.6 → 0.3.7（常量同步＝patch，无能力增减）。历史条目不回改。

### 0.3.6 — 2026-10-13（全仓文档卫生一轮：读者称谓统一「用户」＋中文标点全角化）

- **读者称谓口径**：成品面指称交付物接收方一律「用户」——原「给人读的镜像／可交人核／人来确认／拍板在人／决议权在人／人负终审／人只抽读」等口语表述全部改「用户」；「人工复核／人工审定／人工审」等与「机器」对举的标准词保留不动。
- **中文标点全角化**：半角逗号／分号／冒号／问号／感叹号／括号在邻接中文处统一为全角；代码围栏、行内代码、URL、时间戳、千分位数字、YAML `tags` 数组分隔符一律不碰；中文引述的直引号改「」。
- 能力句、机检词族、判定阈值、退出码、脚本零改动；复验 `python scripts/check_skills.py` 0 error 0 warning，公开面卫生门 ERROR 清零（另修 journal-draft 一处既存过程日期入墙）。
### 0.3.5 — 2026-10-10（公开面卫生：证据文件的过程流水与仓外运行目录指路退出成品面）

- 五处子串改净：`SKILL.md` 一处内部时点叙事（「某日实测的四点（Bridge 1.8.3–1.8.6）」）改为「实测稳定的四点（Bridge 版本以通道现值为准）」；`references/av-backtest.md` 四处——文件题头的内部流水号与定稿日、层级表头的仓外运行目录通配路径、正文一处流水号括注、末行的转录/输出/导出路径指路，统一改为「记在内部运行台账，可应要求提供」形制。
- 判据与阈值零改动：本体结构、sha 复核、grounding 页锚形制、`validate`/`query`/`export-okf` 出口一字未动；本次动的是证据说明文件的指路方式。
- 面与版本锁：`SKILL.md`／`SKILL.en.md`／`scripts/ontology.py` 的 VERSION 三处同锁 0.3.4→0.3.5（锁在本包是硬约束，漏一处即 lint 报）。
- 复验（取脚本自报行）：全仓公开面卫生机检对本包全部成品面逐面现跑，全「PASS 五禁零命中、指路可跟随」；清理前命中为 SKILL 1＋av-backtest 4＝5 条；件内测试面 74 passed 加 19 subtests passed；`check_skills.py --strict` 自报 15 skill(s), 0 error(s), 0 warning(s)。历史 CHANGELOG 条目不回改（该文件 WARN 计数清理前后同为 15＝新条目零新增命中）。
- 名述面三枚现测：见交付回执（脚本实测，非手数；本包双语两份 frontmatter 同步，version 行外零改动）。

### 0.3.4 — 2026-10-09（M177 阶段二·汲取形制包渠道面四项：②反幻觉两句（时点句+未检索到句））

- 落面：本件落了 ②反幻觉两句（时点句+未检索到句）。②的两句各归其位——**时点句进「怎么开口」节**（开口带时点、首行标「来源日期」、与所指日期不一致即禁「今日」「最新」改「截至 <日期>」），**未检索到句进「出错了怎么办」节**（参数／字段／枚举名未见于本次工具返回者不得凭印象填）；同一对句子在场景件 SKILL 输出契约节以指令面复写一次（agent 侧受约束，人侧知情，两处非重复）。README 与 README.en 双语对点。
- 版本位：patch 位 0.3.4。除版本锁字面外 `scripts/` 零触碰；判定与阈值一律指回脚本现值，本文不作穷尽复述。

本文件遵循 keep-a-changelog；版本权威=各 SKILL.md frontmatter 现值。

### 0.3.3 — 2026-10-08（文案面·M174 名述带界句：「含音视频」只在「本地小段/切片≤256 MiB」限定下说）

- 缘起与口径源：M173 音视频端到端回测已在 `references/av-backtest.md` 定形（含 lead 跨会话复现段，其入链笔为 49dc951）。该档 What this decides 段的判词是本次唯一口径源——**「含音视频」supportable only with the qualification「本地小段/切片(≤256 MiB)工作流」**，实测强度为「两场合共三枚 90 秒切片走通全链、逐字回查 8/8，全长视频 URL 路五枪全拒、本地全长受 256 MiB 闸」，全长会议解析=未臻。述面据此**只加带界句**，不写把能力说成无界的词形；本条自身也不复写那两个被禁词形——复写了，「无界说法零出现」这条判据就被自家日志破掉（同型今日已犯两次，不再第三次）。
- 落了哪四处：① `SKILL.md` 与 `SKILL.en.md` 的 `summary` 末追加「音视频限本地小段/切片」（**字节数容不下**：加 ≤256 MiB 即破 C-36 的 80 字闸，故数字界只出现在 ②③④ 三处）；② `description` 的「适合：」清单追加「业绩会音视频（本地小段/切片≤256 MiB）」；③ README 中文主面在「先看实际价值」表加一行、在「边界与许可」加一句（含「完整性≠语义为真」的限定）；④ README.en.md 同两处对点。displayName 未动（品类钩子已占位，音视频属能力细节进述面）。
- 版本锁与实测数字：`SKILL.md` / `SKILL.en.md` frontmatter 与 `scripts/ontology.py` 的 `VERSION` 三处同号 0.3.3（M158 双锁的第三处在脚本里，动它只为对账，判定逻辑零改动）；改后两套自测 **Ran 66 tests / OK** 与 **Ran 8 tests / OK**，全仓 lint 10 skills / 0 error / 0 warning。限额实测：summary 79/80、description 286/300。
### 0.3.2 — 2026-10-08（M173：音视频端到端实跑证据票，C-13 先证据后申报）

- 新增 `references/av-backtest.md`：公开业绩会音视频端到端诚实段。**样本 N=2**（当升材料 2025H1 网上业绩说明会回放、建行 2025 年度业绩发布会视频——两枚均为本机 ffprobe 核过的真 h264+**aac 音轨**，非幻灯片视频，源可达 HTTP 200/206）。
- 分层账（全文见 `references/av-backtest.md`）:L1 全长 URL 腿 5 枪（lead text×3+我 grounded×2，两 CDN）全 **PARSE_FAILED**（retryable=false、operation_created=true、**billed=false**，泛词零归因）;L2 本地全长（1.34GB 字节严合）**SOURCE_TOO_LARGE**=256MiB source 闸（operation_created=false、billed=false，界外清晰非玄学）;L3 本地 90s 切片两枚（3.2MB/6.3MB,ffmpeg 归一化 faststart）**grounded completed**——返回形制=内联 `[画面/说话人 mm:ss]` 锚+`(幻灯片标题)` 标记+`grounding.data` sidecar(`omni.grounding.v1`);L4 全链走通：`omni-source --text-only`→prepare（逐字 quote→字节 span）→build v1（4 幻灯断言）→update v2（+1 口播断言第二源，同 scope title 增量）→validate→独立逐字回查 **5/5**→query found+证据→export-okf 5 概念文件；run.json.skill_version=**0.3.2**（M158 锁在 AV 产物上自证）。口播 ASR 谐音（「利用」=净息差）原样入包不校，basis 注明。
- **实测强度（只准写这个）**:「2 场公开业绩会视频（建行 H1、当升 2025H1）共三枚 90s 切片走通全链（build→update×2→validate→query→export-okf；包=3 源 8 断言）、逐字回查 8/8(100%)；全长视频 URL 路 5 枪全拒、本地全长撞 256MiB 闸=未臻」。「含音视频」如加入 displayName/summary **必须带界**（「本地小段/切片 ≤256MiB 工作流」），不得写「任意/整场音视频」；终判归 lead/Owner，名述面属 4.1。
- 本条为 M173 机器面账；版本 bump 由 lead 合并发，三处同号=SKILL.md+SKILL.en.md frontmatter+ontology.py VERSION（M158 锁，非 manifest——本包无 manifest）。EN 面 displayName 本就与主面同刻中文（M157 渠道一致性设计）,「任意文档」口径两文一致，无需另改。

### 0.3.1 — 2026-10-07

Changed
- 渠道命名升级（Owner 定名候择其一，本版取「任意文档·建逐句可回查知识库」）：displayName 去「公开资料业务」抽象词，钩子换成品类不限（公告只是例一）+逐句可回查（包内实证：页码锚/verify）。「音视频/多模态」字样**本版不写**——omni 工具面支持音视频为真，但本件知识包管线端到端实跑证据只有文档/网页（实跑票 M173 在途，凭据落账后另版解禁申报）。

### 0.3.0 — 2026-10-07（回测修正合入 + Omni 结果转页码 + 留出集回测记录）

- **版本号说明**：回测期间在仓外开发了五个未发布版本，内部编号 0.2.4–0.2.8，与本仓已发布的 0.2.4（2026-10-04 文档版）撞号。为避免混淆，这批改动合并为 0.3.0 发布；代码注释和测试里写作 dev-0.2.x。schema 仍为 0.1.0，旧知识包照常可读。
- **引文匹配**（dev-0.2.4）：`prepare` 精确匹配失败时，忽略表格 `|`、空白和 Markdown `#`/`*` 再定位一次；EvidenceSpan 仍指向原文逐字节片段，返回 `quote_normalized_matches`。仍有歧义就失败，不做语义模糊匹配。
- **catalog 与严格查询**（dev-0.2.4）：新增 `catalog PACKAGE [--kind all|entities|definitions|changes]`；`query` 支持 `--args-json`，未知字段名报错，不再静默忽略。
- **冲突明细**（dev-0.2.4–0.2.6）：`changes.json` 冲突带 `old_value` / `new_value` / `period` / `severity` / `kind`。只有互不相同的值分别来自不同来源才算 `cross_period`，同一报告内并列的多值标 `intra_report`；按 high→medium→low 排序。每个冲突带 `old_evidence` / `new_evidence`，每个新事实带 `new_fact_details`，都是从来源字节切出的逐字摘录（≤160 字）。
- **信用风险固定章节集**（dev-0.2.4）：新增 `references/credit-risk-sections.md` 与 `.json`，信用风险年报任务按节抽取，不再按关键词临时取约 12 页。
- **数字包**（dev-0.2.7–0.2.8）：新增 `scripts/numeric.py`，`numeric-import` 校验宿主用确定性代码算出的跨期变动、重述、勾稽检查和叙述事项：两年都要有数值、单位、页码、表格编号，摘录与来源页逐字一致，`delta` 等于本期减上期，否则整包拒收。`numeric --view overview|drivers|consequences|normal|deltas|restatements|checks|narrative` 按审阅顺序展示：驱动因素 → 后果 → 已解释的正常事项。这是审阅顺序，不是评分或预警。
- **Omni 结果转来源**（0.3.0 新增）：`ontology.py omni-source` 把保存下来的 Omni 解析结果（structuredContent 或完整 JSON 响应）逐字写成内容文件，生成带 `page_spans` 的来源记录，可选写出数字包用的 `FY<年>.pages.jsonl`。响应形状处理复制自 cue-lead-pieces 0.4.2 已有回归测试的代码（inline 与 artifact 两种存储，核对 sha256 digest）。只认源 PDF 页锚，跨页段、仅渲染页锚和无锚文字不给页码。不发起解析、不读 key、不花额度；只有结果以 artifact 存储时，才启动用户自己的 Bridge 从本地缓存 `read_result`。
- **SKILL 第 1 步写入 2026-10-07 实测的四点**：`save_result` 或只存 Markdown 会丢页码；请求 artifact 时小结果仍内联返回；入库按真实响应形状；Bridge 1.8.3 对本地文件 grounded 解析返回 `DETAIL_CAPABILITIES_UNAVAILABLE`，SEC EDGAR 网址返回 `SOURCE_ACCESS_DENIED`。
- **描述改正**：frontmatter 原写「工具只机检输入包完整性」，已不准确（`prepare` 绑定逐字证据，`numeric-import` 校验数字出处）。新描述写明工具做什么、不判断事实真伪、不做预警或风险发现。
- **验证记录**：`references/verification.md` 增加留出集回测（40 份年报、7,598 页）。根因前 3 命中：本体 5 / 关键词检索 4 / 文本差异 6，未过预设通过线；证据有效率 0.958 / 0.463 / 0.660；每家对照误报 3.2 / 3.3 / 3.9。三组数字和局限并列写明，预警说法被证伪。微软实测记录保留不变。
- **测试**：`test_numeric.py` 改为标准库 unittest，夹具数字换成合成整数（原夹具像真实公司数据）；`test_ontology.py` 增加 `OmniSource` 离线测试（合成文本，假 Bridge）。CI 另起仓库级 PR 跑 `test_numeric.py`。版本戳四处同号（脚本 VERSION、两份 frontmatter、锁测试）。
- **README**：保留 0.2.4 的常见问题、出错处理、触发示例和国内取证路径各节；补 `omni-source`、`catalog`、数字包说明和对应出错行；常见问题加一行指向同仓库 cue-lead-pieces（引文核对与线索稿），另一行写明不能拿来做预警。

### 0.2.4 — 2026-10-04（docs·M168 第二批三件套 + 专项「国内可达取证路径」：FAQ 与反模式 / 出错了怎么办 / 触发示例，中英双脸同步；新增节接在 §交付与验证 之后、§试用反馈 之前）

- 缘起：渠道质量测评本件 antiPatternFaq=3.8（全档最低项之一：该禁的散在 update-policy 与 knowledge-contract，无反模式专节）、errorHandling=4.3（技术性强、无面向使用者的修正引导）、trigger=4.8（调用面散在段落里）、**trust.domestic=4.3**（示例与文档链接指向境外站点，网络受限时取证面变窄；另指出「脚本输出与错误提示为英文」——本段只补路径与说明，**不改脚本出口语言**，那属机器面，另票）。
- 「出错了怎么办」按 `ontology.py` **现跑实际出口**写：成功一行 JSON `{"status":"valid", "counts":{...}, "semantic_verification":"not_established_by_scripts"}` 退 0；失败 `{"status":"invalid","error":"…"}` 退 2（stderr），实测两类真实原因 `knowledge integrity mismatch` 与 `source hash mismatch: <来源 ID>`；契约类消息（invalid ID / duplicate ID / duplicate JSON key / invalid value for）取自脚本源码字面。**不新造错误码**，也不把「脚本不证语义」这句省掉——出口里那句 `not_established_by_scripts` 就是本件的精度边界。
- 专项口径：**demo 无需 API key、不联网**为既有事实；真实取证补三条现成路径（用户给文件优先 / 境外取不到就导出成文件而不是绕 / 检索补来源只在授权研究范围内），并保留两条既有铁律：URL 形状不能证明公开可访问、取不到就标「未取得」不推断不静默覆盖。不承诺未开放数据域、不承诺特定站点可达。
- 版本位：README 与 README.en 在渠道包字节面内，占 patch 位 0.2.3 → 0.2.4（SKILL.md 与 SKILL.en.md 的 frontmatter `version` 同步，双语一致性由机检查）；脚本、references、assets 零触碰。
### 0.2.3（文案面·五处窄修）— 2026-09-28 机检范围两分 / 触发尾块补旧形 / 权威向归位 / 计数指针化

- 机检范围收窄为如实：listing 与摘要此前把「打包、更新、查询、导出」与「完整性」并列写成由工具机检——工具只**机检输入包完整性**，其余四件事是工具**执行**的动作，导出路径对消费端返回未验证，外部 OKF 兼容性本件不验证。四词并列句改两分句，中英两份 frontmatter 同文同改。**同时删掉摘要与描述里写死的自测条数**：同一个数在包内出现多处且彼此不一致，改为一句话指现跑命令（活计数只留能被跑出来的那一处）。
- 英文触发尾块补回一个旧字段里存在、迁移时掉出来的英文形状（供应商/产品变化类）；**本包早前一条 CHANGELOG 曾把那次迁移写成"英文触发词零丢失"，那句不实**——当时中文语义确实仍在，但英文检索面少了一形；按「解释性句子只写类别名」的规矩，此处不复述那六个字的原话，只定性：**该声明当时的判定口径把"语义在"当成了"检索词在"，是两件事**。
- 权威向归位：两处称英文译件为权威 Agent 指令，是主从倒正之前的旧句，现改为「Agent 指令以中文主文件为准、英文件为同步译文」；另把我上一轮写的一句过头话（把夹具与代码并列为权威）改回边界内的形状：**判定=脚本现值，夹具只是已跑用例的例证、不保证穷尽**。
- 公开验证记录里那条测试计数改指针形：记录只说"当日全过"，数与结果以现跑命令为准。
- 根 README 两处（同批）：本件那一行的活版本号换成与其余八件同法的 frontmatter 指针；「本件不在旧 ZIP 里」那句按发布页现值改为现状句（发布页实有本件资产），不再与同段九件指路自相矛盾。**「版本权威=frontmatter」这条声明从本条起才是真的**：根行、文档、渠道字段三处都不再各存一份数。
- summary / description 均在字数闸内（75／297）。**本条与同日那条机器面条目同占 0.2.3 一个版本位**（工具版本戳同号化属机器面，两事各写一条、不互抄），贴本条时机器面已在盘，文案面未再动 scripts。
### 0.2.3（机器面·M158+追加）— 2026-09-28 版本戳同号化+双份 frontmatter 一致性锁（M156 第 6 项，M158 追加条闭 EN 面漂移盲区）

- 审方仓外 demo 实测：0.2.2 流程产出的 run.json.skill_version 仍刻脚本常量 0.2.0——凭据分裂，且违本文件顶章「版本权威=各 SKILL.md frontmatter 现值」自书规矩。**案①同号化**:VERSION 与两份 frontmatter 同号（裁单「0.2.3 版本位同批：VERSION+两份 frontmatter 一起走」，三处现值均 0.2.3）。SCHEMA_VERSION(0.1.0)保持独立轨不动——协议版本与 skill 版本分离本属设计意图（:148/:347 皆协议面），此单只修「冒充 skill 版本的字段」。案②（双轨并见+文案注明）不取：字段名就叫 skill_version，让它自证为真优于加解释，且「写可见」的前提工作在文案面、越「只常量+锁」预算。
- **追加条（4.1 发现，lead 转）**：锁初版只读 SKILL.md——本包 SKILL.en.md 同带 version 字段，两文漂移测不到。**判形=双读不撤字段**：渠道加载器可能各读自面 frontmatter，撤 EN 版位=给未验证的读方制造风险；等式收为「脚本==SKILL.md==SKILL.en.md 三点同号」，任何一处独走即 FAIL，零破坏面。锁测试 `VersionConsistency.test_script_version_equals_both_skill_frontmatter`（subTest 两份逐面）；反证两笔实测：**脚本漂 9.9.9→恰 2 failures（两面各逮一次，subTest 归属正确）**；**仅 EN 独漂 0.2.9→恰该面 1 failure、中面不告**（旧单读锁对此哑巴——追加条所要闭的正是这个盲区）,EN 面测后原样恢复、复跑全绿。
- 测试 47→**48 项实测 OK**（锁 +1）;lint 9 skill 0 error 0 warning。改动面：ontology.py 常量一行、两份 SKILL frontmatter 各一行（裁单授权）、test_ontology.py 锁+import re、本机器条；文案面 M157 各写各面互不抄。

### 0.2.2 — 2026-09-28（lead·主从倒正，Owner 二点）

- SKILL 主文件由英文改为**中文主**（原 SKILL.md→SKILL.en.md，原 SKILL.zh-CN.md→SKILL.md）:skillhub 是中文社区，九件主面语言至此全部一致。
- 四处「中文·English」切换行改为**纯文字指路**——渠道页不解析相对链接，可点切换在此环境是死 UI，不装能点。
- 两文口径同步句改「以代码与夹具现值为准」，与 C-46 一致。

### 0.2.1 — 2026-09-28（lead·渠道一致性修正，Owner 点名）

- 渠道 listing description 由英文主改为**中文主**（≤300、三段：拿到什么/机器挡什么/适合与不适合），英文触发词移至尾部保留，零丢失。
- 两份 README 头部「v0.2.0 公开试验版」活版本+状态尾句删除（指针化纪律，对齐族规）。
- 新建本 CHANGELOG（族规补齐：此前为九件中唯一缺 CHANGELOG 的包）。
- 语言切换行经查与姊妹件同制（链接目标四件俱在），保留不动。

### 0.2.0 — 2026-09-28（Owner:v0.2 evidence briefs 与零密钥 demo）

- 上游历史（仓内 PR#1-4）:v0.1.1 audited public knowledge workflow → v0.2 evidence briefs;Windows 首跑兼容三修（.gitattributes LF、symlink 测试平台跳过、claim_kind 默认 reported）,47 项测试。

### 0.1.1 — 2026-09-27（Owner:audited public knowledge workflow 首发）

- 初始上架前审计版，细节以 git log(PR#1)为准。
