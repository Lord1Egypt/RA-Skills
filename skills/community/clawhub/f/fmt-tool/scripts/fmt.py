#!/usr/bin/env python3
import textwrap, sys
width = int(sys.argv[2]) if len(sys.argv)>2 else 80
text = open(sys.argv[1]).read() if len(sys.argv)>1 else sys.stdin.read()
print(textwrap.fill(text, width))
