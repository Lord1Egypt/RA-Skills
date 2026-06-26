"""
DEX Swap Engine — Direct Uniswap V3 swaps on Base
Zero middleman. Our fee: 0.3% (vs Bankr's 0.65%)
Supports: exact input swaps, slippage protection, gas estimation
"""

import json
import sys
import time
from decimal import Decimal
from web3 import Web3
from eth_abi import encode
from eth_abi.packed import encode_packed

from config import (
    CHAIN_ID, TOKENS, UNISWAP,
    DEFAULT_SLIPPAGE_BPS, MAX_SLIPPAGE_BPS, GAS_LIMIT
)
from wallet import load_wallet
from rpc import get_w3

# ABIs
ERC20_ABI = [
    {"constant": True, "inputs": [{"name": "account", "type": "address"}], "name": "balanceOf",
     "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "decimals",
     "outputs": [{"name": "", "type": "uint8"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "symbol",
     "outputs": [{"name": "", "type": "string"}], "type": "function"},
    {"constant": False, "inputs": [{"name": "spender", "type": "address"}, {"name": "amount", "type": "uint256"}],
     "name": "approve", "outputs": [{"name": "", "type": "bool"}], "type": "function"},
    {"constant": True, "inputs": [{"name": "owner", "type": "address"}, {"name": "spender", "type": "address"}],
     "name": "allowance", "outputs": [{"name": "", "type": "uint256"}], "type": "function"},
]

SWAP_ROUTER_ABI = [
    {
        "inputs": [{
            "components": [
                {"name": "tokenIn", "type": "address"},
                {"name": "tokenOut", "type": "address"},
                {"name": "fee", "type": "uint24"},
                {"name": "recipient", "type": "address"},
                {"name": "amountIn", "type": "uint256"},
                {"name": "amountOutMinimum", "type": "uint256"},
                {"name": "sqrtPriceLimitX96", "type": "uint160"},
            ],
            "name": "params",
            "type": "tuple"
        }],
        "name": "exactInputSingle",
        "outputs": [{"name": "amountOut", "type": "uint256"}],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [{
            "components": [
                {"name": "path", "type": "bytes"},
                {"name": "recipient", "type": "address"},
                {"name": "amountIn", "type": "uint256"},
                {"name": "amountOutMinimum", "type": "uint256"},
            ],
            "name": "params",
            "type": "tuple"
        }],
        "name": "exactInput",
        "outputs": [{"name": "amountOut", "type": "uint256"}],
        "stateMutability": "payable",
        "type": "function"
    },
]

QUOTER_ABI = [
    {
        "inputs": [{
            "components": [
                {"name": "tokenIn", "type": "address"},
                {"name": "tokenOut", "type": "address"},
                {"name": "amountIn", "type": "uint256"},
                {"name": "fee", "type": "uint24"},
                {"name": "sqrtPriceLimitX96", "type": "uint160"},
            ],
            "name": "params",
            "type": "tuple"
        }],
        "name": "quoteExactInputSingle",
        "outputs": [
            {"name": "amountOut", "type": "uint256"},
            {"name": "sqrtPriceX96After", "type": "uint160"},
            {"name": "initializedTicksCrossed", "type": "uint32"},
            {"name": "gasEstimate", "type": "uint256"},
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
]


class DexSwapper:
    def __init__(self):
        self.w3 = get_w3()

        self.address, self.private_key = load_wallet()
        if not self.address:
            raise ValueError("No wallet configured. Run: python3 wallet.py generate")

        self.router = self.w3.eth.contract(
            address=Web3.to_checksum_address(UNISWAP["swap_router_02"]),
            abi=SWAP_ROUTER_ABI
        )
        self.quoter = self.w3.eth.contract(
            address=Web3.to_checksum_address(UNISWAP["quoter_v2"]),
            abi=QUOTER_ABI
        )

    def get_token_info(self, token_address):
        """Get token symbol and decimals."""
        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=ERC20_ABI
        )
        return {
            "symbol": contract.functions.symbol().call(),
            "decimals": contract.functions.decimals().call(),
            "contract": contract
        }

    def get_quote(self, token_in, token_out, amount_in, fee=3000):
        """Get a swap quote without executing."""
        try:
            result = self.quoter.functions.quoteExactInputSingle({
                "tokenIn": Web3.to_checksum_address(token_in),
                "tokenOut": Web3.to_checksum_address(token_out),
                "amountIn": amount_in,
                "fee": fee,
                "sqrtPriceLimitX96": 0,
            }).call()
            return result[0]  # amountOut
        except Exception as e:
            print(f"❌ Quote failed: {e}")
            return None

    def ensure_approval(self, token_address, amount):
        """Approve the router to spend tokens if needed."""
        token = self.w3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=ERC20_ABI
        )
        router_addr = Web3.to_checksum_address(UNISWAP["swap_router_02"])
        current_allowance = token.functions.allowance(self.address, router_addr).call()

        if current_allowance >= amount:
            return True

        print(f"   📝 Approving router to spend tokens...")
        max_approval = 2**256 - 1  # Max approval
        tx = token.functions.approve(router_addr, max_approval).build_transaction({
            "from": self.address,
            "chainId": CHAIN_ID,
            "gas": 100_000,
            "nonce": self.w3.eth.get_transaction_count(self.address),
            "maxFeePerGas": self.w3.eth.gas_price * 2,
            "maxPriorityFeePerGas": self.w3.to_wei(0.001, "gwei"),
        })

        signed = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)

        if receipt.status == 1:
            print(f"   ✅ Approved! Tx: {tx_hash.hex()}")
            return True
        else:
            print(f"   ❌ Approval failed!")
            return False

    def swap(self, token_in, token_out, amount_human, slippage_bps=DEFAULT_SLIPPAGE_BPS, fee=3000):
        """
        Execute a swap on Uniswap V3.

        Args:
            token_in: Input token address or symbol (e.g., "USDC")
            token_out: Output token address or symbol (e.g., "WETH")
            amount_human: Amount in human-readable format (e.g., 5.0 for 5 USDC)
            slippage_bps: Slippage tolerance in basis points (100 = 1%)
            fee: Pool fee tier (500=0.05%, 3000=0.3%, 10000=1%)
        """
        # Resolve symbols to addresses
        if token_in.upper() in TOKENS:
            token_in = TOKENS[token_in.upper()]
        if token_out.upper() in TOKENS:
            token_out = TOKENS[token_out.upper()]

        # Get token info
        in_info = self.get_token_info(token_in)
        out_info = self.get_token_info(token_out)

        amount_raw = int(amount_human * (10 ** in_info["decimals"]))

        print(f"\n🔄 Swap: {amount_human} {in_info['symbol']} → {out_info['symbol']}")
        print(f"   Pool fee: {fee/10000:.2%} | Slippage: {slippage_bps/100:.1f}%")

        # Get quote
        quote = self.get_quote(token_in, token_out, amount_raw, fee)
        if not quote:
            return None

        out_human = quote / (10 ** out_info["decimals"])
        print(f"   Quote: ~{out_human:.6f} {out_info['symbol']}")

        # Apply slippage
        min_out = int(quote * (10000 - slippage_bps) / 10000)
        min_out_human = min_out / (10 ** out_info["decimals"])
        print(f"   Min out (with slippage): {min_out_human:.6f} {out_info['symbol']}")

        # Ensure approval
        if not self.ensure_approval(token_in, amount_raw):
            return None

        # Build swap transaction
        swap_params = {
            "tokenIn": Web3.to_checksum_address(token_in),
            "tokenOut": Web3.to_checksum_address(token_out),
            "fee": fee,
            "recipient": self.address,
            "amountIn": amount_raw,
            "amountOutMinimum": min_out,
            "sqrtPriceLimitX96": 0,
        }

        tx = self.router.functions.exactInputSingle(swap_params).build_transaction({
            "from": self.address,
            "chainId": CHAIN_ID,
            "gas": GAS_LIMIT,
            "value": 0,
            "nonce": self.w3.eth.get_transaction_count(self.address),
            "maxFeePerGas": self.w3.eth.gas_price * 2,
            "maxPriorityFeePerGas": self.w3.to_wei(0.001, "gwei"),
        })

        # Sign and send
        print(f"   ⛓️ Sending transaction...")
        signed = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        print(f"   📤 Tx: https://basescan.org/tx/{tx_hash.hex()}")

        # Wait for confirmation
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

        if receipt.status == 1:
            gas_used = receipt.gasUsed
            gas_cost = self.w3.from_wei(gas_used * receipt.effectiveGasPrice, "ether")
            print(f"   ✅ SWAP COMPLETE!")
            print(f"   Gas used: {gas_used} ({gas_cost:.6f} ETH)")
            return {
                "status": "success",
                "tx_hash": tx_hash.hex(),
                "amount_in": amount_human,
                "token_in": in_info["symbol"],
                "estimated_out": out_human,
                "token_out": out_info["symbol"],
                "gas_cost_eth": float(gas_cost),
            }
        else:
            print(f"   ❌ SWAP FAILED! Tx: {tx_hash.hex()}")
            return {"status": "failed", "tx_hash": tx_hash.hex()}

    def swap_eth_for_token(self, token_out, eth_amount, slippage_bps=DEFAULT_SLIPPAGE_BPS, fee=3000):
        """Swap native ETH for a token (wraps to WETH internally)."""
        if token_out.upper() in TOKENS:
            token_out = TOKENS[token_out.upper()]

        out_info = self.get_token_info(token_out)
        amount_raw = self.w3.to_wei(eth_amount, "ether")

        print(f"\n🔄 Swap: {eth_amount} ETH → {out_info['symbol']}")

        # Quote using WETH
        quote = self.get_quote(TOKENS["WETH"], token_out, amount_raw, fee)
        if not quote:
            return None

        out_human = quote / (10 ** out_info["decimals"])
        min_out = int(quote * (10000 - slippage_bps) / 10000)
        print(f"   Quote: ~{out_human:.6f} {out_info['symbol']}")

        swap_params = {
            "tokenIn": Web3.to_checksum_address(TOKENS["WETH"]),
            "tokenOut": Web3.to_checksum_address(token_out),
            "fee": fee,
            "recipient": self.address,
            "amountIn": amount_raw,
            "amountOutMinimum": min_out,
            "sqrtPriceLimitX96": 0,
        }

        tx = self.router.functions.exactInputSingle(swap_params).build_transaction({
            "from": self.address,
            "chainId": CHAIN_ID,
            "gas": GAS_LIMIT,
            "value": amount_raw,  # Send ETH with the transaction
            "nonce": self.w3.eth.get_transaction_count(self.address),
            "maxFeePerGas": self.w3.eth.gas_price * 2,
            "maxPriorityFeePerGas": self.w3.to_wei(0.001, "gwei"),
        })

        print(f"   ⛓️ Sending transaction...")
        signed = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        print(f"   📤 Tx: https://basescan.org/tx/{tx_hash.hex()}")

        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

        if receipt.status == 1:
            gas_cost = self.w3.from_wei(receipt.gasUsed * receipt.effectiveGasPrice, "ether")
            print(f"   ✅ SWAP COMPLETE! Gas: {gas_cost:.6f} ETH")
            return {"status": "success", "tx_hash": tx_hash.hex()}
        else:
            print(f"   ❌ SWAP FAILED!")
            return {"status": "failed", "tx_hash": tx_hash.hex()}


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 swap.py <token_in> <token_out> <amount> [slippage_bps] [fee_tier]")
        print("Example: python3 swap.py USDC WETH 5.0")
        print("Example: python3 swap.py ETH USDC 0.01")
        sys.exit(1)

    token_in = sys.argv[1]
    token_out = sys.argv[2]
    amount = float(sys.argv[3])
    slippage = int(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_SLIPPAGE_BPS
    fee = int(sys.argv[5]) if len(sys.argv) > 5 else 3000

    swapper = DexSwapper()

    if token_in.upper() == "ETH":
        swapper.swap_eth_for_token(token_out, amount, slippage, fee)
    else:
        swapper.swap(token_in, token_out, amount, slippage, fee)
