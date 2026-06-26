#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str((ROOT / 'src').resolve()))

from daily_strava_roast.strava_config import load_strava_app_config, missing_config_requirements


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'strava_app.json'
        path.write_text(json.dumps({
            'client_id': '216808',
            'client_secret': 'secret123',
            'redirect_uri': 'http://localhost/exchange_token',
            'scopes': 'read,activity:read_all',
            'token_file': '/tmp/strava_tokens.json',
        }))
        config = load_strava_app_config(path)
        assert config['client_secret'] == 'secret123'
        assert config['config_present'] is True
        assert missing_config_requirements(config) == []

        os.environ['STRAVA_CLIENT_SECRET'] = 'env-secret'
        config2 = load_strava_app_config(path)
        assert config2['client_secret'] == 'env-secret'
        del os.environ['STRAVA_CLIENT_SECRET']

    print('strava config test passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
