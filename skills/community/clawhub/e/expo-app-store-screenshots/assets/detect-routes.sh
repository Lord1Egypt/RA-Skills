#!/usr/bin/env bash
# Enumerate Expo Router routes from a project's app/ directory.
#
# Expo Router uses file-based routing under app/ — every .tsx/.ts/.jsx/.js
# file (that doesn't start with _ or +) becomes a route. This script walks
# that tree and prints each discovered route in a stable, grep-able format so
# the agent can decide which screens to capture and how to categorize them
# (auth vs unauth) downstream.
#
# Usage:
#   bash detect-routes.sh <project-root>
#
# Output (one line per route, tab-separated):
#   <url-path>\t<group>\t<source-file>
#
# Where:
#   url-path     — the route URL Expo Router exposes
#                  (e.g. "/", "/sign-in", "/profile/[id]")
#   group        — the closest enclosing route group "(name)", or "(root)" if
#                  the route lives at the top level. Useful as an auth-state
#                  hint: by convention, groups like (auth), (authenticated),
#                  (app) usually gate auth-required routes, while (public),
#                  (unauth), (onboarding) tend to mark sign-in/sign-up.
#                  (Verify per project — naming isn't standardized.)
#   source-file  — repo-relative path of the route file, for jump-to-source.
#
# Skipped (intentional):
#   - _layout.tsx, _error.tsx, _* (layout shells, not routes)
#   - +api.ts, +not-found.tsx, +* (special files: API routes, error boundaries)
#   - Any file under api/ subdirectories ending in +api.ts (server routes)
#
# Notes:
#   - Supports both app/ (default) and src/app/ layouts.
#   - The script does NOT classify auth state itself. The (group) hint is just
#     output verbatim; the agent reading the output interprets it using project
#     conventions (or asks the user).
#
# Example downstream:
#   bash detect-routes.sh ~/myapp | sort
#   /                       (root)        app/index.tsx
#   /(auth)/sign-in         (auth)        app/(auth)/sign-in.tsx
#   /(auth)/sign-up         (auth)        app/(auth)/sign-up.tsx
#   /home                   (app)         app/(app)/home.tsx
#   /profile/[id]           (app)         app/(app)/profile/[id].tsx
#   /settings               (app)         app/(app)/settings.tsx

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <project-root>" >&2
  exit 1
fi

project_root="$1"
if [[ ! -d "$project_root" ]]; then
  echo "✗ not a directory: $project_root" >&2
  exit 1
fi

# Resolve the app/ directory — try the two conventional locations.
if   [[ -d "$project_root/app"     ]]; then app_dir="$project_root/app"
elif [[ -d "$project_root/src/app" ]]; then app_dir="$project_root/src/app"
else
  echo "✗ no app/ or src/app/ directory under $project_root" >&2
  echo "  (this script targets Expo Router projects; for legacy React Native, route enumeration is project-specific)" >&2
  exit 2
fi

# Find route files. Skip:
#   - _layout, _error, anything starting with _ (layout shells)
#   - +api.ts, +not-found.tsx, anything starting with + (special files)
#   - .d.ts type files
# Sort for stable output across runs.
find "$app_dir" -type f \
    \( -name "*.tsx" -o -name "*.ts" -o -name "*.jsx" -o -name "*.js" \) \
    -not -name "_*" \
    -not -name "+*" \
    -not -name "*.d.ts" \
    -not -name "*.test.*" \
    -not -name "*.spec.*" \
  | sort \
  | while IFS= read -r file; do
    # Path relative to app/
    rel="${file#$app_dir/}"

    # Strip the file extension
    noext="${rel%.tsx}"
    noext="${noext%.ts}"
    noext="${noext%.jsx}"
    noext="${noext%.js}"

    # Closest enclosing route group: pick the LAST (group)/ on the path.
    group="(root)"
    if [[ "$rel" == *"("*")"* ]]; then
      # Extract all (group) segments, take the last (innermost).
      group=$(printf '%s\n' "$rel" \
        | grep -oE '\([^/)]+\)' \
        | tail -1 || true)
      group="${group:-(root)}"
    fi

    # Build the URL the way Expo Router exposes it: leave (group) segments in
    # place (they're part of the URL hierarchy in the router's source tree,
    # though most callers won't include them in deep links — `/sign-in` works
    # even if the file lives in `(auth)/sign-in.tsx`). Showing them here keeps
    # the URL ⇆ file mapping unambiguous.
    url="/$noext"

    # Normalize trailing `/index` → `/`
    if   [[ "$url" == "/index" ]]; then url="/"
    elif [[ "$url" == */index ]];  then url="${url%/index}/"
    fi

    # Project-relative file path for traceability.
    file_rel="${file#$project_root/}"

    printf "%s\t%s\t%s\n" "$url" "$group" "$file_rel"
done
