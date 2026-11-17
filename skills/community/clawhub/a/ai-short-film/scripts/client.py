"""Fixed-origin PopNow API client. Never log credentials or request bodies."""
import json
import math
import re
from decimal import Decimal
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener

BASE = 'https://api.popnow.ai/api/v1'

class PopNowError(Exception):
    pass

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def required_string(value, name, maximum=256):
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise PopNowError(f'{name} must be a nonempty string (maximum {maximum} characters).')
    return value


def input_object(value):
    raw = required_string(value, 'input_json', 2_000_000)
    try:
        result = json.loads(raw, parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except (ValueError, TypeError):
        raise PopNowError('input_json must be valid JSON.') from None
    if not isinstance(result, dict):
        raise PopNowError('input_json must be a JSON object, not an array or scalar.')
    def finite(item):
        if isinstance(item, float) and not math.isfinite(item):
            raise PopNowError('input_json contains a non-finite number.')
        if isinstance(item, dict):
            for v in item.values(): finite(v)
        if isinstance(item, list):
            for v in item: finite(v)
    finite(result)
    return result


def approved_amount(value):
    if not isinstance(value, str) or not re.fullmatch(r'(?:0|[1-9][0-9]*)(?:\.[0-9]{1,9})?', value) or len(value) > 40:
        raise PopNowError('approved_max_usd must be the approved nonnegative decimal STRING, with up to nine decimal places.')
    if not Decimal(value).is_finite():
        raise PopNowError('approved_max_usd must be finite.')
    return value


class PopNowClient:
    def __init__(self, api_key, opener=None):
        if not isinstance(api_key, str) or not api_key.startswith('sk-popnow-') or any(c.isspace() for c in api_key):
            raise PopNowError('Enter a valid PopNow API key from the API console.')
        self.api_key = api_key
        self.opener = opener or build_opener(NoRedirect())

    def request(self, endpoint, body=None, query=None, idempotency_key=None):
        if endpoint not in {'/models', '/chat/credit', '/jobs/quote', '/jobs/createTask', '/jobs/recordInfo'}:
            raise PopNowError('Unsupported API operation.')
        url = BASE + endpoint
        if query:
            url += '?' + urlencode(query)
        headers = {'Authorization': 'Bearer ' + self.api_key, 'Accept': 'application/json', 'User-Agent': 'PopNow-OpenClaw/1.0.0'}
        if body is not None:
            headers['Content-Type'] = 'application/json'
        if idempotency_key is not None:
            key = required_string(idempotency_key, 'idempotency_key', 100)
            if not re.fullmatch(r'[\x21-\x7e]+', key):
                raise PopNowError('idempotency_key must contain 1–100 visible ASCII characters.')
            headers['Idempotency-Key'] = key
        request = Request(url, data=json.dumps(body, allow_nan=False).encode() if body is not None else None, headers=headers)
        try:
            with self.opener.open(request, timeout=60) as response:
                raw = response.read(8_000_001)
            if len(raw) > 8_000_000:
                raise PopNowError('PopNow response was too large; narrow the model search.')
            envelope = json.loads(raw)
        except HTTPError as error:
            raise PopNowError(f'PopNow HTTP {error.code}. Check the key, permissions, API balance and request parameters. Check task status before retrying generation.') from None
        except (URLError, TimeoutError, OSError):
            raise PopNowError('PopNow could not be reached. A timed-out generation may still exist; check status before retrying with the SAME idempotency key.') from None
        except (ValueError, TypeError):
            raise PopNowError('PopNow returned an invalid response.') from None
        if not isinstance(envelope, dict) or envelope.get('code') != 200:
            code = envelope.get('code') if isinstance(envelope, dict) else None
            safe_code = str(code) if isinstance(code, (int, float)) else 'unknown'
            raise PopNowError(f'PopNow rejected the request (code {safe_code}). Check parameters, permissions and API USD balance. Obtain a fresh quote if it expired.')
        return envelope.get('data')

    def invoke(self, operation, params):
        if operation == 'models':
            query = {'includeSchema': 'true', 'includeExamples': 'true'}
            for key in ('search', 'modality'):
                if params.get(key):
                    query[key] = required_string(params[key], key, 200)
            return self.request('/models', query=query)
        if operation == 'balance':
            return self.request('/chat/credit')
        if operation == 'status':
            return self.request('/jobs/recordInfo', query={'taskId': required_string(params.get('task_id'), 'task_id')})
        if operation not in {'quote', 'create'}:
            raise PopNowError('Unknown operation.')
        body = {'model': required_string(params.get('model'), 'model'), 'input': input_object(params.get('input_json'))}
        if operation == 'quote':
            return self.request('/jobs/quote', body=body)
        body['quoteId'] = required_string(params.get('quote_id'), 'quote_id')
        body['expectedCostUsd'] = approved_amount(params.get('approved_max_usd'))
        key = required_string(params.get('idempotency_key'), 'idempotency_key', 100)
        return self.request('/jobs/createTask', body=body, idempotency_key=key)
