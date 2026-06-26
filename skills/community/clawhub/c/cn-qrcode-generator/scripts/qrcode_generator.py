#!/usr/bin/env python3
"""cn-qrcode-generator - 二维码生成工具"""
import sys, os, base64, ssl, urllib.request, urllib.parse, certifi

def generate_qrcode(text, size=300, margin=4, format='png'):
    """生成二维码
    
    使用qrserver.com API，无需安装依赖
    SSL标准验证（certifi根证书）
    """
    encoded_text = urllib.parse.quote(text)
    url = f"https://api.qrserver.com/v1/create-qr-code/?size={size}x{size}&margin={margin}&format={format}&data={encoded_text}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        ctx = ssl.create_default_context()
        ctx.load_verify_locations(certifi.where())
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=15, context=ctx)
        data = response.read()
        return {
            "success": True,
            "data": f"data:image/{format};base64,{base64.b64encode(data).decode()}",
            "url": url
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == '__main__':
    text = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    result = generate_qrcode(text)
    if result["success"]:
        print(f"✅ 二维码生成成功!")
        print(f"   Base64长度: {len(result['data'])} 字符")
    else:
        print(f"❌ 生成失败: {result['error']}")
