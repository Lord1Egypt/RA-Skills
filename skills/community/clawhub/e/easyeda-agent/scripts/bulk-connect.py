#!/usr/bin/env python3
"""bulk-connect — 连接 spec 驱动的整页电气实现 + 期望网表验证门 + 悬空脚修复循环。

用法:
    EASYEDA_PROJECT=<工程名> bulk-connect.py <spec.json>                 # 执行 + 验证
    EASYEDA_PROJECT=<工程名> bulk-connect.py <spec.json> --verify-only   # 只验证
    EASYEDA_PROJECT=<工程名> bulk-connect.py <spec.json> --repair-floaters  # 悬空脚重连循环

spec 形状:
    {
      "page":  "P1_POWER",
      "rails": [ {"pin": "C4:1", "kind": "power", "net": "+5V"},
                 {"pin": "C4:2", "kind": "gnd",   "net": "GND"} ],
      "ports": [ {"pin": "R4:2", "net": "U2_FB"} ],
      "nc":    { "U3": ["15", "9"] }
    }

策略（box-v2 / 51 件整页实测收敛，2026-07-09）:
- **全部连接走 pin→短桩→netflag/netport**（autoconnect），内部信号网起可读网名
  （U2_FB / SW1 …）用 netport 同名互连。**不要用长导线连远脚**——器件按行列
  排布时长线极易与同行引脚/其他线共线，EasyEDA 把共线相触导线合并成一条 →
  大面积隐性短路（实测两次全页短接，见 issue #64）。
- 验证只信数据：`sch read` 把每个 spec 组（rail/port 同名成员）读回真实 net，
  不一致逐条列出；`sch check --json` 使用统一信封，findings 位于
  `result.findings`。所有 sch 命令都用 `--doc <page>` 固定目标页。
- `--repair-floaters`: 从 sch check 的 floating-pin(pinDetails 带坐标) 出发，按
  spec 决定 kind/net，交给 typed `sch autoconnect` 的活体几何评分器选择方向和偏移。
  循环直到无悬空或不再收敛。
"""
import json
import os
import subprocess
import sys
import time

PROJECT = os.environ.get("EASYEDA_PROJECT", "")
PAGE = ""


def run(args, timeout=120, retries=3):
    proj = ["--project", PROJECT] if PROJECT else []
    doc = ["--doc", PAGE] if PAGE and args and args[0] == "sch" else []
    for attempt in range(retries):
        # encoding 固定 utf-8:easyeda CLI 输出恒为 UTF-8,text=True 在 Windows
        # 中文环境会用系统 GBK 解码而崩溃(issue #133 Bug 4)
        p = subprocess.run(["easyeda"] + proj + doc + args, capture_output=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        if p.returncode == 0 or attempt == retries - 1:
            return p.returncode, p.stdout, p.stderr
        time.sleep(1.5)
    return 1, "", "unreachable"


def jparse(out):
    try:
        return json.loads(out)
    except Exception:
        i = out.find("{")
        try:
            return json.JSONDecoder().raw_decode(out[i:])[0]
        except Exception:
            return {}


def result_payload(data):
    """Return the current CLI envelope payload; tolerate pre-v0.10 bare fixtures."""
    result = data.get("result")
    if isinstance(result, dict):
        return result
    if data.get("summary") is not None or data.get("findings") is not None:
        return data
    return {}


def settle(page, timeout_s=15):
    rc, out, _ = run(["doc", "switch", page])
    if rc != 0:
        raise SystemExit(f"doc switch {page} failed")
    prev = -1
    for _ in range(int(timeout_s / 1.5)):
        rc, out, _ = run(["sch", "list"])
        n = len([c for c in (jparse(out).get("result") or {}).get("components", [])
                 if c.get("componentType") == "part"])
        if n and n == prev:
            return n
        prev = n
        time.sleep(1.5)
    return prev


def check_findings(max_tries=5):
    """Read result.findings from the CLI envelope, retrying page-settle races."""
    for _ in range(max_tries):
        rc, out, _ = run(["sch", "check", "--json"])
        d = result_payload(jparse(out))
        if d.get("summary") is not None:
            return d
        time.sleep(2.5)
    return {}


def verify(spec):
    rc, out, _ = run(["sch", "read"], 240)
    r = jparse(out).get("result") or {}
    pin2net = {}
    for c in r.get("components", []):
        for p in c.get("pins", []):
            pin2net[f"{c.get('designator')}:{p.get('number')}"] = p.get("net")
    bad = []
    for rail in spec.get("rails", []):
        n = pin2net.get(rail["pin"])
        if n != rail["net"]:
            bad.append(f"RAIL {rail['pin']} expect {rail['net']} got {n}")
    for port in spec.get("ports", []):
        n = pin2net.get(port["pin"])
        if n != port["net"]:
            bad.append(f"PORT {port['pin']} expect {port['net']} got {n}")
    floats = r.get("floatingPins") or []
    print(f"VERIFY: {len(bad)} group problems; floatingPins={len(floats)} {floats[:8]}")
    for b in bad[:30]:
        print("  !", b)
    return not bad


def repair_floaters(spec):
    pin_net = {}
    for r in spec.get("rails", []):
        pin_net[r["pin"]] = ({"gnd": "gnd", "power": "power"}.get(r["kind"], r["kind"]), r["net"])
    for p in spec.get("ports", []):
        pin_net[p["pin"]] = ("netport", p["net"])
    nc = {f"{d}:{n}" for d, pl in (spec.get("nc") or {}).items() for n in pl}
    for rnd in range(4):
        d = check_findings()
        fl = []
        for f in d.get("findings", []):
            if f.get("type") == "floating-pin":
                for pd in f.get("pinDetails", []):
                    ref = f"{f.get('designator')}:{pd.get('number')}"
                    if ref not in nc:
                        fl.append((ref, pd.get("x"), pd.get("y")))
        print(f"repair round{rnd}: floating={len(fl)}")
        if not fl:
            return True
        progressed = False
        for ref, _, _ in fl:
            if ref not in pin_net:
                print("  no-spec:", ref)
                continue
            kind, net = pin_net[ref]
            rc, out, err = run(["sch", "autoconnect", "--pin", ref,
                                "--kind", kind, "--net", net, "--json"])
            state = (jparse(out).get("result") or {}).get("state")
            ok = rc == 0
            print(f"  {ref} -> {net}: {state or ('ok' if ok else 'FAIL')}")
            if not ok and err:
                print("   ", err.strip())
            progressed = progressed or ok
        run(["sch", "save"])
        if not progressed:
            return False
        time.sleep(2)
    return False


def main():
    global PAGE
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    PAGE = spec["page"]
    mode = sys.argv[2] if len(sys.argv) > 2 else ""
    settle(PAGE)

    if mode == "--repair-floaters":
        ok = repair_floaters(spec)
        verify(spec)
        sys.exit(0 if ok else 1)

    if mode != "--verify-only":
        conns = [dict(pin=r["pin"], kind=r["kind"], net=r["net"]) for r in spec.get("rails", [])]
        conns += [dict(pin=p["pin"], kind="netport", net=p["net"]) for p in spec.get("ports", [])]
        if conns:
            acspec = {"connections": conns,
                      "rules": {"avoidTitleBlock": True, "avoidPinFanout": True,
                                "staggerLabels": True, "offsetRange": [18, 80],
                                "offsetStep": 6, "minLabelGap": 12}}
            fn = f"/tmp/ac_{spec['page']}.json"
            json.dump(acspec, open(fn, "w", encoding="utf-8"), ensure_ascii=False)
            rc, out, err = run(["sch", "autoconnect", "--spec", fn, "--json"], 600)
            res = jparse(out).get("result") or {}
            results = res.get("results") or res.get("connections") or []
            states = {}
            for r0 in results:
                st = r0.get("state") or r0.get("status") or ("ok" if r0.get("selected") else "?")
                states[st] = states.get(st, 0) + 1
            print(f"autoconnect: {len(conns)} requested ->", states)
            run(["sch", "save"])
        for des, pl in (spec.get("nc") or {}).items():
            run(["sch", "no-connect", "--designator", des, "--pin", ",".join(pl)])
        run(["sch", "save"])

    ok = verify(spec)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
