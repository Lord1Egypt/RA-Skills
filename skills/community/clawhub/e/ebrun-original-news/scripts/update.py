#!/usr/bin/env python3
"""
ebrun-original-news - 检查 Skill 版本更新

用法:
    python3 update.py                                    # 默认输出 JSON 结果
    python3 update.py --json                             # 输出 JSON 结果
    python3 update.py --table                            # 输出易读文本
    python3 update.py --timeout 10 --retries 3          # 调整超时与重试
    python3 update.py --version-url <url>               # 自定义版本接口地址
"""

import argparse
import json
import tempfile
import socket
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional
from urllib import request
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse

SKILL_NAME = 'ebrun-original-news'
DEFAULT_TIMEOUT = 10
DEFAULT_RETRIES = 3
DEFAULT_CHECK_INTERVAL_HOURS = 24
VERSION_API_URL = 'https://www.ebrun.com/_index/ClaudeCode/SkillJson/skill_version.json'
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
# 优先使用 Gitee 作为降级源，避免 GitHub 速率限制
DEFAULT_FALLBACK_ORDER = ['gitee', 'github']
ALLOWED_DOMAINS = ['www.ebrun.com', 'api.ebrun.com', 'github.com', 'raw.githubusercontent.com', 'gitee.com']
VERSION_FILE = Path(__file__).resolve().parent.parent / 'references' / 'version.json'
CACHE_FILE = Path(tempfile.gettempdir()) / f'{SKILL_NAME}-version-cache.json'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (EbrunSkillUpdate/1.0)',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.ebrun.com/'
}

EXIT_USAGE_ERROR = 2
EXIT_SECURITY_ERROR = 3
EXIT_REQUEST_ERROR = 4
EXIT_NOT_FOUND = 5
EXIT_FORBIDDEN = 6
EXIT_JSON_ERROR = 7


class UpdateCheckError(Exception):
    def __init__(self, message: str, exit_code: int):
        super().__init__(message)
        self.exit_code = exit_code


def print_error(message: str):
    print(f'[ERROR] {message}', file=sys.stderr)


def print_warning(message: str):
    print(f'[WARN] {message}', file=sys.stderr)


def is_safe_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        if parsed.scheme != 'https':
            return False
        return any(parsed.hostname == domain or (parsed.hostname and parsed.hostname.endswith('.' + domain)) for domain in ALLOWED_DOMAINS)
    except Exception:
        return False


def validate_positive_int(value: int, flag_name: str) -> int:
    if value <= 0:
        raise UpdateCheckError(f'参数错误: {flag_name} 必须大于 0', EXIT_USAGE_ERROR)
    return value


def validate_url(url: str, label: str) -> str:
    normalized = url.strip()
    if not normalized:
        raise UpdateCheckError(f'参数错误: {label} 不能为空', EXIT_USAGE_ERROR)
    if not is_safe_url(normalized):
        raise UpdateCheckError(f'安全性风险: 非授权地址 -> {url}', EXIT_SECURITY_ERROR)
    return normalized


def read_local_version_info() -> Dict[str, Any]:
    try:
        data = json.loads(VERSION_FILE.read_text(encoding='utf-8'))
    except FileNotFoundError as error:
        raise UpdateCheckError(f'未找到本地版本文件: {VERSION_FILE}', EXIT_NOT_FOUND) from error
    except json.JSONDecodeError as error:
        raise UpdateCheckError(f'本地 version.json 解析失败: {error}', EXIT_JSON_ERROR) from error

    if not isinstance(data, dict):
        raise UpdateCheckError('本地 version.json 格式异常: 顶层必须是对象', EXIT_JSON_ERROR)

    current_version = str(data.get('current_version', '')).strip()
    if not current_version:
        raise UpdateCheckError('本地 version.json 缺少 current_version', EXIT_JSON_ERROR)

    interval_hours = data.get('check_interval_hours', DEFAULT_CHECK_INTERVAL_HOURS)
    if not isinstance(interval_hours, (int, float)) or interval_hours <= 0:
        raise UpdateCheckError('本地 version.json 中 check_interval_hours 必须大于 0', EXIT_JSON_ERROR)

    return data


def get_check_interval_seconds(local_info: Dict[str, Any]) -> int:
    interval_hours = float(local_info.get('check_interval_hours', DEFAULT_CHECK_INTERVAL_HOURS))
    return max(int(interval_hours * 3600), 1)


def read_cache_info() -> Dict[str, Any]:
    try:
        data = json.loads(CACHE_FILE.read_text(encoding='utf-8'))
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

    return data if isinstance(data, dict) else {}


def parse_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def parse_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {'true', '1', 'yes'}:
            return True
        if normalized in {'false', '0', 'no'}:
            return False
    return default


def build_cached_result(
    local_info: Dict[str, Any],
    cache_info: Dict[str, Any],
    now_ts: int,
    version_api_url: str,
) -> Optional[Dict[str, Any]]:
    last_check_time = parse_int(cache_info.get('last_check_time'), 0)
    last_known_version = str(cache_info.get('last_known_version', '')).strip()
    last_check_source = str(cache_info.get('last_check_source', '')).strip()
    cached_version_api_url = str(cache_info.get('version_api_url', '')).strip()

    if last_check_time <= 0 or not last_known_version or not last_check_source:
        return None
    if not cached_version_api_url or cached_version_api_url != version_api_url:
        return None

    interval_seconds = get_check_interval_seconds(local_info)
    if now_ts - last_check_time >= interval_seconds:
        return None

    current_version = str(local_info.get('current_version', '')).strip()
    remaining_seconds = interval_seconds - (now_ts - last_check_time)
    return {
        'skill_name': SKILL_NAME,
        'current_version': current_version,
        'latest_version': last_known_version,
        'update_available': parse_bool(cache_info.get('last_update_available'), last_known_version != current_version),
        'check_source': last_check_source,
        'status': 'cached',
        'version_api_url': version_api_url,
        'version_file_url': str(cache_info.get('last_version_file_url', '')).strip(),
        'update_url_github': str(local_info.get('update_url_github', '')).strip(),
        'update_url_gitee': str(local_info.get('update_url_gitee', '')).strip(),
        'last_check_time': last_check_time,
        'check_interval_hours': local_info.get('check_interval_hours', DEFAULT_CHECK_INTERVAL_HOURS),
        'remaining_seconds': remaining_seconds,
        'message': '未到检查间隔，返回上次缓存结果'
    }


def persist_check_cache(result: Dict[str, Any], now_ts: int, version_api_url: str) -> None:
    latest_version = str(result.get('latest_version', '')).strip()
    if not latest_version or latest_version == 'unknown':
        return

    cache_payload = {
        'version_api_url': version_api_url,
        'last_check_time': now_ts,
        'last_known_version': latest_version,
        'last_check_source': str(result.get('check_source', '')).strip(),
        'last_update_available': bool(result.get('update_available', False)),
        'last_version_file_url': str(result.get('version_file_url', '')).strip(),
    }
    CACHE_FILE.write_text(json.dumps(cache_payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def should_retry_http(status_code: int) -> bool:
    return status_code in RETRYABLE_STATUS_CODES


def should_retry_network(error: BaseException) -> bool:
    if isinstance(error, (TimeoutError, socket.timeout)):
        return True
    if isinstance(error, URLError):
        reason = getattr(error, 'reason', None)
        return isinstance(reason, (TimeoutError, socket.timeout))
    return False


def map_http_error(error: HTTPError) -> UpdateCheckError:
    if error.code == 403:
        return UpdateCheckError('版本接口请求被拒绝: HTTP 403', EXIT_FORBIDDEN)
    if error.code == 404:
        return UpdateCheckError('版本接口不存在: HTTP 404', EXIT_NOT_FOUND)
    if error.code == 503:
        return UpdateCheckError('版本接口暂时不可用: HTTP 503，可稍后重试', EXIT_REQUEST_ERROR)
    return UpdateCheckError(f'版本接口请求失败: HTTP {error.code}', EXIT_REQUEST_ERROR)


def map_network_error(error: BaseException) -> UpdateCheckError:
    if should_retry_network(error):
        return UpdateCheckError('版本接口请求超时，请稍后重试', EXIT_REQUEST_ERROR)
    reason = getattr(error, 'reason', None)
    if reason:
        return UpdateCheckError(f'版本接口请求失败: {reason}', EXIT_REQUEST_ERROR)
    return UpdateCheckError(f'版本接口请求失败: {error}', EXIT_REQUEST_ERROR)


def fetch_json(url: str, timeout: int, retries: int) -> Dict[str, Any]:
    validate_url(url, '--version-url')
    last_error: Optional[UpdateCheckError] = None

    for attempt in range(1, retries + 1):
        try:
            req = request.Request(url, headers=HEADERS)
            with request.urlopen(req, timeout=timeout) as response:
                content = response.read().decode('utf-8')
                data = json.loads(content)
                if not isinstance(data, dict):
                    raise UpdateCheckError('版本接口格式异常: 顶层必须是对象', EXIT_JSON_ERROR)
                return data
        except HTTPError as error:
            last_error = map_http_error(error)
            if not should_retry_http(error.code) or attempt >= retries:
                raise last_error
            print_warning(f'{last_error}. 第 {attempt} 次请求失败，准备重试...')
        except json.JSONDecodeError as error:
            raise UpdateCheckError(f'版本接口 JSON 解析失败: {error}', EXIT_JSON_ERROR) from error
        except (URLError, TimeoutError, socket.timeout) as error:
            last_error = map_network_error(error)
            if not should_retry_network(error) or attempt >= retries:
                raise last_error
            print_warning(f'{last_error}. 第 {attempt} 次请求失败，准备重试...')
        except UpdateCheckError:
            raise
        except Exception as error:
            raise UpdateCheckError(f'版本接口请求异常: {error}', EXIT_REQUEST_ERROR) from error

        time.sleep(min(attempt, 2))

    if last_error is not None:
        raise last_error
    raise UpdateCheckError('版本接口请求失败: 未知错误', EXIT_REQUEST_ERROR)


def parse_repo_url(repo_url: str) -> Optional[Dict[str, str]]:
    try:
        parsed = urlparse(repo_url)
    except Exception:
        return None

    if parsed.scheme != 'https' or not parsed.hostname:
        return None

    parts = [part for part in parsed.path.strip('/').split('/') if part]
    if parsed.hostname == 'github.com':
        if len(parts) < 2:
            return None
        return {'provider': 'github', 'owner': parts[0], 'repo': parts[1]}

    if parsed.hostname == 'gitee.com':
        if len(parts) < 2:
            return None
        return {'provider': 'gitee', 'owner': parts[0], 'repo': parts[1]}

    return None


def build_repo_version_file_urls(repo_url: str) -> list[str]:
    repo_info = parse_repo_url(repo_url)
    if not repo_info:
        return []

    owner = repo_info['owner']
    repo = repo_info['repo']
    branches = ['main', 'master']
    candidates: list[str] = []

    if repo_info['provider'] == 'github':
        candidates.extend([
            f'https://raw.githubusercontent.com/{owner}/{repo}/{branch}/references/version.json'
            for branch in branches
        ])
    elif repo_info['provider'] == 'gitee':
        candidates.extend([
            f'https://gitee.com/{owner}/{repo}/raw/{branch}/references/version.json'
            for branch in branches
        ])

    seen: set[str] = set()
    ordered: list[str] = []
    for candidate in candidates:
        if candidate not in seen:
            seen.add(candidate)
            ordered.append(candidate)
    return ordered


def fetch_repo_version_info(local_info: Dict[str, Any], timeout: int, retries: int) -> Dict[str, Any]:
    repo_sources = [
        ('gitee_version_json', str(local_info.get('update_url_gitee', '')).strip()),
        ('github_version_json', str(local_info.get('update_url_github', '')).strip()),
    ]
    errors: list[str] = []

    for source_name, repo_url in repo_sources:
        if not repo_url:
            continue

        candidate_urls = build_repo_version_file_urls(repo_url)
        if not candidate_urls:
            errors.append(f'{source_name}: 无法从仓库地址推导 references/version.json 地址')
            continue

        for candidate_url in candidate_urls:
            try:
                remote_info = fetch_json(candidate_url, timeout, retries)
                remote_current_version = str(remote_info.get('current_version', '')).strip()
                if not remote_current_version:
                    raise UpdateCheckError('远端 version.json 缺少 current_version', EXIT_JSON_ERROR)

                return {
                    'check_source': source_name,
                    'remote_version': remote_current_version,
                    'version_file_url': candidate_url,
                }
            except UpdateCheckError as error:
                # 专门处理 GitHub 速率限制错误
                if '429' in str(error) and 'github' in candidate_url:
                    errors.append(f'{candidate_url}: GitHub API 速率限制，将尝试 Gitee 源')
                else:
                    errors.append(f'{candidate_url}: {error}')

    raise UpdateCheckError('；'.join(errors) if errors else '无法从 GitHub/Gitee 远端仓库读取 references/version.json', EXIT_REQUEST_ERROR)


def check_url_reachable(url: str, timeout: int) -> bool:
    try:
        validate_url(url, 'update url')
        req = request.Request(url, method='HEAD', headers={'User-Agent': HEADERS['User-Agent']})
        with request.urlopen(req, timeout=timeout):
            return True
    except HTTPError as error:
        if error.code == 405:
            try:
                req = request.Request(url, headers={'User-Agent': HEADERS['User-Agent']})
                with request.urlopen(req, timeout=timeout):
                    return True
            except Exception:
                return False
        return False
    except Exception:
        return False


def build_remote_result(remote_data: Dict[str, Any], local_info: Dict[str, Any], version_api_url: str) -> Dict[str, Any]:
    remote_version = str(remote_data.get(SKILL_NAME, '')).strip()
    if not remote_version:
        raise UpdateCheckError(f'版本接口未返回 {SKILL_NAME} 字段', EXIT_JSON_ERROR)

    current_version = str(local_info.get('current_version', '')).strip()
    update_available = remote_version != current_version

    return {
        'skill_name': SKILL_NAME,
        'current_version': current_version,
        'latest_version': remote_version,
        'update_available': update_available,
        'check_source': 'remote_api',
        'status': 'ok',
        'version_api_url': version_api_url,
        'update_url_github': local_info.get('update_url_github', ''),
        'update_url_gitee': local_info.get('update_url_gitee', ''),
        'message': '检测完成' if not update_available else f'检测到新版本: {remote_version}'
    }


def build_fallback_result(local_info: Dict[str, Any], timeout: int, retries: int, remote_error: UpdateCheckError, version_api_url: str) -> Dict[str, Any]:
    current_version = str(local_info.get('current_version', '')).strip()
    github_url = str(local_info.get('update_url_github', '')).strip()
    gitee_url = str(local_info.get('update_url_gitee', '')).strip()

    try:
        repo_result = fetch_repo_version_info(local_info, timeout, retries)
        latest_version = repo_result['remote_version']
        update_available = latest_version != current_version
        message = (
            f'版本接口不可用，已降级到远端仓库 version.json；检测到版本不一致: {current_version} -> {latest_version}'
            if update_available else
            '版本接口不可用，已降级到远端仓库 version.json；当前未发现版本变化'
        )

        return {
            'skill_name': SKILL_NAME,
            'current_version': current_version,
            'latest_version': latest_version,
            'update_available': update_available,
            'check_source': repo_result['check_source'],
            'status': 'degraded',
            'version_api_url': version_api_url,
            'version_file_url': repo_result['version_file_url'],
            'update_url_github': github_url,
            'update_url_gitee': gitee_url,
            'remote_check_error': str(remote_error),
            'message': message
        }
    except UpdateCheckError as repo_error:
        github_reachable = check_url_reachable(github_url, timeout) if github_url else False
        gitee_reachable = check_url_reachable(gitee_url, timeout) if gitee_url else False
        return {
            'skill_name': SKILL_NAME,
            'current_version': current_version,
            'latest_version': 'unknown',
            'update_available': False,
            'check_source': 'unavailable',
            'status': 'degraded',
            'version_api_url': version_api_url,
            'update_url_github': github_url,
            'update_url_gitee': gitee_url,
            'update_url_github_reachable': github_reachable,
            'update_url_gitee_reachable': gitee_reachable,
            'remote_check_error': str(remote_error),
            'repo_version_check_error': str(repo_error),
            'message': '版本接口不可用，且无法从远端仓库读取 references/version.json，当前无法判断是否有新版本'
        }


def print_table(result: Dict[str, Any]):
    lines = [
        'Skill 版本检查结果',
        f"- skill_name: {result['skill_name']}",
        f"- current_version: {result['current_version']}",
        f"- latest_version: {result['latest_version']}",
        f"- update_available: {result['update_available']}",
        f"- check_source: {result['check_source']}",
        f"- status: {result['status']}",
        f"- message: {result['message']}"
    ]
    if result.get('update_url_github'):
        lines.append(f"- update_url_github: {result['update_url_github']}")
    if result.get('update_url_gitee'):
        lines.append(f"- update_url_gitee: {result['update_url_gitee']}")
    if result.get('version_file_url'):
        lines.append(f"- version_file_url: {result['version_file_url']}")
    if 'remote_check_error' in result:
        lines.append(f"- remote_check_error: {result['remote_check_error']}")
    if 'repo_version_check_error' in result:
        lines.append(f"- repo_version_check_error: {result['repo_version_check_error']}")
    print('\n'.join(lines))


def main():
    parser = argparse.ArgumentParser(
        description='检查 ebrun-original-news Skill 是否有新版本',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument('--json', action='store_true', help='强制输出 JSON 结果')
    output_group.add_argument('--table', action='store_true', help='强制输出文本结果')
    parser.add_argument('--force', action='store_true', help='忽略 check_interval_hours，强制执行远端检查')
    parser.add_argument('--version-url', default=VERSION_API_URL, help='版本接口地址')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT, help='单次请求超时时间（秒），默认 10')
    parser.add_argument('--retries', type=int, default=DEFAULT_RETRIES, help='最大请求次数，默认 3')

    try:
        args = parser.parse_args()
        validate_positive_int(args.timeout, '--timeout')
        validate_positive_int(args.retries, '--retries')
        local_info = read_local_version_info()
        cache_info = read_cache_info()
        now_ts = int(time.time())

        cached_result = None if args.force else build_cached_result(local_info, cache_info, now_ts, args.version_url)
        if cached_result is not None:
            result = cached_result
        else:
            try:
                remote_data = fetch_json(args.version_url, args.timeout, args.retries)
                result = build_remote_result(remote_data, local_info, args.version_url)
            except UpdateCheckError as remote_error:
                result = build_fallback_result(local_info, args.timeout, args.retries, remote_error, args.version_url)

            persist_check_cache(result, now_ts, args.version_url)
    except UpdateCheckError as error:
        print_error(str(error))
        sys.exit(error.exit_code)

    if args.table:
        print_table(result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
