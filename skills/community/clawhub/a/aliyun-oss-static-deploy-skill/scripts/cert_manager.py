#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""阿里云 OSS 自定义域名证书：Let's Encrypt 签发 -> 上传 CAS -> 分发绑定。

泛域名一次覆盖所有子域，新增站点只加 --domain，不必重签。

依赖（全部健康包，零官方 SDK）：
    pip install acme josepy cryptography oss2 requests
    DNS / CAS 走同目录 aliyun_rpc.py（纯 RPC 签名，只依赖 requests）

环境变量（只从这里读，绝不落盘）：
    ALIBABA_CLOUD_ACCESS_KEY_ID / ALIBABA_CLOUD_ACCESS_KEY_SECRET

用法：
    python cert_manager.py --root example.com --email you@example.com \
        --bucket my-site-hk --region cn-hongkong --domain www.example.com
    python cert_manager.py --root example.com --domain a.example.com --targets oss   # 只分发
    python cert_manager.py --root example.com --domain a.example.com --force         # 强制重签

退出码：0 成功或无需续期；1 失败
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

import aliyun_rpc as R

DEFAULT_CERT_BASE = os.path.join(os.path.expanduser("~"), ".acme-oss")


def log(msg):
    print("[%s] %s" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg), flush=True)


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="根域，如 example.com")
    ap.add_argument("--email", required=True, help="ACME 账号邮箱")
    ap.add_argument("--domains", default="", help="逗号分隔，默认 <root>,*.<root>")
    ap.add_argument("--bucket", default="", help="OSS Bucket 名（需要绑定自定义域名时给）")
    ap.add_argument("--region", default="cn-hongkong", help="OSS 地域，默认 cn-hongkong")
    ap.add_argument("--domain", action="append", default=[], help="要绑定的自定义域名，可重复")
    ap.add_argument("--cas-name", default="", help="CAS 证书名，默认 <root 去点>-le")
    ap.add_argument("--cert-dir", default="", help="证书与 ACME 账号存放目录")
    ap.add_argument("--days", type=int, default=30, help="剩余天数阈值，默认 30")
    ap.add_argument("--targets", default="", help="只跑指定阶段，逗号分隔：cert,cas,oss,fc")
    ap.add_argument("--fc-region", default="cn-hongkong", help="FC 所在地域，默认 cn-hongkong")
    ap.add_argument("--fc-domain", action="append", default=[],
                    help="FC 自定义域名，可重复；缺省则自动分发到 FC 账号下所有匹配 --domains 的域名")
    ap.add_argument("--force", action="store_true", help="忽略剩余天数，强制重签")
    ap.add_argument("--fix-cname", action="store_true", help="绑定后把 CNAME 修正到桶标准域名")
    return ap.parse_args()


def traditional_pem(key):
    """CAS / FC 只认传统 RSA PEM，PKCS8 会被拒"""
    from cryptography.hazmat.primitives import serialization

    return key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption(),
    ).decode()


def wait_txt(fqdn, value, timeout=240):
    """轮询公共 DNS，确认 TXT 已生效再让 OSS 去校验"""
    import subprocess

    for _ in range(max(1, timeout // 20)):
        try:
            out = subprocess.run(
                ["nslookup", "-type=TXT", fqdn, "223.5.5.5"],
                capture_output=True, text=True, timeout=40,
            ).stdout
            if value in out:
                return True
        except Exception:
            pass
        time.sleep(20)
    return False


def issue_cert(cfg):
    """DNS-01 签发。返回 (fullchain_pem, private_key_pem)。TXT 增删走 aliyun_rpc。"""
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID
    import josepy as jose
    from acme import challenges, client, messages

    ROOT, CERT_DIR = cfg["root"], cfg["cert_dir"]
    FULLCHAIN = os.path.join(CERT_DIR, "fullchain.pem")
    PRIVKEY = os.path.join(CERT_DIR, "privkey.pem")
    ACCOUNT_KEY = os.path.join(CERT_DIR, "account.key")

    added = []

    def add_txt(name, value):
        rr = name[: -len("." + ROOT)] if name.endswith("." + ROOT) else name
        rid = R.dns_add(ROOT, rr, "TXT", value, ttl=600)
        added.append(rid)
        log("已添加 TXT %s" % rr)

    def cleanup():
        for rid in added:
            try:
                R.dns_delete(rid)
            except Exception:
                pass

    os.makedirs(CERT_DIR, exist_ok=True)
    if os.path.exists(ACCOUNT_KEY):
        acc_key = serialization.load_pem_private_key(
            open(ACCOUNT_KEY, "rb").read(), password=None)
    else:
        acc_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        open(ACCOUNT_KEY, "wb").write(acc_key.private_bytes(
            serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption()))

    jwk = jose.JWKRSA(key=acc_key)
    net = client.ClientNetwork(jwk, user_agent="oss-acme/1.0")
    directory = messages.Directory.from_json(
        net.get("https://acme-v02.api.letsencrypt.org/directory").json())
    acme = client.ClientV2(directory, net)

    try:
        reg = acme.new_account(messages.NewRegistration.from_data(
            email=cfg["email"], terms_of_service_agreed=True))
        net.account = reg
    except Exception as e:
        loc = getattr(e, "location", None)
        if not loc:
            raise
        # 账号已存在：ConflictError 带 location，用它恢复 kid
        net.account = messages.RegistrationResource(
            body=messages.Registration.from_data(
                email=cfg["email"], terms_of_service_agreed=True),
            uri=loc)

    if os.path.exists(PRIVKEY):
        cert_key = serialization.load_pem_private_key(
            open(PRIVKEY, "rb").read(), password=None)
    else:
        cert_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        open(PRIVKEY, "wb").write(cert_key.private_bytes(
            serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption()))

    csr = (x509.CertificateSigningRequestBuilder()
           .subject_name(x509.Name([x509.NameAttribute(
               NameOID.COMMON_NAME, cfg["domains"][0])]))
           .add_extension(x509.SubjectAlternativeName(
               [x509.DNSName(d) for d in cfg["domains"]]), critical=False)
           .sign(cert_key, hashes.SHA256()))

    log("下单 %s" % cfg["domains"])
    order = acme.new_order(csr.public_bytes(serialization.Encoding.PEM))

    tasks = []
    for authz in order.authorizations:
        for ch in authz.body.challenges:
            if isinstance(ch.chall, challenges.DNS01):
                tasks.append((ch,
                              ch.chall.validation_domain_name(authz.body.identifier.value),
                              ch.chall.validation(jwk)))

    try:
        for ch, name, value in tasks:
            add_txt(name, value)
        log("等待 DNS 生效 70 秒")
        time.sleep(70)
        for ch, name, value in tasks:
            acme.answer_challenge(ch, ch.chall.response(jwk))
        order = acme.poll_authorizations(order, datetime.now() + timedelta(seconds=600))
        final = acme.finalize_order(order, deadline=datetime.now() + timedelta(seconds=300))
    finally:
        cleanup()

    pem = final.fullchain_pem
    open(FULLCHAIN, "w", encoding="utf-8").write(pem)
    crt = x509.load_pem_x509_certificate(pem.encode())
    log("新证书已签发，有效期至 %s" % crt.not_valid_after_utc)
    return pem, traditional_pem(cert_key)


def load_local(cert_dir):
    from cryptography.hazmat.primitives import serialization

    pem = open(os.path.join(cert_dir, "fullchain.pem"), encoding="utf-8").read()
    key = serialization.load_pem_private_key(
        open(os.path.join(cert_dir, "privkey.pem"), "rb").read(), password=None)
    return pem, traditional_pem(key)


def days_left(path):
    if not os.path.exists(path):
        return -1
    from cryptography import x509

    cert = x509.load_pem_x509_certificate(open(path, "rb").read())
    return (cert.not_valid_after_utc - datetime.now(timezone.utc)).days


def main():
    args = parse_args()
    AK = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID", "")
    SK = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "")
    if not AK or not SK:
        sys.exit("请先设置 ALIBABA_CLOUD_ACCESS_KEY_ID / ALIBABA_CLOUD_ACCESS_KEY_SECRET")

    targets = [t.strip() for t in args.targets.split(",") if t.strip()] or None

    def DO(t):
        return targets is None or t in targets

    cert_dir = args.cert_dir or os.path.join(DEFAULT_CERT_BASE, args.root)
    os.makedirs(cert_dir, exist_ok=True)
    state_path = os.path.join(cert_dir, "state.json")
    state = {}
    if os.path.exists(state_path):
        try:
            state = json.load(open(state_path, encoding="utf-8"))
        except Exception:
            pass

    domains = [d.strip() for d in args.domains.split(",") if d.strip()] or \
        [args.root, "*." + args.root]
    cas_name = args.cas_name or (args.root.replace(".", "-") + "-le")

    left = days_left(os.path.join(cert_dir, "fullchain.pem"))
    log("当前证书剩余 %s 天（阈值 %s），路径 %s" % (left, args.days, cert_dir))

    if DO("cert"):
        if left > args.days and not args.force:
            log("无需续期，退出")
            return 0
        pem, privkey_pem = issue_cert({
            "root": args.root, "cert_dir": cert_dir,
            "email": args.email, "domains": domains,
        })
    else:
        if left < 0:
            sys.exit("本地没有证书（%s），请先跑一次完整签发" % cert_dir)
        pem, privkey_pem = load_local(cert_dir)
        log("使用本地证书，剩余 %s 天" % left)

    cert_id = None
    if DO("cas"):
        # 上传型证书 list 查不到，旧 cert_id 只能靠本地 state 记录
        old_id = state.get("cert_id")
        if old_id:
            try:
                R.call(R.CAS_EP, R.CAS_VER, "DeleteUserCertificate",
                       {"CertificateId": old_id})
                log("已删除 CAS 旧证书 %s" % old_id)
            except Exception as e:
                log("删除旧证书跳过: %s" % str(e)[:80])
        resp = R.call(R.CAS_EP, R.CAS_VER, "UploadUserCertificate",
                      {"Name": cas_name, "Cert": pem, "Key": privkey_pem})
        cert_id = resp.get("CertificateId") or resp.get("certificateId")
        if not cert_id:
            sys.exit("CAS 上传未返回 CertificateId: %s" % str(resp)[:120])
        state["cert_id"] = cert_id
    else:
        cert_id = state.get("cert_id")
    state["updated"] = datetime.now().strftime("%Y-%m-%d")
    json.dump(state, open(state_path, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    log("CAS cert_id = %s" % cert_id)

    if DO("oss") and args.domain and args.bucket:
        # 本机代理会搞挂 oss2；aliyun_rpc 内部 trust_env=False 直连，不受影响。
        # 只在 OSS 阶段清代理，避免影响 ACME（Let's Encrypt 外网可能需要代理）。
        for _k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
                   "ALL_PROXY", "all_proxy"):
            os.environ.pop(_k, None)
        import oss2
        from oss2.models import PutBucketCnameRequest

        class _Cert(object):
            """oss2 的 cert 参数对象；force 必须是字符串 'true'，传 1 会触发 MalformedXML"""

            def __init__(self, cert_id):
                self.cert_id = str(cert_id) if cert_id else None
                self.certificate = None
                self.private_key = None
                self.previous_cert_id = None
                self.force = "true"
                self.delete_certificate = None

        region = args.region if args.region.startswith("oss-") else "oss-" + args.region
        bk = oss2.Bucket(oss2.Auth(AK, SK),
                         "https://%s.aliyuncs.com" % region, args.bucket)
        target = "%s.%s.aliyuncs.com" % (args.bucket, region)
        try:
            bk.get_bucket_info()
        except oss2.exceptions.NoSuchBucket:
            sys.exit("桶不存在: %s" % args.bucket)

        for domain in args.domain:
            log("处理 OSS %s -> bucket %s" % (domain, args.bucket))
            sub = "@" if domain == args.root else domain[: -len("." + args.root)]

            # 1) CNAME 到桶标准域名（幂等）
            try:
                cname_rid = R.dns_upsert(args.root, sub, "CNAME", target)
                log("  CNAME %s -> %s (记录 %s)" % (domain, target, cname_rid))
            except Exception as e:
                log("  CNAME 设置失败: %s" % str(e)[:120])

            # 2) 取归属验证 token
            token = None
            try:
                token = bk.create_bucket_cname_token(domain).token
                log("  取得归属验证 token")
            except Exception as e:
                log("  取 token 失败（已绑定时正常）: %s" % str(e)[:80])

            # 3) 写 TXT _dnsauth 并等公网生效
            auth_rid = None
            if token:
                try:
                    txt_rr = "_dnsauth" if sub == "@" else "_dnsauth." + sub
                    auth_rid = R.dns_upsert(args.root, txt_rr, "TXT", token)
                    log("  已写入 TXT %s，等待生效" % txt_rr)
                    if not wait_txt(txt_rr + "." + args.root, token):
                        log("  警告：TXT 迟迟未生效，仍会尝试绑定")
                except Exception as e:
                    log("  写 TXT 失败: %s" % str(e)[:120])

            # 4) 绑定（重试）
            for attempt in range(3):
                try:
                    bk.put_bucket_cname(PutBucketCnameRequest(domain, _Cert(cert_id)))
                    log("  已绑定自定义域名（cert_id=%s）" % cert_id)
                    break
                except Exception as e:
                    log("  第 %d 次绑定失败: %s" % (attempt + 1, str(e)[:140]))
                    time.sleep(45)
            if auth_rid:
                try:
                    R.dns_delete(auth_rid)
                except Exception:
                    pass

            # 5) 复核：list_bucket_cname 有秒级传播延迟，刚绑定后立即查可能为空 → 重试
            found = False
            for attempt in range(6):
                try:
                    for c in (bk.list_bucket_cname().cname or []):
                        if c.domain == domain:
                            found = True
                            cert = getattr(c, "certificate", None)
                            log("  复核: %s | status=%s | cert_id=%s" % (
                                c.domain, getattr(c, "status", ""),
                                getattr(cert, "cert_id", "") if cert else ""))
                            break
                except Exception as e:
                    log("  复核查询失败: %s" % str(e)[:100])
                if found:
                    break
                if attempt < 5:
                    time.sleep(5)
            if not found:
                log("  复核未找到绑定（已重试 6 次）: %s" % domain)
                sys.exit(1)

            if args.fix_cname:
                rr = "@" if domain == args.root else domain[: -len("." + args.root)]
                try:
                    for r in R.dns_list(args.root, rr):
                        if (r.get("RR") == rr and r.get("Type") == "CNAME"
                                and r.get("Value") != target):
                            R.call(R.DNS_EP, R.DNS_VER, "UpdateDomainRecord", {
                                "RecordId": r["RecordId"], "RR": rr,
                                "Type": "CNAME", "Value": target, "TTL": 600})
                            log("  CNAME 已修正: %s -> %s" % (r["Value"], target))
                except Exception as e:
                    log("  CNAME 修正失败: %s" % str(e)[:140])

    if DO("fc"):
        # FC 3.0 API（2023-03-30，endpoint fcv3.<region>.aliyuncs.com）。
        # UpdateCustomDomain 是 ROA + V3 签名（ACS3-HMAC-SHA256），由
        # aliyun_rpc.roa_call 处理；PUT 语义为整体替换，所以必须先 GET
        # 现配置，只换 certConfig，protocol/routeConfig/tlsConfig 原样带回。
        fc_domains = args.fc_domain or []
        if not fc_domains:
            fc_domains = [d["domainName"] for d in
                          R.fc_list_custom_domains(args.fc_region)
                          if d["domainName"].endswith("." + args.root) or d["domainName"] == args.root]
            log("FC 未指定 --fc-domain，自动匹配到 %d 个域名: %s" % (len(fc_domains), fc_domains))
        for domain in fc_domains:
            log("处理 FC %s (region=%s)" % (domain, args.fc_region))
            cur = R.fc_get_custom_domain(args.fc_region, domain)
            body = {
                "protocol": cur.get("protocol") or "HTTP,HTTPS",
                "certConfig": {
                    "certName": cas_name,
                    "certificate": pem,
                    "privateKey": privkey_pem,
                },
            }
            if cur.get("routeConfig"):
                body["routeConfig"] = cur["routeConfig"]
            if cur.get("tlsConfig"):
                body["tlsConfig"] = cur["tlsConfig"]
            R.fc_update_custom_domain(args.fc_region, domain, body)
            # 复核：GET 回来 certName 应已是新值（私钥不回传属正常）
            chk = R.fc_get_custom_domain(args.fc_region, domain)
            got = (chk.get("certConfig") or {}).get("certName", "")
            if got == cas_name:
                log("  FC 复核通过: certName=%s | lastModifiedTime=%s" % (
                    got, chk.get("lastModifiedTime")))
            else:
                log("  警告: 复核 certName=%s 与预期 %s 不符" % (got, cas_name))
                sys.exit(1)

    log("全部完成")
    print("RENEW_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
