#!/usr/bin/env python3
"""Smoke + unit tests for agent-caps (stdlib only, no pytest needed)."""
import importlib.util
import os
import sys
import tempfile
import json

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "agent_caps.py")

spec = importlib.util.spec_from_file_location("agent_caps", SRC)
ac = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ac)

ok = True
def check(name, cond):
    global ok
    print(("PASS" if cond else "FAIL"), "-", name)
    ok = ok and cond

# 1) valid manifest passes
good = {"name": "Hermes", "version": "1.0", "capabilities": ["planning"],
        "dependencies": [], "memory_requirements": "256MB",
        "tools": ["terminal"], "api": "hermes_local", "status": "active"}
v, e = ac.validate_manifest(good)
check("valid manifest passes", v and not e)

# 2) missing required field fails
bad = {"name": "X", "version": "1.0"}
v2, e2 = ac.validate_manifest(bad)
check("missing fields detected", (not v2) and "missing required field" in e2[0])

# 3) bad version fails
badver = dict(good); badver["version"] = "v1"
v3, e3 = ac.validate_manifest(badver)
check("bad version rejected", not v3)

# 4) bad status rejected
bads = dict(good); bads["status"] = "running"
v4, e4 = ac.validate_manifest(bads)
check("bad status rejected", not v4)

# 5) CLI validate on a temp good file -> exit 0
tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
json.dump(good, tmp); tmp.close()
rc = ac.main(["validate", tmp.name])
check("CLI validate exit 0", rc == 0)
os.unlink(tmp.name)

# 6) CLI validate on invalid file -> exit 1
tmp2 = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
json.dump(bad, tmp2); tmp2.close()
rc2 = ac.main(["validate", tmp2.name])
check("CLI validate exit 1 on bad", rc2 == 1)
os.unlink(tmp2.name)

# 7) scaffold creates agent-manifest.json in a temp dir
d = tempfile.mkdtemp()
open(os.path.join(d, "README.md"), "w").write("# x")
rc3 = ac.main(["scaffold", d, "--name", "TestAgent"])
mf = os.path.join(d, "agent-manifest.json")
check("scaffold writes manifest", rc3 == 0 and os.path.isfile(mf))
# and the scaffolded manifest is itself valid
rc4 = ac.main(["validate", mf])
check("scaffolded manifest is valid", rc4 == 0)

# 8) check-deps detects unknown dependency
m1 = {"name": "A", "version": "1.0", "capabilities": ["x"], "dependencies": [],
      "memory_requirements": "1MB", "tools": [], "api": "x", "status": "active"}
m2 = {"name": "B", "version": "1.0", "capabilities": ["y"], "dependencies": ["A"],
      "memory_requirements": "1MB", "tools": [], "api": "x", "status": "active"}
m3 = {"name": "C", "version": "1.0", "capabilities": ["z"], "dependencies": ["ghost"],
      "memory_requirements": "1MB", "tools": [], "api": "x", "status": "active"}
f1 = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False); json.dump(m1, f1); f1.close()
f2 = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False); json.dump(m2, f2); f2.close()
f3 = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False); json.dump(m3, f3); f3.close()
rc5 = ac.main(["check-deps", f1.name, f2.name, f3.name])
check("check-deps flags unknown dep (exit 1)", rc5 == 1)
for f in (f1, f2, f3):
    os.unlink(f.name)

print("\nRESULT:", "ALL TESTS PASSED" if ok else "TESTS FAILED")
sys.exit(0 if ok else 1)
