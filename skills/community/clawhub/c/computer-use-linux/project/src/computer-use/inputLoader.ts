import { createRequire } from 'node:module'

const require = createRequire(import.meta.url)
let cached: any

export function requireComputerUseInput(): any {
  if (cached) return cached
  throw new Error(
    'Legacy native input loader was retained only for source-history reference. ' +
    'The standalone runtime now uses the Python bridge in src/computer-use/pythonBridge.ts instead.',
  )
}
