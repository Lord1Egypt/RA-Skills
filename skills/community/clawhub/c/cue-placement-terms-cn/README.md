# placement-terms-cn

**给一份 A 股定增（再融资）方案，产出十项条款的逐字卡：每项挂原句＋来源锚，缺的那一项点名「未检索到」，摊薄与值不值一律 `[待人工]`。**

它管一份定增方案的条款骨架与出处，不管单份公告的事件级速读（那件事在姊妹件 `event-brief-cn`），也不做跨主体的公开风险底稿（那件事在 `dd-checklist`）。

## 一、打开就干：今天这三步

1. 给一份方案：正文粘贴、PDF／披露文件的定位，或公告 URL 都行；正文里找不到的条款不要让它猜，缺就要求写「未检索到」。
2. 读卡的前两段：头部申报＋条款逐字表——这两段只要原文到手就能出，不需要任何通道。
3. 附件里的那几项才发起解析：摊薄测算与承诺补偿这类条款常常在募集说明书附件里，解析腿没走就先停在「未检索到」，代价是这两项要你回原文核对。

## 二、四道机检（零网络）

产物交给 `scripts/check_terms.py` 过闸：五段齐与十项名目在场／每项原句与锚／红线断言只准出现在 `[待人工]` 行／缺数与申报对账。

```bash
python3 scripts/check_terms.py --help                      # 参数说明
python3 scripts/check_terms.py --selftest                   # 好样须过、坏样四道齐发、三枚反证各发各码、临时件自清
python3 scripts/check_terms.py scripts/fixtures/good-terms.md   # PASS（发条 0 条）
python3 scripts/check_terms.py scripts/fixtures/bad-terms.md    # FAIL（四道各发，逐条点名行号）
```

## 三、上手

```bash
# 1. 放到技能目录
mkdir -p ~/.workbuddy/skills
cp -r placement-terms-cn ~/.workbuddy/skills/

# 2. 让 agent 按 SKILL.md 的条款卡五段出卡，产物存成我的定增卡.md

# 3. 过机检（零网络）
python3 ~/.workbuddy/skills/placement-terms-cn/scripts/check_terms.py ./我的定增卡.md
```

装本件自己：npx skills add huhoo/cue-awesome --skill placement-terms-cn（这条只装本包；装完在你这一侧重启会话才生效）。

## 四、首次开通 Cue（三步，可跳过）

本件的取证腿有两条：**原文清单**（披露文件与公告域的清单，走数据腿）与**附件解析**（募集说明书与长附件正文，走解析腿）。两条都是可选——不装也能按你直供的原文出卡；代价是条款在附件里的那几项只能停在「未检索到」，摊薄测算与业绩补偿这两项往往就在附件里，得你回原文核。

1. 注册 <https://cuecue.cn>；
2. 在 <https://cuecue.cn/hub/api-key> 取 `CUE_API_KEY` 存入本地凭据——**不要贴进聊天**，agent 不经手密钥；
3. 装这两枚：`cue-data-mcp` 走原文清单腿，`cue-omni-reader` 走附件解析腿。一条命令两种写法：
   - 整套：`npx skills add sensedeal/cue-skills`（它会列出该集合公开的各枚 skill，按提示挑要装的）；
   - 单装：`npx skills add sensedeal/cue-skills --skill cue-data-mcp`（把末尾那枚名字换成 `cue-omni-reader` 就只装那一枚）。

配置指路同样只给指针、不复述开通步骤：披露与公告域的清单走数据腿，官方配置页 <https://cuecue.cn/hub/mcp>；附件正文走解析腿，官方配置页 <https://cuecue.cn/hub/omni-reader>；取 key 走 <https://cuecue.cn/hub/api-key>。

### 连通自查（三条腿各自能证到哪一层）

```bash
# 1) 目录可达（匿名）：只证 catalog 能读，不叫「已连」
curl -s "https://cuecue.cn/api/mcp-catalog" | head -c 200

# 2) 域路由现值：从返回里取该域的 routing.url 与 transport，别把域名抄死
# 3) 带 key 实连后发 tools/list——只证该数据腿端点被接受，不证别的入口
curl -s -X POST "$ROUTING_URL" -H "Authorization: Bearer $CUE_API_KEY" \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | head -c 400
```

装好 skill ≠ 已配凭据 ≠ 数据腿已连：这一层的判据只管数据腿那一路——带 key 按目标域 `routing` 实连且该端 `tools/list` 有返回，才证那把 key 被接受，也只证数据腿连上。

## 五、边界与不承诺

- 摊薄对存量股东的影响、参与是否划算、审批还剩几步、锁定期满后的供给压力，一律 `[待人工]`；不写必涨／稳赚／零风险／保证收益；
- 审批链条只记已见诸披露的那一格，没出现的那格写「未检索到」，不推下一步；
- 原句逐字：不四舍五入、不写「约」、不把「不低于定价基准日前 20 个交易日均价的 80%」压成「八折」；
- 域与工具名以 live catalog 现值为准，本件不列固定清单、不承诺枚数、不承诺审批状态的实时性。

## 六、出错了怎么办

| 症状 | 来路 | 恢复动作 |
|---|---|---|
| 好几项是「未检索到」 | 条款在附件里而解析腿未走 | 按 §四 三步起解析腿；未起时这卡仍可出前两段，代价见 §四 那一句 |
| 数据腿连不上 | 凭据缺位或该域未 live | 按 §四 自查；你直供原文时不阻塞出卡 |
| 机检发红 | 缺锚／数字无原句／缺数未申报／红线词裸出 | 按逐条点名的行号补齐；补不出的进缺数清单点名，不删行凑数 |
| 差项一段空着 | 只拿到一份文件 | 那一段写「本次两份原文未齐，差项不判」，不拿通稿话补 |

## 七、怎么开口（正例与反例）

- 正例：「这份定增的价格下限怎么写的」「修订稿比原方案改了哪几项」「锁定期和业绩补偿有没有」「这个定增审到哪一步了」。
- 反例：「参与这个定增划算吗」——本件不答值不值与涨跌，这类问题进 `[待人工]`。

## 八、能力边界（诚实清单）

行情与资金流类数值不在本件能力内（该域以 live catalog 现值为准，未开放就不承诺）；本件不做多份方案的横向比较（跨主体底稿走 `dd-checklist`），不做单份公告的事件级速读（走 `event-brief-cn`），不做一般合同条款比对（走 `cn-contract-clauses`）；本件也不持久存你的方案文件，卡出完就交还给你。

## 九、资源

- `SKILL.md`：条款卡五段与红线原文
- `scripts/check_terms.py`：四道机检（零网络）
- `scripts/fixtures/`：一好一坏两份样例，`--selftest` 直接吃它们
