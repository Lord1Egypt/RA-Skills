# Editable Dumb rulesets

Antenna ships `rules/default.json`. Keep custom copies outside the plugin install
folder: upgrades replace the bundled default, not your own files. One file is
active at a time.

```json
{
  "formatVersion": 1,
  "rules": [
    {
      "id": "LOCAL-001",
      "pattern": "\\bignore\\s+previous\\s+instructions\\b",
      "flags": "iu",
      "explanation": "Instruction takeover phrase"
    }
  ]
}
```

Required fields are exactly those shown. IDs are unique, 1–64 letters, digits,
underscores or hyphens. Patterns use JavaScript RegExp syntax without `/.../`
delimiters. Flags may contain `i`, `m`, `s`, `u`, each once; matching iteration is
owned by the scanner. A match flags the message through existing hold/release
handling. No rule has executable code, scoring or a custom action.

Limits: 256 KiB file, 1–128 rules, 2,048 characters per pattern and 512 per
explanation. Files must be regular files, not symlinks/devices/FIFOs. Invalid or
missing selections fail visibly; there is no fallback to a different ruleset.
A worker deadline terminates expensive regexes with an incomplete scan.

## Edit, validate, evaluate, select

First [download and extract the diagnostics kit](OPTIONAL-KITS.md#diagnostics).
The examples use explicit paths: `/absolute/antenna` is your companion root,
`/absolute/diagnostics` is the extracted diagnostics root, and the host argument
is your resolved OpenClaw JSON configuration.

```sh
node /absolute/antenna/plugin/cli.mjs /absolute/openclaw.json rules validate /absolute/my-rules.json
node /absolute/diagnostics/diagnostics/cli.mjs /absolute/openclaw.json evaluate --engine dumb --ruleset /absolute/my-rules.json --preview
node /absolute/diagnostics/diagnostics/cli.mjs /absolute/openclaw.json evaluate --engine dumb --ruleset /absolute/my-rules.json --verbose
```

Review the missed attacks and false positives. Add `--corpus /absolute/my-tests.json`
to use your own examples; see the [corpus authoring guide](https://github.com/ClawReefAntenna/antenna-diagnostics/blob/v1.6.9/plugin/CORPORA.md).
Preview validates the inputs; the next command evaluates them. Neither changes your
active rules or releases held messages. Verbose failures include message content.

When you are ready to use the rules:

```sh
node /absolute/antenna/plugin/cli.mjs /absolute/openclaw.json rules select /absolute/my-rules.json
```

Reload Antenna through your host's normal reload procedure. Restart the gateway if
hot reload is unavailable or disabled. Editing an already-selected rules file also
requires reloading Antenna; each diagnostic invocation reads a fresh snapshot.
Remove a rule to disable it. Keep at least one rule; use MCS Off to disable scanning.
Omit `rulesetFile` from plugin configuration to return to the bundled default.

## Instructions to give your agent

“Edit a copy of this JSON ruleset. Preserve formatVersion and unique IDs. Add,
change or remove patterns, flags and short explanations. Validate it and run
Antenna's existing evaluation/custom tests. Show which attacks were missed and
which benign messages were flagged. Do not activate it unless requested.”

For downloaded rules: translate to JavaScript regex and JSON escaping, preserve
required license notices, and report unsupported constructs. Do not flatten
conjunctions, thresholds or exclusions into independent rules if doing so changes
their meaning. There is no automatic importer. No per-rule provenance or embedded
examples are required; put examples in the separate corpus or custom input files.

## Scanner behavior and default scope

The engine performs NFKC/lowercase normalization, removes selected zero-width
characters, and scans bounded Base64/escape projections. These are scanner code,
not user-supplied rule instructions. Direct clause-local negation can suppress a
match; quoting or code fences do not automatically suppress it. Decoding is never
execution. Original message bytes remain unchanged.

The bundled default contains nine locally authored MIT rules. It covers selected takeover, disclosure, bypass, remote execution
and concealment phrases. It is English-oriented, not a multilingual guarantee.
Security discussion can still cause false alarms; paraphrases can evade patterns.
The baseline corpus is a diagnostic sample, not a protection guarantee.

Design/pattern coverage was reviewed against ATR, OpenRouter's published patterns,
fevziegeyurtsevenler/prompt-injection-detection-rules, and OWASP guidance. No
third-party regex text is bundled; those sources are not runtime
dependencies or compatibility claims. Any future copied rules must carry the
notices their upstream licenses require.
