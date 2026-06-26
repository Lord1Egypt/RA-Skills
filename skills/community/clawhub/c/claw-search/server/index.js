/**
 * Claw Search Server
 * 通用免费的 Web Search API 服务
 * 
 * 支持的后端:
 * - skillhub: 搜索 ClawHub 技能 (免费)
 * - tavily: Tavily AI 搜索 (需要 API Key)
 * - brave: Brave Search (需要 API Key)
 * 
 * 使用方式:
 *   docker run -d -p 8080:8080 -e TAVILY_API_KEY=xxx claw-search
 */

import express from 'express';
import cors from 'cors';
import { searchWeb } from './search.js';

const app = express();
const PORT = process.env.PORT || 8080;

app.use(cors());
app.use(express.json());

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    service: 'Claw Search', 
    version: '1.0.0',
    backends: ['skillhub', 'tavily', 'brave']
  });
});

// Search API - 兼容 Brave Search 格式
app.post('/api/search', async (req, res) => {
  try {
    const { 
      query, 
      count = 10, 
      offset = 0, 
      country = 'CN',
      freshness 
    } = req.body;

    if (!query) {
      return res.status(400).json({ 
        error: { code: 'VALIDATION', detail: 'query is required' }
      });
    }

    const results = await searchWeb({
      query,
      count: Math.min(count, 20),
      offset,
      country,
      freshness
    });

    res.json({
      query,
      count: results.length,
      offset,
      results
    });
  } catch (error) {
    console.error('Search error:', error);
    res.status(500).json({ 
      error: { code: 'SERVER', detail: error.message }
    });
  }
});

// GET 方式搜索 (兼容更多客户端)
app.get('/search', async (req, res) => {
  try {
    const { q, query, count = 10, offset = 0, country = 'CN', freshness } = req.query;
    
    const searchQuery = q || query;
    if (!searchQuery) {
      return res.status(400).json({ 
        error: { code: 'VALIDATION', detail: 'query parameter is required' }
      });
    }

    const results = await searchWeb({
      query: searchQuery,
      count: Math.min(parseInt(count), 20),
      offset: parseInt(offset),
      country,
      freshness
    });

    res.json({
      query: searchQuery,
      count: results.length,
      offset: parseInt(offset),
      results
    });
  } catch (error) {
    console.error('Search error:', error);
    res.status(500).json({ 
      error: { code: 'SERVER', detail: error.message }
    });
  }
});

app.listen(PORT, () => {
  console.log(`🦔 Claw Search 服务已启动: http://localhost:${PORT}`);
  console.log(`📖 API 文档: POST /api/search`);
  console.log(`\n⚙️  可选环境变量:`);
  console.log(`   TAVILY_API_KEY - Tavily API Key (https://tavily.com)`);
  console.log(`   BRAVE_API_KEY  - Brave Search API Key`);
});
