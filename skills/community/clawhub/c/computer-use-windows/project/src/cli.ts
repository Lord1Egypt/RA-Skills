#!/usr/bin/env node
import { runServer } from './server.js'
import { errorMessage } from './lib/errors.js'

try {
  await runServer()
} catch (error) {
  process.stderr.write(`windows-computer-use-skill failed: ${errorMessage(error)}\n`)
  process.exit(1)
}
