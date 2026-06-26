import re
import json
import sys
from typing import List, Dict, Optional
from duckduckgo_search import DDGS
from youtube_transcript_api import YouTubeTranscriptApi
from fastmcp import FastMCP

class ClawVoyant:
    """Core logic for YouTube search and transcript extraction."""
    
    def __init__(self):
        self.ddgs = DDGS()

    def _extract_video_id(self, url: str) -> Optional[str]:
        patterns = [
            r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
            r"(?:embed\/|v\/|youtu.be\/)([0-9A-Za-z_-]{11})"
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search YouTube and return a list of video details."""
        results = []
        search_query = f"{query} YouTube"
        
        raw_results = self.ddgs.text(search_query, max_results=max_results * 4)
        
        for r in raw_results:
            href = r.get("href", "")
            if "youtube.com/watch" in href or "youtu.be/" in href:
                results.append({
                    "title": r.get("title"),
                    "url": href,
                    "description": r.get("body")
                })
                if len(results) >= max_results:
                    break
        
        if not results:
            alt_results = self.ddgs.text(f"site:youtube.com {query}", max_results=max_results)
            for r in alt_results:
                results.append({
                    "title": r.get("title"),
                    "url": r.get("href"),
                    "description": r.get("body")
                })
        
        return results

    def get_transcript(self, url: str) -> str:
        """Fetch the full transcript for a given YouTube URL."""
        video_id = self._extract_video_id(url)
        if not video_id:
            raise ValueError("Could not extract video ID from URL.")

        try:
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
            return " ".join([snippet['text'] for snippet in transcript_data])
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve transcript: {str(e)}")

# Create an MCP server
mcp = FastMCP("ClawVoyant")
cv = ClawVoyant()

@mcp.tool()
def search_youtube(query: str, max_results: int = 5) -> str:
    """
    Search YouTube for videos.
    Returns a list of titles, URLs, and descriptions.
    """
    results = cv.search(query, max_results=max_results)
    if not results:
        return "No results found."
    
    output = []
    for r in results:
        output.append(f"Title: {r['title']}\nURL: {r['url']}\nDescription: {r['description']}\n---")
    return "\n".join(output)

@mcp.tool()
def get_youtube_transcript(url: str) -> str:
    """
    Extract the full transcript from a YouTube video URL.
    """
    try:
        return cv.get_transcript(url)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
