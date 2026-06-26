---
name: commander
description: Commander.js is the most popular command-line interface (CLI) framework for Node.js. Used to create professional CLI programs, supporting option parsing, subcommands, automatic help generation, TypeScript, etc.
---

# Commander.js

## Trigger Scenarios

- Quickly create CLI scaffolding
- Define options and arguments
- Create subcommands
- Customize help information
- TypeScript support

## Quick Start

```js
// 1. Install
npm install commander

// 2. Create CLI
const { Command } = require('commander');
const program = new Command();

program
  .name('my-cli')
  .description('My CLI Tool')
  .version('1.0.0');

program.parse();
```

## Option Definition

### Basic Option Types

```js
// Boolean option (no argument)
program.option('-d, --debug', 'Enable debug mode');

// Value option (requires argument)
program.option('-p, --port <number>', 'Server port', '3000');

// Optional value option
program.option('--cheese [type]', 'Add cheese (optional type)');

// Negated boolean option
program.option('--no-sauce', 'No sauce');

// Required option
program.requiredOption('-c, --cheese <type>', 'Must choose a cheese type');

// Variadic option (array)
program.option('--items <items...>', 'Multiple items');
```

### Accessing Option Values

```js
const options = program.opts();
console.log(options.debug); // or program.opts().debug

// Camel-case naming conversion: --template-engine → opts().templateEngine
```

### Custom Option Processing

```js
program.option('--date <date>', 'Date', (value) => new Date(value));
```

## Subcommands

### Inline Subcommands

```js
program.command('serve')
  .description('Start server')
  .option('-p, --port <port>')
  .action((options) => {
    console.log('Server running on port', options.port);
  });

program.command('build')
  .description('Build project')
  .option('--watch')
  .action((options) => {
    console.log('Building...');
  });
```

### Standalone Executable Subcommands

```js
// Main program
program.command('git hooks', { isDefault: true });

// Subcommand file: commands/git-hook.js
#!/usr/bin/env node
console.log('Running git hook');
```

## Argument Definition

```js
// Required argument
program.argument('<file>', 'Input file');

// Optional argument
program.argument('[file]', 'Input file (optional)');

// Variadic argument
program.argument('<files...>', 'Multiple files');

// Access in action handler
program.command('split')
  .argument('<string>', 'String to split')
  .option('--separator <char>', 'Separator', ',')
  .action((str, options) => {
    console.log(str.split(options.separator));
  });
```

## Help System

### Automatic Help

```bash
node app.js --help
node app.js help command
```

### Custom Help

```js
program.on('option:help', () => {
  console.log('Custom help information');
  program.help();
});

program.addHelpCommand(false); // Disable help subcommand
```

## Global Object Shortcut

For simple scripts, you can use the global object:

```js
const { program } = require('commander');

program
  .name('my-tool')
  .option('-v, --verbose')
  .action(() => {
    console.log(program.opts().verbose ? 'Verbose mode' : 'Normal mode');
  });

program.parse();
```

## TypeScript Support

```ts
import { Command } from 'commander';

const program = new Command();

program
  .name('ts-cli')
  .option('-n, --name <name>', 'Name')
  .action((options) => {
    console.log('Hello', options.name);
  });

program.parse();
```

## Common Configuration

```js
// Configure parsing behavior
program.configureOutput({
  writeErr: (str) => process.stderr.write(str),
  outputWidth: 80,
});

// Enable conflict checks
program.allowUnknownOption();
program.passThroughOptions();

// Lifecycle hooks
program
  .hook('preAction', (thisCommand) => {
    console.log('Pre-action hook');
  })
  .hook('postAction', (thisCommand) => {
    console.log('Post-action hook');
  });
```

## Best Practices

1. **Use a local Command object** (not global) for easier unit testing
2. **Always call program.parse()** to start parsing
3. **Prefer .option() over directly processing process.argv**
4. **Use camelCase option names** for automatic conversion: `--template-engine` → `opts().templateEngine`
5. **Use .description()** to provide clear help information