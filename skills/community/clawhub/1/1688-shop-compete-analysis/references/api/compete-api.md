# 生意参谋「竞争」大 Tab 接口文档 & 竞店分析调用流程

> 站点：`https://sycm.1688.com/ms/compete/*`，所有接口均为 GET，同源 Cookie 鉴权，URL 末尾 `_` 为防缓存时间戳。指标类字段多为「指数」而非绝对值，返回结构常见 `{value, cycleCrc}`（cycleCrc = 环比变化率）。

> ⚠️ **经 AK 网关（`query_shop_data`，dataSource=SYCM）调用本文档接口的须知**：
> - `apiPath` 取接口地址 `/ms/` 之后、去 `.json` 的部分（如 `compete/competeShop/shopList`）。
> - **本文档所有入参示例已按网关要求标注为大写枚举**（dateType：`RECENT_1`/`RECENT_7`/`RECENT_30`/`MONTH`；device：`ALL`/`PC`/`WIRELESS`），**直接照抄即可、无需再转化**。网关对原站小写值（recent7/day/0）会**静默失败**（`success:true` + `data:null`，不报错）；仅当经浏览器直连 sycm 原站调用时，才需换回原站小写值。`dateRange` 照文档原样传。
> - 返回字段名被网关**汉化**（`memberId`→`会员ID`、`offerId`→`商品ID`、`ipvUvIndex`→`流量指数`、`seUvIndex`→`搜索指数`、`payOrdAmtIndex`→`交易指数`、`buyerIndex`→`买家指数`、`statDate`→`时间` 等），解析时以实际返回为准，本文档英文出参名仅供语义对照。
> - memberId 类参数用 `getShopMonitorInfo` 返回的字符串；`ipvUvSourceV2` 的 `offerId1` 必须是本店商品（否则返 1001「您无权查询该商品数据」）。
> - `getLossTopShopList`（客户流失榜）日粒度数据有延迟：查昨天返空数组 `[]` 时，用 `dateType=RECENT_1` + `periodsAgo=1` 回溯前一天即可取到；该接口不支持 RECENT_30 长窗口（返空）。
> - ⚠️ **三个流失类接口经网关只支持日粒度**：`getLossTopShopList`、`searchLossOffer/getOfferList`、`viewLossOffer/getOfferList` 传 `RECENT_7` / `RECENT_30` 均返 **`recordCount=0`（空壳，不报错）**，必须用 **`dateType=RECENT_1` + `dateRange` 单日 + `periodsAgo=1`**（回溯前一天）才有数据。**切勿因 recordCount=0 就判定“无流失数据”**。
> - 流失类接口返回 key 也被汉化且与文档英文名差异较大：`searchLossOffer` 为 `竞品平均搜索引导访客数` / `搜索竞争商品数` / `本店商品搜索引导访客数` / `本店商品搜索引导支付买家数`；`viewLossOffer` 为 `流失率` / `流失金额` / `流失人数`。
> - ⚠️ **`ipvUvSourceV2` 双列字段命名不对称**：竞品侧带 `first` 前缀（`firstOffer访客数`、`firstOffer支付金额`、`first下单买家数`、`firstInquiry指数值`），但**本店侧的访客数与支付金额无 `my` 前缀**，直接叫 `访客数` / `支付金额`（仅 `my下单买家数` / `myInquiry指数值` / `my有效询盘用户数` 带 my 前缀）。**按 `my*` 前缀扫字段会把本店访客/成交全读成空**，造成“本店无流量”误判；另外节点名为 `流量来源名称`（非 `outerName`）、层级为 `来源层级`、父节点为 `流量父来源ID`。
> - **网关接入状态**：本文档接口绝大多数已接入可用，但存在两类已知例外（2026-07 实测）：① `getCompeteShopCoreIndexTrend` 多种参数组合均 `data:null`；② `getOfferMonitorInfo` 返 null、`getOfferMonitorCntInfo` 可通但计数可能与监控池矛盾（报 0/100 而池内实有商品），竞品监控池的权威源用 `getCompeteList`。两个监控配额接口 `getShopMonitorCntInfo` / `getOfferMonitorCntInfo` 必须带 `cateId`（空参数返 null）。网关处于持续迭代中，**偶发整体降级**（多接口同时 `data:null`，含平时正常的 shopList/topItmList），遇 502 / `data:null` 时先按本页须知排查参数，排除后隔段时间复测一次再下结论，不要轻易判定接口不可用。

> ⚡ **优先用内置快捷命令，别从零拼接口**：竞店分析的 Step 0~1（类目树、本店定位、行业榜、流失榜、监控清单）、Step 4（店铺级四维下钻）与竞品级三维下钻已封装成四个 CLI 命令，详见下面「内置快捷命令」节；本文档后面的接口明细用于快捷命令未覆盖的维度与排错。

## 内置快捷命令（竞争分析优先用）

竞店/竞品分析的前置、初步取数与结构下钻已封装为 CLI 命令，**已内置处理大写枚举 / 汉化 key / 流失榜日粒度回溯 / 监控 gate / 脱敏 magic / 双列字段不对称六个坑，并并发调用**，比逐个调 `query_shop_data` 再自己解析快得多、也不会踩参数/字段坑。**竞争类需求优先走这些命令**（竞店/竞品链路：`compete_category` → `compete_shop_analysis` → `compete_shop_drill` → `compete_offer_drill`；买家流失归因：`customer_loss`），它们未覆盖的维度再用 `query_shop_data` 按本文档接口明细调。

### 1）`compete_category` — 竞争分析类目树

获取当前店铺被授权的类目树，并直接给出 cateId 取用建议。**竞争类分析的第一步，类目传错会导致后续接口全部静默返空**。

```bash
python3 {baseDir}/cli.py compete_category
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `--with_children` | 否 | 返回二/三级子类目（默认只返一级，输出更小） |

**输出关键字段**：
- `level1[]`：一级类目列表（`cateId` / `cateName` / `childCount`）
- `needUserChoice`：**`true` = 有多个一级类目，必须把类目名列出来反问用户选哪个**，不要默认拿第一个
- `suggested`：仅 1 个一级类目时直接给出 `{cateId, cateLevel}`，可直接用

### 2）`compete_shop_analysis` — 初步竞店分析

**一次调用完成竞店分析的取数与解析**（内部并发 5 个接口：本店信息 / 行业榜 / 流失榜 / 监控清单 / 监控配额），输出已摸平的结构化结果，**无需再写 Python 脚本、无需采样验证结构**。

```bash
python3 {baseDir}/cli.py compete_shop_analysis --cate_id 54
```

| 参数 | 缩写 | 必填 | 说明 |
|------|------|------|------|
| `--cate_id` | `-c` | 是 | 类目ID，**必须来自 `compete_category`** |
| `--cate_level` | `-l` | 否 | 类目层级，默认 1，需与 cate_id 同层级 |
| `--date_type` | `-d` | 否 | `RECENT_7`（默认）/ `RECENT_30`；dateRange 自动配套生成 |
| `--top` | `-t` | 否 | 行业榜/流失榜各取前 N 条，默认 10 |

**输出四块结构**（数值已从 `{value,cycleCrc}` 里提取好，直接用）：
- `myShop`：本店名称 / memberId / 身份 / 勋章
- `industryRank`：`myRank` 本店名次、`top[]` 行业榜（已标 `isMyShop` / `isMonitored`），**`focusCompetitor` 自动锁定的重点竞店**（榜单排名最高且已监控，可直接下钻不会触发 1001）
- `lossTop`：客户流失去向 TOP（自动处理日粒度延迟，回溯到有数据的那天，`dateRange`/`periodsAgo` 会回显）
- `monitor`：监控竞店数 / 剩余配额 / 已监控清单

### 3）`compete_shop_drill` — 竞店结构下钻

**一次调用完成竞店分析 Step 3~4 的核心指标对比与四维结构下钻**（内部并发 11 个接口：核心指标双列 / 热销商品双列 / 价格带 / 本店+竞店引流词榜 / 买家结构六维），输出已摸平的结构化对比结果，**无需再写 Python 脚本、无需采样验证结构**。

```bash
python3 {baseDir}/cli.py compete_shop_drill --member_id b2b-xxxx --cate_id 54
```

| 参数 | 缩写 | 必填 | 说明 |
|------|------|------|------|
| `--member_id` | `-m` | 是 | 目标竞店会员ID，**必须已在竞店监控清单内**（取自 `compete_shop_analysis` 的行业榜 `isMonitored=true` 行或 monitor 清单，否则网关返 1001） |
| `--cate_id` | `-c` | 是 | 类目ID，**必须来自 `compete_category`** |
| `--cate_level` | `-l` | 否 | 类目层级，默认 1，需与 cate_id 同层级 |
| `--date_type` | `-d` | 否 | `RECENT_7`（默认）/ `RECENT_30`；dateRange 自动配套生成 |
| `--top` | `-t` | 否 | 商品榜/词榜各取前 N 条，默认 10 |

**输出五块结构**（数值已提取、脱敏 magic 已归一为 null、标题汉化误替换已还原，直接用）：
- `coreIndex`：核心指标双列对比（流量/搜索/交易/买家四项 `{my, competitor, myLeadRate 本店领先幅度, myCrc/competitorCrc 环比}` + 全类目交易排名 + 上新数）；按会员ID定位双列、不假设顺序；网关降级时为 `null`（不影响其余四块）
- `topItems`：`myShop[]` / `competitor[]` 热销 TOP（offerId / 标题 / 价格区间 / 是否投广告 / 流量指数+环比 / 交易指数）
- `priceRange`：5 个价格带的 GMV 占比双列（`myRate` / `competitorRate`）
- `keywords`：双方词榜 TOP（`myTop` / `competitorTop`，含 `shared` 标记）+ **`behindWords` 候选买词清单**（双方都布局但本店流量落后，含差距）+ **`missingWords` 候选加标题清单**（仅竞店布局）+ 交差集计数（`bothCount` / `behindCount` / `missingCount` 等）
- `buyer`：六维买家结构双列对比（新老客 byr / 性别 sex / 城市 city / 身份 class_type / 采购等级 cgdj / 回头率 fgl，均为 `{name, myRate, competitorRate}`）

### 4）`compete_offer_drill` — 竞品（商品级）结构下钻

**一次调用完成竞品三维下钻**（内部并发：各商品引流词榜 / 流量来源渠道树双列 / 买家结构七维）。**商品可指定也可不传**：竞品侧必须在竞品监控池（`getCompeteList`）内（下钻 gate 只卡竞品）；**本店侧不受监控约束**，候选自动取自同款商品清单（`sameProductOffer`，即“有同款竞品可比对的自家商品池”）+ 监控池内本店商品合并去重——**竞品监控池里没有本店商品也能正常对比**。

```bash
# 全自动：取池内交易水平最高的竞品 + 自动匹配本店对位商品
python3 {baseDir}/cli.py compete_offer_drill --cate_id 54
# 指定竞品（本店侧仍自动匹配）
python3 {baseDir}/cli.py compete_offer_drill --cate_id 54 --offer_id <竞品商品ID>
# 三方对比 + 手动指定本店对位商品
python3 {baseDir}/cli.py compete_offer_drill -c 54 -o <竞品ID1> --offer_id2 <竞品ID2> --my_offer_id <本店商品ID>
```

| 参数 | 缩写 | 必填 | 说明 |
|------|------|------|------|
| `--cate_id` | `-c` | 是 | 类目ID，**必须来自 `compete_category`** |
| `--offer_id` | `-o` | 否 | 竞品商品ID（須在监控池内）；**不传则自动取池内交易水平最高的竞品** |
| `--offer_id2` | — | 否 | 第二个竞品商品ID（买家结构支持三方对比） |
| `--my_offer_id` | — | 否 | 本店对位商品ID（**不要求在监控池内**，任意本店商品均可）；**不传则自动匹配**（候选=同款商品清单+监控池内本店商品，按 同叶子类目 → 标题词重合 → 价位接近 三级降级） |
| `--cate_level` | `-l` | 否 | 类目层级，默认 1 |
| `--date_type` | `-d` | 否 | `RECENT_7`（默认）/ `RECENT_30` |
| `--top` | `-t` | 否 | 词榜取前 N 条，默认 10 |

**输出五块结构**：
- `pool`：监控池概况（总数 / 池内本店商品数 / 竞品数 / `myCandidateCount` 本店对位候选总数 / `quota` 监控配额——接口计数与监控池矛盾时为 null 不外显）+ `topRivals[]` 候选竞品（**用于反问用户要不要换其它竞品**）
- `offers`：本次对位的 `myOffer` / `rivals[]`（含标题、价格区间、叶子类目、各类指数）+ `autoPicked`（`matchBasis` 匹配依据、**`comparable` 仅同叶子类目才为 true**）
- `keywords`：`myTop` 本店词榜 + `byRival{offerId}` 逐竞品的词榜 / **`behindWords` 候选买词** / **`missingWords` 候选加标题** / 交差集计数
- `flowSource`：`{offerId: rows[]}` 渠道树拍平行，每行含本店/竞品的**真实访客数与支付金额**（非指数）、下单买家数、询盘
- `buyer`：七维买家结构（省份/城市/性别/身份/采购等级/访客场景/成交场景），每维 `rows[{name, myRate, rivalRates{offerId}}]`；**`exclusive=false` 的场景类维度累加可 >1，禁止当互斥占比归一化**

> ⚠️ **对位可比性提醒**：自动匹配时，若本店候选池内没有与竞品同叶子类目的商品（例如竞品是镜片、本店候选只有镜架），命令会返回 `comparable=false` 并在 markdown 里告警。此时应**向用户说明两个商品不同品类、建议换对位商品**（可用 `pool.topRivals` 列候选让用户选，或让用户直接给本店商品ID），不要直接拿跳品类的对比结果下结论。另：手传 `--my_offer_id` 且不在候选池内时照收，但**网关对非本店/不存在的商品不报错而是静默返空**，命令已内置全空校验（本店侧词榜与全渠道访客/支付均空则拒绝输出“本店全 0”的误导性对比并提示核对ID）。

### 5）`customer_loss` — 买家流失商品分析（裸调 + 发散佐证）

**把 `/item/customerLoss`（dataSource=ITEM）的「裸调全景 + 发散多品佐证」多次调用逻辑封装为一条命令**：① 默认裸调（不传 item_id）拿流失商品总数 + 50 条ID列表 + 随机一品的完整对比；② 自动从 ID 列表取样 N 个品**并发**带 item_id 再查（排除已对比的随机品）；③ 多品结果交叉汇总（价格对比 ±30% 可比性标记、竞对更便宜占比、回头率对比），items 按流失严重度降序（流失规模主键、流失宽度次键），双侧「商品的属性」原样透出供归口筛选。已内置处理：静默返空读 errorMsg、字段缺失一律 get、字符串型数字/价格转换、主图拼 CDN 前缀、单品失败不阻断整体。

```bash
# 默认：裸调 + 自动发散取样 5 个品并发佐证
python3 {baseDir}/cli.py customer_loss
# 指定下钻某几个流失商品
python3 {baseDir}/cli.py customer_loss --item_ids 1000050546670,1000450707425
# 调整发散取样品数（0 = 只裸调）
python3 {baseDir}/cli.py customer_loss --sample_n 5
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `--item_ids` | 否 | 指定下钻的流失商品ID，逗号分隔（本店商品、纯数字）；不传则自动从「流失商品ID列表」取样 |
| `--sample_n` | 否 | 发散取样品数（不含裸调随机命中品），默认 5，最大 20 |

**输出结构**：
- `overview`：`totalLossItems` 流失商品总数（全量值）/ `lossItemIdList` 前 50 条ID（按ID升序截断，非白名单）/ `randomPicked` 裸调随机命中的品
- `items[]`：**已按流失严重度降序**（主键浏览买家数、次键转单竞对数，无数据品沉底）；逐品记录（`source`=random/sampled/specified、`lossDetail` 流失信号、`myItem`/`rivalItem` 双方商品含 `attributes` 属性数组供同类归口筛选、`myShop`/`rivalShop` 双方店铺、`priceGap{gapPct, comparable}`）；无数据品 `hasData=false` + `errorMsg` 如实回显
- `summary`：交叉汇总事实统计（下钻品数 / 含竞对对比数 / 价格可比数 / 竞对更便宜数 / 本店更便宜数【**后三者仅计可比品，±30% 之外不混入**】 / 价差超±30%不可对标数 / 回头率双侧对比）

> 命令只做真实调用与事实汇总，**归因解读仍由 Agent 基于 items/summary 完成**：按本接口节末尾「归因分析建议」四步法执行（先归口再比价，先定性再定量）；单品劣势需有至少另一个品佐证才敢归因；`comparable=false` 的品不当同层竞品对标。

## 分析范围与前置约束（开工前必读）

### 1. 类目一定不能传错——传错就没数据

`cateId` / `cateLevel` 是所有竞争接口的生命线，**传错不会报错、只会静默返空**（`data:null` / `recordCount=0`），极易被误判为“接口不可用”或“本店无数据”。硬规则：

- **必须先调 `compete/industryCategory` 取类目树**，`cateId` 只能从返回的 `value` 里选，**禁止凭经验或从其它店铺抬类目ID**（类目树按店铺授权返回，别的店能用的类目本店可能无权）。
- **`cateId` 与 `cateLevel` 必须同层级配对**：一级类目配 `cateLevel=1`、三级配 `cateLevel=3`，**层级不匹配也是静默返空**。
- 用户未指定业务方向时的取值规则（按一级类目个数分流）：
    - **仅 1 个一级类目** → 直接取 `data[0]` + `cateLevel=1`，无需询问。
    - **有多个一级类目** → 🗣️ **先反问用户要分析哪个类目**（把各一级类目名称列出来让用户选），**不要自作主张默认拿第一个**——多类目店铺的经营重心未必是 `data[0]`，选错类目会得出完全无关的竞对结论；且竞争分析的竞店/竞品、行业榜均按类目隔离，跳类目数据不可比。用户明确“全部/都看看”时，才逐个一级类目分开分析并按类目分组展示。
    - 只有用户明确要看某细分类目时才下钻二/三级。
- 任何接口返空时，**第一个排查点就是类目是不是传错了**（其次才是 dateType 大写、日粒度、监控 gate）。

### 2. 默认先分析竞店，竞品分析反问确认（且受监控限制）

- **默认路径：先做竞店（店铺级）分析**——用户说“分析竞争对手 / 竞争分析 / 同行对比”等笼统说法时，按竞店闭环（行业榜 → 流失榜 → 核心指标对比 → 商品/价格带/引流词/买家结构）输出，**不要一上来就钻到商品级**。
- **竞店分析完成后，主动反问用户是否进一步分析竞品**（商品级），用户确认后再走 `getCompeteList` / `seachofferKey` / `ipvUvSourceV2` / 商品级 `shopBuyerAnalysis` 等下钻接口。
- ⚠️ **竞品分析的硬限制：只能分析已加入「竞品监控」的商品**。商品级接口受监控 gate 约束，未添加的 offerId 会返 `code=1001`。流程：
    1. 先调 `compete/common/getOfferMonitorInfo?cateId={cateId}` 拿已监控竞品清单（权威源）；
    2. 若清单为空或用户关心的商品不在清单里，**如实告知用户并引导到生意参谋后台添加**：<https://sycm.1688.com/ms/compete/shopOfferSetting?settingType=1>（竞品 tab），添加保存后再回来分析；
    3. 添加后有几秒生效延迟，**先重调一次监控清单确认已 in list 再下钻**；
    4. 配额满时（竞品 100）需先在同页面移除低价值监控项腾位。
- **禁止拿行业榜（`getItmRank`）或同款识别里的 offerId 直接当竞品下钻**——绕不过 gate；它们只能用于“发现待添加的候选竞品”，发现后仍需用户先添加到监控。

### 3. 默认分析当前登录店铺

- **只分析当前登录店铺**：竞争分析天然是"本店 vs 竞对"的双列对比，本店侧由网关登录态自动注入，无需传店铺 ID。
- 若要分析多个店铺，由 accio 侧配置多个商家授权、宿主 Agent 切换授权后分别调用本 skill，本 skill 内部不感知店铺列表。

### 4. 用户可见文案必须业务化（减少技术语言透出）

竞争分析全程面向用户的文案——**思考过程（Thought / 深度思考）、“正在执行”的命令描述、任务列表项**——必须用自然的业务化中文，**禁止暴露内部技术术语与实现细节**（同 SKILL.md 核心规则 16，本节是竞争域的具体化）。只说“正在做什么业务动作”，不说“用了哪个接口/参数/字段”。

常见替换对照：

| 禁止出现（内部术语） | 面向用户的说法 |
|---------------------|----------------|
| `compete_category` / `compete_shop_analysis` / `query_shop_data` / cli.py / 命令名 | “正在确认要分析的行业类目”“正在调取同行竞争数据” |
| cateId / cateLevel / 类目树 / `industryCategory` | “行业类目”（如“眼镜”“汽车用品”），不提 ID |
| memberId / offerId / loginId | “某家竞店”“某个竞品/商品”“某个店铺”，用店名/商品名代指 |
| dateType / RECENT_7 / RECENT_30 / periodsAgo / dateRange | “近 7 天”“近 30 天”“前一天”等自然时间说法 |
| 指数 / index / cycleCrc / syncCrc / 脱敏 magic | “流量水平”“成交水平”“环比变化”；指数是相对值，向用户说“相对高/低”“领先/落后多少”而非报原始指数值 |
| focusCompetitor / needUserChoice / isMonitored / 字段名 | “重点竞店”“需要您选一个类目”“已加入监控”，不报字段名 |
| 监控 gate / code=1001 / data:null / recordCount=0 | “该竞店/竞品还没加入监控，需要先添加”“这个时段暂无数据”，不报错码 |
| getLossTopShopList / inputShopKey / ipvUvSourceV2 / topItmList 等接口路径 | 用中文业务名：“客户流失去向”“引流搜索词”“流量来源对比”“竞店热销商品” |
| 大写枚举 / 汉化 key / JSON 解析 / 并发 / 落盘 / Python 脚本 | 不外露，只说“正在整理数据”“正在汇总对比” |

**业务化叙述示例**（竞争分析各阶段）：
- ❌“调用 compete_category 拿到 cateId=122916002，发现 needUserChoice=true” → ✅“您店铺涵盖汽车用品、个护家清、宠物园艺三个行业，先确认一下您想分析哪个”
- ❌“shopList 返回本店 payOrdAmtIndex 排名第 2，focusCompetitor 为某 memberId” → ✅“您在该行业成交排第 2，最直接的对手是‘××商行’”
- ❌“getLossTopShopList 用 RECENT_1+periodsAgo=1 回溯到 07-26” → ✅“正在看您的客户最近流失到了哪些同行”
- ❌“该词本店 流量指数 8000 < 竞店 12000” → ✅“‘××’这个词您的流量明显输给对手，建议重点投入”

补充：深度思考 / Thought 一律用中文；内部文件名（如 `compete-api.md`）、接口路径、参数名不得出现在用户可见文本里；数据本身仍必须真实，只是描述“怎么取、怎么算”的过程不外露技术细节。

---

## 竞店分析总体思路（推荐调用顺序）

### 意图分流（先判意图，再决定跑多少）

四个快捷命令齐备后，按用户意图明确程度分流，**笼统提问不要逐步反问、直接连跑出全景数据**：

| 用户意图 | 执行链路 | 说明 |
|---------|---------|------|
| **笼统竞争分析**（“分析竞对/竞争分析/同行对比”，未指定店/品/维度） | `compete_category` →（仅多一级类目时反问）→ `compete_shop_analysis` → `compete_shop_drill -m <focusCompetitor>` **三连跑完再统一输出** | 全只读、无需中途确认；一次性给出行业格局 + 流失去向 + 与重点竞店的五块对比；`focusCompetitor` 为空（无已监控竞店）时降级为只出前两步结果并引导添加监控；**竞品（商品级）仍保持反问后再跑**，不纳入默认链 |
| **指定竞店**（“对比 XX 店”） | `compete_category` → `compete_shop_analysis`（取 memberId 与监控态）→ `compete_shop_drill -m <指定店>` | 目标店未监控时如实告知并引导添加，不硬打 |
| **竞品/商品级意图**（“分析竞品/商品对比/下钻商品”） | `compete_category` → `compete_offer_drill`（未指定商品全自动） | 可比性告警时先向用户说明再下结论 |
| **单维度意图**（只看引流词/价格带/买家画像/流失） | 跑对应命令但**只展示对应数据块**；快捷命令未覆盖的维度（如搜索/访问流失商品、群体对比）按本文档接口明细单调 | 不把无关维度塞给用户 |
| **买家流失商品级归因**（“哪些商品的买家被同行抢走 / 买家看了我的没买去别家下单 / 流失商品与竞对商品对比”） | ⚡ 直接跑 `cli.py customer_loss`（已封装「裸调全景 + 发散多品佐证 + 交叉汇总」，详见「内置快捷命令」第 5 节）：默认不传商品，自动从流失商品ID列表取样 5 个品并发佐证；用户指定商品时用 `--item_ids` | 与上行“竞店流失去向”（getLossTopShopList，**店铺维度**）不同：这个是**商品维度**、直接给到具体竞对商品的逐字段对比，是“为什么被抢走”归因主接口。命令未覆盖的场景（如只查单个指定品、评价原文）再按「商品-买家流失商品识别与竞对对比」节手动调 `/item/customerLoss`（dataSource=ITEM） |
| **配置类**（加/换监控） | 引导到生意参谋「竞店竞品配置」页 | 接口无写能力 |

> 默认链跑完后的输出仍遵守 SKILL.md 默认路径：**只报数据不做解读**，数据表格完整输出后再用深度分析卡片询问；用户选择深度分析时再读竞品分析规范文件做解读。

竞店分析的目标是回答四个问题：**「谁是我的竞店？」→「它跟我差多少？」→「它靠什么在赢？」→「我该怎么打？」**。按下面 6 步串起来即可完成一次完整的竞店分析闭环，每一步都指向本文件后续小节的具体接口。

> **注意：以下流程仅作为默认推荐路径**。如果用户已经带着明确的分析思路来（例如"只看竞店买家画像"、"只对比某价格带"、"直接拉一份竞店 TOP 引流词"等），**优先按用户的思路走，不必强行套用完整 6 步**——从对应 Step 里挑需要的接口调用即可，或用「一分钟极简版」灵活裁剪。标准流程只是新手/无思路时的兜底参考。

### Step 0 — 前置：确定分析类目（cateId / cateLevel）

> ⚡ **快捷方式**：直接跑 `cli.py compete_category`，一步拿到 `level1[]` / `needUserChoice` / `suggested`，无需手动解析类目树。
>
> 🔥 **本步不可跳过**：类目传错会让后续所有接口静默返空（不报错），是竞争分析最常见的"无数据"根因，详见本文「分析范围与前置约束」第 1 条。

- 先调 **`/compete/industryCategory.json`** 拿到当前店铺可选类目树，后续所有接口的 `cateId`/`cateLevel` 都必须来自这里且**层级配对**。未明确业务方向时：**只有 1 个一级类目就直接用它**（`cateLevel=1`）；**有多个一级类目则先把类目名列出来反问用户选哪个**，不要默认拿第一个。
- 附带调 **`/compete/competeShop/getMyShopInfo.json`** 拿本店 memberId / 交易勋章，作为对比左侧列的固定标识。

### Step 1 — 找竞店：发现候选池

> ⚡ **快捷方式**：`cli.py compete_shop_analysis --cate_id <cateId>` 已一次并发完成本 Step 的行业榜 + 流失榜 + 监控清单，并直接给出 `focusCompetitor`（排名最高且已监控的竞店，可直接进 Step 3~4 下钻）。仅当需要下面单独的同款/流失商品视角时，才再另调对应接口。

不同视角发现竞店，取并集作为候选：

- **行业头部对标**：`/compete/competeShop/shopList.json` —— 按类目排出行业 TOP 店铺（默认约 50 条），含本店（`isMyShop=y`）与所有竞店，可按访客/搜索/成交/买家/排名多口径切换。
- **流失去向识别**：`/compete/shopDiscern/lossShop/getLossTopShopList.json`（`dateType=RECENT_1` 日粒度） —— 本店客户流失去哪些店，按 `lossIndex` 降序；配合 `.../plot.json` 做流失散点图。
- **同款商品筛选**：`/compete/offerDiscern/sameProductOffer/getOfferList.json` —— **本店哪些商品在类目下有可识别的同款竞品**（本店商品清单+本店该商品自身指数，非竞品清单）；作为"要不要给这个本店 offer 做同款竞品分析"的入口选品，下一步再走同款竞品明细接口拿具体竞品。
- **已监控清单**：`/compete/common/getShopMonitorInfo.json` —— 拿历史加入监控的竞店（含 `isDelete` 状态），与新发现候选合并去重。

**输出**：一份候选竞店 memberId 列表，可先按 `shopList.payOrdAmtIndex` 或 `lossIndex` 排序，圈定 TOP 3~5 家重点竞店。

> **候选竞店/竞品不在监控清单里怎么办**：`shopBuyerAnalysis` / `getCompeteList` / 商品级 `ipvUvSourceV2` 等下钻接口都受"监控 gate"约束——目标 memberId/offerId 不在本店监控清单时会直接返 `code=1001`（"店铺不在您的监控列表中"）。
>
> **标准操作**：先用 `common/getShopMonitorInfo.json?cateId={cateId}` 查权威已监控竞店清单、`common/getOfferMonitorCntInfo.json?cateId={cateId}` 查已监控竞品清单；若目标不在里面，**引导用户到 <https://sycm.1688.com/ms/compete/shopOfferSetting?settingType=0> 「竞店竞品配置」页手动添加**（竞店 tab 加 memberId、竞品 tab 加 offerId），添加保存后回到本流程，从**已监控清单**里挑店/挑品继续 Step 3~4；不要绕过监控直接用 shopList 榜单里的 memberId 硬打——绕不过 gate。
>
> 若已监控配额已满（竞店 50/50、竞品 100/100），需要先在配置页移除低价值监控项腾位再加新的。

### Step 2 — 锁定重点竞店：拿店铺基本盘

对每个候选 memberId：

- `/compete/common/getMShopInfo.json` —— 店名、店铺URL、交易勋章、身份（svip / 精铺 / 中国制造 / 超级工厂）
- `/compete/shopDiscern/lossShop/getLoss.json` + `.../getLossTrend.json` —— 单店流失指数当期值 + 近 30 天趋势
- 交叉 `getShopMonitorCntInfo` 剩余监控配额，决定是否加入监控

**输出**：3~5 家重点竞店的画像卡（身份 + 流失强度 + 是否已监控），供下一步双选。

### Step 3 — 双选对标：核心指标对比

> ⚡ **快捷方式**：核心指标对比已并入 `cli.py compete_shop_drill`（输出的 `coreIndex` 块），无需单独调接口。

选定 1~2 家重点竞店，做双列/三列对比：

- **核心指标**：`/compete/competeShop/getCompeteShopCoreIndex.json` —— 传 `memberId1`（必）、`memberId2`（可选），并列返回本店与竞店的访客指数、搜索访客指数、支付金额指数、买家指数、类目排名、新品数、环比。**经网关返回为并列数组结构**（每个汉化 key 对应一个 `[本店值, 竞店值]` 数组，用 `会员ID` 数组定位哪列是本店，勿假设顺序）。
- **趋势对比**：`/compete/competeShop/getCompeteShopCoreIndexTrend.json` —— 近30天逐日趋势。⚠️ **经网关实测暂不可用**（RECENT_7/RECENT_30、含/不含 dateRange、memberId/memberId1 等 6 种参数组合均 `data:null`，2026-07 实测），需趋势时先隔段时间复测，不可用则如实告知用户。
- **看是否在打广告**：`/compete/competeShop/topItmList.json`（`tabFlag=payOrdAmtIndex`）返回的商品行有 `isAdServing=Y/N`，可判断竞店有无广告驱动。

**判断**：竞店是「体量压制」（各项指数领先） / 「成长压制」（环比+++） / 「新品/广告拉动」（新品数、广告占比高）中的哪一种。

### Step 4 — 结构下钻：竞店靠什么在赢？

> ⚡ **快捷方式**：`cli.py compete_shop_drill --member_id <已监控竞店> --cate_id <cateId>` 已一次并发完成本 Step 的 a/b/c 三个维度（热销商品+价格带+双方引流词对比+买家结构六维）并直接给出买词/加标题候选清单；仅 d）商品级流量来源仍需单独调接口。

按四个子维度下钻，每一步都会告诉你竞店的一个"打法密码"：

**a) 商品结构**
- `/compete/competeShop/topItmList.json`（`tabFlag` 切换热销/热访/新品） —— 竞店 TOP 商品，看爆款是什么、价格档、有没有广告投放（`isAdServing=Y/N`）。**参数名是 `memberId1` 不是 `memberId`**：传 `memberId=xxx` 会被后端忽略，返回体里只有 `data.myshop`（本店 TOP）而没有 `data.firstShop`（竞店 TOP），容易被误判为「竞店无商品」。正确调用会同时返 `myshop` + `firstShop` 双列。
- `/compete/competeShop/tradeAmountRange.json` —— 本店 vs 竞店的成交价格带 GMV 占比分布，看竞店赢在哪个价格带。**注意价格档颗粒度只到 `>12` 元一档**（`0-2 / 2-3 / 3-6 / 6-12 / >12`），无法区分中高端价位差异；要看 65-98 元这种"中高端 vs 低端"结构差异，得回到 `topItmList` 的 `item.minPrice/maxPrice` 分布做判断。

**b) 搜索引流词**
- `/compete/competeShop/inputShopKey.json` —— 单店 TOP 引流搜索词榜。**同一接口既能拉竞店词榜也能拉本店词榜**：传竞店 memberId 得竞店词、传本店 memberId 得本店词，字段结构一致。做词对比时不需要另调 `getMyShopWords.json`，直接两次 `inputShopKey`（分别传竞店和本店 memberId）就够了——本店抢占的高流量词里，竞店未布局的即为「机会词」，双方都布局的即为「防守/攻坚词」。
- 单品下钻：拿到关键竞品 offerId 后可用 `/compete/competeOffer/seachofferKey.json` 看该竞品的 TOP 引流词榜。**`flowSourceType` 是"指标排序 tab"切换（1=流量指数/2=搜索指数/3=交易指数 desc）而非渠道过滤器**——同一 offer 换 tab = 同一 keyword 池换排序（FT1/FT2 词集一致，FT3 会过滤 payOrdAmt 脱敏 magic）。

> 💡 **引流词对比后的行动建议（输出解读时需给到，别只报词表）**：把本店词榜与竞店词榜做差集/交集后，按两类分别给出不同动作：
>
> | 词的情形 | 判定依据 | 给商家的行动建议 |
> |---------|---------|------------------|
> | **本店已布局、但流量指数输竞对** | 该词在双方词榜里都有，但本店 `流量指数` < 竞店 | **引导到数字营销买该词**——自然排名已落后，靠付费推广快速抢回该词的流量位；可按差距大小排优先级（差距大且竞店交易指数高的词优先买） |
> | **本店完全未布局** | 该词只出现在竞店词榜，本店词榜无此词 | **建议把该词加入合适商品的标题**——先解决“没有入口”的问题；选品时要挑**与该词语义相关的本店商品**（可结合 `sameProductOffer` / `topItmList` 看本店有哪些对应品），不要无关堆词 |
>
> 输出时建议直接列出【建议买词】与【建议加标题】两份词单（各带流量指数与差距），而不是只给一张对比表。注意：指数是相对值，只用于同期同类目内比较；命中脱敏 magic（如 `交易指数 ≈ 0.9527...`）的词不要参与排序与差距计算。

**c) 买家结构**
- 店铺级：`/compete/competeShop/shopBuyerAnalysis.json` —— 一次一个 `scenceName`，把 `byr`(新老客) / `sex`(性别) / `city`(城市 TOP10) / `class_type`(11 类身份人群) / `cgdj`(采购等级 L0~L6) / `fgl`(回头率) 逐个拉一遍，得到一张本店 vs 竞店的六维买家画像对比表。
- 商品级（拿到关键竞品 offerId 后下钻）：`/compete/competeOffer/shopBuyerAnalysis.json` —— 姊妹接口，入参从 memberId 换成 offerId1/2/3，可用维度 7 个：`provice`（省份，页面拼错、原样接受）/`city`/`sex`/`class_type`/`cgdj` 五个静态画像 + `scence_uv`（场景来源访客）/`scence_trd`（场景来源成交）两个动态场景画像；商品级**不支持** `byr`/`fgl`。
- 判断：竞店买家池是**更下沉**（低采购等级 L0/L1 占比高）、**更专业**（专业身份+高等级）、**还是更粘性**（回头率 fgl 明显高于本店）；到商品级再看**场景来源**（旺铺/搜索/进货单/买家订单/1688首页推荐/…）是竞品的主入口还是本店的短板。

**d) 流量来源（若已锁定关键竞品）**
- `/compete/competeOffer/ipvUvSourceV2.json` —— 双列对比本店商品与竞品在市场/搜索/推荐等各渠道的访客/成交/询盘，看竞品是靠**免费搜索**还是**推荐/广告**起量。**`flowSourceType` 是空转参数**（0/1/2/3/4 五个值返回完全相同的字段级数据，仅前端 tab 高亮次序不同）——识别节点务必用 `outerName`（稳定），不要用 `outerId`（会因 flowSourceType 而变）。

### Step 5 — 输出行动 & 持续监控

> 🗣️ **竞店分析输出后，主动反问用户是否要继续分析竞品（商品级）**；用户确认后直接跑 `cli.py compete_offer_drill --cate_id <cateId>`（商品不传就自动从监控池选，已内置 gate 校验与友好报错），无需再手工拉监控清单——详见「分析范围与前置约束」第 2 条。

- 把 Step 3~4 得到的差距点归纳成 **1 页对比页**（体量差、价格带差、搜索词差、买家结构差、流量渠道差）。
- 通过 `/compete/common/getShopMonitorCntInfo.json`（竞店配额，一般 50/50）与 `/compete/common/getOfferMonitorCntInfo.json`（竞品配额，一般 100/100）检查监控配额与已监控清单，把重点竞店/竞品加入监控，后续用「竞店监控 / 竞品监控」定时拉；权威已监控清单看 `getShopMonitorInfo.json`（返 memberId 全量+isDelete 状态）和 `getOfferMonitorInfo.json`（返 offerId 全量）。
- 竞争群体视角复盘：`/compete/getShopAndGroupIndex(E).json` + `.../Trend(E).json` 看本店 vs 相似优秀店铺 TOP10（`competeGroupID=similar`）/ 访客偏爱店铺 TOP10（`prefer`），从群体层面校准是「行业整体涨」还是「只有我掉队」。

### 一分钟极简版

`industryCategory` → `shopList` / `getLossTopShopList` 找竞店 → 选 1~2 家 → `getCompeteShopCoreIndex(Trend)` 看差距 → `topItmList` + `tradeAmountRange` 看商品/价格 → `inputShopKey` 看搜索词 → `shopBuyerAnalysis` 六维扫买家画像 → `getShopAndGroupIndex` 群体校准 → 加监控。

### 通用调用注意

- `cateId` 与 `cateLevel` **必须成对同层级**，来源仅 `industryCategory.json`；未明确时默认一级根节点。
- 指数字段 `{value, cycleCrc}`：`cycleCrc` 是环比变化率（0.05 = +5%）；**唯一例外**：`shopList.cateRank.cycleCqc` 是「变化数」（-7 = 排名前进 7 名）。
- `statDate` 有 3 种风格：`{value:"YYYY-MM-DD"}`（shopList）、`{value:1785...}` 毫秒时间戳（多数）、`直接数值` 无包装（shopBuyerAnalysis）—— 跨接口拼装数据时必须做类型判断。
- `payOrdAmtIndex/buyerIndex` 的 `cycleCrc=-1.0` 表示上期 0 本期非 0（伪 -100%），`null` 表示双期均 0 或缺失，展示时都要改文案为「-」或「新增」。
- **上游数据两个已知口径怪癖（多账号实测，非解析错误，勿当 bug 排查）**：① `getShopMonitorCntInfo.alreadyMonitorCnt` **包含 `isDelete=y` 的已删除监控项**，会比有效监控数偏大；有效数应以 `getShopMonitorInfo` 过滤 `isDelete!=y` 后的条数为准。② `shopBuyerAnalysis` 的新老客（byr）占比合计可能略大于 1（实测 101%～102%），属上游口径/舍入问题，展示时照原值输出即可，不要强行归一化、也不要据此判定数据异常。
- **指数字段脱敏 magic number**：当真实指数太小或样本不足以脱敏公开时，后端**不返 0** 而是回一个**固定占位常量**（避免被反推真实值）。常见 magic：`payOrdAmtIndex.value ≈ 0.9527275047730654`、`seUvIndex.value ≈ 10421.327687806566`、`ipvUvIndex.value ≈ 0.9527275047730654`（多个指标复用同一 magic）。等值判定即视为「近似 0 / 不可用」，**不要参与除法/比率/环比/排序**（否则脱敏行会被错误抬前）。适用于所有 `/ms/compete/*` 指数化字段（ipvUvIndex/seUvIndex/payOrdAmtIndex/buyerIndex 等），出现在 seachofferKey/getCompeteList/getItmRank 等**只要有 index 字段**的接口里都要防。
- 群体侧接口有 `E` 后缀变体（如 `getShopAndGroupIndexE.json`），近 7 天用无后缀、近 30 天切 `E` 后缀，结构一致。
- **双列/三列对比接口的入参名统一是 `memberId1` / `memberId2` / `memberId3`（或 `offerId1/2/3`）而不是 `memberId` / `offerId`**——本文档凡返回 `data.myshop` + `data.firstShop`（+ `data.secondShop`）双/三列结构的接口（如 `topItmList` / `getCompeteShopCoreIndex(Trend)` / `competeOffer/shopBuyerAnalysis` 等）都遵循这个命名。传错成不带数字的 `memberId=xxx` 会被后端**默默忽略**，返回体里只有 `data.myshop`（本店那侧）而没有 `data.firstShop`（竞店/竞品那侧），容易被误判为「竞店无数据」。做对比时务必把重点竞店/竞品放到 `memberId1`/`offerId1`，选填的对比方放到 `memberId2/3`（不需要时传字符串 `"null"` 而非空串 `""`，空串在部分接口会引发 1001）。
- **同一接口既能拉竞店维度也能拉本店维度**：`inputShopKey.json` / `shopBuyerAnalysis.json` 这类"单店 memberId 视角"接口，传竞店 memberId 得竞店数据，传本店 memberId 得本店数据，字段结构一致。做对比时不必另找"本店专用接口"（如已下线或超时的 `getMyShopWords.json`），直接两次调用（分别传竞店和本店 memberId）就够了；避免绕行找不到的姊妹接口浪费时间。
- **浏览器控制台/自动化脚本回放接口的常见坑**：
    - **同步/异步返回值捕获**：`javascript_tool` 类工具通常只捕获**单表达式返回值**，多语句脚本会返 undefined。正确姿势：`fetch(url,{credentials:'include'}).then(r=>r.json()).then(j=>{window.__x=j; window.__xdone=1})` 存到 `window` 全局，下一次调用**单独用一个表达式** `window.__xdone` 轮询完成态，再第三次 `window.__x` 读结果——三步分开调用而不是链式。
    - **同源 Cookie 鉴权**：`/ms/compete/*` 全部走同源 Cookie 鉴权，在 sycm 页面内 fetch 必须加 `{credentials:'include'}` 否则会 302 到登录页并返 HTML；跨 tab 复用时先 `tabs_context` 确认落在 `sycm.1688.com/*` 之下。
    - **`read_network_requests` 只返 URL/method/状态，没有真实 response body**——想拿完整出参必须在页面内 `fetch(url,{credentials:'include'}).then(r=>r.json())` 回放；导航前先 `clear` 请求队列避免拿到过期缓存。
    - **SPA `get_page_text` 只返回页脚版权**（竞争 tab 是 SPA），页面数据须靠 `computer screenshot` / DOM 直读 / 接口 fetch 三选一——别用文本抓取判断"页面是否有数据"。

### 访问权限前提

- **`/ms/compete/*` 全量接口仅对 1688 生意参谋 SVIP 用户开放**。未订阅 SVIP 的账号访问任一竞争接口都会被后端直接拒绝（无数据返回或返回权限提示），此时无论怎么调整参数都取不到数据。**排查顺序**：先确认当前登录账号是否为 SVIP（可从 `/compete/competeShop/getMyShopInfo.json` 返回的 `identity` 字段判断，`svip` 才有竞争 tab 权限）；不是 SVIP 时先引导用户升级订阅，再谈参数与错误处理。

### 常见错误提示与自愈动作

- **返回「抱歉，您无权限查看该类目的信息」** —— 代表所传的 `cateId` / `cateLevel` 不在当前登录店铺的授权类目范围内（可能层级不匹配、也可能选错类目节点）。**自愈动作**：重新调 `/compete/industryCategory.json`，从返回的类目树里挑一个当前店铺授权的节点，重新配对 `cateId` + `cateLevel`（层级必须一致）后再请求；未指定业务方向时直接取 `data[0]` 一级类目（`cateLevel=1`）兜底。
- **返回「查询失败，查询店铺不在您的监控列表中」（code=1001）** —— 语义上是"目标 memberId/offerId 不在本店监控清单"，但**不能直接假设是监控被清或 memberId 错**。正确诊断顺序：
    1. **先调 `common/getShopMonitorInfo.json?cateId={cateId}` 拿权威监控清单**（单参数即可，多传字段反而会 1003，见下条）。查看目标 memberId 是否 `in list`。
    2. **若 `in list` 但 shopBuyerAnalysis 仍 1001** → 极大概率是**会话瞬时态**（tab 处于 login 跨域重定向 / cookie 刚被 refresh / 参数组合不合法如 memberId2 传空串 `""` 而非字符串 `"null"`）。解法：先在浏览器 tab 内导航到一个稳定 sycm 页（如 `/ms/home/home`）刷新会话，再复打；同参数往往就通了。**这类 1001 不代表 memberId 是错的，前面同参数复打常常一次成功一次不成功。**
    3. **若 `not in list`** → 才是真的需要到 <https://sycm.1688.com/ms/compete/shopOfferSetting?settingType=0> 「竞店竞品配置」页把目标 memberId/offerId 加入监控（竞店和竞品在页面里是两个独立 tab，`settingType=0` 是竞店 tab，`settingType=1` 是竞品 tab）。**添加保存后不要立即用刚加的 memberId 打接口**，先重新调 `getShopMonitorInfo.json` 确认新 memberId 已 in list（后端有几秒生效延迟），再回到 Step 3~4 从已监控清单继续分析。若监控配额已满（竞店 50/50 或竞品 100/100），需要在同一页面先移除低价值项腾位。
    4. **切勿把"从 competeShop/shopList.json 榜单里挑的 memberId"或"从 competeOffer/getCompeteList.json 里取的 shop.memberId"当作"已监控竞店"来用** —— 前者是行业全量榜单（要用 `isMonitor===true` 过滤才是本店监控的），后者的 `shop.memberId` 是"已监控**竞品**"的所属店铺，跟"已监控**竞店**"是两个独立清单（配置页里也是分开的两个 tab）。
- **`getShopMonitorInfo.json` 参数只需 `cateId`** —— 多传 dateType/dateRange/pageSize 等无关字段会触发后端严格校验返 `code=1003 请求参数非法`；正确调用是 `GET /ms/compete/common/getShopMonitorInfo.json?cateId=54&_={timestamp}`，返回 `data:[{memberId, shopName, shopUrl, tradeMedalGrade, identity, tp, realBusiness, isDelete}]` 的当前所有已监控竞店（含 `isDelete=y/n` 状态位可用于筛"存活监控"）。`getOfferMonitorInfo.json` 同理，是竞品清单权威源。

---

## 行业类目树（cateId / cateLevel 的核心来源接口）

> **描述**：返回当前登录店铺被授权/主营的行业类目树，是所有 `/ms/compete/*` 接口填 `cateId`、`cateLevel` 参数的唯一合法来源。凡是其它接口把 `cateId`/`cateLevel` 标为「必填」的，都必须先调用此接口拿到合法节点值再传；未指定业务节点时**默认取 `cateLevel=1` 的一级类目**（即店铺主营行业根节点）。

### 接口内容

- **接口地址**：https://sycm.1688.com/ms/compete/industryCategory.json
- **请求方法**：GET
- **接口作用**：获取当前登录店铺被授权/主营的行业类目树（多级递归 children），供竞争 tab 顶部「类目筛选」渲染。同时是其它 `/ms/compete/*` 接口获取 `cateId`、`cateLevel` 的**核心/唯一合法来源**：其它接口标为必填的 `cateId`/`cateLevel` 必须从这里选一个节点取，默认取 `cateLevel=1` 的一级类目根节点。
- **入参**：
  - _：Long，选填，防缓存时间戳
  - 说明：无必填参数；`dateType`/`dateRange` 传或不传均不影响返回（类目树按账号授权取，与时间粒度无关）
- **出参核心字段**：
  - data：数组，顶层为一级类目列表（`cateLevel=1`），每个节点结构同构，通过 `children` 递归到二三级
  - data[].cateLevel：int，层级（1=一级 / 2=二级 / 3=三级）
  - data[].value：String，类目ID —— **即其它接口传的 cateId**
  - data[].text：String，类目名（如「服饰配件、饰品」「项饰」「耳钉」）
  - data[].children：数组，同结构递归子类目；末级类目无 children 或为空
- **出参示例**：
  - `{"code":0,"data":[{"cateLevel":1,"text":"服饰配件、饰品","value":"54","class":"com.alibaba.b2bopen.dto.CategoryInfoDTO","children":[{"cateLevel":2,"text":"饰品保养鉴定","value":"1033987"},{"cateLevel":2,"text":"服饰配件","value":"1045423","children":[{"cateLevel":3,"text":"袖扣","value":"122388003"},{"cateLevel":3,"text":"护膝","value":"201159602"}]},{"cateLevel":2,"text":"项饰","value":"122322005","children":[{"cateLevel":3,"text":"项链","value":"1037275"},{"cateLevel":3,"text":"吊坠","value":"122708005"}]}]}]}`
- **调用注意**：
  - **核心定位**：这是其它 `/ms/compete/*` 接口获取 `cateId`、`cateLevel` 的**唯一合法来源**——其它接口凡把 `cateId`/`cateLevel` 标为「必填」的，都必须先调用此接口取节点值再传。调用方未指定业务类目时：返回**只有 1 个一级类目就直接取 `data[0].value`** 搭配 `cateLevel=1`；返回**多个一级类目时应把各类目名（`text`）列出来反问用户选哪个**，不要默认拿 `data[0]`。
  - `cateId` 与 `cateLevel` 必须成对使用且**层级一致**：传一级类目 `value` 就必须搭配 `cateLevel=1`，传三级类目 `value` 就必须搭配 `cateLevel=3`；不一致会取不到数据。
  - 类目树**按店铺授权范围返回**，并非全平台类目（示例店铺仅返回 1 个一级类目 `服饰配件、饰品`，`value:"54"`，38 个二级子类）。切勿把它当成全平台目录使用。
  - 返回顶层是 `data:[]` 数组结构而非对象，即便只有 1 个一级类目也是长度为 1 的数组，遍历取即可。
  - `children` 递归深度最多 3 层（level 1→2→3），末级类目无 `children`。

---

## 竞店-行业店铺排行列表

> **描述**：按指定类目返回该类目下的行业店铺排行（含本店），每行是一个店铺，含店铺基础信息、多维度指数与环比、类目排名、类目评分对比、平台身份标识等。是竞店监控 tab / 竞店列表的核心数据源，也是店铺对标的主接口。

### 接口内容

- **接口地址**：https://sycm.1688.com/ms/compete/competeShop/shopList.json
- **请求方法**：GET
- **接口作用**：返回指定类目下的行业店铺排行数据，每行一个店铺，含店铺基础信息（shop 子对象）、多维度指数与环比（ipvUvIndex / seUvIndex / payOrdAmtIndex / buyerIndex 均带 cycleCrc）、类目排名（cateRank 带 cycleCqc）、行业均值评分（cateScoreXy/Fh/Hm）与本店评分（scorexy/scorefh/scorehm）、新品数（newItmCnt）、回购率（repeatRate），以及平台身份标签（isPm / isZgcSlr / isCjgcSlr）等，本店行会以 `isMyShop=y` 标识。
- **入参**：
  - dateRange：String，必填，日期区间，示例 2026-06-28|2026-07-27
  - dateType：String，必填，时间粒度，RECENT_7/RECENT_30
  - cateId：int，必填，类目ID，示例 54，通过/compete/industryCategory 接口获取（未指定业务类目时默认取一级根节点）
  - cateLevel：int，必填，类目层级，需与 cateId 层级一致，示例 1
  - device：String，必填，端别，ALL（全部）/ PC / WIRELESS
  - orderBy：String，选填，排序字段，默认 payOrdAmtIndex，可用 ipvUvIndex/seUvIndex/buyerIndex/newItmCnt/cateRank 等
  - order：String，选填，排序方向，asc/desc
  - page：int，选填，页码，示例 1
  - pageSize：int，选填，分页大小，示例 20（详见调用注意）
  - _：Long，选填，防缓存时间戳
- **出参核心字段**：
  - data.data：数组，店铺行列表
  - data.recordCount：int，总条数
  - data.data[].shop：店铺基础信息子对象 { shopName, shopUrl, memberId, identity（如 svip）, tradeMedalGrade（如 AAAA/AAAAA）, realBusiness(bool), tp(bool), class }
  - data.data[].memberId：{value} 店铺会员ID（与 shop.memberId 冗余）
  - data.data[].statDate：{value} 统计日期 YYYY-MM-DD 字符串
  - data.data[].isMyShop：y/n，是否本店
  - 指数类字段（均含 value + cycleCrc 环比变化率）：
    - data.data[].ipvUvIndex：访客指数
    - data.data[].seUvIndex：搜索访客指数
    - data.data[].payOrdAmtIndex：支付金额指数
    - data.data[].buyerIndex：买家指数
  - data.data[].cateRank：{value, cycleCqc} 类目排名（环比字段是 cycleCqc「变化数」，非 cycleCrc「变化率」，注意区分）
  - data.data[].newItmCnt：{value} 新品数
  - data.data[].repeatRate：{value} 回购率
  - 环比比率字段（与上面 cycleCrc 语义冗余，单独出字段）：
    - data.data[].ipvUvRate：{value} 访客环比
    - data.data[].payOrdAmtRate：{value} 支付金额环比
  - 行业均值评分（该类目基准，同一次请求内所有行相同）：
    - data.data[].cateScoreXy：{value} 销量评分基准
    - data.data[].cateScoreFh：{value} 复购评分基准
    - data.data[].cateScoreHm：{value} 好卖评分基准
  - 本店铺评分（各店独立）：
    - data.data[].scorexy：{value} 销量分
    - data.data[].scorefh：{value} 复购分
    - data.data[].scorehm：{value} 好卖分
  - 平台身份标签（均 {value:'Y'/'N'}）：
    - data.data[].isPm：是否精选/精铺店铺
    - data.data[].isZgcSlr：是否中国制造卖家
    - data.data[].isCjgcSlr：是否超级工厂卖家
- **出参示例**：
  - `{"code":0,"data":{"recordCount":50,"data":[{"shop":{"shopName":"<示例竞店A名称>","tradeMedalGrade":"AAAA","identity":"svip","shopUrl":"https://<店铺标识>.1688.com","memberId":"<竞店A memberId>","realBusiness":true,"tp":true},"statDate":{"value":"2026-07-27"},"isMyShop":"n","ipvUvIndex":{"value":349373.68,"cycleCrc":-0.0281},"seUvIndex":{"value":527146.36,"cycleCrc":-0.0030},"payOrdAmtIndex":{"value":300248.28,"cycleCrc":-0.0150},"buyerIndex":{"value":1087426.71,"cycleCrc":0.0461},"cateRank":{"value":42,"cycleCqc":-7},"newItmCnt":{"value":123},"repeatRate":{"value":0.1667},"cateScoreXy":{"value":4.16},"cateScoreFh":{"value":4.35},"cateScoreHm":{"value":4.85},"scorexy":{"value":4.65},"scorefh":{"value":4.58},"scorehm":{"value":5.0},"isPm":{"value":"Y"},"isZgcSlr":{"value":"Y"},"isCjgcSlr":{"value":"Y"}},{"shop":{"shopName":"<示例本店名称>","tradeMedalGrade":"AAAAA"},"isMyShop":"y","payOrdAmtIndex":{"value":292287.22,"cycleCrc":0.0822}}]}}`
- **调用注意**：
  - cateId/cateLevel 必须成对且层级一致，来源 industryCategory.json；未指定业务类目时默认取一级根节点（cateLevel=1）。
  - pageSize=20&page=1 时后端仍返回 50 条（recordCount=50 也是 50），说明该接口存在内置上限（约 50 行），前端分页可能只是本地截取；如需严格分页，建议前端按 pageSize 自行切片，不要完全依赖 page/pageSize 传参生效。
  - 排名环比字段名是 cycleCqc（其它接口普遍是 cycleCrc）：cycleCqc 是「变化数」（如 -7 名），cycleCrc 是「变化率」（如 -0.0281 = -2.81%），别写错。
  - 指数字段（ipvUvIndex/payOrdAmtIndex 等）为「指数」非绝对值，仅用于横向对比与环比走势。
  - cateScoreXy/Fh/Hm 是该类目的**平均基准分**（同一次请求内所有行都相同），用于与每行的 scorexy/scorefh/scorehm（本店实际分）做对标。
  - 结果同时包含本店（isMyShop=y）与竞店（isMyShop=n），前端可据此高亮/分组。
  - orderBy=cateRank 时升序即「排名越小越靠前」；指数字段默认 desc 更符合业务语义。

---

## 竞店-客户流失 TOP 竞店排行

> **描述**：按指定类目返回本店的**客户流失去向 TOP N 竞店**排行（即本店潜在流失客户去了哪些竞店），每行是一个流失竞店，含流失指数 `lossIndex`（核心指标）、店铺基础信息、多维度指数、是否已监控、平台身份标签等。是竞店识别页做「客户流失竞店」发现与一键加监控的主接口。

### 接口内容

- **接口地址**：https://sycm.1688.com/ms/compete/shopDiscern/lossShop/getLossTopShopList.json
- **请求方法**：GET
- **接口作用**：返回指定类目下本店客户流失去向的 TOP N 竞店排行，主排序字段 `lossIndex`（流失指数），并返回每个竞店的访客/搜索访客/支付金额/买家指数、回购率、是否已监控、平台身份标签等。用于竞店识别页发现流失竞店并支持一键加监控。
- **入参**：
    - dateRange：String，必填，日期区间（首尾同一天，示例 2026-07-26|2026-07-26）
    - dateType：String，必填，时间粒度，此接口固定用 **RECENT_1**（日粒度）；日数据有延迟，查昨天返空数组时加 `periodsAgo=1` 回溯前一天
    - cateId：int，必填，类目ID，示例 54，通过/compete/industryCategory 接口获取（未指定业务类目时默认取一级根节点）
    - cateLevel：int，必填，类目层级，需与 cateId 层级一致，示例 1
    - device：String，必填，端别，ALL（全部）/ PC / WIRELESS
    - orderBy：String，选填，排序字段，默认 lossIndex，也支持 ipvUvIndex/seUvIndex/payOrdAmtIndex/buyerIndex
    - order：String，选填，排序方向，asc/desc
    - pageNo：int，选填，页码，示例 1（**注意字段名是 pageNo 而非 page**）
    - pageSize：int，选填，分页大小，示例 10（该接口分页参数**生效**）
    - _：Long，选填，防缓存时间戳
- **出参核心字段**：
    - data.data：数组，流失竞店行列表
    - data.recordCount：int，总条数
    - data.data[].orderNum：int，排名序号（1 起）
    - data.data[].shop：店铺基础信息子对象 { shopName, shopUrl, memberId, identity（如 svip）, tradeMedalGrade（AAA/AAAA…）, realBusiness(bool), tp(bool), class }
    - data.data[].memberId：{value} 冗余会员ID
    - data.data[].statDate：{value} 统计日期，**毫秒时间戳**（如 1784995200000 → 2026-07-26；与 shopList.json 的 YYYY-MM-DD 字符串风格不同）
    - data.data[].lossIndex：{value} **流失指数**（核心指标，值越大表示本店客户流失到该店越多）
    - 其它维度指数（**仅 value、无 cycleCrc**，因日粒度不做环比）：
      - data.data[].ipvUvIndex：访客指数
      - data.data[].seUvIndex：搜索访客指数
      - data.data[].payOrdAmtIndex：支付金额指数
      - data.data[].buyerIndex：买家指数
    - data.data[].repeatRate：{value} 回购率
    - data.data[].isMonitor：**boolean**（true/false），是否已加入本店监控（注意与 shopList.json 里 isMyShop 的 y/n 字符串风格不同）
    - 平台身份标签（均 {value:'Y'/'N'}）：
      - data.data[].isPm：是否精铺店铺
      - data.data[].isZgcSlr：是否中国制造卖家
      - data.data[].isCjgcSlr：是否超级工厂卖家
    - 评分字段占位（日粒度下**均为 0.0**，仅在 RECENT_7/RECENT_30 场景才有意义，可忽略）：cateScoreXy/cateScoreFh/cateScoreHm 行业均值基准、scorexy/scorefh/scorehm 本店评分
- **出参示例**：
    - `{"code":0,"data":{"recordCount":51,"data":[{"orderNum":1,"shop":{"shopName":"<示例竞店B名称>","tradeMedalGrade":"AAAA","identity":"svip","shopUrl":"https://<店铺标识>.1688.com","memberId":"<竞店B memberId>","realBusiness":true,"tp":true},"statDate":{"value":1784995200000},"lossIndex":{"value":218289.71},"ipvUvIndex":{"value":56216.39},"seUvIndex":{"value":365309.07},"payOrdAmtIndex":{"value":90451.31},"buyerIndex":{"value":1019031.68},"repeatRate":{"value":0.0},"isMonitor":true,"isPm":{"value":"Y"},"isZgcSlr":{"value":"Y"},"isCjgcSlr":{"value":"Y"}},{"orderNum":2,"shop":{"shopName":"<示例竞店C名称>","tradeMedalGrade":"AAA"},"lossIndex":{"value":54855.80},"isMonitor":true,"isCjgcSlr":{}}]}}`
- **调用注意**：
    - 分页参数名是 **pageNo（非 page）**、pageSize，且**生效**：pageSize=10 就真返回 10 条（不像 competeShop/shopList.json 会忽略分页返回 ~50 条）。总条数看 `recordCount`。
    - dateType 固定用 **RECENT_1**（日粒度），dateRange 首尾同一天即可（如 2026-07-26|2026-07-26）；日数据有延迟，查昨天返空数组 `[]` 时传 `periodsAgo=1` 回溯前一天。也因此本接口所有指数字段**只有 value、没有环比 cycleCrc**。
    - cateId/cateLevel 必须成对同层级，来源 industryCategory.json；未指定业务类目时默认取一级根节点。
    - `statDate` 是**毫秒时间戳**（前端要 `new Date(value)` 才能格式化），和 shopList.json 里 YYYY-MM-DD 字符串风格不同，跨接口拼装数据时要做兼容。
    - `isMonitor` 是**布尔**（不是 y/n 字符串），UI 判断/加入监控按钮的显隐直接用；返回结果中**本店有可能也出现在流失榜里**，前端如需过滤要按 `shop.memberId` 匹配当前登录店铺剔除。
    - 榜单里可能存在字段返回**空对象 `{}`** 的情况（如示例中 rank2 的 `isCjgcSlr:{}`），代码取 `.value` 前建议做空判断。
    - cateScoreXy/Fh/Hm 与 scorexy/scorefh/scorehm 在日粒度场景全为 0.0，不要拿来做业务判断，建议直接忽略这几个字段。
    - 主排序字段是 lossIndex（默认 desc）；如切换 orderBy=ipvUvIndex 等其它指标，可作为「访客/搜索/支付」维度的行业竞店排行通用查询。

---

## 竞品-搜索流失商品清单（按本店商品维度）

> **描述**：给定类目和时间周期，返回**搜索场景**下**本店哪些商品正在流失流量**——每行 = 本店的一个商品 offer，右侧同时给出「该本店商品在监控搜索词上流失去的竞品聚合表现」与「本店该商品自身表现」双列指标，方便逐个本店商品定位到底在哪些搜索场景被竞品吃走。是竞店竞品分析页「商品流失识别 → 搜索流失商品」的主接口，与店铺维度的 `shopDiscern/lossShop/getLossTopShopList.json` 互为对偶——那个按**店铺**排（流失去了哪几家竞店），本接口按**本店商品**排（本店哪些商品在被流失），流失场景固定为「搜索」。

### 接口内容

- **接口地址**：https://sycm.1688.com/ms/compete/offerDiscern/searchLossOffer/getOfferList.json
- **调用方法**：GET
- **入参说明**：
    - cateId：int，必填，类目 ID，示例 54（来源 industryCategory.json）
    - cateLevel：int，必填，类目层级，示例 1（须与所选 cateId 层级一致）
    - dateType：string，必填，时间口径，示例 RECENT_7（本接口不强制日粒度，可用 7 天窗口）
    - dateRange：string，必填，日期区间，格式 YYYY-MM-DD|YYYY-MM-DD，示例 2026-07-20|2026-07-26
    - pageNo：int，必填，页码，示例 1（配合 pageSize 分页；参数名是 pageNo 不是 page，与 getLossTopShopList 一致）
    - pageSize：int，必填，每页条数，示例 10
    - orderBy：string，必填，排序字段，示例 seMonitorOfferCount（其它可选如 monitorOfferUv/myOfferUv/monitorOfferPayOrdAmtRate 等，取字段名同）
    - order：string，必填，排序方向，desc/asc，示例 desc
- **出参说明**：
    - code：int，业务状态码，0 表示成功
    - message：string，业务提示信息，示例 "操作成功"
    - data.recordCount：int，符合条件的**本店商品**总条数（示例返回 154，即当前类目+周期下共 154 个本店商品在搜索场景发生流失）
    - data.data：array，本页本店商品行列表
    - data.data[].orderNum：int，本页内排名（从 1 开始，跨页需 (pageNo-1)*pageSize+orderNum 换算全局名次）
    - data.data[].itemId：{value} **本店商品 offerId** 字符串（如 "797892274346"，注意是 string，避免精度丢失）
    - data.data[].memberId：{value} **本店** memberId（同一份返回内所有行相同，等于当前登录店铺 memberId，可用来验证是本店视角）
    - data.data[].cateId：{value} 回显入参，示例 54
    - data.data[].cateLevel：{value} 回显入参，示例 1
    - data.data[].statDate：{value} 统计日期，**毫秒时间戳**（如 1784995200000）
    - data.data[].item：object，**本店商品**信息块（结构与 getCompeteList.json 的 item 字段完全一致，item.memberId 即等于本店 memberId）
        - offerId / offerTitle / detailUrl / minPrice / maxPrice / basePrice / categoryID（**商品自挂叶子类目 ≠ 入参 cateId**）/ offerUpdateTime / offerExpireTime / memberId / class
        - offerImageUrl：**相对路径**（如 "img/ibank/O1CN01...jpg"），需自行拼接 `https://cbu01.alicdn.com/` 前缀
    - data.data[].seMonitorOfferCount：{value} 该本店商品在本类目搜索监控词库中命中的搜索热度累计（数值较大，示例 5182；本接口默认按此字段 desc 排——"越大越优先"表明该本店商品覆盖的监控词搜索露出越广、被流失面越大）
    - data.data[].monitorOfferUv：{value} 在该本店商品覆盖的监控词上，**流失去的竞品聚合 UV 指数**（浮点，如 3.746，指数化后数值小；非原始 UV 计数）
    - data.data[].monitorOfferBuyerCount：{value} 在同一批监控词上，**流失去的竞品聚合买家数指数**（浮点 < 1，如 0.4259）
    - data.data[].monitorOfferPayOrdAmtRate：{value} 在同一批监控词上，**流失去的竞品聚合支付金额指数**（浮点，如 11.37）
    - data.data[].myOfferUv：{value} 本店此商品在同一批监控词上的**原始 UV 计数**（整数，如 256；非指数）
    - data.data[].myOfferBuyerCount：{value} 本店此商品在同一批监控词上的**原始买家数**（整数，如 2）
    - data.data[].myOfferPayOrdAmtRate：{value} 本店此商品在同一批监控词上的支付金额相关比率（浮点，如 0.78125）
- **出参示例**：
    - `{"code":0,"message":"操作成功","data":{"recordCount":154,"data":[{"orderNum":1,"itemId":{"value":"797892274346"},"memberId":{"value":"<本店 memberId>"},"cateId":{"value":54},"cateLevel":{"value":1},"statDate":{"value":1784995200000},"item":{"offerId":797892274346,"offerTitle":"<示例商品标题>","offerImageUrl":"img/ibank/<图片标识>.jpg","detailUrl":"https://detail.1688.com/offer/<offerId>.html","minPrice":38.0,"maxPrice":43.0,"basePrice":"38.0","categoryID":1033155,"memberId":"<本店 memberId>"},"seMonitorOfferCount":{"value":5182},"monitorOfferUv":{"value":3.746},"monitorOfferBuyerCount":{"value":0.4259},"monitorOfferPayOrdAmtRate":{"value":11.369},"myOfferUv":{"value":256},"myOfferBuyerCount":{"value":2},"myOfferPayOrdAmtRate":{"value":0.781}}]}}`
- **调用注意**：
    - 分页参数是 **pageNo（不是 page）+ pageSize**，与 getLossTopShopList.json 风格一致；总量看 `recordCount`。
    - 本接口所有指数字段**只有 value、没有环比 cycleCrc**（同 getLossTopShopList/getCompeteList）；如需环比要另调 `getOfferCoreIndexTrend.json` 拉趋势自己算。
    - **双列语义不对称**：`monitorOfferXxx` 是**流失去的竞品聚合**指数化数值（浮点、量级小），`myOfferXxx` 是**本店此商品自身**的原始计数（整数或原始比率）——**不要**直接把 `monitorOfferUv=3.7` 与 `myOfferUv=256` 相比得出"我流量是竞品 68 倍"的错误结论。要么两侧同为指数（本店指数可查 `getOfferCoreIndex.json`），要么两侧同为原始值再做对比。
    - `item.categoryID` 是**该商品自挂的叶子类目**（如 1033155），与入参 cateId（如 54，一级类目）不同；做类目匹配时用叶子类目。
    - `item.offerImageUrl` 是**相对路径**，前端需拼 `https://cbu01.alicdn.com/` 前缀才能加载。
    - 主排序默认字段 `seMonitorOfferCount desc`（"搜索命中量越大越靠前"）；如果关注"流失去的竞品跑得有多凶"，改用 `monitorOfferBuyerCount` 或 `monitorOfferPayOrdAmtRate` 降序。
    - `statDate` 是**毫秒时间戳**（`{value:1784995200000}`），与 shopList.json 的 YYYY-MM-DD 字符串不同，跨接口拼装要做兼容。
    - **返回的 offerId 是本店商品**（`item.memberId` = 本店 memberId），**不要**误认为是"竞品清单"——如需拿竞品 offerId 走单品对比，请用 `getCompeteList.json`（已监控竞品）。
    - 用途：定位"本店哪些商品在搜索场景被谁抢"——拿到重点流失本店商品后，再用 `seachofferKey.json`（本店该商品的引流词）与 `inputShopKey.json`（竞店词榜）交叉，找出丢词点。

---

## 竞品-访问流失商品清单（按本店商品维度，全流量场景）

> **描述**：给定类目和时间周期，返回**访问流失**场景下**本店哪些商品正在流失流量与订单**——每行 = 本店的一个商品 offer，右侧给出该商品的访客最终在竞店产生的成交金额、买家数、订单商品数、涉及竞店家数、流失率，以及从**收藏 / 加购**入口流失的买家数拆分。是竞店竞品分析页「商品流失识别 → 访问流失商品」的主接口，与 `searchLossOffer/getOfferList.json` 结构对偶——那个仅覆盖**搜索场景**并给双列指数对比，本接口覆盖**全流量渠道的访问流失**，字段全是**本店视角的原始金额/人数**而非指数，业务解读更直白。

### 接口内容

- **接口地址**：https://sycm.1688.com/ms/compete/offerDiscern/viewLossOffer/getOfferList.json
- **调用方法**：GET
- **入参说明**：
    - cateId：int，必填，类目 ID，示例 54（来源 industryCategory.json）
    - cateLevel：int，必填，类目层级，示例 1
    - dateType：string，必填，时间口径，示例 RECENT_7
    - dateRange：string，必填，日期区间，格式 YYYY-MM-DD|YYYY-MM-DD，示例 2026-07-20|2026-07-26
    - pageNo：int，必填，页码，示例 1（参数名 pageNo 不是 page）
    - pageSize：int，必填，每页条数，示例 10
    - orderBy：string，必填，排序字段，示例 lossPayAmt（其它可选 lossBuyerCount / lossItemCount / lossShopCount / lossRate / cltLossBuyerCount / cartLossBuyerCount，字段名同）
    - order：string，必填，排序方向，desc/asc，示例 desc
- **出参说明**：
    - code：int，业务状态码，0 表示成功
    - message：string，业务提示信息，示例 "操作成功"
    - data.recordCount：int，符合条件的**本店商品**总条数（示例返回 153）
    - data.data：array，本页本店商品行列表
    - data.data[].orderNum：int，本页内排名（从 1 开始，跨页需 (pageNo-1)*pageSize+orderNum 换算全局名次）
    - data.data[].itemId：{value} **本店商品 offerId** 字符串（如 "713159000665"）
    - data.data[].memberId：{value} **本店** memberId（同一份返回内所有行相同，等于当前登录店铺 memberId）
    - data.data[].cateId：{value} 回显入参，示例 54
    - data.data[].cateLevel：{value} 回显入参，示例 1
    - data.data[].statDate：{value} 统计日期，**毫秒时间戳**（如 1784995200000）
    - data.data[].item：object，**本店商品**信息块（结构同 getCompeteList.json / searchLossOffer 的 item，item.memberId 等于本店 memberId）
        - offerId / offerTitle / detailUrl / minPrice / maxPrice / basePrice / categoryID（叶子类目 ≠ 入参 cateId）/ offerUpdateTime / offerExpireTime / memberId / class
        - offerImageUrl：相对路径，需拼 `https://cbu01.alicdn.com/` 前缀
    - data.data[].lossPayAmt：{value} **流失支付金额**，即本店该商品的访客最终在竞店成交的支付金额合计（**元，原始值**，非指数，如 148050）——本接口默认按此字段 desc 排
    - data.data[].lossBuyerCount：{value} **流失买家数**，本店该商品访客最终在竞店下单的**唯一买家数**（整数，如 39）
    - data.data[].lossItemCount：{value} **流失订单商品数**，被流失买家在竞店买走的商品件数（整数，如 35）
    - data.data[].lossShopCount：{value} **涉及竞店家数**，本店该商品的访客最终流失去的**不同竞店数**（整数，如 21——数值越大说明流失越分散）
    - data.data[].lossRate：{value} **流失率**（0~1 浮点，如 0.848 表示 84.8% 的访问最终在其它店成交；存在 = 1.0 即 100% 流失的极端商品）
    - data.data[].cltLossBuyerCount：{value} **收藏后流失买家数**——把本店该商品加入过收藏、最终却在竞店成交的唯一买家数（整数，如 2；多数为 0）
    - data.data[].cartLossBuyerCount：{value} **加购后流失买家数**——把本店该商品加入过购物车、最终却在竞店成交的唯一买家数（整数，如 1；多数为 0）
- **出参示例**：
    - `{"code":0,"message":"操作成功","data":{"recordCount":153,"data":[{"orderNum":1,"itemId":{"value":"713159000665"},"memberId":{"value":"<本店 memberId>"},"cateId":{"value":54},"cateLevel":{"value":1},"statDate":{"value":1784995200000},"item":{"offerId":713159000665,"offerTitle":"<示例商品标题>","minPrice":200.0,"maxPrice":950.0,"basePrice":"200.0","categoryID":1033153,"detailUrl":"https://detail.1688.com/offer/<offerId>.html","offerImageUrl":"img/ibank/<图片标识>.jpg","memberId":"<本店 memberId>"},"lossPayAmt":{"value":148050.0},"lossBuyerCount":{"value":39},"lossItemCount":{"value":35},"lossShopCount":{"value":21},"lossRate":{"value":0.8478260869565217},"cltLossBuyerCount":{"value":0},"cartLossBuyerCount":{"value":1}}]}}`
- **调用注意**：
    - **返回的 offerId 是本店商品**（同一份返回内所有 `item.memberId` = 本店 memberId），不是竞品清单；本接口不返回具体流失去了哪家竞店（只给聚合的 lossShopCount 家数），如需拿到"流失去了具体哪些竞店"要另调 `shopDiscern/lossShop/getLossTopShopList.json`（店铺维度）。
    - 分页参数是 **pageNo（不是 page）+ pageSize**，与 searchLossOffer/getLossTopShopList 一致；总量看 `recordCount`。
    - **字段全是原始值不是指数**：lossPayAmt 是**元**（可直接汇总求总流失金额），lossBuyerCount/lossItemCount/lossShopCount/cltLossBuyerCount/cartLossBuyerCount 全部是**整数计数**，可直接排序、聚合、SUM；lossRate 是 0~1 比率。与 searchLossOffer 的"monitor 指数 vs my 原始"混合语义不同，本接口的对比更直白。
    - **lossRate 存在 = 1.0 的极端值**（表示 100% 访问都流失去竞店），做健康度分析时要单独看这一批异常商品——通常伴随极低 UV，可能是长尾/新品被完全截胡。
    - **cltLossBuyerCount / cartLossBuyerCount 多为 0**（示例 10 条只有 3 条非零）——但**非零就是高风险信号**：买家都加购/收藏了、最后还是去竞店买，说明本店该 offer 存在决策临门一脚被抢的问题（价格/服务/描述被比下去）。
    - 默认 `orderBy=lossPayAmt desc`（钱多的先看）；如果排查用户体验问题优先看 `cartLossBuyerCount desc` 或 `cltLossBuyerCount desc`；如果排查覆盖度改用 `lossShopCount desc`（涉及竞店越多越分散）。
    - `item.categoryID` 是叶子类目（如 1033153），与入参 cateId（54，一级）不同；`item.offerImageUrl` 是相对路径需拼 `https://cbu01.alicdn.com/` 前缀。
    - `statDate` 是**毫秒时间戳** `{value:1784995200000}`（与 shopList.json 的 YYYY-MM-DD 字符串风格不同）。
    - 用途：与 `searchLossOffer` 组合成完整"本店商品被抢"画像——搜索流失看竞品指数、访问流失看金额/买家/涉及竞店数原始量；对同一本店 offerId 两边都上榜的即为**双通道被抢**的重灾商品，应优先加监控 / 调价 / 换主图 / 优化引流词。

---

## 竞品-同款商品清单（本店有同款竞品的自家商品入口）

> **描述**：给定类目和时间周期，返回**本店在该类目下有可识别的同款/相似竞品**的自家商品清单——每行 = 本店的一个商品 offer，附带本店该商品的访客/搜索/成交/买家指数（value-only）与搜索页浏览环比。是竞店竞品分析页「同款商品识别」tab 的入口清单接口：用户从中挑一个本店 offer 后，再走同款竞品明细接口拿"这个本店 offer 对应的具体同款竞品们"（本接口本身**不返回竞品数据**）。**注意：接口名带 "sameProductOffer" 容易让人误以为返回的是同款竞品，所有行 item.memberId 均等于当前登录店铺 memberId，返回的是"本店有同款竞品可比对"的自家 offer 池。**

### 接口内容

- **接口地址**：https://sycm.1688.com/ms/compete/offerDiscern/sameProductOffer/getOfferList.json
- **调用方法**：GET
- **入参说明**：
    - cateId：int，必填，类目 ID，示例 54（来源 industryCategory.json）
    - cateLevel：int，必填，类目层级，示例 1
    - dateType：string，必填，时间口径，示例 RECENT_7
    - dateRange：string，必填，日期区间，格式 YYYY-MM-DD|YYYY-MM-DD，示例 2026-07-20|2026-07-26
    - pageNo：int，必填，页码，示例 1（参数名 pageNo 不是 page；支持翻页到深页）
    - pageSize：int，必填，每页条数，示例 10
    - orderBy：string，必填，排序字段，示例 payOrdAmtIndex（其它可选 ipvUvIndex / seUvIndex / buyerIndex / seSpvChangeRate，字段名同）
    - order：string，必填，排序方向，desc/asc，示例 desc
- **出参说明**：
    - code：int，业务状态码，0 表示成功
    - message：string，业务提示信息，示例 "操作成功"
    - data.recordCount：int，本店在该类目下有同款竞品可比对的商品总数（示例返回 200）
    - data.data：array，本页本店商品行列表
    - data.data[].orderNum：int，本页内排名（从 1 开始，跨页需 (pageNo-1)*pageSize+orderNum 换算全局名次）
    - data.data[].itemId：{value} **本店商品 offerId** 字符串（如 "595864659430"）
    - data.data[].memberId：{value} **本店** memberId（同一份返回内所有行相同，等于当前登录店铺 memberId）
    - data.data[].cateId：{value} 回显入参，示例 54
    - data.data[].cateLevel：{value} 回显入参，示例 1
    - data.data[].statDate：{value} 统计日期，格式为 **`"YYYY-MM-DD"` 字符串**（如 "2026-07-26"）——与本页其它 offerDiscern 接口的**毫秒时间戳**风格不同，与 shopList.json 一致
    - data.data[].item：object，**本店商品**信息块（结构同 getCompeteList / searchLossOffer / viewLossOffer 的 item，item.memberId 即本店 memberId）
        - offerId / offerTitle / detailUrl / minPrice / maxPrice / basePrice / categoryID（叶子类目 ≠ 入参 cateId）/ offerUpdateTime / offerExpireTime / memberId / class
        - offerImageUrl：相对路径，需拼 `https://cbu01.alicdn.com/` 前缀
    - data.data[].ipvUvIndex：{value} 本店该商品的商品详情页 UV 指数（浮点，如 698.40）
    - data.data[].seUvIndex：{value} 本店该商品的搜索访客指数（浮点，量级偏大，如 86850.5——比通用类目排行接口的 seUvIndex 大 3 个数量级，疑为**日累计 × 分辨率**放大后的呈现）
    - data.data[].payOrdAmtIndex：{value} 本店该商品的支付金额指数（浮点，如 724.68）——本接口默认按此字段 desc 排
    - data.data[].buyerIndex：{value} 本店该商品的买家指数（浮点，量级大，如 145745.4）
    - data.data[].seSpvChangeRate：{value} 本店该商品的**搜索页浏览量（SPV）环比变化率**（浮点，0.20 = +20%，-0.11 = -11%）；存在极端异常值（如 110 = +11000%，通常是短周期从近零涨到有量），做告警时要过滤或截断
- **出参示例**：
    - `{"code":0,"message":"操作成功","data":{"recordCount":200,"data":[{"orderNum":1,"itemId":{"value":"595864659430"},"memberId":{"value":"<本店 memberId>"},"cateId":{"value":54},"cateLevel":{"value":1},"statDate":{"value":"2026-07-26"},"item":{"offerId":595864659430,"offerTitle":"<示例商品标题>","minPrice":13.0,"maxPrice":18.0,"basePrice":"13.0","categoryID":1033155,"detailUrl":"https://detail.1688.com/offer/<offerId>.html","offerImageUrl":"img/ibank/<图片标识>.jpg","memberId":"<本店 memberId>"},"ipvUvIndex":{"value":698.40},"seUvIndex":{"value":86850.51},"payOrdAmtIndex":{"value":724.68},"buyerIndex":{"value":145745.44},"seSpvChangeRate":{"value":0.196}}]}}`
- **调用注意**：
    - **返回的 offerId 全是本店商品**（所有行 item.memberId 均等于本店 memberId），接口命名容易误导——不是"同款竞品清单"，而是"本店有同款可比对的自家商品清单"；如需拿到某本店 offer 对应的具体同款竞品，须走同款竞品明细接口。
    - 本接口指数字段**只有 value、没有 cycleCrc**（同 searchLossOffer/viewLossOffer/getCompeteList/getLossTopShopList）；唯一自带环比的是 `seSpvChangeRate`（且是**搜索页浏览量**变化率，不是常规访客环比，不能等同看待）。
    - `seUvIndex` / `buyerIndex` 数量级明显大于类目排行接口（getItmRank）里同名指数——本接口的指数似乎是**同款筛选后局部标准化**的结果，**不要**直接与 getItmRank / getCompeteList 中同一 offer 的 seUvIndex 做横向比较；如需可比性，只在本接口返回集内做相对排序即可。
    - `seSpvChangeRate` 存在极端异常值（如 110 即 +11000%）——通常是短窗口从近零到有量的正常事件，但做告警排序时要截断/过滤，否则会污染 TOP 榜。
    - 分页参数是 **pageNo（不是 page）+ pageSize**，与 searchLossOffer/viewLossOffer/getLossTopShopList 一致；总量看 `recordCount`。
    - `statDate` 是**字符串日期** `{value:"YYYY-MM-DD"}`（**特例**！本页其它 offerDiscern 接口都是毫秒时间戳），跨接口拼装数据时要按类型分支处理。
    - `item.categoryID` 是叶子类目（如 1033155），与入参 cateId（54，一级）不同；`item.offerImageUrl` 是相对路径需拼 `https://cbu01.alicdn.com/` 前缀。
    - 用途：作为「同款商品分析」的入口选品——先按 payOrdAmtIndex 或 buyerIndex 排出本店销售 TOP N 的商品，再从中挑 5~10 个"值得做同款对标"的 offer 拿去下一步接口拉具体竞品，避免一开始就对 200 个 offer 全量拉。

---

## 竞店-单店引流搜索词榜（按竞店维度）

> **描述**：给定单个竞店的 `memberId`，返回该竞店在指定类目、周期、流量渠道下的 TOP 搜索引流关键词榜（每项一个词，含访客/搜索访客/支付金额/买家指数、环比、排名）。是竞店分析页「流量分析 → 引流关键词」查看某一家竞店靠哪些搜索词引流的主接口，与 seachofferKey.json（竞品维度）互为对偶——本接口按**店铺**下钻，seachofferKey 按**单品**下钻。

### 接口内容

- **接口地址**：https://sycm.1688.com/ms/compete/competeShop/inputShopKey.json
- **请求方法**：GET
- **接口作用**：按 memberId 返回单个竞店在指定类目、周期、流量渠道下的 TOP 引流关键词榜。返回每个关键词的 keyword（UTF-8 明文）、keywordGbk（GBK 编码，用于拼 1688 搜索跳转链接），及多维度指数：ipvUvIndex（访客指数）、seUvIndex（搜索访客指数）、payOrdAmtIndex（支付金额指数）、buyerIndex（买家指数），均含 cycleCrc 环比变化率；同时含 orderNum（排名）、statDate（毫秒时间戳）、isAdServing（是否广告词占位）、memberId（回显目标竞店ID）。
- **入参**：
    - dateRange：String，必填，日期区间，示例 2026-07-21|2026-07-27
    - dateType：String，必填，时间粒度，RECENT_7/RECENT_30
    - cateId：int，必填，类目ID，示例 54，通过/compete/industryCategory 接口获取（未指定业务类目时默认取一级根节点）
    - cateLevel：int，必填，类目层级，需与 cateId 层级一致，示例 1
    - memberId：String，必填，**目标竞店会员ID**（形如 `b2b-` + 18 位字母数字），从竞店监控/竞店排行接口获取，禁止凭记忆填写
    - flowSourceType：int，必填，**指标排序 tab 切换**（不是流量渠道过滤）——1=按 `ipvUvIndex` desc（流量指数）/ 2=按 `seUvIndex` desc（搜索指数）/ 3=按 `payOrdAmtIndex` desc（交易指数）/ **4=按 `buyerIndex` desc（买家指数）**。FT3 剔除 payOrdAmt 脱敏 magic。**与 seachofferKey 的差异**：本接口 4 个 tab 全可用（FT4=买家指数榜），seachofferKey 只有 FT1/2/3 有效、FT4 返空。0 及 ≥5 返回空数组。业务上不确定意图时**默认传 1** 拿标准流量指数榜。
    - device：String，必填，端别，ALL（全部）/ PC / WIRELESS
    - _：Long，选填，防缓存时间戳
- **出参核心字段**：
    - data：数组，每项一个引流关键词（默认返回 TOP N，无分页参数）
    - data[].orderNum：int，排名序号（1 起，默认按 ipvUvIndex 降序）
    - data[].keyword：{value} 关键词（UTF-8 明文，用于展示）
    - data[].keywordGbk：String，关键词的 **GBK URL 编码**（**直接字符串，无 value 包装**，用于拼接 1688 搜索跳转链接）
    - data[].memberId：{value} 目标竞店会员ID（回显入参，便于批量结果落库时区分店铺）
    - data[].statDate：{value} 统计日期，**毫秒时间戳**（如 1785081600000 → 2026-07-25，与 shopList.json 的 YYYY-MM-DD 字符串风格不同）
    - data[].isAdServing：对象占位（常为空对象 `{}`，可能标记是否为广告词，代码取值前需判空）
    - 指数类字段（**均含 value + cycleCrc 环比变化率**）：
      - data[].ipvUvIndex：该词带来的访客指数
      - data[].seUvIndex：该词搜索访客指数
      - data[].payOrdAmtIndex：该词支付金额指数
      - data[].buyerIndex：该词买家指数
- **出参示例**：
    - `{"code":0,"data":[{"orderNum":1,"statDate":{"value":1785081600000},"keyword":{"value":"林德伯格镜架"},"keywordGbk":"%C1%D6%B5%C2%B2%AE%B8%F1%BE%B5%BC%DC","memberId":{"value":"<竞店 memberId>"},"isAdServing":{},"ipvUvIndex":{"value":4158.44,"cycleCrc":-0.0987},"seUvIndex":{"value":212109.06,"cycleCrc":-0.0363},"payOrdAmtIndex":{"value":0.95,"cycleCrc":-1.0000},"buyerIndex":{"value":0.95,"cycleCrc":-1.0000}},{"orderNum":2,"keyword":{"value":"无框眼镜"},"keywordGbk":"%CE%DE%BF%F2%D1%DB%BE%B5","ipvUvIndex":{"value":2463.90,"cycleCrc":0.4314},"seUvIndex":{"value":162316.37,"cycleCrc":-0.1209},"payOrdAmtIndex":{"value":0.95,"cycleCrc":null},"buyerIndex":{"value":0.95,"cycleCrc":null}}]}`
- **调用注意**：
    - **memberId 是必填、且是"目标竞店"的会员ID**（不是本店），从 shopList.json / getLossTopShopList.json / getShopMonitorInfo.json 等接口的 shop.memberId 取；本店自己的引流词榜请用 getMyShopWords.json，不要用本接口传本店 memberId。
    - cateId/cateLevel 必须成对同层级，来源 industryCategory.json；未指定业务类目时默认取一级根节点（cateLevel=1）。
    - `statDate` 是**毫秒时间戳**（与 shopList.json 的 YYYY-MM-DD 字符串不同），前端需 `new Date(value)` 才能格式化，跨接口拼装时要做兼容。
    - `keywordGbk` 字段是**直接字符串、无 value 包装**（与同接口内 keyword / memberId 等 {value} 包装风格不一致），拼接搜索跳转链接直接用：`https://s.1688.com/selloffer/offer_search.htm?keywords=` + `keywordGbk`。
    - `flowSourceType` 是**指标排序 tab 切换**（1=流量指数/2=搜索指数/3=交易指数/**4=买家指数** desc）而非渠道过滤；FT0 返空、**本接口 4 个 tab 全可用**（seachofferKey 中仅 FT1/2/3 可用，FT4 返空——两接口的可用 tab 数不同）。未指定业务意图时**默认传 1** 即可拿标准流量指数榜。
    - `isAdServing` 常返回空对象 `{}`，UI 判断广告标识前需做空判断，不能直接读 .value。
    - `payOrdAmtIndex`/`buyerIndex` 的 cycleCrc 常见 `-1.0` 或 `null`：`-1.0` 表示上期为 0 本期非 0（环比无穷大按满减 100% 显示）、`null` 表示上下期均为 0 或数据缺失，业务上都不代表真实"下滑 100%"，展示时建议改文案为「-」或「新增」。
    - 该接口只做单店维度查询，无分页参数，返回条数为固定 TOP 榜（通常 10~20 条），不需要传 page/pageSize。

---

## 竞店-买家结构对比（本店 vs 竞店）

> **描述**：按买家维度（新老客 / 性别 / 城市…）并列返回**本店（my）**与**竞店（first）**的买家结构占比，用于竞店分析页「买家分析」tab 的双列对比图（饼图 / 柱图）。一次调用只取一个维度，切换维度靠 `scenceName` 枚举。

### 接口内容

- **接口地址**：https://sycm.1688.com/ms/compete/competeShop/shopBuyerAnalysis.json
- **请求方法**：GET
- **接口作用**：按指定买家维度（`scenceName`）并列返回本店（my 数组）与竞店（first 数组）的买家结构占比数据。每个维度返回若干条 `{scenceValue, scoreRate, rank}` 明细，`scoreRate` 是该维度值在店铺买家中的占比（0~1 小数）、`rank` 是维度内排名。是竞店分析「买家分析」tab 各子视图（新老客占比 / 性别分布 / 城市 TOP10）的统一后端。
- **入参**：
    - dateRange：String，必填，日期区间，示例 2026-07-21|2026-07-27
    - dateType：String，必填，时间粒度，RECENT_7/RECENT_30
    - cateId：int，必填，类目ID，示例 54，通过/compete/industryCategory 接口获取（未指定业务类目时默认取一级根节点）；本接口顶层无 cateLevel 参数，但**明细行内会回显 cateLevel1Id**
    - device：String，必填，端别，ALL（全部）/ PC / WIRELESS
    - scenceName：String，必填，买家维度枚举，有效值：
      - `byr`：新老客占比（返回「新客/老客」2 行）
      - `sex`：性别占比（返回「男/女」2 行）
      - `city`：城市 TOP10 占比（返回买家所在城市 TOP10，10 行）
      - `class_type`：**买家身份/人群分类**占比（固定 11 类：专业家庭女性、专业家庭男性、专业年轻女性、专业年轻男性、企业自采、其他、内容&社交电商、实体店(含摊主)、平台电商、潜力买家、跨境；同侧 scoreRate 累加 ≈ 1）
      - `cgdj`：**采购等级**占比（固定 7 档：L0/L1/L2/L3/L4/L5/L6，即 1688 买家采购力等级；同侧 scoreRate 累加 ≈ 1）
      - `fgl`：**复购力/回头率**（**特殊：只返 1 行** `scenceValue="回头率"`，`scoreRate` 即回头率本身，如 0.2425=24.25%；不是分类占比，累加语义不适用）
      - 其它常见候选（age/province/region/stage/lifeCycle/buyerStage/buyerAge/tradeType/identityType/userTag/biz/cateSecId/shopFrom 等）code=0 但 my/first 均返回空数组，业务上不建议传（可能是无权限维度或类目无数据）
    - memberId1：String，必填，**目标竞店会员ID**（形如 `b2b-` + 18 位字母数字），从竞店监控/竞店排行接口获取，禁止凭记忆填写
    - memberId2：String，选填，第二个竞店会员ID（页面支持三方对比时使用）；不用时传字符串 `"null"`
    - _：Long，选填，防缓存时间戳
- **出参核心字段**：
    - data.my：数组，**本店**该维度买家结构明细（每项一个维度值）
    - data.first：数组，**竞店（memberId1 对应店）**该维度买家结构明细，结构与 my 完全对称
    - data.my[].scenceName：String，回显入参 scenceName（byr/sex/city…）
    - data.my[].scenceValue：String，该维度的具体取值（如 byr → "新客"/"老客"、sex → "男"/"女"、city → "镇江"/"上海"…）
    - data.my[].scoreRate：float，该维度值的占比（0~1 小数，如 0.3616 = 36.16%）；单店内**同一 scenceName 下 scoreRate 累加为 1**（city 维度只返 TOP10，剩余归其它，累加可能 <1）
    - data.my[].rank：int，该维度内排名（1 起，按 scoreRate 降序）
    - data.my[].statDate：Long，统计日期毫秒时间戳（**注意此接口 statDate 为直接数值，无 {value} 包装**）
    - data.my[].cateLevel1Id：int，回显一级类目ID（与入参 cateId 对应）
- **出参示例**：
    - `{"code":0,"data":{"my":[{"statDate":1785081600000,"scenceValue":"新客","scoreRate":0.3616,"rank":1,"scenceName":"byr","cateLevel1Id":54},{"statDate":1785081600000,"scenceValue":"老客","scoreRate":0.6516,"rank":2,"scenceName":"byr","cateLevel1Id":54}],"first":[{"statDate":1785081600000,"scenceValue":"新客","scoreRate":0.64,"rank":1,"scenceName":"byr","cateLevel1Id":54},{"statDate":1785081600000,"scenceValue":"老客","scoreRate":0.4,"rank":2,"scenceName":"byr","cateLevel1Id":54}]}}`
- **调用注意**：
    - **一次调用只取一个维度**（scenceName 是单值不是逗号列表），前端多维度对比 tab 需按维度分别调用后合并展示。已知有效值：`byr`（新老客，2 行）/`sex`（性别，2 行）/`city`（城市 TOP10，10 行）/`class_type`（买家身份人群分类，11 行）/`cgdj`（采购等级 L0~L6，7 行）/`fgl`（复购力/回头率，**特殊单行指标**）；其它维度接口返回 code=0 但数据为空，除非页面 UI 明确暴露入口，否则不建议盲传。
    - `memberId1` 是**必填、目标竞店会员ID**（不是本店），本店自动从登录态取，无需传；`memberId2` 用于三方对比场景，不用时传字符串 `"null"`（URL 上体现为 `memberId2=null`），不要漏传导致签名/后端校验失败。
    - **statDate 是直接数值毫秒时间戳**（`statDate: 1785081600000`），与本文件其它接口 `{value: ...}` 包装的 statDate 不同，代码取值时不能用 `.value`，做统一格式化前要按接口做类型判断。
    - `scoreRate` 单位是 0~1 小数（如 0.36 表示 36%），前端展示要 ×100 加 "%"；byr/sex/class_type/cgdj 是**分类占比**（同侧累加 ≈ 1），city 是**TOP10 占比**（累加 <1，如需「其它」桶要前端补齐），`fgl` 是**单值指标**（scoreRate 就是回头率本身，不涉及累加），不同维度语义差异要区分渲染。
    - 本店（my）与竞店（first）返回结构完全对称，可直接用同一渲染模板；一侧无数据时该侧数组为 `[]`（**不是 null**）。
    - dateType/dateRange 建议成对传（RECENT_7 → 近 7 天区间，RECENT_30 → 近 30 天区间），否则可能取到默认周期非预期。
    - cateId 必填但**顶层无 cateLevel** 入参（后端从 cateId 反查），来源仍是 industryCategory.json；未指定业务类目时默认取一级根节点 cateId。

---

## 市场-商品排行列表

> **描述**：获取指定类目下行业商品排行列表，是商品排行 tab 的主接口。

### 接口内容

- **接口地址**：https://sycm.1688.com/ms/compete/slrRank/getItmRank.json
- **请求方法**：GET
- **接口作用**：市场-商品排行主接口（对应页面 `/ms/rival/productRank`），按类目+周期+榜单类型返回**行业内商品** TOP 榜单。每行含 `item`（商品基础信息）+ `shop`（所属店铺信息）+ 5 大指数（访客/搜索/交易/询盘/飙升）+ 3 类目评分（销量/复购/好卖）+ 各子榜绝对排名 + 品牌/工厂标识。**是"看行业里谁在爆"的主入口**，与竞品分析（本店已监控竞品）互补。
- **入参**：
    - dateType：String，必填，时间粒度，示例 RECENT_7
    - dateRange：String，必填，日期区间，格式 YYYY-MM-DD|YYYY-MM-DD，示例 2026-07-21|2026-07-27（**缺则返 1003 参数非法**）
    - order：String，选填，排序方向，示例 desc
    - orderBy：String，必填，排序字段，与 tabFlag 保持一致，可选 payOrdAmtIndex（热销榜）/ ipvUvIndex（热访榜）/ seUvIndex（热搜榜）/ seSpvChangeRate（飙升榜）/ activeInquiryUserIndex（询盘榜）
    - device：String，必填，端别，ALL（全部）/ PC / WIRELESS
    - cateId：int，必填，类目ID（须在 industryCategory.json 授权范围内，如 54，`cateId=13` 不在授权时返 1003），通过 /compete/industryCategory 获取
    - cateLevel：int，必填，类目层级，与 cateId 层级一致，示例 1
    - tabFlag：String，必填，榜单 tab 标识，与 orderBy 同枚举（payOrdAmtIndex/ipvUvIndex/seUvIndex/seSpvChangeRate/activeInquiryUserIndex）
    - flag：String，必填，榜单筛选标识，示例 `all`（**必传，缺则 1003**；页面唯一取值 `all`）
    - page：int，选填，当前页，示例 1
    - pageSize：int，选填，分页大小，示例 10
    - addressLevel：int，必填，地域层级，示例 0
    - addressName：String，必填，地域名称，示例 `全国`（默认）
    - indexCode：String，必填，指标列表逗号分隔，页面实际传 `payOrdAmtIndex,ipvUvIndex,seUvIndex,seSpvChangeRate,activeInquiryUserIndex`（payRate/payItmCnt 为无效枚举，不返对应字段）
    - buyerIdentity：**非必填**（真实页面并不发送），可省略；如误传 total 不影响
- **出参核心字段**（每行同时含以下所有块，绝大多数字段是 `{value}` 包装）：
    - data.recordCount：int，本类目+周期下总记录数（示例 200 = 页面 TOP200 上限）
    - data.data[].orderNum：int 或 rank：{value} —— 本页/全局排名（rank=1 为榜首）
    - data.data[].item：商品基础信息块（offerId / offerTitle / detailUrl / minPrice / maxPrice / basePrice / offerImageUrl(需拼 https://cbu01.alicdn.com/ 前缀) / offerUpdateTime / offerExpireTime / categoryID / memberId / class）
    - data.data[].shop：**所属店铺信息块**（memberId / shopName / shopUrl / tradeMedalGrade 如 "AAAAA" / identity 如 "svip" / realBusiness bool / tp bool 精铺 / class）——可直接取到卖家店铺信息不用二次查询
    - data.data[].itemId：int/{value}，商品 offerId
    - data.data[].memberId：{value} 卖家 memberId 字符串
    - data.data[].statDate：{value:"YYYY-MM-DD"} —— **字符串格式**（与本文档大多数 sycm/compete/ 接口的毫秒时间戳不同，兼容时要判断）
    - data.data[].ipvUvIndex / seUvIndex / payOrdAmtIndex / activeInquiryUserIndex / seSpvChangeRate：{value} 5 大核心指数（浮点，指数化）
    - data.data[].payOrdAmtRank / ipvUvRank / activeInquiryUserRank：{value} 各子榜的**行业绝对排名**（如 payOrdAmtRank=1 表示当前商品在类目支付金额榜第 1 名）—— 可用于跨榜单交叉判断（例：ipvUvRank 靠前但 payOrdAmtRank 靠后 = 高流量低转化）
    - data.data[].cateScoreXy / cateScoreFh / cateScoreHm：{value} 类目**销量 / 复购 / 好卖**评分（0~5 浮点）
    - data.data[].scorexy / scorefh / scorehm：{value} 上述评分的**数值化标签**（保留 2 位小数，如 4.64）
    - data.data[].repeatRate：{value} **回购率**（0~1 浮点，如 0.2773 = 27.73%）
    - data.data[].isPm / isZgcSlr / isCjgcSlr：{value:"Y"/"N"} —— 品牌店 / 中国工厂 / 超级工厂 标识
- **出参示例**：
    - `{"code":0,"data":{"recordCount":200,"data":[{"rank":{"value":1},"itemId":{"value":1291679362},"memberId":{"value":"<竞店D memberId>"},"statDate":{"value":"2026-07-27"},"item":{"offerId":1291679362,"offerTitle":"...","detailUrl":"https://detail.1688.com/offer/<offerId>.html","minPrice":0.99,"maxPrice":3.99,"basePrice":"0.99","categoryID":201331602,"offerImageUrl":"img/ibank/<图片标识>.jpg","offerUpdateTime":"2026-07-28 17:16:33","offerExpireTime":"2036-07-10 10:14:28","memberId":"<竞店D memberId>"},"shop":{"memberId":"<竞店D memberId>","shopName":"<示例竞店D名称>","shopUrl":"https://<店铺标识>.1688.com","tradeMedalGrade":"AAAAA","identity":"svip","realBusiness":true,"tp":true},"payOrdAmtIndex":{"value":28596.53},"ipvUvIndex":{"value":16506.19},"seUvIndex":{"value":143480.48},"activeInquiryUserIndex":{"value":2345.06},"seSpvChangeRate":{"value":0.4147},"payOrdAmtRank":{"value":1},"ipvUvRank":{"value":578},"activeInquiryUserRank":{"value":32},"cateScoreXy":{"value":4.16},"cateScoreFh":{"value":4.35},"cateScoreHm":{"value":4.85},"scorexy":{"value":4.64},"scorefh":{"value":4.57},"scorehm":{"value":5.00},"repeatRate":{"value":0.2773},"isPm":{"value":"Y"},"isZgcSlr":{"value":"Y"},"isCjgcSlr":{"value":"Y"}}]}}`
- **调用注意**：
    - **必带 `flag=all` 和 `dateRange`**，缺任一个直接 1003 参数非法。
    - **buyerIdentity 不是必填**（真实页面不发送），可省略。
    - **cateId 必须在授权范围**（同 industryCategory.json），非授权类目 → 1003。
    - **response 里返 shop{} 块**，可直接拿到店名/店铺 url/身份/精铺/AAAAA 勋章，省一次 shop 详情查询。
    - **statDate 是 YYYY-MM-DD 字符串**（本接口特例，与 competeShop/shopList.json 一致，但和 competeOffer/getCompeteList.json 的毫秒时间戳不同，做时间聚合要显式解析）。
    - **子榜绝对排名（payOrdAmtRank/ipvUvRank/activeInquiryUserRank）是全类目排名**，不受 pageSize/page 影响——可用来判断"当前商品在类目里全局第几"，也可交叉：例如 `ipvUvRank<10 && payOrdAmtRank>100` = 高流量低转化爆款候选。
    - 记录总数 `recordCount=200` 就是页面 TOP200 上限，翻页超出会返空。
    - **回购率 repeatRate = 0.2773** 直接就是回购比率，不用再除任何值；类目均值一般 0.10~0.30，>0.30 属高粘性单品。
    - `indexCode` 传的字段决定 response 里返哪几个指数——payRate/payItmCnt 不返对应字段，页面固定传 `payOrdAmtIndex,ipvUvIndex,seUvIndex,seSpvChangeRate,activeInquiryUserIndex` 5 项。
    - 与店铺排行 `slrRank/getShopRank.json` 是姊妹接口（结构类似，行单位从商品换成店铺）——两者都需 flag=all，不带就 1003。

---

## 竞品-监控竞品列表（已配置监控的竞品全维度指数）

> **描述**：返回**本店已加入监控**的竞品(商品)在指定周期、类目下的多维指数榜单，是竞品监控 tab 主列表接口，也是竞品分析入口——所有后续按 `offerId` 下钻的竞品接口（seachofferKey / ipvUvSourceV2 / getOfferCoreIndex / getOfferCoreIndexTrend）都要先从这里挑一个 `item.offerId` 才能调用。列表元素含商品基础信息 (`item`) + 所属店铺信息 (`shop`) + 访客/成交/买家/加购/收藏多维指数与环比。

### 接口内容

- **接口地址**：https://sycm.1688.com/ms/compete/competeOffer/getCompeteList.json
- **请求方法**：GET
- **接口作用**：按类目+周期返回**本店已监控的竞品(商品)**多维指数榜单，支持排序与分页。每行含 `item`（商品基础信息：offerId/标题/主图/价格区间/上下架时间/categoryID/basePrice）、`shop`（所属店铺基础信息：店名/店铺URL/交易勋章/身份 svip/精铺 tp）以及 5 类指数：访客指数、支付金额指数、买家指数、加购买家指数、收藏买家指数，并附访客/支付金额环比。是竞品分析所有单品下钻接口（seachofferKey / ipvUvSourceV2 / getOfferCoreIndex 等）的**上游 offerId 来源**。
- **入参**：
    - dateRange：String，必填，日期区间，示例 2026-07-20|2026-07-26
    - dateType：String，必填，时间粒度，RECENT_7/RECENT_30
    - cateId：int，必填，类目ID，示例 54，通过/compete/industryCategory 接口获取（未指定业务类目时默认取一级根节点）
    - cateLevel：int，必填，类目层级，需与 cateId 层级一致，示例 1
    - device：String，必填，端别，ALL（全部）/ PC / WIRELESS
    - orderBy：String，选填，排序字段，默认 payOrdAmtIndex，可用 ipvUvIndex/buyerIndex/cartBuyrIndex/cltByrIndex 等
    - order：String，选填，排序方向，asc/desc
    - page：int，选填，页码，示例 1
    - pageSize：int，选填，分页大小，示例 60（受监控总数上限约束，详见调用注意）
    - _：Long，选填，防缓存时间戳
- **出参核心字段**：
    - data.data：数组，每项一个已监控竞品行
    - data.recordCount：int，总监控竞品数（等于本店当前监控名单规模）
    - data.data[].itemId：{value} 竞品商品ID（与 item.offerId 冗余，字符串形式）
    - data.data[].memberId：{value} 竞品所属店铺会员ID（与 item.memberId / shop.memberId 冗余）
    - data.data[].statDate：{value} 统计日期，**毫秒时间戳**（如 1784995200000 → 2026-07-26）
    - data.data[].item：竞品商品基础信息子对象
      - `offerId`：Long，商品ID
      - `offerTitle`：String，商品标题
      - `offerImageUrl`：String，主图路径（拼 `https://cbu01.alicdn.com/` 前缀）
      - `detailUrl`：String，商品详情页 URL
      - `minPrice` / `maxPrice`：float，价格区间
      - `basePrice`：String，基础价（等同 minPrice 字符串形式）
      - `categoryID`：int，商品所属叶子类目ID（**不是本接口入参 cateId**，是商品自己挂载的三级类目）
      - `offerUpdateTime` / `offerExpireTime`：String，商品更新/过期时间（YYYY-MM-DD HH:mm:ss）
      - `memberId`：String，所属店铺会员ID
    - data.data[].shop：所属店铺基础信息子对象 { shopName, shopUrl, memberId, identity（如 svip）, tradeMedalGrade（AAAA/AAAAA…）, realBusiness(bool), tp(bool), class }
    - 指数类字段（**仅 value，无 cycleCrc**，环比另有专字段）：
      - data.data[].ipvUvIndex：{value} 访客指数
      - data.data[].payOrdAmtIndex：{value} 支付金额指数
      - data.data[].buyerIndex：{value} 买家指数
      - data.data[].cartBuyrIndex：{value} 加购买家指数
      - data.data[].cltByrIndex：{value} 收藏买家指数
    - 环比比率字段（**均为 {value}，非 cycleCrc 结构**）：
      - data.data[].ipvUvRate：{value} 访客环比变化率
      - data.data[].payOrdAmtRate：{value} 支付金额环比变化率
- **出参示例**：
    - `{"code":0,"data":{"recordCount":41,"data":[{"itemId":{"value":"776899961846"},"statDate":{"value":1784995200000},"item":{"offerId":776899961846,"offerTitle":"<示例商品标题>","offerImageUrl":"img/ibank/O1CN01kqBmgq250Z...","detailUrl":"https://detail.1688.com/offer/<offerId>.html","minPrice":10.0,"maxPrice":15.0,"basePrice":"10.0","categoryID":1031922,"memberId":"<竞店A memberId>"},"shop":{"shopName":"<示例竞店A名称>","tradeMedalGrade":"AAAA","identity":"svip","tp":true,"realBusiness":true,"memberId":"<竞店A memberId>"},"ipvUvIndex":{"value":4208.26},"ipvUvRate":{"value":-0.0205},"payOrdAmtIndex":{"value":4421.99},"payOrdAmtRate":{"value":0.0481},"buyerIndex":{"value":181629.05},"cartBuyrIndex":{"value":60170.59},"cltByrIndex":{"value":48202.73},"memberId":{"value":"<竞店A memberId>"}}]}}`
- **调用注意**：
    - 本接口返回**仅限本店已加入监控的竞品**（未监控的竞品不会出现），不是行业全量竞品排行；如需在监控外发现新竞品应走 `/compete/offerDiscern/sameProductOffer/getOfferList.json`（同款识别）或 `/compete/slrRank/getItmRank.json`（行业商品排行），拿到 offerId 后再到「竞店竞品配置」<https://sycm.1688.com/ms/compete/shopOfferSetting> 加入监控。
    - `recordCount` 反映的是**当前监控名单规模**，受"竞店竞品配置"页配额限制（一般总配额约 50），不是接口硬编码上限；`pageSize=60&page=1` 时后端会一次性全返，不触发分页。
    - `cateId`/`cateLevel` 必须成对同层级，来源 industryCategory.json；未指定业务类目时默认取一级根节点（cateLevel=1）；`cateId` 只做**过滤维度**（不匹配的监控竞品不返回）而非授权维度，所以想拉全量监控清单直接传主营一级类目即可。
    - **指数字段只有 value 无 cycleCrc**，环比要从**另有专字段** `ipvUvRate.value`/`payOrdAmtRate.value` 取（这两个字段就是环比变化率 0~1 小数），其它指数（buyerIndex/cartBuyrIndex/cltByrIndex）没有独立环比字段。
    - `item.categoryID` 是**商品自己挂载的叶子类目ID**（如 1031922 表示眼镜下的某个三级子类），跟入参 `cateId` 语义不同，做类目下钻分析别混用。
    - `statDate` 是**毫秒时间戳 {value:1784995200000}**（YYYY-MM-DD 需 `new Date(value)` 转），与 shopList.json 的 YYYY-MM-DD 字符串风格不同。
    - `item.offerImageUrl` 是**相对路径**（如 `img/ibank/O1CN01...jpg`），前端展示要补 `https://cbu01.alicdn.com/` 或 `https://picasso.alicdn.com/` 前缀。
    - **本接口是所有竞品单品下钻接口的上游**：把这里返回的 `item.offerId` 作为 `seachofferKey.json` / `ipvUvSourceV2.json` / `getOfferCoreIndex(Trend).json` 的 `offerId1`/`offerId2` 参数使用。
    - 如果返回「查询失败，查询店铺不在您的监控列表中」——本接口一般不会触发（因为它本身就是拉监控清单），但下钻接口 `getOfferCoreIndex` 等会触发，需先确认目标 offerId 已在监控名单。

---

## 竞品-监控竞品配置清单（轻量：仅返 offerId 列表 + 配额）

> **描述**：返回**本店当前已监控的竞品 offerId 清单 + 配额使用情况**，不带任何指数/店铺信息，是「竞品」维度监控管理的轻量接口。与 `getCompeteList.json`（返回全维度指数榜单）互为姊妹接口——本接口用于**快速判断某 offerId 是否已监控 / 剩余配额还有多少 / 拉全部监控 offerId 列表准备批量操作**，getCompeteList 用于拉全量指数做分析。也是「竞店竞品配置」<https://sycm.1688.com/ms/compete/shopOfferSetting?settingType=1> 页竞品 tab 的底层数据源之一。

### 接口内容

- **接口地址**：https://sycm.1688.com/ms/compete/common/getOfferMonitorCntInfo.json
- **请求方法**：GET
- **接口作用**：查询本店在指定类目下已监控的**竞品**(商品)数量、剩余可加配额以及全部已监控 offerId 列表；配合 `getShopMonitorCntInfo.json`（竞店同类接口，返 memberId 清单 + 配额）使用，可在正式下钻前一次性把「谁在监控 / 还能加几个」摸清楚。
- **入参**：
    - cateId：int，必填，类目ID，示例 54，通过 /compete/industryCategory 接口获取
    - _：Long，选填，防缓存时间戳
    - **注意**：本接口**不需要** `cateLevel`/`dateRange`/`dateType`/`device` 等常见入参，只按 cateId 过滤已监控列表，配额是**账户级**不是类目级。
- **出参核心字段**：
    - data.alreadyMonitorCnt：int，已监控竞品数
    - data.remainMonitorCnt：int，剩余可加监控配额（与已监控数相加 = 总配额 100）
    - data.monitorOfferList：Array<String>，已监控竞品 offerId 列表（字符串数组，长度 = alreadyMonitorCnt）
- **出参示例**：
    - `{"code":0,"data":{"alreadyMonitorCnt":44,"remainMonitorCnt":56,"monitorOfferList":["680093355790","684643653935","702445890245","..."]}}`
- **调用注意**：
    - **竞品总配额 100（`alreadyMonitorCnt + remainMonitorCnt = 100`）**，与竞店配额（一般 50）独立计数；加新竞品前先调本接口确认 `remainMonitorCnt > 0`，若已满需先在 shopOfferSetting 页移除低价值监控项。
    - **`monitorOfferList` 是全量拉取**（不分页），44 条一次性返回，字符串型 offerId 直接可作为 `getCompeteList.json`/`seachofferKey.json`/`ipvUvSourceV2.json` 等下钻接口的 `offerId1` 参数。
    - 检测「某 offerId 是否已监控」直接 `monitorOfferList.includes(String(offerId))`；本接口返回速度快（<200ms），适合在批量加监控前循环去重。
    - 本接口**不区分周期**（无 dateRange/dateType 入参），返回的是**当前监控名单的静态快照**；配额和列表是账户级实时状态，改动后立刻生效但下钻指数接口可能有几秒延迟。
    - 与 `getCompeteList.json` 的差异：getCompeteList 按类目+周期返回**全维度指数榜单**（含 item/shop/5 类指数/环比），本接口只返 **offerId 字符串数组 + 计数**，Payload 小 100 倍，适合做「是否监控」的前置校验，不适合做分析。
    - 竞店维度对应接口是 `common/getShopMonitorCntInfo.json`（返 `alreadyMonitorCnt` + `monitorShopList: [memberId,...]` + 配额），两者搭配使用可一次性完整评估监控名单状态。
    - `cateId` 传行业一级根节点（如 54）会返账户下**全部已监控竞品**（不按类目过滤，或过滤松），如果传三级叶子类目会只返该类目下的已监控 offerId——想拉全量监控清单直接传主营一级类目。

---

## 竞品-引流搜索词列表

> **描述**：获取单个竞品在指定流量渠道下的 TOP 引流搜索关键词排行，是竞品分析「流量分析」中查看某竞品靠哪些搜索词引流的接口。

### 接口内容

- **接口地址**：https://sycm.1688.com/ms/compete/competeOffer/seachofferKey.json
- **请求方法**：GET
- **接口作用**：获取单个竞品(商品)在指定流量渠道下的 TOP 引流搜索关键词排行，返回每个关键词的 keyword（明文）、keywordGbk（GBK 编码，用于拼搜索跳转链接）及多维度指数：ipvUvIndex（访客指数）、seUvIndex（搜索访客指数）、payOrdAmtIndex（支付金额指数），并含 orderNum（排名）、statDate（统计日期）、memberId（竞品所属店铺）。
- **入参**：
    - dateRange：String，必填，日期区间，示例 2026-07-21|2026-07-27（RECENT_30 传对应30天区间）
    - dateType：String，必填，时间粒度，示例 RECENT_7（可选 RECENT_30）
    - cateId：int，必填，类目ID，示例 54，通过/compete/industryCategory 接口获取可选类目
    - cateLevel：int，必填，类目层级，示例 1
    - offerId：Long，必填，目标竞品商品ID，示例 944828328296，需先通过竞品监控/识别拿到
    - flowSourceType：int，必填，**指标排序 tab 切换**（不是流量渠道过滤器）——1=按 `ipvUvIndex`（流量指数）desc / 2=按 `seUvIndex`（搜索指数）desc / 3=按 `payOrdAmtIndex`（交易指数）desc；同一 offerId + 日期窗口下，FT1 与 FT2 返回**同一 keyword 池换排序**（10 行完全一致），FT3 会**过滤 `payOrdAmtIndex.value ≈ 0.9527...` 的脱敏 magic 行**再按剩余有效交易词 desc、可能引入 FT1/2 榜外的新词补位；0 及 ≥4 返回空数组
    - device：String，必填，端别，ALL（全部）/ PC / WIRELESS
    - _：Long，选填，防缓存时间戳
- **出参核心字段**：
    - data：数组，每项一个引流关键词
    - data[].keyword：{value} 关键词（UTF-8 明文，用于展示）
    - data[].keywordGbk：{value} 关键词 GBK 编码（用于拼接 1688 搜索跳转链接）
    - data[].itemId：{value} 所属竞品商品ID
    - data[].ipvUvIndex：{value,cycleCrc} 该词带来的访客指数
    - data[].seUvIndex：{value,cycleCrc} 该词搜索访客指数
    - data[].payOrdAmtIndex：{value,cycleCrc} 该词支付金额指数
    - data[].orderNum：int，排名序号
    - data[].statDate：统计日期
    - data[].memberId：{value} 该 offer 的**真实所属店铺会员ID**（不一定是"竞品所属"）——如果传入的 offerId 恰好是本店自家商品，memberId 会返回本店会员ID；因此可反过来用它做 ownership 判断（若 memberId=本店 会员ID → 该 offerId 属本店，不是外部竞品）
- **出参示例**：
    - `{"code":0,"data":[{"itemId":{"value":"944828328296"},"keyword":{"value":"老花镜十大名牌"},"orderNum":1,"ipvUvIndex":{"cycleCrc":-0.2021,"value":6532.67},"seUvIndex":{"cycleCrc":-0.0295,"value":281791.48},"payOrdAmtIndex":{"cycleCrc":0.0219,"value":442947.91},"memberId":{"value":"<竞店 memberId>"}}]}`
- **调用注意**：
    - flowSourceType 是**指标排序 tab 切换**、**不是流量渠道过滤器**：同一 offerId+日期窗口下，`flowSourceType=1` 与 `=2` 返回**同一 keyword 池的换排序视图**（TOP10 逐行 keyword 一致，只有 rank 顺序换）；`=3` 会**先剔除 `payOrdAmtIndex.value ≈ 0.9527...` 的脱敏 magic 行**再按剩余交易词 desc、常有 FT1/2 榜外的有效交易词补位。UI 上的"流量指数 / 搜索指数 / 交易指数"三个 tab 直接映射 1/2/3。0 及 4/5/6 均返回空数组 data:[]。**上限 10 行不代表一定 10 行**——同一 offer 不同 flowSourceType 下行数常见 0/3/6/7/10（FT3 因 magic 过滤更容易少于 10 行）；若某 offer 在 1/2/3 全返 0，通常说明该商品无搜索引流数据（已下架/低曝光/未挂类目匹配词）。
    - 指标均为「指数」非绝对值（value 为指数、cycleCrc 为环比变化率，双期均 0 时 cycleCrc 可能为 null）；keyword 用于展示、keywordGbk 用于拼 1688 搜索跳转链接（GBK URL-encoded 形态如 `%D1%DB%BE%B5%BF%F2` = 眼镜框）。该接口按单个 offerId 下钻，可传本店 offerId 也可传外部竞品 offerId（**接口不做 ownership 校验**），memberId 字段回填能直接告诉你这条 offer 属谁。
    - 与本文件其它 competeOffer/* 接口不同，seachofferKey **不受"竞品监控列表"gate**——即使 `getCompeteList.json` 返 data:[]、shopBuyerAnalysis 抛 "商品不在您的监控列表中" (code=1001)，seachofferKey 仍可直接按 offerId 查引流词，是排查监控/权限异常时最稳的活性检测接口。

---

## 竞品-流量来源对比

> **描述**：按流量来源渠道树（市场 → 搜索 / 1688首页推荐 / …），逐节点并列返回「本店商品」与「竞品」的访客/成交/买家/询盘对比数据，是竞品分析「流量来源对比」视图的主接口。

### 接口内容

- **接口地址**：https://sycm.1688.com/ms/compete/competeOffer/ipvUvSourceV2.json
- **请求方法**：GET
- **接口作用**：按流量来源渠道树（含 outerLevel 1 顶级如「市场」、outerLevel 2 二级如「搜索」「1688首页推荐」等，via children[] 递归），逐节点并列返回 offerId1（本店商品）与 offerId2（竞品）的多维对比数据：访客数/指数（IpvUv/IpvUvIndex）、支付金额/指数（PayOrdAmt/PayOrdAmtIndex）、买家指数（BuyerIndex）、下单买家数（PlaceOrderByrCnt）、询盘指数（InquiryIndex）以及本店有效询盘用户数（myEffectiveInQUsers）。
- **入参**：
    - dateRange：String，必填，日期区间，示例 2026-06-01|2026-06-30（月度需与 dateType=MONTH 配套）
    - dateType：String，必填，时间粒度，RECENT_7/RECENT_30/MONTH
    - cateId：int，必填，类目ID，示例 54，通过/compete/industryCategory 接口获取可选类目
    - cateLevel：int，必填，类目层级，示例 1
    - flowSourceType：int，必填，流量类型口径，示例 1（传 1 可返回完整来源树；与 seachofferKey 里的同名参数含义不同）
    - offerId1：Long，必填，本店商品ID，示例 708212074955
    - offerId2：Long，必填，竞品商品ID，示例 680093355790
    - device：String，必填，端别，ALL（全部）/ PC / WIRELESS
    - _：Long，选填，防缓存时间戳
- **出参核心字段**：
    - data：数组，树形结构，每项一个流量来源节点，`children[]` 递归子节点
    - data[].outerLevel：int，层级（1=顶级如「市场」，2=二级如「搜索」）
    - data[].outerId：String，节点ID（如 "1" / "1.1"）
    - data[].outerName：String，渠道名（市场 / 搜索 / 1688首页推荐 …）
    - data[].parentOuterId：String，父节点ID
    - data[].statDate：{value} 毫秒时间戳
    - data[].memberId：{value} 本店会员ID
    - 竞品侧：data[].firstOfferIpvUv（访客数）、firstOfferIpvUvIndex（访客指数）、firstOfferPayOrdAmt（支付金额）、firstOfferPayOrdAmtIndex（支付金额指数）、firstOfferBuyerIndex（买家指数）、firstPlaceOrderByrCnt（下单买家数）、firstInquiryIndex（询盘指数）
    - 本店侧：data[].myOfferIpvUv、myOfferIpvUvIndex、myOfferPayOrdAmt、myOfferPayOrdAmtIndex、myOfferBuyerIndex、myPlaceOrderByrCnt、myInquiryIndex、myEffectiveInQUsers（本店有效询盘用户数）
    - 所有数值字段格式统一为 {value, cycleCrc}，cycleCrc 为环比变化率
    - kkk：{value,cycleCrc} 未明标签字段，数值形态接近 PV/点击类，建议 UI 忽略
- **出参示例**：
    - `{"code":0,"data":[{"outerLevel":1,"outerName":"市场","outerId":"1","parentOuterId":"0","statDate":{"value":1782748800000},"firstOfferIpvUv":{"value":3475,"cycleCrc":-0.2164},"firstOfferPayOrdAmt":{"value":126463.99,"cycleCrc":-0.2667},"myOfferPayOrdAmt":{"value":692.74,"cycleCrc":-0.1389},"myEffectiveInQUsers":{"value":55,"cycleCrc":0.0185},"children":[{"outerLevel":2,"outerId":"1.1","outerName":"搜索","firstOfferIpvUv":{"value":1029},"myOfferIpvUv":{"value":312},"myOfferPayOrdAmt":{"value":457.0,"cycleCrc":1.0141}},{"outerLevel":2,"outerId":"1.2","outerName":"1688首页推荐","firstOfferIpvUv":{"value":413},"myOfferIpvUv":{"value":537}}]}]}`
- **调用注意**：返回是多级树，前端需递归渲染 `children`；每个节点均为双列并排（first* 竞品 / my* 本店），一侧无数据时对应字段可能为 0 或 cycleCrc=null；dateType=MONTH 时 dateRange 传自然月区间，RECENT_7/RECENT_30 时传对应近 7/30 天；此处的 flowSourceType 与 seachofferKey.json 的同名参数含义不同，此接口 flowSourceType=1 已能返回完整市场/搜索/推荐树；kkk 字段命名可疑（可能是内部占位/PV 类），使用前建议忽略。
- ⚠️ **经网关调用时双列字段命名不对称（必读）**：返回 key 被汉化后，竞品侧保留 `first` 前缀、**本店侧的访客数与支付金额却丢掉了 `my` 前缀**：
    - 本店访客数 = **`访客数`**（不是 `my访客数`）；本店支付金额 = **`支付金额`**
    - 竞品访客数 = `firstOffer访客数`；竞品支付金额 = `firstOffer支付金额`；竞品下单买家数 = `first下单买家数`；竞品询盘 = `firstInquiry指数值`
    - 仅 `my下单买家数` / `myInquiry指数值` / `my有效询盘用户数` 保留 my 前缀；`买家指数` / `流量指数` / `交易指数` 为无前缀的本店侧指数
    - 节点属性：渠道名 = `流量来源名称`（非 `outerName`）、层级 = `来源层级`、节点ID = `流量来源ID`、父节点 = `流量父来源ID`
    - 🚨 **切勿用 `my*` 前缀统一扫本店字段**，否则本店访客/成交会全读成空，得出“本店无流量”的错误结论。
- **流量来源树结构补充**：
    - **根节点固定 4 个**（顺序稳定）：`市场` / `其他` / `自主访问` / `互动`，parentOuterId 均="0"，outerLevel=1；每个 root 的 children 顺序：
        - **市场 (outerId=1)** → 5 个二级：搜索 / 1688首页推荐 / 平台导购 / 旺铺 / 商品详情
        - **其他 (outerId=2)** → 1 个二级：其他（仅占位）
        - **自主访问 (outerId=3)** → 4 个二级：进货单 / 买家后台 / 关注的店铺（会员号） / 收藏夹
        - **互动 (outerId=4)** → 2 个二级：旺旺 / 分享
    - outerLevel=2 节点是**叶子**（children:[] 空数组），本接口只到 2 级，无更深钻取。
    - `device` 参数除 ALL（全部）外，**WIRELESS（无线）也可用**（返回完整 4 根树）；device 值语义等同其它 sycm 接口。
    - `data[].memberId`（仅出现在 outerLevel=2 子节点）**等于竞品 offerId2 所属店铺的 memberId**（不是本店 memberId），可作为反查竞店 memberId 的旁路数据。
    - InquiryIndex 与 EffectiveInQUsers 只在部分节点有值（自主访问/互动 子渠道多为 0）；`firstInquiryIndex` 有 value 但**无 cycleCrc**（不同于其它指标的 {value,cycleCrc} 组合），做环比计算时要判空。
    - `kkk` 字段**根节点非零**（如市场 kkk.value=48）、搜索子节点为 0——形态像**下单/加购/收藏累计计数**但未官方标注，建议不参与业务判断。
    - **flowSourceType 对数据无影响**：flowSourceType=0/1/2/3/4 五个值均返回**完全相同的数据内容**（同一份 4 根 × N 子的树、同一批指标值），**唯一差别**是 outerId 的编号方式——flowSourceType=1 时按遍历顺序编号（市场=1/其他=2/自主访问=3/互动=4），其它值均按"优先级重排"（市场=1/自主访问=2/互动=3/其他=4）。**推论**：本接口的 flowSourceType 是**空转参数**，不真的做流量渠道过滤，前端仅用它决定 tab 视觉高亮次序；**代码里识别节点务必用 `outerName`（稳定），不要用 `outerId`（会因 flowSourceType 而变）**。此结论与 seachofferKey.json 的 flowSourceType 语义（1/2/3 各返一份不同渠道 TOP10 词榜）**完全相反**，跨接口调用时切勿套用同名参数含义。

---

## 竞品-买家结构对比（本店商品 vs 竞品商品）

> **描述**：按买家维度（省份 / 城市 / 性别 / 人群 / 采购等级）并列返回**本店商品（my）**与**竞品商品（first / second）**的买家结构占比，用于竞品对比页「买家分析」tab 的双列/三列对比图。一次调用只取一个维度，切换维度靠 `scenceName`。是 `/compete/competeShop/shopBuyerAnalysis.json` 的**商品级平行接口**——同名不同路径，粒度从店铺换成商品。

### 接口内容

- **接口地址**：https://sycm.1688.com/ms/compete/competeOffer/shopBuyerAnalysis.json
- **请求方法**：GET
- **接口作用**：给定本店商品（offerId1）和 1~2 个竞品商品（offerId2 / offerId3），按指定买家维度返回三方买家结构占比排行；返回体结构与 competeShop/shopBuyerAnalysis 完全对称，但对比粒度是商品而非店铺。
- **入参**：
    - dateRange：String，必填，日期区间，示例 2026-07-21|2026-07-27
    - dateType：String，必填，时间粒度，RECENT_7/RECENT_30
    - cateId：int，必填，类目ID，示例 54，从 industryCategory.json 取（本接口顶层无 cateLevel 参数，明细行内回显 cateLevel1Id）
    - device：String，必填，端别，ALL（全部）/ PC / WIRELESS
    - scenceName：String，必填，买家维度枚举，**商品级共 7 个维度可用**：
      - `provice`：省份 TOP10（**注意页面 SPA 拼错为 provice，正确拼写 province 反而返回空数组**，接口原样接受错别字）
      - `city`：城市 TOP10（10 行）
      - `sex`：性别（男/女 2 行）
      - `class_type`：人群分类（**商品级样本小，约 8~10 行**，非固定 11 行；类目定义同 competeShop 版本）
      - `cgdj`：采购等级（**商品级约 5 行**，非固定 L0~L6 全 7 档）
      - `scence_uv`：访客场景来源（该场景访客占比拆解，行数=有数据的场景数，非 TOP-N；device=PC 时接口返回体 scenceName 自动加 `_pc` 后缀成 `scence_uv_pc` 并只返 PC 子集，device=ALL/WIRELESS 返完整全量且不加后缀）
      - `scence_trd`：成交场景来源（该场景成交/交易占比拆解，同 device 后缀规则 `scence_trd_pc`；数值量级明显小于 scence_uv，疑似为「场景成交件数 / 商品总访客数」量级的场景转化率而非 0~1 占比）
      - 与 competeShop 版本的差异：**商品级不支持 `byr`（新老客）和 `fgl`（回头率）**，传入 code=0 但 my/first 均返回空数组；age/stage 等其它维度同样返空
    - offerId1：Long，必填，**本店商品ID**，示例 696581414137
    - offerId2：Long，必填，**竞品商品ID#1**，示例 596492344415
    - offerId3：Long，选填，**竞品商品ID#2**（三方对比时用），不用时传空串（URL 上体现为 `offerId3=`）
    - _：Long，选填，防缓存时间戳
- **出参核心字段**：
    - data.my：**以数字字符串为键的类数组对象**（keys="0","1",…，非真数组，遍历用 `Object.values()`），本店该商品的买家结构明细
    - data.first：同结构，竞品1（offerId2 对应商品）的买家结构明细
    - data.second：同结构，竞品2（offerId3 对应商品）的买家结构明细；**仅当 offerId3 非空时返回**，offerId3 为空时 data 键仅 my/first
    - data.my[].scenceName：String，回显入参 scenceName（provice/city/sex/class_type/cgdj/scence_uv/scence_trd）；**device=PC 时 scence_uv/scence_trd 会被回写为带 `_pc` 后缀的 `scence_uv_pc`/`scence_trd_pc`**，代码做维度分组要 strip 后缀
    - data.my[].scenceValue：String，维度具体取值（如省份名"广东"/城市名"北京"/"男"/"女"/"L0"/"专业年轻女性"；scence_uv/scence_trd 取自流量场景枚举，约 10 个值：`其他`/`旺铺`/`进货单`/`搜索`/`1688首页推荐`/`买家订单`/`旺旺`/`站外`/`分享`/`直接访问`）
    - data.my[].scoreRate：float，该维度值的占比（0~1 小数，如 0.1209 = 12.09%）
    - data.my[].rank：int，同侧内排名，1 起，按 scoreRate 降序
    - data.my[].statDate：Long，统计日期毫秒时间戳（**直接数值，无 {value} 包装**——与其它 competeOffer 接口的 {value:...} 风格不同，但与 competeShop/shopBuyerAnalysis 一致）
    - data.my[].cateLevel1Id：int，回显一级类目ID（与入参 cateId 对应）
- **出参示例**：
    - `{"code":0,"data":{"my":{"0":{"statDate":1785081600000,"scenceValue":"广东","scoreRate":0.1209,"rank":1,"scenceName":"provice","cateLevel1Id":54},"1":{"scenceValue":"山东","scoreRate":0.0989,"rank":2,"scenceName":"provice"}},"first":{"0":{"scenceValue":"浙江","scoreRate":0.2414,"rank":1,"scenceName":"provice"},"1":{"scenceValue":"河北","scoreRate":0.2069,"rank":2}}}}`
- **调用注意**：
    - 与 `/compete/competeShop/shopBuyerAnalysis.json` 是**同名不同路径**的姊妹接口：路径差 competeShop → competeOffer；入参从 memberId1/memberId2 换成 offerId1/offerId2/offerId3；对比粒度从店铺换成商品。业务代码里必须区分完整 URL，别混用。
    - **省份维度 scenceName 用 `provice`（页面拼错，接口原样接受）**，别自作聪明改成正确拼写 `province`，会返回空数组。
    - **商品级维度覆盖比店铺级窄**：仅 provice/city/sex/class_type/cgdj 五个有效；byr/fgl/age/stage/province 全返空。这是商品级买家画像的能力上限，不要盲传店铺级枚举。
    - **class_type 和 cgdj 行数不固定**：店铺级是固定 11/7 行，商品级因样本小约 5~10 行，同侧 scoreRate 累加**不严格等于 1**（缺失类别会被裁掉）；前端渲染按 rank 顺序展示，不要硬拆固定桶。
    - my/first/second 返回是**类数组对象**（keys="0","1",…），不是真数组，前端遍历用 `Object.values()` 或 `for (const k in obj)` 更稳；直接索引 `.length` 会得到 undefined。`offerId3` 空时**没有** second 键，读取要判空。
    - **statDate 是直接数值毫秒**（`statDate: 1785081600000`），代码取值不能加 `.value`；与本文件其它 competeOffer 接口 `{value: ...}` 包装的 statDate 风格不同，做统一格式化前要按接口做类型判断。
    - **无 cycleCrc、无环比**：本接口只输出当期占比，需要环比对比要自己拉两次不同 dateRange 手动差分。
    - `scoreRate` 单位是 0~1 小数（如 0.24 表示 24%），前端展示要 ×100 加 "%"；city/provice 是 TOP10 占比（累加 <1，剩余需前端补「其它」桶），sex 是分类占比（累加=1），class_type/cgdj 是**样本裁剪后的排行占比**（累加可能明显 <1，不要按等式校验）。
    - **scence_uv/scence_trd 是"场景来源"维度、不是分类占比**：`scoreRate` 是同一场景**独立占比**（该场景访客数或该场景成交数 ÷ 商品总访客/总成交，或类似分子分母口径），**同侧多行 scoreRate 累加通常 > 1**（可达 2 以上），代码里**绝对不要把这两个维度当分类互斥占比归一化**；行数 = 有数据的场景数，不是 TOP-N 截断，缺场景=真无数据。
    - **scence_uv/scence_trd 的 device 端别语义**：`device=ALL`（全部）与 `device=WIRELESS`（无线）**返回完全一致的全量场景数据**，返回体 scenceName 保持原值（`scence_uv`/`scence_trd`）。`device=PC` 分两种情形：**(a)** 商品在 PC 端有场景数据 → 服务端 flag 触发，接口把 scenceName 回写成带 `_pc` 后缀的 `scence_uv_pc`/`scence_trd_pc`，且只返 PC 子集（行数/scoreRate 明显更小）；**(b)** 商品在 PC 端无场景数据（PC 访客/成交太小或为 0） → 返 `code=0, data:{my:[], first:[]}`，**不加 `_pc` 后缀**、也不报错。所以 device=PC 空返 ≠ 无权限（1001）也 ≠ 参数错误（1003），只是该商品 PC 端没数据；做维度分组前要先 strip `_pc` 后缀，做跨 device 累加/对比前先按有无后缀判定可比性。**scence_trd 数值量级明显小于 scence_uv**（同商品同期 scence_trd 最大值 ≈ scence_uv 的 1/3），别用同一色阶/纵轴画在一张图上。

---

## 商品-买家流失商品识别与竞对对比（dataSource=ITEM）

> **描述**：识别近期出现买家流失的商品（买家浏览过本店商品后，最终在其他店铺的竞对商品下单），一次返回「我的商品客户流失分析」SOP 归因所需的全部数据：流失商品列表与流失明细、我的商品/店铺信息、竞对商品/店铺信息（价格、促销、买家保障、属性、评价、回头率、旺旺响应率、企业资质等）。是「为什么被抢走」的商品级归因主接口。
>
> ⚡ **快捷方式**：优先跑 `cli.py customer_loss`，一条命令完成「裸调全景 + 发散多品佐证 + 交叉汇总」（见「内置快捷命令」第 5 节）；仅当命令未覆盖（如只查单个指定品、看评价原文需另调 `/item/rate`）时才手动调本接口。

### 接口内容

- **接口地址**：/item/customerLoss（**dataSource=ITEM，非 SYCM**；CLI 调用时 `-s ITEM` 或 `--data_source ITEM` 必传，不能沿用默认的 SYCM）
- **请求方法**：POST
- **入参**：
    - item_id：String，选填，指定要分析的（本店）商品ID，必须为纯数字；**不传则从流失商品中随机取一个**（同一商家多次调用会返回不同商品，「选取方式」会在响应中回显）。取值不限于返回的「流失商品ID列表」（该列表只是全量流失商品按 ID 升序截断的前 50 条，不是可传 item_id 的白名单）
- **出参核心字段**（`data.data.data` 三层嵌套，最内层为**中文 key 的对象**）：
    - 流失商品总数：int，全量值（如 1538）
    - 流失商品ID列表：数组，单次最多 50 个（超出截断并在 errorMsg 提示，但「流失商品总数」仍为全量）
    - 买家流失情况.商品ID / 选取方式（「按 item_id 指定」或「未指定商品，随机选取」）
    - 买家流失情况.浏览过该商品的买家数 / 该商品被浏览次数（**均为字符串型数字**，做比较/排序须先转 int）
    - 买家流失情况.买家转而下单的竞对商品数 / 竞对商品ID列表 / 本次对比的竞对商品ID
    - 我的商品 / 竞对商品：商品ID、商品主图（**相对路径**，需拼 `https://cbu01.alicdn.com/` 前缀）、商品标题、商品的属性（数组，`"键:值"` 形式）、商品最低价/最高价（**字符串**如 "60.00"）、商品支持的促销优惠、商品支持的买家保障、商品好评率、商品评价星级、商品评价印象、商品评价数量、商品评价中的履约率
    - 我的店铺 / 竞对店铺：店铺老客回头率、店铺旺旺响应率、企业面积、企业拥有品牌数量、企业成立日期、企业拥有证书专利数量
- **出参示例**：
    - `{"流失商品总数":3,"流失商品ID列表":["111","222","333"],"买家流失情况":{"商品ID":"111","选取方式":"未指定商品，随机选取","浏览过该商品的买家数":"5","该商品被浏览次数":"12","买家转而下单的竞对商品数":2,"买家转而下单的竞对商品ID列表":["9001","9002"],"本次对比的竞对商品ID":9001},"我的商品":{"商品ID":111,"商品标题":"...","商品最低价":"35.00","商品主图":"img/ibank/...jpg"},"我的店铺":{"店铺老客回头率":"32%","店铺旺旺响应率":"95%"},"竞对商品":{"商品ID":9001,"商品标题":"...","商品最低价":"35.0"},"竞对店铺":{"店铺老客回头率":"21%"}}`
- **调用注意**：
    - **调用顺序**：**默认不传 item_id 裸调**，一次拿到流失商品总数 + 50 条ID列表 + 随机一品的完整对比；随后从「流失商品ID列表」里**发散性多挑几个品**带 item_id 再调（约 1.3s/次），用多个品的对比结果交叉佐证，避免只凭随机命中的单品下结论。对比所需的商品、店铺数据本接口已备齐，无需再逐个调商品接口（如需评价原文明细可再调 `/item/rate`，且必须带 startDate/endDate，`yyyyMMdd` 跨度 ≤31 天，不传日期固定返「未查询到符合条件的商品评价数据」）。
    - **字段缺失属常态且无提示**：竞对侧的评价类字段（好评率/星级/数量/印象/履约率）非必现；店铺四个企业资质字段取决于企业档案是否齐全，**本店侧也会缺**（跨 7 家绑定店实测：只有「店铺老客回头率」「店铺旺旺响应率」双侧必现）。解析一律 `dict.get(key, 默认值)`，禁止下标访问；缺失即在结论中注明「该维度无数据」，不得当作 0 或劣势（禁止因本店缺企业面积/成立日期就反推「本店资质不如竞对」）。
    - **字段可得性不能用单店重复采样得出结论**：同一家店重复调 8 次字段集合固定，换店后可能直接少 3 个字段。
    - **静默返空**：无数据时 `data` 为 null，唯一线索在同级 `errorMsg`（如「该商品近期没有出现买家流失, item_id=xxx」「item_id 必须为纯数字, 当前值=xxx」）——必须先读 errorMsg 再判断，切勿误判为接口不可用。无竞对商品时竞对商品/竞对店铺为空对象并在 errorMsg 提示。
    - **部分降级不报错**：单个数据源超时或失败只会缺失对应字段，流失数据仍会返回，success 仍为 true，缺失情况在 errorMsg 中提示，可根据提示重试获取完整数据。
    - **推荐用法（实战验证）**：① **默认不传 item_id 裸调**拿全景；② 从返回的「流失商品ID列表」里**发散性多挑几个品**带 item_id 再查（不必全量 50 个都查，挑 5 个左右即可，命令默认 `sample_n=5` 并发下钻，可调大；挑品可优先「买家转而下单的竞对商品数、浏览买家数」信号强的品，若拿不到这两个字段就随机/按序取样）；③ 多个品的本店 vs 竞对逐字段对标结果互相印证后再下结论，单品的价格/资质劣势要有至少另一个品佐证才敢归因。⚠️ **价差超过 ±30% 时不能当同层竞品对标**（如本店 ¥35~43 的品束是高频触发而非个例）。
    - 与「竞店-客户流失 TOP 竞店排行」（getLossTopShopList，**店铺维度**、SYCM 源）区分：本接口是**商品维度**、ITEM 源，直接给到具体竞对商品的逐字段对比。

### 归因分析建议（先归口再比价，先定性再定量）

拿到多品下钻结果后，按以下四步做归因，不做属性筛选直接看系统给的价差等于拿苹果和橘子比价，结论一定是错的：

1. **按流失严重度排序，而非绝对流量**：主排序键「浏览过该商品的买家数」（流失规模），次排序键「买家转而下单的竞对商品数」（流失宽度）；「该商品被浏览次数」与买家数高度相关，只作参考**不做乘数**（相乘会双重放大流量规模偏差，大流量品天然霸榜）。注意：裸调的「流失商品ID列表」是按商品ID升序截断、**不含逐品流失指标**，排序只能针对已下钻的采样品做。
2. **先筛可比竞品，再做对比**：系统匹配的竞品存在跨层问题（实测 4 品下钻即有 1 品价差超 ±30% 不可对标），**每次调用只返回系统选定的 1 个对比竞对**（「买家转而下单的竞对商品ID列表」只有裸 ID、无属性，且 item_id 无法指定对比哪个竞品），所以筛选对象是系统给的这个竞品：按「商品的属性」（双侧都有，`"键:值"` 数组）比对材质/产品类别/功能是否同类 + 价差 ±30% 内是否同档，不满足即标记「不可比，弃用本次对比」，不得进入后续归因。
3. **可比竞品内做价差归因二分**：① 可比竞品确实更便宜 → **价格型流失**，方向是调价或差异化卖点；② 本店价格持平甚至更低仍流失 → **非价格流失**，排查详情页质量、主图点击率、评价数量与评分、SKU 覆盖度、客服承接。两类流失的优化动作完全不同，不能一刀切。注意数据边界：本接口能支撑的非价格维度是评价四件套（好评率/星级/数量/印象，竞对侧非必现）、促销优惠、买家保障；详情页质量、主图点击率、SKU 覆盖度**不在本接口出参内**，需另找数据源或人工核查。
4. **店铺画像做服务对标**：可比竞品的「店铺老客回头率」「店铺旺旺响应率」（双侧必现）明显高于本店 → 客户粘性差距，补售后与复购链路；「企业面积」等资质字段明显占优 → 对方有规模成本优势，硬拼价格不现实，应做差异化定位。⚠️ 资质四字段（面积/品牌数/成立日期/专利数）缺失率高，**仅在字段真实存在时成立**，缺失一律注明「该维度无数据」，不得反推优劣势。
