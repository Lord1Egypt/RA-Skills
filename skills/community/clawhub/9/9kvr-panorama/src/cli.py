"""CLI 入口模块（标准库 argparse 版）"""

import json
import os
import sys
import argparse
import asyncio

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools.works import WorksTools
from src.tools.media import MediaTools
from src.tools.scenes import ScenesTools
from src.tools.music import MusicTools
from src.tools.voice import VoiceTools
from src.tools.hotspot import HotspotTools
from src.tools.score import ScoreTools
from src.tools.develop import DevelopTools
from src.tools.info import InfoTools
from src.config import get_config

# 实例化工具类
works_tools = WorksTools()
media_tools = MediaTools()
scenes_tools = ScenesTools()
music_tools = MusicTools()
voice_tools = VoiceTools()
hotspot_tools = HotspotTools()
score_tools = ScoreTools()
develop_tools = DevelopTools()
info_tools = InfoTools()

VERSION = "1.0.0"


def echo_result(result):
    """格式化输出结果"""
    if isinstance(result, dict):
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result)


def cmd_works_list(args):
    result = works_tools.list_works(limit=args.limit, page=args.page, keyword=args.keyword, pid=args.pid)
    echo_result(result)


def cmd_works_info(args):
    result = works_tools.get_work_info(id=args.work_id)
    echo_result(result)


def cmd_works_scenes(args):
    result = works_tools.get_work_scenes(id=args.work_id)
    echo_result(result)


def cmd_works_update(args):
    result = works_tools.update_work_info(
        id=args.work_id,
        name=args.name,
        work_profile=args.description,
        cover=args.cover,
    )
    echo_result(result)


def cmd_works_create(args):
    if not args.media_ids:
        print("错误：需要至少一个素材ID")
        sys.exit(1)
    result = works_tools.create_work_from_media(
        media_ids=args.media_ids,
        name=args.name,
        desc=args.description,
    )
    echo_result(result)


def cmd_media_list(args):
    result = media_tools.list_media(limit=args.limit, page=args.page, keyword=args.keyword)
    echo_result(result)


def cmd_media_info(args):
    result = media_tools.get_media_info(id=args.media_id)
    echo_result(result)


def cmd_media_update(args):
    result = media_tools.update_media_info(id=args.media_id, name=args.name, description=args.description)
    echo_result(result)


def cmd_media_delete(args):
    if not args.media_ids:
        print("错误：需要至少一个素材ID")
        sys.exit(1)
    result = media_tools.delete_media(ids=args.media_ids)
    echo_result(result)


def cmd_media_upload(args):
    if not os.path.exists(args.file_path):
        print(f"错误：文件不存在: {args.file_path}")
        sys.exit(1)
    result = media_tools.upload_media(
        file=args.file_path,
        filename=os.path.basename(args.file_path),
        name=args.name,
        description=args.description,
    )
    echo_result(result)


def cmd_media_download(args):
    result = media_tools.download_media(id=args.media_id, ans=1 if args.force else 0)
    echo_result(result)


def cmd_scenes_list(args):
    result = scenes_tools.list_scenes(page=args.page, page_size=args.limit, keyword=args.keyword)
    echo_result(result)


def cmd_scenes_info(args):
    result = scenes_tools.get_scene_info(scene_id=args.scene_id)
    echo_result(result)


def cmd_scenes_update(args):
    result = scenes_tools.update_scene_info(scene_id=args.scene_id, name=args.name, description=args.description)
    echo_result(result)


def cmd_scenes_delete(args):
    result = scenes_tools.delete_scene(scene_id=args.scene_id)
    echo_result(result)


def cmd_music_tags(args):
    result = music_tools.get_music_tags()
    echo_result(result)


def cmd_music_search(args):
    tag_ids = [str(args.tag)] if args.tag is not None else None
    result = music_tools.search_music(
        keyword=args.keyword,
        page=args.page,
        page_size=args.limit,
        tag_ids=tag_ids,
    )
    echo_result(result)


def cmd_music_match(args):
    result = music_tools.match_background_music(work_id=args.work_id)
    echo_result(result)


def cmd_music_add(args):
    volume = args.volume / 100 if args.volume > 1 else args.volume
    result = music_tools.add_background_music(
        work_id=args.work_id,
        music_id=args.music_url,
        loop=bool(args.loop),
        volume=volume,
    )
    echo_result(result)


def cmd_voice_anchors(args):
    result = voice_tools.get_voice_anchors({"gender": args.gender})
    echo_result(result)


def cmd_voice_generate(args):
    result = voice_tools.generate_voice_narration({
        "text": args.text,
        "anchor_key": args.anchor_key,
        "source": args.source,
    })
    echo_result(result)


def cmd_voice_query(args):
    result = voice_tools.query_voice_result({"task_id": args.task_id})
    echo_result(result)


def cmd_voice_upload(args):
    if not os.path.exists(args.file_path):
        print(f"错误：文件不存在: {args.file_path}")
        sys.exit(1)
    result = voice_tools.upload_voice_file({"file": args.file_path, "filename": args.name})
    echo_result(result)


def cmd_voice_add(args):
    result = voice_tools.add_voice_narration({
        "work_id": args.work_id,
        "voice_url": args.voice_url,
        "loop": args.loop,
        "voice": args.volume,
    })
    echo_result(result)


def cmd_hotspot_list(args):
    result = hotspot_tools.manage_hotspot(action="query", work_id=args.work_id)
    echo_result(result)


def cmd_hotspot_add_jump(args):
    result = hotspot_tools.add_scene_jump_hotspot(
        work_id=args.work_id,
        from_scene_id=args.from_scene_id,
        to_scene_id=args.to_scene_id,
        name=args.name,
        ath=args.ath,
        atv=args.atv,
    )
    echo_result(result)


def cmd_hotspot_add_text(args):
    result = hotspot_tools.add_text_hotspot(
        work_id=args.work_id,
        scene_id=args.scene_id,
        name=args.name,
        ath=args.ath,
        atv=args.atv,
    )
    echo_result(result)


def cmd_hotspot_delete(args):
    result = hotspot_tools.manage_hotspot(action="delete", work_id=args.work_id, hotspot_id=args.hotspot_id)
    echo_result(result)


def cmd_score_get(args):
    result = asyncio.run(score_tools.getWorkScore({"work_id": args.work_id}))
    echo_result(result)


def cmd_develop_miniprogram(args):
    result = asyncio.run(develop_tools.getMiniprogramGuide({
        "platform": args.platform,
        "feature": args.feature,
    }))
    echo_result(result)


def cmd_develop_web(args):
    result = asyncio.run(develop_tools.getWebIntegrationGuide({
        "framework": args.framework,
    }))
    echo_result(result)


def cmd_develop_existing(args):
    result = asyncio.run(develop_tools.getExistingProjectGuide({
        "project_type": args.type,
    }))
    echo_result(result)


def cmd_develop_code(args):
    result = asyncio.run(develop_tools.generateIntegrationCode({
        "type": args.type,
        "platform": args.platform,
        "framework": args.framework,
        "work_id": args.work_id,
    }))
    echo_result(result)


def cmd_info_version(args):
    result = asyncio.run(info_tools.getVersion({}))
    echo_result(result)


def cmd_info_context(args):
    result = asyncio.run(info_tools.getGlobalContext({}))
    echo_result(result)


def cmd_config(args):
    config = get_config()

    if args.show:
        print(f"Timeout: {config.timeout}ms")
        print(f"Token: {'*' * len(config.token) if config.token else '未设置'}")
        print(f"UID: {config.uid or '未设置'}")

    if args.token:
        config.set(args.token, "auth", "token")
        print("Token 已设置")

    if args.uid:
        config.set(args.uid, "auth", "uid")
        print(f"UID 已设置: {args.uid}")


def build_parser():
    parser = argparse.ArgumentParser(prog="vr", description="全景VR作品管理工具")
    parser.add_argument("--version", action="version", version=VERSION)
    subparsers = parser.add_subparsers(dest="group")

    # works
    works = subparsers.add_parser("works", help="作品管理命令")
    works_sub = works.add_subparsers(dest="action")

    p = works_sub.add_parser("list")
    p.add_argument("--limit", type=int, default=3)
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--keyword", default="")
    p.add_argument("--pid", type=int, default=0)
    p.set_defaults(func=cmd_works_list)

    p = works_sub.add_parser("info")
    p.add_argument("work_id")
    p.set_defaults(func=cmd_works_info)

    p = works_sub.add_parser("scenes")
    p.add_argument("work_id")
    p.set_defaults(func=cmd_works_scenes)

    p = works_sub.add_parser("update")
    p.add_argument("work_id")
    p.add_argument("--name")
    p.add_argument("--description")
    p.add_argument("--cover")
    p.set_defaults(func=cmd_works_update)

    p = works_sub.add_parser("create")
    p.add_argument("media_ids", type=int, nargs="*")
    p.add_argument("--name", required=True)
    p.add_argument("--description", default="")
    p.set_defaults(func=cmd_works_create)

    # media
    media = subparsers.add_parser("media", help="素材管理命令")
    media_sub = media.add_subparsers(dest="action")

    p = media_sub.add_parser("list")
    p.add_argument("--limit", type=int, default=12)
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--keyword", default="")
    p.set_defaults(func=cmd_media_list)

    p = media_sub.add_parser("info")
    p.add_argument("media_id", type=int)
    p.set_defaults(func=cmd_media_info)

    p = media_sub.add_parser("update")
    p.add_argument("media_id", type=int)
    p.add_argument("--name", required=True)
    p.add_argument("--description", default="")
    p.set_defaults(func=cmd_media_update)

    p = media_sub.add_parser("delete")
    p.add_argument("media_ids", type=int, nargs="*")
    p.set_defaults(func=cmd_media_delete)

    p = media_sub.add_parser("upload")
    p.add_argument("file_path")
    p.add_argument("--name", default="素材文件")
    p.add_argument("--description", default="")
    p.set_defaults(func=cmd_media_upload)

    p = media_sub.add_parser("download")
    p.add_argument("media_id")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_media_download)

    # scenes
    scenes = subparsers.add_parser("scenes", help="场景管理命令")
    scenes_sub = scenes.add_subparsers(dest="action")

    p = scenes_sub.add_parser("list")
    p.add_argument("--limit", type=int, default=12)
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--keyword", default="")
    p.set_defaults(func=cmd_scenes_list)

    p = scenes_sub.add_parser("info")
    p.add_argument("scene_id")
    p.set_defaults(func=cmd_scenes_info)

    p = scenes_sub.add_parser("update")
    p.add_argument("scene_id", type=int)
    p.add_argument("--name", required=True)
    p.add_argument("--description", default="")
    p.set_defaults(func=cmd_scenes_update)

    p = scenes_sub.add_parser("delete")
    p.add_argument("scene_id", type=int)
    p.set_defaults(func=cmd_scenes_delete)

    # music
    music = subparsers.add_parser("music", help="音乐管理命令")
    music_sub = music.add_subparsers(dest="action")

    p = music_sub.add_parser("tags")
    p.set_defaults(func=cmd_music_tags)

    p = music_sub.add_parser("search")
    p.add_argument("--keyword", default="")
    p.add_argument("--tag", type=int)
    p.add_argument("--limit", type=int, default=12)
    p.add_argument("--page", type=int, default=1)
    p.set_defaults(func=cmd_music_search)

    p = music_sub.add_parser("match")
    p.add_argument("work_id")
    p.set_defaults(func=cmd_music_match)

    p = music_sub.add_parser("add")
    p.add_argument("work_id")
    p.add_argument("music_url")
    p.add_argument("--loop", type=int, default=1)
    p.add_argument("--volume", type=int, default=100)
    p.set_defaults(func=cmd_music_add)

    # voice
    voice = subparsers.add_parser("voice", help="语音管理命令")
    voice_sub = voice.add_subparsers(dest="action")

    p = voice_sub.add_parser("anchors")
    p.add_argument("--gender")
    p.set_defaults(func=cmd_voice_anchors)

    p = voice_sub.add_parser("generate")
    p.add_argument("text")
    p.add_argument("anchor_key")
    p.add_argument("--source", default="CLI")
    p.set_defaults(func=cmd_voice_generate)

    p = voice_sub.add_parser("query")
    p.add_argument("task_id")
    p.set_defaults(func=cmd_voice_query)

    p = voice_sub.add_parser("upload")
    p.add_argument("file_path")
    p.add_argument("--name", default="voice.mp3")
    p.set_defaults(func=cmd_voice_upload)

    p = voice_sub.add_parser("add")
    p.add_argument("work_id")
    p.add_argument("voice_url")
    p.add_argument("--loop", type=int, default=1)
    p.add_argument("--volume", type=int, default=100)
    p.set_defaults(func=cmd_voice_add)

    # hotspot
    hotspot = subparsers.add_parser("hotspot", help="热点管理命令")
    hotspot_sub = hotspot.add_subparsers(dest="action")

    p = hotspot_sub.add_parser("list")
    p.add_argument("work_id", type=int)
    p.set_defaults(func=cmd_hotspot_list)

    p = hotspot_sub.add_parser("add-jump")
    p.add_argument("work_id", type=int)
    p.add_argument("from_scene_id")
    p.add_argument("to_scene_id")
    p.add_argument("--name")
    p.add_argument("--ath", type=int, default=0)
    p.add_argument("--atv", type=int, default=0)
    p.set_defaults(func=cmd_hotspot_add_jump)

    p = hotspot_sub.add_parser("add-text")
    p.add_argument("work_id", type=int)
    p.add_argument("scene_id")
    p.add_argument("name")
    p.add_argument("--ath", type=int, default=0)
    p.add_argument("--atv", type=int, default=0)
    p.set_defaults(func=cmd_hotspot_add_text)

    p = hotspot_sub.add_parser("delete")
    p.add_argument("work_id", type=int)
    p.add_argument("hotspot_id")
    p.set_defaults(func=cmd_hotspot_delete)

    # score
    score = subparsers.add_parser("score", help="评分管理命令")
    score_sub = score.add_subparsers(dest="action")

    p = score_sub.add_parser("get")
    p.add_argument("work_id")
    p.set_defaults(func=cmd_score_get)

    # develop
    develop = subparsers.add_parser("develop", help="开发指南命令")
    develop_sub = develop.add_subparsers(dest="action")

    p = develop_sub.add_parser("miniprogram")
    p.add_argument("--platform", default="wechat")
    p.add_argument("--feature", default="basic")
    p.set_defaults(func=cmd_develop_miniprogram)

    p = develop_sub.add_parser("web")
    p.add_argument("--framework", default="vue")
    p.set_defaults(func=cmd_develop_web)

    p = develop_sub.add_parser("existing")
    p.add_argument("--type", default="website")
    p.set_defaults(func=cmd_develop_existing)

    p = develop_sub.add_parser("code")
    p.add_argument("type")
    p.add_argument("--platform")
    p.add_argument("--framework")
    p.add_argument("--work-id")
    p.set_defaults(func=cmd_develop_code)

    # info
    info = subparsers.add_parser("info", help="信息命令")
    info_sub = info.add_subparsers(dest="action")

    p = info_sub.add_parser("version")
    p.set_defaults(func=cmd_info_version)

    p = info_sub.add_parser("context")
    p.set_defaults(func=cmd_info_context)

    # config
    p = subparsers.add_parser("config", help="配置管理")
    p.add_argument("--show", action="store_true")
    p.add_argument("--token")
    p.add_argument("--uid")
    p.set_defaults(func=cmd_config)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return 1

    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
