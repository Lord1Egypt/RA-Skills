#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str((ROOT / 'src').resolve()))

import daily_strava_roast.cli as cli


def main() -> int:
    auth_msg = cli.auth_unavailable_message(cli.StravaAuthError('Strava activity fetch failed with 401'))
    recovery_msg = cli.auth_unavailable_message(
        cli.StravaAuthError('Strava activity fetch failed with 401'),
        {'status': 'reauth_required', 'auth_url': 'https://example.com/auth'},
    )
    setup_msg = cli.auth_unavailable_message(
        cli.StravaInitialSetupRequiredError('token file missing'),
        {'status': 'initial_setup_required'},
    )
    config_msg = cli.auth_unavailable_message(
        cli.StravaAuthError('Strava client_secret is not configured'),
        {'status': 'config_incomplete'},
    )
    data_msg = cli.data_unavailable_message(cli.StravaDataUnavailableError('network timeout'))
    assert 'not a confirmed rest day' in auth_msg.lower()
    assert 'authentication failure' in auth_msg.lower()
    assert 'reauthorisation' in recovery_msg.lower()
    assert 'initial setup' in setup_msg.lower()
    assert 'configuration' in config_msg.lower()
    assert 'client credentials' in config_msg.lower()
    assert 'not a confirmed rest day' in data_msg.lower()
    assert cli.reauth_available(Path('/tmp/definitely-missing-script.py'), {'client_secret': 'secret'}) is False

    with tempfile.TemporaryDirectory() as tmp:
        missing = Path(tmp) / 'missing.json'
        try:
            cli.load_tokens(missing)
            raise AssertionError('expected initial setup error for missing token file')
        except cli.StravaInitialSetupRequiredError:
            pass

        bad = Path(tmp) / 'bad.json'
        bad.write_text('{broken json')
        try:
            cli.load_tokens(bad)
            raise AssertionError('expected initial setup error for invalid token file')
        except cli.StravaInitialSetupRequiredError:
            pass

        incomplete = Path(tmp) / 'incomplete.json'
        incomplete.write_text(json.dumps({'access_token': 'a'}))
        try:
            cli.validate_token_shape(json.loads(incomplete.read_text()), incomplete)
            raise AssertionError('expected initial setup error for incomplete token file')
        except cli.StravaInitialSetupRequiredError:
            pass

    print('auth handling test passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
