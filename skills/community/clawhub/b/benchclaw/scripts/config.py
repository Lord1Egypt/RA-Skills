"""
BenchClaw 全局配置常量。
修改此文件即可调整运行参数，无需改动业务代码。
"""
# ---------- APP ----------
CLIENT_VERSION = '1.1.1'

# ---------- 加解密 (RSA + AES 混合) ----------
# 服务端 RSA 公钥 PEM（与 server 配置一致；可通过环境变量覆盖，见 crypto 模块），用于验证来自服务器的任务签名，确保题目未被篡改。
BENCHCLAW_RSA_PUBLIC_KEY_PEM = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArup/oFdhbiac8TtQC297
R6mzP59EToM2OJfnf7ZrbHYSAql0CE03Gv9GpHFhByOVRgNTcux+SQT3W5GohBkF
+emY/ntFd7QGnYIqa+1ME7yiZlzJhQ+ddP9YYpfZn6ixG6SsTne3vpWbiZRAv45A
BswtsJYpi6VRk6dusuo8VzjLL/IA96ua0RW+ik/NaPdpSnsw0MR/xRkJ7nP2k9LJ
L354Q+mroFh8dOkqiZjygqSJOPkyDH3SQMqgmJIMnvE+rqg72Ieb1UcnaESDzlMT
P+GOABlkd9K1M0OSvvs0lbu+8gHtYXllyw98l0SnkLUjZR2gmsYQD4Z5QXdvwNuu
YQIDAQAB
-----END PUBLIC KEY-----"""

# ---------- API ----------
BENCHCLAW_API_HOST = "benchclawapi.antutu.com"  # API 域名，更换时只需修改这里
DEFAULT_API_URL = f"https://{BENCHCLAW_API_HOST}/api/v1/tests/request"
DEFAULT_SUBMIT_API_URL = f"https://{BENCHCLAW_API_HOST}/api/v1/tests/submit"

# ---------- Gateway WebSocket ----------
DEFAULT_WS_URL = "ws://127.0.0.1:18789"
PROTOCOL_VERSION = 3

# ---------- 会话 & 超时 ----------
DEFAULT_AGENT_ID = "main"
DEFAULT_TIMEOUT_SEC = 300  # 单题最长等待秒数
DEFAULT_SESSION_PREFIX = "benchclaw_session_"
USE_LATEST_SESSION = True

# ---------- 上传数据截断配置 ----------
# stdout 内容截断长度（字符数），防止上传数据过大
UPLOAD_STDOUT_TRUNCATE_LENGTH = 2000
# stderr 内容截断长度（字符数）
UPLOAD_STDERR_TRUNCATE_LENGTH = 500
