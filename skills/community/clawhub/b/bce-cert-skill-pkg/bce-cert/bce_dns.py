#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bce_dns.py — 百度智能云 DNS API 操作模块

功能：
  - 查询 Zone ID
  - 添加 / 删除 TXT 记录（用于 ACME DNS-01 验证）

签名方式：BCE Auth V1（使用官方 bce-python-sdk 签名器）

命令行用法（独立测试）：
  python bce_dns.py add _acme-challenge.example.com <txt_value>
  python bce_dns.py del _acme-challenge.example.com <txt_value>
"""

import sys
import os
import time
import json
import datetime
import requests

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.auth import bce_v1_signer


# ============================================================
# 配置加载
# ============================================================

def load_config(config_path=None) -> dict:
    """从 config.conf 加载配置，环境变量优先"""
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
    for key in list(cfg.keys()):
        env = os.environ.get(key)
        if env:
            cfg[key] = env
    return cfg

# 供 acme_client.py / main.py 直接 import 使用
_load_config_for_cli = load_config


# ============================================================
# BCE 签名辅助
# ============================================================

def _make_signed_headers(ak: str, sk: str, method: str, host: str,
                          path: str, params: dict = None) -> dict:
    """
    使用官方 bce-python-sdk 生成签名，返回可直接用于 requests 的 headers dict。
    """
    params = params or {}
    ts_int = int(time.time())
    ts_str = datetime.datetime.fromtimestamp(
        ts_int, tz=datetime.timezone.utc
    ).strftime("%Y-%m-%dT%H:%M:%SZ")

    creds = BceCredentials(
        access_key_id=ak.encode("utf-8"),
        secret_access_key=sk.encode("utf-8"),
    )

    sdk_headers = {
        b"host": host.encode("utf-8"),
        b"x-bce-date": ts_str.encode("utf-8"),
        b"content-type": b"application/json",
    }

    auth_bytes = bce_v1_signer.sign(
        creds,
        method.upper().encode("utf-8"),
        path.encode("utf-8"),
        sdk_headers,
        params,
        timestamp=ts_int,
        expiration_in_seconds=1800,
        headers_to_sign=[b"host", b"x-bce-date"],
    )

    return {
        "Authorization": auth_bytes.decode("utf-8"),
        "x-bce-date": ts_str,
        "Host": host,
        "Content-Type": "application/json",
    }


# ============================================================
# BCE DNS 客户端
# ============================================================

class BCEDnsClient:
    """百度智能云 DNS API 客户端"""

    BASE_URL = "https://dns.baidubce.com"
    HOST = "dns.baidubce.com"

    def __init__(self, access_key_id: str, secret_access_key: str):
        self.ak = access_key_id
        self.sk = secret_access_key

    # ----------------------------------------------------------
    # 内部请求
    # ----------------------------------------------------------

    def _request(self, method: str, path: str,
                 params: dict = None, body: dict = None) -> dict:
        params = params or {}
        headers = _make_signed_headers(
            self.ak, self.sk, method, self.HOST, path, params
        )
        resp = requests.request(
            method,
            self.BASE_URL + path,
            headers=headers,
            params=params,
            json=body,
            timeout=30,
        )
        if resp.status_code not in (200, 201, 204):
            raise RuntimeError(
                f"BCE DNS API 错误 {resp.status_code}: {resp.text}"
            )
        return resp.json() if resp.text.strip() else {}

    # ----------------------------------------------------------
    # Zone 查询
    # ----------------------------------------------------------

    def get_zone_name(self, domain: str) -> str:
        """
        根据域名找到对应的 DNS Zone 名称。
        如 _acme-challenge.example.com → example.com
        """
        # 从最长到最短依次尝试，找到匹配的 zone
        parts = domain.lstrip("_").split(".")
        for i in range(len(parts) - 1):
            candidate = ".".join(parts[i:])
            try:
                result = self._request("GET", "/v1/dns/zone", {"name": candidate})
                for zone in result.get("zones", []):
                    if zone["name"] == candidate:
                        return candidate
            except RuntimeError:
                continue
        raise RuntimeError(
            f"找不到域名 [{domain}] 对应的 DNS Zone，"
            "请确认域名已在百度云 DNS 托管"
        )

    # 保留旧接口兼容性
    def get_zone(self, domain: str) -> tuple:
        zone_name = self.get_zone_name(domain)
        return zone_name, zone_name  # (zone_name, zone_name) 兼容旧调用

    def list_zones(self) -> list:
        """列出所有 Zone（调试用）"""
        result = self._request("GET", "/v1/dns/zone", {})
        return result.get("zones", [])

    # ----------------------------------------------------------
    # TXT 记录操作
    # ----------------------------------------------------------

    def add_txt(self, fulldomain: str, txt_value: str, ttl: int = 300) -> str:
        """
        添加 TXT 记录。
        fulldomain: 完整域名，如 _acme-challenge.example.com
        返回新记录的 ID（百度云 POST 成功返回空 body，ID 需从 GET 查询）。
        """
        zone_name = self.get_zone_name(fulldomain)
        rr = self._extract_rr(fulldomain, zone_name)

        body = {
            "rr": rr,
            "type": "TXT",
            "value": txt_value,
            "ttl": ttl,
        }
        # POST /v1/dns/zone/{zoneName}/record — 成功返回 200 空 body
        self._request("POST", f"/v1/dns/zone/{zone_name}/record", body=body)
        print(f"[DNS] 已添加 TXT: {rr}.{zone_name} = \"{txt_value}\"")
        return rr

    def del_txt(self, fulldomain: str, txt_value: str) -> int:
        """
        删除匹配的 TXT 记录。
        返回删除的记录数量。
        """
        zone_name = self.get_zone_name(fulldomain)
        rr = self._extract_rr(fulldomain, zone_name)

        result = self._request(
            "GET", f"/v1/dns/zone/{zone_name}/record",
            params={"rr": rr, "type": "TXT"},
        )
        records = result.get("records", [])

        deleted = 0
        for rec in records:
            val = rec.get("value", "").strip('"')
            if val == txt_value:
                self._request(
                    "DELETE",
                    f"/v1/dns/zone/{zone_name}/record/{rec['id']}",
                )
                print(f"[DNS] 已删除 TXT: {rr}.{zone_name} (id={rec['id']})")
                deleted += 1

        if deleted == 0:
            print(f"[DNS] 未找到匹配的 TXT 记录: {rr}.{zone_name} = \"{txt_value}\"")
        return deleted

    # ----------------------------------------------------------
    # 工具方法
    # ----------------------------------------------------------

    @staticmethod
    def _extract_rr(fulldomain: str, zone_name: str) -> str:
        """从完整域名中提取相对于 zone 的子域名部分（RR）"""
        suffix = f".{zone_name}"
        if fulldomain.endswith(suffix):
            return fulldomain[: -len(suffix)]
        if fulldomain == zone_name:
            return "@"
        return fulldomain


# ============================================================
# 命令行入口（独立测试用）
# ============================================================

def main():
    if len(sys.argv) < 4:
        print("用法: python bce_dns.py <add|del|list> <fulldomain> <txtvalue>")
        print("示例: python bce_dns.py add _acme-challenge.example.com abc123")
        print("      python bce_dns.py list - -")
        sys.exit(1)

    action = sys.argv[1]
    fulldomain = sys.argv[2]
    txtvalue = sys.argv[3] if len(sys.argv) > 3 else ""

    cfg = load_config()
    ak = cfg.get("BCE_ACCESS_KEY_ID", "")
    sk = cfg.get("BCE_SECRET_ACCESS_KEY", "")
    ttl = int(cfg.get("DNS_TTL", 300))

    if not ak or ak == "your_access_key_id_here":
        print("[ERROR] 请在 config.conf 中填写 BCE_ACCESS_KEY_ID")
        sys.exit(1)
    if not sk or sk == "your_secret_access_key_here":
        print("[ERROR] 请在 config.conf 中填写 BCE_SECRET_ACCESS_KEY")
        sys.exit(1)

    client = BCEDnsClient(ak, sk)

    if action == "list":
        zones = client.list_zones()
        for z in zones:
            print(f"  id={z['id']}  name={z['name']}  status={z['status']}")
    elif action == "add":
        client.add_txt(fulldomain, txtvalue, ttl)
    elif action == "del":
        client.del_txt(fulldomain, txtvalue)
    else:
        print(f"[ERROR] 未知操作: {action}")
        sys.exit(1)


if __name__ == "__main__":
    main()
