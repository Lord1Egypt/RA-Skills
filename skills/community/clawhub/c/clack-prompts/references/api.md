# @clack/prompts API Reference

Build beautiful command-line apps. An opinionated, pre-styled wrapper around `@clack/core`.

```
npm install @clack/prompts
```

## Table of Contents

- [Session Helpers](#session-helpers)
- [Input Components](#input-components)
- [Selection Components](#selection-components)
- [Multi-Select Components](#multi-select-components)
- [UI Components](#ui-components)
- [Utilities](#utilities)
- [Logging](#logging)
- [Streaming Logs](#streaming-logs)
- [Task Log](#task-log)

---

## Session Helpers

### intro(message: string)

Print a message to begin a prompt session.

```js
import { intro } from '@clack/prompts';
intro(`create-my-app`);
```

### outro(message: string)

Print a message to end a prompt session.

```js
import { outro } from '@clack/prompts';
outro(`You're all set!`);
```

### cancel(message?: string)

Print a styled cancellation message. Use after detecting cancellation with `isCancel()`.

```js
import { cancel } from '@clack/prompts';
cancel('Operation cancelled.');
```

### isCancel(value: any): boolean

Guard that detects when a user cancels a question with `CTRL + C`. Returns `true` if the value is a cancel symbol. Always check before using a prompt result.

```js
import { isCancel, cancel, text } from '@clack/prompts';

const value = await text({ message: 'Name?' });
if (isCancel(value)) {
  cancel('Cancelled.');
  process.exit(0);
}
```

---

## Input Components

### text(options): Promise&lt;string | symbol&gt;

Single-line text input.

| Option | Type | Description |
|--------|------|-------------|
| message | string | **Required.** Prompt message |
| placeholder | string | Placeholder text when empty |
| initialValue | string | Pre-filled value |
| defaultValue | string | Returned on empty submit |
| validate | (value: string) => string \| void | Validation fn. Return error string or undefined |

```js
const name = await text({
  message: 'What is your name?',
  placeholder: 'John',
  initialValue: '',
  validate(value) {
    if (!value.length) return 'Value is required!';
  },
});
```

### password(options): Promise&lt;string | symbol&gt;

Like `text` but masks input. Same options as `text`, plus:

| Option | Type | Description |
|--------|------|-------------|
| mask | string | Mask character (default: hidden) |

```js
const secret = await password({
  message: 'Set a password.',
  mask: '*',
  validate(value) {
    if (!value || value.length < 8)
      return 'Password must be at least 8 characters.';
  },
});
```

### confirm(options): Promise&lt;boolean | symbol&gt;

Yes/no confirmation. Returns `true` or `false`.

| Option | Type | Description |
|--------|------|-------------|
| message | string | **Required.** Prompt message |
| initialValue | boolean | Default selection (default: `true`) |

```js
const shouldContinue = await confirm({
  message: 'Do you want to continue?',
});
```

### multiline(options): Promise&lt;string | symbol&gt;

Multi-line text input. By default, press `Enter` twice to submit.

| Option | Type | Description |
|--------|------|-------------|
| message | string | **Required.** Prompt message |
| placeholder | string | Placeholder text |
| initialValue | string | Pre-filled value |
| defaultValue | string | Returned on empty submit |
| validate | (value: string) => string \| void | Validation fn |
| showSubmit | boolean | Show explicit submit button instead of double-Enter |

```js
const bio = await multiline({
  message: 'Tell us about yourself.',
  placeholder: 'Start typing...',
  validate(value) {
    if (!value.length) return 'value is required';
  },
});

// With explicit submit button:
const bio2 = await multiline({
  message: 'Tell us about yourself.',
  showSubmit: true,
});
```

### path(options): Promise&lt;string | symbol&gt;

Filesystem path input with tab-completion suggestions.

| Option | Type | Description |
|--------|------|-------------|
| message | string | **Required.** Prompt message |
| directory | boolean | Only allow directory selection |

```js
const targetDir = await path({
  message: 'Select an existing directory.',
  directory: true,
});
```

---

## Selection Components

### select(options): Promise&lt;string | symbol&gt;

Choose one value from a list. Result is the `value` prop of the chosen option.

| Option | Type | Description |
|--------|------|-------------|
| message | string | **Required.** Prompt message |
| options | Option[] | **Required.** Array of options |

**Option object:**

| Field | Type | Description |
|-------|------|-------------|
| value | string | **Required.** Return value when selected |
| label | string | Display label |
| hint | string | Hint shown after label |
| disabled | boolean | Gray out and prevent selection |

```js
const projectType = await select({
  message: 'Pick a project type.',
  options: [
    { value: 'ts', label: 'TypeScript' },
    { value: 'js', label: 'JavaScript', disabled: true },
    { value: 'coffee', label: 'CoffeeScript', hint: 'oh no' },
  ],
});
```

### autocomplete(options): Promise&lt;string | symbol&gt;

Filter a list by typing, then choose one. Matching uses each option's `label`, `hint`, and `value`. Result is the selected `value`.

| Option | Type | Description |
|--------|------|-------------|
| message | string | **Required.** Prompt message |
| options | Option[] | **Required.** Array of options |
| placeholder | string | Placeholder when empty |

Options use the same shape as `select`.

```js
const framework = await autocomplete({
  message: 'Pick a framework.',
  placeholder: 'Type to search...',
  options: [
    { value: 'next', label: 'Next.js' },
    { value: 'nuxt', label: 'Nuxt' },
    { value: 'sveltekit', label: 'SvelteKit' },
    { value: 'remix', label: 'Remix' },
  ],
});
```

### selectKey(options): Promise&lt;string | symbol&gt;

Choose an option by pressing its single-character `value` key directly.

| Option | Type | Description |
|--------|------|-------------|
| message | string | **Required.** Prompt message |
| options | Option[] | **Required.** Array of options |

```js
const action = await selectKey({
  message: 'Pick an action.',
  options: [
    { value: 'd', label: 'Deploy' },
    { value: 't', label: 'Run tests' },
    { value: 'q', label: 'Quit' },
  ],
});
```

---

## Multi-Select Components

### multiselect(options): Promise&lt;string[] | symbol&gt;

Choose multiple values from a list. Result is an array of selected `value` strings.

| Option | Type | Description |
|--------|------|-------------|
| message | string | **Required.** Prompt message |
| options | Option[] | **Required.** Options (same shape as `select`) |
| required | boolean | Require at least one selection (default: `true`) |
| cursorAt | string | Pre-select an option by its `value` |

```js
const tools = await multiselect({
  message: 'Select additional tools.',
  options: [
    { value: 'eslint', label: 'ESLint', hint: 'recommended' },
    { value: 'prettier', label: 'Prettier', disabled: true },
    { value: 'gh-action', label: 'GitHub Action' },
  ],
  required: false,
});
```

### groupMultiselect(options): Promise&lt;string[] | symbol&gt;

Grouped multi-select. Options organized into named groups.

| Option | Type | Description |
|--------|------|-------------|
| message | string | **Required.** Prompt message |
| options | Record&lt;string, Option[]&gt; | **Required.** Grouped options |

```js
const basket = await groupMultiselect({
  message: 'Select your favorite fruits and vegetables:',
  options: {
    fruits: [
      { value: 'apple', label: 'apple' },
      { value: 'banana', label: 'banana' },
    ],
    vegetables: [
      { value: 'carrot', label: 'carrot' },
      { value: 'spinach', label: 'spinach' },
    ],
  },
});
```

---

## UI Components

### spinner(): Spinner

Surfaces a pending action. Call `.start(msg)` to begin, `.stop(msg?)` to end.

```js
import { spinner } from '@clack/prompts';

const s = spinner();
s.start('Installing via npm');
// Do installation work...
s.stop('Installed via npm');
```

The stop message can be omitted for a simple stop animation:
```js
s.start('Working...');
// ...
s.stop();  // Clears spinner with checkmark, no message
```

### progress(options): Progress

Extends spinner with a progress bar.

| Option | Type | Description |
|--------|------|-------------|
| max | number | **Required.** Total progress steps |

```js
import { progress } from '@clack/prompts';

const p = progress({ max: 10 });
p.start('Downloading archive');
p.advance(3, 'Downloading (30%)');
p.advance(5, 'Downloading (80%)');
p.stop('Archive downloaded');
```

---

## Utilities

### group(questions, options?): Promise&lt;T&gt;

Group multiple prompts together. Each key is a lazily-evaluated question function.
The `results` parameter carries previously-answered values within the group, enabling dynamic prompts.

| Option | Type | Description |
|--------|------|-------------|
| onCancel | ({ results }) => void | Called if user cancels any prompt in the group |

```js
import * as p from '@clack/prompts';

const group = await p.group(
  {
    name: () => p.text({ message: 'What is your name?' }),
    age: () => p.text({ message: 'What is your age?' }),
    color: ({ results }) =>
      p.multiselect({
        message: `What is your favorite color ${results.name}?`,
        options: [
          { value: 'red', label: 'Red' },
          { value: 'green', label: 'Green' },
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

console.log(group.name, group.age, group.color);
```

**Key behavior:** Each function in `group` receives `{ results }` containing the accumulated results from prior prompts. This allows conditional or dynamic prompts based on previous answers.

### tasks(tasks): Promise&lt;void&gt;

Execute multiple tasks with individual spinners.

```js
import { tasks } from '@clack/prompts';

await tasks([
  {
    title: 'Installing via npm',
    task: async (message) => {
      // message is a callback to update the task's spinner text
      // Do installation here
      return 'Installed via npm';
    },
  },
  {
    title: 'Running tests',
    task: async () => {
      // This task runs after the first completes
      throw new Error('Tests failed!');
    },
  },
]);
```

**Note:** Tasks execute sequentially. Throwing an error marks the task as failed (red X). Returning a string marks it as succeeded (green checkmark with the string).

---

## Logging

### log methods

Print styled log messages without prompting.

```js
import { log } from '@clack/prompts';

log.info('Info!');
log.success('Success!');
log.step('Step!');
log.warn('Warn!');
log.error('Error!');
log.message('Hello, World', { symbol: color.cyan('~') });
```

| Method | Style |
|--------|-------|
| log.info(msg) | Blue info symbol |
| log.success(msg) | Green checkmark |
| log.step(msg) | Yellow step symbol |
| log.warn(msg) | Yellow warning |
| log.error(msg) | Red X |
| log.message(msg, opts?) | Custom symbol via `opts.symbol` |

`log.message` requires a `symbol` option (typically from a color library):
```js
import color from 'picocolors';
log.message('Custom', { symbol: color.cyan('~') });
```

### note(message, title?)

Print a bordered note block.

```js
import { note } from '@clack/prompts';
note('Please configure your API key.', 'API Key Required');
```

---

## Streaming Logs

### stream methods

Render log messages from an iterable (sync or async). Useful for LLM streaming or other dynamic data sources.

```js
import { stream } from '@clack/prompts';
import color from 'picocolors';

stream.info((function* () { yield 'Info!'; })());
stream.success((function* () { yield 'Success!'; })());
stream.step((function* () { yield 'Step!'; })());
stream.warn((function* () { yield 'Warn!'; })());
stream.error((function* () { yield 'Error!'; })());
stream.message((function* () { yield 'Hello'; yield ', World'; })(), {
  symbol: color.cyan('~'),
});
```

Methods mirror `log`: `info`, `success`, `step`, `warn`, `error`, `message`.
Each accepts an iterable (generator, async generator, array, etc.).

---

## Task Log

### taskLog(options)

Render sub-process output with live streaming. On success, output is cleared; on failure, output remains visible.

| Option | Type | Description |
|--------|------|-------------|
| title | string | **Required.** Title for the task |

```js
import { taskLog } from '@clack/prompts';

const log = taskLog({
  title: 'Running npm install',
});

// Stream each line to the task log
for await (const line of npmInstall()) {
  log.message(line);
}

if (success) {
  log.success('Done!');  // Clears output on success
} else {
  log.error('Failed!');  // Output remains visible on error
}
```

| Method | Description |
|--------|-------------|
| log.message(line) | Append a line of output |
| log.success(msg?) | Mark as success (clears log output) |
| log.error(msg?) | Mark as failure (keeps output visible) |
