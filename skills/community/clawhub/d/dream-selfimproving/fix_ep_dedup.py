from pathlib import Path

gb = Path(r'C:\Users\26240\.openclaw\workspace\skills\dream\graph-builder.py')
c = gb.read_text(encoding='utf-8', errors='replace')

idx = c.find('def link_facetpoint_to_episode')
segment = c[idx:idx+600]
print('First 600 chars:')
print(repr(segment[:600]))
