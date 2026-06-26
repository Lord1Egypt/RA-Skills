#!/usr/bin/env python3
"""
创建视频合成任务（数字人驱动）。与 chanjing-credentials-guard 使用同一配置文件获取 Token。
用法:
  TTS 驱动:
    create_video.py --person-id <id> --person-x 0 --person-y 480 --person-width 1080 --person-height 1440 \
      --text "台词" --audio-man <声音id> [--model 2] [--bg-color "#EDEDED"]
  音频驱动:
    create_video.py --person-id <id> ... --audio-type audio --audio-file-id <id>
    create_video.py --person-id <id> ... --audio-type audio --wav-url "https://example.com/a.mp3"
--model: 0=基础版(1蝉豆/秒); 1=高质版(2蝉豆/秒); 2=卡通形象专用(3蝉豆/秒，素材须为卡通形象)。默认 0。
输出: 视频任务 id（一行）或错误到 stderr
"""
import argparse
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _auth import resolve_chanjing_access_token

API_BASE = __import__("os").environ.get("CHANJING_API_BASE", "https://open-api.chanjing.cc")


def main():
    parser = argparse.ArgumentParser(description="创建视频合成任务（数字人驱动）")
    # person
    parser.add_argument("--person-id", required=True, help="数字人形象 ID")
    parser.add_argument("--person-x", type=int, default=0, help="数字人 x 坐标")
    parser.add_argument("--person-y", type=int, default=0, help="数字人 y 坐标")
    parser.add_argument("--person-width", type=int, default=1080, help="数字人显示宽度")
    parser.add_argument("--person-height", type=int, default=1920, help="数字人显示高度")
    parser.add_argument("--figure-type", help="公共数字人形态，如 whole_body / sit_body（仅公共数字人需传）")
    parser.add_argument("--drive-mode", default="", help="驱动模式：空=正常顺序，random=随机帧")
    parser.add_argument("--is-rgba-mode", action="store_true", help="输出四通道 webm（需 webm 定制数字人）")
    parser.add_argument("--backway", type=int, default=1, help="末尾播放：1 正放（默认），2 倒放")
    # audio
    parser.add_argument("--audio-type", default="tts", choices=["tts", "audio"], help="tts=文本驱动，audio=音频驱动")
    parser.add_argument("--text", help="TTS 文本（audio-type=tts 时必填）")
    parser.add_argument("--audio-man", help="声音 ID（TTS 时必填）")
    parser.add_argument("--speed", type=float, default=1, help="TTS 语速 0.5-2，默认 1")
    parser.add_argument("--pitch", type=float, help="TTS 音调")
    parser.add_argument("--audio-file-id", help="音频 file_id（audio 驱动时可选）")
    parser.add_argument("--wav-url", help="音频文件 URL（audio 驱动时可选）")
    parser.add_argument("--volume", type=int, default=100, help="音量，默认 100")
    parser.add_argument("--language", default="cn", help="语言，默认 cn")
    # screen
    parser.add_argument("--screen-width", type=int, default=1080, help="屏幕宽度，默认 1080")
    parser.add_argument("--screen-height", type=int, default=1920, help="屏幕高度，默认 1920")
    # background
    parser.add_argument("--bg-color", help="背景颜色，如 #EDEDED")
    parser.add_argument("--bg-src-url", help="背景图片 URL（仅 jpg/png）")
    parser.add_argument("--bg-file-id", help="背景素材 file_id")
    # subtitle
    parser.add_argument("--subtitle-show", action="store_true", help="显示字幕")
    parser.add_argument("--subtitle-font-size", type=int, help="字幕字体大小")
    parser.add_argument("--subtitle-color", help="字幕颜色 #RRGGBB")
    # model & misc
    parser.add_argument("--model", type=int, default=0, choices=[0, 1, 2], help="0=基础; 1=高质 Pro; 2=卡通专用（素材须为卡通）")
    parser.add_argument("--callback", help="任务完成回调 URL")
    parser.add_argument("--add-compliance-watermark", action="store_true", help="添加 AI 合规水印")
    parser.add_argument("--watermark-position", type=int, choices=[0, 1, 2, 3], help="水印位置：0左上 1右上 2左下 3右下")
    parser.add_argument("--resolution-rate", type=int, default=0, choices=[0, 1], help="0=1080p, 1=4K")
    args = parser.parse_args()

    person = {
        "id": args.person_id,
        "x": args.person_x,
        "y": args.person_y,
        "width": args.person_width,
        "height": args.person_height,
    }
    if args.figure_type:
        person["figure_type"] = args.figure_type
    if args.drive_mode:
        person["drive_mode"] = args.drive_mode
    if args.is_rgba_mode:
        person["is_rgba_mode"] = True
    if args.backway != 1:
        person["backway"] = args.backway

    audio = {
        "type": args.audio_type,
        "volume": args.volume,
        "language": args.language,
    }
    if args.audio_type == "tts":
        if not args.text or not args.audio_man:
            print("TTS 模式需指定 --text 和 --audio-man", file=sys.stderr)
            sys.exit(1)
        tts = {"text": [args.text], "speed": args.speed, "audio_man": args.audio_man}
        if args.pitch is not None:
            tts["pitch"] = args.pitch
        audio["tts"] = tts
    else:
        if not args.audio_file_id and not args.wav_url:
            print("音频模式需指定 --audio-file-id 或 --wav-url", file=sys.stderr)
            sys.exit(1)
        if args.audio_file_id:
            audio["file_id"] = args.audio_file_id
        if args.wav_url:
            audio["wav_url"] = args.wav_url

    body = {
        "person": person,
        "audio": audio,
        "screen_width": args.screen_width,
        "screen_height": args.screen_height,
        "model": args.model,
    }
    if args.bg_color:
        body["bg_color"] = args.bg_color
    if args.bg_src_url or args.bg_file_id:
        bg = {}
        if args.bg_src_url:
            bg["src_url"] = args.bg_src_url
        if args.bg_file_id:
            bg["file_id"] = args.bg_file_id
        body["bg"] = bg
    if args.subtitle_show:
        sc = {"show": True}
        if args.subtitle_font_size:
            sc["font_size"] = args.subtitle_font_size
        if args.subtitle_color:
            sc["color"] = args.subtitle_color
        body["subtitle_config"] = sc
    if args.callback:
        body["callback"] = args.callback
    if args.add_compliance_watermark:
        body["add_compliance_watermark"] = True
    if args.watermark_position is not None:
        body["compliance_watermark_position"] = args.watermark_position
    if args.resolution_rate != 0:
        body["resolution_rate"] = args.resolution_rate

    token, err = resolve_chanjing_access_token()
    if err:
        print(err, file=sys.stderr)
        sys.exit(1)

    url = f"{API_BASE}/open/v1/create_video"
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"access_token": token, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode("utf-8"))

    if res.get("code") != 0:
        print(res.get("msg", res), file=sys.stderr)
        sys.exit(1)

    video_id = res.get("data")
    if not video_id:
        print("响应无 data", file=sys.stderr)
        sys.exit(1)
    print(video_id)


if __name__ == "__main__":
    main()
