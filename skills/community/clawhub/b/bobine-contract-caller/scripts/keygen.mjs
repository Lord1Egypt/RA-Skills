import { generateKeyPairSync } from "node:crypto"

import { bytesToHex } from "./lib/hex.mjs"

const { privateKey, publicKey } = generateKeyPairSync("ed25519")

const privateDer = privateKey.export({ format: "der", type: "pkcs8" })
const publicDer = publicKey.export({ format: "der", type: "spki" })

console.log(
  JSON.stringify(
    {
      sigkey: bytesToHex(new Uint8Array(privateDer)),
      pubkey: bytesToHex(new Uint8Array(publicDer)),
    },
    null,
    2,
  ),
)
