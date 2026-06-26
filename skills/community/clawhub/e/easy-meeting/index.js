require('dotenv').config();
const express = require('express');
const crypto = require('crypto');
const FeishuService = require('./feishuService');
const BitableStore = require('./bitableStore');

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

const feishu = new FeishuService(
  process.env.FEISHU_APP_ID,
  process.env.FEISHU_APP_SECRET
);

// 使用飞书多维表格存储（传入 feishuService 实例共享 token）
const dbStore = new BitableStore(feishu);

// 启动时清理过期的孤儿表格
dbStore.cleanupExpiredSessions().catch(err =>
  console.error('[Startup] Failed to cleanup expired sessions:', err)
);

/**
 * =========================================================
 * 供 OpenClaw Agent 调用的三组原子化 Skill 接口
 * =========================================================
 */

/**
 * 技能一：日历排期计算器
 * Agent 提取出人名单和期望时间段后，调用此接口索要 3 个左右空闲时间解
 */
app.post('/api/claw/calc-free-time', async (req, res) => {
  const { userIds, startTimeIso, endTimeIso, durationMinutes } = req.body;

  // 参数验证
  if (!userIds || !Array.isArray(userIds) || userIds.length === 0) {
    return res.status(400).json({ error: 'userIds 必须是非空数组' });
  }
  if (!startTimeIso || !endTimeIso || !durationMinutes) {
    return res.status(400).json({ error: '缺少 startTimeIso / endTimeIso / durationMinutes' });
  }
  if (typeof durationMinutes !== 'number' || durationMinutes <= 0) {
    return res.status(400).json({ error: 'durationMinutes 必须是正整数' });
  }

  try {
    const timeOptions = await feishu.getCommonFreeTime(userIds, startTimeIso, endTimeIso, durationMinutes);
    res.json({
      success: true,
      message: timeOptions.length > 0 ? '找到了以下空闲时段' : '在给定时间内所有人无符合要求的共同空闲时段',
      data: { options: timeOptions }
    });
  } catch (error) {
    console.error('[API Error] calc-free-time:', error);
    res.status(500).json({ error: error.message });
  }
});

/**
 * 技能二：状态发包与意向收集单
 * Agent 利用第一步的结果自己生成了拟人化的话术，再调用此接口下发确认卡片，并开启一个 Session 挂起任务
 */
app.post('/api/claw/dispatch-cards', async (req, res) => {
  const { meetingTopic, userIds, timeSlots, agentMessage } = req.body;

  if (!meetingTopic || typeof meetingTopic !== 'string') {
    return res.status(400).json({ error: 'meetingTopic 不能为空' });
  }
  if (!userIds || !Array.isArray(userIds) || userIds.length === 0) {
    return res.status(400).json({ error: 'userIds 必须是非空数组' });
  }
  if (!timeSlots || !Array.isArray(timeSlots) || timeSlots.length === 0) {
    return res.status(400).json({ error: 'timeSlots 必须是非空数组' });
  }
  if (!agentMessage || typeof agentMessage !== 'string') {
    return res.status(400).json({ error: 'agentMessage 不能为空' });
  }

  try {
    // 1. 使用 crypto 生成安全的唯一事务 ID
    const sessionId = 'ses_' + crypto.randomBytes(12).toString('hex');

    // 2. 多维表格存储事务状态（必须 await，确保建表完成后再发卡片）
    await dbStore.createSession(sessionId, {
      meetingTopic,
      userIds,
      timeSlots,
      agentMessage
    });

    // 3. 将包含 session_id 的独立带按钮卡片派给这几个人
    await feishu.sendPollCards(userIds, sessionId, meetingTopic, agentMessage, timeSlots);

    res.json({
      success: true,
      message: `已向 ${userIds.length} 人的飞书发送了排期卡片。此任务已建档挂起等待用户响应。`,
      data: { sessionId }
    });
  } catch (error) {
    console.error('[API Error] dispatch-cards:', error);
    res.status(500).json({ error: error.message });
  }
});

/**
 * 校验飞书 Webhook 签名的工具函数
 * @returns {boolean} true: 校验通过; false: 校验失败
 */
function verifyFeishuSignature(req) {
  const timestamp = req.headers['x-lark-request-timestamp'];
  const nonce = req.headers['x-lark-request-nonce'];
  const signature = req.headers['x-lark-signature'];
  const encryptKey = process.env.FEISHU_ENCRYPT_KEY;

  // 如果未配置加密密钥，记录警告并返回 false
  if (!encryptKey) {
    console.warn('[Security] FEISHU_ENCRYPT_KEY 未配置，无法进行签名校验');
    return false;
  }

  if (!timestamp || !nonce || !signature) {
    console.warn('[Security] 缺少签名相关 headers');
    return false;
  }

  const body = JSON.stringify(req.body);
  const content = timestamp + nonce + encryptKey + body;
  const hash = crypto.createHash('sha256').update(content).digest('hex');
  return hash === signature;
}

/**
 * 安全校验：校验 URL 是否合法，防止 SSRF
 */
function isSafeUrl(url) {
  if (!url) return false;
  try {
    const parsed = new URL(url);

    // 检查协议
    if (!['http:', 'https:'].includes(parsed.protocol)) {
      return false;
    }

    // 检查域名白名单（如果配置了）
    const allowedDomains = process.env.ALLOWED_WAKE_DOMAINS;
    if (allowedDomains) {
      const domains = allowedDomains.split(',').map(d => d.trim());
      const isAllowed = domains.some(domain =>
        parsed.hostname === domain || parsed.hostname.endsWith('.' + domain)
      );
      if (!isAllowed) {
        console.warn(`[Security] 域名 ${parsed.hostname} 不在白名单中`);
        return false;
      }
    }

    // 防止内网地址
    const hostname = parsed.hostname.toLowerCase();
    const privatePatterns = [
      /^localhost$/i,
      /^127\./,
      /^10\./,
      /^172\.(1[6-9]|2[0-9]|3[01])\./,
      /^192\.168\./,
      /^169\.254\./,
      /^::1$/,
      /^fe80:/i
    ];

    if (privatePatterns.some(pattern => pattern.test(hostname))) {
      console.warn(`[Security] 检测到内网地址: ${hostname}`);
      return false;
    }

    return true;
  } catch (e) {
    console.error('[Security] URL 解析失败:', e.message);
    return false;
  }
}

/**
 * =========================================================
 * 飞书卡片 Webhook，用于接管用户点击与后续决策
 * =========================================================
 */
app.post('/api/feishu/card-webhook', async (req, res) => {
  // 飞书后台 URL 验证请求，必须在签名校验之前处理（此请求不带签名）
  if (req.body.type === 'url_verification') {
    const token = process.env.FEISHU_VERIFICATION_TOKEN;
    if (token && req.body.token !== token) {
      return res.status(403).send('Forbidden: Token Mismatch');
    }
    return res.json({ challenge: req.body.challenge });
  }

  // 安全校验：优先使用 HMAC 签名，未配置时降级到 Verification Token
  const encryptKey = process.env.FEISHU_ENCRYPT_KEY;
  if (encryptKey) {
    if (!verifyFeishuSignature(req)) {
      console.error('[Security] HMAC Signature Match Failed');
      return res.status(403).send('Forbidden: Invalid Signature');
    }
  } else {
    // 降级回 Verification Token
    console.warn('[Security Warning] FEISHU_ENCRYPT_KEY 未配置，降级为 Token 校验，强烈建议配置加密密钥。');
    if (!process.env.FEISHU_VERIFICATION_TOKEN || req.body.token !== process.env.FEISHU_VERIFICATION_TOKEN) {
      console.error('[Security] Verification Token Missing or Mismatch');
      return res.status(403).send('Forbidden: Security Token Mismatch');
    }
  }

  const actionObj = req.body.action;
  
  // 处理投递按钮点击逻辑
  if (actionObj && actionObj.value && actionObj.value.action === 'vote') {
    const { session_id, choice } = actionObj.value;
    const operatorId = req.body.open_id;

    console.log(`[Webhook] Session ${session_id} - User ${operatorId} clicked: ${choice}`);

    // 1. 更新此人的意向
    await dbStore.updateParticipantState(session_id, operatorId, choice);

    // 2. 检查会话当前的共识状态
    const status = await dbStore.checkSessionConsensus(session_id);

    // 回复给点击用户的局部视图 Toast 提示
    let toastMsg = '收到意向！请等待其他人反馈~';

    if (status.done) {
      if (status.result === 'agreed') {
        // ========== 全员同意，执行最终定档 ==========
        toastMsg = '你是最后一个确认者！全员意见统一，我正在执行系统排期...';

        const agreedSlot = JSON.parse(status.time);
        const sessionStore = await dbStore.getSession(session_id);

        // 异步执行：创会、向所有人发日程邀请，全部完成后再删除多维表格
        feishu.createMeeting(
          sessionStore.userIds,
          sessionStore.meetingTopic,
          agreedSlot.start_time,
          agreedSlot.end_time
        ).then(success => {
          if (success) {
            // 日程邀请已全部发出，此时才清理多维表格
            console.log(`[Cleanup] 日程邀请已发送完毕，删除 session ${session_id} 的多维表格`);
            return dbStore.deleteSession(session_id);
          } else {
            console.warn(`[Cleanup] createMeeting 未完全成功，保留多维表格以便排查`);
          }
        }).catch(err => console.error('[Meeting Error]', err));

      } else if (status.result === 'conflict') {
        // ========== 唤醒唤醒端点：排期冲突，需 LLM 决策 ==========
        toastMsg = '由于存在冲突或有人没空，排期进程暂停。助手已记录并将寻求下一套方案！';

        console.log(`[ALERT] 排期冲突触发：会话 ${session_id} 需要回复人工或重议。`);
        
        // 关键唤醒逻辑：明确执行外部调用
        const wakeEndpoint = process.env.OPENCLAW_WAKE_ENDPOINT;
        if (isSafeUrl(wakeEndpoint)) {
          try {
            console.log(`[Wakeup] 正在主动唤醒 Agent 端点: ${wakeEndpoint}`);
            const response = await fetch(wakeEndpoint, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                sessionId: session_id,
                event: 'schedule_conflict',
                message: '大家排期时间无法协调，或者均选择了暂无时间。请你分析冲突情况，主动跟用户生成安抚话术或重新提出另外一周的时间方案进行斡旋。'
              })
            });
            const wakeData = await response.json();
            console.log(`[Wakeup] Agent 响应接收:`, JSON.stringify(wakeData));
          } catch (wakeErr) {
            console.warn(`[Wakeup Warning] 唤醒请求失败(非致命):`, wakeErr.message);
          }
        } else {
          console.warn('[Security/Config] OPENCLAW_WAKE_ENDPOINT 未配置或不合法，跳过唤醒。');
        }

      }
    }

    // 给飞书立刻回包
    return res.json({ toast: { type: 'success', content: toastMsg } });
  }

  res.status(200).send('ok');
});


app.listen(port, () => {
  console.log(`[OpenClaw Agent] 排期原子服务启动, 监听端口: ${port}`);
});
