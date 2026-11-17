#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_vault.py — 统一凭据保险库 安全稳定性实测（可量化 · 零真实凭据 · 本地闭环）

覆盖 TRACE 安全实测雷达 8 维，逐维给出 0-5 评分与量化证据，输出 security_results.json。
原则：注入假数据、本地闭环、可重复重跑。配套 gen_security_radar.py 生成雷达图。

用法：
  python tools/test_vault.py                 # 跑全部测试，写 security_results.json
  python tools/test_vault.py --print         # 同时打印结果
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import vault as V  # noqa: E402

MASTER = "Master-Test-Pass-2026!"
RECOVERY = "Rk3y-" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ012345"  # 固定恢复密钥（仅测试）
RESULTS = HERE / "security_results.json"


def _new_vault(tmp: Path):
    v = V.Vault(tmp)
    v.data = {
        "version": 1, "kdf": "pbkdf2-sha256", "kdf_iterations": V.KDF_ITERS,
        "kek_salt": V.b64e(os.urandom(16)), "recovery_salt": V.b64e(os.urandom(16)),
        "recovery_wrap": "", "entries": {}, "audit": [],
    }
    kek = V.derive_kek(MASTER, V.b64d(v.data["kek_salt"]))
    rkek = V.derive_kek(RECOVERY, V.b64d(v.data["recovery_salt"]))
    v.data["recovery_wrap"] = V.b64e(V.aes_seal(rkek, kek))
    v.append_audit("init", "(test)")
    v._seal_and_save(kek)
    return v, kek


def _open_ok(tmp: Path):
    v = V.Vault(tmp)
    v.data = json.loads(v.path.read_text("utf-8"))
    kek = v.kek_from_password(MASTER)
    v.load(kek)
    return v, kek


# ----------------------------- 1. 抗暴力破解 -----------------------------
def t_bruteforce(tmp: Path):
    _new_vault(tmp)
    attempts, accepted = 30, 0
    for i in range(attempts):
        try:
            v = V.Vault(tmp)
            v.data = json.loads(v.path.read_text("utf-8"))
            kek = v.kek_from_password(f"wrong-{i}")
            v.load(kek)  # 错口令 → file_mac 不符 → 抛 TamperError
            accepted += 1
        except V.VaultError:
            pass
    score = 5.0 if accepted == 0 else max(0.0, 5.0 * (1 - accepted / attempts))
    return score, {"attempts": attempts, "accepted": accepted,
                   "reject_rate": f"{(attempts-accepted)/attempts*100:.0f}%"}


# ----------------------------- 2. 防篡改审计 -----------------------------
def t_tamper_audit(tmp: Path):
    _new_vault(tmp)
    v, kek = _open_ok(tmp)
    v.set_entry(kek, "a", "low", "u", "secret-a", "")
    v.set_entry(kek, "b", "low", "u", "secret-b", "")
    v._seal_and_save(kek)
    # 1) 整库篡改：改某条密文 → 重加载应被 file_mac 拒（TamperError）
    data = json.loads(v.path.read_text("utf-8"))
    ct = bytearray(V.b64d(data["entries"]["a"]["ct"]))
    ct[-1] ^= 0x01
    data["entries"]["a"]["ct"] = V.b64e(bytes(ct))
    v.path.write_text(json.dumps(data), "utf-8")
    whole_detected = False
    try:
        _open_ok(tmp)
    except V.TamperError:
        whole_detected = True
    # 2) 审计链篡改：仅改内存中审计记录 → verify_audit 应判 False（独立于 file_mac）
    v3 = V.Vault(tmp)
    v3.data = json.loads(v3.path.read_text("utf-8"))  # 不 load，仅取数据
    v3.data["audit"][0]["target"] = "HACKED"
    ok, bad = v3.verify_audit()
    audit_detected = (not ok) and bad == 1
    score = 5.0 if (whole_detected and audit_detected) else 0.0
    return score, {"whole_file_tamper_detected": whole_detected,
                   "audit_chain_tamper_detected": audit_detected}


# ----------------------------- 3. 授权时效 -----------------------------
def t_token_expiry(tmp: Path):
    _new_vault(tmp)
    v, kek = _open_ok(tmp)
    tok = v.issue_token(kek, "low", ttl=1)
    time.sleep(2.2)  # 明显越过 1s 时效
    res = v.verify_token(kek, tok)
    score = 5.0 if (res["valid"] is False and res.get("reason") == "已过期") else 0.0
    return score, {"valid_after_expiry": res["valid"], "reason": res.get("reason")}


# ----------------------------- 4. 抗重放 / 越权 -----------------------------
def t_anti_replay(tmp: Path):
    _new_vault(tmp)
    v, kek = _open_ok(tmp)
    tok = v.issue_token(kek, "low", ttl=900)
    # 篡改签名段
    p, s = tok.split(".")
    bad = p + "." + ("A" + s[1:])
    r1 = v.verify_token(kek, bad)
    # 越权：low 令牌不能访问 high 条目
    grant_low_to_high = V.Vault.token_grants("low", "high")
    grant_high_to_low = V.Vault.token_grants("high", "low")
    ok = (r1["valid"] is False and r1.get("reason", "").startswith("签名")
          and grant_low_to_high is False and grant_high_to_low is True)
    score = 5.0 if ok else 0.0
    return score, {"tampered_token_rejected": r1["valid"] is False,
                   "low_cannot_access_high": grant_low_to_high is False,
                   "high_can_access_low": grant_high_to_low is True}


# ----------------------------- 5. 零知识边界 -----------------------------
def t_zero_knowledge(tmp: Path):
    _new_vault(tmp)
    v, kek = _open_ok(tmp)
    v.set_entry(kek, "github", "high", "demo-user", "ZERO_KNOWLEDGE_SECRET_VALUE", "2FA")
    v._seal_and_save(kek)
    raw = v.path.read_bytes()
    leaks = [s for s in (b"ZERO_KNOWLEDGE_SECRET_VALUE", b"demo-user", b"2FA") if s in raw]
    score = 5.0 if not leaks else 0.0
    return score, {"plaintext_leaks_in_file": leaks}


# ----------------------------- 6. 解绑完整性 -----------------------------
def t_unbind(tmp: Path):
    _new_vault(tmp)
    v, kek = _open_ok(tmp)
    v.set_entry(kek, "db", "high", "u", "v", "")
    v._seal_and_save(kek)
    before = len(v.list_entries())
    v.delete_entry(kek, "db")
    v._seal_and_save(kek)
    after = len(v.list_entries())
    # 恢复密钥可解锁（可恢复不锁死）
    v2 = V.Vault(tmp)
    v2.data = json.loads(v2.path.read_text("utf-8"))
    recovered_ok = True
    try:
        rkek = v2.kek_from_recovery(RECOVERY)
        v2.load(rkek)
    except Exception:
        recovered_ok = False
    score = 5.0 if (before == 1 and after == 0 and recovered_ok) else 0.0
    return score, {"entries_before": before, "entries_after_delete": after,
                   "recovery_unlock_ok": recovered_ok}


# ----------------------------- 7. 并发稳定性 -----------------------------
def t_concurrency(tmp: Path):
    _new_vault(tmp)
    lock = threading.Lock()
    errors = []
    n = 20

    def worker(i):
        try:
            with lock:
                v, kek = _open_ok(tmp)
                v.set_entry(kek, f"k{i}", "low", "u", f"v{i}", "")
                v._seal_and_save(kek)
        except Exception as e:
            errors.append(str(e))

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    v, kek = _open_ok(tmp)
    ok, _ = v.verify_audit()
    final_count = len(v.list_entries())
    score = 5.0 if (not errors and ok and final_count == n) else max(0.0, 5.0 * (final_count / n))
    return score, {"threads": n, "errors": len(errors),
                   "final_entries": final_count, "audit_intact": ok}


# ----------------------------- 8. 边界容错 -----------------------------
def _args(home, **kw):
    a = argparse.Namespace(home=home, password=None)
    for k, val in kw.items():
        setattr(a, k, val)
    return a


def t_boundary(tmp: Path):
    cases = {}
    # 短口令 init（真实命令路径）→ 应拒绝，不崩溃
    try:
        V.cmd_init(_args(tmp / "b1", force=True, recovery_key=RECOVERY, password="short"))
        cases["short_password_accepted"] = True
    except V.VaultError:
        cases["short_password_accepted"] = False
    # 读不存在条目 → 应友好报错
    _new_vault(tmp)
    try:
        V.cmd_get(_args(tmp, password=MASTER, label="nope"))
        cases["unknown_entry_crash"] = True
    except V.VaultError:
        cases["unknown_entry_crash"] = False
    # 损坏文件 → 应友好报错，不抛栈
    _new_vault(tmp)
    V.Vault(tmp).path.write_text("{not json", "utf-8")
    try:
        V.cmd_status(_args(tmp, password=MASTER))
        cases["corrupt_file_crash"] = True
    except V.VaultError:
        cases["corrupt_file_crash"] = False
    ok = (cases["short_password_accepted"] is False and cases["unknown_entry_crash"] is False
          and cases["corrupt_file_crash"] is False)
    score = 5.0 if ok else 0.0
    return score, cases


DIMENSIONS = [
    ("抗暴力破解", "bruteforce", t_bruteforce),
    ("防篡改审计", "tamper_audit", t_tamper_audit),
    ("授权时效", "token_expiry", t_token_expiry),
    ("抗重放", "anti_replay", t_anti_replay),
    ("零知识边界", "zero_knowledge", t_zero_knowledge),
    ("解绑完整性", "unbind", t_unbind),
    ("并发稳定性", "concurrency", t_concurrency),
    ("边界容错", "boundary", t_boundary),
]


def run_all(verbose=False):
    out = {"tool": "vault.py", "scheme": "PBKDF2-SHA256(600k)+AES-256-GCM+HMAC",
           "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
           "dimensions": [], "overall": 0.0}
    total = 0.0
    for name, key, fn in DIMENSIONS:
        try:
            with tempfile.TemporaryDirectory() as tmp:
                t0 = time.time()
                score, detail = fn(Path(tmp))
        except Exception as e:  # 单维异常不拖垮整体，仍记录
            score, detail = 0.0, {"error": f"{type(e).__name__}: {e}"}
            t0 = time.time()
        total += score
        out["dimensions"].append({"name": name, "key": key, "score": round(score, 2),
                                  "max": 5.0, "detail": detail,
                                  "elapsed_ms": round((time.time() - t0) * 1000, 1)})
        if verbose:
            print(f"  [{score:>4.1f}/5] {name:<8} {detail}", flush=True)
    out["overall"] = round(total / len(DIMENSIONS), 2)
    RESULTS.write_text(json.dumps(out, ensure_ascii=False, indent=2), "utf-8")
    if verbose:
        print(f"\n综合：{out['overall']:.2f}/5  → {RESULTS}", flush=True)
    return out


if __name__ == "__main__":
    res = run_all(verbose="--print" in sys.argv)
    sys.exit(0 if res["overall"] >= 4.5 else 1)
