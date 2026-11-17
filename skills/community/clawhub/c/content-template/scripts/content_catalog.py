import json
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stdin.encoding != "utf-8":
    sys.stdin.reconfigure(encoding="utf-8")

CATEGORIES = [
    {
        "name": "网文小说",
        "formats": ["article"],
        "platforms": ["番茄", "起点"],
        "skill": "inkos",
        "how_to": "inkos init → inkos book create --brief 创意简报.md → inkos write next 书名"
    },
    {
        "name": "古诗文故事(图文+短视频)",
        "formats": ["article", "short_video"],
        "platforms": ["小红书", "知乎", "公众号", "抖音", "快手", "视频号", "B站"],
        "skill": "poetry-weaver",
        "how_to": "poetry-weaver(character=人物, poem_title=诗名, mode=dual_character, output_format=article|short_video, narrator=none|voiceover)"
    },
    {
        "name": "论语vs抡语(图文+短视频)",
        "formats": ["article", "short_video"],
        "platforms": ["小红书", "知乎", "抖音", "快手", "视频号"],
        "skill": "poetry-weaver",
        "how_to": "poetry-weaver(character=孔子, mode=contrast, output_format=article|short_video, narrator=none|voiceover)"
    },
    {
        "name": "打油诗改编(图文+短视频)",
        "formats": ["article", "short_video"],
        "platforms": ["小红书", "抖音图文", "抖音", "快手"],
        "skill": "poetry-weaver",
        "how_to": "poetry-weaver(character=人物, mode=parody, output_format=article|short_video, narrator=none|voiceover)"
    },
    {
        "name": "企业GEO宣传",
        "formats": ["article"],
        "platforms": ["百度", "公众号"],
        "skill": "geo-content-optimizer",
        "how_to": "geo-content-optimizer(action=optimize, content=企业内容)"
    },
    {
        "name": "知识卡片/课件(图文+短视频)",
        "formats": ["article", "short_video"],
        "platforms": ["小红书", "公众号", "抖音", "快手", "视频号"],
        "skill": "visual-content-generator+poetry-weaver",
        "how_to": "图文: visual-content-generator(archetype=知识卡片) | 短视频: poetry-weaver(mode=blend, output_format=short_video)"
    },
    {
        "name": "商品图/封面",
        "formats": ["article"],
        "platforms": ["闲鱼", "电商"],
        "skill": "flux/kolors",
        "how_to": "flux(action=generate, prompt=描述) 或 kolors(action=generate, scene=场景)"
    },
    {
        "name": "营销短视频",
        "formats": ["short_video"],
        "platforms": ["抖音", "快手", "B站"],
        "skill": "video-generator",
        "how_to": "video-generator(action=generate, topic=主题)"
    },
    {
        "name": "口型同步/数字人",
        "formats": ["short_video"],
        "platforms": ["抖音", "视频号"],
        "skill": "flyworks-lip-sync",
        "how_to": "flyworks-lip-sync(action=generate, image=人物图, text=台词)"
    },
    {
        "name": "小说解说视频",
        "formats": ["short_video"],
        "platforms": ["抖音", "B站"],
        "skill": "inkos+novel-to-script+video-generator",
        "how_to": "inkos write next → novel-to-script → video-generator"
    },
    {
        "name": "角色一致性漫画/配图",
        "formats": ["article"],
        "platforms": ["小红书", "知乎", "公众号"],
        "skill": "character-consistency-mcp",
        "how_to": "character-consistency-mcp.generate_consistent_characters(character_description=描述, scene_descriptions=场景列表, style=虾仁画风)"
    },
    {
        "name": "漫画分格生成",
        "formats": ["article"],
        "platforms": ["小红书", "知乎", "公众号"],
        "skill": "character-consistency-mcp",
        "how_to": "character-consistency-mcp.generate_comic_panel(character_description=描述, dialogue=对话JSON, scene_description=场景, style=虾仁画风)"
    },
    {
        "name": "小说解说脚本",
        "formats": ["short_video"],
        "platforms": ["抖音", "B站", "快手"],
        "skill": "narrato-mcp",
        "how_to": "narrato-mcp.generate_narration_script(story_text=小说文本, style=幽默解说, target_duration=60s)"
    },
    {
        "name": "短剧剧本生成",
        "formats": ["short_video"],
        "platforms": ["抖音", "快手", "视频号"],
        "skill": "narrato-mcp",
        "how_to": "narrato-mcp.generate_short_drama_script(novel_text=小说文本, genre=搞笑, episodes=1)"
    },
    {
        "name": "TTS语音合成",
        "formats": ["audio"],
        "platforms": ["全平台配音"],
        "skill": "cosyvoice",
        "how_to": "cosyvoice(action=synthesize, text=文本, emotion=情感)"
    },
    {
        "name": "语音克隆",
        "formats": ["audio"],
        "platforms": ["闲鱼", "内容配音"],
        "skill": "gpt-sovits",
        "how_to": "gpt-sovits(action=clone_and_speak, reference_audio=参考音频, text=文本)"
    },
]


def list_categories(filter_format: str = "all", filter_platform: str = "all") -> dict:
    results = CATEGORIES
    if filter_format and filter_format != "all":
        results = [c for c in results if filter_format in c["formats"]]
    if filter_platform and filter_platform != "all":
        results = [c for c in results if any(filter_platform in p for p in c["platforms"])]
    return {"success": True, "data": {"categories": results, "total": len(results)}}


def format_as_text(data: dict) -> str:
    categories = data["data"]["categories"]
    lines = [f"📋 JueJin内容生成目录 (共{data['data']['total']}个品类)\n"]
    article_cats = [c for c in categories if "article" in c["formats"]]
    video_cats = [c for c in categories if "short_video" in c["formats"]]
    audio_cats = [c for c in categories if "audio" in c["formats"]]
    if article_cats:
        lines.append("📝 图文内容:")
        for c in article_cats:
            platforms = "、".join(c["platforms"])
            lines.append(f"  • {c['name']} → {platforms}")
            lines.append(f"    生成: {c['how_to']}")
    if video_cats:
        lines.append("\n🎬 短视频内容:")
        for c in video_cats:
            platforms = "、".join(c["platforms"])
            lines.append(f"  • {c['name']} → {platforms}")
            lines.append(f"    生成: {c['how_to']}")
    if audio_cats:
        lines.append("\n🔊 音频内容:")
        for c in audio_cats:
            platforms = "、".join(c["platforms"])
            lines.append(f"  • {c['name']} → {platforms}")
            lines.append(f"    生成: {c['how_to']}")
    return "\n".join(lines)


def main():
    try:
        raw = sys.stdin.read()
        args = json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, EOFError):
        args = {}
    action = args.get("action", "list")
    if action == "list":
        result = list_categories(
            filter_format=args.get("filter_format", "all"),
            filter_platform=args.get("filter_platform", "all"),
        )
    else:
        result = {"success": False, "error": f"未知action: {action}", "code": "INVALID_ACTION"}
    text_output = format_as_text(result)
    result["data"]["text_output"] = text_output
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
