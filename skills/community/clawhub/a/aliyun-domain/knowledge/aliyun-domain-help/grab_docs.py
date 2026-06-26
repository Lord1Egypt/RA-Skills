#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云域名帮助文档批量抓取脚本
使用 browser_use 的 JavaScript 执行功能来提取页面内容
"""

import json
import os
from datetime import datetime

# 配置
TARGET_DIR = "/Users/kevin/doc/aliyun-domain-help"
BASE_URL = "https://help.aliyun.com"

# 文档列表
DOCS = [
  {"category": "01-产品概述", "name": "什么是阿里云域名服务", "url": "/zh/dws/product-overview/what-is-domains"},
  {"category": "01-产品概述", "name": "图说域名", "url": "/zh/dws/product-overview/from-domain-name-to-website-illustration"},
  {"category": "01-产品概述", "name": "功能特性", "url": "/zh/dws/product-overview/product-function-custom-node-domain-normal"},
  {"category": "01-产品概述", "name": "限制条件", "url": "/zh/dws/product-overview/limits"},
  {"category": "01-产品概述", "name": "基本概念", "url": "/zh/dws/product-overview/terms"},
  {"category": "01-产品概述", "name": "顶级域名分类解析", "url": "/zh/dws/product-overview/top-level-domain-name-suffix-list"},
  {"category": "02-快速入门", "name": "域名注册快速入门", "url": "/zh/dws/getting-started/quickly-register-a-new-domain-name"},
  {"category": "02-快速入门", "name": "域名交易快速入门", "url": "/zh/dws/getting-started/domain-name-trading-quick-start"},
  {"category": "02-快速入门", "name": "从域名注册到网站搭建", "url": "/zh/dws/getting-started/the-whole-process-of-website-building"},
  {"category": "03-操作指南", "name": "域名实名认证", "url": "/zh/dws/user-guide/how-to-complete-domain-name-authentication"},
  {"category": "03-操作指南", "name": "域名注册", "url": "/zh/dws/user-guide/how-to-register-a-domain-name"},
  {"category": "03-操作指南", "name": "域名过户与信息修改", "url": "/zh/dws/user-guide/domain-information-modification"},
  {"category": "03-操作指南", "name": "域名转移", "url": "/zh/dws/user-guide/domain-transfer"},
  {"category": "03-操作指南", "name": "域名交易", "url": "/zh/dws/user-guide/domain-name-transaction"},
  {"category": "03-操作指南", "name": "域名管理", "url": "/zh/dws/user-guide/domain-name-management"},
  {"category": "03-操作指南", "name": "域名安全", "url": "/zh/dws/user-guide/domain-name-security1"},
  {"category": "03-操作指南", "name": "轻量网站搭建", "url": "/zh/dws/user-guide/ai-static-display-station"},
  {"category": "04-安全合规", "name": "侵权与域名滥用的处理", "url": "/zh/dws/security-and-compliance/handling-of-copyright-infringements-and-domain-name-abuse"},
  {"category": "05-开发参考", "name": "集成概览", "url": "/zh/dws/developer-reference/call-openapi"},
  {"category": "06-服务支持", "name": "域名功能介绍视频", "url": "/zh/dws/support/function-introduction-video"},
  {"category": "07-万小智 AI 建站", "name": "万小智 AI 建站操作指南", "url": "/zh/dws/website-backend-management"},
  {"category": "07-万小智 AI 建站", "name": "常见问题", "url": "/zh/dws/faq"}
]

def create_output_dirs():
    """创建输出目录结构"""
    categories = set(doc["category"] for doc in DOCS)
    for cat in categories:
        os.makedirs(os.path.join(TARGET_DIR, cat), exist_ok=True)
    print(f"已创建 {len(categories)} 个分类目录")

def generate_js_extract():
    """生成用于 browser_use eval 的 JavaScript 代码"""
    return """() => {
  // 提取标题
  const title = document.querySelector('h1')?.textContent || document.title;
  
  // 提取更新时间
  const updateTime = document.querySelector('.update-time')?.textContent || 
                     document.querySelector('text')?.textContent?.match(/更新时间：([\\d-]+)/)?.[1] || '';
  
  // 提取参与者
  const participants = document.querySelector('text')?.textContent?.match(/参与者：([^\\s]+)/)?.[1] || '';
  
  // 提取主要内容区域
  const main = document.querySelector('main');
  if (!main) return { title, content: 'No main content found', error: true };
  
  // 克隆节点以便修改
  const clones = main.cloneNode(true);
  
  // 移除不需要的元素
  clones.querySelectorAll('nav, footer, .copyright, .feedback, .prev-next, .breadcrumb, .sidebar').forEach(el => el.remove());
  
  // 提取纯文本内容
  const content = clones.textContent
    .replace(/\\s+/g, ' ')
    .replace(/(首页 | 域名 | 产品概述 | 产品简介 | 我的收藏 | 上一篇 | 下一篇 | 反馈 | 本页导读)/g, '')
    .trim();
  
  // 提取所有内部链接
  const links = Array.from(clones.querySelectorAll('a'))
    .map(a => ({ 
      text: a.textContent.trim(), 
      href: a.href 
    }))
    .filter(l => l.text && l.href && l.href.includes('help.aliyun.com') && !l.href.includes('#'))
    .slice(0, 30);
  
  // 提取图片
  const images = Array.from(clones.querySelectorAll('img'))
    .map(img => ({ src: img.src, alt: img.alt || '' }))
    .filter(i => i.src && (i.src.includes('aliyuncs.com') || i.src.includes('alicdn.com')));
  
  return { 
    title, 
    updateTime, 
    participants,
    content: content.substring(0, 10000), 
    links, 
    images 
  };
}"""

def save_document(doc, data):
    """保存文档为 Markdown 格式"""
    category = doc["category"]
    name = doc["name"]
    
    # 生成文件名
    filename = f"{name.replace(' ', '_')}.md"
    output_path = os.path.join(TARGET_DIR, category, filename)
    
    # 生成 Markdown 内容
    md_content = f"""# {data.get('title', name)}

> **来源**: 阿里云帮助文档  
> **原文地址**: {BASE_URL}{doc['url']}  
> **更新时间**: {data.get('updateTime', '未知')}  
> **参与者**: {data.get('participants', '未知')}  
> **抓取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📄 文档内容

{data.get('content', '内容提取失败')}

---

## 🔗 相关链接

"""
    
    # 添加链接
    links = data.get('links', [])
    if links:
        seen = set()
        for link in links:
            if link['href'] not in seen:
                seen.add(link['href'])
                md_content += f"- [{link['text']}]({link['href']})\n"
    else:
        md_content += "暂无相关链接\n"
    
    # 添加图片
    images = data.get('images', [])
    if images:
        md_content += "\n---\n\n## 🖼️ 文档图片\n\n"
        for i, img in enumerate(images, 1):
            md_content += f"![{img['alt'] or f'图片{i}'}]({img['src']})\n"
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return output_path

def main():
    print("=" * 60)
    print("阿里云域名帮助文档批量抓取工具")
    print("=" * 60)
    print(f"目标目录：{TARGET_DIR}")
    print(f"文档数量：{len(DOCS)}")
    print()
    
    # 创建目录
    create_output_dirs()
    
    # 输出文档列表供 browser_use 使用
    print("文档列表:")
    for i, doc in enumerate(DOCS, 1):
        url = f"{BASE_URL}{doc['url']}"
        print(f"  {i:2d}. [{doc['category']}] {doc['name']}")
        print(f"      {url}")
    
    print()
    print("=" * 60)
    print("使用说明:")
    print("1. 使用 browser_use 依次访问每个 URL")
    print("2. 执行 extract JS 代码获取内容")
    print("3. 调用 save_document 保存为 Markdown")
    print("=" * 60)
    
    # 保存文档列表为 JSON
    with open(os.path.join(TARGET_DIR, 'docs_list_full.json'), 'w', encoding='utf-8') as f:
        json.dump(DOCS, f, ensure_ascii=False, indent=2)
    
    print(f"\n文档列表已保存：{os.path.join(TARGET_DIR, 'docs_list_full.json')}")

if __name__ == "__main__":
    main()
