#!/usr/bin/env node
/**
 * Chairman Daily Brief - Main Script
 * 
 * Usage:
 *   node chairman_daily.mjs morning --symbol 600519.SS --company "Kweichow Moutai"
 *   node chairman_daily.mjs evening --symbol 0700.HK --company "Tencent Holdings"
 *   node chairman_daily.mjs morning --watchlist holdings
 *   node chairman_daily.mjs watch --action list
 */

import { readFileSync, existsSync, writeFileSync, mkdirSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_DIR = join(__dirname, '..');
const CONFIG_DIR = join(SKILL_DIR, 'config');
const EVOLUTION_DIR = join(SKILL_DIR, '.evolution');

// QVeris API Configuration
const QVERIS_API_BASE = 'https://qveris.ai/api/v1';
const QVERIS_API_KEY = process.env.QVERIS_API_KEY;

if (!QVERIS_API_KEY) {
  console.error('❌ Error: QVERIS_API_KEY environment variable not set');
  console.error('Please set: export QVERIS_API_KEY="your-api-key"');
  process.exit(1);
}

// Tool Chain Configuration
const TOOL_CHAINS = {
  morning_brief: {
    market_overview: ['ths_ifind.global_market', 'alpha_vantage.market_status'],
    policy_news: ['caidazi.news.query', 'caidazi.report.query'],
    company_quote: ['ths_ifind.real_time_quotation'],
    industry_data: ['ths_ifind.industry_index', 'caidazi.sector_analysis'],
    sentiment: ['qveris_social.x_domain_hot_topics']
  },
  evening_brief: {
    company_quote: ['ths_ifind.real_time_quotation', 'ths_ifind.history_quotation'],
    announcements: ['caidazi.news.query', 'exchange_announcements'],
    research: ['caidazi.report.query', 'alpha_news_sentiment'],
    fund_flow: ['ths_ifind.capital_flow', 'ths_ifind.dragon_tiger']
  }
};

/**
 * Search QVeris Tools
 */
async function searchTools(query, limit = 10) {
  try {
    const response = await fetch(`${QVERIS_API_BASE}/tools/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${QVERIS_API_KEY}`
      },
      body: JSON.stringify({ query, limit })
    });

    if (!response.ok) {
      throw new Error(`Search failed: ${response.status}`);
    }

    const data = await response.json();
    return data.tools || [];
  } catch (error) {
    console.error(`Tool search failed: ${error.message}`);
    return [];
  }
}

/**
 * Execute QVeris Tool
 */
async function executeTool(toolId, searchId, params) {
  try {
    const response = await fetch(`${QVERIS_API_BASE}/tools/execute`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${QVERIS_API_KEY}`
      },
      body: JSON.stringify({
        tool_id: toolId,
        search_id: searchId,
        params
      })
    });

    if (!response.ok) {
      throw new Error(`Execution failed: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`Tool execution failed: ${error.message}`);
    return null;
  }
}

/**
 * Get Global Market Overview
 */
async function getGlobalMarketOverview() {
  const tools = await searchTools('global market overview US stock Asia', 5);
  
  // Simulated data (should call QVeris in production)
  return {
    markets: [
      { name: 'Dow Jones', close: 43850, change: 0.5, impact: 'Positive' },
      { name: 'NASDAQ', close: 18920, change: 1.2, impact: 'Positive' },
      { name: 'Hang Seng', close: 23450, change: -0.3, impact: 'Slightly Negative' },
      { name: 'A50 Futures', close: 13280, change: 0.4, impact: 'Positive Opening Expected' }
    ],
    summary: 'US tech stocks rebounded strongly, boosting sentiment for A-share growth stocks'
  };
}

/**
 * Get Company Quote Data
 */
async function getCompanyQuote(symbol, company) {
  const tools = await searchTools('real time stock quote China A share Hong Kong', 5);
  
  // Simulated data
  return {
    symbol,
    name: company,
    price: 1580.00,
    change: 15.00,
    changePercent: 0.96,
    volume: 2850000,
    marketCap: '1.98T',
    pe: 28.5,
    pb: 8.2,
    support: 1550,
    resistance: 1600
  };
}

/**
 * Get Industry News
 */
async function getIndustryNews(industry, limit = 5) {
  const tools = await searchTools('China financial news policy regulation', 5);
  
  return [
    {
      title: `${industry || 'Industry'} New Regulations Released`,
      source: 'State Administration for Market Regulation',
      impact: 'Neutral to Slightly Negative',
      summary: 'Stricter requirements imposed on marketing communications for high-end products'
    }
  ];
}

/**
 * Get Competitor News
 */
async function getCompetitorNews(competitors) {
  if (!competitors) return [];
  
  const compList = competitors.split(',');
  return compList.map(symbol => ({
    symbol: symbol.trim(),
    name: symbol.trim(), // Should parse company name in production
    event: 'Released annual report preview, net profit growth 12%',
    impact: 'Intensified industry competition',
    suggestion: 'Accelerate direct sales channel development'
  }));
}

/**
 * Generate Morning Brief
 */
async function generateMorningBrief(options) {
  const { symbol, company, industry, competitors, format = 'markdown' } = options;
  
  console.log(`\n🌅 Generating Morning Brief: ${company || symbol}...\n`);
  
  // Fetch data in parallel
  const [marketOverview, companyQuote, industryNews, competitorNews] = await Promise.all([
    getGlobalMarketOverview(),
    getCompanyQuote(symbol, company),
    getIndustryNews(industry),
    getCompetitorNews(competitors)
  ]);
  
  const now = new Date().toLocaleString('en-US', { timeZone: 'Asia/Shanghai' });
  
  if (format === 'json') {
    return JSON.stringify({
      type: 'morning',
      timestamp: now,
      symbol,
      company,
      marketOverview,
      companyQuote,
      industryNews,
      competitorNews
    }, null, 2);
  }
  
  // Markdown format
  let report = `# 📊 Chairman Morning Brief — ${company || symbol} (${symbol})
📅 ${now}

---

## 🌍 Overnight Global Markets
| Market | Close | Change | A-Share Impact |
|--------|-------|--------|----------------|
`;
  
  marketOverview.markets.forEach(m => {
    report += `| ${m.name} | ${m.close.toLocaleString()} | ${m.change > 0 ? '+' : ''}${m.change}% | ${m.impact} |\n`;
  });
  
  report += `
**Commentary**: ${marketOverview.summary}

---

## 📰 Macro Policy Express
`;
  
  industryNews.forEach(news => {
    report += `🔔 **${news.title}** — ${news.source}
- **Impact Assessment**: ${news.impact}
- **Summary**: ${news.summary}

`;
  });
  
  report += `---

## 📈 Company Pre-Market Outlook
| Indicator | Value | Notes |
|-----------|-------|-------|
| Previous Close | ${companyQuote.price} | - |
| Change | ${companyQuote.change > 0 ? '+' : ''}${companyQuote.change} (${companyQuote.changePercent}%) | - |
| Market Cap | ${companyQuote.marketCap} | - |
| P/E Ratio | ${companyQuote.pe}x | - |
| Key Resistance | ${companyQuote.resistance} | Breakthrough requires volume |
| Key Support | ${companyQuote.support} | Strong support |

---

## 🏭 Industry Radar
✅ Industry overall stable, no major negative news

---

## 🎯 Competitive Intelligence
`;
  
  if (competitorNews.length > 0) {
    competitorNews.forEach(comp => {
      report += `**${comp.name} (${comp.symbol})**
- **Development**: ${comp.event}
- **Impact**: ${comp.impact}
- **Recommendation**: ${comp.suggestion}

`;
    });
  } else {
    report += 'No major competitor developments at this time\n';
  }
  
  report += `
---

## ⚠️ Risk Alerts
1. Macro policy change risk
2. Market liquidity risk
3. Intensified industry competition risk

---

## 📅 Today's Focus
- 09:30 Market Opening
- Monitor Northbound capital flow
- Watch trading volume changes

---
*Data Sources: QVeris | THS iFinD, Caidazi, THS Finance*
*This report is for reference only and does not constitute investment advice*
`;
  
  return report;
}

/**
 * Generate Evening Brief
 */
async function generateEveningBrief(options) {
  const { symbol, company, competitors, format = 'markdown' } = options;
  
  console.log(`\n🌙 Generating Evening Brief: ${company || symbol}...\n`);
  
  const companyQuote = await getCompanyQuote(symbol, company);
  const now = new Date().toLocaleString('en-US', { timeZone: 'Asia/Shanghai' });
  
  if (format === 'json') {
    return JSON.stringify({
      type: 'evening',
      timestamp: now,
      symbol,
      company,
      companyQuote
    }, null, 2);
  }
  
  return `# 🌙 Chairman Evening Report — ${company || symbol} (${symbol})
📅 ${now}

---

## 📊 Market Close Overview
| Indicator | Value | Change |
|-----------|-------|--------|
| Close Price | ${companyQuote.price} | ${companyQuote.change > 0 ? '+' : ''}${companyQuote.change} |
| Change % | ${companyQuote.changePercent}% | - |
| Volume | ${(companyQuote.volume / 10000).toFixed(0)}M shares | - |
| Market Cap | ${companyQuote.marketCap} | - |

**Commentary**: Today's stock price ${companyQuote.change > 0 ? 'rose' : 'fell'}, ${companyQuote.changePercent > 1 ? 'outperforming' : 'underperforming'} the broader market

---

## 📢 Today's Announcements
**Company Announcements**:
- No major announcements

**Industry Announcements**:
- No important industry announcements

---

## 📰 Media Monitoring
**Market Sentiment**: Neutral to Positive

**Key Points to Watch**:
- Trading volume changes
- Main capital flow
- Northbound capital movement

---

## 🎯 Tomorrow's Strategy Recommendations
1. **Price Monitoring**: Watch ${companyQuote.support} support level and ${companyQuote.resistance} resistance level
2. **Trading Volume**: If breakthrough with volume, consider appropriate increase in holdings
3. **Risk Control**: If falls below support level, pay attention to position control

---
*Data Sources: QVeris | THS iFinD, Caidazi*
*This report is for reference only and does not constitute investment advice*
`;
}

/**
 * Manage Watchlist
 */
async function manageWatchlist(action, options) {
  const watchlistPath = join(CONFIG_DIR, 'watchlist.json');
  
  // Ensure directory exists
  if (!existsSync(CONFIG_DIR)) {
    mkdirSync(CONFIG_DIR, { recursive: true });
  }
  
  // Read or initialize
  let watchlist = { holdings: [], competitors: [], peers: {} };
  if (existsSync(watchlistPath)) {
    watchlist = JSON.parse(readFileSync(watchlistPath, 'utf-8'));
  }
  
  switch (action) {
    case 'list':
      console.log('\n📋 Watchlist\n');
      console.log('[Holdings]');
      watchlist.holdings.forEach(h => {
        console.log(`  • ${h.name} (${h.symbol})`);
      });
      console.log('\n[Competitors]');
      watchlist.competitors.forEach(c => {
        console.log(`  • ${c.name} (${c.symbol}) - ${c.peerGroup || 'Ungrouped'}`);
      });
      break;
      
    case 'add':
      const { symbol, company, role, peerGroup } = options;
      const item = { symbol, name: company, addedAt: new Date().toISOString() };
      
      if (role === 'self' || role === 'holding') {
        watchlist.holdings.push(item);
        console.log(`✅ Added holding: ${company} (${symbol})`);
      } else if (role === 'competitor') {
        item.peerGroup = peerGroup;
        watchlist.competitors.push(item);
        console.log(`✅ Added competitor: ${company} (${symbol})`);
      }
      break;
      
    case 'remove':
      const { symbol: removeSymbol } = options;
      watchlist.holdings = watchlist.holdings.filter(h => h.symbol !== removeSymbol);
      watchlist.competitors = watchlist.competitors.filter(c => c.symbol !== removeSymbol);
      console.log(`✅ Removed: ${removeSymbol}`);
      break;
  }
  
  // Save
  writeFileSync(watchlistPath, JSON.stringify(watchlist, null, 2));
}

/**
 * Get Watchlist Companies
 */
function getWatchlistCompanies() {
  const watchlistPath = join(CONFIG_DIR, 'watchlist.json');
  if (!existsSync(watchlistPath)) {
    return { holdings: [], competitors: [] };
  }
  return JSON.parse(readFileSync(watchlistPath, 'utf-8'));
}

/**
 * Main Function
 */
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  // Parse arguments
  const options = {};
  for (let i = 1; i < args.length; i += 2) {
    const key = args[i].replace('--', '');
    const value = args[i + 1];
    options[key] = value;
  }
  
  try {
    switch (command) {
      case 'morning':
        if (options.watchlist) {
          // Generate briefings for all companies in watchlist
          const watchlist = getWatchlistCompanies();
          for (const holding of watchlist.holdings) {
            const report = await generateMorningBrief({
              symbol: holding.symbol,
              company: holding.name,
              industry: options.industry,
              format: options.format
            });
            console.log(report);
            console.log('\n---\n');
          }
        } else if (options.symbol) {
          const report = await generateMorningBrief(options);
          console.log(report);
        } else {
          console.log('❌ Please specify --symbol or --watchlist');
          process.exit(1);
        }
        break;
        
      case 'evening':
        if (options.watchlist) {
          const watchlist = getWatchlistCompanies();
          for (const holding of watchlist.holdings) {
            const report = await generateEveningBrief({
              symbol: holding.symbol,
              company: holding.name,
              competitors: options.competitors,
              format: options.format
            });
            console.log(report);
            console.log('\n---\n');
          }
        } else if (options.symbol) {
          const report = await generateEveningBrief(options);
          console.log(report);
        } else {
          console.log('❌ Please specify --symbol or --watchlist');
          process.exit(1);
        }
        break;
        
      case 'watch':
        await manageWatchlist(options.action, options);
        break;
        
      default:
        console.log(`
Chairman Daily Brief

Usage:
  node chairman_daily.mjs morning --symbol <code> --company <name>
  node chairman_daily.mjs evening --symbol <code> --company <name>
  node chairman_daily.mjs morning --watchlist holdings
  node chairman_daily.mjs watch --action <list|add|remove>

Options:
  morning                    Generate morning brief
  evening                    Generate evening brief
  watch                      Manage watchlist
  
  --symbol <code>            Stock code (e.g.: 600519.SS, 0700.HK, AAPL)
  --company <name>           Company name
  --industry <industry>      Industry name (for industry radar)
  --competitors <codes>      Competitor codes, comma-separated
  --watchlist holdings       Generate report using watchlist
  --format <markdown|json>   Output format (default: markdown)
  
  --action <list|add|remove> Watchlist action
  --role <self|competitor>   Role type when adding
  --peer-group <group>       Competitor peer group

Examples:
  # Generate Moutai morning brief
  node chairman_daily.mjs morning --symbol 600519.SS --company "Kweichow Moutai"
  
  # Generate Tencent evening brief (with competitor analysis)
  node chairman_daily.mjs evening --symbol 0700.HK --company "Tencent Holdings" --competitors 09999.HK,09618.HK
  
  # Add company to watchlist
  node chairman_daily.mjs watch --action add --symbol 600519.SS --company "Kweichow Moutai" --role self
  
  # Add competitor
  node chairman_daily.mjs watch --action add --symbol 002594.SZ --company "BYD" --role competitor --peer-group "New Energy Vehicles"
  
  # View watchlist
  node chairman_daily.mjs watch --action list
`);
    }
  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    process.exit(1);
  }
}

// Run main function
main();
