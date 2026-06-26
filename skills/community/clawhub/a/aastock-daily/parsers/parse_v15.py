import re
import sys

def is_cjk(c):
    return c and ord(c) > 0x3000

with open("/tmp/snapshot_current.txt") as f:
    lines = f.read().split("\n")

NAV = set(["X", "Telegram", "Sina Weibo", "Copy Link", "分享", "Email", "WeChat", "研报聚合", "订阅更新"])

for idx, l in enumerate(lines):
    if idx > 20 and l.strip().startswith("- text: PRO"):
        i = idx
        break

out = []
pb = []
disc = False
in_cell = False
cell_base = 0

def flush():
    global pb
    if pb:
        t = "".join(pb)
        if t.strip():
            out.append(t)
    pb = []

def add(t):
    global pb
    if not t:
        return
    if pb:
        lc = pb[-1][-1] if pb[-1] else ""
        if lc.isalpha() and t[0].isalpha():
            pb.append(" ")
        elif is_cjk(lc) and (is_cjk(t[0]) or t[0].isalpha()):
            pb.append(" ")
    pb.append(t)

def gi(l):
    return len(l) - len(l.lstrip())

def gc(l):
    s = l.strip()
    return s[2:] if s.startswith("- ") else s

while i < len(lines):
    raw = lines[i]
    if not raw.strip().startswith("- "):
        i += 1
        continue
    ind = gi(raw)
    cont = gc(raw)

    if in_cell and ind < cell_base:
        in_cell = False

    if cont.startswith("/url:"):
        i += 1
        continue
    if cont.startswith("text: PRO"):
        i += 1
        continue
    if re.match(r"^text:\s*\d{4}/\d{2}/\d{2}\s+", cont):
        i += 1
        continue
    if cont.startswith("button "):
        i += 1
        continue
    if cont.startswith("strong:") and "免责声明" in cont:
        disc = True
    if cont.startswith('link "分享"') and disc:
        break
    if any(cont.startswith(x) for x in ["figure", "blockquote", "list:", "table:", "rowgroup"]):
        i += 1
        continue

    if cont.startswith("cell "):
        in_cell = True
        cell_base = ind + 2
        i += 1
        continue

    if in_cell:
        i += 1
        continue

    mh = re.search(r'^heading\s+"([^"]+)"', cont)
    if mh:
        flush()
        out.append(mh.group(1))
        i += 1
        continue

    if cont.startswith("columnheader"):
        i += 1
        continue

    if cont.startswith("row "):
        flush()
        rt = cont[len('row "'):]
        if rt.endswith('"'):
            rt = rt[:-1]
        for suf in ['":', '"', '：']:
            if rt.endswith(suf):
                rt = rt[:-len(suf)].rstrip()
        rt_s = rt.strip()
        if rt_s == '查阅' or (rt_s.startswith('日期') and rt_s.endswith('披露来源')):
            i += 1; continue
        parts = [p.strip() for p in rt.split("  ") if p.strip()]
        if parts and parts[-1] == "查阅":
            parts = parts[:-1]
        if parts:
            out.append("\t".join(parts))
        i += 1
        continue

    ms = re.search(r"strong:\s*(.*)$", cont)
    if ms:
        st = ms.group(1).strip().strip("'\"")
        if st:
            flush()
            out.append(st)
        i += 1
        continue

    if cont.startswith("paragraph:"):
        txt = cont[len("paragraph:"):].strip().strip("'\"")
        if txt:
            add(txt)
            i += 1
        else:
            cb = ind + 2
            j = i + 1
            ct = []
            while j < len(lines):
                rj = lines[j].lstrip()
                ij = gi(lines[j])
                if ij < cb:
                    break
                if not rj.startswith("- "):
                    j += 1
                    continue
                cj = gc(lines[j])
                mt = re.match(r"^text:\s*(.*)", cj)
                if mt:
                    t = mt.group(1).strip().strip("'\"")
                    if t:
                        ct.append(t)
                    j += 1
                    continue
                mlk = re.search(r'^link\s+"([^"]+)"', cj)
                if mlk:
                    lt = mlk.group(1)
                    if lt not in NAV:
                        ct.append(lt)
                    j += 1
                    continue
                ms_strong = re.match(r"^strong:\s*(.*)$", cj)
                if ms_strong:
                    st = ms_strong.group(1).strip().strip("'\"")
                    if st: ct.append(st)
                    j += 1; continue
                if any(cj.startswith(x) for x in ["paragraph:", "blockquote", "figure", "list:", "cell ", "columnheader", "/url", "row "]):
                    break
                j += 1
            if ct:
                add("".join(ct))
            i = j
            continue

    mt = re.match(r"^text:\s*(.*)", cont)
    if mt:
        txt = mt.group(1).strip().strip("'\"")
        if txt and len(txt) > 1:
            add(txt)
        i += 1
        continue

    ml = re.search(r'^link\s+"([^"]+)"', cont)
    if ml:
        lt = ml.group(1)
        if lt not in NAV:
            add(lt)
        i += 1
        continue

    if cont.startswith("listitem:"):
        flush()
        li = cont[len("listitem:"):].strip()
        if not li:
            base = ind + 2
            j = i + 1
            items = []
            ibuf = []
            ist = False
            while j < len(lines):
                rj = lines[j].lstrip()
                ij = gi(lines[j])
                if ij < base:
                    break
                if not rj.startswith("- "):
                    j += 1
                    continue
                cj = gc(lines[j])
                mt = re.match(r"^text:\s*(.*)", cj)
                if mt:
                    t = mt.group(1).strip().strip("'\"")
                    if t:
                        if not ist:
                            items.append(t)
                            ist = True
                        else:
                            ibuf.append(t)
                    j += 1
                    continue
                mlk = re.search(r'^link\s+"([^"]+)"', cj)
                if mlk:
                    lt = mlk.group(1)
                    if lt not in NAV:
                        if not ist:
                            items.append(lt)
                            ist = True
                        else:
                            ibuf.append(lt)
                    j += 1
                    continue
                mp = re.match(r"^paragraph:\s*(.*)", cj)
                if mp:
                    t = mp.group(1).strip().strip("'\"")
                    if t:
                        if not ist:
                            items.append(t)
                            ist = True
                        else:
                            ibuf.append(t)
                    j += 1
                    continue
                if cj.startswith("list:"):
                    lb = ij + 2
                    k = j + 1
                    while k < len(lines):
                        rk = lines[k].lstrip()
                        ik = gi(lines[k])
                        if ik < lb:
                            break
                        if not rk.startswith("- "):
                            k += 1
                            continue
                        ck = gc(lines[k])
                        if ck.startswith("listitem:"):
                            li3 = ck[len("listitem:"):].strip()
                            if li3:
                                items.append(li3)
                            else:
                                nb = ik + 2
                                nm = k + 1
                                nbuf = []
                                nst = False
                                while nm < len(lines):
                                    rn = lines[nm].lstrip()
                                    inn = gi(lines[nm])
                                    if inn < nb:
                                        break
                                    if not rn.startswith("- "):
                                        nm += 1
                                        continue
                                    cn = gc(lines[nm])
                                    mt3 = re.match(r"^text:\s*(.*)", cn)
                                    if mt3:
                                        t3 = mt3.group(1).strip().strip("'\"")
                                        if t3:
                                            if not nst:
                                                items.append(t3)
                                                nst = True
                                            else:
                                                nbuf.append(t3)
                                        nm += 1
                                        continue
                                    mlk3 = re.search(r'^link\s+"([^"]+)"', cn)
                                    if mlk3:
                                        lt3 = mlk3.group(1)
                                        if lt3 not in NAV:
                                            if not nst:
                                                items.append(lt3)
                                                nst = True
                                            else:
                                                nbuf.append(lt3)
                                        nm += 1
                                        continue
                                    if cn.startswith(("list:", "listitem:", "blockquote", "figure", "/url", "row ")):
                                        nm += 1
                                        continue
                                    nm += 1
                                if nbuf:
                                    items.append("".join(nbuf))
                                k = nm
                                continue
                            k += 1
                            continue
                        if ck.startswith("text:"):
                            mt2 = re.match(r"^text:\s*(.*)", ck)
                            if mt2:
                                t2 = mt2.group(1).strip().strip("'\"")
                                if t2:
                                    if not ist:
                                        items.append(t2)
                                        ist = True
                                    else:
                                        ibuf.append(t2)
                            k += 1
                            continue
                        if ck.startswith("link "):
                            mlk2 = re.search(r'^link\s+"([^"]+)"', ck)
                            if mlk2:
                                lt2 = mlk2.group(1)
                                if lt2 not in NAV:
                                    if not ist:
                                        items.append(lt2)
                                        ist = True
                                    else:
                                        ibuf.append(lt2)
                            k += 1
                            continue
                        k += 1
                    j = k
                    continue
                j += 1
            for it in items:
                if it.strip():
                    out.append(it)
            if ibuf:
                out.append("".join(ibuf))
            i = j
            continue
        else:
            out.append(li)
            i += 1
            continue
    i += 1

flush()

def is_sec(l):
    return l in ("目录", "本周研究报告推荐", "本周市场风向一览", "市场热点事件点评", "本周融资事件一览", "热门融资项目分析", "研究简报如下", "免责声明") or l.startswith("会员周报")

final = []
for line in out:
    s = line.strip()
    if is_sec(s) and final:
        final.append("")
    final.append(line)

rl = [l for l in final if l.strip()]
r = "\n".join(rl)

with open("/tmp/parse_result.txt", "w") as f:
    f.write(r)

with open("/tmp/gt_44900.txt") as f:
    gt = f.read()

print(f"PARSER: {len(r):,} chars, {len(rl)} lines")
print(f"GT:     {len(gt):,} chars, {len(gt.splitlines())} lines")
print(f"Ratio:  {len(r)/len(gt)*100:.1f}%")
print()
checks = ["Origins Network", "Vitalik Buterin", "OpenFX", "9400", "Cango", "7500", "Pixie", "Uniblock", "免责声明", "Gnosis", "签名体系", "研究简报如下"]
for c in checks:
    p = c in r
    g = c in gt
    print(f"  {'OK' if p else 'NO'} {'OK' if g else 'NO'}: {c}")
print()
for i, l in enumerate(rl[:35]):
    print(f"{i:3d}: {l[:100]}")
