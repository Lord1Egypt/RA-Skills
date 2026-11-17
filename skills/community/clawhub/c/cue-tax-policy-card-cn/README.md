# tax-policy-card-cn

**给一份境内税务文件，产出八项逐字卡：文号、税种与适用主体、税率、计税依据、施行日期、申报期限、过渡安排、优惠与留存资料，每项挂原句＋来源锚；能省多少税一律 `[待人工]`。**

它只管一份税务文件怎么写：政策影响链在 `policy-impact-cn`，定增与发行条款在 `placement-terms-cn`，公司公告清单在 `announcement-daily-cn`。税务文件的原文是唯一依据——**解读件与地方口径都要标明层级**，这条界线是本件存在的理由。

## 一、打开就干：今天这三步

1. 给一份文件：正文粘贴、官方页面或 PDF 定位都行；没写的那一项要求它写「未检索到」，不许按惯例补。
2. 读前两段：头部申报＋八项逐字速读——这两段只要文件到手就能出，不需要任何通道。
3. 看日期与税率两格：税率逐字、日期逐字；「另行规定」「待定」不算日期，遇到了就让它进缺数清单。

## 二、五道机检（零网络）

产物交给 `scripts/check_tax_card.py` 过闸：五段齐＋八项名目行级在场（每枚名目须占一行，散文里提到不算）／每项原句与锚（书名号内空或只剩一个字算缺原句，「锚：」后面空着也发）／红线断言只准出现在 `[待人工]` 行／齐缺申报恰一枚且与未检索到行数对账／日期项不许用推定语顶替（施行日期与申报期限须有日期或期限原值）。

```bash
python3 scripts/check_tax_card.py --help                          # 参数说明
python3 scripts/check_tax_card.py --selftest                       # 好样须过、坏样五道齐发、五形钉阈各钉一档、临时件自清
python3 scripts/check_tax_card.py scripts/fixtures/good-tax-card.md    # PASS（发条 0 条）
python3 scripts/check_tax_card.py scripts/fixtures/bad-tax-card.md     # FAIL（五道各发，逐条点名行号）
```

## 三、上手

```bash
# 1. 放到技能目录
mkdir -p ~/.workbuddy/skills
cp -r tax-policy-card-cn ~/.workbuddy/skills/

# 2. 让 agent 按 SKILL.md 的税务卡五段出卡，产物存成我的税务卡.md

# 3. 过机检（零网络）
python3 ~/.workbuddy/skills/tax-policy-card-cn/scripts/check_tax_card.py ./我的税务卡.md
```

装本件自己：npx skills add huhoo/cue-awesome --skill tax-policy-card-cn（这条只装本包；装完在你这一侧重启会话才生效）。

## 四、首次开通 Cue（三步，可跳过）

本件的取证腿有两条：**原文取数**（找官方原文与文号，走数据腿）与**附件解析**（长附件与多页 PDF，走解析腿）。两条都是可选——不装也能按你直供的文件出卡；代价是文号与长附件里的条款只能停在「未检索到」，层级对照也没法自动补，要你人工回原文核。

1. 注册 <https://cuecue.cn>；
2. 在 <https://cuecue.cn/hub/api-key> 取 `CUE_API_KEY` 存入本地凭据——**不要贴进聊天**，agent 不经手密钥；
3. 装这两枚：`cue-data-mcp` 走原文取数腿，`cue-omni-reader` 走附件解析腿。一条命令两种写法：
   - 整套：`npx skills add sensedeal/cue-skills`（它会列出该集合公开的各枚 skill，按提示挑要装的）；
   - 单装：`npx skills add sensedeal/cue-skills --skill cue-data-mcp`（把末尾那枚名字换成 `cue-omni-reader` 就只装那一枚）。

配置指路同样只给指针、不复述开通步骤：找官方原文走数据腿，官方配置页 <https://cuecue.cn/hub/mcp>；长附件与 PDF 走解析腿，官方配置页 <https://cuecue.cn/hub/omni-reader>；取 key 走 <https://cuecue.cn/hub/api-key>。

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

- 税率测算结果、税负变化、能省多少税、退税金额一律 `[待人工]`；不出「省税 X 元」「税负下降」这类定量结论，不写必涨／稳赚／零风险／保证收益；
- 不承诺代客申报：本件不出申报表、不给办理通道、不接代办；
- 未检索到＝照实写「未检索到」，禁以旧文或行业惯例补写，也不写「无该项」顶替；
- 日期与文号逐字：「另行规定」「待定」「以…为准」不算日期值，遇到了进缺数清单；
- 域与工具名以 live catalog 现值为准，本件不列固定清单、不承诺枚数，也不承诺该域是否开放与原文的实时性。

## 六、出错了怎么办

| 症状 | 来路 | 恢复动作 |
|---|---|---|
| 好几项是「未检索到」 | 文件是摘要件，或原句在附件里 | 起附件解析腿补原句；起不动就保留缺数点名，不补写 |
| 数据腿连不上 | 凭据缺位或该域未 live | 按 §四 自查；前两段仍可出，代价见 §四 那一句 |
| 机检发红 | 缺锚／缺原句／日期用推定语／齐缺不符 | 按逐条点名的行号补齐；补不出的进缺数清单，不删行凑数 |
| 中央文件与地方口径说法不一致 | 层级不同或口径更新 | 两句原句并列进「口径对照」，各挂各锚，不做适用判断 |

## 七、怎么开口（正例与反例）

- 正例：「这份公告里税率和计税依据怎么写的」「什么时候施行、旧文还作不作数」「申报期限是几号之前」「研发费用加计扣除比例的原话是哪句」。
- 反例：「帮我算算能省多少税」「替我申报」——测算与代办不在本件，一律 `[待人工]`。

## 八、能力边界（诚实清单）

行情与资金流类数值不在本件能力内（该域以 live catalog 现值为准，未开放就不承诺）；本件不做税务筹划、不出申报表、不判断你是否适用；本件不评估地方口径的执行力度，只登记层级与原文；本件也不持久存你的文件，卡出完就交还给你。

## 九、资源

- `SKILL.md`：税务卡五段与红线原文（中文面为权威）
- `SKILL.en.md`：同文的英文对照面，冲突以中文面为准
- `references/tax-layers.md`：文件层级与三要素记法速查（含日期推定语清单）
- `scripts/check_tax_card.py`：五道机检（零网络）
- `scripts/fixtures/`：一好一坏两份样例，`--selftest` 直接吃它们