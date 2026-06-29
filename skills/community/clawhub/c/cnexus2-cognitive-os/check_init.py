#!/usr/bin/env python3
"""Check init code and window assignments in new shell."""
with open("D:/类脑记忆/CNexus2.0/app_ui_new.py", "r", encoding="utf-8") as f:
    content = f.read()

marker = "SHELL_HTML = r"
apos = content.find(marker) + 15
bpos = content.find("'''", apos)
shell = content[apos:bpos]

# Check window assignments
checks = [
    "window.pollStatus=pollStatus;",
    "window.drawFlowGraph=drawFlowGraph;",
    "window.switchView=switchView;",
    "window.gvInitControls=gvInitControls;",
    "window.gvToggle=gvToggle;",
    "window.gvSetSlider=gvSetSlider;",
    "window.gvSetSearch=gvSetSearch;",
    "window.refreshAll=refreshAll;",
]
for c in checks:
    if c in shell:
        print(f"  OK {c}")
    else:
        print(f"  MISSING {c}")

# Find init code
init_pos = shell.find("// Init")
if init_pos >= 0:
    print(f"\nInit code at offset {init_pos}:")
    print(shell[init_pos:init_pos+600])
else:
    print("\nNo // Init comment found, looking for pollStatus()")
    # The old init code is at the end of the JS
    ps_pos = shell.find("pollStatus();")
    if ps_pos >= 0:
        print(shell[ps_pos-50:ps_pos+300])
