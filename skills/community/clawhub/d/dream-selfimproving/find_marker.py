from pathlib import Path
content = Path(r'C:\Users\26240\.openclaw\workspace\skills\dream\scripts\dream.py').read_text(encoding='utf-8', errors='replace')
bad_marker = 'Bundle Search'
idx_bad = content.find(bad_marker)
print('First occurrence at:', idx_bad)
print('Context:')
print(repr(content[idx_bad-200:idx_bad+300]))
