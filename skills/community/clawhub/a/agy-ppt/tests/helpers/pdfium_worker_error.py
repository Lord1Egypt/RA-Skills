"""Deterministic controlled-error harness for PDFium worker mapping."""

import sys

from pdf_ocr.pdfium_ipc import PROTOCOL_VERSION, read_frame, write_frame


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
write_frame(
    sys.stdout.buffer,
    {
        "protocol_version": PROTOCOL_VERSION,
        "status": "error",
        "payload_length": 0,
        "error_code": "OCR_PDF_INPUT_INVALID",
        "diagnostic": "controlled invalid PDF",
    },
)
