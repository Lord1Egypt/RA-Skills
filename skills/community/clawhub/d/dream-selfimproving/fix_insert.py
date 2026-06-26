"""
Fix the wrongly-inserted Bundle Search section.
The text was inserted after the f-string closed, not inside it.
"""
from pathlib import Path

dream_py = Path(r'C:\Users\26240\.openclaw\workspace\skills\dream\scripts\dream.py')
content = dream_py.read_text(encoding='utf-8', errors='replace')
lines = content.split('\n')

# Remove lines 877-878 (0-indexed: 876-877) which are the wrongly placed text
# And insert the Bundle Search section INSIDE the f-string, before line 876 (the closing """)
# Line 876 (1-indexed) = index 875: the closing """

# The wrongly placed block starts at line 877 (index 876)
# We want to remove lines 877-878 (indices 876-877)

new_lines = lines[:876]  # keep lines 1-876 (indices 0-875)

# Insert Bundle Search section inside f-string, before the closing """
# Use a multi-line string that becomes part of the f-string
bundle_section = """
**Bundle Search 检索结果**: {len(bundle_results)} 个相关历史Episode
"""
new_lines.append(bundle_section)

# Skip the wrongly placed lines (indices 876-877) and continue from 878 (index 878)
new_lines.extend(lines[878:])

new_content = '\n'.join(new_lines)
dream_py.write_text(new_content, encoding='utf-8')
print('File rewritten.')

# Verify
import subprocess
r = subprocess.run(['python', '-m', 'py_compile', str(dream_py)],
                  capture_output=True, text=True, encoding='utf-8', errors='replace')
if r.returncode == 0:
    print('Syntax OK')
else:
    print('Syntax FAILED:', r.stderr[:300])
