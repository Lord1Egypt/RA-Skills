#!/usr/bin/env python3
"""
文件管理大师 - 安装脚本
"""

import os
import sys
import shutil
from pathlib import Path

def install_file_master():
    """安装文件管理大师"""
    print("=" * 60)
    print("📁 文件管理大师安装程序")
    print("=" * 60)
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        return False
    
    # 确定安装目录
    if os.name == 'nt':  # Windows
        install_dir = Path(os.environ.get('LOCALAPPDATA', '')) / 'FileMaster'
    else:  # macOS/Linux
        install_dir = Path.home() / '.local' / 'file-master'
    
    # 创建安装目录
    install_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制文件
    source_dir = Path(__file__).parent
    files_to_copy = [
        ('file_master.py', 'file_master.py'),
        ('config.example.yaml', 'config.yaml'),
        ('README.md', 'README.md')
    ]
    
    print(f"安装目录: {install_dir}")
    print("正在复制文件...")
    
    for src_name, dst_name in files_to_copy:
        src_path = source_dir / src_name
        dst_path = install_dir / dst_name
        
        if src_path.exists():
            shutil.copy2(src_path, dst_path)
            print(f"  ✅ {src_name} -> {dst_name}")
        else:
            print(f"  ⚠️  {src_name} 不存在，跳过")
    
    # 创建可执行文件
    if os.name == 'nt':  # Windows
        # 创建批处理文件
        bat_content = f'''@echo off
python "{install_dir}\\file_master.py" %*
'''
        bat_path = install_dir / 'file-master.bat'
        with open(bat_path, 'w', encoding='utf-8') as f:
            f.write(bat_content)
        
        # 添加到PATH（需要管理员权限）
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r'Environment', 
                                0, 
                                winreg.KEY_READ | winreg.KEY_WRITE)
            
            current_path, _ = winreg.QueryValueEx(key, 'Path')
            if str(install_dir) not in current_path:
                new_path = current_path + ';' + str(install_dir)
                winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)
                print("  ✅ 已添加到PATH（需要重启终端）")
            
            winreg.CloseKey(key)
        except Exception as e:
            print(f"  ⚠️ 无法自动添加到PATH: {e}")
            print(f"  请手动添加 {install_dir} 到PATH环境变量")
    
    else:  # macOS/Linux
        # 创建shell脚本
        script_content = f'''#!/bin/bash
python3 "{install_dir}/file_master.py" "$@"
'''
        script_path = install_dir / 'file-master'
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # 设置执行权限
        os.chmod(script_path, 0o755)
        
        # 创建符号链接到/usr/local/bin（需要sudo）
        try:
            bin_path = Path('/usr/local/bin/file-master')
            if bin_path.exists():
                bin_path.unlink()
            bin_path.symlink_to(script_path)
            print("  ✅ 已创建符号链接到 /usr/local/bin/file-master")
        except PermissionError:
            print("  ⚠️ 需要sudo权限创建符号链接")
            print(f"  请手动运行: sudo ln -s {script_path} /usr/local/bin/file-master")
    
    # 创建配置文件目录
    config_dir = Path.home() / '.file-master'
    config_dir.mkdir(exist_ok=True)
    
    # 复制示例配置
    example_config = source_dir / 'config.example.yaml'
    user_config = config_dir / 'config.yaml'
    
    if example_config.exists() and not user_config.exists():
        shutil.copy2(example_config, user_config)
        print(f"  ✅ 已创建配置文件: {user_config}")
    
    # 创建备份目录
    backup_dir = config_dir / 'backups'
    backup_dir.mkdir(exist_ok=True)
    
    print("\n" + "=" * 60)
    print("🎉 安装完成！")
    print("=" * 60)
    
    print("\n使用方法:")
    print("  1. 重命名文件:")
    print("     file-master rename \"D:\\photos\\\" --pattern \"vacation_{num:03d}.jpg\"")
    print("")
    print("  2. 按类型整理:")
    print("     file-master organize \"D:\\Downloads\\\" --recursive")
    print("")
    print("  3. 搜索文件:")
    print("     file-master search \"D:\\projects\\\" --content \"TODO:\"")
    print("")
    print("  4. 查找重复文件:")
    print("     file-master find-duplicates \"D:\\backup\\\"")
    print("")
    print("获取帮助:")
    print("  file-master --help")
    print("  file-master rename --help")
    print("")
    print("配置文件位置:")
    print(f"  {config_dir / 'config.yaml'}")
    print("")
    print("操作日志位置:")
    print(f"  {config_dir / 'operations.log'}")
    
    return True

def create_example_config():
    """创建示例配置文件"""
    config_content = '''# 文件管理大师配置文件

# 基本设置
confirm_deletion: true      # 删除前确认
backup_before_rename: true  # 重命名前备份
log_level: info             # 日志级别: debug, info, warning, error

# 默认路径
default_paths:
  downloads: "~/Downloads"
  documents: "~/Documents"
  pictures: "~/Pictures"
  music: "~/Music"
  videos: "~/Videos"

# 自动化规则
rules:
  auto_organize_downloads: false  # 自动整理下载文件夹
  clean_temp_files_daily: false   # 每日清理临时文件
  backup_important_folders: weekly # 重要文件夹备份频率

# 文件类型分类
file_types:
  images:
    - .jpg
    - .jpeg
    - .png
    - .gif
    - .bmp
    - .webp
  documents:
    - .pdf
    - .doc
    - .docx
    - .txt
    - .md
    - .rtf
  videos:
    - .mp4
    - .avi
    - .mov
    - .mkv
    - .wmv
  audio:
    - .mp3
    - .wav
    - .flac
    - .m4a
  archives:
    - .zip
    - .rar
    - .7z
    - .tar
    - .gz
  code:
    - .py
    - .js
    - .html
    - .css
    - .json
    - .xml

# 排除列表
exclude:
  paths:
    - "**/node_modules/**"
    - "**/.git/**"
    - "**/__pycache__/**"
  files:
    - "*.tmp"
    - "*.temp"
    - "Thumbs.db"
    - ".DS_Store"
'''
    
    config_path = Path(__file__).parent / 'config.example.yaml'
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"✅ 已创建示例配置文件: {config_path}")
    return True

def create_readme():
    """创建README文件"""
    readme_content = '''# 文件管理大师 📁✨

强大的文件批量处理工具，让文件管理变得简单高效。

## 功能特性

### 🎯 批量重命名
- 智能编号重命名
- 正则表达式替换
- 添加前缀后缀
- 日期时间变量

### 📂 智能整理
- 按文件类型分类
- 按日期整理
- 按大小分组
- 自动创建文件夹

### 🔍 高级搜索
- 文件内容搜索
- 元数据搜索
- 重复文件查找
- 快速文件定位

### ⚡ 快速操作
- 批量复制移动
- 格式转换
- 文件压缩
- 自动备份

## 快速开始

### 安装
```bash
# 运行安装脚本
python install.py
```

### 基本使用
```bash
# 批量重命名
file-master rename "~/photos" --pattern "vacation_{num:03d}.jpg"

# 按类型整理
file-master organize "~/Downloads" --recursive

# 搜索文件
file-master search "~/projects" --content "TODO:"

# 查找重复文件
file-master find-duplicates "~/backup"
```

## 详细文档

### 重命名模式
支持以下变量：
- `{num}` 或 `{num:03d}`: 序号（001, 002, ...）
- `{date:YYYYMMDD}`: 文件修改日期
- `{date:YYYY-MM-DD}`: 带分隔符的日期

示例：
```bash
# 添加前缀
file-master rename "." --prefix "backup_"

# 使用正则表达式
file-master rename "." --regex "^(.*)\.old$" --replace "$1.new"

# 按日期重命名
file-master rename "~/photos" --pattern "{date:YYYYMMDD}_{num:03d}.jpg"
```

### 整理选项
```bash
# 按类型整理（默认）
file-master organize "~/Downloads"

# 递归整理子文件夹
file-master organize "~/Downloads" --recursive

# 按日期整理
file-master organize "~/photos" --by date --format "YYYY/MM"

# 按大小整理
file-master organize "~/files" --by size --groups "small:<1MB,medium:1MB-10MB,large:>10MB"
```

### 搜索功能
```bash
# 简单搜索
file-master search "~/docs" --name "*.pdf"

# 内容搜索
file-master search "~/code" --content "function" --recursive

# 组合搜索
file-master search "~/work" --name "*.docx" --content "会议记录" --date "2026-01-01..2026-03-31"
```

## 配置说明

配置文件位置：`~/.file-master/config.yaml`

主要配置项：
- `confirm_deletion`: 删除前确认（默认：true）
- `backup_before_rename`: 重命名前备份（默认：true）
- `log_level`: 日志级别（debug/info/warning/error）
- `default_paths`: 默认路径配置
- `rules`: 自动化规则
- `file_types`: 文件类型分类
- `exclude`: 排除列表

## 安全特性

- 🔒 重要操作前确认
- 💾 自动备份机制
- 📝 完整操作日志
- ↩️ 操作撤销功能
- 🛡️ 权限检查保护

## 系统要求

- **操作系统**: Windows 10+, macOS 10.15+, Linux
- **Python**: 3.8 或更高版本
- **内存**: 512MB RAM（推荐2GB）
- **磁盘空间**: 50MB

## 技术支持

- 📚 文档：运行 `file-master --help`
- 💬 社区：https://github.com/file-master-pro/community
- 🐛 问题反馈：https://github.com/file-master-pro/issues
- 📧 邮箱支持：support@file-master.pro

## 许可证

MIT License - 详见 LICENSE 文件

## 更新日志

### v1.0.0 (2026-04-01)
- 首次发布
- 批量重命名功能
- 智能文件整理
- 高级搜索功能
- 重复文件查找

---

**让文件管理变得简单高效！** 🚀
'''
    
    readme_path = Path(__file__).parent / 'README.md'
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ 已创建README文件: {readme_path}")
    return True

def run_tests():
    """运行测试"""
    print("\n" + "=" * 60)
    print("[TEST] 运行测试")
    print("=" * 60)
    
    import subprocess
    import tempfile
    import time
    
    # 创建测试目录
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir) / 'test_files'
        test_dir.mkdir()
        
        # 创建测试文件
        test_files = [
            "photo1.jpg",
            "photo2.jpg",
            "document1.pdf",
            "document2.docx",
            "music1.mp3",
            "video1.mp4"
        ]
        
        for filename in test_files:
            file_path = test_dir / filename
            file_path.write_text(f"Test content for {filename}")
            # 设置不同的修改时间
            mtime = time.time() - (hash(filename) % 86400)
            os.utime(file_path, (mtime, mtime))
        
        print(f"测试目录: {test_dir}")
        print(f"创建了 {len(test_files)} 个测试文件")
        
        # 测试重命名
        print("\n1. 测试重命名功能...")
        result = subprocess.run([
            sys.executable, "file_master.py", "rename", 
            str(test_dir), "--pattern", "file_{num:03d}{ext}"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  [OK] 重命名测试通过")
        else:
            print(f"  [ERROR] 重命名测试失败: {result.stderr}")
        
        # 测试整理功能
        print("\n2. 测试整理功能...")
        result = subprocess.run([
            sys.executable, "file_master.py", "organize", 
            str(test_dir)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  [OK] 整理测试通过")
        else:
            print(f"  [ERROR] 整理测试失败: {result.stderr}")
        
        # 测试搜索功能
        print("\n3. 测试搜索功能...")
        result = subprocess.run([
            sys.executable, "file_master.py", "search", 
            str(test_dir), "--content", "Test"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  [OK] 搜索测试通过")
        else:
            print(f"  [ERROR] 搜索测试失败: {result.stderr}")
    
    print("\n" + "=" * 60)
    print("[TEST] 测试完成")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    print("文件管理大师 - 开发工具")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "install":
            install_file_master()
        elif command == "config":
            create_example_config()
        elif command == "readme":
            create_readme()
        elif command == "test":
            run_tests()
        elif command == "all":
            create_example_config()
            create_readme()
            install_file_master()
            run_tests()
        else:
            print("可用命令:")
            print("  install - 安装文件管理大师")
            print("  config  - 创建示例配置文件")
            print("  readme  - 创建README文件")
            print("  test    - 运行测试")
            print("  all     - 执行所有步骤")
    else:
        print("请指定命令:")
        print("  python install.py install")
        print("  python install.py config")
        print("  python install.py readme")
        print("  python install.py test")
        print("  python install.py all")