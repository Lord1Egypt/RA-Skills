"""Build a deterministic, explicitly allowlisted public source ZIP (stdlib only)."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import posixpath
from urllib.parse import unquote, urlsplit
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_PATTERNS = [
    r'\bgh[pousr]_[A-Za-z0-9]{12,}', r'\bsk[-][A-Za-z0-9_-]{25,}',
    r'\b[A-Za-z]:[\\/]', r'(?i)/(?:home|users)/[^/\s]+',
    r'(?i)\blocal[-][a-f0-9]{5,}\b', r'(?i)tail[a-z0-9]+\.ts\.net',
    r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    r'(?i)Bearer\s+[A-Za-z0-9._-]{20,}',
    r'''(?i)(?:api_key|password|secret|token)\s*[:=]\s*["'][^"'\r\n]{6,}["']''',
]


def validate_public_text(name, data):
    path = PurePosixPath(name)
    forbidden_parts = {'.git', '__pycache__', '.cache', 'sessions', 'generation', 'evidence', 'private', 'dist'}
    if any(p.lower() in forbidden_parts for p in path.parts):
        raise ValueError('Private directory: ' + name)
    forbidden_names = {'responses.json', 'judgments.json', 'auth.json', 'config.yaml', 'calibration.md', 'state.db'}
    if path.name.lower() in forbidden_names or path.name.startswith('.env'):
        raise ValueError('Private filename: ' + name)
    if path.suffix.lower() not in {'.md', '.json', '.py', ''} and name not in {'.gitignore', '.gitattributes'}:
        raise ValueError('Non-source file: ' + name)
    text = data.decode('utf-8')
    for pattern in PRIVATE_PATTERNS:
        if re.search(pattern, text):
            raise ValueError('Potential private content: ' + name)
    return text


def validate_local_links(files):
    for name, data in files.items():
        if not name.endswith('.md'):
            continue
        text = data.decode('utf-8')
        for target in re.findall(r'\]\(([^)\s]+)\)', text):
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(url.path)))
            if resolved not in files:
                raise ValueError('Missing linked member: ' + name + ' -> ' + target)
        for target in re.findall(r'`((?:references|scripts|tests)/[A-Za-z0-9_./-]+\.(?:md|json|py))`', text):
            if target not in files:
                raise ValueError('Missing code-linked member: ' + name + ' -> ' + target)


def collect(root):
    root = root.resolve()
    names = json.loads((root / 'distribution-files.json').read_text(encoding='utf-8'))['files']
    if not isinstance(names, list) or not names or any(not isinstance(n, str) for n in names):
        raise ValueError('Distribution files must be a nonempty list of paths')
    folded = [name.casefold() for name in names]
    if len(folded) != len(set(folded)) or 'manifest.json' in folded:
        raise ValueError('Duplicate, case-colliding, or reserved distribution member')
    files = {}
    for name in names:
        path = PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or '\\' in name or ':' in name or path.as_posix() != name:
            raise ValueError('Unsafe distribution path: ' + name)
        source = root / name
        if source.is_symlink() or any(p.is_symlink() for p in source.parents if p != root and root in p.parents):
            raise ValueError('Symlink not allowed: ' + name)
        if not source.resolve().is_relative_to(root) or not source.is_file():
            raise ValueError('Missing or external distribution file: ' + name)
        files[name] = source.read_bytes()
        validate_public_text(name, files[name])
    for required in ['SKILL.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md', 'README.md', 'distribution-files.json']:
        if required not in files:
            raise ValueError('Missing required member: ' + required)
    validate_local_links(files)
    match = re.search(r'(?m)^version: ([0-9]+\.[0-9]+\.[0-9]+(?:-[A-Za-z0-9.-]+)?)$', files['SKILL.md'].decode('utf-8').replace('\r\n', '\n'))
    if not match:
        raise ValueError('Missing valid version')
    return match.group(1), files


def build(root, output_dir):
    version, files = collect(root)
    output_dir = output_dir.resolve()
    if output_dir == root.resolve() or output_dir.is_relative_to(root.resolve()):
        raise ValueError('Keep release artifacts outside the source repository')
    manifest = {'version': version, 'files': {n: hashlib.sha256(b).hexdigest() for n, b in sorted(files.items())}}
    files['MANIFEST.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / ('emirati-arabic-' + version + '.zip')
    with zipfile.ZipFile(archive_path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo('emirati-arabic/' + name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    with zipfile.ZipFile(archive_path) as archive:
        if archive.testzip() is not None:
            raise ValueError('ZIP CRC check failed')
        for name, data in files.items():
            if archive.read('emirati-arabic/' + name) != data:
                raise ValueError('Archive readback mismatch: ' + name)
    checksum = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    (output_dir / 'SHA256SUMS').write_text(checksum + '  ' + archive_path.name + '\n', encoding='utf-8')
    return {'version': version, 'archive': archive_path.name, 'sha256': checksum, 'members': len(files)}


def main():
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, 'reconfigure', None)
        if reconfigure is not None:
            reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True, help='Destination outside the source tree')
    args = parser.parse_args()
    try:
        result = build(ROOT, args.output_dir)
    except (ValueError, OSError, UnicodeError, KeyError, TypeError) as exc:
        print('Distribution rejected: ' + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
