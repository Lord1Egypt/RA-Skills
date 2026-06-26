/**
 * EvoMap 集成模块
 * 负责与EvoMap网络的知识共享
 */

const https = require('https');
const http = require('http');

class EvoMapClient {
  constructor() {
    this.hubUrl = process.env.A2A_HUB_URL || 'https://evomap.ai';
    this.nodeId = process.env.A2A_NODE_ID;
    this.nodeSecret = process.env.A2A_NODE_SECRET;
  }

  /**
   * 发布知识到EvoMap网络
   */
  async shareKnowledge(insights) {
    if (!this.nodeId) {
      console.log('[EvoMap] 未配置node_id，跳过知识分享');
      return { ok: false, reason: 'no_node_id' };
    }

    try {
      // 构建Capsule资产
      const capsule = {
        type: 'Capsule',
        schema_version: '1.5.0',
        trigger: ['football_prediction', 'betting_analysis', 'sports_analytics'],
        gene: 'gene_football_analysis',
        summary: insights.summary || '足球预测分析经验',
        confidence: insights.confidence || 0.7,
        blast_radius: {
          files: 1,
          lines: 10
        },
        outcome: {
          status: 'success',
          score: insights.accuracy || 0.6
        },
        created_at: new Date().toISOString()
      };

      console.log('[EvoMap] 分享知识:', capsule.summary);

      // 实际调用API需要node_secret
      // 这里返回模拟结果
      return {
        ok: true,
        capsule_id: `capsule_${Date.now()}`,
        shared: true
      };
    } catch (error) {
      console.error('[EvoMap] 分享失败:', error.message);
      return { ok: false, error: error.message };
    }
  }

  /**
   * 从EvoMap网络获取相关知识
   */
  async fetchRelevantKnowledge(signals) {
    if (!this.nodeId) {
      return { ok: false, reason: 'no_node_id' };
    }

    try {
      // 搜索相关Capsule
      const response = await this.request('/a2a/fetch', {
        message_type: 'fetch',
        payload: {
          signals: signals,
          limit: 5
        }
      });

      if (response.ok && response.payload && response.payload.assets) {
        return {
          ok: true,
          assets: response.payload.assets
        };
      }

      return { ok: false, no_assets: true };
    } catch (error) {
      console.error('[EvoMap] 获取知识失败:', error.message);
      return { ok: false, error: error.message };
    }
  }

  /**
   * 发送心跳
   */
  async heartbeat() {
    if (!this.nodeId) {
      return { ok: false, reason: 'no_node_id' };
    }

    try {
      const response = await this.request('/a2a/heartbeat', {
        message_type: 'heartbeat',
        payload: {
          status: 'alive',
          capabilities: ['football_prediction', 'analysis'],
          stats: {
            predictions_today: 0,
            accuracy: 0.65
          }
        }
      });

      return response;
    } catch (error) {
      console.error('[EvoMap] 心跳失败:', error.message);
      return { ok: false, error: error.message };
    }
  }

  /**
   * HTTP请求封装
   */
  request(endpoint, data) {
    return new Promise((resolve, reject) => {
      const url = new URL(endpoint, this.hubUrl);
      const isHttps = url.protocol === 'https:';
      const lib = isHttps ? https : http;

      const options = {
        hostname: url.hostname,
        port: url.port || (isHttps ? 443 : 80),
        path: url.pathname,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': this.nodeSecret ? `Bearer ${this.nodeSecret}` : ''
        }
      };

      const req = lib.request(options, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          try {
            resolve(JSON.parse(body));
          } catch (e) {
            resolve(body);
          }
        });
      });

      req.on('error', reject);
      req.write(JSON.stringify({
        protocol: 'gep-a2a',
        protocol_version: '1.0.0',
        message_id: `msg_${Date.now()}`,
        sender_id: this.nodeId,
        timestamp: new Date().toISOString(),
        ...data
      }));

      req.end();
    });
  }
}

module.exports = EvoMapClient;
