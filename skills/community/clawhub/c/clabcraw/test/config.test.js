/**
 * Tests for skill config consistency.
 *
 * Ensures the production contract address is kept in sync across:
 *   - skill/skill.json  (env default loaded by env.js)
 *   - skill/lib/game.js (hardcoded fallback in claim())
 */

import { test } from "node:test"
import assert from "node:assert/strict"
import { readFileSync } from "node:fs"
import { fileURLToPath } from "node:url"
import { dirname, join } from "node:path"

const __dirname = dirname(fileURLToPath(import.meta.url))
const ROOT = join(__dirname, "..")

const PROD_CONTRACT = "0xafffcEAD2e99D04e5641A2873Eb7347828e1AAd3"

test("skill.json CLABCRAW_CONTRACT_ADDRESS matches production contract", () => {
  const skillJson = JSON.parse(readFileSync(join(ROOT, "skill.json"), "utf-8"))
  assert.equal(
    skillJson.env.CLABCRAW_CONTRACT_ADDRESS,
    PROD_CONTRACT,
    `skill.json contract address should be ${PROD_CONTRACT}`,
  )
})

test("game.js hardcoded fallback contract address matches production contract", () => {
  const gameJs = readFileSync(join(ROOT, "lib", "game.js"), "utf-8")
  // Match the fallback string: config.contractAddress || "0x..."
  const match = gameJs.match(/config\.contractAddress\s*\|\|\s*"(0x[0-9a-fA-F]+)"/)
  assert.ok(match, "game.js should have a hardcoded fallback contract address")
  assert.equal(
    match[1],
    PROD_CONTRACT,
    `game.js fallback contract address should be ${PROD_CONTRACT}`,
  )
})

test("skill.json and game.js fallback contract address are identical", () => {
  const skillJson = JSON.parse(readFileSync(join(ROOT, "skill.json"), "utf-8"))
  const gameJs = readFileSync(join(ROOT, "lib", "game.js"), "utf-8")
  const match = gameJs.match(/config\.contractAddress\s*\|\|\s*"(0x[0-9a-fA-F]+)"/)
  assert.ok(match, "game.js should have a hardcoded fallback contract address")
  assert.equal(
    skillJson.env.CLABCRAW_CONTRACT_ADDRESS,
    match[1],
    "skill.json and game.js fallback must reference the same contract address",
  )
})
