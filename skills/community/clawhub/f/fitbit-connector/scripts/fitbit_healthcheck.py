#!/usr/bin/env python3
import json
from datetime import datetime, timezone

from _fitbit_common import db, get_config, load_tokens


def main():
    cfg = get_config()
    tokens = load_tokens(cfg)

    db_ok = False
    latest = None
    warn_count_24h = 0
    try:
        conn = db(cfg)
        db_ok = True
        row = conn.execute(
            "SELECT date, updated_at, readiness_state, data_quality FROM daily_metrics ORDER BY date DESC LIMIT 1"
        ).fetchone()
        if row:
            latest = {"date": row[0], "updated_at": row[1], "readiness_state": row[2], "data_quality": row[3]}
        warn_count_24h = conn.execute(
            "SELECT COUNT(*) FROM quality_flags WHERE datetime(created_at) >= datetime('now','-1 day')"
        ).fetchone()[0]
    except Exception as e:
        latest = {"db_error": str(e)}

    exp = tokens.get("expires_at")
    token_status = "missing"
    seconds_to_expiry = None
    if exp:
        now_ts = datetime.now(timezone.utc).timestamp()
        seconds_to_expiry = int(float(exp) - now_ts)
        token_status = "valid" if seconds_to_expiry > 0 else "expired"

    print(
        json.dumps(
            {
                "token_status": token_status,
                "seconds_to_expiry": seconds_to_expiry,
                "has_refresh_token": bool(tokens.get("refresh_token")),
                "db_ok": db_ok,
                "latest_daily_metric": latest,
                "quality_flags_last_24h": warn_count_24h,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
