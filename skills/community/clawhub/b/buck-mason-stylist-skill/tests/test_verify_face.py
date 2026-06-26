"""Unit tests for scripts/verify-face.py.

Mocks the OpenAI vision call so we can test the threshold logic + JSON
parsing + server-side override of the model's overall_pass without
spending money or needing network. Uses a HTTP server fixture rather
than monkey-patching urllib because the script invokes urllib directly.
"""
import http.server, json, os, pathlib, shutil, subprocess, threading, time

REPO_ROOT      = pathlib.Path(__file__).resolve().parent.parent
VERIFY_SCRIPT  = REPO_ROOT / "scripts" / "verify-face.py"
MINIMAL_JPEG   = REPO_ROOT / "tests" / "fixtures" / "minimal.jpg"


def _make_minimal_image(path: pathlib.Path):
    """Copy the bundled minimal JPEG fixture so the file can be base64-encoded into the request."""
    shutil.copy(MINIMAL_JPEG, path)


class _FakeOpenAIHandler(http.server.BaseHTTPRequestHandler):
    """Pretend to be api.openai.com /v1/chat/completions."""

    # The test sets this on the class before each call.
    response_payload: dict = {}
    http_status: int = 200

    def do_POST(self):  # noqa: N802
        # Don't bother reading/validating the multipart; just emit a canned
        # chat-completions response.
        body = json.dumps({
            "choices": [{
                "message": {"content": json.dumps(self.response_payload)},
            }],
        }).encode("utf-8")
        self.send_response(self.http_status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a, **k):
        pass  # silence


def _start_fake_openai():
    """Spin up a localhost server pretending to be the OpenAI API.
    Returns (server, host, port)."""
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _FakeOpenAIHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server, "127.0.0.1", server.server_port


def _run_verify(generated, references, server_url, **kwargs):
    """Run scripts/verify-face.py against a fake OpenAI host.
    The script doesn't honor an --api-base flag; we route via /etc/hosts
    -style stubbing by setting the OPENAI_API_KEY and patching urllib via
    an env var the script uses. Since the script hardcodes the URL,
    alternatively we inject by replacing the URL with a custom env."""
    # The script hardcodes the OpenAI URL; we test it by importing the module
    # under a patched urllib.request. Cleanest path: invoke as subprocess
    # with a wrapper that stubs the URL via PYTHONSTARTUP. Keep it pragmatic:
    # use a wrapper script that monkey-patches urllib.request.Request to
    # route /v1/chat/completions to the fake server.
    raise NotImplementedError  # stubbed; see test functions below


def test_verify_face_passes_when_all_scores_above_threshold(tmp_path, monkeypatch):
    """Strong scores + low off_putting → exit 0, overall_pass: true."""
    gen = tmp_path / "gen.png"
    ref = tmp_path / "ref.jpg"
    _make_minimal_image(gen)
    _make_minimal_image(ref)

    _FakeOpenAIHandler.response_payload = {
        "scores": {
            "hair_match": 9, "beard_match": 9, "eye_color_match": 8,
            "skin_tone_match": 8, "age_match": 9, "asymmetry_match": 8,
        },
        "off_putting": 3,
        "overall_pass": True,
        "reason": "All features match well.",
    }
    _FakeOpenAIHandler.http_status = 200

    server, host, port = _start_fake_openai()
    try:
        env = {**os.environ, "OPENAI_API_KEY": "sk-test"}
        # Route the script's OpenAI URL through the fake server via a tiny
        # wrapper-script that monkey-patches urllib before importing.
        wrapper = tmp_path / "wrap.py"
        wrapper.write_text(f"""
import sys, urllib.request
orig = urllib.request.Request
def patched(url, *a, **kw):
    url = url.replace("https://api.openai.com", "http://{host}:{port}")
    return orig(url, *a, **kw)
urllib.request.Request = patched
sys.argv = ["verify-face.py", "--generated", "{gen}",
            "--reference", "{ref}", "--threshold", "6", "--off-putting-cap", "4"]
exec(open("{VERIFY_SCRIPT}").read())
""")
        r = subprocess.run(["python3", str(wrapper)], env=env, capture_output=True, text=True, timeout=15)
        assert r.returncode == 0, f"expected pass, got rc={r.returncode}\n{r.stdout}\n{r.stderr}"
        out = json.loads(r.stdout)
        assert out["overall_pass"] is True
        assert out["off_putting"] == 3
    finally:
        server.shutdown()


def test_verify_face_fails_when_any_score_below_threshold(tmp_path):
    """Even one score below threshold → exit 1, overall_pass: false."""
    gen = tmp_path / "gen.png"
    ref = tmp_path / "ref.jpg"
    _make_minimal_image(gen)
    _make_minimal_image(ref)

    _FakeOpenAIHandler.response_payload = {
        "scores": {
            "hair_match": 9, "beard_match": 9, "eye_color_match": 8,
            "skin_tone_match": 8, "age_match": 9,
            "asymmetry_match": 4,        # ← below threshold of 6
        },
        "off_putting": 3,
        "overall_pass": True,             # ← model says pass; script must override
        "reason": "Asymmetry was simplified.",
    }
    _FakeOpenAIHandler.http_status = 200

    server, host, port = _start_fake_openai()
    try:
        wrapper = tmp_path / "wrap.py"
        wrapper.write_text(f"""
import sys, urllib.request
orig = urllib.request.Request
def patched(url, *a, **kw):
    url = url.replace("https://api.openai.com", "http://{host}:{port}")
    return orig(url, *a, **kw)
urllib.request.Request = patched
sys.argv = ["verify-face.py", "--generated", "{gen}",
            "--reference", "{ref}", "--threshold", "6", "--off-putting-cap", "4"]
exec(open("{VERIFY_SCRIPT}").read())
""")
        env = {**os.environ, "OPENAI_API_KEY": "sk-test"}
        r = subprocess.run(["python3", str(wrapper)], env=env, capture_output=True, text=True, timeout=15)
        assert r.returncode == 1, f"expected fail, got rc={r.returncode}\n{r.stdout}"
        out = json.loads(r.stdout)
        # Script should override the model's overall_pass to false.
        assert out["overall_pass"] is False
    finally:
        server.shutdown()


def test_verify_face_fails_when_off_putting_above_cap(tmp_path):
    """High off_putting score → exit 1 even if all match scores pass."""
    gen = tmp_path / "gen.png"
    ref = tmp_path / "ref.jpg"
    _make_minimal_image(gen)
    _make_minimal_image(ref)

    _FakeOpenAIHandler.response_payload = {
        "scores": {
            "hair_match": 9, "beard_match": 9, "eye_color_match": 9,
            "skin_tone_match": 9, "age_match": 9, "asymmetry_match": 9,
        },
        "off_putting": 7,                # ← above cap of 4
        "overall_pass": True,
        "reason": "Smooth-symmetric AI-male face.",
    }
    _FakeOpenAIHandler.http_status = 200

    server, host, port = _start_fake_openai()
    try:
        wrapper = tmp_path / "wrap.py"
        wrapper.write_text(f"""
import sys, urllib.request
orig = urllib.request.Request
def patched(url, *a, **kw):
    url = url.replace("https://api.openai.com", "http://{host}:{port}")
    return orig(url, *a, **kw)
urllib.request.Request = patched
sys.argv = ["verify-face.py", "--generated", "{gen}",
            "--reference", "{ref}", "--threshold", "6", "--off-putting-cap", "4"]
exec(open("{VERIFY_SCRIPT}").read())
""")
        env = {**os.environ, "OPENAI_API_KEY": "sk-test"}
        r = subprocess.run(["python3", str(wrapper)], env=env, capture_output=True, text=True, timeout=15)
        assert r.returncode == 1, f"expected fail, got rc={r.returncode}\n{r.stdout}"
        out = json.loads(r.stdout)
        assert out["overall_pass"] is False
    finally:
        server.shutdown()


def test_verify_face_inconclusive_on_missing_api_key(tmp_path):
    """No OPENAI_API_KEY → exit 2 (inconclusive — setup error, not face fail)."""
    gen = tmp_path / "gen.png"
    ref = tmp_path / "ref.jpg"
    _make_minimal_image(gen)
    _make_minimal_image(ref)

    env = {k: v for k, v in os.environ.items() if k != "OPENAI_API_KEY"}
    r = subprocess.run(
        ["python3", str(VERIFY_SCRIPT),
         "--generated", str(gen),
         "--reference", str(ref)],
        env=env, capture_output=True, text=True, timeout=10,
    )
    assert r.returncode == 2
    assert "OPENAI_API_KEY" in r.stderr


def test_verify_face_inconclusive_on_missing_files(tmp_path):
    """Missing reference path → exit 2."""
    gen = tmp_path / "gen.png"
    _make_minimal_image(gen)

    env = {**os.environ, "OPENAI_API_KEY": "sk-test"}
    r = subprocess.run(
        ["python3", str(VERIFY_SCRIPT),
         "--generated", str(gen),
         "--reference", str(tmp_path / "does-not-exist.jpg")],
        env=env, capture_output=True, text=True, timeout=10,
    )
    assert r.returncode == 2
    assert "not found" in r.stderr
