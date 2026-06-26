#!/usr/bin/env python3
"""
ASMR.one 音频搜索/下载/压缩工具 - v4

命令:
  search <关键词>   搜索作品（多关键词 AND，仅最新 ~600 个）
  hot               热门推荐
  info <RJ编号>     查看作品详情
  download <RJ编号> 下载并压缩
  sendlist <RJ编号> 列出已下载文件
  collection        查看收藏列表
  check             检查运行环境（依赖/网络）
  config            配置文件管理

配置优先级: CLI 参数 > 环境变量 > 配置文件 > 默认值

快速上手:
  1. asmr_tool.py config init           # 交互式配置（代理/输出目录）
  2. asmr_tool.py check                 # 验证环境
  3. asmr_tool.py search "阳向葵ゅか"  # 搜索作品
  4. asmr_tool.py download RJxxxxxx    # 下载
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

# === 外部依赖 ===
try:
    import requests
except ImportError:
    print("❌ 需要 requests 库，请运行: pip3 install requests")
    sys.exit(1)

# === 路径常量 ===
CONFIG_DIR = Path.home() / ".config" / "asmr-tool"
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_OUTPUT_DIR = Path.home() / "asmr_downloads"
DEFAULT_COLLECTION_FILE = CONFIG_DIR / "collection.json"

# === API ===
API_MIRRORS = [
    "https://api.asmr-200.com",
    "https://api.asmr.one",
    "https://api.asmr-100.com",
    "https://api.asmr-300.com",
]
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/121.0.0.0 Safari/537.36"
)
QQ_AUDIO_MAX_BYTES = 20 * 1024 * 1024  # 20MB
VBR_BITRATE = {"q0":"245k","q1":"225k","q2":"190k","q3":"175k","q4":"160k",
               "q5":"130k","q6":"115k","q7":"100k","q8":"85k","q9":"65k"}

# =============================================
# 配置系统
# =============================================

DEFAULT_CONFIG = {
    "proxy": "",
    "output_dir": str(DEFAULT_OUTPUT_DIR),
    "default_vbr": "q3",
    "default_bitrate": "128k",
    "qq_target": "",
}


def load_config() -> dict:
    """加载配置文件，不存在则返回默认值"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, encoding="utf-8") as f:
                cfg = json.load(f)
            # 合并默认值（新版本可能增加了字段）
            merged = dict(DEFAULT_CONFIG)
            merged.update(cfg)
            return merged
        except:
            print("  [⚠️] 配置文件损坏，使用默认值")
    return dict(DEFAULT_CONFIG)


def save_config(cfg: dict):
    """保存配置文件"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    print(f"  ✅ 配置已保存: {CONFIG_FILE}")
    os.chmod(CONFIG_FILE, 0o600)  # 敏感文件权限


def resolve_args(cfg: dict, args, keys: list) -> dict:
    """
    解析参数：CLI 参数 > 环境变量 > 配置文件 > 默认值
    返回填充好的参数字典
    """
    env_map = {
        "proxy": "ASMR_PROXY",
        "output_dir": "ASMR_OUTPUT_DIR",
        "qq_target": "QQ_TARGET",
        "default_vbr": "ASMR_VBR",
        "default_bitrate": "ASMR_BITRATE",
    }
    defaults_map = {
        "proxy": "",
        "output_dir": str(DEFAULT_OUTPUT_DIR),
        "qq_target": "",
        "default_vbr": "q3",
        "default_bitrate": "128k",
    }

    result = {}
    for key in keys:
        # CLI 参数优先
        cli_val = getattr(args, key, None)
        if cli_val:
            result[key] = cli_val
            continue

        # 环境变量
        env_var = env_map.get(key)
        if env_var:
            env_val = os.environ.get(env_var)
            if env_val:
                result[key] = env_val
                continue

        # 配置文件
        if key in cfg and cfg[key]:
            result[key] = cfg[key]
            continue

        # 默认值
        result[key] = defaults_map.get(key, "")

    return result


def cmd_config(args):
    """配置管理"""
    if args.action == "show":
        cfg = load_config()
        masked = dict(cfg)
        print(f"\n{'='*45}")
        print(f"  ⚙️  ASMR 工具配置")
        print(f"{'='*45}")
        print(f"  配置文件: {CONFIG_FILE}")
        for k, v in masked.items():
            print(f"    {k:20s} = {v}")
        print()

    elif args.action == "init":
        print(f"\n{'='*45}")
        print(f"  交互式配置初始化")
        print(f"{'='*45}")
        cfg = load_config()

        # Proxy
        current = cfg.get("proxy", "")
        hint = f" [{current}]" if current else ""
        inp = input(f"  代理地址 (如 http://127.0.0.1:7890){hint}:\n  > ").strip()
        if inp:
            cfg["proxy"] = inp

        # Output dir
        current = cfg.get("output_dir", str(DEFAULT_OUTPUT_DIR))
        inp = input(f"  下载目录 [{current}]:\n  > ").strip()
        if inp:
            cfg["output_dir"] = inp

        # VBR quality
        current = cfg.get("default_vbr", "q3")
        inp = input(f"  默认 VBR 质量 (q0~q9, 数字越高质量越好) [{current}]:\n  > ").strip()
        if inp:
            cfg["default_vbr"] = inp

        save_config(cfg)

    elif args.action == "set":
        cfg = load_config()
        if args.key in cfg:
            cfg[args.key] = args.value
            save_config(cfg)
        else:
            valid_keys = ", ".join(cfg.keys())
            print(f"[x] 无效配置项。可用: {valid_keys}")

    elif args.action == "get":
        cfg = load_config()
        if args.key in cfg:
            print(cfg[args.key])
        else:
            valid_keys = ", ".join(cfg.keys())
            print(f"[x] 无效配置项。可用: {valid_keys}")


# =============================================
# 环境检查
# =============================================

def cmd_check(args):
    """检查运行环境"""
    cfg = load_config()
    resolved = resolve_args(cfg, args, ["proxy"])
    errors = 0

    print(f"\n{'='*45}")
    print(f"  🩺 环境检查")
    print(f"{'='*45}")

    # 1. Python
    print(f"\n  [Python]")
    print(f"   版本: {sys.version.split()[0]}")
    print(f"   ✅ OK")

    # 2. requests
    print(f"\n  [requests]")
    try:
        import requests
        print(f"   版本: {requests.__version__}")
        print(f"   ✅ OK")
    except ImportError:
        print(f"   ❌ 未安装 → pip3 install requests")
        errors += 1

    # 3. ffmpeg
    print(f"\n  [ffmpeg]")
    for cmd, label in [("ffmpeg", "ffmpeg"), ("ffprobe", "ffprobe")]:
        r = subprocess.run(["which", cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if r.returncode == 0:
            ver = subprocess.run([cmd, "-version"], capture_output=True, text=True, timeout=5)
            first_line = ver.stdout.split("\n")[0] if ver.stdout else "?"
            print(f"   {label}: ✅ {first_line[:60]}")
        else:
            print(f"   {label}: ❌ 未找到")
            print(f"   安装: sudo apt install ffmpeg  (或 brew install ffmpeg)")
            errors += 1

    # 4. 网络
    proxy = resolved.get("proxy", "")
    print(f"\n  [网络]")
    if proxy:
        print(f"   代理: {proxy}")
    else:
        print(f"   代理: 未设置（可能直连）")
    
    conn = check_connectivity(proxy)
    print(f"   外网: {'✅' if conn['internet'] else '❌'}")
    print(f"   ASMR.one: {'✅' if conn['asmr'] else '❌'}")
    if not conn['internet']:
        print(f"   → 无法访问外网，跳过网络依赖的功能")
    elif not conn['asmr']:
        if not proxy:
            print(f"   → 可能需要代理: asmr_tool.py config set proxy http://yourproxy")
        else:
            print(f"   → ASMR.one 服务可能暂时不可用")
        errors += 1

    # 6. 配置
    print(f"\n  [配置]")
    if CONFIG_FILE.exists():
        print(f"   ✅ 配置文件: {CONFIG_FILE}")
    else:
        print(f"   ⚠️ 未创建配置文件")
        print(f"   提示: asmr_tool.py config init")
    print(f"   输出目录: {cfg.get('output_dir', str(DEFAULT_OUTPUT_DIR))}")

    # 7. 收藏文件
    cf = Path(cfg.get("collection_file", DEFAULT_COLLECTION_FILE))
    if not cf.exists():
        cf = Path(DEFAULT_COLLECTION_FILE)
    print(f"   收藏文件: {cf} ({'✅' if cf.exists() else '📭 空'})")

    # Summary
    print(f"\n{'='*45}")
    if errors == 0:
        print(f"  ✅ 一切正常，可以开始使用！")
    else:
        print(f"  ⚠️ 发现 {errors} 个问题需要修复")
    print()


# =============================================
# 工具函数
# =============================================

def sanitize_filename(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|]', '_', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name[:100]


def fmt_size(bytes_: int) -> str:
    for unit in ['B','KB','MB','GB']:
        if bytes_ < 1024: return f"{bytes_:.1f}{unit}"
        bytes_ /= 1024
    return f"{bytes_:.1f}TB"


def normalize_rj(code: str) -> str:
    return f"RJ{code.upper().strip().lstrip('RJ')}"


def get_collection_file(cfg: dict) -> Path:
    cf = cfg.get("collection_file", "")
    if cf:
        return Path(cf)
    return DEFAULT_COLLECTION_FILE


# =============================================
# 网络
# =============================================

def make_session(proxy: str = None) -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": USER_AGENT,
        "Referer": "https://asmr.one/",
        "Origin": "https://asmr.one",
    })
    if proxy:
        s.proxies = {"http": proxy, "https": proxy}
    s.allow_redirects = False
    return s


def api_get(session: requests.Session, endpoint: str, timeout: int = 30):
    """尝试所有 API 镜像"""
    for mirror in API_MIRRORS:
        url = f"{mirror}{endpoint}"
        try:
            resp = session.get(url, timeout=timeout)
            if resp.status_code == 200:
                return resp.json()
            if resp.status_code == 401:
                return {"_auth_error": True}
        except requests.RequestException:
            continue
    return None


def check_connectivity(proxy: str = None) -> dict:
    """检查外网和 ASMR.one 可达性
    返回: {"internet": bool, "asmr": bool}"""
    proxies = {"http": proxy, "https": proxy} if proxy else None
    result = {"internet": False, "asmr": False}

    for url, key in [
        ("https://www.google.com/generate_204", "internet"),
        ("https://asmr.one", "asmr"),
    ]:
        try:
            r = requests.get(url, headers={"User-Agent": USER_AGENT},
                             proxies=proxies, timeout=8)
            result[key] = r.status_code in (200, 204, 301, 302)
        except:
            pass

    return result


# =============================================
# 元数据获取
# =============================================

def get_work_meta(session, rj_id):
    """获取作品元数据"""
    print(f"  → 获取作品信息: {rj_id}")
    numeric = rj_id.replace("RJ", "")
    
    data = api_get(session, f"/api/workInfo/{rj_id}")
    if not data or data.get("_auth_error"):
        data = api_get(session, f"/api/workInfo/{numeric}")
    if not data or data.get("_auth_error"):
        data = api_get(session, f"/api/workInfo/RJ{numeric}")
    if not data or data.get("_auth_error"):
        return None
    
    return {
        "rj_id": rj_id,
        "numeric_id": data.get("id", numeric),
        "title": data.get("title", "Unknown"),
        "circle": data.get("name", "Unknown"),
        "cv": ", ".join(v.get("name", "") for v in data.get("vas", [])),
        "tags": [t.get("name", "") for t in data.get("tags", [])],
        "price": data.get("price", 0),
        "dl_count": data.get("dl_count", 0),
        "rating": data.get("rate_average_2dp", 0),
        "release_date": data.get("release", ""),
        "cover_url": data.get("mainCoverUrl", ""),
        "nsfw": data.get("nsfw", False),
    }


# =============================================
# 搜索
# =============================================

def cmd_search(args):
    keyword = args.keyword
    cfg = load_config()
    r = resolve_args(cfg, args, ["proxy", "output_dir"])
    session = make_session(r["proxy"])
    
    # 网络检查
    conn = check_connectivity(r["proxy"])
    if not conn["internet"]:
        print("\n  [⚠️] 无法访问外网，搜索功能需要网络连接")
        print("  → 检查代理: asmr_tool.py config set proxy http://你的代理地址")
        return
    if not conn["asmr"]:
        print(f"\n  [⚠️] 无法连接 ASMR.one，服务可能暂时不可用")
        return
    
    print(f"\n🔍 搜索: {keyword}")
    print(f"  ⚠️ API 限制：仅覆盖最新 ~600 个作品")
    
    results = []
    kw_lower = keyword.lower().strip()
    keywords = [k for k in re.split(r'[\s,，、]+', kw_lower) if k]
    
    for page in range(1, 31):
        data = api_get(session, f"/api/works?page={page}")
        if not data or "works" not in data:
            break
        works = data["works"]
        if not works:
            break
        
        page_matched = 0
        for w in works:
            title = w.get("title", "") or ""
            circle = w.get("name", "") or ""
            vas = [v.get("name", "") for v in w.get("vas", [])]
            tags = [t.get("name", "") for t in w.get("tags", [])]
            haystack = f"{title} {circle} {' '.join(vas)} {' '.join(tags)}".lower()
            
            if keywords:
                match = all(kw in haystack for kw in keywords)
            else:
                match = True
            
            if match:
                page_matched += 1
                results.append({
                    "id": str(w.get("id", "")),
                    "title": title,
                    "circle": circle,
                    "vas": ", ".join(vas),
                    "release": w.get("release", ""),
                    "dl_count": w.get("dl_count", 0),
                    "price": w.get("price", 0),
                    "rate": w.get("rate_average_2dp", 0),
                    "duration": w.get("duration", 0),
                    "nsfw": w.get("nsfw", False),
                    "has_subtitle": w.get("has_subtitle", False),
                })
        
        if page_matched == 0 and page > 10:
            break
    
    if not results:
        print(f"\n  😿 没有找到匹配的作品")
        print(f"  → 确认关键词，或已知 RJ 编号直接: asmr_tool.py info RJxxxx")
        return
    
    _print_results(keyword, results, r["output_dir"])


def cmd_hot(args):
    cfg = load_config()
    r = resolve_args(cfg, args, ["proxy", "output_dir"])
    session = make_session(r["proxy"])
    print(f"\n🔥 热门作品\n")
    
    results = []
    for page in [1, 2, 3]:
        data = api_get(session, f"/api/works?page={page}")
        if not data or "works" not in data:
            break
        for w in data["works"]:
            if w.get("dl_count", 0) > 0:
                results.append({
                    "id": str(w.get("id", "")),
                    "title": w.get("title", ""),
                    "circle": w.get("name", ""),
                    "vas": ", ".join(v.get("name", "") for v in w.get("vas", [])),
                    "release": w.get("release", ""),
                    "dl_count": w.get("dl_count", 0),
                    "price": w.get("price", 0),
                    "rate": w.get("rate_average_2dp", 0),
                    "duration": w.get("duration", 0),
                    "nsfw": w.get("nsfw", False),
                })
    
    results.sort(key=lambda r: r["dl_count"], reverse=True)
    _print_results("(热门推荐)", results[:20], r["output_dir"])


def _print_results(keyword, results, output):
    print(f"\n  找到 {len(results)} 个匹配作品:\n")
    for i, r in enumerate(results, 1):
        rid = r["id"]
        dur_m = r["duration"] // 60 if r["duration"] else 0
        flag = "🔞" if r["nsfw"] else ""
        sub = "📝" if r.get("has_subtitle") else ""
        print(f"  [{i:2d}] RJ{rid} {flag}{sub}")
        print(f"       {r['title'][:55]}")
        if r["circle"]:
            print(f"       社团: {r['circle'][:30]}")
        if r["vas"]:
            print(f"       CV: {r['vas'][:40]}")
        print(f"       {r['release']} | DL:{r['dl_count']} | ¥{r['price']} | ⭐{r['rate']} | {dur_m}min")
        print()
    
    out_dir = Path(output or str(DEFAULT_OUTPUT_DIR))
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_kw = sanitize_filename(keyword.replace(" ","_")) if keyword else "hot"
    sf = out_dir / f"search_{safe_kw}_{int(time.time())}.json"
    with open(sf, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"  结果已保存: {sf}")


# =============================================
# 详情
# =============================================

def cmd_info(args):
    meta = _fetch_and_print_meta(args)
    if not meta:
        sys.exit(1)


def _fetch_and_print_meta(args):
    rj_id = normalize_rj(args.rj_code)
    cfg = load_config()
    r = resolve_args(cfg, args, ["proxy"])
    session = make_session(r["proxy"])
    meta = get_work_meta(session, rj_id)
    if not meta:
        print(f"[x] 无法获取作品信息: {args.rj_code}")
        print("  可能原因: 作品不存在 / 需要代理")
        return None
    
    print(f"\n{'='*50}")
    print(f"  📀 {meta['title']}")
    print(f"{'='*50}")
    print(f"  RJ编号:  {meta['rj_id']}")
    print(f"  社团:    {meta['circle']}")
    print(f"  CV:      {meta['cv']}")
    print(f"  价格:    ¥{meta['price']}")
    print(f"  下载:    {meta['dl_count']} DL")
    print(f"  评分:    ⭐ {meta['rating']}/5")
    print(f"  发布:    {meta['release_date']}")
    if meta['tags']:
        print(f"  标签:    {', '.join(meta['tags'][:10])}")
    
    numeric_id = meta.get("numeric_id", rj_id.replace("RJ",""))
    tracks = api_get(session, f"/api/tracks/{numeric_id}?v=2")
    if tracks and isinstance(tracks, list):
        def count(nodes):
            t = 0
            for n in nodes:
                if isinstance(n, dict) and n.get("type") != "folder":
                    t += 1
                t += count(n.get("children", []))
            return t
        print(f"  音轨数:  {count(tracks)}")
    print(f"  封面:    {meta['cover_url']}")
    print()
    return meta


# =============================================
# 下载
# =============================================

def cmd_download(args):
    rj_id = normalize_rj(args.rj_code)
    cfg = load_config()
    r = resolve_args(cfg, args, ["proxy", "output_dir", "default_vbr", "default_bitrate"])
    session = make_session(r["proxy"])
    base_dir = Path(r["output_dir"])
    work_dir = base_dir / rj_id
    
    # 模式参数
    send_mode = args.mode  # "voice" | "file"
    use_vbr = args.vbr is not None or cfg.get("default_vbr") is not None
    use_opus = args.opus
    no_compress = args.no_compress or (send_mode == "file")
    obfuscate = args.obfuscate
    vbr_quality = args.vbr if args.vbr else r.get("default_vbr", "q3")
    
    print(f"\n{'='*50}")
    print(f"  ⬇️ 下载: {rj_id}")
    mode_label = {'voice': '🎤 语音 MP3', 'file': '📁 文件'}[send_mode]
    print(f"  模式: {mode_label}")
    if obfuscate:
        print(f"  混淆: 文件名自动 Hash")
    print(f"{'='*50}\n")

    # 去重检查：目录存在且含 manifest.json 或已收藏则跳过
    if work_dir.exists():
        mf = work_dir / "manifest.json"
        if mf.exists():
            try:
                with open(mf, encoding="utf-8") as _fm:
                    existing = json.load(_fm)
                print(f"  ⏭️ 作品已在 {work_dir} 下载过 ({existing.get('download_date','')})")
                print(f"     如需重新下载，请删除目录: rm -rf {work_dir}")
                return
            except:
                pass
    
    meta = get_work_meta(session, rj_id)
    if not meta:
        print("  [x] 获取作品信息失败")
        sys.exit(1)
    
    numeric_id = meta.get("numeric_id", rj_id.replace("RJ",""))
    print(f"  → 获取音轨列表...")
    tracks_raw = api_get(session, f"/api/tracks/{numeric_id}?v=2")
    if not tracks_raw or not isinstance(tracks_raw, list):
        print("  [x] 获取音轨失败")
        sys.exit(1)
    
    tracks = []
    def flatten(nodes):
        for node in nodes:
            if not isinstance(node, dict):
                continue
            if node.get("type") != "folder":
                url = (node.get("mediaDownloadUrl") or node.get("mediaUrl") or "").strip()
                if url:
                    ext = os.path.splitext(urlparse(url).path)[1].lower()
                    tracks.append({
                        "title": node.get("title", ""),
                        "url": url,
                        "ext": ext,
                    })
            flatten(node.get("children", []))
    flatten(tracks_raw)
    
    has_mp3 = any(t["ext"] == ".mp3" for t in tracks)
    if has_mp3 and not args.all_formats:
        non_mp3 = sum(1 for t in tracks if t["ext"] != ".mp3")
        tracks = [t for t in tracks if t["ext"] == ".mp3"]
        if non_mp3:
            print(f"  → 过滤掉 {non_mp3} 个非 MP3 格式，用 --all-formats 下载全部")
    
    print(f"  → 找到 {len(tracks)} 个音轨\n")
    if not tracks:
        print("  [x] 没有可下载的音轨")
        sys.exit(1)
    
    downloaded = []
    for i, track in enumerate(tracks, 1):
        clean_title = sanitize_filename(track["title"])
        while clean_title.lower().endswith('.mp3'):
            clean_title = clean_title[:-4]
        
        raw_name = f"{rj_id}_{i:03d}_{clean_title}{track['ext']}"
        raw_path = work_dir / "raw" / raw_name
        out_name = f"{rj_id}_{i:03d}_{clean_title}.mp3"
        out_path = work_dir / out_name
        
        if out_path.exists():
            print(f"  [{i}/{len(tracks)}] ✅ {clean_title[:40]} (已存在)")
            downloaded.append(out_path)
            continue
        
        print(f"  [{i}/{len(tracks)}] {clean_title[:40]}")
        
        if not raw_path.exists():
            print(f"    ↓ 下载中...")
            if not _download_file(session, track["url"], raw_path):
                print(f"    [x] 下载失败，跳过")
                continue
        else:
            print(f"    ⏭️ 原始文件已存在")
        
        raw_sz = raw_path.stat().st_size
        
        if no_compress:
            shutil.copy2(raw_path, out_path)
            print(f"    📦 不压缩，复制为 {out_name}")
        elif raw_sz <= QQ_AUDIO_MAX_BYTES:
            shutil.copy2(raw_path, out_path)
            print(f"    📦 无需压缩 ({fmt_size(raw_sz)} < 20MB)")
        elif use_opus:
            out_path = work_dir / f"{rj_id}_{i:03d}_{clean_title}.opus"
            _compress_opus(raw_path, out_path, r.get("default_bitrate", "96k"))
        else:
            _compress_vbr_mp3(raw_path, out_path, vbr_quality)
        
        # 降码率（仅在 voice 模式下）
        if out_path.exists() and out_path.stat().st_size > QQ_AUDIO_MAX_BYTES and send_mode == "voice":
            print(f"    ⚠️ {out_path.stat().st_size/1024**2:.1f}MB > 20MB")
            lower = work_dir / f"{rj_id}_{i:03d}_{clean_title}_64k.mp3"
            if _compress_cbr_mp3(raw_path, lower, "64k"):
                out_path = lower
                print(f"    ✅ 降码率: {out_path.stat().st_size/1024**2:.1f}MB")
        
        downloaded.append(out_path)
        print()
    
        # 混淆文件名（可选）
    name_map = {}
    if obfuscate and downloaded:
        print(f"\n  🔒 混淆文件名中...")
        obfuscated_list = []
        for f in downloaded:
            obf_name = _obfuscate_name(f.name)
            obf_path = f.parent / obf_name
            if f.exists():
                f.rename(obf_path)
                name_map[obf_name] = f.name
                obfuscated_list.append(obf_path)
                print(f"    {f.name} → {obf_name}")
        downloaded = obfuscated_list
        _make_map_file(work_dir, name_map)
    
    _print_download_summary(rj_id, meta, downloaded, work_dir, send_mode)
    
    if downloaded:
        meta["download_dir"] = str(work_dir)
        _save_collection(cfg, rj_id, meta, downloaded)


def _print_download_summary(rj_id, meta, downloaded, work_dir, send_mode=None):
    print(f"{'='*50}")
    print(f"  下载完成: {rj_id}")
    labels = {'voice': '🎤 语音 MP3', 'file': '📁 文件'}
    if send_mode:
        print(f"  发送方式: {labels.get(send_mode, send_mode)}")
    print(f"{'='*50}")
    
    if not downloaded:
        return
    
    total = sum(f.stat().st_size for f in downloaded)
    print(f"  文件: {len(downloaded)} 个 | 总计: {fmt_size(total)}")
    print(f"  目录: {work_dir.resolve()}")
    print()
    
    manifest = {
        "rj_id": rj_id,
        "title": meta["title"],
        "download_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "directory": str(work_dir.resolve()),
        "send_mode": send_mode or "voice",
        "obfuscated": bool(obfuscate) if 'obfuscate' in dir() else False,
        "files": [str(f.resolve()) for f in downloaded],
        "total_size_mb": round(total / 1024**2, 1),
    }
    with open(work_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print(f"  📋 发送列表:\n")
    for f in downloaded:
        sz = f.stat().st_size
        if send_mode == "file":
            print(f"  📁 {f.resolve()}  ({fmt_size(sz)})")
        else:
            ok = "✅" if sz <= QQ_AUDIO_MAX_BYTES else "⚠️"
            print(f"  {ok} <qqmedia>{f.resolve()}</qqmedia>  ({fmt_size(sz)})")
    print(f"\n  清单: {work_dir / 'manifest.json'}")


# =============================================
# 发送列表
# =============================================

def cmd_sendlist(args):
    rj_id = normalize_rj(args.rj_code)
    cfg = load_config()
    r = resolve_args(cfg, args, ["output_dir"])
    work_dir = Path(r["output_dir"]) / rj_id
    
    if not work_dir.exists():
        print(f"[x] 目录不存在: {work_dir}")
        sys.exit(1)
    
    # 从 manifest.json 读取发送模式
    send_mode = "voice"
    obfuscated = False
    mf = work_dir / "manifest.json"
    if mf.exists():
        try:
            with open(mf, encoding="utf-8") as f:
                mf_data = json.load(f)
                send_mode = mf_data.get("send_mode", "voice")
                obfuscated = mf_data.get("obfuscated", False)
        except:
            pass
    
    # 根据模式匹配文件
    patterns = {
        "file": f"{rj_id}_*.*",
        "voice": f"{rj_id}_*.mp3",
    }
    files = sorted(work_dir.glob(patterns.get(send_mode, f"{rj_id}_*.mp3")))
    if send_mode == "voice":
        files += sorted(work_dir.glob(f"{rj_id}_*.opus"))
    
    if not files:
        print(f"[x] 在 {work_dir} 中未找到匹配的音频文件")
        sys.exit(1)
    
    labels = {'voice': '🎤 语音 MP3', 'file': '📁 文件'}
    label = labels.get(send_mode, send_mode)
    if obfuscated:
        label += ' 🔒 已混淆'
    print(f"\n📋 {rj_id} - 发送列表 ({label}):\n")
    
    # 如果有混淆对照表，显示原名
    name_map = {}
    nmf = work_dir / "name_map.json"
    if nmf.exists():
        try:
            with open(nmf, encoding="utf-8") as f:
                name_map = json.load(f)
        except:
            pass
    
    for f in files:
        sz = f.stat().st_size
        display_name = name_map.get(f.name, f.name)
        dur = _get_duration(f)
        
        if send_mode == "file":
            print(f"  📁 {display_name}  ({fmt_size(sz)}, {dur:.0f}s)")
        else:
            ok = "✅" if sz <= 20*1024*1024 else "⚠️"
            print(f"  {ok} <qqmedia>{f.resolve()}</qqmedia>  ({fmt_size(sz)}, {dur:.0f}s)")
    
    print(f"\n  共 {len(files)} 个文件")
    if mf.exists():
        with open(mf, encoding="utf-8") as f:
            m = json.load(f)
        print(f"  作品: {m.get('title', '?')}")


# =============================================
# 收藏功能
# =============================================

def _save_collection(cfg, rj_id, meta, downloaded):
    """下载完成后保存到收藏记录"""
    total_mb = sum(f.stat().st_size for f in downloaded) / 1024**2
    entry = {
        "rj_id": rj_id,
        "title": meta["title"],
        "circle": meta["circle"],
        "cv": meta["cv"],
        "release_date": meta["release_date"],
        "download_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "file_count": len(downloaded),
        "total_size_mb": round(total_mb, 1),
        "directory": str(Path(meta["download_dir"])) if meta.get("download_dir") else str(Path(cfg.get("output_dir", str(DEFAULT_OUTPUT_DIR))) / rj_id),
    }
    _save_collection_entry(cfg, entry)


def cmd_collection(args):
    cfg = load_config()
    cf = get_collection_file(cfg)
    
    if not cf.exists():
        print("\n  📭 还没有收藏的作品")
        return
    
    with open(cf, encoding="utf-8") as f:
        collection = json.load(f)
    
    if not collection:
        print("\n  📭 收藏列表为空")
        return
    
    print(f"\n{'='*50}")
    print(f"  📚 收藏的作品 ({len(collection)} 个)")
    print(f"{'='*50}\n")
    
    for i, c in enumerate(collection, 1):
        print(f"  [{i}] {c['rj_id']} — {c['title'][:50]}")
        if args.detail:
            print(f"      社团: {c.get('circle','?')}")
            print(f"      CV: {c.get('cv','?')}")
            print(f"      发布: {c.get('release_date','?')}")
            print(f"      下载: {c.get('download_date','?')}")
        print(f"      文件: {c.get('file_count',0)} 个 | {c.get('total_size_mb',0)}MB")
        print()
    
    print(f"  📁 收藏文件: {cf}")


def cmd_import(args):
    """从本地目录导入已下载的音频文件"""
    rj_id = normalize_rj(args.rj_code)
    src_dir = Path(args.dir)
    cfg = load_config()
    base_dir = Path(cfg.get("output_dir", str(DEFAULT_OUTPUT_DIR)))
    work_dir = base_dir / rj_id

    if not src_dir.is_dir():
        print(f"[x] 目录不存在: {src_dir}")
        return

    audio_exts = {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".opus"}
    files = sorted([f for f in src_dir.iterdir() if f.suffix.lower() in audio_exts])
    if not files:
        print(f"[x] 目录中没有找到音频文件: {src_dir}")
        print(f"   支持的格式: {', '.join(sorted(audio_exts))}")
        return

    print(f"\n{'='*50}")
    print(f"  📂 导入: {rj_id} ← {src_dir}")
    print(f"{'='*50}")

    work_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = work_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    downloaded = []
    for i, f in enumerate(files, 1):
        clean_title = sanitize_filename(f.stem)
        raw_name = f"{rj_id}_{i:03d}_{clean_title}{f.suffix}"
        out_name = f"{rj_id}_{i:03d}_{clean_title}.mp3"

        raw_path = raw_dir / raw_name
        out_path = work_dir / out_name

        shutil.copy2(f, raw_path)
        print(f"  [{i}/{len(files)}] ✅ {raw_name} ({fmt_size(f.stat().st_size)})")

        # 如果文件超过 20MB 且不是 mp3，压缩
        if f.stat().st_size > QQ_AUDIO_MAX_BYTES and f.suffix.lower() != ".mp3":
            _compress_cbr_mp3(raw_path, out_path, "64k")
            print(f"    ⚡ 超过 20MB，已压缩至 64k")
        else:
            if f.suffix.lower() != ".mp3":
                _compress_cbr_mp3(raw_path, out_path, "128k")
            else:
                shutil.copy2(f, out_path)

        if out_path.exists():
            downloaded.append(out_name)

    if not downloaded:
        print("\n  [x] 导入失败，没有文件被处理")
        return

    # 创建 manifest
    meta = {
        "rj_code": rj_id,
        "download_dir": str(work_dir),
    }
    manifest = {
        "rj_id": rj_id,
        "title": args.title or rj_id,
        "circle": args.name or "",
        "cv": args.cv or "",
        "download_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "files": downloaded,
        "source_dir": str(src_dir),
    }

    with open(work_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # 加入收藏
    total_sz = sum(f.stat().st_size for f in files)
    entry = {
        "rj_id": rj_id,
        "title": args.title or rj_id,
        "circle": args.name or "",
        "cv": args.cv or "",
        "release_date": "",
        "download_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "file_count": len(downloaded),
        "total_size_mb": round(total_sz / 1024 / 1024, 1),
        "directory": str(work_dir),
    }
    _save_collection_entry(cfg, entry)

    print(f"\n{'='*50}")
    print(f"  ✅ 导入完成: {rj_id}")
    print(f"  文件: {len(downloaded)} 个 | 合计: {fmt_size(total_sz)}")
    print(f"  目录: {work_dir}")


def _save_collection_entry(cfg: dict, entry: dict):
    """往收藏列表头部插入一条记录并保存"""
    cf = get_collection_file(cfg)
    collection = []
    if cf.exists():
        try:
            with open(cf, encoding="utf-8") as f:
                collection = json.load(f)
        except:
            pass

    # 去重
    collection = [c for c in collection if c.get("rj_id") != entry["rj_id"]]
    collection.insert(0, entry)

    cf.parent.mkdir(parents=True, exist_ok=True)
    with open(cf, "w", encoding="utf-8") as f:
        json.dump(collection, f, ensure_ascii=False, indent=2)
    print(f"  📌 已添加到收藏")


# =============================================
# 文件操作
# =============================================

def _download_file(session, url, dest) -> bool:
    try:
        session.allow_redirects = True
        resp = session.get(url, timeout=300, stream=True)
        session.allow_redirects = False
        if resp.status_code != 200:
            print(f"    [!] HTTP {resp.status_code}")
            return False
        
        total = int(resp.headers.get("content-length", 0))
        downloaded = 0
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total > 0:
                        pct = downloaded * 100 // total
                        sys.stdout.write(f"\r    {fmt_size(downloaded)} / {fmt_size(total)} ({pct}%)")
                        sys.stdout.flush()
        print()
        print(f"    ✅ {fmt_size(dest.stat().st_size)}")
        return True
    except Exception as e:
        print(f"\n    [x] 下载异常: {e}")
        return False


def _compress_cbr_mp3(in_path, out_path, bitrate):
    try:
        cmd = ["ffmpeg","-y","-i",str(in_path),"-c:a","libmp3lame",
               "-b:a",bitrate,"-ar","44100","-ac","2","-map_metadata","0",str(out_path)]
        r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=600)
        if r.returncode == 0 and out_path.exists():
            in_sz = in_path.stat().st_size
            out_sz = out_path.stat().st_size
            ratio = (1 - out_sz/in_sz) * 100 if in_sz else 0
            print(f"    💾 {fmt_size(in_sz)} → {fmt_size(out_sz)} (-{ratio:.0f}%) @ CBR {bitrate}")
            return True
        return False
    except:
        return False


def _compress_vbr_mp3(in_path, out_path, quality="q3"):
    vbr_val = quality.replace("q","")
    target = VBR_BITRATE.get(quality, "175k")
    try:
        cmd = ["ffmpeg","-y","-i",str(in_path),"-c:a","libmp3lame",
               "-q:a",vbr_val,"-ar","44100","-ac","2","-map_metadata","0",str(out_path)]
        r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=600)
        if r.returncode == 0 and out_path.exists():
            in_sz = in_path.stat().st_size
            out_sz = out_path.stat().st_size
            ratio = (1 - out_sz/in_sz) * 100 if in_sz else 0
            print(f"    💾 {fmt_size(in_sz)} → {fmt_size(out_sz)} (-{ratio:.0f}%) @ VBR q{vbr_val}(~{target})")
            return True
        return False
    except:
        return False


def _compress_opus(in_path, out_path, bitrate="96k"):
    try:
        cmd = ["ffmpeg","-y","-i",str(in_path),"-c:a","libopus",
               "-b:a",bitrate,"-vbr","on","-compression_level","10",
               "-ar","48000","-ac","2","-map_metadata","0",str(out_path)]
        r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=600)
        if r.returncode == 0 and out_path.exists():
            in_sz = in_path.stat().st_size
            out_sz = out_path.stat().st_size
            ratio = (1 - out_sz/in_sz) * 100 if in_sz else 0
            print(f"    💾 {fmt_size(in_sz)} → {fmt_size(out_sz)} (-{ratio:.0f}%) @ OPUS {bitrate}")
            return True
        return False
    except:
        return False


def _get_duration(file_path) -> float:
    try:
        r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                           "-of","default=noprint_wrappers=1:nokey=1",str(file_path)],
                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=30)
        return float(r.stdout.decode().strip())
    except:
        return 0


def _obfuscate_name(name: str) -> str:
    """根据文件名生成混淆 Hash"""
    raw = name.encode("utf-8")
    h = hashlib.sha256(raw).hexdigest()[:12]
    ext = Path(name).suffix
    return f"Audio_Cache_{h}{ext}"


def _make_map_file(work_dir: Path, mapping: dict):
    """写入混淆对照表"""
    mf = work_dir / "name_map.json"
    with open(mf, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    return mf


# =============================================
# 主入口
# =============================================

def main():
    parser = argparse.ArgumentParser(
        description="ASMR.one 搜索/下载/压缩工具 v4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
快速入门:
  1. asmr_tool.py config init              # 初始化配置
  2. asmr_tool.py check                    # 验证环境
  3. asmr_tool.py search "关键词"          # 搜索作品
  4. asmr_tool.py download RJxxxxxx        # 下载

配置优先级: CLI 参数 > 环境变量 > 配置文件(~/.config/asmr-tool/config.json)

环境变量:
  ASMR_PROXY        代理地址 (如 http://127.0.0.1:7890)
  ASMR_OUTPUT_DIR   下载目录
  ASMR_VBR          默认 VBR 质量 (q0~q9)
  QQ_TARGET         QQ Bot 发送目标
""")
    
    sub = parser.add_subparsers(dest="command", title="命令")
    
    # search
    p = sub.add_parser("search", help="搜索作品（多关键词AND，仅最新作品）")
    p.add_argument("keyword")
    p.add_argument("--proxy", "-p")
    
    # hot
    p = sub.add_parser("hot", help="热门推荐")
    p.add_argument("--proxy", "-p")
    
    # info
    p = sub.add_parser("info", help="作品详情")
    p.add_argument("rj_code")
    p.add_argument("--proxy", "-p")
    
    # download
    p = sub.add_parser("download", help="下载并压缩")
    p.add_argument("rj_code")
    p.add_argument("--proxy", "-p")
    p.add_argument("--vbr", default=None,
                   choices=["q0","q1","q2","q3","q4","q5","q6","q7","q8","q9"])
    p.add_argument("--opus", action="store_true")
    p.add_argument("--no-compress", action="store_true")
    p.add_argument("--all-formats", action="store_true")
    p.add_argument("--mode", choices=["voice","file"], default="voice",
                   help="voice: 压缩至 QQ 语音兼容 MP3（默认）| file: 不压缩")
    p.add_argument("--obfuscate", action="store_true",
                   help="混淆文件名，防和谐（生成随机 Hash 命名 + 对照表）")

    # sendlist
    p = sub.add_parser("sendlist", help="列出已下载文件")
    p.add_argument("rj_code")

    # collection
    p = sub.add_parser("collection", help="查看收藏列表")
    p.add_argument("--detail", "-d", action="store_true")
    
    # import local
    p = sub.add_parser("import", help="从本地目录导入已下载的音频文件")
    p.add_argument("rj_code", help="RJ 编号")
    p.add_argument("dir", help="音频文件所在目录路径")
    p.add_argument("--title", help="作品标题（可选，自动从文件名推测）")
    p.add_argument("--name", help="社团名称")
    p.add_argument("--cv", help="CV 名称")

    # check
    p = sub.add_parser("check", help="检查运行环境")
    
    # config
    p = sub.add_parser("config", help="配置文件管理")
    p.add_argument("action", choices=["init", "show", "set", "get"],
                   help="init:交互配置 | show:查看 | set key value:设置值 | get key:读取值")
    p.add_argument("key", nargs="?", help="配置项名称")
    p.add_argument("value", nargs="?", help="配置项值")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # config 和 check 不需要 Proxy 解析（skip resolve_args）
    if args.command in ("config", "check"):
        route = {
            "config": cmd_config,
            "check": cmd_check,
        }
        route[args.command](args)
        return
    
    # 其他命令: 环境变量优先级次于 CLI 但高于配置文件
    # resolve_args 会在各个 cmd 函数中调用
    
    route = {
        "search": cmd_search,
        "hot": cmd_hot,
        "info": cmd_info,
        "download": cmd_download,
        "sendlist": cmd_sendlist,
        "collection": cmd_collection,
        "import": cmd_import,
    }
    fn = route.get(args.command)
    if fn:
        fn(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
