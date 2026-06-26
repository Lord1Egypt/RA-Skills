#!/usr/bin/env python3
"""Token-free selfcheck for fsids normalization path."""

from netdisk import _normalize_fsids


if __name__ == "__main__":
    normalized = _normalize_fsids([1, 2])
    assert normalized == [1, 2], normalized
    print("selfcheck ok: _normalize_fsids([1, 2]) ->", normalized)
