from pathlib import Path
import sys


def main():
    if len(sys.argv) < 3:
        print('usage: python search_scans.py <root_dir> <query>')
        sys.exit(1)

    root = Path(sys.argv[1])
    query = sys.argv[2].lower()
    scan_root = root / 'daily-scan-storage'

    if not scan_root.exists():
        print('[]')
        return

    matches = []
    for p in scan_root.rglob('*.pdf'):
        if query in p.name.lower():
            matches.append(str(p))

    print('\n'.join(matches[:20]))


if __name__ == '__main__':
    main()
