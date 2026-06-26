from __future__ import annotations

import os
import time
import uuid
from typing import Any, Dict, List, Optional

import requests


CHAIN_ALIASES = {
    "bsc": "56",
    "base": "8453",
    "solana": "CT_501",
    "ethereum": "1",
}

RANK_TYPE_ALIASES = {
    "trending": 10,
    "top_search": 11,
    "alpha": 20,
}


class BinanceWeb3Error(RuntimeError):
    pass


class BinanceWeb3Client:
    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout_sec: Optional[float] = None,
        proxy_mode: str = "auto",
        proxies: Optional[Dict[str, str]] = None,
    ) -> None:
        self.base_url = (base_url or os.getenv("BINANCE_WEB3_BASE_URL") or "https://web3.binance.com").rstrip("/")
        self.timeout_sec = timeout_sec or float(os.getenv("BINANCE_HTTP_TIMEOUT_SEC", "12"))
        self.session = self._build_session(proxy_mode=proxy_mode, proxies=proxies)
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (compatible; AlphaCopilot/0.1)",
                "Accept": "application/json",
            }
        )
        self.proxy_mode = (proxy_mode or "auto").strip().lower()

    def _build_session(self, proxy_mode: str, proxies: Optional[Dict[str, str]]) -> requests.Session:
        session = requests.Session()
        mode = (proxy_mode or "auto").strip().lower()
        if mode not in {"auto", "env", "direct", "custom"}:
            raise BinanceWeb3Error(f"unsupported_proxy_mode:{proxy_mode}")

        # auto/env: follow terminal env proxies when present; direct: always bypass env proxies.
        session.trust_env = mode in {"auto", "env"}
        if mode == "custom":
            session.trust_env = False
            if not proxies:
                raise BinanceWeb3Error("missing_custom_proxies")
            session.proxies.update(proxies)
        return session

    def unified_rank(self, chain_id: str, rank_type: int, size: int = 20) -> List[Dict[str, Any]]:
        data = self._post(
            "/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/unified/rank/list",
            payload={"rankType": rank_type, "chainId": chain_id, "period": 50, "page": 1, "size": size},
            headers={"Accept-Encoding": "identity", "Content-Type": "application/json"},
        )
        if not isinstance(data, dict):
            return []
        tokens = data.get("tokens", [])
        return tokens if isinstance(tokens, list) else []

    def token_meta(self, chain_id: str, contract_address: str) -> Dict[str, Any]:
        data = self._get(
            "/bapi/defi/v1/public/wallet-direct/buw/wallet/dex/market/token/meta/info",
            params={"chainId": chain_id, "contractAddress": contract_address},
            headers={"Accept-Encoding": "identity"},
        )
        return data if isinstance(data, dict) else {}

    def token_audit(self, chain_id: str, contract_address: str) -> Dict[str, Any]:
        payload = {
            "binanceChainId": chain_id,
            "contractAddress": contract_address,
            "requestId": str(uuid.uuid4()),
        }
        return self._post(
            "/bapi/defi/v1/public/wallet-direct/security/token/audit",
            payload,
            headers={"Accept-Encoding": "identity", "source": "agent"},
        )

    def ping_root(self) -> Dict[str, Any]:
        resp = self.session.get(self.base_url, timeout=self.timeout_sec, allow_redirects=True)
        return {"status_code": resp.status_code, "ok": resp.ok, "final_url": str(resp.url)}

    def _get(self, path: str, params: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return self._request("get", f"{self.base_url}{path}", params=params, headers=headers or {})

    def _post(self, path: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return self._request("post", f"{self.base_url}{path}", json=payload, headers=headers or {})

    def _request(self, method: str, url: str, **kwargs: Any) -> Dict[str, Any]:
        delay = 0.6
        last_error: Optional[Exception] = None
        for attempt in range(3):
            try:
                resp = self.session.request(method, url, timeout=self.timeout_sec, **kwargs)
                return self._unwrap(resp)
            except (requests.Timeout, requests.ConnectionError) as exc:
                last_error = exc
                if attempt == 2:
                    break
                time.sleep(delay)
                delay *= 2
        raise BinanceWeb3Error(str(last_error) if last_error else "binance_request_failed")

    def _unwrap(self, resp: requests.Response) -> Dict[str, Any]:
        if resp.status_code >= 400:
            raise BinanceWeb3Error(f"binance_http_{resp.status_code}: {resp.text[:200]}")
        try:
            payload = resp.json()
        except ValueError as exc:
            raise BinanceWeb3Error("binance_invalid_json") from exc
        if not isinstance(payload, dict):
            raise BinanceWeb3Error("binance_invalid_payload")
        if payload.get("success") is False:
            raise BinanceWeb3Error(f"binance_api_error:{payload.get('code')}")
        data = payload.get("data")
        return data if isinstance(data, dict) else {"data": data}
