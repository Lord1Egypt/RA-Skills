#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
加密备份 / 恢复 — AES-256-GCM
防暴力破解：连续输错3次密码，锁定1小时
"""
import sys; sys.stdout.reconfigure(encoding='utf-8')
import os, json, stat, getpass, hashlib
from datetime import datetime, timedelta

SECRETS_FILE = os.path.expanduser("~/.openclaw/workspace/secrets.json")
BACKUP_FILE  = os.path.expanduser("~/.openclaw/workspace/secrets.json.enc")
LOCK_FILE     = os.path.expanduser("~/.openclaw/workspace/secrets.lock")
AUDIT_FILE    = os.path.expanduser("~/.openclaw/workspace/secrets.audit.log")

MAX_ATTEMPTS = 3
LOCK_DURATION_HOURS = 1

def _audit(action, success=True, note=""):
    entry = {
        "ts": datetime.now().isoformat(),
        "action": action,
        "success": success,
        "note": note
    }
    try:
        with open(AUDIT_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        os.chmod(AUDIT_FILE, stat.S_IRUSR | stat.S_IWUSR)
    except Exception:
        pass

def _load_lock():
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"attempts": 0, "locked_until": None}

def _save_lock(lock):
    with open(LOCK_FILE, "w", encoding="utf-8") as f:
        json.dump(lock, f)
    os.chmod(LOCK_FILE, stat.S_IRUSR | stat.S_IWUSR)

def _is_locked():
    lock = _load_lock()
    if lock["attempts"] < MAX_ATTEMPTS:
        return False
    locked_until = lock.get("locked_until")
    if not locked_until:
        return False
    if datetime.now() < datetime.fromisoformat(locked_until):
        remaining = (datetime.fromisoformat(locked_until) - datetime.now()).seconds
        print(f"[锁定] 太多次失败尝试，{remaining//60}分钟后重试")
        return True
    # 锁定已过期，重置
    _save_lock({"attempts": 0, "locked_until": None})
    return False

def _record_failed():
    lock = _load_lock()
    lock["attempts"] += 1
    if lock["attempts"] >= MAX_ATTEMPTS:
        lock["locked_until"] = (datetime.now() + timedelta(hours=LOCK_DURATION_HOURS)).isoformat()
        print(f"[锁定] 连续{MAX_ATTEMPTS}次密码错误，锁定{LOCK_DURATION_HOURS}小时")
    _save_lock(lock)

def _reset_attempts():
    lock = _load_lock()
    if lock["attempts"] > 0:
        lock["attempts"] = 0
        lock["locked_until"] = None
        _save_lock(lock)

try:
    from Crypto.Cipher import AES
    from Crypto.Protocol.KDF import PBKDF2
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

def pbkdf2(password, salt, iterations=100000):
    # PBKDF2-HMAC-SHA256, count=iterations
    return PBKDF2(password, salt, dkLen=32, count=iterations, hmac_gen=hashlib.sha256)

def aes_encrypt(data_bytes: bytes, password: str) -> bytes:
    if not HAS_CRYPTO:
        raise ImportError("需要 pycryptodome: pip install pycryptodome")
    salt = os.urandom(16)
    iv = os.urandom(16)
    key = pbkdf2(password, salt)
    cipher = AES.new(key, AES.MODE_GCM, iv)
    ct, tag = cipher.encrypt_and_digest(data_bytes)
    return salt + iv + ct + tag

def aes_decrypt(enc_data: bytes, password: str) -> bytes:
    if not HAS_CRYPTO:
        raise ImportError("需要 pycryptodome: pip install pycryptodome")
    salt = enc_data[:16]
    iv = enc_data[16:32]
    ct = enc_data[32:-16]
    tag = enc_data[-16:]
    key = pbkdf2(password, salt)
    cipher = AES.new(key, AES.MODE_GCM, iv)
    return cipher.decrypt_and_verify(ct, tag)

def export_backup():
    if not os.path.exists(SECRETS_FILE):
        print("[错误] secrets.json 不存在"); return False
    if _is_locked():
        _audit("backup", False, "locked out")
        return False

    with open(SECRETS_FILE, encoding="utf-8") as f:
        data = json.load(f)

    password = getpass.getpass("设置备份密码: ")
    if len(password) < 8:
        print("[错误] 密码长度至少8位"); return False
    confirm = getpass.getpass("确认密码: ")
    if password != confirm:
        print("[错误] 两次密码不一致"); return False

    try:
        data_bytes = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        enc_data = aes_encrypt(data_bytes, password)
        with open(BACKUP_FILE, "wb") as f:
            f.write(enc_data)
        os.chmod(BACKUP_FILE, stat.S_IRUSR | stat.S_IWUSR)
        _reset_attempts()
        _audit("backup_export", True)
        print(f"[OK] 备份已加密保存到: {BACKUP_FILE}")
        print(f"     AES-256-GCM + PBKDF2")
        return True
    except ImportError as e:
        print(f"[错误] {e}"); _audit("backup", False, str(e)); return False
    except Exception as e:
        print(f"[错误] {e}"); _audit("backup", False, str(e)); return False

def import_backup(backup_path):
    if not os.path.exists(backup_path):
        print(f"[错误] 备份文件不存在: {backup_path}"); return False
    if _is_locked():
        _audit("backup_restore", False, "locked out")
        return False

    password = getpass.getpass("输入备份密码: ")

    try:
        with open(backup_path, "rb") as f:
            enc_data = f.read()
        data_bytes = aes_decrypt(enc_data, password)
        data = json.loads(data_bytes.decode("utf-8"))
        _reset_attempts()

        if os.path.exists(SECRETS_FILE):
            with open(SECRETS_FILE, encoding="utf-8") as f:
                existing = json.load(f)
            existing["entries"].update(data.get("entries", {}))
            data = existing

        with open(SECRETS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.chmod(SECRETS_FILE, stat.S_IRUSR | stat.S_IWUSR)

        _audit("backup_restore", True)
        print(f"[OK] 备份已恢复，共 {len(data.get('entries', {}))} 个令牌")
        return True
    except Exception as e:
        _record_failed()
        _audit("backup_restore", False, "wrong password")
        attempts = _load_lock().get("attempts", 0)
        print(f"[错误] 解密失败 ({attempts}/{MAX_ATTEMPTS} 次尝试)")
        return False

def check_backup(backup_path):
    if not os.path.exists(backup_path):
        print(f"[错误] 备份文件不存在: {backup_path}"); return
    size = os.path.getsize(backup_path)
    mtime = datetime.fromisoformat(datetime.fromtimestamp(os.path.getmtime(backup_path)).strftime("%Y-%m-%d %H:%M:%S"))
    print(f"备份文件: {backup_path}")
    print(f"文件大小: {size} bytes")
    print(f"修改时间: {mtime}")
    print(f"加密算法: AES-256-GCM + PBKDF2")

if __name__ == "__main__":
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print("""加密备份工具

用法:
  python backup.py --export              加密导出
  python backup.py --import <file>       解密导入
  python backup.py --check               检查备份文件
  python backup.py --check <file>       检查指定备份文件

安全机制:
  - 连续3次密码错误，锁定1小时
  - 密码长度至少8位
"""); sys.exit(0)

    if "--import" in args:
        idx = args.index("--import")
        path = args[idx + 1] if idx + 1 < len(args) else BACKUP_FILE
        import_backup(path)
    elif "--check" in args:
        idx = args.index("--check")
        path = args[idx + 1] if idx + 1 < len(args) else BACKUP_FILE
        check_backup(path)
    else:
        export_backup()
