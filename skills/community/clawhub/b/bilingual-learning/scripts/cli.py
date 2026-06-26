#!/usr/bin/env python3
"""
词库管理 CLI 工具
支持: add, delete, exchange, list, clear 模式
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from core import NewWordLibrary, KnownWordLibrary, transfer_word

def usage():
    print("""用法:
  python cli.py <模式> [参数]

模式:
  add <word> [pos] [field] [book]   - 添加单词到生词库
  delete <word> [-n|-k]             - 从生词库(-n)或熟词库(-k)删除
  exchange <word> [-n|-k]           - 单词在生熟词库间传递
  list [-n|-k]                       - 列出词库内容
  clear [-n|-k]                      - 清空词库

示例:
  python cli.py add apple n. fruit default
  python cli.py delete apple -n
  python cli.py exchange apple -n -k
""")

if len(sys.argv) < 2:
    usage()
    sys.exit(1)

cmd = sys.argv[1].lower()

if cmd == "add":
    if len(sys.argv) < 3:
        print("错误: 请提供单词")
        sys.exit(1)
    word = sys.argv[2]
    pos = sys.argv[3] if len(sys.argv) > 3 else ""
    field = sys.argv[4] if len(sys.argv) > 4 else ""
    book = sys.argv[5] if len(sys.argv) > 5 else "default"
    
    lib = NewWordLibrary()
    if lib.add(word, pos, field, book):
        print(f"✓ 单词 '{word}' 已添加到生词库")
    else:
        print(f"✗ 单词 '{word}' 已存在")

elif cmd == "delete":
    if len(sys.argv) < 3:
        print("错误: 请提供单词")
        sys.exit(1)
    word = sys.argv[2]
    target = sys.argv[3] if len(sys.argv) > 3 else "-n"
    
    lib = NewWordLibrary() if target == "-n" else KnownWordLibrary()
    if lib.delete(word):
        print(f"✓ 单词 '{word}' 已删除")
    else:
        print(f"✗ 单词 '{word}' 不存在")

elif cmd == "exchange":
    if len(sys.argv) < 4:
        print("错误: 请提供单词和源/目标库")
        sys.exit(1)
    word = sys.argv[2]
    from_lib = "new" if sys.argv[3] == "-n" else "known"
    to_lib = "known" if from_lib == "new" else "new"
    
    success, msg = transfer_word(word, from_lib, to_lib)
    print(f"{'✓' if success else '✗'} {msg}")

elif cmd == "list":
    target = sys.argv[2] if len(sys.argv) > 2 else "-n"
    lib = NewWordLibrary() if target == "-n" else KnownWordLibrary()
    words = lib.list_all()
    
    if not words:
        print(f"{'生词库' if target == '-n' else '熟词库'} 为空")
    else:
        print(f"\n{'='*50}")
        print(f"{'生词库' if target == '-n' else '熟词库'} (共{len(words)}个)")
        print(f"{'='*50}")
        for w in words:
            print(f"[{w['id']}] {w['name']} ({w['pos']}) | 领域:{w['field']} | 词书:{w['book']} | 入库:{w['added_time']}")

elif cmd == "clear":
    target = sys.argv[2] if len(sys.argv) > 2 else "-n"
    lib = NewWordLibrary() if target == "-n" else KnownWordLibrary()
    lib.clear()
    print(f"{'生词库' if target == '-n' else '熟词库'} 已清空")

else:
    usage()
