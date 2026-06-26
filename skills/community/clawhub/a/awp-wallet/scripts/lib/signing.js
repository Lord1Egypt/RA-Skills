import { loadSigner } from "./keystore.js"

export async function signMessage(message) {
  const { account } = loadSigner()
  return { signature: await account.signMessage({ message }), signer: account.address }
}

export async function signTypedData(typedData) {
  const { account } = loadSigner()
  return { signature: await account.signTypedData(typedData), signer: account.address }
}
