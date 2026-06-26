#!/usr/bin/env python3
import os
import sys
import json

print("=== 环境检查 ===")

# 1. 检查环境变量
print("\n1. 检查环境变量:")
important_vars = ['BAIDU_AK', 'BAIDU_API_KEY', 'BAIDU_SEARCH_KEY', 'PATH']
for key in important_vars:
    val = os.environ.get(key)
    if val:
        if 'KEY' in key or 'AK' in key:
            # 隐藏API密钥
            masked = f"****{val[-4:] if len(val)>4 else '****'}"
            print(f"  {key}: {masked}")
        else:
            if len(val) > 80:
                print(f"  {key}: {val[:80]}...")
            else:
                print(f"  {key}: {val}")
    else:
        print(f"  {key}: 未设置")

# 2. 检查是否有百度搜索技能
print("\n2. 检查百度搜索技能:")
baidu_skill_path = r"C:\Users\duyun\.openclaw\workspace\skills\baidu-search"
if os.path.exists(baidu_skill_path):
    print(f"  百度搜索技能路径存在: {baidu_skill_path}")
    files = os.listdir(baidu_skill_path)
    print(f"  文件列表: {', '.join(files[:5])}{'...' if len(files) > 5 else ''}")
else:
    print(f"  百度搜索技能路径不存在于: {baidu_skill_path}")

# 3. 搜索百度AK
print("\n3. 搜索百度AK配置:")
search_paths = [
    r"C:\Users\duyun\.openclaw\workspace\TOOLS.md",
    r"C:\Users\duyun\.openclaw\workspace\MEMORY.md",
    r"C:\Users\duyun\.openclaw\workspace\.env",
    r"C:\Users\duyun\.openclaw\.env"
]

for path in search_paths:
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'BAIDU' in content.upper() or '百度' in content:
                print(f"  在 {path} 中找到百度相关配置")
                # 提取相关行
                lines = content.split('\n')
                baidu_lines = [line for line in lines if 'BAIDU' in line.upper() or '百度' in line]
                for line in baidu_lines[:3]:
                    print(f"    - {line[:80]}{'...' if len(line)>80 else ''}")

# 4. 检查工作目录和权限
print("\n4. 系统信息:")
print(f"  当前目录: {os.getcwd()}")
print(f"  Python版本: {sys.version}")
print(f"  平台: {sys.platform}")