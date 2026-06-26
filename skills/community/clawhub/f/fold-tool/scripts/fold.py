#!/usr/bin/env python3
import sys, textwrap
w = int(sys.argv[2]) if len(sys.argv)>2 else 80
print('\n'.join(textwrap.wrap(open(sys.argv[1]).read() if len(sys.argv)>1 else sys.stdin.read(), w)))
