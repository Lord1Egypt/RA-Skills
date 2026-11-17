#!/usr/bin/env python3
"""Re-resolve standard-parts.json device uuids for the CURRENT EasyEDA edition.

Why: the curated references/standard-parts.json carries deviceUuid values captured
on the China edition (lceda.cn). The international edition (easyeda.com) ships the
same system library (identical libraryUuid) but assigns DIFFERENT device uuids, so
every `schematic.component.place { libraryUuid, uuid }` from the canonical file
targets a device the platform does not know — the connector never answers and
`sch block-apply` fails at its first placement with "connector did not respond"
(verified: 0/143 uuids matched on desktop 3.2.149 international, e.g. C8678 is
804240ef97df427480be2a5281ccea31 there vs 009407eaaa604eb9b6f73cc3868f316d in the
file).

What: batch every part's LCSC C-number through `easyeda lib by-lcsc` (the
edition-local, deterministic resolver) and write a RELOCALIZED COPY:

    parts-relocalize.py --out /tmp/parts.intl.json --project <name>
    easyeda sch block-apply <block> --parts /tmp/parts.intl.json --project <name>

Per part: resolved uuid == existing → unchanged; different → deviceUuid is replaced
and the original kept under deviceUuidOrigin; not returned → entry untouched and
marked "_relocalize": "unresolved". The returned libraryUuid must equal the file's
(or the part's own override); a mismatch is warned about and NOT applied
("_relocalize": "libraryUuid-mismatch"). The source file is never modified.

The output is edition-specific: do not commit it over the canonical file.
Exit status: 0 on success (even with unresolved parts), 2 when the CLI is missing
or no batch succeeded, 1 on bad arguments / unreadable input.

Pure stdlib; the transform (`relocalize`) and the stdout parser (`extract_json`)
are plain functions so they are unit-testable without the CLI — the offline
regressions live in the repo at `scripts/tests/test_parts_relocalize.py`
(`python -m unittest discover -s scripts/tests -p 'test_*.py'`).
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PARTS = os.path.normpath(os.path.join(HERE, '..', 'references', 'standard-parts.json'))
BATCH_MAX = 20
MARK = '_relocalize'
ORIGIN = 'deviceUuidOrigin'
# Placeholders like "(onboard)" live in the lcsc field of a few curated entries;
# they are not orderable C-numbers and must never be sent to `lib by-lcsc`.
LCSC_RE = re.compile(r'C\d+$', re.IGNORECASE)


def normalize_lcsc(value):
    """'  c6186 ' → 'C6186'; anything that is not a C-number → ''."""
    text = str(value or '').strip().upper()
    return text if LCSC_RE.match(text) else ''


def _utf8_console():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8', errors='replace')
        except (AttributeError, ValueError):
            pass


def extract_json(text):
    """Parse the JSON object in CLI stdout, ignoring non-JSON lines around it.

    The CLI may print progress/warning lines before or after the response; the
    document is taken from the first '{' to the last '}'. Raises ValueError when
    there is no object or it does not parse.
    """
    if text is None:
        raise ValueError('empty stdout')
    start, end = text.find('{'), text.rfind('}')
    if start < 0 or end < start:
        raise ValueError('no JSON object in CLI output')
    return json.loads(text[start:end + 1])


def components_of(doc):
    """Component list from a daemon response, a bare {components:[…]} or a list."""
    if isinstance(doc, list):
        return [c for c in doc if isinstance(c, dict)]
    if not isinstance(doc, dict):
        return []
    if doc.get('ok') is False:
        err = doc.get('error')
        msg = err.get('message') if isinstance(err, dict) else err
        raise ValueError('CLI reported failure: %s' % (msg or 'unknown error'))
    inner = doc.get('result') if isinstance(doc.get('result'), dict) else doc
    comps = inner.get('components')
    return [c for c in comps if isinstance(c, dict)] if isinstance(comps, list) else []


def index_by_lcsc(components):
    """lcsc → [component…]; C-numbers are compared upper-cased and trimmed."""
    out = {}
    for c in components:
        key = normalize_lcsc(c.get('lcsc'))
        if key:
            out.setdefault(key, []).append(c)
    return out


def relocalize(parts, resolved, library_uuid):
    """Pure transform: (parts dict, lcsc→components, file libraryUuid) → (new parts, summary).

    `resolved` is the merged index from every successful by-lcsc batch. Parts are
    deep-copied; the input is not mutated. Summary keys: same / changed /
    unresolved / libraryMismatch (lists of part keys) and warnings (strings).
    """
    new_parts = {}
    summary = {'same': [], 'changed': [], 'unresolved': [], 'libraryMismatch': [], 'warnings': []}
    for key, entry in parts.items():
        entry = json.loads(json.dumps(entry, ensure_ascii=False))
        new_parts[key] = entry
        if not isinstance(entry, dict):
            summary['unresolved'].append(key)
            summary['warnings'].append('%s: entry is not an object' % key)
            continue
        entry.pop(MARK, None)
        lcsc = normalize_lcsc(entry.get('lcsc'))
        want_lib = str(entry.get('libraryUuid') or library_uuid or '')
        hits = resolved.get(lcsc, []) if lcsc else []
        if want_lib:
            same_lib = [h for h in hits if str(h.get('libraryUuid') or '') == want_lib]
            if same_lib:
                hits = same_lib
        uuids = sorted({str(h.get('uuid') or '') for h in hits if h.get('uuid')})
        if not lcsc:
            entry[MARK] = 'unresolved'
            summary['unresolved'].append(key)
            summary['warnings'].append('%s: lcsc %r is not a C-number, cannot resolve'
                                       % (key, entry.get('lcsc')))
            continue
        if not uuids:
            entry[MARK] = 'unresolved'
            summary['unresolved'].append(key)
            continue
        if len(uuids) > 1:
            entry[MARK] = 'unresolved'
            summary['unresolved'].append(key)
            summary['warnings'].append('%s: %s resolved to %d devices (%s); pick one by hand'
                                       % (key, lcsc, len(uuids), ', '.join(uuids)))
            continue
        hit = hits[0]
        got_lib = str(hit.get('libraryUuid') or '')
        if want_lib and got_lib and got_lib != want_lib:
            entry[MARK] = 'libraryUuid-mismatch'
            summary['libraryMismatch'].append(key)
            summary['warnings'].append(
                '%s: %s lives in library %s (file says %s); uuid %s NOT applied — check the entry by hand'
                % (key, lcsc, got_lib, want_lib, uuids[0]))
            continue
        current = str(entry.get('deviceUuid') or '')
        if current == uuids[0]:
            summary['same'].append(key)
            continue
        if current and ORIGIN not in entry:
            entry[ORIGIN] = current
        entry['deviceUuid'] = uuids[0]
        summary['changed'].append(key)
    return new_parts, summary


def find_cli(explicit=None):
    """Locate the easyeda binary: --easyeda (path or name) first, then PATH.

    A path is accepted only when it really exists, so a typo fails fast with a
    clear message instead of an opaque OSError per batch. Returns None when
    nothing usable is found. Windows: `shutil.which` applies PATHEXT, so a bare
    `easyeda` resolves to `easyeda.exe`.
    """
    if explicit:
        if os.path.isfile(explicit):
            return explicit
        return shutil.which(explicit)
    return shutil.which('easyeda')


def batches(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def build_command(binary, lcsc_batch, project=None, window=None):
    cmd = [binary, 'lib', 'by-lcsc', '--lcsc', ','.join(lcsc_batch)]
    if project:
        cmd += ['--project', project]
    if window:
        cmd += ['--window', window]
    return cmd


def run_cli(cmd, timeout):
    """Run one by-lcsc batch; returns (components, error string or None)."""
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=timeout)
    except OSError as e:
        return [], 'cannot run %s: %s' % (cmd[0], e)
    except subprocess.TimeoutExpired:
        return [], 'timed out after %ss' % timeout
    out = proc.stdout.decode('utf-8', errors='replace')
    err = proc.stderr.decode('utf-8', errors='replace').strip()
    try:
        comps = components_of(extract_json(out))
    except ValueError as e:
        tail = err or out.strip()
        detail = tail.splitlines()[-1] if tail else ''
        return [], '%s (exit %s) %s' % (e, proc.returncode, detail)
    if proc.returncode != 0 and not comps:
        return [], 'exit %s: %s' % (proc.returncode, err.splitlines()[-1] if err else 'no components')
    return comps, None


def resolve_all(binary, lcscs, project, window, batch_size, timeout, log):
    """Query every batch; returns (lcsc→components index, batch results)."""
    resolved, results = {}, []
    for batch in batches(lcscs, batch_size):
        cmd = build_command(binary, batch, project, window)
        comps, error = run_cli(cmd, timeout)
        results.append({'lcsc': batch, 'count': len(comps), 'error': error})
        if error:
            log('batch %s..%s FAILED: %s' % (batch[0], batch[-1], error))
            continue
        for key, hits in index_by_lcsc(comps).items():
            resolved.setdefault(key, []).extend(hits)
        log('batch %s..%s → %d components' % (batch[0], batch[-1], len(comps)))
    return resolved, results


def load_parts(path):
    with open(path, 'r', encoding='utf-8') as f:
        doc = json.load(f)
    if not isinstance(doc, dict) or not isinstance(doc.get('parts'), dict):
        raise ValueError('%s: expected {"libraryUuid": …, "parts": {…}}' % path)
    return doc


def main(argv=None):
    _utf8_console()
    ap = argparse.ArgumentParser(
        prog='parts-relocalize.py',
        description='Re-resolve standard-parts.json deviceUuids through `easyeda lib by-lcsc` '
                    'for the connected EasyEDA edition and write a relocalized copy.',
        epilog='Example: parts-relocalize.py --out /tmp/parts.intl.json --project demo && '
               'easyeda sch block-apply usb_c_power --parts /tmp/parts.intl.json --project demo')
    ap.add_argument('--parts', default=DEFAULT_PARTS,
                    help='source standard-parts.json (default: the Skill copy next to this script)')
    ap.add_argument('--out', help='output file (required unless --dry-run); never the source path')
    ap.add_argument('--easyeda', default=None, help='easyeda binary (default: `easyeda` on PATH)')
    ap.add_argument('--project', default=None, help='passed through to the CLI as --project')
    ap.add_argument('--window', default=None, help='passed through to the CLI as --window')
    ap.add_argument('--batch', type=int, default=BATCH_MAX,
                    help='C-numbers per by-lcsc call (1..%d, default %d)' % (BATCH_MAX, BATCH_MAX))
    ap.add_argument('--timeout', type=float, default=120.0, help='seconds per CLI call (default 120)')
    ap.add_argument('--dry-run', action='store_true', help='query and report, write nothing')
    ap.add_argument('--json', action='store_true', help='print the summary as JSON on stdout')
    args = ap.parse_args(argv)

    def log(msg):
        print(msg, file=sys.stderr)

    if not args.dry_run and not args.out:
        ap.error('--out is required (or use --dry-run)')
    if not 1 <= args.batch <= BATCH_MAX:
        ap.error('--batch must be within 1..%d' % BATCH_MAX)
    src = os.path.abspath(args.parts)
    if args.out and os.path.abspath(args.out) == src:
        ap.error('--out must not be the source file; write a copy and keep the canonical file intact')

    try:
        doc = load_parts(src)
    except OSError as e:
        log('parts-relocalize.py: cannot read %s: %s' % (src, e))
        return 1
    except ValueError as e:
        log('parts-relocalize.py: %s is not a standard-parts.json: %s' % (src, e))
        return 1

    binary = find_cli(args.easyeda)
    if not binary:
        log('parts-relocalize.py: easyeda CLI not found (%s); pass --easyeda <path> or add it to PATH'
            % (args.easyeda or 'easyeda'))
        return 2

    parts = doc['parts']
    lcscs = sorted({normalize_lcsc(p.get('lcsc')) for p in parts.values() if isinstance(p, dict)} - {''})
    log('%s: %d parts, %d distinct C-numbers, libraryUuid %s'
        % (os.path.basename(src), len(parts), len(lcscs), doc.get('libraryUuid')))

    resolved, results = resolve_all(binary, lcscs, args.project, args.window, args.batch, args.timeout, log)
    ok_batches = sum(1 for r in results if not r['error'])
    if lcscs and ok_batches == 0:
        log('parts-relocalize.py: no by-lcsc batch succeeded (%d tried); is the daemon/editor connected?'
            % len(results))
        return 2

    new_parts, summary = relocalize(parts, resolved, str(doc.get('libraryUuid') or ''))
    summary['batches'] = {'ok': ok_batches, 'failed': len(results) - ok_batches}
    summary['source'] = src
    summary['out'] = None if args.dry_run else os.path.abspath(args.out)

    if not args.dry_run:
        out_doc = dict(doc)
        out_doc['parts'] = new_parts
        out_doc[MARK] = {
            'source': os.path.basename(src),
            'note': 'edition-local copy produced by parts-relocalize.py; do not commit over the canonical file',
            'same': len(summary['same']), 'changed': len(summary['changed']),
            'unresolved': len(summary['unresolved']), 'libraryMismatch': len(summary['libraryMismatch']),
        }
        out_dir = os.path.dirname(os.path.abspath(args.out))
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(args.out, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(out_doc, f, ensure_ascii=False, indent=2)
            f.write('\n')

    for w in summary['warnings']:
        log('warning: ' + w)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print('same %d / changed %d / unresolved %d / libraryUuid-mismatch %d (batches ok %d, failed %d)'
              % (len(summary['same']), len(summary['changed']), len(summary['unresolved']),
                 len(summary['libraryMismatch']), ok_batches, len(results) - ok_batches))
        if summary['unresolved']:
            print('unresolved: ' + ', '.join(summary['unresolved']))
        if summary['libraryMismatch']:
            print('libraryUuid-mismatch: ' + ', '.join(summary['libraryMismatch']))
        print('dry-run: nothing written' if args.dry_run else 'written: %s' % summary['out'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
