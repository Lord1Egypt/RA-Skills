from pathlib import Path
import json

c = Path(r'C:\Users\26240\.openclaw\workspace\skills\dream\scripts\dream.py').read_text(encoding='utf-8', errors='replace')
lines = c.split('\n')

# Find the line with the closing """ of the report f-string
# It's line 876 currently (1-indexed)
print('Line 875 (before closing):', repr(lines[874][:80]))
print('Line 876 (closing):', repr(lines[875][:80]))
print('Line 877 (after):', repr(lines[876][:80]))
print('Line 878 (after):', repr(lines[877][:80]))
print('Line 879 (after):', repr(lines[878][:80]))
print()
print('The closing """ is at line 876 (1-indexed) = index 875')
print('Bundle Search wrongly at line 878 (1-indexed) = index 877')
print()
print('Fix: remove lines 877-878, insert Bundle section inside f-string before line 876')
