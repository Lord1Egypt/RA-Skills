/**
 * validate.ts — 轻量 API 入参验证（零依赖，替代 Zod）
 */

type Rule = {
  required?: boolean
  type?: 'string' | 'number' | 'boolean' | 'object'
  min?: number      // string: min length; number: min value
  max?: number
  enum?: string[]   // allowed values
}

type Schema = Record<string, Rule>

interface ValidateOk { ok: true; data: Record<string, any> }
interface ValidateFail { ok: false; error: string }
type ValidateResult = ValidateOk | ValidateFail

export function validate(body: any, schema: Schema): ValidateResult {
  if (!body || typeof body !== 'object') {
    return { ok: false, error: 'request body must be a JSON object' }
  }

  const data: Record<string, any> = {}
  for (const [key, rule] of Object.entries(schema)) {
    const val = body[key]

    if (rule.required && (val === undefined || val === null || val === '')) {
      return { ok: false, error: `"${key}" is required` }
    }

    if (val === undefined || val === null) continue

    if (rule.type && typeof val !== rule.type) {
      return { ok: false, error: `"${key}" must be ${rule.type}, got ${typeof val}` }
    }

    if (rule.type === 'string') {
      if (rule.min !== undefined && val.length < rule.min) {
        return { ok: false, error: `"${key}" must be at least ${rule.min} characters` }
      }
      if (rule.max !== undefined && val.length > rule.max) {
        return { ok: false, error: `"${key}" must be at most ${rule.max} characters` }
      }
    }

    if (rule.type === 'number') {
      if (rule.min !== undefined && val < rule.min) {
        return { ok: false, error: `"${key}" must be >= ${rule.min}` }
      }
      if (rule.max !== undefined && val > rule.max) {
        return { ok: false, error: `"${key}" must be <= ${rule.max}` }
      }
    }

    if (rule.enum && !rule.enum.includes(val)) {
      return { ok: false, error: `"${key}" must be one of: ${rule.enum.join(', ')}` }
    }

    data[key] = val
  }

  // Pass through unlisted fields（不阻止额外字段，只验证 schema 里的）
  for (const key of Object.keys(body)) {
    if (!(key in schema)) data[key] = body[key]
  }

  return { ok: true, data }
}

