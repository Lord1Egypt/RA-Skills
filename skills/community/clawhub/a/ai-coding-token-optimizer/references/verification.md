# Verification

Run these from the project root of a Git repository. They only read files. Before you edit anything, save a copy of each always-loaded file, for example `cp CLAUDE.md /tmp/CLAUDE.before.md`.

## Measure the always-loaded context

Each host loads its own entry point, so measure **one host at a time** and report each separately. Never add them together.
- Claude Code reads `CLAUDE.md` (or `.claude/CLAUDE.md`) and follows its `@path` imports, including imports of imports.
- Codex reads `AGENTS.md` and does not follow imports.

Run this before and after the change. Files that resolve outside the project are listed but not read.

```python
import re, pathlib
FENCE = '`' * 3  # a code-fence marker, spelled so it can't close this block
root = pathlib.Path('.').resolve()
def measure(entries, follow_imports):
    todo = [root / p for p in entries if (root / p).exists()]
    seen, total = set(), 0
    while todo:
        p = todo.pop(0).resolve()
        if p in seen: continue
        seen.add(p)
        if root not in p.parents or not p.is_file():
            print('    not read (outside project or missing):', p); continue
        text = p.read_text(errors='ignore')
        total += len(text.encode())
        print(f'  {len(text.encode()):>7}  {p.relative_to(root)}')
        if follow_imports:
            body = re.sub(FENCE + '.*?' + FENCE + r'|`[^`\n]*`', '', text, flags=re.S)  # imports in code are not imports
            todo += [p.parent / m for m in re.findall(r'(?<![\w/])@([\w./-]+\.\w+)', body)]
    return total
for host, entries, follow in (('Claude Code', ('CLAUDE.md', '.claude/CLAUDE.md'), True),
                              ('Codex', ('AGENTS.md',), False)):
    print(host)
    t = measure(entries, follow)
    print(f'  {t:>7}  bytes loaded every session, about {t // 4} tokens')
```

Nested instruction files that a host loads while working inside a subdirectory (such as `app/AGENTS.md`) count for tasks in that area. Measure them the same way and report them separately.

## No-loss check

For each old always-loaded file, this lists every heading, backticked term and link destination that no longer appears in the project's documentation.

- Only Markdown that Git tracks, or that is new but not ignored, is read. Build output, virtual environments and ignored private files cannot satisfy the check.
- Symlinks and anything that resolves outside the root are skipped.
- Code examples are ignored on both sides, so a term that survives only inside an example doesn't count as kept.
- Relative links are compared by **destination**, resolved from the file that holds them. A link that moved into a nested guide and was rewritten (`docs/setup.md` → `../setup.md`) still counts as kept. External URLs are compared literally.

Restore anything listed, or name it in the report as deliberately dropped.

```python
import re, os, subprocess, pathlib
FENCE = '`' * 3
OLD, OLD_AT = '/tmp/CLAUDE.before.md', 'CLAUDE.md'   # saved copy, and where it lived
root = pathlib.Path('.').resolve()
listed = subprocess.run(['git', 'ls-files', '-co', '--exclude-standard', '--', '*.md'],
                        capture_output=True, text=True, check=True).stdout.splitlines()
def readable(rel):
    p = root / rel
    return p.is_file() and not p.is_symlink() and root in p.resolve().parents
docs = {rel: (root / rel).read_text(errors='ignore') for rel in listed if readable(rel)}
def prose(text):
    return re.sub(FENCE + '.*?' + FENCE, '', text, flags=re.S)
def destinations(src, text):
    out = set()
    for t in re.findall(r'\]\(([^)\s]+)\)', prose(text)):
        if '://' in t or t.startswith('mailto:'):
            out.add(t)                                # external: compared literally, fragment included
        elif t.split('#')[0]:
            out.add(os.path.normpath(os.path.join(os.path.dirname(src), t.split('#')[0])))
    return out
old = open(OLD).read()
corpus = ''.join(prose(t) for t in docs.values())
kept = set().union(set(), *(destinations(rel, text) for rel, text in docs.items()))
old_prose = prose(old)
terms = set(re.findall(r'`([^`\n]{3,80})`', old_prose)) | {h.strip() for h in re.findall(r'^#{1,6} +(.+)$', old_prose, re.M)}
lost = sorted(t for t in terms if t not in corpus) + sorted(d for d in destinations(OLD_AT, old) if d not in kept)
print('\n'.join(lost) or 'nothing lost')
```

## Links and anchors

Pass the files you touched as arguments. Code examples are ignored on both sides: a link inside an example is not checked, and a `# Heading` inside an example is not treated as an anchor. Links that leave the project, such as into a sibling repository cloned beside it, are listed as not checked rather than read or counted as broken. Files passed in that are symlinks or outside the project are not read. Anchors follow GitHub's slug rule, including its numbering of repeated headings,, which lowercases the heading, drops punctuation and turns spaces into hyphens.

```python
import re, os, sys
FENCE = '`' * 3
root = os.path.realpath('.')
def inside(path):  # never read a symlink or anything outside the project
    return not os.path.islink(path) and os.path.realpath(path).startswith(root + os.sep)
def prose(path):
    return re.sub(FENCE + '.*?' + FENCE, '', open(path).read(), flags=re.S)
def slugs(path):  # GitHub numbers repeated headings: setup, setup-1, setup-2…
    out, count = set(), {}
    for line in prose(path).splitlines():
        if re.match(r'#{1,6} ', line):
            slug = re.sub(r'[^\w\- ]', '', line.lstrip('#').strip().lower()).replace(' ', '-')
            n = count.get(slug, 0); count[slug] = n + 1
            out.add(slug if n == 0 else f'{slug}-{n}')
    return out
bad = 0
for f in sys.argv[1:]:
    if not inside(f):
        print('not read (outside project or a symlink):', f); continue
    for m in re.findall(r'\]\(([^)\s]+)\)', re.sub(r'`[^`\n]*`', '', prose(f))):
        if '://' in m or m.startswith('mailto:'): continue
        path, _, anchor = m.partition('#')
        t = os.path.normpath(os.path.join(os.path.dirname(f), path)) if path else f
        if not os.path.exists(t): print('missing', f, m); bad += 1
        elif not inside(t): print('not checked (outside project):', f, m)  # e.g. a sibling repo
        elif anchor and t.endswith('.md') and anchor not in slugs(t): print('anchor', f, m); bad += 1
print('broken:', bad)
```

## Stale references

```sh
git grep -n -e 'CLAUDE\.md' -e 'AGENTS\.md' -- ':!CLAUDE.md' ':!AGENTS.md'
```

Check every hit that names a section of the old entry point, and repoint it to where that section now lives.
