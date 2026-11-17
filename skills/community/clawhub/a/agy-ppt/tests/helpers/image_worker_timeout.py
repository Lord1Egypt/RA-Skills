"""Phase 15.3 watchdog timeout harness."""

import sys
import time

from image_ocr.ipc import PROTOCOL_VERSION, write_frame


write_frame(sys.stdout.buffer, {"protocol_version": PROTOCOL_VERSION, "status": "ready", "payload_length": 0, "isolation": {"credentials": False, "network": False}})
time.sleep(10)
