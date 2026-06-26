/**
 * soul-reply.ts — Soul mode reply (灵魂模式)
 *
 * Handles POST /soul — generates a reply AS the user (not imitating, being).
 * Requires LLM configuration.
 */

async function handleSoul(body: any): Promise<any> {
  const message = body.message || ''
  const userId = body.user_id || body.userId || 'default'
  const speakerHint = body.speaker || ''

  if (!message) return { error: 'message is required' }

  const { generateAvatarReply, loadAvatarProfile } = await import('./avatar.ts')
  const { spawnCLI } = await import('./cli.ts')

  // Auto-detect speaker
  let speaker = speakerHint
  if (!speaker) {
    const profile = loadAvatarProfile(userId)
    const contacts = Object.entries(profile.social || {})
      .map(([name, c]: [string, any]) => `${name}（${c.relation}）`)
    if (contacts.length > 0) {
      speaker = await new Promise<string>((resolve) => {
        spawnCLI(
          `已知关系：${contacts.join('、')}\n消息："${message.slice(0, 100)}"\n最可能是谁发的？只回答名字，无法判断回答"未知"。`,
          (output) => {
            const name = (output || '').trim().replace(/["""。.，,\s]/g, '')
            if (profile.social[name]) { resolve(name); return }
            for (const known of Object.keys(profile.social)) {
              if ((output || '').includes(known)) { resolve(known); return }
            }
            resolve('')
          }, 10000
        )
      })
    }
  }

  const reply = await new Promise<string>((resolve) => {
    generateAvatarReply(userId, speaker || '未知', message, (r: string, refused?: boolean) => {
      resolve(refused ? '' : r)
    })
  })

  return { reply, speaker: speaker || '未知' }
}
