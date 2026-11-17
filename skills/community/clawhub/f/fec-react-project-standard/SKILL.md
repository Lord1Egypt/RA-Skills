---
name: fec-react-project-standard
description: Use when designing or reviewing React + TypeScript project structure, feature/module boundaries, component architecture, hooks organization, routing composition, state/API/error/styling defaults, or repository-wide React conventions. Prefer narrower skills for forms, data fetching, tests, accessibility, virtualization, animation, or security deep dives; Chinese triggers include React project specification, React component architecture.
---

# React project specifications

Suitable for medium and large module construction, page reconstruction and engineering structure design in React + TypeScript warehouse.

## Purpose

Provide engineering structure, module boundaries and default implementation conventions for React + TypeScript projects to ensure clear architecture and maintainable code.

## Procedure

This skill mainly solves the problem of "how to design and implement" React engineering tasks, without repeating the basic coding bottom line. When handling React engineering tasks, perform them in the following order:

1. Identify the warehouse and have an agreement
   - Directory organization
   - Style system
   - Status management solution
   - Request packaging method
   - Testing framework
   - UI component library/design system

2. Determine which layer the target belongs to
   - Routing page
   -Page private components
   - feature business module
   - Global common components
   - hooks / services / stores / utils

3. Design the boundaries before writing the code
   - What logic belongs to page layout
   - Which logic belongs to feature
   - Which logic should be transferred to general capabilities?
   - Which state should be managed locally and which should be handed over to store/query/URL
   - When the status ownership is complex, use the status management process to make a status list first
   - When the boundaries of DTO, public props, generic components or `tsconfig` are complex, first use the TypeScript project specification process to converge cross-framework type contracts

4. Complete key quality items when outputting
   - loading / error / empty / data status
   - Error handling and retrying
   - Type constraints
   - Key test entrance
   - Diversion of necessary special skills
   - Check whether the dependency already exists in `package.json`. If it is missing, give the installation command first and then use it.
   - Whether heavy UI capabilities (animation, charts, 3D, editors, maps) are isolated as leaf components and loaded on demand
   - Whether images, videos, fonts and other resources are localized and cacheable, and avoid placeholder URLs from entering delivery
   - Whether page-level Error Boundary, module-level fallback, API error mapping and user-recoverable actions are consistent
   - Whether Tailwind token/variant or responsive layout requirements should be diverted to the corresponding special skill
- Perform lightweight screening for obvious architectural performance risks, such as heavy dependency boundaries, too wide Context, high-frequency derived values and lazy loading fallback; enter the performance optimization workflow when indicator evidence is needed

## Detailed reference

Load more detailed reference files as needed:

- Project Directory, Component Hierarchy, Component Boundary and Component Directory Recommendations: Load [references/react-project-structure.md](references/react-project-structure.md).
- Component pattern, Hooks, routing, state ownership, API layer, error handling and Suspense/lazy loading: Load [references/react-runtime-patterns.md](references/react-runtime-patterns.md).
- Style, annotations, TypeScript, tests, anti-patterns and output checklist: Loading [references/react-quality-patterns.md](references/react-quality-patterns.md).
- Lightweight performance conventions at the React project specification level: Load [references/react-performance-patterns.md](references/react-performance-patterns.md).

## Constraints

- Comply with the existing global rules and React rules of the warehouse by default
- If the warehouse already has a clear directory structure, style system, status management or request encapsulation, the warehouse convention will be used first.
- The size of the component file should be approximately **300 lines**; if it exceeds **500 lines** or is too complex, it must be split into sub-components, Hooks, utils, and types.
- It is forbidden to add new class components (Error Boundary uses libraries such as `react-error-boundary`)
- Disable bypassing module exports and importing from feature deep paths
- Do not use `useEffect + setState` to simulate derived values that can be calculated directly
- Avoid prop drilling too deep without considering composition or partial encapsulation
- Do not synchronously introduce GSAP, Three.js, Lottie, rich text editor or map SDK into common page components; use dynamic import, route-level subcontracting or leaf component isolation when necessary.
- No bare `fetch`, API URL, token refresh or upload processes scattered around React components; cross-border requests should be converged to the API integration layer.
- Do not use Error Boundary to handle normal API failures; request errors should first fall into the loading/error/empty/data state and recoverable operations.
- Do not write React performance recommendations as global memo without evidence; first locate request waterfall, bundle boundaries, repeated rendering or effect misuse.

## Expected Output

- Component boundaries are clear, pages/features/components are clearly layered
- The Props type is complete and clear; the narrowing of complex public types or external data has been diverted to the TypeScript project specification process
- Reusable logic has been extracted into hooks, and the loading/error/empty/data status is complete
- The API layer has type constraints and unified error handling, and status management conforms to the proximity principle
- URL status, server status, form status and global client status have clear boundaries
- Key behaviors are covered by tests, and key modules have been wrapped with `react-error-boundary`
- The long list has been evaluated for virtualization, and pop-up/composite components have keyboard and focus support
- Respect the current situation of the warehouse first, and then recommend the structure
- Give necessary suggestions for file division
- Explain why this is layered if necessary
- For new modules, give priority to outputting the smallest floor-mountable structure rather than over-designing it all at once
- For reconstruction tasks, give priority to ensuring portability and risk controllability
- For performance-related React changes, describe the triggered risk categories, evidence sources, and verification commands
