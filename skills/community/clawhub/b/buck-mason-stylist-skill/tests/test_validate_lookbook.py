"""End-to-end tests for scripts/validate-lookbook.py.

Builds synthetic deploy directories that should pass / fail each local
gate (L1-L10) and asserts the right exit code. Deployed checks (D1-D6)
are not exercised here — they require a live URL.
"""
import pathlib, shutil, subprocess

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
VALIDATE_SCRIPT = REPO_ROOT / "scripts" / "validate-lookbook.py"
MINIMAL_JPEG = REPO_ROOT / "tests" / "fixtures" / "minimal.jpg"


def run_validate(dir_path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", str(VALIDATE_SCRIPT), "--dir", str(dir_path)],
        capture_output=True, text=True, timeout=30,
    )


def write_minimal_jpeg(path: pathlib.Path, size_bytes: int = 200) -> None:
    """Copy the bundled minimal-but-valid JPEG fixture to the test path.

    The fixture (`tests/fixtures/minimal.jpg`, 222 bytes) is a real
    SOI/JFIF/EOI-framed JPEG. Validate-lookbook only stats the file size
    and inspects the MIME via the extension, so any compliant JPEG works;
    `size_bytes` is accepted for backwards compatibility with older calls
    but ignored — pad in the caller if a specific size matters.
    """
    shutil.copy(MINIMAL_JPEG, path)
    _ = size_bytes  # unused; kept for signature compatibility


def good_html(extra_meta: str = "") -> str:
    """Reusable minimal-but-passing HTML body used as a test fixture.
    Includes everything the L1-L10 gates need.

    Padded with comment text to exceed the L1 file-size floor (4 KB)
    without affecting the parseable structure tested by L2-L10."""
    # 4 KB filler in a single HTML comment — ignored by every regex check.
    filler = ("<!-- " + ("padding " * 80) + "-->\n") * 8
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Buck Mason</title>
  <meta property="og:type" content="website">
  <meta property="og:title" content="Test Lookbook">
  <meta property="og:description" content="A test lookbook.">
  <meta property="og:url" content="https://test.pages.dev/">
  <meta property="og:image" content="https://test.pages.dev/og.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Test Lookbook">
  <meta name="twitter:description" content="A test lookbook.">
  <meta name="twitter:image" content="https://test.pages.dev/og.jpg">
  {extra_meta}
</head>
<body>
{filler}
  <p>AI-generated try-on previews — not real photos.</p>
  <section class="look">
    <img src="look1.jpg" data-fullsize="look1.jpg">
    <label class="piece">
      <input type="checkbox" data-name="Camp Shirt" data-size="L" data-sku="CAMP-L" data-qty="1" data-price-cents="9800">
      <img src="thumb.jpg" data-fullsize="thumb.jpg">
      <div>
        <div>Camp Shirt</div>
        <div>$98</div>
        <a href="https://www.buckmason.com/products/camp-shirt">View</a>
        <div>Size L · In stock</div>
      </div>
    </label>
  </section>
</body>
</html>"""


def make_passing_deploy(tmp_path):
    d = tmp_path / "deploy"
    d.mkdir()
    (d / "index.html").write_text(good_html())
    write_minimal_jpeg(d / "og.jpg", size_bytes=4096)
    return d


# ── Happy path ─────────────────────────────────────────────────────────────

def test_passing_deploy_exits_zero(tmp_path):
    d = make_passing_deploy(tmp_path)
    r = run_validate(d)
    assert r.returncode == 0, f"expected 0, got {r.returncode}: {r.stdout}\n{r.stderr}"


# ── Per-gate failures ──────────────────────────────────────────────────────

def test_l1_missing_index_html_fails(tmp_path):
    d = tmp_path / "deploy"
    d.mkdir()
    write_minimal_jpeg(d / "og.jpg", size_bytes=4096)
    r = run_validate(d)
    assert r.returncode == 1
    assert "L1" in r.stderr or "index.html missing" in r.stderr


def test_l1_tiny_index_html_fails(tmp_path):
    d = tmp_path / "deploy"
    d.mkdir()
    (d / "index.html").write_text("tiny")  # < 4 KB
    write_minimal_jpeg(d / "og.jpg", size_bytes=4096)
    r = run_validate(d)
    assert r.returncode == 1
    assert "L1" in r.stderr


def test_l6_unsubstituted_placeholder_in_og_url_fails(tmp_path):
    d = tmp_path / "deploy"
    d.mkdir()
    bad = good_html().replace(
        'content="https://test.pages.dev/"',
        'content="{{ABSOLUTE_PAGE_URL}}"',
    )
    (d / "index.html").write_text(bad)
    write_minimal_jpeg(d / "og.jpg", size_bytes=4096)
    r = run_validate(d)
    assert r.returncode == 1
    assert "L6" in r.stderr


def test_l6_relative_og_url_fails(tmp_path):
    d = tmp_path / "deploy"
    d.mkdir()
    bad = good_html().replace(
        'content="https://test.pages.dev/og.jpg"',
        'content="/og.jpg"',
    )
    (d / "index.html").write_text(bad)
    write_minimal_jpeg(d / "og.jpg", size_bytes=4096)
    r = run_validate(d)
    assert r.returncode == 1
    assert "L6" in r.stderr


def test_l7_missing_og_jpg_fails(tmp_path):
    d = tmp_path / "deploy"
    d.mkdir()
    (d / "index.html").write_text(good_html())
    # No og.jpg.
    r = run_validate(d)
    assert r.returncode == 1
    assert "L7" in r.stderr


def test_l8_piece_missing_data_attrs_fails(tmp_path):
    d = tmp_path / "deploy"
    d.mkdir()
    bad = good_html().replace(
        'data-sku="CAMP-L"', "",
    )
    (d / "index.html").write_text(bad)
    write_minimal_jpeg(d / "og.jpg", size_bytes=4096)
    r = run_validate(d)
    assert r.returncode == 1
    assert "L8" in r.stderr


def test_l3_piece_without_price_fails(tmp_path):
    """A .piece block with no $price token should fail L3."""
    d = tmp_path / "deploy"
    d.mkdir()
    bad = good_html().replace("$98", "free")
    (d / "index.html").write_text(bad)
    write_minimal_jpeg(d / "og.jpg", size_bytes=4096)
    r = run_validate(d)
    assert r.returncode == 1
    assert "L3" in r.stderr


def test_l4_piece_without_stock_line_fails(tmp_path):
    """A .piece block with no In stock / Low / Out token fails L4."""
    d = tmp_path / "deploy"
    d.mkdir()
    bad = good_html().replace("Size L · In stock", "Size L · ?")
    (d / "index.html").write_text(bad)
    write_minimal_jpeg(d / "og.jpg", size_bytes=4096)
    r = run_validate(d)
    assert r.returncode == 1
    assert "L4" in r.stderr


def test_l5_ai_disclosure_required_when_look_image_present(tmp_path):
    """If a look<N>.jpg img is referenced, AI disclosure copy must
    also be present somewhere in the page."""
    d = tmp_path / "deploy"
    d.mkdir()
    bad = good_html().replace("AI-generated try-on previews — not real photos.", "")
    (d / "index.html").write_text(bad)
    write_minimal_jpeg(d / "og.jpg", size_bytes=4096)
    r = run_validate(d)
    assert r.returncode == 1
    assert "L5" in r.stderr


def test_l10_empty_data_fullsize_fails(tmp_path):
    """`data-fullsize=""` is a placeholder leftover and should fail L10."""
    d = tmp_path / "deploy"
    d.mkdir()
    bad = good_html().replace('data-fullsize="thumb.jpg"', 'data-fullsize=""')
    (d / "index.html").write_text(bad)
    write_minimal_jpeg(d / "og.jpg", size_bytes=4096)
    r = run_validate(d)
    assert r.returncode == 1
    assert "L10" in r.stderr


def test_no_dir_or_url_arg_returns_2(tmp_path):
    """Calling validate with neither --dir nor --url errors."""
    r = subprocess.run(
        ["python3", str(VALIDATE_SCRIPT)],
        capture_output=True, text=True, timeout=10,
    )
    assert r.returncode == 2
    assert "specify --dir or --url" in r.stderr
