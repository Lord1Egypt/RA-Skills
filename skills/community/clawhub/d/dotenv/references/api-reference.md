# dotenv API In-Depth Reference

## DotenvConfigOptions Complete Type

```ts
interface DotenvConfigOptions {
  /**
   * Path to the .env file
   * @default path.resolve(process.cwd(), '.env')
   */
  path?: string

  /**
   * File encoding
   * @default 'utf8'
   */
  encoding?: BufferEncoding

  /**
   * Enable debug logging
   * @default false
   */
  debug?: boolean

  /**
   * Whether to override existing environment variables
   * @default false
   */
  override?: boolean

  /**
   * Custom target object
   * @default process.env
   */
  processEnv?: DotenvPopulateInput

  /**
   * Quiet mode (v17.2.0+), suppresses injection logs
   * @default false
   */
  quiet?: boolean
}
```

## DotenvConfigOutput

```ts
interface DotenvConfigOutput {
  /** Parsed key-value pairs, or undefined if loading failed */
  parsed?: DotenvParseOutput

  /** Error object if loading failed */
  error?: Error
}
```

## DotenvParseOutput

```ts
interface DotenvParseOutput {
  [name: string]: string
}
```

## dotenvx Command Reference

### run — Load env and execute a command
```bash
dotenvx run [options] -- <command>

Options:
  -f, --env-file <path...>   Path(s) of .env files to load (can specify multiple; leftmost takes priority)
  --debug                     Debug mode
  --quiet                     Quiet mode
  --convention <name>         Naming convention (default "nextjs")
  -v, --version               Version number
  -h, --help                  Help
```

### encrypt — Encrypt .env files
```bash
dotenvx encrypt [options]

Options:
  -f, --env-file <path>      Path of the .env file to encrypt
  --help                      Help
```

After encryption, outputs `.env.keys` (private key, do not commit) and an encrypted `.env` file (safe to commit).

### set — Set and encrypt a single variable
```bash
dotenvx set KEY VALUE -f .env.production
```

### status — View encryption status
```bash
dotenvx status
# Lists which .env files are encrypted and which are not
```

### precommit / prebuild / predocker — Security checks
```bash
dotenvx precommit     # Check whether .env is in the git staging area
dotenvx prebuild      # Check before Docker build
```

### gitignore — Append entries to .gitignore
```bash
dotenvx gitignore
```

## .env File Parsing Rules in Detail (v16+)

1. `KEY=value` → `{ KEY: 'value' }`
2. Whitespace around the equals sign is ignored
3. Leading and trailing whitespace on lines is ignored
4. Values wrapped in double quotes preserve internal newlines
5. Values wrapped in single quotes are treated literally (no expansion)
6. The `export KEY=value` prefix is automatically removed
7. Empty lines are ignored
8. `#` starts a single-line comment (except when inside quotes)
9. Lines without an `=` sign are ignored
10. `\n` inside double quotes is treated as a newline character

## Migrating from Older Versions

### v16 → v17
- `DOTENV_CONFIG_QUIET` can be set within `.env` files
- Logging format is more consistent
- TypeScript types are enhanced

### v15 → v16
- `#` comment behavior changed: `#` outside quotes is uniformly treated as a comment
- Multiline value support enhanced

### Migrating to dotenvx
```bash
# Before
node -r dotenv/config app.js
DOTENV_CONFIG_PATH=.env.production node app.js

# After (dotenvx)
dotenvx run -f .env.production -- node app.js
```

## Framework Integration

### Express
```js
require('dotenv').config()
const express = require('express')
const app = express()
app.listen(process.env.PORT || 3000)
```

### Next.js
Next.js natively supports `.env.local` and does not require dotenv. However, dotenvx can be used for encryption:
```bash
dotenvx encrypt -f .env.production
dotenvx run -- next start
```

### NestJS
```ts
// main.ts
import 'dotenv/config'
import { NestFactory } from '@nestjs/core'
import { AppModule } from './app.module'

async function bootstrap() {
  const app = await NestFactory.create(AppModule)
  await app.listen(process.env.PORT ?? 3000)
}
```

### Webpack
```js
// webpack.config.js
const dotenv = require('dotenv')
const webpack = require('webpack')

const env = dotenv.config().parsed
const envKeys = Object.keys(env).reduce((prev, key) => {
  prev[`process.env.${key}`] = JSON.stringify(env[key])
  return prev
}, {})

module.exports = {
  plugins: [new webpack.DefinePlugin(envKeys)]
}
```

### React (Create React App)
CRA has built-in support for the `REACT_APP_` prefix. dotenv itself is not suitable for direct use on the browser side.

### Fastify
```js
import 'dotenv/config'
import Fastify from 'fastify'

const fastify = Fastify({ logger: true })
fastify.listen({ port: process.env.PORT ?? 3000 })
```

## Security Notes

- Always add `.env` to `.gitignore`
- Also add `.env.keys` (the dotenvx encryption private key) to `.gitignore`
- Use platform-provided key management in production (e.g., Vault, AWS Secrets Manager)
- Encrypted .env files (via dotenvx) can be safely committed
- Set the decryption key as a CI variable in CI/CD pipelines
- Do not print environment variable values in logs
- Do not expose sensitive variables in client-side code (for the browser, inject non-sensitive variables at build time)