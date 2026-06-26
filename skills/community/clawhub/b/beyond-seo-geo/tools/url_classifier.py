#!/usr/bin/env python3
import sys
def classify(url):
    u = url.lower()
    if "blog" in u or "article" in u: return "Blog/Support"
    if "service" in u or "services" in u: return "Service"
    if "course" in u or "academy" in u: return "Course"
    if "contact" in u or "book" in u: return "Conversion"
    if "about" in u or "team" in u: return "Trust"
    return "Unknown"
for url in sys.stdin:
    url=url.strip()
    if url: print(f"{url},{classify(url)}")
