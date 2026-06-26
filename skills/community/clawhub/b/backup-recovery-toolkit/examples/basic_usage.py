"""
备份恢复工具包 - 基础使用示例
Backup Recovery Toolkit - Basic Usage Examples
"""

import os
import sys
import tempfile
import shutil

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from backup_toolkit import FileBackup, IncrementalBackup, RestoreManager


def example_basic_backup():
    """
    示例1: 基础文件备份
    Example 1: Basic file backup
    """
    print("=" * 60)
    print("示例1: 基础文件备份 | Example 1: Basic File Backup")
    print("=" * 60)
    
    # 创建临时源目录 | Create temp source directory
    source_dir = tempfile.mkdtemp(prefix="backup_source_")
    
    # 创建一些测试文件 | Create some test files
    for i in range(5):
        with open(os.path.join(source_dir, f"file{i}.txt"), 'w') as f:
            f.write(f"This is test file {i}\n" * 100)
    
    # 创建子目录 | Create subdirectory
    subdir = os.path.join(source_dir, "subdir")
    os.makedirs(subdir)
    with open(os.path.join(subdir, "nested.txt"), 'w') as f:
        f.write("Nested file content\n" * 50)
    
    print(f"\n源目录 | Source: {source_dir}")
    
    # 创建备份 | Create backup
    dest_dir = tempfile.mkdtemp(prefix="backup_dest_")
    print(f"目标目录 | Destination: {dest_dir}")
    
    backup = FileBackup(
        source=source_dir,
        destination=dest_dir,
        compress=True
    )
    
    print("\n执行备份... | Running backup...")
    result = backup.run(name="test-backup")
    
    print(f"\n备份结果 | Backup Result:")
    print(f"  成功 | Success: {result['success']}")
    print(f"  文件数 | Files: {result['files_backed_up']}")
    print(f"  总大小 | Size: {result['total_size']} bytes")
    print(f"  备份路径 | Path: {result['backup_path']}")
    print(f"  时间戳 | Timestamp: {result['timestamp']}")
    
    # 清理 | Cleanup
    shutil.rmtree(source_dir)
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    
    return result


def example_incremental_backup():
    """
    示例2: 增量备份
    Example 2: Incremental backup
    """
    print("\n" + "=" * 60)
    print("示例2: 增量备份 | Example 2: Incremental Backup")
    print("=" * 60)
    
    # 创建源目录 | Create source
    source_dir = tempfile.mkdtemp(prefix="incr_source_")
    dest_dir = tempfile.mkdtemp(prefix="incr_dest_")
    
    # 创建初始文件 | Create initial files
    for i in range(3):
        with open(os.path.join(source_dir, f"file{i}.txt"), 'w') as f:
            f.write(f"Initial content {i}\n")
    
    print(f"\n源目录 | Source: {source_dir}")
    print(f"目标目录 | Destination: {dest_dir}")
    
    # 第一次完整备份 | First full backup
    print("\n1. 执行完整备份... | Full backup...")
    full_backup = FileBackup(source_dir, dest_dir, compress=True)
    full_result = full_backup.run(name="full-backup")
    print(f"   完整备份完成，文件数: {full_result['files_backed_up']}")
    
    # 添加新文件 | Add new files
    print("\n2. 添加新文件... | Adding new files...")
    with open(os.path.join(source_dir, "new_file.txt"), 'w') as f:
        f.write("New file content\n" * 100)
    
    # 修改一个文件 | Modify one file
    with open(os.path.join(source_dir, "file0.txt"), 'a') as f:
        f.write("Modified content\n")
    
    # 增量备份 | Incremental backup
    print("\n3. 执行增量备份... | Incremental backup...")
    incr_backup = IncrementalBackup(
        source=source_dir,
        destination=dest_dir,
        reference_backup=full_result['backup_path']
    )
    incr_result = incr_backup.run(name="incremental-backup")
    
    print(f"\n增量备份结果 | Incremental Result:")
    print(f"  成功 | Success: {incr_result['success']}")
    print(f"  新增/变更文件数 | Changed files: {incr_result['files_backed_up']}")
    print(f"  备份路径 | Path: {incr_result['backup_path']}")
    
    # 清理 | Cleanup
    shutil.rmtree(source_dir)
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    
    return incr_result


def example_restore():
    """
    示例3: 备份恢复
    Example 3: Restore from backup
    """
    print("\n" + "=" * 60)
    print("示例3: 备份恢复 | Example 3: Restore Backup")
    print("=" * 60)
    
    # 创建源目录和备份 | Create source and backup
    source_dir = tempfile.mkdtemp(prefix="restore_source_")
    dest_dir = tempfile.mkdtemp(prefix="backup_dest_")
    restore_dir = tempfile.mkdtemp(prefix="restore_dest_")
    
    # 创建测试文件 | Create test files
    for i in range(5):
        with open(os.path.join(source_dir, f"file{i}.txt"), 'w') as f:
            f.write(f"Test file content {i}\n" * 50)
    
    print(f"\n源目录 | Source: {source_dir}")
    
    # 创建备份 | Create backup
    backup = FileBackup(source_dir, dest_dir, compress=True)
    result = backup.run(name="restore-test")
    
    print(f"备份路径 | Backup: {result['backup_path']}")
    print(f"\n执行恢复... | Restoring...")
    
    # 执行恢复 | Restore
    restore_result = RestoreManager.restore_file_backup(
        result['backup_path'],
        restore_dir
    )
    
    print(f"\n恢复结果 | Restore Result:")
    print(f"  成功 | Success: {restore_result['success']}")
    print(f"  恢复文件数 | Files restored: {restore_result['files_restored']}")
    print(f"  恢复路径 | Restore path: {restore_dir}")
    
    # 验证恢复的文件 | Verify restored files
    restored_files = os.listdir(restore_dir)
    print(f"\n验证恢复的文件 | Verified files: {len(restored_files)}")
    for f in restored_files:
        print(f"  - {f}")
    
    # 清理 | Cleanup
    for d in [source_dir, dest_dir, restore_dir]:
        if os.path.exists(d):
            shutil.rmtree(d)
    
    return restore_result


def example_directory_stats():
    """
    示例4: 目录统计信息
    Example 4: Directory statistics
    """
    print("\n" + "=" * 60)
    print("示例4: 目录统计 | Example 4: Directory Statistics")
    print("=" * 60)
    
    source_dir = tempfile.mkdtemp(prefix="stats_source_")
    
    # 创建不同大小的文件 | Create files of different sizes
    sizes = [1024, 10240, 102400]  # 1KB, 10KB, 100KB
    
    for i, size in enumerate(sizes):
        with open(os.path.join(source_dir, f"file_{size}bytes.txt"), 'w') as f:
            f.write("x" * size)
    
    # 统计信息 | Statistics
    total_size = 0
    file_count = 0
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            total_size += file_size
            file_count += 1
            print(f"  {file}: {file_size} bytes")
    
    print(f"\n统计 | Statistics:")
    print(f"  文件总数 | Total files: {file_count}")
    print(f"  总大小 | Total size: {total_size} bytes ({total_size / 1024:.2f} KB)")
    
    # 清理 | Cleanup
    shutil.rmtree(source_dir)


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("备份恢复工具包 - 完整示例")
    print("Backup Recovery Toolkit - Complete Examples")
    print("=" * 60)
    
    try:
        example_basic_backup()
        example_incremental_backup()
        example_restore()
        example_directory_stats()
        
        print("\n" + "=" * 60)
        print("所有示例运行完成！| All examples completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n错误 | Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
