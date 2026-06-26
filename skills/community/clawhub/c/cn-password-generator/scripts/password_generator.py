#!/usr/bin/env python3
"""
密码生成器 - 生成安全的随机密码
"""
import secrets
import string
import sys
import json

def generate_password(length=16, use_upper=True, use_lower=True, use_digits=True, use_special=True, exclude_similar=False):
    """生成随机密码"""
    chars = ''
    
    if use_upper:
        chars += string.ascii_uppercase
    if use_lower:
        chars += string.ascii_lowercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
    
    if exclude_similar:
        similar = '0O1lI'
        chars = ''.join(c for c in chars if c not in similar)
    
    if not chars:
        chars = string.ascii_letters + string.digits
    
    return ''.join(secrets.choice(chars) for _ in range(length))

def main():
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    # 默认参数
    length = 16
    count = 1
    use_upper = True
    use_lower = True
    use_digits = True
    use_special = True
    exclude_similar = False
    
    # 解析参数
    i = 0
    while i < len(args):
        arg = args[i]
        if arg.isdigit():
            if length == 16:
                length = int(arg)
            else:
                count = int(arg)
        elif arg in ['--no-upper', '-nu']:
            use_upper = False
        elif arg in ['--no-lower', '-nl']:
            use_lower = False
        elif arg in ['--no-digits', '-nd']:
            use_digits = False
        elif arg in ['--no-special', '-ns']:
            use_special = False
        elif arg in ['--exclude-similar', '-es']:
            exclude_similar = True
        i += 1
    
    # 生成密码
    passwords = [generate_password(length, use_upper, use_lower, use_digits, use_special, exclude_similar) for _ in range(count)]
    
    result = {
        'count': count,
        'length': length,
        'passwords': passwords
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
