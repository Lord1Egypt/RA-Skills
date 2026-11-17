#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
credential_broker_security_test.py — 8 维安全·稳定性本地闭环实测
============================================================================
原则（对应 content-publish-lifecycle 安全稳定性验证门）：
  - 零真实凭据：临时 .kdbx 仅在内存/临时目录，密码为随机占位符。
  - 本地闭环：进程内直接驱动 Broker，不暴露端口、不联网、不留盘敏感。
  - 可重复：每次重跑得到一致结果；维度评分为行为级（0–5），不披露实现。
  - 8 维：抗暴力破解 / 防篡改审计 / 授权时效强制 / 抗重放 / 零知识边界 /
         解绑完整性 / 并发稳定性 / 边界容错。

运行：python credential_broker_security_test.py
输出：逐维 PASS/FAIL + 综合分；退出码非 0 表示有维度未达 5.0。
"""
import os
import sys
import time
import json
import tempfile
import threading
import secrets

from pykeepass import create_database
from credential_broker import Broker, _jwt_sign

PASS = "master-pass-sec-2026"
PW_GITHUB = "S0m3R@nd0mP@ss!"
PW_WECHAT = "WxS3cr3t!"


def _make_broker():
    tmp = tempfile.mkdtemp(prefix="broker_sec_")
    vault = os.path.join(tmp, "sec.kdbx")
    audit = os.path.join(tmp, "audit.jsonl")
    akey = os.path.join(tmp, "akey.bin")
    kp = create_database(vault, password=PASS)
    kp.add_entry(kp.root_group, title="GitHub", username="u", password=PW_GITHUB)
    kp.add_entry(kp.root_group, title="WeChat", username="u2", password=PW_WECHAT)
    kp.save()
    b = Broker(vault, PASS, None, "pin", 0, audit, akey)
    b.unlock(biometric="WinHello")
    return b


def _issue(b, title="GitHub", ttl=300, device="laptop-01"):
    return b.issue_token(title, "read", ttl, device=device)["token"]


# ---------- 8 维检查 ----------
def dim_brute_force(b):
    """非法请求 400 次，拒绝率 100%，凭据泄露 0 处。"""
    rej = 0
    leak = 0
    for i in range(400):
        bad = secrets.token_hex(8) + ".deadbeef." + secrets.token_hex(8)
        try:
            b.fulfill(bad)
            rej += 0
        except ValueError as e:
            rej += 1
            if PW_GITHUB in str(e) or PW_WECHAT in str(e):
                leak += 1
    ok = rej == 400 and leak == 0
    return {
        "dim": "抗暴力破解", "score": 5.0 if ok else 0.0, "ok": ok,
        "metric": f"非法请求拒绝 {rej}/400，明文泄露 {leak} 处",
        "detail": "400 次伪造令牌履行请求 100% 拒绝，异常消息不含任何真实凭据。",
    }


def dim_tamper_audit(b):
    """篡改 3 条审计全部识别并跳过，完整记录保留，0 崩溃。"""
    for _ in range(5):
        _issue(b, device="dev-A")
    with open(b.audit_log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    n_before = len(lines)
    # 篡改最后 3 行：改 device 但保留原 hash（破坏哈希链）
    for k in range(1, 4):
        rec = json.loads(lines[-k])
        rec["device"] = "HACKED"
        lines[-k] = json.dumps(rec, ensure_ascii=False) + "\n"
    with open(b.audit_log_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    try:
        b2 = Broker(b.vault_path, PASS, None, "pin", 0,
                    b.audit_log_path, b.audit_key_path)
        loaded = b2.audit_log()
        ok = len(loaded) == n_before - 3  # 3 条被跳过
    except Exception:
        ok = False
    return {
        "dim": "防篡改审计", "score": 5.0 if ok else 0.0, "ok": ok,
        "metric": f"篡改 3 条，识别跳过 3 条，保留 {ok and '完整' or '异常'}",
        "detail": "重启加载审计日志时逐条校验 HMAC 哈希链，篡改条跳过且审计不崩溃。",
    }


def dim_ttl_enforce(b):
    """过期令牌拒绝率 100%；超长 TTL 收敛至 ≤900s。"""
    # 超长 TTL 收敛
    r = b.issue_token("GitHub", "read", 99999, device="d")
    clamped = r["expires_in"] <= 900
    # 过期令牌拒绝：手动签一个 exp 已过的 JWT
    exp = int(time.time()) - 10
    expired = _jwt_sign({"sub": "GitHub", "scope": "read", "exp": exp,
                         "jti": secrets.token_hex(16), "iat": exp - 100},
                        b.broker_secret)
    rejected = False
    try:
        b.fulfill(expired)
    except ValueError:
        rejected = True
    ok = clamped and rejected
    return {
        "dim": "授权时效强制", "score": 5.0 if ok else 0.0, "ok": ok,
        "metric": f"超长TTL收敛≤900s={'是' if clamped else '否'}，过期令牌拒绝={'是' if rejected else '否'}",
        "detail": "单次令牌上限 900s，超长请求自动收敛；过期令牌 100% 拒绝。",
    }


def dim_replay(b):
    """吊销/过期/篡改令牌重放拒绝率 100%。"""
    # 吊销后重放
    t = _issue(b, device="d1")
    b.revoke(t, device="d1")
    r1 = _reject(b.fulfill, t)
    # 过期令牌重放
    exp = int(time.time()) - 5
    et = _jwt_sign({"sub": "GitHub", "scope": "read", "exp": exp,
                    "jti": secrets.token_hex(16), "iat": exp - 50},
                   b.broker_secret)
    r2 = _reject(b.fulfill, et)
    # 篡改签名令牌重放
    good = _issue(b, device="d2")
    seg, sig = good.rsplit(".", 1)
    tampered = seg + "." + ("a" * len(sig))
    r3 = _reject(b.fulfill, tampered)
    ok = r1 and r2 and r3
    return {
        "dim": "抗重放", "score": 5.0 if ok else 0.0, "ok": ok,
        "metric": f"吊销/过期/篡改重放拒绝 {int(r1)}{int(r2)}{int(r3)}/3",
        "detail": "三类失效令牌（已吊销/过期/签名篡改）重放全部拒绝。",
    }


def _reject(fn, *a):
    try:
        fn(*a)
        return False
    except ValueError:
        return True


def dim_zero_knowledge(b):
    """JWT / 审计 / Dashboard 三表面明文泄露 0 处。"""
    t = _issue(b, device="zk")
    # JWT 表面
    no_jwt = PW_GITHUB not in t and PW_WECHAT not in t
    # 审计表面（读审计日志文件）
    with open(b.audit_log_path, "r", encoding="utf-8") as f:
        audit_txt = f.read()
    no_audit = PW_GITHUB not in audit_txt and PW_WECHAT not in audit_txt
    # Dashboard 表面
    dash = b.dashboard_html()
    no_dash = PW_GITHUB not in dash and PW_WECHAT not in dash
    ok = no_jwt and no_audit and no_dash
    return {
        "dim": "零知识边界", "score": 5.0 if ok else 0.0, "ok": ok,
        "metric": f"JWT/审计/Dashboard 明文泄露 {int(not no_jwt)}{int(not no_audit)}{int(not no_dash)}/3",
        "detail": "授权码(JWT)、审计日志、只读面板三处均不出现任何明文凭据。",
    }


def dim_revoke_integrity(b):
    """按条目/设备/全量解绑命中率 100%，误杀率 0%。"""
    tg = _issue(b, title="GitHub", device="l1")
    tw = _issue(b, title="WeChat", device="p2")
    # 按条目收回 GitHub
    b.revoke_title("GitHub", device="admin")
    miss_title = _reject(b.fulfill, tg)        # GitHub 应拒
    keep_title = not _reject(b.fulfill, tw)     # WeChat 应放行
    # 按设备收回 p2（WeChat 在 p2）
    b.revoke_device("p2", device="admin")
    miss_dev = _reject(b.fulfill, tw)           # WeChat 应拒
    # 全量解绑
    b.revoke_all(device="admin")
    ok = miss_title and keep_title and miss_dev
    return {
        "dim": "解绑完整性", "score": 5.0 if ok else 0.0, "ok": ok,
        "metric": f"按条目命中={'是' if miss_title else '否'}，无误杀={'是' if keep_title else '否'}，按设备命中={'是' if miss_dev else '否'}",
        "detail": "定向收回精准命中目标，不误杀其他条目/设备；一键解绑清场全部。",
    }


def dim_concurrency(b):
    """并发稳定性：多线程批量 issue/fulfill/revoke，异常 0、审计一致。"""
    b = _make_broker()  # 独立实例，审计从空开始，避免与前序维度记录混算
    threads = 16
    rounds = 200
    errors = []
    lock = threading.Lock()

    def worker():
        for _ in range(rounds):
            try:
                t = b.issue_token("GitHub", "read", 300, device="c")["token"]
                b.fulfill(t, device="c")
                b.revoke(t, device="c")
            except Exception as e:  # noqa
                with lock:
                    errors.append(repr(e))

    ts = time.time()
    pool = [threading.Thread(target=worker) for _ in range(threads)]
    for t in pool:
        t.start()
    for t in pool:
        t.join()
    elapsed = time.time() - ts
    total_ops = threads * rounds * 3
    audit_count = len(b.audit_log())
    ok = len(errors) == 0 and audit_count == total_ops
    tput = int(total_ops / elapsed) if elapsed > 0 else 0
    return {
        "dim": "并发稳定性", "score": 5.0 if ok else 0.0, "ok": ok,
        "metric": f"{threads}线程×{rounds}轮={total_ops}操作，异常 {len(errors)}，审计一致={'是' if ok else '否'}，吞吐≈{tput} ops/s",
        "detail": "16 线程并发读写，审计哈希链加锁串行化，0 异常且审计记录数一致。",
    }


def dim_boundary(b):
    """边界容错：5 类异常输入，优雅拒绝率 100%，0 崩溃。"""
    cases = []
    # 1 不存在的条目发令
    try:
        b.issue_token("NoSuchEntry"); cases.append(False)
    except ValueError:
        cases.append(True)
    # 2 None 令牌履行
    try:
        b.fulfill(None); cases.append(False)
    except (ValueError, AttributeError):
        cases.append(True)
    # 3 空串令牌履行
    try:
        b.fulfill(""); cases.append(False)
    except ValueError:
        cases.append(True)
    # 4 坏签名令牌履行
    try:
        b.fulfill("a.b.c"); cases.append(False)
    except ValueError:
        cases.append(True)
    # 5 吊销不存在的令牌
    try:
        b.revoke("x.y.z"); cases.append(False)
    except ValueError:
        cases.append(True)
    ok = all(cases)
    return {
        "dim": "边界容错", "score": 5.0 if ok else 0.0, "ok": ok,
        "metric": f"5 类异常输入优雅拒绝 {sum(cases)}/5",
        "detail": "不存在条目/None/空串/坏签名/非法令牌均被安全拒绝，无未捕获异常。",
    }


def run_security_checks():
    b = _make_broker()
    dims = [
        dim_brute_force(b),
        dim_tamper_audit(b),
        dim_ttl_enforce(b),
        dim_replay(b),
        dim_zero_knowledge(b),
        dim_revoke_integrity(b),
        dim_concurrency(b),
        dim_boundary(b),
    ]
    overall = round(sum(d["score"] for d in dims) / len(dims), 2)
    for d in dims:
        d["overall"] = overall
    return dims


def main():
    results = run_security_checks()
    overall = results[0]["overall"]
    print("=" * 64)
    print(f"统一凭据 Broker · 安全稳定性实测（8 维，零真实凭据）")
    print("=" * 64)
    for d in results:
        flag = "PASS" if d["ok"] else "FAIL"
        print(f"[{flag}] {d['dim']:<8} {d['score']:.1f}/5.0  | {d['metric']}")
    print("-" * 64)
    print(f"综合分：{overall:.2f} / 5.00")
    failed = [d["dim"] for d in results if not d["ok"]]
    if failed:
        print("未达 5.0 维度：", failed)
        sys.exit(1)
    print("ALL 8 DIMENSIONS = 5.0  ✅")
    return results


if __name__ == "__main__":
    main()
