# bond-terms-cn

**给一份境内债券发行文件，产出八项逐字卡：发行人、规模与期限、票面利率、发行价格、增信、赎回回售、信息披露、违约条款，每项挂原句＋来源锚；估值与评级一律 `[待人工]`。**

它只管一只债的发行条款怎么写：可转债条款在 `convertible-bond-terms-cn`、定增条款在 `placement-terms-cn`，招股书速览在 `prospectus-digest-cn`，公司公告清单在 `announcement-daily-cn`。募集说明书原文是唯一依据——**发行公告与承销商推介材料都要标明层级**，这条界线是本件存在的理由。

## 一、打开就干：今天这三步

1. 给一份文件：募集说明书、发行公告或推介材料都行；没写的那一项要求它写「未检索到」，不许按同类债惯例补。
2. 读前两段：头部申报＋八项逐字速读——这两段只要文件到手就能出，不需要任何通道。
3. 看规模与利率两格：规模、期限、票面利率逐字；「待定」「询价」「以发行公告为准」不算值，遇到了就让它进缺数清单；评级符号要么同句带锚，要么整行挂 `[待人工]`。

## 二、六道机检（零网络）

产物交给 `scripts/check_bond_card.py` 过闸：五段齐＋八项名目行级在场（每枚名目须占一行，散文里提到不算）／每项原句与锚（书名号内空或只剩一个字算缺原句，「锚：」后面空着也发）／红线断言只准出现在 `[待人工]` 行／齐缺申报恰一枚且与未检索到行数对账／规模与利率项不许用推定语顶替（须有带单位的数字原值）／评级符号不许裸奔（AAA、AA+、AA-、AA、A+、A- 出现在非 `[待人工]` 行而同行无锚即发）。

```bash
python3 scripts/check_bond_card.py --help                          # 参数说明
python3 scripts/check_bond_card.py --selftest                       # 好样须过、坏样六道齐发、六形钉阈各钉一档、临时件自清
python3 scripts/check_bond_card.py scripts/fixtures/good-bond-card.md    # PASS（发条 0 条）
python3 scripts/check_bond_card.py scripts/fixtures/bad-bond-card.md     # FAIL（六道各发，逐条点名行号）
```

## 三、上手

```bash
# 1. 放到技能目录
mkdir -p ~/.workbuddy/skills
cp -r bond-terms-cn ~/.workbuddy/skills/

# 2. 让 agent 按 SKILL.md 的债券卡五段出卡，产物存成我的债券卡.md

# 3. 过机检（零网络）
python3 ~/.workbuddy/skills/bond-terms-cn/scripts/check_bond_card.py ./我的债券卡.md
```

装本件自己：npx skills add huhoo/cue-awesome --skill bond-terms-cn（这条只装本包；装完在你这一侧重启会话才生效）。

## 四、首次开通 Cue（三步，可跳过）

本件的取证腿有两条：**原文取数**（找募集说明书与发行公告原文，走数据腿）与**附件解析**（长附件与多页 PDF，走解析腿）。两条都是可选——不装也能按你直供的文件出卡；代价是违约条款与增信细节只能停在「未检索到」，层级对照也没法自动补，要你人工回原文核。

1. 注册 <https://cuecue.cn>；
2. 在 <https://cuecue.cn/hub/api-key> 取 `CUE_API_KEY` 存入本地凭据——**不要贴进聊天**，agent 不经手密钥；
3. 装这两枚：`cue-data-mcp` 走原文取数腿，`cue-omni-reader` 走附件解析腿。一条命令两种写法：
   - 整套：`npx skills add sensedeal/cue-skills`（它会列出该集合公开的各枚 skill，按提示挑要装的）；
   - 单装：`npx skills add sensedeal/cue-skills --skill cue-data-mcp`（把末尾那枚名字换成 `cue-omni-reader` 就只装那一枚）。

配置指路同样只给指针、不复述开通步骤：找原文走数据腿，官方配置页 <https://cuecue.cn/hub/mcp>；长附件与 PDF 走解析腿，官方配置页 <https://cuecue.cn/hub/omni-reader>；取 key 走 <https://cuecue.cn/hub/api-key>。

### 连通自查（各条腿能证到哪一层）

```bash
# 1) 目录可达（匿名）：只证 catalog 能读，不叫「已连」
curl -s "https://cuecue.cn/api/mcp-catalog" | head -c 200

# 2) 域路由现值：从返回里取该域的 routing.url 与 transport，别把域名抄死
# 3) 带 key 实连后发 tools/list——只证该数据腿端点被接受，不证别的入口
curl -s -X POST "$ROUTING_URL" -H "Authorization: Bearer $CUE_API_KEY" \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | head -c 400
```

装好 skill ≠ 已配凭据 ≠ 数据腿已连：这一层的判据只管数据腿那一路——带 key 按目标域 `routing` 实连且该端 `tools/list` 有返回，才证那把 key 被接受，也只证数据腿连上；解析腿的连通另按它自己那面的判据读。

## 五、边界与不承诺

- 债项估值、估值结果、收益率测算、评级与目标价、是否值得认购一律 `[待人工]`；不出「建议买入／卖出」「评级上调／下调」「必涨」「稳赚」「零风险」「保证收益」；
- 不承诺代客认购：本件不出认购单、不给销售通道、不做包销承诺；
- 未检索到＝照实写「未检索到」，禁以同类债惯例补写，也不写「无该项」顶替；
- 规模与利率逐字：「待定」「询价」「另行公告」「以发行公告为准」「视市场情况」不算值，遇到了进缺数清单；
- 评级符号不许裸奔：同句无锚就整行挂 `[待人工]` 或改写「未检索到」；
- 域与工具名以 live catalog 现值为准，本件不列固定清单、不承诺枚数，也不承诺该域是否开放与原文的实时性。

## 六、出错了怎么办

| 症状 | 来路 | 恢复动作 |
|---|---|---|
| 好几项是「未检索到」 | 文件是摘要件，或原句在附件里 | 起附件解析腿补原句；起不动就保留缺数点名，不补写 |
| 数据腿连不上 | 凭据缺位或该域未 live | 按 §四 自查；前两段仍可出，代价见 §四 那一句 |
| 机检发红 | 缺锚／缺原句／规模利率用推定语／评级裸奔／齐缺不符 | 按逐条点名的行号补齐；补不出的进缺数清单，不删行凑数 |
| 募集说明书与发行公告说法不一致 | 层级不同或条款更新 | 两句原句并列进「口径对照」，各挂各锚，不做判断 |

## 七、怎么开口（正例与反例）

- 正例：「这只债的票面利率和期限怎么写的」「有没有担保、谁担保」「几年后能回售、发行人能不能赎回」「违约和交叉违约条款在哪一条」。
- 反例：「这只债值多少钱」「收益率能到多少」「评级会不会上调」「帮我认购」——估值、测算、评级判断与认购不在本件，一律 `[待人工]`。

## 八、能力边界（诚实清单）

行情与资金流类数值不在本件能力内（该域以 live catalog 现值为准，未开放就不承诺）；本件不做信用分析、不评估违约概率、不比较同类债；本件不判断评级符号的含义，只要求它带出处；本件也不持久存你的文件，卡出完就交还给你。

## 九、资源

- `SKILL.md`：债券卡五段与红线原文（中文面为权威）
- `SKILL.en.md`：同文的英文对照面，冲突以中文面为准
- `references/bond-layers.md`：文件层级与三要素记法速查（含规模利率推定语与评级符号规则）
- `scripts/check_bond_card.py`：六道机检（零网络）
- `scripts/fixtures/`：一好一坏两份样例，`--selftest` 直接吃它们