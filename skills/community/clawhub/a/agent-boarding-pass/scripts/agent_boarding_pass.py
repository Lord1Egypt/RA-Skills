# -*- coding: utf-8 -*-
"""智能体登机牌：给任何 AI 智能体签发一张可验证的『登机牌』。零依赖。

一张登机牌 = 身份（有籍）+ 证据哈希（有证）+ 权限白名单/有效期（有门禁）。
签发铁律：三律证据缺任一律 → 拒绝签发（rc=1）。
可整张贴进 system prompt / 仓库 / 工单，接收方一条命令验真。

用法：
  签发：python agent_boarding_pass.py --agent research-bot \
          --evidence l1-registered=passport.json l2-evidence=chain.jsonl l3-gate=gate.json \
          --allow search summarize write_draft --ttl 24 --out pass.json
  验真：python agent_boarding_pass.py --verify pass.json
"""
import argparse, datetime, hashlib, json, pathlib, sys

LAW_PREFIX = ("l1-", "l2-", "l3-")


def sha256_of(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def load_evidence_ref(p: str) -> str:
    q = p[1:] if p.startswith("@") else p
    if pathlib.Path(q).is_file():
        return sha256_of(pathlib.Path(q).read_text(encoding="utf-8-sig"))
    return sha256_of(p)


def issue(a):
    ev, laws_hit = {}, set()
    for item in a.evidence:
        if "=" not in item:
            print(f"证据格式错误（应为 key=value）：{item}", file=sys.stderr)
            sys.exit(2)
        k, v = item.split("=", 1)
        if not k.startswith(LAW_PREFIX):
            print(f"证据键须以 l1-/l2-/l3- 开头：{k}", file=sys.stderr)
            sys.exit(2)
        ev[k] = load_evidence_ref(v)
        laws_hit.add(k[:3])
    missing = [l for l in ("l1-", "l2-", "l3-") if l not in laws_hit]
    if missing:
        msg = "⛔ 拒绝签发：三律证据缺失（" + "、".join(missing) + "）"
        print(json.dumps({"issued": False, "agent": a.agent, "missing": missing,
                          "note": msg}, ensure_ascii=False, indent=2) if a.json else msg)
        sys.exit(1)

    now = datetime.datetime.now()
    expires = (now + datetime.timedelta(hours=a.ttl)).isoformat(timespec="seconds")
    card = {
        "pass_type": "lgd-agent-boarding-pass",
        "agent": a.agent,
        "issued_at": now.isoformat(timespec="seconds"),
        "expires_at": expires,
        "allow": a.allow or [],
        "evidence_sha256": ev,
    }
    card["fingerprint"] = sha256_of(json.dumps(card, ensure_ascii=False, sort_keys=True))
    if a.out:
        outp = pathlib.Path(a.out)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(json.dumps(card, ensure_ascii=False, indent=2), encoding="utf-8")
    if a.json:
        print(json.dumps({"issued": True, "card": card, "out": a.out},
                         ensure_ascii=False, indent=2))
    else:
        print("✅ 已签发登机牌：" + a.agent)
        print("  有效期至：" + expires + f"（ttl={a.ttl}h）")
        print("  允许动作：" + (", ".join(card["allow"]) or "（未列，视为只读）"))
        print("  证据：" + str(len(ev)) + " 条（三律齐备）  指纹：" + card["fingerprint"][:16] + "…")
        if a.out:
            print("  登机牌文件：" + a.out)
    sys.exit(0)


def verify(a):
    p = a.verify
    q = p[1:] if p.startswith("@") else p
    try:
        if pathlib.Path(q).is_file():
            raw = pathlib.Path(q).read_text(encoding="utf-8-sig")
        else:
            raw = p
        card = json.loads(raw)
    except (json.JSONDecodeError, OSError) as e:
        print(f"登机牌不可读/非 JSON：{e}", file=sys.stderr)
        sys.exit(2)

    checks = []
    miss = [k for k in ("pass_type", "agent", "issued_at", "expires_at",
                        "allow", "evidence_sha256", "fingerprint") if k not in card]
    checks.append(("结构完整", not miss, "缺失字段: " + ",".join(miss) if miss else "字段齐全"))

    body = {k: card[k] for k in ("pass_type", "agent", "issued_at", "expires_at",
                                 "allow", "evidence_sha256") if k in card}
    checks.append(("指纹防篡改",
                   bool(card.get("fingerprint")) and sha256_of(json.dumps(body, ensure_ascii=False, sort_keys=True)) == card.get("fingerprint"),
                   "重算一致" if checks and sha256_of(json.dumps(body, ensure_ascii=False, sort_keys=True)) == card.get("fingerprint") else "不一致（已被篡改或非本体系签发）"))

    try:
        expired = datetime.datetime.now() > datetime.datetime.fromisoformat(card.get("expires_at", "2000-01-01T00:00:00"))
    except ValueError:
        expired = True
    checks.append(("未过期", not expired, "有效期至 " + str(card.get("expires_at"))))

    ok = all(c[1] for c in checks)
    if a.json:
        print(json.dumps({"verified": ok, "agent": card.get("agent"),
                          "allow": card.get("allow"),
                          "checks": [{"name": n, "pass": pp, "note": t} for n, pp, t in checks]},
                         ensure_ascii=False, indent=2))
    else:
        print(("✅ 验真通过：" if ok else "⛔ 验真失败：") + str(card.get("agent")))
        for n, pp, t in checks:
            print(f"  {'✅' if pp else '⛔'} {n}：{t}")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser(description="智能体登机牌 · 智能体三律便携证件")
    sub = ap.add_mutually_exclusive_group(required=True)
    sub.add_argument("--agent", help="签发：智能体标识")
    sub.add_argument("--verify", help="验真：登机牌 JSON（内联 / @文件 / 纯路径）")
    ap.add_argument("--evidence", nargs="+", help="证据键值（键须以 l1-/l2-/l3- 开头）")
    ap.add_argument("--allow", nargs="*", default=[], help="允许动作白名单")
    ap.add_argument("--ttl", type=int, default=72, help="有效时长（小时，默认 72）")
    ap.add_argument("--out", help="登机牌输出路径")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.agent:
        if not a.evidence:
            print("签发需 --evidence（三律证据 key=value）", file=sys.stderr)
            sys.exit(2)
        issue(a)
    else:
        verify(a)


if __name__ == "__main__":
    main()
