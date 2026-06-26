#!/usr/bin/env python3
"""
敏感信息清理脚本
清理文件中的API Key、密码等敏感信息
"""

import os
import re
import glob

# 敏感信息模式
SENSITIVE_PATTERNS = [
    # API Keys
    (r'sk-[a-zA-Z0-9]{20,}', 'sk-***REDACTED***'),
    (r'tvly-[a-zA-Z0-9-]{20,}', 'tvly-***REDACTED***'),
    (r'BOCHA_API_KEY:\s*`[^`]+`', 'BOCHA_API_KEY: `***REDACTED***`'),
    (r'TAVILY_API_KEY:\s*`[^`]+`', 'TAVILY_API_KEY: `***REDACTED***`'),
    (r'MIMO_API_KEY:\s*`[^`]+`', 'MIMO_API_KEY: `***REDACTED***`'),
    
    # Passwords
    (r"PASSWORD\s*=\s*'[^']*'", "PASSWORD = '***REDACTED***'"),
    (r'password\s*=\s*"[^"]*"', 'password = "***REDACTED***"'),
    (r"password\s*=\s*'[^']*'", "password = '***REDACTED***'"),
    
    # Auth codes / tokens
    (r'auth[._-]?code', '***REDACTED***'),
    (r'token\s*[=:]\s*\S+', 'token = ***REDACTED***'),
    
    # Email addresses (anonymize)
    (r'[a-zA-Z0-9._%+-]+@qq\.com', 'user@example.com'),
    (r'[a-zA-Z0-9._%+-]+@example\.com', 'user@example.com'),
    
    # User IDs
    (r'ou_[a-zA-Z0-9]{20,}', 'ou_***REDACTED***'),
    
    # Other sensitive fields
    (r'APP_SECRET\s*=\s*"[^"]*"', 'APP_SECRET = "***REDACTED***"'),
    (r'APP_ID\s*=\s*"[^"]*"', 'APP_ID = "***REDACTED***"'),
    
    # Generic patterns
    (r'your-api-key-here', '***REDACTED***'),
    (r'your-password-here', '***REDACTED***'),
    (r'your-auth-code', 'your-auth-code'),
]

def clean_file(filepath):
    """
    清理单个文件中的敏感信息
    
    Args:
        filepath: 文件路径
    
    Returns:
        bool: 是否进行了清理
    """
    try:
        # 检查文件类型
        file_ext = os.path.splitext(filepath)[1].lower()
        text_extensions = ['.md', '.json', '.py', '.js', '.ts', '.env', '.config', '.yaml', '.yml', '.txt', '.sh', '.bash']
        
        if file_ext not in text_extensions:
            return False
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        
        for pattern, replacement in SENSITIVE_PATTERNS:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ 处理失败 {filepath}: {e}")
        return False

def clean_directory(directory, recursive=True):
    """
    清理目录中的所有文件
    
    Args:
        directory: 目录路径
        recursive: 是否递归处理子目录
    
    Returns:
        tuple: (总文件数, 已清理文件数)
    """
    total_count = 0
    cleaned_count = 0
    
    if recursive:
        for root, dirs, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                total_count += 1
                if clean_file(filepath):
                    cleaned_count += 1
    else:
        for file in os.listdir(directory):
            filepath = os.path.join(directory, file)
            if os.path.isfile(filepath):
                total_count += 1
                if clean_file(filepath):
                    cleaned_count += 1
    
    return total_count, cleaned_count

def main():
    """主函数（用于测试）"""
    import argparse
    
    parser = argparse.ArgumentParser(description='敏感信息清理工具')
    parser.add_argument('path', help='要清理的文件或目录路径')
    parser.add_argument('--no-recursive', action='store_true', help='不递归处理子目录')
    
    args = parser.parse_args()
    
    path = os.path.expanduser(args.path)
    
    if not os.path.exists(path):
        print(f"❌ 路径不存在: {path}")
        exit(1)
    
    print(f"🧹 开始清理敏感信息: {path}")
    
    if os.path.isfile(path):
        if clean_file(path):
            print(f"✅ 已清理: {path}")
        else:
            print(f"⏭️  无需清理: {path}")
    else:
        total, cleaned = clean_directory(path, not args.no_recursive)
        print(f"\n📊 清理完成:")
        print(f"   总文件数: {total}")
        print(f"   已清理: {cleaned}")
        print(f"   无需清理: {total - cleaned}")

if __name__ == "__main__":
    main()