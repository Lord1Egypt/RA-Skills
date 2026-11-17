#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cue_connectivity_check.py —— 一条命令跑完「通道到底连没连上」这一层（与面内那块可复制命令同语义）。

它做三件事，全按该包 README 连通那一节的现值走，不在本件里另立第二套判据：
  1. 取目录（缺省匿名 GET 那处目录入口；--catalog-url 换源、--catalog-file 改读本地快照）；
  2. 按 --domain 给的域 id 从返回里取该域 routing 里的 url 字段——取的是对象里那个可发请求的 url，不是整枚 routing 对象；
  3. 显式带 --post 时，才用本地凭据设施里那把 key 向那个 url 发一次 tools/list，把 HTTP 状态码与 result.tools 枚数打出来——发之前先过两关：scheme=https、且该 host 命中授权后缀；任一不过就拒发，一个凭据字节都不附（退 6）。

缺省一个包都不发：不带 --post 时本件只走到「取到该域 routing 里的 url」为止（退码 4，连通未证）。
换源不无声也**不免检**：目录来源不是缺省那一处时，本件照样把目标 host 印在回字首行；而带凭据那一次发出去之前，无论地址来自缺省目录、换入的 --catalog-url，还是 --catalog-file 那份本地快照，都过同一道两关（https＋授权后缀）——过不了就拒发（退 6），本件不附 key 也不发那个请求。目录入口自己也得是 https（退 7）；--catalog-file 是本读、不发请求，不走这一关。

退码（每条都响亮、零 Traceback）：
  0  实连：HTTP 200 且 result.tools 是非空数组（即该包 README 连通那一节那句判据成立，本件不另述数字）
  4  只取到地址、连通未证——缺省那一支就是这一态，要证连通请带 --post
  5  发出去了、也拿到响应、但判据不满足：result.tools 是空数组、返回体里没有它、返回体解析不出、或 result 形状不认识
  6  凭据外发被拒：目的地没过两关（非 https，或 host 不在授权后缀之内）——本件不发出任何带 key 的请求，一个凭据字节都不附
  7  目录入口没过 https 关：--catalog-url 给的是非 https 的地址（--catalog-file 是本读，不走这一关）
  1  取不到／发不出去／HTTP 层报错：域不在场、该域没有 routing、routing 缺 url、目录取不回、本地凭据缺位、请求发不出去，以及 4xx 与 5xx（urllib 在这一支抛 HTTPError，本件按 HTTP 层报错退 1）
  2  用法错：既没给 --domain 也没给 --list

任何失败都走一句人话出口：except 里要用的名字先赋初值，绝不格式化未绑定的变量。
零计费：目录那一次匿名只读；tools/list 是清单方法，不取数据、不计消耗；本件缺省不发任何包。
本件不写死域清单、工具名或 routing 值——域 id 与 url 一律从目录当场返回里取。授权后缀也不硬编一张表：缺省那一枚由本件头 CATALOG_DEFAULT 的 host 现推（依据＝渠道自己的目录入口域），要显式放行别的目的地请带 --allow-host（那是你替自己认下的，本件不猜）。
凭据只从环境变量读（CUE_API_KEY，或宿主凭据设施注入的等价变量），本件永不打印它的值。
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

CATALOG_DEFAULT = "https://cuecue.cn/api/mcp-catalog"
ACCEPT = "application/json, text/event-stream"


def authorized_suffixes(extra=()):
    """授权目的地后缀：缺省一枚，由本件头 CATALOG_DEFAULT 那枚现值推出——依据＝渠道自己的目录入口域，
    不是本件另编的第二张清单；--allow-host 只能由你显式追加（你替自己认下的目的地）。"""
    host = urllib.parse.urlsplit(CATALOG_DEFAULT).hostname or ""
    parts = [p for p in host.split(".") if p]
    base = ".".join(parts[-2:]) if len(parts) >= 2 else host
    out = [base] if base else []
    out += [e.strip().lstrip(".").lower() for e in (extra or ()) if e and e.strip()]
    return out


def host_of(url):
    return urllib.parse.urlsplit(url).netloc or "(这个 url 解析不出主机)"


def guard_credential_target(url, suffixes):
    """带凭据发出去之前的两关（任何路径都不得绕过）：scheme 必须是 https，且 host 命中授权后缀。
    → (是否放行, 原因)。拒发时调用方必须在此之前不读 key、不构造那个请求。"""
    parts = urllib.parse.urlsplit(url)
    host = (parts.hostname or "").lower()
    if parts.scheme != "https":
        return False, "scheme=%s（只收 https）｜host=%s" % (parts.scheme or "(无)", host or "(解析不出主机)")
    if not host:
        return False, "https 前缀在，但 host 解析不出来（现读 url=%s）" % url
    if not any(host == s or host.endswith("." + s) for s in suffixes):
        return False, "host=%s 不在授权后缀之内（授权后缀＝%s；要显式放行请带 --allow-host）" % (
            host, "、".join(suffixes) or "(空)")
    return True, "https＋授权 host=%s" % host


def die(msg, code=1):
    """一句人话出口——绝不抛异常，免得下一位照着 Traceback 查错方向。"""
    print(msg, file=sys.stderr)
    return code


def read_catalog(url, path, timeout):
    """目录来源：--catalog-file 给路径时读本地快照（受控靶用），否则匿名 GET。返回 (文档, 来源说明, 是否换源)。"""
    src = path if path else url
    if path:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                text = fh.read()
        except OSError as err:
            raise SystemExit(die("读不到目录快照：%s（%s: %s）" % (path, type(err).__name__, str(err)[:80])))
        try:
            return json.loads(text), "本地快照 %s" % src, True
        except ValueError as err:
            raise SystemExit(die("目录快照不是合法 JSON：%s（%s）" % (src, str(err)[:80])))
    payload = ""
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = resp.read().decode("utf-8", "replace")
    except (urllib.error.URLError, OSError, ValueError) as err:
        raise SystemExit(die("目录取不回：%s（%s）" % (src, str(err)[:120])))
    try:
        return json.loads(payload), "匿名 GET %s" % src, (url != CATALOG_DEFAULT)
    except ValueError as err:
        raise SystemExit(die("目录返回不是合法 JSON：%s（%s）" % (src, str(err)[:80])))


def rows_of(doc):
    """从返回里取域清单——形状不认识时也要一句人话，不许 KeyError。"""
    if not isinstance(doc, dict):
        raise SystemExit(die("目录返回不是对象（顶层类型＝%s）——换源或换 --catalog-file" % type(doc).__name__))
    data = doc.get("data")
    rows = data.get("domains") if isinstance(data, dict) else None
    if not isinstance(rows, list):
        raise SystemExit(die("目录返回里没有 data.domains 数组（顶层键＝%s）——本件按那形读，换源请直说" % ", ".join(sorted(doc))))
    return [r for r in rows if isinstance(r, dict)]


def routing_url(row):
    """取该域 routing 里的 url 字段；routing 在场但缺 url 时返回 None，由调用方出一句人话。"""
    routing = row.get("routing")
    if not isinstance(routing, dict):
        return None
    url = routing.get("url")
    return url if isinstance(url, str) and url else None


def table(listed):
    for rid, status, url in listed:
        print("  %-16s %-12s %s" % (rid or "(缺 id)", status or "(缺状态)", url or "(routing 里没有 url)"))


def main():
    ap = argparse.ArgumentParser(
        description="一条命令跑完连通自检：从目录现取该域 routing 里的 url；要真发那一次 tools/list 请显式带 --post。",
        epilog="判据的权威表述在该包 README 连通那一节，本件只执行、不复述。零计费：目录匿名只读，tools/list 不取数据；缺省不发任何包。")
    ap.add_argument("--domain", help="要连的域 id（取值请从 --list 的现场输出里挑，本件不写死域清单）")
    ap.add_argument("--list", action="store_true", help="只列在场域 id、external_status 与 routing 里的 url，不发 POST")
    ap.add_argument("--post", action="store_true", help="显式发那一次 tools/list；不带这一项本件一个包都不发，退码 4（连通未证）")
    ap.add_argument("--catalog-url", default=CATALOG_DEFAULT, help="换目录入口用（默认本件唯一那处）；只收 https，且返回里给的 url 照样要过凭据外发两关")
    ap.add_argument("--catalog-file", help="离线：改读本地目录快照（受控靶用）：本开关自身只读该文件、不发包；带 --post 时那份快照里给的 url 仍要过同一道两关，过不了就拒发（退 6）")
    ap.add_argument("--timeout", type=int, default=20, help="单次请求超时秒数（默认 20）")
    ap.add_argument("--allow-host", action="append", metavar="SUFFIX", help="显式追加一枚授权目的地后缀（可重复）；缺省那一枚由件头目录入口现值推出，本件不猜目的地")
    args = ap.parse_args()

    suffixes = authorized_suffixes(args.allow_host)
    if not args.catalog_file and urllib.parse.urlsplit(args.catalog_url).scheme != "https":
        return die("目录入口没过 https 关：%s（scheme=%s）——本件不向它发请求，也不把任何凭据附给它；"
                   "离线请改 --catalog-file 读本地快照，或把 --catalog-url 换成 https 那一处；退码 7"
                   % (args.catalog_url, urllib.parse.urlsplit(args.catalog_url).scheme or "(无)"), 7)
    doc, src, swapped = read_catalog(args.catalog_url, args.catalog_file, args.timeout)

    rows = rows_of(doc)
    listed = [(str(r.get("id", "")), str(r.get("external_status", "")), routing_url(r)) for r in rows]

    if args.list:
        print("目录来源＝%s｜在场域 %d 枚（id／external_status／routing 里的 url）" % (src, len(listed)))
        table(listed)
        print("下一步：python3 -B scripts/cue_connectivity_check.py --domain <上面那一列里的 id> --post（不带 --post 退码 4＝连通未证）")
        return 0

    if not args.domain:
        print("--domain 没给（也不带 --list）——本件不猜域。在场域如下，挑一个再跑：")
        table(listed)
        return 2

    hit = [x for x in listed if x[0] == args.domain]
    if not hit:
        return die("未取到：目录现值里没有 id＝%s 这一枚（在场 %d 枚，先跑 --list 看清单）" % (args.domain, len(listed)))
    rid, status, url = hit[0]
    if url is None:
        row = next((r for r in rows if str(r.get("id", "")) == rid) or {})
        keys = ", ".join(sorted((row.get("routing") or {}))) or "(routing 不是对象)"
        if status and status != "live":
            return die("未取到：域 %s 的 external_status＝%s，目录这一枚没给 routing 里的 url——非 live 域本件不装也不承诺" % (rid, status))
        return die("未取到：域 %s 的 routing 在场但没有 url 字段（键＝%s）——本件要的是其中那个可发请求的 url，不猜别的键" % (rid, keys))

    host = host_of(url)
    if not args.post:
        print("域 %s｜external_status=%s｜取到 routing 里的 url=%s" % (rid, status, url))
        print("缺省零发包：本件到此为止，没有发 POST，退码 4＝连通未证。要证连通请显式加 --post。")
        return 4

    ok, why = guard_credential_target(url, suffixes)
    if not ok:
        return die("拒发：目的地没过凭据外发两关（原因＝%s）——本件没有读 key、没有构造那个请求、也没有发出它；退码 6" % why, 6)
    print("POST 目标 host＝%s｜目录来源＝%s｜授权后缀＝%s%s" % (
        host, src, "、".join(suffixes) or "(空)",
        "（目标地址来自换入的目录，它与缺省那一处过的是同一道两关）" if swapped else ""))
    key = os.environ.get("CUE_API_KEY", "").strip()
    if not key:
        return die("取到了 routing 里的 url，但本地凭据缺位：环境变量 CUE_API_KEY 没读到——本件不打印 key，也不替你写进任何文件")
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": "Bearer " + key, "Accept": ACCEPT, "Content-Type": "application/json"})
    code = None
    raw = ""
    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as resp:
            code, raw = resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as err:
        detail = ""
        try:
            detail = (err.read().decode("utf-8", "replace").splitlines() or ["(空)"])[0][:120]
        except (OSError, ValueError):
            detail = "(错误体读不出)"
        return die("POST 到 %s 实得 HTTP %s——连通未过（判据见该包 README 连通那一节）；错误体首行：%s" % (host, err.code, detail))
    except (urllib.error.URLError, OSError, ValueError) as err:
        return die("POST 发不出去（目标 host＝%s；%s）：连接报错不等于域无数据——如实报，只重试错误标明可重试的部分" % (host, str(err)[:120]))

    parsed = None
    try:
        parsed = json.loads(raw.strip())
    except ValueError:
        for line in raw.splitlines():
            if line.startswith("data:"):
                try:
                    parsed = json.loads(line[5:].strip())
                    break
                except ValueError:
                    continue
    if parsed is None:
        return die("POST 实得 HTTP %s（目标 host＝%s），但返回体既不是单个 JSON、也没有可解析的 data: 行（首 60 字：%s）——退码 5，按现场回字判，别按本件的解析判" % (code, host, raw[:60]), 5)
    result = parsed.get("result") if isinstance(parsed, dict) else None
    if not isinstance(result, dict):
        return die("POST 实得 HTTP %s（目标 host＝%s），返回体里的 result 不是对象——本件不猜形状（顶层类型＝%s，result 类型＝%s）；退码 5，按现场回字判" % (code, host, type(parsed).__name__, type(result).__name__), 5)
    tools = result.get("tools")
    n = len(tools) if isinstance(tools, list) else None
    print("域 %s｜external_status=%s｜目标 host=%s｜POST tools/list 实得 HTTP %s｜result.tools 枚数=%s" % (
        rid, status, host, code, n if n is not None else "(返回体里没有 tools 数组)"))
    if code == 200 and isinstance(tools, list) and tools:
        print("退码 0：现场值满足判据（判据本身见该包 README 连通那一节，本件不复制第二处真值）")
        return 0
    print("退码 5：请求发出去了、也拿到了响应，但判据未满足——result.tools 是空数组，或返回体里没有它")
    return 5


if __name__ == "__main__":
    sys.exit(main())
