#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1-Click WOA - 微信公众号草稿箱一键发布脚本
读取 ~/.openclaw/agents/gzh-assistant/wechat/credentials.json 获取配置
"""

import requests
import json
import os
import sys
import re
from pathlib import Path

# ========== 配置路径 ==========
AGENT_DIR = Path.home() / ".openclaw/agents/gzh-assistant"
CONFIG_FILE = AGENT_DIR / "wechat/credentials.json"
IMAGE_DIR_DEFAULT = AGENT_DIR / "wechat_images"


def load_credentials():
    """加载凭证配置"""
    if not CONFIG_FILE.exists():
        print(f"❌ 配置文件不存在: {CONFIG_FILE}")
        print("请先运行 skill 配置流程或手动创建 credentials.json")
        return None
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        creds = json.load(f)
    required = ["app_id", "app_secret"]
    for key in required:
        if key not in creds:
            print(f"❌ 配置缺少必要字段: {key}")
            return None
    return creds


def get_access_token(app_id, app_secret):
    """获取 access_token"""
    url = f"https://api.weixin.qq.com/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": app_id,
        "secret": app_secret
    }
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()
    if "access_token" in data:
        return data["access_token"], None
    return None, data


def upload_material(access_token, file_path, material_type="image"):
    """上传永久素材"""
    if not os.path.exists(file_path):
        return None, {"errcode": -1, "errmsg": f"文件不存在: {file_path}"}
    
    filename = os.path.basename(file_path)
    mime = "image/png" if filename.endswith(".png") else "image/jpeg"
    
    with open(file_path, "rb") as f:
        files = {"media": (filename, f, mime)}
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type={material_type}"
        r = requests.post(url, files=files, timeout=30)
    result = r.json()
    if "media_id" in result:
        return result["media_id"], None
    return None, result


def create_draft(access_token, article):
    """创建草稿"""
    payload = {"articles": [article]}
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    resp = requests.post(url, json=payload, headers=headers, timeout=15)
    return resp.json()


def generate_html_fallback(title, digest, content, image_dir):
    """生成 HTML fallback 文件供手动发布"""
    html_path = AGENT_DIR / "article_fallback.html"
    
    # 处理图片路径
    content_with_imgs = content
    for i in range(1, 5):
        local_img = f"{image_dir}/layer{i}.png"
        if os.path.exists(local_img):
            # 在 fallback 模式下使用本地路径引用（用户需确保图片可访问）
            content_with_imgs = content_with_imgs.replace(f"layer{i}.png", local_img)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
h1 {{ font-size: 24px; margin-bottom: 10px; }}
.digest {{ color: #666; margin-bottom: 20px; font-size: 14px; }}
.content img {{ max-width: 100%; height: auto; margin: 10px 0; }}
</style>
</head>
<body>
<h1>{title}</h1>
<p class="digest">{digest}</p>
<hr>
<div class="content">
{content}
</div>
</body>
</html>"""
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    return html_path


def main():
    print("=" * 50)
    print("1-Click WOA - 微信公众号草稿箱发布")
    print("=" * 50)
    
    # 1. 加载凭证
    print("\n[1/6] 加载凭证配置...")
    creds = load_credentials()
    if not creds:
        sys.exit(1)
    app_id = creds["app_id"]
    app_secret = creds["app_secret"]
    image_dir = Path(creds.get("image_dir", str(IMAGE_DIR_DEFAULT)))
    print(f"  ✅ AppID: {app_id[:10]}...")
    
    # 2. 获取 Token
    print("\n[2/6] 获取 access_token...")
    token, err = get_access_token(app_id, app_secret)
    if err:
        print(f"  ❌ Token 获取失败: {err}")
        sys.exit(1)
    print(f"  ✅ Token 获取成功")
    
    # 3. 上传图片
    print("\n[3/6] 上传图片素材...")
    image_map = {
        "cover": image_dir / "cover.png",
        "layer1": image_dir / "layer1.png",
        "layer2": image_dir / "layer2.png",
        "layer3": image_dir / "layer3.png",
        "layer4": image_dir / "layer4.png",
    }
    
    media_ids = {}
    for name, path in image_map.items():
        if path.exists():
            mid, err = upload_material(token, str(path))
            if err:
                print(f"  ⚠️  {name}: 上传失败 {err}")
            else:
                media_ids[name] = mid
                print(f"  ✅ {name}: {mid[:20]}...")
        else:
            print(f"  ○ {name}: 跳过（文件不存在）")
    
    if "cover" not in media_ids:
        print("  ❌ 封面图必须上传")
        sys.exit(1)
    
    # 4. 从命令行参数或 stdin 读取文章内容
    print("\n[4/6] 读取文章内容...")
    if len(sys.argv) > 1:
        # 从文件读取
        article_file = sys.argv[1]
        if os.path.exists(article_file):
            with open(article_file, "r", encoding="utf-8") as f:
                article_content = f.read()
            print(f"  ✅ 从文件读取: {article_file}")
        else:
            # 直接作为内容
            article_content = sys.argv[1]
            print("  ✅ 从命令行参数读取")
    else:
        print("  ⚠️  未提供文章内容，请在 OpenClaw 对话中提供")
        print("  用法: python3 publish.py <文章内容或文件路径>")
        article_content = ""
    
    if not article_content.strip():
        print("  ❌ 文章内容为空")
        sys.exit(1)
    
    # 5. 解析文章（简单处理）
    # 期望格式：标题|摘要|正文（用|||分隔）
    parts = article_content.split("|||")
    if len(parts) >= 3:
        title = parts[0].strip()
        digest = parts[1].strip()
        body = parts[2].strip()
    elif len(parts) == 2:
        title = parts[0].strip()
        digest = parts[1].strip()[:60]
        body = parts[1].strip()
    else:
        title = "未命名文章"
        digest = article_content[:60]
        body = article_content
    
    print(f"  标题: {title[:30]}...")
    print(f"  摘要: {digest[:30]}...")
    
    # 6. 构建草稿并发布
    print("\n[5/6] 构建草稿...")
    layer_ids = [media_ids.get(f"layer{i}") for i in range(1, 5) if f"layer{i}" in media_ids]
    
    # 构建正文 HTML
    content_html = f"<p>{body.replace(chr(10), '</p><p>')}</p>"
    for i, lid in enumerate(layer_ids, 1):
        content_html += f'<p><img src="{lid}" /></p>'
    
    article = {
        "title": title,
        "author": "",
        "digest": digest,
        "content": content_html,
        "content_source_url": "",
        "thumb_media_id": media_ids["cover"],
        "need_open_comment": 0,
        "only_fans_can_comment": 0
    }
    
    print("\n[6/6] 提交草稿...")
    result = create_draft(token, article)
    
    if "media_id" in result:
        media_id = result["media_id"]
        print(f"\n{'='*50}")
        print(f"🎉 草稿发布成功！")
        print(f"{'='*50}")
        print(f"media_id: {media_id}")
        print(f"预览链接: https://mp.weixin.qq.com/cgi-bin/draft?spm={media_id[:10]}")
        print(f"\n请到微信公众号后台 → 内容与互动 → 草稿箱 查看")
    else:
        errcode = result.get("errcode", -1)
        errmsg = result.get("errmsg", "未知错误")
        print(f"\n❌ 草稿发布失败: [{errcode}] {errmsg}")
        
        # 检测是否是中文编码问题
        if errcode in [40001, 40008] or "encoding" in errmsg.lower():
            print("\n🔄 切换到 HTML Fallback 模式...")
            fallback_path = generate_html_fallback(title, digest, content_html, image_dir)
            print(f"✅ HTML 文件已生成: {fallback_path}")
            print("请下载后手动复制内容到微信公众号后台发布")
        
        sys.exit(1)


if __name__ == "__main__":
    main()
