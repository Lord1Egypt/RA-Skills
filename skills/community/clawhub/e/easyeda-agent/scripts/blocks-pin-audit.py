#!/usr/bin/env python3
"""Audit every circuit block's pin references against REAL symbol pins.

A block references pins by FUNCTION NAME (`CH340.TXD`) so it survives designator
churn — but nothing checked those names against the actual symbols, so blocks
shipped `verified` while silently mis-wiring. One example cost a whole day:
`ch340c_usb_serial` referenced `J_USB.VBUS`, which is ambiguous on a USB-C 16P
(two VBUS pins), so `block-apply` never connected VBUS at all — the USB port was
not powered, and the block was marked verified because it had been validated by
HAND-wiring, which bypasses the block's own pin references entirely.

Two modes:

  --probe --project <scratch-project> --doc <scratch-page> --allow-clear
             Place every part the library references on one dedicated page.
             Read real pins back and refresh the pin table snapshot.
             This explicitly clears that page; it does not create a scratch page.
             Resumable: re-run after a connection hiccup and it continues.
  (default)  Offline: judge every block pin reference against the snapshot.
             Exits non-zero if any reference is FANOUT or MISSING, so it gates.

Verdicts:
  unique   exactly one pin matches (by name or number) — fine as written
  fanout   several pins share that function name — needs the `*` suffix, which
           bonds them all (a connector's redundant VBUS/GND/shield, a chip's
           doubled power pins, a crystal's two case grounds)
  missing  no pin matches — the name is simply wrong; real candidates are shown
  unknown  that part has no probed pins yet (unmeasured, not a defect)
"""
import argparse, difflib, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.realpath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
BLOCKS = os.path.join(REPO, 'internal', 'blocks', 'data')
STDPARTS = os.path.join(HERE, '..', 'references', 'standard-parts.json')
SNAPSHOT = os.path.join(HERE, '..', 'references', 'symbol-pins.json')
FANOUT = '*'


def read_json(path):
    with open(path, encoding='utf-8') as stream:
        return json.load(stream)


def cli_binary():
    explicit = os.environ.get('EASYEDA_BIN')
    if explicit:
        resolved = shutil.which(explicit)
        if not resolved:
            raise RuntimeError(f'EASYEDA_BIN is not an executable: {explicit}')
        return resolved
    resolved = shutil.which('easyeda')
    if resolved:
        return resolved
    fallback = os.path.join(REPO, 'bin', 'easyeda')
    if os.path.isfile(os.path.join(REPO, 'go.mod')) and os.access(fallback, os.X_OK):
        return fallback
    raise RuntimeError('easyeda CLI not found: install it on PATH or set EASYEDA_BIN=/absolute/path/to/easyeda')


def load_blocks():
    # Repository contributors audit their edited source. Installed skills use
    # the same data embedded in the CLI; ls is only a projection, so fetch show.
    if os.path.isdir(BLOCKS):
        return [read_json(os.path.join(BLOCKS, name))
                for name in sorted(os.listdir(BLOCKS))
                if name.endswith('.json') and not name.startswith('_')]
    binary = cli_binary()
    def query(args):
        proc = subprocess.run([binary, 'blocks'] + args, capture_output=True,
                              encoding='utf-8', errors='replace', timeout=30)
        if proc.returncode:
            raise RuntimeError(f'embedded block lookup failed: {proc.stderr.strip() or proc.stdout.strip()}')
        return json.loads(proc.stdout)
    listing = query(['ls', '--json'])
    if not isinstance(listing, list) or not listing:
        raise RuntimeError('embedded block list is missing or empty; update the easyeda CLI')
    blocks = []
    for item in listing:
        if not isinstance(item, dict) or not isinstance(item.get('id'), str) or not item['id']:
            raise RuntimeError('embedded block list has an invalid identity')
        block = query(['show', item['id']])
        if not isinstance(block, dict) or block.get('id') != item['id']:
            raise RuntimeError(f'embedded block detail identity mismatch: {item["id"]}')
        blocks.append(block)
    return blocks


def load_refs():
    """Extract (role, pin, part_key) for every internal_nets member of every block."""
    refs, parts = {}, set()
    for b in load_blocks():
        bid = b.get('id')
        if not bid:
            raise RuntimeError('block has no id')
        roles = {r: (v.get('part') if isinstance(v, dict) else None)
                 for r, v in (b.get('parts') or {}).items()}
        nets = b.get('internal_nets')
        if not isinstance(nets, list):
            continue  # `"pending"` — topology not settled yet
        items = []
        for net in nets:
            if not isinstance(net, list):
                continue
            for m in net:
                if not isinstance(m, str) or m.startswith('PORT:') or '.' not in m:
                    continue
                role, pin = m.split('.', 1)
                pk = roles.get(role)
                if pk:
                    parts.add(pk)
                items.append((role, pin, pk))
        # schematic_layout.attach 的目标也是**引脚引用**,必须一起审 —— 否则
        # attach 里的引脚名拼错了没人管(#145 的教训:块标着 verified 却静默
        # 错接了十几天)。Go 侧的 V4 只验"有没有电气依据",引脚名对不对得上
        # 真实符号,得靠这张引脚真值表(issue #180)。
        layout = b.get('schematic_layout')
        if isinstance(layout, dict):
            for key, target in (layout.get('attach') or {}).items():
                if not isinstance(target, str) or '.' not in target:
                    continue
                role, pin = target.split('.', 1)
                pk = roles.get(role)
                if pk:
                    parts.add(pk)
                items.append((role, pin.rstrip('*'), pk))
        refs[bid] = items
    return refs, sorted(parts)


def probe(project, doc, allow_clear=False):
    """Place each referenced part once and read its real pins. Resumable."""
    if not project or not doc or not allow_clear:
        raise RuntimeError('--probe requires explicit --project, --doc and --allow-clear for a dedicated measurement page')
    std = read_json(STDPARTS)
    lib, parts = std['libraryUuid'], std['parts']
    _, wanted_all = load_refs()

    table = {}
    if os.path.exists(SNAPSHOT):
        table = read_json(SNAPSHOT).get('parts', {})
        print(f'resuming from snapshot: {len(table)} part(s) already probed')

    skipped = [p for p in wanted_all if p not in parts or not parts[p].get('deviceUuid')]
    if skipped:
        print(f'!! {len(skipped)} part(s) have no deviceUuid in standard-parts.json '
              f'and cannot be probed: {", ".join(skipped)}')
    wanted = [p for p in wanted_all
              if p in parts and parts[p].get('deviceUuid') and p not in table]
    print(f'to probe: {len(wanted)}')
    if not wanted:
        print('nothing to probe; page unchanged')
        return
    if not os.access(SNAPSHOT if os.path.exists(SNAPSHOT) else os.path.dirname(SNAPSHOT), os.W_OK):
        raise RuntimeError(f'pin snapshot is not writable: {SNAPSHOT}; no page was changed')
    binary = cli_binary()

    def run(args, timeout=180):
        return subprocess.run([binary] + args[1:] + ['--doc', doc], capture_output=True,
                              encoding='utf-8', errors='replace', timeout=timeout)

    def must_run(args):
        result = run(args)
        try:
            ok = json.loads(result.stdout).get('ok') is True
        except (ValueError, AttributeError):
            ok = False
        if result.returncode or not ok:
            raise RuntimeError(f'{" ".join(args[1:3])} failed on {project}/{doc}; probe stopped: '
                               f'{result.stderr.strip() or result.stdout.strip()}')

    BATCH = 12  # a small page keeps the pin read fast and the clear reliable
    for start in range(0, len(wanted), BATCH):
        chunk = wanted[start:start + BATCH]
        must_run(['easyeda', 'sch', 'clear', '--project', project])
        must_run(['easyeda', 'sch', 'save', '--project', project])

        placed = {}
        for i, pk in enumerate(chunk):
            x, y = 200 + (i % 4) * 400, 200 + (i // 4) * 400
            r = run(['easyeda', 'sch', 'place', '--lib', lib,
                     '--uuid', parts[pk]['deviceUuid'],
                     '--x', str(x), '--y', str(y), '--project', project])
            if r.returncode == 0:
                placed[pk] = (x, y)

        # The list call is the fragile step; retry rather than lose the batch.
        data = None
        for _ in range(3):
            r = run(['easyeda', 'sch', 'list', '--project', project, '--include-pins'])
            try:
                d = json.loads(r.stdout)
                if isinstance(d.get('result', {}).get('components'), list):
                    data = d
                    break
            except Exception:
                pass
        if data is None:
            print(f'  batch {start}: list failed after retries — skipped')
            continue

        # Match by the coordinate we placed at: the response's device.uuid is a
        # 16-hex symbol id, NOT the 32-hex deviceUuid we passed, so uuid matching
        # never lines up.
        by_xy = {(round(float(c.get('x', -1))), round(float(c.get('y', -1)))): c
                 for c in data['result']['components'] if c.get('componentType') == 'part'}
        for pk, xy in placed.items():
            c = by_xy.get(xy)
            if c:
                table[pk] = [{'n': p.get('pinNumber'), 'name': p.get('pinName')}
                             for p in (c.get('pins') or [])]
        with open(SNAPSHOT, 'w', encoding='utf-8') as stream:
            json.dump({'_doc': 'Real symbol pins, read back from placed parts. Refresh on a dedicated page with '
                               'blocks-pin-audit.py --probe --project <scratch> --doc <page> --allow-clear.',
                       'parts': table}, stream, ensure_ascii=False, indent=1)
        print(f'  batch {start}-{start + len(chunk)}: {len(placed)} probed')

    must_run(['easyeda', 'sch', 'clear', '--project', project])
    must_run(['easyeda', 'sch', 'save', '--project', project])
    print(f'snapshot: {len(table)} part(s) → {SNAPSHOT}')


def audit():
    if not os.path.exists(SNAPSHOT):
        print(f'no pin snapshot at {SNAPSHOT} — run with --probe first', file=sys.stderr)
        return 2
    table = read_json(SNAPSHOT)['parts']
    refs, _ = load_refs()

    def classify(pk, pin):
        pins = table.get(pk)
        if pins is None:
            return 'unknown', []
        starred = pin.endswith(FANOUT)
        want = pin[:-1] if starred else pin
        hits = [p for p in pins if p.get('name') == want or p.get('n') == want]
        if not hits:
            names = sorted({p['name'] for p in pins if p.get('name')})
            return 'missing', difflib.get_close_matches(want, names, n=4, cutoff=0.4) or names[:6]
        if len(hits) > 1:
            return ('unique' if starred else 'fanout'), [h.get('n') for h in hits]
        return 'unique', [hits[0].get('n')]

    stats = {'unique': 0, 'fanout': 0, 'missing': 0, 'unknown': 0}
    bad = []
    for bid, items in sorted(refs.items()):
        for role, pin, pk in items:
            if not pk:
                continue
            verdict, info = classify(pk, pin)
            stats[verdict] += 1
            if verdict in ('fanout', 'missing'):
                bad.append((bid, role, pin, pk, verdict, info))

    print(f"refs judged: {sum(stats.values())}  unique={stats['unique']} "
          f"fanout={stats['fanout']} missing={stats['missing']} unknown={stats['unknown']}")
    cur = None
    for bid, role, pin, pk, verdict, info in bad:
        if bid != cur:
            print(f'\n{bid}')
            cur = bid
        if verdict == 'fanout':
            print(f'  FANOUT   {role}.{pin:<14} → pins {info}   ⇒ write "{role}.{pin}*"')
        else:
            print(f'  MISSING  {role}.{pin:<14} ({pk})   real candidates: {info}')
    if bad:
        print(f'\n{len(bad)} bad reference(s). FANOUT → add the `*` suffix; '
              f'MISSING → use the symbol\'s real pin name.')
    return 1 if bad else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--probe', action='store_true',
                    help='refresh pin snapshot on a dedicated page; requires --project --doc --allow-clear')
    ap.add_argument('--project', help='explicit scratch project for --probe')
    ap.add_argument('--doc', help='explicit dedicated schematic page for --probe (will be cleared)')
    ap.add_argument('--allow-clear', action='store_true', help='authorize clearing the specified measurement page')
    a = ap.parse_args()
    try:
        if a.probe:
            probe(a.project, a.doc, a.allow_clear)
            sys.exit(0)
        sys.exit(audit())
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
        ap.exit(2, f'blocks-pin-audit: {error}\n')
