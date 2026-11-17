#!/usr/bin/env python3
"""File-first Obsidian operations. Python 3.10+, POSIX; no third-party packages."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import signal
import stat
import subprocess
import sys
import tempfile
from urllib.parse import quote, unquote


PROTECTED = {'.obsidian', '.git', '.trash'}


class VaultError(Exception):
    def __init__(self, message, saved_locally=False):
        super().__init__(message)
        self.saved_locally = saved_locally


def digest(data):
    return hashlib.sha256(data).hexdigest()


def prefix_match(path, prefixes):
    return any(path == p or path.startswith(p + '/') for p in prefixes)


def relative_name(value):
    p = PurePosixPath(value)
    if not value or p.is_absolute() or '..' in p.parts or '\\' in value or not p.parts:
        raise VaultError('Paths must be nonempty vault-relative paths without traversal or backslashes')
    if any(part in PROTECTED for part in p.parts):
        raise VaultError('Protected path: ' + value)
    return p.as_posix()


class Vault:
    def __init__(self, args):
        value = os.environ.get('OBSIDIAN_VAULT_PATH', '')
        root = Path(value)
        if not value or not root.is_absolute() or not root.is_dir():
            raise VaultError('OBSIDIAN_VAULT_PATH must name an existing absolute directory; check mounts')
        self.root = root.resolve(strict=True)
        self.no_read = [relative_name(p) for p in args.no_read]
        self.read_only = [relative_name(p) for p in args.read_only]
        self.rules = None
        rules_path = os.environ.get('OBSIDIAN_VAULT_RULES')
        if rules_path:
            p = Path(rules_path)
            if not p.is_absolute():
                raise VaultError('OBSIDIAN_VAULT_RULES must be an absolute file path')
            self.rules = p

    def path(self, name, write=False, directory=False):
        name = relative_name(name)
        if prefix_match(name, self.no_read):
            raise VaultError('No-read rule blocks: ' + name)
        if write and prefix_match(name, self.read_only):
            raise VaultError('Read-only rule blocks: ' + name)
        current = self.root
        for part in PurePosixPath(name).parts:
            current = current / part
            if current.is_symlink():
                raise VaultError('Symlinks are not supported: ' + name)
        if current.exists() and not (current.is_dir() if directory else current.is_file()):
            raise VaultError(('Not a directory: ' if directory else 'Not a regular file: ') + name)
        return current

    def read(self, name):
        p = self.path(name)
        try:
            data = p.read_bytes()
            return data, data.decode('utf-8')
        except (OSError, UnicodeError) as exc:
            raise VaultError(f'Cannot read UTF-8 note {name}: {exc}') from exc

    def scope(self, under=None):
        if under is None or under == '.':
            return '', self.root
        name = relative_name(under)
        path = self.path(name, directory=True)
        if not path.is_dir():
            raise VaultError('Scope directory must exist: ' + name)
        return name, path

    def inventory(self, under=None, empty=False):
        _, root = self.scope(under)
        files, directories = [], []

        def visit(path):
            # scandir errors are deliberately not swallowed: an incomplete inventory is unsafe.
            with os.scandir(path) as entries:
                children = sorted(entries, key=lambda entry: entry.name)
            for entry in children:
                child = Path(entry.path)
                name = child.relative_to(self.root).as_posix()
                if entry.name in PROTECTED or entry.is_symlink() or prefix_match(name, self.no_read):
                    continue
                if entry.is_dir(follow_symlinks=False):
                    if empty:
                        with os.scandir(child) as contents:
                            is_empty = next(contents, None) is None
                        if is_empty:
                            directories.append(name)
                    else:
                        directories.append(name)
                    visit(child)
                elif entry.is_file(follow_symlinks=False):
                    files.append(name)

        visit(root)
        return sorted(files), sorted(directories)

    def files(self, under=None):
        return self.inventory(under)[0]

    def rules_data(self):
        if self.rules is None:
            return None
        try:
            data = self.rules.read_bytes()
            content = data.decode('utf-8')
        except (OSError, UnicodeError) as exc:
            raise VaultError(f'Configured rules file is unreadable: {exc}') from exc
        return {'path': str(self.rules), 'sha256': digest(data), 'content': content}

    def writable(self, name, directory=False):
        p = self.path(name, write=True, directory=directory)
        if self.rules and p.resolve() == self.rules.resolve():
            raise VaultError('Rules file is configuration; edit only through an explicit separate user-authorized workflow')
        return p


@contextmanager
def locked(vault):
    cache = Path(os.environ.get('XDG_CACHE_HOME', str(Path.home() / '.cache')))
    directory = cache / 'openclaw-obsidian'
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    path = directory / (digest(str(vault.root).encode()) + '.lock')
    with path.open('a') as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise VaultError('Another cooperating vault operation is running') from exc
        yield


def hook(variable, vault):
    command = os.environ.get(variable)
    if not command:
        return
    try:
        timeout = float(os.environ.get('OBSIDIAN_HOOK_TIMEOUT', '120'))
        if timeout <= 0 or not timeout < float('inf'):
            raise ValueError()
    except ValueError as exc:
        raise VaultError('OBSIDIAN_HOOK_TIMEOUT must be a positive finite number') from exc
    process = subprocess.Popen(command, shell=True, cwd=vault.root, start_new_session=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        _, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        # Kill the whole hook group, not only its shell, before releasing the vault lock.
        os.killpg(process.pid, signal.SIGKILL)
        process.communicate()
        raise VaultError(variable + ' timed out; inspect sync state before continuing') from exc
    if process.returncode:
        detail = stderr.decode('utf-8', errors='replace')[-4000:]
        raise VaultError(f'{variable} failed ({process.returncode}): {detail}')


def masked(text):
    """Keep offsets while hiding fenced code, inline code, and HTML comments."""
    chars = list(text)
    def hide(start, end):
        chars[start:end] = ['\n' if c == '\n' else ' ' for c in text[start:end]]
    fence = None
    offset = 0
    for line in text.splitlines(keepends=True):
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)', line)
        if fence:
            hide(offset, offset + len(line))
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
        elif marker:
            fence = marker[1]
            hide(offset, offset + len(line))
        elif line.startswith('    ') or line.startswith('\t'):
            hide(offset, offset + len(line))
        offset += len(line)
    visible = ''.join(chars)
    for match in re.finditer(r'<!--[\s\S]*?(?:-->|\Z)', visible):
        hide(match.start(), match.end())
    visible = ''.join(chars)
    cursor = 0
    while cursor < len(visible):
        match = re.search(r'`+', visible[cursor:])
        if not match:
            break
        start = cursor + match.start()
        run = match[0]
        end = start + len(run)
        closing = re.search(r'(?<!`)`{' + str(len(run)) + r'}(?!`)', visible[end:])
        if closing:
            stop = end + closing.end()
            hide(start, stop)
            cursor = stop
        else:
            cursor = end
    return ''.join(chars)


def escaped(text, position):
    count = 0
    position -= 1
    while position >= 0 and text[position] == '\\':
        count += 1
        position -= 1
    return count % 2 == 1


def tokens(text):
    """Yield target-only spans; labels, anchors, titles remain untouched."""
    visible = masked(text)
    occupied = []
    for m in re.finditer(r'\[\[([^\]\n]+)\]\]', visible):
        if escaped(visible, m.start()):
            continue
        raw = m[1].split('|', 1)[0]
        end = m.start(1) + len(raw)
        occupied.append((m.start(), m.end()))
        yield {'start': m.start(1), 'end': end, 'raw': text[m.start(1):end], 'kind': 'wiki'}
    # Common inline Markdown links, balanced URL parentheses, and reference definitions.
    starts = []
    for m in re.finditer(r'\]\([ \t]*', visible):
        if not escaped(visible, m.start()) and not any(a <= m.start() < b for a, b in occupied):
            starts.append((m.end(), False))
    for m in re.finditer(r'^ {0,3}\[[^\]\n]+\]:[ \t]*', visible, re.MULTILINE):
        starts.append((m.end(), True))
    for start, definition in starts:
        if start >= len(visible):
            continue
        angle = visible[start] == '<'
        pos = start + int(angle)
        begin = pos
        depth = 0
        while pos < len(visible):
            c = visible[pos]
            if escaped(visible, pos):
                pos += 1
                continue
            if angle:
                if c == '>':
                    break
                if c == '\n':
                    break
            else:
                if c.isspace() or (c == ')' and depth == 0):
                    break
                if c == '(':
                    depth += 1
                elif c == ')':
                    depth -= 1
            pos += 1
        if pos == begin or (angle and (pos == len(visible) or visible[pos] != '>')):
            continue
        if not definition:
            rest = visible[pos + int(angle):]
            if not re.match(r'''^[ \t]*(?:["'][^\n]*?["'][ \t]*)?\)''', rest):
                continue
        yield {'start': begin, 'end': pos, 'raw': text[begin:pos], 'kind': 'markdown'}


def link_parts(raw, kind):
    # Wiki headings and block anchors both start with #. Markdown queries are external/unsupported.
    path, sep, anchor = raw.partition('#')
    return path, sep + anchor if sep else ''


def normalize(base, value):
    parts = list(PurePosixPath(base).parts) if base else []
    for part in value.split('/'):
        if part in ('', '.'):
            continue
        if part == '..':
            if not parts:
                return None
            parts.pop()
        else:
            parts.append(part)
    return '/'.join(parts)


def resolve(source, token, files):
    raw_path, _ = link_parts(token['raw'], token['kind'])
    value = unquote(raw_path) if token['kind'] == 'markdown' else raw_path
    if token['kind'] == 'markdown':
        value = re.sub(r'\\([\\()\[\] ])', r'\1', value)
    if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', value) or value.startswith('//') or '?' in value:
        return {'state': 'external', 'target': None, 'candidates': []}
    if not value:
        return {'state': 'resolved', 'target': source, 'candidates': [source]}
    if token['kind'] == 'markdown' or value.startswith(('./', '../')):
        base = '' if value.startswith('/') else str(PurePosixPath(source).parent)
        normalized = normalize(base if base != '.' else '', value)
        candidates = [p for p in (normalized, (normalized + '.md') if normalized else None) if p in files]
    else:
        normalized = normalize('', value)
        candidates = []
        if normalized:
            exact = [p for p in (normalized, normalized + '.md') if p in files]
            if exact and '/' in normalized:
                candidates = exact
            else:
                candidates = [p for p in files if p == normalized or p == normalized + '.md'
                              or p.endswith('/' + normalized) or p.endswith('/' + normalized + '.md')]
    candidates = sorted(set(candidates))
    return {'state': 'resolved' if len(candidates) == 1 else 'ambiguous' if candidates else 'unresolved',
            'target': candidates[0] if len(candidates) == 1 else None, 'candidates': candidates}


def scan(vault, under=None, source=None):
    scope, _ = vault.scope(under)
    files = vault.files()
    notes = {}
    edges = []
    for name in files:
        if (not name.lower().endswith('.md')
                or (scope and not name.startswith(scope + '/'))
                or (source is not None and name != source)):
            continue
        data, text = vault.read(name)
        notes[name] = (data, text)
        for token in tokens(text):
            edges.append({'source': name, **token, **resolve(name, token, files)})
    return files, notes, edges


def expect(vault, name, expected):
    p = vault.path(name)
    if not p.is_file() or digest(p.read_bytes()) != expected:
        raise VaultError('Concurrent change or stale SHA-256: ' + name)


def atomic_write(vault, name, data, expected=None, create=False):
    path = vault.writable(name)
    # Do not create folders implicitly: parent selection must be deliberate.
    if not path.parent.is_dir():
        raise VaultError('Destination parent directory must already exist: ' + name)
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o600
    fd, temporary = tempfile.mkstemp(prefix='.obsidian-edit-', dir=path.parent)
    committed = False
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        vault.writable(name)
        if create:
            # link is exclusive, unlike replace; never overwrite a competing creation.
            os.link(temporary, path)
        else:
            expect(vault, name, expected)
            os.replace(temporary, path)
        committed = True
    finally:
        try:
            if os.path.exists(temporary):
                os.unlink(temporary)
        except OSError as exc:
            raise VaultError(f'Temporary-file cleanup failed for {name}: {exc}',
                             saved_locally=committed) from exc


def rewritten_target(edge, new_source, new_target):
    old_path, anchor = link_parts(edge['raw'], edge['kind'])
    if not old_path and new_source == new_target:
        return edge['raw']
    if edge['kind'] == 'wiki':
        target = new_target[:-3] if new_target.endswith('.md') else new_target
        return target + anchor
    parent = str(PurePosixPath(new_source).parent)
    target = os.path.relpath(new_target, parent).replace(os.sep, '/')
    if old_path.startswith('/'):
        target = '/' + new_target
    if not unquote(old_path).endswith('.md') and new_target.endswith('.md'):
        target = target[:-3]
    return quote(target, safe='/._~-') + anchor


def plan_hash(files, notes, details):
    snapshot = {'files': files, 'notes': {name: digest(data) for name, (data, _) in notes.items()},
                'operation': details}
    return digest(json.dumps(snapshot, sort_keys=True).encode('utf-8'))


def edited_notes(vault, notes, replacements):
    changes = {}
    for name, entries in replacements.items():
        vault.writable(name)
        text = notes[name][1]
        for span, replacement in sorted(entries, key=lambda item: item[0]['start'], reverse=True):
            text = text[:span['start']] + replacement + text[span['end']:]
        data = text.encode('utf-8')
        if data != notes[name][0]:
            changes[name] = data
    return changes


def check_scan(vault, files, notes):
    if vault.files() != files:
        raise VaultError('Vault listing changed during refactor planning')
    for name, (data, _) in notes.items():
        expect(vault, name, digest(data))


def tree_snapshot(vault, source):
    """Read every descendant, refusing entries that discovery normally prunes."""
    directories, contents = [], {}

    def visit(name):
        path = vault.writable(name, directory=True)
        directories.append(name)
        with os.scandir(path) as entries:
            children = sorted(entries, key=lambda entry: entry.name)
        for entry in children:
            child = name + '/' + entry.name
            if entry.is_symlink():
                raise VaultError('Symlink in move subtree: ' + child)
            if entry.is_dir(follow_symlinks=False):
                visit(child)
            elif entry.is_file(follow_symlinks=False):
                contents[child] = vault.writable(child).read_bytes()
            else:
                raise VaultError('Unsupported entry in move subtree: ' + child)

    visit(source)
    fingerprint = digest(json.dumps({
        'directories': sorted(directories),
        'files': {name: digest(data) for name, data in sorted(contents.items())},
    }, sort_keys=True).encode('utf-8'))
    return sorted(directories), contents, fingerprint


def move(vault, args):
    source, destination = relative_name(args.source), relative_name(args.destination)
    if source == destination or destination.startswith(source + '/'):
        raise VaultError('Source and destination are identical or destination is inside source')
    if vault.no_read:
        raise VaultError('Move requires a complete readable content scope; no-read rules prevent safe backlink refactoring')
    is_directory = (vault.root / source).is_dir()
    src = vault.writable(source, directory=is_directory)
    dst = vault.writable(destination, directory=is_directory)
    if not src.exists() or dst.exists() or not dst.parent.is_dir():
        raise VaultError('Move requires existing source, absent destination, and existing destination parent')
    if not is_directory and source.lower().endswith('.md') != destination.lower().endswith('.md'):
        raise VaultError('Move cannot change between Markdown and attachment file types')
    if is_directory:
        directories, contents, source_sha = tree_snapshot(vault, source)
    else:
        directories, contents = [], {source: src.read_bytes()}
        source_sha = digest(contents[source])

    def relocated(name):
        if name == source or (is_directory and name.startswith(source + '/')):
            return destination + name[len(source):]
        return name

    for name in directories:
        vault.writable(relocated(name), directory=True)
    for name in contents:
        vault.writable(relocated(name))
    files, notes, edges = scan(vault)
    future_files = sorted(relocated(name) for name in files)
    replacements, unresolved = {}, []
    for edge in edges:
        moved_source = edge['source'] in contents
        if edge['state'] == 'ambiguous' and (moved_source or any(p in contents for p in edge['candidates'])):
            raise VaultError('Ambiguous link prevents move: ' + edge['source'] + ': ' + edge['raw'])
        new_source = relocated(edge['source'])
        if edge['state'] == 'unresolved' and moved_source:
            old_path, anchor = link_parts(edge['raw'], edge['kind'])
            if edge['kind'] == 'wiki' and old_path.startswith(('./', '../')):
                raise VaultError('Unresolved relative wikilink prevents move: ' + edge['raw'])
            replacement = edge['raw']
            if edge['kind'] == 'markdown' and old_path and not old_path.startswith('/'):
                parent = str(PurePosixPath(edge['source']).parent)
                decoded = re.sub(r'\\([\\()\[\] ])', r'\1', unquote(old_path))
                target = normalize('' if parent == '.' else parent, decoded)
                if target is None:
                    raise VaultError('Outgoing link escapes vault: ' + edge['raw'])
                # Missing descendants conceptually travel with their containing subtree.
                target = relocated(target) if is_directory else target
                replacement = quote(os.path.relpath(target, str(PurePosixPath(new_source).parent)),
                                    safe='/._~-') + anchor
            if resolve(new_source, {**edge, 'raw': replacement}, future_files)['state'] != 'unresolved':
                raise VaultError('Move would change the meaning of an unresolved link: ' + edge['raw'])
            if replacement != edge['raw']:
                replacements.setdefault(edge['source'], []).append((edge, replacement))
            unresolved.append({'source': edge['source'], 'link': edge['raw']})
            continue
        if edge['state'] != 'resolved':
            continue
        target = relocated(edge['target'])
        future = resolve(new_source, edge, future_files)
        if future['state'] != 'resolved' or future['target'] != target:
            replacement = rewritten_target(edge, new_source, target)
            checked = resolve(new_source, {**edge, 'raw': replacement}, future_files)
            if checked['state'] != 'resolved' or checked['target'] != target:
                raise VaultError('Move would create an ambiguous or incorrect link: '
                                 + edge['source'] + ': ' + replacement)
            if replacement != edge['raw']:
                replacements.setdefault(edge['source'], []).append((edge, replacement))
    changes = edited_notes(vault, notes, replacements)
    output = {'source': source, 'destination': destination,
              'source_type': 'directory' if is_directory else 'file', 'sha256': source_sha,
              'updated_notes': sorted(changes), 'unresolved_outgoing': unresolved,
              'applied': False, 'atomicity': 'per-file only; multi-file move is not crash-atomic',
              'parser': 'conservative file-link subset; folder and plugin references are unsupported'}
    output['plan_sha256'] = plan_hash(files, notes, output)
    if not args.apply:
        return output, False
    if args.expected_sha256 != source_sha:
        raise VaultError('Missing or stale --expected-sha256; preview the current move again')
    if args.expected_plan_sha256 != output['plan_sha256']:
        raise VaultError('Missing or stale --expected-plan-sha256; preview and authorize the current move again')
    check_scan(vault, files, notes)
    if is_directory:
        if tree_snapshot(vault, source)[2] != source_sha:
            raise VaultError('Source directory changed during move planning')
    else:
        expect(vault, source, source_sha)
    completed = []
    try:
        # Exclusive publication never overwrites a concurrently-created destination.
        for name in sorted(directories, key=lambda p: (p.count('/'), p)):
            target = relocated(name)
            vault.writable(target, directory=True).mkdir(mode=0o700)
            completed.append(target)
        for name, data in sorted(contents.items()):
            target = relocated(name)
            atomic_write(vault, target, changes.get(name, data), create=True)
            completed.append(target)
        for name, data in sorted(changes.items()):
            if name not in contents:
                atomic_write(vault, name, data, expected=digest(notes[name][0]))
                completed.append(name)
        if is_directory:
            if tree_snapshot(vault, source)[2] != source_sha:
                raise VaultError('Source directory changed before removal')
        else:
            expect(vault, source, source_sha)
        for name, data in sorted(contents.items()):
            expect(vault, name, digest(data))
            vault.writable(name).unlink()
            completed.append('removed:' + name)
        for name in sorted(directories, key=lambda p: (p.count('/'), p), reverse=True):
            vault.writable(name, directory=True).rmdir()
            completed.append('removed:' + name)
    except (OSError, VaultError) as exc:
        raise VaultError(f'Move interrupted; inspect files before further edits. Completed changes: {completed}. {exc}',
                         saved_locally=bool(completed) or getattr(exc, 'saved_locally', False)) from exc
    output['applied'] = True
    return output, True


def anchor_definition(text, old, new):
    block = old.startswith('^')
    if block != new.startswith('^'):
        raise VaultError('Cannot change between heading and block anchor kinds')
    for anchor in (old, new):
        if (not anchor or anchor != anchor.strip()
                or any(ord(c) < 32 or ord(c) == 127 or c in '\x85\u2028\u2029' for c in anchor)):
            raise VaultError('Anchors must be nonempty single-line text without surrounding whitespace')
        if block:
            if not re.fullmatch(r'\^[A-Za-z0-9-]+', anchor):
                raise VaultError('Block anchors must be a caret followed by letters, digits or hyphens')
        elif re.search(r'[#^*_\[\]()`~\\<>!|{}]', anchor):
            raise VaultError('Only plain-text heading anchors are supported; Markdown syntax is unsafe')
    visible = masked(text)
    # YAML metadata is not a Markdown anchor-definition scope.
    frontmatter = re.match(r'\A---[ \t]*\r?\n[\s\S]*?^(?:---|\.\.\.)[ \t]*(?:\r?\n|\Z)', text, re.MULTILINE)
    if frontmatter:
        end = frontmatter.end()
        visible = ''.join('\n' if c == '\n' else ' ' for c in text[:end]) + visible[end:]
    definitions = []
    offset = 0
    lines = text.splitlines(keepends=True)
    for index, line in enumerate(lines):
        body = line.rstrip('\r\n')
        shown = visible[offset:offset + len(body)]
        if block:
            match = re.search(r'(?<!\S)(\^[A-Za-z0-9-]+)[ \t]*$', body)
            if match and shown[match.start(1):match.end(1)] == match[1]:
                definitions.append((match[1], offset + match.start(1), offset + match.end(1)))
        else:
            match = re.fullmatch(r' {0,3}#{1,6}[ \t]+(.*?)(?:[ \t]+#+[ \t]*|[ \t]*)', body)
            if match and shown[:match.start(1)] == body[:match.start(1)]:
                heading = match[1]
                unsafe = re.search(r'[#^*_\[\]()`~\\<>!|{}]', heading)
                if unsafe and any(anchor.casefold() in heading.casefold() for anchor in (old, new)):
                    raise VaultError('Relevant Markdown-rendered heading definitions are unsupported')
                # Inline code/comments are not plain headings, even if masking leaves matching text.
                if shown[match.start(1):match.end(1)] == heading:
                    definitions.append((heading, offset + match.start(1), offset + match.end(1)))
            if index + 1 < len(lines) and shown.strip().casefold() in (old.casefold(), new.casefold()):
                following = lines[index + 1].rstrip('\r\n')
                next_shown = visible[offset + len(line):offset + len(line) + len(following)]
                if re.fullmatch(r' {0,3}(?:=+|-+)[ \t]*', next_shown):
                    raise VaultError('Setext heading definitions are unsupported for anchor refactoring')
        offset += len(line)
    old_matches = [d for d in definitions if d[0] == old]
    if len(old_matches) != 1:
        raise VaultError('Anchor definition is missing, unsupported or ambiguous: ' + old)
    if any(d[0].casefold() == old.casefold() and d != old_matches[0] for d in definitions):
        raise VaultError('Anchor definition has case-insensitive duplicates: ' + old)
    collisions = [d for d in definitions if d[0].casefold() == new.casefold() and d != old_matches[0]]
    if collisions:
        raise VaultError('New anchor collides with an existing definition: ' + new)
    _, start, end = old_matches[0]
    return {'start': start, 'end': end}


def refactor_anchor(vault, args):
    name = relative_name(args.path)
    if not name.lower().endswith('.md'):
        raise VaultError('Anchor refactoring requires a UTF-8 Markdown note')
    vault.writable(name)
    if vault.no_read:
        raise VaultError('Anchor refactoring requires a complete readable scope; no-read rules prevent safe edits')
    files, notes, edges = scan(vault)
    if name not in notes:
        raise VaultError('Anchor note must exist: ' + name)
    old, new = args.old_anchor, args.new_anchor
    definition = anchor_definition(notes[name][1], old, new)
    replacements = {name: [(definition, new)]}
    for edge in edges:
        path, fragment = link_parts(edge['raw'], edge['kind'])
        if not fragment:
            continue
        anchor = unquote(fragment[1:]) if edge['kind'] == 'markdown' else fragment[1:]
        if anchor != old:
            continue
        if edge['state'] == 'ambiguous' and name in edge['candidates']:
            raise VaultError('Ambiguous reference prevents anchor refactor: ' + edge['source'] + ': ' + edge['raw'])
        if edge['state'] == 'resolved' and edge['target'] == name:
            encoded = quote(new, safe='-._~') if edge['kind'] == 'markdown' else new
            replacements.setdefault(edge['source'], []).append((edge, path + '#' + encoded))
    changes = edited_notes(vault, notes, replacements)
    output = {'path': name, 'sha256': digest(notes[name][0]), 'old_anchor': old, 'new_anchor': new,
              'updated_notes': sorted(changes), 'applied': False,
              'atomicity': 'per-file only; multi-file anchor refactor is not crash-atomic'}
    output['plan_sha256'] = plan_hash(files, notes, output)
    if not args.apply:
        return output, False
    if args.expected_sha256 != output['sha256']:
        raise VaultError('Missing or stale --expected-sha256; preview the current anchor refactor again')
    if args.expected_plan_sha256 != output['plan_sha256']:
        raise VaultError('Missing or stale --expected-plan-sha256; preview and authorize the anchor refactor again')
    check_scan(vault, files, notes)
    completed = []
    try:
        for target, data in sorted(changes.items()):
            atomic_write(vault, target, data, expected=digest(notes[target][0]))
            completed.append(target)
    except (OSError, VaultError) as exc:
        raise VaultError(f'Anchor refactor interrupted. Completed writes: {completed}. {exc}',
                         saved_locally=bool(completed) or getattr(exc, 'saved_locally', False)) from exc
    output['applied'] = True
    return output, bool(changes)


def targeted_edit(vault, args):
    name = relative_name(args.path)
    vault.writable(name)
    if not name.lower().endswith('.md'):
        raise VaultError('append/replace accept UTF-8 Markdown files only')
    original, _ = vault.read(name)
    if digest(original) != args.expected_sha256:
        raise VaultError('Concurrent change or stale SHA-256: ' + name)
    expect(vault, name, args.expected_sha256)
    if args.command == 'append':
        extra = Path(args.content_file).read_bytes()
        extra.decode('utf-8')
        data = original + extra
    else:
        old = Path(args.old_file).read_bytes()
        new = Path(args.new_file).read_bytes()
        old.decode('utf-8')
        new.decode('utf-8')
        if not old:
            raise VaultError('Replacement OLD content must be nonempty')
        first = original.find(old)
        if first < 0 or original.find(old, first + 1) >= 0:
            raise VaultError('Replacement OLD content must occur exactly once, including overlapping matches')
        data = original[:first] + new + original[first + len(old):]
    if data == original:
        return {'path': name, 'sha256': digest(original), 'changed': False}, False
    atomic_write(vault, name, data, expected=args.expected_sha256)
    return {'path': name, 'sha256': digest(data), 'changed': True}, True


def import_attachment(vault, args):
    source = Path(args.source)
    if not source.is_absolute() or '..' in source.parts:
        raise VaultError('Attachment source must be an absolute regular file without traversal')
    current = Path(source.anchor)
    for component in source.parts[1:]:
        current = current / component
        if current.is_symlink():
            raise VaultError('Symlinks are not supported in attachment source paths')
    if not source.is_file():
        raise VaultError('Attachment source must be an existing regular file')
    if source.is_relative_to(vault.root):
        vault.path(source.relative_to(vault.root).as_posix())
    name = relative_name(args.destination)
    if name.lower().endswith('.md'):
        raise VaultError('Attachment destination must not be a Markdown file')
    vault.writable(name)
    data = source.read_bytes()
    atomic_write(vault, name, data, create=True)
    return {'path': name, 'sha256': digest(data), 'changed': True}, True


def make_directory(vault, args):
    name = relative_name(args.path)
    parts = PurePosixPath(name).parts
    names = ['/'.join(parts[:i]) for i in range(1, len(parts) + 1)] if args.parents else [name]
    # Validate the whole requested scope before creating even the first parent.
    for prefix in names:
        vault.path(prefix, write=True, directory=True)
    created = []
    try:
        for prefix in names:
            path = vault.path(prefix, write=True, directory=True)
            try:
                path.mkdir(mode=0o700)
            except FileExistsError:
                # Existing directories are a no-op; files and symlinks are not.
                vault.path(prefix, write=True, directory=True)
            else:
                created.append(prefix)
    except (OSError, VaultError) as exc:
        raise VaultError(f'Directory creation failed. Created directories: {created}. {exc}',
                         saved_locally=bool(created)) from exc
    return {'path': name, 'created_directories': created, 'changed': bool(created)}, bool(created)


def perform(vault, args):
    command = args.command
    if command == 'mkdir':
        return make_directory(vault, args)
    if command == 'rmdir':
        name = relative_name(args.path)
        path = vault.path(name, write=True, directory=True)
        with os.scandir(path) as entries:
            if next(entries, None) is not None:
                raise VaultError('Directory is not empty: ' + name)
        if args.apply:
            # rmdir atomically refuses nonempty directories, including concurrent additions.
            vault.path(name, write=True, directory=True).rmdir()
        return {'path': name, 'empty': True, 'applied': args.apply}, args.apply
    if command == 'status':
        return {'vault': str(vault.root), 'files': len(vault.files()),
                'excluded_components': sorted(PROTECTED), 'no_read': vault.no_read,
                'read_only': vault.read_only}, False
    if command == 'rules':
        return {'rules': vault.rules_data(), 'restrictions_are': 'Markdown guidance plus explicit helper prefix flags'}, False
    if command == 'list':
        if args.empty and args.type != 'dirs':
            raise VaultError('--empty is valid only with list --type dirs')
        files, directories = vault.inventory(args.under, empty=args.empty)
        result = {}
        if args.type in ('files', 'all'):
            result['files'] = files
        if args.type in ('dirs', 'all'):
            result['directories'] = directories
        return result, False
    if command == 'read':
        data, text = vault.read(args.path)
        return {'path': args.path, 'sha256': digest(data), 'content': text}, False
    if command == 'search':
        matches = []
        for name in vault.files(args.under):
            if name.lower().endswith('.md'):
                _, text = vault.read(name)
                for number, line in enumerate(text.splitlines(), 1):
                    if args.query.casefold() in line.casefold():
                        matches.append({'path': name, 'line': number, 'text': line})
        return {'matches': matches, 'scope': 'readable Markdown files'}, False
    if command in ('links', 'backlinks'):
        name = relative_name(args.path) if args.path else None
        if name is not None:
            vault.path(name)
        files, _, edges = scan(vault, under=getattr(args, 'under', None),
                               source=name if command == 'links' else None)
        if command == 'backlinks':
            if name not in files:
                raise VaultError('Backlink target must exist: ' + name)
            edges = [e for e in edges if name in e['candidates']]
        return {'links': [{k: v for k, v in e.items() if k not in ('start', 'end')} for e in edges],
                'scope': 'readable files excluding protected paths and symlinks',
                'complete': not vault.no_read, 'parser': 'conservative Markdown/wiki subset; not Obsidian metadata cache'}, False
    if command in ('create', 'write'):
        name = relative_name(args.path)
        path = vault.writable(name)
        data = Path(args.content_file).read_bytes()
        data.decode('utf-8')
        if not name.lower().endswith('.md'):
            raise VaultError('create/write accept Markdown files only; attachments may be moved or inspected as link targets')
        if command == 'write':
            expect(vault, name, args.expected_sha256)
            if data == path.read_bytes():
                return {'path': name, 'sha256': digest(data), 'changed': False}, False
        atomic_write(vault, name, data, expected=getattr(args, 'expected_sha256', None), create=command == 'create')
        return {'path': name, 'sha256': digest(data), 'changed': True}, True
    if command in ('append', 'replace'):
        return targeted_edit(vault, args)
    if command == 'import-attachment':
        return import_attachment(vault, args)
    if command == 'refactor-anchor':
        return refactor_anchor(vault, args)
    if command == 'move':
        return move(vault, args)
    if command == 'delete':
        name = relative_name(args.path)
        path = vault.writable(name)
        expect(vault, name, args.expected_sha256)
        if vault.no_read:
            raise VaultError('Delete requires a complete readable scope to check references')
        files, notes, edges = scan(vault)
        incoming = [e for e in edges if name in e['candidates'] and e['source'] != name]
        result = {'path': name, 'sha256': args.expected_sha256, 'applied': False,
                  'references': [{'source': e['source'], 'link': e['raw'], 'state': e['state']} for e in incoming]}
        result['plan_sha256'] = plan_hash(files, notes, result)
        if args.apply:
            if args.expected_plan_sha256 != result['plan_sha256']:
                raise VaultError('Missing or stale --expected-plan-sha256; preview and authorize the current deletion again')
            if incoming and not args.allow_referenced:
                raise VaultError('File has incoming references; inspect preview and explicitly authorize --allow-referenced')
            if vault.files() != files:
                raise VaultError('Vault listing changed during deletion planning')
            for note, (data, _) in notes.items():
                expect(vault, note, digest(data))
            expect(vault, name, args.expected_sha256)
            path.unlink()
            result['applied'] = True
        return result, args.apply
    raise VaultError('Unknown command')


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--no-read', action='append', default=[], metavar='PREFIX')
    p.add_argument('--read-only', action='append', default=[], metavar='PREFIX')
    commands = p.add_subparsers(dest='command', required=True)
    for name in ('status', 'rules'):
        commands.add_parser(name)
    sub = commands.add_parser('list')
    sub.add_argument('--type', choices=('files', 'dirs', 'all'), default='files')
    sub.add_argument('--under', metavar='DIR')
    sub.add_argument('--empty', action='store_true')
    sub = commands.add_parser('mkdir', help='Create an allowed vault directory')
    sub.add_argument('path')
    sub.add_argument('--parents', action='store_true', help='Also create missing parent directories')
    sub = commands.add_parser('rmdir', help='Preview removal of an empty vault directory')
    sub.add_argument('path')
    sub.add_argument('--apply', action='store_true', help='Remove only this directory if it is empty')
    commands.add_parser('read').add_argument('path')
    sub = commands.add_parser('search')
    sub.add_argument('query')
    sub.add_argument('--under', metavar='DIR')
    for name in ('links', 'backlinks'):
        sub = commands.add_parser(name)
        sub.add_argument('path', nargs='?' if name == 'links' else None)
        if name == 'links':
            sub.add_argument('--under', metavar='DIR')
    for name in ('create', 'write'):
        sub = commands.add_parser(name)
        sub.add_argument('path')
        sub.add_argument('--content-file', required=True)
        if name == 'write':
            sub.add_argument('--expected-sha256', required=True)
    sub = commands.add_parser('append')
    sub.add_argument('path')
    sub.add_argument('--content-file', required=True)
    sub.add_argument('--expected-sha256', required=True)
    sub = commands.add_parser('replace')
    sub.add_argument('path')
    sub.add_argument('--old-file', required=True)
    sub.add_argument('--new-file', required=True)
    sub.add_argument('--expected-sha256', required=True)
    sub = commands.add_parser('import-attachment')
    sub.add_argument('source')
    sub.add_argument('destination')
    sub = commands.add_parser('refactor-anchor')
    sub.add_argument('path')
    sub.add_argument('--old-anchor', required=True)
    sub.add_argument('--new-anchor', required=True)
    sub.add_argument('--apply', action='store_true')
    sub.add_argument('--expected-sha256')
    sub.add_argument('--expected-plan-sha256')
    sub = commands.add_parser('move')
    sub.add_argument('source')
    sub.add_argument('destination')
    sub.add_argument('--apply', action='store_true')
    sub.add_argument('--expected-sha256')
    sub.add_argument('--expected-plan-sha256')
    sub = commands.add_parser('delete')
    sub.add_argument('path')
    sub.add_argument('--expected-sha256', required=True)
    sub.add_argument('--apply', action='store_true')
    sub.add_argument('--allow-referenced', action='store_true')
    sub.add_argument('--expected-plan-sha256')
    return p


def main():
    args = parser().parse_args()
    changed = False
    try:
        vault = Vault(args)
        with locked(vault):
            hook('OBSIDIAN_PRE_COMMAND', vault)
            rules = vault.rules_data()
            result, changed = perform(vault, args)
            if changed:
                try:
                    hook('OBSIDIAN_POST_COMMAND', vault)
                except (VaultError, OSError) as exc:
                    print(json.dumps({'ok': False, 'saved_locally': True, 'synchronization': 'failed',
                                      'result': result, 'error': str(exc)}, ensure_ascii=False))
                    return 2
            result['ok'] = True
            result['rules_file'] = {k: v for k, v in rules.items() if k != 'content'} if rules else None
            print(json.dumps(result, ensure_ascii=False))
            return 0
    except (VaultError, OSError, UnicodeError) as exc:
        print(json.dumps({'ok': False, 'error': str(exc),
                          'saved_locally': changed or getattr(exc, 'saved_locally', False)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    sys.exit(main())
