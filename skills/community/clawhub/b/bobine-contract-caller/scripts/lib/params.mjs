import { hexToBytes } from "./hex.mjs"

function isWhitespace(char) {
  return char === " " || char === "\n" || char === "\t" || char === "\r"
}

function skipWhitespace(state) {
  while (isWhitespace(state.text[state.index])) state.index += 1
}

function expect(state, expected) {
  if (!state.text.startsWith(expected, state.index)) {
    throw new Error(`Expected "${expected}" at position ${state.index}`)
  }

  state.index += expected.length
}

function readUntilDelimiter(state) {
  const start = state.index

  while (state.index < state.text.length) {
    const char = state.text[state.index]
    if (char === "," || char === "]") break
    state.index += 1
  }

  return state.text.slice(start, state.index).trim()
}

function readQuoted(state) {
  const quote = state.text[state.index]
  let value = ""
  state.index += 1

  while (state.index < state.text.length) {
    const char = state.text[state.index]

    if (char === "\\") {
      state.index += 1

      if (state.index >= state.text.length) {
        throw new Error("Unterminated escape sequence in quoted text")
      }

      const escaped = state.text[state.index]
      if (escaped === "n") value += "\n"
      else if (escaped === "r") value += "\r"
      else if (escaped === "t") value += "\t"
      else value += escaped

      state.index += 1
      continue
    }

    if (char === quote) {
      state.index += 1
      return value
    }

    value += char
    state.index += 1
  }

  throw new Error("Unterminated quoted text value")
}

function readTextValue(state) {
  const next = state.text[state.index]

  if (next === '"' || next === "'") {
    return readQuoted(state)
  }

  return readUntilDelimiter(state)
}

function parseArray(state) {
  const values = []
  expect(state, "[")
  skipWhitespace(state)

  if (state.text[state.index] === "]") {
    state.index += 1
    return values
  }

  while (state.index < state.text.length) {
    values.push(parseValue(state))
    skipWhitespace(state)

    const char = state.text[state.index]
    if (char === ",") {
      state.index += 1
      skipWhitespace(state)
      continue
    }

    if (char === "]") {
      state.index += 1
      return values
    }

    throw new Error(`Expected "," or "]" at position ${state.index}`)
  }

  throw new Error("Unterminated packed array")
}

function parseValue(state) {
  skipWhitespace(state)

  if (state.text.startsWith("null", state.index)) {
    state.index += "null".length
    return null
  }

  if (state.text.startsWith("blob:", state.index)) {
    state.index += "blob:".length
    return hexToBytes(readUntilDelimiter(state))
  }

  if (state.text.startsWith("bigint:", state.index)) {
    state.index += "bigint:".length
    return BigInt(readUntilDelimiter(state))
  }

  if (state.text.startsWith("number:", state.index)) {
    state.index += "number:".length
    const value = Number(readUntilDelimiter(state))

    if (!Number.isFinite(value)) throw new Error("Invalid number value")

    return value
  }

  if (state.text.startsWith("text:", state.index)) {
    state.index += "text:".length
    return readTextValue(state)
  }

  if (state.text.startsWith("pack:[", state.index)) {
    state.index += "pack:".length
    return parseArray(state)
  }

  if (state.text.startsWith("array:[", state.index)) {
    state.index += "array:".length
    return parseArray(state)
  }

  throw new Error(`Unknown value type at position ${state.index}`)
}

export function parseParam(text) {
  const state = { text, index: 0 }
  const value = parseValue(state)
  skipWhitespace(state)

  if (state.index !== state.text.length) {
    throw new Error(`Unexpected trailing content at position ${state.index}`)
  }

  return value
}

export function parseParams(texts) {
  return texts.map(parseParam)
}
