#!/usr/bin/env python3
"""
SQLite3 版本修复启动器

在导入 chromadb 之前，先用 pysqlite3-binary 替换系统 sqlite3
"""

import sys

# 1. 在导入任何模块之前，先修补 sqlite3
try:
    import pysqlite3.dbapi2 as pysqlite3_dbapi2
    sys.modules['sqlite3'] = pysqlite3_dbapi2
    print(f"✅ 已修补 sqlite3 -> pysqlite3-binary (SQLite3 {pysqlite3_dbapi2.sqlite_version})", file=sys.stderr)
except ImportError:
    print("⚠️  未找到 pysqlite3-binary，使用系统 sqlite3", file=sys.stderr)

# 2. 现在可以安全导入 chromadb
import chromadb

print(f"✅ ChromaDB {chromadb.__version__} 初始化成功", file=sys.stderr)

# 3. 运行主脚本
if __name__ == '__main__':
    import os
    import runpy
    script_dir = os.path.dirname(os.path.abspath(__file__))
    build_script = os.path.join(script_dir, 'build_corpus.py')
    runpy.run_path(build_script, run_name='__main__')
