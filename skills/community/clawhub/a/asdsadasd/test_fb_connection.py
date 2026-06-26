"""
test_fb_connection.py
──────────────────────
Script test nhanh kết nối Facebook Graph API.
Chạy cái này TRƯỚC khi dùng main.py để xác nhận token OK.

    python test_fb_connection.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
import config
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def test_app_credentials():
    """Test App ID + Secret hợp lệ."""
    console.print("[yellow]1️⃣  Kiểm tra App credentials...[/yellow]")
    url = f"{config.FB_BASE_URL}/app"
    resp = requests.get(url, params={
        "access_token": f"{config.FB_APP_ID}|{config.FB_APP_SECRET}"
    })
    if resp.status_code == 200:
        data = resp.json()
        console.print(f"[green]✅ App OK:[/green] {data.get('name')} (ID: {data.get('id')})")
        return True
    else:
        console.print(f"[red]❌ App credentials lỗi: {resp.text}[/red]")
        return False


def test_page_token():
    """Test Page Access Token và lấy thông tin Page."""
    console.print("[yellow]2️⃣  Kiểm tra Page Access Token...[/yellow]")

    if not config.FB_PAGE_ACCESS_TOKEN:
        console.print(
            "[red]❌ FB_PAGE_ACCESS_TOKEN chưa set![/red]\n"
            "→ Chạy: [bold]python agents/fb_token_helper.py[/bold]"
        )
        return False

    url = f"{config.FB_BASE_URL}/{config.FB_PAGE_ID}"
    resp = requests.get(url, params={
        "fields": "id,name,fan_count,category",
        "access_token": config.FB_PAGE_ACCESS_TOKEN,
    })

    if resp.status_code == 200:
        data = resp.json()
        table = Table(show_header=False, border_style="green")
        table.add_column("Key", style="bold")
        table.add_column("Value")
        table.add_row("Page ID", data.get("id", "N/A"))
        table.add_row("Tên Page", data.get("name", "N/A"))
        table.add_row("Followers", str(data.get("fan_count", 0)))
        table.add_row("Category", data.get("category", "N/A"))
        console.print("[green]✅ Page Token OK[/green]")
        console.print(table)
        return True
    else:
        err = resp.json().get("error", {})
        console.print(f"[red]❌ Page token lỗi ({err.get('code')}): {err.get('message')}[/red]")
        if err.get("code") == 190:
            console.print("→ Token hết hạn! Chạy lại [bold]python agents/fb_token_helper.py[/bold]")
        return False


def main():
    console.print(Panel.fit(
        "[bold cyan]🔌 Facebook Connection Test[/bold cyan]",
        border_style="cyan"
    ))
    console.print(f"[dim]App ID: {config.FB_APP_ID}[/dim]")
    console.print(f"[dim]Page ID: {config.FB_PAGE_ID}[/dim]\n")

    ok_app = test_app_credentials()
    ok_token = test_page_token()

    console.print()
    if ok_app and ok_token:
        console.print(Panel.fit(
            "[bold green]🎉 Tất cả OK! Sẵn sàng chạy pipeline.[/bold green]\n"
            "→ [bold]python main.py --test-post[/bold]",
            border_style="green"
        ))
    else:
        console.print(Panel.fit(
            "[bold red]⚠️  Có lỗi. Xem hướng dẫn bên trên để fix.[/bold red]",
            border_style="red"
        ))


if __name__ == "__main__":
    main()
