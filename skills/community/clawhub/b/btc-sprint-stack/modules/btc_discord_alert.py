from __future__ import annotations

import json
import os
from typing import Mapping
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class DiscordAlertError(RuntimeError):
    pass


def load_discord_webhook_url(env: Mapping[str, str] | None = None) -> str:
    values = env if env is not None else os.environ
    webhook_url = str(values.get('DISCORD_WEBHOOK_URL') or '').strip()
    if not webhook_url:
        raise DiscordAlertError('DISCORD_WEBHOOK_URL is required for Discord alerts')
    if not webhook_url.startswith('https://discord.com/api/webhooks/') and not webhook_url.startswith('https://discordapp.com/api/webhooks/'):
        raise DiscordAlertError('DISCORD_WEBHOOK_URL must be a Discord webhook URL')
    return webhook_url


def _with_wait_param(webhook_url: str) -> str:
    separator = '&' if '?' in webhook_url else '?'
    if 'wait=' in webhook_url:
        return webhook_url
    return f'{webhook_url}{separator}wait=true'


def send_discord_alert(message: str, *, env: Mapping[str, str] | None = None, timeout: float = 15.0) -> dict:
    webhook_url = load_discord_webhook_url(env)
    body = json.dumps(
        {
            'content': message,
            'allowed_mentions': {'parse': []},
        }
    ).encode('utf-8')
    request = Request(
        _with_wait_param(webhook_url),
        data=body,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            status_code = getattr(response, 'status', response.getcode())
            raw_body = response.read().decode('utf-8').strip()
    except HTTPError as exc:
        raise DiscordAlertError(f'Discord webhook request failed with HTTP {exc.code}') from exc
    except URLError as exc:
        raise DiscordAlertError(f'Discord webhook request failed: {exc.reason}') from exc

    parsed_body = None
    if raw_body:
        try:
            parsed_body = json.loads(raw_body)
        except json.JSONDecodeError:
            parsed_body = raw_body

    return {
        'ok': 200 <= status_code < 300,
        'status_code': status_code,
        'response': parsed_body,
    }
