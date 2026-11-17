# CRM 认证流程详解

## 背景

同花顺 CRM (crm.10jqka.com.cn) 使用多层认证：
1. **mTLS 客户端证书** — TLS 层身份认证，证书由 HexinCA 签发
2. **密码认证** — 应用层密码登录
3. **PHP 会话** — 认证后的 PHPSESSID 会话管理

没有 mTLS 证书，服务器返回"你不允许在外网访问本系统"。
有证书但没有认证会话，服务器重定向到登录页。

## 三步认证流程

所有步骤必须在同一个 cookie jar 中完成（PHPSESSID 需要在步骤间保持）。

### Step 1: GET 登录页

```
curl -k --cert ~/my_cert.pem --key ~/my_cert.pem \
  --noproxy '*' -c jar.txt \
  "https://crm.10jqka.com.cn/gb_v3/default/index/login"
```

**目的**: 获取初始 PHPSESSID（未认证状态）

**响应**: HTML 页面，包含：
- `user_name='<你的姓名>'` — mTLS 证书已识别用户
- `user_id='<你的user_id>'` — CRM 用户 ID
- 密码输入框和 JavaScript 认证逻辑
- `set-cookie: PHPSESSID=xxx`

### Step 2: GET 认证 API

```
curl -k --cert ~/my_cert.pem --key ~/my_cert.pem \
  --noproxy '*' -b jar.txt -c jar.txt \
  "https://crm.10jqka.com.cn/auth/crm/cloud-software/auth/login?password=<你的密码>&mailFlag=0&email="
```

**目的**: 验证密码，获取 crm_user_token

**响应**: JSON `{"status_code":0,"status_msg":"success","data":null}`

**Set-Cookie**:
- `crm_user_token=xxx` — 认证 token
- `X-Token=` (空值)

**注意**: 此步骤只验证密码，PHPSESSID 仍未认证。需要 Step 3。

### Step 3: POST 表单

```
curl -k --cert ~/my_cert.pem --key ~/my_cert.pem \
  --noproxy '*' -b jar.txt -c jar.txt \
  -X POST -d "state=1&oldurl=&mailFlag=0&password=*&si_passwd=<你的密码>" \
  "https://crm.10jqka.com.cn/gb_v3/default/index/login"
```

**目的**: 用 crm_user_token 换取认证 PHPSESSID

**表单字段**:
- `state=1` — 固定值
- `oldurl=` — 空（原始 URL ）
- `mailFlag=0` — 邮件标记
- `password=*` — 掩码后的密码（不重要）
- `si_passwd=<你的密码>` — 真实密码（JavaScript 从 passwordHide hidden field 获取）

**成功响应**: HTML `<title>登录成功</title>`

**Set-Cookie**:
- `crm_sale_id=<你的sale_id>` — 销售人员 ID
- `logTime=xxx` — 登录时间戳

**失败情况**: 如果返回登录页而非"登录成功"，检查：
1. Step 2 是否成功（密码是否正确）
2. Cookie jar 是否在步骤间保持一致
3. crm_user_token 是否被正确设置

## 伪码提取

认证后，访问客户详情页：
```
GET https://crm.10jqka.com.cn/gb_v3/default/account/clientsdetailsinformation?ai_userid={userid}
```

页面编码: GBK

伪码在 HTML 中的位置:
```html
<font color="red">手机-移动(浙江-温州):</font>
<input type="text" id="ai_tel_0" class="fake_tel" value="#83465779#">
```

一个 userid 可能有多个电话号码（手机、座机等），每个对应一个伪码。

提取正则:
```python
re.findall(
    r'<font[^>]*>([^<]*)</font>\s*<input[^>]*class="fake_tel"[^>]*value="#(\d+)#"',
    html
)
```

## 会话过期处理

PHPSESSID 会过期（约 12 小时）。查询中途如果返回重定向到登录页（HTTP 302 → `/gb_v3/default/index/login`），重新执行三步认证即可。

## 网络要求

- **必须** `--noproxy '*'` — macOS 系统代理 (127.0.0.1:7890, Clash/V2Ray) 会干扰 CRM 连接
- **必须** `--cert` + `--key` — mTLS 双向认证
- **必须** `-k` — 忽略服务器证书验证（HexinCA 不在系统信任链中，需要单独添加）

## 证书管理

### 证书信任

HexinCA 需添加为受信任根证书（一次性操作）:
```bash
security add-trusted-cert -r trustRoot -k ~/Library/Keychains/login.keychain-db assets/hexin_ca.pem
```

验证:
```bash
security find-identity -v | grep <你的邮箱>
```

### 证书重新导出

如果 `assets/my_cert.pem` 丢失（如系统重装），运行 `scripts/extract_cert.py`。

前置操作（需要用户在系统弹窗点击"始终允许"）:
```bash
security export -k ~/Library/Keychains/login.keychain-db -t identities -f pkcs12 \
  -P "temppass" -o /tmp/client_cert.p12
```

然后运行:
```bash
python3 scripts/extract_cert.py
```

脚本会从 PKCS12 中匹配 `<你的邮箱>@myhexin.com` 的证书和对应私钥（通过 modulus 对比），写入 `assets/my_cert.pem` 和 `~/my_cert.pem`。
