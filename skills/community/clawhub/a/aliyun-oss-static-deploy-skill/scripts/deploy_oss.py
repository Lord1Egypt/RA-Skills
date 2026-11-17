#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把静态站产物部署到阿里云 OSS（建桶/上传/静态托管/公开访问/校验）。

支持两种输入：
    --dir  <目录>    上传整个目录（推荐，配合 build_static.py 的对外产物）
    --file <文件>    上传单个文件（默认对象名 = 文件名，可用 --key 覆盖）

依赖：
    pip install oss2

环境变量（只从这里读，绝不落盘、绝不打印）：
    ALIBABA_CLOUD_ACCESS_KEY_ID / ALIBABA_CLOUD_ACCESS_KEY_SECRET

用法：
    python deploy_oss.py --check                                    # 列账号下所有桶
    python deploy_oss.py --bucket my-site-hk --region cn-hongkong --dir public \
        --setup-website --verify-public --verify                    # 整目录上线
    python deploy_oss.py --bucket my-site-hk --file index.html --key index.html \
        --verify --expect 'schema_version'                          # 单文件更新
    python deploy_oss.py --bucket my-site-hk --dir dist --dry-run   # 只看不传

退出码：0 成功；1 失败
"""
import argparse
import hashlib
import os
import sys
import time
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DEFAULT_REGION = "cn-hongkong"

# OSS 不猜 Content-Type，猜错浏览器行为很怪（css 变 plain 直接不生效）
CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8", ".htm": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",   ".js": "application/javascript; charset=utf-8",
    ".mjs": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".map": "application/json; charset=utf-8",
    ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp",
    ".ico": "image/x-icon", ".woff": "font/woff", ".woff2": "font/woff2",
    ".ttf": "font/ttf", ".otf": "font/otf", ".txt": "text/plain; charset=utf-8",
    ".xml": "application/xml; charset=utf-8", ".pdf": "application/pdf",
    ".md": "text/markdown; charset=utf-8",
}
DEFAULT_CT = "application/octet-stream"

# html / 数据文件改完要立刻生效；js/css 基本不变，给 5 分钟省回源
CACHE_HTML = "no-cache"
CACHE_ASSET = "public, max-age=300"
HTML_EXT = {".html", ".htm", ".json", ".xml", ".txt"}

PROXY_KEYS = ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
              "ALL_PROXY", "all_proxy"]


def log(msg):
    print("[%s] %s" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg), flush=True)


def norm_region(region):
    """region 短名 -> endpoint 用的地域标识。

    SKILL 里习惯写 cn-hongkong，而 endpoint 需要 oss-cn-hongkong，这里统一补前缀。
    """
    region = (region or DEFAULT_REGION).strip()
    return region if region.startswith("oss-") else "oss-" + region


def endpoint_of(region):
    return "https://%s.aliyuncs.com" % norm_region(region)


def strip_proxy():
    """本机常驻代理会让 oss2 报 Tunnel connection failed: 502，且时好时坏。

    curl 可以 --noproxy 绕开，但 oss2（底层 requests）会老实读这些环境变量。
    本地手动跑脚本前必须清掉；GitHub Actions 在云端本来就没有，不受影响。
    """
    removed = [k for k in PROXY_KEYS if os.environ.pop(k, None) is not None]
    if removed:
        log("已清除代理环境变量（本机代理会搞挂 oss2）：%s" % ", ".join(removed))


def content_type_for(path):
    return CONTENT_TYPES.get(os.path.splitext(path)[1].lower(), DEFAULT_CT)


def cache_control_for(path):
    ext = os.path.splitext(path)[1].lower()
    return CACHE_HTML if ext in HTML_EXT else CACHE_ASSET


def md5_of(data):
    return hashlib.md5(data).hexdigest()


def get_bucket(bucket, region):
    import oss2
    ak = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if not ak or not sk:
        log("✗ 缺少环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID / ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        log("  （AK 只从环境变量读，不要写进任何文件、也不要提交到 git）")
        sys.exit(1)
    auth = oss2.Auth(ak, sk)
    return oss2.Bucket(auth, endpoint_of(region), bucket, connect_timeout=30)


def do_check(args):
    import oss2
    ak = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if not ak or not sk:
        log("✗ 缺少 AK 环境变量"); sys.exit(1)
    auth = oss2.Auth(ak, sk)
    # Service 的第二个参数是完整 endpoint，不是 region 短名；传短名会报
    # RequestError: HTTPConnectionPool ... 看起来像网络/权限故障，其实是用错了参数
    svc = oss2.Service(auth, endpoint_of(args.region), connect_timeout=30)
    log("账号下的桶（endpoint=%s）：" % endpoint_of(args.region))
    try:
        for b in svc.list_buckets().buckets:
            log("  %-40s %s" % (b.name, getattr(b, "location", "?")))
    except Exception as e:
        log("✗ 列举失败：%s" % e)
        sys.exit(1)


def backup_object(b, key, backup_dir):
    """覆盖前先把线上原对象拉下来，留回滚基线。"""
    try:
        head = b.head_object(key)
        exists = True
    except Exception:
        exists = False
    if not exists:
        log("  对象 %s 不存在，无需备份" % key)
        return None
    dest_dir = backup_dir or os.path.join(
        os.path.expanduser("~"), ".oss-deploy-backup", b.bucket_name)
    os.makedirs(dest_dir, exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    safe = key.replace("/", "__")
    dest = os.path.join(dest_dir, "%s.%s" % (safe, ts))
    b.get_object_to_file(key, dest)
    data = open(dest, "rb").read()
    log("  已备份旧版本 -> %s (md5=%s, %d 字节)" % (dest, md5_of(data), len(data)))
    return dest


def upload_one(b, src_path, key, args):
    data = open(src_path, "rb").read()
    headers = {
        "Content-Type": content_type_for(src_path),
        "Cache-Control": cache_control_for(src_path),
    }
    if args.dry_run:
        log("  [dry-run] PUT %s <- %s (%d 字节, %s)"
            % (key, src_path, len(data), headers["Content-Type"]))
        return None
    if not args.no_backup:
        backup_object(b, key, args.backup_dir)
    r = b.put_object(key, data, headers=headers)
    log("  ✓ %s <- %s (%d 字节, md5=%s, http=%s)"
        % (key, os.path.basename(src_path), len(data), md5_of(data), r.status))
    return r


def verify_object(b, key, local_path, expect):
    """验收：比 md5 而不是比字节数；可选再做语义标记断言。"""
    try:
        remote = b.get_object(key).read()
    except Exception as e:
        log("  ✗ 回读失败：%s" % e)
        return False
    if local_path and os.path.exists(local_path):
        local = open(local_path, "rb").read()
        rm, lm = md5_of(remote), md5_of(local)
        ok = rm == lm
        log("  %s md5 比对：线上=%s 本地=%s" % ("✓" if ok else "✗", rm, lm))
        if not ok:
            return False
    if expect:
        try:
            text = remote.decode("utf-8", "ignore")
        except Exception:
            text = ""
        found = all(m in text for m in expect)
        for m in expect:
            log("  %s 语义标记：%s" % ("✓" if m in text else "✗", m))
        if not found:
            return False
    return True


def setup_website(b, index, error):
    import oss2
    try:
        b.put_bucket_website(oss2.models.BucketWebsite(index, error))
        got = b.get_bucket_website()
        log("  ✓ 静态网站托管已设置：Index=%s Error=%s"
            % (got.index_file, getattr(got, "error_file", "")))
        log("    （不设的话访问域名根路径返回的是 XML 对象列表而不是首页）")
    except Exception as e:
        log("  ✗ 设置静态托管失败：%s" % e)
        return False
    return True


def verify_public(b, region):
    """新建桶默认 BlockPublicAccess=true：匿名访问 403，且 PutBucketPolicy 也被拒。

    改 ACL 没用，必须关掉桶级阻止公共访问。
    """
    try:
        r = b.get_bucket_public_access_block()
        enabled = bool(getattr(r, "block_public_access", True))
        log("  BlockPublicAccess = %s" % enabled)
        if enabled:
            b.delete_bucket_public_access_block()
            r2 = b.get_bucket_public_access_block()
            enabled2 = bool(getattr(r2, "block_public_access", True))
            log("  已关闭桶级阻止公共访问 -> %s" % enabled2)
            if enabled2:
                log("  ✗ 关闭失败，可能需要账号级权限")
                return False
        else:
            log("  ✓ 桶未阻止公共访问")
    except Exception as e:
        log("  ! 查询/关闭 BlockPublicAccess 失败：%s" % e)
        log("    （oss2 < 2.16 无此 API，可改用 curl/scp 直发 DELETE ?publicAccessBlock）")
        return False
    # 匿名探测
    import urllib.request
    url = "https://%s.%s.aliyuncs.com/%s" % (
        b.bucket_name, norm_region(region), "index.html")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "deploy-verify"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            log("  ✓ 匿名访问 %s -> HTTP %s" % (url, resp.status))
            return True
    except Exception as e:
        code = getattr(e, "code", "")
        log("  %s 匿名访问 %s -> %s" % ("✓" if code == 200 else "!", url, e))
        return code == 200


def verify_and_report(b, pairs, args):
    """回读校验。dry-run 时对象并未真正上传，回读必然 404，直接跳过而不是误报失败。"""
    if not args.verify:
        return
    if args.dry_run:
        log("  [dry-run] 跳过回读校验（对象未真正上传）")
        return
    ok = all(verify_object(b, k, local, args.expect) for local, k in pairs)
    log("✓ 校验通过" if ok else "✗ 校验失败")
    if not ok:
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description="静态站部署到阿里云 OSS")
    ap.add_argument("--bucket", help="OSS Bucket 名")
    ap.add_argument("--region", default=DEFAULT_REGION,
                    help="地域，cn-hongkong 或 oss-cn-hongkong 均可，默认 %(default)s")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--dir", help="上传整个目录")
    src.add_argument("--file", help="上传单个文件")
    ap.add_argument("--key", default="", help="--file 时指定对象名，默认用文件名")
    ap.add_argument("--index", default="index.html", help="静态托管首页，默认 %(default)s")
    ap.add_argument("--error", default="404.html", help="静态托管错误页，默认 %(default)s")
    ap.add_argument("--prefix", default="", help="对象名前缀，如 site/")
    ap.add_argument("--setup-website", action="store_true", help="配置静态网站托管")
    ap.add_argument("--verify-public", action="store_true",
                    help="关闭桶级阻止公共访问并匿名验证")
    ap.add_argument("--verify", action="store_true", help="上传后回读 md5 校验")
    ap.add_argument("--expect", action="append", default=[],
                    help="语义标记，可重复；例如 --expect 'schema_version'")
    ap.add_argument("--check", action="store_true", help="只列账号下的桶")
    ap.add_argument("--dry-run", action="store_true", help="只打印将要执行的操作")
    ap.add_argument("--backup-dir", default="", help="旧版本备份目录")
    ap.add_argument("--no-backup", action="store_true", help="关闭自动备份")
    ap.add_argument("--keep-proxy", action="store_true",
                    help="保留代理环境变量（默认清除，见脚本顶部说明）")
    args = ap.parse_args()

    try:
        import oss2  # noqa: F401
    except ImportError:
        log("✗ 缺少依赖：pip install oss2")
        sys.exit(1)

    if not args.keep_proxy:
        strip_proxy()

    region = args.region
    log("地域=%s  endpoint=%s" % (norm_region(region), endpoint_of(region)))

    if args.check:
        do_check(args)
        return

    if not args.bucket or not (args.dir or args.file):
        log("✗ 需要 --bucket 且 --dir 或 --file 之一（或 --check）")
        sys.exit(1)

    b = get_bucket(args.bucket, norm_region(region))
    log("桶=%s" % args.bucket)

    if args.dir:
        root = os.path.abspath(args.dir)
        if not os.path.isdir(root):
            log("✗ 目录不存在：%s" % root); sys.exit(1)
        if not os.path.exists(os.path.join(root, args.index)):
            log("! 目录里没有 %s，若为子路径部署请确认 --prefix" % args.index)
        uploaded = []
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules", "__pycache__")]
            for fn in sorted(filenames):
                if fn.startswith("."):
                    continue
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, root).replace("\\", "/")
                upload_one(b, full, args.prefix + rel, args)
                uploaded.append((full, args.prefix + rel))
        log("共 %d 个对象" % len(uploaded))
        verify_and_report(b, uploaded, args)
    else:
        src_path = os.path.abspath(args.file)
        if not os.path.exists(src_path):
            log("✗ 文件不存在：%s" % src_path); sys.exit(1)
        key = args.key or os.path.basename(src_path)
        upload_one(b, src_path, args.prefix + key, args)
        verify_and_report(b, [(src_path, args.prefix + key)], args)

    if args.setup_website:
        if not args.dry_run:
            setup_website(b, args.index, args.error)
        else:
            log("  [dry-run] 会设置静态托管：Index=%s Error=%s" % (args.index, args.error))
    if args.verify_public:
        if not args.dry_run:
            verify_public(b, region)
        else:
            log("  [dry-run] 会关闭 BlockPublicAccess 并匿名验证")

    log("完成。自定义域名若走 CDN，记得刷新目录缓存 /")


if __name__ == "__main__":
    main()
