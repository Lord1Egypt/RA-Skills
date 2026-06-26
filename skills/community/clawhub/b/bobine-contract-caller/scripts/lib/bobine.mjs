import { createHash, createPrivateKey, sign } from "node:crypto"

import { generateSpark } from "./effort.mjs"
import { bytesToHex, hexToBytes } from "./hex.mjs"
import { jsonify, pack, unpack } from "./packed.mjs"

const DEFAULT_SPARK_EFFORT = 1048576n

function loadServer(server) {
  if (!server) throw new Error("Missing required server argument")
  return server
}

async function loadSpark({ sparkHex, sparkEffort }) {
  const predefined = sparkHex
  if (predefined) {
    return { sparkHex: predefined, sparkBytes: hexToBytes(predefined) }
  }

  const effortRaw = sparkEffort ?? DEFAULT_SPARK_EFFORT.toString()
  const target = BigInt(effortRaw)
  const sparkBytes = await generateSpark(target)

  return { sparkHex: bytesToHex(sparkBytes), sparkBytes }
}

async function decodeError(response) {
  try {
    return await response.text()
  } catch {
    return "<unreadable response body>"
  }
}

export async function execute(module, method, params, options = {}) {
  const server = loadServer(options.server)
  const { sparkHex, sparkBytes } = await loadSpark(options)

  const body = new FormData()
  body.append("module", module)
  body.append("method", method)
  body.append("params", new Blob([Buffer.from(pack(params))]))
  body.append("effort", new Blob([Buffer.from(sparkBytes)]))

  const response = await fetch(new URL("/api/execute", server), {
    method: "POST",
    body,
  })

  if (!response.ok) {
    const details = await decodeError(response)
    throw new Error(
      `Failed Bobine execute request (${response.status} ${response.statusText}): ${details}`,
    )
  }

  const proofBytes = new Uint8Array(await response.arrayBuffer())
  const proof = unpack(proofBytes)

  if (!Array.isArray(proof) || proof.length < 5) {
    throw new Error("Unexpected Bobine proof payload")
  }

  const [logs, _reads, _writes, returned, reportedSparks] = proof

  if (!Array.isArray(logs) || typeof reportedSparks !== "bigint") {
    throw new Error("Unexpected Bobine proof tuple shape")
  }

  return {
    logs: logs.map((log) => {
      if (typeof log !== "string")
        throw new Error("Unexpected non-string log entry")

      return log
    }),
    returned: jsonify(returned),
    sparkHex,
    reportedSparks: reportedSparks.toString(),
  }
}

export function deriveSessionAddress(authModule, publicKeyHex) {
  const sessionBytes = pack([authModule, hexToBytes(publicKeyHex)])
  const digest = createHash("sha256").update(Buffer.from(sessionBytes)).digest()
  return bytesToHex(new Uint8Array(digest))
}

function importEd25519PrivateKey(privateKeyHex) {
  return createPrivateKey({
    key: Buffer.from(hexToBytes(privateKeyHex)),
    format: "der",
    type: "pkcs8",
  })
}

export async function signEd25519Call(
  authModule,
  targetModule,
  method,
  params,
  privateKeyHex,
  publicKeyHex,
  options = {},
) {
  const privateKey = importEd25519PrivateKey(privateKeyHex)
  const publicKey = hexToBytes(publicKeyHex)

  const sessionAddress = deriveSessionAddress(authModule, publicKeyHex)
  const nonceResult = await execute(
    authModule,
    "get_nonce",
    [sessionAddress],
    options,
  )

  if (nonceResult.returned.type !== "bigint") {
    throw new Error("Auth module get_nonce did not return a bigint")
  }

  const nonce = BigInt(nonceResult.returned.value)
  const message = pack([
    "17fa1cb5-c5af-4cfd-9bea-1a36590b890d",
    targetModule,
    method,
    params,
    nonce,
  ])

  const signature = new Uint8Array(sign(null, Buffer.from(message), privateKey))

  return await execute(
    authModule,
    "call",
    [targetModule, method, params, publicKey, signature],
    options,
  )
}
