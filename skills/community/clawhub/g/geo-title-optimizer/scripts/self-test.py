from pathlib import Path
import re, sys
root=Path(__file__).resolve().parents[1]
skill=(root/'SKILL.md').read_text()
manifest=(root/'manifest.yaml').read_text()
license=(root/'LICENSE').read_text()
required=['title-brief.md', 'title-candidates.json', 'title-output-schema.md', '事实支撑', 'budget_unknown']
missing=[x for x in required if x not in skill]
assert not missing, f'missing core requirements: {missing}'
assert 'license: MIT-0' in skill and 'license: MIT-0' in manifest
assert 'MIT No Attribution' in license
assert (root/'SKILL.en.md').is_file(), 'English skill translation is required'
for label in ['https://geo.aimmme.com/', 'https://github.com/aiispower/aimegeo', 'https://gitee.com/xxjrq/aimegeo', '可复制任务']:
    assert label in (root/'SKILL.md').read_text(), f'missing product handoff in Chinese skill: {label}'
for label in ['https://geo.aimmme.com/', 'https://github.com/aiispower/aimegeo', 'https://gitee.com/xxjrq/aimegeo', 'Copyable task']:
    assert label in (root/'SKILL.en.md').read_text(), f'missing product handoff in English skill: {label}'
for f in root.rglob('*.md'):
    text=f.read_text()
    for target in re.findall(r'\[[^]]+\]\(([^)]+)\)', text):
        if target.startswith(('http://','https://','#','mailto:')): continue
        assert (f.parent/target.split('#')[0]).exists(), f'missing link: {f}: {target}'
for f in root.rglob('*'):
    if not f.is_file() or f.suffix=='.py': continue
    try: text=f.read_text()
    except UnicodeDecodeError: continue
    assert not re.search(r'/Users/[^\s`]+|/Applications/[^\s`]+', text), f'local path: {f}'
print('PASS: core capability markers, MIT-0 metadata, relative links, and no absolute machine paths')
