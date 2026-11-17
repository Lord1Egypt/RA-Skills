# prospectus-digest-cn

**给一份 A 股招股说明书，产出八项逐字速览卡：每项挂原句＋原文页码锚，发行人自称那句另标「发行人自述」，估值与打新一律 `[待人工]`。**

它只管把几百页的文件读成可以被回原文核对的八行。单份方案的条款拆解在 `placement-terms-cn`，公告清单级速览在 `announcement-daily-cn`，跨主体公开风险底稿在 `dd-checklist`。

## 一、打开就干：今天这三步

1. 给一份招股书：正文粘贴或 PDF／披露页定位；说明是申报稿、上会稿还是注册稿，稿件版本写在头部。
2. 读前两段：头部申报＋八项逐字速览——这两段只要正文到手就能出，不需要任何通道。
3. 盯两类标注：自称与最高级那句要带「发行人自述，无第三方依据」；财务那项的期间与单位照原文留着，不做换算。

## 二、五道机检（零网络）

产物交给 `scripts/check_prospectus.py` 过闸：五段齐＋八项名目行级在场（每枚名目须占一行，散文里提到不算）／每项原句与页码锚（书名号内空或只剩一个字算缺原句；「锚：」后面空着发；锚里落不回页码也发）／自称句未标「发行人自述」即发／红线断言只准出现在 `[待人工]` 行／齐缺申报恰一枚且与清单对账（两处互相矛盾的申报同样发）。

```bash
python3 scripts/check_prospectus.py --help                       # 参数说明
python3 scripts/check_prospectus.py --selftest                    # 好样须过、坏样五道齐发、九档反证各发各支且各带独有点名句、临时件自清
python3 scripts/check_prospectus.py scripts/fixtures/good-prospectus.md   # PASS（发条 0 条）
python3 scripts/check_prospectus.py scripts/fixtures/bad-prospectus.md    # FAIL（五道各发，逐条点名行号）
```

## 三、上手

```bash
# 1. 放到技能目录
mkdir -p ~/.workbuddy/skills
cp -r prospectus-digest-cn ~/.workbuddy/skills/

# 2. 让 agent 按 SKILL.md 的速览卡五段出卡，产物存成我的招股书卡.md

# 3. 过机检（零网络）
python3 ~/.workbuddy/skills/prospectus-digest-cn/scripts/check_prospectus.py ./我的招股书卡.md
```

装本件自己：npx skills add huhoo/cue-awesome --skill prospectus-digest-cn（这条只装本包；装完在你这一侧重启会话才生效）。

## 四、首次开通 Cue（三步，可跳过）

本件的取证腿有两条：**找原文与稿件**（招股书原文与稿件版本，走数据腿）与**按节取用**（几百页的正文与附件，走解析腿）。两条都是可选——不装也能按你直供的正文出卡；代价是深处章节拿不到，研发与风险那两节常停在「未检索到」，而自称句最集中的恰是那两节。

1. 注册 <https://cuecue.cn>；
2. 在 <https://cuecue.cn/hub/api-key> 取 `CUE_API_KEY` 存入本地凭据——**不要贴进聊天**，agent 不经手密钥；
3. 装这两枚：`cue-data-mcp` 走找原文腿，`cue-omni-reader` 走按节取用腿。一条命令两种写法：
   - 整套：`npx skills add sensedeal/cue-skills`（它会列出该集合公开的各枚 skill，按提示挑要装的）；
   - 单装：`npx skills add sensedeal/cue-skills --skill cue-data-mcp`（把末尾那枚名字换成 `cue-omni-reader` 就只装那一枚）。

配置指路同样只给指针、不复述开通步骤：原文与稿件走数据腿，官方配置页 <https://cuecue.cn/hub/mcp>；长文件按节取用走解析腿，官方配置页 <https://cuecue.cn/hub/omni-reader>；取 key 走 <https://cuecue.cn/hub/api-key>。

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

装好 skill ≠ 已配凭据 ≠ 数据腿已连：这一层的判据只管数据腿那一路——带 key 按目标域 `routing` 实连且该端 `tools/list` 有返回，才证那把 key 被接受，也只证数据腿连上；按节取用那条腿的连通另按它自己那面的判据读。

## 五、边界与不承诺

- 估值、可比公司、是否申购、涨跌与风险大小排序一律 `[待人工]`；不写必涨／稳赚／零风险／保证收益；
- **自述不当事实**：领先、先进水平、最大、龙头、首创那类句子必须带「发行人自述，无第三方依据」；标不出来就不写进结论；排名式的事实描述（如「第一大客户占比」）不受这一判；
- **前瞻不当既成**：「公司将」「预计」「力争」「在研」的限定词整句留着；
- 数字与期间逐字：不换算、不四舍五入、不写「约」，「万元」不写成「亿元」；
- 域与工具名以 live catalog 现值为准，本件不列固定清单、不承诺枚数，也不承诺稿件更新的实时性。

## 六、出错了怎么办

| 症状 | 来路 | 恢复动作 |
|---|---|---|
| 研发与风险两节是「未检索到」 | 深处章节没取到 | 起按节取用腿；起不动就保留缺数点名，不从媒体稿借一句 |
| 数据腿连不上 | 凭据缺位或该域未 live | 按 §四 自查；你直供正文时不阻塞出卡 |
| 机检发红 | 缺页码锚／自称未标／齐缺不符／红线词裸出 | 按逐条点名的行号补齐；补不出的进缺数清单，不删行凑数 |
| 同一事实两处数字不同 | 招股书内部口径并存（业务节与财务节统计范围不同） | 两句并列进「口径对照」各挂各锚，不取其一当结论 |

## 七、怎么开口（正例与反例）

- 正例：「这份招股书募集多少钱、投到哪里」「前三大客户占多少」「实际控制人是谁」「风险因素自己写了什么」「申报稿和上会稿改了哪几处」。
- 反例：「这股票值多少钱、能不能打」——估值与申购决策不在本件，进 `[待人工]`。

## 八、能力边界（诚实清单）

行情与资金流类数值不在本件能力内（该域以 live catalog 现值为准，未开放就不承诺）；本件不做估值与可比公司，不做风险评级打分，不做媒体口径补位；单份公告事件级速读走 `event-brief-cn`，条款级拆解走 `placement-terms-cn`，跨主体底稿走 `dd-checklist`；本件也不持久存你的招股书文件。

## 九、资源

- `SKILL.md`：速览卡五段与红线原文（中文面为权威）
- `SKILL.en.md`：同文的英文对照面，冲突以中文面为准
- `references/self-claimed.md`：自述与第三方依据的分层速查（哪六类词要标注、排名式为何不判）
- `scripts/check_prospectus.py`：五道机检（零网络）
- `scripts/fixtures/`：一好一坏两份样例，`--selftest` 直接吃它们
