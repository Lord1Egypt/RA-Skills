#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py — 证书申请/续期主入口

用法：
  python main.py issue    # 首次申请证书
  python main.py renew    # 检查并续期（到期前 RENEW_DAYS 天触发）
  python main.py force    # 强制重新申请（忽略有效期）
  python main.py status   # 查看证书状态

依赖安装：
  pip install requests cryptography
"""

import os
import sys
import logging
import subprocess
from pathlib import Path

from acme_client import (
    ACMEClient,
    load_or_create_account_key,
    cert_days_remaining,
    load_config,
)
from bce_dns import BCEDnsClient

log = logging.getLogger("main")

# ============================================================
# 主流程
# ============================================================

def get_dns_callbacks(cfg: dict):
    """构造 DNS 操作回调函数"""
    ak = cfg.get("BCE_ACCESS_KEY_ID", "")
    sk = cfg.get("BCE_SECRET_ACCESS_KEY", "")
    ttl = int(cfg.get("DNS_TTL", 300))

    if not ak or ak == "your_access_key_id_here":
        raise ValueError("请在 config.conf 中填写 BCE_ACCESS_KEY_ID")
    if not sk or sk == "your_secret_access_key_here":
        raise ValueError("请在 config.conf 中填写 BCE_SECRET_ACCESS_KEY")

    client = BCEDnsClient(ak, sk)

    def dns_add(fulldomain, txt_value):
        client.add_txt(fulldomain, txt_value, ttl)

    def dns_del(fulldomain, txt_value):
        client.del_txt(fulldomain, txt_value)

    return dns_add, dns_del


def do_issue(cfg: dict, force: bool = False):
    """申请或续期证书"""
    domain = cfg.get("DOMAIN", "")
    email  = cfg.get("EMAIL", "")
    cert_dir = cfg.get("CERT_DIR", "./certs")
    renew_days = int(cfg.get("RENEW_DAYS", 30))
    propagation_wait = int(cfg.get("DNS_PROPAGATION_WAIT", 30))

    if not domain or domain == "example.com":
        raise ValueError("请在 config.conf 中填写 DOMAIN")
    if not email or email == "admin@example.com":
        raise ValueError("请在 config.conf 中填写 EMAIL")

    # 证书路径
    primary_domain = domain.lstrip("*.")
    cert_path = Path(cert_dir) / f"{primary_domain}.crt"

    # 检查是否需要续期
    if not force:
        days = cert_days_remaining(str(cert_path))
        if days > renew_days:
            log.info("证书有效期还剩 %d 天，无需续期（阈值 %d 天）", days, renew_days)
            return
        if days >= 0:
            log.info("证书剩余 %d 天，开始续期...", days)
        else:
            log.info("证书不存在，开始申请...")

    # 账号密钥
    script_dir = Path(__file__).parent
    account_key_path = script_dir / "account.key"
    account_key_pem = load_or_create_account_key(str(account_key_path))

    # 初始化 ACME 客户端（测试环境无速率限制）
    staging = cfg.get("STAGING", "true").lower() in ("true", "1", "yes")
    acme = ACMEClient(account_key_pem, staging=staging)
    acme.register(email)
    
    if staging:
        log.info("⚠️  使用测试环境，证书仅供测试，不能用于生产！")

    # 申请域名列表（主域名 + 通配符）
    domains = [primary_domain, f"*.{primary_domain}"]
    log.info("申请证书域名: %s", domains)

    # DNS 回调
    dns_add, dns_del = get_dns_callbacks(cfg)

    # 申请证书
    result = acme.issue_cert(
        domains=domains,
        cert_dir=cert_dir,
        dns_add_fn=dns_add,
        dns_del_fn=dns_del,
        propagation_wait=propagation_wait,
    )

    log.info("✅ 证书申请成功！")
    for k, v in result.items():
        log.info("  %s: %s", k, v)

    # 执行续期后钩子
    renew_hook = cfg.get("RENEW_HOOK", "").strip()
    if renew_hook:
        log.info("执行续期钩子: %s", renew_hook)
        ret = subprocess.run(renew_hook, shell=True)
        if ret.returncode != 0:
            log.warning("续期钩子执行失败（返回码 %d）", ret.returncode)


def do_status(cfg: dict):
    """查看证书状态"""
    domain = cfg.get("DOMAIN", "example.com").lstrip("*.")
    cert_dir = cfg.get("CERT_DIR", "./certs")
    cert_path = Path(cert_dir) / f"{domain}.crt"

    days = cert_days_remaining(str(cert_path))
    if days < 0:
        print(f"❌ 证书不存在: {cert_path}")
    elif days <= 7:
        print(f"🔴 证书即将过期！剩余 {days} 天 ({cert_path})")
    elif days <= 30:
        print(f"🟡 证书剩余 {days} 天 ({cert_path})")
    else:
        print(f"✅ 证书有效，剩余 {days} 天 ({cert_path})")


# ============================================================
# 入口
# ============================================================

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    action = sys.argv[1] if len(sys.argv) > 1 else "renew"

    # 支持 --config 参数指定配置文件路径
    config_path = None
    if "--config" in sys.argv:
        idx = sys.argv.index("--config")
        if idx + 1 < len(sys.argv):
            config_path = sys.argv[idx + 1]

    cfg = load_config(config_path)

    if action == "issue":
        do_issue(cfg, force=False)
    elif action == "renew":
        do_issue(cfg, force=False)
    elif action == "force":
        do_issue(cfg, force=True)
    elif action == "status":
        do_status(cfg)
    else:
        print(f"未知操作: {action}")
        print("用法: python main.py [issue|renew|force|status]")
        sys.exit(1)


if __name__ == "__main__":
    main()
