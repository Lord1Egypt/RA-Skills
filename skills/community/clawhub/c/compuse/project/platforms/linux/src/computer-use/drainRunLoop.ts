import { logDebug } from '../lib/log.js'
import { withResolvers } from '../lib/withResolvers.js'
import { requireComputerUseSwift } from './swiftLoader.js'

let pump: ReturnType<typeof setInterval> | undefined
let pending = 0
const TIMEOUT_MS = 30_000

function retain(): void {
  pending += 1
  if (!pump) {
    pump = setInterval(() => requireComputerUseSwift()._drainMainRunLoop(), 1)
    logDebug('drain run loop started')
  }
}

function release(): void {
  pending -= 1
  if (pending <= 0 && pump) {
    clearInterval(pump)
    pump = undefined
    pending = 0
    logDebug('drain run loop stopped')
  }
}

export const retainPump = retain
export const releasePump = release

export async function drainRunLoop<T>(fn: () => Promise<T>): Promise<T> {
  retain()
  let timer: ReturnType<typeof setTimeout> | undefined
  try {
    const work = fn()
    work.catch(() => {})
    const timeout = withResolvers<never>()
    timer = setTimeout(() => timeout.reject(new Error(`computer-use native call exceeded ${TIMEOUT_MS}ms`)), TIMEOUT_MS)
    return await Promise.race([work, timeout.promise])
  } finally {
    if (timer) clearTimeout(timer)
    release()
  }
}
