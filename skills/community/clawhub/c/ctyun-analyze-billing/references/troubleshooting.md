# Troubleshooting Without Guessing

| Condition | Required response |
| --- | --- |
| CLI missing or version changed | Stop real queries; check `ctyun-cli version` and local help. |
| Credentials missing | Ask the user to configure locally; never receive keys. |
| Permission denied | Record that the resource check is unavailable; do not assume the resource is absent or spend is zero. |
| Action or flag rejected | Re-read local help; do not guess parameters. |
| Empty result | Report only the exact queried scope. |
| Pagination mismatch | Report collected scope only; continue only within the same scope. |
| Schema changes | Stop field derivation and state `Cannot determine`. |
| Resource not found | Preserve the bill fact; it may be historical. |
| Amounts differ | Report the summary, checked detail, difference, basis, and coverage separately. |

Do not widen scope or enable `--log` to troubleshoot.
