import argparse, csv, json, sys

def main():
    ap = argparse.ArgumentParser(description="csv-slice · CSV 快速查看/筛选/去重（零依赖）")
    ap.add_argument("--file", required=True)
    ap.add_argument("--head", type=int, help="只看前N行")
    ap.add_argument("--cols", help="只取这些列（序号从1起，逗号分隔，如 1,3）")
    ap.add_argument("--where", help="条件筛选，格式 列号=值，如 2=北京")
    ap.add_argument("--dedup", action="store_true", help="整行去重")
    ap.add_argument("--count", action="store_true", help="只统计行数")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        rows = list(csv.reader(open(a.file, encoding="utf-8-sig", newline="")))
    except Exception as e:
        print("读取失败: %s" % e); sys.exit(2)
    if not rows:
        print("空文件"); sys.exit(1)
    hdr, body = rows[0], rows[1:]
    if a.where and "=" in a.where:
        ci, val = a.where.split("=", 1)
        ci = int(ci) - 1
        body = [r for r in body if ci < len(r) and r[ci] == val]
    if a.dedup:
        seen, out = set(), []
        for r in body:
            k = tuple(r)
            if k not in seen:
                seen.add(k); out.append(r)
        removed = len(body) - len(out)
        body = out
    else:
        removed = 0
    cols = None
    if a.cols:
        cols = [int(c) - 1 for c in a.cols.split(",")]
        hdr = [hdr[i] for i in cols if i < len(hdr)]
        body = [[r[i] for i in cols if i < len(r)] for r in body]
    if a.json:
        print(json.dumps({"header": hdr, "rows": body[:a.head] if a.head else body,
                          "total": len(body), "dedup_removed": removed},
                         ensure_ascii=False, indent=2))
        sys.exit(0)
    if a.count:
        print("数据行: %d（不含表头）%s" % (len(body), "｜去重删除 %d 行" % removed if removed else ""))
        sys.exit(0)
    print(" | ".join(hdr))
    for r in (body[:a.head] if a.head else body):
        print(" | ".join(r))
    tail = "（前%d行/共%d行）" % (a.head, len(body)) if a.head and len(body) > a.head else "（共%d行）" % len(body)
    print(tail + ("｜去重删除 %d 行" % removed if removed else ""))
    sys.exit(0)

if __name__ == "__main__":
    main()
