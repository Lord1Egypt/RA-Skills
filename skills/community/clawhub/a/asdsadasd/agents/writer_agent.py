"""
agents/writer_agent.py
───────────────────────
Agent 2: Dùng Google Gemini biến raw content → bài post Facebook hấp dẫn.

Output: GeneratedContent (title, caption, hashtags, image_prompt)
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import time
import config
from google import genai
from rich.console import Console

from models import ScrapedContent, GeneratedContent
from utils import logger, truncate_text

console = Console()

client = genai.Client(api_key=config.GEMINI_API_KEY)


SYSTEM_PROMPT = """Bạn là một chuyên gia viết bài Facebook viral cho thị trường Việt Nam.

Nhiệm vụ: Viết lại nội dung bài báo/post thành một bài đăng Facebook hấp dẫn.

Quy tắc:
1. KHÔNG sao chép nguyên văn - phải viết lại hoàn toàn bằng góc nhìn riêng
2. Hook mạnh: câu đầu tiên phải gây chú ý ngay lập tức (dùng số liệu, câu hỏi, hoặc sự thật bất ngờ)
3. Nội dung: súc tích, dễ đọc, xuống dòng sau mỗi 2-3 câu
4. Emoji: dùng vừa phải (3-5 cái), phù hợp ngữ cảnh
5. Kết thúc: 1 câu hỏi gợi mở để tăng comment/engagement
6. Độ dài caption: 150-250 từ (KHÔNG quá dài)
7. Tông: thân thiện, tự nhiên như người bình thường viết — KHÔNG phải tin tức chính thức
8. KHÔNG đề cập nguồn báo, KHÔNG dùng từ "theo báo X"
9. Hashtag liên quan và phổ biến
10. Tối ưu cho engagement trên Facebook

Output PHẢI là JSON hợp lệ với format sau (không markdown, không code block):
{
    "title": "Tiêu đề ngắn gọn, thu hút (tối đa 100 ký tự)",
    "caption": "Nội dung caption cho Facebook (tối đa 500 ký tự). Phải có hook mở đầu, nội dung chính, và CTA cuối.",
    "hashtags": ["hashtag1", "hashtag2", "hashtag3", "hashtag4", "hashtag5"],
    "image_prompt": "English DALL-E prompt for a thumbnail image (1 sentence, photorealistic style)"
}"""


class WriterAgent:
    def __init__(self):
        self.model = config.GEMINI_MODEL

    def write(self, scraped: ScrapedContent) -> GeneratedContent | None:
        """Generate social media content from scraped data using Gemini."""
        if not scraped.is_accessible or not scraped.text:
            logger.warning(f"Cannot generate content: no text available for {scraped.url}")
            return None

        source_text = truncate_text(scraped.text, 4000)

        user_prompt = (
            f"Nguồn: {scraped.url}\n"
            f"Tiêu đề gốc: {scraped.title or 'Không có'}\n"
            f"Mô tả: {scraped.description or 'Không có'}\n"
            f"Tác giả: {scraped.author or 'Không rõ'}\n\n"
            f"Nội dung bài viết:\n{source_text}"
        )

        console.print(f"[yellow]✍️  AI đang viết bài ({self.model})...[/yellow]")

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=self.model,
                    contents=user_prompt,
                    config=genai.types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                    ),
                )
                raw_text = response.text.strip()

                # Clean markdown code blocks if present
                if raw_text.startswith("```"):
                    raw_text = raw_text.split("\n", 1)[1]
                    raw_text = raw_text.rsplit("```", 1)[0]
                    raw_text = raw_text.strip()

                data = json.loads(raw_text)

                caption = data.get("caption", "")
                if len(caption) > config.MAX_CAPTION_LENGTH:
                    caption = truncate_text(caption, config.MAX_CAPTION_LENGTH)

                # Build hashtag-appended full text
                hashtags = data.get("hashtags", [])
                hashtags_str = " ".join(
                    f"#{tag}" if not tag.startswith("#") else tag
                    for tag in hashtags
                )

                result = GeneratedContent(
                    source_url=scraped.url,
                    title=data.get("title", ""),
                    caption=caption + (f"\n\n{hashtags_str}" if hashtags_str else ""),
                    hashtags=hashtags,
                    image_prompt=data.get("image_prompt"),
                    original_title=scraped.title,
                )

                console.print(
                    f"[green]✅ Bài viết xong![/green] "
                    f"{len(caption)} chars | hashtags: {hashtags}"
                )
                return result

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse Gemini response as JSON: {e}")
                logger.error(f"Raw response: {raw_text[:500]}")
                return None
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    wait = 10 * (attempt + 1)
                    logger.warning(f"Rate limited. Retrying in {wait}s... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait)
                    continue
                logger.error(f"Content generation failed: {type(e).__name__}: {e}")
                return None

        logger.error("All retries exhausted for Gemini API.")
        return None

    def write_multiple(self, scraped_list: list[ScrapedContent]) -> list[GeneratedContent]:
        """Generate content for multiple scraped items."""
        results = []
        for i, scraped in enumerate(scraped_list, 1):
            logger.info(f"[{i}/{len(scraped_list)}] Generating for: {scraped.url}")
            content = self.write(scraped)
            if content:
                results.append(content)
                console.print(content.formatted_output())
                console.print()
            else:
                logger.warning(f"Skipped: {scraped.url}")
        return results


# ── Test ────────────────────────────────────────────────────
if __name__ == "__main__":
    agent = WriterAgent()
    sample = ScrapedContent(
        url="https://dantri.com.vn/example",
        title="Hà Nội nắng nóng 39 độ, kỷ lục tháng 3",
        text=(
            "Theo Đài khí tượng thủy văn khu vực đồng bằng Bắc bộ, "
            "hôm nay Hà Nội ghi nhận nhiệt độ lên tới 39 độ C, phá vỡ kỷ lục "
            "nhiệt độ tháng 3 từng được thiết lập năm 1998. "
            "Người dân được khuyến cáo hạn chế ra ngoài từ 10h-16h, "
            "uống nhiều nước và mặc quần áo thoáng mát..."
        ),
        source_name="dantri",
    )
    result = agent.write(sample)
    if result:
        print(result.formatted_output())
