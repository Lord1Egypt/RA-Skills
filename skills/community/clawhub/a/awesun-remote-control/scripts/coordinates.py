#!/usr/bin/env python3
# Copyright (c) 2026 Oray Inc. All rights reserved.
#
# No Part of this file may be reproduced, stored
# in a retrieval system, or transmitted, in any form, or by any means,
# electronic, mechanical, photocopying, recording, or otherwise,
# without the prior consent of Oray Inc.
#
# @Author: wuwenze <wuwenze@oray.com>
# @Date: 2026-07-08 12:56:00
# @FileName: coordinates.py

"""
UI element coordinate utility. Computes normalized coordinates ONLY.
"""

import sys
from typing import Tuple


def calculate_coordinates(
    pixel_x: int, pixel_y: int, image_width: int, image_height: int
) -> Tuple[float, float]:
    """
    Compute normalized coordinates

    Formula:
    x = pixel_x / image_width
    y = pixel_y / image_height

    Args:
        pixel_x: pixel X coordinate
        pixel_y: pixel Y coordinate
        image_width: image width
        image_height: image height

    Returns:
        (x, y) normalized coordinate tuple, range [0.0, 1.0]
    """
    x = pixel_x / image_width
    y = pixel_y / image_height
    return (round(x, 6), round(y, 6))


def validate_coordinates(x: float, y: float) -> bool:
    """
    Validate normalized coordinates are in valid range

    Args:
        x: X normalized coordinate
        y: Y normalized coordinate

    Returns:
        True if coordinates are in range [0.0, 1.0]
    """
    return 0.0 <= x <= 1.0 and 0.0 <= y <= 1.0


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 coordinates.py norm <pixel_x> <pixel_y> <width> <height>")
        print("  python3 coordinates.py validate <x> <y>")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "norm":
        x, y = calculate_coordinates(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
        print(f"Normalized coordinates: ({x}, {y})")

    elif cmd == "validate":
        x, y = float(sys.argv[2]), float(sys.argv[3])
        valid = validate_coordinates(x, y)
        print(f"Coordinates ({x}, {y}) valid: {'YES' if valid else 'NO'}")
        sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
