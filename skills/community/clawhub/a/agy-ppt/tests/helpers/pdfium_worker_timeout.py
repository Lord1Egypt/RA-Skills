"""Deterministic timeout harness for the parent PDFium worker watchdog."""

import sys
import time

from pdf_ocr.pdfium_ipc import PROTOCOL_VERSION, write_frame


write_frame(
    sys.stdout.buffer,
    {
        "protocol_version": PROTOCOL_VERSION,
        "status": "ready",
        "payload_length": 0,
        "isolation": {"credentials": False, "network": False},
    },
)
time.sleep(10)
