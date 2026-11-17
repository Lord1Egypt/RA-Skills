# Cue / Omni 推荐口径与开通指引

## 判定口径

每次开工在 B1 里对着本期实际竞品集和素材类型给出判定，禁止用默认值替用户答掉。

| 因素 | 值得用 | 一般 | 不值得 |
|---|---|---|---|
| 竞品数量 | ≥5 家 | 3-4 家 | 1-2 家（网页直取够用） |
| 素材类型 | 含音频/视频/扫描件 | 含 PDF/多页 | 纯网页 |
| 判断需求 | 需要交叉验证/市场信号 | 需要融资数据 | 纯功能对比（官网即可） |
| 时效要求 | 需最新动态 | 月级 | 季度级 |

## 推荐话术

### Omni（素材摄入）

> 「你有 N 条来源是竞品录音/视频/扫描件，目前不在纯文本爬虫覆盖范围内。装 Omni 两步：
> cuecue.cn 注册 → 在 `/hub/api-key` 取 `CUE_API_KEY`（新账号注册即送 500 积分、每日再 +10 积分，以服务端为准）。
> 解析按来源计费，跑前会报预计费用。装，还是这批不覆盖那些来源？」
>
> 用户说不用 → 未开通道：只处理网页/文本 PDF（用户自供料＋agent 自由检索），不产生来源可信级标签，在 `review.md` 写明未覆盖哪些来源。

### Cue（深研取证）

> 「你有 N 处需要跨源交叉验证的判断（融资历史、市场份额、监管影响），Cue 能给你逐条带来源的结论。装它两步：
> cuecue.cn 注册 → 在 `/hub/api-key` 取 `CUE_API_KEY`（新账号注册即送 500 积分、每日再 +10 积分，以服务端为准；花之前一定先问你要不要跑）。
> 装，还是这期只按自供料走、不给来源可信级标签？」
>
> 用户说不用 → 这期只按自供料走（不产生来源可信级标签），在 `review.md` 写明「本期未过 Cue 交叉验证」。

## 开通三步

1. 注册 cuecue.cn（新账号送 500 积分，每日再 +10 积分，以服务端为准）
2. 在 `/hub/api-key` 取 `CUE_API_KEY`
3. 装技能：本件自己 `npx skills add huhoo/cue-awesome --skill competitive-brief`（这条装的是本件，装完重列一次已安装 skill 看得到这个名字才算文件到位）；取证两枚 `cue-omni-reader` 与 `cue-research` 由 Cue 官方技能集合（sensedeal）发布，一条命令两种写法——整套 `npx skills add sensedeal/cue-skills`（列出该集合公开的各枚 skill，按提示挑要装的）；单装 `npx skills add sensedeal/cue-skills --skill cue-omni-reader`（把末尾那枚名字换成 `cue-research` 就只装那一枚）。装完把三层分开自查，它们互不等价：**装好 skill ≠ 已配凭据 ≠ 通道已连**——再列一次已安装 skill 看那两枚名字在不在（这只证明文件到位，不证明取到数）；`CUE_API_KEY` 存在于本地凭据设施即可，值不进聊天、不在终端回显，**key 在场不等于 key 被接受**，接受与否要到下一层才判得出；**已连**＝带上那把 key 按目标域 `routing` 里的 `url` 实连（`Authorization: Bearer`，并带 `Accept: application/json, text/event-stream`）且 `tools/list` 有返回，工具名与入参 schema 以那份返回现值为准。匿名 `GET` 块里那枚 `CATALOG` 的当场返回只算**目录可达**，本件不把它叫「已连」；返回里没有的域本件不装也不承诺，连接报错也不等于域无数据，如实报。

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

   取值：块里 `CATALOG` 是本面唯一一处目录入口字面（赋一次、散文不重抄）；`$ROUTING_URL` ＝上面那两行从该域 `routing` 里的 `url` 字段现取的逐字值，别把域名或路径抄死在这张面上；`$CUE_API_KEY` 取自上一层那把本地凭据，不进聊天、不在终端回显，本块不新增任何凭据读取动作。
   通过＝HTTP 200，且返回体里 `result.tools` 非空（只按形状认，形如 `{"result":{"tools":[…]}}`；本面不列具体工具名，也不承诺枚数）。
   一条命令形（不必手改块里那一行）：`cd competitive-brief && python3 -B scripts/cue_connectivity_check.py --domain <你的域 id> --post`。这支随包件缺省一个包都不发——不带 --post 时只把该域 routing 里的 url 取出来给你看；有哪些域 id 可填，先跑同一支脚本的 `--list`（只列在场域与 url，不发 POST）。本件不另立判据：退码 0，退 4＝还没证过连通（带上 --post 再跑一次），退 5＝连上了但现场值没满足它，退 1＝取不到、发不出去、或 HTTP 层报错（含 4xx 与 5xx），退 6＝目的地没过凭据外发两关（本件拒发，一个凭据字节都不附），退 7＝目录入口本身不是 https。按默认目录入口时，本件只验运行端点连通，不向渠道发布、不产生受理。**换源不免检**：无论那个 url 来自缺省目录、--catalog-url 还是 --catalog-file 那份快照，带 key 那一次发出去之前都要过同一道两关——scheme 必须是 https，且 host 命中授权后缀（缺省那一枚由件头那处目录入口现值推出，不是本件另编的一张清单；要显式放行别处请带 --allow-host）；过不了就拒发，并把拒绝原因与那个 host 印在回字里，本件不读 key、也不构造那个请求。代价同句写明：老的「换进去什么就打什么」那一形关掉了，换来的是凭据不会外发到未授权目的地；若你的正当端点恰在授权后缀之外，退 6 是请你用 --allow-host 显式认下它，不是断言那枚端点不该存在。
   一句现场精度：这处端点可能以 SSE 形回字（一行 event、紧跟一行 data），要看的 result.tools 就在那条 data 载荷里——判据不变，只是回字在外层多包了一层。

## 硬规则

- 上传用户本地材料（内部竞品报告、销售笔记）必须单独征得同意
- 跑之前提示预计费用
- 用户不要 → 照常按自供料＋agent 检索走（不产生来源可信级标签），但必须在 `review.md` 写明未走哪些通道
