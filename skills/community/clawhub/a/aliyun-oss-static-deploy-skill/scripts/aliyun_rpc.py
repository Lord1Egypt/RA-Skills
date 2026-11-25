#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""零依赖阿里云 RPC 客户端（只依赖 requests + oss2，均为健康包）。

为什么存在：alibabacloud_* 官方 SDK 在本机依赖链损坏
（旧版要 Tea.core、新版要 darabonba.model，缺一不可且装不全），
顶层 import 能过、一实例化就 ModuleNotFoundError。用标准 RPC 签名
直调 API 反而稳定，且换机器/换模型不会踩 SDK 版本坑。

API 定义均查自阿里云 OpenAPI 官方门户（2026-11 核实）：
  - DNS   alidns.aliyuncs.com   v2015-01-09  DescribeDomainRecords / AddDomainRecord / DeleteDomainRecord
  - CAS   cas.aliyuncs.com      v2020-04-07  ListUserCertificateOrder（不是 ListUserCertificate！）
  - OSS   <bucket>.oss-<region>.aliyuncs.com  通过 oss2 操作（健康）

凭据只从环境变量读，绝不落盘、不打印。
"""
import base64
import hashlib
import hmac
import json
import os
import time
import uuid
from datetime import datetime, timezone
from urllib.parse import quote, urlencode

import requests

AK = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID", "")
SK = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "")


def _pe(s):
    """阿里云 RPC 的 percent-encode（RFC3986，空格用 %20 不是 +）"""
    return quote(str(s), safe="~").replace("+", "%20")


def call(endpoint, version, action, params=None, proxy=False, timeout=30):
    """通用 RPC 调用，返回解析后的 dict。proxy=False 直连（本机 aliyuncs.com 直连稳定）。"""
    if not AK or not SK:
        raise RuntimeError("缺少 ALIBABA_CLOUD_ACCESS_KEY_ID / SECRET 环境变量")
    p = {
        "Action": action,
        "Version": version,
        "Format": "JSON",
        "AccessKeyId": AK,
        "SignatureMethod": "HMAC-SHA1",
        "SignatureVersion": "1.0",
        "SignatureNonce": str(uuid.uuid4()),
        "Timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    if params:
        p.update({k: v for k, v in params.items() if v is not None})
    canonical = "&".join("%s=%s" % (_pe(k), _pe(v)) for k, v in sorted(p.items()))
    string_to_sign = "GET&%2F&" + _pe(canonical)
    sig = base64.b64encode(
        hmac.new((SK + "&").encode(), string_to_sign.encode(), hashlib.sha1).digest()
    ).decode()
    url = "https://%s/?%s&Signature=%s" % (endpoint, canonical, _pe(sig))
    s = requests.Session()
    s.trust_env = proxy
    r = s.get(url, timeout=timeout)
    data = r.json()
    if r.status_code != 200 or "Error" in data:
        err = data.get("Error", {})
        raise RuntimeError("%s %s -> %s: %s" % (
            action, version, err.get("Code", r.status_code), err.get("Message", "")))
    return data


# ---------------- DNS ----------------
DNS_EP = "alidns.aliyuncs.com"
DNS_VER = "2015-01-09"


def dns_list(root, keyword=None):
    params = {"DomainName": root, "PageSize": 100}
    if keyword:
        params["RRKeyWord"] = keyword
    d = call(DNS_EP, DNS_VER, "DescribeDomainRecords", params)
    return (d.get("DomainRecords") or {}).get("Record") or []


def dns_add(root, rr, type_, value, ttl=600):
    d = call(DNS_EP, DNS_VER, "AddDomainRecord", {
        "DomainName": root, "RR": rr, "Type": type_, "Value": value, "TTL": ttl})
    return d.get("RecordId")


def dns_delete(record_id):
    call(DNS_EP, DNS_VER, "DeleteDomainRecord", {"RecordId": record_id})
    return True


def dns_upsert(root, rr, type_, value, ttl=600):
    """存在则更新、不存在则新增，返回 RecordId。用于幂等写解析。"""
    for r in dns_list(root, rr):
        if r["RR"] == rr and r["Type"] == type_:
            if r["Value"] == value:
                return r["RecordId"]
            call(DNS_EP, DNS_VER, "UpdateDomainRecord", {
                "RecordId": r["RecordId"], "RR": rr, "Type": type_,
                "Value": value, "TTL": ttl})
            return r["RecordId"]
    return dns_add(root, rr, type_, value, ttl)


# ---------------- CAS ----------------
CAS_EP = "cas.aliyuncs.com"
CAS_VER = "2020-04-07"


def cas_list_certs(order_type="UPLOAD", keyword=None):
    """ListUserCertificateOrder：OrderType=CERT|UPLOAD 查证书，CPACK|BUY 查订单。"""
    params = {"OrderType": order_type, "ShowSize": 100, "CurrentPage": 1}
    if keyword:
        params["Keyword"] = keyword
    d = call(CAS_EP, CAS_VER, "ListUserCertificateOrder", params)
    return d.get("CertificateOrderList") or []


def cas_find_cert_id(cert_dir=None):
    """找已上传到 CAS 的 cert_id。

    上传型证书在 ListUserCertificateOrder 里没有 Domain 字段（只有 InstanceId/
    CertificateId/Sha2/EndDate），无法按域名反查；CAS 的 DescribeUserCertificate
    这个 Action 实测返回 404。所以最可靠来源就是签发脚本落盘的 cas_id.txt /
    state.json —— 绑定时直接读它，别去 API 猜。
    """
    if cert_dir is None:
        cert_dir = os.path.expanduser("~/.acme-oss/ydtgo-wild")
    for fn in ("cas_id.txt", "state.json"):
        p = os.path.join(cert_dir, fn)
        if not os.path.exists(p):
            continue
        txt = open(p, encoding="utf-8").read().strip()
        if fn == "cas_id.txt" and txt.isdigit():
            return int(txt)
        if fn == "state.json":
            try:
                v = json.loads(txt).get("cert_id")
                if v:
                    return int(v)
            except Exception:
                pass
    return None


# ---------------- V3 ROA（ACS3-HMAC-SHA256）----------------
# 规则查自阿里云官方《V3 请求结构与签名》（help.aliyun.com/zh/open-api 与
# functioncompute/signature-mechanism，2026-11 核实）：
#   CanonicalRequest = METHOD\n CanonicalURI\n CanonicalQueryString\n
#                      CanonicalHeaders\n SignedHeaders\n HashedRequestPayload
#   CanonicalHeaders 只含 "除 Authorization 外的公共请求头"（host/content-type/x-acs-*），
#   小写、按字典序、每行 "name:value\n"；
#   StringToSign = "ACS3-HMAC-SHA256\n" + hex(sha256(CanonicalRequest))；
#   Signature = hex(hmac_sha256(SK, StringToSign))，key 是裸 SK（不带 "&"）。
# percent-encoding 按 RFC3986（字母/数字/-_ .~ 不编码，空格 %20，星号 %2A）。

def _v3enc(s):
    return quote(str(s), safe="")


def roa_call(endpoint, version, action, method, path, body=None, query=None,
             extra_headers=None, proxy=False, timeout=30):
    """V3 签名的通用 ROA 调用（PUT/POST/GET/DELETE + JSON body）。返回 dict。

    body=None 时不带 Content-Type（GET 等无 body 请求）。
    query 参与 CanonicalQueryString（按 key 字典序、RFC3986 编码）。
    """
    if not AK or not SK:
        raise RuntimeError("缺少 ALIBABA_CLOUD_ACCESS_KEY_ID / SECRET 环境变量")
    body_bytes = json.dumps(body, ensure_ascii=False).encode("utf-8") \
        if body is not None else b""
    payload_hash = hashlib.sha256(body_bytes).hexdigest()

    canon_uri = "/".join(_v3enc(seg) for seg in path.split("/"))
    q = {k: v for k, v in (query or {}).items() if v is not None}
    canon_query = "&".join("%s=%s" % (_v3enc(k), _v3enc(v))
                           for k, v in sorted(q.items()))

    hdrs = {
        "host": endpoint,
        "x-acs-action": action,
        "x-acs-version": version,
        "x-acs-date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "x-acs-signature-nonce": uuid.uuid4().hex,
        "x-acs-content-sha256": payload_hash,
    }
    if body_bytes:
        hdrs["content-type"] = "application/json"
    for k, v in (extra_headers or {}).items():
        hdrs[k.lower()] = str(v)
    signed = sorted(hdrs.keys())
    canonical_headers = "".join("%s:%s\n" % (k, hdrs[k]) for k in signed)
    canonical_request = "\n".join([method.upper(), canon_uri, canon_query,
                                   canonical_headers, ";".join(signed),
                                   payload_hash])
    string_to_sign = "ACS3-HMAC-SHA256\n" + \
        hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    sig = hmac.new(SK.encode("utf-8"), string_to_sign.encode("utf-8"),
                   hashlib.sha256).hexdigest()
    auth = "ACS3-HMAC-SHA256 Credential=%s,SignedHeaders=%s,Signature=%s" % (
        AK, ";".join(signed), sig)

    headers = {k: hdrs[k] for k in signed}
    headers["Authorization"] = auth
    url = "https://%s%s%s" % (endpoint, canon_uri,
                              ("?" + canon_query) if canon_query else "")
    s = requests.Session()
    s.trust_env = proxy
    r = s.request(method.upper(), url,
                  data=body_bytes if body_bytes else None,
                  headers=headers, timeout=timeout)
    try:
        data = r.json()
    except Exception:
        data = {}
    if r.status_code < 200 or r.status_code >= 300:
        # FC 3.0 错误体：{RequestId, Code/ErrorCode, ErrorMessage/Message}
        err = data.get("Code") or data.get("ErrorCode") or r.status_code
        msg = data.get("ErrorMessage") or data.get("Message") or r.text[:200]
        raise RuntimeError("%s %s -> %s: %s" % (action, version, err, msg))
    return data


# ---------------- 函数计算 FC 3.0 ----------------
# API 2023-03-30（FC 3.0），endpoint fcv3.<region>.aliyuncs.com。
# UpdateCustomDomain：PUT /2023-03-30/custom-domains/{domainName}，body 含
# certConfig{certName, certificate, privateKey}（传统 RSA PEM，PKCS8 会被拒）。
# PUT 语义为整体替换，务必先 GET 现配置再合并，避免丢路由。
FC_VER = "2023-03-30"


def _fc_ep(region):
    return "fcv3.%s.aliyuncs.com" % region


def fc_list_custom_domains(region, limit=100):
    d = roa_call(_fc_ep(region), FC_VER, "ListCustomDomains", "GET",
                 "/%s/custom-domains" % FC_VER, query={"limit": limit})
    items = d.get("customDomains") or []
    token = d.get("nextToken")
    while token:
        d = roa_call(_fc_ep(region), FC_VER, "ListCustomDomains", "GET",
                     "/%s/custom-domains" % FC_VER,
                     query={"limit": limit, "nextToken": token})
        items += d.get("customDomains") or []
        token = d.get("nextToken")
    return items


def fc_get_custom_domain(region, domain):
    return roa_call(_fc_ep(region), FC_VER, "GetCustomDomain", "GET",
                    "/%s/custom-domains/%s" % (FC_VER, domain))


def fc_update_custom_domain(region, domain, body):
    return roa_call(_fc_ep(region), FC_VER, "UpdateCustomDomain", "PUT",
                    "/%s/custom-domains/%s" % (FC_VER, domain), body=body)
