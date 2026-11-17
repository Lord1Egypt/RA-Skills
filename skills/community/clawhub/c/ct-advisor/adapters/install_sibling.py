#!/usr/bin/env python3
r"""安装 ct 系列兄弟技能（A 档 · SkillHub 公开发布）。

存在理由（2026-09-10，实测驱动）
---------------------------------------------------------------------------
A/B 档门控里「用户同意 → 安装 → 再执行」这一步，此前给用户的是一条
`skillhub install <slug>` 的裸命令，实测**三重不可用**：

  1. PATH 中并无 `skillhub` 命令（~/.local/bin/skillhub 本机不存在；skill-publish
     记载该 bash 启动器另有 Windows 路径 bug）→ 用户照抄必失败；
  2. 直接调 `~/.skillhub/skills_store_cli.py` 时，本机该文件是**精简版**
     （v2026.3.6, 44KB），其下载端点指向内网 LB，实测返回非 zip
     （"Downloaded file is not a valid zip archive"）；
  3. 完整版 CLI 位于内网文件盘，路径是 UNC（`//<内网文件服务器>/...`），把 UNC 写进命令串经
     bash/Git-Bash 传递会被二次拼接（盘符共享根重复，如 `\\<host>\c$\<host>\c$\...`）而打不开。

本脚本把安装动作收敛成**一条由同解释器执行的命令**：纯标准库、路径以参数列表
传递（subprocess 不经 shell，天然规避 MSYS 路径转换与 UNC 拼接）、先核验上架
状态再下载，从而不受 CLI 版本 / UNC 路径 / PATH 配置影响。

行为
----
  1. 核验：查 SkillHub search API，`slug` 或 `namespace.publicSlug` 精确命中才继续。
     未命中 → 拒绝安装并退出码 3（防止把未发布 / B 档技能装进来）。
  2. 下载：GET {DOWNLOAD_URL}?slug=<slug>。**端点默认锁定官方 host 白名单**（HTTPS）；
     镜像/联调需显式 --allow-custom-endpoint 才接受 env 覆写（防环境变量劫持重定向）。
  3. 校验：合法 zip 且根含 SKILL.md + **zip 内部 CRC 全量校验（zf.testzip）** +
     拒绝符号链接条目 + 越界路径检查；可用 --expect-sha256 锚定包内容摘要。
  4. 落盘：解压到 <dir>/<slug>/。已存在则拒绝，除非 --force。
     （SkillHub 包是扁平结构：SKILL.md 直接在 zip 根，故目标目录须带 slug 层。）

用法
----
  python adapters/install_sibling.py <slug> [--dir <技能根目录>] [--force] [--dry-run] [--json]
                                      [--allow-custom-endpoint] [--expect-sha256 <hex>]

环境变量：CT_SKILLS_DIR 覆盖默认技能根目录；SKILLHUB_SEARCH_URL /
SKILLHUB_DOWNLOAD_URL 覆盖接口地址（**须与官方 host 一致，或显式传
--allow-custom-endpoint**，否则拒绝——见「行为」第 2 条）。
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import shutil
import stat as _stat
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

OFFICIAL_HOST = "api.skillhub.cn"
SEARCH_URL = os.environ.get("SKILLHUB_SEARCH_URL", "https://api.skillhub.cn/api/v1/search")
DOWNLOAD_URL = os.environ.get("SKILLHUB_DOWNLOAD_URL", "https://api.skillhub.cn/api/v1/download")
TIMEOUT = 60
UA = "ct-advisor-install-sibling"
# 技能根目录：与 handle_need_tool.SKILLS_DIR 同一约定，保证装完即可被探测到
SKILLS_DIR = os.environ.get("CT_SKILLS_DIR", str(Path.home() / ".workbuddy" / "skills"))

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_NOT_PUBLISHED = 3
EXIT_ALREADY_INSTALLED = 4
EXIT_DOWNLOAD_FAILED = 5
EXIT_BAD_ARCHIVE = 6
EXIT_UNTRUSTED_ENDPOINT = 7
EXIT_INTEGRITY_FAILED = 8


def _endpoint_trusted(url: str) -> bool:
    """端点 host 必须为官方 host 且走 HTTPS——防 env 劫持重定向到恶意源。"""
    try:
        p = urllib.parse.urlparse(url)
    except ValueError:
        return False
    return p.scheme == "https" and (p.hostname or "").lower() == OFFICIAL_HOST


def _get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def check_published(slug: str, handle: str | None = None) -> dict:
    """查 SkillHub 是否上架；返回 {published, version, handle}。精确匹配，避免包含式误判。"""
    url = SEARCH_URL + "?" + urllib.parse.urlencode({"q": slug, "limit": 20})
    d = _get_json(url)
    hits = [h for h in (d.get("results") or [])
            if h.get("slug") == slug or (h.get("namespace") or {}).get("publicSlug") == slug]
    if handle:
        hits = [h for h in hits if (h.get("namespace") or {}).get("handle") == handle]
    if not hits:
        return {"published": False, "version": None, "handle": None}
    h = hits[0]
    return {"published": True, "version": h.get("version"),
            "handle": (h.get("namespace") or {}).get("handle")}


def fetch_zip_bytes(slug: str) -> bytes:
    url = DOWNLOAD_URL + "?" + urllib.parse.urlencode({"slug": slug})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read()


def install(slug: str, dest_root: Path, force: bool = False,
            dry_run: bool = False, handle: str | None = None,
            allow_custom_endpoint: bool = False,
            expect_sha256: str | None = None) -> dict:
    """核验 → 下载 → 校验 → 落盘。返回结构化结果（不抛业务异常，错误以 code 表达）。"""
    # slug 仅允许安全字符：防止 ../ 之类越出技能根目录
    if not slug or any(c in slug for c in ("/", "\\", "..")) or slug.startswith("."):
        return {"ok": False, "code": EXIT_USAGE, "slug": slug,
                "error": f"非法 slug：{slug!r}（不得含路径分隔符或 ..）"}

    # 端点信任闸门：非官方 host（env 覆写所致）默认拒绝，须显式 --allow-custom-endpoint
    if not allow_custom_endpoint:
        for name, u in (("SKILLHUB_SEARCH_URL", SEARCH_URL), ("SKILLHUB_DOWNLOAD_URL", DOWNLOAD_URL)):
            if not _endpoint_trusted(u):
                return {"ok": False, "code": EXIT_UNTRUSTED_ENDPOINT, "slug": slug,
                        "error": (f"{name} 指向非官方端点：{u!r}——默认仅信任 https://{OFFICIAL_HOST}。"
                                  f"确需镜像/联调请显式加 --allow-custom-endpoint（自担信任风险）。")}

    dest = dest_root / slug
    if dest.exists() and not force:
        return {"ok": False, "code": EXIT_ALREADY_INSTALLED, "slug": slug,
                "error": f"已存在：{dest}（如需覆盖请加 --force）", "dest": str(dest)}

    st = check_published(slug, handle)
    if not st["published"]:
        return {"ok": False, "code": EXIT_NOT_PUBLISHED, "slug": slug,
                "error": (f"{slug} 未在 SkillHub 上架 —— 本脚本只安装已公开发布的 A 档技能；"
                          f"未发布或 B 档（涉密输入）技能请勿安装，改由 ct-advisor 本地作答。"),
                "checked_url": SEARCH_URL}

    if dry_run:
        return {"ok": True, "code": EXIT_OK, "slug": slug, "dry_run": True,
                "version": st["version"], "handle": st["handle"], "dest": str(dest),
                "message": f"[dry-run] 已上架 v{st['version']}，将安装到 {dest}"}

    try:
        blob = fetch_zip_bytes(slug)
    except (urllib.error.URLError, OSError) as e:
        return {"ok": False, "code": EXIT_DOWNLOAD_FAILED, "slug": slug,
                "error": f"下载失败：{e}"}

    # 完整性锚定：可选 --expect-sha256 对下载字节做内容摘要校验（防中间人换包）
    blob_sha = hashlib.sha256(blob).hexdigest()
    if expect_sha256 and blob_sha.lower() != expect_sha256.strip().lower():
        return {"ok": False, "code": EXIT_INTEGRITY_FAILED, "slug": slug,
                "error": f"包摘要不符：期望 {expect_sha256}，实际 {blob_sha}——拒绝安装。"}

    try:
        zf = zipfile.ZipFile(io.BytesIO(blob))
    except zipfile.BadZipFile:
        return {"ok": False, "code": EXIT_BAD_ARCHIVE, "slug": slug,
                "error": (f"下载内容不是合法 zip（{len(blob)} 字节）——"
                          f"常见原因：CLI/端点指向内网 LB 或返回了 HTML 错误页。")}
    # CRC 全量校验：所有条目解压后与存档 CRC 逐一比对，坏包/篡改包直接出局
    bad = zf.testzip()
    if bad is not None:
        zf.close()
        return {"ok": False, "code": EXIT_INTEGRITY_FAILED, "slug": slug,
                "error": f"zip 条目 CRC 校验失败：{bad}——拒绝安装。"}
    names = zf.namelist()
    if not any(n == "SKILL.md" or n.endswith("/SKILL.md") for n in names):
        return {"ok": False, "code": EXIT_BAD_ARCHIVE, "slug": slug,
                "error": f"zip 内未找到 SKILL.md（条目 {len(names)} 个），疑似不是技能包。"}
    # 符号链接条目拒绝：zip symlink + 后续写入组合可逃逸目录边界（越出技能根写文件）
    for info in zf.infolist():
        mode = info.external_attr >> 16
        if mode and _stat.S_ISLNK(mode):
            return {"ok": False, "code": EXIT_INTEGRITY_FAILED, "slug": slug,
                    "error": f"zip 含符号链接条目：{info.filename}——拒绝安装。"}

    # 先解压到同盘临时目录再改名 —— 避免半成品目录被探测成「已安装」
    dest_root.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix=f".{slug}.tmp-", dir=str(dest_root)))
    try:
        # zip 为扁平结构（SKILL.md 在根），故整体解压到临时目录
        for n in names:
            target = (tmp / n).resolve()
            if not str(target).startswith(str(tmp.resolve())):
                raise ValueError(f"zip 含越界路径：{n}")
        zf.extractall(str(tmp))
        zf.close()
        if dest.exists() and force:
            shutil.rmtree(str(dest))
        tmp.rename(dest)
    except Exception as e:  # noqa: BLE001 — 落盘失败一律清临时目录后上报
        shutil.rmtree(str(tmp), ignore_errors=True)
        return {"ok": False, "code": EXIT_BAD_ARCHIVE, "slug": slug,
                "error": f"解压失败：{e}"}

    return {"ok": True, "code": EXIT_OK, "slug": slug, "dest": str(dest),
            "version": st["version"], "handle": st["handle"], "bytes": len(blob),
            "sha256": blob_sha, "entries": len(names),
            "message": f"✓ 已安装 {slug} v{st['version']} → {dest}（sha256 {blob_sha[:12]}…）"}


def _refresh_registry():
    """安装/卸载后刷新 sibling_registry。静默失败——注册表过期会有调用侧兜底。"""
    try:
        from subprocess import run
        import subprocess
        scripts_dir = Path(__file__).resolve().parent.parent / "scripts"
        run([sys.executable, str(scripts_dir / "discover_siblings.py"), "--force"],
            capture_output=True, timeout=30)
    except Exception:
        pass  # 静默——注册表刷新非关键路径}


def main(argv: list | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="安装 ct 系列 A 档兄弟技能（SkillHub）。只装已上架技能，先核验后下载。")
    ap.add_argument("slug", help="技能 slug，如 ct-registry")
    ap.add_argument("--dir", default=SKILLS_DIR,
                    help=f"技能根目录（默认 {SKILLS_DIR}；env CT_SKILLS_DIR 可覆盖）")
    ap.add_argument("--handle", default=None, help="限定 SkillHub 发布者 handle（可选）")
    ap.add_argument("--force", action="store_true", help="覆盖已存在的同名技能目录")
    ap.add_argument("--dry-run", action="store_true", help="只核验并打印计划，不下载不落盘")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出（供上游解析）")
    ap.add_argument("--allow-custom-endpoint", action="store_true",
                    help="接受 env 覆写的非官方 SkillHub 端点（镜像/联调用，自担信任风险）")
    ap.add_argument("--expect-sha256", default=None, metavar="HEX",
                    help="锚定下载包的 sha256，不符则拒绝安装（可选）")
    args = ap.parse_args(argv)

    res = install(args.slug, Path(args.dir), force=args.force,
                  dry_run=args.dry_run, handle=args.handle,
                  allow_custom_endpoint=args.allow_custom_endpoint,
                  expect_sha256=args.expect_sha256)
    # 安装成功后刷新 sibling_registry
    if res.get("ok"):
        _refresh_registry()
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(res.get("message") or res.get("error"))
    return res["code"]


if __name__ == "__main__":
    sys.exit(main())
