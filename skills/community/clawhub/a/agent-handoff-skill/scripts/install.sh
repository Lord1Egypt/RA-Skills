#!/bin/sh
# Old repository install commands must not silently mutate global configuration.
set -eu
printf '%s\n' 'Repository protocol installation has been retired.' >&2
printf '%s\n' 'To clean up legacy entry blocks, use scripts/setup.py status or disable --agents <clients>.' >&2
printf '%s\n' 'For an old repository, use scripts/migrate.py status|migrate <repo>.' >&2
exit 2
