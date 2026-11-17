#!/bin/sh
# Validate one or more Candidate XML files against the unofficial schema.
#   sh tools/validate.sh examples/*.xml my-cv.xml
# Needs xmllint (libxml2), preinstalled on macOS and most Linux distributions.
set -e
dir=$(cd "$(dirname "$0")/.." && pwd)
status=0
for f in "$@"; do
  if xmllint --noout --schema "$dir/schema/europass-candidate.xsd" "$f" 2>&1; then :; else status=1; fi
done
exit $status
