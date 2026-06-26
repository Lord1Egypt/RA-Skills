#!/usr/bin/env python3
"""ArmorClaw — full test suite."""
import sys, os, tempfile, shutil
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Use a temp vault dir for tests
_tmp_dir = tempfile.mkdtemp()
os.environ["HOME"] = _tmp_dir

from armorclaw.crypto import encrypt, decrypt
from armorclaw.auth   import validate_password, get_machine_fingerprint, LockConfig
from armorclaw.core   import ArmorClaw
from armorclaw.importer import parse_env_file

passed = failed = 0

def assert_(val, msg=""):
    assert val, msg

def test(name, fn):
    global passed, failed
    try:
        fn()
        print(f"  ✅ {name}")
        passed += 1
    except Exception as e:
        print(f"  ❌ {name}: {e}")
        failed += 1


# ── Crypto ────────────────────────────────────────────────────────────────
print("\nCrypto")
test("encrypt/decrypt roundtrip",
     lambda: assert_(decrypt(encrypt("my-secret-api-key-123", "P@ssw0rd!Secure"), "P@ssw0rd!Secure") == "my-secret-api-key-123"))

def _test_wrong_pw():
    try:
        decrypt(encrypt("secret", "P@ssw0rd!1"), "WrongPass1!")
        assert False, "Should have raised"
    except ValueError:
        pass

test("wrong password raises ValueError", _test_wrong_pw)
test("different keys produce different ciphertext",
     lambda: assert_(encrypt("same", "P@ssw0rd!1") != encrypt("same", "P@ssw0rd!2")))
test("special chars in value preserved",
     lambda: assert_(decrypt(encrypt("sk-abc!@#$%^&*()", "P@ssw0rd!1"), "P@ssw0rd!1") == "sk-abc!@#$%^&*()"))

def _test_wrong_pw():
    try:
        decrypt(encrypt("secret", "P@ssw0rd!1"), "WrongPass1!")
        assert False, "Should have raised"
    except ValueError:
        pass


# ── Password validation ───────────────────────────────────────────────────
print("\nPassword Validation")
test("strong password accepted",
     lambda: assert_(not validate_password("MyStr0ng!Pass#2026")))
test("too short rejected",
     lambda: assert_(validate_password("Short1!")))
test("no uppercase rejected",
     lambda: assert_(validate_password("nouppercase1!aaa")))
test("no number rejected",
     lambda: assert_(validate_password("NoNumbers!Here!!")))
test("no special char rejected",
     lambda: assert_(validate_password("NoSpecialChar1Abc")))


# ── Store / Core ──────────────────────────────────────────────────────────
print("\nVault Core")
PWD = "TestP@ss1!SecureX"

def test_setup():
    ck = ArmorClaw()
    assert not ck.is_setup
    r = ck.setup(password=PWD, mode="password")
    assert r["ok"], r
    assert ck.is_setup
    assert ck.is_unlocked

def test_set_get():
    ck = ArmorClaw()
    r = ck.unlock(PWD)
    assert r["ok"], r
    ck.set("OPENAI_KEY", "sk-testkey12345678901234567890")
    val = ck.get("OPENAI_KEY")
    assert val == "sk-testkey12345678901234567890"

def test_list():
    ck = ArmorClaw()
    ck.unlock(PWD)
    ck.set("KEY_A", "value_a")
    ck.set("KEY_B", "value_b")
    names = [s["name"] for s in ck.list()]
    assert "KEY_A" in names
    assert "KEY_B" in names

def test_delete():
    ck = ArmorClaw()
    ck.unlock(PWD)
    ck.set("TEMP_KEY", "temp")
    assert ck.get("TEMP_KEY") == "temp"
    ck.delete("TEMP_KEY")
    assert ck.get("TEMP_KEY") is None

def test_wrong_password():
    ck = ArmorClaw()
    r = ck.unlock("WrongPass1!nope")
    assert not r["ok"]

def test_locked_raises():
    ck = ArmorClaw()
    try:
        ck.get("ANYTHING")
        assert False, "Should raise"
    except PermissionError:
        pass

test("vault setup", test_setup)
test("set and get secret", test_set_get)
test("list secrets", test_list)
test("delete secret", test_delete)
test("wrong password rejected", test_wrong_password)
test("locked vault raises PermissionError", test_locked_raises)


# ── Importer ──────────────────────────────────────────────────────────────
print("\nImporter")

def test_parse_env():
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False)
    tmp.write("# comment\nOPENAI_KEY=sk-abc123\nDISCORD_TOKEN=tok456\n\nEMPTY=\n")
    tmp.close()
    parsed = parse_env_file(tmp.name)
    os.unlink(tmp.name)
    assert parsed["OPENAI_KEY"] == "sk-abc123"
    assert parsed["DISCORD_TOKEN"] == "tok456"
    assert "EMPTY" not in parsed or parsed.get("EMPTY") == ""

def test_import_env():
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False)
    tmp.write("IMPORT_TEST_KEY=imported_value_123\n")
    tmp.close()
    ck = ArmorClaw()
    ck.unlock(PWD)
    result = ck.import_env(tmp.name, after="keep")
    os.unlink(tmp.name)
    assert "IMPORT_TEST_KEY" in result.get("imported", [])
    assert ck.get("IMPORT_TEST_KEY") == "imported_value_123"

test("parse .env file", test_parse_env)
test("import .env into vault", test_import_env)


# ── Access log ────────────────────────────────────────────────────────────
print("\nAccess Log")

def test_access_log():
    ck = ArmorClaw()
    ck.unlock(PWD)
    ck.get("OPENAI_KEY", skill="senticlaw")
    log = ck.access_log("OPENAI_KEY", limit=5)
    assert any(e["skill"] == "senticlaw" for e in log)

def test_skill_report():
    ck = ArmorClaw()
    ck.unlock(PWD)
    ck.get("OPENAI_KEY", skill="clawpulse")
    report = ck.skill_report()
    assert "clawpulse" in report

test("access log records reads", test_access_log)
test("skill report shows usage", test_skill_report)


# ── Summary ───────────────────────────────────────────────────────────────
shutil.rmtree(_tmp_dir, ignore_errors=True)
print(f"\n{'='*40}")
print(f"  {passed} passed  ·  {failed} failed")
print(f"{'='*40}\n")
sys.exit(0 if failed == 0 else 1)
