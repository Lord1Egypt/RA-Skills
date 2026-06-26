// Android → CLI の受信テスト
// Android の番号とPINで Server としてリッスン
import { channelSecret } from './src/core/channel.js'
import Hyperswarm from 'hyperswarm'

const topic = channelSecret('0x0-215-5028-5446', '48b3a2')
console.log('// listening for messages from Android...')
console.log('// topic:', topic.toString('hex').slice(0, 16) + '...')
console.log('// Android で何かメッセージを送ってみて')

const swarm = new Hyperswarm()
swarm.join(topic, { server: true, client: true })

swarm.on('connection', (conn) => {
  console.log('[connected from peer]')
  conn.on('error', () => {})
  conn.on('data', (data) => {
    try {
      const msg = JSON.parse(data.toString())
      if (msg.type === 'message') {
        console.log('[received]', msg.content)
      } else {
        console.log('[data type]', msg.type)
      }
    } catch (e) {
      console.log('[raw data]', data.toString().slice(0, 100))
    }
  })
  conn.on('close', () => console.log('[disconnected]'))
})

setTimeout(async () => {
  console.log('// timeout 90s')
  await swarm.destroy()
  process.exit(0)
}, 90000)
