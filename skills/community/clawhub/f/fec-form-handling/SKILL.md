---
name: fec-form-handling
description: Use when building or reviewing substantial forms with React Hook Form, Zod schemas, typed validation, dynamic fields, controlled third-party inputs, file upload, multi-step flows, dependent validation, or form performance. Do not use for trivial 1-3 field forms without validation; Chinese triggers include form, form validation, dynamic fields.
---

# Form processing

## Purpose

Manage form status, verification and submission to avoid lags in complex form input.

## Procedure

1. First identify the framework, existing form library of the project, schema verification library, component library and complexity; then introduce special form solutions when there are 10+ fields, dynamic fields, linkage verification, file upload, multi-step process or input lag.
2. Select according to project stack: React can consider React Hook Form + Zod; Vue can consider vee-validate / FormKit + Zod, Yup or Valibot; simple forms can use the framework's native state and basic verification.
3. Use runtime schema or explicit validation functions to guard external input boundaries; TypeScript types can be deduced from the schema, but don’t just write TS types.
4. Clarify default values, field registration, controlled/uncontrolled boundaries and component library adaptation; use `aria-invalid`, `aria-describedby` and `role="alert"` for error prompts.
5. Handle loading, server-side errors, repeated submissions and resets when submitting; use local subscriptions and sub-component isolation to control re-rendering of large forms.

## React Quick Start

```tsx
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

const loginSchema = z.object({
  email: z.string().email("Please enter a valid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

type LoginForm = z.infer<typeof loginSchema>;

export function LoginFormView() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "", password: "" },
  });

  return (
    <form onSubmit={handleSubmit((data) => api.login(data))} noValidate>
      <label htmlFor="email">Email</label>
      <input id="email" {...register("email")} aria-invalid={!!errors.email} />
      {errors.email && <span role="alert">{errors.email.message}</span>}

      <label htmlFor="password">Password</label>
      <input id="password" type="password" {...register("password")} />
      {errors.password && <span role="alert">{errors.password.message}</span>}

      <button disabled={isSubmitting}>
        {isSubmitting ? "Submitting..." : "Submitting"}
      </button>
    </form>
  );
}
```

## Detailed reference

When it comes to whether you need a form library, framework selection, `Controller`, `useFieldArray`, linkage verification, file upload, multi-step form, asynchronous verification and performance mode, load [references/advanced-form-patterns.md](references/advanced-form-patterns.md).

## Constraints

- Inherit the existing form library, schema library and component library adaptation method of the warehouse, and do not introduce a second system for a single form.
- Default values must be complete to avoid undefined triggering controlled/uncontrolled warnings or initialization flutter.
- reset should be passed the full default object returned by the server or explicit.
- Asynchronous validation must be debounced or placed on a commit boundary to avoid typing requests every time.
- The error path of schema cascade dynamic verification must point to the actual field.

## Expected Output

The output form is type-safe, accessible, and has a clear submission status; complex fields and file uploads have schema constraints, there is no obvious lag in the input process, and server-side errors can be backfilled to a position that the user can understand.
