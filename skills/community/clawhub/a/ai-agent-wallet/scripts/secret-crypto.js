const crypto = require('node:crypto')

const ALGORITHM = 'aes-256-gcm'

function encryptSecret(secretValue) {
  const value = String(secretValue || '')
  if (!value) {
    throw new Error('Cannot encrypt an empty secret value.')
  }

  const key = resolveKey()
  const iv = crypto.randomBytes(12)
  const cipher = crypto.createCipheriv(ALGORITHM, key, iv)
  const ciphertext = Buffer.concat([cipher.update(value, 'utf8'), cipher.final()])
  const tag = cipher.getAuthTag()
  return `${iv.toString('hex')}:${tag.toString('hex')}:${ciphertext.toString('hex')}`
}

function decryptSecret(payload) {
  const raw = String(payload || '')
  const [ivHex, tagHex, ciphertextHex] = raw.split(':')
  if (!ivHex || !tagHex || !ciphertextHex) {
    throw new Error('Encrypted secret payload is malformed.')
  }

  const key = resolveKey()
  const decipher = crypto.createDecipheriv(
    ALGORITHM,
    key,
    Buffer.from(ivHex, 'hex')
  )
  decipher.setAuthTag(Buffer.from(tagHex, 'hex'))
  const plaintext = Buffer.concat([
    decipher.update(Buffer.from(ciphertextHex, 'hex')),
    decipher.final(),
  ])
  return plaintext.toString('utf8')
}

function resolveKey() {
  const material = process.env.WALLET_SECRET_KEY
  if (!material) {
    throw new Error('Missing WALLET_SECRET_KEY. Set it before running wallet scripts.')
  }
  return crypto.createHash('sha256').update(material, 'utf8').digest()
}

module.exports = {
  encryptSecret,
  decryptSecret,
}
