#!/usr/bin/env python3
"""Verify new app_ui_new.py for embedded string terminators."""
with open("D:/类脑记忆/CNexus2.0/app_ui_new.py", "r", encoding="utf-8") as f:
    content = f.read()

# Find SHELL_HTML content
marker = "SHELL_HTML = r'''"
start = content.find(marker) + len(marker)
end = content.find("'''", start)
shell_content = content[start:end]

# Find FLOAT_HTML content
fmarker = "FLOAT_HTML = r'''"
fstart = content.find(fmarker) + len(fmarker)
fend = content.find("'''", fstart)
float_content = content[fstart:fend]

print(f"SHELL_HTML length: {len(shell_content)}")
print(f"FLOAT_HTML length: {len(float_content)}")

# Check for r''' that's not the delimeter
pos = shell_content.find("r'''")
if pos >= 0:
    print(f"WARNING: Found 'r' in SHELL_HTML at pos {pos}: ...{shell_content[max(0,pos-20):pos+20]}...")

pos = shell_content.find("\n'''")
if pos >= 0:
    print(f"WARNING: Found ''' on newline in SHELL_HTML at pos {pos}")

pos = float_content.find("\n'''")
if pos >= 0:
    print(f"WARNING: Found ''' on newline in FLOAT_HTML at pos {pos}")

print("First 80 of SHELL:", repr(shell_content[:80]))
print("Last 80 of SHELL:", repr(shell_content[-80:]))
print()
print("First 80 of FLOAT:", repr(float_content[:80]))
print("Last 80 of FLOAT:", repr(float_content[-80:]))

# Also check that the JS logic is in place
if "/* JS_LOGIC */" in shell_content:
    print("ERROR: JS_LOGIC placeholder not replaced!")
else:
    print("OK: JS_LOGIC replaced successfully")
    
# Check for key JS functions
for fn in ['pollStatus', 'drawFlowGraph', 'gvInitControls', 'gvBuildGraphViewModel']:
    if fn in shell_content:
        print(f"  OK {fn} present in SHELL_HTML")
    else:
        print(f"  MISSING {fn} in SHELL_HTML")

print("\nAll checks passed!")
