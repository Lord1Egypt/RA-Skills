#!/usr/bin/env python3
import os
import re
import requests
import argparse
import markdownify
from urllib.parse import urlparse
from pathlib import Path
import time

# 飞书API配置
FEISHU_API_HOST = "https://open.feishu.cn"
APP_ID = os.getenv("FEISHU_APP_ID")
APP_SECRET = os.getenv("FEISHU_APP_SECRET")

# 全局缓存token
tenant_access_token = None
token_expire_time = 0

def get_tenant_access_token():
    global tenant_access_token, token_expire_time
    current_time = int(time.time())
    if tenant_access_token and current_time < token_expire_time - 60:
        return tenant_access_token
    
    url = f"{FEISHU_API_HOST}/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {"app_id": APP_ID, "app_secret": APP_SECRET}
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    if result.get("code") != 0:
        raise Exception(f"获取token失败: {result.get('msg')}")
    
    tenant_access_token = result.get("tenant_access_token")
    token_expire_time = current_time + result.get("expire", 7200)
    return tenant_access_token

def get_doc_info(doc_token):
    """获取文档基本信息"""
    url = f"{FEISHU_API_HOST}/open-apis/docx/v1/documents/{doc_token}"
    headers = {"Authorization": f"Bearer {get_tenant_access_token()}"}
    
    response = requests.get(url, headers=headers)
    result = response.json()
    if result.get("code") != 0:
        raise Exception(f"获取文档信息失败: {result.get('msg')}")
    return result.get("data", {}).get("document", {})

def get_doc_raw_content(doc_token):
    """获取文档的原始HTML内容"""
    url = f"{FEISHU_API_HOST}/open-apis/docx/v1/documents/{doc_token}/raw_content"
    headers = {"Authorization": f"Bearer {get_tenant_access_token()}"}
    params = {"lang": 0}
    
    response = requests.get(url, headers=headers, params=params)
    result = response.json()
    if result.get("code") != 0:
        raise Exception(f"获取文档内容失败: {result.get('msg')}")
    return result.get("data", {}).get("content", "")

def download_image(img_url, output_dir):
    """下载文档内图片到本地"""
    if not img_url.startswith("http"):
        return img_url
    
    img_dir = Path(output_dir) / "assets"
    img_dir.mkdir(parents=True, exist_ok=True)
    
    # 解析文件名
    parsed = urlparse(img_url)
    filename = os.path.basename(parsed.path)
    if not "." in filename:
        filename += ".png"
    
    img_path = img_dir / filename
    if img_path.exists():
        return f"assets/{filename}"
    
    try:
        response = requests.get(img_url, timeout=10)
        response.raise_for_status()
        with open(img_path, "wb") as f:
            f.write(response.content)
        return f"assets/{filename}"
    except Exception as e:
        print(f"图片下载失败 {img_url}: {str(e)}")
        return img_url

def html_to_markdown(html_content, output_dir):
    """HTML转Markdown，处理图片路径"""
    # 转换为Markdown
    md_content = markdownify.markdownify(html_content, heading_style="ATX")
    
    # 处理图片链接，下载到本地
    img_pattern = re.compile(r'!\[.*?\]\((https?://.*?)\)')
    def replace_img(match):
        img_url = match.group(1)
        local_path = download_image(img_url, output_dir)
        return f"![]({local_path})"
    
    md_content = img_pattern.sub(replace_img, md_content)
    return md_content

def export_single_doc(doc_url, output_dir, keep_html=False):
    """导出单个飞书文档"""
    # 解析doc_token
    doc_token_match = re.search(r'docx/([a-zA-Z0-9]+)', doc_url)
    if not doc_token_match:
        print(f"无效的文档链接: {doc_url}")
        return False
    doc_token = doc_token_match.group(1)
    
    try:
        # 获取文档信息
        doc_info = get_doc_info(doc_token)
        doc_title = doc_info.get("title", f"未命名文档_{doc_token}")
        # 清理标题中的非法字符
        doc_title = re.sub(r'[\\/*?:"<>|]', "_", doc_title)
        
        # 创建输出目录
        doc_output_dir = Path(output_dir) / doc_title
        doc_output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"正在导出: {doc_title}")
        
        # 获取文档内容
        html_content = get_doc_raw_content(doc_token)
        
        # 保存HTML（可选）
        if keep_html:
            with open(doc_output_dir / f"{doc_title}.html", "w", encoding="utf-8") as f:
                f.write(html_content)
        
        # 转换为Markdown
        md_content = html_to_markdown(html_content, doc_output_dir)
        
        # 保存Markdown
        with open(doc_output_dir / f"{doc_title}.md", "w", encoding="utf-8") as f:
            f.write(md_content)
        
        print(f"导出完成: {doc_output_dir}/{doc_title}.md")
        return True
    except Exception as e:
        print(f"导出文档失败 {doc_url}: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description="飞书文档批量导出工具")
    parser.add_argument("--url", required=True, help="飞书文档/文件夹链接")
    parser.add_argument("--output", default="./feishu_export", help="输出目录")
    parser.add_argument("--recursive", action="store_true", help="是否递归导出子文件夹")
    parser.add_argument("--keep-html", action="store_true", help="是否保留原始HTML文件")
    
    args = parser.parse_args()
    
    # 检查环境变量
    if not APP_ID or not APP_SECRET:
        print("错误：请先设置FEISHU_APP_ID和FEISHU_APP_SECRET环境变量")
        return
    
    # 创建输出目录
    Path(args.output).mkdir(parents=True, exist_ok=True)
    
    # 判断是文档还是文件夹
    if "docx/" in args.url:
        # 单个文档
        success = export_single_doc(args.url, args.output, args.keep_html)
        if success:
            print("全部导出完成！")
        else:
            print("导出失败！")
    else:
        # 文件夹导出功能待实现
        print("文件夹批量导出功能正在开发中，目前仅支持单个文档导出")

if __name__ == "__main__":
    main()
