"""Conservative ownership checks and rollback-capable local output publication.

Markers identify tool-managed directories, not a security boundary against a
hostile local user. Concurrent writers to the same destination are unsupported.
"""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile

MARKER = '.pptsmith-output-owner.json'


def checked_path(path: Path) -> Path:
    """Reject symlinks before resolving (including dangling/parent links)."""
    path = Path(path)
    if not path.is_absolute():
        path = Path.cwd() / path
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError(f'symlink path is not allowed: {part}')
    return path.resolve()


def overlaps(a: Path, b: Path) -> bool:
    return a == b or a in b.parents or b in a.parents


def check_source(path: Path) -> Path:
    path = checked_path(path)
    if path.is_dir():
        for child in path.rglob('*'):
            if child.is_symlink():
                raise ValueError(f'symlink source is not allowed: {child}')
    return path


def path_key(path: Path) -> str:
    # Bind ownership without recording local user or source path text.
    return hashlib.sha256(os.fsencode(str(path))).hexdigest()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class OutputTransaction:
    def __init__(self, output: Path, *, tool: str, overwrite: bool,
                 sources=(), sidecars=(), source_roots=()):
        self.output = checked_path(output)
        self.tool = tool
        self.overwrite = overwrite
        self.sources = [check_source(Path(p)) for p in sources]
        self.source_roots = [checked_path(Path(p)) for p in source_roots]
        self.sidecars = [checked_path(Path(p)) for p in sidecars]
        self.validate()

    def validate(self):
        out = checked_path(self.output)
        protected = {Path(out.anchor), Path.home().resolve(), Path.cwd().resolve()}
        if out in protected or out in Path.home().resolve().parents or out in Path.cwd().resolve().parents:
            raise ValueError(f'protected output path: {out}')
        for source in self.sources:
            if overlaps(out, source):
                raise ValueError(f'output overlaps source: {source}')
        for root in self.source_roots:
            if out == root or out in root.parents:
                raise ValueError(f'output contains source root: {root}')
        paths = [out, *self.sidecars]
        for i, path in enumerate(paths):
            checked_path(path)
            for other in paths[:i]:
                if overlaps(path, other):
                    raise ValueError(f'overlapping output paths: {path}, {other}')
            for source in self.sources:
                if overlaps(path, source):
                    raise ValueError(f'output overlaps source: {source}')
        owner = {}
        if out.exists():
            if not self.overwrite:
                raise ValueError(f'output exists; explicit --overwrite required: {out}')
            if not out.is_dir():
                raise ValueError(f'output is not a directory: {out}')
            marker = checked_path(out / MARKER)
            try:
                owner = json.loads(marker.read_text(encoding='utf-8'))
            except (OSError, ValueError) as exc:
                raise ValueError(f'output has no valid ownership marker: {out}') from exc
            if not isinstance(owner, dict) or owner.get('tool') != self.tool or owner.get('output_key') != path_key(out) or owner.get('schema_version') != 1:
                raise ValueError(f'output ownership mismatch: {out}')
            check_source(out)
        for path in self.sidecars:
            if path.exists():
                if (not self.overwrite or not path.is_file() or
                    owner.get('sidecars', {}).get(path_key(path)) != digest(path)):
                    raise ValueError(f'sidecar is not an unchanged owned output: {path}')

    @contextmanager
    def staging(self):
        self.output.parent.mkdir(parents=True, exist_ok=True)
        # Only this random, exclusively-created directory is ever cleaned up.
        self.temp = Path(tempfile.mkdtemp(prefix=f'.{self.output.name}.staging-', dir=self.output.parent))
        self.preserve_backup = False
        try:
            stage = self.temp / 'payload' / self.output.name
            stage.mkdir(parents=True)
            yield stage
        finally:
            if not self.preserve_backup:
                shutil.rmtree(self.temp)

    def commit(self, stage: Path, sidecars=()):
        """Publish each path via rename; roll back earlier renames on failure.

        Not crash-atomic across multiple files. Backups survive a rollback failure.
        """
        self.validate()
        sidecars = list(sidecars)
        if {target for _, target in sidecars} != set(self.sidecars):
            raise ValueError('sidecar publication set mismatch')
        owner = {'schema_version': 1, 'tool': self.tool, 'output_key': path_key(self.output),
                 'sidecars': {path_key(target): digest(source) for source, target in sidecars}}
        (stage / MARKER).write_text(json.dumps(owner, sort_keys=True) + '\n', encoding='utf-8')
        pairs = [(stage, self.output), *sidecars]
        moved = []
        backups = []
        backup_dir = self.temp / 'backups'
        backup_dir.mkdir()
        try:
            for index, (source, target) in enumerate(pairs):
                target.parent.mkdir(parents=True, exist_ok=True)
                backup = backup_dir / str(index)
                if target.exists():
                    os.replace(target, backup)
                    backups.append((backup, target))
                os.replace(source, target)
                moved.append((source, target))
        except BaseException:
            try:
                for source, target in reversed(moved):
                    os.replace(target, source)
                for backup, target in reversed(backups):
                    os.replace(backup, target)
            except BaseException:
                self.preserve_backup = True
                raise RuntimeError(f'Rollback interrupted; original backups retained at {self.temp}')
            raise
