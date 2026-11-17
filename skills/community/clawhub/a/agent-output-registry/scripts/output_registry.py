# -*- coding: utf-8 -*-
"""agent-output-registry · AI 产出有籍登记器 v1.0（LGD-I 有籍实例化）
=========================================================================
痛点：AI 产出满天飞，却无溯源、无 IP 归属、审计时找不到"这是谁、用哪个模型、哪版提示生成的"。
解法：给每条 AI 产出发一张"籍"（户口）——SHA-256 指纹 + 模型/版本/提示哈希 + 时间戳 + 血缘 + 权属。
登记即"有籍"：可 verify 证完整性、可 lookup 查归属。

命令：
  add     --out 文件或文本  --model 名 --version 版 --prompt "提示" [--issuer 权属人] [--license 许可]
         → 写入台账，返回籍号 LGD-REG-xxxxxxxx
  verify  --id 籍号 --out 文件  → 重算哈希，比对台账，证明"此产出即彼产出"
  lookup  --id 籍号            → 查某条籍
  report                     → 列出全部籍

零依赖（纯 stdlib）。产物落 ./registry/（md+csv+jsonl）。
© SynomosAI · LGD-Powered
"""
import argparse, csv, hashlib, json, os, sys, datetime as dt

REG_DIR = "registry"
NOW = lambda: dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")


def sha256_text(t):
    return "sha256:" + hashlib.sha256(t.encode("utf-8")).hexdigest()


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(65536), b""):
            h.update(ch)
    return "sha256:" + h.hexdigest()


def load():
    p = os.path.join(REG_DIR, "registry.jsonl")
    if not os.path.exists(p):
        return []
    return [json.loads(l) for l in open(p, encoding="utf-8-sig") if l.strip()]


def save(rows):
    os.makedirs(REG_DIR, exist_ok=True)
    p = os.path.join(REG_DIR, "registry.jsonl")
    with open(p, "w", encoding="utf-8-sig") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    # csv
    with open(os.path.join(REG_DIR, "registry.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["籍号", "时间", "模型", "版本", "产出指纹", "提示哈希", "权属人", "许可", "摘要"])
        for r in rows:
            w.writerow([r["id"], r["ts"], r["model"], r["version"], r["out_hash"][:19],
                        r["prompt_hash"][:19], r.get("issuer", ""), r.get("license", ""), r.get("summary", "")])
    # md
    with open(os.path.join(REG_DIR, "registry.md"), "w", encoding="utf-8") as f:
        f.write("# AI 产出有籍台账（LGD-I 有籍）\n\n")
        for r in rows:
            f.write(f"- **{r['id']}** {r['ts']} 模型={r['model']} v{r['version']} "
                    f"权属={r.get('issuer','')} 许可={r.get('license','')}\n")
            f.write(f"  - 产出指纹 `{r['out_hash'][:32]}…` 提示哈希 `{r['prompt_hash'][:32]}…`\n")


def cmd_add(a):
    if not a.out:
        print("[!] add 需要 --out（文件路径或直接在 --out 后跟文本）", file=sys.stderr); sys.exit(2)
    if os.path.isfile(a.out):
        out_text = open(a.out, encoding="utf-8-sig", errors="replace").read()
        out_hash = sha256_file(a.out)
        summary = out_text[:60].replace("\n", " ")
    else:
        out_text = a.out
        out_hash = sha256_text(a.out)
        summary = a.out[:60]
    prompt_hash = sha256_text(a.prompt or "")
    rid = "LGD-REG-" + out_hash[7:15]
    row = {"id": rid, "ts": NOW(), "model": a.model or "未知", "version": a.version or "未知",
           "out_hash": out_hash, "prompt_hash": prompt_hash, "issuer": a.issuer or "",
           "license": a.license or "未声明", "summary": summary}
    rows = load()
    rows.append(row)
    save(rows)
    print(f"[✓] 有籍 · 已登记 → {rid}")
    print(f"    产出指纹={out_hash[:32]}…  提示哈希={prompt_hash[:32]}…")
    print(f"    模型={row['model']} v{row['version']}  权属={row['issuer']}  许可={row['license']}")
    print(f"    台账 → registry/registry.md | .csv | .jsonl")


def cmd_verify(a):
    rows = load()
    hit = next((r for r in rows if r["id"] == a.id), None)
    if not hit:
        print(f"[!] 籍号 {a.id} 不在台账中"); sys.exit(2)
    if not a.out or not os.path.isfile(a.out):
        print("[!] verify 需要 --out 指向待证文件"); sys.exit(2)
    cur = sha256_file(a.out)
    ok = cur == hit["out_hash"]
    print(f"[{'✓' if ok else '✗'}] 完整性校验：台账指纹={hit['out_hash'][:32]}…  当前={cur[:32]}…")
    print("    结论：" + ("产出一致，籍可证（有籍成立）" if ok else "不一致，产出已被改动或非负同条"))
    if not ok:
        sys.exit(1)


def cmd_lookup(a):
    rows = load()
    hit = next((r for r in rows if r["id"] == a.id), None)
    print(json.dumps(hit, ensure_ascii=False, indent=2) if hit else f"[!] 籍号 {a.id} 不存在")


def cmd_report():
    rows = load()
    if not rows:
        print("[i] 暂无登记（先跑 add）"); return
    for r in rows:
        print(f"{r['id']}  {r['ts']}  {r['model']} v{r['version']}  {r.get('issuer','')}  {r.get('summary','')}")


def main():
    ap = argparse.ArgumentParser(description="AI 产出有籍登记器（LGD-I）")
    sub = ap.add_subparsers(dest="cmd")
    pa = sub.add_parser("add"); pa.add_argument("--out", required=True); pa.add_argument("--model")
    pa.add_argument("--version"); pa.add_argument("--prompt", default=""); pa.add_argument("--issuer")
    pa.add_argument("--license")
    pv = sub.add_parser("verify"); pv.add_argument("--id", required=True); pv.add_argument("--out")
    pl = sub.add_parser("lookup"); pl.add_argument("--id", required=True)
    pr = sub.add_parser("report")
    a = ap.parse_args()
    if a.cmd == "add": cmd_add(a)
    elif a.cmd == "verify": cmd_verify(a)
    elif a.cmd == "lookup": cmd_lookup(a)
    elif a.cmd == "report": cmd_report()
    else:
        print("[!] 子命令：add / verify / lookup / report"); sys.exit(1)


if __name__ == "__main__":
    main()
