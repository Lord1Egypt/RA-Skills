"""Slim port of precog-tracker `common/web3_service.py`.

Only the surface the launchpad scripts need is carried over. Method names,
semantics, and static helpers are unchanged from the tracker so upstream fixes
port cleanly. Dropped: flashbots, multicall, oracle/market getters, tx history
caches, POA middleware handling differences (kept: geth_poa_middleware inject,
same as tracker `connect`).
"""
import json
from decimal import Decimal
from os import path
from time import sleep

from eth_account import Account
from web3 import Web3, HTTPProvider
try:
    # web3 v8 renamed WebsocketProvider to WebSocketProvider
    from web3 import WebSocketProvider as WebsocketProvider
except ImportError:
    from web3 import WebsocketProvider
try:
    # web3 v8 renamed geth_poa_middleware to ExtraDataToPOAMiddleware
    from web3.middleware import ExtraDataToPOAMiddleware as geth_poa_middleware
except ImportError:
    from web3.middleware import geth_poa_middleware


class Web3Service:
    # Class variables
    request_timeout = 30
    timeout = 120

    # Instance variables
    default_account = None
    provider_url = None
    provider = None
    web3 = None

    def __init__(self) -> None:
        self.default_account = None
        self.provider_url = None
        self.provider = None
        self.web3 = None

    def init(self, provider_url: str, default_private_key: str = None, timeout=None):
        if timeout:
            self.request_timeout = timeout
            self.timeout = timeout

        self.provider_url = provider_url
        self.set_provider(provider_url)
        self.connect()

        if default_private_key:
            self.set_default_account(default_private_key)

        return self

    def set_provider(self, provider_url):
        from urllib.parse import urlparse
        self.provider_url = provider_url
        url = urlparse(provider_url)

        # Case: HTTP provider
        if url.scheme in ['http', 'https']:
            self.provider = HTTPProvider(provider_url, {'timeout': self.request_timeout})
        # Case: WebSocket provider
        elif url.scheme in ['ws', 'wss']:
            self.provider = WebsocketProvider(provider_url, websocket_timeout=self.request_timeout)
        else:
            raise ValueError(f'Provider not supported: {provider_url}')

    def connect(self, provider=None):
        self.web3 = Web3(provider or self.provider)
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    def set_default_account(self, default_private_key):
        self.default_account = Account.from_key(default_private_key)

    def get_next_pending_nonce(self, address: str = None):
        address = address or self.default_account.address
        return self.web3.eth.get_transaction_count(address, 'pending')

    def get_token_balance(self, account_address, token_address):
        """
        Gets the balance of `address` in the ERC20 token deployed in `token_address`
        """
        if not (account_address and token_address):
            raise RuntimeError('Could not get pair contract')

        # Sanitize addresses
        account_address = self.web3.to_checksum_address(account_address)
        token_address = self.web3.to_checksum_address(token_address)

        # Get the ERC20 contract instance and fetch current balance
        erc20_token = self.get_erc_20_contract(token_address)
        return erc20_token.functions.balanceOf(account_address).call()

    def get_account_balance(self, address: str = None):
        address = address or self.default_account.address
        return self.web3.eth.get_balance(address)

    def wait_for_transaction_receipt(self, tx_hash, timeout=None, block_confirmations=1):
        if not timeout:
            timeout = self.timeout

        # Send receipt request to node
        from eth_typing import HexStr
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(
            transaction_hash=HexStr(tx_hash), timeout=timeout)

        # Wait until the receipt is confirmed based on block confirmations number
        while True:
            current_block = int(self.web3.eth.block_number)
            if current_block > tx_receipt.blockNumber + block_confirmations:
                break
            sleep(0.01)

        # Return requested transaction receipt
        return tx_receipt

    def send_tx(self, transaction):
        if 'chainId' not in transaction:
            transaction['chainId'] = self.web3.eth.chain_id
        # TODO Add support to EIP1559 txs (type 2)

        signed_tx = self.web3.eth.account.sign_transaction(transaction, self.default_account.key)
        # NOTE eth-account renamed rawTransaction to raw_transaction
        raw_tx = getattr(signed_tx, 'raw_transaction', None) or signed_tx.rawTransaction
        tx_hash = self.web3.eth.send_raw_transaction(raw_tx)
        tx_hash = tx_hash.hex() if tx_hash else None
        return tx_hash

    def estimate_gas(self, transaction):
        return self.web3.eth.estimate_gas(transaction, 'latest')

    def get_erc_20_contract(self, erc_20_address):
        return self.get_eth_contract_from_path(erc_20_address, 'IERC20.json')

    def get_eth_contract_from_path(self, contract_address, contract_abi_file_name):
        try:
            contract_abi_path = path.join(path.dirname(__file__), 'abis', contract_abi_file_name)
            with open(contract_abi_path, 'r', encoding='utf-8') as file:
                contract_abi = json.loads(file.read())
            return self.web3.eth.contract(address=contract_address, abi=contract_abi)
        except Exception as e:
            msg = f'Could not get contract in file={contract_abi_file_name} with address={contract_address}'
            raise RuntimeError(msg) from e

    @staticmethod
    def encode_eip_712_message(typed_data):
        try:
            from eth_account.messages import encode_typed_data
            return encode_typed_data(full_message=typed_data)
        except (ImportError, TypeError):
            from eth_account.messages import encode_structured_data
            return encode_structured_data(primitive=typed_data)

    @staticmethod
    def to_wei(amount, decimals):
        # Note: this function returns an `int`
        return int(Decimal(str(amount)) * (Decimal(10) ** decimals))

    @staticmethod
    def from_wei(amount, decimals):
        # Note: this function returns a `Decimal`
        return Decimal(amount) / (Decimal(10) ** decimals)

    @staticmethod
    def to_int(hex_value):
        return Web3.to_int(hexstr=hex_value)

    @staticmethod
    def to_checksum_address(value):
        return Web3.to_checksum_address(value)

    @staticmethod
    def is_address(value):
        return Web3.is_address(value)
