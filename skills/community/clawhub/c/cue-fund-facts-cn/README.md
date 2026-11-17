# fund-facts-cn

**给一份境内基金资料，产出八项逐字卡：类型、投资范围、业绩比较基准、管理费与托管费、申赎费用、基金经理、风险等级、分红规则，每项挂原句＋来源锚；打新收益与收益预测一律 `[待人工]`。**

它只管一只基金的公开资料怎么写：政策影响链在 `policy-impact-cn`，债券条款在 `bond-terms-cn`，公司公告清单在 `announcement-daily-cn`。正式文件原文是唯一依据——**销售页面都要标明层级**，这条界线是本件存在的理由。

## 一、打开就干：今天这三步

1. 给一份资料：产品资料概要、招募说明书节选或销售页面都行；没写的那一项要求它写「未检索到」，不许按同类基金惯例补。
2. 读前两段：头部申报＋八项逐字速读——这两段只要资料到手就能出，不需要任何通道。
3. 看费率两格：管理费、托管费、申赎费用逐字；「以基金合同为准」「视渠道而定」不算值，遇到了就让它进缺数清单。

## 二、五道机检（零网络）

产物交给 `scripts/check_fund_card.py` 过闸：五段齐＋八项名目行级在场（每枚名目须占一行，散文里提到不算）／每项原句与锚（书名号内空或只剩一个字算缺原句，「锚：」后面空着也发）／红线断言只准出现在 `[待人工]` 行／齐缺申报恰一枚且与未检索到行数对账／费率项不许用推定语顶替（管理费与托管费、申赎费用须有百分数原值）。

```bash
python3 scripts/check_fund_card.py --help                          # 参数说明
python3 scripts/check_fund_card.py --selftest                       # 好样须过、坏样五道齐发、五形钉阈各钉一档、临时件自清
python3 scripts/check_fund_card.py scripts/fixtures/good-fund-card.md    # PASS（发条 0 条）
python3 scripts/check_fund_card.py scripts/fixtures/bad-fund-card.md     # FAIL（五道各发，逐条点名行号）
```

## 三、上手

```bash
# 1. 放到技能目录
mkdir -p ~/.workbuddy/skills
cp -r fund-facts-cn ~/.workbuddy/skills/

# 2. 让 agent 按 SKILL.md 的基金卡五段出卡，产物存成我的基金卡.md

# 3. 过机检（零网络）
python3 ~/.workbuddy/skills/fund-facts-cn/scripts/check_fund_card.py ./我的基金卡.md
```

装本件自己：npx skills add huhoo/cue-awesome --skill fund-facts-cn（这条只装本包；装完在你这一侧重启会话才生效）。

## 四、首次开通 Cue（三步，可跳过）

本件的取证腿有两条：**原文取数**（找官方概要、合同与招募说明书，走数据腿）与**附件解析**（长附件与多页 PDF，走解析腿）。两条都是可选——不装也能按你直供的资料出卡；代价是风险等级与分红细节只能停在「未检索到」，层级对照也没法自动补，要你人工回原文核。

1. 注册 <https://cuecue.cn>；
2. 在 <https://cuecue.cn/hub/api-key> 取 `CUE_API_KEY` 存入本地凭据——**不要贴进聊天**，agent 不经手密钥；
3. 装这两枚：`cue-data-mcp` 走原文取数腿，`cue-omni-reader` 走附件解析腿。一条命令两种写法：
   - 整套：`npx skills add sensedeal/cue-skills`（它会列出该集合公开的各枚 skill，按提示挑要装的）；
   - 单装：`npx skills add sensedeal/cue-skills --skill cue-data-mcp`（把末尾那枚名字换成 `cue-omni-reader` 就只装那一枚）。

配置指路同样只给指针、不复述开通步骤：找官方资料走数据腿，官方配置页 <https://cuecue.cn/hub/mcp>；长附件与 PDF 走解析腿，官方配置页 <https://cuecue.cn/hub/omni-reader>；取 key 走 <https://cuecue.cn/hub/api-key>。

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

- 打新收益、收益预测、预期收益、年化收益、评级与目标价、是否值得申购一律 `[待人工]`；不出「稳赚」「零风险」「保证收益」「必涨」「保本」；
- 不承诺代客申购：本件不出申购单、不给销售通道、不接代办；
- 未检索到＝照实写「未检索到」，禁以同类基金惯例补写，也不写「无该项」顶替；
- 费率逐字：「以基金合同为准」「详见招募说明书」「视渠道而定」「待定」不算值，遇到了进缺数清单；
- 域与工具名以 live catalog 现值为准，本件不列固定清单、不承诺枚数，也不承诺该域是否开放与资料的实时性。

## 六、出错了怎么办

| 症状 | 来路 | 恢复动作 |
|---|---|---|
| 好几项是「未检索到」 | 资料是节选件，或原句在附件里 | 起附件解析腿补原句；起不动就保留缺数点名，不补写 |
| 数据腿连不上 | 凭据缺位或该域未 live | 按 §四 自查；前两段仍可出，代价见 §四 那一句 |
| 机检发红 | 缺锚／缺原句／费率用推定语／齐缺不符 | 按逐条点名的行号补齐；补不出的进缺数清单，不删行凑数 |
| 概要、合同与销售页面说法不一致 | 层级不同或销售改写 | 两句原句并列进「口径对照」，各挂各锚，不做判断 |

## 七、怎么开口（正例与反例）

- 正例：「这只基金的管理费和托管费是多少」「业绩比较基准怎么写的」「股票仓位范围是多少」「基金经理是谁、什么时候任职」「分红规则怎么定」。
- 反例：「这只基金能赚多少」「打新能增厚多少收益」「帮我挑只更好的」「帮我申购」——收益、推荐与申购不在本件，一律 `[待人工]`。

## 八、能力边界（诚实清单）

行情与资金流类数值不在本件能力内（该域以 live catalog 现值为准，未开放就不承诺）；本件不做基金评价、不预测收益、不比较同类产品；本件不判断风险等级是否与你的风险偏好匹配，只登记文件里怎么写；本件也不持久存你的资料，卡出完就交还给你。

## 九、资源

- `SKILL.md`：基金卡五段与红线原文（中文面为权威）
- `SKILL.en.md`：同文的英文对照面，冲突以中文面为准
- `references/fund-layers.md`：文件层级与三要素记法速查（含费率推定语清单）
- `scripts/check_fund_card.py`：五道机检（零网络）
- `scripts/fixtures/`：一好一坏两份样例，`--selftest` 直接吃它们