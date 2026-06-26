import os
import sys
import json
import base64
import argparse
import requests
import uuid
import time
import logging
import subprocess
import tempfile
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stderr)
logger = logging.getLogger(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))
skill_env_path = os.path.join(script_dir, '..', '.env')

# 加载 Skill 本地 .env 配置 / Load skill local .env config
# TTS/ASR 凭证（VOLC_APPID + VOLC_ACCESS_TOKEN）配置在 skills/.env 中
load_dotenv(skill_env_path, override=True)

# 从环境变量获取配置 / Read config from environment variables
# 语音服务凭证（来自 skills/.env）
APPID = os.getenv("VOLC_APPID", "")
ACCESS_TOKEN = os.getenv("VOLC_ACCESS_TOKEN", "")
RESOURCE_ID_TTS = os.getenv("VOLC_RESOURCE_ID", "seed-tts-1.0")
VOICE_TYPE = os.getenv("VOLC_VOICE_TYPE", "zh_female_sajiaonvyou_moon_bigtts")
RESOURCE_ID_ASR = os.getenv("VOLC_RESOURCE_ID_ASR", "volc.bigasr.auc")

TTS_URL = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"
ASR_SUBMIT_URL = "https://openspeech-direct.zijieapi.com/api/v3/auc/bigmodel/submit"
ASR_QUERY_URL = "https://openspeech-direct.zijieapi.com/api/v3/auc/bigmodel/query"


def is_safe_path(target_path):
    """
    检查路径是否安全，防止路径遍历漏洞 (Path Traversal)
    根据安全扫描反馈，移除了工作区根目录和用户 home 目录的访问权限，
    仅允许临时目录和指定的 OpenClaw media 目录。
    """
    try:
        abs_path = os.path.abspath(target_path)
        # 拒绝访问系统敏感目录
        restricted_dirs = ['/etc', '/bin', '/sbin', '/usr/bin', '/usr/sbin', '/dev', '/sys', '/proc']
        if any(abs_path.startswith(d + '/') or abs_path == d for d in restricted_dirs):
            return False
            
        # 严格限制：仅允许 /tmp、系统临时目录，以及 OpenClaw 媒体目录
        allowed_dirs = [
            '/tmp',
            tempfile.gettempdir(),
            '/tmp/openclaw/media/inbound',
            '/tmp/openclaw/voice-tts'
        ]
            
        return any(abs_path.startswith(d) for d in allowed_dirs)
    except Exception:
        return False


def check_config():
    """检查必要的环境变量配置 / Check required environment variables"""
    if not APPID or not ACCESS_TOKEN:
        logger.error("Error: 请在 skills/feishu-voice-chat/.env 中配置 VOLC_APPID 和 VOLC_ACCESS_TOKEN")
        logger.error("Error: Please configure VOLC_APPID and VOLC_ACCESS_TOKEN in skills/.env")
        sys.exit(1)


def get_tts_headers():
    """
    获取 TTS 请求头 / Get TTS request headers
    """
    return {
        "Content-Type": "application/json",
        "X-Api-App-Id": APPID,
        "X-Api-Access-Key": ACCESS_TOKEN,
        "X-Api-Resource-Id": RESOURCE_ID_TTS,
        "Connection": "keep-alive",
    }


def get_asr_headers(task_id):
    """
    获取 ASR 请求头 / Get ASR request headers
    """
    return {
        "X-Api-App-Key": APPID,
        "X-Api-Access-Key": ACCESS_TOKEN,
        "X-Api-Resource-Id": RESOURCE_ID_ASR,
        "X-Api-Request-Id": task_id,
        "X-Api-Sequence": "-1",
        "Content-Type": "application/json"
    }


def is_ogg_opus(file_path):
    """
    检测文件是否为有效的 OGG/Opus 格式 / Check if file is a valid OGG/Opus audio
    Returns True if file starts with OGG magic bytes (4f 67 67 53)
    """
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4)
            return header == b'OggS'
    except Exception:
        return False


def convert_to_ogg_opus(input_path, output_path):
    """
    使用 ffmpeg 将音频转换为 OGG/Opus 格式 / Convert audio to OGG/Opus using ffmpeg
    飞书语音消息需要 OGG 容器 + Opus 编码 / Feishu voice messages require OGG container + Opus encoding
    """
    try:
        cmd = [
            'ffmpeg', '-y', '-i', input_path,
            '-c:a', 'libopus', '-ar', '48000', '-ac', '1',
            '-f', 'ogg',
            output_path
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        if result.returncode == 0 and os.path.exists(output_path):
            logger.info(f"转换成功: {output_path}")
            return True
        else:
            logger.error(f"ffmpeg 转换失败: {result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        logger.error("ffmpeg 转换超时")
        return False
    except FileNotFoundError:
        logger.error("ffmpeg 未安装，请先安装: brew install ffmpeg")
        return False
    except Exception as e:
        logger.error(f"转换异常: {e}")
        return False


def tts(text, output_path):
    """
    火山引擎大模型语音合成 (TTS) V3 HTTP 单向流式
    输出 OGG/Opus 格式（适配飞书语音消息）/ Output OGG/Opus format (for Feishu voice messages)
    """
    check_config()
    
    if not is_safe_path(output_path):
        logger.error(f"Error: 不安全的输出路径 / Unsafe output path: {output_path}")
        sys.exit(1)

    headers = get_tts_headers()

    payload = {
        "user": {"uid": "openclaw_user"},
        "req_params": {
            "text": text,
            "speaker": VOICE_TYPE,
            "audio_params": {
                "format": "ogg",
                "sample_rate": 24000,
            },
            "additions": "{\"explicit_language\":\"zh\",\"disable_markdown_filter\":true}"
        },
    }

    logger.info(f"Starting TTS for text: {text[:20]}...")

    try:
        with requests.Session() as session:
            with session.post(TTS_URL, headers=headers, json=payload, stream=True, timeout=60) as resp:
                if resp.status_code != 200:
                    logger.error(f"TTS Error: HTTP {resp.status_code}, Body: {resp.text[:200]}")
                    sys.exit(1)

                audio_bytes = bytearray()

                for line in resp.iter_lines(decode_unicode=True):
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    code = int(data.get("code", 0))

                    if code == 0:
                        audio_b64 = data.get("data")
                        if audio_b64:
                            audio_bytes.extend(base64.b64decode(audio_b64))
                    elif code == 20000000:
                        break
                    else:
                        logger.error(f"TTS Error in stream: {data.get('message')} (code: {code})")
                        sys.exit(1)

                if len(audio_bytes) > 0:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as f:
                        temp_path = f.name
                        f.write(audio_bytes)
                    logger.info(f"原始音频保存到: {temp_path} ({len(audio_bytes)} bytes)")

                    if is_ogg_opus(temp_path):
                        os.rename(temp_path, output_path)
                        logger.info(f"Success: Audio saved to {output_path} (OGG format)")
                    else:
                        logger.warning(f"收到的音频不是 OGG 格式，开始转换... (Not OGG format, converting...)")
                        if convert_to_ogg_opus(temp_path, output_path):
                            os.remove(temp_path)
                            logger.info(f"Success: Audio converted and saved to {output_path}")
                        else:
                            logger.warning(f"转换失败，保留原始文件: {temp_path}")
                            os.rename(temp_path, output_path)

                    print(json.dumps({"status": "success", "file_path": output_path}))
                else:
                    logger.error("TTS Error: 未接收到音频数据")
                    sys.exit(1)

    except Exception as e:
        logger.error(f"TTS Request Exception: {str(e)}")
        sys.exit(1)


def asr(audio_path):
    """
    火山引擎大模型录音文件识别 (ASR) V3 (Submit/Query 模式)
    支持 ogg、opus、mp3、wav 格式 / Supports ogg, opus, mp3, wav formats
    """
    check_config()

    if not is_safe_path(audio_path):
        logger.error(f"Error: 不安全的输入路径 / Unsafe input path: {audio_path}")
        sys.exit(1)

    if not os.path.exists(audio_path):
        logger.error(f"Error: 音频文件 {audio_path} 不存在")
        sys.exit(1)

    try:
        with open(audio_path, "rb") as f:
            audio_data = f.read()
    except Exception as e:
        logger.error(f"Error: 读取音频文件失败: {e}")
        sys.exit(1)

    task_id = str(uuid.uuid4())
    headers = get_asr_headers(task_id)

    ext = audio_path.split('.')[-1].lower()
    audio_format = ext if ext in ['wav', 'mp3', 'ogg', 'opus'] else 'wav'
    logger.info(f"检测到音频格式 / Detected audio format: {audio_format} (extension: .{ext})")

    request_payload = {
        "user": {
            "uid": "openclaw_user"
        },
        "audio": {
            "format": audio_format,
            "data": base64.b64encode(audio_data).decode('utf-8')
        },
        "request": {
            "model_name": "bigmodel",
            "enable_channel_split": True,
            "enable_ddc": True,
            "enable_speaker_info": True,
            "enable_punc": True,
            "enable_itn": True,
            "corpus": {
                "correct_table_name": "",
                "context": ""
            }
        }
    }

    logger.info(f"Starting ASR for file: {audio_path}, Task ID: {task_id}")
    logger.info(f"音频大小 / Audio size: {len(audio_data)} bytes, 格式 / format: {audio_format}")

    try:
        response = requests.post(ASR_SUBMIT_URL, data=json.dumps(request_payload), headers=headers)
        
        x_tt_logid = ""
        if 'X-Api-Status-Code' in response.headers and response.headers["X-Api-Status-Code"] == "20000000":
            x_tt_logid = response.headers.get("X-Tt-Logid", "")
            logger.info(f"ASR Task Submitted. LogID: {x_tt_logid}")
        else:
            logger.error(f"Submit task failed. HTTP Status: {response.status_code}")
            logger.error(f"Response headers: {response.headers}")
            logger.error(f"Response body: {response.text}")
            sys.exit(1)

        query_headers = {
            "X-Api-App-Key": APPID,
            "X-Api-Access-Key": ACCESS_TOKEN,
            "X-Api-Resource-Id": RESOURCE_ID_ASR,
            "X-Api-Request-Id": task_id,
            "Content-Type": "application/json"
        }
        
        # 只在有 x_tt_logid 时添加到 header
        if x_tt_logid:
            query_headers["X-Tt-Logid"] = x_tt_logid

        for i in range(120):
            query_response = requests.post(ASR_QUERY_URL, data=json.dumps({}), headers=query_headers)

            if 'X-Api-Status-Code' in query_response.headers:
                code = query_response.headers["X-Api-Status-Code"]
                if code == '20000000':
                    res_json = query_response.json()

                    text = ""
                    result_data = res_json.get("result", {})
                    if isinstance(result_data, dict):
                        text = result_data.get("text", "")
                    elif isinstance(result_data, list) and len(result_data) > 0:
                        text = result_data[0].get("text", "")

                    logger.info("ASR Success")
                    print(json.dumps({"status": "success", "text": text}))
                    return text
                elif code in ['20000001', '20000002']:
                    time.sleep(0.5)
                    continue
                else:
                    err_msg = query_response.headers.get('X-Api-Message', 'Unknown error')
                    logger.error(f"ASR Task Failed! Status Code: {code}, Message: {err_msg}")
                    logger.error(f"提示 / Hint: 如果是格式错误，请确认音频文件是 ogg/opus/mp3/wav 格式且未损坏")
                    sys.exit(1)
            else:
                logger.error(f"Query task failed. HTTP Status: {query_response.status_code}")
                logger.error(f"Response headers: {query_response.headers}")
                logger.error(f"Response body: {query_response.text}")
                sys.exit(1)

            time.sleep(1)

        logger.error("ASR Timeout!")
        sys.exit(1)

    except Exception as e:
        logger.error(f"ASR Request Exception: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="火山引擎 ASR/TTS 工具")
    subparsers = parser.add_subparsers(dest="command", help="支持的命令")

    asr_parser = subparsers.add_parser("asr", help="语音识别")
    asr_parser.add_argument("audio_path", help="音频文件路径")

    tts_parser = subparsers.add_parser("tts", help="语音合成")
    tts_parser.add_argument("text", help="要合成的文本")
    tts_parser.add_argument("output_path", help="输出音频文件路径")

    args = parser.parse_args()

    if args.command == "asr":
        asr(args.audio_path)
    elif args.command == "tts":
        tts(args.text, args.output_path)
    else:
        parser.print_help()
