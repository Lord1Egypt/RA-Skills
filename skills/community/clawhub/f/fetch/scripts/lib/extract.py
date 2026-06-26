#!/usr/bin/env python3
import html
import re
from html.parser import HTMLParser

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)

def strip_html(raw_html: str) -> str:
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", raw_html)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\r", "", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

def extract_title(raw_html: str) -> str:
    m = re.search(r"(?is)<title>(.*?)</title>", raw_html)
    if not m:
        return "Untitled"
    return html.unescape(m.group(1)).strip()

def extract_links(raw_html: str):
    parser = LinkParser()
    parser.feed(raw_html)
    return parser.links[:100]
