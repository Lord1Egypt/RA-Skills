#!/usr/bin/env python3
"""Read-only GitHub release check; Python standard library only."""
import json
from pathlib import Path
import re
import ssl
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPOSITORY = 'gengwenhao/book-to-mentor'
RELEASES = f'https://github.com/{REPOSITORY}/releases'
API = f'https://api.github.com/repos/{REPOSITORY}/releases/latest'


def version_tuple(value):
    if not isinstance(value, str) or not re.fullmatch(r'v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)', value):
        raise ValueError('Expected a stable version such as 1.2.3')
    return tuple(map(int, value.removeprefix('v').split('.')))


def compare_release(current, release):
    if not isinstance(release, dict) or release.get('draft') is not False or release.get('prerelease') is not False:
        raise ValueError('GitHub did not return a published stable release')
    latest = release.get('tag_name')
    local, remote = version_tuple(current), version_tuple(latest)
    status = 'update_available' if remote > local else 'up_to_date' if remote == local else 'ahead_of_release'
    return {'status': status, 'current_version': current, 'latest_version': latest.removeprefix('v'),
            'release_url': f'{RELEASES}/tag/{latest}',
            'release_notes': release.get('body') or '',
            'scope': 'GitHub release only; availability on other channels is not checked.'}


def check(root=None, opener=urlopen):
    root = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    current = None
    try:
        current = json.loads((root / 'release.json').read_text(encoding='utf-8'))['version']
        version_tuple(current)
        request = Request(API, headers={'Accept': 'application/vnd.github+json',
                                      'User-Agent': 'book-to-mentor-update-check'})
        with opener(request, timeout=10) as response:
            return compare_release(current, json.load(response))
    except HTTPError as error:
        reason = 'No public release was found.' if error.code == 404 else f'GitHub HTTP {error.code}; retry later.'
    except URLError as error:
        reason = ('Python could not verify GitHub TLS certificates; configure its trusted CA certificates and retry.'
                  if isinstance(error.reason, ssl.SSLCertVerificationError)
                  else 'Could not reach GitHub; retry later.')
    except (TimeoutError, OSError):
        reason = 'Could not read local version or reach GitHub; retry later.'
    except (ValueError, KeyError, TypeError):
        reason = 'Invalid local version or GitHub release metadata.'
    return {'status': 'check_unavailable', 'current_version': current,
            'reason': reason, 'release_url': RELEASES}


if __name__ == '__main__':
    result = check()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(2 if result['status'] == 'check_unavailable' else 0)
