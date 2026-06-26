#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------
# sanitize_snapshot.sh – Deprecated as of v1.1.7
#
# The snapshot functionality (agent_config_files table) has been removed
# to prevent storage of sensitive operational files (MEMORY.md, AGENTS.md,
# BOOT.md, SECURITY.md).
#
# This script is retained for backward compatibility but no longer
# performs any sanitization. It exits successfully as a no-op.
#
# If secret redaction is needed in the future, implement it as a
# standalone utility rather than tied to database snapshot storage.
# ------------------------------------------------------------------

echo "NOTE: Snapshot functionality removed in v1.1.7. No action taken." >&2
exit 0
