from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

class CryptoIdentity:
    def __init__(self):
        self.private_key = Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def sign(self, message: bytes) -> bytes:
        """
        使用私钥对消息签名
        """
        return self.private_key.sign(message)

    def serialize_public(self) -> str:
        """
        输出公钥 hex，用于验证身份
        """
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        ).hex()
