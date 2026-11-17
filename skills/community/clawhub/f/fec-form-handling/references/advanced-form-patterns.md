# Advanced form mode

## First determine whether a form library is needed

- A form with 1-3 fields, no complex validation, no dynamic fields, and no component library adaptation pressure. The native state of the framework, browser constraint verification, and lightweight submission state are available.
- When dynamic fields, cross-field verification, multi-step processes, file uploads, asynchronous verification, server-side error backfilling or obvious input lag are required, a special form solution will be introduced.
- The form library only manages field status and verification process, and does not replace API error mapping, permission judgment, accessibility annotation or server-side final verification.

## Selection reference

First, use the existing form library, schema library and component library adaptation method of the project; when adding new dependencies, select them according to the scenario.

| Scenarios | Alternative solutions | Notes |
| --- | --- | --- |
| React complex form | React Hook Form + Zod | Uncontrolled first, use `Controller` for third-party controlled components. |
| Vue complex forms | vee-validate / FormKit + Zod, Yup or Valibot | Do not introduce React-only form API into Vue projects; give priority to using the existing Vue form library of the project. |
| Simple form | Framework native state + basic validation | Avoid introducing heavy form system for 1-3 fields. |
| Multi-step form | Step-by-step schema + final submission schema | Clear step-by-step data saving, return to the previous step and final verification strategies. |
| File upload | Form library field status + `FormData` | Verify file quantity, size, type; do not serialize `File` JSON. |
| Asynchronous validation | Submit bounds validation or debounce field validation | Avoid each type request; handle race conditions and old response overwrites. |

## General implementation principles

- The runtime schema or validation function is responsible for external input bounds; TypeScript types are not a substitute for runtime validation.
- The default value, reset data and server-side backfill data must have the same shape to avoid fields switching between controlled/uncontrolled.
- Field errors must be mapped to specific fields; global errors are used for non-field problems such as submission failure, permissions or service unavailability.
- The component library adaptation layer must transparently transmit value, onChange, onBlur, name/ref or equivalent field registration capabilities.
- Protect loading, duplicate submissions, cancellation/expiration requests, server-side error backfill and reset after success when submitting.
- File upload uses `FormData` or direct transfer process. Front-end verification is only for experience protection, and the server still needs final verification.
- Performance optimization prioritizes the use of field-level subscriptions, partial component splitting, and delayed verification. Do not watch the entire form and then drive the entire page to re-render.

## React Hook Form Controller

```tsx
<Controller
  name="role"
  control={control}
  rules={{ required: "Please select a role" }}
  render={({ field, fieldState }) => (
    <>
      <Select {...field} options={roleOptions} />
      {fieldState.error && <span role="alert">{fieldState.error.message}</span>}
    </>
  )}
/>
```

Used for components such as Select, DatePicker, RichEditor, etc. that do not expose native `ref`.

## React Hook Form dynamic fields

```tsx
const { fields, append, remove } = useFieldArray({
  control,
  name: "contacts",
});

{fields.map((field, index) => (
  <div key={field.id}>
    <input {...register(`contacts.${index}.name`)} />
    <button type="button" onClick={() => remove(index)}>Delete</button>
  </div>
))}
```

`key` must use `field.id`, do not use array index.

## Zod linkage verification

```ts
const schema = z
  .object({
    password: z.string().min(8),
    confirmPassword: z.string().min(8),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "The two passwords are inconsistent",
    path: ["confirmPassword"],
  });
```

## Zod file upload verification

```ts
const schema = z.object({
  avatar: z
    .instanceof(FileList)
    .refine((files) => files.length > 0, "Please upload an avatar")
    .refine((files) => files[0]?.size <= 5 * 1024 * 1024, "The file size does not exceed 5MB")
    .refine((files) => ["image/jpeg", "image/png"].includes(files[0]?.type), "Only JPG/PNG is supported"),
});
```

Use `FormData` when submitting, do not serialize `File` JSON.

## Performance

- Replace full form watch with `useWatch` or field level subscription.
- Split large forms into memoized sub-components or framework-equivalent local update units.
- For high-frequency input, do not trigger network verification every time you type.
- For multi-step forms, the schema of each step and the final schema of the step must be clear.
