"""Unit test: verify GhostPublisher exposes all seven Publisher Interface v1
methods with the expected signatures. Does not hit Ghost."""

import sys
import inspect
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import publisher as pub_mod


REQUIRED_METHODS = {
    "createPost":   ["post"],
    "updatePost":   ["post_id", "fields"],
    "publishPost":  ["post_id", "opts"],
    "schedulePost": ["post_id", "datetime_iso"],
    "deletePost":   ["post_id"],
    "uploadImage":  ["url_or_path", "alt"],
    "getPost":      ["post_id"],
}


def test_class_exists():
    assert hasattr(pub_mod, "GhostPublisher"), "GhostPublisher class missing"
    print("[PASS] GhostPublisher class exists")


def test_all_seven_methods_exist():
    cls = pub_mod.GhostPublisher
    for name in REQUIRED_METHODS:
        assert hasattr(cls, name), f"method {name} missing from GhostPublisher"
        assert callable(getattr(cls, name)), f"{name} is not callable"
    print(f"[PASS] all seven Publisher Interface v1 methods present: "
          f"{sorted(REQUIRED_METHODS)}")


def test_method_signatures():
    cls = pub_mod.GhostPublisher
    for name, expected_params in REQUIRED_METHODS.items():
        sig = inspect.signature(getattr(cls, name))
        # Drop 'self'
        params = [p for p in sig.parameters if p != "self"]
        for p in expected_params:
            assert p in params, (
                f"{name}{tuple(params)} missing expected parameter {p!r}"
            )
    print("[PASS] all method signatures include the expected parameters")


def test_constructor_allows_explicit_credentials():
    """Should not need env vars if both URL and key are passed explicitly."""
    # Remove env vars to simulate caller passing everything in
    import os
    saved = {k: os.environ.pop(k, None) for k in ("GHOST_URL", "GHOST_ADMIN_API_KEY")}
    try:
        p = pub_mod.GhostPublisher(
            ghost_url="https://example.test",
            admin_api_key="abc123:" + "de" * 32,
            config={},
        )
        assert p.ghost_url == "https://example.test"
        assert p.admin_api_key.startswith("abc123:")
    finally:
        for k, v in saved.items():
            if v is not None:
                os.environ[k] = v
    print("[PASS] constructor accepts explicit credentials without env vars")


def test_constructor_errors_without_creds():
    """Without env vars and without explicit credentials, should raise."""
    import os
    saved = {k: os.environ.pop(k, None) for k in ("GHOST_URL", "GHOST_ADMIN_API_KEY")}
    try:
        try:
            pub_mod.GhostPublisher()
        except RuntimeError as e:
            assert "GHOST_URL" in str(e) or "GHOST_ADMIN_API_KEY" in str(e)
            print("[PASS] constructor raises RuntimeError when creds missing")
            return
        raise AssertionError("expected RuntimeError when no credentials provided")
    finally:
        for k, v in saved.items():
            if v is not None:
                os.environ[k] = v


if __name__ == "__main__":
    test_class_exists()
    test_all_seven_methods_exist()
    test_method_signatures()
    test_constructor_allows_explicit_credentials()
    test_constructor_errors_without_creds()
    print("\nAll 5 interface tests passed.")
