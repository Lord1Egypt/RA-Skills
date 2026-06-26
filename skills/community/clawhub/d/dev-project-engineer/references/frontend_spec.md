# Frontend Specification Template

This section of the Implementation Plan is written exclusively for the FE Developer. It must be self-contained — the FE dev should be able to complete all frontend work using only this section and the cross-cutting concerns section.

## ID Convention

All frontend items use the prefix `FE-` followed by a sequential number: FE-001, FE-002, etc.

---

## FE-S1: Page & Component Breakdown

List every page and its components. For each page:

```
Page: [Page Name]
Route: [/path/to/page]
SRS Requirement(s): [SRS-XXX, SRS-YYY]
Description: [what this page does from the user's perspective]

Components:
  - [ComponentName]
    Purpose: [what it renders/does]
    Props: [key props it receives]
    State: [local state it manages, if any]
    Children: [nested components, if any]
```

Group pages by feature area when there are many.

## FE-S2: Routes & Navigation

```
Route: [path]
Component: [PageComponent]
Auth Required: Yes | No
Roles Allowed: [list or "all authenticated"]
Redirects: [where to redirect if unauthorized]
Params: [URL params, if any]
Query Params: [supported query string params, if any]
```

Include the navigation structure: what links appear in nav bars, sidebars, or menus, and under what conditions (e.g., admin-only links).

## FE-S3: State Management

Define the state management approach and data shapes:

```
State Solution: [React Context, Redux, Zustand, Pinia, etc.]

Global State Shape:
  auth:
    user: { id, email, name, role }
    token: string | null
    isAuthenticated: boolean
  [feature]:
    items: [item type][]
    loading: boolean
    error: string | null
    selectedId: string | null
```

For each piece of global state, note: what sets it, what reads it, and when it resets.

## FE-S4: API Integration

For every backend endpoint the FE calls, specify:

```
FE-API-001: [descriptive name]
Maps to: [BE-XXX endpoint ID from backend spec]
Method: GET | POST | PUT | PATCH | DELETE
Path: /api/[path]
Auth: [token in header, cookie, none]
Request Body: [shape, or "none" for GET]
Response (success): [shape with types]
Response (error): [expected error format]
FE Handling:
  - Loading: [what the UI shows while waiting]
  - Success: [what happens on success — redirect, toast, update state]
  - Error: [what happens on error — message display, field highlighting]
```

Group API calls by feature area for clarity.

## FE-S5: UI Behavior Specifications

For each significant interaction, define the expected behavior:

### Form Behavior

```
Form: [form name]
Fields:
  - [field name]: [type] | Required: [yes/no] | Validation: [rules]
  - [field name]: [type] | Required: [yes/no] | Validation: [rules]
Submit Behavior:
  - Disable submit button while request is in flight
  - Show inline field errors on validation failure
  - Show success [toast/redirect/message] on success
  - Show error [toast/inline] on server error
  - [any field-specific behavior: auto-format phone numbers, debounce search, etc.]
```

### Component States

Every data-driven component must define these states:

```
Component: [name]
States:
  Loading: [what renders — skeleton, spinner, placeholder]
  Empty: [what renders when data set is empty — message, illustration, CTA]
  Error: [what renders on fetch failure — retry button, error message]
  Success: [normal render with data]
  Partial: [if applicable — what renders when some data loads and some fails]
```

### Modals & Confirmations

```
Modal: [name/purpose]
Trigger: [what opens it — button click, action]
Content: [what it displays]
Actions: [Confirm, Cancel — what each does]
Destructive: [yes/no — if yes, require explicit confirmation, e.g., type project name]
```

## FE-S6: Responsive & Accessibility Requirements

```
Breakpoints:
  - Mobile: < 768px
  - Tablet: 768px - 1024px
  - Desktop: > 1024px

Accessibility:
  - All interactive elements must be keyboard navigable
  - Form fields must have associated labels (not just placeholders)
  - Error messages must be announced to screen readers (aria-live)
  - Color contrast must meet WCAG 2.1 AA
  - Images must have alt text
  - Focus management on modal open/close and route changes
```

Adjust breakpoints and standards to match the project's requirements. These are defaults.

## FE-S7: Acceptance Criteria

For each page or major component, write acceptance criteria in Given-When-Then format:

```
FE-AC-001 (maps to FE-001, SRS-XXX):
  Given: [precondition]
  When: [user action]
  Then: [expected result]

FE-AC-002 (maps to FE-001, SRS-XXX):
  Given: [precondition]
  When: [user action]
  Then: [expected result]
```

Every SRS requirement that touches the frontend must have at least one acceptance criterion here. QA uses these directly.
