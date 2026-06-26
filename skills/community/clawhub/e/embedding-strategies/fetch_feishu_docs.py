# 飞书文档抓取脚本
# 创建时间：2026-03-15 22:31
# 创建者：阿香 🦞
# 功能：抓取飞书文档内容，用于向量化

import requests
import json
import os
from datetime import datetime

# 飞书 API 配置
APP_ID = "cli_a91d70683c789bc7"
APP_SECRET = "t0am3JU79N9TSEPgrk7GKbVLHmCdRGUe"

# 获取 tenant_access_token
def get_tenant_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    response = requests.post(url, json=payload)
    data = response.json()
    if data.get("code") == 0:
        return data.get("tenant_access_token")
    else:
        print(f"获取 Token 失败：{data.get('msg')}")
        return None

# 获取文档列表
def get_doc_list(token, folder_token=None):
    url = "https://open.feishu.cn/open-apis/drive/v1/files"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "type": "docx",
        "page_size": 50
    }
    if folder_token:
        params["folder_token"] = folder_token
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if data.get("code") == 0:
        return data.get("items", [])
    else:
        print(f"获取文档列表失败：{data.get('msg')}")
        return []

# 获取文档内容
def get_doc_content(token, doc_token):
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/raw_content"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    if data.get("code") == 0:
        return data.get("content", "")
    else:
        print(f"获取文档内容失败：{data.get('msg')}")
        return None

# 获取文档元数据
def get_doc_meta(token, doc_token):
    url = f"https://open.feishu.cn/open-apis/drive/v1/files/{doc_token}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    if data.get("code") == 0:
        item = data.get("data", {})
        return {
            "title": item.get("name"),
            "created_time": item.get("created_time"),
            "modified_time": item.get("modified_time"),
            "owner": item.get("owner", {}).get("name"),
            "token": doc_token
        }
    else:
        print(f"获取文档元数据失败：{data.get('msg')}")
        return None

# 主函数
def fetch_feishu_docs():
    print("=== 飞书文档抓取 ===")
    
    # 获取 Token
    token = get_tenant_token()
    if not token:
        return
    
    print(f"✅ Token 获取成功")
    
    # 获取文档列表
    docs = get_doc_list(token)
    if not docs:
        print("❌ 未找到文档")
        return
    
    print(f"✅ 找到 {len(docs)} 个文档")
    
    # 重点文档列表（全文抓取）
    key_docs = [
        "CvKSdaoTOotc2txchsqcH2xJnDg",  # 供应商直连系统项目全记录
        "QWpadUapuosE6qxDql6cTh7Ynxy",  # 端到端质量追溯项目全记录
        "Sr6wd7Co7oRULhxofYHcrcmonhg",  # Skill 系统全记录
        "YOIGdBCaVo7a7bxynfXcbZ1cnIf",  # 项目边界梳理与知识库分类
        "U1OcdSW61oiplBxoovQcoKzpnrd",  # 配置变更记录
        "MgXmdVVuzopcjZxY8lMchwwdnoc",  # 优先级提醒规范
    ]
    
    # 抓取文档
    output_dir = r"C:\Users\Xiabi\.openclaw\workspace\feishu_docs"
    os.makedirs(output_dir, exist_ok=True)
    
    metadata_list = []
    fulltext_count = 0
    meta_count = 0
    
    for doc in docs:
        doc_token = doc.get("token")
        meta = get_doc_meta(token, doc_token)
        
        if not meta:
            continue
        
        # 保存元数据
        metadata_list.append(meta)
        meta_count += 1
        
        # 重点文档抓取全文
        if doc_token in key_docs:
            content = get_doc_content(token, doc_token)
            if content:
                # 保存为 Markdown
                filename = f"{meta['title'][:50]}_{doc_token}.md"
                filepath = os.path.join(output_dir, filename)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"# {meta['title']}\n\n")
                    f.write(f"**作者：** {meta['owner']}\n")
                    f.write(f"**创建时间：** {meta['created_time']}\n")
                    f.write(f"**修改时间：** {meta['modified_time']}\n")
                    f.write(f"**文档 Token：** {doc_token}\n\n")
                    f.write(f"---\n\n")
                    f.write(content)
                print(f"✅ 全文抓取：{meta['title']}")
                fulltext_count += 1
    
    # 保存元数据
    meta_file = os.path.join(output_dir, "metadata.json")
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(metadata_list, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== 抓取完成 ===")
    print(f"元数据：{meta_count} 个")
    print(f"全文：{fulltext_count} 个")
    print(f"输出目录：{output_dir}")

if __name__ == "__main__":
    fetch_feishu_docs()
