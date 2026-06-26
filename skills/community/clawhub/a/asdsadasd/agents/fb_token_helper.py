"""
agents/fb_token_helper.py
──────────────────────────
Tiện ích lấy và exchange Facebook Access Token.

Chạy trực tiếp:
    python agents/fb_token_helper.py

Hướng dẫn:
  1. Chạy script này
  2. Làm theo hướng dẫn để lấy short-lived token từ Graph Explorer
  3. Script sẽ exchange → long-lived user token → page token
  4. Copy Page Access Token vào .env  (FB_PAGE_ACCESS_TOKEN)
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import json
import config
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def exchange_to_long_lived(short_token: str) -> str:
    """
    Đổi Short-lived User Token → Long-lived User Token (60 ngày).
    """
    url = f"{config.FB_BASE_URL}/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": config.FB_APP_ID,
        "client_secret": config.FB_APP_SECRET,
        "fb_exchange_token": short_token,
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    if "access_token" not in data:
        raise ValueError(f"Lỗi exchange token: {data}")
    return data["access_token"]


def get_page_tokens(long_lived_user_token: str) -> list[dict]:
    """
    Lấy danh sách Pages + Page Access Tokens từ long-lived user token.
    """
    url = f"{config.FB_BASE_URL}/me/accounts"
    params = {"access_token": long_lived_user_token}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json().get("data", [])


def debug_token(token: str) -> dict:
    """Kiểm tra thông tin token."""
    url = f"{config.FB_BASE_URL}/debug_token"
    params = {
        "input_token": token,
        "access_token": f"{config.FB_APP_ID}|{config.FB_APP_SECRET}",
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json().get("data", {})


def run_interactive():
    console.print(Panel.fit(
        "[bold cyan]Facebook Token Helper[/bold cyan]\n"
        "Giúp bạn lấy Page Access Token để đăng bài Fanpage",
        border_style="cyan"
    ))

    console.print("\n[bold yellow]BƯỚC 1:[/bold yellow] Lấy Short-lived User Token")
    console.print(
        "→ Mở link sau trong trình duyệt:\n"
        f"[link]https://developers.facebook.com/tools/explorer[/link]\n\n"
        "Chọn App [bold]4348763312075291[/bold], click [bold]Generate Access Token[/bold]\n"
        "Tích chọn permissions:\n"
        "  ✅ pages_manage_posts\n"
        "  ✅ pages_read_engagement\n"
        "  ✅ pages_show_list\n"
        "  ✅ public_profile\n"
    )

    short_token = console.input("[bold green]Paste Short-lived Token vào đây:[/bold green] ").strip()
    if not short_token:
        console.print("[red]Token rỗng — thoát.[/red]")
        return

    console.print("\n[yellow]⏳ Đang exchange sang Long-lived token...[/yellow]")
    try:
        long_token = exchange_to_long_lived(short_token)
        console.print(f"[green]✅ Long-lived User Token:[/green]\n{long_token}\n")
    except Exception as e:
        console.print(f"[red]❌ Exchange thất bại: {e}[/red]")
        return

    # Debug token
    info = debug_token(long_token)
    console.print(f"[dim]Token expires: {info.get('expires_at', 'N/A')} | valid: {info.get('is_valid')}[/dim]\n")

    console.print("[yellow]⏳ Đang lấy Page Access Tokens...[/yellow]")
    try:
        pages = get_page_tokens(long_token)
    except Exception as e:
        console.print(f"[red]❌ Lỗi lấy pages: {e}[/red]")
        return

    if not pages:
        console.print("[red]⚠️  Không tìm thấy Page nào. Đảm bảo tài khoản FB quản lý ít nhất 1 Page.[/red]")
        return

    table = Table(title="📄 Danh sách Pages", show_header=True, header_style="bold magenta")
    table.add_column("Page ID", style="cyan")
    table.add_column("Page Name", style="white")
    table.add_column("Page Token (50 ký tự đầu)", style="dim")

    for page in pages:
        table.add_row(
            page.get("id", ""),
            page.get("name", ""),
            page.get("access_token", "")[:50] + "..."
        )
    console.print(table)

    # Save to .env hint
    console.print("\n[bold green]✅ XONG! Cập nhật .env:[/bold green]")
    for page in pages:
        console.print(f"\nPage: [bold]{page.get('name')}[/bold] (ID: {page.get('id')})")
        console.print(f"FB_USER_ACCESS_TOKEN={long_token}")
        console.print(f"FB_PAGE_ACCESS_TOKEN={page.get('access_token')}")
        console.print(f"FB_PAGE_ID={page.get('id')}")

    # Save to file
    output_path = "fb_tokens_output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "long_lived_user_token": long_token,
            "pages": pages
        }, f, ensure_ascii=False, indent=2)
    console.print(f"\n[dim]Token đã lưu vào {output_path} (đừng commit file này!)[/dim]")


if __name__ == "__main__":
    run_interactive()
