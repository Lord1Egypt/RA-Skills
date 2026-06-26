#!/usr/bin/env python3
"""获取视频数据，输出 JSON 供 agent 用 LLM 生成总结

用法:
  python scripts/fetch_data.py <收藏夹名称> [latest|random|<bvid>]

输出: JSON 到 stdout，包含视频详情、字幕、评论、弹幕
"""

import sys
import json
from pathlib import Path

skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir))

from src.config import Config
from src.bilibili_api import BilibiliAPI
from src.memory import Memory


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "用法: python fetch_data.py <收藏夹名称> [latest|random|<bvid>]"}))
        sys.exit(1)

    folder_name = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "latest"

    # 验证配置
    missing = Config.validate()
    if missing:
        print(json.dumps({"error": f"缺少配置: {', '.join(missing)}"}))
        sys.exit(1)

    Config.ensure_dirs()
    api = BilibiliAPI(Config.BILIBILI_SESSDATA, Config.BILIBILI_BILI_JCT, Config.BILIBILI_BUVID3)
    memory = Memory(Config.DATA_DIR / "processed.json")

    # 获取收藏夹
    try:
        folders = api.get_favorites_list()
    except Exception as e:
        print(json.dumps({"error": f"获取收藏夹失败: {e}"}))
        sys.exit(1)

    folder = next((f for f in folders if f.title == folder_name), None)
    if not folder:
        print(json.dumps({
            "error": f"找不到收藏夹 '{folder_name}'",
            "available": [f.title for f in folders],
        }))
        sys.exit(1)

    # 获取视频列表
    all_videos = []
    page = 1
    while True:
        videos = api.get_videos_from_folder(folder.id, page=page, page_size=20)
        if not videos:
            break
        all_videos.extend(videos)
        if len(videos) < 20:
            break
        page += 1

    # 选择视频
    if mode == "latest":
        unprocessed = [v for v in all_videos if not memory.is_processed(v.bvid)]
        if not unprocessed:
            print(json.dumps({"error": "所有视频都已处理过"}))
            sys.exit(0)
        video_brief = unprocessed[0]
    elif mode == "random":
        import random
        unprocessed = [v for v in all_videos if not memory.is_processed(v.bvid)]
        if not unprocessed:
            print(json.dumps({"error": "所有视频都已处理过"}))
            sys.exit(0)
        video_brief = random.choice(unprocessed)
    else:
        video_brief = next((v for v in all_videos if v.bvid == mode), None)
        if not video_brief:
            print(json.dumps({"error": f"收藏夹中找不到 {mode}"}))
            sys.exit(1)

    # 获取视频详情
    try:
        video = api.get_video_detail(video_brief.bvid)
    except Exception as e:
        print(json.dumps({"error": f"获取视频详情失败: {e}"}))
        sys.exit(1)

    # 获取字幕
    subtitles = []
    if video.subtitle_url:
        try:
            subtitles = api.get_subtitles(video.subtitle_url)
        except Exception:
            pass

    # 获取评论
    comments = []
    try:
        raw_comments = api.get_top_comments(video.aid, limit=Config.MAX_COMMENTS)
        comments = [{"user": c.uname, "content": c.content, "likes": c.like} for c in raw_comments]
    except Exception:
        pass

    # 获取弹幕
    danmakus = []
    try:
        raw_danmakus = api.get_danmakus(video.cid, limit=Config.MAX_DANMAKUS)
        danmakus = [{"content": d.content, "time": d.send_time} for d in raw_danmakus]
    except Exception:
        pass

    # 输出 JSON
    output = {
        "bvid": video.bvid,
        "title": video.title,
        "desc": video.desc,
        "owner": video.owner,
        "duration": video.duration,
        "view": video.view,
        "like": video.like,
        "subtitle_count": len(subtitles),
        "subtitles": subtitles,
        "comments": comments,
        "danmakus": danmakus,
        "folder_name": folder.title,
        "folder_total": folder.media_count,
        "processed_count": memory.get_processed_count(),
    }

    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
