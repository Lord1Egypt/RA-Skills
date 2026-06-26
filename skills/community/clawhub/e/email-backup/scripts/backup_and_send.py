#!/usr/bin/env python3
"""
QQ邮箱文件备份主脚本
打包文件并发送到QQ邮箱
"""

import os
import sys
import argparse
import tarfile
import tempfile
import shutil
import datetime
import re
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from send_email import send_email_with_attachment
from clean_sensitive import clean_file

# QQ邮箱配置（可通过环境变量覆盖）
QQ_EMAIL = os.getenv('QQ_EMAIL', 'your-email@example.com')
QQ_SMTP_PASSWORD = os.getenv('QQ_SMTP_PASSWORD', 'your-auth-code')

def create_archive(directories, output_path, exclude_patterns=None, compression=6):
    """
    创建tar.gz压缩包
    
    Args:
        directories: 要打包的目录列表
        output_path: 输出文件路径
        exclude_patterns: 排除的文件模式列表
        compression: 压缩级别（1-9）
    
    Returns:
        bool: 是否成功
    """
    try:
        exclude_patterns = exclude_patterns or []
        
        with tarfile.open(output_path, 'w:gz', compresslevel=compression) as tar:
            for directory in directories:
                dir_path = Path(directory).expanduser().resolve()
                
                if not dir_path.exists():
                    print(f"⚠️  目录不存在: {dir_path}")
                    continue
                
                print(f"📦 正在打包: {dir_path}")
                
                # 遍历目录
                for item in dir_path.rglob('*'):
                    # 检查是否需要排除
                    should_exclude = False
                    for pattern in exclude_patterns:
                        if item.match(pattern):
                            should_exclude = True
                            break
                    
                    if should_exclude:
                        continue
                    
                    # 计算相对路径
                    arcname = item.relative_to(dir_path.parent)
                    
                    # 添加到压缩包
                    tar.add(item, arcname=str(arcname))
        
        print(f"✅ 打包完成: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ 打包失败: {e}")
        return False

def clean_sensitive_info(file_path):
    """
    清理文件中的敏感信息
    
    Args:
        file_path: 文件路径
    
    Returns:
        bool: 是否成功
    """
    try:
        print(f"🧹 正在清理敏感信息: {file_path}")
        
        # 创建临时文件
        temp_fd, temp_path = tempfile.mkstemp(suffix='.tar.gz')
        os.close(temp_fd)
        
        # 解压到临时目录
        temp_dir = tempfile.mkdtemp()
        
        with tarfile.open(file_path, 'r:gz') as tar:
            tar.extractall(temp_dir)
        
        # 清理敏感信息
        cleaned_count = 0
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if clean_file(file_path):
                    cleaned_count += 1
        
        # 重新打包
        with tarfile.open(temp_path, 'w:gz') as tar:
            tar.add(temp_dir, arcname='.')
        
        # 替换原文件
        shutil.move(temp_path, file_path)
        
        # 清理临时目录
        shutil.rmtree(temp_dir)
        
        print(f"✅ 清理完成: 已清理 {cleaned_count} 个文件")
        return True
        
    except Exception as e:
        print(f"❌ 清理失败: {e}")
        return False

def send_backup_email(archive_path, to_email=None, subject=None, body=None):
    """
    发送备份邮件
    
    Args:
        archive_path: 压缩包路径
        to_email: 收件人邮箱
        subject: 邮件主题
        body: 邮件正文
    
    Returns:
        bool: 是否成功
    """
    try:
        # 设置默认值
        to_email = to_email or QQ_EMAIL
        subject = subject or f"🌸 文件备份 ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})"
        
        if body is None:
            file_size = os.path.getsize(archive_path) / (1024 * 1024)  # MB
            body = f"""Hello! This is your file backup from the Email Backup Skill. 📦

📁 File: {os.path.basename(archive_path)}
📦 Size: {file_size:.2f} MB
📅 Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
This backup contains your configured directories.
Feel free to reach out if you need any help! 🌸
"""
        
        print(f"📧 正在发送邮件到: {to_email}")
        
        # 发送邮件
        success = send_email_with_attachment(
            to_email=to_email,
            subject=subject,
            body=body,
            attachment_path=archive_path,
            smtp_server='smtp.qq.com',
            smtp_port=465,
            username=QQ_EMAIL,
            password=QQ_SMTP_PASSWORD
        )
        
        if success:
            print("✅ 邮件发送成功！")
        else:
            print("❌ 邮件发送失败！")
        
        return success
        
    except Exception as e:
        print(f"❌ 发送邮件失败: {e}")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='QQ邮箱文件备份工具 - 打包文件并发送到QQ邮箱',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s /path/to/directory
  %(prog)s /path/to/dir1 /path/to/dir2 --to recipient@qq.com
  %(prog)s /path/to/directory --subject "我的备份" --clean
        """
    )
    
    parser.add_argument(
        'directories',
        nargs='+',
        help='要打包的目录（支持多个）'
    )
    
    parser.add_argument(
        '--to',
        help='收件人邮箱（默认：发件人邮箱）'
    )
    
    parser.add_argument(
        '--subject',
        help='邮件主题'
    )
    
    parser.add_argument(
        '--body',
        help='邮件正文'
    )
    
    parser.add_argument(
        '--clean',
        action='store_true',
        help='清理敏感信息'
    )
    
    parser.add_argument(
        '--exclude',
        nargs='+',
        default=[],
        help='排除的文件模式（如：*.log *.tmp）'
    )
    
    parser.add_argument(
        '--compression',
        type=int,
        choices=range(1, 10),
        default=6,
        help='压缩级别（1-9，默认：6）'
    )
    
    parser.add_argument(
        '--output',
        help='输出文件路径（默认：自动生成）'
    )
    
    parser.add_argument(
        '--no-send',
        action='store_true',
        help='只打包，不发送邮件'
    )
    
    args = parser.parse_args()
    
    print("🔍 开始文件备份流程...")
    print(f"📁 要打包的目录: {', '.join(args.directories)}")
    
    # 生成输出文件名
    if args.output:
        output_path = args.output
    else:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"~/backup_{timestamp}.tar.gz"
    
    output_path = os.path.expanduser(output_path)
    
    # 创建压缩包
    if not create_archive(args.directories, output_path, args.exclude, args.compression):
        sys.exit(1)
    
    # 清理敏感信息
    if args.clean:
        if not clean_sensitive_info(output_path):
            print("⚠️  敏感信息清理失败，但继续发送邮件")
    
    # 发送邮件
    if not args.no_send:
        if not send_backup_email(output_path, args.to, args.subject, args.body):
            sys.exit(1)
    
    print("\n✅ 文件备份流程完成！")
    print(f"📦 压缩包位置: {output_path}")

if __name__ == "__main__":
    main()