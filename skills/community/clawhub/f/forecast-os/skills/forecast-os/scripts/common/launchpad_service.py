"""Launchpad service shaped after precog-tracker `MarketService`.

Holds the provider, the funder account, and the domain actions. Tracker
methods copied verbatim where noted: `build_signature_typed_data`, `to_wei`,
`from_wei`. Fee style follows tracker `_send_investor_claim` (legacy gasPrice,
+20% on Arbitrum). Receipt parsing follows `_parse_collateral_transfer`.
"""
import json
import logging
import os
import urllib.request
from decimal import Decimal

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore

DEFAULT_API = "https://service.precog.markets/api/v1"


class LaunchpadService:
    precog_creator = '0x5D45B7d8e517eF6b7085175ed395D9c8562b952f'  # Address that has market funds
    precog_master_map = {
        # (chain_id, precog_master_address)
        8453: '0x00000000000c109080dfa976923384b97165a57a',    # PrecogMasterV8
        84532: '0x61ec71F1Fd37ecc20d695E83F3D68e82bEfe8443',   # PrecogMasterV8
        42161: '0x0000000000990400E12543B7f400136e8672E2F0',   # PrecogMasterV8
    }
    transfer_topic = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'  # ERC20 Transfer event
    fund_tolerance = 0.00001

    # Internal services
    web3_service = None

    def __init__(self, name='launchpad'):
        # Initialize service logger
        self.log = logging.getLogger(name)
        self.web3_service = None

    def initialize_web3_provider(self, network, private_key, rpc_arg=None):
        # NOTE web3 imports stay local so keyless previews run on stdlib only
        from common.web3_service import Web3Service
        self.web3_service = Web3Service()

        # Get provider based on received network and load the funder account
        provider_url = self.resolve_rpc(int(network), rpc_arg)
        self.web3_service.init(provider_url=provider_url, timeout=30)
        self.web3_service.set_default_account(private_key)

        # Web3 provider was initialized successfully
        return True

    def validate_signature(self, chain_id, address, signature, action):
        # Only for debug
        # self.log.debug('Validating signature', address=address, signature=signature)
        from common.signature_verifier import SignatureVerifier

        # Get next nonce from the received address
        next_nonce = self.web3_service.get_next_pending_nonce(address)

        # Build typed-data authorization and verify the received signature
        action_typed_data = self.build_signature_typed_data(chain_id, address, next_nonce, action)
        signature_verifier = SignatureVerifier(self.web3_service.web3)
        return signature_verifier.is_valid_eip_712_signature(address, action_typed_data, signature)

    def sign_action(self, chain_id, address, action):
        """Sign a PrecogMarketAuthorization and pre-verify it recovers to address."""
        from common.signature_verifier import SignatureVerifier
        from common.web3_service import Web3Service as W3
        from eth_account import Account

        # Get next pending nonce for the signing address
        nonce = self.web3_service.get_next_pending_nonce(address)

        # Build typed-data authorization and sign it with the funder key
        typed_data = self.build_signature_typed_data(chain_id, address, nonce, action)
        encoded = W3.encode_eip_712_message(typed_data)
        signature = Account.sign_message(encoded, self.web3_service.default_account.key).signature.hex()
        signature = '0x' + signature.replace('0x', '')

        # Check that the signature recovers to the expected address
        recovered = SignatureVerifier.recover_eip_712_signer(typed_data, signature)
        if recovered.lower() != address.lower():
            raise RuntimeError('Signature signer mismatch')

        # Signature successfully verified
        return signature

    @staticmethod
    def build_signature_typed_data(chain_id, address, nonce, action):
        chain_id = int(chain_id)
        precog_master = LaunchpadService.precog_master_map.get(chain_id)
        if not precog_master:
            raise RuntimeError('Invalid market chain (PrecogMaster not found)')

        # Build EIP-712 typed-data structure
        result = {
            'types': {},
            'primaryType': 'PrecogMarketAuthorization',
        }
        result['types']['EIP712Domain'] = [
            {'name': 'name', 'type': 'string'},
            {'name': 'version', 'type': 'string'},
            {'name': 'chainId', 'type': 'uint256'},
            {'name': 'verifyingContract', 'type': 'address'},
        ]
        result['types']['PrecogMarketAuthorization'] = [
            {'name': 'action', 'type': 'string'},
            {'name': 'account', 'type': 'address'},
            {'name': 'chainId', 'type': 'uint256'},
            {'name': 'nonce', 'type': 'uint256'},
        ]

        # Add domain metadata for the Precog master contract
        result['domain'] = {
            'name': 'Precog Markets',
            'version': '1',
            'chainId': chain_id,
            'verifyingContract': precog_master,
        }

        # Add authorization message data
        result['message'] = {
            'action': action,
            'account': address,
            'chainId': chain_id,
            'nonce': int(nonce),
        }

        return result

    def transfer_collateral(self, token_address, human_amount, to=None, dry_run=False):
        """Transfer funding collateral with balance pre-checks. dry_run reports without sending."""
        # Only for debug
        # self.log.debug('Funding upcoming market', token=token_address, amount=human_amount)
        to = to or self.precog_creator
        address = self.web3_service.default_account.address

        # Load the market collateral contract and convert the human amount to wei
        token = self.web3_service.get_erc_20_contract(token_address)
        decimals = token.functions.decimals().call()
        amount_wei = self.to_wei(human_amount, decimals)
        if amount_wei <= 0:
            raise RuntimeError(f'Amount {human_amount} converts to 0 wei.')

        # Check that the funder holds enough collateral
        balance = self.web3_service.get_token_balance(address, token_address)
        if balance < amount_wei:
            raise RuntimeError(f'Insufficient collateral: balance {balance} wei < needed {amount_wei} wei.')

        # Estimate gas and price the fee (legacy gasPrice, same as tracker `_send_investor_claim`)
        chain_id = int(self.web3_service.web3.eth.chain_id)
        gas_estimate = self.web3_service.estimate_gas(
            {'from': address, 'to': token_address,
             'data': token.functions.transfer(
                 self.web3_service.to_checksum_address(to), amount_wei)._encode_transaction_data()})
        gas_price = int(self.web3_service.web3.eth.gas_price)

        # Add extra 20% gas price only on Arbitrum due to being a fast chain
        if chain_id == 42161:
            gas_price = int(gas_price * 1.2)
        est_fee = gas_estimate * gas_price

        # Check that the funder holds enough native token for gas
        native = self.web3_service.get_account_balance(address)
        if native < est_fee:
            raise RuntimeError(f'Insufficient native token for gas: balance {native} wei < ~{est_fee} wei.')

        # Build and return the pre-flight report
        result = {'decimals': decimals, 'amount_wei': amount_wei,
                  'collateral_balance_wei': balance, 'native_balance_wei': native,
                  'gas_estimate': gas_estimate, 'est_fee_wei': est_fee}
        if dry_run:
            return result

        # Build, sign, and send the collateral transfer
        transfer_tx = token.functions.transfer(
            self.web3_service.to_checksum_address(to), amount_wei).build_transaction({
                'from': address,
                'nonce': self.web3_service.get_next_pending_nonce(),
                'gasPrice': gas_price,
                'gas': gas_estimate,
                'chainId': chain_id,
            })
        tx_hash = self.web3_service.send_tx(transfer_tx)
        result['tx_hash'] = tx_hash
        return result

    def validate_fund_receipt(self, tx_hash, funder_address, token_address, human_amount, decimals):
        """Hard validation of a funding transfer receipt. Returns (ok, reason)."""
        # Only for debug
        # self.log.debug('Validating funding tx', tx_hash=tx_hash)
        try:
            receipt = self.web3_service.wait_for_transaction_receipt(tx_hash, block_confirmations=1)
        except Exception as e:
            return False, f'receipt not available: {e}'

        # Check that tx did not revert
        if receipt.status != 1:
            return False, f'tx reverted (status {receipt.status}).'

        # Walk the receipt logs looking for the collateral Transfer to the precog creator
        total = 0
        for log in receipt.logs:
            # Skip logs from other token contracts
            if str(log.address).lower() != str(token_address).lower():
                continue
            topics = log.topics

            # Skip not `transfer` topic action
            if not topics or topics[0].hex().lower() != self.transfer_topic:
                continue

            # Parse sender and receiver of the collateral transfer
            sender = '0x' + topics[1].hex()[-40:]
            receiver = '0x' + topics[2].hex()[-40:]

            # Skip transfers to anyone but the precog creator
            if receiver.lower() != self.precog_creator.lower():
                continue

            # Check that the transfer came from the funder account
            if sender.lower() != funder_address.lower():
                return False, f'log sender {sender} != funder {funder_address}.'

            # All validation passed, sum the matching inbound transfer (multi-transfer txs)
            total += self.web3_service.to_int(log.data.hex())

        # Check that the transferred amount matches the expected funding amount
        transferred = float(self.from_wei(total, int(decimals)))
        if abs(transferred - float(human_amount)) >= self.fund_tolerance:
            return False, (f'amount mismatch: receipt shows {transferred} '
                           f'vs expected {human_amount} (token {token_address}).')
        return True, ''

    @staticmethod
    def from_wei(amount, decimals):
        # Note: this function returns a `Decimal`
        return Decimal(amount) / (Decimal(10) ** decimals)

    @staticmethod
    def to_wei(amount, decimals):
        # Note: this function returns an `int`
        return int(Decimal(str(amount)) * (Decimal(10) ** decimals))

    @staticmethod
    def load_key(key_file=None, config=None):
        """Resolve the Precog private key like the forecast CLI. Returns (key, address)."""
        from eth_account import Account
        key = None

        # Case: explicit key file
        if key_file:
            with open(os.path.expanduser(key_file)) as f:
                key = f.read().strip()

        # Case: environment variable
        if not key:
            key = (os.environ.get("PRECOG_PRIVATE_KEY") or "").strip()

        # Case: forecast config file ([precog] private_key_file / private_key)
        if not key:
            cfg_path = config or os.environ.get("FORECAST_CONFIG") or "./forecast_config.toml"
            precog = LaunchpadService.load_config(cfg_path).get("precog", {})
            kf = precog.get("private_key_file")
            if kf and os.path.exists(os.path.expanduser(kf)):
                with open(os.path.expanduser(kf)) as f:
                    key = f.read().strip()
            elif precog.get("private_key"):
                key = str(precog["private_key"]).strip()

        # Check that a key was found somewhere
        if not key:
            raise RuntimeError("Precog private key not found "
                               "(use --key-file, PRECOG_PRIVATE_KEY, or forecast_config.toml [precog]).")
        if not key.startswith("0x"):
            key = "0x" + key
        return key, Account.from_key(key).address

    @staticmethod
    def resolve_rpc(chain, rpc_arg=None, config=None):
        # Case: explicit RPC url
        if rpc_arg:
            return rpc_arg
        chain = int(chain)

        # Case: environment variable per chain family
        env_var = "BASE_RPC" if chain in (8453, 84532) else "ARBITRUM_RPC"
        rpc = (os.environ.get(env_var) or "").strip()

        # Case: forecast config file ([precog] base_rpc / arbitrum_rpc)
        if not rpc:
            cfg_path = config or os.environ.get("FORECAST_CONFIG") or "./forecast_config.toml"
            precog = LaunchpadService.load_config(cfg_path).get("precog", {})
            cfg_key = "base_rpc" if chain in (8453, 84532) else "arbitrum_rpc"
            rpc = str(precog.get(cfg_key) or "").strip()

        # Check that an RPC url was found somewhere
        if not rpc:
            raise RuntimeError(f"no RPC for chain {chain}: pass --rpc, set {env_var}, "
                               "or add [precog] base_rpc/arbitrum_rpc to forecast_config.toml.")
        return rpc

    @staticmethod
    def load_config(config_path):
        if not config_path or not os.path.exists(config_path):
            return {}
        with open(config_path, "rb") as f:
            return tomllib.load(f)

    @staticmethod
    def api_get(base, endpoint, params=""):
        # Forward the GET request to the backend and parse the JSON body
        with urllib.request.urlopen(f"{base.rstrip('/')}/{endpoint}/?{params}", timeout=30) as r:
            return json.load(r)

    @staticmethod
    def api_post(base, endpoint, payload):
        # Forward the POST request to the backend and parse the JSON body
        req = urllib.request.Request(f"{base.rstrip('/')}/{endpoint}/",
                                     data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)

    @classmethod
    def get_market(cls, base, market_id):
        # Get backend response for the received market id
        rows = cls.list_markets(base, {"id": market_id})

        # Check that a market was found
        if not rows:
            raise RuntimeError(f"market {market_id} not found on {base}.")
        return rows[0]

    @classmethod
    def list_markets(cls, base, params=None):
        # Build the querystring, repeating multi-value params like status.
        query = cls.build_query(params or {})

        # Get backend response for the upcoming-markets list.
        m = cls.api_get(base, "upcoming-markets", query)

        # Case: backend returned a paginated dict.
        rows = (m.get("results") or []) if isinstance(m, dict) else (m or [])
        return rows

    @staticmethod
    def build_query(params):
        # Encode each param, repeating list values as separate pairs.
        # The tracker reads status as a multiple-choice filter.
        from urllib.parse import urlencode
        pairs = []
        for key, value in params.items():
            if value is None:
                continue
            if isinstance(value, (list, tuple)):
                for item in value:
                    pairs.append((key, item))
            else:
                pairs.append((key, value))
        return urlencode(pairs)

    @staticmethod
    def is_fundable(row):
        # A row is fundable when validators opened it and cap room is left.
        # Returns an (ok, reason) pair for display.
        status = (row.get("status") or "").upper()
        if status == "VALIDATED":
            return True, ""
        if status == "FUNDED":
            funded = row.get("collateral_funding") or 0
            max_funding = row.get("max_funding_amount")
            if max_funding is None:
                return True, ""
            if float(funded) < float(max_funding):
                return True, ""
            return False, "FULL"
        if not status:
            return False, "UNKNOWN"
        return False, status

    @staticmethod
    def funding_room(row):
        # Room left under the max funding cap, None when the cap is unknown.
        funded = row.get("collateral_funding") or 0
        max_funding = row.get("max_funding_amount")
        if max_funding is None:
            return None
        return float(max_funding) - float(funded)

    @staticmethod
    def parse_end(row):
        # Read the market end as an aware UTC datetime, None when unknown.
        # Prefers end_at ISO text, falls back to end_timestamp unix seconds.
        from datetime import datetime, timezone
        end_at = row.get("end_at")
        if isinstance(end_at, str) and end_at.strip():
            try:
                parsed = datetime.fromisoformat(end_at.strip().replace("Z", "+00:00"))
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=timezone.utc)
                return parsed
            except ValueError:
                pass
        end_ts = row.get("end_timestamp")
        if isinstance(end_ts, bool):
            return None
        if isinstance(end_ts, (int, float)) and end_ts > 0:
            return datetime.fromtimestamp(end_ts, tz=timezone.utc)
        return None

    @staticmethod
    def has_ended(row, now=None):
        # A market has ended when its end datetime is in the past.
        # Unknown ends never count as ended.
        from datetime import datetime, timezone
        end = LaunchpadService.parse_end(row)
        if end is None:
            return False
        now = now or datetime.now(timezone.utc)
        return end <= now
