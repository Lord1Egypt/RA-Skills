#!/usr/bin/env python3
"""本地执行滴答开放平台 OAuth。"""

from __future__ import annotations

import argparse
import json
import sys
import webbrowser

from tools.openapi_auth import (
    build_authorization_url,
    exchange_code_for_token,
    wait_for_oauth_callback,
    write_openapi_env,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="完成 Dida Open API OAuth 授权")
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--client-secret", required=True)
    parser.add_argument("--redirect-uri", default="http://localhost:38000/callback")
    parser.add_argument("--scope", default="tasks:read tasks:write")
    parser.add_argument("--open-browser", action="store_true")
    args = parser.parse_args()

    url, state = build_authorization_url(
        args.client_id,
        redirect_uri=args.redirect_uri,
        scope=args.scope,
    )
    print(json.dumps({"authorization_url": url, "state": state}, ensure_ascii=False))
    sys.stdout.flush()

    if args.open_browser:
        webbrowser.open(url)

    callback = wait_for_oauth_callback(expected_state=state)
    if callback.error:
        print(json.dumps({"ok": False, "error": callback.error}, ensure_ascii=False))
        return 1

    token_data = exchange_code_for_token(
        args.client_id,
        args.client_secret,
        callback.code or "",
        redirect_uri=args.redirect_uri,
    )
    env_path = write_openapi_env(
        args.client_id,
        args.client_secret,
        token_data,
        redirect_uri=args.redirect_uri,
    )
    print(
        json.dumps(
            {
                "ok": True,
                "env_path": str(env_path),
                "token_type": token_data.get("token_type"),
                "scope": token_data.get("scope"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
