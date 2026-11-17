#TypeScript type safety

## Purpose

Establish evolvable type contracts for front-end and TypeScript projects, reducing `any`, assertions, and runtime shape drift.

## Procedure

### 1. First determine the type boundary

Divide types into external input, domain model, UI view model, component props, and tool function API. Don't let backend DTOs, form models, and UI presentation models pretend to be each other.

```ts
interface UserDto {
  id: string;
  display_name: string;
  status: "ACTIVE" | "DISABLED";
}

interface UserViewModel {
  id: string;
  displayName: string;
  status: "active" | "disabled";
}

export function mapUserDto(dto: UserDto): UserViewModel {
  return {
    id: dto.id,
    displayName: dto.display_name,
    status: dto.status === "ACTIVE" ? "active" : "disabled",
  };
}
```

### 2. Use `unknown` and narrowing to handle untrusted data

External input must be verified before use. Don't use `as` to shut up the compiler.

```ts
interface ApiErrorBody {
  message: string;
}

function isApiErrorBody(value: unknown): value is ApiErrorBody {
  return (
    typeof value === "object" &&
    value !== null &&
    "message" in value &&
    typeof value.message === "string"
  );
}

export function getApiErrorMessage(value: unknown): string {
  return isApiErrorBody(value) ? value.message : "Unexpected error";
}
```

### 3. Express state machine using discriminant union

Limited states such as asynchronous status, permission branches, payment status, etc. use discriminant fields to expose new branches during compilation.

```ts
type Loadable<T> =
  | { state: "idle" }
  | { state: "loading" }
  | { state: "success"; data: T }
  | { state: "error"; error: Error };

function assertNever(value: never): never {
  throw new Error(`Unhandled state: ${JSON.stringify(value)}`);
}

export function renderUserState(user: Loadable<{ name: string }>): string {
  switch (user.state) {
    case "idle":
      return "Ready";
    case "loading":
      return "Loading";
    case "success":
      return user.data.name;
    case "error":
      return user.error.message;
    default:
      return assertNever(user);
  }
}
```

### 4. Let generics serve callers, not show off their skills

Generics should reduce duplication and keep caller inference clear. When the complex type exceeds the reading cost, the named type will be demolished first.

```ts
interface SelectOption<TValue extends string | number> {
  label: string;
  value: TValue;
}

interface SelectProps<TValue extends string | number> {
  value: TValue;
  options: Array<SelectOption<TValue>>;
  onChange: (value: TValue) => void;
}

export function Select<TValue extends string | number>({
  value,
  options,
  onChange,
}: SelectProps<TValue>) {
  return (
    <select value={value} onChange={(event) => onChange(event.target.value as TValue)}>
      {options.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
}
```

### 5. Protect public types with type testing

Public tool types, component library types, and SDK types should have lightweight type tests or compile-time assertions.

```ts
type Equal<TLeft, TRight> =
  (<T>() => T extends TLeft ? 1 : 2) extends <T>() => T extends TRight ? 1 : 2
    ? true
    : false;

type Expect<T extends true> = T;

type UserStatus = UserViewModel["status"];
type _UserStatusTest = Expect<Equal<UserStatus, "active" | "disabled">>;
```

## Constraints

- Avoid `any`, unguarded non-null assertions and coercion `as` between unrelated types.
- Don’t pile large anonymous types on function parameters or JSX props; extract named types to express business meaning.
- Do not over-design recursive conditional types for simple business; type complexity should serve maintainability.
- The input and output of the public API must be explicitly annotated, and local variables can be relied upon for inference.
- Type modeling does not replace runtime validation; external data still requires schema or type guard.

## Expected Output

Produce clear type boundaries, narrowable data models, and necessary type testing and verification commands. The review should list type risks, runtime impacts, recommended modeling methods, and whether special fixes are needed.
