import { channelSecret } from './src/core/channel.js'
import Hyperswarm from 'hyperswarm'

const topic = channelSecret('0x0-215-5028-5446', '48b3a2')
console.log('topic hex:', topic.toString('hex'))
console.log('connecting as client, waiting 90s...')

const swarm = new Hyperswarm()
swarm.join(topic, { server: false, client: true })

let connected = false

swarm.on('connection', (conn) => {
  connected = true
  conn.on('error', () => {})
  console.log('[CONNECTED at', new Date().toISOString(), ']')
  conn.on('data', (d) => console.log('data:', d.toString()))
  conn.on('close', () => console.log('closed'))
})

let elapsed = 0
const interval = setInterval(() => {
  elapsed += 5
  if (!connected) console.log(`...waiting ${elapsed}s`)
}, 5000)

setTimeout(async () => {
  clearInterval(interval)
  if (!connected) console.log('TIMEOUT: no connection after 90s')
  await swarm.destroy()
  process.exit(0)
}, 90000)
