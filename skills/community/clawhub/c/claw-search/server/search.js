/**
 * 搜索后端 - 使用 skillhub 进行搜索
 */

import { execSync } from 'child_process';

// 从环境变量获取 API Keys (可选的后端)
const TAVILY_API_KEY = process.env.TAVILY_API_KEY;
const BRAVE_API_KEY = process.env.BRAVE_API_KEY;

/**
 * 使用 skillhub 进行搜索 (免费，无需 API Key)
 */
async function searchSkillhub({ query, count = 10 }) {
  try {
    const output = execSync(`skillhub search "${query}"`, {
      encoding: 'utf8',
      timeout: 30000
    });

    const results = [];
    const lines = output.split('\n').filter(line => line.trim());
    
    // 解析 skillhub 输出
    // 格式: skill-name  description
    let currentTitle = '';
    for (const line of lines) {
      if (results.length >= count) break;
      
      // 跳过标题行
      if (line.includes('You can use') || line.includes('to install')) continue;
      
      // 匹配 skill 名称和描述
      const match = line.match(/^(\S+)\s+(.+)$/);
      if (match) {
        const [_, title, description] = match;
        // 过滤掉非搜索结果行
        if (!title.includes('skillhub') && description.length > 10) {
          results.push({
            title: title,
            url: `https://clawhub.com/skill/${title}`,
            description: description.substring(0, 300),
            age: ''
          });
        }
      }
    }

    console.log(`Skillhub: found ${results.length} results`);
    return results;
  } catch (error) {
    console.error('Skillhub search failed:', error.message);
    return [];
  }
}

/**
 * 使用 Tavily API (需要 API Key)
 */
async function searchTavily({ query, count = 10 }) {
  if (!TAVILY_API_KEY) return null;

  try {
    const axios = (await import('axios')).default;
    const response = await axios.post(
      'https://api.tavily.com/search',
      { query, max_results: count },
      {
        headers: { 'Content-Type': 'application/json' },
        timeout: 15000
      }
    );

    return response.data.results.map(item => ({
      title: item.title || '',
      url: item.url || '',
      description: item.content || item.snippet || '',
      age: item.published_date || ''
    }));
  } catch (error) {
    console.error('Tavily search failed:', error.message);
    return null;
  }
}

/**
 * 使用 Brave Search API (需要 API Key)
 */
async function searchBrave({ query, count = 10, country = 'CN', freshness }) {
  if (!BRAVE_API_KEY) return null;

  try {
    const axios = (await import('axios')).default;
    const params = { q: query, count };
    if (country) params.country = country;
    if (freshness) params.freshness = freshness;

    const response = await axios.get('https://api.search.brave.com/res/v1/web/search', {
      params,
      headers: {
        'X-Subscription-Token': BRAVE_API_KEY,
        'Accept': 'application/json'
      },
      timeout: 15000
    });

    return response.data.web?.results?.map(item => ({
      title: item.title || '',
      url: item.url || '',
      description: item.description || '',
      age: item.age || ''
    })) || [];
  } catch (error) {
    console.error('Brave search failed:', error.message);
    return null;
  }
}

/**
 * 主搜索函数 - 智能选择后端
 */
export async function searchWeb({ query, count = 10, offset = 0, country = 'CN', freshness }) {
  let results = [];

  // 1. 优先使用有 API Key 的后端
  if (BRAVE_API_KEY) {
    const braveResults = await searchBrave({ query, count, country, freshness });
    if (braveResults && braveResults.length > 0) {
      console.log('Using Brave backend');
      results = braveResults;
    }
  }

  if (results.length === 0 && TAVILY_API_KEY) {
    const tavilyResults = await searchTavily({ query, count });
    if (tavilyResults && tavilyResults.length > 0) {
      console.log('Using Tavily backend');
      results = tavilyResults;
    }
  }

  // 2. 默认使用 skillhub 搜索 (免费)
  if (results.length === 0) {
    console.log('Using Skillhub backend (free)');
    results = await searchSkillhub({ query, count });
  }

  // 应用分页偏移
  if (offset > 0 && offset < results.length) {
    results = results.slice(offset);
  }

  return results.slice(0, count);
}
