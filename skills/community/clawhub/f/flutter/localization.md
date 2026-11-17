# Localization — Translations, Plurals, RTL, and Formats

Localization is four separate problems: extracting strings, choosing the right variant at runtime, formatting numbers and dates per locale, and surviving right-to-left layout. Doing the first three and skipping the fourth is the usual outcome, and it is the one users notice most.

## Setup and the ARB Workflow

- `flutter_localizations` plus generated delegates is the supported path: declare `generate: true` under `flutter:` in `pubspec.yaml`, add `l10n.yaml`, put translations in `lib/l10n/app_<locale>.arb`, and the SDK generates a lookup class at build time.
- `MaterialApp` needs both `localizationsDelegates` (yours plus the Material, Widgets, and Cupertino delegates) and `supportedLocales`. Missing the framework delegates means Material's own strings — dialog buttons, date pickers, tooltips — stay in English while yours translate.
- The template ARB (usually English) is the schema. Every key added there must reach every other file; a missing key falls back to the template silently, so an untranslated app looks finished.
- Keys are identifiers, not sentences. `checkoutPayButton` survives a copy change; `payNow` becomes a lie the moment the copy changes.
- Every string gets a `@key` description entry with context ("verb, button label"). Translators receiving a bare word cannot know whether "Order" is a noun or a verb, and that ambiguity is where the worst translations come from.
- Placeholders are typed in the ARB (`"count": {"type": "int"}`); a mistyped placeholder produces a compile error in generated code rather than a runtime surprise.

## Plurals, Gender, and Interpolation

- ICU plural syntax is the mechanism: `{count, plural, =0{No items} =1{1 item} other{{count} items}}`. Never build a plural by concatenating a number and a suffix — many languages have more than two plural categories, and several have none.
- `=1` and `one` are different: `=1` matches the literal value, `one` matches the language's "one" CATEGORY, which in some languages includes 21 and 31. Use the categories, and let the translator add the ones their language needs.
- ICU `select` handles gendered strings; hardcoding two branches in Dart pushes a grammar decision into code that translators cannot reach.
- Never concatenate translated fragments. "Deleted " + n + " files" is untranslatable because word order changes; one parameterized string per sentence is the rule.
- Do not translate at parse time and cache the result: locale can change while the app runs (`didChangeLocales`), and cached strings then go stale.

## Runtime Resolution

- `Localizations.of(context)` — and the generated `AppLocalizations.of(context)` — read from the tree, so strings need a `BuildContext` below `MaterialApp`. Code in the data or application layer must return keys or typed errors, and let the UI render them (`architecture.md`).
- `localeResolutionCallback` decides what happens when the device locale is not supported. The default picks a language match ignoring the country, then falls back to the first supported locale — verify that fallback is the one you want, because it is what most users of unsupported locales will see.
- Locale is language + optional script + optional country: `zh_Hans` and `zh_Hant` are not interchangeable, and `pt_BR` and `pt_PT` differ enough to matter.
- An in-app language switch means storing the choice (`data.md`) and passing `locale:` to `MaterialApp` explicitly; the OS setting is only the default.
- Changing locale rebuilds the app: any widget caching a localized string in `initState` keeps the old language. Read strings in `build` or `didChangeDependencies` (`state.md`).

## Numbers, Dates, and Units

- `package:intl` formats per locale: `NumberFormat.currency(locale: ..., name: 'EUR')`, `DateFormat.yMMMd(locale)`. `DateTime.toString()` and manual `'$d/$m/$y'` are wrong in most of the world.
- Decimal separators, thousands separators, and currency symbol position all vary. A parser that assumes `.` as the decimal point rejects perfectly valid input in much of Europe — parse with `NumberFormat.parse`, not `double.parse`, on user input (`forms.md`).
- Dates are the classic ambiguity: 03/04 is two different days depending on the locale. Use a format with a named month wherever a mistake would matter.
- Time zones: `DateTime` is either local or UTC. Store UTC, format local, and never subtract two dates across a DST boundary without a time-zone-aware library.
- `DateFormat` for a non-current locale requires that locale's data to be initialized first (`initializeDateFormatting`), or it throws at the first format call.

## Right-to-Left

- Arabic, Hebrew, Persian, and Urdu mirror the entire layout, not just the text. Flutter does most of it if you let it.
- **Use the directional variants**: `EdgeInsetsDirectional` (`start`/`end`) instead of `EdgeInsets` (`left`/`right`), `AlignmentDirectional`, `BorderRadiusDirectional`, and `PositionedDirectional`. Every hardcoded `left` is a bug in RTL.
- `MainAxisAlignment.start` already flips; `Alignment.centerLeft` does not. That asymmetry is the source of most half-mirrored screens.
- Icons that indicate direction (back arrows, next chevrons, undo) must mirror; icons that represent objects (a camera, a clock) must not. `Transform.flip` on the whole icon set is the wrong fix.
- `Directionality` is the ambient value. Wrapping a preview in `Directionality(textDirection: TextDirection.rtl, ...)` — including in a widget test — is the cheapest way to check a screen (`testing.md`).
- Mixed-direction content (an English brand name in an Arabic sentence, a phone number) renders through the Unicode bidi algorithm; test with real strings, not with reversed Latin text.

## Layout Under Translation

- Translated text is routinely longer than the source: German and Finnish commonly overflow buttons and tabs sized to fit English. Design for growth or let the text wrap; a fixed-width button with a centered label is the widget that breaks first (`layout.md`).
- Combine with text scaling: a long translation at a large accessibility text size is the real worst case, and it is the one to test (`accessibility.md`).
- Never bake text into images — it cannot be translated, and it fails accessibility at the same time.
- Sorting a list of names alphabetically is locale-dependent; the default `compareTo` is code-point order, which puts accented characters in the wrong place for most languages.

## Verifying

- A pseudo-locale pass (wrap every string in markers and pad its length) exposes both hardcoded strings and layouts that cannot grow, before any translation exists.
- Widget tests can pump a screen once per supported locale plus one RTL locale, asserting no overflow — that catches the whole category cheaply (`testing.md`).
- Audit for hardcoded strings periodically: any user-visible literal in a widget file is a missed translation. A lint rule for literal strings in widget constructors keeps it from regressing.
