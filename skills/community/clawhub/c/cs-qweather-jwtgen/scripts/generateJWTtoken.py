#!/usr/bin/env python3
"""
生成和风天气 JWT Token 的工具。

环境变量（支持从 ~/.openclaw/.env 自动加载）：
    QWEATHER_SUB  和风账户的用户标识（sub 字段）
    QWEATHER_KID  和风账户的密钥 ID（kid 字段）

Token 输出到:
    ~/.myjwtkey/last-token.dat（每次生成后覆盖写入）

日志输出到:
    /tmp/cslog/generateJWTtoken-YYYYMMDD.log
"""

import sys
import os
import time
import jwt
from datetime import datetime

# 尝试加载 dotenv（标准方式读取 .env 文件）
try:
    import dotenv
    # 优先加载 ~/.openclaw/.env（OpenClaw 标准配置位置）
    # 若 OpenClaw 已将 env 注入了当前进程，此调用不会覆盖已存在的变量
    dotenv.load_dotenv(os.path.expanduser("~/.openclaw/.env"), override=True)
except ImportError:
    # 未安装 dotenv 时跳过，完全依赖环境继承
    pass


# ============ 脱敏工具 ============

def _mask(s: str, show_front: int = 2, show_back: int = 2) -> str:
    """只显示前 show_front 位和后 show_back 位，其余用 *** 代替。"""
    if len(s) <= show_front + show_back + 3:
        return "***"
    return s[:show_front] + "***" + s[-show_back:]


# ============ 日志配置 ============

def _get_log_path() -> str:
    """获取日志文件路径，每天一个文件，放在 /tmp/cslog/ 目录中。"""
    log_dir = "/tmp/cslog"
    os.makedirs(log_dir, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    return os.path.join(log_dir, f"generateJWTtoken-{today}.log")


def _log(msg: str) -> None:
    """写入日志文件并在 stderr 打印。"""
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    log_path = _get_log_path()
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, file=sys.stderr)


# ============ 保存 Token 到文件 ============

def _save_token_to_file(token: str) -> str:
    """将 token 写入 ~/.myjwtkey/last-token.dat，返回文件路径。"""
    token_file = os.path.expanduser("~/.myjwtkey/last-token.dat")
    os.makedirs(os.path.dirname(token_file), exist_ok=True)
    with open(token_file, "w", encoding="utf-8") as f:
        f.write(token)
    os.chmod(token_file, 0o600)
    return token_file


# ============ 主逻辑 ============

def main():
    # 1. 读取私钥
    key_path = os.path.expanduser("~/.myjwtkey/ed25519-private.pem")
    _log(f"Private key: {key_path}")

    if not os.path.exists(key_path):
        _log(f"ERROR: Private key not found: {key_path}")
        sys.exit(1)

    with open(key_path, "r", encoding="utf-8") as f:
        private_key = f.read()
    _log(f"Private key loaded ({len(private_key)} chars, masked)")

    # 2. 读取 sub
    sub = os.environ.get("QWEATHER_SUB")
    if not sub:
        _log("ERROR: QWEATHER_SUB environment variable is not set")
        _log("Hint: set it in ~/.openclaw/.env or export to environment")
        sys.exit(1)
    _log(f"sub: {_mask(sub)}")

    # 3. 读取 kid
    kid = os.environ.get("QWEATHER_KID")
    if not kid:
        _log("ERROR: QWEATHER_KID environment variable is not set")
        _log("Hint: set it in ~/.openclaw/.env or export to environment")
        sys.exit(1)
    _log(f"kid: {_mask(kid)}")

    # 4. 生成 JWT（EdDSA 算法）
    iat = int(time.time()) - 30   # 提前30秒避免时钟误差
    exp = iat + 84000             # 24小时后过期

    payload = {
        "iat": iat,
        "exp": exp,
        "sub": sub,
    }
    headers = {
        "kid": kid,
    }

    _log(f"iat={iat}, exp={exp}, sub={_mask(sub)}, kid={_mask(kid)}")
    _log("Generating JWT ...")

    encoded_jwt = jwt.encode(payload, private_key, algorithm="EdDSA", headers=headers)
    _log(f"JWT generated [masked: {_mask(encoded_jwt)}]")

    # 5. 写入 token 文件
    token_file = _save_token_to_file(encoded_jwt)
    _log(f"Token saved to: {token_file}")

    # 6. 输出结果
    print(f"\n[JWT Token]\n{encoded_jwt}\n")


if __name__ == "__main__":
    main()
