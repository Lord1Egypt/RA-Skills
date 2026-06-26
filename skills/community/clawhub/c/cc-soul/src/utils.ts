/**
 * utils.ts — Shared utility functions
 */

/**
 * Robust JSON extraction from LLM output.
 * Handles markdown fences, trailing text, nested objects.
 */
export function extractJSON(output: string): any | null {
  let text = output.replace(/```(?:json)?\s*\n?([\s\S]*?)\n?\s*```/g, '$1').trim()
  const objStart = text.indexOf('{')
  const arrStart = text.indexOf('[')
  // Pick whichever comes first: { or [
  const start = objStart === -1 ? arrStart : arrStart === -1 ? objStart : Math.min(objStart, arrStart)
  if (start === -1) return null

  const openChar = text[start]
  const closeChar = openChar === '{' ? '}' : ']'

  let depth = 0
  let inString = false
  let escape = false

  for (let i = start; i < text.length; i++) {
    const ch = text[i]
    if (escape) { escape = false; continue }
    if (ch === '\\' && inString) { escape = true; continue }
    if (ch === '"' && !escape) { inString = !inString; continue }
    if (inString) continue
    if (ch === openChar) depth++
    else if (ch === closeChar) {
      depth--
      if (depth === 0) {
        try { return JSON.parse(text.slice(start, i + 1)) } catch { continue }
      }
    }
  }
  return null
}
