"""Flap.sh VaultPortal token launcher — the core launch mechanism."""

import json
import os
import time

import requests
from eth_account import Account
from web3 import Web3

from ..config import OpenClawConfig
from ..utils.logger import log
from .constants import (
    AGENT_SHARE_BPS,
    ANTI_FARMER_DURATION,
    CONTRACTS,
    D9_BASE_URL,
    DISTRICT9_SHARE_BPS,
    DISTRICT9_TREASURY,
    FLAP_UPLOAD_API,
    FORCED_TAX_RATE,
    MIN_SHARE_BALANCE,
    TAX_DURATION,
    TAX_TOKEN_SUFFIX,
)

# VaultPortal ABI — newTaxTokenWithVault (Split Vault for 50/50 tax split)
VAULT_PORTAL_ABI = [
    {
        "inputs": [
            {
                "components": [
                    {"name": "name", "type": "string"},
                    {"name": "symbol", "type": "string"},
                    {"name": "meta", "type": "string"},
                    {"name": "dexThresh", "type": "uint8"},
                    {"name": "salt", "type": "bytes32"},
                    {"name": "taxRate", "type": "uint16"},
                    {"name": "migratorType", "type": "uint8"},
                    {"name": "quoteToken", "type": "address"},
                    {"name": "quoteAmt", "type": "uint256"},
                    {"name": "permitData", "type": "bytes"},
                    {"name": "extensionID", "type": "bytes32"},
                    {"name": "extensionData", "type": "bytes"},
                    {"name": "dexId", "type": "uint8"},
                    {"name": "lpFeeProfile", "type": "uint8"},
                    {"name": "taxDuration", "type": "uint64"},
                    {"name": "antiFarmerDuration", "type": "uint64"},
                    {"name": "mktBps", "type": "uint16"},
                    {"name": "deflationBps", "type": "uint16"},
                    {"name": "dividendBps", "type": "uint16"},
                    {"name": "lpBps", "type": "uint16"},
                    {"name": "minimumShareBalance", "type": "uint256"},
                    {"name": "vaultFactory", "type": "address"},
                    {"name": "vaultData", "type": "bytes"},
                ],
                "name": "params",
                "type": "tuple",
            }
        ],
        "name": "newTaxTokenWithVault",
        "outputs": [{"name": "token", "type": "address"}],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "name": "ts", "type": "uint256"},
            {"indexed": False, "name": "creator", "type": "address"},
            {"indexed": False, "name": "nonce", "type": "uint256"},
            {"indexed": False, "name": "token", "type": "address"},
            {"indexed": False, "name": "name", "type": "string"},
            {"indexed": False, "name": "symbol", "type": "string"},
            {"indexed": False, "name": "meta", "type": "string"},
        ],
        "name": "TokenCreated",
        "type": "event",
    },
]


def _encode_split_vault_data(recipients: list[tuple[str, int]]) -> bytes:
    """
    ABI-encode Split Vault recipients.

    Args:
        recipients: List of (address, bps) tuples. bps must sum to 10000.

    Returns:
        ABI-encoded bytes for vaultData parameter.
    """
    # Recipient[] is a dynamic array of (address, uint16) tuples
    # ABI layout: offset to array → length → (addr, bps) per recipient
    from eth_abi import encode

    addresses = [Web3.to_checksum_address(addr) for addr, _ in recipients]
    bps_values = [bps for _, bps in recipients]

    total_bps = sum(bps_values)
    if total_bps != 10000:
        raise ValueError(f"Split vault bps must sum to 10000, got {total_bps}")

    # Encode as array of (address, uint16) tuples
    return encode(["(address,uint16)[]"], [list(zip(addresses, bps_values))])


class FlapLauncher:
    """Launch tokens through Flap.sh VaultPortal with enforced DISTRICT9 tax split."""

    def __init__(self, config: OpenClawConfig):
        self.config = config
        self.account = Account.from_key(config.wallet.private_key)

        # Select chain config
        chain_key = config.chain
        if config.testnet:
            chain_key += "_testnet"
        self.chain = CONTRACTS.get(chain_key)
        if not self.chain:
            raise ValueError(f"Unsupported chain: {chain_key}")

        self.w3 = Web3(Web3.HTTPProvider(self.chain["rpc"]))
        if not self.w3.is_connected():
            raise ConnectionError(f"Cannot connect to {self.chain['rpc']}")

    def launch(self, metadata: dict, image_path: str = "") -> dict:
        """
        Launch a token through Flap VaultPortal with Split Vault.

        Tax split: 0.5% DISTRICT9 + 0.5% Agent wallet (hardcoded).
        Flow: Find salt → Set website URL → Upload IPFS → Deploy on-chain.
        """
        # Step 1: Find CREATE2 salt (vanity address ending in 7777)
        # VaultPortal delegates token creation to Portal, so CREATE2 deployer is Portal
        token_impl = self.chain["tax_token_v1_impl"]
        portal_addr = self.chain["portal"]
        salt, predicted_addr = self._find_salt(token_impl, portal_addr)

        # Step 2: Inject token detail page URL, then upload metadata to IPFS
        # /token/{token_addr} for token detail, /agent/{wallet_addr} for agent profile
        metadata["website"] = f"{D9_BASE_URL}/token/{predicted_addr}"
        cid = self._upload_to_ipfs(metadata, image_path)

        # Step 3: Build and send transaction
        quote_amt = self.w3.to_wei(float(self.config.launch.initial_buy), "ether")
        result = self._send_launch_tx(metadata, cid, salt, quote_amt)

        # Add convenience URLs
        explorer = self.chain["explorer"]
        token_addr = result["contract_address"]
        result.update({
            "predicted_address": predicted_addr,
            "ipfs_cid": cid,
            "explorer_tx": f"{explorer}/tx/{result['tx_hash']}",
            "explorer_token": f"{explorer}/token/{token_addr}",
            "flap_url": f"https://flap.sh/bnb/{token_addr}",
            "d9_token_url": f"{D9_BASE_URL}/token/{token_addr}",
            "d9_agent_url": f"{D9_BASE_URL}/agent/{self.account.address}",
        })

        return result

    def _upload_to_ipfs(self, metadata: dict, image_path: str = "") -> str:
        """Upload token metadata to Flap's IPFS via GraphQL mutation."""
        mutation = """
        mutation Create($file: Upload!, $meta: MetadataInput!) {
          create(file: $file, meta: $meta)
        }
        """

        meta = {
            "website": metadata.get("website", ""),
            "twitter": metadata.get("twitter") or None,
            "telegram": metadata.get("telegram") or None,
            "description": metadata.get("description", ""),
            "creator": "0x0000000000000000000000000000000000000000",
        }

        operations = json.dumps({
            "query": mutation,
            "variables": {"file": None, "meta": meta},
        })
        mapping = json.dumps({"0": ["variables.file"]})

        # Load image
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as f:
                image_data = f.read()
            filename = os.path.basename(image_path)
        else:
            # Minimal 1x1 PNG placeholder
            import base64
            png_b64 = (
                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4"
                "2mP8/58BAwAI/AL+hc2rNAAAAABJRU5ErkJggg=="
            )
            image_data = base64.b64decode(png_b64)
            filename = "logo.png"

        files = {
            "operations": (None, operations, "application/json"),
            "map": (None, mapping, "application/json"),
            "0": (filename, image_data, "image/png"),
        }

        log.info("Uploading metadata to IPFS...")
        resp = requests.post(FLAP_UPLOAD_API, files=files, timeout=30)

        if resp.status_code != 200:
            raise RuntimeError(f"IPFS upload failed: {resp.status_code} {resp.text}")

        data = resp.json()
        if "errors" in data:
            raise RuntimeError(f"GraphQL errors: {data['errors']}")

        cid = data["data"]["create"]
        log.info(f"Metadata uploaded: {cid}")
        return cid

    def _find_salt(self, token_impl: str, portal: str) -> tuple[bytes, str]:
        """Find CREATE2 salt for vanity address (7777 suffix)."""
        impl_hex = token_impl[2:].lower()

        # EIP-1167 minimal proxy bytecode
        bytecode_hex = (
            "3d602d80600a3d3981f3"
            "363d3d373d3d3d363d73"
            + impl_hex
            + "5af43d82803e903d91602b57fd5bf3"
        )
        bytecode = bytes.fromhex(bytecode_hex)
        bytecode_hash = Web3.keccak(bytecode)
        portal_bytes = bytes.fromhex(portal[2:].lower())

        log.info("Finding CREATE2 salt (7777 suffix)...")
        seed = Account.create().key
        salt = Web3.keccak(seed)
        iterations = 0
        start = time.time()

        while True:
            data = b"\xff" + portal_bytes + salt + bytecode_hash
            addr_hash = Web3.keccak(data)
            addr = Web3.to_checksum_address(addr_hash[-20:].hex())

            if addr.lower().endswith(TAX_TOKEN_SUFFIX.lower()):
                elapsed = time.time() - start
                log.info(f"Salt found in {iterations} iterations ({elapsed:.1f}s): {addr}")
                return salt, addr

            salt = Web3.keccak(salt)
            iterations += 1

    def _send_launch_tx(self, metadata: dict, cid: str, salt: bytes, quote_amt: int) -> dict:
        """Build, sign, and send the newTaxTokenWithVault transaction."""
        vault_portal_addr = self.chain["vault_portal"]
        vault_portal = self.w3.eth.contract(
            address=Web3.to_checksum_address(vault_portal_addr),
            abi=VAULT_PORTAL_ABI,
        )

        # Encode Split Vault data — DISTRICT9 + Agent wallet, 50/50 split
        split_factory = self.chain["split_vault_factory"]
        vault_data = _encode_split_vault_data([
            (DISTRICT9_TREASURY, DISTRICT9_SHARE_BPS),  # 50% → DISTRICT9
            (self.account.address, AGENT_SHARE_BPS),     # 50% → Agent
        ])

        log.info(f"Split Vault: {DISTRICT9_SHARE_BPS}bps DISTRICT9 + {AGENT_SHARE_BPS}bps Agent")

        # Build params tuple
        params = (
            metadata["name"],                                              # name
            metadata["symbol"],                                            # symbol
            cid,                                                           # meta
            1,                                                             # dexThresh
            salt,                                                          # salt
            FORCED_TAX_RATE,                                               # taxRate (1%)
            1,                                                             # migratorType
            "0x0000000000000000000000000000000000000000",                   # quoteToken (native)
            quote_amt,                                                     # quoteAmt
            b"",                                                           # permitData
            b"\x00" * 32,                                                  # extensionID
            b"",                                                           # extensionData
            0,                                                             # dexId
            0,                                                             # lpFeeProfile
            TAX_DURATION,                                                  # taxDuration (~100 years)
            ANTI_FARMER_DURATION,                                          # antiFarmerDuration (3 days)
            10000,                                                         # mktBps (100% to vault)
            0,                                                             # deflationBps
            0,                                                             # dividendBps
            0,                                                             # lpBps
            MIN_SHARE_BALANCE,                                             # minimumShareBalance
            Web3.to_checksum_address(split_factory),                       # vaultFactory
            vault_data,                                                    # vaultData
        )

        wallet = self.account.address
        nonce = self.w3.eth.get_transaction_count(wallet)
        balance = self.w3.eth.get_balance(wallet)

        log.info(f"Wallet: {wallet}")
        log.info(f"Balance: {self.w3.from_wei(balance, 'ether')} BNB")

        if balance < quote_amt:
            raise ValueError(
                f"Insufficient balance: {self.w3.from_wei(balance, 'ether')} BNB, "
                f"need {self.w3.from_wei(quote_amt, 'ether')} BNB + gas"
            )

        # Estimate gas
        try:
            gas_est = vault_portal.functions.newTaxTokenWithVault(params).estimate_gas({
                "from": wallet,
                "value": quote_amt,
            })
            gas_limit = int(gas_est * 1.3)
        except Exception as e:
            log.warning(f"Gas estimation failed ({e}), using fallback")
            gas_limit = 3_000_000

        tx = vault_portal.functions.newTaxTokenWithVault(params).build_transaction({
            "from": wallet,
            "value": quote_amt,
            "gas": gas_limit,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": nonce,
            "chainId": self.w3.eth.chain_id,
        })

        log.info("Signing and sending transaction...")
        signed = self.w3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        log.info(f"TX sent: {tx_hash.hex()}")

        log.info("Waiting for confirmation...")
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

        if receipt["status"] != 1:
            raise RuntimeError(f"Transaction reverted! TX: {tx_hash.hex()}")

        log.info(f"Confirmed in block {receipt['blockNumber']} (gas: {receipt['gasUsed']})")

        # Parse TokenCreated event (emitted by Portal, not VaultPortal)
        portal_addr = self.chain["portal"]
        portal_contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(portal_addr),
            abi=VAULT_PORTAL_ABI,  # shares same event ABI
        )
        token_address = None
        try:
            logs = portal_contract.events.TokenCreated().process_receipt(receipt)
            if logs:
                token_address = logs[0]["args"]["token"]
        except Exception:
            pass

        if not token_address:
            token_address = "unknown"
            log.warning("Could not parse token address from event logs")

        return {
            "contract_address": token_address,
            "tx_hash": tx_hash.hex(),
            "block_number": receipt["blockNumber"],
            "gas_used": receipt["gasUsed"],
        }
