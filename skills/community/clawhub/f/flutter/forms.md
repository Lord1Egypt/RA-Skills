# Forms — Text Input, Focus, Validation, and the Keyboard

Forms concentrate three separate lifetimes: the controller's, the focus node's, and the form state's. Most form bugs are one of them being created in the wrong place or outliving its widget.

## Controller and Focus Lifetime

- `TextEditingController` and `FocusNode` are created in `initState` (or as `final` fields) and disposed in `dispose` (SKILL.md rule 3). Created inside `build`, the field clears itself on every rebuild — including the rebuild the keyboard causes when it opens.
- `TextFormField` accepts `initialValue` OR `controller`, never both — the assertion fires at runtime, in debug only.
- Setting `controller.text = value` moves the cursor to position 0 on some platforms and fires `onChanged`. To set text without losing the caret, set `value`: `controller.value = TextEditingValue(text: s, selection: TextSelection.collapsed(offset: s.length))`.
- Reading the value: `controller.text` at submit time. Mirroring every keystroke into `setState` rebuilds the screen per character — bind to `controller` where you need live display (a character counter listening to the controller) instead.
- A field inside a `ListView.builder` gets recycled: without a stable key, scrolling away and back moves the text to a different row (`state.md` rule 4).

## Form, Validation, and When Errors Appear

```dart
final _formKey = GlobalKey<FormState>();
// ...
Form(key: _formKey, autovalidateMode: AutovalidateMode.onUserInteraction, child: ...)
// on submit:
if (_formKey.currentState!.validate()) { _formKey.currentState!.save(); }
```

- `autovalidateMode` defaults to `disabled`: nothing validates until you call `validate()`. `AutovalidateMode.always` shows errors on an untouched empty form — hostile. `onUserInteraction` is the right default: errors appear only after the user has touched the field.
- `validator` returns `null` for valid and a message for invalid. Returning an empty string shows an empty error row that shifts the layout — return `null`.
- Validation runs on every `validate()` call and on every rebuild in autovalidate modes: keep validators pure and cheap. Async validation (username availability) does not belong in `validator` — run it on submit or on debounce, and hold the result in state that the validator reads.
- `save()` calls each field's `onSaved`; it is optional when you already hold controllers. Pick one path — controllers or `onSaved` — not both.
- Server-side errors are not form errors: map them onto fields explicitly after the response, by setting an error state your validator returns. A snackbar for a field-specific error is a usability bug.

## Focus Movement

- `textInputAction: TextInputAction.next` changes the keyboard's action key; moving focus is still your job in `onFieldSubmitted`: `FocusScope.of(context).nextFocus()`. Use `TextInputAction.done` on the last field and submit there.
- `autofocus: true` on the first field is right for single-purpose screens and wrong when it opens the keyboard over content the user needs to read first.
- `FocusScope.of(context).unfocus()` dismisses the keyboard. Tap-outside-to-dismiss needs a `GestureDetector` with `behavior: HitTestBehavior.opaque` around the body (`widgets.md`).
- Focus traversal follows the widget tree, not the visual layout. A two-column form built as two `Column`s tabs down one column then the other; `FocusTraversalGroup` with an ordering policy fixes it — and this matters on web and desktop where Tab is the primary navigation (`adaptive.md`).
- A `FocusNode` used with `addListener` to detect blur must remove that listener in `dispose`; the node's own dispose does not undo your subscription.

## The Keyboard

- `Scaffold.resizeToAvoidBottomInset` defaults to `true`: the body shrinks by the keyboard's height, which is why a `Column` that fit suddenly overflows (`layout.md`). Wrap the form body in a `SingleChildScrollView` — the standard answer.
- Inside a `ListView`/`SingleChildScrollView`, focusing a field scrolls it into view automatically. Inside a `Stack` or a fixed layout, nothing does — call `Scrollable.ensureVisible(context)` from the focus listener.
- `MediaQuery.viewInsetsOf(context).bottom` is the keyboard height; use it for a footer button that must sit above the keyboard. `viewPadding` and `padding` are different things (`adaptive.md`).
- `resizeToAvoidBottomInset: false` plus manual padding is the pattern for a full-bleed background that must not shrink — and it makes the ensure-visible behavior your responsibility.
- On iOS, the keyboard's accessory bar and the safe-area inset overlap; test on a device with a home indicator, not only on a simulator with a hardware keyboard attached.

## Input Formatting

- `inputFormatters` run before `onChanged`. A formatter that rewrites the whole string must also produce a sensible `TextSelection`, or the caret jumps to the end on every keystroke — the classic phone-mask and currency-field bug.
- `keyboardType: TextInputType.number` is a hint to the platform, not a constraint: some IMEs and hardware keyboards still deliver letters. Validate the value regardless.
- `TextInputType.numberWithOptions(decimal: true)` on iOS shows a keypad without a minus sign; negative numbers need a different input type or a sign toggle.
- Composing text (Japanese, Chinese, Korean IMEs, and autocorrect on iOS) arrives as intermediate values: a formatter or validator that rejects partial input makes those keyboards unusable. Validate on submit or on blur for text fields, not per keystroke.
- Trim whitespace and normalize case at the boundary, once, on submit — not inside the validator, which then disagrees with what gets saved.

## Autofill and Password Managers

- Wrap related fields in an `AutofillGroup` and set `autofillHints` (`AutofillHints.username`, `.password`, `.newPassword`, `.oneTimeCode`) — without them, platform password managers do not offer to fill or save.
- Signal a completed login with `TextInput.finishAutofillContext()` so the OS offers to save the credentials; skipping it is why "the app never asks to save my password".
- `obscureText: true` alone does not mark a field as a password to the platform; the autofill hint does.
- SMS one-time codes: `AutofillHints.oneTimeCode` gets the iOS keyboard suggestion and Android autofill for free — cheaper and more reliable than reading SMS, which requires permissions and store justification (`platform.md`).

## Submit Discipline

- Disable the submit control while the request is in flight, and re-enable it in a `finally`. Double submission creates duplicate records more often than any other form bug.
- Validate first, then disable, then send: disabling before validation leaves the user staring at a dead button with no error shown.
- Keep the user's input on failure. Clearing the form on a network error is destructive; re-render the same values with the error attached.
- After success, decide explicitly: pop with a result (`navigation.md`), reset the form (`_formKey.currentState!.reset()`), or navigate onward. Doing nothing leaves a submitted form on screen that the user will submit again.
