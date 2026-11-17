"""Controlled Phase 15.3 worker error harness."""

import sys

from image_ocr.ipc import PROTOCOL_VERSION, read_frame, write_frame


write_frame(sys.stdout.buffer, {"protocol_version": PROTOCOL_VERSION, "status": "ready", "payload_length": 0, "isolation": {"credentials": False, "network": False}})
read_frame(sys.stdin.buffer, max_payload=100 * 1024 * 1024)
write_frame(sys.stdout.buffer, {"protocol_version": PROTOCOL_VERSION, "status": "error", "payload_length": 0, "error_code": "OCR_IMAGE_INPUT_INVALID", "diagnostic": "controlled invalid image"})
