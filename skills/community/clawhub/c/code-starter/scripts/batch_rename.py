#!/usr/bin/env python3
"""
文件重命名工具
适合教学 - 展示文件操作和自动化
"""

import os
import sys

def batch_rename(folder_path, prefix="", suffix=""):
    """
    批量重命名文件夹中的所有文件
    
    参数：
        folder_path: 文件夹路径
        prefix: 添加到文件名前面的文字
        suffix: 添加到文件名后面的文字（扩展名之前）
    """
    
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"错误：找不到文件夹 {folder_path}")
        return
    
    # 获取所有文件
    files = os.listdir(folder_path)
    
    print(f"在 {folder_path} 中找到 {len(files)} 个文件")
    print()
    
    # 预览重命名
    print("重命名预览：")
    print("-" * 50)
    
    rename_list = []
    for filename in files:
        # 跳过文件夹
        if os.path.isdir(os.path.join(folder_path, filename)):
            continue
        
        # 分离文件名和扩展名
        name, ext = os.path.splitext(filename)
        
        # 新文件名
        new_name = f"{prefix}{name}{suffix}{ext}"
        
        print(f"{filename:30s} → {new_name}")
        rename_list.append((filename, new_name))
    
    print("-" * 50)
    print(f"共 {len(rename_list)} 个文件将被重命名")
    
    # 确认
    confirm = input("\n确认执行？(y/n): ")
    if confirm.lower() != 'y':
        print("已取消")
        return
    
    # 执行重命名
    success = 0
    for old_name, new_name in rename_list:
        try:
            old_path = os.path.join(folder_path, old_name)
            new_path = os.path.join(folder_path, new_name)
            os.rename(old_path, new_path)
            success += 1
        except Exception as e:
            print(f"重命名 {old_name} 失败: {e}")
    
    print(f"\n✅ 成功重命名 {success} 个文件")

def add_numbering(folder_path, start=1):
    """
    给文件添加序号
    
    参数：
        folder_path: 文件夹路径
        start: 起始序号
    """
    
    if not os.path.exists(folder_path):
        print(f"错误：找不到文件夹 {folder_path}")
        return
    
    files = [f for f in os.listdir(folder_path) 
             if os.path.isfile(os.path.join(folder_path, f))]
    
    print(f"找到 {len(files)} 个文件")
    print("\n重命名预览：")
    print("-" * 50)
    
    rename_list = []
    for i, filename in enumerate(files, start=start):
        name, ext = os.path.splitext(filename)
        new_name = f"{i:03d}_{name}{ext}"  # 三位数序号
        
        print(f"{filename:30s} → {new_name}")
        rename_list.append((filename, new_name))
    
    print("-" * 50)
    
    confirm = input("\n确认执行？(y/n): ")
    if confirm.lower() != 'y':
        print("已取消")
        return
    
    for old_name, new_name in rename_list:
        old_path = os.path.join(folder_path, old_name)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
    
    print(f"\n✅ 成功重命名 {len(rename_list)} 个文件")

if __name__ == "__main__":
    # 使用示例
    print("=" * 50)
    print("📁 文件批量重命名工具")
    print("=" * 50)
    print()
    print("功能：")
    print("1. 添加前缀/后缀")
    print("2. 添加序号")
    print()
    
    choice = input("选择功能 (1/2): ")
    folder = input("输入文件夹路径: ")
    
    if choice == "1":
        prefix = input("前缀（直接回车跳过）: ")
        suffix = input("后缀（直接回车跳过）: ")
        batch_rename(folder, prefix, suffix)
    elif choice == "2":
        start = input("起始序号（默认1）: ")
        start = int(start) if start else 1
        add_numbering(folder, start)
    else:
        print("无效选择")
