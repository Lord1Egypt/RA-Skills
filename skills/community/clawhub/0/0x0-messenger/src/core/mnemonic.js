import * as bip39 from 'bip39'

export function numberToMnemonic(number) {
  // "0x0-012-3456-7890" → "01234567890"
  const digits = number.replace(/^0x0-/, '').replaceAll('-', '')
  const n = BigInt(digits)
  // 16バイト (128bit) にゼロパディング
  const buf = Buffer.alloc(16)
  const hex = n.toString(16).padStart(32, '0')
  buf.write(hex, 'hex')
  return bip39.entropyToMnemonic(buf.toString('hex'))
}

export function mnemonicToNumber(words) {
  const entropy = bip39.mnemonicToEntropy(words)
  const n = BigInt('0x' + entropy)
  const digits = n.toString().padStart(11, '0')
  return `0x0-${digits.slice(0, 3)}-${digits.slice(3, 7)}-${digits.slice(7)}`
}
