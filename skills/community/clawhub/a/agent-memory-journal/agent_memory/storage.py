from __future__ import annotations

import hashlib
import json
import re
import os
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .models_v2 import MemoryItem
from .security import require_safe_memory_text, sanitize_evidence_text, validate_hot_path

VALID_CATEGORIES = {"decision", "constraint", "gotcha", "preference", "capability"}
META_RE = re.compile(r"\s+\[(.*)\]\s*$")
ID_RE = re.compile(r"(?:^|\s)id:([^\s\]]+)")
STATE_RE = re.compile(r"(?:^|\s)state:([^\s\]]+)")


def sanitize_session_id(session_id: str) -> str:
    safe_session_id = ''.join(ch for ch in session_id if ch.isalnum() or ch in {'-', '_'})
    if not safe_session_id:
        raise ValueError('session_id must contain at least one safe character')
    return safe_session_id


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def make_memory_id(category: str, text: str) -> str:
    digest = hashlib.sha1(f'{category}:{text}'.encode('utf-8')).hexdigest()[:12]
    return f'{category[:3]}-{digest}'


def split_claim_and_metadata(line: str) -> tuple[str, str]:
    stripped = line.strip()
    if stripped.startswith('- '):
        stripped = stripped[2:]
    match = META_RE.search(stripped)
    if not match:
        return stripped.strip(), ''
    meta = match.group(1).strip()
    claim = stripped[:match.start()].strip()
    return claim, meta


def extract_id(line: str) -> str | None:
    _claim, meta = split_claim_and_metadata(line)
    match = ID_RE.search(meta)
    return match.group(1) if match else None


def extract_state(line: str) -> str | None:
    _claim, meta = split_claim_and_metadata(line)
    match = STATE_RE.search(meta)
    return match.group(1) if match else None


def has_active_memory(target: Path, memory_id: str) -> bool:
    if not target.exists():
        return False
    for line in target.read_text(encoding='utf-8', errors='ignore').splitlines():
        if not line.strip().startswith('- '):
            continue
        if extract_id(line) == memory_id and extract_state(line) != 'superseded':
            return True
    return False


def render_memory_item(item: MemoryItem) -> str:
    flags = [
        f'id:{item.id}',
        f'state:{item.state}',
        f'source:{item.source}',
        f'created:{item.created_at}',
    ]
    if item.last_seen:
        flags.append(f'last_seen:{item.last_seen}')
    if item.pinned:
        flags.append('pinned:true')
    if item.supersedes:
        flags.append(f'supersedes:{item.supersedes}')
    return f"- {item.text} [{' '.join(flags)}]"


def _load_memory_config(root: Path) -> dict:
    config_path = root / 'config.json'
    if not config_path.exists():
        return {}
    try:
        data = json.loads(config_path.read_text(encoding='utf-8'))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


@dataclass
class MemoryPaths:
    root: Path

    @property
    def config_file(self) -> Path:
        return self.root / 'config.json'

    @property
    def config(self) -> dict:
        return _load_memory_config(self.root)

    @property
    def hot_file(self) -> Path:
        hot_path = self.config.get('hot_path', 'AGENT.md')
        return validate_hot_path(self.root, hot_path)

    @property
    def episodic_dir(self) -> Path:
        return self.root / 'episodic'

    @property
    def core_dir(self) -> Path:
        return self.root / 'core'

    @property
    def sessions_dir(self) -> Path:
        return self.root / 'sessions'

    @property
    def archive_core_dir(self) -> Path:
        return self.root / 'archive' / 'core'

    @property
    def index_dir(self) -> Path:
        return self.root / 'index'

    def core_file(self, category: str) -> Path:
        normalized = category.strip().lower()
        if normalized not in VALID_CATEGORIES:
            raise ValueError(f"Invalid category '{category}'")
        mapping = {
            'decision': 'decisions.md',
            'constraint': 'constraints.md',
            'gotcha': 'gotchas.md',
            'preference': 'preferences.md',
            'capability': 'capabilities.md',
        }
        return self.core_dir / mapping[normalized]


def init_memory_root(root: str | Path) -> MemoryPaths:
    paths = MemoryPaths(Path(root).expanduser().resolve())
    paths.root.mkdir(parents=True, exist_ok=True)
    paths.episodic_dir.mkdir(parents=True, exist_ok=True)
    paths.core_dir.mkdir(parents=True, exist_ok=True)
    paths.sessions_dir.mkdir(parents=True, exist_ok=True)
    paths.archive_core_dir.mkdir(parents=True, exist_ok=True)
    paths.index_dir.mkdir(parents=True, exist_ok=True)
    if not paths.config_file.exists():
        paths.config_file.write_text(json.dumps({
            'hot_path': 'AGENT.md',
            'hot_header': '# AGENT.md',
            'hot_max_chars': 2048
        }, indent=2) + '\n', encoding='utf-8')
    if not paths.hot_file.exists():
        paths.hot_file.parent.mkdir(parents=True, exist_ok=True)
        header = paths.config.get('hot_header', '# AGENT.md')
        paths.hot_file.write_text(f'{header}\n\n', encoding='utf-8')
    for category in sorted(VALID_CATEGORIES):
        target = paths.core_file(category)
        if not target.exists():
            title = target.stem.replace('_', ' ').replace('-', ' ').title()
            target.write_text(f'# {title}\n\n', encoding='utf-8')
    manifest = paths.index_dir / 'manifest.json'
    if not manifest.exists():
        manifest.write_text('{"schema":1,"layout":"agent-memory-v2"}\n', encoding='utf-8')
    return paths


def _refresh_manifest_entry(paths: 'MemoryPaths', file_path: Path) -> None:
    manifest_path = paths.index_dir / 'manifest.json'
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        if not isinstance(manifest, dict):
            manifest = {}
    except Exception:
        manifest = {}
    manifest.setdefault('schema', 1)
    manifest.setdefault('layout', 'agent-memory-v2')
    tracked = manifest.get('core_sha256')
    if not isinstance(tracked, dict):
        tracked = {}
        manifest['core_sha256'] = tracked
    if not file_path.exists():
        return
    digest = hashlib.sha256(file_path.read_bytes()).hexdigest()
    rel = str(file_path.relative_to(paths.root))
    tracked[rel] = digest
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')


def _atomic_append(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(text, encoding='utf-8')
        return

    # Use a temporary file to prevent corruption during concurrent writes
    fd, temp_path = tempfile.mkstemp(dir=str(path.parent), prefix=path.name + ".tmp")
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            # Copy existing content
            f.write(path.read_text(encoding='utf-8', errors='ignore'))
            # Append new text
            f.write(text)
        # Atomically replace the original file
        shutil.move(temp_path, str(path))
    except Exception:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise


def append_episodic_note(root: str | Path, text: str, category: str | None = None, importance: str = 'normal', source: str = 'agent') -> Path:
    paths = init_memory_root(root)
    now = datetime.now(timezone.utc)
    path = paths.episodic_dir / f"{now.date()}.md"
    cleaned = sanitize_evidence_text(text)
    suffix = []
    if category:
        suffix.append(f'category:{category}')
    if importance != 'normal':
        suffix.append(f'importance:{importance}')
    if source:
        suffix.append(f'source:{source}')
    trailer = f" [{' '.join(suffix)}]" if suffix else ''
    _atomic_append(path, f"- {now.strftime('%H:%M')} {cleaned}{trailer}\n")
    return path


def append_core_memory(root: str | Path, category: str, text: str, source: str = 'agent', pinned: bool = False, supersedes: str | None = None, state: str = 'active') -> Path:
    paths = init_memory_root(root)
    target = paths.core_file(category)
    cleaned = require_safe_memory_text(text)

    if supersedes:
        # Validate that the supersedes ID actually exists
        found_target = False
        for core_file in paths.core_dir.glob('*.md'):
            if f'id:{supersedes}' in core_file.read_text(encoding='utf-8', errors='ignore'):
                found_target = True
                break
        if not found_target:
            raise ValueError(f"supersedes ID '{supersedes}' not found in core memory")

    item = MemoryItem(
        id=make_memory_id(category, cleaned),
        text=cleaned,
        category=category,
        tier='warm',
        state=state,
        source=source,
        created_at=utc_now_iso(),
        last_seen=utc_now_iso(),
        pinned=pinned,
        supersedes=supersedes,
    )
    if has_active_memory(target, item.id):
        return target
    _atomic_append(target, render_memory_item(item) + '\n')
    _refresh_manifest_entry(paths, target)
    return target


def append_session_note(root: str | Path, session_id: str, text: str, category: str | None = None, importance: str = 'normal', source: str = 'agent') -> Path:
    paths = init_memory_root(root)
    safe_session_id = sanitize_session_id(session_id)
    target = paths.sessions_dir / f'{safe_session_id}.md'
    now = datetime.now(timezone.utc)
    cleaned = sanitize_evidence_text(text)
    suffix = []
    if category:
        suffix.append(f'category:{category}')
    if importance != 'normal':
        suffix.append(f'importance:{importance}')
    if source:
        suffix.append(f'source:{source}')
    trailer = f" [{' '.join(suffix)}]" if suffix else ''
    _atomic_append(target, f"- {now.strftime('%H:%M')} {cleaned}{trailer}\n")
    return target


def supersede_memory(root: str | Path, memory_id: str, new_state: str = 'superseded') -> bool:
    paths = init_memory_root(root)
    found = False
    for core_file in paths.core_dir.glob('*.md'):
        content = core_file.read_text(encoding='utf-8', errors='ignore')
        if f'id:{memory_id}' not in content:
            continue

        new_lines = []
        lines = content.splitlines()
        for line in lines:
            if not line.strip().startswith('- '):
                new_lines.append(line)
                continue

            current_id = extract_id(line)
            if current_id == memory_id:
                # Update state:active -> state:superseded
                new_line = re.sub(r'state:[^\s\]]+', f'state:{new_state}', line)
                new_lines.append(new_line)
                found = True
            else:
                new_lines.append(line)

        if found:
            # Atomic rewrite
            fd, temp_path = tempfile.mkstemp(dir=str(core_file.parent), prefix=core_file.name + ".tmp")
            try:
                with os.fdopen(fd, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_lines).rstrip() + '\n')
                shutil.move(temp_path, str(core_file))
            except Exception:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                raise
            _refresh_manifest_entry(paths, core_file)
            break
    return found
