"""Email Extractor - Extract emails from text or URL"""
import re, requests, json

def handle(input_text: str, user_id: str = "default") -> dict:
    text = input_text
    if "http" in input_text:
        try:
            url = re.search(r'https?://[^\s]+', input_text).group(0)
            text = requests.get(url, timeout=10).text
        except:
            return {"error": "Could not fetch URL"}
    
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    emails = list(set(emails))[:20]
    return {"emails": emails, "count": len(emails), "payment_status": "paid"}

if __name__ == "__main__":
    import sys
    print(json.dumps(handle(sys.argv[1] if len(sys.argv) > 1 else "", "cli"), indent=2))
