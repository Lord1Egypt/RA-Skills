"""
agents/image_agent.py
──────────────────────
Agent 3: Tạo ảnh bằng DALL-E 3 từ image_prompt do WriterAgent sinh ra.

Output: local file path hoặc image URL tạm thời
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx
import config
from openai import OpenAI
from rich.console import Console
from pathlib import Path

console = Console()
OUTPUT_DIR = Path("output/images")


class ImageAgent:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def generate(self, prompt: str, filename: str = "fb_post") -> str:
        """
        Tạo ảnh từ prompt, download về local.
        Trả về đường dẫn file local.
        """
        console.print(f"[yellow]🎨 Đang tạo ảnh...[/yellow]")
        console.print(f"[dim]Prompt: {prompt[:100]}...[/dim]")

        # Thêm style suffix để ảnh nhất quán
        full_prompt = (
            f"{prompt}. "
            "Editorial photography style, vibrant colors, high contrast, "
            "cinematic lighting, 16:9 aspect ratio. "
            "No text overlay, no watermark."
        )

        response = self.client.images.generate(
            model=config.IMAGE_MODEL,
            prompt=full_prompt,
            size="1792x1024",   # Landscape — phù hợp Facebook
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        revised_prompt = response.data[0].revised_prompt or prompt

        console.print(f"[green]✅ Ảnh đã tạo xong[/green]")
        console.print(f"[dim]URL: {image_url[:80]}...[/dim]")

        # Download ảnh về local
        local_path = self._download(image_url, filename)
        console.print(f"[green]💾 Đã lưu:[/green] {local_path}")

        return str(local_path), image_url

    def _download(self, url: str, filename: str) -> Path:
        """Download ảnh từ URL về thư mục output/images/."""
        import time
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in filename)
        ts = int(time.time())
        filepath = OUTPUT_DIR / f"{safe_name}_{ts}.jpg"

        with httpx.Client(follow_redirects=True) as client:
            resp = client.get(url, timeout=60)
            resp.raise_for_status()
            filepath.write_bytes(resp.content)

        return filepath

    def get_public_url(self, local_path: str) -> str:
        """
        Nếu cần URL công khai để upload lên FB, dùng imgbb miễn phí.
        Hoặc để đơn giản: trả nguyên DALL-E URL (hợp lệ ~1h).
        
        Hiện tại: trả lại DALL-E URL trực tiếp (đủ dùng trong pipeline).
        """
        # TODO: Nếu cần URL bền vững, tích hợp imgbb.com hoặc Cloudinary
        return local_path  # Placeholder — xem fb_publisher_agent.py


# ── Test ────────────────────────────────────────────────────
if __name__ == "__main__":
    agent = ImageAgent()
    test_prompt = (
        "A crowded Hanoi street in extreme summer heat, people using umbrellas, "
        "thermometer showing 39 degrees Celsius, golden light haze in the air."
    )
    local_path, url = agent.generate(test_prompt, "test_hanoi_heat")
    print(f"\nLocal: {local_path}")
    print(f"URL: {url}")
