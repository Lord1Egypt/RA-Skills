import chalk from 'chalk'
import * as identityStore from '../storage/identity.js'
import { numberToMnemonic, mnemonicToNumber } from '../core/mnemonic.js'

export function cmdBackup() {
  const identity = identityStore.load()
  if (!identity) { console.log(chalk.gray('// not initialized')); return }
  const words = numberToMnemonic(identity.number)
  console.log(chalk.gray('// backup seed phrase'))
  console.log()
  words.split(' ').forEach((w, i) => {
    console.log(`  ${String(i + 1).padStart(2)}. ${chalk.white(w)}`)
  })
  console.log()
  console.log(chalk.gray('// store these 12 words safely'))
}

export function cmdRestore(words) {
  let number
  try {
    number = mnemonicToNumber(words)
  } catch {
    console.log(chalk.gray('// invalid seed phrase'))
    process.exit(1)
  }
  identityStore.save({ number, createdAt: Date.now() })
  console.log(chalk.gray('// number restored'))
  console.log(chalk.gray('number  ') + number)
}
