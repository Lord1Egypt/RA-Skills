"""
main.py — Orchestrator: Analyze + Publish Pipeline
───────────────────────────────────────────────────
Two modes:

  ANALYZE (scrape + generate content — batch supported):
    python main.py https://dantri.com.vn/...
    python main.py url1 url2 url3 --save
    python main.py -f urls.txt --save

  PUBLISH (full pipeline → Facebook):
    python main.py --url "https://dantri.com.vn/..." 
    python main.py --url "https://..." --no-image --dry-run
    python main.py --url "https://..." --schedule 1735689600
    python main.py --test-post
"""

import argparse
import json
import sys
import time
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

import config
from models import ScrapedContent, GeneratedContent
from utils import logger

console = Console()


def print_banner():
    console.print(Panel.fit(
        "[bold cyan]🤖 AI Content Pipeline[/bold cyan]\n"
        "[dim]Hybrid Scraper · Gemini · DALL-E 3 · Facebook Graph API[/dim]",
        border_style="cyan",
        padding=(1, 4),
    ))


# ═══════════════════════════════════════════════════════════
# ANALYZE MODE — scrape + generate content (batch supported)
# ═══════════════════════════════════════════════════════════

def analyze_single(url: str, save: bool = False) -> None:
    """Scrape a single URL and generate content."""
    from agents.crawler_agent import CrawlerAgent
    from agents.writer_agent import WriterAgent

    print(f"\n🔍 Scraping: {url}\n")
    crawler = CrawlerAgent()
    scraped = crawler.crawl(url)
    print(scraped.summary())
    print()

    if not scraped.is_accessible:
        print("⚠️  Cannot generate content — source is inaccessible.")
        return

    print("🤖 Generating content with AI...\n")
    writer = WriterAgent()
    content = writer.write(scraped)

    if content:
        print(content.formatted_output())
        if save:
            _save_analyze_result(url, scraped, content)
    else:
        print("❌ Content generation failed.")


def analyze_batch(urls: list[str], save: bool = False) -> None:
    """Scrape multiple URLs and generate content for each."""
    from agents.crawler_agent import CrawlerAgent
    from agents.writer_agent import WriterAgent

    print(f"\n📋 Processing {len(urls)} URLs...\n")

    crawler = CrawlerAgent()
    scraped_list = crawler.crawl_multiple(urls)
    accessible = [s for s in scraped_list if s.is_accessible]

    if not accessible:
        print("⚠️  No accessible content found. Check URLs and try again.")
        return

    print(f"\n🤖 Generating content for {len(accessible)} accessible sources...\n")
    writer = WriterAgent()
    generated = writer.write_multiple(accessible)

    print(f"\n✅ Done! Generated {len(generated)}/{len(urls)} posts.")

    if save and generated:
        for scraped, content in zip(accessible, generated):
            _save_analyze_result(scraped.url, scraped, content)


def analyze_from_file(filepath: str, save: bool = False) -> None:
    """Read URLs from a file (one per line) and process them."""
    path = Path(filepath)
    if not path.exists():
        print(f"❌ File not found: {filepath}")
        sys.exit(1)

    urls = [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    if not urls:
        print("❌ No URLs found in file.")
        sys.exit(1)

    analyze_batch(urls, save=save)


def _save_analyze_result(url: str, scraped: ScrapedContent, content: GeneratedContent) -> None:
    """Save analyze results to JSON file in output/ directory."""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = url.split("//")[-1].replace("/", "_").replace("?", "_")[:50]
    filename = output_dir / f"{timestamp}_{safe_name}.json"

    data = {
        "scraped": {
            "url": scraped.url,
            "title": scraped.title,
            "description": scraped.description,
            "author": scraped.author,
            "published_date": scraped.published_date,
            "source_name": scraped.source_name,
            "text_length": len(scraped.text) if scraped.text else 0,
            "scraped_at": scraped.scraped_at,
        },
        "generated": {
            "title": content.title,
            "caption": content.caption,
            "hashtags": content.hashtags,
            "image_prompt": content.image_prompt,
            "generated_at": content.generated_at,
        },
    }

    filename.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"💾 Saved to: {filename}")


# ═══════════════════════════════════════════════════════════
# PUBLISH MODE — full pipeline → Facebook
# ═══════════════════════════════════════════════════════════

def run_pipeline(
    source_url: str,
    use_image: bool = True,
    schedule_ts: int | None = None,
    dry_run: bool = False,
) -> dict:
    """
    Full pipeline:
    URL → Crawl → Write → Image → Post FB Fanpage

    """
    config.validate(mode="publish")
    print_banner()

    results = {}

    # ──────────────────────────────────────────────────────────
    # STEP 1: Crawl
    # ──────────────────────────────────────────────────────────
    console.print(Rule("[bold]STEP 1: CRAWL[/bold]", style="cyan"))
    from agents.crawler_agent import CrawlerAgent
    crawler = CrawlerAgent()
    scraped = crawler.crawl(source_url)

    if not scraped.is_accessible:
        console.print(f"[bold red]❌ Cannot access: {source_url}[/bold red]")
        console.print(f"[red]{scraped.error_message}[/red]")
        return {"error": scraped.error_message}

    results["crawl"] = {
        "title": scraped.title,
        "text_length": len(scraped.text) if scraped.text else 0,
        "url": scraped.url,
        "source_name": scraped.source_name,
    }
    console.print(f"[green]Content crawled:[/green] {len(scraped.text or '')} chars")

    # ──────────────────────────────────────────────────────────
    # STEP 2: Write
    # ──────────────────────────────────────────────────────────
    console.print(Rule("[bold]STEP 2: AI WRITE[/bold]", style="yellow"))
    from agents.writer_agent import WriterAgent
    writer = WriterAgent()
    written = writer.write(scraped)

    if not written:
        console.print("[bold red]❌ Content generation failed.[/bold red]")
        return {"error": "Content generation failed"}

    results["written"] = {
        "title": written.title,
        "caption": written.caption,
        "hashtags": written.hashtags,
        "image_prompt": written.image_prompt,
    }

    console.print("\n[bold]📝 Preview bài post:[/bold]")
    console.print(Panel(written.caption[:600], border_style="dim"))

    # ──────────────────────────────────────────────────────────
    # STEP 3: Image (optional)
    # ──────────────────────────────────────────────────────────
    image_local_path = None
    image_url = None

    if use_image and written.image_prompt:
        console.print(Rule("[bold]STEP 3: GENERATE IMAGE[/bold]", style="magenta"))
        from agents.image_agent import ImageAgent
        image_agent = ImageAgent()
        safe_name = "".join(
            c if c.isalnum() else "_" for c in (scraped.title or "post")[:30]
        )
        image_local_path, image_url = image_agent.generate(
            prompt=written.image_prompt,
            filename=safe_name,
        )
        results["image_local"] = image_local_path
        results["image_url"] = image_url
    else:
        console.print(Rule("[bold]STEP 3: SKIP IMAGE[/bold]", style="dim"))

    # ──────────────────────────────────────────────────────────
    # STEP 4: Post to FB
    # ──────────────────────────────────────────────────────────
    console.print(Rule("[bold]STEP 4: POST TO FACEBOOK[/bold]", style="green"))

    if dry_run:
        console.print("[bold yellow]⚠️  DRY RUN — không đăng thật![/bold yellow]")
        console.print("[dim]--dry-run mode: bỏ flag này để đăng thật[/dim]")
        results["post"] = {"dry_run": True}
        _save_results(results)
        return results

    from agents.fb_publisher_agent import FacebookPublisherAgent
    publisher = FacebookPublisherAgent()
    post_text = written.caption

    if schedule_ts:
        result = publisher.post_scheduled(post_text, schedule_ts)
    elif use_image and image_url:
        result = publisher.post_with_image_url(post_text, image_url)
    else:
        result = publisher.post_text(post_text)

    results["post"] = result

    # ──────────────────────────────────────────────────────────
    # DONE
    # ──────────────────────────────────────────────────────────
    console.print(Rule("[bold green]✅ PIPELINE HOÀN THÀNH[/bold green]", style="green"))
    _save_results(results)
    return results


def _save_results(results: dict):
    """Lưu kết quả pipeline ra file JSON."""
    Path("output").mkdir(exist_ok=True)
    ts = int(time.time())
    out_file = f"output/run_{ts}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    console.print(f"\n[dim]💾 Kết quả lưu tại: {out_file}[/dim]")


def run_test_post():
    """Đăng 1 bài test để kiểm tra token + connection."""
    config.validate(mode="publish")
    print_banner()
    console.print("[yellow]🧪 Chế độ TEST POST...[/yellow]")

    from agents.fb_publisher_agent import FacebookPublisherAgent
    publisher = FacebookPublisherAgent()
    result = publisher.post_text(
        "🤖 Test post từ AI Agent!\n\n"
        "Đây là bài test tự động bằng:\n"
        "  • AI Content Pipeline\n"
        "  • Facebook Graph API v21.0\n"
        "  • Gemini + DALL-E 3\n\n"
        "Nếu bạn thấy bài này → pipeline đang chạy tốt! 🚀\n\n"
        "#AIAgent #Automation"
    )
    console.print(f"[green]✅ Test post thành công![/green] ID: {result.get('id')}")
    return result


# ── CLI ─────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="AI Content Pipeline (Analyze + Publish)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Analyze mode (scrape + generate content):
  python main.py https://dantri.com.vn/some-article.htm
  python main.py url1 url2 url3 --save
  python main.py -f urls.txt --save

Publish mode (full pipeline → Facebook):
  python main.py --url "https://dantri.com.vn/..." 
  python main.py --url "https://..." --no-image --dry-run
  python main.py --test-post
        """,
    )

    # Analyze mode args
    parser.add_argument(
        "urls",
        nargs="*",
        help="One or more URLs to scrape and generate content (analyze mode)",
    )
    parser.add_argument(
        "-f", "--file",
        help="Path to a text file with URLs (one per line)",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save results to JSON files in output/ directory",
    )

    # Publish mode args
    parser.add_argument("--url", type=str, help="URL to process with full publish pipeline (→ Facebook)")
    parser.add_argument("--no-image", action="store_true", help="Bỏ qua bước tạo ảnh")
    parser.add_argument("--schedule", type=int, help="Unix timestamp để lên lịch đăng")
    parser.add_argument("--dry-run", action="store_true", help="In kết quả nhưng không đăng thật")
    parser.add_argument("--test-post", action="store_true", help="Đăng bài test để kiểm tra kết nối")

    args = parser.parse_args()

    try:
        if args.test_post:
            # Publish: test connection
            run_test_post()
        elif args.url:
            # Publish: full pipeline → Facebook
            run_pipeline(
                source_url=args.url,
                use_image=not args.no_image,
                schedule_ts=args.schedule,
                dry_run=args.dry_run,
            )
        elif args.file:
            # Analyze: batch from file
            config.validate(mode="analyze")
            print_banner()
            analyze_from_file(args.file, save=args.save)
        elif args.urls:
            # Analyze: single or batch from positional args
            config.validate(mode="analyze")
            print_banner()
            if len(args.urls) == 1:
                analyze_single(args.urls[0], save=args.save)
            else:
                analyze_batch(args.urls, save=args.save)
        else:
            parser.print_help()
            console.print("\n[yellow]Ví dụ:[/yellow]")
            console.print("  python main.py https://dantri.com.vn/...           [dim]# Analyze[/dim]")
            console.print("  python main.py url1 url2 --save                    [dim]# Batch analyze[/dim]")
            console.print("  python main.py --url 'https://dantri.com.vn/...'   [dim]# Publish to FB[/dim]")
            console.print("  python main.py --test-post                         [dim]# Test FB[/dim]")
            sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]❌ QUÁ TRÌNH CHẠY GẶP LỖI:[/bold red]")

        err_str = str(e)
        if "insufficient_quota" in err_str or "RESOURCE_EXHAUSTED" in err_str:
            console.print("[red]Lỗi: API quota đã hết.[/red]")
            console.print("[dim]→ Kiểm tra quota Gemini/OpenAI và nạp thêm nếu cần.[/dim]")
        elif "FB API Error" in err_str:
            console.print(f"[red]Lỗi: {err_str}[/red]")
            console.print("[dim]→ Kiểm tra lại quyền của Fanpage hoặc Token FB trong file .env[/dim]")
        else:
            console.print(f"[red]{err_str}[/red]")

        sys.exit(1)

