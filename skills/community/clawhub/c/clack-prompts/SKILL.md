---
name: clack-prompts
description: Build beautiful interactive Node.js command-line apps with @clack/prompts. Use when building CLI apps, wizards, setup scripts, or any interactive terminal prompt flow in Node.js. Covers text input, password, confirm, select, autocomplete, multiselect, spinner, progress bars, grouped prompts, task runners, and styled logging.
---

# @clack/prompts

Build beautiful, minimal interactive CLI apps. Pre-styled, tree-shakeable, 80% smaller than alternatives.

## Quick Start

```
npm install @clack/prompts
```

```js
import { intro, outro, text, isCancel, cancel } from '@clack/prompts';

intro('create-my-app');

const name = await text({ message: 'Project name?' });
if (isCancel(name)) { cancel('Cancelled.'); process.exit(0); }

outro(`Done! Created ${name}.`);
```

## Core Pattern — Always Guard Cancellation

Every prompt can return a cancel symbol (user pressed `Ctrl+C`). Always use `isCancel()`:

```js
const result = await text({ message: 'Name?' });
if (isCancel(result)) {
  cancel('Cancelled.');
  process.exit(0);
}
```

## Choosing the Right Component

| Need | Component | Returns |
|------|-----------|---------|
| Single-line text | `text` | string |
| Masked secret | `password` | string |
| Yes / No | `confirm` | boolean |
| Pick one from list | `select` | string (value) |
| Searchable pick one | `autocomplete` | string (value) |
| Single-key selection | `selectKey` | string (value) |
| Pick many from list | `multiselect` | string[] |
| Pick many, grouped | `groupMultiselect` | string[] |
| Multi-line text area | `multiline` | string |
| Filesystem path | `path` | string |
| Calendar date | `date` | Date |

## Common Patterns

### Sequential Prompts with group()

Chain prompts where later ones depend on earlier answers:

```js
import * as p from '@clack/prompts';

const result = await p.group(
  {
    name: () => p.text({ message: 'What is your name?' }),
    age: () => p.text({ message: 'What is your age?' }),
    color: ({ results }) =>
      p.multiselect({
        message: `What is your favorite color ${results.name}?`,
        options: [
          { value: 'red', label: 'Red' },
          { value: 'blue', label: 'Blue' },
        ],
      }),
  },
  {
    onCancel: ({ results }) => {
      p.cancel('Operation cancelled.');
      process.exit(0);
    },
  },
);
```

### Task Runner with Spinners

Run sequential tasks, each with its own spinner:

```js
import { tasks } from '@clack/prompts';

await tasks([
  {
    title: 'Installing via npm',
    task: async () => {
      // Return a string = success with checkmark
      return 'Installed via npm';
    },
  },
  {
    title: 'Running tests',
    task: async () => {
      throw new Error('Tests failed!');  // Error = red X
    },
  },
]);
```

### Standalone Spinner

```js
import { spinner } from '@clack/prompts';

const s = spinner();
s.start('Uploading...');
try { await upload(); s.stop('Uploaded!'); }
catch { s.stop('Upload failed'); }
```

### Progress Bar

```js
const p = progress({ max: 100 });
p.start('Downloading');
for (const chunk of chunks) { p.advance(1); }
p.stop('Done');
```

### Live Sub-Process Output with taskLog

```js
import { taskLog } from '@clack/prompts';

const log = taskLog({ title: 'npm install' });
for await (const line of npmInstall()) { log.message(line); }
log.success('Done!');   // Clears output on success
// log.error('Failed!'); // Keeps output visible on failure
```

## Styled Logging (no user input)

```js
import { log } from '@clack/prompts';
import color from 'picocolors';

log.info('Starting setup...');
log.success('Config written!');
log.step('Checking dependencies...');
log.warn('Optional peer dep missing');
log.error('Build failed');
log.message('Custom', { symbol: color.cyan('~') });
```

## Streaming Logs

For LLM output or dynamic streams:

```js
import { stream } from '@clack/prompts';

stream.info((function* () { yield 'Info!'; })());
stream.success((async function* () { yield 'Done!'; })());
stream.message(
  (function* () { yield 'Hello'; yield ', World'; })(),
  { symbol: color.cyan('~') }
);
```

## Selection Options Shape

Used by `select`, `autocomplete`, `selectKey`, `multiselect`, `groupMultiselect`:

```js
{ value: 'ts', label: 'TypeScript' }           // Basic
{ value: 'js', label: 'JavaScript', disabled: true }  // Disabled
{ value: 'coffee', label: 'CoffeeScript', hint: 'oh no' } // With hint
```

## Validation

Most components accept a `validate(value)` that returns `string` (error message) or `undefined` (valid):

```js
const name = await text({
  message: 'Username?',
  validate(value) {
    if (!value.length) return 'Username is required!';
    if (value.length < 3) return 'At least 3 characters.';
  },
});
```

## Full API Reference

See [references/api.md](references/api.md) for every component's complete signature, options table, and examples.
