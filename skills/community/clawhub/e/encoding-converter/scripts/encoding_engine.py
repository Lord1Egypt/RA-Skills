"""
Encoding Converter - 多格式编码转换工具引擎
"""
import base64
import urllib.parse
import hashlib
import html
import json
import binascii
import uuid
import secrets
from typing import Dict, Any, Optional, Union


class EncodingConverter:
    """支持 Base64、URL 编码、哈希、JWT 解码、HTML 实体、进制转换的工具集"""

    def base64_encode(self, data: Union[str, bytes], url_safe: bool = False) -> str:
        """Base64 编码"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        if url_safe:
            return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')
        return base64.b64encode(data).decode('utf-8')

    def base64_decode(self, data: str, url_safe: bool = False) -> str:
        """Base64 解码"""
        if url_safe:
            # 补齐 padding
            padding = 4 - len(data) % 4
            if padding != 4:
                data += '=' * padding
            decoded = base64.urlsafe_b64decode(data)
        else:
            decoded = base64.b64decode(data)
        return decoded.decode('utf-8') if isinstance(decoded, bytes) else decoded

    def url_encode(self, text: str, safe: str = '') -> str:
        """URL 编码"""
        return urllib.parse.quote(text, safe=safe)

    def url_decode(self, text: str) -> str:
        """URL 解码"""
        return urllib.parse.unquote(text)

    def to_hex(self, data: Union[str, int, bytes]) -> str:
        """转换为十六进制表示"""
        if isinstance(data, int):
            return hex(data)[2:]
        if isinstance(data, str):
            return data.encode('utf-8').hex()
        if isinstance(data, bytes):
            return data.hex()
        return str(data)

    def from_hex(self, hex_string: str) -> str:
        """十六进制字符串还原为文本"""
        try:
            return bytes.fromhex(hex_string).decode('utf-8')
        except (ValueError, UnicodeDecodeError):
            return hex_string

    def hex_to_int(self, hex_string: str) -> int:
        """十六进制转整数"""
        return int(hex_string, 16)

    def to_binary(self, num: int) -> str:
        """整数转二进制字符串"""
        return bin(num)[2:]

    def from_binary(self, binary: str) -> int:
        """二进制字符串转整数"""
        return int(binary, 2)

    def to_octal(self, num: int) -> str:
        """整数转八进制字符串"""
        return oct(num)[2:]

    def from_octal(self, octal: str) -> int:
        """八进制字符串转整数"""
        return int(octal, 8)

    def md5(self, data: Union[str, bytes]) -> str:
        """计算 MD5 哈希"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.md5(data).hexdigest()

    def sha1(self, data: Union[str, bytes]) -> str:
        """计算 SHA1 哈希"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha1(data).hexdigest()

    def sha256(self, data: Union[str, bytes]) -> str:
        """计算 SHA256 哈希"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()

    def sha512(self, data: Union[str, bytes]) -> str:
        """计算 SHA512 哈希"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha512(data).hexdigest()

    def hmac_sha256(self, key: Union[str, bytes], message: Union[str, bytes]) -> str:
        """计算 HMAC-SHA256"""
        import hmac
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(message, str):
            message = message.encode('utf-8')
        return hmac.new(key, message, hashlib.sha256).hexdigest()

    def jwt_decode(self, token: str) -> Dict[str, Any]:
        """解码 JWT Token（不验证签名）"""
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return {"error": "Invalid JWT format"}

            def decode_part(part: str) -> Dict:
                # 补齐 padding
                padding = 4 - len(part) % 4
                if padding != 4:
                    part += '=' * padding
                decoded = base64.urlsafe_b64decode(part)
                return json.loads(decoded)

            return {
                "header": decode_part(parts[0]),
                "payload": decode_part(parts[1]),
                "signature": parts[2],
            }
        except Exception as e:
            return {"error": str(e)}

    def html_encode(self, text: str) -> str:
        """HTML 实体编码"""
        return html.escape(text)

    def html_decode(self, text: str) -> str:
        """HTML 实体解码"""
        return html.unescape(text)

    def random_uuid(self) -> str:
        """生成随机 UUID"""
        return str(uuid.uuid4())

    def random_hex(self, length: int = 32) -> str:
        """生成随机十六进制字符串"""
        return secrets.token_hex(length // 2 if length % 2 == 0 else (length + 1) // 2)[:length]

    def random_string(self, length: int = 16) -> str:
        """生成随机安全字符串"""
        import string
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def crc32(self, data: Union[str, bytes]) -> str:
        """计算 CRC32 校验值"""
        import zlib
        if isinstance(data, str):
            data = data.encode('utf-8')
        return format(zlib.crc32(data) & 0xffffffff, '08x')
