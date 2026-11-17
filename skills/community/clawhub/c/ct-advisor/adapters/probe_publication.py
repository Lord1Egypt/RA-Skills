#!/usr/bin/env python3
"""probe_publication.py — 复核 tiers 注册表里各技能的对外发布状态。

权威源 = **SkillHub**（skillhub.cn 技能市场），不是 GitHub。
    判据：SkillHub 搜索 API 中能按 publicSlug 精确命中 → 已发布。
    为什么不用 GitHub：GitHub 上「已创建但从未推送内容」的空占位仓库同样返回
    HTTP 200（API `size == 0`），会得出「已发布」的假结论。2026-09-10 的
    ct-pipeline 事故即由此而来——按 200/404 核定把 published 误标为 true，
    install_required 分支因此给用户一个 `git clone` 后仍是空目录的假安装地址。
    SkillHub 只有真正完成上架（含服务端校验 + 版本号占用）才会被搜到，故更准。

GitHub 仍会一并探测，但仅作**诊断**用途（说明「为什么没上架」，如空占位仓库），
不参与 published 判定。

用法：
    python adapters/probe_publication.py                    # 人读表格 + 漂移告警
    python adapters/probe_publication.py --json             # 机器可读
    python adapters/probe_publication.py --fix              # 实测结果回写注册表（仅 published 字段）
    python adapters/probe_publication.py --only ct-pipeline ct-samplesize
    python adapters/probe_publication.py --no-github        # 只查 SkillHub，跳过 GitHub 诊断

退出码：0 = 注册表与实测一致；1 = 存在漂移（可挂 CI / 发布前闸门）；2 = 回写出错。
零副作用：默认只读网络与本地文件；仅 --fix 会改写 tool_mapping.json。
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAPPING_PATH = ROOT / "scripts" / "tool_mapping.json"
DEFAULT_SEARCH_URL = "https://api.skillhub.cn/api/v1/search"
GITHUB_API = "https://api.github.com/repos"
TIMEOUT = 25

# SkillHub CLI（skill-publish 技能约定）的 metadata.json，可从中读实际 search URL。
_META_CANDIDATES = [
    Path.home() / ".skillhub" / "metadata.json",
]


def load_mapping() -> dict:
    with open(MAPPING_PATH, encoding="utf-8") as f:
        return json.load(f)


def _metadata_search_urls() -> list:
    """从 SkillHub CLI 的 metadata.json 收集候选 search URL（多个安装位置）。"""
    out = []
    for p in _META_CANDIDATES:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            u = d.get("skills_search_url")
            if u:
                out.append(u)
        except Exception:  # noqa: BLE001 — 缺文件/无权限一律忽略
            continue
    return out


def _search_candidates(cli_value: str | None = None) -> list:
    """候选 search URL，按可靠性排序。

    顺序：--search-url > env > **公网 api.skillhub.cn** > CLI metadata.json 里的地址。
    公网地址排在内网/本机元数据之前是刻意的：某些环境里 metadata.json 指向内网 LB
    （http + 证书不匹配），本机直连会失败；公网端点才是对外可复现的判据。
    """
    cands = []
    for u in (cli_value, os.environ.get("SKILLHUB_SEARCH_URL"), DEFAULT_SEARCH_URL):
        if u and u not in cands:
            cands.append(u)
    meta = [u for u in _metadata_search_urls() if u not in cands]
    # 内网 http 端点排到最后（优先 https）
    meta.sort(key=lambda u: 0 if u.startswith("https://") else 1)
    cands.extend(meta)
    return cands


def _get_json(url: str, timeout: int = TIMEOUT, retries: int = 2, backoff: float = 1.5) -> dict:
    """GET + 解析 JSON；对瞬时故障（限流 / 超时 / 连接重置）做少量重试后退避。

    SkillHub 与 GitHub 在短时间内的连续请求会被限流（实测：连续跑两轮后 GitHub 返 403、
    SkillHub 偶发返回非 JSON）。少量重试可让「未能判定」只反映真实不可达，而不是瞬时抖动。
    """
    last = None
    for attempt in range(max(1, retries)):
        req = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "User-Agent": "ct-advisor-probe-publication",
        })
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8", "replace"))
        except Exception as e:  # noqa: BLE001 — 重试后再失败才上报
            last = e
            if attempt + 1 < max(1, retries):
                time.sleep(backoff * (attempt + 1))
    raise last  # type: ignore[misc]


# ---------------------------------------------------------------------------
# 一、SkillHub（权威判据）
# ---------------------------------------------------------------------------

# 已确认可用的端点缓存：避免每个 slug 都从头重试失败端点（21 项 × N 端点会很慢）
_WORKING_URL: list = []


def probe_skillhub(slug: str, candidates: list, handle: str | None = None) -> dict:
    """在 SkillHub 搜索 slug，精确命中即视为「已发布」。

    依次尝试 candidates，首个应答成功者即定为本轮端点（缓存复用）。
    返回 {published, version, handle, downloads, updated_at, url, error}。
    精确命中 = 结果条目的 slug 或 namespace.publicSlug 与 slug 完全相同
    （避免 "ct-safety" 命中 "ct-safety-review" 之类的包含式误判）。
    """
    tried = []
    order = (_WORKING_URL + [u for u in candidates if u not in _WORKING_URL]) or candidates
    for url in order:
        qs = urllib.parse.urlencode({"q": slug, "limit": 20})
        try:
            d = _get_json(f"{url}?{qs}")
        except Exception as e:  # noqa: BLE001 — 逐个端点降级，全失败才放弃
            tried.append(f"{url} → {e}")
            continue
        if not isinstance(d, dict) or "results" not in d:
            tried.append(f"{url} → 应答非预期结构")
            continue
        _WORKING_URL[:] = [url]
        hits = [h for h in (d.get("results") or [])
                if h.get("slug") == slug or (h.get("namespace") or {}).get("publicSlug") == slug]
        if handle:
            hits = [h for h in hits if (h.get("namespace") or {}).get("handle") == handle]
        if not hits:
            return {"published": False, "version": None, "handle": None, "downloads": None,
                    "updated_at": None, "url": url, "error": None}
        h = hits[0]
        return {
            "published": True,
            "version": h.get("version"),
            "handle": (h.get("namespace") or {}).get("handle"),
            "downloads": h.get("downloads"),
            "updated_at": h.get("updated_at"),
            "url": url,
            "error": None,
        }
    return {"published": None, "url": None,
            "error": "全部端点失败：" + " ｜ ".join(tried[:3])}


# ---------------------------------------------------------------------------
# 二、GitHub（仅诊断：解释「为什么没上架」）
# ---------------------------------------------------------------------------

def _slug_to_repo(github: str) -> str | None:
    m = re.match(r"https?://github\.com/([^/]+)/([^/#?]+)", github or "")
    return f"{m.group(1)}/{m.group(2)}" if m else None


def probe_github(repo: str) -> dict:
    """探测仓库存在性与是否为空。HTTP 200 只说明「存在」，size==0 才是空仓证据。"""
    try:
        d = _get_json(f"{GITHUB_API}/{repo}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"exists": False, "empty": None, "size": None, "error": None}
        return {"exists": None, "empty": None, "size": None, "error": f"HTTP {e.code}"}
    except Exception as e:  # noqa: BLE001
        return {"exists": None, "empty": None, "size": None, "error": str(e)}
    size = int(d.get("size") or 0)
    return {"exists": True, "empty": size == 0, "size": size,
            "private": bool(d.get("private")), "error": None}


# ---------------------------------------------------------------------------
# 三、审计 + 渲染
# ---------------------------------------------------------------------------

def audit(only: list | None = None, search_url: str | None = None,
          handle: str | None = None, skip_github: bool = False) -> list:
    mapping = load_mapping()
    registry = (mapping.get("tiers") or {}).get("registry") or {}
    cands = _search_candidates(search_url)
    rows = []
    for slug, entry in registry.items():
        if only and slug not in only:
            continue
        if entry.get("tier") == "meta":
            continue  # 元层（ct-base / ct-update）不是安装对象，不参与发布判定
        sh = probe_skillhub(slug, cands, handle)
        declared = bool(entry.get("published"))
        gh = {}
        if not skip_github:
            repo = _slug_to_repo(entry.get("github") or f"https://github.com/medstatstar/{slug}")
            if repo:
                gh = probe_github(repo)
        ver = sh.get("published")
        rows.append({
            "slug": slug,
            "tier": entry.get("tier"),
            "declared": declared,
            "verified": ver,
            "drift": (ver is not None) and (ver != declared),
            "skillhub": sh,
            "github": gh,
            "why": _explain(sh, gh),
        })
    return rows


def _explain(sh: dict, gh: dict) -> str:
    """给出一句「为什么是这个结论」，特别标出 SkillHub 与 GitHub 不一致的情形。"""
    if sh.get("error"):
        return f"SkillHub 查询失败：{sh['error']}"
    if sh.get("published"):
        return f"SkillHub 已上架 v{sh.get('version')}（{sh.get('handle')}）"
    # 未上架 → 用 GitHub 诊断补充原因
    if not gh:
        return "SkillHub 未上架"
    if gh.get("error"):
        return f"SkillHub 未上架；GitHub 探测失败：{gh['error']}"
    if not gh.get("exists"):
        return "SkillHub 未上架；GitHub 无此仓库（404）"
    if gh.get("empty"):
        return "SkillHub 未上架；GitHub 仓库存在但为空（size=0）→ 未发布"
    return (f"SkillHub 未上架；⚠️ GitHub 仓库存在且非空（size={gh.get('size')}KB）"
            f"→ 疑似「推了 GitHub 但没上架 SkillHub」，请人工确认")


def render(rows: list, candidates: list, skip_github: bool) -> int:
    unknown = [r for r in rows if r["verified"] is None]
    used = _WORKING_URL[0] if _WORKING_URL else "(未连通)"
    print("ct-advisor · 对外发布状态复核")
    print("  权威源：SkillHub —— 实际使用 %s" % used)
    print("  候选端点：" + " ｜ ".join(candidates))
    print("  GitHub 仅作诊断（空占位仓库 HTTP 200 ≠ 已发布）"
          + ("　[本轮机 GitHub 已跳过]" if skip_github else ""))
    print("=" * 96)
    print("  %-20s %-5s %-10s %-10s %s" % ("技能", "档", "注册表", "SkillHub", "依据"))
    print("-" * 96)
    drift = []
    for r in rows:
        v = "—" if r["verified"] is None else ("true" if r["verified"] else "false")
        mark = "↯" if r["drift"] else " "
        print("  %s %-18s %-5s %-10s %-10s %s"
              % (mark, r["slug"], r["tier"], "true" if r["declared"] else "false", v, r["why"]))
        if r["drift"]:
            drift.append(r)
    print("=" * 96)
    if unknown:
        print("  ⚠️ %d 项**未能判定**（SkillHub 全部端点不可达），其 published 未参与比对：" % len(unknown))
        print("     " + ", ".join(r["slug"] for r in unknown))
        print("     端点不可达时不会误报「一致」——请修好网络后重跑。")
    if drift:
        print("  ⚠️ 发现 %d 处漂移（注册表与 SkillHub 实际不一致）：" % len(drift))
        for r in drift:
            print("     - %s: 注册表 published=%s → 实测 %s（%s）"
                  % (r["slug"], r["declared"], r["verified"], r["why"]))
        print("     修复：python adapters/probe_publication.py --fix")
    elif not unknown:
        print("  ✓ 注册表与 SkillHub 实际发布状态一致（共 %d 项）" % len(rows))
    elif len(unknown) < len(rows):
        ok = len(rows) - len(unknown)
        print("  ✓ 已判定的 %d 项与 SkillHub 一致；另有 %d 项未判定。" % (ok, len(unknown)))
    return 1 if (drift or unknown) else 0


def apply_fix(rows: list) -> int:
    """把实测结果回写 tool_mapping.json 的 published 字段（行级替换，保留原排版）。

    注意：必须**字节级**读写（read_bytes + decode），不能用 read_text/write_text ——
    后者会做通用换行转换，把文件的 CRLF 统一成 LF，产生「整文件 diff」这种
    与本次改动无关的噪音（2026-09-10 实测踩到）。
    """
    targets = {r["slug"]: r["verified"] for r in rows if r["drift"] and r["verified"] is not None}
    if not targets:
        print("无需修复（无漂移）。")
        return 0
    raw = MAPPING_PATH.read_bytes()
    text = raw.decode("utf-8")
    changed = 0
    for slug, ver in targets.items():
        pat = re.compile(r'("' + re.escape(slug) + r'":\s*\{[^\n]*?"published":\s*)(true|false)')
        text, n = pat.subn(lambda m: m.group(1) + ("true" if ver else "false"), text, count=1)
        if n:
            changed += 1
            print("  ✓ %s: published → %s" % (slug, "true" if ver else "false"))
    if changed:
        # 回写前先自校验，避免把坏 JSON 落盘
        try:
            json.loads(text)
        except json.JSONDecodeError as e:
            print("  ✗ 替换后 JSON 解析失败，已放弃写入：%s" % e)
            return 2
        MAPPING_PATH.write_bytes(text.encode("utf-8"))
        same_eol = (b"\r\n" in raw) == (b"\r\n" in text.encode("utf-8"))
        print("  JSON 校验通过（%d 处已更新%s）"
              % (changed, "，换行风格保持原样" if same_eol else "，⚠️ 换行风格发生变化"))
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="复核 tiers 注册表的对外发布状态（权威源：SkillHub）")
    p.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    p.add_argument("--fix", action="store_true", help="把实测结果回写 tool_mapping.json")
    p.add_argument("--only", nargs="*", help="只探测指定 slug")
    p.add_argument("--search-url", help="SkillHub 搜索 API 地址（默认读 CLI metadata.json）")
    p.add_argument("--handle", help="只认指定发布者 handle（如 user_xxx）")
    p.add_argument("--no-github", action="store_true", help="跳过 GitHub 诊断探测")
    args = p.parse_args(argv)

    url = _search_candidates(args.search_url)
    rows = audit(args.only, args.search_url, args.handle, args.no_github)

    if args.json:
        print(json.dumps({"authority": "skillhub",
                          "search_url": _WORKING_URL[0] if _WORKING_URL else None,
                          "candidates": url,
                          "rows": [{k: v for k, v in r.items() if k != "github"}
                                   for r in rows]},
                         ensure_ascii=False, indent=2))
        return 1 if any(r["drift"] or r["verified"] is None for r in rows) else 0

    rc = render(rows, url, args.no_github)
    if args.fix:
        rc = apply_fix(rows) or rc
    return rc


if __name__ == "__main__":
    sys.exit(main())
