import path from 'node:path'
import { fileURLToPath } from 'node:url'

const scriptDir = path.dirname(fileURLToPath(import.meta.url))
const skillRoot = path.resolve(scriptDir, '..')

const platformMap = {
  darwin: 'macos',
  win32: 'windows',
  linux: 'linux',
}

const target = platformMap[process.platform]
if (!target) {
  console.error(`Unsupported platform: ${process.platform}`)
  process.exit(1)
}

console.log(path.join(skillRoot, 'project', 'platforms', target))
