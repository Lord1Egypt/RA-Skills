from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from web3_client import BinanceWeb3Client, BinanceWeb3Error


def test_direct_mode_disables_env_proxy() -> None:
    client = BinanceWeb3Client(proxy_mode="direct")
    assert client.session.trust_env is False


def test_auto_mode_keeps_env_proxy() -> None:
    client = BinanceWeb3Client(proxy_mode="auto")
    assert client.session.trust_env is True


def test_custom_mode_requires_proxy() -> None:
    try:
        BinanceWeb3Client(proxy_mode="custom")
        assert False
    except BinanceWeb3Error as exc:
        assert "missing_custom_proxies" in str(exc)
