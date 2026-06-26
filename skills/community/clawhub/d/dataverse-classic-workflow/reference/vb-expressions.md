# VB.NET Bracket Expression Patterns

Dynamic values in classic workflow XAML are **VB.NET expressions wrapped in
square brackets `[…]`** and parsed by the WF4 expression compiler. They are
not text placeholders, not JMESPath, not Power Fx.

> All examples below use OOB entities (`account`, `contact`) or the synthetic
> `sample_widget` entity.
>
> Every bracketed expression is the `ExpressionText` of a `VisualBasicValue<T>`
> (r-value) or `VisualBasicReference<T>` (l-value) and is compiled to a
> LINQ-to-Entities expression at activation time. See
> [`web-research.md` §2](./web-research.md#2-vb-expressions--what-the-engine-actually-evaluates)
> for the engine-level binding rules and the constraints LINQ-to-Entities
> imposes on what an expression can reference.

---

## Anatomy of a bracket expression

```xml
<InArgument x:TypeArguments="x:String" x:Key="Subject">
  ["Follow up: " &amp; GetVariableValue(EntityProperty("name", "account"), "")]
</InArgument>
```

Breaking that down:

- The whole thing is wrapped in `[…]` — the VB compiler treats anything
  inside as a VB expression.
- `&amp;` is the XML escape for `&`, which is VB's string concatenation
  operator. (You will see `&` in the *unescaped* expression and `&amp;`
  in the XAML file.)
- `"…"` are VB string literals.
- `EntityProperty("name", "account")` returns a typed reference to a
  field on the workflow's primary entity context.
- `GetVariableValue(..., default)` resolves the typed reference into an
  actual value, with a fallback if null.

---

## The functions you'll see most

### `EntityProperty(attributeLogicalName, entityLogicalName)`

Returns a typed property reference. By itself it does not produce a value —
it produces something `GetVariableValue` can resolve. Always paired with
`GetVariableValue`.

### `GetVariableValue(reference, defaultValue)`

Resolves an `EntityProperty` (or other variable reference) to its actual
runtime value. The second argument is the fallback when the field is null.

```vb
GetVariableValue(EntityProperty("revenue", "account"), 0D)
```

### Concatenation and formatting

```vb
"Account: " & GetVariableValue(EntityProperty("name", "account"), "")
```

For numbers and dates, you'll usually see explicit conversion or formatting:

```vb
GetVariableValue(EntityProperty("createdon", "account"), Now()).ToString("yyyy-MM-dd")
```

### Conditional values

```vb
If(GetVariableValue(EntityProperty("statecode", "account"), 0) = 1, "Inactive", "Active")
```

### Math

```vb
GetVariableValue(EntityProperty("revenue", "account"), 0D) * 1.10D
```

---

## The seven expression shapes you'll actually encounter

In practice, every bracket expression in a real classic workflow XAML is
one of these seven shapes. Recognize them on sight — anything that doesn't
match is either a custom activity input or an expression you should preserve
verbatim and not try to interpret.

| # | Shape | Example | Where it appears |
|---|---|---|---|
| 1 | **Entity-dictionary access** | `InputEntities("primaryEntity")` or `CreatedEntities("Step3_localParameter#Temp").Id` | Step inputs and entity references |
| 2 | **`New Entity` constructor** | `New Entity("account")` | First activity of a Create / Update step — instantiates the in-memory record |
| 3 | **`New Object()` array (CreateCrmType payload)** | `New Object() { WorkflowPropertyType.String, "Hello", "" }` | Right-hand side of `EvaluateExpression` with `ExpressionOperator="CreateCrmType"` — carries `(propertyType, literalValue, typeHint)` |
| 4 | **`DirectCast`** | `DirectCast(someVariable, System.String)` | Coercing a workflow variable to a specific .NET type before use |
| 5 | **TerminateWorkflow exception ctor** | `New Microsoft.Xrm.Sdk.InvalidPluginExecutionException(OperationStatus.Succeeded)` | Body of a TerminateWorkflow / StopWorkflow activity — the enum value (`Succeeded` or `Canceled`) determines the exit status |
| 6 | **Bare variable reference** | `[primaryContactRef]` | Passing a previously-set workflow variable into another step's input |
| 7 | **Anything else** | `DateTime.UtcNow >= DirectCast(…).ToUniversalTime()` | Fall back to "unknown / preserve verbatim". Do not try to parse, do not modify — just round-trip the string. |

When rendering for the user, simplify shapes 1–6 into friendly tokens. Show
shape 7 as `<custom expression>` and offer the raw VB on demand.

---

## The `CreateCrmType` payload shape — critical for write operations

Whenever the designer needs to assign a literal value to an entity field,
it wraps the literal in a three-element `New Object()` array carrying the
Dataverse type information:

```xml
<mxswa:ActivityReference
    AssemblyQualifiedName="…EvaluateExpression…"
    DisplayName="">
  <mxswa:ActivityReference.Properties>
    <InArgument x:TypeArguments="x:String" x:Key="ExpressionOperator">
      <Literal>CreateCrmType</Literal>
    </InArgument>
    <InArgument x:TypeArguments="sco:ICollection(x:Object)" x:Key="Parameters">
      [New Object() { WorkflowPropertyType.String, &quot;Reviewed&quot;, &quot;&quot; }]
    </InArgument>
  </mxswa:ActivityReference.Properties>
</mxswa:ActivityReference>
```

The three array elements are always **(propertyType, literalValue, typeHint)**:

| Index | Meaning | Example values |
|---|---|---|
| 0 | `WorkflowPropertyType.<TypeName>` | `String`, `Boolean`, `DateTime`, `Decimal`, `Float`, `Integer`, `EntityReference`, `Money`, `OptionSetValue`, `Guid`, `PartyList` |
| 1 | The literal value (typed correctly for index 0) | `"Reviewed"`, `True`, `42`, `100D`, an `EntityReference`, etc. |
| 2 | Type hint string — entity logical name for `EntityReference`, optionset metadata for `OptionSetValue`, empty for primitives | `"contact"`, `"account_status"`, `""` |

When generating new field assignments, you must produce both the
`EvaluateExpression(CreateCrmType)` step **and** the following
`SetEntityProperty` that consumes its output variable. Skipping the
CreateCrmType wrapper produces a workflow that fails at activation with a
type mismatch, even when the literal looks the right type — Dataverse
requires the explicit `WorkflowPropertyType` tag.

**Special case — `Null` / `NotNull` operators skip CreateCrmType.** When a
Check Condition operator is `Null` or `NotNull`, no compare value is
needed, so the designer emits `<x:Null x:Key="Parameters" />` instead of an
`EvaluateExpression`. Generators must respect this special case.

---

## Token / placeholder formats inside `InputEntities` and `CreatedEntities`

The two dictionaries use specific key formats. Recognize them so you can
render tokens correctly:

| Key shape | Meaning |
|---|---|
| `InputEntities("primaryEntity")` | The triggering record itself |
| `InputEntities("related_<lookupField>#<targetEntity>")` | A record reached via an N:1 lookup from the primary entity (the field's logical name + `#` + the target entity's logical name) |
| `CreatedEntities("<StepName>_localParameter")` | The final stored record produced by an earlier Create or Update step |
| `CreatedEntities("<StepName>_localParameter#Temp")` | A **temporary** in-memory entity used during field assignments, before the actual `CreateEntity` / `UpdateEntity` commits |

The `#Temp` suffix is the most commonly-missed detail — within a single
Create or Update step, the same logical entity exists under both keys at
different times. Field assignments target the `#Temp` form; consumers in
later steps see the un-suffixed form. When summarizing for the user,
collapse both forms to the same friendly token — e.g. both
`CreatedEntities("CreateContact_localParameter")` and
`CreatedEntities("CreateContact_localParameter#Temp")` render as
`{Step "Create Contact": new Contact}`.

---

## Token vs literal — how the designer surfaces these

The classic workflow designer presents expressions as **tokens** (chips) in
the UI. The user picks "Account → Name" from a dropdown, and the designer
generates the underlying `GetVariableValue(EntityProperty("name", "account"), "")`
behind the scenes.

When you summarize a workflow for a user, render expressions in friendly form:

| XAML expression | Friendly form |
|-----------------|---------------|
| `GetVariableValue(EntityProperty("name", "account"), "")` | `{Account: Name}` |
| `GetVariableValue(EntityProperty("primarycontactid", "account"), Nothing)` | `{Account: Primary Contact}` |
| `[True]` | `True` |
| `[Now()]` | `(current date/time)` |

When you generate XAML for a user from a friendly description, expand to the
full bracket-expression form.

---

## Common pitfalls

- **Forgetting the brackets.** A naked VB expression (no `[…]`) is treated
  as a literal string by WF4. Result: the UpdateEntity step sets a field to
  the literal text "GetVariableValue(...)".
- **Wrong type literal.** VB requires type suffixes for some literals:
  `0D` for Decimal, `0L` for Long, `0F` for Single. Mixing types causes
  expression compile errors at workflow activation time, not authoring time.
- **`Nothing` vs `""` vs `0`.** Use `Nothing` as the default for reference
  types (lookups, dates), `""` for strings, `0` (or `0D`) for numerics.
  Mismatching produces NullReferenceException at runtime.
- **`&` vs `+`.** Use `&` for string concatenation. `+` works for numerics
  but VB's overload resolution sometimes silently coerces, leading to
  surprising results.
- **EntityProperty is not a value.** `EntityProperty("name", "account")` by
  itself, used as a string, will return the *type descriptor*, not the
  field value. Always wrap with `GetVariableValue`.

---

## Traversing related entities

To read a field on a related entity (via a lookup), the designer generates a
**RetrieveEntity → GetEntityProperty** chain rather than nesting inside one
expression. You will not see `EntityProperty("name", "account.primarycontactid")`
or similar dotted notation. The traversal is always procedural in the XAML
even if the designer presents it as a single token to the user.

Example: read the email of an account's primary contact:

```
1. GetEntityProperty: account.primarycontactid → primaryContactRef
2. RetrieveEntity:    primaryContactRef        → primaryContact (full Entity)
3. GetEntityProperty: primaryContact.emailaddress1 → primaryContactEmail
4. EvaluateExpression: ["Email is: " & GetVariableValue(primaryContactEmail, "")]
```

When summarizing, collapse this entire chain into the friendly form
`{Account → Primary Contact → Email}`.

---

## When the user gives you a friendly token, generate the XAML form

If a user says "set the subject to 'Follow up — ' followed by the account
name", you need to generate:

```xml
<InArgument x:TypeArguments="x:String" x:Key="Subject">
  [&quot;Follow up — &quot; &amp; GetVariableValue(EntityProperty(&quot;name&quot;, &quot;account&quot;), &quot;&quot;)]
</InArgument>
```

Note the XML escapes:
- `"` becomes `&quot;` inside XAML attribute values **and** inside text
  content of an element where it's quoted.
- `&` becomes `&amp;`.
- `<` becomes `&lt;`.
- `>` becomes `&gt;`.

Apply these escapes when generating; do not hand the raw `"` characters to
the file write — the resulting XAML will fail to parse on import.
