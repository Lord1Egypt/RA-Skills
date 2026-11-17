# roadshow-minutes-cn

**给一份路演、调研或业绩说明会的纪要，产出八项逐字速读卡：每项挂原句＋来源锚，含数字的那项另带「口头表述，未经披露文件核对」，评级与目标价一律 `[待人工]`。**

它只管一份已成文的纪要读成什么样：公告清单级速览在 `announcement-daily-cn`，单份方案的条款拆解在 `placement-terms-cn`，录音成稿在 `meeting-minutes-cn`。纪要里的话是管理层说的，**不等于公司披露过**——这条界线是本件存在的理由。

## 一、打开就干：今天这三步

1. 给一份纪要：正文粘贴、PDF／披露页定位、录音转写件都行；没写的那一项要求它写「未检索到」，不许按惯例补。
2. 读前两段：头部申报＋八项逐字速读——这两段只要纪要到手就能出，不需要任何通道。
3. 看标注：含金额、比例、产能、家数的那几行必须带「口头表述，未经披露文件核对」；要拿它当事实用，就先起对照腿去找官方投资者关系活动记录表。

## 二、四道机检（零网络）

产物交给 `scripts/check_minutes.py` 过闸：五段齐＋八项名目行级在场（每枚名目须占一行，散文里提到不算）／每项原句、锚与口头表述标注（书名号内空或只剩一个字算缺原句，「锚：」后面空着也发）／红线断言只准出现在 `[待人工]` 行／齐缺申报恰一枚且与清单对账（两处互相矛盾的申报同样发）。

```bash
python3 scripts/check_minutes.py --help                          # 参数说明
python3 scripts/check_minutes.py --selftest                       # 好样须过、坏样四道齐发、八档反证各发各支且各带独有点名句、临时件自清
python3 scripts/check_minutes.py scripts/fixtures/good-minutes.md      # PASS（发条 0 条）
python3 scripts/check_minutes.py scripts/fixtures/bad-minutes.md       # FAIL（四道各发，逐条点名行号）
```

## 三、上手

```bash
# 1. 放到技能目录
mkdir -p ~/.workbuddy/skills
cp -r roadshow-minutes-cn ~/.workbuddy/skills/

# 2. 让 agent 按 SKILL.md 的纪要卡五段出卡，产物存成我的纪要卡.md

# 3. 过机检（零网络）
python3 ~/.workbuddy/skills/roadshow-minutes-cn/scripts/check_minutes.py ./我的纪要卡.md
```

装本件自己：npx skills add huhoo/cue-awesome --skill roadshow-minutes-cn（这条只装本包；装完在你这一侧重启会话才生效）。

## 四、首次开通 Cue（三步，可跳过）

本件的取证腿有两条：**正文解析**（长转写件与多页纪要，走解析腿）与**官方对照**（找公司发布的投资者关系活动记录表来对照转手纪要，走数据腿）。两条都是可选——不装也能按你直供的纪要出卡；代价是所有数字都停在口头表述层，「管理层说产能满了」这类话没法与披露文件对上，要你人工回原文核。

1. 注册 <https://cuecue.cn>；
2. 在 <https://cuecue.cn/hub/api-key> 取 `CUE_API_KEY` 存入本地凭据——**不要贴进聊天**，agent 不经手密钥；
3. 装这两枚：`cue-omni-reader` 走正文解析腿，`cue-data-mcp` 走官方对照腿。一条命令两种写法：
   - 整套：`npx skills add sensedeal/cue-skills`（它会列出该集合公开的各枚 skill，按提示挑要装的）；
   - 单装：`npx skills add sensedeal/cue-skills --skill cue-omni-reader`（把末尾那枚名字换成 `cue-data-mcp` 就只装那一枚）。

配置指路同样只给指针、不复述开通步骤：正文与附件走解析腿，官方配置页 <https://cuecue.cn/hub/omni-reader>；找官方记录表走数据腿，官方配置页 <https://cuecue.cn/hub/mcp>；取 key 走 <https://cuecue.cn/hub/api-key>。

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

- 评级、目标价、涨跌与「这算不算利好」一律 `[待人工]`；不写必涨／稳赚／零风险／保证收益；
- 口头表述不当披露事实：含金额、比例、产能、家数的项行必须带「口头表述，未经披露文件核对」，写不出这行标注的就进缺数清单；
- 未检索到＝照实写「未检索到」，禁按「管理层一般会怎么说」补写，也不写「无」顶替；
- 域与工具名以 live catalog 现值为准，本件不列固定清单、不承诺枚数，也不承诺该域是否开放与记录表的实时性。

## 六、出错了怎么办

| 症状 | 来路 | 恢复动作 |
|---|---|---|
| 好几项是「未检索到」 | 转手纪要本就残缺，或原句在附件里 | 起正文解析腿补原句；起不动就保留缺数点名，不补写 |
| 数据腿连不上 | 凭据缺位或该域未 live | 按 §四 自查；前两段仍可出，代价见 §四 那一句 |
| 机检发红 | 缺锚／缺原句／数字缺口头标注／齐缺不符 | 按逐条点名的行号补齐；补不出的进缺数清单，不删行凑数 |
| 纪要与官方记录表说法不一致 | 转手件改写或漏句 | 两句原句并列进「口径对照」，各挂各锚，不做取舍判断 |

## 七、怎么开口（正例与反例）

- 正例：「这份调研纪要里管理层说了什么」「机构问了哪几个问题、怎么答的」「纪要里的产能和订单数字有没有出处」「这场会谁出席了」。
- 反例：「这算利好吗、要不要加仓」——涨跌与持仓动作不在本件，进 `[待人工]`。

## 八、能力边界（诚实清单）

行情与资金流类数值不在本件能力内（该域以 live catalog 现值为准，未开放就不承诺）；本件不做纪要的口碑或可信度评分，只做逐字与出处登记；本件不判断管理层表态的真伪，只标注它未与披露文件核对；本件也不持久存你的纪要，卡出完就交还给你。

## 九、资源

- `SKILL.md`：纪要卡五段与红线原文（中文面为权威）
- `SKILL.en.md`：同文的英文对照面，冲突以中文面为准
- `references/oral-claims.md`：口头表述与披露事实的分层速查（含四类标注的写法）
- `scripts/check_minutes.py`：四道机检（零网络）
- `scripts/fixtures/`：一好一坏两份样例，`--selftest` 直接吃它们
