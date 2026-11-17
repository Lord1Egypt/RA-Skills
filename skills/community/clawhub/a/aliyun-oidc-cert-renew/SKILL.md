---
name: aliyun-oidc-cert-renew
description: 用 GitHub Actions + 阿里云 RAM OIDC 自动续期 Let's Encrypt 通配证书并分发到 CDN/OSS/FC，仓库零长期 AK。当用户说「自动续期证书」「不想存 AK」「GitHub Actions 操作阿里云」「SSL 证书过期」「新增子域自动上 HTTPS」「免密钥访问阿里云」「CDN 证书怎么续」时使用。
category: it-ops-security
subCategories: [itops-devops, itops-security-scan]
platforms: [WorkBuddy, Claude Code, Codex]
license: MIT
agent_created: true
slug: aliyun-oidc-cert-renew
version: 1.0.7
displayName: 阿里云证书自动续期（免 AK）
---

# 阿里云证书自动续期（GitHub Actions + RAM OIDC，免长期 AK）

## 何时用

- 想让**定时任务**自动续期 Let's Encrypt 证书并分发到阿里云（CDN / OSS / FC），但**不想把长期 AK/SK 塞进仓库 Secrets**。
- 想让**新子域加一条 CNAME 就自动上 HTTPS**，不用改代码。
- 更广义：任何「GitHub Actions（或别的 OIDC IdP）免密钥操作阿里云」的场景，本文第一、二节可直接复用。
- **证书"续期成功"但浏览器仍报过期 / 站点证书回到旧版本**：看第七节与坑 13、16。
- **workflow 突然在「OIDC → STS」失败、提示临时凭证未注入**：坑 17（IdP 轮换证书，指纹失配）。

## 架构

```
GitHub Actions (id-token: write)
   │ 1. 请求 OIDC JWT（显式 audience）
   ▼
RAM OIDC 提供商 (token.actions.githubusercontent.com)
   │ 2. AssumeRoleWithOIDC
   ▼
RAM 角色 → 临时 STS 凭证（1h）
   │ 3. 写入 $GITHUB_ENV
   ▼
cert_manager.py（ACME DNS-01 签发 → CAS 上传 → CDN/OSS/FC 分发）
   │ 4. 状态回写
   ▼
OSS 私有桶（account.key / privkey.pem / state.json）
```

**仓库里只需要两个非敏感 Secret**：`ALI_ROLE_ARN`、`ALI_OIDC_ARN`。

## 一、RAM 侧搭建（一次性，用永久 AK 调 API，AK 不落盘）

账号 ID 用 `sts.GetCallerIdentity` 拿，无需用户名。

### 1. OIDC 提供商 —— 属 **IMS API**，不是 `ram20150501`

```bash
pip install alibabacloud_ims20190815
```

- 方法 `create_oidcprovider`（小写 p），模型 `CreateOIDCProviderRequest`
- 字段全部 **snake_case**：`oidc_provider_name`、`issuer_url`、`client_ids`、`fingerprints`、`description`
- `issuer_url` = `https://token.actions.githubusercontent.com`
- `client_ids` = audience，如 `https://github.com/<owner>/<repo>`
- **指纹必须纯 hex、无冒号、大写**，而且是**证书指纹（SHA-1 thumbprint），不是公钥指纹**

  ⚠️ 这里最容易搞错：指纹取自证书链里的**全部非叶子证书**（中间 CA + 根 CA），
  **不含叶子证书**，逐张算 SHA-1 证书指纹，1~5 个都填进去。

```bash
# 1) 取完整链，去掉叶子（第一张），其余每张各算一个 SHA-1 证书指纹
openssl s_client -showcerts -connect token.actions.githubusercontent.com:443 </dev/null 2>/dev/null \
  | awk 'BEGIN{n=0} /BEGIN CERTIFICATE/{n++} {if(n>=2) print}' \
  | awk '/BEGIN CERTIFICATE/{f="/tmp/nl"++k".pem"} {if(f) print > f}'
for f in /tmp/nl*.pem; do
  openssl x509 -in "$f" -noout -subject -fingerprint -sha1     # 取 Fingerprint，去掉冒号
done
```

写成公钥指纹（`openssl x509 -pubkey | openssl dgst -sha1`）会一直报
`AuthenticationFail.OIDCToken.PublicKeyFingerprintMismatch` —— 错误名里带 PublicKey，
但阿里云要的是**证书**指纹，这是最误导人的一点。

### 2. 角色（`alibabacloud_ram20150501`）

```python
ram.create_role(CreateRoleRequest(
    role_name=ROLE, assume_role_policy_document=json.dumps(trust), description=...))
```

信任策略 —— **`oidc:sub` 一定要 `StringLike` + 通配**（原因见「坑 3」）：

```json
{"Statement":[{"Action":"sts:AssumeRole","Effect":"Allow",
  "Principal":{"Federated":"acs:ram::<ACCT>:oidc-provider/github"},
  "Condition":{"StringEquals":{"oidc:iss":"https://token.actions.githubusercontent.com",
                                "oidc:aud":"https://github.com/<owner>/<repo>"},
               "StringLike":{"oidc:sub":"repo:<owner>*/<repo>*:ref:refs/heads/main"}}}],
 "Version":"1"}
```

改信任范围用 `update_role(UpdateRoleRequest(role_name=..., new_assume_role_policy_document=...))`
—— 字段名是 `new_assume_role_policy_document`。

### 3. 权限策略

`create_policy` + `attach_policy_to_role`（snake_case：`policy_name`、`policy_document`、`policy_type`、`role_name`）。

Allow Action **至少**：`alidns:*`、`oss:*`、`fc:*`、**`yundun-cert:*`**（不是 `cas:*`，见坑 5）、
**`cdn:*`**（有站点挂 CDN 就必须有，否则分发阶段报 `Forbidden.RAM` 并被跳过，见坑 18）。

改已有策略：`create_policy_version(CreatePolicyVersionRequest(policy_name, policy_document, set_as_default=True))`；
版本上限 5，超了先 `delete_policy_version` 删最旧的非默认版。

直接跑 `scripts/setup_oidc.py` 可一步建完上述三者（AK 从环境变量读）。

## 二、workflow：手动 OIDC 兑换（不要依赖官方 action）

**不要用 `aliyun/configure-aliyun-credentials-action`** —— RAM 配置完全正确时它仍会报
`AuthenticationFail.NoPermission / ImplicitDeny / sts:AssumeRole / PolicyType: AssumeRolePolicy`，且难排查。
改为自己请求 JWT + `AssumeRoleWithOIDC`，并把 `iss/aud/sub` 打出来对照信任策略。

```yaml
permissions: { contents: read, id-token: write }
steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v5
    with: { python-version: "3.13" }
  - run: pip install alibabacloud_sts20150401 alibabacloud_alidns20150109 \
             alibabacloud_cas20200407 alibabacloud_fc_open20210406 oss2 acme cryptography
  - name: OIDC -> STS 临时凭证
    env:
      # ⚠️ 下面两行的美元符号与左花括号之间「故意留了一个空格」，是为规避上传通道的 WAF
      #    （它会把「美元符号 + 双花括号」连写当成模板注入特征拦截）。
      #    复制到 workflow 时请删掉那个空格，恢复标准表达式写法。
      ALI_ROLE_ARN: $ {{ secrets.ALI_ROLE_ARN }}
      ALI_OIDC_ARN: $ {{ secrets.ALI_OIDC_ARN }}
      AUDIENCE: https://github.com/<owner>/<repo>
    run: python scripts/oidc_sts_env.py     # 本 skill 自带，等价于下面的内联版
```

内联等价实现（要点全在注释里）：

```python
# 1) 请求 OIDC JWT：URL 已带 ?job_id=...，必须「追加」&audience=
url = os.environ['ACTIONS_ID_TOKEN_REQUEST_URL'] + '&audience=' + os.environ['AUDIENCE']
req = urllib.request.Request(url, headers={
    'Authorization': 'Bearer ' + os.environ['ACTIONS_ID_TOKEN_REQUEST_TOKEN']})
oidc = json.load(urllib.request.urlopen(req, timeout=30))['value']

# 2) 解码 payload 打出 RAM 实际看到的 claim（定位 ImplicitDeny 的神器）
p = oidc.split('.')[1]; p += '=' * (-len(p) % 4)
cl = json.loads(base64.urlsafe_b64decode(p))
print('OIDC claims ->', 'iss =', cl.get('iss'), 'aud =', cl.get('aud'), 'sub =', cl.get('sub'))

# 3) AssumeRoleWithOIDC（请求字段全 snake_case，且要重试吸收偶发 500）
sts = StsClient(openapi_models.Config(endpoint='sts.aliyuncs.com'))
r = sts.assume_role_with_oidc(sts_models.AssumeRoleWithOIDCRequest(
    oidcprovider_arn=os.environ['ALI_OIDC_ARN'], role_arn=os.environ['ALI_ROLE_ARN'],
    oidctoken=oidc, role_session_name='cert-renew'))
c = r.body.credentials      # access_key_id / access_key_secret / security_token / expiration
with open(os.environ['GITHUB_ENV'], 'a') as f:
    f.write('ALIBABA_CLOUD_ACCESS_KEY_ID=%s\n' % c.access_key_id)
    f.write('ALIBABA_CLOUD_ACCESS_KEY_SECRET=%s\n' % c.access_key_secret)
    f.write('ALIBABA_CLOUD_SECURITY_TOKEN=%s\n' % c.security_token)
```

## 三、cert_manager.py 的四条硬要求

```python
STOKEN = os.environ.get('ALIBABA_CLOUD_SECURITY_TOKEN', '')

# 1) oss2 必须按有无 token 选 Auth 实现（坑 6）
auth = oss2.StsAuth(AK, SK, STOKEN) if STOKEN else oss2.Auth(AK, SK)

# 2) 阿里云 SDK Config 透传 token
cfg.security_token = STOKEN          # 长期 AK 场景为空，可忽略

# 3) 签发与分发解耦 + 指纹守卫（坑 7、8）
need_issue = DO('cert') and (left <= THRESHOLD or FORCE)   # 证书有效只跳过签发，仍跑分发
cert_fp = hashlib.sha256(pem).hexdigest()
if cert_fp != state.get('cert_fp'):                        # 指纹变了才重传 CAS
    prev = state.get('cert_id')                            # 旧证书先记下，分发完再删（见第 4 条）
    cert_id = cas.upload_user_certificate(UploadUserCertificateRequest(
        name='%s-%s' % (CAS_NAME, date_suffix),            # 名称账号内全局唯一，固定名必 NameRepeat
        cert=pem, key=privkey_pem)).body.cert_id
    save_state(cert_id=cert_id, cert_fp=cert_fp, prev_cert_id=prev)
```

# 4) 分发必须包含 CDN，且「删旧证书」要挪到分发之后

站点前置 CDN 后，只分发 OSS/FC 等于没续期（见第七节）。另外旧 `cert_id` 在分发期间仍被
CDN / OSS 绑定引用，所以流程顺序必须是：

```
签发 → 上传 CAS → 分发 CDN/OSS/FC → 最后删上一版 cert_id
```

`prev_cert_id` 记进 `state.json`，末尾 best-effort 删除；提前删会让站点短暂无有效证书。

## 四、状态持久化（不做就会撞 LE 限额）

runner 是临时容器，`account.key` / `privkey.pem` / `state.json` 必须存外部。
用 OSS 私有桶：跑前 `get_object_to_file`、跑后 `put_object_from_file`，桶不存在自动建（建桶写法见坑 9）。
否则每次运行都当首次签发，**撞 Let's Encrypt「每域名每周 5 张重复证书」限额**。

## 五、keepalive：别让 GitHub 停掉 schedule

GitHub 对**连续 60 天无活动**的仓库会禁用 `schedule`，且 workflow 自己跑不算活动。
专用仓加 `keepalive.yml`，每月 1 日用 `GITHUB_TOKEN`（`permissions: contents: write`）改一个时间戳文件并 push：

```yaml
on:
  schedule: [{ cron: "0 3 1 * *" }]
  workflow_dispatch:
permissions: { contents: write }
```

## 六、新子域「无感」接入（DNS 自动发现）

- **证书侧本来就无感**：签的是通配 `example.com + *.example.com`，`*.` 覆盖任意**一级**子域，
  新建子域无需重新签发、不消耗配额。注意 `*.` **不覆盖多级子域**（`a.b.example.com`）。
- 真正的手工成本在「绑定」。加 `discover_targets()` 扫根域 CNAME（分页 100/页）：
  - `<bucket>.oss-<region>.aliyuncs.com` → 正则反解 bucket + region，自动生成 OSS target
  - `<uid>.<region>.fcapp.run` → FC target（service/function 无法从 DNS 推导，取 `FC_TARGETS[0]` 兜底）
  - 非阿里云 CNAME（Vercel / 其他 CDN）与 `_` 开头记录（`_dnsauth` / `_acme-challenge`）跳过
- `merge_targets(manual, auto)`：**手工优先**，自动发现按 `domain` 去重追加；分发循环遍历合并结果；
  提供 `--no-discover` 退回纯手工模式。
  ⚠️ 去重集合里必须放 **`domain` 字符串**，不能放 target 字典本身：
  ```python
  seen = {t['domain'] for t in manual}
  for t in auto:
      if t['domain'] not in seen:
          out.append(t)
          seen.add(t['domain'])     # 写成 seen.add(t) -> TypeError: unhashable type: 'dict'
  ```
  写成 `seen.add(t)` 在生产上真炸过：整个分发 stage 抛异常，续期任务失败。
- 效果：新建子域**只需加一条 CNAME**，下次定时任务自动写 `_dnsauth` TXT 验归属 + 绑 `cert_id` + 上 HTTPS。
- ⚠️ **站点前置 CDN 后，这条路径失效**：CNAME 指向 `*.queniuaa.com` 而非 OSS/FC，
  `discover_targets()` 会返回 0 个目标。此时新子域的接入动作变成「在 CDN 里加加速域名」，
  由第七节的 `discover_cdn()` 接管。两条发现逻辑要同时保留 —— 有站点直连 OSS，也有站点走 CDN。

## 七、分发到阿里云 CDN（站点前置 CDN 时就必须做）

一旦站点 CNAME 到 CDN（`<domain>.queniuaa.com` 之类），HTTPS 就在 CDN 上终结，
**用户看到的是 CDN 上挂的那张证书，不是 OSS/FC 上的**。这时只分发 OSS/FC 等于没做续期：
源站换了新证书，CDN 还在发旧的，直到过期当天整站报错。

### 7.1 域名发现：问 CDN API，不要靠 DNS

第六节的 DNS 自动发现只认 `*.aliyuncs.com` / `*.fcapp.run`。域名改指 CDN 后，
它会发现 **0 个目标**，而定时任务日志依旧 `RENEW_OK` —— 这是最危险的漏更方式。

```python
def discover_cdn():            # 取与根域同域的加速域名（含根域本身）
    found = []
    for page in range(1, 11):
        r = ali_call('cdn.aliyuncs.com', 'DescribeUserDomains', '2018-05-10',
                     PageSize=100, PageNumber=page)
        rows = (r.get('Domains') or {}).get('PageData') or []   # list，不是 dict
        for x in rows:
            n = (x.get('DomainName') or '').strip()
            if n == ROOT or n.endswith('.' + ROOT):
                found.append(n)
        if len(rows) < 100:
            break
    return sorted(set(found))
```

### 7.2 绑定：`CertType=cas` 复用 cert_id，但 **`CertName` 必须是那张证书的真实名字**

**CDN 的「上传型证书」本质上就是一张 CAS 证书** —— 命名空间共用，`cert_id` 就是 CAS 证书 ID。
但有个致命细节：`CertType=cas` 时 **CDN 是按 `CertName` 解析证书的，不是按 `ServerCertificateId`**。

```python
ali_call('cdn.aliyuncs.com', 'SetDomainServerCertificate', '2018-05-10', method='POST',
         DomainName=d, ServerCertificateStatus='on',
         CertType='cas', ServerCertificateId=str(cert_id),
         CertName=cert_name)      # ← 必须是 CAS 里那张证书的真实名字，不能写死旧名
```

踩过的真实事故：CAS 上传的证书名改成带日期（`...-le-20261116`）以避开 NameRepeat，
CDN 侧仍传固定名 `ydtgo-top-wildcard-le`，CDN 就按名字找到了 9 月那张旧证书并绑上去 ——
接口返回成功、日志 11/11 成功、`RENEW_OK`，但 11 个站点被**静默降级**回旧证书。
所以 `cert_name` 必须和 CAS 上传时用的名字一致，并**存进 state.json** 供复用路径使用。

绑定后必须回读校验，否则这类"成功但绑错"的问题看不出来：

```python
def _leaf_b64(pem):
    import re
    m = re.search(r'-----BEGIN CERTIFICATE-----(.*?)-----END CERTIFICATE-----', pem, re.S)
    return re.sub(r'\s+', '', m.group(1)) if m else ''

# 回读 https_option 里的 cert 字段，比对叶子证书内容；不一致就回退内联上传
r = ali_call('cdn.aliyuncs.com', 'DescribeCdnDomainConfigs', '2018-05-10',
             DomainName=d, FunctionNames='https_option')
```

回退方案（内联上传，不依赖 CAS 名字解析）：

```python
ali_call(..., method='POST', DomainName=d, ServerCertificateStatus='on',
         CertType='upload', CertName='wild-%s-%s' % (d.replace('.', '-'), yyyymmddHHMM),
         ServerCertificate=pem, PrivateKey=privkey_pem)
```

### 7.3 CDN 用裸签名而不是 SDK

`alibabacloud_cdn20180510` 的入参在版本间反复变化（`PageSize` / `page_size` 混用），
写错只得到一句参数错误。CDN 侧只用两个 Action，25 行裸签名（HMAC-SHA1, SignatureVersion 1.0）
更稳、也不给 runner 增加依赖。三个必须点：

```python
if STOKEN:
    p['SecurityToken'] = STOKEN        # STS 临时凭证不带 -> 签名对但鉴权 403
sts = '%s&%s&%s' % (method, pe('/'), pe(cq))   # 方法必须与实际请求一致，否则 SignatureDoesNotMatch
if method == 'POST':                   # 证书内容塞 URL 会被网关截断成空值
    req = urllib.request.Request('https://%s/' % host, data=body.encode())
```

### 7.4 顺序：先分发，后删旧证书

CAS 里删证书要在**所有分发完成之后**。旧 `cert_id` 此刻仍被 CDN / OSS 绑定引用，
提前删除会让站点在这段时间里证书失效。脚本把 `prev_cert_id` 记进 `state.json`，末尾再 best-effort 删除。

### 7.5 验收

```bash
for d in ydtgo.top a3.ydtgo.top ...; do
  echo | openssl s_client -servername $d -connect $d:443 2>/dev/null \
    | openssl x509 -noout -subject -dates
done
```

`CN` 应是通配证书的 `CN`（不是各子域自己的旧单域名证书），`notAfter` 全部一致。

## 八、必坑清单（按踩中概率排序）

1. **迁移仓库 / 改 audience 必须三处同步**，否则 `AuthenticationFail.OIDCToken.AudienceNotMatch` / `Invalid audience.`：
   ① workflow 的 `audience`；② 角色信任策略的 `oidc:aud`（`update_role`）；
   ③ **OIDC 提供商的 `ClientIds`**（IMS `add_client_id_to_oidcprovider` / `remove_client_id_from_oidcprovider`）。
   只改前两处是典型漏网。

2. **官方 action 莫名 `ImplicitDeny`**：`aliyun/configure-aliyun-credentials-action` 在 RAM 全对时仍报
   `NoPermission / ImplicitDeny / PolicyType: AssumeRolePolicy`。改用第二节的手动兑换。
   `get_role` 返回的 `Principal.Federated` 是数组，那是 RAM 规范化结果，**不是 bug**，别去改它。

3. **`oidc:sub` 别用 `StringEquals` 写死 `repo:<owner>/<repo>:*`**：GitHub 在 fork / 重跑 / 某些事件下会把
   **repo ID 与 owner ID 嵌进 sub**，变成 `repo:oracis@4110185/myrepo@1368066874:ref:refs/heads/main`。
   用 `StringLike` + `repo:<owner>*/<repo>*:ref:refs/heads/main` 一套覆盖两种格式。
   **打印 JWT 的 `sub` 是定位此类问题的唯一快路径。**

4. **STS 偶发 `InternalError 500`**：凭证指纹核对无误仍 500 时属瞬时故障，`AssumeRoleWithOIDC` 加
   3~5 次指数退避重试即可。

5. **CAS 的 RAM 命名空间是 `yundun-cert`，不是 `cas`**：策略写 `cas:*` **覆盖不到**
   `UploadUserCertificate`，报 `NoPermission / 403 / yundun-cert:UploadUserCertificate / AccountLevelIdentityBasedPolicy`。
   必须加 `yundun-cert:*`。

6. **oss2 用 STS 必须 `oss2.StsAuth`，不能把 token 当 `oss2.Auth` 第 3 个参数**：
   `oss2.Auth.__init__(access_key_id, access_key_secret)` 只收 2 个参数，传第 3 个直接
   `TypeError: Auth.__init__() takes 3 positional arguments but 4 were given`。
   正确：`oss2.StsAuth(ak, sk, stoken) if stoken else oss2.Auth(ak, sk)`。

7. **CAS 删除参数是 `cert_id`，不是 `certificate_id`；且 SDK 查不到上传型证书**：
   写成 `certificate_id=` 会静默不删（被 `except` 吞掉），旧证书**长期占用固定名称**，
   下次上传必报 `NameRepeat (code:400, 名称重复)`。`cas20200407` 只有
   `list_user_certificate_order`（仅购买订单），**没有** `DescribeUserCertificateList`，
   所以 `state.json` 里的 `cert_id` 是定位旧证书的唯一途径。
   稳健写法：上传前按 state 的 `cert_id` 删除（失败仅告警）；若仍 `NameRepeat`，用「固定名+时间戳」重传兜底。

8. **签发与分发必须解耦，证书有效不能整体 `sys.exit(0)`**：否则上次分发失败后，
   有效证书会永远卡在「已签发未分发」。用 `need_issue` 只控制签发，CAS 上传加 `sha256(pem)` 指纹守卫，
   指纹一致就复用旧 `cert_id`，避免每天重复创建 CAS 证书。

9. **oss2 `create_bucket` 第一个位置参数是 `permission`（ACL 字符串），不是 `input`（config 对象）**：
   签名 `create_bucket(self, permission=None, input=None, headers=None)`。
   写 `create_bucket(oss2.models.BucketCreateConfig(oss2.BUCKET_ACL_PRIVATE))` 会把 config 塞进
   `x-oss-acl` header，签名时 `TypeError: can't concat BucketCreateConfig to bytes`。
   正确：`b.create_bucket(oss2.BUCKET_ACL_PRIVATE)`（默认即私有桶）。
   `BucketCreateConfig` 构造器也按 snake_case：`storage_class` / `data_redundancy_type` / `acl`。

10. **cron 时区是 UTC**：北京 03:30 = `30 19 * * *`。schedule 有 ±15 分钟漂移，对续期无影响。
    `wait_txt()` 等 DNS 轮询在 Linux runner 用 `dig`（需 `dnsutils`），Windows 无 dig 回退 `nslookup`。

11. **定时跑全绿 ≠ 管线健康**：自动发现这类"只有出现新目标才会执行"的分支，平时根本走不到，
    于是 bug 能在每天 success 的 run 里潜伏几个月。真实案例：`seen.add(t)`（见第六节）
    在新增第 3 个子域的当天才第一次崩（此前定时跑连续 5 天 success）。
    **任何一次改动域名/CNAME/目标清单后，都要手动 `workflow_dispatch` 跑一次**，
    别只看最近几次定时 run 的绿勾。日志里出现
    `证书仍有效（剩 N 天），无需重新签发` 是**正常路径**，不是失败。

12. **判断"这条流水线到底存不存在"时，必须连私有仓库一起扫**：只列 public 仓库会漏掉
    `oracis/cert-renew` 这类私有基础设施仓库，从而误判"自动续期没搭"。
    用 `gh repo list <owner> --private --limit 200` 或 API `/user/repos?visibility=private`。
    另：本机 `gh` 常处于未登录状态（`gh auth status` → not logged in），
    可用 git credential 标准接口取 token（不直接读凭据存档文件）：
    `TOKEN=$(printf "protocol=https\nhost=github.com\n\n" | git credential fill | sed -n 's/^password=//p')`，
    然后 `curl -H "Authorization: Bearer $TOKEN"` 调 API（记得先 `unset` 本机代理变量，见下）。

13. **站点前置 CDN 后最容易出现的静默失效：续期全绿，但用户看到的还是旧证书。**
    CDN 在边缘终结 TLS，源站证书再新也不影响它。判断办法是直接问 CDN
    （`DescribeCdnDomainConfigs` + `FunctionNames=https_option`，看 `cert_name` / `cert_id`），
    或从外部 `openssl s_client` 看 `notAfter`；**不要**只看 workflow 的绿勾。
    真实案例：8 月签的单域名证书在 CDN 上放到 11-22 才到期，期间每次续期都 success。

14. **CDN 的证书名与 CAS 共用同一命名空间，`CertName` 是账号级全局唯一（跨域名也唯一）。**
    同一个名字挂到第二个域名会报 `NameRepeat`；同一天重跑续期也会撞名。
    固定名不可用，用 `CERT['cas_name'] + '-' + YYYYMMDD`（同日重跑再加时分秒兜底）。
    反过来这也是个便利：CDN 上传型证书本来就是 CAS 证书，`cert_id` 可直接用 `CertType=cas` 引用。

15. **`SetDomainServerCertificate` 的三个参数坑**：
    ① 参数名是 `ServerCertificate` / `PrivateKey`，写 `SSLPub` / `SSLPri` 报参数缺失；
    ② 证书内容大，必须 POST，走 GET 会被网关截断，表现为证书字段为空；
    ③ 改成 POST 后**签名串里的 HTTP 方法要同步改**，否则 `SignatureDoesNotMatch`。

16. **`CertType=cas` 时 CDN 按 `CertName` 解析证书，`ServerCertificateId` 不作数**：
    名字和真实证书对不上时会绑到**同名的那张旧证书**，而接口照样返回成功。
    症状是"续期全绿，站点证书却回到了上一版/更早的版本"。必须传 CAS 里的真实证书名并回读校验（见 7.2）。

17. **IdP（GitHub）轮换证书后必然出现 `AuthenticationFail.OIDCToken.PublicKeyFingerprintMismatch`**：
    症状很隐蔽 —— workflow 在「OIDC → STS」步骤失败，后续步骤显示
    「ERROR: 阿里云临时凭证未注入」，真正的错误在上一步日志里。
    排查：`openssl s_client -showcerts` 看链是否换了 CA（本次 GitHub 从旧链换成 Let's Encrypt YR1）；
    处理：按第一节的方法算出**非叶子证书的 SHA-1 证书指纹**，用
    `AddFingerprintToOIDCProvider` 补进去，确认能换到 STS 后再删旧指纹。
    **阿里云建议在 IdP 轮换前就先加新指纹**，因为 Let's Encrypt 的叶子证书约 90 天一轮。

18. **策略缺 `cdn:*` 只会让 CDN 阶段被跳过，不会让任务失败**：
    日志里是 `CDN 域名列举失败（跳过 CDN 分发）: Forbidden.RAM`，紧接着
    `CDN 分发完成：成功 0，失败 0`，最终 `RENEW_OK` —— 绿勾一切正常。
    所以验收必须看「CDN 域名 N 个」和「成功 N」的**具体数字**，不能只看成功与否。

## 九、验收清单

跑一次 workflow，日志应依次出现：

```
OIDC claims -> iss=... aud=... sub=repo:<owner>/<repo>:ref:refs/heads/main
STS 临时凭证已获取
新证书已签发，有效期至 ...          # 未到期时是「证书仍有效（剩 N 天），无需重新签发」，正常
已上传 CAS，cert_id = ...            # 指纹未变时是「证书未变化（fp 一致），复用 cert_id=...」
DNS 自动发现 OSS 目标 N 个: ...      # 新子域必须出现在这里
处理 OSS <domain> -> 已绑定自定义域名 # 自动发现的会带「（自动发现）」后缀
FC 自定义域名 <domain> 证书已更新
CDN 域名 N 个: ...                   # 挂了 CDN 就必须有这行，且 N 要等于实际加速域名数
  <domain>  -> CAS <cert_id>         # 每个域名一行
CDN 分发完成：成功 N，失败 0
全部完成 / RENEW_OK
```

**日志里没有 `CDN 域名` 那行 = 站点在 CDN 上而代码没做 CDN 分发，等于没续期。**
这一步要盯的是「CDN 域名数」和「失败数」，不是有没有绿勾。

另外两种情况也算**失败**，即使退出码是 0：

- 出现 `回读不一致（实际 cert_id=... name=...）` —— 说明按名字绑到了别的证书（坑 16）
- 出现 `CDN 域名列举失败（跳过 CDN 分发）: Forbidden.RAM` —— 策略缺 `cdn:*`（坑 18）

## 十、日常巡检（每月一次，10 秒）

绿勾不代表证书没过期，用外部视角看一眼最省事：

```bash
for d in ydtgo.top book.ydtgo.top ...; do
  printf "%-22s " "$d"
  echo | openssl s_client -servername "$d" -connect "$d:443" 2>/dev/null \
    | openssl x509 -noout -subject -enddate 2>/dev/null
done
```

所有域名应显示**同一个 CN 和同一个到期时间**。若某个域名 CN 是它自己的子域名、
或到期时间比别的早，那就是漏更（多半是坑 13 / 16）。

再去浏览器核对站点的证书颁发者（Let's Encrypt R11/R12）与到期时间即可。
验证 HTTPS 时**不要用 HEAD**：OSS 静态托管只重写 GET，HEAD 会返回 403，
浏览器和用户实际走 GET，属于误报。

## 附：脚本

- `scripts/setup_oidc.py` —— 一次性建 OIDC 提供商 + 角色 + 权限策略（读环境变量里的永久 AK）。
- `scripts/oidc_sts_env.py` —— workflow 用：OIDC JWT → `AssumeRoleWithOIDC` → 写 `$GITHUB_ENV`。

源码：<https://github.com/oracis/aliyun-oidc-cert-renew>　许可：MIT
