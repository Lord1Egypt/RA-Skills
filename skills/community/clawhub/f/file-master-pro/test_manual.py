#!/usr/bin/env python3
"""
手动测试脚本 - 验证文件管理大师核心功能
"""

import os
import tempfile
import shutil
from pathlib import Path
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from file_master import FileMaster

def test_rename_function():
    """测试重命名功能"""
    print("测试1: 批量重命名功能")
    print("-" * 40)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建测试文件
        test_files = ["a.txt", "b.txt", "c.txt", "d.txt"]
        for filename in test_files:
            file_path = Path(tmpdir) / filename
            file_path.write_text(f"Content of {filename}")
        
        print(f"创建测试目录: {tmpdir}")
        print(f"创建文件: {test_files}")
        
        # 测试重命名
        fm = FileMaster()
        result = fm.rename_files(tmpdir, "file_{num:03d}.txt")
        
        print(f"重命名结果:")
        print(f"  总文件数: {result['total']}")
        print(f"  成功重命名: {result['renamed']}")
        print(f"  失败数: {result['failed']}")
        
        # 检查重命名后的文件
        renamed_files = list(Path(tmpdir).glob("*.txt"))
        print(f"重命名后文件: {[f.name for f in renamed_files]}")
        
        if result['renamed'] == 4 and result['failed'] == 0:
            print("[PASS] 重命名测试通过")
            return True
        else:
            print("[FAIL] 重命名测试失败")
            return False

def test_organize_function():
    """测试整理功能"""
    print("\n测试2: 文件整理功能")
    print("-" * 40)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建不同类型文件
        test_files = [
            "photo1.jpg",
            "photo2.png", 
            "document1.pdf",
            "document2.docx",
            "music1.mp3",
            "video1.mp4"
        ]
        
        for filename in test_files:
            file_path = Path(tmpdir) / filename
            file_path.write_text(f"Test {filename}")
        
        print(f"创建测试目录: {tmpdir}")
        print(f"创建文件: {test_files}")
        
        # 测试整理
        fm = FileMaster()
        result = fm.organize_by_type(tmpdir)
        
        print(f"整理结果:")
        print(f"  总文件数: {result['total']}")
        print(f"  成功整理: {result['organized']}")
        print(f"  失败数: {result['failed']}")
        print(f"  创建文件夹: {result['folders_created']}")
        
        # 检查整理结果
        for folder in ['images', 'documents', 'audio', 'video', 'others']:
            folder_path = Path(tmpdir) / folder
            if folder_path.exists():
                files = list(folder_path.glob("*"))
                print(f"  {folder}: {len(files)} 个文件")
        
        if result['organized'] >= 4 and result['failed'] == 0:
            print("[PASS] 整理测试通过")
            return True
        else:
            print("[FAIL] 整理测试失败")
            return False

def test_search_function():
    """测试搜索功能"""
    print("\n测试3: 文件搜索功能")
    print("-" * 40)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建测试文件
        test_files = {
            "todo.txt": "TODO: Finish the project",
            "notes.txt": "Important notes here",
            "readme.txt": "README file content",
            "data.json": '{"key": "value"}'
        }
        
        for filename, content in test_files.items():
            file_path = Path(tmpdir) / filename
            file_path.write_text(content)
        
        print(f"创建测试目录: {tmpdir}")
        
        # 测试搜索
        fm = FileMaster()
        result = fm.search_files(tmpdir, "TODO")
        
        print(f"搜索结果:")
        print(f"  搜索文件数: {result['total_searched']}")
        print(f"  找到文件数: {result['found']}")
        
        if result['found'] > 0:
            print(f"  找到的文件:")
            for file_info in result['files']:
                if file_info.get('content_match'):
                    print(f"    - {file_info['path']}")
        
        if result['found'] == 1:  # 应该只找到todo.txt
            print("[PASS] 搜索测试通过")
            return True
        else:
            print("[FAIL] 搜索测试失败")
            return False

def test_duplicate_find():
    """测试重复文件查找"""
    print("\n测试4: 重复文件查找功能")
    print("-" * 40)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建重复文件
        content1 = "This is duplicate content"
        content2 = "This is unique content"
        
        files = [
            ("dup1.txt", content1),
            ("dup2.txt", content1),  # 重复文件
            ("unique1.txt", content2),
            ("unique2.txt", "Another unique content")
        ]
        
        for filename, content in files:
            file_path = Path(tmpdir) / filename
            file_path.write_text(content)
        
        print(f"创建测试目录: {tmpdir}")
        print(f"创建4个文件（其中2个重复）")
        
        # 测试重复查找
        fm = FileMaster()
        result = fm.find_duplicates(tmpdir)
        
        print(f"重复查找结果:")
        print(f"  总文件数: {result['total_files']}")
        print(f"  重复组数: {result['duplicate_groups']}")
        print(f"  重复文件数: {result['duplicate_files']}")
        
        if result['duplicate_groups'] == 1 and result['duplicate_files'] == 2:
            print("[PASS] 重复查找测试通过")
            return True
        else:
            print("[FAIL] 重复查找测试失败")
            return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("文件管理大师 - 手动功能测试")
    print("=" * 60)
    
    tests = [
        ("重命名功能", test_rename_function),
        ("整理功能", test_organize_function),
        ("搜索功能", test_search_function),
        ("重复查找", test_duplicate_find)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"[ERROR] {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = 0
    for test_name, success in results:
        status = "通过" if success else "失败"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n总计: {passed}/{len(tests)} 个测试通过")
    
    if passed == len(tests):
        print("\n[SUCCESS] 所有测试通过！文件管理大师功能正常。")
        return True
    else:
        print(f"\n[WARNING]  {len(tests) - passed} 个测试失败，需要检查。")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n测试异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)