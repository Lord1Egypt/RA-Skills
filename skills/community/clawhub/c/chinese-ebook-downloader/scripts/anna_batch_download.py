#!/usr/bin/env python3
"""Download books from Anna's Archive using the existing search_source_c.py infrastructure."""
import sys, os, json, subprocess, time, glob, shutil

BOOKS = [
    {"title": "你是你吃出来的2", "alt_titles": ["你是你吃出来的 / 2", "你是你吃出来的2：家常便饭里的营养秘密"], "author": "夏萌"},
    {"title": "生命密码", "alt_titles": ["生命密码（套装共2册）"], "author": "尹烨"},
    {"title": "吃出自愈力", "alt_titles": [], "author": "威廉·李"},
    {"title": "谷物大脑", "alt_titles": [], "author": "戴维·珀尔马特"},
    {"title": "不老时代", "alt_titles": ["不老时代：年轻又长寿的科学和方法"], "author": "迈克尔·罗伊森"},
    {"title": "疗愈的饮食与断食", "alt_titles": ["疗愈的饮食与断食：新时代的个人营养学"], "author": "杨定一"},
    {"title": "菌群大脑", "alt_titles": [], "author": "克里斯廷·洛伯格"},
    {"title": "疯狂的尿酸", "alt_titles": ["疯狂的尿酸：不止是痛风"], "author": "戴维·珀尔马特"},
    {"title": "逆龄饮食", "alt_titles": ["逆龄饮食：逆转慢性疾病与衰老的再生医学新成果"], "author": "安德烈亚斯·乔普"},
]

OUTPUT_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Documents/Books/微信读书/医学&健康/")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON = "/opt/homebrew/Caskroom/miniforge/base/envs/env9/bin/python"

def search_and_download(book, output_dir):
    """Try each title variant until we find a PDF."""
    titles = [book["title"]] + book.get("alt_titles", [])
    for title in titles:
        query = f"{title} {book['author']}"
        print(f"\n🔍 Trying: {query}")
        
        tmp_dir = f"/tmp/ebook_dl_{int(time.time())}"
        os.makedirs(tmp_dir, exist_ok=True)
        
        try:
            result = subprocess.run(
                [PYTHON, f"{SCRIPT_DIR}/search_source_c.py", title, book["author"], tmp_dir],
                capture_output=True, text=True, timeout=120
            )
            
            output = result.stdout + result.stderr
            
            # Check if any PDF was downloaded
            pdfs = glob.glob(os.path.join(tmp_dir, "*.pdf"))
            if pdfs:
                for pdf in pdfs:
                    size = os.path.getsize(pdf)
                    if size > 1000:  # Not a fake/error page
                        # Move to output dir
                        dest = os.path.join(output_dir, os.path.basename(pdf))
                        if os.path.exists(dest):
                            os.remove(dest)
                        shutil.move(pdf, dest)
                        print(f"  ✅ Downloaded: {os.path.basename(dest)} ({size/1024/1024:.1f} MB)")
                        shutil.rmtree(tmp_dir)
                        return True
                    else:
                        print(f"  ⚠️ Fake PDF ({size}B), skipping")
            
            # Also check epub for conversion
            epubs = glob.glob(os.path.join(tmp_dir, "*.epub"))
            if epubs:
                for epub in epubs:
                    size = os.path.getsize(epub)
                    if size > 1000:
                        dest = os.path.join(output_dir, os.path.basename(epub))
                        if os.path.exists(dest):
                            os.remove(dest)
                        shutil.move(epub, dest)
                        print(f"  📥 Got EPUB: {os.path.basename(dest)} ({size/1024/1024:.1f} MB) - will convert to PDF")
                        shutil.rmtree(tmp_dir)
                        return True
            
            print(f"  ❌ No valid download found")
            shutil.rmtree(tmp_dir)
            
        except subprocess.TimeoutExpired:
            print(f"  ⏱️ Timeout")
            shutil.rmtree(tmp_dir, ignore_errors=True)
        except Exception as e:
            print(f"  💥 Error: {e}")
            shutil.rmtree(tmp_dir, ignore_errors=True)
        
        time.sleep(3)  # Rate limiting
    
    return False

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    done = 0
    failed = 0
    
    for i, book in enumerate(BOOKS, 1):
        # Skip if already downloaded as PDF
        existing = glob.glob(os.path.join(OUTPUT_DIR, f"*{book['title']}*.pdf"))
        if existing:
            print(f"\n⏭️ [{i}/{len(BOOKS)}] {book['title']} - already exists, skipping")
            done += 1
            continue
        
        print(f"\n{'='*60}")
        print(f"📚 [{i}/{len(BOOKS)}] {book['title']} - {book['author']}")
        print(f"{'='*60}")
        
        if search_and_download(book, OUTPUT_DIR):
            done += 1
        else:
            failed += 1
        
        time.sleep(5)
    
    print(f"\n{'='*60}")
    print(f"📊 Results: {done} done, {failed} failed out of {len(BOOKS)}")
    print(f"{'='*60}")
