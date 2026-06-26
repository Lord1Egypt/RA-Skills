#!/usr/bin/env python3
"""Skill security check CLI tool — Python 3.9+ (stdlib only)."""

import argparse
import hashlib
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================================
# Configuration
# ============================================================

API_BASE_URL = 'https://skill-sec.baidu.com'
API_PATH = '/v1/skill/security/results'
REQUEST_TIMEOUT = 10  # 10s
CONCURRENT_LIMIT = 5

# 渠道标识，由打包脚本注入（如 'openclaw-skill'）；None 表示无渠道（通用包）
_CHANNEL_ID = 'openclaw-skill'

# ============================================================
# Utilities
# ============================================================

_ssl_ctx = ssl.create_default_context()


def safe_json_parse(text):
    """Parse JSON text safely, raising a descriptive error on failure."""
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        raise Exception(f'响应解析失败（非JSON格式）: {text[:200]}')


def make_query_full_result(code, msg, **overrides):
    """Build a standard queryfull result dict with default counters."""
    result = {
        'code': code,
        'msg': msg,
        'ts': int(time.time() * 1000),
        'total': 0,
        'safe_count': 0,
        'danger_count': 0,
        'caution_count': 0,
        'error_count': 0,
        'results': [],
    }
    result.update(overrides)
    return result


def _build_compact(obj):
    """Build a compact JSON-serializable dict for normal (non-debug) output."""
    if 'results' in obj:
        # Scenario D (queryfull): batch summary
        return {
            'code': obj.get('code'),
            'msg': obj.get('msg'),
            'ts': obj.get('ts'),
            'total': obj.get('total'),
            'safe_count': obj.get('safe_count'),
            'danger_count': obj.get('danger_count'),
            'caution_count': obj.get('caution_count'),
            'error_count': obj.get('error_count'),
            'report_text': obj.get('report_text'),
        }
    # Scenario A/C: single query
    data = obj.get('data')
    first = data[0] if isinstance(data, list) and data else None
    report = obj.get('report')
    return {
        'code': obj.get('code'),
        'message': obj.get('message'),
        'ts': obj.get('ts'),
        'bd_confidence': first.get('bd_confidence') if first else None,
        'final_verdict': report.get('final_verdict') if report else None,
        'report_text': obj.get('report_text'),
    }


def output_result(obj):
    """Print result to stdout based on debug mode."""
    if _DEBUG:
        print(json.dumps(obj, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(_build_compact(obj), indent=2, ensure_ascii=False))


_DEBUG = False


def _debug_log(msg):
    """Print debug message to stderr only when debug mode is enabled."""
    if _DEBUG:
        print(msg, file=sys.stderr)


def output_and_exit(obj, exit_code):
    """Print result to stdout and exit with the given code."""
    if _DEBUG:
        print(json.dumps(obj, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(_build_compact(obj), indent=2, ensure_ascii=False))
    sys.exit(exit_code)


# ============================================================
# Report Builder
# ============================================================

_SOURCE_MAP = {
    'openclaw': 'ClawdHub',
    'github': 'GitHub',
    'appbuilder': '百度AppBuilder',
}

_CONFIDENCE_MAP = {
    'safe': {
        'verdict': '✅ 白名单(可信)',
        'final_verdict': '✅ 安全安装',
        'suggestion': '已通过安全检查，可安全安装',
    },
    'caution': {
        'verdict': '⚠️ 灰名单，谨慎安装',
        'final_verdict': '⚠️ 谨慎安装(需人工确认)',
        'suggestion': '存在潜在风险，建议人工审查后再安装',
    },
    'dangerous': {
        'verdict': '🚫 黑名单，❌ 不建议安装',
        'final_verdict': '❌ 不建议安装(需人工确认)',
        'suggestion': '发现严重安全风险，建议人工审查后再安装',
    },
}

_CONFIDENCE_DEFAULT = {
    'verdict': '❓ 未收录，不建议安装',
    'final_verdict': '❌ 不建议安装(需人工确认)',
    'suggestion': '尚未被安全系统收录，建议人工审查后再安装'
}


def _format_timestamp(ms):
    """Convert millisecond timestamp to UTC+8 formatted string."""
    import datetime
    if not ms:
        ms = int(time.time() * 1000)
    dt = datetime.datetime.utcfromtimestamp(ms / 1000) + datetime.timedelta(hours=8)
    return '[UTC+8 ' + dt.strftime('%Y-%m-%d %H:%M:%S') + ']'


def _build_overview(confidence, findings_count, virus_count):
    """Build the overview text based on confidence level."""
    if confidence == 'safe':
        return None
    if confidence == 'dangerous':
        text = '🚫 Skill存在安全风险'
        if findings_count > 0:
            text += f'，发现{findings_count}项危险行为'
        if virus_count > 0:
            text += f'，发现{virus_count}项病毒风险'
    elif confidence == 'caution':
        text = '⚠️ Skill存在潜在风险'
        if findings_count > 0:
            text += f'，发现{findings_count}项可疑行为'
    else:
        text = '❓ Skill未收录'
    return text


def build_report(data, ts=None):
    """Build a pre-processed report object from data[0] for the LLM template."""
    if not isinstance(data, list) or len(data) == 0:
        return None

    item = data[0]
    detail = item.get('detail') or {}
    confidence = (item.get('bd_confidence') or '').lower()
    mapped = _CONFIDENCE_MAP.get(confidence, _CONFIDENCE_DEFAULT)

    github = detail.get('github') or {}
    vt = detail.get('virustotal') or {}
    oc = detail.get('openclaw') or {}
    scanner = detail.get('skillscanner') or {}
    av = detail.get('antivirus') or {}

    vt_status = vt.get('vt_status')
    vt_describe = None
    if vt_status and vt_status != 'Benign' and vt_status != 'Pending' and vt.get('vt_describe'):
        vt_describe = vt['vt_describe']

    oc_status = oc.get('oc_status')
    oc_describe = oc.get('oc_describe') if (oc_status and oc_status != 'Benign') else None

    raw_findings = scanner.get('findings') or []
    findings = [
        {'severity': f.get('severity'), 'title': f.get('title'), 'description': f.get('description')}
        for f in raw_findings
    ]

    findings_count = scanner.get('findings_count') or len(findings)
    virus_count = av.get('virus_count') or 0
    virus_list = []
    if virus_count > 0 and isinstance(av.get('virus_details'), list):
        virus_list = [
            {'virus_name': v.get('virus_name'), 'file': v.get('file')}
            for v in av['virus_details']
        ]

    return {
        'name': item.get('slug'),
        'version': item.get('version'),
        'source': _SOURCE_MAP.get(item.get('source'), '其他'),
        'author': github.get('name'),
        'scanned_at': _format_timestamp(ts),
        'bd_confidence': confidence or None,
        'verdict': mapped['verdict'],
        'final_verdict': mapped['final_verdict'],
        'suggestion': mapped['suggestion'],
        'bd_describe': item.get('bd_describe'),
        'overview': _build_overview(confidence, findings_count, virus_count),
        'virustotal': {'status': vt_status, 'describe': vt_describe},
        'openclaw': {'status': oc_status, 'describe': oc_describe},
        'findings': findings,
        'antivirus': {'virus_count': virus_count, 'virus_list': virus_list},
    }


# ============================================================
# Report Text Formatter
# ============================================================

def format_single_report_text(report):
    """Render a single-skill report object into plain-text report string."""
    lines = []
    lines.append('🛡️ Skill安全守卫报告')
    lines.append('═══════════════════════════════════════')
    lines.append('📊 守卫摘要')
    lines.append('评估时间：' + (report.get('scanned_at') or '未知'))
    lines.append('Skill名称：' + (report.get('name') or '未知'))
    lines.append('来    源：' + (report.get('source') or '未知'))
    lines.append('作    者：' + (report.get('author') or '未知'))
    lines.append('版    本：' + (report.get('version') or '未知'))
    lines.append('评估结果：' + (report.get('verdict') or '未知'))

    overview = report.get('overview')
    if overview:
        lines.append('')
        lines.append('───────────────────────────────────────')
        lines.append('📕 评估结果概述')
        lines.append(overview)

        lines.append('')
        lines.append('───────────────────────────────────────')
        lines.append('🗒 安全评估详情')
        lines.append(report.get('bd_describe') or 'N/A')

        lines.append('')
        lines.append('评估过程')

        # VirusTotal
        vt = report.get('virustotal') or {}
        vt_line = '- VirusTotal：' + (vt.get('status') or 'N/A')
        if vt.get('describe'):
            vt_line += '，' + vt['describe']
        lines.append(vt_line)

        # OpenClaw
        oc = report.get('openclaw') or {}
        oc_line = '- OpenClaw：' + (oc.get('status') or 'N/A')
        if oc.get('describe'):
            oc_line += '，' + oc['describe']
        lines.append(oc_line)

        # Findings
        for f in (report.get('findings') or []):
            lines.append('- 发现' + (f.get('severity') or '未知')
                         + '行为，' + (f.get('title') or ''))
            if f.get('description'):
                lines.append('   - ' + f['description'])

        # Antivirus
        av = report.get('antivirus') or {}
        if av.get('virus_count', 0) > 0 and isinstance(av.get('virus_list'), list):
            for v in av['virus_list']:
                lines.append('- 病毒扫描：发现'
                             + (v.get('virus_name') or '未知病毒') + '，'
                             + (v.get('file') or '未知文件'))
        else:
            lines.append('- 病毒扫描：未检测到病毒')

    lines.append('')
    lines.append('───────────────────────────────────────')
    lines.append('🏁 最终裁决：')
    lines.append(report.get('final_verdict') or '未知')

    if overview:
        lines.append('')
        lines.append('💡 建议：' + (report.get('suggestion') or ''))
    lines.append('═══════════════════════════════════════')

    return '\n'.join(lines)


def format_not_indexed_report_text(slug):
    """Generate report text for skills not indexed in the security system."""
    now = _format_timestamp(int(time.time() * 1000))
    lines = []
    lines.append('🛡️ Skill安全守卫报告')
    lines.append('═══════════════════════════════════════')
    lines.append('📊 守卫摘要')
    lines.append('评估时间：' + now)
    lines.append('Skill名称：' + (slug or '未知'))
    lines.append('来    源：未知')
    lines.append('作    者：未知')
    lines.append('版    本：未知')
    lines.append('评估结果：❓ 未收录，不建议安装')
    lines.append('')
    lines.append('───────────────────────────────────────')
    lines.append('🏁 最终裁决：')
    lines.append('❌ 不建议安装(需人工确认)')
    lines.append('')
    lines.append('💡 建议：尚未被安全系统收录，建议人工审查后再安装')
    lines.append('═══════════════════════════════════════')
    return '\n'.join(lines)


def format_error_report_text(msg):
    """Generate report text for error scenarios."""
    now = _format_timestamp(int(time.time() * 1000))
    lines = []
    lines.append('🛡️ Skill安全守卫报告')
    lines.append('═══════════════════════════════════════')
    lines.append('📊 守卫摘要')
    lines.append('评估时间：' + now)
    lines.append('评估结果：❌ 安全检查失败')
    if msg:
        lines.append('')
        lines.append('错误信息：' + str(msg))
    lines.append('')
    lines.append('───────────────────────────────────────')
    lines.append('🏁 最终裁决：')
    lines.append('❌ 暂缓安装(安全检查未完成)')
    lines.append('')
    lines.append('💡 建议：安全检查服务调用失败，建议稍后重试，请勿跳过安全检查直接安装')
    lines.append('═══════════════════════════════════════')
    return '\n'.join(lines)


def _format_batch_item_text(report):
    """Render a single skill detail section within a batch report."""
    lines = []
    lines.append('───────────────────────────────────────')
    lines.append('📌 ' + (report.get('name') or '未知') + ' v'
                 + (report.get('version') or '未知'))
    lines.append('来源：' + (report.get('source') or '未知')
                 + ' | 作者：' + (report.get('author') or '未知'))
    lines.append('评估结果：' + (report.get('verdict') or '未知'))

    overview = report.get('overview')
    if overview:
        lines.append('')
        lines.append('📕 ' + overview)

        lines.append('')
        lines.append('🗒 ' + (report.get('bd_describe') or 'N/A'))

        lines.append('')
        lines.append('评估过程')

        vt = report.get('virustotal') or {}
        vt_line = '- VirusTotal：' + (vt.get('status') or 'N/A')
        if vt.get('describe'):
            vt_line += '，' + vt['describe']
        lines.append(vt_line)

        oc = report.get('openclaw') or {}
        oc_line = '- OpenClaw：' + (oc.get('status') or 'N/A')
        if oc.get('describe'):
            oc_line += '，' + oc['describe']
        lines.append(oc_line)

        for f in (report.get('findings') or []):
            lines.append('- 发现' + (f.get('severity') or '未知')
                         + '行为，' + (f.get('title') or ''))
            if f.get('description'):
                lines.append('   - ' + f['description'])

        av = report.get('antivirus') or {}
        if av.get('virus_count', 0) > 0 and isinstance(av.get('virus_list'), list):
            for v in av['virus_list']:
                lines.append('- 病毒扫描：发现'
                             + (v.get('virus_name') or '未知病毒') + '，'
                             + (v.get('file') or '未知文件'))
        else:
            lines.append('- 病毒扫描：未检测到病毒')

    lines.append('')
    lines.append('🏁 最终裁决：' + (report.get('final_verdict') or '未知'))
    lines.append('💡 建议：' + (report.get('suggestion') or ''))
    return '\n'.join(lines)


def format_batch_report_text(batch_result):
    """Render a batch query result into plain-text batch report string."""
    now = _format_timestamp(int(time.time() * 1000))
    danger_and_error = (batch_result.get('danger_count') or 0) \
        + (batch_result.get('error_count') or 0)
    lines = []

    lines.append('🛡️ Skill安全守卫报告')
    lines.append('═══════════════════════════════════════')
    lines.append('')
    lines.append('📊守卫摘要')
    lines.append('评估时间：' + now)
    lines.append('评估Skills总量：' + str(batch_result.get('total') or 0) + '个')
    lines.append(' ✅通过：' + str(batch_result.get('safe_count') or 0) + '个')
    lines.append(' 🚫不通过：' + str(danger_and_error) + '个')
    lines.append(' ⚠️需关注：' + str(batch_result.get('caution_count') or 0) + '个')
    lines.append('═══════════════════════════════════════')

    # 不通过 Skills
    lines.append('🚫不通过Skills（不建议安装，需人工确认）：')
    lines.append('')

    results = batch_result.get('results') or []
    danger_items = []
    for r in results:
        if not r.get('report'):
            if (r.get('code') == 'error'
                    or (r.get('code') == 'success'
                        and (not isinstance(r.get('data'), list)
                             or len(r['data']) == 0))):
                danger_items.append(r)
            continue
        c = (r['report'].get('bd_confidence') or '').lower()
        if c in ('dangerous', '', 'error'):
            danger_items.append(r)

    if not danger_items:
        lines.append('无')
    else:
        for item in danger_items:
            if item.get('report'):
                lines.append(_format_batch_item_text(item['report']))
            else:
                lines.append('───────────────────────────────────────')
                lines.append('📌 ' + (item.get('slug') or '未知'))
                lines.append('评估结果：❌ '
                             + (item.get('msg') or '安全检查失败'))
                lines.append('')
                lines.append('🏁 最终裁决：❌ 不建议安装(需人工确认)')
                lines.append('💡 建议：安全检查未通过，建议人工审查')

    lines.append('')
    lines.append('═══════════════════════════════════════')

    # 需关注 Skills
    lines.append('⚠️需关注Skills（需谨慎安装）：')
    lines.append('')

    caution_items = [
        r for r in results
        if r.get('report')
        and (r['report'].get('bd_confidence') or '').lower() == 'caution'
    ]

    if not caution_items:
        lines.append('无')
    else:
        for item in caution_items:
            lines.append(_format_batch_item_text(item['report']))

    lines.append('')
    lines.append('═══════════════════════════════════════')
    return '\n'.join(lines)


# ============================================================
# HTTP Client
# ============================================================

def make_request(url, timeout=REQUEST_TIMEOUT):
    """Send a GET request and return parsed JSON."""
    req = urllib.request.Request(url, method='GET')
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ssl_ctx) as resp:
            data = resp.read().decode('utf-8')
            return safe_json_parse(data)
    except urllib.error.HTTPError as e:
        body = ''
        try:
            body = e.read().decode('utf-8')[:200]
        except Exception:
            pass
        raise Exception(f'HTTP {e.code}: {body}')
    except urllib.error.URLError as e:
        raise Exception(f'请求失败: {e.reason}')


def _make_get_request(url, timeout=REQUEST_TIMEOUT):
    """Send a GET request with optional X-Caller header and return parsed JSON."""
    req = urllib.request.Request(url, method='GET')
    if _CHANNEL_ID:
        req.add_header('X-Caller', _CHANNEL_ID)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ssl_ctx) as resp:
            data = resp.read().decode('utf-8')
            return safe_json_parse(data)
    except urllib.error.HTTPError as e:
        body = ''
        try:
            body = e.read().decode('utf-8')[:200]
        except Exception:
            pass
        raise Exception(f'HTTP {e.code}: {body}')
    except urllib.error.URLError as e:
        raise Exception(f'请求失败: {e.reason}')


# ============================================================
# API: checkSkillSecurityFullResponse
# ============================================================

def check_skill_security_full_response(slug, version=None):
    """Query the security API for a skill by slug and optional version."""
    params = {'slug': slug}
    if version:
        params['version'] = version
    query_string = urllib.parse.urlencode(params)
    url = f'{API_BASE_URL}{API_PATH}?{query_string}'
    return _make_get_request(url)


# ============================================================
# Slug Extraction from SKILL.md
# ============================================================

def extract_slug_from_skill_md(dir_path):
    """Extract skill slug and version from _meta.json (preferred) or SKILL.md front-matter."""
    fallback_slug = os.path.basename(dir_path)

    # Step 1: 尝试从 _meta.json 读取
    meta_json_path = os.path.join(dir_path, '_meta.json')
    if os.path.isfile(meta_json_path):
        try:
            with open(meta_json_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            if meta.get('slug'):
                return meta['slug'], meta.get('version') or None
        except Exception:
            pass  # _meta.json 解析失败，继续回退

    # Step 2: 回退 - slug使用目录名，从SKILL.md提取version
    skill_md_path = os.path.join(dir_path, 'SKILL.md')
    if not os.path.isfile(skill_md_path):
        return fallback_slug, None

    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    fm_match = re.match(r'^---\r?\n([\s\S]*?)\r?\n---', content)
    if not fm_match:
        return fallback_slug, None

    fm = fm_match.group(1)
    version_match = re.search(r'^version:\s*(.+)$', fm, re.MULTILINE)
    version = version_match.group(1).strip() if version_match else None
    # 若顶层未找到，尝试 metadata.version
    if not version:
        meta_version_match = re.search(
            r'^metadata:\s*\r?\n(?:[ \t]+.*\r?\n)*?[ \t]+version:\s*(.+)$',
            fm, re.MULTILINE
        )
        if meta_version_match:
            version = meta_version_match.group(1).strip()
    if version and len(version) >= 2 and version[0] == version[-1] and version[0] in ('"', "'"):
        version = version[1:-1]
    return fallback_slug, version


# ============================================================
# Content SHA256 (directory-based, matches server-side algorithm)
# ============================================================

def compute_content_sha256(dir_path):
    """Compute content_sha256 for a skill directory, matching server-side algo."""
    # 1. Recursively collect all files (relative paths)
    files = []
    for root, dirs, filenames in os.walk(dir_path):
        dirs[:] = [d for d in dirs if d != '__MACOSX']
        for fname in filenames:
            abs_path = os.path.join(root, fname)
            rel = os.path.relpath(abs_path, dir_path)
            files.append(rel)

    # 2. Filter out top-level _meta.json, .clawhub/ directory and .DS_Store
    filtered = [
        f for f in files
        if f != '_meta.json'
        and not f.startswith('.clawhub' + os.sep)
        and not f.startswith('.clawhub/')
        and os.path.basename(f) != '.DS_Store'
    ]
    if not filtered:
        return ''

    # 3. Normalize paths and sort lexicographically
    normalized = []
    for f in filtered:
        p = f.replace('\\', '/')
        p = os.path.normpath(p).replace('\\', '/')
        p = p.lstrip('/')
        normalized.append(p)
    normalized.sort()

    # 4. Build manifest: "{relativePath}\n{fileSHA256}\n" for each file
    manifest = ''
    for rel in normalized:
        abs_path = os.path.join(dir_path, rel)
        h = hashlib.sha256()
        with open(abs_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
        manifest += f'{rel}\n{h.hexdigest()}\n'

    # 5. SHA256 of the entire manifest
    return hashlib.sha256(manifest.encode('utf-8')).hexdigest()


# ============================================================
# API: check_skill_security_by_sha256
# ============================================================

def check_skill_security_by_sha256(sha256_val):
    """Query the security API for a skill by content SHA256."""
    params = {'sha256': sha256_val}
    query_string = urllib.parse.urlencode(params)
    url = f'{API_BASE_URL}{API_PATH}?{query_string}'
    return _make_get_request(url)


# ============================================================
# Concurrent execution with limit
# ============================================================

def parallel_limit(task_fns, limit):
    """Run callables concurrently (max *limit*) and return results in order."""
    results = [None] * len(task_fns)
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_to_index = {executor.submit(fn): i for i, fn in enumerate(task_fns)}
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            try:
                results[idx] = future.result()
            except Exception:
                results[idx] = {'__error': True}
    return results


# ============================================================
# QueryFull: Batch query all subdirectories by slug (Scenario C)
# ============================================================

def classify_confidence(response):
    """Classify a skill response into safe, dangerous, caution, or error."""
    if (response.get('code') == 'success'
            and isinstance(response.get('data'), list)
            and len(response['data']) > 0):
        c = (response['data'][0].get('bd_confidence') or '').lower()
        if c in ('safe', 'trusted'):
            return 'safe'
        if c == 'dangerous':
            return 'dangerous'
        if c == 'caution':
            return 'caution'
    return 'error'


def query_full_directory(dir_path):
    """Batch query security results for all skill subdirectories."""
    if not dir_path or not os.path.exists(dir_path):
        return make_query_full_result('error', f'❌ 错误：目录路径不存在 -- {dir_path or "(空)"}')

    if not os.path.isdir(dir_path):
        return make_query_full_result('error', f'❌ 错误：路径不是目录 -- {dir_path}')

    # List immediate subdirectories, skip hidden dirs
    entries = [
        name for name in sorted(os.listdir(dir_path))
        if not name.startswith('.') and name != '__MACOSX' and os.path.isdir(os.path.join(dir_path, name))
    ]

    if not entries:
        return make_query_full_result('success', 'queryfull completed, no skill subdirectories found')

    # Build task callables
    def make_task(name):
        def task():
            skill_dir = os.path.join(dir_path, name)
            slug, version = extract_slug_from_skill_md(skill_dir)
            try:
                response = check_skill_security_full_response(slug, version)
                result = {'slug': slug, **response}

                # SHA256 fallback: when slug query returns empty data, try content_sha256
                if (response.get('code') == 'success'
                        and isinstance(response.get('data'), list)
                        and len(response['data']) == 0):
                    try:
                        content_sha256 = compute_content_sha256(skill_dir)
                        if content_sha256:
                            sha256_resp = check_skill_security_by_sha256(content_sha256)
                            if (sha256_resp.get('code') == 'success'
                                    and isinstance(sha256_resp.get('data'), list)
                                    and len(sha256_resp['data']) > 0):
                                result = {'slug': slug, **sha256_resp}
                    except Exception:
                        pass  # SHA256 fallback failed, keep original empty result

                report = build_report(result.get('data'), result.get('ts'))
                if report:
                    result['report'] = report
                return result
            except Exception as e:
                return {'slug': slug, 'code': 'error', 'msg': str(e), 'data': []}
        return task

    task_fns = [make_task(name) for name in entries]
    results = parallel_limit(task_fns, CONCURRENT_LIMIT)

    # Classify results
    safe_count = 0
    danger_count = 0
    caution_count = 0
    error_count = 0
    for r in results:
        category = classify_confidence(r)
        if category == 'safe':
            safe_count += 1
        elif category == 'dangerous':
            danger_count += 1
        elif category == 'caution':
            caution_count += 1
        else:
            error_count += 1

    return make_query_full_result(
        'success', 'queryfull completed',
        total=len(entries),
        safe_count=safe_count,
        danger_count=danger_count,
        caution_count=caution_count,
        error_count=error_count,
        results=results,
    )


# ============================================================
# QuerySingle: Query one skill directory by slug (Scenario A2)
# ============================================================

def query_single_directory(dir_path):
    """Query security results for a single skill directory."""
    if not dir_path or not os.path.exists(dir_path):
        return {
            'code': 'error',
            'msg': f'❌ 错误：目录路径不存在 -- {dir_path or "(空)"}',
            'ts': int(time.time() * 1000),
            'data': [],
        }

    if not os.path.isdir(dir_path):
        return {
            'code': 'error',
            'msg': f'❌ 错误：路径不是目录 -- {dir_path}',
            'ts': int(time.time() * 1000),
            'data': [],
        }

    slug, version = extract_slug_from_skill_md(dir_path)

    try:
        response = check_skill_security_full_response(slug, version)
        result = {**response}

        # SHA256 fallback: when slug query returns empty data
        if (response.get('code') == 'success'
                and isinstance(response.get('data'), list)
                and len(response['data']) == 0):
            try:
                content_sha256 = compute_content_sha256(dir_path)
                _debug_log(
                    f'[sha256-fallback] slug={slug}, contentSha256='
                    f'{content_sha256 or "(empty)"}'
                )
                if content_sha256:
                    sha256_resp = check_skill_security_by_sha256(
                        content_sha256
                    )
                    data_len = (
                        len(sha256_resp['data'])
                        if isinstance(sha256_resp.get('data'), list)
                        else 'N/A'
                    )
                    _debug_log(
                        f'[sha256-fallback] slug={slug},'
                        f' sha256 query result: code={sha256_resp.get("code")},'
                        f' data.length={data_len}'
                    )
                    if (sha256_resp.get('code') == 'success'
                            and isinstance(sha256_resp.get('data'), list)
                            and len(sha256_resp['data']) > 0):
                        result = {**sha256_resp}
            except Exception as fallback_err:
                _debug_log(
                    f'[sha256-fallback] slug={slug},'
                    f' fallback error: {fallback_err}'
                )

        report = build_report(result.get('data'), result.get('ts'))
        if report:
            result['report'] = report
        return result
    except Exception as error:
        return {
            'code': 'error',
            'msg': f'🚫 安全检查服务调用失败：{error}',
            'ts': int(time.time() * 1000),
            'data': [],
        }


# ============================================================
# CLI Entry Point
# ============================================================

def parse_args():
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Skill security check CLI',
        add_help=False,
    )
    parser.add_argument('--slug', default=None)
    parser.add_argument('--version', default=None)
    parser.add_argument('--action', default=None)
    parser.add_argument('--file', default=None)
    parser.add_argument('--debug', action='store_true', default=False)
    return parser.parse_args()


def main():
    """CLI entry point dispatching to queryfull, query, or slug-query."""
    global _DEBUG
    args = parse_args()
    _DEBUG = args.debug

    if args.action == 'queryfull':
        # Batch query all subdirectories by slug
        if not args.file:
            qf_result = make_query_full_result(
                'error',
                '❌ 错误：--action queryfull 需要提供 --file 参数（skills 父目录）\n'
                '用法：python3 check.py --action queryfull --file "/path/to/skills"',
            )
            qf_result['report_text'] = format_error_report_text(qf_result['msg'])
            output_and_exit(qf_result, 2)

        response = query_full_directory(args.file)
        response['report_text'] = format_batch_report_text(response)
        output_result(response)

        # Exit code: 0 if all safe and total > 0, 1 otherwise
        all_safe = (
            response.get('code') == 'success'
            and response.get('total', 0) > 0
            and response.get('safe_count', 0) == response.get('total', 0)
        )
        sys.exit(0 if all_safe else 1)

    elif args.action == 'query':
        # Single directory query
        if not args.file:
            err_msg = (
                '❌ 错误：--action query 需要提供 --file 参数（skill 目录路径）\n'
                '用法：python3 check.py --action query --file "/path/to/skill-dir"'
            )
            output_and_exit({
                'code': 'error',
                'msg': err_msg,
                'ts': int(time.time() * 1000),
                'data': [],
                'report_text': format_error_report_text(err_msg),
            }, 2)

        response = query_single_directory(args.file)
        if response.get('report'):
            response['report_text'] = format_single_report_text(
                response['report']
            )
        elif response.get('code') == 'error':
            response['report_text'] = format_error_report_text(
                response.get('msg')
            )
        else:
            response['report_text'] = format_not_indexed_report_text(
                args.file
            )
        output_result(response)

        if (response.get('code') == 'success'
                and isinstance(response.get('data'), list)
                and len(response['data']) > 0):
            bd_confidence = (response['data'][0].get('bd_confidence') or '').lower()
            safe = bd_confidence in ('safe', 'trusted')
            sys.exit(0 if safe else 1)
        else:
            sys.exit(1)

    else:
        # Slug query flow
        if not args.slug:
            err_msg = (
                '❌ 错误：缺少必填参数 --slug\n'
                "用法：python3 check.py --slug 'skill-slug' [--version '1.0.0']"
            )
            output_and_exit({
                'code': 'error',
                'msg': err_msg,
                'ts': int(time.time() * 1000),
                'data': [],
                'report_text': format_error_report_text(err_msg),
            }, 2)

        try:
            response = check_skill_security_full_response(args.slug, args.version)
            report = build_report(response.get('data'), response.get('ts'))
            if report:
                response['report'] = report
                response['report_text'] = format_single_report_text(report)
            else:
                response['report_text'] = format_not_indexed_report_text(
                    args.slug
                )
            output_result(response)

            # Determine exit code based on bd_confidence
            if (response.get('code') == 'success'
                    and isinstance(response.get('data'), list)
                    and len(response['data']) > 0):
                item = response['data'][0]
                bd_confidence = (item.get('bd_confidence') or '').lower()
                safe = bd_confidence in ('safe', 'trusted')
                sys.exit(0 if safe else 1)
            else:
                sys.exit(1)
        except SystemExit:
            raise
        except Exception as error:
            err_msg = f'🚫 安全检查服务调用失败：{error}'
            output_and_exit({
                'code': 'error',
                'msg': err_msg,
                'ts': int(time.time() * 1000),
                'data': [],
                'report_text': format_error_report_text(err_msg),
            }, 2)


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception as err:
        err_msg = f'❌ 脚本执行异常：{err}'
        output_and_exit({
            'code': 'error',
            'msg': err_msg,
            'ts': int(time.time() * 1000),
            'data': [],
            'report_text': format_error_report_text(err_msg),
        }, 2)