from pathlib import Path
c = Path(r'C:\Users\26240\.openclaw\workspace\skills\dream\graph-builder.py').read_text(encoding='utf-8', errors='replace')
idx = c.find('def build_all')
segment = c[idx:idx+800]
lines = segment.split('\n')
for i, line in enumerate(lines[:40]):
    print(i, line[:100])
