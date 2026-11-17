from web3 import Web3
from eth_account import Account


_ERC6492_DETECTION_SUFFIX = '6492649264926492649264926492649264926492649264926492649264926492'
_ERC1271_SUCCESS = '0x1626ba7e'

# DeploylessUniversalSigValidator.sol bytecode used for EIP-6492 off-chain validation.
# It simulates deploy/prepare + ERC1271 validation and returns 0x01/0x00.
# Full contract in packages/hardhat/contracts/DeploylessUniversalSigValidator.sol https://github.com/0xMarto/precog-core
_ERC6492_OFFCHAIN_VALIDATOR_BYTECODE = (
    '0x608060405234801561000f575f5ffd5b506040516106fb3803806106fb83398101604081905261002e91610559565b'
    '5f61003a848484610045565b9050805f526001601ff35b5f5f846001600160a01b0316803b8060200160405190810160'
    '40528181525f908060200190933c90507f64926492649264926492649264926492649264926492649264926492649264'
    '9261009884610470565b036101f9575f606080858060200190518101906100b591906105ae565b865192955090935091'
    '505f03610174575f836001600160a01b0316836040516100de919061060f565b5f604051808303815f865af19150503d'
    '805f8114610117576040519150601f19603f3d011682016040523d82523d5f602084013e61011c565b606091505b5050'
    '9050806101725760405162461bcd60e51b815260206004820152601e60248201527f5369676e617475726556616c6964'
    '61746f723a206465706c6f796d656e74000060448201526064015b60405180910390fd5b505b604051630b135d3f60e1'
    '1b808252906001600160a01b038a1690631626ba7e906101a4908b908690600401610625565b60206040518083038186'
    '5afa1580156101bf573d5f5f3e3d5ffd5b505050506040513d601f19601f820116820180604052508101906101e39190'
    '610661565b6001600160e01b03191614945050505050610469565b8051156102e3575f5f866001600160a01b03166316'
    '26ba7e60e01b8787604051602401610227929190610625565b60408051601f1981840301815291815260208201805160'
    '01600160e01b03166001600160e01b0319909416939093179092529051610265919061060f565b5f6040518083038185'
    '5afa9150503d805f811461029d576040519150601f19603f3d011682016040523d82523d5f602084013e6102a2565b60'
    '6091505b50915091508180156102b5575080516020145b156102e057630b135d3f60e11b6102cb82610688565b600160'
    '0160e01b031916149350505050610469565b50505b82516041146103475760405162461bcd60e51b8152602060048201'
    '52603a60248201525f5160206106db5f395f51905f5260448201527f3a20696e76616c6964207369676e617475726520'
    '6c656e6774680000000000006064820152608401610169565b61034f610487565b506020830151604080850151855186'
    '93925f918591908110610373576103736106c6565b016020015160f81c9050601b811480159061039257508060ff1660'
    '1c14155b156103f25760405162461bcd60e51b815260206004820152603b60248201525f5160206106db5f395f51905f'
    '5260448201527f3a20696e76616c6964207369676e617475726520762076616c75650000000000606482015260840161'
    '0169565b604080515f8152602081018083528a905260ff83169181019190915260608101849052608081018390526001'
    '600160a01b038a169060019060a0016020604051602081039080840390855afa15801561044d573d5f5f3e3d5ffd5b50'
    '5050602060405103516001600160a01b031614955050505050505b9392505050565b5f60208251101561047f575f5ffd'
    '5b508051015190565b60405180606001604052806003906020820280368337509192915050565b6001600160a01b0381'
    '1681146104b9575f5ffd5b50565b634e487b7160e01b5f52604160045260245ffd5b5f82601f8301126104df575f5ffd'
    '5b81516001600160401b038111156104f8576104f86104bc565b604051601f8201601f19908116603f01168101600160'
    '0160401b0381118282101715610526576105266104bc565b60405281815283820160200185101561053d575f5ffd5b81'
    '60208501602083015e5f918101602001919091529392505050565b5f5f5f6060848603121561056b575f5ffd5b835161'
    '0576816104a5565b6020850151604086015191945092506001600160401b03811115610598575f5ffd5b6105a4868287'
    '016104d0565b9150509250925092565b5f5f5f606084860312156105c0575f5ffd5b83516105cb816104a5565b602085'
    '01519093506001600160401b038111156105e6575f5ffd5b6105f2868287016104d0565b604086015190935090506001'
    '600160401b03811115610598575f5ffd5b5f82518060208501845e5f920191825250919050565b828152604060208201'
    '525f82518060408401528060208501606085015e5f606082850101526060601f19601f83011684010191505093925050'
    '50565b5f60208284031215610671575f5ffd5b81516001600160e01b031981168114610469575f5ffd5b805160208201'
    '516001600160e01b03198116919060048210156106bf576001600160e01b0319600483900360031b81901b8216169250'
    '5b5050919050565b634e487b7160e01b5f52603260045260245ffdfe5369676e617475726556616c696461746f722372'
    '65636f7665725369676e6572'
)


class SignatureVerifier:

    def __init__(self, web3):
        self.web3 = web3

    def is_valid_eip_712_signature(self, signer, typed_data, signature):
        # Check EOA signature
        is_signature_valid = self.is_valid_eoa_signature(signer, typed_data, signature)

        if is_signature_valid:
            return is_signature_valid
        else:
            message_hash = None

            # Check deployed smart wallet signature
            if self.has_contract_code(signer):
                message_hash = self.get_eip_712_message_hash(typed_data)
                is_signature_valid = self.is_valid_erc_1271_signature(signer, message_hash, signature)

            # Check counterfactual smart wallet signature
            if not is_signature_valid and self.is_erc_6492_signature(signature):
                if message_hash is None:
                    message_hash = self.get_eip_712_message_hash(typed_data)
                is_signature_valid = self.is_valid_erc_6492_signature(signer, message_hash, signature)

        return is_signature_valid

    def is_valid_eoa_signature(self, signer, typed_data, signature):
        is_signature_valid = False
        try:
            recovered_signer = self.recover_eip_712_signer(typed_data, signature)
            is_signature_valid = recovered_signer.lower() == signer.lower()
        except Exception:  # pylint: disable=broad-except
            is_signature_valid = False

        return is_signature_valid

    def is_valid_erc_6492_signature(self, signer, message_hash, signature):
        is_signature_valid = False
        signature_bytes = self.to_bytes(signature)
        call_data = _ERC6492_OFFCHAIN_VALIDATOR_BYTECODE + self.abi_encode_hex(
            ['address', 'bytes32', 'bytes'],
            [Web3.to_checksum_address(signer), message_hash, signature_bytes]
        )[2:]
        result = self.web3.eth.call({'data': call_data})
        result_hex = self.to_hex(result)
        if result_hex == '0x01':
            is_signature_valid = True
        elif result_hex == '0x00':
            is_signature_valid = False
        else:
            raise ValueError(f'Unexpected ERC-6492 validator result: {result_hex}')

        return is_signature_valid

    def is_valid_erc_1271_signature(self, signer, message_hash, signature):
        selector = Web3.keccak(text='isValidSignature(bytes32,bytes)')[:4]
        call_data = Web3.to_hex(selector) + self.abi_encode_hex(
            ['bytes32', 'bytes'],
            [message_hash, self.to_bytes(signature)]
        )[2:]
        result = self.web3.eth.call({
            'to': Web3.to_checksum_address(signer),
            'data': call_data
        })
        result_hex = self.to_hex(result).lower()
        is_signature_valid = result_hex.startswith(_ERC1271_SUCCESS)
        return is_signature_valid

    def has_contract_code(self, address):
        code = self.web3.eth.get_code(Web3.to_checksum_address(address))
        has_code = self.to_hex(code) != '0x'
        return has_code

    def abi_encode_hex(self, types, values):
        codec = self.web3.codec
        if hasattr(codec, 'encode'):
            encoded = codec.encode(types, values)
        else:
            encoded = codec.encode_abi(types, values)
        encoded_hex = Web3.to_hex(encoded)
        return encoded_hex

    @classmethod
    def is_erc_6492_signature(cls, signature):
        signature_hex = cls.to_hex(signature).lower()
        is_erc_6492_signature = signature_hex.endswith(_ERC6492_DETECTION_SUFFIX)
        return is_erc_6492_signature

    @staticmethod
    def to_bytes(value):
        if isinstance(value, bytes):
            value_bytes = value
        else:
            value_bytes = Web3.to_bytes(hexstr=value)

        return value_bytes

    @staticmethod
    def to_hex(value):
        if isinstance(value, str):
            value_hex = value.lower()
        else:
            value_hex = Web3.to_hex(value).lower()

        return value_hex

    @staticmethod
    def encode_eip_712_message(typed_data):
        try:
            from eth_account.messages import encode_typed_data
            encoded_message = encode_typed_data(full_message=typed_data)
        except (ImportError, TypeError):
            from eth_account.messages import encode_structured_data
            encoded_message = encode_structured_data(primitive=typed_data)

        return encoded_message

    @staticmethod
    def get_eip_712_message_hash(typed_data):
        encoded_message = SignatureVerifier.encode_eip_712_message(typed_data)
        message_hash = Web3.keccak(b'\x19' + encoded_message.version + encoded_message.header + encoded_message.body)
        return message_hash

    @staticmethod
    def recover_eip_712_signer(typed_data, signature):
        encoded_message = SignatureVerifier.encode_eip_712_message(typed_data)
        recovered_signer = Account.recover_message(encoded_message, signature=signature)
        return recovered_signer
