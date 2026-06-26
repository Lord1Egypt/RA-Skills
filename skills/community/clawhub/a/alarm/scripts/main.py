from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from zoneinfo import ZoneInfo

from asr import SenseAudioASR
from config import get_optional
from feishu_api import FeishuClient
from reminder_store import ReminderStore
from time_parser import analyze_message


def parse_now(now_text: str | None, tz_name: str) -> datetime:
    tz = ZoneInfo(tz_name)
    if not now_text:
        return datetime.now(tz)
    dt = datetime.fromisoformat(now_text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz)
    return dt.astimezone(tz)


def get_store() -> ReminderStore:
    db_path = get_optional('FEISHU_SMART_ALARM_DB', './data/reminders.db')
    return ReminderStore(db_path)


def build_analysis_result(parsed) -> dict:
    return {
        'need_reminder': parsed.need_reminder,
        'reason': parsed.reason,
        'deadline_iso': parsed.deadline_dt.isoformat() if parsed.deadline_dt else None,
        'reminder_iso': parsed.reminder_dt.isoformat() if parsed.reminder_dt else None,
        'lead_minutes': parsed.lead_minutes,
        'deadline_text': parsed.deadline_text,
        'summary': parsed.summary,
        'confirm_text': parsed.confirm_text,
        'reminder_text': parsed.reminder_text,
    }


def analyze_text_payload(text: str, sender_name: str, now_text: str) -> dict:
    tz_name = get_optional('FEISHU_SMART_ALARM_TZ', 'Asia/Shanghai')
    now = parse_now(now_text, tz_name)
    parsed = analyze_message(text, now, tz_name, sender_name)
    return build_analysis_result(parsed)


def cmd_analyze_message(args: argparse.Namespace) -> dict:
    result = analyze_text_payload(args.text, args.sender_name, args.now)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def cmd_transcribe_audio(args: argparse.Namespace) -> dict:
    raw = SenseAudioASR().transcribe(args.audio, language=args.language)
    result = {
        'ok': True,
        'audio_path': args.audio,
        'transcript': (raw.get('text') or '').strip(),
        'raw': raw,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def cmd_analyze_audio(args: argparse.Namespace) -> dict:
    raw = SenseAudioASR().transcribe(args.audio, language=args.language)
    transcript = (raw.get('text') or '').strip()
    result = analyze_text_payload(transcript, args.sender_name, args.now)
    result.update({
        'audio_path': args.audio,
        'transcript': transcript,
        'asr_model': get_optional('SENSEAUDIO_ASR_MODEL', 'sense-asr'),
        'analysis_source': 'audio',
    })
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def create_reminder_from_text(
    *,
    text: str,
    receive_id: str,
    receive_id_type: str,
    sender_open_id: str,
    sender_name: str,
    message_id: str,
    no_confirm: bool,
    now_text: str,
    source_type: str,
    source_audio_path: str = '',
    transcript_raw: dict | None = None,
) -> dict:
    tz_name = get_optional('FEISHU_SMART_ALARM_TZ', 'Asia/Shanghai')
    now = parse_now(now_text, tz_name)
    parsed = analyze_message(text, now, tz_name, sender_name)
    result = build_analysis_result(parsed)
    result.update({
        'reminder_id': None,
        'confirmation_sent': False,
        'source_type': source_type,
        'source_audio_path': source_audio_path or None,
        'transcript': text if source_type == 'audio' else None,
    })
    if not parsed.need_reminder:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result

    extra_payload = {
        'message_id': message_id,
        'source_type': source_type,
        'source_audio_path': source_audio_path or None,
    }
    if transcript_raw is not None:
        extra_payload['asr_raw'] = transcript_raw

    store = get_store()
    reminder_id = store.add({
        'source_text': text,
        'summary': parsed.summary,
        'receive_id': receive_id,
        'receive_id_type': receive_id_type,
        'sender_open_id': sender_open_id,
        'sender_name': sender_name,
        'deadline_iso': parsed.deadline_dt.isoformat(),
        'reminder_iso': parsed.reminder_dt.isoformat(),
        'confirm_text': parsed.confirm_text,
        'reminder_text': parsed.reminder_text,
        'created_at': now.isoformat(),
        'extra_json': json.dumps(extra_payload, ensure_ascii=False),
    })
    result['reminder_id'] = reminder_id

    if not no_confirm:
        client = FeishuClient()
        client.send_text_message(
            receive_id=receive_id,
            receive_id_type=receive_id_type,
            text=parsed.confirm_text,
        )
        result['confirmation_sent'] = True

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def cmd_create_reminder(args: argparse.Namespace) -> dict:
    return create_reminder_from_text(
        text=args.text,
        receive_id=args.receive_id,
        receive_id_type=args.receive_id_type,
        sender_open_id=args.sender_open_id,
        sender_name=args.sender_name,
        message_id=args.message_id,
        no_confirm=args.no_confirm,
        now_text=args.now,
        source_type='text',
    )


def cmd_create_reminder_audio(args: argparse.Namespace) -> dict:
    raw = SenseAudioASR().transcribe(args.audio, language=args.language)
    transcript = (raw.get('text') or '').strip()
    return create_reminder_from_text(
        text=transcript,
        receive_id=args.receive_id,
        receive_id_type=args.receive_id_type,
        sender_open_id=args.sender_open_id,
        sender_name=args.sender_name,
        message_id=args.message_id,
        no_confirm=args.no_confirm,
        now_text=args.now,
        source_type='audio',
        source_audio_path=args.audio,
        transcript_raw=raw,
    )


def cmd_poll_due(args: argparse.Namespace) -> dict:
    tz_name = get_optional('FEISHU_SMART_ALARM_TZ', 'Asia/Shanghai')
    now = parse_now(args.now, tz_name)
    store = get_store()
    due_items = store.list_due(now.isoformat())
    client = FeishuClient()
    sent_ids: list[int] = []
    for item in due_items:
        client.send_text_message(
            receive_id=item.receive_id,
            receive_id_type=item.receive_id_type,
            text=item.reminder_text,
        )
        store.mark_sent(item.id, now.isoformat())
        sent_ids.append(item.id)
    result = {'now': now.isoformat(), 'checked': len(due_items), 'sent_ids': sent_ids}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def cmd_run_loop(args: argparse.Namespace) -> dict:
    interval = max(5, int(args.interval))
    while True:
        try:
            cmd_poll_due(argparse.Namespace(now=None))
        except Exception as exc:  # pragma: no cover
            print(json.dumps({'error': str(exc)}, ensure_ascii=False))
        time.sleep(interval)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='feishu smart alarm skill')
    sub = parser.add_subparsers(dest='command', required=True)

    p1 = sub.add_parser('analyze-message', help='分析文本消息是否需要建立提醒')
    p1.add_argument('--text', required=True, help='飞书消息文本')
    p1.add_argument('--sender-name', default='', help='发送者名称，可选')
    p1.add_argument('--now', default='', help='当前时间，ISO 格式，可选')
    p1.set_defaults(func=cmd_analyze_message)

    p2 = sub.add_parser('transcribe-audio', help='先做 ASR，把语音转成文本')
    p2.add_argument('--audio', required=True, help='本地音频文件路径')
    p2.add_argument('--language', default='zh', help='ASR 语言，默认 zh')
    p2.set_defaults(func=cmd_transcribe_audio)

    p3 = sub.add_parser('analyze-audio', help='先做 ASR，再分析语音中是否需要建立提醒')
    p3.add_argument('--audio', required=True, help='本地音频文件路径')
    p3.add_argument('--sender-name', default='', help='发送者名称，可选')
    p3.add_argument('--now', default='', help='当前时间，ISO 格式，可选')
    p3.add_argument('--language', default='zh', help='ASR 语言，默认 zh')
    p3.set_defaults(func=cmd_analyze_audio)

    p4 = sub.add_parser('create-reminder', help='根据文本建立提醒并发送确认消息')
    p4.add_argument('--text', required=True, help='飞书消息文本')
    p4.add_argument('--receive-id', required=True, help='原飞书会话的 receive_id')
    p4.add_argument('--receive-id-type', default='chat_id', help='chat_id 或 open_id')
    p4.add_argument('--sender-open-id', default='', help='原消息发送者 open_id，可选')
    p4.add_argument('--sender-name', default='', help='原消息发送者名称，可选')
    p4.add_argument('--message-id', default='', help='原消息 ID，可选')
    p4.add_argument('--no-confirm', action='store_true', help='只建提醒，不发送确认消息')
    p4.add_argument('--now', default='', help='当前时间，ISO 格式，可选')
    p4.set_defaults(func=cmd_create_reminder)

    p5 = sub.add_parser('create-reminder-audio', help='先做 ASR，再根据语音内容建立提醒并发送确认消息')
    p5.add_argument('--audio', required=True, help='本地音频文件路径')
    p5.add_argument('--receive-id', required=True, help='原飞书会话的 receive_id')
    p5.add_argument('--receive-id-type', default='chat_id', help='chat_id 或 open_id')
    p5.add_argument('--sender-open-id', default='', help='原消息发送者 open_id，可选')
    p5.add_argument('--sender-name', default='', help='原消息发送者名称，可选')
    p5.add_argument('--message-id', default='', help='原消息 ID，可选')
    p5.add_argument('--no-confirm', action='store_true', help='只建提醒，不发送确认消息')
    p5.add_argument('--now', default='', help='当前时间，ISO 格式，可选')
    p5.add_argument('--language', default='zh', help='ASR 语言，默认 zh')
    p5.set_defaults(func=cmd_create_reminder_audio)

    p6 = sub.add_parser('poll-due', help='轮询并发送到期提醒')
    p6.add_argument('--now', default='', help='当前时间，ISO 格式，可选')
    p6.set_defaults(func=cmd_poll_due)

    p7 = sub.add_parser('run-loop', help='以循环方式常驻轮询')
    p7.add_argument('--interval', default='30', help='轮询间隔秒数，默认 30')
    p7.set_defaults(func=cmd_run_loop)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
