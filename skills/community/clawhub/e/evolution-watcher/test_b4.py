#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from scripts.adapter_auto_fix import test_end_to_end

if __name__ == "__main__":
    result = test_end_to_end()
    sys.exit(0 if result else 1)