#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把自定义域名绑定到 OSS 桶并复用已有证书——幂等、零依赖、一次成功。

用法：
  python bind_domain.py --bucket esp32-handbook-hk --region cn-hongkong \
      --domain esp32.ydtgo.top --root ydtgo.top \
      --cert-dir ~/.acme-oss/ydtgo-wild

流程（全部幂等，重复执行安全）：
  1. Upsert CNAME <domain> -> <bucket>.oss-<region>.aliyuncs.com
  2. 取归属验证 token（oss2 create_bucket_cname_token）
  3. Upsert TXT _dnsauth.<子域> = token，等公网 DNS 生效
  4. put_bucket_cname 绑定（复用 cas_id.txt 里的 cert_id）
  5. 删除临时 TXT
  6. 复核绑定状态 + 输出验收

依赖：oss2 + 同目录 aliyun_rpc.py（都用健康包，无坏 SDK）。
"""
import argparse
import os
import subprocess
import sys
import time
from datetime import datetime

# 本机代理会搞挂 oss2；DNS/RPC 又走直连更稳。统一在入口清代理。
for _k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
           "ALL_PROXY", "all_proxy"):
    os.environ.pop(_k, None)

import oss2
from oss2.models import PutBucketCnameRequest
import aliyun_rpc as R


def log(msg):
    print("[%s] %s" % (datetime.now().strftime("%H:%M:%S"), msg), flush=True)


def norm_region(r):
    return r if r.startswith("oss-") else "oss-" + r


def wait_txt(fqdn, token, tries=18, interval=8):
    """用公共 DNS 等 TXT 生效；本机 nslookup 走系统 DNS，秒级。"""
    for i in range(tries):
        try:
            out = subprocess.run(
                ["nslookup", "-type=TXT", fqdn, "223.5.5.5"],
                capture_output=True, text=True, timeout=15).stdout
            if token in out.replace('"', "").replace(" ", ""):
                log("  TXT 已生效（第 %d 次查询）" % (i + 1))
                return True
        except Exception:
            pass
        time.sleep(interval)
    log("  ! TXT %d 次未查到，仍继续尝试绑定" % tries)
    return False


class _Cert:
    """oss2 的 cert 参数对象；force 必须是字符串 'true'（传 1 会 MalformedXML）"""
    def __init__(self, cert_id):
        self.cert_id = str(cert_id) if cert_id else None
        self.certificate = None
        self.private_key = None
        self.previous_cert_id = None
        self.force = "true"
        self.delete_certificate = None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bucket", required=True)
    ap.add_argument("--region", default="cn-hongkong")
    ap.add_argument("--domain", required=True, help="如 esp32.ydtgo.top")
    ap.add_argument("--root", required=True, help="根域，如 ydtgo.top")
    ap.add_argument("--cert-dir", default="~/.acme-oss/ydtgo-wild")
    ap.add_argument("--cert-id", type=int, default=0, help="可选，覆盖自动读取的 cert_id")
    args = ap.parse_args()

    region = norm_region(args.region)
    target = "%s.%s.aliyuncs.com" % (args.bucket, region)
    cert_dir = os.path.expanduser(args.cert_dir)
    auth = oss2.Auth(R.AK, R.SK)
    b = oss2.Bucket(auth, "https://%s.aliyuncs.com" % region, args.bucket)

    # 桶存在性预检（避免上传/绑定时 NoSuchBucket 才报错）
    try:
        b.get_bucket_info()
        log("桶 %s 存在（%s）" % (args.bucket, region))
    except oss2.exceptions.NoSuchBucket:
        log("✗ 桶不存在，请先用 build 流程建桶：python deploy_oss.py --check 或手动建桶")
        sys.exit(1)

    # cert_id
    cert_id = args.cert_id or R.cas_find_cert_id(cert_dir)
    if not cert_id:
        log("✗ 找不到 cert_id：请在 %s 放 cas_id.txt，或用 --cert-id 指定" % cert_dir)
        sys.exit(1)
    log("复用 CAS cert_id = %s" % cert_id)

    # 1) CNAME
    sub = args.domain[: -len("." + args.root)] if args.domain != args.root else "@"
    rid = R.dns_upsert(args.root, sub, "CNAME", target)
    log("CNAME %s -> %s (记录 %s)" % (args.domain, target, rid))

    # 2) 取 token + 3) TXT 验证
    try:
        token = b.create_bucket_cname_token(args.domain).token
        log("取得归属验证 token")
        txt_rr = "_dnsauth" if sub == "@" else "_dnsauth." + sub
        txt_rid = R.dns_upsert(args.root, txt_rr, "TXT", token)
        log("写入 TXT %s (记录 %s)" % (txt_rr, txt_rid))
        wait_txt(txt_rr + "." + args.root, token)

        # 4) 绑定
        ok = False
        for attempt in range(3):
            try:
                b.put_bucket_cname(PutBucketCnameRequest(args.domain, _Cert(cert_id)))
                ok = True
                log("✓ 绑定成功：%s -> bucket，cert_id=%s" % (args.domain, cert_id))
                break
            except Exception as e:
                log("第 %d 次绑定失败: %s" % (attempt + 1, str(e)[:140]))
                time.sleep(15)
        # 5) 清理 TXT
        try:
            R.dns_delete(txt_rid)
            log("已清理临时 TXT %s" % txt_rr)
        except Exception:
            pass
        if not ok:
            log("✗ 绑定失败")
            sys.exit(1)
    except Exception as e:
        # 已绑定时取 token 会失败，直接复核是否已是 Enabled
        log("取 token 失败（可能已绑定）: %s" % str(e)[:120])

    # 6) 复核（list_bucket_cname 有秒级传播延迟，刚绑定后立即查可能为空 → 带重试）
    found = False
    for attempt in range(6):
        for c in (b.list_bucket_cname().cname or []):
            if c.domain == args.domain:
                found = True
                cert = getattr(c, "certificate", None)
                log("复核: %s | status=%s | cert_id=%s" % (
                    c.domain, getattr(c, "status", ""),
                    getattr(cert, "cert_id", "") if cert else ""))
                break
        if found:
            break
        if attempt < 5:
            time.sleep(5)
    if not found:
        log("✗ 复核未找到绑定（已重试 6 次）")
        sys.exit(1)
    log("完成。https://%s/ 应可访问（需 index.html 已上传 + 静态托管已配）" % args.domain)


if __name__ == "__main__":
    main()
