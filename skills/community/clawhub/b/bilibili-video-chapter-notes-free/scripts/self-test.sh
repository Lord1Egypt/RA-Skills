#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
test -f SKILL.md && test -f manifest.yaml && test -f agents/openai.yaml
test -f icon-512.png && test -f assets/promo-1600x900.png && test -f fixtures/success-visible-page.json && test -f fixtures/failure-no-subtitles.json
python3 - <<'PY'
from pathlib import Path
b = Path('icon-512.png').read_bytes()
assert b[:8] == b'\x89PNG\r\n\x1a\n'
assert b[16:24] == (512).to_bytes(4, 'big') + (512).to_bytes(4, 'big')
p = Path('assets/promo-1600x900.png').read_bytes()
assert p[:8] == b'\x89PNG\r\n\x1a\n'
assert p[16:24] == (1600).to_bytes(4, 'big') + (900).to_bytes(4, 'big')
m = Path('manifest.yaml').read_text(encoding='utf-8')
s = Path('SKILL.md').read_text(encoding='utf-8')
a = Path('agents/openai.yaml').read_text(encoding='utf-8')
assert 'name: bilibili-video-chapter-notes-free' in m and 'slug: bilibili-video-chapter-notes-free' in m
assert 'name: bilibili-video-chapter-notes-free' in s and 'allow_implicit_invocation: false' in a
PY
python3 scripts/render_fixture_notes.py fixtures/success-visible-page.json > /tmp/bili-success.md
python3 scripts/render_fixture_notes.py fixtures/failure-no-subtitles.json > /tmp/bili-failure.md
rg -q '00:00 / 问题定义' /tmp/bili-success.md
python3 - <<'PY'
from pathlib import Path
output = Path('/tmp/bili-success.md').read_text(encoding='utf-8')
times = ['00:00 / 问题定义', '00:12 / 字幕', '01:20 / 整理证据']
positions = [output.index(value) for value in times]
assert positions == sorted(positions), 'fixture notes must be ordered by visible timestamp'
PY
rg -q '不能声称已看完视频' /tmp/bili-failure.md
echo 'self-test passed: offline success and missing-material branches verified'
