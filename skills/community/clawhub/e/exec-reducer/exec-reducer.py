#!/usr/bin/env python3
"""
exec-reducer skill - 封装常用操作为Python脚本，减少exec调用
"""
import sys
import os
import json

def main():
    if len(sys.argv) < 2:
        print("Usage: python exec-reducer.py <command> [args]")
        print("Commands:")
        print("  read <file> - 读取文件")
        print("  write <file> <content> - 写入文件")
        print("  append <file> <content> - 追加写入")
        print("  list <dir> - 列出目录")
        print("  search <path> <pattern> - 搜索文件")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "read" and len(sys.argv) > 2:
        with open(sys.argv[2], 'r', encoding='utf-8') as f:
            print(f.read())
    elif cmd == "write" and len(sys.argv) > 3:
        with open(sys.argv[2], 'w', encoding='utf-8') as f:
            f.write(sys.argv[3])
    elif cmd == "list" and len(sys.argv) > 2:
        for item in os.listdir(sys.argv[2]):
            print(item)
    elif cmd == "search" and len(sys.argv) > 3:
        import glob
        for f in glob.glob(sys.argv[2] + "/**/" + sys.argv[3], recursive=True):
            print(f)
    else:
        print("Unknown command or missing args")

if __name__ == "__main__":
    main()
