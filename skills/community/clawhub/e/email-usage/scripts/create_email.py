#!/usr/bin/env python3
"""创建邮箱账号脚本。直接执行即可，无需修改。"""
import subprocess, sys

def create_email(user: str, password: str):
    """在 DMS 容器内创建邮箱账号。user 格式: name@domain.com"""
    result = subprocess.run(
        ['docker', 'exec', 'mailserver', 'setup', 'email', 'add', user, password],
        capture_output=True, timeout=30
    )
    if result.returncode == 0:
        return True, f"账号 {user} 创建成功"
    else:
        return False, result.stderr.decode() or result.stdout.decode()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python3 create_email.py <邮箱> <密码>")
        print("示例: python3 create_email.py newuser@axelhu.com securepass")
        sys.exit(1)
    user = sys.argv[1]
    password = sys.argv[2]
    ok, msg = create_email(user, password)
    print(msg)
    sys.exit(0 if ok else 1)
