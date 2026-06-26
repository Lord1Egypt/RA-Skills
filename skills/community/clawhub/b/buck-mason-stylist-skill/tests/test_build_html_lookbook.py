"""Smoke tests for scripts/build-html-lookbook.py.

The script does I/O (downloads thumbnails from product URLs, writes JPEGs)
so a true unit test is awkward. Instead we run it against synthetic picks
that already carry inline image_url fields and assert the expected files
land in --out and the HTML structure is sane.

Network dependency: thumbnail downloads use `curl` against pima.s3.
We use small known-stable URLs from the live MCP catalog. The build runs
in --no-tryon mode (Editorial tier) so no gpt-image-2 calls happen.
"""
import json, pathlib, re, subprocess

REPO_ROOT     = pathlib.Path(__file__).resolve().parent.parent
BUILD_SCRIPT  = REPO_ROOT / "scripts" / "build-html-lookbook.py"


def make_config(out_dir: pathlib.Path, lookbook_id: str = "test-lookbook") -> pathlib.Path:
    """Minimal lookbook config the build script consumes."""
    cfg = {
        "lookbook_id":    lookbook_id,
        "lookbook_title": "Test Lookbook",
        "lookbook_date":  "2026-05-09",
        "subtitle":       "A test lookbook for build-html-lookbook.py.",
        "page_url":       f"https://{lookbook_id}.pages.dev/",
        "looks": [
            {"id": "look1", "eyebrow": "Look 01", "title": "Test Look 1", "note": "First look."},
        ],
    }
    p = out_dir / "config.json"
    p.write_text(json.dumps(cfg))
    return p


def make_picks(out_dir: pathlib.Path, with_inline_image: bool = True) -> pathlib.Path:
    """Synthetic picks. Uses image_url (the format discover-weekly emits)."""
    picks = [{
        "look":        "look1",
        "picked_size": "L",
        "id":          10543,
        "slug":        "natural-draped-linen-deuce-coupe-camp-shirt",
        "name":        "Natural Draped Linen Deuce Coupe Camp Shirt",
        "color":       "Natural",
        "price":       "$168.00",
        "price_cents": 16800,
        "url":         "https://www.buckmason.com/products/natural-draped-linen-deuce-coupe-camp-shirt",
        "sku":         "BM-TEST-NATL",
        "image_url":   "https://pima.s3.amazonaws.com/uploads/product_image/file/36855/BM13211.679NAT_NATURAL_DRAPED_LINEN_DEUCE_COUPE_CAMP_SHIRT_NATURAL_27390_220260423-2-op7dv2.jpg" if with_inline_image else None,
        "in_stock_online": {"in_stock": True, "status": "in_stock", "label": "In stock"},
    }]
    if not with_inline_image:
        picks[0].pop("image_url")
    p = out_dir / "picks.json"
    p.write_text(json.dumps(picks))
    return p


def test_build_no_tryon_produces_index_html(tmp_path):
    """Editorial tier: --no-tryon, no AI images → index.html + og.jpg + thumbnail."""
    cfg = make_config(tmp_path, "test-build-1")
    picks = make_picks(tmp_path)
    out = tmp_path / "deploy"

    r = subprocess.run(
        ["python3", str(BUILD_SCRIPT),
         "--config", str(cfg),
         "--picks",  str(picks),
         "--out",    str(out),
         "--no-tryon"],
        capture_output=True, text=True, timeout=60,
    )
    assert r.returncode == 0, f"build failed: rc={r.returncode}\n{r.stdout}\n{r.stderr}"
    assert (out / "index.html").exists()
    assert (out / "index.html").stat().st_size > 4 * 1024


def test_build_stamps_lookbook_id_marker(tmp_path):
    """--out/.lookbook_id should hold the config's lookbook_id after build."""
    cfg = make_config(tmp_path, "test-build-marker")
    picks = make_picks(tmp_path)
    out = tmp_path / "deploy"

    r = subprocess.run(
        ["python3", str(BUILD_SCRIPT),
         "--config", str(cfg),
         "--picks",  str(picks),
         "--out",    str(out),
         "--no-tryon"],
        capture_output=True, text=True, timeout=60,
    )
    assert r.returncode == 0
    marker = out / ".lookbook_id"
    assert marker.exists()
    assert marker.read_text().strip() == "test-build-marker"


def test_build_html_contains_all_meta_tags(tmp_path):
    """OG + Twitter Card meta tags from references/output-formats.md."""
    cfg = make_config(tmp_path, "test-build-meta")
    picks = make_picks(tmp_path)
    out = tmp_path / "deploy"

    r = subprocess.run(
        ["python3", str(BUILD_SCRIPT),
         "--config", str(cfg),
         "--picks",  str(picks),
         "--out",    str(out),
         "--no-tryon"],
        capture_output=True, text=True, timeout=60,
    )
    assert r.returncode == 0
    html = (out / "index.html").read_text()
    expected_props = [
        "og:type", "og:title", "og:description", "og:url", "og:image",
        "og:image:width", "og:image:height",
        "twitter:card", "twitter:title", "twitter:description", "twitter:image",
    ]
    for p in expected_props:
        assert (f'property="{p}"' in html or f'name="{p}"' in html), \
            f"missing meta property: {p}"


def test_build_html_carries_piece_data_attrs(tmp_path):
    """Each .piece checkbox needs data-name / data-size / data-sku /
    data-qty / data-price-cents — that's the contract validate-lookbook
    enforces on L8 + the prose handoff composer reads."""
    cfg = make_config(tmp_path, "test-build-data-attrs")
    picks = make_picks(tmp_path)
    out = tmp_path / "deploy"

    r = subprocess.run(
        ["python3", str(BUILD_SCRIPT),
         "--config", str(cfg),
         "--picks",  str(picks),
         "--out",    str(out),
         "--no-tryon"],
        capture_output=True, text=True, timeout=60,
    )
    assert r.returncode == 0
    html = (out / "index.html").read_text()
    for attr in ("data-name", "data-size", "data-sku", "data-qty", "data-price-cents", "data-url"):
        assert re.search(rf'<input[^>]+{re.escape(attr)}=', html), f"missing {attr}"


def test_build_aborts_on_lookbook_id_marker_mismatch(tmp_path):
    """If --look-images directory has a .lookbook_id marker that doesn't
    match the config's lookbook_id, the build aborts (exit 5) per
    references/run-layout.md."""
    cfg = make_config(tmp_path, "this-run")
    picks = make_picks(tmp_path)
    out = tmp_path / "deploy"

    looks_dir = tmp_path / "stale-looks"
    looks_dir.mkdir()
    (looks_dir / ".lookbook_id").write_text("a-DIFFERENT-run")
    # Need a fake look1.png for the build to consume.
    (looks_dir / "look1.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)

    r = subprocess.run(
        ["python3", str(BUILD_SCRIPT),
         "--config", str(cfg),
         "--picks",  str(picks),
         "--out",    str(out),
         "--look-images", str(looks_dir)],
        capture_output=True, text=True, timeout=60,
    )
    assert r.returncode == 5, f"expected exit 5 for marker mismatch, got {r.returncode}\n{r.stderr}"
    assert "lookbook_id" in r.stderr


def test_build_help_works(tmp_path):
    """--help should succeed and print usage."""
    r = subprocess.run(
        ["python3", str(BUILD_SCRIPT), "--help"],
        capture_output=True, text=True, timeout=10,
    )
    assert r.returncode == 0
    assert "config" in r.stdout
    assert "picks" in r.stdout
