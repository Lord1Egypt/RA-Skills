"""
批量下载图片/视频到本地目录
用法: python batch-download.py "目标目录" "URL1|文件名1" "URL2|文件名2" ...
"""
import os
import sys
import urllib.request
from pathlib import Path

def download_file(url: str, dest_path: Path, timeout: int = 30) -> bool:
    """下载单个文件"""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read()
            dest_path.write_bytes(data)
            size = len(data) / (1024 * 1024)
            print(f"[OK] {dest_path.name} ({size:.1f}MB)")
            return True
    except Exception as e:
        print(f"[FAIL] {url} -> {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("用法: python batch-download.py \"目标目录\" \"URL|文件名\" ...")
        sys.exit(1)
    
    dest_dir = Path(sys.argv[1])
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    for item in sys.argv[2:]:
        if '|' in item:
            url, filename = item.split('|', 1)
        else:
            url = item
            filename = url.split('/')[-1].split('?')[0]
        
        if not filename:
            print(f"[SKIP] 无法从URL提取文件名: {url}")
            continue
        
        dest_path = dest_dir / filename
        ok = download_file(url.strip(), dest_path)
        results.append((url, ok))
    
    total = len(results)
    ok_count = sum(1 for _, ok in results if ok)
    print(f"\n完成: {ok_count}/{total} 成功")

if __name__ == "__main__":
    main()
