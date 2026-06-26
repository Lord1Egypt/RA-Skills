# FILE_META
# INPUT:  HarnessFile list (src path / arc name / scrub flag) from each adapter
# OUTPUT: HarnessBundle (zip bytes + scrub report) + upload helpers
# POS:    skill lib — generic packaging + upload framework shared by all adapters
# MISSION: Centralize zip/scrub/upload for harness submissions so adapters only supply the file manifest.

"""Harness packaging and upload framework.

See ``docs/adapter-design.md`` §6 (Harness mechanism) for scope semantics
and §4.3 for the ``build_harness`` contract each adapter fulfills.
"""

from .packager import HarnessFile, HarnessBundle, build_bundle
from .uploader import upload_harness

__all__ = ["HarnessFile", "HarnessBundle", "build_bundle", "upload_harness"]
