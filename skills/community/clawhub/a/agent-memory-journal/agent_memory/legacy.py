from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .models import RecallResult
from .normalize import token_counter


class LegacyJournal:
    def __init__(self, root: str | Path = '.'):
        self.root = Path(root).expanduser().resolve()
        self.long_file = self.root / 'MEMORY.md'
        self.daily_dir = self.root / 'memory'

    def recall(self, query: str, k: int = 5, tier: str = 'all') -> list[RecallResult]:
        q = query.lower().strip()
        results: list[RecallResult] = []
        if tier in {'all', 'warm'} and self.long_file.exists():
            results.extend(self._scan_file(self.long_file, q, tier='warm'))
        if tier in {'all', 'cold'} and self.daily_dir.exists():
            for path in sorted(self.daily_dir.glob('*.md'), reverse=True):
                results.extend(self._scan_file(path, q, tier='cold'))
        results.sort(key=lambda item: (-item.score, item.path, item.line_no))
        return results[: max(1, k)]

    def note(self, text: str, category: str | None = None, importance: str = 'normal', source: str = 'agent') -> Path:
        self.daily_dir.mkdir(parents=True, exist_ok=True)
        from datetime import datetime
        path = self.daily_dir / f"{datetime.now().date()}.md"
        ts = datetime.now().strftime('%H:%M')
        suffix = ''
        if category:
            suffix += f' [category:{category}]'
        if importance != 'normal':
            suffix += f' [importance:{importance}]'
        with path.open('a', encoding='utf-8') as handle:
            handle.write(f"- {ts} {text.strip()}{suffix}\n")
        return path

    def _scan_file(self, path: Path, query: str, tier: str) -> Iterable[RecallResult]:
        for line_no, line in enumerate(path.read_text(encoding='utf-8', errors='ignore').splitlines(), start=1):
            lowered = line.lower()
            if not query:
                continue
            query_tokens = token_counter(query)
            line_tokens = token_counter(line)
            overlap = sum(min(line_tokens[t], query_tokens[t]) for t in query_tokens)
            substring_bonus = 1 if query in lowered else 0
            if overlap or substring_bonus:
                score = float(overlap + substring_bonus)
                yield RecallResult(text=line.strip(), path=str(path), line_no=line_no, score=score, tier=tier)
