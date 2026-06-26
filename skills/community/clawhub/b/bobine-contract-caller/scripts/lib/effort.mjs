import { createHash, randomBytes } from "node:crypto"

export async function generateSpark(target) {
  const targetBig = BigInt(target)
  const max = 2n ** 256n

  while (true) {
    const effort = new Uint8Array(randomBytes(32))
    const hash = createHash("sha256").update(effort).digest("hex")
    const hashInt = BigInt(`0x${hash}`)

    if (hashInt === 0n) continue

    const value = max / hashInt
    if (value < targetBig) continue

    return effort
  }
}
