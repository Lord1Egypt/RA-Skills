from pathlib import Path

dream_py = Path(r'C:\Users\26240\.openclaw\workspace\skills\dream\scripts\dream.py')
c = dream_py.read_text(encoding='utf-8', errors='replace')

old = "is_raw = not v.get('snippet','').startswith(('assistant ', 'user '))"
new = "is_raw = not v.get('snippet','').startswith(('User:', 'assistant '))"

print('Found:', old in c)
c2 = c.replace(old, new, 1)
dream_py.write_text(c2, encoding='utf-8')
print('Replaced')
