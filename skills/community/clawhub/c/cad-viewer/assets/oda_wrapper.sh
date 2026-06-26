#!/bin/bash
# Auto-start real ODA converter in virtual display
xvfb-run -a /usr/local/bin/ODAFileConverter "$@"
