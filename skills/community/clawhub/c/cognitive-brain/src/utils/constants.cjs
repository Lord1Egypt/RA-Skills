/**
 * 应用常量定义
 * 集中管理所有魔法数字和配置常量
 */

const CONSTANTS = {
  // 内容限制
  CONTENT: {
    MIN_LENGTH: 3,
    MAX_LENGTH: 10000,
    SUMMARY_LENGTH: 200
  },

  // API 配置
  API: {
    DEFAULT_PORT: 3000,
    RATE_LIMIT_WINDOW_MS: 60000,    // 1分钟
    RATE_LIMIT_MAX_REQUESTS: 100,   // 每分钟最大请求数
    REQUEST_BODY_LIMIT: '10mb'
  },

  // WebSocket 配置
  WEBSOCKET: {
    HEARTBEAT_INTERVAL_MS: 30000,   // 30秒心跳
    ACTIVITY_TIMEOUT_MS: 60000,     // 60秒无活动检测
    DISCONNECT_TIMEOUT_MS: 120000   // 120秒超时断开
  },

  // 编码限制
  ENCODING: {
    RATE_LIMIT_WINDOW_MS: 60000,    // 1分钟窗口
    RATE_LIMIT_MAX: 100,            // 每分钟最大编码次数
    MAX_ASSOC_ENTITIES: 5           // 最大关联实体数
  },

  // 数据库配置
  DB: {
    DEFAULT_POOL_SIZE: 10,
    CONNECTION_TIMEOUT_MS: 5000,
    QUERY_TIMEOUT_MS: 10000,
    IDLE_TIMEOUT_MS: 30000
  },

  // 重要性范围
  IMPORTANCE: {
    MIN: 0,
    MAX: 1,
    DEFAULT: 0.5
  },

  // 关联权重
  ASSOCIATION: {
    DEFAULT_WEIGHT: 0.5,
    MIN_WEIGHT: 0,
    MAX_WEIGHT: 1,
    DECAY_FACTOR: 0.95,
    WEAK_THRESHOLD: 0.1
  },

  // 熔断器配置
  CIRCUIT_BREAKER: {
    FAILURE_THRESHOLD: 5,
    SUCCESS_THRESHOLD: 3,
    TIMEOUT_MS: 30000
  }
};

module.exports = { CONSTANTS };
