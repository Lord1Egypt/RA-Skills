"""
Encoding Converter 单元测试
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.encoding_engine import EncodingConverter


def test_base64():
    ec = EncodingConverter()
    original = "Hello World"
    encoded = ec.base64_encode(original)
    decoded = ec.base64_decode(encoded)
    assert decoded == original

    # URL-safe
    encoded_safe = ec.base64_encode(original, url_safe=True)
    decoded_safe = ec.base64_decode(encoded_safe, url_safe=True)
    assert decoded_safe == original
    print("✓ test_base64 passed")


def test_url_encoding():
    ec = EncodingConverter()
    text = "hello world"
    encoded = ec.url_encode(text)
    decoded = ec.url_decode(encoded)
    assert decoded == text
    print("✓ test_url_encoding passed")


def test_hex():
    ec = EncodingConverter()
    assert ec.to_hex(255) == "ff"
    assert ec.hex_to_int("ff") == 255
    assert ec.to_hex("ABC") == "414243"
    assert ec.from_hex("414243") == "ABC"
    print("✓ test_hex passed")


def test_binary():
    ec = EncodingConverter()
    assert ec.to_binary(255) == "11111111"
    assert ec.from_binary("11111111") == 255
    print("✓ test_binary passed")


def test_hash():
    ec = EncodingConverter()
    data = "test"
    assert len(ec.md5(data)) == 32
    assert len(ec.sha1(data)) == 40
    assert len(ec.sha256(data)) == 64
    assert len(ec.sha512(data)) == 128
    # 一致性检查
    assert ec.md5(data) == ec.md5(data)
    print("✓ test_hash passed")


def test_jwt_decode():
    ec = EncodingConverter()
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    result = ec.jwt_decode(token)
    assert "error" not in result
    assert result["header"]["alg"] == "HS256"
    assert result["payload"]["name"] == "John Doe"
    print("✓ test_jwt_decode passed")


def test_html_encoding():
    ec = EncodingConverter()
    text = "<div>Hello & 你好</div>"
    encoded = ec.html_encode(text)
    decoded = ec.html_decode(encoded)
    assert "&lt;" in encoded
    assert decoded == text
    print("✓ test_html_encoding passed")


def test_random():
    ec = EncodingConverter()
    uuid1 = ec.random_uuid()
    uuid2 = ec.random_uuid()
    assert uuid1 != uuid2
    assert len(ec.random_hex(16)) == 16
    assert len(ec.random_string(16)) == 16
    print("✓ test_random passed")


def test_hmac():
    ec = EncodingConverter()
    result = ec.hmac_sha256("key", "message")
    assert len(result) == 64
    print("✓ test_hmac passed")


if __name__ == "__main__":
    test_base64()
    test_url_encoding()
    test_hex()
    test_binary()
    test_hash()
    test_jwt_decode()
    test_html_encoding()
    test_random()
    test_hmac()
    print("\n所有测试通过! ✅")
