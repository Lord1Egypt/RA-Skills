export function errorMessage(error: unknown): string {
  if (error instanceof Error) return error.message
  return String(error)
}

export function getErrnoCode(error: unknown): string | undefined {
  if (typeof error === 'object' && error !== null && 'code' in error) {
    const code = (error as { code?: unknown }).code
    return typeof code === 'string' ? code : undefined
  }
  return undefined
}
