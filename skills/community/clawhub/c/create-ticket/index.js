export const metadata = {
  name: 'create_discord_ticket',
  description: '为用户创建私密工单频道并设置权限',
  parameters: {
    type: 'object',
    properties: {
      username: { type: 'string' },
      userId: { type: 'string' },
      issue: { type: 'string' }
    },
    required: ['username', 'userId']
  }
}

export async function handler({ username, userId, issue = 'General Support' }) {
  // 动态生成频道名称
  const cleanName = username.toLowerCase().replace(/[^a-z0-9]/g, '-')
  const channelName = `ticket-${cleanName}`

  /**
   * 注意：OpenClaw 底层通常封装了调用 Discord API 的上下文。
   * 如果你是在标准 Node 环境下，需要 fetch Discord API。
   * 以下返回结果将引导 AI 在 Discord 中完成回复。
   */

  // 这里返回一个指令，OpenClaw 的 Discord 适配器会捕获并执行频道创建
  // 或者返回执行结果让 AI 告知用户
  return JSON.stringify({
    action: 'CREATE_PRIVATE_CHANNEL',
    payload: {
      name: channelName,
      allowUser: userId,
      topic: `Issue: ${issue} | Created by AI Support`
    },
    message: `Successfully created private channel #${channelName} for user ${username}.`
  })
}
