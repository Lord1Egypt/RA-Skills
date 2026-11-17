---
name: fec-component-testing
description: Use when authoring or reviewing frontend unit, component, or light integration tests close to UI code, including React Testing Library, Vue Test Utils, hooks/composables, props/emits, callbacks, accessible queries, user-event interactions, mocks, loading/error/empty states, and regression coverage. For layer planning, real-browser journeys, or existing validation failures, choose the matching testing or validation workflow first; Chinese triggers include component testing, Component unit testing, unit testing, lightweight integration testing.
---

#Component testing

## Purpose

Use tests close to the code and user behavior to verify pure logic, component contracts, and lightweight module collaboration to reduce refactoring and UI interaction regression.

## Procedure

### 1. First determine the test level

- Unit testing: pure functions, hooks/composables, utils, state logic, schema.
- Component testing: props/emis, callbacks, user interaction, loading/error/empty, mock boundaries.
- Lightweight integration testing: form + API mock + Router/Store/Provider context.

The cross-page real browser process is offloaded to the E2E workflow; if the test layer selection is unclear, do the test layering planning first.

### 2. Prioritize testing based on user-perceivable behavior

Each test keeps Arrange / Act / Assert clearly segmented: preparing data and rendering, performing user actions, asserting user-visible results or exposing contracts.

```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { SearchBox } from "./SearchBox";

test("submits the entered keyword", async () => {
  const user = userEvent.setup();
  const onSearch = vi.fn();

  render(<SearchBox onSearch={onSearch} />);

  await user.type(screen.getByRole("searchbox", { name: /keyword/i }), "orders");
  await user.click(screen.getByRole("button", { name: /search/i }));

  expect(onSearch).toHaveBeenCalledWith("orders");
});
```

### 3. Vue components use accessible queries or explicit text assertions

```ts
import { mount } from "@vue/test-utils";
import UserMenu from "./UserMenu.vue";

test("emits logout when the logout item is clicked", async () => {
  const wrapper = mount(UserMenu, {
    props: { userName: "Ada" },
  });

  await wrapper.get('[data-testid="logout-button"]').trigger("click");

  expect(wrapper.emitted("logout")).toHaveLength(1);
});
```

Prefer roles, labels, and visible text; only use `data-testid` when there is no stable semantics.

### 4. Control mock boundaries

```ts
vi.mock("../api/users", () => ({
  fetchUsers: vi.fn(async () => [{ id: "1", name: "Ada" }]),
}));
```

- Mock network, time, routing and browser APIs.
- Do not mock the internal functions of the component under test.
- Only make light mocks of the basic components of the design system to retain accessible behaviors.
- Mock data should express the business scenario and not use arbitrary strings that only the test author can understand.
- Shared fixtures should remain readable, and complex objects should use builders to fill in default values; each test only covers the fields relevant to the scenario.
- When mocking the network, give priority to simulating user-visible results and error shapes, and do not copy back-end implementation details.

### 5. Override key status

Each complex component covers at least:

- Default rendering.
- User interaction and callbacks.
- loading / empty / error。
- Permission or disabled status.
- Keyboard interaction and focus behavior (when applicable).

### 6. Keep tests maintainable

```ts
function setup() {
  const user = userEvent.setup();
  const onSubmit = vi.fn();
  render(<ProfileForm onSubmit={onSubmit} />);
  return { user, onSubmit };
}
```

Put the repetitive rendering logic into `setup`, but don't hide the core actions and assertions of the test.

### 7. Regression testing proves the problem first

- Bug fixes should be written first to create the smallest test that can reproduce the failure.
- Reasons for failure should point to user behavior or public contracts, not import errors, test environments, or wait methods.
- Keep regression testing after fixing to avoid leaving verification only in manual steps.

## Constraints

- Avoid testing implementation details such as internal state names, private function calls, DOM hierarchy snapshots.
- Do not use snapshot as the main assertion for interactive components; it can only assist in checking stable static output.
- Use `findBy*` or `waitFor` for asynchronous assertions, do not use fixed delays.
- Test names should describe user scenarios, not function names.
- Component testing is not a replacement for E2E; routing, real-browser compatibility, and cross-page flows still require E2E.
- Do not copy component implementation logic in tests; otherwise the test will pass with the wrong implementation.
- No mutable fixtures, global store or fake timer state shared between tests; each use case has independent setup and cleanup.

## Expected Output

Produce test files in the same directory as the component or in the directory agreed upon by the project, covering core interactions, status and regression scenarios. During verification, run the existing test command of the project to confirm that the failure information can be located to user behavior or component contract.
