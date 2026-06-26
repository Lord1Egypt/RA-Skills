#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
網頁抓取工具 - 基於 Agent Browser
支持微信文章、新聞、博客等內容抓取，自動保存為飛書文檔

使用示例：
```python
from web_scraper import WebScraper

scraper = WebScraper()

# 抓取單個網頁
scraper.scrape("https://example.com/article", save_to_feishu=True)

# 批量抓取
urls = ["url1", "url2", "url3"]
scraper.batch_scrape(urls, output_dir="./articles")

# 定時抓取（配合 cron）
# 每天 9:00 抓取指定網站
# 0 9 * * * python3 /path/to/web_scraper.py scheduled
```
"""

import os
import sys
import json
from datetime import datetime
from typing import List, Dict, Optional
from browser_tool import BrowserTool


class WebScraper:
    """網頁抓取器"""
    
    def __init__(self, session_name: str = "scraper"):
        self.browser = BrowserTool(session_name=session_name)
        self.output_dir = "./scraped_content"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def scrape(self, url: str, title: Optional[str] = None, 
               save_to_feishu: bool = False, 
               extract_images: bool = True,
               extract_links: bool = False) -> Dict[str, any]:
        """
        抓取單個網頁
        
        Args:
            url: 網址
            title: 自定義標題（可選，自動檢測如果未提供）
            save_to_feishu: 是否保存到飛書文檔
            extract_images: 是否提取圖片
            extract_links: 是否提取鏈接
            
        Returns:
            抓取結果
        """
        result = {
            "url": url,
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "content": "",
            "title": "",
            "images": [],
            "links": [],
            "feishu_doc_token": None
        }
        
        try:
            # 1. 打開網頁
            print(f"📖 打開網頁：{url}")
            open_result = self.browser.open(url)
            
            if not open_result.get("success"):
                result["error"] = f"打開網頁失敗：{open_result.get('error')}"
                return result
            
            # 2. 等待加載
            print("⏳ 等待頁面加載...")
            self.browser.wait(load_state="networkidle")
            
            # 3. 獲取標題
            title_result = self.browser.get_title()
            page_title = title or title_result.get("data", "無標題")
            result["title"] = page_title
            print(f"📑 頁面標題：{page_title}")
            
            # 4. 獲取快照（識別元素）
            print("📸 獲取頁面快照...")
            snapshot_result = self.browser.snapshot(interactive=True)
            
            # 5. 提取主要內容
            print("📝 提取內容...")
            
            # 嘗試提取文章內容（常見選擇器）
            content_selectors = [
                "article", 
                ".article-content", 
                ".post-content", 
                ".content", 
                "#content",
                ".entry-content",
                ".article-body"
            ]
            
            content = ""
            for selector in content_selectors:
                content_result = self.browser.get_text(selector)
                if content_result.get("success") and content_result.get("data"):
                    content = content_result["data"]
                    print(f"✅ 使用選擇器提取內容：{selector}")
                    break
            
            # 如果沒找到，提取 body
            if not content:
                content_result = self.browser.get_text("body")
                content = content_result.get("data", "")
            
            result["content"] = content
            print(f"📊 提取內容長度：{len(content)} 字符")
            
            # 6. 提取圖片（可選）
            if extract_images:
                print("🖼️ 提取圖片...")
                images = self.browser.extract_images()
                result["images"] = images
                print(f"📊 提取圖片數量：{len(images)}")
            
            # 7. 提取鏈接（可選）
            if extract_links:
                print("🔗 提取鏈接...")
                links = self.browser.extract_links()
                result["links"] = links
                print(f"📊 提取鏈接數量：{len(links)}")
            
            # 8. 保存到飛書文檔（可選）
            if save_to_feishu:
                print("📤 保存到飛書文檔...")
                # 格式化內容
                feishu_content = self._format_for_feishu(result)
                
                # 使用 feishu_doc 工具
                try:
                    from feishu_doc import feishu_doc
                    
                    doc_result = feishu_doc(
                        action="create",
                        title=f"📄 {page_title}",
                        content=feishu_content
                    )
                    
                    if doc_result.get("success"):
                        result["feishu_doc_token"] = doc_result.get("doc_token")
                        print(f"✅ 已保存到飛書文檔：{doc_result.get('doc_token')}")
                    else:
                        print(f"⚠️ 飛書保存失敗：{doc_result.get('error')}")
                
                except Exception as e:
                    print(f"⚠️ 飛書保存失敗：{e}")
            
            # 9. 保存到本地文件
            local_file = self._save_to_local(result)
            print(f"💾 保存到本地：{local_file}")
            
            result["success"] = True
            result["local_file"] = local_file
            
        except Exception as e:
            result["error"] = str(e)
            print(f"❌ 抓取失敗：{e}")
        
        finally:
            # 關閉瀏覽器
            self.browser.close()
        
        return result
    
    def batch_scrape(self, urls: List[str], output_dir: Optional[str] = None,
                     save_to_feishu: bool = False) -> List[Dict[str, any]]:
        """
        批量抓取網頁
        
        Args:
            urls: 網址列表
            output_dir: 輸出目錄
            save_to_feishu: 是否保存到飛書
            
        Returns:
            抓取結果列表
        """
        if output_dir:
            self.output_dir = output_dir
        
        results = []
        total = len(urls)
        
        print(f"🚀 開始批量抓取，共 {total} 個網頁")
        
        for i, url in enumerate(urls, 1):
            print(f"\n{'='*60}")
            print(f"[{i}/{total}] 抓取：{url}")
            print(f"{'='*60}")
            
            result = self.scrape(url, save_to_feishu=save_to_feishu)
            results.append(result)
            
            # 簡單延遲，避免過於頻繁
            if i < total:
                import time
                time.sleep(2)
        
        # 生成汇总報告
        summary = self._generate_summary(results)
        summary_file = os.path.join(self.output_dir, f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 批量抓取完成，汇总報告：{summary_file}")
        
        return results
    
    def _format_for_feishu(self, scraped_data: Dict) -> str:
        """格式化內容為飛書文檔"""
        content = []
        
        # 標題
        content.append(f"# {scraped_data['title']}")
        content.append("")
        
        # 元信息
        content.append(f"**來源**: {scraped_data['url']}")
        content.append(f"**抓取時間**: {scraped_data['timestamp']}")
        content.append("")
        content.append("---")
        content.append("")
        
        # 主要內容
        content.append("## 📝 內容")
        content.append("")
        content.append(scraped_data['content'])
        content.append("")
        
        # 圖片（如果有）
        if scraped_data.get('images'):
            content.append("---")
            content.append("")
            content.append(f"## 🖼️ 圖片 ({len(scraped_data['images'])} 張)")
            content.append("")
            
            for i, img in enumerate(scraped_data['images'][:10], 1):  # 最多 10 張
                content.append(f"{i}. {img.get('alt', '無標題')}")
                content.append(f"   - {img.get('src')}")
                content.append("")
        
        # 鏈接（如果有）
        if scraped_data.get('links'):
            content.append("---")
            content.append("")
            content.append(f"## 🔗 鏈接 ({len(scraped_data['links'])} 個)")
            content.append("")
            
            for i, link in enumerate(scraped_data['links'][:20], 1):  # 最多 20 個
                content.append(f"{i}. [{link.get('text')}]({link.get('href')})")
            
        return "\n".join(content)
    
    def _save_to_local(self, scraped_data: Dict) -> str:
        """保存到本地文件"""
        # 生成文件名
        safe_title = scraped_data['title'].replace('/', '_').replace('\\', '_')[:50]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{safe_title}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        # 保存 JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(scraped_data, f, ensure_ascii=False, indent=2)
        
        # 同時保存 Markdown 版本
        md_filepath = filepath.replace('.json', '.md')
        md_content = self._format_for_feishu(scraped_data)
        
        with open(md_filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return filepath
    
    def _generate_summary(self, results: List[Dict]) -> Dict:
        """生成汇总報告"""
        total = len(results)
        success = sum(1 for r in results if r.get('success'))
        failed = total - success
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total": total,
            "success": success,
            "failed": failed,
            "success_rate": f"{success/total*100:.1f}%" if total > 0 else "0%",
            "results": results
        }
        
        return summary


# 命令行接口
if __name__ == "__main__":
    scraper = WebScraper()
    
    if len(sys.argv) < 2:
        print("使用方式：python3 web_scraper.py <命令> [參數]")
        print()
        print("命令:")
        print("  scrape <url>              抓取單個網頁")
        print("  batch <file>              批量抓取（文件包含 URL 列表）")
        print("  scheduled                 定時抓取模式（配合 cron）")
        print()
        print("示例:")
        print("  python3 web_scraper.py scrape https://example.com/article")
        print("  python3 web_scraper.py batch urls.txt")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "scrape" and len(sys.argv) > 1:
        url = sys.argv[2]
        result = scraper.scrape(url, save_to_feishu=True)
        print("\n" + "="*60)
        print("抓取結果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "batch" and len(sys.argv) > 2:
        file_path = sys.argv[2]
        
        with open(file_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"讀取到 {len(urls)} 個 URL")
        results = scraper.batch_scrape(urls, save_to_feishu=True)
        
        print(f"\n完成：成功 {sum(1 for r in results if r.get('success'))}/{len(results)}")
    
    elif command == "scheduled":
        # 定時抓取模式（從環境變量讀取 URL）
        urls_str = os.environ.get('SCRAPER_URLS', '')
        if not urls_str:
            print("❌ 請設置環境變量 SCRAPER_URLS（逗號分隔的 URL 列表）")
            sys.exit(1)
        
        urls = [u.strip() for u in urls_str.split(',')]
        print(f"定時抓取：{len(urls)} 個網頁")
        results = scraper.batch_scrape(urls, save_to_feishu=True)
    
    else:
        print(f"❌ 未知命令：{command}")
        sys.exit(1)

# ============================================================
# 作者：RedOpenClaw
# 完成日期：2026.04.02
# 版本：v1.0.0
# 功能：網頁抓取 + 飛書保存
# ============================================================
