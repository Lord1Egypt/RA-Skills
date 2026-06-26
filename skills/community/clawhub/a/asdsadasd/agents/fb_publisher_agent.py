"""
agents/fb_publisher_agent.py
─────────────────────────────
Agent 4: Đăng bài lên Facebook Fanpage bằng Graph API.

Features:
- Đăng text post
- Đăng post kèm ảnh (từ URL hoặc file local)
- Retry với exponential backoff
- Rate limit safe
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import requests
import config
from pathlib import Path
from rich.console import Console

console = Console()


class FacebookPublisherAgent:
    def __init__(self):
        self.page_token = config.FB_PAGE_ACCESS_TOKEN
        self.page_id = config.FB_PAGE_ID
        self.base_url = config.FB_BASE_URL

        if not self.page_token:
            console.print(
                "[bold red]⚠️  FB_PAGE_ACCESS_TOKEN chưa được set trong .env![/bold red]\n"
                "→ Chạy: python agents/fb_token_helper.py để lấy token."
            )

    # ── Internal: retry wrapper ─────────────────────────────
    def _request(self, method: str, url: str, max_retries: int = None, **kwargs) -> dict:
        """HTTP request với retry + exponential backoff."""
        max_retries = max_retries or config.MAX_POST_RETRIES
        for attempt in range(max_retries):
            try:
                resp = requests.request(method, url, timeout=30, **kwargs)

                # Rate limit
                if resp.status_code == 429:
                    wait_sec = 10 * (2 ** attempt)
                    console.print(f"[yellow]⏳ Rate limited. Chờ {wait_sec}s...[/yellow]")
                    time.sleep(wait_sec)
                    continue

                # Token expired / invalid
                if resp.status_code in (400, 401, 403):
                    data = resp.json()
                    err = data.get("error", {})
                    console.print(f"[red]❌ FB API Error {err.get('code')}: {err.get('message')}[/red]")
                    if err.get("code") in (190, 102):  # Token expired
                        console.print("[red]→ Token hết hạn! Chạy lại fb_token_helper.py[/red]")
                    raise RuntimeError(f"FB API Error: {err.get('message')}")

                resp.raise_for_status()
                return resp.json()

            except requests.exceptions.ConnectionError:
                console.print(f"[yellow]🔌 Mất kết nối (lần {attempt+1}/{max_retries}). Chờ 5s...[/yellow]")
                time.sleep(5)

        raise RuntimeError(f"Request thất bại sau {max_retries} lần thử: {url}")

    # ── Upload ảnh (unpublished) ────────────────────────────
    def _upload_photo_from_url(self, image_url: str) -> str:
        """Upload ảnh từ URL lên FB, trả về photo_id."""
        console.print("[yellow]📤 Đang upload ảnh lên Facebook...[/yellow]")
        url = f"{self.base_url}/{self.page_id}/photos"
        data = self._request("POST", url, data={
            "url": image_url,
            "published": "false",
            "access_token": self.page_token,
        })
        photo_id = data.get("id")
        console.print(f"[green]✅ Upload ảnh xong — photo_id: {photo_id}[/green]")
        return photo_id

    def _upload_photo_from_file(self, file_path: str) -> str:
        """Upload ảnh từ file local lên FB, trả về photo_id."""
        console.print("[yellow]📤 Đang upload ảnh từ file local...[/yellow]")
        url = f"{self.base_url}/{self.page_id}/photos"
        with open(file_path, "rb") as f:
            data = self._request("POST", url, data={
                "published": "false",
                "access_token": self.page_token,
            }, files={"source": (Path(file_path).name, f, "image/jpeg")})
        photo_id = data.get("id")
        console.print(f"[green]✅ Upload ảnh xong — photo_id: {photo_id}[/green]")
        return photo_id

    # ── Post text only ──────────────────────────────────────
    def post_text(self, message: str) -> dict:
        """Đăng bài text thuần lên Fanpage."""
        console.print("[bold cyan]📝 Đăng text post lên Fanpage...[/bold cyan]")
        url = f"{self.base_url}/{self.page_id}/feed"
        result = self._request("POST", url, data={
            "message": message,
            "access_token": self.page_token,
        })
        post_id = result.get("id", "unknown")
        console.print(f"[bold green]🎉 Đăng thành công! Post ID: {post_id}[/bold green]")
        console.print(f"[link]https://www.facebook.com/{post_id}[/link]")
        return result

    # ── Post ảnh + caption ──────────────────────────────────
    def post_with_image_url(self, message: str, image_url: str) -> dict:
        """Đăng bài kèm ảnh (từ URL công khai) lên Fanpage."""
        console.print("[bold cyan]🖼️  Đăng post kèm ảnh (URL) lên Fanpage...[/bold cyan]")
        photo_id = self._upload_photo_from_url(image_url)
        time.sleep(config.POST_DELAY_SECONDS)  # Chờ FB xử lý

        url = f"{self.base_url}/{self.page_id}/feed"
        result = self._request("POST", url, data={
            "message": message,
            "attached_media[0]": f'{{"media_fbid":"{photo_id}"}}',
            "access_token": self.page_token,
        })
        post_id = result.get("id", "unknown")
        console.print(f"[bold green]🎉 Đăng thành công! Post ID: {post_id}[/bold green]")
        console.print(f"[link]https://www.facebook.com/{post_id}[/link]")
        return result

    def post_with_image_file(self, message: str, file_path: str) -> dict:
        """Đăng bài kèm ảnh (từ file local) lên Fanpage."""
        console.print("[bold cyan]🖼️  Đăng post kèm ảnh (file) lên Fanpage...[/bold cyan]")
        photo_id = self._upload_photo_from_file(file_path)
        time.sleep(config.POST_DELAY_SECONDS)

        url = f"{self.base_url}/{self.page_id}/feed"
        result = self._request("POST", url, data={
            "message": message,
            "attached_media[0]": f'{{"media_fbid":"{photo_id}"}}',
            "access_token": self.page_token,
        })
        post_id = result.get("id", "unknown")
        console.print(f"[bold green]🎉 Đăng thành công! Post ID: {post_id}[/bold green]")
        console.print(f"[link]https://www.facebook.com/{post_id}[/link]")
        return result

    # ── Scheduled post ──────────────────────────────────────
    def post_scheduled(self, message: str, unix_timestamp: int) -> dict:
        """Đăng bài theo lịch."""
        console.print(f"[cyan]⏰ Lên lịch đăng bài lúc timestamp: {unix_timestamp}[/cyan]")
        url = f"{self.base_url}/{self.page_id}/feed"
        result = self._request("POST", url, data={
            "message": message,
            "scheduled_publish_time": str(unix_timestamp),
            "published": "false",
            "access_token": self.page_token,
        })
        console.print(f"[green]✅ Đã lên lịch! Post ID: {result.get('id')}[/green]")
        return result

    # ── Xem insights bài đăng ──────────────────────────────
    def get_post_insights(self, post_id: str) -> dict:
        """Lấy thống kê reactions, comments, shares của bài."""
        url = f"{self.base_url}/{post_id}"
        result = self._request("GET", url, params={
            "fields": "message,created_time,reactions.summary(true),comments.summary(true),shares",
            "access_token": self.page_token,
        })
        return result


# ── Test ────────────────────────────────────────────────────
if __name__ == "__main__":
    agent = FacebookPublisherAgent()
    # Test text post
    result = agent.post_text(
        "🤖 Test post từ AI Agent!\n\n"
        "Đây là bài test tự động bằng OpenClaw + Facebook Graph API.\n\n"
        "Bạn thấy bài này thì pipeline đang chạy đúng rồi! 🚀\n\n"
        "#AIAgent #Automation #Facebook"
    )
    print(result)
