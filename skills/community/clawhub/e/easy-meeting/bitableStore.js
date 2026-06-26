/**
 * 基于飞书多维表格的会话存储模块
 *
 * 设计策略：
 * - 每次 dispatch-cards 时，临时创建一张多维表格（一个 app + 一个 table）
 * - 表格名称带有 sessionId，便于查找和去重
 * - 会议完成（agreed）或冲突解决后，自动删除对应多维表格
 * - 启动时检查并清理超过 TTL 的孤儿表格（防止异常中断导致的残留）
 */

const logger = {
  info: (ctx, msg) => console.log(`[INFO]`, JSON.stringify({ ...ctx, msg })),
  error: (ctx, msg) => console.error(`[ERR]`, JSON.stringify({ ...ctx, msg }))
};

// 会话最大存活时间：48 小时（毫秒）
const SESSION_TTL_MS = 48 * 60 * 60 * 1000;

// 多维表格 app 名称前缀，便于识别和清理
const APP_NAME_PREFIX = 'sched_session_';

class BitableStore {
  /**
   * @param {FeishuService} feishuService - 已初始化的 FeishuService 实例（共享 token 缓存）
   */
  constructor(feishuService) {
    this.svc = feishuService;
  }

  // ─── 内部辅助 ────────────────────────────────────────────────

  async _req(method, url, body) {
    return this.svc._request(method, url, body ? { body } : {});
  }

  /** 将 session 数据序列化为多维表格单行字段 */
  _toFields(data) {
    return {
      session_id:         data.id,
      meeting_topic:      data.meetingTopic,
      user_ids:           JSON.stringify(data.userIds),
      time_slots:         JSON.stringify(data.timeSlots),
      agent_message:      data.agentMessage,
      status:             data.status,
      participants_state: JSON.stringify(data.participantsState),
      created_at:         data.createdAt
    };
  }

  /** 将多维表格单行字段反序列化为 session 数据 */
  _fromFields(fields, recordId, appToken, tableId) {
    return {
      id:                 fields.session_id,
      meetingTopic:       fields.meeting_topic,
      userIds:            JSON.parse(fields.user_ids || '[]'),
      timeSlots:          JSON.parse(fields.time_slots || '[]'),
      agentMessage:       fields.agent_message,
      status:             fields.status,
      participantsState:  JSON.parse(fields.participants_state || '{}'),
      createdAt:          fields.created_at,
      // 元信息，用于后续更新/删除
      _recordId:          recordId,
      _appToken:          appToken,
      _tableId:           tableId
    };
  }

  // ─── 多维表格生命周期 ─────────────────────────────────────────

  /**
   * 为一个 session 创建专属多维表格 app
   * 表格结构：一张 table，包含所有 session 字段
   */
  async _createBitableApp(sessionId) {
    // 1. 创建多维表格 app
    const appRes = await this._req('POST',
      'https://open.feishu.cn/open-apis/bitable/v1/apps',
      { name: `${APP_NAME_PREFIX}${sessionId}` }
    );
    const appToken = appRes.app.app_token;

    // 2. 在 app 内创建数据表（带字段定义）
    const tableRes = await this._req('POST',
      `https://open.feishu.cn/open-apis/bitable/v1/apps/${appToken}/tables`,
      {
        table: {
          name: 'sessions',
          fields: [
            { field_name: 'session_id',         type: 1 }, // 文本
            { field_name: 'meeting_topic',       type: 1 },
            { field_name: 'user_ids',            type: 1 },
            { field_name: 'time_slots',          type: 1 },
            { field_name: 'agent_message',       type: 1 },
            { field_name: 'status',              type: 1 },
            { field_name: 'participants_state',  type: 1 },
            { field_name: 'created_at',          type: 2 } // 数字（时间戳）
          ]
        }
      }
    );
    const tableId = tableRes.table_id;

    logger.info({ sessionId, appToken, tableId }, 'Bitable app created for session');
    return { appToken, tableId };
  }

  /**
   * 删除多维表格 app（会议完成或过期时调用）
   */
  async _deleteBitableApp(appToken) {
    try {
      await this._req('DELETE',
        `https://open.feishu.cn/open-apis/bitable/v1/apps/${appToken}`
      );
      logger.info({ appToken }, 'Bitable app deleted');
    } catch (err) {
      logger.error({ appToken, err: err.message }, 'Failed to delete bitable app');
    }
  }

  // ─── 公开 API ─────────────────────────────────────────────────

  /**
   * 创建会话（新建多维表格 + 写入第一行）
   * 创建前检查是否已存在同名 session，防止重复
   */
  async createSession(id, details) {
    // 去重检查：查询已有 app 列表，看是否有同名的
    const existing = await this._findAppBySessionId(id);
    if (existing) {
      logger.info({ id }, 'Session already exists, skipping creation');
      return this.getSession(id);
    }

    const { appToken, tableId } = await this._createBitableApp(id);

    const sessionData = {
      id,
      ...details,
      status: 'WAITING',
      participantsState: details.userIds.reduce((acc, uid) => {
        acc[uid] = { status: 'PENDING', selectedTime: null };
        return acc;
      }, {}),
      createdAt: Date.now()
    };

    // 写入第一行记录
    await this._req('POST',
      `https://open.feishu.cn/open-apis/bitable/v1/apps/${appToken}/tables/${tableId}/records`,
      { fields: this._toFields(sessionData) }
    );

    return { ...sessionData, _appToken: appToken, _tableId: tableId };
  }

  /**
   * 读取会话数据
   */
  async getSession(id) {
    const meta = await this._findAppBySessionId(id);
    if (!meta) return null;

    const { appToken, tableId } = meta;
    const res = await this._req('GET',
      `https://open.feishu.cn/open-apis/bitable/v1/apps/${appToken}/tables/${tableId}/records?page_size=1`
    );
    const record = res.items?.[0];
    if (!record) return null;

    return this._fromFields(record.fields, record.record_id, appToken, tableId);
  }

  /**
   * 更新参会人意向，并回写多维表格
   */
  async updateParticipantState(sessionId, userId, selectedTime) {
    const session = await this.getSession(sessionId);
    if (!session) return null;

    if (session.participantsState[userId] !== undefined) {
      session.participantsState[userId] = {
        status: selectedTime === 'none' ? 'REJECTED' : 'CONFIRMED',
        selectedTime
      };

      await this._req('PUT',
        `https://open.feishu.cn/open-apis/bitable/v1/apps/${session._appToken}/tables/${session._tableId}/records/${session._recordId}`,
        { fields: this._toFields(session) }
      );
    }

    return session;
  }

  /**
   * 检查共识状态（逻辑与原 dbStore 一致）
   */
  async checkSessionConsensus(sessionId) {
    const session = await this.getSession(sessionId);
    if (!session) return { done: false, result: null };

    const states = Object.values(session.participantsState);
    const pendingCount = states.filter(s => s.status === 'PENDING').length;

    if (pendingCount > 0) return { done: false, result: 'pending' };

    const rejects = states.filter(s => s.status === 'REJECTED');
    if (rejects.length > 0) return { done: true, result: 'conflict' };

    const selectedTimes = states.map(s => s.selectedTime);
    // 至少 2 人且所有人选的时间一致才算 agreed
    const allSame = selectedTimes.length >= 2 && selectedTimes.every(t => t === selectedTimes[0]);

    if (allSame) return { done: true, result: 'agreed', time: selectedTimes[0] };
    return { done: true, result: 'conflict' };
  }

  /**
   * 会议完成后删除多维表格（自动清理）
   */
  async deleteSession(sessionId) {
    const meta = await this._findAppBySessionId(sessionId);
    if (!meta) return;
    await this._deleteBitableApp(meta.appToken);
  }

  /**
   * 启动时清理超过 TTL 的孤儿表格
   * 建议在 index.js 启动时调用一次
   */
  async cleanupExpiredSessions() {
    try {
      const res = await this._req('GET',
        'https://open.feishu.cn/open-apis/bitable/v1/apps?page_size=50'
      );
      const apps = res.items || [];
      const now = Date.now();
      let cleaned = 0;

      for (const app of apps) {
        if (!app.name.startsWith(APP_NAME_PREFIX)) continue;

        // 通过 app 的创建时间判断是否过期（飞书返回秒级时间戳）
        const createdAt = (app.create_time || 0) * 1000;
        if (now - createdAt > SESSION_TTL_MS) {
          await this._deleteBitableApp(app.app_token);
          cleaned++;
        }
      }

      if (cleaned > 0) logger.info({ cleaned }, 'Expired bitable sessions cleaned up');
    } catch (err) {
      logger.error({ err: err.message }, 'Failed to cleanup expired sessions');
    }
  }

  // ─── 内部查找 ─────────────────────────────────────────────────

  /**
   * 通过 sessionId 查找对应的多维表格 app
   * 利用 app 名称约定 `sched_session_<sessionId>` 快速定位
   *
   * 注意：当前实现只扫描前 50 个 app，如果账号下有大量多维表格，可能找不到目标。
   * 生产环境建议：
   * 1. 使用独立的飞书账号专门运行此 skill
   * 2. 或实现分页逻辑（page_token）遍历所有 app
   * 3. 或使用外部 KV 存储（Redis）缓存 sessionId -> appToken 映射
   */
  async _findAppBySessionId(sessionId) {
    try {
      const res = await this._req('GET',
        'https://open.feishu.cn/open-apis/bitable/v1/apps?page_size=50'
      );
      const apps = res.items || [];
      const target = apps.find(a => a.name === `${APP_NAME_PREFIX}${sessionId}`);
      if (!target) return null;

      // 获取该 app 下的第一张表
      const tableRes = await this._req('GET',
        `https://open.feishu.cn/open-apis/bitable/v1/apps/${target.app_token}/tables`
      );
      const tableId = tableRes.items?.[0]?.table_id;
      if (!tableId) return null;

      return { appToken: target.app_token, tableId };
    } catch (err) {
      logger.error({ sessionId, err: err.message }, 'Failed to find bitable app');
      return null;
    }
  }
}

module.exports = BitableStore;
