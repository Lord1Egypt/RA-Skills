#!/usr/bin/env python3
"""Read-only comparison against a trusted release ZIP. No installation or execution."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile

import publish


def compare(release, installed, profile):
    publish.need(release.is_file(), 'Trusted release ZIP required')
    publish.need(installed.is_dir(), 'Select the actual installed package directory')
    expected = publish.load_files(release)
    metadata = publish.validate(expected, profile)
    if profile == 'folder':
        root = metadata['name'] + '/'
        expected = {name[len(root):]: data for name, data in expected.items()}
    actual = publish.load_files(installed)
    missing = sorted(set(expected) - set(actual))
    changed = sorted(n for n in expected.keys() & actual.keys() if expected[n] != actual[n])
    extra = sorted(set(actual) - set(expected))
    matched = not missing and not changed
    return {'artifact_role': 'installation-comparison-report', 'importable_workflow': False,
            'passed': matched, 'release_sha256': hashlib.sha256(release.read_bytes()).hexdigest(),
            'release_metadata': metadata, 'release_files_match': matched,
            'exact_file_set': matched and not extra, 'missing': missing, 'changed': changed,
            'extra': extra, 'files_checked': len(expected), 'network_called': False,
            'target_invocation': 'not_verified',
            'scope': 'Selected directory only; extra files listed, runtime/cache exclusions follow load_files. No repair, source authenticity or active-client verification.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('release', type=Path)
    p.add_argument('installed', type=Path)
    p.add_argument('--profile', choices=publish.PROFILES, default='standard')
    a = p.parse_args()
    try:
        result = compare(a.release, a.installed, a.profile)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result['passed'] else 1
    except (publish.Invalid, OSError, zipfile.BadZipFile) as exc:
        print(json.dumps({'artifact_role': 'installation-comparison-report', 'importable_workflow': False,
                          'passed': False, 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    sys.exit(main())
