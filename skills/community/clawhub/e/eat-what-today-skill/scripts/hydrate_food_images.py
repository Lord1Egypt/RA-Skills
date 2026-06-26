import argparse
import json
import re
import subprocess
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
MENU_FILE = BASE / "assets" / "menu_db.json"
TARGET_DIR = BASE / "assets" / "foods_image"

EXTS = ("jpg", "jpeg", "png", "webp")
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)


def has_local_image(name: str) -> bool:
    return any((TARGET_DIR / f"{name}.{ext}").exists() for ext in EXTS)


def fetch_url_bytes(url: str, timeout: float = 12.0) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def search_bing_image_url(query: str) -> str:
    encoded = urllib.parse.quote(query)
    search_url = f"https://www.bing.com/images/search?q={encoded}&form=HDRSC2"
    html = fetch_url_bytes(search_url, timeout=12.0).decode("utf-8", errors="ignore")

    patterns = [
        r'"murl":"(https?://[^"\\]+)"',
        r"murl&amp;quot;:&amp;quot;(https?://[^&]+)&amp;quot;",
        r'src="(https?://[^"]+)"',
    ]
    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            url = match.group(1)
            return bytes(url, "utf-8").decode("unicode_escape")
    return ""


def download_image(url: str, out_path: Path, timeout: float = 15.0) -> bool:
    try:
        data = fetch_url_bytes(url, timeout=timeout)
        if len(data) < 1024:
            return False
        out_path.write_bytes(data)
        return True
    except Exception:
        return False


def pollinations_generate(
    name: str,
    out_path: Path,
    model: str = "flux",
    width: int = 768,
    height: int = 512,
    timeout: float = 25.0,
) -> bool:
    prompt = f"{name} 菜品实拍, Chinese food photography, realistic, plated dish"
    encoded_prompt = urllib.parse.quote(prompt)
    url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width={width}&height={height}&model={model}&nologo=true"
    )
    return download_image(url, out_path, timeout=timeout)


def external_ai_generate(name: str, out_path: Path, external_ai_cmd: str, timeout: float = 60.0) -> bool:
    if not external_ai_cmd.strip():
        return False

    cmd = (
        external_ai_cmd
        .replace("{name}", name)
        .replace("{out_path}", str(out_path))
    )
    try:
        result = subprocess.run(cmd, shell=True, check=False, timeout=timeout)
    except Exception:
        return False

    if result.returncode != 0:
        return False

    return out_path.exists() and out_path.stat().st_size >= 1024


def hydrate(
    limit: int,
    delay: float,
    dry_run: bool,
    external_ai_cmd: str,
    use_pollinations: bool,
    pollinations_model: str,
):
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    items = json.loads(MENU_FILE.read_text(encoding="utf-8"))
    missing = [item["name"] for item in items if not has_local_image(item["name"])]

    if limit > 0:
        missing = missing[:limit]

    stats = {
        "total_missing": len(missing),
        "downloaded": 0,
        "generated_by_pollinations": 0,
        "generated_by_external_ai": 0,
        "failed": 0,
        "ai_unavailable": 0,
    }

    for idx, name in enumerate(missing, start=1):
        out_path = TARGET_DIR / f"{name}.jpg"
        print(f"[{idx}/{len(missing)}] {name}")
        if dry_run:
            continue

        search_query = f"{name} 美食 实拍"
        ok = False
        try:
            img_url = search_bing_image_url(search_query)
            if img_url:
                ok = download_image(img_url, out_path)
                if ok:
                    stats["downloaded"] += 1
        except Exception:
            ok = False

        if not ok and use_pollinations:
            ok = pollinations_generate(name, out_path, model=pollinations_model)
            if ok:
                stats["generated_by_pollinations"] += 1

        if not ok and external_ai_cmd.strip():
            ok = external_ai_generate(name, out_path, external_ai_cmd)
            if ok:
                stats["generated_by_external_ai"] += 1

        if not ok and not external_ai_cmd.strip():
            stats["ai_unavailable"] += 1
            print("  - 无可用外部 AI 生图命令，建议配置你自己的 AI 生图技能作为最终兜底")

        if not ok:
            stats["failed"] += 1

        if delay > 0:
            time.sleep(delay)

    print("---")
    print("total_missing:", stats["total_missing"])
    print("downloaded:", stats["downloaded"])
    print("generated_by_pollinations:", stats["generated_by_pollinations"])
    print("generated_by_external_ai:", stats["generated_by_external_ai"])
    print("ai_unavailable:", stats["ai_unavailable"])
    print("failed:", stats["failed"])


def main():
    parser = argparse.ArgumentParser(description="为缺少图片的菜品自动补图：联网搜图优先，外部AI技能可选兜底")
    parser.add_argument("--limit", type=int, default=0, help="最多处理多少个缺图菜品，0 表示全部")
    parser.add_argument("--delay", type=float, default=0.3, help="每个菜品处理后的延迟秒数")
    parser.add_argument("--dry-run", action="store_true", help="仅展示待处理条目，不实际下载")
    parser.add_argument(
        "--external-ai-cmd",
        default="",
        help="可选：调用用户已有AI生图能力的命令模板，支持占位符 {name} 和 {out_path}",
    )
    parser.add_argument(
        "--no-pollinations",
        action="store_true",
        help="禁用 Pollinations 公共接口兜底（默认启用）",
    )
    parser.add_argument(
        "--pollinations-model",
        default="flux",
        help="Pollinations 模型名，默认 flux",
    )
    args = parser.parse_args()

    hydrate(
        limit=args.limit,
        delay=args.delay,
        dry_run=args.dry_run,
        external_ai_cmd=args.external_ai_cmd,
        use_pollinations=not args.no_pollinations,
        pollinations_model=args.pollinations_model,
    )


if __name__ == "__main__":
    main()
