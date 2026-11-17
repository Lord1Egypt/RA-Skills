"""Fetch pinned public example data outside the distributable skill."""
import hashlib
import os
from pathlib import Path
import tempfile
import urllib.request

REVISION = "1ec8777d69525b6037fa2654d084cddcf61e3c62"
BASE_URL = f"https://raw.githubusercontent.com/tznurmin/fitctl/{REVISION}/"
SKILL_ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 1024 * 1024
# Cache-relative path -> (public repository path, SHA-256 of upstream bytes).
FILES = {
    'fixtures/host_state/linux-bare-metal-like-fresh-v1.json': ('fixtures/host_state/linux-bare-metal-like-fresh-v1.json', '3625a714ab5667ba601660ec0e3387d969a6dcc9e348eb232a60c2d22b89b730'),
    'fixtures/host_state/manifest.v1.json': ('fixtures/host_state/manifest.v1.json', 'e7769cbef189682b58393bb81aa27b50b1336a98f2da9033224ae6674c8d0f6a'),
    'fixtures/host_survey/linux-bare-metal-like-v1.json': ('fixtures/host_survey/linux-bare-metal-like-v1.json', '0b71b8611154797f20006fc8cdc483441f5b3653b9adea0e2b790c2a17a22cd2'),
    'fixtures/host_survey/linux-container-restricted-v1.json': ('fixtures/host_survey/linux-container-restricted-v1.json', 'ddbd68d9b2c242f6da9dfa8b536859974da469c80251e7f59206fa464e2e9556'),
    'fixtures/host_survey/linux-gpu-workstation-like-v1.json': ('fixtures/host_survey/linux-gpu-workstation-like-v1.json', '5d898755ff297428a44092e8548da14ce8f9e5e60b722806d704a5e2c21833f0'),
    'fixtures/host_survey/manifest.v1.json': ('fixtures/host_survey/manifest.v1.json', '021bce304382078a2be0c832af7dbe7339c072a2c3e34e571399104ceb771d93'),
    'policy/general_compute_default.v1.json': ('configs/policy/general_compute_default.v1.json', '4defdaf81b46541d4523f51a0b1e45c3e4648a7a1faa826717d926076efa2289'),
    'service_profiles/cpu_small_state_required.v2.json': ('configs/service_profiles/cpu_small_state_required.v2.json', '394c62bd09f7fff0c4fd9edbcb5a3b34199f0ab98113c9874c158556cb61f01d'),
    'service_profiles/general_compute_contract_only.v2.json': ('configs/service_profiles/general_compute_contract_only.v2.json', '92982419840ec2def4f7fec672f10a992e45711b29c425e2f8f52e707b9b41d7'),
    'service_profiles/gpu_preferred_with_general_compute_fallback_contract_only.v2.json': ('configs/service_profiles/gpu_preferred_with_general_compute_fallback_contract_only.v2.json', '9ed16f36f3e77fd8ad2cdb79fb4a5b2faadff28cd87c4e8eb56647010f678ad2'),
    'service_profiles/gpu_required_contract_only.v2.json': ('configs/service_profiles/gpu_required_contract_only.v2.json', 'cd0503a047a17d0ae52243a58aa84c579c5ced80396a513086e747ae00aa3d91'),
}


def _check_components(root, relative):
    """Every path component of relative (that exists) must be a non-symlink
    resolving inside root."""
    current = root
    for part in Path(relative).parts:
        current = current / part
        if current.is_symlink() or (current.exists() and
                                    not current.resolve().is_relative_to(root)):
            raise ValueError(f"cache component escapes the cache root: {current}")


def _contained_mkdirs(root, relative):
    """Create each path component below root, refusing symlinked components.

    root must already be resolved. Every existing component must resolve to
    itself under root; every new component is created without following
    links, so a symlinked cache subdirectory cannot redirect writes into
    the skill tree.
    """
    current = root
    for part in Path(relative).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"symlinked cache component refused: {current}")
        if not current.exists():
            current.mkdir()
        elif current.is_file() or not current.resolve().is_relative_to(root):
            raise ValueError(f"cache component escapes the cache root: {current}")
    return current


def public_inputs(cache_dir):
    """Return a verified input directory; download only missing, pinned files.

    Network, filesystem, and integrity failures are operational errors. Cached
    files are checked on every use. Containment: the cache root must be
    outside the skill, and every path component below it must be a non-symlink
    resolving inside the cache root, on reads and writes alike. This assumes
    the cache directory is operation-owned with no concurrent writer; a
    local attacker racing to swap a checked directory for a symlink is out
    of scope and would defeat any pathname-based check.
    """
    root = (Path(cache_dir).expanduser() / REVISION).resolve()
    if root.is_relative_to(SKILL_ROOT):
        raise ValueError("choose --cache-dir outside the installed skill")
    root.mkdir(parents=True, exist_ok=True)
    for relative, (upstream, expected) in FILES.items():
        destination = root / relative
        _check_components(root, relative)
        if destination.exists():
            with destination.open("rb") as stream:
                data = stream.read(MAX_BYTES + 1)
        else:
            request = urllib.request.Request(BASE_URL + upstream,
                                             headers={"User-Agent": "fitctl-skill/0.3.5"})
            with urllib.request.urlopen(request, timeout=20) as response:
                data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES or hashlib.sha256(data).hexdigest() != expected:
            raise ValueError(f"upstream input integrity mismatch: {destination}")
        if not destination.exists():
            parent = _contained_mkdirs(root, str(Path(relative).parent))
            temporary = None
            try:
                with tempfile.NamedTemporaryFile(dir=parent,
                                                 prefix=".fitctl-input-", delete=False) as stream:
                    temporary = Path(stream.name)
                    stream.write(data)
                if destination.is_symlink():
                    raise ValueError(f"symlinked cache file refused: {destination}")
                os.replace(temporary, destination)
            finally:
                if temporary is not None:
                    temporary.unlink(missing_ok=True)
    return root
