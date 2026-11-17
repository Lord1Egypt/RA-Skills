import argparse, json, os, sys

def dir_size(path):
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total

def main():
    ap = argparse.ArgumentParser(description="disk-scan · 目录占用扫描（只读不删）")
    ap.add_argument("--dir", required=True)
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not os.path.isdir(a.dir):
        print("目录不存在: %s" % a.dir); sys.exit(2)
    files = []
    subdirs = {}
    for root, dirs, fs in os.walk(a.dir):
        rel = os.path.relpath(root, a.dir)
        if rel != ".":
            subdirs[rel] = dir_size(root)
        for f in fs:
            p = os.path.join(root, f)
            try:
                files.append((os.path.getsize(p), p))
            except OSError:
                pass
    files.sort(reverse=True)
    subs = sorted(subdirs.items(), key=lambda kv: -kv[1])[:a.top]
    total = dir_size(a.dir)
    if a.json:
        print(json.dumps({"total_bytes": total,
                          "top_files": [{"path": os.path.relpath(p, a.dir), "bytes": s} for s, p in files[:a.top]],
                          "top_dirs": [{"path": k, "bytes": v} for k, v in subs]},
                         ensure_ascii=False, indent=2))
    else:
        print("总占用: %.2f MB ｜ Top %d 大文件:" % (total / 1048576, min(a.top, len(files))))
        for s, p in files[:a.top]:
            print("  %8.2f MB  %s" % (s / 1048576, os.path.relpath(p, a.dir)))
        print("Top %d 子目录:" % len(subs))
        for k, v in subs:
            print("  %8.2f MB  %s" % (v / 1048576, k))
        print("（只读扫描，删除请自行判断或配合 dup-finder）")
    sys.exit(0)

if __name__ == "__main__":
    main()
