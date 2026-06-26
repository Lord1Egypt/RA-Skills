"""
CyberHorn (赛博小喇叭) 入口。
支持 CLI: python main.py "测试语音内容" "YOUR_CHAT_ID"
OpenClaw 可通过环境变量 + 命令行参数调用。
TTS 引擎可通过 .env 中的 TTS_PROVIDER 配置，默认 EDGE，可选 ELEVEN。
"""
import sys
from pathlib import Path

from config import check_env, get_env, get_feishu_config, load_env
from audio_engine import text_to_opus_file
from feishu_client import get_tenant_access_token, upload_audio, send_audio_message


def run_horn(text: str, chat_id: str, receive_id_type: str = "chat_id") -> None:
    """完整流程：TTS → Opus → 上传飞书 → 发送语音。临时文件会在结束后删除。"""
    check_env()
    feishu = get_feishu_config()

    mp3_path = None
    opus_path = None
    try:
        mp3_path, opus_path = text_to_opus_file(text)
        token = get_tenant_access_token(feishu["app_id"], feishu["app_secret"])
        file_key = upload_audio(token, opus_path)
        send_audio_message(token, chat_id, file_key, receive_id_type=receive_id_type)
        print("[CyberHorn] 语音已发送到飞书。")
    except Exception as e:
        # 打印具体错误，便于排查余额、权限等
        print(f"[CyberHorn] 错误: {e}", file=sys.stderr)
        raise
    finally:
        # 清理临时文件
        for p in (opus_path, mp3_path):
            if p and isinstance(p, Path) and p.exists():
                try:
                    p.unlink()
                except OSError:
                    pass


def main() -> int:
    # 确保在读取环境变量前加载 .env
    load_env()
    if len(sys.argv) < 2:
        print(
            "用法: python main.py \"<语音内容>\" \"[CHAT_ID]\" [receive_id_type=chat_id]\n"
            "若未传 CHAT_ID，则会尝试从环境变量 FEISHU_DEFAULT_CHAT_ID 读取。",
            file=sys.stderr,
        )
        return 1

    text = sys.argv[1]
    # 优先使用命令行传入的 CHAT_ID，否则从 .env / 环境中的 FEISHU_DEFAULT_CHAT_ID 读取
    chat_id = sys.argv[2] if len(sys.argv) > 2 else get_env("FEISHU_DEFAULT_CHAT_ID")
    receive_id_type = sys.argv[3] if len(sys.argv) > 3 else "chat_id"

    if not text:
        print("语音内容不能为空。", file=sys.stderr)
        return 1
    if not chat_id:
        print(
            "CHAT_ID 未提供，且环境变量 FEISHU_DEFAULT_CHAT_ID 也未配置。",
            file=sys.stderr,
        )
        return 1
    run_horn(text, chat_id, receive_id_type)
    return 0


if __name__ == "__main__":
    sys.exit(main())
