import re

with open('/root/.openclaw/workspace/skills/fp-skill/skill.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_func = '''# 将 base64 字符串转换成图片
def base64_to_image(base64_str):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    img = img.convert("RGB")
    return img'''

new_func = '''# 将 base64 字符串或 URL 转换成图片
def base64_to_image(base64_str):
    # 如果是 URL，下载图片
    if base64_str.startswith('http'):
        print(f"从 URL 下载验证码图片...")
        response = requests.get(base64_str, timeout=10, verify=False)
        byte_data = response.content
    else:
        # 是 base64 字符串
        base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
        byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    img = img.convert("RGB")
    return img'''

content = content.replace(old_func, new_func)

with open('/root/.openclaw/workspace/skills/fp-skill/skill.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied successfully")
