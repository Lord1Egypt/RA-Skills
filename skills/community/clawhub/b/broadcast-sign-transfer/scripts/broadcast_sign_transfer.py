"""
Broadcast Sign Transfer
========================
完整的 EVM 链转账流程：构造交易 → 签名 → 广播到链上。

支持：
- 原生代币转账（ETH / BNB 等）
- ERC20 Token 转账
- Legacy gas（gasPrice）和 EIP-1559（maxFeePerGas）自动切换

Usage:
    from broadcast_transaction import BroadcastTransaction

    bt = BroadcastTransaction(chain_index="56")  # BSC

    # 原生代币转账
    result = bt.transfer_native(
        to_address="0xRecipient...",
        amount=0.01,
        enable_mev_protection=True,
    )

    # ERC20 转账
    result = bt.transfer_token(
        token_address="0xTokenContract...",
        to_address="0xRecipient...",
        amount=100.0,
    )

    print(result.tx_hash)
    print(result.explorer_url)

Environment variables (必须配置):
    WALLET_PRIVATE_KEY   - 钱包私钥（0x 开头）
    OKX_ACCESS_KEY       - OKX API Key
    OKX_SECRET_KEY       - OKX Secret Key
    OKX_PASSPHRASE       - OKX Passphrase
"""

import os
import hmac
import hashlib
import base64
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

try:
    import requests
except ImportError:
    raise ImportError("请先安装依赖: pip install requests web3")

try:
    from web3 import Web3
except ImportError:
    raise ImportError("请先安装依赖: pip install web3")


# ---------------------------------------------------------------------------
# 链配置（多链扩展只需在这里添加）
# ---------------------------------------------------------------------------

@dataclass
class ChainConfig:
    name:          str           # 链名称
    chain_id:      int           # EVM chain ID（用于签名）
    rpc_url:       str           # RPC 节点
    explorer:      str           # 区块浏览器 tx 前缀
    eip1559:       bool          # 是否支持 EIP-1559 gas
    mev:           bool          # 是否支持 MEV 保护
    native_symbol: str           # 原生代币符号（仅用于日志显示）
    gas_multiplier: float = 1.2  # gas 安全系数

SUPPORTED_CHAINS: dict[str, ChainConfig] = {
    "56": ChainConfig(
        name="BSC",
        chain_id=56,
        rpc_url="https://bsc-dataseed1.binance.org/",
        explorer="https://bscscan.com/tx/",
        eip1559=False,          # BSC 使用 Legacy gas
        mev=True,
        native_symbol="BNB",
    )
}

# Gas 固定值：原生代币转账是协议层常量，所有 EVM 链通用
NATIVE_TRANSFER_GAS = 21000

# OKX API
OKX_BASE_URL   = "https://web3.okx.com"
BROADCAST_PATH = "/api/v6/dex/pre-transaction/broadcast-transaction"

# ERC20 ABI
ERC20_ABI = [
    # transfer：outputs 为空兼容无返回值的老 token（如早期 USDT）
    {
        "name": "transfer",
        "type": "function",
        "inputs": [
            {"name": "_to",    "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "outputs": [],
        "stateMutability": "nonpayable",
    },
    # decimals：token 精度
    {
        "name": "decimals",
        "type": "function",
        "inputs": [],
        "outputs": [{"name": "", "type": "uint8"}],
        "stateMutability": "view",
    },
    # symbol：token 符号（如 USDT）
    {
        "name": "symbol",
        "type": "function",
        "inputs": [],
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
    },
    # name：token 全名备用（symbol 解析失败时使用）
    {
        "name": "name",
        "type": "function",
        "inputs": [],
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
    },
    # balanceOf：转账前校验余额是否充足
    {
        "name": "balanceOf",
        "type": "function",
        "inputs": [{"name": "_owner", "type": "address"}],
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
    },
    # allowance：查询授权额度（用于检查是否需要 approve）
    {
        "name": "allowance",
        "type": "function",
        "inputs": [
            {"name": "_owner",   "type": "address"},
            {"name": "_spender", "type": "address"},
        ],
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
    },
]


# ---------------------------------------------------------------------------
# 返回结果
# ---------------------------------------------------------------------------

@dataclass
class BroadcastResult:
    order_id:    str
    tx_hash:     str
    chain_index: str

    @property
    def explorer_url(self) -> str:
        base = SUPPORTED_CHAINS[self.chain_index].explorer
        return f"{base}{self.tx_hash}"

    @property
    def chain_name(self) -> str:
        return SUPPORTED_CHAINS[self.chain_index].name

    def summary(self) -> str:
        return (
            f"✅ {self.chain_name} 广播成功\n"
            f"Order ID: {self.order_id}\n"
            f"Tx Hash:  {self.tx_hash}\n"
            f"浏览器:   {self.explorer_url}"
        )


# ---------------------------------------------------------------------------
# BroadcastTransaction
# ---------------------------------------------------------------------------

class BroadcastTransaction:
    """
    EVM 链通用转账：构造交易 → 签名 → 广播。
    通过 chain_index 切换链，gas 类型自动适配。
    """

    def __init__(
        self,
        chain_index: str,
        api_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        passphrase: Optional[str] = None,
        private_key: Optional[str] = None,
        timeout: int = 30,
    ):
        if chain_index not in SUPPORTED_CHAINS:
            raise ValueError(
                f"暂不支持链 {chain_index}，"
                f"当前支持：{', '.join(SUPPORTED_CHAINS.keys())}"
            )

        self.chain_index = chain_index
        self.chain       = SUPPORTED_CHAINS[chain_index]
        self.api_key     = api_key     or os.environ.get("OKX_ACCESS_KEY", "")
        self.secret_key  = secret_key  or os.environ.get("OKX_SECRET_KEY", "")
        self.passphrase  = passphrase  or os.environ.get("OKX_PASSPHRASE", "")
        self.private_key = private_key or os.environ.get("WALLET_PRIVATE_KEY", "")
        self.timeout     = timeout
        self.session     = requests.Session()

        if not all([self.api_key, self.secret_key, self.passphrase]):
            raise ValueError(
                "缺少 OKX API 凭证，请设置环境变量：\n"
                "OKX_ACCESS_KEY / OKX_SECRET_KEY / OKX_PASSPHRASE"
            )
        if not self.private_key:
            raise ValueError("缺少钱包私钥，请设置环境变量：WALLET_PRIVATE_KEY")

        self.w3      = Web3(Web3.HTTPProvider(self.chain.rpc_url))
        self.account = self.w3.eth.account.from_key(self.private_key)
        self.address = self.account.address

    # ── OKX API 签名 ────────────────────────────────────────
    def _okx_sign(self, timestamp: str, method: str, path: str, body: str = "") -> str:
        prehash = timestamp + method + path + body
        mac = hmac.new(
            self.secret_key.encode("utf-8"),
            prehash.encode("utf-8"),
            hashlib.sha256,
        )
        return base64.b64encode(mac.digest()).decode("ascii")

    def _okx_headers(self, method: str, path: str, body: str = "") -> dict:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        sign = self._okx_sign(timestamp, method, path, body)
        print(f"   [DEBUG] timestamp: {timestamp}")
        print(f"   [DEBUG] method: {method}")
        print(f"   [DEBUG] path: {path}")
        print(f"   [DEBUG] body: {body}")
        print(f"   [DEBUG] sign: {sign}")
        return {
            "OK-ACCESS-KEY":        str(self.api_key),
            "OK-ACCESS-SIGN":       str(sign),
            "OK-ACCESS-PASSPHRASE": str(self.passphrase),
            "OK-ACCESS-TIMESTAMP":  str(timestamp),
            "Content-Type":         "application/json",
        }
    # ── Gas 参数（根据链自动切换 Legacy / EIP-1559）─────────
    def _gas_params(self) -> dict:
        if self.chain.eip1559:
            fee_history  = self.w3.eth.fee_history(1, "latest", [50])
            base_fee     = fee_history["baseFeePerGas"][-1]
            priority_fee = fee_history["reward"][0][0]
            max_fee      = base_fee * 2 + priority_fee
            print(f"   Gas 类型: EIP-1559 | baseFee={base_fee} priorityFee={priority_fee}")
            return {
                "maxFeePerGas":         max_fee,
                "maxPriorityFeePerGas": priority_fee,
            }
        else:
            gas_price = self.w3.eth.gas_price
            print(f"   Gas 类型: Legacy | gasPrice={gas_price}")
            return {"gasPrice": gas_price}

    # ── 动态估算 Gas + 安全系数 ─────────────────────────────
    def _estimate_gas(self, tx: dict) -> int:
        estimated = self.w3.eth.estimate_gas(tx)
        safe_gas  = int(estimated * self.chain.gas_multiplier)
        print(f"   Gas 估算: {estimated} → 安全值: {safe_gas} (x{self.chain.gas_multiplier})")
        return safe_gas

    # ── 构造基础 tx 字段（通用）─────────────────────────────
    def _base_tx(self) -> dict:
        return {
            "from":    self.address,
            "nonce":   self.w3.eth.get_transaction_count(self.address, "pending"),
            "chainId": self.chain.chain_id,
            **self._gas_params(),
        }

    # ── 签名原生代币转账 ────────────────────────────────────
    def _sign_native_tx(self, to_address: str, amount_wei: int) -> str:
        tx = {
            **self._base_tx(),
            "to":    Web3.to_checksum_address(to_address),
            "value": amount_wei,
            "gas":   NATIVE_TRANSFER_GAS,  # 协议层常量，无需估算
        }
        signed = self.w3.eth.account.sign_transaction(tx, self.private_key)
        return signed.raw_transaction.to_0x_hex()

    # ── 签名 ERC20 Token 转账 ───────────────────────────────
    def _sign_token_tx(self, token_address: str, to_address: str, amount_raw: int) -> str:
        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=ERC20_ABI,
        )
        base = self._base_tx()

        # 先估算 gas
        tx_for_estimate = contract.functions.transfer(
            Web3.to_checksum_address(to_address), amount_raw,
        ).build_transaction(base)
        safe_gas = self._estimate_gas(tx_for_estimate)

        # 用估算值构造最终交易
        tx = contract.functions.transfer(
            Web3.to_checksum_address(to_address), amount_raw,
        ).build_transaction({**base, "gas": safe_gas})

        signed = self.w3.eth.account.sign_transaction(tx, self.private_key)
        return signed.raw_transaction.to_0x_hex()

    # ── 调用 OKX 广播接口 ───────────────────────────────────
    def _broadcast(self, signed_tx: str, enable_mev_protection: bool) -> BroadcastResult:
        if enable_mev_protection and not self.chain.mev:
            raise ValueError(f"链 {self.chain_index}（{self.chain.name}）不支持 MEV 保护")

        body_dict = {
            "chainIndex": self.chain_index,
            "address":    self.address,
            "signedTx":   signed_tx,
        }
        if enable_mev_protection:
            body_dict["extraData"] = json.dumps({"enableMevProtection": True})

        body_str = json.dumps(body_dict, ensure_ascii=False)
        headers  = self._okx_headers("POST", BROADCAST_PATH, body_str)

        resp = self.session.post(
            OKX_BASE_URL + BROADCAST_PATH,
            headers=headers,
            data=body_str.encode("utf-8"),
            timeout=self.timeout,
        )
        resp.raise_for_status()
        data = resp.json()

        if data.get("code") != "0":
            raise Exception(f"广播失败（code={data.get('code')}）: {data.get('msg')}")
        if not data.get("data"):
            raise Exception("广播 API 返回空数据")

        result = data["data"][0]
        return BroadcastResult(
            order_id=result.get("orderId", ""),
            tx_hash=result.get("txHash", ""),
            chain_index=self.chain_index,
        )

    # ── 公开方法：原生代币转账 ──────────────────────────────
    def transfer_native(
        self,
        to_address: str,
        amount: float,
        enable_mev_protection: bool = False,
    ) -> BroadcastResult:
        """
        转账原生代币（ETH / BNB / MATIC 等）。

        Args:
            to_address:            接收方地址（0x 开头）
            amount:                转账金额（人类可读单位，如 0.01）
            enable_mev_protection: 是否开启 MEV 保护

        Returns:
            BroadcastResult（含 tx_hash 和 explorer_url）
        """
        if not to_address or not to_address.startswith("0x"):
            raise ValueError("to_address 格式错误，必须以 0x 开头")
        if amount <= 0:
            raise ValueError("amount 必须大于 0")

        amount_wei = self.w3.to_wei(amount, "ether")
        print(f"📤 原生代币转账: {amount} {self.chain.native_symbol} → {to_address}")
        print(f"   From:  {self.address}")
        print(f"   Chain: {self.chain.name}")

        signed_tx = self._sign_native_tx(to_address, amount_wei)
        print(f"   signed_tx: {signed_tx}")
        return self._broadcast(signed_tx, enable_mev_protection)

    # ── 公开方法：ERC20 Token 转账 ──────────────────────────
    def transfer_token(
        self,
        token_address: str,
        to_address: str,
        amount: float,
        enable_mev_protection: bool = False,
    ) -> BroadcastResult:
        """
        转账 ERC20 Token。

        Args:
            token_address:         Token 合约地址（0x 开头）
            to_address:            接收方地址（0x 开头）
            amount:                转账金额（人类可读单位，如 100.0）
            enable_mev_protection: 是否开启 MEV 保护

        Returns:
            BroadcastResult（含 tx_hash 和 explorer_url）
        """
        if not token_address or not token_address.startswith("0x"):
            raise ValueError("token_address 格式错误，必须以 0x 开头")
        if not to_address or not to_address.startswith("0x"):
            raise ValueError("to_address 格式错误，必须以 0x 开头")
        if amount <= 0:
            raise ValueError("amount 必须大于 0")

        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=ERC20_ABI,
        )
        decimals   = contract.functions.decimals().call()
        symbol     = contract.functions.symbol().call()
        amount_raw = int(amount * (10 ** decimals))

        # 校验余额是否充足
        balance = contract.functions.balanceOf(self.address).call()
        if balance < amount_raw:
            balance_human = balance / (10 ** decimals)
            raise ValueError(
                f"余额不足：当前 {balance_human} {symbol}，需要 {amount} {symbol}"
            )

        print(f"📤 Token 转账: {amount} {symbol} → {to_address}")
        print(f"   From:  {self.address}")
        print(f"   Chain: {self.chain.name}")
        print(f"   Token: {token_address} (decimals={decimals})")

        signed_tx = self._sign_token_tx(token_address, to_address, amount_raw)
        print(f"   signed_tx: {signed_tx}")
        return self._broadcast(signed_tx, enable_mev_protection)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Broadcast Sign Transfer CLI")
    parser.add_argument("--chain", required=True, help="链 ID，如 56 (BSC)")
    sub = parser.add_subparsers(dest="command", required=True)

    # 原生代币转账
    native = sub.add_parser("native", help="原生代币转账（ETH/BNB/MATIC 等）")
    native.add_argument("--to",     required=True,             help="接收方地址")
    native.add_argument("--amount", required=True, type=float, help="转账金额")
    native.add_argument("--mev",    action="store_true",       help="开启 MEV 保护")

    # ERC20 转账
    token = sub.add_parser("token", help="ERC20 Token 转账")
    token.add_argument("--token",  required=True,             help="Token 合约地址")
    token.add_argument("--to",     required=True,             help="接收方地址")
    token.add_argument("--amount", required=True, type=float, help="转账金额")
    token.add_argument("--mev",    action="store_true",       help="开启 MEV 保护")

    args = parser.parse_args()
    bt   = BroadcastTransaction(chain_index=args.chain)

    try:
        if args.command == "native":
            result = bt.transfer_native(
                to_address=args.to,
                amount=args.amount,
                enable_mev_protection=args.mev,
            )
        else:
            result = bt.transfer_token(
                token_address=args.token,
                to_address=args.to,
                amount=args.amount,
                enable_mev_protection=args.mev,
            )
        print(result.summary())
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"❌ 错误: {e}")