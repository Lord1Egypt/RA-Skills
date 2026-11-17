# React quality patterns

## Style access

This skill does not enforce a specific style scheme and follows the current status of the warehouse by default.

Please note when adapting:

- Tailwind project continues to use Tailwind
- CSS Modules projects keep naming consistent with file organization
- The styled-components project continues to follow its pattern
- Theme, color, font size, spacing, etc. give priority to reusing warehouse token / CSS variables
- Avoid hardcoding a large number of visual constants within the component
- Disable inline styles (except dynamic values)
- Responsive processing must be consistent with the project breakpoint agreement

---

## Comment specifications

- **Prefer using Chinese**: When explaining "why this is done", business constraints, boundary conditions, and non-obvious trade-offs, give priority to writing comments in Chinese to make it easier for the team and business parties to read.
- **Exception when consistent with the code language**: When connecting third-party protocol field names, HTTP headers, and English terms in specifications, English proper nouns can be retained in the comments, and Chinese and English descriptions can be given when necessary.
- **Less but more precise**: Can express clear logic through clear naming and types without writing nonsense comments; complex branches, temporary compatibility, and performance trade-offs must be clearly stated.
- **Public API**: The external contract of modules or hooks can use JSDoc (`@param` / `@returns` / `@example`). The instructions can be in Chinese, unless the warehouse requires English.

---

## TypeScript Specification

Common TypeScript project rules are taken care of by `fec-typescript-project-standard`, including `tsconfig`, strictness, DTO / view model boundaries, `unknown` narrowing, public API types, declared artifacts, and type tests.

The React specification only supplements components, Props, events and TSX generic writing; complex type modeling or cross-framework type contracts are first offloaded to `fec-typescript-project-standard`.

### React project supplementary conventions

- Props interface naming: `ComponentNameProps`
- Event handling function: `handle` prefix (such as `handleClick`)
- Callback Props: `on` prefix (such as `onChange`, `onSubmit`)
- Components give priority to writing explicit props and return value types (`JSX.Element` / `React.ReactElement`) to avoid behavioral differences such as relying on the implicit `children` of `React.FC`
- Generic components use `<T>` constraints to maintain call-site type derivation; callback and event types preferentially use DOM/React’s own types (such as `React.ChangeEvent<HTMLInputElement>`)

```tsx
interface TableProps<T extends Record<string, unknown>> {
  data: T[];
  columns: ColumnDef<T>[];
  onRowClick?: (row: T) => void;
}
```

---

## Test specifications

### Content that should be covered first

- Core interaction behaviors (click, input, submit)
- Conditional rendering (loading/error/empty/data)
- Return values and side effects of key hooks
- API call mock and module-level integration testing

### Recommended style

- Test user behavior, not implementation details
- Prioritize using `screen.getByRole`, `getByLabelText`
- Avoid writing brittle tests around internal state
- Only measure key behaviors and do not mechanically pursue coverage figures

### Example

```tsx
describe("UserForm", () => {
  it("should submit with valid data", async () => {
    const onSubmit = vi.fn();
    render(<UserForm onSubmit={onSubmit} />);

    await userEvent.type(screen.getByLabelText("username"), "test");
    await userEvent.click(screen.getByRole("button", { name: "Submit" }));

    expect(onSubmit).toHaveBeenCalledWith({ username: "test" });
  });

  it("should show error on invalid input", async () => {
    render(<UserForm onSubmit={vi.fn()} />);
    await userEvent.click(screen.getByRole("button", { name: "Submit" }));
    expect(screen.getByText("Username cannot be empty")).toBeInTheDocument();
  });
});
```

---


## Common anti-patterns

Avoid:

- prop drilling is too deep without considering combination or partial encapsulation
- Excessive use of context for local issues
- Stuff data requests, view rendering, and imperative DOM operations into one file
- Do things in useEffect that can be done in event handlers
- Use `useEffect + setState` to simulate derived values that could be calculated directly
- Push all states to the global store
- Put business coupling components in `components/`
- Directly bypass the module export and import from the feature deep path
- There is no obvious benefit but complex optimization is done in advance
- **New class component** or handwritten class Error Boundary (should function component + `react-error-boundary`, etc.)

---

## Output checklist

When outputting React code or solutions, at least check:

- [ ] Whether to align the existing contracts of the warehouse first
- [ ] Page / feature / Is the boundary of common components clear?
- [ ] Whether the directory structure matches the module complexity
- [ ] Props type is complete and clear
- [ ] Whether explanatory comments should be given priority in Chinese and to the point
- [ ] Whether reusable logic has been extracted into hooks
- [ ] loading / error / empty / data status is complete
- [ ] Whether the API layer has type constraints and unified error handling
- [ ] Whether complex DTO, external data narrowing, public types or `tsconfig` issues have been offloaded to `fec-typescript-project-standard`
- [ ] Whether status management complies with the proximity principle
- [ ] Whether lazy loading is considered for routing-level or heavy-duty modules
- [ ] Whether the style scheme is consistent with the warehouse
- [ ] Whether key behaviors are covered by tests
- [ ] Key modules have been wrapped with **`react-error-boundary`** (etc.), and no hand-written class component Boundary
- [ ] Whether the long list evaluates virtualization; whether the pop-up window/composite component has keyboard and focus conventions
- [ ] Whether unnecessary new dependencies or new paradigms are introduced

---
