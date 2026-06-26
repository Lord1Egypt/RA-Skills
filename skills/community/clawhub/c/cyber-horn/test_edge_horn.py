"""
CyberHorn Edge TTS 最小化闭环测试。
1. 使用 Edge TTS 生成 test_edge.mp3
2. 使用 FFmpeg 转为 test_edge.opus
3. 可选：发送到飞书并删除本地测试文件

用法:
  python test_edge_horn.py                    # 仅 TTS + 转码，产出 test_edge.mp3 / test_edge.opus
  python test_edge_horn.py --feishu CHAT_ID   # 再上传并发送到飞书（会删除本地测试文件）

TTS_PROVIDER 默认为 EDGE，如已显式设置为其他值，请确保为 EDGE。
"""
import argparse
import sys
from pathlib import Path

# 测试产出文件名（当前目录）
TEST_MP3 = Path("test_edge.mp3")
TEST_OPUS = Path("test_edge.opus")


def main() -> int:
    parser = argparse.ArgumentParser(description="CyberHorn Edge TTS 闭环测试")
    parser.add_argument("--feishu", metavar="CHAT_ID", help="发送到飞书（需配置 .env）")
    parser.add_argument("--text", default="这是一条来自 Edge TTS 的测试语音，来自赛博小喇叭。", help="TTS 文本")
    args = parser.parse_args()

    from config import check_env, get_edge_config, get_feishu_config, get_tts_provider
    from audio_engine import edge_tts_to_mp3, mp3_to_opus_16000
    from feishu_client import get_tenant_access_token, upload_audio, send_audio_message

    check_env()

    provider = get_tts_provider()
    if provider != "EDGE":
        print(f"[Test] 当前 TTS_PROVIDER={provider!r}，本测试脚本仅用于验证 Edge TTS。", file=sys.stderr)
        print("       请在 .env 中将 TTS_PROVIDER 设置为 EDGE 后重试。", file=sys.stderr)
        return 1

    edge = get_edge_config()

    # 1) Edge TTS → test_edge.mp3
    print("[Test] Edge TTS 生成 MP3...")
    try:
        edge_tts_to_mp3(args.text, edge["voice"], TEST_MP3)
    except Exception as e:
        print(f"[Test] Edge TTS 失败: {e}", file=sys.stderr)
        return 1
    if not TEST_MP3.exists():
        print("[Test] 未生成 test_edge.mp3", file=sys.stderr)
        return 1
    print(f"[Test] 已生成 {TEST_MP3}")

    # 2) FFmpeg → test_edge.opus
    print("[Test] FFmpeg 转 Opus...")
    try:
        mp3_to_opus_16000(TEST_MP3, TEST_OPUS)
    except Exception as e:
        print(f"[Test] FFmpeg 失败: {e}", file=sys.stderr)
        return 1
    if not TEST_OPUS.exists():
        print("[Test] 未生成 test_edge.opus", file=sys.stderr)
        return 1
    print(f"[Test] 已生成 {TEST_OPUS}，可用 VLC 等播放验证。")

    # 3) 可选：飞书上传并发送
    if args.feishu:
        print("[Test] 上传并发送到飞书...")
        feishu = get_feishu_config()
        try:
            token = get_tenant_access_token(feishu["app_id"], feishu["app_secret"])
            file_key = upload_audio(token, TEST_OPUS)
            send_audio_message(token, args.feishu, file_key, receive_id_type="chat_id")
            print("[Test] 飞书已发送，请在手机端查看绿色语音条。")
        except Exception as e:
            print(f"[Test] 飞书失败: {e}", file=sys.stderr)
            return 1
        # 测试结束删除本地测试文件
        for f in (TEST_MP3, TEST_OPUS):
            if f.exists():
                f.unlink()
                print(f"[Test] 已删除 {f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

