/**
 * Novai360 智能市场分析 Skill v7.0
 * 新架构：利用 OpenClaw LLM 进行前置意图识别 + 后置总结
 * 不再依赖 DeepSeek，让 OpenClaw 自己思考
 */

// 19 个 MCP 工具定义（供 OpenClaw LLM 参考）
const MCP_TOOLS_LIST = `
可用的分析工具：
1. product_detail - 产品详情：查询 ASIN 的价格、评分、销量、排名等
2. product_search - 产品搜索：搜索亚马逊产品
3. product_variations - 产品子体：查询产品子体明细
4. product_history - 产品历史趋势：产品历史数据
5. product_keyword_reverse - 产品关键词反查：产品反查关键词
6. product_keyword_rank - 产品关键词排名：产品在关键词下的曝光位置
7. product_keyword_trend - 产品关键词趋势：产品在关键词下的排名趋势
8. keyword_detail - 关键词详情：查询热搜关键词详情
9. keyword_search_results - 关键词搜索结果：关键词搜索结果产品清单
10. keyword_history - 关键词历史趋势：关键词历史趋势
11. keyword_related - 关键词延伸词：查询关键词的延伸词
12. category_trend - 类目标目趋势：查询亚马逊细分类目市场趋势数据
13. category_search - 类目标目搜索：基于名称查询细分类目 nodeid
14. category_realtime - 类目标目实时数据：细分类目实时数据报告
15. category_keywords - 类目标目关键词：查询类目标目的核心关键词
16. category_filter - 类目标目筛选：筛选细分类目市场
17. category_history - 类目标目历史数据：类目历史时间段数据
18. category_features - 类目标目特点：查询产品类目特点
19. competitor_analysis - 竞品分析：竞品数据分析
`;

class Novai360Analytics {
  constructor(config) {
    this.baseUrl = config?.api?.baseUrl || 'https://api.novai360.com';
    this.name = 'novai360-analytics';
    this.version = '7.0';
  }

  /**
   * 获取技能列表
   */
  async getSkills() {
    try {
      const response = await fetch(`${this.baseUrl}/skills`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('获取技能列表失败');
      }

      const data = await response.json();
      return {
        success: true,
        skills: data.skills || [],
        metadata: {
          provider: 'Novai360',
          version: this.version,
          totalSkills: data.skills?.length || 0
        }
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        metadata: {
          provider: 'Novai360',
          version: this.version
        }
      };
    }
  }

  /**
   * 执行智能分析（新架构：前置思考 + 后置总结）
   * @param {string} message - 用户查询
   * @param {object} context - 上下文信息
   * @returns {Promise<object>} 分析结果
   */
  async analyze(message, context = {}) {
    try {
      // ========== 第 1 步：前置意图识别（让 OpenClaw LLM 思考）==========
      console.log('Step 1: 意图识别...');
      
      const intentPrompt = `你是一个专业的跨境电商数据分析师。用户提出了一个问题，请分析他需要使用哪个分析工具。

${MCP_TOOLS_LIST}

用户问题：${message}

请返回 JSON 格式（只返回 JSON，不要其他文字）：
{
  "tool": "工具名称（从上面列表中选择）",
  "params": {
    // 提取关键参数
    "asin": "如果提到 ASIN 则提取，否则 null",
    "keyword": "如果提到关键词则提取，否则 null",
    "searchName": "如果提到产品/类目名称则提取，否则 null",
    "site": "US" // 默认美国站
  },
  "confidence": 0.9, // 置信度 0-1
  "reason": "简要说明为什么选择这个工具"
}`;

      // 调用 OpenClaw 的 LLM 进行意图识别
      const intentResult = await this.callOpenClawLLM(intentPrompt, context);
      const intent = this.parseIntent(intentResult);
      
      console.log('意图识别结果:', intent);

      // ========== 第 2 步：调用 API 获取数据 ==========
      console.log('Step 2: 调用 API 获取数据...');
      
      const payload = {
        message: message,
        intent: intent,  // 告诉 API 已经识别好的意图
        context: {
          userId: context.userId || 'anonymous',
          sessionId: context.sessionId || Date.now().toString(),
          platform: context.platform || 'openclaw',
          ...context
        }
      };

      const response = await fetch(`${this.baseUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || '分析请求失败');
      }

      const apiResult = await response.json();
      console.log('API 返回数据:', apiResult);
      
      // ========== 第 3 步：后置总结（让 OpenClaw LLM 总结）==========
      console.log('Step 3: 数据总结...');
      
      const summaryPrompt = `你是一个专业的跨境电商数据分析师。请基于以下数据，为用户生成一份专业的市场分析报告。

【数据摘要】
${JSON.stringify(apiResult.dataSummary, null, 2)}

【分析框架】
${apiResult.analysisFramework || '请根据数据提供专业的分析建议'}

【输出要求】
- 使用专业的中文
- 数据驱动，引用具体数字
- 给出具体可执行的建议
- 避免技术术语，让用户容易理解
- 长度适中，重点突出

请直接输出分析报告，不要说"基于以上数据"这类话。`;

      const summaryResult = await this.callOpenClawLLM(summaryPrompt, context);
      
      console.log('总结完成');

      // ========== 第 4 步：返回完整结果 ==========
      return {
        success: true,
        data: {
          // 原始 MCP 数据
          marketData: apiResult.mcpResults || null,
          // 数据摘要
          dataSummary: apiResult.dataSummary || null,
          // LLM 总结的分析报告
          analysisReport: summaryResult,
          // 意图识别结果
          intent: intent
        },
        analysis: {
          // 意图识别
          intent: intent.tool || 'unknown',
          confidence: intent.confidence || 0,
          // 分析时间戳
          timestamp: apiResult.metadata?.timestamp || new Date().toISOString()
        },
        metadata: {
          provider: 'Novai360',
          version: this.version,
          tool: intent.tool || 'unknown',
          timestamp: new Date().toISOString()
        },
        // 网页报告链接（如果有）
        reportUrl: apiResult.reportUrl,
        // 交互菜单（如果有）
        interactiveMenu: apiResult.interactiveMenu
      };
    } catch (error) {
      console.error('Analysis error:', error);
      return {
        success: false,
        error: error.message,
        metadata: {
          provider: 'Novai360',
          timestamp: new Date().toISOString(),
          version: this.version
        }
      };
    }
  }

  /**
   * 调用 OpenClaw LLM（前置思考和后置总结）
   * @param {string} prompt - 提示词
   * @param {object} context - 上下文
   * @returns {Promise<string>} LLM 返回
   */
  async callOpenClawLLM(prompt, context) {
    // 注意：这里假设 OpenClaw 提供了调用 LLM 的方法
    // 实际实现取决于 OpenClaw 的 Skill 框架
    
    // 方式 1：如果 OpenClaw 提供了 LLM 接口
    if (context.llm) {
      return await context.llm(prompt);
    }
    
    // 方式 2：如果 OpenClaw 没有提供 LLM 接口，返回原始 prompt
    // 让 OpenClaw 的主 LLM 在处理 skill 时自然调用
    return prompt;
  }

  /**
   * 解析意图识别结果
   * @param {string} intentResult - LLM 返回的结果
   * @returns {object} 解析后的意图
   */
  parseIntent(intentResult) {
    try {
      // 尝试解析 JSON
      const jsonMatch = intentResult.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
      
      // 解析失败，返回默认意图
      return {
        tool: 'product_search',
        params: { searchName: intentResult, site: 'US' },
        confidence: 0.5
      };
    } catch (e) {
      console.error('Parse intent error:', e);
      return {
        tool: 'product_search',
        params: { searchName: intentResult, site: 'US' },
        confidence: 0.5
      };
    }
  }

  /**
   * 获取 API 健康状态
   */
  async getHealth() {
    try {
      const response = await fetch(`${this.baseUrl}/health`, {
        method: 'GET',
      });

      if (!response.ok) {
        return {
          status: 'error',
          code: response.status
        };
      }

      const data = await response.json();
      return {
        status: data.status || 'ok',
        service: data.service || 'novai360-analytics',
        version: data.version || this.version
      };
    } catch (error) {
      return {
        status: 'error',
        message: error.message
      };
    }
  }
}

// 导出 Skill 实例
module.exports = {
  name: 'novai360-analytics',
  version: '7.0',
  description: 'Novai360 智能市场分析服务（v7 新架构：利用 OpenClaw LLM 思考）',
  handler: Novai360Analytics,
  
  // 快速使用函数
  analyze: async (message, context) => {
    const analytics = new Novai360Analytics({
      api: { baseUrl: 'https://api.novai360.com' }
    });
    return await analytics.analyze(message, context);
  },
  
  getSkills: async () => {
    const analytics = new Novai360Analytics({
      api: { baseUrl: 'https://api.novai360.com' }
    });
    return await analytics.getSkills();
  }
};
