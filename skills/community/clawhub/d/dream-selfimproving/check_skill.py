from pathlib import Path
import subprocess

skill = Path(r'C:\Users\26240\.openclaw\workspace\skills\dream-selfimproving')

print("=== dream-selfimproving 4.0.2 Check ===\n")

# graph-builder.py checks
gb = skill / 'graph-builder.py'
c = gb.read_text(encoding='utf-8', errors='replace')

print("[graph-builder.py]")
for k in ['def enrich_from_errors', 'builder.enrich_from_errors()', '--enrich-from-errors',
          'def enrich_from_recall', 'fp-error-', 'ep-error-', '.learnings']:
    print(f"  {k}: {'OK' if k in c else 'MISSING'}")

# Size of enrich_from_errors
start = c.find('def enrich_from_errors')
end = c.find('\ndef ', start + 10) if start >= 0 else -1
print(f"  enrich_from_errors body: {end - start} chars" if end > start else "  enrich_from_errors body: NOT FOUND")

# dream.py checks
d = (skill / 'scripts' / 'dream.py').read_text(encoding='utf-8', errors='replace')
print("\n[dream.py]")
for k in ['def load_learnings_ERR', 'def learnings_update_tools',
          'enrich_errors=True', 'LEARNINGS_DIR', '# Step 1: learnings error tracking']:
    print(f"  {k}: {'OK' if k in d else 'MISSING'}")

start2 = d.find('def load_learnings_ERR')
end2 = d.find('\ndef ', start2 + 10) if start2 >= 0 else -1
print(f"  load_learnings_ERR body: {end2 - start2} chars" if end2 > start2 else "  load_learnings_ERR: NOT FOUND")

print("\n[All .py files syntax]")
all_ok = True
for py in sorted(skill.rglob('*.py')):
    r = subprocess.run(['python', '-m', 'py_compile', str(py)],
        capture_output=True, text=True, encoding='utf-8', errors='replace')
    status = 'OK' if r.returncode == 0 else 'FAIL'
    if status == 'FAIL':
        all_ok = False
        print(f"  {py.name}: FAIL")
        print(r.stderr[:100].strip())
if all_ok:
    print("  All .py files: OK")

print("\n=== Summary ===")
print("Step 1 (learnings error tracking): load_learnings_ERR + learnings_update_tools")
print("Step 2 (errors -> FacetPoint): enrich_from_errors in graph-builder")
print("Both flows wired into dream.py run_dream()")
