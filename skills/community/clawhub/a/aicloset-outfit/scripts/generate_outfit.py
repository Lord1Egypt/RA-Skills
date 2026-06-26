#!/usr/bin/env python3
"""AI 衣橱搭配推荐 - 调用 API、下载图片、合成画布、输出 MEDIA 标记"""
import os, sys, json, time, tempfile, platform, subprocess, shutil
from urllib import request, error
from pathlib import Path

# ===== 配置 =====
API_KEY = os.environ.get("AICLOSET_API_KEY", "")
if not API_KEY:
    cfg_path = Path.home() / ".openclaw" / "openclaw.json"
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        API_KEY = cfg.get("skills", {}).get("entries", {}).get("aicloset-outfit", {}).get("apiKey", "")
    except Exception:
        pass
if not API_KEY:
    print("❌ API Key 未配置，请先设置 AICLOSET_API_KEY")
    sys.exit(1)

API_URL = "https://aicloset-dev-h5.wxbjq.top/algorithm/open/system_outfit/create_task"
OUTDIR = Path(tempfile.gettempdir()) / f"aicloset_outfit_{int(time.time())}"
OUTDIR.mkdir(parents=True, exist_ok=True)
CANVAS_H = 800

# ===== 读取命令行参数 =====
args = {}
for arg in sys.argv[1:]:
    if "=" in arg:
        k, v = arg.split("=", 1)
        args[k.lstrip("-")] = v

params = {
    "date": args.get("date", time.strftime("%Y-%m-%d")),
    "city_name": args.get("city", "杭州"),
    "province_name": args.get("province", "浙江"),
    "style_text": args.get("style", "休闲")
}

# ===== 检查 ImageMagick =====
if not shutil.which("magick"):
    print("❌ 未检测到 ImageMagick，请先安装:")
    print("   macOS:   brew install imagemagick")
    print("   Windows: choco install imagemagick")
    print("   Linux:   apt install imagemagick")
    sys.exit(1)

# ===== 调用 API =====
print("📡 正在调用 AI 搭配引擎...")
req = request.Request(
    API_URL,
    data=json.dumps(params).encode("utf-8"),
    headers={"Content-Type": "application/json", "x-api-key": API_KEY},
    method="POST"
)
result = None
for attempt in range(2):
    try:
        with request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        break
    except Exception as e:
        if attempt == 0:
            print("⏳ 请求超时，正在重试...")
        else:
            print(f"❌ 网络请求失败: {e}")
            sys.exit(1)

if result.get("code") != 0:
    print(f"❌ API 错误: {result.get('msg', '未知错误')}")
    sys.exit(1)

outfits = result["data"]["system_outfit_json"]
print(f"✅ 搭配方案已生成，共 {len(outfits)} 套，正在合成图片...")

# ===== 辅助函数 =====
def download(url, dest):
    try:
        request.urlretrieve(url, str(dest))
        return True
    except Exception:
        return False

def magick(*args):
    subprocess.run(["magick"] + list(args), check=True, capture_output=True)

# ===== 合成每套搭配 =====
outfit_desc = []
for i, outfit in enumerate(outfits):
    ar = outfit.get("canvas_content", {}).get("aspect_ratio", 0.731)
    cw = int(CANVAS_H * ar)
    out_path = OUTDIR / f"outfit_{i+1}.png"

    magick("-size", f"{cw}x{CANVAS_H}", "xc:#FFFFFF", str(out_path))

    products = sorted(outfit.get("product_list", []), key=lambda p: p.get("z_index", 0))
    names = []
    for p in products:
        names.append(p.get("class_name", "单品"))
        img_url = p.get("cutout_image", "")
        if not img_url:
            continue
        item_path = OUTDIR / "item_tmp.png"
        if not download(img_url, item_path):
            continue
        sw = p.get("size", {}).get("width", 0.3)
        sh = p.get("size", {}).get("height", 0.3)
        cx = p.get("center", {}).get("x", 0.5)
        cy = p.get("center", {}).get("y", 0.5)
        iw = int(cw * sw)
        ih = int(CANVAS_H * sh)
        ox = int(cw * cx - iw / 2)
        oy = int(CANVAS_H * cy - ih / 2)

        magick(
            str(out_path),
            "(", str(item_path), "-resize", f"{iw}x{ih}!", ")",
            "-geometry", f"+{ox}+{oy}", "-composite",
            str(out_path)
        )

    magick(
        str(out_path),
        "-bordercolor", "#E0E0E0", "-border", "2",
        "-bordercolor", "#F5F5F5", "-border", "15",
        "-gravity", "North", "-pointsize", "28", "-fill", "#333333",
        "-annotate", "+0+5", f"Look {i+1}",
        str(out_path)
    )

    outfit_desc.append(" + ".join(names))
    print(f"🎨 搭配 {i+1}/{len(outfits)} 合成完成")

# ===== 拼接总览图 =====
parts = [str(OUTDIR / f"outfit_{i+1}.png") for i in range(len(outfits))]
overview_path = OUTDIR / "all_outfits.png"
magick(*parts, "+append", str(overview_path))

# ===== 输出结果 =====
print(f"\n🖼️ 图片合成完毕\n")
print(f"👗 AI 搭配推荐 | {params['city_name']} · {params['date']} · {params['style_text']}风\n")
for i, desc in enumerate(outfit_desc):
    print(f"━━━ 搭配 {i+1} ━━━  单品：{desc}")
print(f"\n📂 图片保存在: {OUTDIR}")

# ===== 输出 MEDIA 标记（IM 渠道自动发送图片） =====
print(f"\nMEDIA:{overview_path}")

# ===== 跨平台打开图片 =====
system = platform.system()
if system == "Darwin":
    subprocess.run(["open", str(overview_path)])
elif system == "Windows":
    os.startfile(str(overview_path))
elif system == "Linux":
    subprocess.run(["xdg-open", str(overview_path)])
