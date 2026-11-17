# competitive-brief

围绕一个决策问题做竞品分析，出带证据链的简报。

```
+brief "我们要不要进入北美中小律所的合规工具市场"
  → 先定决策、看谁、到什么程度
  → omni-reader 收素材，cue-research 深研交叉验证
  → 每一条 claim 标 fact/inference/opinion
  → 交付：结论 + 追溯 + 自己还需要确认什么
```

## 一句话

核心不是流程，是**证据表（evidence table）**——所有结论性主张在进简报之前，先写进证据表，填不满的维度不写进简报。

## 详细说明

见 [`SKILL.md`](SKILL.md)，包含证据表定义、约束、简报渲染规则。

## 实跑示例

[`examples/competitive-test/`](examples/competitive-test/) — 5人团队从 Cursor 迁移到替代方案的竞品简报：
- [证据表](examples/competitive-test/evidence-table.md)（24 行，其中 21 行为 fact ≈ 88%）
- [简报](examples/competitive-test/brief.md)

数据来源经 omni-reader 解析 cursor.com/pricing、claude.com/pricing、GitHub README 验证。

### 离线复跑（零网络，不取任何外部数据）

本包自带机检与八件守护样（好样 4＋坏样 4），装上后即可就地复跑一遍判定：

```bash
python3 scripts/check_brief.py --help                       # 四道说明，零网络
python3 scripts/check_brief.py --selftest                   # 末行期望：selftest: ALL GREEN，退码 0；档名与各档枚数由脚本那一行自报，本文不复述
python3 scripts/check_brief.py scripts/fixtures/good-full.md            # 期望 PASS（扫过 22 行，发条 0 条）
python3 scripts/check_brief.py scripts/fixtures/bad-coverage.md         # 期望 FAIL（申报计数与表内实测不符，发 E-COVERAGE）
```

判定全集在 `scripts/check_brief.py` 现值——四道分别是形制／锚／禁词与混标／计数与申报，本文不复述词表与阈值。

## 依赖（推荐安装）

- `cue-omni-reader`：解析网页/PDF/录音/视频，提取原文填入证据表
- `cue-research`：交叉验证、深度研究

开通与安装的命令写法与三层分开自查见 `references/cue-onboarding.md` §开通三步；本文只留下面这一条**最小实连形**（不留全量叙述，以免两处漂移——两处若读出不一致，以 `references/cue-onboarding.md` 为准并回来改这里）。配置指路给指针不复述步骤：数据腿官方配置页 <https://cuecue.cn/hub/mcp>、解析腿官方配置页 <https://cuecue.cn/hub/omni-reader>（本件两条腿都用——取数走数据腿、远端正文取证走解析腿）。

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | python3 -c 'import json,sys
rows=json.load(sys.stdin)["data"]["domains"]
[print(r.get("id"), r.get("external_status"), (r.get("routing") or {}).get("url", "-")) for r in rows]'
DOMAIN_ID="<把这里换成上一行列出的那个域 id>"
ROUTING_URL="$(curl -s "$CATALOG" | python3 -c 'import json,sys
rows=json.load(sys.stdin)["data"]["domains"]
hit=[r["routing"]["url"] for r in rows if r.get("id")==sys.argv[1] and r.get("routing")]
print(*hit,sep="\n") if hit else sys.exit("未取到：该 id 不在目录现值里（或它没有 routing 里的 url 字段）——先跑上面那行列出现场的 id 再填")' "$DOMAIN_ID")"
[ -n "$ROUTING_URL" ] || { echo "取值失败：ROUTING_URL 为空——先跑上面那行列出现场 id，再把 DOMAIN_ID 换成其中之一" >&2; exit 1; }
curl -s -X POST "$ROUTING_URL" \
  -H "Authorization: Bearer $CUE_API_KEY" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
  -w '\nHTTP %{http_code}\n'
```

一条命令形（不必手改块里那一行）：`cd competitive-brief && python3 -B scripts/cue_connectivity_check.py --domain <你的域 id> --post`；有哪些域 id 可填，先跑同一支脚本的 `--list`（只列在场域与 url，不发 POST）。匿名 `GET` 只证**目录可达**，带上 key 且 `tools/list` 有返回才证那把 key 被接受；通过＝HTTP 200 且 `result.tools` 非空（只按形状认，本面不列工具名也不承诺枚数）。这支随包件在把 key 附上去之前先过两关：scheme 必须是 https，且 host 命中授权后缀（缺省那一枚由件头目录入口现值推出，要放行别处请带 --allow-host）；过不了就拒发、退 6，本件不读 key 也不构造那个请求。代价同句写明：换源不免检，老的「换进去什么就打什么」那一形关掉了。

两者都由 Cue 通道提供，用量以服务端返回为准，本件不作价格承诺。不装也能跑，但缺的是整条交叉验证腿与解析腿（缺的那一层只能由你自供料顶上，可信级标签就不产生）。

## 国内可达取证路径（境外源不通时怎么办）

本件实跑示例的数据源是 `cursor.com/pricing`、`claude.com/pricing` 与 GitHub README——**这些例子照原样保留**，
它们是那一次真跑实际用到的来源。若你的网络取不到境外站点，取证路径换成本件已有的三条，**结论形制不变**：

1. **国内公开页直接交给 `cue-omni-reader` 解析**：厂商中文官网、产品文档站、应用商店详情页、
   公开财报与招股书页面（交易所/披露平台公开文件）、行业媒体的公开报道。解析结果照原样进证据表的「主张」列，
   标注来源 URL 与解析日期。
2. **公众号文章与境外站点**：这类页面常被登录墙或反爬挡住。可访问时走在线解析；
   不可访问时**由你把原文导出成文件**（PDF、HTML、截图皆可）后走本件的本地解析路径——
   工具读取的是用户明确提供的文件，不代你去抓。
3. **交叉验证**：需要横向比对的判断走 `cue-research`；不发起时对应行按「未经交叉验证」标注。

境外源不可达时该怎么办，按本件那条唯一硬约束办：**取证工具挂了，不准自己替它填**。
`cue-omni-reader` 返回错误 → 该行注明「omni 不可用，此来源未经解析验证」；
`cue-research` 报错或额度不足 → 补一行「此判断未经交叉验证」。缓存知识或推测**不得**伪装成有出处的行。

> 本段不承诺任何未开放的数据域，也不承诺任何特定站点必然可达：它只说明「用现成通道怎么把证据取到」，
> 取不到时的标注规矩，以及为什么不能空手补条。国内替代源与境外源**同形制、同标注要求**，不互相贬低。

## 常见问题与反模式（你想这么用 → 本件不接，因为 → 替代去向）

本件以方法论为主，可执行面只有形制机检 `scripts/check_brief.py`（四枚 `E-*` 码，`--selftest` 可跑）：它判形制与申报对不对，不替你判「这一条该不该写」，所以「反模式」仍靠证据表与覆盖度声明来兜。
判据以 `SKILL.md` 的约束与 `references/evidence-standards.md` 现文为准，本文不作穷尽复述。

| 你想 | 本件接不接，为什么不接 | 替代去向 |
|---|---|---|
| 先出一版「大致像」的简报，决策问题回头再定 | **不接**。约束一：定决策再填表；说不出「懂了能做什么」的简报不做 | 先把决策问题写成一问，再定看谁、到什么程度 |
| 某个维度只有 1/3 竞品有数据，也放进对比表 | **不接**。约束二：填不满的维度不放进对比表 | 放进未覆盖清单，交付时随附覆盖度说明 |
| 「推测」也算一种来源吧 | **不接**。约束三：来源不可靠的行不写，推测不是来源 | 推测一律标 `inference` 并写明依据；没有依据就不写这一行 |
| 取证工具挂了，先按记忆把主张填上 | **不接**（本件唯一硬约束）。用户看到没有来源标记的简报，会误以为每条都有出处 | 注明「未经解析验证 / 未经交叉验证」，该行留空并计入覆盖度 |
| 简报写满就是完整 | **不对**。完整性由覆盖度声明回答：填了多少行、多少 fact / inference / opinion、哪些维度未覆盖 | 交付附覆盖度（约束四），缺什么直说 |
| 竞品自家博客吹的参数直接当事实 | **不接**。主张要分 fact / inference / opinion 标注，厂商自述属需核验主张 | 交叉验证后降级或改标；未验证就注明 |

## 出错了怎么办（症状 → 原因 → 恢复动作）

**未见于本次返回的一律写「未检索到」**：参数名、字段名、枚举值没有出现在本次工具返回里的，不得凭印象填写；写「未检索到」并记入待核清单或覆盖率账，不得留空顶替。
错误码不在本文复述：`scripts/check_brief.py` 的详行自报 `E-*` 码，末行「码表:」只列那次真正用到的码与含义；下面是流程卡住时的症状与恢复动作，
全部按 `SKILL.md` 既有约束写（不新造术语、不承诺工具能力）：

| 症状 | 原因 | 恢复动作 |
|---|---|---|
| `cue-omni-reader` 解析报错 / 页面取不到 | 外部站点不可达、登录墙、或音视频扫描件解析不出 | 该行注明「omni 不可用，此来源未经解析验证」；改由用户导出文件走本地解析，或换国内公开源；**不代填** |
| `cue-research` 报错或额度不足 | 依赖工具不可用或消耗未批 | 补一行「此判断未经交叉验证」；深研发起前先报成本，由你决定是否继续 |
| 证据表某维度只有零星几行有数据 | 素材面覆盖不足，不是渲染问题 | 该维度移出对比表，进未覆盖清单；要补就补素材，不补空行 |
| 简报里出现「看起来是结论但没有出处」的段落 | 主张没先写进证据表就进了简报 | 回到证据表补行并标 `fact` / `inference` / `opinion`；补不出的那句删掉 |
| 决策问题太大，填表无从下手 | 决策未落到能改变动作的那一层 | 把问句收窄（谁 / 什么条件下会改变结论 / 到什么程度），收窄后再填 |
| 覆盖度写不出来 | 行数与标注没逐条对 | 交付前统计：总行数、fact / inference / opinion 各多少、未覆盖维度清单——写不出就是还没做完 |

## 怎么开口（触发示例：三条正例 + 一条反例）

**开口请带上时点，输出标来源日期**：请求里给出报告期／基准日或回看窗口；成品首行标注**来源日期**，当它与用户所指日期不一致时，正文禁用「今日」「最新」，一律改写为「截至 <日期>」。
- **正例（一句决策问题）**：「我们要不要进入北美中小律所的合规工具市场，用竞品简报看一眼」
  ——先定决策与对手集，再谈证据表；这一句就是 README 顶部的形制。
- **正例（复杂输入：对手集 + 维度 + 素材 + 国内源）**：「对手就这三家：`A`、`B`、`C`。要比的维度是价格与计费口径、
  部署形态、数据合规承诺三项；素材我已经下载成 PDF 放在 `~/cb/src/`，境外官网取不到就先用这些文件；
  厂商博客里的参数一律先当待核验主张，别直接进事实列」——文件走本地解析、来源与解析日期照标；未核验的进 `inference` 或留空。
- **正例（只要一份能自证的简报）**：「这份简报要给投委会看，每条结论我都要能点回原文；比不过的维度直说没数据」
  ——正是「结论 + 追溯 + 还需确认什么」三件的形制；未覆盖走未覆盖清单而不是空行。
- **反例（相邻需求，本件不接）**：「帮我做个一页纸看看这家公司」→ 一页速览是 `tear-sheet`；
  「这家上市主体公开信息里的风险逐条带锚、查不到什么也记账」→ `dd-checklist`；
  「这两份公告的新旧事实与口径差异做成可更新的知识包」→ `cue-omni-ontology`。本件只做「围绕一个决策问题的竞品证据链」。

## 版本

版本以本包 `SKILL.md` frontmatter 为唯一权威，历史见 [`CHANGELOG.md`](CHANGELOG.md)。
