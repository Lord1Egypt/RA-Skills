# policy-impact-cn

**给一份政策文件，产出要点逐字卡＋受影响环节的候选链：每条链挂政策原文的一句依据与来源锚，因果、涨跌与受益名单一律 `[待人工]`。**

它只管「这份文件写了什么、字面上牵动哪些环节」。一家公司的处罚与监管措施底稿在 `event-risk-scan`，行业面综述在 `sector-overview`，已披露日期入表在 `catalyst-calendar`——这三件事本件都不做。

## 一、打开就干：今天这三步

1. 给一份文件：正文粘贴、PDF／网页链接的定位都行；正文没有的那一格要求写「未检索到」，不许让它按常识补。
2. 读前两段：头部申报＋政策要点逐字——这两段只要原文到手就能出，不需要任何通道。
3. 看链条的挂处：每条环节链都要能指回政策原文的一句依据；指不回的那一级会被剪掉，代价是链条比你预期的短——这是设计，不是缺数。

## 二、四道机检（零网络）

产物交给 `scripts/check_chain.py` 过闸：五段齐与名目在场／每条原句、依据与锚／红线断言只准出现在 `[待人工]` 行／候选链条数与申报一致。

```bash
python3 scripts/check_chain.py --help                        # 参数说明
python3 scripts/check_chain.py --selftest                     # 好样须过、坏样四道齐发、反证各发各码、临时件自清
python3 scripts/check_chain.py scripts/fixtures/good-chain.md     # PASS（发条 0 条）
python3 scripts/check_chain.py scripts/fixtures/bad-chain.md      # FAIL（四道各发，逐条点名行号）
```

## 三、上手

```bash
# 1. 放到技能目录
mkdir -p ~/.workbuddy/skills
cp -r policy-impact-cn ~/.workbuddy/skills/

# 2. 让 agent 按 SKILL.md 的政策卡五段出卡，产物存成我的政策链卡.md

# 3. 过机检（零网络）
python3 ~/.workbuddy/skills/policy-impact-cn/scripts/check_chain.py ./我的政策链卡.md
```

装本件自己：npx skills add huhoo/cue-awesome --skill policy-impact-cn（这条只装本包；装完在你这一侧重启会话才生效）。

## 四、首次开通 Cue（三步，可跳过）

本件的取证腿有两条：**文件清单**（政策与监管域的清单与定位，走数据腿）与**正文解析**（长文件与附件，走解析腿）。两条都是可选——不装也能按你直供的原文出卡；代价是依据句落在附件里时挂不上，环节链只能剪短，时间与窗口表里那三格也可能停在「未检索到」。

1. 注册 <https://cuecue.cn>；
2. 在 <https://cuecue.cn/hub/api-key> 取 `CUE_API_KEY` 存入本地凭据——**不要贴进聊天**，agent 不经手密钥；
3. 装这两枚：`cue-data-mcp` 走文件清单腿，`cue-omni-reader` 走正文解析腿。一条命令两种写法：
   - 整套：`npx skills add sensedeal/cue-skills`（它会列出该集合公开的各枚 skill，按提示挑要装的）；
   - 单装：`npx skills add sensedeal/cue-skills --skill cue-data-mcp`（把末尾那枚名字换成 `cue-omni-reader` 就只装那一枚）。

配置指路同样只给指针、不复述开通步骤：政策与监管域的清单走数据腿，官方配置页 <https://cuecue.cn/hub/mcp>；正文与附件走解析腿，官方配置页 <https://cuecue.cn/hub/omni-reader>；取 key 走 <https://cuecue.cn/hub/api-key>。

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

- 解读、受益与受损判断、执行强度与落地节奏、对任何主体的影响大小一律 `[待人工]`；不写必涨／稳赚／零风险／保证收益，不点名「受益股」「龙头标的」；
- 环节链只到环节为止，末端不接投资结论；一句原文依据挂不住的环节不进链；
- 原句逐字：不四舍五入、不写「约」、不把「分阶段实施」那类限定词省成一句结论；正文没写的日期与期限写「未检索到」，不写「无」也不推断；
- 域与工具名以 live catalog 现值为准，本件不列固定清单、不承诺枚数、不承诺政策文本的实时性。

## 六、出错了怎么办

| 症状 | 来路 | 恢复动作 |
|---|---|---|
| 环节链很短 | 依据句在附件里而解析腿未走 | 按 §四 三步起解析腿；未起时前两段仍可出，代价见 §四 那一句 |
| 数据腿连不上 | 凭据缺位或该域未 live | 按 §四 自查；你直供原文时不阻塞出卡 |
| 机检发红 | 缺锚／依据不是原句／链条数与申报不符／红线词裸出 | 按逐条点名的行号补齐；补不出的进缺数清单点名，不删行凑数 |
| 时间表三格都空 | 正文未见日期与期限 | 逐格写「未检索到」，不拿「无」顶替，也不按惯例补一个日期 |

## 七、怎么开口（正例与反例）

- 正例：「这份新规写了什么、什么时候生效」「这条规定字面上牵动产业链哪些环节」「过渡期和申报窗口怎么填」「正式稿和征求意见稿差在哪」。
- 反例：「这政策利好哪个板块」——本件不答利好利空与名单，这类问题进 `[待人工]`。

## 八、能力边界（诚实清单）

行情与资金流类数值不在本件能力内（该域以 live catalog 现值为准，未开放就不承诺）；本件不做政策解读与影响大小排序，不做具体公司的风险底稿（走 `event-risk-scan`），不做行业综述（走 `sector-overview`），不把日期做成日历（走 `catalyst-calendar`）；本件也不持久存你的政策文件，卡出完就交还给你。

## 九、资源

- `SKILL.md`：政策卡五段与红线原文
- `scripts/check_chain.py`：四道机检（零网络）
- `scripts/fixtures/`：一好一坏两份样例，`--selftest` 直接吃它们
