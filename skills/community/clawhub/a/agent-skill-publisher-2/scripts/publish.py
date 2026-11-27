#!/usr/bin/env python3
"""Offline skill/expert packaging. Requires Python 3.10+ and PyYAML 6.x."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import stat
import struct
import sys
import tempfile
import time
import unicodedata
from urllib.parse import unquote, urlsplit
import zipfile

try:
    import yaml
except ImportError:
    raise SystemExit("Missing PyYAML 6.x. Install in your Python environment: python -m pip install 'PyYAML>=6,<7'")

MAX_FILES = 2000
MAX_FILE = 16 * 1024 * 1024
MAX_TOTAL = 64 * 1024 * 1024
PROFILES = ('standard', 'trae', 'workbuddy', 'folder', 'expert')
EXCLUDED = {'.git', '__pycache__', '.pytest_cache', '.venv', 'node_modules'}
WORKBUDDY_FIELDS = ('name', 'display_name', 'display_name_en', 'description',
                    'description_zh', 'description_en', 'version', 'author')
CATEGORIES = {'01-ProductDesign', '02-Engineering', '03-GameSpatial', '04-DataAI',
              '05-MarketingGrowth', '06-ContentCreative', '07-SalesCommerce',
              '08-FinanceInvestment', '09-OperationsHR', '10-ProjectQuality',
              '11-SecurityCompliance', '12-IndustryConsultant', '13-TencentZone',
              '14-WorldWise', '15-Education'}
SEMVER = re.compile(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?\Z')


class Invalid(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise Invalid(message)


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate YAML fields rather than silently taking the last value."""


def mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        need(isinstance(key, str), 'YAML keys must be strings')
        need(key not in result, f'Duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)


def frontmatter(data: bytes):
    try:
        text = data.decode('utf-8-sig').replace('\r\n', '\n')
        match = re.match(r'\A---\n(.*?)\n---(?:\n|$)(.*)\Z', text, re.S)
        need(match is not None, 'Missing YAML frontmatter')
        meta = yaml.load(match[1], Loader=UniqueLoader)
    except (UnicodeError, yaml.YAMLError) as exc:
        raise Invalid(f'Invalid UTF-8/YAML ({type(exc).__name__}); inspect the source locally') from None
    need(isinstance(meta, dict), 'Frontmatter must be a mapping')
    return meta, match[2]


def encode_frontmatter(meta, body):
    return ('---\n' + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False).rstrip()
            + '\n---\n' + body).encode('utf-8')


def json_object(data: bytes, label: str):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, f'Duplicate JSON key in {label}: {key}')
            result[key] = value
        return result
    try:
        value = json.loads(data.decode('utf-8-sig'), object_pairs_hook=pairs)
    except (ValueError, UnicodeError) as exc:
        if isinstance(exc, Invalid):
            raise
        raise Invalid(f'Invalid JSON: {label}') from None
    need(isinstance(value, dict), f'{label} must contain an object')
    return value


def text_field(obj, key):
    value = obj.get(key)
    need(isinstance(value, str) and bool(value.strip()), f'Missing non-empty string: {key}')
    return value


def machine_name(name):
    need(isinstance(name, str) and len(name) <= 64 and
         re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name), 'Invalid machine name')


def safe_path(name: str):
    need(isinstance(name, str) and bool(name), 'Empty path')
    need('\\' not in name and ':' not in name and not name.startswith('/'), f'Unsafe path: {name!r}')
    parts = name.split('/')
    need(all(p not in ('', '.', '..') for p in parts), f'Unsafe path: {name!r}')
    for part in parts:
        need(not re.search(r'[\x00-\x1f<>"|?*]', part) and not part.endswith((' ', '.')),
             f'Nonportable filename: {name!r}')
        need(not re.fullmatch(r'(?i)(con|prn|aux|nul|com[1-9]|lpt[1-9])', part.split('.')[0]),
             f'Reserved filename: {name!r}')
    return name


def check_entries(files):
    need(0 < len(files) <= MAX_FILES, f'File count must be 1..{MAX_FILES}')
    seen = set()
    total = 0
    for name, data in files.items():
        safe_path(name)
        key = unicodedata.normalize('NFC', name).casefold()
        need(key not in seen, f'Case/Unicode path collision: {name}')
        seen.add(key)
        need(len(data) <= MAX_FILE, f'File exceeds {MAX_FILE} bytes: {name}')
        total += len(data)
    need(total <= MAX_TOTAL, f'Expanded size exceeds {MAX_TOTAL} bytes')
    for name in seen:
        parts = name.split('/')
        need(not any('/'.join(parts[:i]) in seen for i in range(1, len(parts))),
             f'File/directory collision: {name}')


def load_files(path: Path):
    files = {}
    if path.is_dir():
        need(not path.is_symlink(), 'Symlink source directories are not supported')
        total = 0
        for current, dirs, names in os.walk(path, followlinks=False):
            for name in dirs + names:
                candidate = Path(current) / name
                need(not candidate.is_symlink() and not (hasattr(candidate, 'is_junction') and candidate.is_junction()),
                     f'Symlink/junction not allowed: {candidate.name}')
            dirs[:] = sorted(n for n in dirs if n not in EXCLUDED)
            for name in sorted(names):
                if name.endswith(('.pyc', '.pyo')) or name in ('.DS_Store',):
                    continue
                file = Path(current) / name
                need(file.is_file(), f'Not a regular file: {file.name}')
                size = file.stat().st_size
                total += size
                need(size <= MAX_FILE and total <= MAX_TOTAL, 'Input size exceeds inspection limits')
                need(len(files) < MAX_FILES, 'Too many files')
                files[file.relative_to(path).as_posix()] = file.read_bytes()
    else:
        need(path.is_file(), 'Input does not exist')
        with zipfile.ZipFile(path) as archive:
            info = archive.infolist()
            need(len(info) <= MAX_FILES * 2, 'Too many ZIP entries')
            need(sum(i.file_size for i in info) <= MAX_TOTAL, 'Expanded ZIP size exceeds limit')
            seen = set()
            for item in info:
                name = item.filename.rstrip('/') if item.is_dir() else item.filename
                safe_path(name)
                key = unicodedata.normalize('NFC', name).casefold()
                need(key not in seen, f'Duplicate ZIP entry: {name}')
                seen.add(key)
                mode = (item.external_attr >> 16) & 0xFFFF
                need(not stat.S_ISLNK(mode), f'ZIP symlink not allowed: {name}')
                need(not item.flag_bits & 1, 'Encrypted ZIP not supported')
                need(item.file_size <= MAX_FILE, f'ZIP entry too large: {name}')
                if not item.is_dir():
                    files[name] = archive.read(item)  # Includes CRC validation.
    check_entries(files)
    return files


def check_private(files):
    patterns = [
        ('private-key', re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')),
        ('github-token', re.compile(rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b')),
        ('aws-access-key', re.compile(rb'\bAKIA[A-Z0-9]{16}\b')),
    ]
    for name, data in files.items():
        leaf = PurePosixPath(name).name.lower()
        need(not (leaf == '.env' or (leaf.startswith('.env.') and leaf not in ('.env.example', '.env.sample'))
                  or leaf in ('id_rsa', 'id_ed25519', 'credentials.json') or leaf.endswith(('.p12', '.pfx'))),
             f'Potential credential file excluded from distribution: {name}')
        for label, pattern in patterns:
            need(not pattern.search(data), f'Potential secret ({label}) in {name}; value suppressed')


def check_links(files):
    # Inline Markdown links only. Dynamic code paths and reference-style links require review.
    for name, data in files.items():
        if not name.endswith('.md'):
            continue
        try:
            text = data.decode('utf-8-sig')
        except UnicodeError:
            raise Invalid(f'Invalid UTF-8 Markdown: {name}') from None
        for match in re.finditer(r'\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+["\'][^\n]*?["\'])?\s*\)', text):
            target = match[1].strip('<>')
            if target.startswith('#'):
                continue
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            local = unquote(parsed.path)
            need(not local.startswith('/') and '\\' not in local, f'Nonportable Markdown link in {name}')
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), local))
            need(not resolved.startswith('../'), f'Markdown link escapes package: {name}')
            need(resolved in files or any(x.startswith(resolved.rstrip('/') + '/') for x in files),
                 f'Missing local link: {name} -> {local}')


def skill_info(files, profile='standard'):
    need('SKILL.md' in files, 'SKILL.md must be at the package root')
    meta, body = frontmatter(files['SKILL.md'])
    machine_name(text_field(meta, 'name'))
    need(len(text_field(meta, 'description')) <= 1024, 'Skill description exceeds 1024 characters')
    need(bool(body.strip()), 'Skill body is empty')
    version = meta.get('version')
    if isinstance(meta.get('metadata'), dict):
        version = meta['metadata'].get('version', version)
    if 'assets/skill-version.json' in files:
        version_meta = json_object(files['assets/skill-version.json'], 'skill-version.json')
        version = text_field(version_meta, 'version')
        source_version = meta.get('metadata', {}).get('version') if isinstance(meta.get('metadata'), dict) else None
        need(not source_version or source_version == version, 'Skill versions disagree')
    if version:
        need(isinstance(version, str) and SEMVER.fullmatch(version), 'Skill version must be a semver string')
        need(not meta.get('version') or meta['version'] == version, 'Skill frontmatter/manifest version mismatch')
    if profile == 'workbuddy':
        for key in WORKBUDDY_FIELDS:
            text_field(meta, key)
        need(SEMVER.fullmatch(meta['version']), 'WorkBuddy version must be semver')
        need(not version or meta['version'] == version, 'WorkBuddy/source version mismatch')
        need(all(len(name.split('/')) <= 2 for name in files),
             'WorkBuddy skill profile requires root files or directory/file; adapt deep resources in a separate source copy')
        version = meta['version']
    manifest = json_object(files['assets/skill-version.json'], 'skill-version.json') if 'assets/skill-version.json' in files else {}
    identity = manifest.get('skill_name', manifest.get('name'))
    need(not identity or identity == meta['name'], 'Skill manifest/name mismatch')
    return {'name': meta['name'], 'version': version, 'build_id': manifest.get('build_id'),
            'local_revision': manifest.get('local_revision'), 'skill_entry': 'SKILL.md',
            'version_source': 'assets/skill-version.json' if manifest else 'SKILL.md metadata'}


def localized(config, key):
    value = config.get(key)
    need(isinstance(value, dict), f'{key} must contain zh and en')
    for lang in ('zh', 'en'):
        text_field(value, lang)
    return value


def image_size(data):
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        need(len(data) >= 33 and data[12:16] == b'IHDR', 'Invalid PNG header')
        return struct.unpack('>II', data[16:24])
    if data.startswith(b'\xff\xd8'):
        stream = io.BytesIO(data[2:])
        while stream.tell() < len(data) - 2:
            need(stream.read(1) == b'\xff', 'Invalid JPEG marker')
            marker = stream.read(1)
            while marker == b'\xff':
                marker = stream.read(1)
            if marker in (b'\xd9', b'\xda', b''):
                break
            if marker == b'\x01' or 0xD0 <= marker[0] <= 0xD7:
                continue
            raw_length = stream.read(2)
            need(len(raw_length) == 2, 'Truncated JPEG')
            length = struct.unpack('>H', raw_length)[0]
            need(length >= 2, 'Invalid JPEG segment')
            segment = stream.read(length - 2)
            need(len(segment) == length - 2, 'Truncated JPEG segment')
            if marker[0] in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                need(len(segment) >= 5, 'Invalid JPEG size segment')
                h, w = struct.unpack('>HH', segment[1:5])
                return w, h
    raise Invalid('Avatar must be PNG or JPEG with readable dimensions')


def relative_config_path(value):
    need(isinstance(value, str), 'Configuration path must be a string')
    if value.startswith('./'):
        value = value[2:]
    return safe_path(value)


def expert_info(files):
    key = '.codebuddy-plugin/plugin.json'
    need(key in files, 'Missing root .codebuddy-plugin/plugin.json')
    c = json_object(files[key], 'plugin.json')
    machine_name(text_field(c, 'name'))
    need(c.get('plugin') == c['name'], 'plugin must equal name')
    need(c.get('expertType') == 'agent', 'This tool supports single-agent experts only')
    need(SEMVER.fullmatch(text_field(c, 'version')), 'Expert version must be semver')
    text_field(c, 'description')
    need(not re.search(r'[\u4e00-\u9fff]', c['description']), 'Expert description should be English')
    author = c.get('author')
    need(isinstance(author, dict), 'Missing author')
    text_field(author, 'name')
    need(re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', text_field(author, 'email')), 'Invalid author email')
    for field in ('displayName', 'profession', 'displayDescription', 'defaultInitPrompt'):
        localized(c, field)
    for lang in ('zh', 'en'):
        need(len(c['displayName'][lang]) <= 15,
             f'Expert displayName.{lang}: {len(c["displayName"][lang])} characters; compatibility limit 15')
    need(40 <= len(c['displayDescription']['zh']) <= 50, 'Chinese card description must have 40..50 characters')
    for field in ('tags', 'quickPrompts'):
        need(isinstance(c.get(field), list) and len(c[field]) == 3, f'{field} must have exactly 3 entries')
        for item in c[field]:
            localized({'value': item}, 'value')
    need(c['defaultInitPrompt'] == c['quickPrompts'][0], 'Default prompt must equal first quickPrompt')
    need(c.get('categoryId') in CATEGORIES, 'Unknown categoryId; verify current platform schema')
    need('tools' not in c, 'Do not declare expert tools; platform controls permissions')
    need('dependencies' not in c and '.mcp.json' not in files,
         'This offline expert profile does not validate MCP/connector dependencies; use the current platform schema separately')
    name = text_field(c, 'agentName')
    machine_name(name)
    agent_path = f'agents/{name}.md'
    need(isinstance(c.get('agents'), list) and len(c['agents']) == 1, 'Single agent path required')
    need(relative_config_path(c['agents'][0]) == agent_path and agent_path in files, 'Agent path/name mismatch')
    agent, body = frontmatter(files[agent_path])
    for field in ('name', 'description', 'displayName', 'profession'):
        expected = name if field == 'name' else c[field]
        need(agent.get(field) == expected, f'Agent/plugin mismatch: {field}')
    need('tools' not in agent and body.strip(), 'Agent body required and tools must not be declared')
    avatar = relative_config_path(c.get('avatar'))
    need(avatar.startswith('avatars/') and avatar in files, 'Missing avatar under avatars/')
    need(len(files[avatar]) <= 500 * 1024 and image_size(files[avatar]) == (512, 512), 'Avatar must be 512x512 and <=500KB')
    skills = []
    paths = c.get('skills', [])
    need(isinstance(paths, list), 'skills must be a list')
    for path in paths:
        prefix = relative_config_path(path) + '/'
        subset = {n[len(prefix):]: data for n, data in files.items() if n.startswith(prefix)}
        info = skill_info(subset)
        need(PurePosixPath(path).name == info['name'], 'Embedded skill directory/name mismatch')
        # Resolve embedded links independently; dependencies must not escape into another skill.
        check_links(subset)
        skills.append({**info, 'path': prefix.rstrip('/')})
    need(len(skills) == len({x['name'] for x in skills}), 'Duplicate embedded skill names')
    need(agent.get('skills', []) == [s['name'] for s in skills], 'Agent preloaded skills mismatch')
    return {'name': c['name'], 'version': c['version'], 'display_name_characters':
            {lang: len(value) for lang, value in c['displayName'].items()}, 'embedded_skills': skills,
            'version_source': key, 'agent_entry': agent_path,
            'avatar': {'path': avatar, 'sha256': hashlib.sha256(files[avatar]).hexdigest(),
                       'bytes': len(files[avatar]), 'dimensions': list(image_size(files[avatar]))}}


def check_avatar(files, expected):
    """Compare actual packaged artwork with the caller's selected image."""
    info = expert_info(files)
    need(files[info['avatar']['path']] == expected.read_bytes(), 'Expert avatar differs from selected image')
    return {'selected_avatar_match': True, **info['avatar']}


def validate(files, profile):
    check_entries(files)
    check_private(files)
    check_links(files)
    entry = 'SKILL.md'
    if profile == 'expert':
        info = expert_info(files)
        entry = '.codebuddy-plugin/plugin.json'
    else:
        subset = files
        if profile == 'folder':
            roots = {name.split('/')[0] for name in files}
            need(len(roots) == 1 and all('/' in name for name in files), 'Folder profile requires one outer skill directory')
            root = roots.pop()
            subset = {name[len(root) + 1:]: data for name, data in files.items()}
            entry = root + '/SKILL.md'
        info = skill_info(subset, profile)
        if profile == 'folder':
            need(root == info['name'], 'Outer directory must equal skill machine name')
    return {**info, 'profile': profile, 'files': len(files), 'entry': entry,
            'artifact_role': 'package-validation-report', 'importable_workflow': False,
            'static_validation': 'passed', 'runtime_test': 'not_run', 'target_import': 'not_verified',
            'target_invocation': 'not_verified', 'marketplace_publication': 'not_submitted',
            'limits': ['Inline Markdown links only', 'No dynamic-path or runtime execution check',
                       'Secret pattern scan is not a comprehensive audit', 'Target platform acceptance not proven']}


def output_preflight(output: Path, sources, force=False):
    need(not output.is_symlink() and not output.with_suffix(output.suffix + '.report.json').is_symlink(),
         'Output and report must not be symbolic links')
    resolved = output.resolve()
    for source in sources:
        root = source.resolve()
        need(not resolved.is_relative_to(root) if source.is_dir() else resolved != root,
             'Output must be outside source inputs')
    need(not output.exists() or force, 'Output exists; choose a new version or explicitly use --force')
    need(not output.with_suffix(output.suffix + '.report.json').exists() or force, 'Output report already exists')


def write_zip(files, output: Path, profile, force=False, sources=()):
    output_preflight(output, sources, force)
    report = validate(files, profile)
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.package-', suffix='.zip', dir=output.parent)
    os.close(fd)
    temporary = Path(name)
    try:
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path, data in sorted(files.items()):
                info = zipfile.ZipInfo(path, (2020, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, data, compresslevel=9)
        readback = load_files(temporary)
        need(readback == files, 'ZIP readback differs from input')
        validate(readback, profile)
        report.update(sha256=hashlib.sha256(temporary.read_bytes()).hexdigest(), bytes=temporary.stat().st_size,
                      zip=output.name, zip_readback='passed')
        if force:
            os.replace(temporary, output)
        else:
            # Exclusive create avoids silently replacing a file created since preflight.
            with output.open('xb') as target:
                target.write(temporary.read_bytes())
        report_path = output.with_suffix(output.suffix + '.report.json')
        with report_path.open('w' if force else 'x', encoding='utf-8') as target:
            json.dump(report, target, ensure_ascii=False, indent=2)
            target.write('\n')
    finally:
        for attempt in range(5):
            try:
                temporary.unlink(missing_ok=True)
                break
            except PermissionError:
                if attempt == 4:
                    # Windows scanners may hold the scratch ZIP after readback.
                    # Preserve the real build exception (if any); do not invalidate
                    # a completed artifact solely because scratch cleanup is delayed.
                    report['temporary_cleanup'] = 'deferred_file_in_use'
                    break
                time.sleep(0.1 * (attempt + 1))
    if report.get('temporary_cleanup'):
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


def package(source: Path, output: Path, profile, metadata=None, force=False):
    need(profile != 'expert', 'Use the expert command for experts')
    output_preflight(output, [source], force)
    files = load_files(source)
    info = skill_info(files)
    if source.is_dir():
        need(source.name == info['name'], 'Source folder must equal skill machine name')
    if profile == 'workbuddy':
        need(metadata is not None, 'WorkBuddy profile requires --metadata JSON')
        market = json_object(metadata.read_bytes(), 'market metadata')
        meta, body = frontmatter(files['SKILL.md'])
        need(not any(k in market and market[k] != meta[k] for k in ('name', 'description')), 'Market metadata must not change skill identity/trigger')
        allowed = set(WORKBUDDY_FIELDS) - {'name', 'description'}
        need(not (set(market) - allowed), 'Market metadata contains unsupported fields')
        meta.update(market)
        files['SKILL.md'] = encode_frontmatter(meta, body)
    elif profile == 'folder':
        files = {info['name'] + '/' + name: data for name, data in files.items()}
    return write_zip(files, output, profile, force, [source])


def build_expert(config_path, body_path, avatar_path, output, skill_paths, force=False):
    sources = [config_path, body_path, avatar_path, *skill_paths]
    output_preflight(output, sources, force)
    config = json_object(config_path.read_bytes(), 'expert config')
    machine_name(text_field(config, 'name'))
    need(not any(k in config for k in ('tools', 'dependencies')), 'Unsupported expert permission/dependency fields')
    body = body_path.read_text(encoding='utf-8-sig')
    need(body.strip() and not body.lstrip().startswith('---'), 'Provide agent body only, without frontmatter')
    agent_name = config.get('agentName', config['name'])
    machine_name(agent_name)
    suffix = '.png' if avatar_path.read_bytes().startswith(b'\x89PNG') else '.jpg'
    avatar_key = 'avatars/expert' + suffix
    files = {avatar_key: avatar_path.read_bytes()}
    skill_names = []
    for path in skill_paths:
        subset = load_files(path)
        info = skill_info(subset)
        need(info['name'] not in skill_names, 'Duplicate skill name')
        check_links(subset)
        skill_names.append(info['name'])
        files.update({f'skills/{info["name"]}/{name}': data for name, data in subset.items()})
    prompts = config.get('quickPrompts')
    need(isinstance(prompts, list) and len(prompts) == 3, 'Three quickPrompts required')
    config.update(expertType='agent', agentName=agent_name, agents=[f'./agents/{agent_name}.md'],
                  skills=[f'./skills/{name}' for name in skill_names], avatar=avatar_key,
                  plugin=config['name'], defaultInitPrompt=prompts[0])
    agent = {key: config[key] for key in ('description', 'displayName', 'profession')}
    agent.update(name=agent_name, maxTurns=100, skills=skill_names)
    files[f'agents/{agent_name}.md'] = encode_frontmatter(agent, body)
    files['.codebuddy-plugin/plugin.json'] = (json.dumps(config, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    title = localized(config, 'displayName')['zh']
    files['README.md'] = (f'# {title}\n\nExpert version: {config["version"]}\n\n'
                          + body + '\n\nTarget WorkBuddy import/invocation/review: not verified.\n').encode('utf-8')
    report = write_zip(files, output, 'expert', force, sources)
    report['selected_avatar_match'] = check_avatar(load_files(output), avatar_path)['selected_avatar_match']
    output.with_suffix(output.suffix + '.report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    check = commands.add_parser('check', help='Inspect a directory or ZIP without executing its code')
    check.add_argument('source', type=Path)
    check.add_argument('--profile', choices=PROFILES, default='standard')
    check.add_argument('--expected-avatar', type=Path, help='Expert only: require byte equality with the selected avatar')
    pack = commands.add_parser('package', help='Create a client-specific skill ZIP')
    pack.add_argument('source', type=Path)
    pack.add_argument('output', type=Path)
    pack.add_argument('--profile', choices=PROFILES[:-1], default='standard')
    pack.add_argument('--metadata', type=Path)
    pack.add_argument('--force', action='store_true')
    expert = commands.add_parser('expert', help='Build a self-contained single-agent WorkBuddy expert')
    for name in ('config', 'body', 'avatar', 'output'):
        expert.add_argument(name, type=Path)
    expert.add_argument('--skill', action='append', type=Path, default=[])
    expert.add_argument('--force', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'check':
            report = validate(load_files(args.source), args.profile)
            if args.expected_avatar:
                need(args.profile == 'expert', '--expected-avatar requires --profile expert')
                report['selected_avatar_match'] = check_avatar(load_files(args.source), args.expected_avatar)['selected_avatar_match']
            if args.source.is_dir() and args.profile not in ('folder', 'expert'):
                need(args.source.name == report['name'], 'Source folder must equal skill machine name')
            if args.source.is_file():
                report['sha256'] = hashlib.sha256(args.source.read_bytes()).hexdigest()
        elif args.command == 'package':
            report = package(args.source, args.output, args.profile, args.metadata, args.force)
        else:
            report = build_expert(args.config, args.body, args.avatar, args.output, args.skill, args.force)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except (Invalid, OSError, zipfile.BadZipFile, RuntimeError, KeyError, TypeError) as exc:
        # YAML/JSON parsers are wrapped above to avoid echoing secret source lines.
        print(json.dumps({'status': 'failed', 'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
