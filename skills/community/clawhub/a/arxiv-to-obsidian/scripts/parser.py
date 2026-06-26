#!/usr/bin/env python3
"""RSS XML parser for arXiv papers."""

import html
from email.utils import parsedate_to_datetime
import sys
import xml.etree.ElementTree as ET
import re


def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


def clean_abstract(text):
    abstract = re.sub(r"<[^>]+>", "", text.strip())
    abstract = html.unescape(abstract)
    abstract = re.sub(r"^arXiv:\S+\s+Announce Type:\s+\w+\s*", "", abstract)
    abstract = re.sub(r"^Abstract:\s*", "", abstract)
    return clean_text(abstract)

def parse_rss(xml_content, paper_count=10):
    """Parse arXiv RSS XML and extract paper information"""

    # Remove namespaces for easier parsing
    xml_content = re.sub(r'\sxmlns="[^"]*"', '', xml_content)

    root = ET.fromstring(xml_content)

    papers = []

    # Find all item elements
    for item in root.findall('.//item'):
        paper = {}

        # Extract title
        title_elem = item.find('title')
        if title_elem is not None and title_elem.text:
            paper['title'] = clean_text(html.unescape(title_elem.text))

        # Extract link
        link_elem = item.find('link')
        if link_elem is not None and link_elem.text:
            paper['link'] = link_elem.text.strip()

        # Extract description/abstract
        desc_elem = item.find('description')
        if desc_elem is not None and desc_elem.text:
            paper['abstract'] = clean_abstract(desc_elem.text)

        # Extract publication date
        pubdate_elem = item.find('pubDate')
        if pubdate_elem is not None and pubdate_elem.text:
            try:
                date_str = pubdate_elem.text.strip()
                paper['published'] = date_str
                dt = parsedate_to_datetime(date_str)
                paper['published_sort'] = dt.strftime('%Y-%m-%d')
                paper['_published_ts'] = dt.timestamp()
            except:
                paper['published_sort'] = '1970-01-01'
                paper['_published_ts'] = 0

        if 'title' in paper and 'link' in paper:
            papers.append(paper)

    # Sort by publication date (newest first)
    papers.sort(key=lambda x: x.get('_published_ts', 0), reverse=True)

    for paper in papers:
        paper.pop('_published_ts', None)

    # Return top N papers
    return papers[:paper_count]


def output_json(papers):
    """Output papers as JSON for downstream processing"""
    import json
    print(json.dumps(papers, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        paper_count = 10
    else:
        paper_count = int(sys.argv[1])

    # Read XML from stdin
    xml_content = sys.stdin.read()

    papers = parse_rss(xml_content, paper_count)
    output_json(papers)


if __name__ == '__main__':
    main()
