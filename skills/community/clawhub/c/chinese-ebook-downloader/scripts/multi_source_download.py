#!/usr/bin/env python3
"""Multi-source download with fallback: Source A -> Source B -> Source C (Anna's) -> epub->pdf"""
import sys, os, asyncio, json, time, glob, shutil, subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
PYTHON = "/opt/homebrew/Caskroom/miniforge/base/envs/env9/bin/python"

BOOKS = [
    {"title": "菌群大脑", "author": "克里斯廷·洛伯格", "search": "菌群大脑 克里斯廷·洛伯格"},
    {"title": "疯狂的尿酸", "author": "戴维·珀尔马特", "search": "疯狂的尿酸 痛风 戴维·珀尔马特"},
    {"title": "逆龄饮食", "author": "安德烈亚斯·乔普", "search": "逆龄饮食 再生医学 乔普"},
]

OUTPUT_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Documents/Books/微信读书/医学&健康/")


def run_source_a(title, author, output_dir):
    """Source A: dushupai.com (primary, ZIP with PDF inside)"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("download_book", f"{SCRIPT_DIR}/download_book.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    async def _dl():
        try:
            result = await mod.download_book(title=title, author=author, output_dir=output_dir, headless=True)
            return result
        except Exception as e:
            print(f"  Source A error: {e}")
            return None
    
    return asyncio.run(_dl())


def run_source_b(title, author, output_dir):
    """Source B: yabook.org -> file host download"""
    from search_secondary_source import search_yabook, decrypt_ctfile, get_download_url
    
    async def _dl():
        try:
            results = await search_yabook(title, author, headless=True)
            if not results:
                print("  Source B: no results")
                return None
            
            # Try first result
            r = results[0]
            print(f"  Source B found: {r.get('title', '?')}")
            
            # Get download link from file host
            if not r.get('file_host_url'):
                print("  Source B: no file host URL")
                return None
            
            # Download via curl
            url = r['file_host_url']
            pwd = r.get('password', '')
            out_path = os.path.join(output_dir, f"{title} - {author}.pdf")
            
            # Try direct curl first
            cmd = ["curl", "-L", "-o", out_path, "--max-time", "300", url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=310)
            if os.path.exists(out_path) and os.path.getsize(out_path) > 5000:
                return out_path
            
            # If password-protected, need browser decrypt
            print(f"  Source B: direct download failed, trying browser decrypt...")
            dl_url = await get_download_url(r['file_host_url'], pwd, headless=True)
            if dl_url:
                cmd = ["curl", "-L", "-o", out_path, "--max-time", "600", dl_url]
                subprocess.run(cmd, capture_output=True, text=True, timeout=610)
                if os.path.exists(out_path) and os.path.getsize(out_path) > 5000:
                    return out_path
            
            return None
        except Exception as e:
            print(f"  Source B error: {e}")
            return None
    
    return asyncio.run(_dl())


def run_source_c(title, author, output_dir):
    """Source C: Anna's Archive"""
    from search_source_c import download_book_from_annas_archive
    
    async def _dl():
        try:
            result = await download_book_from_annas_archive(title, author, output_dir=output_dir, headless=True)
            if result and result.get('status') == 'done' and result.get('files'):
                for f in result['files']:
                    if os.path.exists(f) and os.path.getsize(f) > 5000:
                        return f
            print("  Source C: no valid download")
            return None
        except Exception as e:
            print(f"  Source C error: {e}")
            return None
    
    return asyncio.run(_dl())


def convert_epub_to_pdf(epub_path, output_dir):
    """Convert epub to PDF using weasyprint"""
    pdf_path = epub_path.rsplit('.', 1)[0] + '.pdf'
    try:
        cmd = [PYTHON, f"{SCRIPT_DIR}/epub_to_pdf.py", epub_path, pdf_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 5000:
            return pdf_path
    except Exception as e:
        print(f"  Convert error: {e}")
    return None


def download_book_all_sources(book, output_dir):
    """Try all sources in order, fallback to epub->pdf conversion"""
    title, author = book["title"], book["author"]
    
    # Check if PDF already exists
    existing = glob.glob(os.path.join(output_dir, f"*{title}*.pdf"))
    for e in existing:
        if os.path.getsize(e) > 1000:
            print(f"  ⏭️ {title} already exists: {os.path.basename(e)}")
            return True
    
    sources = [
        ("Source A (dushupai)", lambda: run_source_a(title, author, output_dir)),
        ("Source B (yabook)", lambda: run_source_b(title, author, output_dir)),
        ("Source C (Anna's)", lambda: run_source_c(title, author, output_dir)),
    ]
    
    last_epub = None
    
    for src_name, src_fn in sources:
        print(f"\n  🔄 Trying {src_name}...")
        try:
            result = src_fn()
        except Exception as e:
            print(f"  ❌ {src_name} crashed: {e}")
            result = None
            continue
        
        if result:
            if isinstance(result, list):
                for f in result:
                    if os.path.exists(f):
                        size = os.path.getsize(f)
                        if size > 5000:
                            ext = os.path.splitext(f)[1].lower()
                            if ext == '.pdf':
                                print(f"  ✅ {src_name} → PDF: {os.path.basename(f)} ({size/1024/1024:.1f} MB)")
                                return True
                            elif ext == '.epub':
                                last_epub = f
                                print(f"  📥 {src_name} → EPUB: {os.path.basename(f)} ({size/1024/1024:.1f} MB)")
                            elif ext == '.zip':
                                # Source A returns ZIP, extract and check for PDF
                                print(f"  📦 {src_name} → ZIP: {os.path.basename(f)} ({size/1024/1024:.1f} MB)")
                                # Extract
                                extract_dir = f"/tmp/ebook_extract_{int(time.time())}"
                                os.makedirs(extract_dir, exist_ok=True)
                                try:
                                    subprocess.run(["unzip", "-o", "-d", extract_dir, f], capture_output=True, timeout=60)
                                    pdfs = glob.glob(os.path.join(extract_dir, "**/*.pdf"), recursive=True)
                                    for pdf in pdfs:
                                        if os.path.getsize(pdf) > 5000:
                                            dest = os.path.join(output_dir, f"{title} - {author}.pdf")
                                            if os.path.exists(dest):
                                                os.remove(dest)
                                            shutil.copy2(pdf, dest)
                                            print(f"  ✅ Extracted PDF: {os.path.basename(pdf)} ({os.path.getsize(pdf)/1024/1024:.1f} MB)")
                                            shutil.rmtree(extract_dir)
                                            return True
                                    # Check for epub inside zip
                                    epubs = glob.glob(os.path.join(extract_dir, "**/*.epub"), recursive=True)
                                    for epub in epubs:
                                        if os.path.getsize(epub) > 5000:
                                            last_epub = epub
                                            print(f"  📥 Found EPUB in ZIP")
                                    shutil.rmtree(extract_dir)
                                except Exception as e:
                                    print(f"  ❌ Extract failed: {e}")
                                    shutil.rmtree(extract_dir, ignore_errors=True)
            elif isinstance(result, str) and os.path.exists(result):
                size = os.path.getsize(result)
                if size > 5000:
                    ext = os.path.splitext(result)[1].lower()
                    if ext == '.pdf':
                        print(f"  ✅ {src_name} → PDF ({size/1024/1024:.1f} MB)")
                        return True
                    elif ext == '.epub':
                        last_epub = result
                        print(f"  📥 {src_name} → EPUB ({size/1024/1024:.1f} MB)")
        time.sleep(3)
    
    # Fallback: convert epub to pdf
    if last_epub:
        print(f"\n  🔄 Converting EPUB → PDF with weasyprint...")
        pdf = convert_epub_to_pdf(last_epub, output_dir)
        if pdf:
            print(f"  ✅ Converted: {os.path.basename(pdf)} ({os.path.getsize(pdf)/1024/1024:.1f} MB)")
            return True
    
    return False


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    done, failed = 0, 0
    
    for i, book in enumerate(BOOKS, 1):
        print(f"\n{'='*60}")
        print(f"📚 [{i}/{len(BOOKS)}] {book['title']} - {book['author']}")
        print(f"{'='*60}")
        
        if download_book_all_sources(book, OUTPUT_DIR):
            done += 1
        else:
            failed += 1
        
        time.sleep(5)
    
    print(f"\n{'='*60}")
    print(f"📊 Results: {done} done, {failed} failed")
    print(f"{'='*60}")
