# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'C:\Users\an\.openclaw\workspace\skills\gequhai-music\scripts')
from gequhai_crawler import get_hot_songs, get_top_songs

print("=== 热门歌曲 ===")
songs = get_hot_songs()
if songs:
    for i, s in enumerate(songs[:15], 1):
        print(f"{i}. {s['title']} - {s['artist']}")
else:
    print("获取热门歌曲失败")

print("\n=== 新歌榜 ===")
new_songs = get_top_songs("new")
if new_songs:
    for i, s in enumerate(new_songs[:10], 1):
        print(f"{i}. {s['title']} - {s['artist']}")
