# -*- coding: utf-8 -*-
import sys
print("argv:", sys.argv)
if len(sys.argv) > 2:
    print("argv[2]:", repr(sys.argv[2]))
