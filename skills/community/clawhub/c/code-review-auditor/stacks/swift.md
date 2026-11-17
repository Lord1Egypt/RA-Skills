# Swift Review Rules

Use for Swift, SwiftUI, UIKit, Vapor, async/await, Combine, packages, and Apple-platform projects.

## Bugs And Reliability

- Check force unwraps, implicitly unwrapped optionals, weak/unowned reference correctness, retain cycles, and lifecycle callbacks.
- Review actor isolation, `MainActor` boundaries, async cancellation, task ownership, and detached tasks.
- Verify error handling does not erase actionable failures.
- Check date, locale, currency, Codable defaults, and migration behavior.

## Security And Privacy

- Check Keychain vs UserDefaults storage, token lifecycle, ATS/network config, certificate pinning assumptions, and privacy-sensitive logging.
- Review file access, URL handling, deep links, pasteboard, screenshots, and background data exposure.
- For server-side Swift, apply web/API security rules from Node/TypeScript as relevant.

## Architecture

- Avoid views owning business rules, networking, persistence, or broad orchestration.
- Check MVVM/TCA/Clean-style boundaries only against the project's chosen architecture.
- Identify state explosion in views where a reducer/state machine would reduce bugs.

## Performance

- Review main-thread work, excessive view invalidation, image handling, large Codable payloads, and collection rendering.
- Check memory pressure, retain cycles, and unbounded tasks/subscriptions.

## Testing

- Prefer deterministic tests for reducers/view models/domain logic.
- Flag UI-only coverage when business behavior lacks direct tests.
