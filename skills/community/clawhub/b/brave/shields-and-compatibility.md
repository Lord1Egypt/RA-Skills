# Shields and Compatibility

## Symptom to First Check

| Symptom | First check |
|---------|-------------|
| Login loop | Cookies, cross-site sign-in flow, and aggressive blocking |
| Video or audio missing | Media permissions and blocked scripts |
| Checkout or payment page fails | Blocked third-party scripts, popups, or embedded frames |
| Page never finishes loading | Script blocking, extension conflict, or bad cached state |
| Site works in Chrome but not Brave | Per-site Shields, extension set, and profile difference |

## Recovery Order

Use the smallest reversible change first:
1. Confirm the issue in the intended Brave profile
2. Retry in a clean private or disposable session
3. Test per-site Shields adjustments
4. Test with suspicious extensions disabled
5. Compare against a fresh Brave profile
6. Only then consider broader cleanup

## Per-Site Before Global

Prefer per-site Shields changes when one site breaks:
- preserves defaults elsewhere
- makes the fix easier to reverse
- keeps the root cause narrow

Global relaxations are a last resort and should be explicit.

## Compatibility Notes Worth Saving

Write to `sites.md` only when the pattern is durable:
- one site always needs a specific per-site adjustment
- a known extension always breaks a workflow
- a profile or flag consistently changes the result

Do not save one-off failures caused by temporary outages.
