#!/usr/bin/env python3
import sys
def verdict(relevance, risk):
    if risk == "high": return "Avoid"
    if relevance == "high" and risk in ("low","medium"): return "Good prospect"
    if relevance == "medium" and risk == "low": return "Review manually"
    return "Low priority"
print("Use CSV columns manually: url,relevance(low/medium/high),risk(low/medium/high)")
