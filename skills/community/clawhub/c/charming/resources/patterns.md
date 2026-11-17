# Patterns worth reusing

## Agent-mediated enrich

For data that needs research (a place, a book, a company), store a stub record immediately, then show a dismissible modal with a copy-paste prompt that tells the agent to call an `enrich`/`addDetails` op with the researched fields. The agent does the lookup and writes the result back through the same `window.charming.api(id).<op>()` call any other mutation uses — there is no separate write path for agent-sourced data.

## Undo-toast deletes

Preferred over confirm dialogs, which no-op in the sandbox. Delete immediately, show a bottom-center toast — "Removed · Undo" — for about six seconds, and have Undo call a `restore` op that upserts the full record back by id:

```js
async function removeItem(id) {
  const removed = items.find((item) => item.id === id);
  items = items.filter((item) => item.id !== id);
  await api.remove({ id });
  render();
  showToast('Removed', {
    action: 'Undo',
    onAction: async () => {
      await api.restore({ item: removed });
      items = [...items, removed];
      render();
    },
  });
}
```

## Inline confirm

For destructive actions big enough to want a confirmation but where a modal `confirm()` would no-op — delete-all, delete-list — swap the trigger button's own label and handler instead of opening a dialog:

```js
button.textContent = 'Delete?';
button.onclick = () => {
  button.replaceWith(confirmRow(onConfirm, onCancel));
};
```

## Migration discipline

Use a versioned storage key from the start — `items_v1`, not `items`. On read, run a `normalize()` step that fills defaults for any field added since the app was first written, so old records stay valid without a migration:

```js
function normalize(item) {
  return { done: false, tags: [], ...item };
}
```

When a change is a genuine shape change (a field renamed, a type changed), write a `migrate(old)` function, bump the key to `items_v2`, and read+migrate from the old key for one release cycle before removing it. Never mutate old records in place without a version bump — an agent revisiting the app months later has no other way to know which shape it's looking at.

## PII and sharing

Keep all user data in `env.storage`. Never put real data — a name, an email, a value the user typed — into a `module.js` constant, even temporarily while prototyping. Charming apps can be shared, templated, or remixed; a copy made from a `manifest`/`module` that embeds real data leaks it into every copy. Seed data for a template or example app belongs in a `seed` route the app calls once at first load, not in the source.

## Display-only apps

Not every app needs storage. A dashboard, a static reference, a one-shot calculator can skip `capabilities.imports` entirely and do all of its work in `ui.js` — no `routes` beyond what's needed, no `env.storage`. Don't reach for storage by default; add it only when the app needs to remember something between visits.

## Partner-facing apps

An app meant to be shared externally — a living engagement doc, a feature-status page for a partner or customer — reads differently from a personal tool: no placeholder copy, no "TBD" sections, and no internal shorthand the recipient wouldn't recognize. Source every claim from real notes or a real conversation rather than writing generic filler, and read the whole thing back once as if you were the recipient forwarding it to their own team — anything that would need an explanation in that forward should be cut or rewritten in place.
