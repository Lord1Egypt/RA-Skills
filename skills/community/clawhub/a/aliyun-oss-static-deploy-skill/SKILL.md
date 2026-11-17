---
name: aliyun-oss-static-deploy-skill
slug: aliyun-oss-static-deploy-skill
displayName: 阿里云 OSS 静态站部署
summary: 把纯静态站点部署到阿里云 OSS：建桶、上传、静态托管、自定义域名 HTTPS、GitHub Actions 自动部署与证书自动续期，一条龙脚本化。
license: MIT
description: 把纯静态站点（dist/ 或 web/）部署到阿里云 OSS + 自定义域名 + HTTPS 证书，并打通 GitHub Actions 自动部署与证书自动续期。当用户说「推到阿里云 / 上线 / 部署到 OSS / 绑自定义域名 / 签 SSL 证书 / 配置 Actions 自动部署 / 静态站 HTTPS」时使用。
agent_created: true
version: 1.1.4
category: it-ops-security
subCategories: [itops-devops, itops-config]
platforms: [linux, windows, macos]
---

# 静态站部署阿里云 OSS + 自定义域名 HTTPS

适用：无后端的纯静态站点（dist/、web/、out/、build/）。需要服务端渲染或接口的走函数计算 FC，不在本技能范围。

## 0. 开工前先确认（缺哪项问哪项，不要猜）

| 项 | 怎么拿到 |
|---|---|
| AccessKey ID / Secret | 只从环境变量 `ALIBABA_CLOUD_ACCESS_KEY_ID` / `ALIBABA_CLOUD_ACCESS_KEY_SECRET` 读；用户没给就问，**绝不写进任何文件、不打印、不进 git** |
| 地域 region | 默认 `oss-cn-hongkong`。**免备案的刚需 → 用香港**；大陆地域绑自定义域名必须备案，且部分账号策略会拦公开读 |
| Bucket 名 | 全局唯一，被占用会 409，换名重来即可 |
| 自定义域名 | 子域即可（如 `case.example.com`），根域也支持但 `dns_rr` 要填 `@` |
| 静态产物目录 | 构建一次确认存在（如 `dist/index.html`） |

依赖（一次性）：
`pip install oss2 acme josepy cryptography alibabacloud_alidns20150109 alibabacloud_cas20200407 alibabacloud_ram20150501 pynacl`

## 1. 建桶 → 上传 → 配静态托管

建桶时给 `public-read` ACL 并指定香港地域；上传时按扩展名设 `Content-Type`（OSS 不猜，猜错浏览器行为很怪）：

| 文件 | Cache-Control | 理由 |
|---|---|---|
| `index.html` / `*.html` / 数据文件 | `no-cache` | 内容常变，改完立刻生效 |
| `*.js` / `*.css` | `public, max-age=300` | 基本不变，省回源 |

**必须设静态网站托管**（`PUT ?website`，IndexDocument=`index.html`，ErrorDocument=`404.html`）；
不设的话访问域名根路径返回的是 XML 对象列表，而不是首页。

## 2. 关键坑：公开访问 403

新建桶默认 `BlockPublicAccess=true` —— 现象：匿名访问 403，且 `PutBucketPolicy` 也被拒
（`Put public bucket policy is not allowed`），此时**改 ACL 没用**，必须关掉桶级阻止公共访问：

```
DELETE https://<bucket>.oss-<region>.aliyuncs.com/?publicAccessBlock   → 204 即成功
GET    https://<bucket>.oss-<region>.aliyuncs.com/?publicAccessBlock   → 确认 <BlockPublicAccess>false</BlockPublicAccess>
```

排查顺序：先 `GET ?publicAccessBlock` 看是不是 true → 关掉 → 再匿名 `curl` 一次确认 200。

## 3. 域名 + HTTPS 证书

顺序不能反：**先加 CNAME 记录**指向 `<bucket>.oss-<region>.aliyuncs.com`，等解析生效后再绑域名。

- 走 CDN 加速：CNAME 指 CDN 域名，证书在 CDN 上配（部署后记得刷新目录缓存 `/`）。
- 直连 OSS：CNAME 指桶的标准域名。**注意 OSS 按 Host 头匹配自定义域名**，CNAME 指向 OSS 海外公共入口
  （如 `*.thepacificphs.com`）时自定义证书不生效，必须指到 `<bucket>.oss-<region>.aliyuncs.com`。

证书两条路：

1. **已有通配证书**（推荐，多站点共用一张）——只做分发，不重签：上传 CAS 拿到 `cert_id`，
   再用 `PutCname` 绑到桶，绑定前自动写 `_dnsauth.<子域>` TXT 做归属验证。
   注意 `force` 字段必须是字符串 `'true'`，传 `1` 会触发 `MalformedXML` 并盖住真正的报错。
2. **没有证书**——用 `scripts/cert_manager.py` 一步到位：DNS-01 签发（alidns 自动加 TXT）→ 上传 CAS
   → 绑定 OSS（可选同步推 FC 自定义域名）。泛域名 `example.com + *.example.com` 一次覆盖所有子域，
   后续新增站点只加一行分发目标，不必重签。

```bash
# 签发泛域名证书并绑定到 OSS 自定义域名
python scripts/cert_manager.py --root example.com --email you@example.com \
    --bucket my-site-hk --region cn-hongkong --domain www.example.com

# 证书已存在、只做分发（续期后常用）
python scripts/cert_manager.py --root example.com --domain www.example.com --targets oss
```

ACME 证书只有 90 天，脚本剩余 >30 天自动跳过；到期前重签并重新分发。

## 4. GitHub Actions 自动部署

**动手配之前先过一遍 4.5(1c) 的判断**：这条 CI 改了哪些文件、那些文件会进对外产物吗？
如果答案是「不进」（典型：采集类 workflow 只写内部队列，而对外产物显式剔除了它），
那它部署的是和上次一样的站点 —— **别配部署，去把 workflow 的部署步骤删掉**。
2026-09-20 实测过一个配错方向的：那条 workflow 每天推 400+ 条未核实素材上公网，
连跑 4 天全是 success，靠对比产物体积才发现。

先查现状再动手，别猜（只能读名字，读不到值）：

```bash
# ~/.git-credentials 每行形如 https://<user>:<token>@github.com
# 坑：别假设 token 前缀是 gho_ —— 那是 gh 自己的 OAuth token；PAT 是 40 位裸串，
# grep -o "gho_..." 会取到空值，后面所有请求 401 却看不出原因。用 python 取：
TOKEN=$(python -c "
import os,re
for l in open(os.path.expanduser('~/.git-credentials'),encoding='utf-8'):
    m=re.match(r'https://[^:]+:([^@]+)@github\.com', l.strip())
    if m: print(m.group(1)); break
")
curl --noproxy '*' -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/<owner>/<repo>/actions/{secrets,variables}
```

**收尾别忘了反向清理**：部署步骤一旦从 workflow 里删掉，那两个 Secret 与两个
Variable 就成了不再被使用的长期凭证。删掉它们（`DELETE /actions/secrets/<name>`、
`DELETE /actions/variables/<name>`）—— 留着既不安全，也会让下一个人以为「CI 会自动部署」。

- **Variables**（明文，直接 POST）：`OSS_BUCKET`、`OSS_REGION`。
- **Secrets**：先 `GET /actions/secrets/public-key` 拿 `key_id` + 公钥，再用 PyNaCl `SealedBox` 加密后 PUT
  （`scripts/set_github_secret.py` 封装了这段）。
- **公开仓库绝不放主账号 AK**：先用 RAM 建专用子账号，策略只给这一个桶的
  `oss:PutObject / GetObject / DeleteObject / ListObjects` + `oss:PutBucketWebsite / GetBucketWebsite`，
  外加全局 `oss:ListBuckets`（部署脚本的凭证自检要用）；Secret 用后即删本地副本。
- 验证：`POST /actions/workflows/<file>/dispatches` 手动触发（204 成功）→
  `GET /actions/runs/<id>/jobs` 看每个 step 的 conclusion，确认部署步骤真的跑了而不是被 skip。

**顺带一个本地 git 的坑**：`gh auth status` 经常是「未登录」，而全局配置里
`credential.https://github.com.helper=!gh auth git-credential` 会让 `git push` 直接报
`could not read Username ... terminal prompts disabled`。修法是给仓库加一条更局部的
credential helper，让它回落到 `~/.git-credentials`：

```bash
git config credential.https://github.com.helper store   # 写进 .git/config，压过全局的 gh helper
```

**回写验证要看内容，不要看字节数。** 数据每天都在涨，`wc -c` 对不上分不出是「没部署」
还是「部署了但数据变了」。找一个只有新版才有的**语义标记**去判：

```bash
curl --noproxy '*' -s "https://<bucket>.oss-<region>.aliyuncs.com/data.json" | head -c 200
# 或直接断言某个字段，例如 jq -e '.schema_version' >/dev/null && echo DEPLOYED
```

触发 dispatch 到产物更新通常 1～3 分钟；轮询时带上 `Cache-Control: no-cache`，
否则会一直读到边缘缓存里的旧对象。


## 4.5 三个反复踩到的部署细节

**（1）别默认传 `dist/`：先问「这份产物是要给外人看的吗」**

有些站有两份构建：内部完整版（含未核实/未公开的数据）和对外发布版。
默认目录往往是前者。上线前确认一次：

```bash
python scripts/build_static.py --site-url https://<域名> --no-inbox --out public   # 对外那份
python scripts/deploy_oss.py --bucket <桶> --region cn-hongkong --dir public \
    --setup-website --verify-public                                                # 注意 --dir
```

把对外那份加进 `.gitignore`（如 `public/`），避免哪天顺手 `git add -A` 把不带治理的
中间产物推上去。

**（1b）放进 Actions 的部署步骤，必须显式写死产物参数 —— 别用默认值**

上一条的防线是「扫一眼排除清单再上传」，而**CI 里没有人会看输出**。
2026-09-20 实测：一个 workflow 的构建与部署两步都用了默认参数

```yaml
- run: python scripts/build_static.py                          # 默认 --out dist，没加 --no-inbox
- run: python scripts/deploy_oss.py --bucket $B --region $R    # 默认 --dir dist
```

于是它**每天把 400+ 条未核实素材的全文推上公网，连跑 4 天全是 success**。
发现靠的是对比产物体积（CI 传的 `data.json` 525 KB，对外那份只有 174 KB），
不是靠日志 —— 日志里那两行和正常部署长得一模一样。

三条可操作的做法：

1. **workflow 里不允许出现裸的 `build_static.py`**：产物目录与 `--no-inbox`
   都写成字面量，宁可长也别省。想让两边约定永不漂移，就让 CI 调同一个编排器
   （如 `release.py --only build,deploy`），而不是各写一遍参数。
2. **在上传脚本里加硬闸门，而不是靠人记得**：读产物 `data.json` 的敏感字段
   （未核实条数、密钥、内部路径），非空且没给显式的放行参数就拒绝上传。
   注意让这个检查返回**三态**（0 干净 / 正数脏 / 读不出来）——
   把「读不出来」也当 0 会把真 bug 吞成「看起来正常」。
3. **给对外产物写一条语义断言进 CI**：线上 `inbox` 必须是 0 之类，
   让「推错产物」变成红的，而不是等读者发现。

**（1c）先问「这条 CI 到底该不该部署」，再谈怎么部署对**

参数写对只是治标。更值得先问的是：**这条 CI 的产出，会上公网吗？**

上面的例子里，那条 workflow 的职责是「采集原始素材」，而对外产物
显式剔除了这些素材（`--no-inbox`）—— 也就是说它部署的是**和上次一模一样的站点**，
纯属空转；真正的部署入口是本地那条发布链路，它自己就含 build + deploy。

判据很简单：**看这条 CI 改了哪些文件**
- 改的文件会进对外产物 → 才需要部署
- 改的文件被对外产物排除 → 部署是空转，删掉更干净
- 改的文件**不该**进对外产物，但产物没排除它 → 这是在推脏数据，最危险

删掉空转的部署还有个附带好处：CI 不再需要长期挂着 OSS 凭证。
（本例删掉部署后，仓库里那两个 Secret 与两个 Variable 一并清掉，
少一份长期凭证的暴露面。）

**（2）部署脚本里的「连通性探针」别写成 `read(400)`**

只探前 400 字节然后打印「HTTP 200 400 字节」，日志读起来像首页只有 400 字节，
部署完一眼扫过去会以为传坏了（实际 `index.html` 是 15 KB）。要么读全量再报长度，
要么干脆别打字节数，只打状态码。

**（3）region 填错的表现是「指定 endpoint」报错**

dry-run 报 `AccessDenied ... must be addressed using the specified endpoint`
= 桶不在这个 region，换地域重试即可，不是权限问题。先用 `--check` 列一遍账号下的桶。

**（4）「线上 vs 本地」的漂移检测：网络失败不是内容差异**

比本地产物与线上内容来决定「要不要重新部署」时，最容易写错的一点：
把「取不到」当成「线上没有这个文件」。2026-09-20 实测踩到 ——
一次瞬时失败让一个在线上的页面被判「缺失」，脚本就触发了一次没必要的部署
（同一条 URL 手工一取就是 HTTP 200）。

必须分三态，而且**只有明确 404 才算缺失**：

| 结果 | 含义 | 处置 |
|---|---|---|
| `ok` | 取到了 | 比哈希 |
| `missing` | **明确 404** | 算差异，需要部署 |
| `error` | 超时/连接失败/5xx | **不参与判断**，只报告 |

配套三条：
- 404 **不重试**（没意义，只拖慢）；网络错误重试 2 次
- 取不到的比例达到约 1/3 时直接停下报「大概率是网络或域名不对」，
  别拿一堆没比出来的文件去部署
- 报告里要分开写「内容不同」「线上缺失」「取不到」「线上多出来的」——
  尤其最后一类：**部署不会删多余文件**，拿它触发部署等于每天白跑

顺带一条同源教训：这类脚本的「有差异」判断要能区分
「测试/预演」与「真跑」，而且 `--dry-run` 必须真的一个写请求都不发
（见本节第 3 条最后那段）。

## 4.6 写一个语义校验脚本，别每次手敲 curl

把验收固化成 `scripts/verify_deploy.py`，覆盖：首页 / 所有详情页 / 404 页 / 数据文件 /
sitemap / robots / 静态资源。断言的是这些不会因为数据增长而失效的东西：

- `site.title`、`site.url`、`generated_at`（能定位到「传的是哪次构建」）
- `cases` 条数、`inbox` 是否为 0（公开版不应该含未核实数据）
- 每个详情页 HTTP 200 且字节数 > 20000（正文是否真的内联，禁用 JS 也能读）
- 根路径不以 `<?xml` 开头（确认静态托管生效）

案例数会涨，所以条数做成参数（`--expect-cases`），别写死在断言里。

**一个容易误判为失效的点**：预渲染的列表页里链接常常是相对路径（`./slug.html`），
这样根目录部署和子目录部署都能用。校验时别拿绝对路径去匹配，否则会误报。

脚本已实现（`scripts/verify_deploy.py`，纯 stdlib）：

```bash
python scripts/verify_deploy.py --base-url https://<域名> \
    --xml-root-is-fail --forbid-text '<?xml' \
    --expect-text 'generated_at' --expect-text '本次构建标记'
python scripts/verify_deploy.py --base-url https://<域名> \
    --pages-file pages.txt --min-bytes 20000 --check-seo
python scripts/verify_deploy.py --base-url https://<域名> \
    --data-json data.json --expect-cases 42 --expect-json-field site.url
```

`--xml-root-is-fail` 对应「根路径不以 `<?xml` 开头」那条（静态托管是否真生效）；
`data.json` 若含 `inbox` 字段，脚本会自动断言其为 0（公开版不该夹带未核实数据）。

## 5. 证书自动续期

把 `scripts/cert_manager.py` 挂到每日定时任务（Windows 上 `schtasks` 常被环境禁用，优先用宿主自带的
定时/自动化能力，例如 WorkBuddy 自动化）。脚本幂等：没到期就退出，到期才重签 + 分发。

## 附：验收清单

```bash
curl -o /dev/null -w "%{http_code} %{ssl_verify_result}\n" https://<域名>/   # 200 且 ssl_verify_result=0
curl -o /dev/null -w "%{http_code}\n" https://<域名>/not-exist-page          # 404 页生效

# 内容对不对：断言语义标记，别比字节数
curl --noproxy '*' -s https://<域名>/data.json \
  | python -c "import sys,json; d=json.load(sys.stdin); print(d['generated_at'], len(d['cases']))"
```

上面那条绝对不要写成 `curl .../data.js | wc -c` 去跟本地产物比字节数——
`data.js`/`data.json` 每天重新生成，比不出来是「没部署」还是「数据变了」。
只有 `app.js`、`style.css` 这种内容稳定的文件适合比大小。

## 附：常见错误对照

| 报错 | 真实原因 |
|---|---|
| 匿名访问 403 + `bucket acl` | 桶级 `BlockPublicAccess=true`，须 `DELETE ?publicAccessBlock` |
| `Put public bucket policy is not allowed` | 账号级策略限制，改 ACL 即可，不必强求 bucket policy |
| 根路径返回 XML 列表 | 没配静态网站托管 |
| `MalformedXML` 于 PutCname | `force` 传了非字符串；改 `'true'` 后才会暴露真正的 `NeedVerifyDomainOwnership` |
| 绑域名报 `DomainNameNotResolved` | CNAME 还没生效，先加解析等生效 |
| 自定义证书不生效 | CNAME 指到了 OSS 海外公共入口，改指 `<bucket>.oss-<region>.aliyuncs.com` |
| 上传后线上还是旧的 | 走了 CDN 未刷新，或浏览器缓存了 `max-age` 资源 |
| `AccessDenied ... must be addressed using the specified endpoint` | 填的 region 不对，桶不在这个地域（换 region，不是权限问题） |
| 日志显示「HTTP 200 400 字节」但文件有 15 KB | 那是 `read(400)` 的探针长度，不是真实大小，见 §4.5(2) |
| 校验脚本报「列表页缺链接」 | 列表页用的是相对路径 `./slug.html`，别按绝对路径匹配 |
| oss2 报 `ProxyError` / `Tunnel connection failed: 502` | 本机 `HTTP(S)_PROXY` 指向本地代理，Python 会走它而 `curl --noproxy` 不会；`unset` 代理变量即可，见 §4.7 |

## 4.7 本机代理会把 oss2 搞挂（本地跑部署脚本的头号故障）

本机常驻一个本地代理（形如 `http://127.0.0.1:3777`），且 `HTTP_PROXY/HTTPS_PROXY` 已导出。
`curl` 可以靠 `--noproxy '*'` 绕开，但 **Python 的 oss2（底层 requests）会老实读这两个环境变量**，
代理一抽风就报：

```
RequestError: ... ProxyError('Unable to connect to proxy',
    OSError('Tunnel connection failed: 502 Bad Gateway'))
```

**迷惑点**：`curl --noproxy '*'` 直连明明是 200，脚本却连不上；而且**时好时坏**
（同一条命令第一次成功、隔几分钟再跑就 502）。所以别去怀疑 bucket 权限或 region。

排查顺序：
1. `env | grep -i proxy` —— 确认代理变量存在；
2. `curl --noproxy '*' -o /dev/null -w "%{http_code}" <url>` —— 确认直连是通的；
3. 两者不一致 → 就是代理的锅。

修法（**已内置到脚本**，了解原理即可）：`deploy_oss.py` / `verify_deploy.py` 启动时会主动
清掉 `HTTP(S)_PROXY` 等变量并打印一行提示，正常情況下**不用再手动 unset**：

```bash
python scripts/deploy_oss.py --bucket <桶> --file index.html --verify
[..] 已清除代理环境变量（本机代理会搞挂 oss2）：HTTP_PROXY, HTTPS_PROXY
```

要保留代理（例如必须走代理才能出网）就加 `--keep-proxy`；
只想放行 OSS 域名则保留代理并设 `no_proxy="oss-cn-hongkong.aliyuncs.com"`。

## 4.8 两个部署脚本的用法（scripts/ 下已实现）

`deploy_oss.py`（依赖 `oss2`）：

```bash
python scripts/deploy_oss.py --check                     # 先列账号下的桶定位名字/地域
python scripts/deploy_oss.py --bucket <桶> --region cn-hongkong --dir public \
    --setup-website --verify-public --verify             # 整目录上线（推荐）
python scripts/deploy_oss.py --bucket <桶> --file fixed.html --key index.html \
    --verify --expect '语义标记'                          # 单文件热更新
python scripts/deploy_oss.py --bucket <桶> --dir dist --dry-run   # 只打印计划
```

要点：
- `--region` 写 `cn-hongkong` 或 `oss-cn-hongkong` 都行，脚本自动补前缀；
  内部 endpoint 用**完整** `https://oss-cn-hongkong.aliyuncs.com`——`oss2.Service(auth, ...)`
  第二个参数必须是完整 endpoint，**传 region 短名会报 `RequestError: HTTPConnectionPool`**，
  看起来像网络/权限故障，实际是参数用错（这条踩过）。
- Content-Type 按扩展名查表（OSS 不猜类型）；html/json/xml 用 `no-cache`，js/css 用 `max-age=300`。
- 覆盖同名对象前**自动备份**旧版本到 `~/.oss-deploy-backup/<桶>/<key>.<时间戳>`（`--no-backup` 可关）。
- `--verify` 是回读 **md5 比对**，不是比字节数；再加 `--expect '某串'` 做语义标记断言。
- `--dry-run` 会跳过回读校验（对象根本没上传，回读必然 404，不要误判为失败）。
- **`--dry-run` 必须真的只读 —— 写完要数一遍写请求，别信输出。**
  2026-09-20 实测一个 deploy 脚本：`--dry-run` 只保护了 upload 那一段，
  而 Bucket Policy 的 PUT 跑在 dry_run 判断**之前**、无条件执行 ——
  于是「只列出会传的文件，不真传」实际是「不传文件，但照样重设线上权限策略」。
  同类：`--create` + `--dry-run` 桶不存在时会真的建桶。

  这个 bug 的可恶之处在于**它只骗人、不报错**：调用方（如一个
  `release.py --dry-run` 全链路预演）对外宣称「不写盘不上传」，
  实际上每次预演都真的改了一遍线上配置。

  排查手法：把「写操作」全部列出来（PUT/POST/DELETE/建桶/改策略/改权限），
  逐个确认它在 dry-run 分支**之内**。上传那一段最容易检查到，
  权限、策略、托管设置、CDN 刷新这些「顺手的收尾动作」最容易漏。

  测试要**数写请求**（记下每个 method，断言 dry-run 时非 GET 数为 0），
  而不是断言「打印了跳过」。打印一句「（跳过）」很容易，真发没发 PUT 才是事实。
  反向也要钉一条：真跑时必须照发 —— 别为了「dry-run 干净」把正常路径一起废掉。

`build_static.py`（零依赖，整理**对外产物**）：

```bash
python scripts/build_static.py --src dist --out public --site-url https://<域名>
python scripts/build_static.py --src . --out public --no-inbox --exclude "*.bak,staging/"
python scripts/build_static.py --src dist --out public --dry-run
```

默认就排除源码 / 密钥 / `.env*` / VCS / node_modules，并替换 `__SITE_URL__` `{{SITE_URL}}` 占位符；
`--no-inbox` 额外剔除 `inbox/` 等未核实数据（对外版不能带）。收尾会校验入口页存在、
产物里不含密钥或未核实数据。**运行即打印排除清单**，建议扫一眼再上传。

GitHub Actions 在云端、没有这个代理，**不受影响**——别把这段写进工作流。
反过来也成立：CI 报连接失败时，不要拿本地代理经验去解释。
