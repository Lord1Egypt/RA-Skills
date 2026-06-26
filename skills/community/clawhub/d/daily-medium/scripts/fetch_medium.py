#!/usr/bin/env python3
"""
Daily Medium Digest Fetcher
Fetches Medium Daily Digest emails from Gmail and extracts article information.
"""

import imaplib
import email
import re
import os
from email.header import decode_header
from datetime import datetime

def extract_medium_urls(text):
    """Extract Medium article URLs from email content"""
    # Look for medium.com article URLs
    urls = re.findall(r'https?://(?:www\.)?medium\.com/[^\s<>"\?]+', text)
    # Also look for medium.com/p/ article links
    urls += re.findall(r'https?://(?:www\.)?medium\.com/p/[^\s<>"\?]+', text)
    
    # Filter out non-article URLs
    article_urls = []
    for url in urls:
        # Skip image CDN URLs
        if 'miro.medium.com' in url:
            continue
        # Skip policy, help, plans pages
        if any(x in url for x in ['/policy/', '/help/', '/plans', '@omnimahui']):
            continue
        # Must look like an article URL
        if '/@' in url or '/p/' in url:
            article_urls.append(url)
    
    return list(set(article_urls))  # Remove duplicates

def fetch_medium_digest(
    email_address=None,
    password=None,
    imap_server="imap.gmail.com",
    max_articles=15
):
    """
    Fetch Medium Daily Digest emails from Gmail.
    
    Args:
        email_address: Gmail address (defaults to EMAIL_ADDRESS env var)
        password: App password (defaults to EMAIL_PASSWORD env var)
        imap_server: IMAP server address
        max_articles: Maximum number of articles to return
    
    Returns:
        List of article dictionaries with title, author, url
    """
    # Get credentials from environment if not provided
    email_address = email_address or os.environ.get('EMAIL_ADDRESS')
    password = password or os.environ.get('EMAIL_PASSWORD')
    
    if not email_address or not password:
        raise ValueError("Email credentials required. Set EMAIL_ADDRESS and EMAIL_PASSWORD env vars.")
    
    try:
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, password)
        mail.select("inbox")
        
        # Search for emails from medium.com
        status, messages = mail.search(None, 'FROM', '"medium.com"')
        
        if status != "OK":
            print("No emails found from medium.com")
            return []
        
        email_ids = messages[0].split()
        
        if not email_ids:
            return []
        
        # Get the most recent email
        latest_email_id = email_ids[-1]
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        
        if status != "OK":
            return []
        
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        # Decode subject
        subject = decode_header(msg["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()
        
        # Get date
        date_str = msg.get("Date", "")
        
        # Extract HTML body
        html_body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/html":
                    try:
                        html_body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
                    except:
                        continue
        else:
            try:
                html_body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            except:
                pass
        
        # Extract article URLs
        urls = extract_medium_urls(html_body)
        
        # Parse articles from URLs
        articles = []
        for url in urls[:max_articles]:
            # Extract author from URL
            author_match = re.search(r'@([^/]+)', url)
            author = author_match.group(1) if author_match else "unknown"
            
            # Extract article slug for title
            slug_match = re.search(r'@.+/([^\?]+)', url)
            if slug_match:
                slug = slug_match.group(1)
                # Convert slug to readable title
                title = slug.replace('-', ' ').title()
            else:
                title = "Article"
            
            articles.append({
                'title': title,
                'author': author,
                'url': url,
                'freedium_url': f"https://freedium-mirror.cfd/{url}"
            })
        
        mail.close()
        mail.logout()
        
        return {
            'digest_date': date_str,
            'digest_title': subject,
            'articles': articles
        }
        
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return None

if __name__ == "__main__":
    result = fetch_medium_digest()
    if result:
        print(f"\n📰 {result['digest_title']}")
        print(f"Date: {result['digest_date']}\n")
        for i, article in enumerate(result['articles'], 1):
            print(f"{i}. {article['title']}")
            print(f"   By: @{article['author']}")
            print(f"   Freedium: {article['freedium_url']}\n")