# -*- coding: utf-8 -*-
"""
受控素材库下载模板
------------------------------------------------------------------
用法：
  python download_template.py --map urls.json
  （urls.json 结构：{ "<node_id>": {"png": "<CDN_URL>", "svg": "<CDN_URL>"}, ... }）

依赖：同目录下的 _asset_index.json（node -> 本地 png/svg 绝对路径映射）
说明：Ardot export_nodes 返回的 CDN 直链带签名会过期，拿到后立即下载。
"""
import os, sys, json, argparse, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
# 默认库根：向上两级到工作区（技能在 skills/.../scripts，库在 工作区/SynomosAI_素材库）
# 实际使用时通过 --lib 覆盖
DEFAULT_LIB = os.path.normpath(os.path.join(BASE, "..", "..", "..", "SynomosAI_素材库"))
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def download(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    with open(dest, "wb") as f:
        f.write(data)
    return len(data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", required=True, help="URL 映射 JSON：{node_id:{png,svg}}")
    ap.add_argument("--lib", default=DEFAULT_LIB, help="SynomosAI_素材库根目录")
    ap.add_argument("--index", default=None, help="_asset_index.json 路径（默认 <lib>/_asset_index.json）")
    args = ap.parse_args()

    lib = os.path.abspath(args.lib)
    index_path = args.index or os.path.join(lib, "_asset_index.json")
    index = json.load(open(index_path, encoding="utf-8"))
    urls = json.load(open(os.path.abspath(args.map), encoding="utf-8"))

    ok = fail = 0
    for node_id, u in urls.items():
        if node_id not in index:
            print(f"  [跳过] {node_id} 不在索引中"); fail += 1; continue
        info = index[node_id]
        for kind in ("png", "svg"):
            try:
                sz = download(u[kind], info[kind])
                ok += 1
                print(f"  [{kind}] {node_id} -> {os.path.basename(info[kind])} ({sz}B)")
            except Exception as ex:
                fail += 1
                print(f"  [失败] {kind} {node_id}: {ex}")
    print(f"下载完成：成功 {ok} · 失败 {fail}")


if __name__ == "__main__":
    main()
