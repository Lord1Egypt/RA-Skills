#!/usr/bin/env python3
"""Batch download from Anna's Archive using async download_book_from_annas_archive."""
import sys, os, asyncio, time, glob, shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from search_source_c import download_book_from_annas_archive

BOOKS = [
    {"title": "生命密码（套装共2册）", "author": "尹烨", "search": "生命密码 尹烨"},
    {"title": "吃出自愈力", "author": "[美]威廉·李", "search": "吃出自愈力 威廉·李"},
    {"title": "谷物大脑", "author": "戴维·珀尔马特 克里斯廷·洛伯格", "search": "谷物大脑 戴维·珀尔马特"},
    {"title": "不老时代", "author": "迈克尔·罗伊森", "search": "不老时代 年轻 长寿 罗伊森"},
    {"title": "疗愈的饮食与断食", "author": "杨定一", "search": "疗愈的饮食与断食 杨定一"},
    {"title": "菌群大脑", "author": "克里斯廷·洛伯格", "search": "菌群大脑 克里斯廷·洛伯格"},
    {"title": "疯狂的尿酸", "author": "戴维·珀尔马特", "search": "疯狂的尿酸 痛风 戴维·珀尔马特"},
    {"title": "逆龄饮食", "author": "安德烈亚斯·乔普", "search": "逆龄饮食 再生医学 乔普"},
]

OUTPUT_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Documents/Books/微信读书/医学&健康/")

async def download_one(book, output_dir):
    """Download a single book, return True if successful."""
    parts = book["search"].split()
    title = parts[0] if len(parts) == 1 else " ".join(parts[:-1])
    author = parts[-1]
    
    print(f"  🔍 Searching: {title} - {author}")
    
    result = await download_book_from_annas_archive(
        title, author, output_dir=output_dir, headless=True
    )
    
    if result and result.get("status") == "done" and result.get("files"):
        for f in result["files"]:
            if os.path.exists(f):
                size = os.path.getsize(f)
                if size > 1000:
                    ext = os.path.splitext(f)[1].lower()
                    if ext != ".pdf":
                        print(f"  📥 Got {ext.upper()}: {os.path.basename(f)} ({size/1024/1024:.1f} MB) - needs PDF conversion")
                    else:
                        print(f"  ✅ PDF: {os.path.basename(f)} ({size/1024/1024:.1f} MB)")
                    return True
                else:
                    print(f"  ⚠️ Fake file ({size}B), removing")
                    os.remove(f)
    
    print(f"  ❌ Failed: {book['title']}")
    return False

async def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    done, failed, skipped = 0, 0, 0
    
    for i, book in enumerate(BOOKS, 1):
        # Check if already exists
        existing_pdf = glob.glob(os.path.join(OUTPUT_DIR, f"*{book['title']}*.pdf"))
        existing_epub = glob.glob(os.path.join(OUTPUT_DIR, f"*{book['title']}*.epub"))
        if existing_pdf:
            print(f"\n⏭️ [{i}/{len(BOOKS)}] {book['title']} - PDF already exists")
            skipped += 1
            continue
        
        print(f"\n{'='*60}")
        print(f"📚 [{i}/{len(BOOKS)}] {book['title']}")
        print(f"{'='*60}")
        
        if await download_one(book, OUTPUT_DIR):
            done += 1
        else:
            failed += 1
        
        time.sleep(3)
    
    print(f"\n{'='*60}")
    print(f"📊 Results: {done} done, {failed} failed, {skipped} skipped (total {len(BOOKS)})")
    print(f"{'='*60}")

if __name__ == "__main__":
    asyncio.run(main())
