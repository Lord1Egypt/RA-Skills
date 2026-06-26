/**
 * China Localization Pack v2 - 中国本地化包（安全优化版）
 * 
 * 全中文界面 + 本地服务集成 + 百度搜索支持
 * 
 * 安全特性：
 * - 所有 API keys 通过环境变量配置
 * - 无硬编码敏感信息
 * - 符合 ClawHub 安全规范
 */

import { TAVILY_CONFIG, FEISHU_CONFIG, WECHAT_CONFIG, DINGTALK_CONFIG, AMAP_CONFIG, ALIPAY_CONFIG } from './config';
import { baiduSearch } from './baidu-search';

// ==================== 语言包 ====================

const zhCN = {
  // 通用
  welcome: '欢迎使用 China Localization Pack',
  loading: '正在加载...',
  success: '成功',
  error: '错误',
  
  // 飞书集成
  feishu: {
    calendar: '飞书日历',
    tasks: '飞书任务',
    docs: '飞书文档',
    meetings: '飞书会议',
    noEvents: '今日无日程安排',
    noTasks: '暂无待办事项',
  },
  
  // 天气
  weather: {
    query: '查询天气',
    city: '城市',
    temperature: '温度',
    condition: '天气',
    humidity: '湿度',
    advice: '建议',
  },
  
  // 搜索引擎
  search: {
    tavily: 'Tavily 搜索',
    baidu: '百度搜索',
    wechat: '微信搜索',
  },
  
  // 错误提示
  errors: {
    networkError: '网络连接失败，请检查网络',
    apiError: 'API 调用失败：{message}',
    permissionDenied: '权限不足，请先授权',
    notFound: '未找到相关内容',
    configMissing: '缺少必要的配置，请设置环境变量',
  },
};

// ==================== 主类 ====================

export class ChinaLocalization {
  private language: 'zh-CN' | 'en' = 'zh-CN';
  
  /**
   * 设置语言
   */
  setLanguage(lang: 'zh-CN' | 'en'): void {
    this.language = lang;
    console.log(`语言已切换为：${lang}`);
  }
  
  /**
   * 获取翻译
   */
  t(key: string): string {
    const keys = key.split('.');
    let value: any = this.language === 'zh-CN' ? zhCN : {};
    
    for (const k of keys) {
      value = value?.[k];
    }
    
    return value || key;
  }
  
  /**
   * 获取飞书日历事件
   */
  async getCalendarEvents(options?: {
    date?: string;
    limit?: number;
  }): Promise<CalendarEvent[]> {
    console.log(this.t('feishu.calendar'));
    
    // TODO: 调用飞书日历 API
    // 现在返回示例数据
    return [
      {
        title: '示例：团队周会',
        time: '10:00-11:00',
        location: '会议室',
      },
    ];
  }
  
  /**
   * 获取飞书任务
   */
  async getTasks(options?: {
    due?: string;
    status?: string;
  }): Promise<Task[]> {
    console.log(this.t('feishu.tasks'));
    
    // TODO: 调用飞书任务 API
    // 现在返回示例数据
    return [
      {
        title: '示例：完成代码审查',
        due: 'today',
        priority: 'high',
        completed: false,
      },
    ];
  }
  
  /**
   * 中文搜索（支持多种搜索引擎）
   */
  async search(query: string, options?: {
    engine?: 'tavily' | 'baidu' | 'wechat';
    limit?: number;
  }): Promise<SearchResult[]> {
    const engine = options?.engine || 'baidu'; // 默认使用百度搜索
    const limit = options?.limit || 5;
    
    console.log(`${this.t(`search.${engine}`)}：${query}`);
    
    try {
      if (engine === 'baidu') {
        return await baiduSearch(query, { limit });
      } else if (engine === 'tavily') {
        return await this.tavilySearch(query, limit);
      } else if (engine === 'wechat') {
        return await this.wechatSearch(query, limit);
      } else {
        throw new Error(`不支持的搜索引擎：${engine}`);
      }
    } catch (error: any) {
      console.error(`搜索失败 (${engine}):`, error.message);
      throw new Error(this.t('errors.apiError').replace('{message}', error.message));
    }
  }
  
  /**
   * Tavily 搜索封装
   */
  private async tavilySearch(query: string, limit: number = 5): Promise<SearchResult[]> {
    if (!TAVILY_CONFIG.apiKey) {
      throw new Error(this.t('errors.configMissing'));
    }
    
    const response = await fetch(TAVILY_CONFIG.apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        api_key: TAVILY_CONFIG.apiKey,
        query: query,
        max_results: limit,
        search_depth: 'basic',
      }),
    });

    if (!response.ok) {
      throw new Error(`API 错误：${response.status}`);
    }

    const data: any = await response.json();
    return (data.results || []).map((r: any) => ({
      title: r.title,
      url: r.url,
      content: r.content || r.snippet || '',
    }));
  }
  
  /**
   * 微信搜索封装（待实现）
   */
  private async wechatSearch(query: string, limit: number = 5): Promise<SearchResult[]> {
    // TODO: 实现微信搜索
    throw new Error('微信搜索功能暂未实现');
  }
  
  /**
   * 查询天气
   */
  async getWeather(city: string): Promise<WeatherResult> {
    console.log(`${this.t('weather.query')}: ${city}`);
    
    // 使用百度搜索获取天气信息（更适合中文内容）
    const results = await this.search(`${city} 天气 温度 预报`, { engine: 'baidu', limit: 3 });
    
    return this.parseWeather(results, city);
  }
  
  /**
   * 解析天气信息
   */
  private parseWeather(results: SearchResult[], city: string): WeatherResult {
    const text = results.map(r => `${r.title} ${r.content || ''}`).join(' ').toLowerCase();

    // 提取温度
    let temperature = '未知';
    const tempPatterns = [
      /(\d+)[°度]\s*c/i,
      /气温[:：]?\s*(\d+)[°度]/,
      /温度[:：]?\s*(\d+)[°度]/,
      /(\d+)[°度][左右约]?/,
    ];
    
    for (const pattern of tempPatterns) {
      const match = text.match(pattern);
      if (match && match[1]) {
        temperature = `${match[1]}°C`;
        break;
      }
    }

    // 提取天气状况
    let condition = '未知';
    const weatherPatterns = [
      { keywords: ['暴雨', '大暴雨', '特大暴雨'], value: '暴雨' },
      { keywords: ['小雨', '中雨', '大雨', '阵雨', '雨'], value: '雨' },
      { keywords: ['雪', '雨夹雪'], value: '雪' },
      { keywords: ['雾', '雾霾', '沙尘'], value: '雾' },
      { keywords: ['多云', '阴'], value: '多云' },
      { keywords: ['晴', '阳光'], value: '晴' },
    ];
    
    for (const { keywords, value } of weatherPatterns) {
      if (keywords.some(k => text.includes(k))) {
        condition = value;
        break;
      }
    }

    // 提取湿度
    let humidity = '未知';
    const humidityPatterns = [
      /湿度[:：]?\s*(\d+)%/,
      /相对湿度[:：]?\s*(\d+)%/,
      /(\d+)%\s*湿度/,
    ];
    
    for (const pattern of humidityPatterns) {
      const match = text.match(pattern);
      if (match && match[1]) {
        humidity = `${match[1]}%`;
        break;
      }
    }

    // 生成建议
    const advice = this.generateWeatherAdvice(condition, temperature);

    return {
      city,
      temperature,
      condition,
      humidity,
      advice,
    };
  }
  
  /**
   * 生成天气建议
   */
  private generateWeatherAdvice(condition: string, temperature: string): string {
    const temp = parseInt(temperature) || 25;
    const advices: string[] = [];

    // 基于天气状况的建议
    if (condition === '雨' || condition === '暴雨') {
      advices.push('记得带伞');
      if (condition === '暴雨') {
        advices.push('暴雨天气，尽量避免外出');
      } else {
        advices.push('路面湿滑注意安全');
      }
    } else if (condition === '雪') {
      advices.push('雪天路滑，注意交通安全');
      advices.push('注意保暖防冻');
    } else if (condition === '雾' || condition === '雾霾') {
      advices.push('能见度低，出行注意安全');
      advices.push('建议佩戴口罩');
    } else if (condition === '多云' || condition === '阴') {
      advices.push('天气适宜，正常出行');
    } else if (condition === '晴') {
      advices.push('天气不错，适合出行');
      if (temp > 25) {
        advices.push('阳光较强，注意防晒');
      }
    }

    // 基于温度的建议
    if (temp < 0) {
      advices.push('天气严寒，注意保暖防冻');
    } else if (temp < 10) {
      advices.push('天气较冷，注意保暖');
    } else if (temp > 35) {
      advices.push('天气炎热，注意防暑降温');
    } else if (temp > 30) {
      advices.push('气温较高，注意防暑');
    }

    return [...new Set(advices)].join('，');
  }
}

// ==================== 类型定义 ====================

export interface CalendarEvent {
  title: string;
  time: string;
  location?: string;
}

export interface Task {
  title: string;
  due?: string;
  priority: 'high' | 'medium' | 'low';
  completed: boolean;
}

export interface SearchResult {
  title: string;
  url: string;
  content: string;
}

export interface WeatherResult {
  city: string;
  temperature: string;
  condition: string;
  humidity: string;
  advice: string;
}

// ==================== 导出 ====================

export default ChinaLocalization;