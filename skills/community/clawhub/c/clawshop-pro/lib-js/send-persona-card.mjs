/**
 * 发数字人选择卡片。
 *
 * 登录成功后检测到用户没有数字人时调用。
 * 用户点预设按钮 → handle-button.mjs 处理 → 调 /api/v1/persona/create
 * 用户点“自定义” → 弹 Modal → 提交后同样走 handle-button.mjs
 * 用户点“跳过” → handle-button.mjs 标记跳过，进推荐流程
 */
import * as ct from './card-tools.mjs';

// 预设按钮 label → description 映射
export const PERSONA_PRESETS = {
  '👩 亚洲女': '25岁亚洲女性，长发大眼睛，自然写实风格',
  '👩 欧美女': '25岁欧美女性，金色波浪卷发，写实风格',
  '👩 拉丁裔女': '25岁拉丁裔女性，自然卷发，写实风格',
  '👨 亚洲男': '28岁亚洲男性，短发，干净利落，写实风格',
  '👨 欧美男': '28岁欧美男性，短发，商务风，写实风格',
  '👨 拉丁裔男': '28岁拉丁裔男性，短发，阳光健康，写实风格',
};

export async function send() {
  const text =
    '🎭 **创建你的专属数字人**\n\n' +
    '点击下方按钮选择形象，或点“自定义”输入描述。约 1 分钟生成。';

  const buttonsRow1 = [
    { label: '👩 亚洲女', style: 'primary' },
    { label: '👩 欧美女', style: 'primary' },
    { label: '👩 拉丁裔女', style: 'primary' },
  ];
  const buttonsRow2 = [
    { label: '👨 亚洲男', style: 'primary' },
    { label: '👨 欧美男', style: 'primary' },
    { label: '👨 拉丁裔男', style: 'primary' },
  ];
  const buttonsRow3 = [
    { label: '📝 自定义', style: 'secondary' },
    { label: '⏭️ 跳过', style: 'secondary' },
  ];

  const { channel, target } = ct.detectChannel();

  // 统一 presentation 格式（分行排列）
  const mapBtns = row => row.map(b => ({
    label: b.label,
    value: b.label,
    style: b.style === 'primary' ? 'primary' : 'secondary',
  }));

  const args = {
    action: 'send',
    channel,
    message: text,
    presentation: {
      blocks: [
        { type: 'text', text },
        { type: 'buttons', buttons: mapBtns(buttonsRow1) },
        { type: 'buttons', buttons: mapBtns(buttonsRow2) },
        { type: 'buttons', buttons: mapBtns(buttonsRow3) },
      ],
    },
  };
  if (target) args.target = target;

  // Discord 增强：多行按钮（兼容所有版本，不用 modal）
  if (channel === 'discord') {
    args.components = {
      flags: 32768,
      reusable: true,
      blocks: [
        { type: 'actions', buttons: buttonsRow1.map(b => ({ ...b, allowedUsers: ['*'] })) },
        { type: 'actions', buttons: buttonsRow2.map(b => ({ ...b, allowedUsers: ['*'] })) },
        { type: 'actions', buttons: buttonsRow3.map(b => ({ ...b, allowedUsers: ['*'] })) },
      ],
    };
  }

  const payload = { tool: 'message', args };

  try {
    const r = await fetch(ct.GATEWAY_URL, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${ct._gatewayToken()}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(60000),
    });
    if (!r.ok) throw new Error(`gateway ${r.status}`);
    const d = await r.json();
    const msgId = d?.result?.details?.result?.messageId || null;
    return { ok: true, messageId: msgId };
  } catch {
    return { ok: false, messageId: null };
  }
}

// CLI 入口
if (process.argv[1] && process.argv[1].includes('send-persona-card.mjs')) {
  send().then(r => console.log(JSON.stringify(r))).catch(e => { console.error(e); process.exit(1); });
}
