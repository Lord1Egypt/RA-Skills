# Rails Turbo And Controller Traps

The places a Rails framework does something different from what the code looks like it does.

## What unit tests miss in Rails

Rails has a large surface where the framework does something different from
what the code looks like it does. These are the places a Rails review earns
its keep.

### Turbo: the attribute lands on the wrong element

```erb
<%# WRONG - puts data-turbo on the button, but Turbo reads the form %>
<%= button_to "Save", path, data: { turbo: false } %>
```

```erb
<%# RIGHT - the attribute has to be on the form %>
<%= form_with model: @record, data: { turbo: false } do |f| %>
```

`form_with` also has a `local: true` option, which does **not** opt the form
out of Turbo. To get a non-Turbo form, pass `data: { turbo: false }`
explicitly.

**Symptom:** the form submits, the page stays put, no flash, no error, and the
request never reaches the server.

### Turbo: `data-turbo-frame` beats `data-turbo="false"`

If an element has **both** attributes, Turbo ignores the opt-out and
processes within the frame. The result is a form that appears to hang in an
infinite spinner.

```erb
<%# WRONG - both attributes present %>
<%= form_with model: @record, data: { turbo_frame: "modal", turbo: false } %>
```

```erb
<%# RIGHT - branch the data hash so only one is ever present %>
<%= form_with model: @record, data: turbo_frame_options %>
```

where `turbo_frame_options` is built so that the frame attribute is omitted
in the case that needs a full-page navigation.

### Turbo: `turbo_stream.replace` destroys its target

`turbo_stream.replace "dom_id", partial: "..."` replaces the **entire**
element. Any Stimulus controller attached to it is destroyed and
re-initialized, losing its state.

```erb
<%# WRONG - tears down the controller %>
<%= turbo_stream.replace "card_#{item.id}" do %>
  <%= render "item", item: item %>
<% end %>
```

```erb
<%# RIGHT - update targets the content, append preserves the controller %>
<%= turbo_stream.update "status_#{item.id}" do %>
  <%= render "status", item: item %>
<% end %>
```

### Redirects from inside a Turbo Frame

A form inside `<turbo-frame id="modal">` that redirects to a URL **outside**
the frame produces a broken request to the original path with `undefined`
appended.

- Use `data: { turbo: false }` on forms that do full-page navigation
  (password changes, sign-out).
- Make sure the redirect target is inside the frame, or that the form is not
  frame-scoped.

### `skip_before_action` with both `only:` and `if:`

This is a framework trap worth checking on every Rails review that touches
callbacks:

```ruby
skip_before_action :foo, only: %i[a b], if: -> { some_predicate }
```

When both `only:` and `if:` are present, Rails adds an always-truthy filter
to the skip's `unless` array. The skip does not behave the way it reads.

**Diagnostic:**

```ruby
controller._process_action_callbacks.select { |c| c.kind == :before }.each do |c|
  puts "filter=#{c.filter} unless=#{c.instance_variable_get(:@unless).inspect}"
end
```

### `params.expect` and index-keyed nested attributes

Rails 8's `params.expect` is the preferred strong-parameter pattern, but it
strips the hash keys from nested attributes keyed by index
(`items_attributes: { "0" => {...} }`).

```ruby
# works for flat + simple nested
params.expect(post: [:title, :body, tag_ids: []])

# use the classic form for index-keyed nested attributes
params.require(:post).permit(:title, items_attributes: [:id, :name, :_destroy])
```

**Symptom:** the top-level attributes arrive and the nested collection comes
back empty.

### CSRF scope

`skip_forgery_protection` belongs on an API-only controller - one that
renders no forms and authenticates machine clients carrying their own
token. It is not something to add to a controller that serves an HTML form.

In a review, treat a CSRF skip on a form-rendering controller as
`block-merge`. A browser attaches the session cookie to a cross-site POST,
and without the token check that request is accepted as the signed-in user.

**Related:** a request spec failing on `ActionController::InvalidAuthenticityToken`
is usually a missing token in the spec, not a controller problem. Fix the
spec rather than weakening the controller.

---

## Rails review findings that are usually `block-merge`

| Finding | Why |
|---|---|
| CSRF disabled on a form-rendering controller | Forged requests accepted as the signed-in user |
| A form that submits but never reaches the server | The user's action silently does nothing |
| A Turbo Frame redirect to outside the frame | Infinite spinner, user is stuck |
| A spec that injects a param to satisfy a guard | The real path is broken and hidden |
| `skip_before_action` with both `only:` and `if:` | The skip does not do what it reads like |
| Missing transaction around a multi-write operation | Partial state on failure |
| No idempotency on a charge or a state transition | Double charge on retry |
| `update_column` / `update_all` on a validated field | Validation bypassed in production |
| A cached fragment containing permission-dependent data | One user sees another's data |

---
