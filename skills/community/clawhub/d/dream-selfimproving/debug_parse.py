from pathlib import Path
import re, sys

content = Path(r'C:\Users\26240\.openclaw\workspace\skills\dream\scripts\dream.py').read_text(encoding='utf-8', errors='replace')
idx = content.find('def parse_distillation_output')
end_idx = content.find('\n\ndef ', idx + 100)
print(content[idx:end_idx])
