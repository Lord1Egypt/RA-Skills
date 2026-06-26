---
name: dotenv
description: Use dotenv to manage environment variables for Node.js projects.
---

# dotenv — Node.js Environment Variable Loader

dotenv is a zero-dependency module that loads environment variables from a `.env` file into `process.env`.

## Use Cases

Use when users need to load .env files, configure environment variables, handle API keys and sensitive configuration, set up multi-environment variables, or use dotenv/dotenvx.
Trigger words include "dotenv," "environment variables," "env file," "dotenvx," "process.env," "encrypted env," etc.

## Installation

```bash
npm install dotenv
# or
bun add dotenv
yarn add dotenv
pnpm add dotenv
```

## Basic Usage

### Create a `.env` file

```ini
# .env
HELLO="World"
OPENAI_API_KEY="sk-your-key-here"
DATABASE_URL="postgres://localhost/mydb"
PORT=3000
DEBUG=true
```

### Load into your application

```js
// CommonJS — call at the top of your entry file as early as possible
require('dotenv').config()

console.log(process.env.HELLO)       // "World"
console.log(process.env.OPENAI_API_KEY)
```

```js
// ES Module
import 'dotenv/config'

// Or when custom configuration is needed:
import dotenv from 'dotenv'
dotenv.config({ path: '/custom/path/to/.env' })
```

```
$ node index.js
◇ injected env (4) from .env
```

### `.gitignore` Security

**Never** commit `.env` to version control:

```gitignore
# .gitignore
.env
.env.local
.env.*.local
```

Commit a `.env.example` template file (without real keys) for team members' reference.

## `config()` Options

```js
dotenv.config({
  path: '/custom/path/to/.env',     // Default: path.resolve(process.cwd(), '.env')
  encoding: 'utf8',                  // File encoding, default utf8
  debug: true,                       // Enable debug logging
  override: false,                   // Whether to override existing process.env values
  processEnv: {},                    // Custom target object (default process.env)
  quiet: false,                      // v17.2+ quiet mode
})
```

Return value:
```js
const result = dotenv.config()
// result.parsed → { HELLO: 'World', PORT: '3000' }
// result.error  → Error or undefined
```

### Environment Variable Configuration (DOTENV_CONFIG_*)

Config options can be overridden via environment variables (CLI arguments take higher priority):

```bash
DOTENV_CONFIG_PATH=/custom/path/.env \
DOTENV_CONFIG_DEBUG=true \
DOTENV_CONFIG_QUIET=true \
node index.js
```

Or within the `.env` file itself:
```ini
DOTENV_CONFIG_QUIET=true
HELLO="World"
```

## `parse()` — Manual Parsing

```js
const dotenv = require('dotenv')

const buf = Buffer.from('HELLO=world\nPORT=3000')
const config = dotenv.parse(buf)
// { HELLO: 'world', PORT: '3000' }
```

## Preload

Load without requiring dotenv in your code by preloading via the command line:

```bash
node -r dotenv/config your_script.js
node -r dotenv/config your_script.js dotenv_config_path=/custom/path/.env
```

## .env File Format Details

### Basic Format
```ini
KEY=value
KEY2="value with spaces"
KEY3='single quoted value'
```

### Comments
```ini
# This is a comment
SECRET_KEY=abc123  # End-of-line comment
HASH="value-with-#-in-it"  # Values containing # must be wrapped in quotes
```

### Multiline Values (v15.0.0+)
```ini
PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
Line1
Line2
-----END RSA PRIVATE KEY-----"

# Or use \n
PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\nLine1\nLine2\n-----END RSA PRIVATE KEY-----"
```

## TypeScript

```ts
import dotenv from 'dotenv'
dotenv.config()

// Or
import 'dotenv/config'

// Declare type augmentation
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      OPENAI_API_KEY: string
      DATABASE_URL: string
    }
  }
}
```

## dotenvx — Advanced Features

dotenvx is an upgraded CLI tool for dotenv that provides advanced features such as encryption, variable expansion, and multi-environment management.

### Installation
```bash
npm install -g @dotenvx/dotenvx
# or
brew install dotenvx
# or
curl -fsS https://dotenvx.sh/ | sh
```

### Variable Expansion
```ini
# .env
USERNAME="admin"
DATABASE_URL="postgres://${USERNAME}@localhost/mydb"
```
```bash
dotenvx run -- node index.js
```

### Command Substitution
```ini
DATABASE_URL="postgres://$(whoami)@localhost/mydb"
```

### Multi-Environment Management
```bash
# .env.production
echo "HELLO=production" > .env.production

# Load a specific environment
dotenvx run -f=.env.production -- node index.js

# Load multiple files (leftmost takes higher priority)
dotenvx run -f=.env.local -f=.env -- node index.js
```

### Encryption (Safe to Commit to Git)
```bash
# Encrypt the .env file
dotenvx encrypt -f .env.production

# Generate .env.keys (contains the decryption key) → add to .gitignore
# The encrypted .env.production can now be safely committed

# Set the decryption key during deployment
heroku config:set DOTENV_PRIVATE_KEY_PRODUCTION="<key from .env.keys>"

# Automatic decryption at runtime
dotenvx run -- node index.js
```

### Use Case Comparison

| Requirement | Tool |
|---|---|
| Load `.env` into `process.env` | dotenv |
| Encrypt env + safe git commit | dotenvx encrypt |
| Variable expansion `${VAR}` | dotenvx run |
| Command substitution `$(cmd)` | dotenvx run |
| Multi-environment switching | dotenvx run -f=.env.ENV |
| Production deployment decryption | dotenvx + DOTENV_PRIVATE_KEY |

## Common Patterns and Best Practices

### Application Entry Loading
```js
// app.js — First line
require('dotenv').config()

const express = require('express')
const app = express()
// All subsequent modules can read values via process.env
```

### Loading with Validation
```js
const dotenv = require('dotenv')
dotenv.config()

const required = ['DATABASE_URL', 'SECRET_KEY']
for (const key of required) {
  if (!process.env[key]) {
    throw new Error(`Missing required env var: ${key}`)
  }
}
```

### Monorepo Scenario
```
apps/backend/
├── .env          ← Place in the app's runtime directory
├── app.js
└── package.json
```

### Multi-Environment File Recommendations
- `.env` — Local development (default)
- `.env.production` — Production environment
- `.env.test` — Testing environment
- `.env.example` — Template (commit to git, without real values)

**Do not** let `.env.production` inherit values from `.env` — each environment file should be independently complete.

### Logging Control

```bash
# Suppress injection logs
DOTENV_CONFIG_QUIET=true node index.js
```

## Troubleshooting

| Issue | Solution |
|---|---|
| env variable is `undefined` | Ensure `dotenv.config()` is called at the earliest point; check that `.env` is in the correct directory |
| Changes to `.env` not taking effect | Restart the process (the `require` cache does not auto-reload) |
| Multiline value parsing errors | Ensure dotenv >= v15.0.0 |
| env not loaded in Docker | Ensure `.env` is COPY'd into the container and the path is correct |
| `#` truncated in values | Wrap values containing `#` in quotes |