#!/usr/bin/env python3
"""
打包脚本 - 创建可发布的技能包（清理版）
"""

import os
import sys
import shutil
import zipfile
import tarfile
from pathlib import Path
from datetime import datetime

def create_directory_structure():
    """创建目录结构"""
    print("📁 创建目录结构...")
    
    # 源目录
    source_dir = Path(__file__).parent
    
    # 打包目录
    package_name = "bilibili-transcriber-pro"
    package_dir = source_dir / "dist" / package_name
    package_dir.mkdir(parents=True, exist_ok=True)
    
    # 需要包含的文件
    include_files = [
        "bilibili_transcriber.py",
        "cli.py",
        "config.yaml",
        "setup.py",
        "requirements.txt",
        "README.md",
        "SKILL.md",
        "package.json",
        "test_install.py",
        "make_package.py"
    ]
    
    # 需要包含的目录
    include_dirs = [
        "examples"
    ]
    
    # 复制文件
    for file_name in include_files:
        source_file = source_dir / file_name
        if source_file.exists():
            shutil.copy2(source_file, package_dir / file_name)
            print(f"  ✅ 复制文件: {file_name}")
        else:
            print(f"  ⚠️ 文件不存在: {file_name}")
    
    # 复制目录
    for dir_name in include_dirs:
        source_dir_path = source_dir / dir_name
        if source_dir_path.exists():
            dest_dir_path = package_dir / dir_name
            shutil.copytree(source_dir_path, dest_dir_path, dirs_exist_ok=True)
            print(f"  ✅ 复制目录: {dir_name}")
        else:
            print(f"  ⚠️ 目录不存在: {dir_name}")
    
    return package_dir

def create_zip_package(package_dir):
    """创建ZIP包"""
    print("\n📦 创建ZIP包...")
    
    dist_dir = package_dir.parent.parent
    zip_filename = dist_dir / f"bilibili-transcriber-pro-{datetime.now().strftime('%Y%m%d')}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arcname)
    
    print(f"  ✅ ZIP包创建完成: {zip_filename}")
    print(f"     大小: {zip_filename.stat().st_size / 1024:.1f} KB")
    
    return zip_filename

def create_tar_package(package_dir):
    """创建tar.gz包"""
    print("\n📦 创建tar.gz包...")
    
    dist_dir = package_dir.parent.parent
    tar_filename = dist_dir / f"bilibili-transcriber-pro-{datetime.now().strftime('%Y%m%d')}.tar.gz"
    
    with tarfile.open(tar_filename, 'w:gz') as tar:
        tar.add(package_dir, arcname=package_dir.name)
    
    print(f"  ✅ tar.gz包创建完成: {tar_filename}")
    print(f"     大小: {tar_filename.stat().st_size / 1024:.1f} KB")
    
    return tar_filename

def create_clawhub_package(package_dir):
    """创建ClawHub发布包"""
    print("\n🚀 创建ClawHub发布包...")
    
    # ClawHub包结构
    clawhub_dir = package_dir.parent / "clawhub"
    clawhub_dir.mkdir(exist_ok=True)
    
    # 复制必要文件
    essential_files = [
        "SKILL.md",
        "bilibili_transcriber.py",
        "cli.py",
        "config.yaml",
        "setup.py",
        "requirements.txt",
        "README.md",
        "package.json"
    ]
    
    for file_name in essential_files:
        source_file = package_dir / file_name
        if source_file.exists():
            shutil.copy2(source_file, clawhub_dir / file_name)
    
    # 创建manifest文件
    manifest = {
        "name": "bilibili-transcriber-pro",
        "version": "1.0.0",
        "description": "专业处理B站视频字幕问题，支持语音转文字、字幕下载、内容分析",
        "author": "B站视频转录专家团队",
        "license": "MIT",
        "repository": "https://github.com/community/bilibili-transcriber-pro",
        "skills": ["bilibili", "transcription", "video-processing"],
        "files": essential_files,
        "install_command": "python setup.py",
        "test_command": "python test_install.py"
    }
    
    import json
    with open(clawhub_dir / "manifest.json", 'w') as f:
        json.dump(manifest, f, indent=2)
    
    # 创建ClawHub包
    clawhub_package = clawhub_dir.parent / f"bilibili-transcriber-pro-clawhub-{datetime.now().strftime('%Y%m%d')}.zip"
    
    with zipfile.ZipFile(clawhub_package, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(clawhub_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(clawhub_dir)
                zipf.write(file_path, arcname)
    
    print(f"  ✅ ClawHub包创建完成: {clawhub_package}")
    print(f"     大小: {clawhub_package.stat().st_size / 1024:.1f} KB")
    
    return clawhub_package

def generate_checksum(file_path):
    """生成文件校验和"""
    import hashlib
    
    with open(file_path, 'rb') as f:
        file_hash = hashlib.sha256()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    
    return file_hash.hexdigest()

def create_release_notes():
    """创建发布说明"""
    print("\n📝 创建发布说明...")
    
    release_notes = f"""# B站视频转录专家 v1.0.0 发布说明

## 🎉 新版本发布

**发布日期**: {datetime.now().strftime('%Y-%m-%d')}
**版本**: 1.0.0
**Python要求**: >= 3.8

## ✨ 主要特性

### 🎯 核心功能
1. **智能字幕处理**：自动检测B站字幕系统状态，智能选择最佳方案
2. **语音转文字**：使用Whisper模型进行高精度语音识别
3. **国内镜像支持**：自动使用国内镜像源，解决网络问题
4. **错误处理**：自动检测字幕关联错误，切换到语音转文字
5. **批量处理**：支持批量处理多个B站视频

### 🔧 技术特点
- **绕过B站字幕系统**：直接处理音频，避免字幕关联错误
- **多模型支持**：Whisper base/small/medium模型可选
- **Cookie管理**：支持Cookie文件管理和自动刷新
- **进度显示**：实时显示下载和转录进度
- **结果验证**：自动验证转录内容与视频标题相关性

## 🚀 快速开始

### 安装
```bash
# 运行安装脚本
python setup.py

# 或手动安装
pip install -r requirements.txt
```

### 基本使用
```bash
# 处理单个视频
bilibili-transcribe BV1txQGByERW

# 批量处理
bilibili-transcribe --batch bv_list.txt
```

## 📦 文件清单

### 核心文件
- `bilibili_transcriber.py` - 核心处理模块
- `cli.py` - 命令行工具
- `config.yaml` - 配置文件
- `setup.py` - 安装脚本
- `requirements.txt` - 依赖列表

### 文档文件
- `README.md` - 说明文档
- `SKILL.md` - 技能文档
- `examples/` - 示例文件

### 工具文件
- `test_install.py` - 安装测试
- `make_package.py` - 打包脚本
- `package.json` - 包配置

## 🔧 系统要求

### 必需
- Python 3.8+
- FFmpeg
- 网络连接

### 推荐
- 4GB+ 内存
- 支持CUDA的GPU（可选，加速转录）

## 📄 许可证

MIT License

## 🤝 支持

- 问题反馈: GitHub Issues
- 文档: README.md
- 示例: examples/

## 🔄 更新日志

### v1.0.0 (2026-04-15)
- 初始版本发布
- 基于实际B站字幕问题处理经验
- 完整的命令行工具和Python API
- 支持批量处理和内容验证

---

**基于实际经验开发，专门解决B站字幕系统错误问题，稳定可靠！**
"""
    
    dist_dir = Path(__file__).parent / "dist"
    dist_dir.mkdir(exist_ok=True)
    
    release_file = dist_dir / "RELEASE_NOTES.md"
    with open(release_file, 'w', encoding='utf-8') as f:
        f.write(release_notes)
    
    print(f"  ✅ 发布说明创建完成: {release_file}")
    
    return release_file

def main():
    """主打包函数"""
    print("=" * 60)
    print("📦 B站视频转录专家 - 打包工具（清理版）")
    print("=" * 60)
    
    try:
        # 1. 创建目录结构
        package_dir = create_directory_structure()
        
        # 2. 创建各种包格式
        zip_file = create_zip_package(package_dir)
        tar_file = create_tar_package(package_dir)
        clawhub_file = create_clawhub_package(package_dir)
        
        # 3. 生成校验和
        print("\n🔐 生成文件校验和...")
        files = [zip_file, tar_file, clawhub_file]
        checksums = {}
        
        for file_path in files:
            if file_path.exists():
                checksum = generate_checksum(file_path)
                checksums[file_path.name] = checksum
                print(f"  ✅ {file_path.name}: {checksum[:16]}...")
        
        # 4. 创建发布说明
        release_file = create_release_notes()
        
        # 5. 保存校验和文件
        checksum_file = package_dir.parent.parent / "checksums.txt"
        with open(checksum_file, 'w') as f:
            f.write(f"B站视频转录专家 v1.0.0 文件校验和\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            for filename, checksum in checksums.items():
                f.write(f"{filename}\n")
                f.write(f"SHA256: {checksum}\n\n")
        
        print(f"\n✅ 校验和文件: {checksum_file}")
        
        # 6. 打印总结
        print("\n" + "=" * 60)
        print("🎉 打包完成！")
        print("=" * 60)
        
        print("\n📦 生成的包文件:")
        print(f"  1. ZIP包: {zip_file.name}")
        print(f"     路径: {zip_file}")
        print(f"     大小: {zip_filename.stat().st_size / 1024:.1f} KB")
        
        print(f"\n  2. tar.gz包: {tar_file.name}")
        print(f"     路径: {tar_file}")
        print(f"     大小: {tar_file.stat().st_size / 1024:.1f} KB")
        
        print(f"\n  3. ClawHub包: {clawhub_file.name}")
        print(f"     路径: {clawhub_file}")
        print(f"     大小: {clawhub_file.stat().st_size / 1024:.1f} KB")
        
        print(f"\n📝 发布说明: {release_file.name}")
        print(f"🔐 校验和文件: {checksum_file.name}")
        
        print("\n🚀 发布建议:")
        print("  1. 上传包文件到GitHub Releases")
        print("  2. 发布到ClawHub: clawhub publish")
        print("  3. 更新文档和示例")
        
        print("\n" + "=" * 60)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 打包失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())