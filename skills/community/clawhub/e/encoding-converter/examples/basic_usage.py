"""
Encoding Converter - 基础使用示例
"""
from scripts.encoding_engine import EncodingConverter


def main():
    ec = EncodingConverter()

    print("=" * 50)
    print("示例 1: Base64 编解码")
    print("=" * 50)
    original = "Hello World 你好世界"
    encoded = ec.base64_encode(original)
    decoded = ec.base64_decode(encoded)
    print(f"原文: {original}")
    print(f"Base64 编码: {encoded}")
    print(f"Base64 解码: {decoded}")

    print("\n" + "=" * 50)
    print("示例 2: URL 编码")
    print("=" * 50)
    text = "key=你好 world&value=测试"
    encoded = ec.url_encode(text)
    decoded = ec.url_decode(encoded)
    print(f"原文: {text}")
    print(f"URL 编码: {encoded}")
    print(f"URL 解码: {decoded}")

    print("\n" + "=" * 50)
    print("示例 3: 哈希计算")
    print("=" * 50)
    data = "password123"
    print(f"MD5:    {ec.md5(data)}")
    print(f"SHA1:   {ec.sha1(data)}")
    print(f"SHA256: {ec.sha256(data)}")

    print("\n" + "=" * 50)
    print("示例 4: JWT 解码")
    print("=" * 50)
    # 示例 JWT token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    decoded = ec.jwt_decode(token)
    print(f"JWT Token: {token}")
    print(f"解码结果: {decoded}")

    print("\n" + "=" * 50)
    print("示例 5: 进制转换")
    print("=" * 50)
    num = 255
    print(f"十进制: {num}")
    print(f"二进制: {ec.to_binary(num)}")
    print(f"八进制: {ec.to_octal(num)}")
    print(f"十六进制: {ec.to_hex(num)}")
    print(f"十六进制还原: {ec.hex_to_int('ff')}")

    print("\n" + "=" * 50)
    print("示例 6: HTML 实体编码")
    print("=" * 50)
    html_text = "<div>Hello & 你好</div>"
    encoded = ec.html_encode(html_text)
    decoded = ec.html_decode(encoded)
    print(f"原文: {html_text}")
    print(f"编码: {encoded}")
    print(f"解码: {decoded}")

    print("\n" + "=" * 50)
    print("示例 7: 随机生成")
    print("=" * 50)
    print(f"UUID: {ec.random_uuid()}")
    print(f"随机 HEX: {ec.random_hex(16)}")
    print(f"随机字符串: {ec.random_string(16)}")


if __name__ == "__main__":
    main()
