"""Local Flask dashboard for BillClaw."""

from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, jsonify, request, send_file

from db import (
    aggregate_by_category,
    count_transactions,
    daily_totals,
    default_db_path,
    get_connection,
    monthly_totals,
    query_transactions,
    totals,
    transaction_date_bounds,
)

_DASHBOARD_FILE = Path(__file__).with_name("dashboard.html")
_STATIC_DIR = Path(__file__).parent / "static"


def create_app(db_path: Path | str | None = None) -> Flask:
    app = Flask(
        __name__,
        static_folder=str(_STATIC_DIR),
        static_url_path="/static",
    )
    path = Path(db_path) if db_path else default_db_path()

    def conn_ctx():
        return get_connection(path)

    def _date_args() -> tuple[str | None, str | None]:
        return request.args.get("date_from") or None, request.args.get("date_to") or None

    @app.route("/")
    def index():
        if not _DASHBOARD_FILE.is_file():
            return (
                "dashboard.html 缺失，请与 web.py 同目录放置。",
                500,
                {"Content-Type": "text/plain; charset=utf-8"},
            )
        return send_file(_DASHBOARD_FILE, mimetype="text/html; charset=utf-8")

    @app.route("/api/meta")
    def api_meta():
        with conn_ctx() as conn:
            bounds = transaction_date_bounds(conn)
        return jsonify(bounds)

    @app.route("/api/summary")
    def api_summary():
        date_from, date_to = _date_args()
        with conn_ctx() as conn:
            t = totals(conn, date_from=date_from, date_to=date_to)
            rows = aggregate_by_category(
                conn, date_from=date_from, date_to=date_to, type_="支出"
            )
            exp_only = [{"category": r["category"], "total": float(r["total"])} for r in rows]
            inc_rows = aggregate_by_category(
                conn, date_from=date_from, date_to=date_to, type_="收入"
            )
            inc_only = [{"category": r["category"], "total": float(r["total"])} for r in inc_rows]
        return jsonify(
            {
                "totals": t,
                "expense_by_category": exp_only,
                "income_by_category": inc_only,
            }
        )

    @app.route("/api/trend")
    def api_trend():
        date_from, date_to = _date_args()
        with conn_ctx() as conn:
            daily = daily_totals(conn, date_from=date_from, date_to=date_to)
        return jsonify({"daily": daily})

    @app.route("/api/monthly")
    def api_monthly():
        date_from, date_to = _date_args()
        with conn_ctx() as conn:
            monthly = monthly_totals(conn, date_from=date_from, date_to=date_to)
        return jsonify({"monthly": monthly})

    @app.route("/api/transactions")
    def api_transactions():
        date_from, date_to = _date_args()
        type_ = request.args.get("type") or None
        if type_ == "":
            type_ = None
        page = max(1, int(request.args.get("page", 1)))
        per_page = min(500, max(10, int(request.args.get("per_page", 100))))
        offset = (page - 1) * per_page
        with conn_ctx() as conn:
            total = count_transactions(
                conn, date_from=date_from, date_to=date_to, type_=type_
            )
            rows = query_transactions(
                conn,
                date_from=date_from,
                date_to=date_to,
                type_=type_,
                limit=per_page,
                offset=offset,
            )
        return jsonify(
            {
                "rows": rows,
                "total": total,
                "page": page,
                "per_page": per_page,
            }
        )

    return app


def run_server(
    host: str = "127.0.0.1",
    port: int = 8000,
    db_path: Path | str | None = None,
    debug: bool = False,
) -> None:
    os.environ.setdefault("FLASK_ENV", "production")
    app = create_app(db_path)
    app.run(host=host, port=port, debug=debug, use_reloader=False)
