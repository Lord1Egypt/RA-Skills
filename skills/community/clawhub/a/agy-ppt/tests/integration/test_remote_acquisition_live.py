#!/usr/bin/env python3
"""Bounded live public-source acquisition check (Phase 13.5). Opt-in.

Unlike the deterministic suite, this test does reach the public internet. It is
therefore **opt-in** and is skipped unless explicitly enabled:

    AGY_PPT_LIVE_REMOTE=1 python3 skills/agy-ppt/tests/integration/test_remote_acquisition_live.py

Scope is deliberately one source, one acquisition, one ingestion:

* one ``GET`` for RFC 2119, a small, stable, public, non-confidential document
* the acquired bytes must match a pinned SHA-256
* the payload must pass the existing plain-text ingestion
* no additional network resource is fetched
* the downloaded payload lives in a temporary directory and is deleted

It consumes no AI subscription quota, calls no Codex or Kiro, uses no API
fallback, and performs no crawling or polling. A network outage is an
environment condition, not a production bug: the test reports the failure
plainly rather than pretending to pass.
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import source_acquisition as sa  # noqa: E402
import source_ingestion as si  # noqa: E402

LIVE_ENV_FLAG = "AGY_PPT_LIVE_REMOTE"

SKIP_REASON = (
    f"live remote acquisition is opt-in; set {LIVE_ENV_FLAG}=1 to run it. "
    "It performs exactly one public HTTP GET and consumes no AI quota."
)

#: A small, stable, public, non-confidential document.
RFC_2119_URL = "https://www.rfc-editor.org/rfc/rfc2119.txt"

#: Pinned fingerprint for the document above.
RFC_2119_SHA256 = "3c2ceb7bfc84cd34720f4a5271338ab9d8280d34bdd1eb250c64306202f2ed8b"


def live_enabled() -> bool:
    return os.environ.get(LIVE_ENV_FLAG) == "1"


@unittest.skipUnless(live_enabled(), SKIP_REASON)
class TestLiveRemoteAcquisition(unittest.TestCase):
    def test_public_rfc_acquisition_and_ingestion(self) -> None:
        with tempfile.TemporaryDirectory() as workspace:
            try:
                acquisition, extraction = sa.acquire_and_ingest(
                    RFC_2119_URL, "src_rfc2119", workspace
                )
            except sa.SourceAcquisitionError as exc:
                self.fail(
                    "LIVE_REMOTE_VALIDATION_BLOCKED: "
                    f"{exc.error_code}: {exc} -- this indicates an external "
                    "network or upstream availability problem, not a production bug"
                )

            self.assertEqual(
                acquisition.source_digest,
                RFC_2119_SHA256,
                "acquired bytes do not match the pinned RFC 2119 fingerprint",
            )
            self.assertEqual(acquisition.redirect_count, 0)
            self.assertGreater(acquisition.downloaded_bytes, 0)
            self.assertEqual(
                acquisition.downloaded_bytes,
                Path(acquisition.local_payload_path).stat().st_size,
            )

            # The payload flows through the existing deterministic ingestion.
            self.assertEqual(extraction.source_format, si.FORMAT_TEXT)
            self.assertGreater(extraction.block_count, 0)
            self.assertEqual(extraction.source_digest, acquisition.source_digest)
            body = "\n".join(block.text for block in extraction.blocks)
            self.assertIn("Key words for use in RFCs", body)

            # Exactly one payload file; nothing else was fetched or written.
            written = sorted(p.name for p in Path(workspace).iterdir())
            self.assertEqual(written, ["src_rfc2119.txt"])

        # The temporary workspace, and therefore the payload, is gone.
        self.assertFalse(Path(workspace).exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
