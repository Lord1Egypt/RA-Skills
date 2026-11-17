#!/usr/bin/env python3
"""
ISBN 條碼圖片辨識腳本
使用 isbnlib 從圖片萃取 ISBN 數字
"""

import sys
import argparse

try:
    import isbnlib
    from PIL import Image
except ImportError as e:
    print(f"依賴缺失：{e}", file=sys.stderr)
    print("請先安裝：pip3 install isbnlib Pillow", file=sys.stderr)
    sys.exit(1)


def scan_isbn(image_path: str) -> str | None:
    """從圖片檔案路徑辨識 ISBN"""
    try:
        # 嘗試元數據法（不需 OCR，直接從圖片 EXIF 讀取）
        isbn = isbnlib.from_image(image_path)
        if isbn:
            return isbn
    except Exception as e:
        print(f"[isbnlib] 失敗: {e}", file=sys.stderr)

    # fallback: 使用 cover-header 方式
    try:
        isbn = isbnlib.canonical(isbnlib.get_isbnlike(image_path))
        if isbn:
            return isbn
    except Exception:
        pass

    return None


def main():
    parser = argparse.ArgumentParser(description="ISBN 條碼圖片辨識")
    parser.add_argument("--image", "-i", required=True, help="條碼圖片檔案路徑")
    parser.add_argument("--show", action="store_true", help="顯示圖片預覽（需 GUI 環境）")
    args = parser.parse_args()

    # 檢查檔案是否存在
    try:
        img = Image.open(args.image)
        if args.show:
            img.show()
    except FileNotFoundError:
        print(f"找不到圖片：{args.image}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"無法開啟圖片：{e}", file=sys.stderr)
        sys.exit(1)

    isbn = scan_isbn(args.image)

    if isbn:
        print(f"✅ 掃描成功！ISBN：{isbn}")
        # 自動觸發 lookup
        import subprocess, json
        result = subprocess.run(
            ["python3", __file__.replace("isbn_scan.py", "isbn_lookup.py"), "--isbn", isbn],
            capture_output=True, text=True,
            cwd=__file__.rsplit("/", 1)[0]
        )
        if result.returncode == 0:
            try:
                book_data = json.loads(result.stdout)
                print(f"\n📖 找到書籍：")
                print(f"   書名：{book_data.get('title', 'N/A')}")
                print(f"   作者：{', '.join(book_data.get('authors', book_data.get('title', '').split()))}")
                print(f"   來源：{book_data.get('source', 'N/A')}")
            except Exception:
                print(result.stdout)
        sys.exit(0)
    else:
        print("❌ 無法從圖片識別 ISBN，請嘗試：")
        print("  1. 確保圖片清晰、ISBN 條碼完整")
        print("  2. 或直接提供 ISBN：python3 scripts/isbn_lookup.py --isbn 978xxxx")
        sys.exit(1)


if __name__ == "__main__":
    main()
