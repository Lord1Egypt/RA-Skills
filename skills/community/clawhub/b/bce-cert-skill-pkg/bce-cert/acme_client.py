#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
acme_client.py — 轻量 ACME v2 客户端

功能：
  - 向 Let's Encrypt 申请 / 续期 SSL 证书
  - 使用 DNS-01 Challenge（通过 bce_dns.py 操作百度云 DNS）
  - 支持通配符证书（*.example.com）
  - 证书保存到本地目录

依赖：
  pip install requests cryptography
"""

import os
import sys
import json
import time
import base64
import hashlib
import logging
import subprocess
from pathlib import Path
from datetime import datetime, timezone

import requests
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from cryptography.x509.oid import NameOID

# ============================================================
# 日志
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("acme")

# ============================================================
# 工具函数
# ============================================================

def b64url(data: bytes) -> str:
    """Base64 URL 编码（无填充）"""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def load_config(config_path: str = None) -> dict:
    """加载 config.conf，环境变量优先"""
    cfg = {}
    if config_path is None:
        config_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "config.conf"
        )
    if os.path.exists(config_path):
        with open(config_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    cfg[k.strip()] = v.strip()
    # 环境变量覆盖
    for key in cfg:
        env = os.environ.get(key)
        if env:
            cfg[key] = env
    return cfg


# ============================================================
# ACME v2 客户端
# ============================================================

LETSENCRYPT_DIRECTORY = "https://acme-v02.api.letsencrypt.org/directory"
LETSENCRYPT_STAGING   = "https://acme-staging-v02.api.letsencrypt.org/directory"


class ACMEClient:
    """
    轻量 ACME v2 客户端，支持 DNS-01 Challenge。
    account_key: EC P-256 私钥（PEM bytes）
    staging: 是否使用测试环境（无速率限制，证书无效）
    """

    def __init__(self, account_key_pem: bytes, staging: bool = True):
        self.directory_url = LETSENCRYPT_STAGING if staging else LETSENCRYPT_DIRECTORY
        self._directory = None
        self._nonce = None
        self._account_url = None

        # 加载账号私钥
        self.account_key: ec.EllipticCurvePrivateKey = (
            serialization.load_pem_private_key(account_key_pem, password=None)
        )
        pub = self.account_key.public_key()
        pub_numbers = pub.public_key().public_numbers() if hasattr(pub, "public_key") else pub.public_numbers()
        self._jwk = {
            "crv": "P-256",
            "kty": "EC",
            "x": b64url(pub_numbers.x.to_bytes(32, "big")),
            "y": b64url(pub_numbers.y.to_bytes(32, "big")),
        }
        # JWK Thumbprint（用于 key-authorization）
        jwk_str = json.dumps(self._jwk, sort_keys=True, separators=(",", ":"))
        self._thumbprint = b64url(hashlib.sha256(jwk_str.encode()).digest())

    # ----------------------------------------------------------
    # 目录 & Nonce
    # ----------------------------------------------------------

    @property
    def directory(self) -> dict:
        if self._directory is None:
            self._directory = requests.get(self.directory_url, timeout=30).json()
        return self._directory

    def _new_nonce(self) -> str:
        resp = requests.head(self.directory["newNonce"], timeout=30)
        return resp.headers["Replay-Nonce"]

    def _get_nonce(self) -> str:
        if self._nonce:
            n, self._nonce = self._nonce, None
            return n
        return self._new_nonce()

    # ----------------------------------------------------------
    # JWS 签名
    # ----------------------------------------------------------

    def _sign_request(self, url: str, payload) -> dict:
        """构造 JWS 请求体"""
        nonce = self._get_nonce()
        protected = {
            "alg": "ES256",
            "nonce": nonce,
            "url": url,
        }
        if self._account_url:
            protected["kid"] = self._account_url
        else:
            protected["jwk"] = self._jwk

        protected_b64 = b64url(json.dumps(protected, separators=(",", ":")).encode())

        if payload == "":
            payload_b64 = ""
        else:
            payload_b64 = b64url(json.dumps(payload, separators=(",", ":")).encode())

        signing_input = f"{protected_b64}.{payload_b64}".encode()
        sig_der = self.account_key.sign(signing_input, ec.ECDSA(hashes.SHA256()))
        r, s = decode_dss_signature(sig_der)
        sig = b64url(r.to_bytes(32, "big") + s.to_bytes(32, "big"))

        return {
            "protected": protected_b64,
            "payload": payload_b64,
            "signature": sig,
        }

    def _post(self, url: str, payload, expected_status: int = None) -> requests.Response:
        body = self._sign_request(url, payload)
        resp = requests.post(
            url, json=body,
            headers={"Content-Type": "application/jose+json"},
            timeout=30,
        )
        # 保存下一个 nonce
        if "Replay-Nonce" in resp.headers:
            self._nonce = resp.headers["Replay-Nonce"]
        if expected_status and resp.status_code != expected_status:
            raise RuntimeError(
                f"ACME 请求失败 [{url}] "
                f"status={resp.status_code} body={resp.text[:500]}"
            )
        return resp

    # ----------------------------------------------------------
    # 账号注册
    # ----------------------------------------------------------

    def register(self, email: str) -> str:
        """注册或获取已有账号，返回账号 URL"""
        payload = {
            "termsOfServiceAgreed": True,
            "contact": [f"mailto:{email}"],
        }
        resp = self._post(self.directory["newAccount"], payload)
        if resp.status_code not in (200, 201):
            raise RuntimeError(f"账号注册失败: {resp.text}")
        self._account_url = resp.headers["Location"]
        log.info("ACME 账号: %s", self._account_url)
        return self._account_url

    # ----------------------------------------------------------
    # 申请证书
    # ----------------------------------------------------------

    def issue_cert(
        self,
        domains: list[str],
        cert_dir: str,
        dns_add_fn,
        dns_del_fn,
        propagation_wait: int = 30,
    ) -> dict:
        """
        申请证书。
        domains: 域名列表，如 ["example.com", "*.example.com"]
        cert_dir: 证书保存目录
        dns_add_fn(fulldomain, txt_value): 添加 TXT 记录的回调
        dns_del_fn(fulldomain, txt_value): 删除 TXT 记录的回调
        返回 {"cert": path, "key": path, "fullchain": path}
        """
        cert_dir = Path(cert_dir)
        cert_dir.mkdir(parents=True, exist_ok=True)

        primary_domain = domains[0].lstrip("*.")

        # 1. 生成证书私钥
        cert_key = ec.generate_private_key(ec.SECP256R1())
        cert_key_pem = cert_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        )

        # 2. 提交 Order
        identifiers = [{"type": "dns", "value": d} for d in domains]
        order_resp = self._post(
            self.directory["newOrder"],
            {"identifiers": identifiers},
            expected_status=201,
        )
        order = order_resp.json()
        order_url = order_resp.headers["Location"]
        log.info("Order 创建成功: %s", order_url)

        # 3. 完成每个 Authorization（DNS-01 Challenge）
        added_records = []
        try:
            for auth_url in order["authorizations"]:
                auth = requests.get(auth_url, timeout=30).json()
                domain = auth["identifier"]["value"]

                # 找到 dns-01 challenge
                challenge = next(
                    c for c in auth["challenges"] if c["type"] == "dns-01"
                )
                key_auth = f"{challenge['token']}.{self._thumbprint}"
                txt_value = b64url(hashlib.sha256(key_auth.encode()).digest())
                challenge_domain = f"_acme-challenge.{domain}"

                log.info("DNS-01 验证: %s → TXT=%s", challenge_domain, txt_value)
                dns_add_fn(challenge_domain, txt_value)
                added_records.append((challenge_domain, txt_value))

            # 等待 DNS 传播
            log.info("等待 DNS 传播 %d 秒...", propagation_wait)
            time.sleep(propagation_wait)

            # 4. 通知 ACME 服务器开始验证
            for auth_url in order["authorizations"]:
                auth = requests.get(auth_url, timeout=30).json()
                if auth["status"] == "valid":
                    continue
                challenge = next(
                    c for c in auth["challenges"] if c["type"] == "dns-01"
                )
                self._post(challenge["url"], {})

            # 5. 轮询 Order 状态
            log.info("等待 ACME 验证完成...")
            for _ in range(20):
                time.sleep(5)
                order = requests.get(order_url, timeout=30).json()
                log.info("Order 状态: %s", order["status"])
                if order["status"] == "ready":
                    break
                if order["status"] == "invalid":
                    raise RuntimeError(f"ACME 验证失败: {json.dumps(order, indent=2)}")
            else:
                raise RuntimeError("ACME 验证超时")

        finally:
            # 清理 DNS 记录
            for rec_domain, rec_val in added_records:
                try:
                    dns_del_fn(rec_domain, rec_val)
                except Exception as e:
                    log.warning("删除 DNS 记录失败（可手动清理）: %s", e)

        # 6. 提交 CSR
        csr = (
            x509.CertificateSigningRequestBuilder()
            .subject_name(x509.Name([
                x509.NameAttribute(NameOID.COMMON_NAME, primary_domain),
            ]))
            .add_extension(
                x509.SubjectAlternativeName([
                    x509.DNSName(d) for d in domains
                ]),
                critical=False,
            )
            .sign(cert_key, hashes.SHA256())
        )
        csr_der = csr.public_bytes(serialization.Encoding.DER)

        finalize_resp = self._post(
            order["finalize"],
            {"csr": b64url(csr_der)},
        )
        log.info("CSR 已提交")

        # 7. 等待证书签发
        for _ in range(20):
            time.sleep(5)
            order = requests.get(order_url, timeout=30).json()
            log.info("Order 状态: %s", order["status"])
            if order["status"] == "valid":
                break
            if order["status"] == "invalid":
                log.error("Order 无效: %s", json.dumps(order, indent=2))
                raise RuntimeError(f"Order 无效: {json.dumps(order, indent=2)}")
        else:
            raise RuntimeError("证书签发超时")

        # 8. 下载证书
        cert_resp = requests.get(order["certificate"], timeout=60)
        if cert_resp.status_code != 200:
            raise RuntimeError(f"证书下载失败: {cert_resp.status_code}")
        fullchain_pem = cert_resp.content

        # 分离证书和中间证书
        certs = fullchain_pem.decode().split("-----END CERTIFICATE-----")
        cert_pem = (certs[0] + "-----END CERTIFICATE-----\n").encode()

        # 9. 保存文件
        key_path       = cert_dir / f"{primary_domain}.key"
        cert_path      = cert_dir / f"{primary_domain}.crt"
        fullchain_path = cert_dir / f"{primary_domain}.fullchain.crt"

        key_path.write_bytes(cert_key_pem)
        cert_path.write_bytes(cert_pem)
        fullchain_path.write_bytes(fullchain_pem)

        log.info("证书已保存:")
        log.info("  私钥:     %s", key_path)
        log.info("  证书:     %s", cert_path)
        log.info("  完整链:   %s", fullchain_path)

        return {
            "cert": str(cert_path),
            "key": str(key_path),
            "fullchain": str(fullchain_path),
        }


# ============================================================
# 账号密钥管理
# ============================================================

def load_or_create_account_key(key_path: str) -> bytes:
    """加载或创建 ACME 账号私钥（EC P-256）"""
    key_path = Path(key_path)
    if key_path.exists():
        log.info("加载已有账号密钥: %s", key_path)
        return key_path.read_bytes()

    log.info("生成新账号密钥: %s", key_path)
    key_path.parent.mkdir(parents=True, exist_ok=True)
    key = ec.generate_private_key(ec.SECP256R1())
    pem = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption(),
    )
    key_path.write_bytes(pem)
    return pem


# ============================================================
# 证书有效期检查
# ============================================================

def cert_days_remaining(cert_path: str) -> int:
    """返回证书剩余有效天数，文件不存在返回 -1"""
    p = Path(cert_path)
    if not p.exists():
        return -1
    cert = x509.load_pem_x509_certificate(p.read_bytes())
    delta = cert.not_valid_after_utc - datetime.now(timezone.utc)
    return delta.days
