# Project Memory — Learned Patterns

## Context Summary
- **Last session**: [Date] - Worked on [feature]
- **Current focus**: [Current task]
- **Active decisions**: [Key architectural choices]

## Learned Patterns

### File Organization
- `/src/components/` → React components with TypeScript
- `/src/utils/` → Helper functions, custom hooks
- `/src/types/` → TypeScript definitions
- `/tests/` mirrors `/src/` structure

### API Patterns
- Use `axios` for HTTP requests with interceptors
- API responses are typed with `interface`
- Error handling: try/catch with custom error classes
- Loading states managed with React Query

### State Management
- Global state: Zustand (lightweight)
- Form state: React Hook Form
- URL state: React Router params

### Performance Optimizations
- React.memo for expensive components
- useCallback for event handlers
- Virtualization for long lists
- Code splitting with React.lazy

## Recurring Decisions
- Prefer functional components over class components
- Use CSS modules over styled-components
- ESLint over TSLint
- Jest over Mocha

## Cross-Session Notes
- [Note about a particular pattern that worked well]
- [Decision to avoid a certain library]
- [Team preference for a specific approach]