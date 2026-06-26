#!/usr/bin/env python3
import json
import sqlite3
import time
from pathlib import Path

DB_PATH = Path('/root/.openclaw/workspace-dev/skills/feishu-card-sender/tmp/card_snapshots.db')


def _conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(str(DB_PATH))
    c.execute(
        '''CREATE TABLE IF NOT EXISTS card_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at INTEGER NOT NULL,
            card_key TEXT,
            message_id TEXT,
            receive_id TEXT,
            account_id TEXT,
            media_type TEXT,
            tmdb_id TEXT,
            title TEXT,
            raw_card_json TEXT NOT NULL
        )'''
    )
    try:
        c.execute('ALTER TABLE card_snapshots ADD COLUMN card_key TEXT')
    except Exception:
        pass
    try:
        c.execute('ALTER TABLE card_snapshots ADD COLUMN message_id TEXT')
    except Exception:
        pass
    c.execute('CREATE INDEX IF NOT EXISTS idx_snap_lookup ON card_snapshots(receive_id, media_type, tmdb_id, created_at DESC)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_snap_card_key ON card_snapshots(card_key, created_at DESC)')
    return c


def save_snapshot(*, card_key: str | None, message_id: str | None, receive_id: str, account_id: str | None, media_type: str | None, tmdb_id: str | None, title: str | None, raw_card_json: str):
    conn = _conn()
    try:
        conn.execute(
            'INSERT INTO card_snapshots(created_at, card_key, message_id, receive_id, account_id, media_type, tmdb_id, title, raw_card_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (int(time.time()), card_key or '', message_id or '', receive_id, account_id or '', media_type or '', tmdb_id or '', title or '', raw_card_json),
        )
        conn.commit()
    finally:
        conn.close()


def find_latest_snapshot(*, receive_id: str, media_type: str, tmdb_id: str):
    conn = _conn()
    try:
        cur = conn.execute(
            'SELECT raw_card_json, account_id, title, created_at, card_key, message_id FROM card_snapshots WHERE receive_id=? AND media_type=? AND tmdb_id=? ORDER BY created_at DESC LIMIT 1',
            (receive_id, media_type, tmdb_id),
        )
        row = cur.fetchone()
        if not row:
            return None
        return {
            'raw_card_json': row[0],
            'account_id': row[1] or None,
            'title': row[2] or None,
            'created_at': row[3],
            'card_key': row[4] or None,
            'message_id': row[5] or None,
        }
    finally:
        conn.close()


def find_snapshot_by_card_key(card_key: str):
    conn = _conn()
    try:
        cur = conn.execute(
            'SELECT raw_card_json, account_id, title, created_at, receive_id, media_type, tmdb_id, message_id FROM card_snapshots WHERE card_key=? ORDER BY created_at DESC LIMIT 1',
            (card_key,),
        )
        row = cur.fetchone()
        if not row:
            return None
        return {
            'raw_card_json': row[0],
            'account_id': row[1] or None,
            'title': row[2] or None,
            'created_at': row[3],
            'receive_id': row[4] or None,
            'media_type': row[5] or None,
            'tmdb_id': row[6] or None,
            'message_id': row[7] or None,
        }
    finally:
        conn.close()


def patch_subscribe_button(raw_card_json: str, *, text: str, disabled: bool):
    card = json.loads(raw_card_json)
    body = card.get('body') if isinstance(card, dict) else None
    elements = body.get('elements') if isinstance(body, dict) else None
    if not isinstance(elements, list):
        return raw_card_json

    for el in elements:
        if not isinstance(el, dict):
            continue
        if el.get('tag') != 'button':
            continue
        txt = ((el.get('text') or {}).get('content') if isinstance(el.get('text'), dict) else '') or ''
        if txt in ('立即订阅', '✅ 已订阅', '处理中...', '订阅失败，重试'):
            el['disabled'] = bool(disabled)
            if isinstance(el.get('text'), dict):
                el['text']['content'] = text
            else:
                el['text'] = {'tag': 'plain_text', 'content': text}
            # Some Feishu clients render badly when disabled button still carries callback behaviors.
            if bool(disabled):
                el.pop('behaviors', None)
            break

    return json.dumps(card, ensure_ascii=False)
