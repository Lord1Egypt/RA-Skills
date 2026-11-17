"""Deterministic oversized-payload harness for bounded PDFium IPC."""

import sys

from pdf_ocr.pdfium_ipc import PROTOCOL_VERSION, canonical_header, read_frame, write_frame


write_frame(
    sys.stdout.buffer,
    {
        "protocol_version": PROTOCOL_VERSION,
        "status": "ready",
        "payload_length": 0,
        "isolation": {"credentials": False, "network": False},
    },
)
read_frame(sys.stdin.buffer, max_payload=100 * 1024 * 1024)
sys.stdout.buffer.write(
    canonical_header(
        {
            "protocol_version": PROTOCOL_VERSION,
            "status": "ok",
            "payload_length": 101,
        }
    )
)
sys.stdout.buffer.flush()
