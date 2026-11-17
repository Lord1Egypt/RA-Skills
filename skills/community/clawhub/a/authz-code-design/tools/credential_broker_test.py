#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
credential_broker_test.py — v2.1 本地闭环测试（临时 vault，零真实凭据）
覆盖：解锁→发令→履行→吊销→吊销后拒→错误pin 401→dashboard 只读
     + 审计持久化(重启不丢) + 设备指纹 + 生物字段 + 哈希链篡改检测
     + 完整吊销体系：revoke_device / revoke_title / revoke_all 一键解绑
"""
import os
import sys
import json
import time
import tempfile
import threading
import urllib.request
import urllib.error
from pykeepass import create_database
from credential_broker import Broker, _Handler, ThreadingHTTPServer

PASS = "test-master-pass-2026"
VAULT = os.path.join(tempfile.gettempdir(), f"broker_test_{os.getpid()}.kdbx")
AUDIT = os.path.join(tempfile.gettempdir(), f"broker_audit_{os.getpid()}.jsonl")
AKEY = os.path.join(tempfile.gettempdir(), f"broker_audit_key_{os.getpid()}.bin")
PIN = "test-pin"
PORT = 18731


def setup():
    for p in (VAULT, AUDIT, AKEY):
        if os.path.exists(p):
            os.remove(p)
    kp = create_database(VAULT, password=PASS)
    kp.add_entry(kp.root_group, title="GitHub", username="用户",
                 password="S0m3R@nd0mP@ss!")
    g = kp.add_group(kp.root_group, "用户 主身份")
    kp.add_entry(g, title="微信", username="用户_wx", password="wx-x")
    kp.save()


def req(method, path, body=None, pin=PIN, device=None):
    url = f"http://127.0.0.1:{PORT}{path}"
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("X-Broker-Pin", pin)
    if device:
        r.add_header("X-Device-Id", device)
    if data:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())


def main():
    setup()
    broker = Broker(VAULT, PASS, None, PIN, PORT, AUDIT, AKEY)
    broker.unlock(biometric="WinHello")
    _Handler.broker = broker
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), _Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    time.sleep(0.4)

    results = []
    def check(name, cond):
        results.append((name, cond))
        print(f"[{'PASS' if cond else 'FAIL'}] {name}")

    # 1 发令（带设备指纹）
    st, r = req("POST", "/token", {"title": "GitHub", "scope": "read", "ttl": 60},
                device="laptop-01")
    check("issue 200+token", st == 200 and "token" in r)
    token = r["token"]

    # 2 履行拿到正确密码
    st, r = req("POST", "/fulfill", {"token": token}, device="laptop-01")
    check("fulfill 正确密码", st == 200 and r.get("password") == "S0m3R@nd0mP@ss!")

    # 3 吊销
    st, r = req("POST", "/revoke", {"token": token}, device="laptop-01")
    check("revoke 200", st == 200 and r.get("revoked") is True)

    # 4 吊销后履行被拒
    st, r = req("POST", "/fulfill", {"token": token}, device="laptop-01")
    check("吊销后履行拒绝", st == 400)

    # 5 错误 pin 401
    st, r = req("POST", "/token", {"title": "GitHub"}, pin="wrong")
    check("错误pin 401", st == 401)

    # 6 dashboard 只读面板
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/dashboard?pin={PIN}",
                                    timeout=5) as resp:
            html = resp.read().decode()
        check("dashboard 200含分组树", resp.status == 200
              and "用户 主身份" in html and "GitHub" in html
              and "S0m3R@nd0mP@ss!" not in html)
    except Exception:
        check("dashboard 200含分组树", False)

    # ---- 完整吊销体系（对应方法论 §3.8） ----
    # 多设备 / 多条目场景
    st, r = req("POST", "/token", {"title": "GitHub", "scope": "read", "ttl": 120},
                device="laptop-01")
    check("二次发令(同设备)", st == 200 and "token" in r)
    t_g = r["token"]

    st, r = req("POST", "/token", {"title": "微信", "scope": "read", "ttl": 120},
                device="phone-02")
    check("发令(异设备)", st == 200 and "token" in r)
    t_w = r["token"]

    # revoke_device：按设备指纹收回，不误杀异设备
    st, r = req("POST", "/revoke_device", {"device_id": "laptop-01"},
                device="laptop-01")
    check("revoke_device 计数≥1", st == 200 and r.get("count", 0) >= 1)
    st, r = req("POST", "/fulfill", {"token": t_g}, device="laptop-01")
    check("revoke_device后同设备拒", st == 400)
    st, r = req("POST", "/fulfill", {"token": t_w}, device="phone-02")
    check("revoke_device不误杀异设备", st == 200 and r.get("title") == "微信")

    # revoke_title：按条目收回
    st, r = req("POST", "/revoke_title", {"title": "微信"}, device="phone-02")
    check("revoke_title 命中条目", st == 200 and r.get("title") == "微信")
    st, r = req("POST", "/fulfill", {"token": t_w}, device="phone-02")
    check("revoke_title后拒", st == 400)

    # revoke_all：一键解绑，应急清场
    st, r = req("POST", "/token", {"title": "GitHub", "scope": "read", "ttl": 120},
                device="laptop-01")
    t_g2 = r.get("token")
    st, r = req("POST", "/token", {"title": "微信", "scope": "read", "ttl": 120},
                device="phone-02")
    t_w2 = r.get("token")
    st, r = req("POST", "/revoke_all", {}, device="admin")
    check("revoke_all 计数≥2", st == 200 and r.get("count", 0) >= 2)
    st, r = req("POST", "/fulfill", {"token": t_g2}, device="laptop-01")
    check("revoke_all后拒(GitHub)", st == 400)
    st, r = req("POST", "/fulfill", {"token": t_w2}, device="phone-02")
    check("revoke_all全覆盖(微信)", st == 400)

    # 7 审计持久化：停 server，新 broker 加载同日志
    srv.shutdown()
    srv.server_close()
    broker2 = Broker(VAULT, PASS, None, PIN, PORT, AUDIT, AKEY)
    audit2 = broker2.audit_log()
    check("审计持久化不丢", len(audit2) >= 3)
    check("设备指纹记录", any(a.get("device") == "laptop-01" for a in audit2))
    check("生物字段记录", any(a.get("bio") == "WinHello" for a in audit2))

    # 8 哈希链篡改检测：改最后一行 device 但不改 hash
    with open(AUDIT, "r", encoding="utf-8") as f:
        lines = f.readlines()
    last = json.loads(lines[-1])
    last["device"] = "HACKED"
    lines[-1] = json.dumps(last, ensure_ascii=False) + "\n"
    with open(AUDIT, "w", encoding="utf-8") as f:
        f.writelines(lines)
    broker3 = Broker(VAULT, PASS, None, PIN, PORT, AUDIT, AKEY)  # 加载应跳过篡改条
    check("篡改检测不崩溃", True)
    check("篡改条被跳过", len(broker3.audit_log()) < len(lines))

    # 清理
    for p in (VAULT, AUDIT, AKEY):
        if os.path.exists(p):
            os.remove(p)

    passed = sum(1 for _, c in results if c)
    print(f"\n=== {passed}/{len(results)} PASS ===")
    if passed != len(results):
        print("FAILED:", [n for n, c in results if not c])
        sys.exit(1)
    print("ALL GREEN")


if __name__ == "__main__":
    main()
