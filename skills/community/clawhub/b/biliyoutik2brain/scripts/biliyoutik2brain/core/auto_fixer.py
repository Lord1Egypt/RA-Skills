"""
auto_fixer.py — 流水线自修复引擎

读 ERROR_PATTERNS.json，匹配错误 → 自动修复 → 验证
"""
import subprocess, sys, os, json

from .paths import storage_path
ERROR_DB = storage_path("biliyoutik2brain_evolution", "ERROR_PATTERNS.json")

def load_error_db():
    with open(ERROR_DB) as f:
        return json.load(f)

def fix_yt_dlp_upgrade():
    """E001: 升级 yt-dlp"""
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], check=False)
    result = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True)
    return f"yt-dlp {result.stdout.strip()}"

def fix_set_pythonpath():
    """E004: 设置 PYTHONPATH"""
    scripts_dir = os.path.expanduser("~/.openclaw/skills/biliyoutik2brain/scripts")
    result = subprocess.run(
        [sys.executable, "-c", "from biliyoutik2brain.core.enhance_engine import enhance_and_analyze"],
        env={"PYTHONPATH": scripts_dir, "PATH": os.environ["PATH"]},
        capture_output=True, text=True
    )
    return result.returncode == 0

def fix_use_gateway_api():
    """E005: 切到 Gateway 内部 API — 从环境变量读取 Key，不硬编码"""
    import urllib.request
    gw_key = os.environ.get("GATEWAY_API_KEY", "")
    if not gw_key:
        return False  # 无 Key 不探测
    req = urllib.request.Request(
        "http://127.0.0.1:18789/v1/models",
        headers={"Authorization": f"Bearer {gw_key}"}
    )
    try:
        urllib.request.urlopen(req, timeout=5)
        return True
    except Exception:
        return False

def preflight(platform: str, url: str) -> dict:
    """P1下载前预检 — 四平台差异化检查
    
    B站: API 412状态 + BV号完整性
    抖音: Session 指纹 + 域名可达
    小红书: yt-dlp 版本 >= 2026.6.9
    YouTube: 代理连通性
    通用: 磁盘空间
    """
    warnings = []
    errors = []
    
    import urllib.request
    from .anti_crawl_middleware import _create_insecure_ssl_context
    
    # ── yt-dlp 版本（小红书特检） ──
    r = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True)
    if r.returncode != 0:
        errors.append("yt-dlp 未安装")
    else:
        version = r.stdout.strip()
        if platform == "xiaohongshu":
            # 语义版本比较（2026.06.09 应对齐 2026.6.9）
            try:
                parts = [int(p) for p in version.split(".")[:3]]
            except ValueError:
                parts = [0, 0, 0]
            if parts < [2026, 6, 9]:
                errors.append(f"yt-dlp {version} 不兼容小红书，需 ≥2026.6.9")
    
    # ── B站反爬预检 ──
    if platform == "bilibili":
        import re
        m = re.search(r'(BV[\w]+)', url)
        if m:
            api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={m.group(1)}"
            req = urllib.request.Request(api_url, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
                "Referer": "https://www.bilibili.com/",
            })
            try:
                resp = urllib.request.urlopen(req, timeout=10)
                if resp.status == 412:
                    errors.append("B站API 412反爬拦截")
            except urllib.request.HTTPError as e:
                if e.code == 412:
                    errors.append("B站API 412反爬拦截")
                else:
                    warnings.append(f"B站API HTTP {e.code}")
            except Exception as e:
                warnings.append(f"B站API连接异常: {e}")
        else:
            errors.append("B站URL缺少BV号")
    
    # ── 抖音域名可达 ──
    if platform == "douyin":
        ctx = _create_insecure_ssl_context()
        try:
            req = urllib.request.Request("https://www.douyin.com/", headers={
                "User-Agent": "Mozilla/5.0"
            })
            resp = urllib.request.urlopen(req, timeout=10, context=ctx)
            if resp.status != 200:
                warnings.append(f"抖音主页HTTP {resp.status}")
        except Exception as e:
            warnings.append(f"抖音域名检测失败: {e}")
    
    # ── YouTube 代理连通性 ──
    if platform == "youtube":
        ctx = _create_insecure_ssl_context()
        try:
            opener = urllib.request.build_opener(
                urllib.request.ProxyHandler({
                    "http": "http://127.0.0.1:9981",
                    "https": "http://127.0.0.1:9981"
                }),
                urllib.request.HTTPSHandler(context=ctx)
            )
            req = urllib.request.Request("https://www.google.com", method="HEAD")
            resp = opener.open(req, timeout=5)
            if resp.status not in (200, 301, 302):
                errors.append(f"代理连通但Google返回{resp.status}")
        except Exception as e:
            errors.append(f"YouTube代理不通: {str(e)[:60]}")
    
    # ── 磁盘空间 ──
    stat = os.statvfs(os.path.expanduser("~"))
    free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
    if free_gb < 0.5:
        errors.append(f"磁盘空间不足: {free_gb:.1f}GB")
    
    return {"ok": len(errors) == 0, "warnings": warnings, "errors": errors}


def noise_precheck(wav_path: str) -> dict:
    """P2噪声预检"""
    try:
        import numpy as np
        import wave
        wf = wave.open(wav_path, 'r')
        frames = wf.readframes(wf.getnframes())
        wf.close()
        samples = np.frombuffer(frames, dtype=np.int16).astype(np.float32)
        rms = np.sqrt(np.mean(samples**2))
        db = 20 * np.log10(rms / 32768) if rms > 0 else -96
        
        if db > -30:
            level = "high"; estimated_rft = 2.0; warning = "高噪声，预计转录时间翻倍"
        elif db > -40:
            level = "normal"; estimated_rft = 1.0; warning = None
        else:
            level = "low"; estimated_rft = 0.8; warning = None
        
        return {"level": level, "db": round(db, 1), "estimated_rft": estimated_rft, "warning": warning}
    except Exception as e:
        return {"level": "unknown", "error": str(e)}


def quality_check(text: str) -> dict:
    """P4输出质量检查"""
    import re
    total = len(text)
    punct = len(re.findall(r'[，。、！？""；：（）…—\n]', text))
    punct_density = punct / max(total, 1)
    paragraphs = text.count('\n\n') + 1
    # 繁体字检测 (CJK统一汉字中繁简差异区间)
    traditional = len(re.findall(r'[爲時來見裡後麼麵體]', text))
    trad_ratio = traditional / max(total, 1)
    
    checks = {
        "punctuation_density": round(punct_density * 100, 1),
        "paragraph_count": paragraphs,
        "traditional_ratio": round(trad_ratio * 100, 1),
    }
    passed = punct_density >= 0.05 and paragraphs >= 3 and trad_ratio < 0.02
    return {"passed": passed, "checks": checks}


if __name__ == "__main__":
    print("auto_fixer.py 已就绪")
    print(f"  修复方法: {[k for k in dir() if k.startswith('fix_')]}")
    print(f"  预检函数: preflight, noise_precheck, quality_check")
