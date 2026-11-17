#!/usr/bin/env python3
"""Daily Poem - Helper script for fetching poem sources"""
import sys

SOURCES = [
    "https://poemanalysis.com/poem-of-the-day/",
    "https://poets.org/poem-a-day",
    "https://poems.com/",
    "https://discoverpoetry.com/poems/poem-of-the-day/",
]

for i, url in enumerate(SOURCES, 1):
    print(f"Source {i}: {url}")
