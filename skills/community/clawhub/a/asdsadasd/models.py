"""
models.py — Shared data models for scraped and generated content.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ScrapedContent:
    """Represents raw scraped content from a URL."""
    url: str
    title: Optional[str] = None
    text: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    published_date: Optional[str] = None
    source_name: Optional[str] = None
    scraped_at: str = field(default_factory=lambda: datetime.now().isoformat())
    is_accessible: bool = True
    error_message: Optional[str] = None

    def summary(self) -> str:
        """Return a brief summary of scraped data."""
        status = "✅ Accessible" if self.is_accessible else "❌ Inaccessible"
        return (
            f"[{status}] {self.url}\n"
            f"  Title: {self.title or 'N/A'}\n"
            f"  Source: {self.source_name or 'N/A'}\n"
            f"  Text length: {len(self.text) if self.text else 0} chars"
        )


@dataclass
class GeneratedContent:
    """Represents AI-generated content for social media."""
    source_url: str
    title: str
    caption: str
    hashtags: list[str] = field(default_factory=list)
    image_prompt: Optional[str] = None
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    original_title: Optional[str] = None

    def formatted_output(self) -> str:
        """Return formatted content ready for review."""
        hashtag_str = " ".join(f"#{tag}" for tag in self.hashtags)
        lines = [
            f"{'='*60}",
            f"📝 GENERATED CONTENT",
            f"{'='*60}",
            f"Source: {self.source_url}",
            f"Original Title: {self.original_title or 'N/A'}",
            f"{'-'*60}",
            f"📌 Title:\n{self.title}\n",
            f"📄 Caption:\n{self.caption}\n",
            f"🏷️ Hashtags:\n{hashtag_str}",
        ]
        if self.image_prompt:
            lines.append(f"\n🎨 Image Prompt:\n{self.image_prompt}")
        lines.append(f"{'='*60}")
        return "\n".join(lines)
