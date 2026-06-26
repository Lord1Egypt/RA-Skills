import base64
import hashlib
from pathlib import Path
import json


def test_skill_metadata_is_single_line_json():
    skill = Path(__file__).resolve().parents[1] / "SKILL.md"
    metadata_line = next(line for line in skill.read_text(encoding="utf-8").splitlines() if line.startswith("metadata:"))
    assert metadata_line.startswith("metadata: {")
    assert metadata_line.rstrip().endswith("}")


def test_skill_metadata_declares_sensitive_env_and_bins():
    skill = Path(__file__).resolve().parents[1] / "SKILL.md"
    metadata_line = next(line for line in skill.read_text(encoding="utf-8").splitlines() if line.startswith("metadata:"))
    payload = metadata_line.split("metadata:", 1)[1].strip()
    meta = json.loads(payload)
    requires = meta["openclaw"]["requires"]
    env = set(requires["env"])
    bins = set(requires["bins"])

    expected_env = {
        "ENTRA_TENANT_ID",
        "ENTRA_CLIENT_ID",
        "ENTRA_CLIENT_SECRET",
        "EXCHANGE_DEFAULT_MAILBOX",
        "EXCHANGE_ORGANIZATION",
        "ORGANIZATION_DOMAIN",
        "CLOUDFLARE_API_TOKEN",
        "CLOUDFLARE_ZONE_ID",
    }
    expected_bins = {"bash", "node", "python3", "jq"}

    assert expected_env.issubset(env)
    assert expected_bins.issubset(bins)


def test_skill_documents_verified_local_install():
    skill = (Path(__file__).resolve().parents[1] / "SKILL.md").read_text(encoding="utf-8")
    assert "pinned SHA-512 integrity value" in skill
    assert "does not fetch code from npm at runtime" in skill
    assert "reduced environment" in skill


def test_release_manifest_matches_vendored_tarball():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "vendor" / "caduceusmail-release.json").read_text(encoding="utf-8"))
    tarball = root / "vendor" / manifest["filename"]

    payload = tarball.read_bytes()
    sha1 = hashlib.sha1(payload).hexdigest()
    sha512 = base64.b64encode(hashlib.sha512(payload).digest()).decode("ascii")

    assert manifest["shasum"] == sha1
    assert manifest["integrity"] == f"sha512-{sha512}"


def test_skill_package_dependency_is_local_artifact():
    root = Path(__file__).resolve().parents[1]
    package_json = json.loads((root / "package.json").read_text(encoding="utf-8"))
    assert package_json["dependencies"]["caduceusmail"] == "file:vendor/caduceusmail-3.6.7.tgz"


def test_run_wrapper_enforces_sanitized_env_defaults():
    wrapper = (Path(__file__).resolve().parents[1] / "scripts" / "run.sh").read_text(encoding="utf-8")
    assert "exec env -i" in wrapper
    assert 'CADUCEUSMAIL_ALLOW_EXTERNAL_SCRIPT_RESOLUTION"]="${CADUCEUSMAIL_ALLOW_EXTERNAL_SCRIPT_RESOLUTION:-0}"' in wrapper
