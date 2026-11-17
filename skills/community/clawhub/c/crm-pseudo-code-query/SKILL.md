---
name: crm-pseudo-code-query
description: "同花顺 CRM (crm.10jqka.com.cn) 批量查询用户伪码。此 skill 应在用户提供一批 userid 并需要查询对应的伪码（格式 #数字#，出现在客户详情页联系电话字段）时使用。通过 mTLS 客户端证书加密码三步认证登录 CRM，然后批量抓取客户详情页提取伪码。触发场景：用户说给我伪码、提供 userid 列表、提到同花顺 CRM 伪码查询。使用前需自行配置证书和密码。"
agent_created: true
---

# CRM 批量查询伪码

## Overview

从同花顺 CRM 系统 (crm.10jqka.com.cn) 批量查询 userid 对应的伪码。伪码格式为 `#数字#`，出现在客户详情页的联系电话字段（`class="fake_tel"` 的 input 的 `value` 属性）。

## 前置条件（首次使用需配置）

### 1. mTLS 客户端证书

同花顺 CRM 使用 mTLS 双向认证。需从 macOS Keychain 导出个人客户端证书：

```bash
# 导出 HexinCA 根证书并添加为受信任根
security find-certificate -c "HexinCA" -p > /tmp/hexin_ca.pem
security add-trusted-cert -r trustRoot -k ~/Library/Keychains/login.keychain-db /tmp/hexin_ca.pem

# 导出身份为 PKCS12（会弹出系统对话框，点击"始终允许"）
security export -k ~/Library/Keychains/login.keychain-db -t identities -f pkcs12 -P "temppass" -o /tmp/client_cert.p12

# 从 PKCS12 提取个人证书+私钥
python3 scripts/extract_cert.py --email <your_email> --p12 /tmp/client_cert.p12 --output /tmp/my_cert.pem
```

### 2. CRM 密码

需知道 CRM 登录密码（登录页仅需密码，用户名由 mTLS 证书自动识别）。

### 3. Python 3 + curl

- Python 3 (推荐 3.13+)
- curl 命令行工具

## 快速执行

```bash
python3 scripts/batch_query.py \
  --cert /tmp/my_cert.pem \
  --password <your_password> \
  11010686 485462305 520418276
```

脚本自动完成：三步认证 → 批量查询 → 提取伪码 → 输出汇总表 → 保存结果到 `伪码查询结果.txt`。

## 认证流程（三步）

CRM 使用三步认证，所有步骤在同一个 cookie jar 中完成。详见 `references/auth_flow.md`。

1. **GET 登录页** — 获取初始 PHPSESSID（未认证）
2. **GET 认证 API** — 验证密码，返回 `crm_user_token` + JSON `{"status_code":0,"status_msg":"success"}`
3. **POST 表单** — 用 `crm_user_token` 换取认证 PHPSESSID，返回 `<title>登录成功</title>` + `crm_sale_id` cookie

## 查询伪码

认证后，GET `https://crm.10jqka.com.cn/gb_v3/default/account/clientsdetailsinformation?ai_userid={userid}`，页面为 GBK 编码。伪码在 `class="fake_tel"` input 的 `value="#数字#"` 中。一个 userid 可能有多个电话号码，对应多个伪码。

## 注意事项

- 所有 curl 请求必须带 `--noproxy '*'`（macOS 系统代理 127.0.0.1:7890 会干扰）
- 页面编码 GBK，需 `decode('gbk', errors='replace')`
- 会话约 12 小时过期，查询中途过期时脚本自动重新认证
- 证书文件含私钥，注意安全

## Resources

### scripts/
- `batch_query.py` — 批量查询脚本，通过 `--cert` 和 `--password` 参数传入证书和密码，userid 作为位置参数
- `extract_cert.py` — 证书导出脚本，从 PKCS12 提取指定用户的证书+私钥

### references/
- `auth_flow.md` — CRM 三步认证流程详解、伪码提取方法、网络和证书管理说明

### assets/
- （无）证书文件由用户自行生成，不随 skill 分发
