# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "flask",
# ]
# ///

from __future__ import annotations

import json
import logging
import os
import sqlite3
from pathlib import Path
from typing import Any
from uuid import uuid4

from flask import Flask, request, jsonify

OUTPUT_ROOT = Path(os.environ.get("OUTPUT_ROOT", "~/")).expanduser().resolve()
DEFAULT_DB_PATH = OUTPUT_ROOT / "outputs" / "doubao" / "video_tasks.db"
TOKEN_FILE = OUTPUT_ROOT / "outputs" / "doubao" / ".webhook_token"


def _generate_token() -> str:
    """Generate a random webhook token and persist it."""
    token = uuid4().hex
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(token, encoding="utf-8")
    return token


def _load_or_generate_token() -> str:
    """Load existing token from file, or generate a new one."""
    if TOKEN_FILE.exists():
        token = TOKEN_FILE.read_text(encoding="utf-8").strip()
        if token:
            return token
    return _generate_token()


def create_app(db_path: Path | str | None = None, webhook_token: str | None = None) -> Flask:
    """Create and configure the Flask app."""
    app = Flask(__name__)
    db = str(db_path or DEFAULT_DB_PATH)
    db_path_obj = Path(db)
    db_path_obj.parent.mkdir(parents=True, exist_ok=True)
    token = webhook_token or _load_or_generate_token()

    log_file = db_path_obj.parent / "webhook.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(str(log_file)), logging.StreamHandler()],
    )

    def get_conn() -> sqlite3.Connection:
        conn = sqlite3.connect(db)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db() -> None:
        conn = get_conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS video_generation_tasks (
                task_id TEXT PRIMARY KEY,
                model TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at INTEGER NOT NULL,
                updated_at INTEGER NOT NULL,
                service_tier TEXT NOT NULL,
                execution_expires_after INTEGER NOT NULL,
                video_url TEXT,
                last_callback_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
        logging.info("Database initialized")

    init_db()

    @app.before_request
    def reject_unauthorized() -> tuple[Any, int] | None:
        """Block access from non-localhost origins."""
        if request.remote_addr not in ("127.0.0.1", "::1", "localhost"):
            logging.warning("Rejected request from %s to %s", request.remote_addr, request.path)
            return jsonify({"code": 403, "msg": "Forbidden"}), 403
        return None

    @app.route(f"/webhook/callback/<token_val>", methods=["POST"])
    @app.route("/webhook/callback", methods=["POST"])
    def video_task_callback(token_val: str = "") -> tuple[Any, int]:
        """Core interface for receiving Ark callback."""
        # Token verification
        if token_val != token:
            logging.warning("Callback rejected: invalid token")
            return jsonify({"code": 403, "msg": "Invalid token"}), 403

        try:
            callback_data = request.get_json(force=True, silent=True)
            if not callback_data:
                logging.error("Callback request body empty or non-JSON")
                return jsonify({"code": 400, "msg": "Invalid JSON data"}), 400

            required_fields = [
                "id", "model", "status", "created_at",
                "updated_at", "service_tier", "execution_expires_after",
            ]
            missing = [f for f in required_fields if f not in callback_data]
            if missing:
                logging.error(f"Missing fields: {missing}")
                return jsonify({"code": 400, "msg": f"Missing fields: {missing}"}), 400

            task_id = callback_data["id"]
            status = callback_data["status"]
            model = callback_data["model"]
            logging.info(f"Task callback | id={task_id} | status={status} | model={model}")

            # Extract video_url if present (succeeded tasks)
            video_url = ""
            content = callback_data.get("content")
            if isinstance(content, dict):
                video_url = content.get("video_url", "")

            conn = get_conn()
            conn.execute("""
                INSERT INTO video_generation_tasks (
                    task_id, model, status, created_at, updated_at,
                    service_tier, execution_expires_after, video_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(task_id) DO UPDATE SET
                    status = excluded.status,
                    updated_at = excluded.updated_at,
                    video_url = COALESCE(excluded.video_url, video_generation_tasks.video_url),
                    last_callback_at = CURRENT_TIMESTAMP
            """, (
                task_id, model, status,
                callback_data["created_at"], callback_data["updated_at"],
                callback_data["service_tier"], callback_data["execution_expires_after"],
                video_url,
            ))
            conn.commit()
            conn.close()

            output = {
                "type": "video",
                "scene": "webhook_callback",
                "provider": "doubao",
                "task_id": task_id,
                "status": status,
            }
            if video_url:
                output["video_url"] = video_url

            print(json.dumps(output, ensure_ascii=False, indent=2))
            return jsonify({"code": 200, "msg": "ok", "task_id": task_id}), 200

        except Exception as e:
            logging.error(f"Callback processing failed: {e}", exc_info=True)
            # Always return 200 to avoid Ark API retry storms
            return jsonify({"code": 200, "msg": "received (internal error)"}), 200

    @app.route("/tasks/<task_id>", methods=["GET"])
    def get_task_status(task_id: str) -> tuple[Any, int]:
        """Query latest status of a task."""
        conn = get_conn()
        row = conn.execute(
            "SELECT * FROM video_generation_tasks WHERE task_id = ?", (task_id,)
        ).fetchone()
        conn.close()
        if not row:
            return jsonify({"code": 404, "msg": "Task not found"}), 404
        return jsonify({"code": 200, "data": dict(row)}), 200

    @app.route("/tasks", methods=["GET"])
    def list_tasks() -> tuple[Any, int]:
        """List all tasks, optional ?status= filter."""
        status_filter = request.args.get("status")
        conn = get_conn()
        if status_filter:
            rows = conn.execute(
                "SELECT * FROM video_generation_tasks WHERE status = ? ORDER BY last_callback_at DESC",
                (status_filter,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM video_generation_tasks ORDER BY last_callback_at DESC"
            ).fetchall()
        conn.close()
        return jsonify({"code": 200, "data": [dict(r) for r in rows]}), 200

    # Store token on app for external access
    app.webhook_token = token
    return app


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="豆包视频生成 Webhook 回调服务器")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址")
    parser.add_argument("--port", type=int, default=8888, help="监听端口")
    parser.add_argument("--db", default=None, help="SQLite 数据库路径")
    parser.add_argument("--token", default=None, help="Webhook 验证 token，不传则自动生成")
    args = parser.parse_args()

    app = create_app(db_path=args.db, webhook_token=args.token)
    token = app.webhook_token
    logging.info(f"Starting webhook server on {args.host}:{args.port}")
    print(f"Webhook server listening on http://{args.host}:{args.port}")
    print(f"Webhook token: {token}")
    print(f"POST /webhook/callback/{token} — 接收 Ark 回调")
    print(f"GET  /tasks/<task_id>  — 查询任务状态")
    print(f"GET  /tasks            — 列出所有任务")
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
