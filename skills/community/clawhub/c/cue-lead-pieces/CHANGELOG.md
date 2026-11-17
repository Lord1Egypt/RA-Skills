
### 0.4.35 — 2026-11-02（本格仅刷新在架时间戳与收录新鲜度，无能力变更、无接口变更）

### 0.4.34 — 2026-10-29（指路补齐两页：三通道那张表早写明谁是主解析通道、未开通走哪条兜底，缺的只是官方配置页入口；主次照本包原句、兜底不复写，非能力面变更）
- 改因：本包把三条通道的分工写全了——技能面那张表的行首写着「cue-omni-reader（主解析通道）」「cue-data-mcp（可选）」「cue-research（可选，≤1 次）」，第三列逐条写着未开通时走哪条兜底；中文说明面「装本件用到的三枚 skill」那句写着「主解析腿是 cue-omni-reader」，英文说明面同一张表那行写着 "(primary parser)"。可整包对两枚官方配置页的引用改前为 0 枚（三面逐字各 0，包级 数据腿页 0∥解析腿页 0，带「缺指路：数据腿(可选)无页、解析腿(可选)无页」两条报警）。
- 改法（只补指路、原句一字未动；主次照原句、代价不新造）：技能面在「官方技能的调用契约以各自 SKILL.md 为准」那段之后、中文说明面在单装那条命令之后、英文说明面在同位置那句之后各接一句「主解析腿 cue-omni-reader 的官方配置页 https://cuecue.cn/hub/omni-reader，可选的 cue-data-mcp 走数据腿官方配置页 https://cuecue.cn/hub/mcp；深研那枚 cue-research 是独立入口（自带运行脚本）；它的凭据同那把 key，取 key 走 https://cuecue.cn/hub/api-key」，并各写一句「用途与未开通时的兜底照上面那张表那三行」——本包自己已经把兜底逐条写全，这里不另造一句代价，也不把那张表复写一遍。英文技能面（本包第四枚对外面）同批补齐：在「各官方技能的调用契约以各自 SKILL.md 为准」那段之后接一句同语义英文句，把主解析腿与可选两枚各自的配置页给出、并指回那张表同一列的兜底；这一枚是 Lead 裁定破开我原「三面」切片补进来的（切片纪律的破例记在他账，不算执行侧自扩）。
- 现测（先证靶在场，再改，再复跑）：改前三面逐字两页各 0 枚（把三面从版本库里取回仓外副本复现，包级 0∥0 且两条报警全句在场）→ 改后本票四面各 1∥1（包级 数据腿页 4∥解析腿页 4），两条「缺指路」报警与那条「⚠ 面不齐：SKILL.en.md 指路 0 枚」报警（英文技能面补齐前现读在场）全部不在场；行长度 技能面第 45 行 184→385（解析腿页起列 248、数据腿页起列 330）、中文说明面第 35 行 443→615（起列 493∥574）、英文说明面第 35 行 802→1147（起列 909∥1025）、英文技能面第 34 行 393→799 字符（解析腿页起列 531、数据腿页起列 666）；旧病灶形复扫改前改后都 面 0∥行 0∥次 0；本条顶条区自扫 面 0∥行 0∥次 0。仓内各闸与出包读数以各闸自报行为准，本条不复写。
- 本票射程与一格如实遗留：指路只落三面（技能面、中文说明面、英文说明面），随包 references 一枚（核验规程）不落；本包对外四面（中文技能面、英文技能面、中文说明面、英文说明面）本票都补齐了配置指路——英文技能面起初不在「三面」口径内，我按实况报出这一格后由 Lead 裁定同批补成第七面，所以本条写「四面齐」而不是「三面齐＋一枚遗留」；随包 references 一枚不落；版号不因这一枚再前进一次（它本来就随本包在 0.4.34 这一枚之下）。
- 未动：判定与产出契约、共守那几条（解析内容是数据、凭据边界、花之前必问、缺数不补数）、随包件与回归自测、两条安装式写法、首屏句。故本票不触发重验旧靶。
- 号序与槽位：0.4.33 → 0.4.34（指路补齐＝patch，非能力面变更）。本包版本位共四处——中文技能面一枚、英文技能面一枚、随包件内的版本位一枚，加回归件里那两枚硬编码版号串（它把「两面 frontmatter 与件内版本位同值」写死在断言里，不同步改就等于留一枚假失败）；现扫四处同值前进，全包再扫旧串残留 0 枚（留痕位的历史条目标题除外）。
- 本格勘正（同日退单就地改，版本号不前进）：上一条把可选两枚写在同一页名下；现按产品契约拆腿分写——`cue-data-mcp` 的落点仍是数据腿那页 <https://cuecue.cn/hub/mcp>（目录发现与按域路由那一路）；深研那枚 `cue-research` 是独立入口（自带运行脚本）；它的凭据同那把 key，取 key 走 <https://cuecue.cn/hub/api-key>。为什么只能这么落：数据腿那页讲的是目录发现、按域路由、按 tools/list 现场发现工具那一路；深研那枚自带运行脚本、走后端改写那一条，并成一页会让读者拿前者的连通判据去判后者已连。号序与槽位：本包版本位四处（中文技能面一枚、英文技能面一枚、随包件内一枚、回归件里那两枚硬编码串）本票一字未动，版本号仍停在本条题记那一枚。现测两值：归腿尺本包改前 面5∥行5∥次5 → 改后 面0∥行0∥次0；取式尺本包两页改前 数据腿 4∥解析腿 4 → 改后 4∥4（数据腿那页在四面各留一枚，把它删掉才是这次退单要避免的另一种错）。仓内各闸与出包读数以各闸自报行为准，本条不复写。

### 0.4.33 — 2026-10-27（补一枚产物形态样例：`brief` 跑包内合成夹具的原样输出，两面各挂一句指路）
- 改因：站点生成器取「示例」走三级回退（面文产物块 → 包内样例件 → 包内 good 前缀样例），本包三级全空——`find scripts/fixtures -maxdepth 1 -name 'good*.md'` 现读 0 枚，那一页只能写「该枚面文未含可复制的样例输出」。句子是真的，但用户在这一页看不到这件东西交回来长什么样。
- 改法：新增一枚 `scripts/fixtures/good_lead_pack_sample.md`，正文是 `cue.py brief` 那**一条**命令的 stdout 原样（材料目录＋线索件＋逐字证据 JSON 行；产物本体 17 行、698 字符含尾换行、697 字符去尾换行），一行没改一字没补。整枚文件 50 行、3126 字符（5506 字节），其中产物本体 17 行、697 字符（这段两种数法同值：`wc -l` 17 行、去首尾空白也 17 行；含末换行是 698 字符），其余 33 行、2428 字符是说明与复跑命令（那段 bash 围栏 15 行）——**行数口径一律 `wc -l` 的换行数**（本文件以末换行结尾，「换行数＋1」那种数法会多出一行，别拿它当这个数）。数据源与跑法都取自本包已提交的合成夹具 `scripts/fixtures/omni_real_shape.json`（实测回执形制、文本为合成、编号为假，与包内回归同源）——本包不编财务数字，也不含真实机构或个人。样例头部写清四件事：怎么复跑（五条命令）、`brief` 那一支在什么条件下会走网络、评级与目标价一律 `[待人工]`、里面那条「建议动作」是核对动作不是买卖动作。README.md 与 README.en.md 各挂一句指路，措辞与实现同形（不说「有完整示例」，只说这是跑出来的原样输出）。
- 复验一（Major LP-1「零网络」没封住请求分支，判语成立）：`cue.py:750-752` 的 `cmd_brief` 在 `leads.json` 缺位时会先调 `cmd_leads(no_llm=False)`，`llm()` 在 `CUE_LLM_BASE_URL`＋`CUE_LLM_API_KEY`＋`CUE_LLM_MODEL` 三枚齐位时才 `get()` 发起——所以「零网络」是**条件句**，不是无条件。判据我自己搭了假传输桩复现（只把 `cue.py` 的 `get` 换成记次桩、桩内直接抛，绝不出网；合成 base 用保留域 `llm.invalid`）：三枚缺位＝发起 0 次；**三枚齐位且无缓存＝发起 4 次**（`chat/completions`，你那一档我复现上了）；三枚齐位但先用 `leads --no-llm` 落缓存＝0 次；三枚缺位带缓存＝0 次。改法取你给的第二种并留住第一种的信息量：**样例显式带那三枚合成值**，中间插一条 `leads "$RUN/DEMO" --no-llm` 把缓存先落盘，`brief` 只读缓存——这条链的零网络由命令形制保证，不靠用户机器上环境恰好缺位；头部同时把条件写明（缺任一枚走确定性分组、三枚齐位且无缓存时会走网络那一支，去掉 `--no-llm` 那条就不再是本样例的形制）。**判据与退码语义一字未动**，没为凑那句话放宽任何东西。
- 复验二（Minor TMP-1 固定名仍会撞）：上一版把写死的 `/tmp/DEMO` 换成固定名 `cue-lead-pieces-sample-run`，同机多会话照样撞。改成 `RUN="$(mktemp -d "${TMPDIR:-/tmp}/cue-lead-pieces-sample-XXXXXX")"`——唯一名由系统给，头部那句「同机多会话也不互撞」从此落在实现射程内。样例内固定名与写死路径现读各 0 处。
- 复验三（Minor COUNT-1 口径）：上一版顶条写「45 行」，用的是「换行数＋1」那种数法；磁盘 `wc -l` 当时是 44。本轮所有行数一律标口径（`wc -l` 换行数），并按改后磁盘现值落字：整枚 50 行、3126 字符（5506 字节），产物本体 17 行、697 字符（含末换行 698），说明与复跑那一段 33 行、2428 字符（bash 围栏 15 行）。2141／2709 那两枚字符数你判实则对，保留同一数法（Python `len(文本)`）。
- 复验四（R2-TMP：那行 mktemp 没有失败短路，判语成立）：上一版首行是 `RUN="$(mktemp -d …)"; export RUN`——**赋值吃掉失败码**。把 TMPDIR 指到不存在的父目录、只执行首行，现读 `first_rc=0 且 run_len=0`（外层 rc 也是 0），空 RUN 一展开，面文下游那两枚路径就变成根下的 `/DEMO` 与 `/in_full.json`。按你给的三件改：mktemp 那行加 `|| { echo 取不到临时根，停手; exit 1; }`；紧跟一枚非空且在场的断言 `test -n "$RUN" && test -d "$RUN" || { …; exit 1; }`；`export` 拆到断言之后。改后同一探针复跑：只执行首行在不设 -e、`-e`、`-euo pipefail` 三种形制下**都 rc=1**、run_len 不再以空值往下走、根下 `/DEMO` 与 `/good` 在场判断现读各 False；正常 TMPDIR 下整段照旧 rc=0、临时根在场。ldt 那枚同批同改（同一族，不留一面改一面不改）。
- 复验五（零网络那句改由出网计数证，不再只看退码）：取证形制照你教的——从面文 bash 围栏里**逐字抽块**，`PYTHONPATH` 挂一枚 sitecustomize 把 `socket.connect` 与 `create_connection` 换成遇调即抛并落文件记次。现读：抽块那 15 行整段 rc=0、临时根在场、**本段出网尝试计数 0**、根内 7 枚文件；缓存在场时再单跑一次 `brief`，17 行、697 字符、与样例正文逐字对拍差异 0 行。头部那句「按假传输桩核过，这一趟发请求次数 0」从此有两种独立证法（记次桩与 socket 拦），不再只有退码一个读数。
- 现测：`find scripts/fixtures -maxdepth 1 -name 'good*.md'` 由 0 枚变 1 枚；改后头部那五条按原样在 `mktemp -d` 现取的临时根复跑，退码各 0——`ingest` 打 1 行登记回执、`leads --no-llm` 打 9 行线索件、`brief` 打 17 行／698 字符含尾换行；`brief` 那条与样例正文逐字对拍**差异 0 行**。带三枚合成环境值那一趟同样 17 行、对拍差异 0 行，桩记发起 0 次。包内回归 **Ran 12 tests / OK**、退码 0，`cue.py --version` 现读 0.4.33，旧字面在非 CHANGELOG 面残留 0 枚（首跑那次红在版本锁那一支的来龙去脉见上一条批次的自记，补齐五枚字面后转绿）。另在临时副本里删掉这枚新样例后重跑一遍回归：同样 OK、退码 0——样例是随包读物，不进任何判据。请求分支之外全程零网络：数据目录里的清单由脚本直接写、正文先落盘，`local_pages` 见文件已在盘上就不取，`fetch` 与 `omni` 两支都没走。
- 号序：0.4.32 → 0.4.33（加一枚样例＋两句指路＝patch；能力面、判据、通道口径一字未动）。槽位同批：本包沿用既有形制共四枚面五枚字面——SKILL.md 与 SKILL.en.md 各一枚、`scripts/cue.py` 的 `__version__` 一枚、`scripts/test_skill_regression.py` 同一行内两枚断言字面，五枚同号；本包单锁，无 manifest。上一行那句「两处同号」是漏算，如实改在这儿。

### 0.4.32 — 2026-10-22（凭据外发两关：非 https 或未授权目的地的 url 一律拒发，换源不免检）
- 改因：外部安全扫描器判本包随包的连通自检件可把 CUE_API_KEY 外发到未授权目的地——带 --post 时它把 key 挂到目录返回的 routing.url 上，既不强制 https、也不校验目的地是不是被认下的那枚。改因写在这儿的是扫描器判语，不是渠道要求；渠道那一侧没有改过任何字。
- 改法（只治在汇聚处）：发请求前统一到两关——scheme 必须是 https，且 host 命中授权后缀。缺省那一枚授权后缀由件头目录入口那枚现值推出（依据写在件头注释里，不另编一张域名清单），要放行别处由用户显式带 --allow-host。过不了就拒发：不读 key、不构造那个请求、退码 6，并把拒绝原因与目标 host 印出来；目录入口本身不是 https 走退码 7。--catalog-url 与 --catalog-file 两条换源路径过同一道关，不再有「换进去什么就打什么」那一形。
- 面文：README.md里那句「本件不校验它是不是渠道端点」的旧承诺改成新承诺，代价同句写清——老的免检形制关掉了，换来的是凭据不会外发到未授权目的地；正当端点恰在授权后缀之外时，退 6 是请用户显式认下它，不是断言那枚端点不该存在。
- 现测：反证尺 scripts/m393_key_send_probe.py 逐枚跑满五格（真 socket 靶＋打桩传输层）。修前那组副本读数：件数=12｜过靶=0，靶自己数到请求 1 次、Authorization 头 1 个（哨兵 key 真的发出去了）；修后同一把尺：件数=12｜过靶=12，T1 那一格靶数到请求=0。正控那一格（https＋授权 host）修前后都通，说明这关没把今天那条正当请求改坏。全仓那几把尺同日同值：lint --strict、卫生闸、首屏尺、安装式对表、场景图各 rc=0（数取各尺自报行，本文不复写）。
- 未动：退码 0／4／5／1／2 的既有语义与连通判据本身（判据仍在各包 README 连通那一节，本件不复制第二处真值）、包内其它脚本、闸与词表、CHANGELOG 历史条目（不回改）。
- 号序：0.4.31 → 0.4.32（凭据外发面收窄＝patch：对外只减不加，原来该发得出去的正当请求照旧发得出去）。


### 0.4.31 — 2026-10-22（英文面的运行前置声明归位到 openclaw 层，版本锁与面件成对退休）
- 改因：全仓只有本包这一枚 `SKILL.en.md` 还写着裸的 `metadata.requires`，而抽取器认的层是 `metadata.openclaw`——少一层，那份声明在任何工具里都读不到，后来人按它排查会白跑一趟。中文主面早已归位，英文面是当时漏下的那一枚。
- 改法：把 `requires` 整枝挂到 `openclaw` 下——`bins` 与 `recommendedSkills` 两枚键名、值与顺序照原样搬，一字未动；本面不新增 `envVars`（声明层只读 `SKILL.md`，英文面重复一份就会变成第二个真值源）。同批把随版本走的三处锁一起对齐：`SKILL.md`／`SKILL.en.md` 的 version、`scripts/cue.py` 的 `__version__`、`scripts/test_skill_regression.py` 里那两枚断言字面，四处同号（旧写法只改面不改锁，就会自报与门对不上）。
- 射程（现数，不按记忆）：声明层改动＝SKILL.en.md 一枚；版本位所在文件 4 枚（口径＝按「盘上含旧号的非 CHANGELOG 件」以字面串现扫得出：SKILL.md／SKILL.en.md／scripts/cue.py／scripts/test_skill_regression.py，落笔后残留 0）；本包其余面文与脚本逻辑一字未动。同批还有一处不在本包内：仓根 README 两条安装路之外新加的第四条路，见仓根面自述，不占本包版本位。
- 现测：`python3 -B -m unittest discover -s scripts -p "test_*.py"` rc=0／OK（那支回归件同时校 `__version__` 与面内 version 同值，锁没对齐它当场会红）；`python3 -B scripts/cue.py --version` 现读 0.4.31；lint --strict rc=0、末行「summary: 19 skill(s), 0 error(s), 0 warning(s)」；卫生闸 rc=0、末行「summary: 面 184，ERROR 0，WARN 233」；面尺 rc=0、末行「面数=23 不合=0」；场景图 rc=0、末行「全包=19 枚…非孤点=10 枚」。
- 未动：判定与契约段、inputs／produces 声明键、slug、闸与夹具、CHANGELOG 历史条目（不回改）。
- 号序：0.4.30 → 0.4.31（英文面声明归位与版本锁对齐＝patch）。

### 0.4.30 — 2026-10-21（可选凭据从硬前置改成 envVars 的可选声明）
- 改因：上一版把这枚渠道变量写进了 requires.env，而那一层的语义是「没有它就不能开工」。本包面文另有 3 行写明不装也能跑（用户直供与降级路径），而包内代码级引用这枚变量共 4 次——所以它是「装了才有渠道数据腿」的可选通道钥匙，不是「没它就不能开工」的前置。这一处属对外把前置说重了（宣告比覆盖面大），不是排版。
- 改法：requires.env 里那枚串摘掉，改挂 openclaw 层的 envVars 一项——name、required: false、另带一句只述边界的 description（不承诺效果、不带价格）；requires.bins 照原值不动。同批把 primaryEnv 一并摘掉：它的语义是「本件主凭据」，对一把可选的通道钥匙同样说重了。
- 射程（现数，不按记忆）：声明层改动＝SKILL.md 一枚（本面）；版本位所在文件 4 枚＝SKILL.en.md、SKILL.md、scripts/cue.py、scripts/test_skill_regression.py；其余件零改动（本件按「含旧号的非 CHANGELOG 件」逐枚现扫，落笔后残留 0）。
- 现测：渠道面件尺（只读、零网络）对本枚判 ok，全仓末行「名册=18 不合=0 计划位=有」退码 0；卫生闸末行「summary: 面 180，ERROR 0，WARN 233」；面尺末行「面数=23 不合=0」；本包入口自测退码 0、末行「OK」；场景图读数与本轮开工时逐字节同＝否。lint --strict 复跑 rc=0、末行「summary: 18 skill(s), 0 error(s), 0 warning(s)」。
- 未动：面文其余段落、inputs／produces／legs 那批场景图声明键、两面 README、闸与夹具、CHANGELOG 历史条目（不回改）。
- 号序：0.4.29 → 0.4.30（对外语义更正＝patch）。新条目反引号 0 枚、美元号 0 枚（本条现读：含反引号的行 0 行／出现次数 0 次）。

### 0.4.29 — 2026-10-21（运行前置声明归位到 openclaw 层＋主凭据声明补齐）
- 改因：这枚面的运行前置写在 metadata 下的 requires 那一层，而渠道抽取器认的层是 metadata.openclaw（别名两支亦可）——少一层，声明读不到。本包引用那枚主凭据共 16 次、散在 6 枚件里（尺与本件独立扫描两值同），而 frontmatter 未声明它——官方把「代码用了却没声明」判成元数据不符。
- 改法：把 metadata 下既有的 requires 整枝挂到 metadata.openclaw 下，键序、判定语义与值一字未动，只加一层；并在 openclaw 层补 requires.env 与 primaryEnv 各一枚；面内 inputs／produces／consumes 那批场景图声明键与两面 README 未碰。
- 射程（现数，不按记忆）：声明层改动＝SKILL.md 一枚（本面）；版本位所在文件 4 枚＝SKILL.en.md、SKILL.md、scripts/cue.py、scripts/test_skill_regression.py（本包若有多处锁，枚数由这一行现读给出，不手抄）；其余件零改动（本件按「含旧号的非 CHANGELOG 件」逐枚现扫，落笔后残留 0）。
- 现测：渠道面件尺（只读、零网络）对本枚判 ok，全仓末行「名册=18 不合=0 计划位=有」退码 0；卫生闸末行「summary: 面 180，ERROR 0，WARN 233」；面尺末行「面数=23 不合=0」；本包入口自测退码 0、末行「OK」；场景图读数与本批开工时逐字节同＝是。
- 未动：面文其余段落、闸与夹具、包内代码判定、CHANGELOG 历史条目（不回改）。
- 号序：0.4.28 → 0.4.29（面件结构变更＝patch）。新条目反引号 0 枚、美元号 0 枚（本条现读：含反引号的行 0 行／出现次数 0 次）。

### 0.4.28 — 2026-10-20（真值源面的退码枚举补齐「取不到、发不出去、HTTP 层报错」那一态，与件内已重写的分形对齐）
- 改因：上一轮把随包连通自检件的退码分形按真实行为重写（4xx 与 5xx 归「HTTP 层报错」那一态），可这一层的对外说明只列了 0、4、5 三态——读者照面文跑一次协议层拒绝，拿到一个面文没解释过的退码。这一处属宣告落后于行为，不是行为变了。
- 改法：仍走指路式，不复制判据、不新增第二处真值——只在那句枚举末尾补上「取不到、发不出去、或 HTTP 层报错（含 4xx 与 5xx）」这一态；中文面与英文面各按本语言的既有句式写，句中不出现任何状态码字面，通过与否仍只看该节上面那句判据。
- 射程（现数，不按记忆）：真值源面 23 枚＝十一包的 README.md 与 README.en.md 各 11 枚，另加 competitive-brief 那枚共用源面；十二枚件内文本本轮一字未动（SHA 与上一轮终读同值：十一枚一枚、指法不同那一枚另算）。补齐后逐枚核 0／1／4／5 四态齐：23 枚齐、缺态 0 枚；同一句里第二处判据真值 0 处。
- 现测：面尺直跑 rc=0、末行「面数=23 不合=0」、PASS 行 23 枚；逐面按尺的项自取一遍，13 项全绿、红项 0 枚，其中「同节通过判据句恰 1 枚」在 23 枚面上仍各为 1 枚（补的句子不带那枚字面）。
- 未动：件内代码、退码判定、闸与夹具、各包其余面；CHANGELOG 历史条目不回改。
- 号序：0.4.27 → 0.4.28（对外宣告补齐＝patch）。旧号在非 CHANGELOG 面残留 0；新条目无反引号与美元号。

### 0.4.27 — 2026-10-20（连通自检件：一处帮助句收到条件形、退码表按真实分形重写、返回体形状不认识那一支不再抛异常）
- 改因：三处宣告比覆盖面大。其一，改读本地快照那个开关的帮助句对「这一个开关触不触网」写了无条件全称断言，而同一开关配上显式发包开关仍会向快照里给的地址发一次。其二，退码表把 4xx 与 5xx 归进「有响应、判据不满足」那一档，可标准库在这一支抛 HTTPError，件走的是退 1 那条出口。其三，返回体里那个 result 字段不是对象时，件直接取它的属性，抛异常带回溯，与件自称的「每条失败都走一句人话出口」不符。
- 改法（只把宣告收到覆盖面内，不新增取式）：帮助句改成条件形——本开关自身只读该文件、不发包，带显式发包开关时仍会向该快照里给的地址发一次。退码表按真实分形重写：退 1＝取不到、发不出去、或 HTTP 层报错（含 4xx 与 5xx 这一支）；退 5＝请求发出去了、也拿到了响应，但判据不满足（tools 是空数组、返回体里没有它、解析不出、或形状不认识）。取 result 之前先判类型，认不得就一句人话点出顶层类型与该字段类型、退 5，不猜形状。
- 一枚同族自抓：返回体解析不出那一支，旧文案写着退 5、代码却退 1——同一条消息与自己的退码打架。本轮把退码收到与文案一致（5）；这一处不在本轮那三处之内，是我跑反证靶时现读到的，如实记在这里。
- 现测（进程内桩、零真实出站，十二枚逐枚各跑一遍）：result 为数组那枚反形靶 ⇒ 退 5、Traceback 0、点名句带顶层类型与该字段类型；406 与 503 两支同退 1；本地快照单用 ⇒ 发包 0 次、退 4；快照配显式开关 ⇒ 发包 1 次、退 0；解析不出 ⇒ 退 5；tools 空数组与缺 tools 各退 5；好样与 SSE 形各退 0；缺凭据、域不在场、该域无 routing、非 live 域各退 1；既不给域也不给清单退 2。十二枚件仍同构（内容两形：十一枚一枚，判据出处指法不同那一枚另算）。
- 未动：三处真值源面与那块可复制命令一字未动；目录取法、routing 取式、缺省零发包这个默认、判据的权威表述位置、闸与夹具都没碰；CHANGELOG 历史条目不回改。
- 号序：0.4.26 → 0.4.27（件内文案与一支取式的勘正＝patch）。旧号在非 CHANGELOG 面残留 0；新条目无反引号与美元号。

### 0.4.26 — 2026-10-20（连通自检件的三处对外精度：失败要响亮、退码要分态、换源不许无声）

- 病灶三条（逐条都在本包这件上真跑复现过，不采信转述）：①取目录失败那一支的错误句里格式化了一个尚未绑定的变量——把网络层换成离线桩实跑，默认目录入口形与换源 URL 形各抛一次未绑定变量异常并带回溯（第三支「本地快照路径不存在」原本就走优雅支，照实报，不当自己修好的）；②退码不分态：只取到地址也退 0、连上了但 result.tools 是空数组甚至返回体里根本没有它也退 0——把「跑过一步」与「连上且非空」压成同一个数，读的人据此以为连通已证；③件接受换源（目录 URL 或本地快照），并把那个源给的任意地址直接发出去，既不校验也无声明，而面文当时那句「打的也是运行端点、不是渠道」是无条件承诺。
- 改法四条：①失败形整族补齐——凡错误支要用的名字先赋初值，三扇失败统一一句人话、退码 1、零回溯，取目录与解析返回的失败也走同一形；②退码分五态并写明——0＝实连（HTTP 200 且 result.tools 是非空数组），4＝只取到地址、连通未证（缺省那一支），5＝连上了但现场值未满足，1＝取不到或发不出，2＝既没给域也没给列清单；面文那句改成指路式（「退码 0 即满足上面那句判据；退 4＝还没证过连通，带 --post 再跑一次」），不在任何面上复制第二处通过判据；③换源不许无声——发那一次之前先把目标 host 印出来，目录来源不是默认那一处时回字首行再带一句「目标地址来自换入的目录，本件不校验它是不是渠道端点」，面文那半句同步改成条件形（默认入口时才承诺只验运行端点），双语各按本语言原文重写、不代译；④帮助文本的判据出处指法逐枚按各包实际真值面写（本包就是门面那一节），不复述数字条件。
- 判据现值（全程离线：桩只拦在本进程内，一次真实出站都没有）：两头值成对——改前那份默认 URL 形与换源 URL 形各跑出未绑定变量异常带回溯、改后三扇皆退 1 零回溯首行点名；退码四态成对喂桩——tools 非空退 0、空数组退 5、返回体无该项退 5、不带 --post 退 4 且桩见 POST 次数 0，另两扇（缺凭据、域不在场）退 1、无参退 2；换源可见性——把快照里那枚地址指向回环端口，首行印出目标 host 与那句不校验声明，POST 次数由桩计数、零真实出站。逐枚 rc 值在证据档内。
- 面文：23 枚真值源面的那行指路各重写成「退码指路式＋条件形承诺」，逐面终态断言——每面恰 1 行、新句内不出现状态码字面（同节通过判据句仍恰 1 枚每面）、退码说明与条件形两半各在场；上一轮补上的那块围栏本体一字未动。
- 未动：判定语义与机检闸、夹具、包内既有脚本；三层句其余部分、降级句、取证腿句、安装句一字未改。
- 版本位：0.4.25 → 0.4.26（随包件失败形与退码分态＋面文条件形＝patch）。旧值非 CHANGELOG 面残留 0；新条目无反引号与美元号、票号零、旧病灶串零原样引。

### 0.4.25 — 2026-10-20（连通自检改为缺省零发包、要发须显式带 --post；一条命令形指路补到每一枚真值源面）

- 病灶两条：①上一版那支随包件默认就把那一次 tools/list 发出去，"忘带开关"这个形状一直存在——实测里它已经咬到过两次（写脚本的人和跑脚本的人都中过），根因不在手滑，在缺省方向；②除两枚试点包，其余各枚包的面文没有一行指路到这支件——用户读得到回字形状的说明，却不知道有一条命令可以不手改域。
- 改法一（行为）：随包件改为缺省零发包——不带 --post 时只走到"取到该域 routing 里的 url"并印一行提示；要真发那一次清单调用必须显式带 --post。原先那个"只取值不发包"的开关取消（它成了缺省），退出码语义与判据出处一字未改。桩测自证：本地桩只监听回环地址，逐枚跑两趟——缺省一趟桩见 0 次、带 --post 一趟恰 1 次，且桩收到的请求头带 Bearer、Accept 是那串两值、请求体里 method 就是 tools/list；凭据用的是一串假键，真实凭据未进这一趟，任何出口读数里也不出现它的值。
- 改法二（面文）：每一枚真值源面各有一行一条命令形指路（本包共两面；门面明文不复述三层句的那一枚包，指路落在它被指的那一节），形制与试点包同一句话的形——命令含 --post、并写明"缺省一个包都不发、不带时只取 url 给你看"，域 id 请从同支件的 --list 现取。双语各按本语言原文写，不代译；上一轮补上的那块围栏本体逐字节未动。（同一句里再补半句：本件只验运行端点连通，不向渠道发布、不产生受理，带 --post 那一次打的也是运行端点、不是渠道——缺省改成零发包之后，用户最容易误读的反而是"跑过自检就等于和渠道打过交道"，这半句一次把那层削掉；补进去的字样刻意不含状态码数字，同节判据行仍恰 1 枚每面。）
- 判据现值：23 枚真值源面逐面现读——一条命令形指路恰 1 枚、回字形状精度句恰 1 枚、--post 字样在场；该节围栏仍 1 枚、块内五串 5/5、块本体语法检查各退码 0、同节判据行仍恰 1 枚每面；十二枚随包件同构（各 168 行），唯一差异仍是那枚包的五行注释指法。
- 未动：判定语义与机检闸、夹具、包内既有脚本；三层句其余部分、降级句、取证腿句、安装句一字未改。
- 版本位：0.4.24 → 0.4.25（随包件行为改为显式发包＋面文指路补齐＝patch）。旧值非 CHANGELOG 面残留 0；新条目无反引号与美元号、票号零。

### 0.4.24 — 2026-10-20（连通自检扩成一条命令随包件＋面文补一句回字形状精度）

- 病灶两条：①上一轮那条「一条命令跑完连通自检」的随包件只在两枚试点包里，其余各枚包的用户读同一节说明仍要手改块里那一行域占位，或自己拼 curl——同一能力在各包之间不齐，是「装完之后连不连得上」这条链上的第二处断口；②现场事实一枚：这处端点答的是 SSE 形回字（一行 event、紧跟一行 data），要看的 result.tools 在那条 data 载荷里。面文此前只写「返回体里 result.tools 非空」，严格按字面找的人在真实回字里看不见它——不是判据写错，是回字外层包了一层没写出来。
- 改法：本票新增随包件 scripts/cue_connectivity_check.py（165 行、纯标准库、零依赖）。它匿名 GET 目录、按 --domain 给的域 id 取该域 routing 里的 url（取对象里那个可发请求的字段，不取整枚对象）、带 Bearer 与 Accept 两个头向它发一次 tools/list，把 HTTP 状态码与 result.tools 枚数打到屏幕上；--list 只列在场域 id 与 url，--dry-run 只取值不发 POST，--catalog-file 改读本地快照（受控离线靶走这一形）。退码 0／1（域不在场、没有 routing、routing 缺 url、本地凭据缺位、请求发不出去——五类各一句人话）／2（既没给 --domain 也没给 --list）。
- 面文一句：连通那一格里各补一句回字形状精度（中文面与英文面各按本语言原文写，不代译），只描述回字外层形状与 result.tools 所在位置，判据本身仍只有既有那一行——句子里刻意不出现状态码数字，以免同节多出第二处判据真值。
- 同批修一枚对外精度缺陷（上一轮那条 minor）：目录里某域 routing 在场却缺 url 时，旧取值式先抛回溯再由空值守卫报「先从现场 id 中选一个」，提示不精确。新件走「对象里取那个字段」的形，同一份删掉 url 的本地快照实跑：旧式退码 1 且错误流里有一枚回溯、末行是那个键名的 KeyError；新件退码 1、零回溯、首行直接点名「这一枚 routing 在场但没有 url 字段」并列出它实际有哪几枚键。两头值成对，十二枚新件各喂同一份变异快照跑过，不留「只一枚包修了、其余照旧崩」的半修面。
- 判据现值：23 枚真值源面逐面 SSE 句恰 1 枚在场；上一轮那块围栏本体与各面既有判据行逐字节未动（块体对上层版本逐面同值）；该节围栏仍 1 枚、块内五串 5/5、块本体语法检查各退码 0、同节判据行仍恰 1 枚每面。
- 未动：判定语义与机检闸、夹具、包内既有脚本；三层句其余部分、降级句、取证腿句、安装句一字未改。
- 版本位：0.4.23 → 0.4.24（新增随包只读自检件＋面文一句回字精度＝patch）。旧值非 CHANGELOG 面残留 0；新条目无反引号与美元号、票号零。

### 0.4.23 — 2026-10-20（连通块不再要人手抄 routing；值指向对象里的 url；块自己把 HTTP 状态打出来）

- 病灶三条：①上一轮补上的命令块要求用户把目录里该域 routing 的现值手工抄进变量——抄错就连不上，这是「装完之后连不连得上」这条链上最后一处人肉环节；②旧面文那句把 routing 说成可以直接逐字粘贴的单个值，而目录返回里 routing 是一个对象（含 path、url、transport、protocol_version、headers 五个键），能直接发请求的是其中的 url——照旧面文抄就是把整枚对象当地址发，命令必然跑不通；③块里 POST 用静默开关发出去，把「通过＝HTTP 200」留给读者自己核，块本身一个状态都不打。
- 改法（四处文件五把锁同批（双语两面 frontmatter、包内脚本的版本常量、回归测试那一行里的两枚断言）之外，只动本面包的面文）：块内按顺序补五件——把目录入口赋一次给变量（本面唯一一处该字面，散文不再重抄）、先列一遍在场域与其 routing 里的 url、按用户填的域标识现取 url、取不到时一句人话并退码 1（显式判空，不用「未设即报错」那形——它退 127，会被读成命令找不到）、最后 POST 那行加状态输出形把 HTTP 码自己打出来。散文四处同步改：匿名 GET 那句改为指块里那枚变量、「按目标域 routing 实连」改为「按 routing 里的 url 实连」、取值句改述为现取过程并写明取的是对象里的 url 字段。中英两面各按本语言原文改，不代译、不复写第二处通过判据。
- 判据现值（每真值源一枚，逐面 23 枚）：该节围栏仍 1 枚（并入现有块、未另开）｜块内五串齐在 5/5｜块本体语法检查退码各 0｜同节「通过判据」行仍恰 1 枚每面（未新增第二处真值）｜块内含状态输出形｜值指向 routing 里的 url｜每面目录入口字面恰 1 处（约束收紧扣死）。
- 真跑凭据（只读匿名目录 GET、零计费、POST 那行不执行）：三枚不同族的面切出块体前段实跑，各取回非空 url（长度 36／41／39 字符）退码 0、错误输出 0 字节；坏标识靶退码 1、错误首行即点名、零 Traceback；状态那形在同一入口实测印出 HTTP 200。
- 一枚落面缺陷自抓（本包判据逮的，不是注入）：第一版落面后 23 枚面的块体语法检查全退 2——命令替换收尾少一个双引号；补齐收尾引号后重跑，上面那组读数是修后值。
- 未动：判定语义与机检闸、夹具、各包脚本；三层句其余部分、降级句、取证腿句、安装句一字未改。
- 版本位：0.4.22 → 0.4.23（面文补取值命令与状态输出、勘正 url 指向＝patch）。旧值非 CHANGELOG 面残留 0；新条目无反引号与美元号。

### 0.4.22 — 2026-10-20（连通自检那一格补上可整段复制运行的命令块·每真值源一枚）

- 病灶：三层自查的连接层只有散文——怎么问、看哪个字段算过都写了，却没有一枚能整段复制就跑的块。上一版记录当时已把「可执行样例」降级为散文规格并写明命令块另票补，本票补的就是这一格。
- 改法：双语两面各落一枚（本包两面都是三层句的真值源，各含完整的取值与判据表述，不是指路式外包，所以按「每真值源一枚」各补一块、共两枚）。块内四件：向 routing 占位符（带美元符那种写法）发一次 POST、带上 Bearer 头引用本地凭据变量、带上那个缺了会 406 的 Accept 头、请求体里写 tools/list 这个 method。块后补一句取值说明：占位符的值＝上面那句里那份匿名目录返回中该域 routing 字段的逐字现值，面内不硬编码域名或路径，凭据变量取自上一层那把本地凭据、不进聊天也不在终端回显，本块不新增任何凭据读取动作。
- 一格刻意不复写：通过判据（HTTP 200 且返回体里 result.tools 非空）本包两面那句原文已在同一节里写全，本票不再抄第二遍——一处事实两处真值正是这一族要防的，判据句沿用既有那一行，块只做「怎么问」这一半。
- 判据现值（逐面四件同拍，取值窗＝工作树进行态）：该节内围栏块各恰 1 枚（数法用逐行状态机、同缩进开闭配对，不用行首宽式，防缩进漏数）；块内五串齐在各 5/5；对块本体单跑 bash 语法检查退码各 0；同节含取值句与本票新补那句说明。块内域名字面 0 处、具体工具名 0 处，成功回字只给形状样例。
- 未动：判定语义与机检闸、夹具、各包脚本零改动（四处锁同批（双语两面 frontmatter、包内脚本的版本常量、回归测试里那两枚断言）之外）；三层句其余部分、降级句、取证腿句、安装句一字未改，插入全是追加、未删任何原行（锚行号改前改后同值）。
- 版本位：0.4.21 → 0.4.22（面文补可执行样例＝patch）。旧值非 CHANGELOG 面残留 0；新条目无反引号与美元号。

### 0.4.21 — 2026-10-20（「已连」那句主语摘对；随包记录里「可执行样例」降级为散文规格）

- 改因一（面文主语）：三层自查里中文那句写成（旧句把「在场」这件上一格已判完的事，又推到本格重判一次，主语错位）——上一格已经判完「key 存在于本地凭据设施」，这一格判的是服务端接不接受，把「在场性」推迟到连通层会让三层自相矛盾。现改为「上一格判的是那把 key 在不在本地凭据设施里，它被不被服务端接受，要到这一格才判得出」。同包英文面那句语义本就正确，一字未动；改后中英同形。
- 改因二（随包记录超实）：上一条记录里写（旧句把这件事写成「可执行样例」，比成品面实际交付的多一格），而成品面当时只有散文（面文里可复制运行的命令块零枚），等于宣告还没交付的东西。现降级为「连通自检的散文规格与通过判据（写怎么问、看哪个字段算过，不承诺工具清单；可整段复制运行的命令块另票补）」。
- 那条改动落在未入库的进行态记录上（工作树直读，git show HEAD 对该串零命中），属就地改进行中那条、不触「历史条目不回改」；改因另立本条写明，便于对照。
- 未动：判定逻辑、阈值、错误码集合、夹具与脚本；取证腿两句、降级句、中英其余判据一字未改。
- 版本位：0.4.20 → 0.4.21（面文勘正＝patch）。旧值非 CHANGELOG 面残留 0；新条目无反引号与美元号。

### 0.4.20 — 2026-10-19（「已连」不再等于匿名目录可达；补实连问法与通过回字）

- 病灶：README.md:40 与 README.en.md:40 这两枚面把「已连」定义成匿名 GET https://cuecue.cn/api/mcp-catalog 拿得到当场返回——那只证公开目录可达，证不了这把 key 被接受，更证不了某个 live 域真的连上；同仓另一批件已改成「匿名只算目录可达」，两边口径分叉就是公开面最坏的一种。
- 改法（三层各自写明能证到什么＋反向禁止）：装好＝重列已安装清单看得到名字，只证明文件到位、不证明取到数；配好凭据＝key 在场，并明写被不被接受要到下一格才判得出；已连＝带上那把 key 按目标域 routing 实连（Authorization: Bearer，并带 Accept: application/json, text/event-stream——缺这个头会 406，是协议行为不是鉴权失败）且 tools/list 有返回。匿名目录那半句改判为只证目录可达，本件不把它叫「已连」；另补「连接报错≠域无数据，如实报，只重试错误标明可重试的部分」。
- 连通自检的散文规格与通过判据（写怎么问、看哪个字段算过，不承诺工具清单；可整段复制运行的命令块另票补）：向该域 routing 给出的地址发一个 JSON-RPC 的 tools/list 请求；算通过＝HTTP 200 且返回体里 result.tools 非空，逐字形如 {"result":{"tools":[…]}}，工具名与入参 schema 就在那一格；工具清单以那份返回现值为准，本件不预先承诺有哪几枚、也不硬编码工具名。
- 双语同形：中文面与英文面各按本面语序写全，同一判据同一次落，不留一半新一旧。判定逻辑、阈值、错误码集合、夹具与脚本一字未动；降级那一半（不装也能跑、用户直供、缺数点名句）原样留住。
- 版本位：0.4.19 → 0.4.20（对外口径勘正＝patch）。单锁（本包无 manifest；cue-lead-pieces 另有英文镜像面同批同步），旧值非 CHANGELOG 面残留 0；新条目无反引号与美元号。

### 0.4.19 — 2026-10-19（赠送句补单位：500 积分／10 积分，限定语原样留住）

- 改因：口径补了单位，新写法是「新账号注册送 500 积分、每日 10 积分，以服务端为准」与英文面对应式；本包 README 第 35 行（英文面第 35 行）照此各补两枚单位，「以服务端为准」一枚未丢，破折号／分号／括号等句形随该面原样，未重排句子。五枚版本字面同步（两面 frontmatter、cue.py 内版本常量、回归样内断言两枚）。
- 边界：只补单位，不做换算——没写「几页几积分」「够跑多久」一类，也没有任何单价、费率或换算字样；三层分开自查、「不要贴进聊天」「花之前一定先问／发起前先报」等既有句逐字未动；历史版本条目里的旧写法不回改，改因只记在本条。
- 未动：判定逻辑、阈值、错误码集合、夹具、闸与脚本（除版本字面同步外）；本票不加判据也不放宽判据（新增 0／放宽 0）。
- 版本位：0.4.18 → 0.4.19（面文勘正＝patch）。旧值非 CHANGELOG 面残留 0；新条目无反引号、美元号与流水号。
### 0.4.18 — 2026-10-19（句柄判别补第二路：跑完仍被引用的活句柄，不靠析构也不靠警告）

- 病灶：0.4.17 的入口判别只看析构期的 ResourceWarning。产品读取路径若把句柄留在列表里（被检件真实读取路径的形制，不是测试里临时 open 一枚），它一直有引用、永不析构，既不发警告也不被 gc 逼出——入口于是 rc=0，而进程里确实有一只开着的文件。独立探针当场读到 retained=1／closed=False／fd 有值，证明确有活句柄。
- 改法（选补判据这条路，不写「无警告即无活句柄」那种话）：入口两路并查——跑完之后再取一次仍开着的文件对象（排除标准输入输出与跑之前就存在的那些），加上原有的析构期警告计数；任一路非 0 就点名逐枚输出并以非 0 退码收口。判定逻辑与用例数一字未改，12 枚用例同名同结论。
- 实测账：干净树两路各 0 枚、rc=0、Ran 12 tests／OK，连跑两次逐字节同（改前改后同一份合格样退码与末行同值）；两枚注入各自证在场（needle 命中 1、写后串命中 1）——测试内临时 open 那枚走析构路（UNCLOSED-HANDLE 1 枚）rc=1；产品读取器留引用那枚走活句柄路（LIVE-HANDLE 逐枚点名仍开着的文件与 fd）rc=1，改前同一注入是 rc=0。
- 面文同步：README 双语的「跑两遍逐字节可比」那段补明两路判别的实际形制与「无警告不等于无活句柄」这层关系。
- 版本位：0.4.17 → 0.4.18（判据覆盖面补严＝patch，理由同上：对外能力未变，自测能否抓到已声称要抓的那一类变了；minor 与否由 leader 判）。五枚字面同步（SKILL.md 与 SKILL.en.md 各一枚 frontmatter、cue.py 内版本常量一枚、回归样内断言两枚），旧值非 CHANGELOG 面残留 0；新条目无反引号、美元号与流水号。
### 0.4.17 — 2026-10-19（两处指路对表发布物：许可文本的位置、包外件点名不随发）

- 改的第一处：README 双语原写「代码及说明为 MIT（见包内 LICENSE）」，而随样态发布物里没有那枚文件——分发件的排除清单把许可文本与演示图一并排掉（本包发布物 17 条目内该件 0 枚，两态实测同值）。那句现改为如实：许可文本在本包的源仓库目录内，渠道发布物不随发。没有为凑这句话把分发件塞进包体；要动体积或排除白名单是另一件事，得先报。
- 改的第二处：README 双语指向同仓库相邻那枚知识包件的 ../cue-omni-ontology 相对路径，与 SKILL 双语「官方技能的调用契约以各自 SKILL.md 为准」那两处，指的都不是发布物里的东西——现各加一句「仓内相对路径／包外件，不随发布物交付」。指路本身保留，因为它是正确的去向；只是把「你在发布物里点不到它」这层说清。判据仍按现值走：调用契约以官方技能面为准、不硬编码工具名那句一字未改。
- 未动：核对三档与判定逻辑、四枚错误码族、退出码、夹具与自测用例；脚本内只同步了版本字面。本票不加判据也不放宽判据（新增 0／放宽 0）。
- 版本位：0.4.16 → 0.4.17（指路对表＝patch）。五枚字面同步（SKILL.md 与 SKILL.en.md 各一枚 frontmatter、cue.py 内版本常量一枚、回归样内断言两枚），单锁（无 manifest），旧值非 CHANGELOG 面残留 0；新条目无反引号、美元号与流水号。

### 0.4.16 — 2026-10-19（接入指路补齐：三枚技能按腿选装、命令两种写法、安装／凭据／连通三层分开自查）

- 病灶：README 双语「首次开通 Cue」那一格尾部留着把装法指向那三枚技能各自的说明文件，而那些文件不在本包内——用户照这一句在发布物里走不到下一步。现值另核一处：同一行里命令本身早已在场（单装写法 npx skills add sensedeal/cue-skills --skill cue-omni-reader 双语各有），所以本票补的是断掉的那半句与缺的分层自查，不是从零建命令；双语两面同形，差别只在措辞。
- 改法：尾部那半句换成「三枚都由 Cue 官方技能集合（sensedeal）发布，一条命令两种写法」——整套那一枚列出集合里公开的各枚按提示挑，单装那一枚把末尾的名字换掉即只装指定的一枚；并按腿写明主解析腿 cue-omni-reader、要列公告加 cue-data-mcp、要给「为何现在」补背景加 cue-research（≤1 次，可不做）。其后加一层三行分开自查：装好 skill ≠ 已配凭据 ≠ 通道已连，连通那行以匿名 GET https://cuecue.cn/api/mcp-catalog 的当场返回为准，域与工具按现值走。整套形制沿用仓内既定的那一套，只按包名与腿做最小改动。
- 未动：三步仍是三步、各节节号一字未动；「新账号注册送 500、每日 10，以服务端为准」「别贴进聊天／never paste it into chat」「发起前告知要解析几份并等同意、只转述服务端返回的计费事实、不估算单价」三处原句完整保留；判定逻辑、脚本、夹具、退出码、三档核对规则一字未改，本票不加判据也不放宽判据（新增 0／放宽 0）。
- 版本位：0.4.15 → 0.4.16（指路补齐＝patch）。五枚字面同步（SKILL.md／SKILL.en.md／cue.py 的 __version__／回归样内两枚断言字面），单锁（无 manifest），旧值非 CHANGELOG 面残留 0；新条目无反引号、美元号与流水号。

### 0.4.15 — 2026-10-19（覆盖面硬化：入口自带句柄判别，漏一枚就翻退码）

- 病灶：上一版（清噪声那枚）的验收写了两支测法，其中「普通跑 grep 计数」是恒真支——baseline 与注入永不关闭的句柄后都报 0 枚；另一支 -W error::ResourceWarning 在注入时才现 1 行，而 unittest 总退码仍为 0（警告落在析构处，只打成 Exception ignored）。结论：入口自己不能判别这格回归，判据挂在外面。
- 改法：把判别装进入口——跑完整套用例后在进程内收一次警告（record 模式，不改任何用例的判定），强制回收一次逼出析构期的那批，凡见未关闭句柄就逐枚打出 UNCLOSED-HANDLE 行、报明枚数并以非 0 退出；用例数、汇总行（Ran 12 tests／OK）与失败详情形制不变，QuietStream 剥耗时的处理保留。
- 反证成对（6.1 的 C1 原样复跑件，TMPDIR=/tmp）：baseline 普通跑 rc=0／警告行 0／Ran 12 tests／OK=True；注入 _leak = open(os.devnull, "r") 后**普通跑 rc=1**、ok=False（旧形制这里仍是 rc=0）；-W error 两态也各 rc=0／rc=1。两法都测后如实记：退码这支现在能判别了，普通跑 grep 那支按 6.1 的话从判据里撤下，验收只认入口退码与入口自报的枚数。
- 新增判据 1 枚（入口内句柄断言）、放宽判据 0 枚；cue.py 的判定逻辑与 12 枚用例一字未动。面文：README 双语自测块各加一句「入口自带句柄判别，不靠外部 -W、不靠恒真的 grep 计数」。
- 版本位：0.4.14 → 0.4.15（覆盖面硬化＝patch）。五枚字面同步（SKILL.md／SKILL.en.md／cue.py 的 __version__／回归样内两枚断言字面），单锁（无 manifest），旧值非 CHANGELOG 残留 0；新条目无反引号与美元号。

### 0.4.14 — 2026-10-19（清掉回归双跑的噪声源：开过的文件一律即时关闭）

- 病灶（双跑比对里 148 行 ResourceWarning 的根因）：cue.py 与回归样里多处 open() 不关——json.load(open(..))、open(..).read()、json.dump(obj, open(..))、urlopen(..).read()、fitz.open 的文档句柄、subprocess 之外的一路写句柄。判定与用例数一处没动，改的只是收口方式：该读的用 with 读完即用，该写的用 with 写完即关，PDF 文档 try/finally 关，urlopen 进 with；回归样内 14 枚同族落点一并收（新增四个小助手 wj/rj/rl/wt 承担开-用-关）。上一轮那 148 行读数里 146 行含临时路径或耗时，全是这一类的尾巴。
- 同族另一处：离线替身 scripts/fixtures/fake_omni_bridge.py 里读夹具与写调用日志两处开句未关，本枚一并收口（替身的响应形制与坏帧报错行为一字未动）。
- 汇总行的耗时：unittest 自带「Ran 12 tests in 1.397s」，同一份代码连跑必然不同——它与临时路径同族，是双跑比对的纯噪声。改法是给测试运行器套一层输出流，把该行里的耗时剥掉，结论行照原样出「Ran 12 tests」与「OK」；用例数、失败详情、退出码一律不变（不造假数字，也不归一化别的行）。
- 实测三件（TMPDIR=/tmp）：裸双跑（不做任何归一）diff **0 行**，末行仍 OK、汇总行仍 Ran 12 tests，连跑两次的退码同 0；ResourceWarning 两法都测——普通跑 grep 计数 **0**，python3 -W error::ResourceWarning 直跑 **rc=0**（末行 OK）；用例数与结论不变（Ran 12 tests／OK，12 枚同名）。
- 面文：README 双语的自检块各加一句「跑两遍逐字节可比：输出不带耗时行也不带临时路径，判定与用例数一字未改」。
- 版本字面同步：SKILL.md／SKILL.en.md 的 version、cue.py 的 __version__、回归样内两枚断言字面共五枚一并 0.4.13→0.4.14（沿用本包既有形制）。版本位：0.4.13 → 0.4.14（清噪声＝patch，判定能力不变）。本包单锁（无 manifest），旧值在非 CHANGELOG 面残留 0；新条目无反引号与美元号。

### 0.4.13 — 2026-10-17（修缺陷：回归替身 fake_omni_bridge 遇坏帧不再静默吞）

- 病灶：离线替身按 JSON-RPC 逐行读 stdin，旧代码一行 json.loads 不加判形。实测分两族：数组与字符串形（帧本身不是对象）走进「取不到 id 就 continue」那一路——零输出、零退码、一句不吭；数字／布尔／null 三形则在「'id' not in m」处抛 TypeError。两族都不是想要的：替身静默吞帧，回归就失去鉴别力（用例发错帧也会跑通）；抛 TypeError 则是把崩溃当出口。
- 改法：逐行先判能否解析、再判是不是对象，两种坏形各出一句点名行号与实收类型的可见错并退 1；顺带把「是对象却没有 method」也点出来（旧代码会 KeyError）。行号从 1 起计、空行跳过不计。合法通知帧（对象、无 id）仍不应答且不报错——那是 JSON-RPC 的正常形态，不是吞。
- 回归仍绿：scripts/test_skill_regression.py 改后连跑六次全 rc=0、自报「Ran 12 tests / OK」两跑同值——没有任何用例依赖这枚静默行为。（一格如实标注：这枚回归的**原始 stdout 双跑不逐字节同**，差异全部来自 148 行 ResourceWarning 里的临时目录名与耗时行——那是回归样与本包 cue.py 第 42 行开文件未关留下的既有形制，与本票无关，改前改后同态；把临时路径与耗时归一之后六跑逐字节同。），故未改用例、未迁就绿（票面要求先报的正是这一格，实测结论：无依赖）。它是包内替身不是用户面，故 README 与 SKILL 无需跟改；fixtures 一枚替身，不新增夹具。
- 版本字面同步：SKILL.md／SKILL.en.md 的 version、cue.py 的 __version__、回归样内两枚断言字面五枚一并 0.4.12→0.4.13（沿用本包既有形制，不同步回归样即判红）。
- 版本位：0.4.12 → 0.4.13（修缺陷＝patch，判定能力不变）。本包单锁（无 manifest），旧值在非 CHANGELOG 面残留 0。新条目无反引号与美元号。

### 0.4.12 — 2026-10-17（首页两句与 --fix 成功句同 ±1 口径；英文孪生面 description 译英）

- 口径对齐（只动文案，判定与 --fix 行为一字未改）：实码的判定一直是 abs(页 − 所注页) ≤ 1（scripts/cue.py 第 624 行，本轮未触碰），SKILL.md 第 75 行的定义句「所注页 ±1 逐字找到」也本就写对——打脸的是另外三句更强的说法。逐枚改：第 3 行 description 由「逐句核对答案引文是否逐字出自所注页」改「……出自所注页±1」；第 8 行 summary 同调（并把「核对引文是否出自」补成「逐字出自」，与实码一致）；scripts/cue.py 第 735 行 --fix 成功句由「引文现在都是所注页的原文」改「引文现在都能在所注页 ±1 内逐字命中」。相邻页命中会被判最高等级而不必 --fix，强句会让用户以为已校到精确页。README 双语第 17 行现值本就写「（±1 页）／(±1)」（先 grep 现值再决定，未跟改）；references/verification.md 第 13 行亦是 ±1 形。
- 英文孪生面：SKILL.en.md 的 description 与 summary 此前与中文面逐字同——英文入口挂着中文门面，冷启动读者拿不到触发面。本轮译英，Triggers 里的中文串（年报、引文核对）原样保留，那是中文用户的命中面；新句把 ±1 口径一并写进去，两面同调。两面 name／slug／version 一致。
- 长度帽（命门，取 check_skills.py 解析后的值）：中文面 description 改前 300／改后 299，summary 改前 60／改后 64；英文面 description 改前 300（中文串）／改后 290，summary 改前 60（中文串）／改后 77。帽为 description ≤300／summary ≤80，四枚全在帽内；中文面为塞进 ±1 而收掉三处冗字（「未开通 Cue 时」的「时」、「用本件流程」的「用」、触发串里「年报， 引文核对」的空格改顿号），触发词族与「不适合：投资与信贷建议」边界句逐枚仍在，现跑断言核过。
- 版本字面同步（沿用既有形制，不同步回归样即判红）：SKILL.md 与 SKILL.en.md 的 version、scripts/cue.py 的 __version__、scripts/test_skill_regression.py 内两枚断言字面，五枚一并 0.4.11→0.4.12。
- 未做（属功能改动，另票另裁）：6.1 提的「单列『邻页找到、页码待修』状态并令 --fix 真修」本轮一字未动——那要改判定与 --fix 行为，不在这张文案票里。
- 复验（取脚本自报行）：scripts/test_skill_regression.py 仓内与解包件两态均退码 0；仓级两门 rc=0；check_shipment 对本包发布物 rc=0。
- 版本位：0.4.11 → 0.4.12（口径与门面纠正＝patch，判定能力不变）。本包无 manifest，版本锁为 SKILL.md／SKILL.en.md 两枚面字面加码内一枚常量与回归样两枚断言；旧值在非 CHANGELOG 面残留 0。历史条目不回改。

### 0.4.11 — 2026-10-14（码内版本常量与回归样硬编码同步到面版本位）

- 同步四处五枚字面：`SKILL.md` 与 `SKILL.en.md` 的 version 0.4.10→0.4.11；`scripts/cue.py` 的 `__version__` 0.4.9→0.4.11；`scripts/test_skill_regression.py` 内两枚断言字面随之同步（回归样把 frontmatter 串与码内值双向对拍，不同步它便判红）。旧值在非 CHANGELOG 面残留 0 枚。
- 面内其余文字零改动：机检判据、通道形制与退出码都未动；此前码内常量落后两版，属真漂号，不是断言写错。
- 复验（取脚本自报行）：`python3 -B -m unittest discover -s scripts -p 'test_*.py'` 在仓内与解包件两态均退码 0，自报「Ran 12 tests」＋「OK」；成品面逐面现跑全「PASS 五禁零命中、指路可跟随」。
- 版本位：0.4.10 → 0.4.11（常量同步＝patch，无能力增减）。历史条目不回改。

### 0.4.10 — 2026-10-13（全仓文档卫生一轮：读者称谓统一「用户」＋中文标点全角化）

- **读者称谓口径**：成品面指称交付物接收方一律「用户」——原「给人读的镜像／可交人核／人来确认／拍板在人／决议权在人／人负终审／人只抽读」等口语表述全部改「用户」；「人工复核／人工审定／人工审」等与「机器」对举的标准词保留不动。
- **中文标点全角化**：半角逗号／分号／冒号／问号／感叹号／括号在邻接中文处统一为全角；代码围栏、行内代码、URL、时间戳、千分位数字、YAML `tags` 数组分隔符一律不碰；中文引述的直引号改「」。
- 能力句、机检词族、判定阈值、退出码、脚本零改动；复验 `python scripts/check_skills.py` 0 error 0 warning，公开面卫生门 ERROR 清零（另修 journal-draft 一处既存过程日期入墙）。
### 0.4.9 — 2026-10-12（对比演示图改文字说明：分发件里没有那张图，就不留包内相对路径）

- `README.md` 与 `README.en.md` 首段：原句把对比演示图写成本包 assets 目录下的一枚 png 路径，同时已声明渠道包不随发图片。渠道对图片是拒收面（两试两拒），分发件里那条路径必然空手，所以本轮**撤掉该路径字面**，改为「图在仓库内本包 assets 目录可看（GitHub 直接渲染），渠道包不随发图片，分发件内不含这张图」，并把图里数字的口径去处指向下文「交付与验证」段。图片本体未动，也不改打包排除面去让路径「通过」。
- 版本锁四处五枚字面同步 0.4.8→0.4.9：`SKILL.md` 与 `SKILL.en.md` 的 frontmatter、`scripts/cue.py` 的 `__version__`、`scripts/test_skill_regression.py` 内两枚断言字面——回归自测把 frontmatter 与码内版本对拍，锁没改齐它就不绿。
- 复验（取脚本自报行）：`python3 scripts/test_skill_regression.py` 自报「Ran 12 tests」＋「OK」，退码 0；成品面逐面现跑全「PASS 五禁零命中、指路可跟随」；本包面内那枚 png 路径字面现值 0 枚（脚本数）。
- 版本位：0.4.8 → 0.4.9（指路形制收口＝patch，无能力增减）。历史条目不回改。

### 0.4.8 — 2026-10-10（大结果取数句改成正条件句：按该 part 自己的存储形制分流，游标绑 part 与 offset）

- 凭据＝双 part artifact 实据（四条读数：①侧车可按游标分块读回，条件是该 part 被判 artifact，游标为 base64(JSON)＋签名、同时绑住 part 与 offset，改体改位一律 `INVALID_RESULT_CURSOR`（`retryable:false`、`billed:false`）；②`save_result` 只交 content，两种交付形制都交不出侧车；③`result_delivery_effective` 四种组合都不回显于 MCP 回执；④换 detail 只换侧车表示、正文一字节不动）。**本轮未复跑任何付费件**，字节数与跳数以那份账为准，成品面只写形制不写数。
- `SKILL.md`／`SKILL.en.md` 步骤 1 取数句：原「按游标从 Bridge 本地读回正文和页码 sidecar（不再计费）」改为按 part 分流——正文被判 artifact 才顺服务端逐跳发出的游标读回（读回实测未另计费，句形仍写「计费以返回为准」），`grounded` 的页码 sidecar 实测多为内联、直接从完成回执取；同段加「请求 artifact 不改变实际交付形制，`result_delivery_effective` 不回显——一律以回执内该 part 自己的 `storage.kind` 现值为准」；`save_result` 那句补「两种交付形制都只交正文一枚、侧车交不出，Bridge 的私有缓存不是公开出口、本件不依赖它」——**不写任何缓存旁路建议**。
- `README.md`／`README.en.md` 同段三处同步：命令表 `ingest` 行的「大结果…不再计费」改为「被判 artifact 的 part 按游标逐跳读回，计费以返回为准」；故障面 `INVALID_RESULT_CURSOR` 行的成因由「大结果存在 Bridge 本地」改为「游标绑死 part 与 offset，改体改位一律拒，无自造出口；过期另按 `expires_at` 判」；`page_basis=block` 行补「侧车内联时要当场整段存住」的因由。
- 代码一字未动：`cue.py` 的 `bundle_from_response` 本就按 `storage.kind` 逐 part 分流、artifact 侧逐跳读到 eof 并以 `parts.content.digest` 复算 sha256——那句文案是**写窄了（描述缺陷），不是功能缺陷**，真件凭证在账。
- 版本锁五处字面同锁 0.4.7 → 0.4.8：`SKILL.md`、`SKILL.en.md`、`cue.py` 的 __version__、回归样同一行的两处断言；改后这四面旧字面各复算＝0（CHANGELOG 历史条目里的 0.4.7 不回改，故口径写作「非 CHANGELOG 面残留 0」）。
- 复验（取脚本自报行）：件内回归面全绿；`check_skills.py --strict` 自报 17 skill(s), 0 error(s), 0 warning(s)，本包 OK v0.4.8；成品面逐面卫生闸 exit 0；旧句「按游标从 Bridge 本地读回正文和页码 sidecar」grep＝0 命中，条件句关键词（游标／以返回为准／`storage.kind`）在同段共现。

### 0.4.7 — 2026-10-10（公开面卫生：一处类别名用词改等长同义表述）

- 成品面 1 处改净（`SKILL.md` §红线）：「那一类判…」的类别名换为等长同义表述，禁面范围与判据一字未动；`SKILL.en.md` 为镜像同文，本轮无该词，未改。
- 版本锁五处字面同锁 0.4.6 → 0.4.7：`SKILL.md`、`SKILL.en.md`、主脚本里的 __version__ 字面、回归样里同一行的两处断言。**首拍只覆盖四处，同行第二处漏改，件内测试当即 red（AssertionError: '0.4.7' != '0.4.6'）**——补净后复跑全绿；这条自曝同时进交付回执。
- 复验（取脚本自报行）：件内回归面 12 passed；全包成品面逐面现跑全「PASS 五禁零命中、指路可跟随」；`check_skills.py --strict` 自报 15 skill(s), 0 error(s), 0 warning(s)。历史条目不回改。

### 0.4.6 — 2026-10-09（M177 阶段二·汲取形制包渠道面四项：①负向触发+②反幻觉两句（时点句+未检索到句））

- 落面：本件落了 ①负向触发+②反幻觉两句（时点句+未检索到句）。②的两句各归其位——**时点句进「怎么开口」节**（开口带时点、首行标「来源日期」、与所指日期不一致即禁「今日」「最新」改「截至 <日期>」），**未检索到句进「出错了怎么办」节**（参数／字段／枚举名未见于本次工具返回者不得凭印象填）；README 与 README.en 双语对点。
- ①description 尾嵌负向触发，条目全部取自本件既有边界现文（未新增反承诺）。
- 版本位：patch 位 0.4.6。除版本锁字面外 `scripts/` 零触碰；判定与阈值一律指回脚本现值，本文不作穷尽复述。

### 0.4.5 — 2026-10-09

Changed
- 供体回流重钉：渠道下载端点自 10-08 起持续供 0.4.3（服方字段分裂——tags 索引仍指 0.4.4；条目无上游同步源；服方对我方无上报渠道）。同号重发不可能（渠道拒绝 ≤ 现值版本号，0.4.4 版本位已消耗），故以内容等同 0.4.4 的字节发车重钉版本位；无功能变化，缘由如实入账。

### 0.4.4 — 2026-10-07

Changed
- 渠道分类修复：补 frontmatter `tags: [投研, 信用信号, 引文核对, 财报, A股, 美股]`（双语两份）——渠道页此前挂「未分类」，根因是本件全件无 tags 面（姊妹件皆有，子类映射由它驱动；渠道 API 现值对点：lead-pieces category=空 vs ontology=knowledge-management、earnings=pro-finance）。

### 0.4.3 — 2026-10-07

Changed
- 双语 README「常见问题与反模式」加一条互指：要把多份公告做成可更新的知识包、跟踪跨期变化和口径冲突，去同仓库 cue-omni-ontology（该件 0.3.0 的常见问题也指回本件做引文核对与线索稿）。只改文档和版本锁（frontmatter ×2、`cue.py`、测试钉），代码行为不变。
- 说明：下方两条 `### 0.4.2` 是同一版本的两次记录，原样保留，未改写。

### 0.4.2 — 2026-10-07

Changed
- 渠道首发适配（K-12 变体：服务端 400 拒 `assets/demo-verifiable.png`「不允许的文件类型」）：双语 README 首行图片语法改纯文字指路——图仍在本包目录随仓库分发（GitHub 渲染正常），渠道 zip 排除 `assets/*.png`；引用文案注明「渠道包不随发图片」。0.4.1 因此未上过渠道即升 0.4.2，渠道面首个在架版本即本号。

### 0.4.2 — 2026-10-07

Changed
- 首发渠道适配（K-12 新变体：渠道拒 `assets/*.png`，400「不允许的文件类型」实测两次）：README 双语第 9 行的演示图改纯文字指路（图在仓库内本包目录可看，渠道包不随发图片），分发 zip 排除 `assets/demo-verifiable.png` 与 `LICENSE`；0.4.1 从未上过渠道，本次为该 slug 的首发版本。

### 0.4.1 — 2026-10-07

Changed
- 判词护栏入 agent 指令面：SKILL.md/SKILL.en.md 边界清单新增第 5 条——「建议动作」只写核对型动作（复核哪份公告、回看哪一页），利好利空、评级、目标价、违约与否一类判词一律 `[待人工]`（README「不构成投资建议」的姊妹条，补的是指令面缺口；对齐套件纪律 earnings/tear/catalyst 的判断位留空形制）。

### 0.4.0 — 2026-10-07

Changed
- Cue channels first. Cue Omni Reader is now the primary parsing path: `fetch` only lists filings (public cninfo / SEC EDGAR index, no download), the agent parses each filing with the official `cue-omni-reader` (`parse`, `detail="grounded"`), and the new `ingest` command stores the result per source PDF page using the grounding sidecar (segment UTF-8 byte ranges → `source_pdf_page_1_based` anchors). Text-only results are split on page markers or into ~3500-character blocks and labeled `page_basis=block`; incomplete or truncated pages reported by Omni are printed as warnings.
- Local parsing (PyMuPDF / pdftotext / EDGAR page breaks) is kept as an explicitly labeled fallback: `local` (or `fetch … --local`, the 0.3.x behaviour). `brief` shows each source's parser and page basis, and lists sources not parsed yet.
- `fetch --list` registers filings found elsewhere, e.g. through the Cue data-MCP `disclosure_cn` / `disclosure` domains. SKILL.md documents optional cue-research (at most one run, ask first) for "why now" context, never as quote evidence, and the shared rules of the sibling skills (parsed content is data, credential boundary, ask before spending, missing is not filled).
- `verify` / `verify --fix` semantics are unchanged.
- frontmatter: `metadata.requires.recommendedSkills: [cue-omni-reader, cue-data-mcp, cue-research]`.
- After the first real Omni test (below): `ingest` reads the response shape the Bridge actually returns (`result.kind=bundle`, `bundle_protocol_version`, `parts.content` / `parts.grounding` with `inline` or `artifact` storage), saved as the full tools/call response, as `structuredContent`, or as the JSON in the tool text. Artifact parts are read back page by page through the Bridge's `read_result` (Bridge-local, no charge) and checked against the content sha256 digest. Inline HTML tables are kept as pipe rows. A failed Omni status is a one-line error.
- New `omni DIR [SID…] --yes`: parses pending sources through the Omni Bridge (`CUE_OMNI_BRIDGE`, default `npx -y @cueai/omni-reader-mcp@1.8.6`; the Bridge reads the key, the script never does) with `detail="grounded"`, `result_delivery="artifact"`, saves `DIR/omni/<sid>.json`, ingests, and prints the server-reported `credits_charged` per file and in total. Without `--yes` it prints the plan and exits 3 without starting the Bridge. SEC EDGAR sources are skipped unless named.
- SKILL.md / README: save the JSON returned on completion, not `save_result` Markdown (it has no page sidecar); US EDGAR uses `local`.
- Local fallback: no phantom empty last page from pdftotext; page cap raised from 300 to 1000 (the 391-page annual report below was cut at 300 before).

Verified
- Offline regression: 12 tests (Python 3.9, 3.12, 3.13), including a sanitized fixture with the real response shapes (synthetic text, fake ids): inline result saved three ways, artifact result read through a fake Bridge with cursor paging and a digest check, a failed status, and `omni` asking first and then parsing.
- Real Omni test, 2026-10-07, `@cueai/omni-reader-mcp` 1.8.3, `detail="grounded"`, cninfo PDF URLs of 600606 (Greenland Holdings). Charges as reported by Omni billing:

  | File | PDF pages | Omni pages | Charged | Storage |
  |---|---|---|---|---|
  | announcement 2026-10-01 （临 2026-052） | 3 | 3 | 0.201 credits | inline |
  | 2025 annual report | 391 | 391 | 26.197 credits | artifact (989,981 B content, 87,371 B grounding) |

  Every grounding anchor was `source_pdf_page_1_based`, `reliable`; `partial=false`, no incomplete or truncated pages. Against a local PyMuPDF parse of the same PDFs: the best-matching Omni page was the same page number for 3/3 and 391/391 pages; median share of local text found on the same Omni page 1.0 and 0.983 (the 7 annual-report pages below 0.8 are multi-column tables whose cell order differs, not missing text); 30/30 and 16,973/16,984 numeric tokens of the local parse appear on the same Omni page. Tables came back as GFM tables (14 rows on 2 pages; 5,896 rows on 277 pages) plus 3 inline HTML tables on one page; in the announcement's litigation tables two adjacent columns were merged into one cell (both numbers kept).
- Mini end-to-end on the Omni-ingested store: `brief` (cites both sources by PDF page), 8 quotes taken from the Omni pages → `verify`: 5 verbatim, 1 wrong page, 1 edited number, 1 too short → `verify --fix`: page corrected (p3 → p1), 2 dropped, 6/6 verbatim. Each kept quote was checked against the local PDF text: 5 on the cited page, 1 on the next page (accepted by the ±1 rule).
- `omni` end to end against live Omni (2026-10-07, user's launcher, Bridge 1.8.3): `omni DIR` without `--yes` printed the plan and exited 3; `omni DIR --yes` on the same 3-page announcement completed in about 30 s, charged 0.201 credits (as reported), ingested 3 PDF pages identical to the first run, and quotes verified on their pages. With `result_delivery="artifact"` this small result still came back inline (both parts), so for small results the page sidecar exists only in `structuredContent`.
- Ingesting the annual report from the 1.9 KB JSON an agent sees (artifact cursors) through Bridge 1.8.6 took about 5 s, no charge.

Not verified
- US EDGAR through Omni: the HYFM 8-K could not be parsed (EDGAR URL: `SOURCE_ACCESS_DENIED`; local file, grounded: `DETAIL_CAPABILITIES_UNAVAILABLE` in Bridge 1.8.3; local file, text: `MIME_MISMATCH` for the inline-XBRL .htm/.html); none of the three was billed. The text-block path was therefore not tested on real Omni output.
- The 24-company rates in references/verification.md are still from local parsing.

### 0.3.1 — 2026-10-07

Fixed
- `fetch` with an unknown A-share code, US ticker or CIK used to exit with a Python traceback ending in `StopIteration`. It now prints one line on stderr and exits with code 2, e.g. `cue.py: error: unknown US ticker 'ZZZZQX': not in the SEC EDGAR ticker list (use the ticker, e.g. LESL, or the numeric CIK)`. HTTP 4xx responses (except 429) are no longer retried.
- Regression test `test_unknown_code_one_line_error` covers all three cases offline.

### 0.3.0 — 2026-10-07 (first release in this repository)

Changed
- Fewer, fuller agent turns: `brief` returns the source catalog, lead pieces and paste-ready verbatim evidence in one call; `find` returns paste-ready sentences for several terms; `page` reads several sources and page ranges in one call (compacted, capped at 12 pages).
- `verify --json answer.json --fix` repairs the answer in place: wrong page → real page; edited quote (similarity ≥ 0.5) → the original sentence; table cells rewritten as a sentence → the original table rows (tries page p, p+1, then both); not in the source or numbers that differ → dropped. The draft is saved as `answer.before_fix.json`, and a warning is printed when a signal is left without evidence. Verdict levels are unchanged.
- Model alignment in `leads` is optional and provider-neutral (`CUE_LLM_BASE_URL` / `CUE_LLM_API_KEY` / `CUE_LLM_MODEL`, any OpenAI-compatible endpoint); without them a deterministic grouping is used. SEC contact via `CUE_SEC_UA`.
- Added the offline regression test `scripts/test_skill_regression.py` (frontmatter, verdict levels, `--fix`, `page` / `brief`).

Verified (measured; one host, one model; details in `references/verification.md`)
- 24 listed companies (12 A-share, 12 US, including 4 healthy controls), one run per company per arm, same question and filings. Bare agent: 61% of 421 quotes verbatim on the cited page, 39% not (95% interval 33%–46%). With the skill: 95% of 443 (91%–98%). Measured with the version before 0.3.0.
- 0.3.0 on the 14 previously slowest companies, run interleaved with the old version: final answers 100% of 279 quotes verbatim (agent draft before `--fix` 98%, 273/278); 60-minute timeouts 1 vs 4; median wall time 42.1 vs 45.4 minutes.
- Numbers that appear nowhere in the source: 0 in every arm above. Healthy controls: every claimed signal had source support (10/10 bare, 15/15 with the skill).
- Caveats: verbatim means found on the cited page ±1 ignoring whitespace and punctuation; it does not judge whether a signal is right. Sentences swapped in by `--fix` were not reviewed by a person. Five bare-agent quotes lost a "$digit" to shell expansion while the agent rewrote its answer file; counting them as matching still leaves 38% not matching. One model and one host only; results may differ elsewhere.
- Known issue: for a few companies the `brief` output exceeds the host's single-output limit and is saved to a file, costing the agent one more turn.
