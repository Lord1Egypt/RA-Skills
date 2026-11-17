"""Self-bootstrap the scripts' Python dependencies with ``uv``.

Why this exists
---------------
The skill declares its deps in ``SKILL.md`` frontmatter
(``metadata.openclaw.install.uv``) for hosts that honor it. Not every host
does — and a user may run a script directly — so the agent kept hitting
``ModuleNotFoundError: rembg`` and having to ``pip install`` by hand. These
helpers make the scripts self-contained instead: on a missing import we build a
cached virtualenv in the skill data dir with ``uv`` and re-exec into it. Steady
state is a couple of ``find_spec`` probes (near-zero) — only the *first* run in
a fresh container pays the install cost, and it lands in the persistent data dir.

Two dependency tiers
---------------------
* ``IMAGING`` — Pillow + numpy. Tiny, fast, no model download. Everything the
  compositing / color-key / DTF-sizing scripts need.
* ``REMBG`` — adds ``rembg`` + ``onnxruntime`` (~170 MB wheels **plus** a one-time
  ~170 MB U²-Net model download). Only the two scripts that actually run
  segmentation (garment-bbox detection, photographic background removal) ask for
  it, so the common flat-art path never pays that cost.

Usage (top of a script, right after adding ``scripts/`` to ``sys.path``)::

    import _bootstrap
    _bootstrap.ensure(_bootstrap.IMAGING, _bootstrap.IMAGING_MODS)
    from PIL import Image  # now guaranteed importable
"""

from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _paths  # noqa: E402

# One Pillow pin for the whole venv so the tiers never disagree.
IMAGING = ["Pillow>=10.3,<12", "numpy>=1.24,<3"]
REMBG = IMAGING + ["rembg>=2.0.56,<3", "onnxruntime>=1.18,<2"]
# CLEANUP — flat-art restoration (cleanup_art.py): connected-component despeckle
# and morphology (scipy) + corner-preserving vector trace / AA fill (opencv).
# Headless OpenCV so there's no GUI/X11 baggage. No model download (unlike REMBG).
CLEANUP = IMAGING + ["scipy>=1.10,<2", "opencv-python-headless>=4.8,<6"]

IMAGING_MODS = ["PIL", "numpy"]
REMBG_MODS = IMAGING_MODS + ["rembg", "onnxruntime"]
CLEANUP_MODS = IMAGING_MODS + ["scipy", "cv2"]

_VENV = _paths.data_dir() / ".venv"


def _venv_python() -> Path:
    if os.name == "nt":
        return _VENV / "Scripts" / "python.exe"
    return _VENV / "bin" / "python"


def _in_our_venv() -> bool:
    try:
        return Path(sys.prefix).resolve() == _VENV.resolve()
    except OSError:
        return False


def _missing(modules: list[str]) -> list[str]:
    out = []
    for m in modules:
        try:
            if importlib.util.find_spec(m) is None:
                out.append(m)
        except ModuleNotFoundError:
            out.append(m)
    return out


def ensure(requirements: list[str], modules: list[str]) -> None:
    """Guarantee ``modules`` import; install ``requirements`` via ``uv`` if not.

    No-op when the host already provides the modules (zero overhead in that
    common case). Otherwise create/reuse a cached venv in the data dir, install
    into it, and re-exec the current command inside it so the imports resolve.
    """
    missing = _missing(modules)
    if not missing:
        return

    # We already re-exec'd into our managed venv and the deps *still* aren't
    # importable — installation genuinely failed; don't loop forever.
    if _in_our_venv():
        raise SystemExit(
            "ERROR: dependencies still missing after bootstrap ("
            + ", ".join(missing)
            + "). Install manually with:  uv pip install "
            + " ".join(requirements)
        )

    uv = shutil.which("uv")
    if not uv:
        raise SystemExit(
            "ERROR: this script needs Python packages ["
            + ", ".join(missing)
            + "] and neither they nor `uv` are available. Install uv "
            "(https://docs.astral.sh/uv/) or run:  pip install "
            + " ".join(requirements)
        )

    py = _venv_python()
    # uv chatter goes to stderr so a script's JSON stdout stays clean.
    if not py.exists():
        _VENV.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([uv, "venv", str(_VENV)], check=True, stdout=sys.stderr)
    subprocess.run(
        [uv, "pip", "install", "--python", str(py), *requirements],
        check=True,
        stdout=sys.stderr,
    )

    # Re-run the exact same command, now under the venv interpreter. On that
    # second entry `ensure()` finds the modules present and returns immediately.
    os.execv(str(py), [str(py), *sys.argv])
