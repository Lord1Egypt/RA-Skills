# React Review Rules

Use for React, Next.js, Remix, Vite, React Native-adjacent patterns, component libraries, hooks, and client-side TypeScript.

## Bugs And Reliability

- Check hook dependency arrays, stale closures, race conditions in effects, cleanup behavior, and state derived inconsistently from props.
- Look for invalid controlled/uncontrolled transitions, unstable keys, hydration mismatches, and client/server boundary mistakes.
- Verify error boundaries, loading states, empty states, and optimistic update rollback.

## Security

- Check `dangerouslySetInnerHTML`, URL construction, open redirects, token storage, client-exposed secrets, and authorization assumptions in UI.
- Verify server actions/API routes enforce authorization independently from components.
- Review dependency risk for rich text, markdown, uploads, previews, and third-party scripts.

## Architecture

- Keep components focused: rendering, local interaction, and composition.
- Move business rules and data transformations to hooks/services/domain helpers when repetition or testability warrants it.
- Avoid global state for local state and avoid prop drilling that hides ownership boundaries.
- Recommend component patterns only when they reduce duplication or clarify data flow.

## Performance

- Check unnecessary re-renders, expensive calculations in render, large lists without virtualization, unstable callback/object props, and oversized bundles.
- Review server/client split, caching, suspense boundaries, prefetching, and image handling.

## Testing

- Prefer behavior-oriented tests with realistic user interaction.
- Flag snapshots that do not protect behavior, over-mocked data hooks, and missing accessibility assertions for critical UI.
