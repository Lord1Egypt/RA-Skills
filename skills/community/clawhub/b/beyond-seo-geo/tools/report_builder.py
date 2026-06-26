#!/usr/bin/env python3
from pathlib import Path
import sys
title = sys.argv[1] if len(sys.argv) > 1 else "SEO Audit Report"
print(f"# {title}\n")
print("## Executive Summary\n")
print("[Add summary]\n")
print("## Findings\n")
print("| Issue | Evidence | Impact | Fix | Priority |\n|---|---|---|---|---|")
