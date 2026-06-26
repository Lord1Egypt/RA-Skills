#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import plistlib
import re
import subprocess
from collections import defaultdict
from datetime import datetime
from http.client import IncompleteRead, RemoteDisconnected
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from paths import favorites_paths

PATHS = favorites_paths()
WORKSPACE_ROOT = PATHS['workspace_root']
ENTRIES_DIR = PATHS['entries_dir']
SNAPSHOT_DIR = PATHS['snapshots_dir']
REPORT_DIR = PATHS['reports_dir']
CACHE_PATH = PATHS['favorites_root'] / 'enrichment-cache.json'
TZ = datetime.now().astimezone().tzinfo
ALLOWED = re.compile(r'[^a-z0-9._-]+')
USER_AGENT = 'favorites-curator/2.0 (+local-first catalog)'


def now_iso():
    return datetime.now(TZ).replace(microsecond=0).isoformat()


def ensure_dirs():
    for path in (ENTRIES_DIR, SNAPSHOT_DIR, REPORT_DIR):
        path.mkdir(parents=True, exist_ok=True)


def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def slugify(value):
    value = value.strip().lower().replace(' ', '-')
    value = ALLOWED.sub('-', value)
    value = re.sub(r'-{2,}', '-', value).strip('-')
    return value or 'unknown'


def iso_from_ts(ts):
    if ts is None:
        return ''
    return datetime.fromtimestamp(ts, TZ).replace(microsecond=0).isoformat()


def stat_times(path):
    try:
        stat = Path(path).stat()
    except OSError:
        return '', ''
    return iso_from_ts(stat.st_ctime), iso_from_ts(stat.st_mtime)


def yaml_quote(value):
    if value is None:
        return '""'
    text = str(value)
    text = text.replace('\\', '\\\\').replace('"', '\\"')
    return f'"{text}"'


def dump_yaml_like(value, indent=0):
    prefix = ' ' * indent
    lines = []
    if isinstance(value, list):
        if not value:
            return [prefix + '[]']
        for item in value:
            if isinstance(item, (dict, list)):
                nested = dump_yaml_like(item, indent + 2)
                first = nested[0].lstrip()
                lines.append(prefix + '- ' + first)
                lines.extend(nested[1:])
            else:
                lines.append(prefix + '- ' + yaml_quote(item))
        return lines
    if isinstance(value, dict):
        if not value:
            return [prefix + '{}']
        for key in sorted(value):
            item = value[key]
            if isinstance(item, (dict, list)):
                nested = dump_yaml_like(item, indent + 2)
                lines.append(prefix + f'{key}:')
                lines.extend(nested)
            else:
                lines.append(prefix + f'{key}: {yaml_quote(item)}')
        return lines
    return [prefix + yaml_quote(value)]


def dump_frontmatter(data):
    lines = ['---']
    order = [
        'schema_version', 'item_id', 'canonical_key', 'name', 'author', 'data_type', 'source_name',
        'source_kind', 'source_ref', 'install_path', 'install_paths', 'observed_locations',
        'variants', 'merged_from_count', 'variant_source_names', 'install_time', 'update_time',
        'summary', 'simple_usage', 'source_url', 'canonical_source_url', 'content_fingerprint',
        'content_diff_status', 'skill_variant_analysis', 'tags', 'field_sources',
        'created_at', 'last_scanned_at', 'score', 'notable_reason'
    ]
    for key in order:
        if key not in data:
            continue
        value = data[key]
        if isinstance(value, (list, dict)):
            lines.append(f'{key}:')
            lines.extend(dump_yaml_like(value, 2))
        else:
            lines.append(f'{key}: {yaml_quote(value)}')
    lines.append('---')
    return '\n'.join(lines)


def parse_skill_frontmatter(path):
    try:
        text = path.read_text(encoding='utf-8')
    except OSError:
        return {}
    if not text.startswith('---\n'):
        return {}
    end = text.find('\n---', 4)
    if end == -1:
        return {}
    lines = text[4:end].splitlines()
    result = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if ':' not in line:
            i += 1
            continue
        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()
        if value in {'|', '>'}:
            block = []
            i += 1
            while i < len(lines) and (lines[i].startswith('  ') or not lines[i].strip()):
                block.append(lines[i][2:] if lines[i].startswith('  ') else '')
                i += 1
            result[key] = ' '.join(part.strip() for part in block if part.strip())
            continue
        result[key] = value.strip('"')
        i += 1
    return result


def read_text_snippet(path, limit=400):
    try:
        text = path.read_text(encoding='utf-8', errors='ignore').strip()
    except OSError:
        return ''
    return re.sub(r'\s+', ' ', text)[:limit]


def read_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return default


class EnrichmentStore:
    def __init__(self, path):
        self.path = path
        self.payload = read_json(path, {'github': {}, 'url_meta': {}})

    def get_github(self, key):
        return self.payload.setdefault('github', {}).get(key)

    def set_github(self, key, value):
        self.payload.setdefault('github', {})[key] = value

    def get_url_meta(self, key):
        return self.payload.setdefault('url_meta', {}).get(key)

    def set_url_meta(self, key, value):
        self.payload.setdefault('url_meta', {})[key] = value

    def save(self):
        self.path.write_text(json.dumps(self.payload, indent=2, ensure_ascii=True), encoding='utf-8')


ENRICHMENT = EnrichmentStore(CACHE_PATH)


def fetch_json(url):
    req = Request(url, headers={'User-Agent': USER_AGENT, 'Accept': 'application/vnd.github+json'})
    with urlopen(req, timeout=8) as resp:
        return json.loads(resp.read().decode('utf-8'))


def fetch_text(url):
    req = Request(url, headers={'User-Agent': USER_AGENT})
    with urlopen(req, timeout=8) as resp:
        content_type = resp.headers.get_content_charset() or 'utf-8'
        return resp.read().decode(content_type, errors='ignore')


GITHUB_RE = re.compile(r'github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/#]+?)(?:\.git)?(?:$|[?#/])', re.I)


def github_repo_key(url):
    if not url:
        return ''
    match = GITHUB_RE.search(url)
    if not match:
        return ''
    owner = match.group('owner').strip()
    repo = match.group('repo').strip()
    return f'{owner}/{repo}'


def normalize_url(url):
    if not url:
        return ''
    url = url.strip()
    if url.startswith('git@github.com:'):
        url = 'https://github.com/' + url.split(':', 1)[1]
    if url.endswith('.git'):
        url = url[:-4]
    parsed = urlparse(url)
    if not parsed.scheme:
        return url
    return f'{parsed.scheme}://{parsed.netloc.lower()}{parsed.path}'.rstrip('/')


def github_enrichment(remote_url):
    repo_key = github_repo_key(remote_url)
    if not repo_key:
        return None
    cached = ENRICHMENT.get_github(repo_key)
    if cached:
        return cached
    try:
        data = fetch_json(f'https://api.github.com/repos/{repo_key}')
    except (HTTPError, URLError, TimeoutError, IncompleteRead, RemoteDisconnected, json.JSONDecodeError, OSError):
        return None
    payload = {
        'author': data.get('owner', {}).get('login', ''),
        'summary': data.get('description', '') or '',
        'source_url': data.get('html_url', '') or '',
        'simple_usage': f'git clone {data.get("clone_url", remote_url)}',
        'fetched_at': now_iso(),
    }
    ENRICHMENT.set_github(repo_key, payload)
    return payload


def extract_meta_description(html):
    patterns = [
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']+)["\']',
        r'<title>([^<]+)</title>',
    ]
    for pattern in patterns:
        match = re.search(pattern, html, flags=re.I)
        if match:
            return re.sub(r'\s+', ' ', match.group(1)).strip()
    return ''


def extract_site_name(html):
    patterns = [
        r'<meta[^>]+property=["\']og:site_name["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+name=["\']application-name["\'][^>]+content=["\']([^"\']+)["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, html, flags=re.I)
        if match:
            return re.sub(r'\s+', ' ', match.group(1)).strip()
    parsed = re.search(r'<title>([^<]+)</title>', html, flags=re.I)
    if parsed:
        title = re.sub(r'\s+', ' ', parsed.group(1)).strip()
        return title.split(' - ')[-1][:120]
    return ''


def url_meta_enrichment(url):
    normalized = normalize_url(url)
    if not normalized or 'github.com/' in normalized:
        return None
    cached = ENRICHMENT.get_url_meta(normalized)
    if cached:
        return cached
    try:
        html = fetch_text(normalized)
    except (HTTPError, URLError, TimeoutError, IncompleteRead, RemoteDisconnected, UnicodeDecodeError, OSError):
        return None
    payload = {
        'author': extract_site_name(html),
        'summary': extract_meta_description(html),
        'source_url': normalized,
        'fetched_at': now_iso(),
    }
    ENRICHMENT.set_url_meta(normalized, payload)
    return payload


def is_missing(value):
    return not value or str(value).strip() in {'', 'inferred', 'unknown'}


def summary_quality(value):
    text = (value or '').strip()
    if not text:
        return 0
    score = min(len(text), 160)
    if text.lower().startswith('installed '):
        score -= 30
    if 'local ' in text.lower():
        score -= 15
    return score


def maybe_apply_enrichment(entry, enrichment, source_label):
    if not enrichment:
        return
    if enrichment.get('author') and (is_missing(entry['author']) or entry['author'] in {'Homebrew'}):
        entry['author'] = enrichment['author']
        entry['field_sources']['author'] = source_label
    enriched_summary = enrichment.get('summary', '').strip()
    if enriched_summary and summary_quality(enriched_summary) > summary_quality(entry.get('summary', '')) + 10:
        entry['summary'] = enriched_summary
        entry['field_sources']['summary'] = source_label
    if enrichment.get('source_url') and not entry.get('source_url'):
        entry['source_url'] = enrichment['source_url']
        entry['field_sources']['source_url'] = source_label
    if enrichment.get('simple_usage') and is_missing(entry.get('simple_usage', '')):
        entry['simple_usage'] = enrichment['simple_usage']
        entry['field_sources']['simple_usage'] = source_label


def body_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]


def file_sha(path):
    try:
        data = path.read_bytes()
    except OSError:
        return ''
    return hashlib.sha256(data).hexdigest()[:16]


def list_script_fingerprints(base):
    script_dir = base / 'scripts'
    result = {}
    if not script_dir.exists():
        return result
    for path in sorted(script_dir.rglob('*')):
        if not path.is_file():
            continue
        rel = str(path.relative_to(base)).replace(os.sep, '/')
        parts = Path(rel).parts
        if '__pycache__' in parts or rel.endswith(('.pyc', '.pyo')):
            continue
        result[rel] = file_sha(path)
    return result


def skill_variant_metadata(path):
    skill_md = path / 'SKILL.md'
    text = ''
    if skill_md.exists():
        try:
            text = skill_md.read_text(encoding='utf-8')
        except OSError:
            text = ''
    return {
        'skill_md_hash': body_hash(text) if text else '',
        'skill_md_present': bool(text),
        'script_files': list_script_fingerprints(path),
    }


def author_from_package(package):
    author = package.get('author', 'inferred')
    if isinstance(author, dict):
        return author.get('name', 'inferred')
    return author


def url_from_package(package):
    for key in ('homepage', 'repository', 'bugs'):
        value = package.get(key)
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            for sub_key in ('url', 'web'):
                if value.get(sub_key):
                    return value[sub_key]
    return ''


def build_entry(name, author, data_type, source_name, source_kind, source_ref, install_path,
                install_time, update_time, summary, simple_usage, source_url, field_sources,
                tags=None, notes=None, variant_meta=None):
    slug = slugify(Path(install_path).name if install_path else name)
    created_at = now_iso()
    return {
        'schema_version': '2',
        'item_id': '',
        'canonical_key': '',
        'name': name,
        'author': author or 'inferred',
        'data_type': data_type,
        'source_name': source_name,
        'source_kind': source_kind,
        'source_ref': source_ref,
        'install_path': install_path,
        'install_paths': [install_path] if install_path else [],
        'observed_locations': [{
            'source_name': source_name,
            'source_kind': source_kind,
            'source_ref': source_ref,
            'install_path': install_path,
        }],
        'variants': [],
        'merged_from_count': 1,
        'variant_source_names': [source_name],
        'install_time': install_time,
        'update_time': update_time,
        'summary': summary,
        'simple_usage': simple_usage,
        'source_url': source_url,
        'canonical_source_url': normalize_url(source_url),
        'content_fingerprint': variant_meta or {},
        'content_diff_status': 'not-compared',
        'skill_variant_analysis': {},
        'tags': tags or [],
        'field_sources': field_sources,
        'created_at': created_at,
        'last_scanned_at': created_at,
        'score': 0,
        'notable_reason': '',
        'notes': notes or [],
        'slug': slug,
        'entry_filename': '',
    }


def git_root_entries():
    base = Path.home() / 'ai'
    if not base.exists():
        return []
    entries = []
    for child in sorted(base.iterdir()):
        git_dir = child / '.git'
        if not child.is_dir() or not git_dir.exists():
            continue
        name = child.name
        author = 'inferred'
        update_time = ''
        source_url = ''
        summary = ''
        simple_usage = 'git -C {} status'.format(child)
        field_sources = {'author': 'inferred', 'summary': 'inferred', 'simple_usage': 'inferred'}

        log = run(['git', '-C', str(child), 'log', '-1', '--format=%an|%aI|%s'])
        if log and log.stdout.strip():
            parts = log.stdout.strip().split('|', 2)
            if len(parts) == 3:
                author, update_time, subject = parts
                summary = subject
                field_sources['author'] = 'git_log'
                field_sources['summary'] = 'git_log_subject'
        remote = run(['git', '-C', str(child), 'remote', 'get-url', 'origin'])
        if remote and remote.stdout.strip():
            source_url = remote.stdout.strip()
            field_sources['source_url'] = 'git_remote_origin'
        install_time, path_update = stat_times(child)
        if not update_time:
            update_time = path_update
        entry = build_entry(
            name=name,
            author=author,
            data_type='git-repo',
            source_name='ai',
            source_kind='git',
            source_ref=str(child),
            install_path=str(child),
            install_time=install_time,
            update_time=update_time,
            summary=summary or 'Local git repository under ~/ai.',
            simple_usage=simple_usage,
            source_url=source_url,
            field_sources=field_sources,
            notes=['Detected from ~/ai.', 'Summary or author may be inferred from the latest commit.'],
        )
        maybe_apply_enrichment(entry, github_enrichment(source_url), 'github_api')
        if entry.get('source_url'):
            maybe_apply_enrichment(entry, url_meta_enrichment(entry['source_url']), 'vendor_homepage')
        entries.append(entry)
    return entries


def brew_entries():
    result = run(['brew', 'info', '--json=v2', '--installed'])
    if not result:
        return []
    data = json.loads(result.stdout)
    entries = []
    for formula in data.get('formulae', []):
        name = formula.get('name', 'unknown')
        installed = formula.get('installed', [])
        install_path = ''
        install_time = ''
        update_time = ''
        if installed:
            first = installed[-1]
            install_path = first.get('prefix', '') or formula.get('installed_prefix', '')
            _, update_time = stat_times(install_path or formula.get('full_name', ''))
        field_sources = {'author': 'brew_tap', 'summary': 'brew_desc', 'simple_usage': 'inferred'}
        if install_path and not install_time:
            install_time, _ = stat_times(install_path)
        tap = formula.get('tap', '') or 'Homebrew'
        source_url = formula.get('homepage', '')
        if source_url:
            field_sources['source_url'] = 'brew_homepage'
        entry = build_entry(
            name=name,
            author=tap,
            data_type='brew-formula',
            source_name='brew',
            source_kind='brew-formula',
            source_ref=name,
            install_path=install_path,
            install_time=install_time,
            update_time=update_time,
            summary=formula.get('desc', '') or 'Installed brew formula.',
            simple_usage=f'brew info {name}',
            source_url=source_url,
            field_sources=field_sources,
            tags=['brew', 'formula'],
            notes=['Detected from brew installed formulae.'],
        )
        maybe_apply_enrichment(entry, github_enrichment(source_url), 'github_api')
        if entry.get('source_url'):
            maybe_apply_enrichment(entry, url_meta_enrichment(entry['source_url']), 'vendor_homepage')
        entries.append(entry)
    for cask in data.get('casks', []):
        name = cask.get('token', 'unknown')
        artifacts = cask.get('artifacts', [])
        install_path = ''
        for item in artifacts:
            if isinstance(item, list) and item and str(item[0]).endswith('.app'):
                candidate = Path('/Applications') / item[0]
                if candidate.exists():
                    install_path = str(candidate)
                    break
        if not install_path:
            install_path = str(Path('/opt/homebrew/Caskroom') / name)
        install_time, update_time = stat_times(install_path)
        source_url = cask.get('homepage', '')
        field_sources = {'author': 'brew_tap', 'summary': 'brew_desc', 'simple_usage': 'inferred'}
        if source_url:
            field_sources['source_url'] = 'brew_homepage'
        entry = build_entry(
            name=name,
            author=cask.get('tap', '') or 'Homebrew',
            data_type='brew-cask',
            source_name='brew',
            source_kind='brew-cask',
            source_ref=name,
            install_path=install_path,
            install_time=install_time,
            update_time=update_time,
            summary=cask.get('desc', '') or 'Installed brew cask.',
            simple_usage=f'brew info --cask {name}',
            source_url=source_url,
            field_sources=field_sources,
            tags=['brew', 'cask'],
            notes=['Detected from brew installed casks.'],
        )
        maybe_apply_enrichment(entry, github_enrichment(source_url), 'github_api')
        if entry.get('source_url'):
            maybe_apply_enrichment(entry, url_meta_enrichment(entry['source_url']), 'vendor_homepage')
        entries.append(entry)
    return entries


def app_entries():
    entries = []
    for source_name, base in [('system-apps', Path('/Applications')), ('user-apps', Path.home() / 'Applications')]:
        if not base.exists():
            continue
        for app in sorted(base.glob('*.app')):
            info_plist = app / 'Contents' / 'Info.plist'
            meta = {}
            if info_plist.exists():
                try:
                    with info_plist.open('rb') as handle:
                        meta = plistlib.load(handle)
                except Exception:
                    meta = {}
            name = meta.get('CFBundleDisplayName') or meta.get('CFBundleName') or app.stem
            bundle_id = meta.get('CFBundleIdentifier', 'inferred')
            summary = meta.get('CFBundleGetInfoString', '') or meta.get('NSHumanReadableCopyright', '')
            source_url = meta.get('SUFeedURL', '') or meta.get('SUOriginalFeedURL', '') or ''
            install_time, update_time = stat_times(app)
            field_sources = {'author': 'bundle_identifier', 'summary': 'info_plist_or_inferred', 'simple_usage': 'inferred'}
            if source_url:
                field_sources['source_url'] = 'info_plist_feed_url'
            entry = build_entry(
                name=name,
                author=bundle_id,
                data_type='app',
                source_name=source_name,
                source_kind='app-bundle',
                source_ref=str(app),
                install_path=str(app),
                install_time=install_time,
                update_time=update_time,
                summary=summary or 'Installed application bundle.',
                simple_usage=f'open -a "{name}"',
                source_url=source_url,
                field_sources=field_sources,
                tags=['app'],
                notes=['Detected from application bundle metadata.'],
            )
            if entry.get('source_url'):
                maybe_apply_enrichment(entry, github_enrichment(entry['source_url']), 'github_api')
                maybe_apply_enrichment(entry, url_meta_enrichment(entry['source_url']), 'vendor_homepage')
            entries.append(entry)
    return entries


def skill_entries():
    sources = [
        ('codex-skills', Path.home() / '.codex' / 'skills'),
        ('claude-skills', Path.home() / '.claude' / 'skills'),
        ('agents-skills', Path.home() / '.agents' / 'skills'),
        ('workspace-skills', Path.home() / '.openclaw' / 'workspace' / 'skills'),
    ]
    entries = []
    for source_name, base in sources:
        if not base.exists():
            continue
        for child in sorted(base.iterdir()):
            if child.name.startswith('.') or not child.is_dir():
                continue
            skill_md = child / 'SKILL.md'
            fm = parse_skill_frontmatter(skill_md) if skill_md.exists() else {}
            install_time, update_time = stat_times(child)
            summary = fm.get('description', '')
            notes = ['Detected from a skill directory.']
            if not summary:
                summary = 'Local skill directory.'
                notes.append('Description inferred because SKILL.md frontmatter was missing or complex.')
            entry = build_entry(
                name=fm.get('name', child.name),
                author='inferred',
                data_type='skill',
                source_name=source_name,
                source_kind='skill-dir',
                source_ref=str(child),
                install_path=str(child),
                install_time=install_time,
                update_time=update_time,
                summary=summary,
                simple_usage=f'read {skill_md}' if skill_md.exists() else f'ls {child}',
                source_url='',
                field_sources={'author': 'inferred', 'summary': 'skill_frontmatter_or_inferred', 'simple_usage': 'inferred'},
                tags=['skill'],
                notes=notes,
                variant_meta=skill_variant_metadata(child),
            )
            entries.append(entry)
    return entries


def extension_entries():
    base = Path.home() / '.openclaw' / 'extensions'
    if not base.exists():
        return []
    entries = []
    for child in sorted(base.iterdir()):
        if child.name.startswith('.') or not child.is_dir():
            continue
        package_json = child / 'package.json'
        package = {}
        if package_json.exists():
            try:
                package = json.loads(package_json.read_text(encoding='utf-8'))
            except Exception:
                package = {}
        install_time, update_time = stat_times(child)
        entry = build_entry(
            name=package.get('name', child.name),
            author=author_from_package(package),
            data_type='extension',
            source_name='extensions',
            source_kind='extension-dir',
            source_ref=str(child),
            install_path=str(child),
            install_time=install_time,
            update_time=update_time,
            summary=package.get('description', '') or 'OpenClaw extension directory.',
            simple_usage=f'ls {child}',
            source_url=url_from_package(package),
            field_sources={'author': 'package_json_or_inferred', 'summary': 'package_json_or_inferred', 'simple_usage': 'inferred'},
            tags=['extension'],
            notes=['Detected from ~/.openclaw/extensions.'],
        )
        if entry.get('source_url'):
            maybe_apply_enrichment(entry, github_enrichment(entry['source_url']), 'github_api')
            maybe_apply_enrichment(entry, url_meta_enrichment(entry['source_url']), 'vendor_homepage')
        entries.append(entry)
    return entries


def hook_entries():
    base = Path.home() / '.openclaw' / 'hooks'
    if not base.exists():
        return []
    entries = []
    for child in sorted(base.iterdir()):
        if child.name.startswith('.'):
            continue
        install_time, update_time = stat_times(child)
        usage = 'bash {}'.format(child) if child.is_file() else f'ls {child}'
        summary = 'OpenClaw hook.'
        if child.is_file():
            first_line = read_text_snippet(child, 120)
            if first_line:
                summary = first_line
        entries.append(build_entry(
            name=child.name,
            author='inferred',
            data_type='hook',
            source_name='hooks',
            source_kind='hook-file' if child.is_file() else 'hook-dir',
            source_ref=str(child),
            install_path=str(child),
            install_time=install_time,
            update_time=update_time,
            summary=summary,
            simple_usage=usage,
            source_url='',
            field_sources={'author': 'inferred', 'summary': 'file_snippet_or_inferred', 'simple_usage': 'inferred'},
            tags=['hook'],
            notes=['Detected from ~/.openclaw/hooks.'],
        ))
    return entries


def canonical_key(entry):
    url = normalize_url(entry.get('source_url', ''))
    if url:
        return f'url:{url}'
    if entry['data_type'] == 'skill':
        return f'skill:{slugify(entry["name"])}'
    install_name = Path(entry.get('install_path') or entry['name']).name
    install_slug = slugify(install_name)
    return f'{entry["data_type"]}:{slugify(entry["name"])}:{install_slug}'


def pick_best(entries, key):
    def quality(item):
        value = item.get(key, '')
        if key == 'summary':
            return summary_quality(value)
        if key == 'author':
            return 0 if is_missing(value) else len(str(value))
        if key == 'source_url':
            return len(normalize_url(value))
        if key == 'simple_usage':
            return len(str(value or ''))
        return len(str(value or ''))
    return max(entries, key=quality)


def choose_primary(variants):
    def score(item):
        variant_score = 0
        if item['data_type'] == 'skill' and item['source_name'] == 'workspace-skills':
            variant_score += 6
        if item['data_type'] == 'git-repo':
            variant_score += 4
        if item['source_name'] == 'brew':
            variant_score += 2
        variant_score += summary_quality(item.get('summary', ''))
        variant_score += len(normalize_url(item.get('source_url', '')))
        return variant_score
    return max(variants, key=score)


def compare_skill_variants(variants):
    hashes = [v.get('content_fingerprint', {}).get('skill_md_hash', '') for v in variants]
    script_maps = [v.get('content_fingerprint', {}).get('script_files', {}) for v in variants]
    unique_hashes = {h for h in hashes if h}
    script_sets = {tuple(sorted(m.items())) for m in script_maps}
    status_parts = []
    if len(unique_hashes) <= 1:
        status_parts.append('skill-md-identical')
    else:
        status_parts.append('skill-md-different')
    if len(script_sets) <= 1:
        status_parts.append('scripts-identical')
    else:
        status_parts.append('scripts-different')
    pairwise = []
    for variant in variants:
        pairwise.append({
            'source_name': variant['source_name'],
            'install_path': variant['install_path'],
            'skill_md_hash': variant.get('content_fingerprint', {}).get('skill_md_hash', ''),
            'script_files': sorted(variant.get('content_fingerprint', {}).get('script_files', {}).keys()),
        })
    return {
        'status': ','.join(status_parts),
        'skill_md_hashes': sorted(unique_hashes),
        'script_fingerprints': sorted({hashlib.sha256(json.dumps(m, sort_keys=True).encode('utf-8')).hexdigest()[:16] for m in script_maps if m}),
        'variants_review': pairwise,
    }


def merge_group(group):
    primary = choose_primary(group)
    merged = json.loads(json.dumps(primary))
    merged['variants'] = []
    merged['observed_locations'] = []
    merged['install_paths'] = []
    merged['variant_source_names'] = []
    merged['notes'] = list(dict.fromkeys(primary.get('notes', [])))
    merged['canonical_key'] = canonical_key(primary)
    merged['canonical_source_url'] = normalize_url(primary.get('source_url', ''))

    for field in ('author', 'summary', 'simple_usage', 'source_url'):
        best = pick_best(group, field)
        merged[field] = best.get(field, '')
        if best is not primary:
            merged['field_sources'][field] = best['field_sources'].get(field, f'merged:{best["source_name"]}')

    times_install = [item.get('install_time', '') for item in group if item.get('install_time')]
    times_update = [item.get('update_time', '') for item in group if item.get('update_time')]
    merged['install_time'] = min(times_install) if times_install else ''
    merged['update_time'] = max(times_update) if times_update else ''

    tag_set = set(primary.get('tags', []))
    for item in group:
        tag_set.update(item.get('tags', []))
        merged['observed_locations'].append({
            'source_name': item['source_name'],
            'source_kind': item['source_kind'],
            'source_ref': item['source_ref'],
            'install_path': item['install_path'],
        })
        if item.get('install_path'):
            merged['install_paths'].append(item['install_path'])
        merged['variant_source_names'].append(item['source_name'])
        merged['variants'].append({
            'source_name': item['source_name'],
            'data_type': item['data_type'],
            'install_path': item['install_path'],
            'summary': item.get('summary', ''),
            'source_url': item.get('source_url', ''),
            'content_fingerprint': item.get('content_fingerprint', {}),
        })
    merged['tags'] = sorted(tag_set)
    merged['install_paths'] = sorted(dict.fromkeys(merged['install_paths']))
    merged['variant_source_names'] = sorted(dict.fromkeys(merged['variant_source_names']))
    merged['observed_locations'] = sorted(
        merged['observed_locations'],
        key=lambda item: (item['source_name'], item['install_path'])
    )
    merged['variants'] = sorted(merged['variants'], key=lambda item: (item['source_name'], item['install_path']))
    merged['merged_from_count'] = len(group)

    skill_variants = [item for item in group if item['data_type'] == 'skill']
    if len(skill_variants) > 1:
        analysis = compare_skill_variants(skill_variants)
        merged['skill_variant_analysis'] = analysis
        merged['content_diff_status'] = analysis['status']
        merged['content_fingerprint'] = {
            'skill_md_hashes': analysis['skill_md_hashes'],
            'script_fingerprints': analysis['script_fingerprints'],
        }
        if 'different' in analysis['status']:
            merged['notes'].append('Skill variants differ across installed locations and should be reviewed manually.')
    else:
        merged['content_diff_status'] = 'single-variant'
        merged['content_fingerprint'] = primary.get('content_fingerprint', {})
        merged['skill_variant_analysis'] = {}

    merged['score'] = score_entry(
        merged['data_type'],
        merged['update_time'],
        merged['source_url'],
        merged['summary'],
        merged['simple_usage'],
        merged['merged_from_count'],
        merged['content_diff_status'],
    )
    merged['notable_reason'] = notable_reason_for(
        merged['score'],
        merged['data_type'],
        merged['update_time'],
        merged['source_url'],
        merged['merged_from_count'],
        merged['content_diff_status'],
    )
    slug = slugify(primary['name'])
    merged['item_id'] = f'{merged["data_type"]}:{slug}'
    merged['entry_filename'] = f'{merged["data_type"]}__merged__{slug}.md'
    return merged


def score_entry(data_type, update_time, source_url, summary, simple_usage, merged_from_count=1, content_diff_status='single-variant'):
    score = 0
    if data_type in {'git-repo', 'skill', 'extension', 'hook'}:
        score += 2
    if source_url:
        score += 1
    if summary:
        score += 1
    if simple_usage:
        score += 1
    if merged_from_count > 1:
        score += 1
    if 'different' in content_diff_status:
        score += 2
    if update_time:
        try:
            dt = datetime.fromisoformat(update_time)
            age = datetime.now(TZ) - dt
            if age.days <= 30:
                score += 2
            elif age.days <= 120:
                score += 1
        except ValueError:
            pass
    return score


def notable_reason_for(score, data_type, update_time, source_url, merged_from_count=1, content_diff_status='single-variant'):
    reasons = []
    if score >= 6:
        reasons.append('high-signal')
    if data_type in {'skill', 'extension', 'hook'}:
        reasons.append('custom-tooling')
    if source_url:
        reasons.append('has-source-url')
    if merged_from_count > 1:
        reasons.append('merged-duplicate')
    if 'different' in content_diff_status:
        reasons.append('content-diff-alert')
    if update_time:
        try:
            dt = datetime.fromisoformat(update_time)
            if (datetime.now(TZ) - dt).days <= 30:
                reasons.append('recently-updated')
        except ValueError:
            pass
    return ','.join(reasons)


def entry_to_markdown(entry):
    body = ['## Notes', '']
    for note in entry.get('notes', []):
        body.append(f'- {note}')
    if not entry.get('notes'):
        body.append('- No extra notes.')
    data = {k: v for k, v in entry.items() if k not in {'notes', 'slug'}}
    return dump_frontmatter(data) + '\n\n' + '\n'.join(body) + '\n'


def write_entries(entries):
    existing = {path.name: path for path in ENTRIES_DIR.glob('*.md')}
    kept = set()
    for entry in entries:
        filename = entry['entry_filename']
        kept.add(filename)
        path = ENTRIES_DIR / filename
        path.write_text(entry_to_markdown(entry), encoding='utf-8')
    for name, path in existing.items():
        if name not in kept:
            path.unlink()


def normalize_for_snapshot(entry):
    return {
        'item_id': entry['item_id'],
        'canonical_key': entry['canonical_key'],
        'name': entry['name'],
        'author': entry['author'],
        'data_type': entry['data_type'],
        'source_name': entry['source_name'],
        'variant_source_names': entry['variant_source_names'],
        'install_path': entry['install_path'],
        'install_paths': entry['install_paths'],
        'observed_locations': entry['observed_locations'],
        'variants': entry['variants'],
        'merged_from_count': entry['merged_from_count'],
        'install_time': entry['install_time'],
        'update_time': entry['update_time'],
        'summary': entry['summary'],
        'simple_usage': entry['simple_usage'],
        'source_url': entry['source_url'],
        'canonical_source_url': entry['canonical_source_url'],
        'content_fingerprint': entry['content_fingerprint'],
        'content_diff_status': entry['content_diff_status'],
        'skill_variant_analysis': entry['skill_variant_analysis'],
        'score': int(entry['score']),
        'notable_reason': entry['notable_reason'],
        'entry_filename': entry['entry_filename'],
    }


def write_snapshot(entries):
    stamp = datetime.now(TZ).strftime('%Y%m%d-%H%M%S')
    payload = {
        'generated_at': now_iso(),
        'entry_count': len(entries),
        'entries': {entry['item_id']: normalize_for_snapshot(entry) for entry in entries},
    }
    latest = SNAPSHOT_DIR / 'latest.json'
    latest.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding='utf-8')
    stamped = SNAPSHOT_DIR / f'{stamp}.json'
    stamped.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding='utf-8')
    return stamped


def collect_raw(limit_source=None):
    scanners = {
        'ai': git_root_entries,
        'brew': brew_entries,
        'apps': app_entries,
        'skills': skill_entries,
        'extensions': extension_entries,
        'hooks': hook_entries,
    }
    selected = [limit_source] if limit_source else list(scanners)
    entries = []
    for name in selected:
        scanner = scanners.get(name)
        if not scanner:
            raise SystemExit(f'Unknown source: {name}')
        entries.extend(scanner())
    return entries


def merge_entries(entries):
    groups = defaultdict(list)
    for entry in entries:
        groups[canonical_key(entry)].append(entry)
    merged = [merge_group(group) for _, group in sorted(groups.items())]
    merged.sort(key=lambda item: (item['data_type'], item['name'].lower(), item['item_id']))
    return merged


def collect(limit_source=None):
    raw = collect_raw(limit_source=limit_source)
    return merge_entries(raw)


def summarize(entries):
    counts = defaultdict(int)
    merged_variants = 0
    diff_alerts = 0
    for entry in entries:
        counts[entry['data_type']] += 1
        if entry.get('merged_from_count', 1) > 1:
            merged_variants += entry['merged_from_count'] - 1
        if 'different' in entry.get('content_diff_status', ''):
            diff_alerts += 1
    print(f'Generated {len(entries)} merged entries.')
    for key in sorted(counts):
        print(f'- {key}: {counts[key]}')
    print(f'- merged duplicates collapsed: {merged_variants}')
    print(f'- content diff alerts: {diff_alerts}')


def main():
    parser = argparse.ArgumentParser(description='Scan local sources and refresh favorites catalog entries.')
    parser.add_argument('--limit-source', choices=['ai', 'brew', 'apps', 'skills', 'extensions', 'hooks'])
    args = parser.parse_args()
    ensure_dirs()
    entries = collect(limit_source=args.limit_source)
    write_entries(entries)
    snapshot_path = write_snapshot(entries)
    ENRICHMENT.save()
    summarize(entries)
    print(f'Snapshot: {snapshot_path}')


if __name__ == '__main__':
    main()
