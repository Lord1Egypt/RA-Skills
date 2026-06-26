/**
 * 数据采集模块 v2.1 (稳定版)
 * 支持：模拟数据 + 可选API扩展
 */

class DataCollector {
  constructor() {
    this.cache = new Map();
    this.cacheExpiry = 5 * 60 * 1000;
    
    // API Keys (可通过环境变量配置)
    this.apiKeys = {
      football: process.env.FOOTBALL_API_KEY || null,
      openweather: process.env.OPENWEATHER_API_KEY || null
    };
  }

  /**
   * 采集单场比赛数据
   */
  async collect(match) {
    console.log('[DataCollector] 采集数据:', match.home, 'vs', match.away);
    
    // 并行采集（使用模拟数据作为后备）
    const [oddsData, teamData, h2hData, weatherData] = await Promise.all([
      this.getOdds(match),
      this.getTeamData(match),
      this.getHeadToHead(match),
      this.getWeather(match)
    ].map(p => p.catch(e => null)));

    return {
      match: match,
      odds: oddsData || this.getMockOdds(),
      teams: teamData || this.getMockTeamData(match),
      head2head: h2hData || this.getMockH2H(),
      weather: weatherData || this.getMockWeather(),
      source: oddsData ? 'api' : 'mock',
      collected_at: new Date().toISOString()
    };
  }

  // ========== 赔率数据 ==========

  async getOdds(match) {
    // 如果有API Key，尝试获取真实数据
    if (this.apiKeys.football) {
      try {
        const odds = await this.fetchFromFootballAPI(match, this.apiKeys.football);
        if (odds) return odds;
      } catch (e) {
        console.log('[DataCollector] API获取失败，使用模拟数据');
      }
    }
    return this.getMockOdds();
  }

  async fetchFromFootballAPI(match, apiKey) {
    // 简化版API调用
    return null; // 暂时返回null使用模拟数据
  }

  // ========== 球队数据 ==========

  async getTeamData(match) {
    return this.getMockTeamData(match);
  }

  // ========== 历史交锋 ==========

  async getHeadToHead(match) {
    return this.getMockH2H();
  }

  // ========== 天气数据 ==========

  async getWeather(match) {
    return this.getMockWeather();
  }

  // ========== 今日比赛 ==========

  async getTodayMatches() {
    return this.getMockTodayMatches();
  }

  // ========== 比赛结果 ==========

  async getResults(matchIds) {
    // 返回模拟结果（实际需要接入比分API）
    return matchIds.map(id => ({
      match_id: id,
      home_score: Math.floor(Math.random() * 4),
      away_score: Math.floor(Math.random() * 3),
      status: 'finished'
    }));
  }

  // ========== 模拟数据生成器 ==========

  getMockOdds() {
    const homeOdds = this.random(1.6, 3.5);
    const drawOdds = this.random(2.8, 4.0);
    const awayOdds = this.random(2.0, 6.0);
    
    return {
      european: { home: homeOdds, draw: drawOdds, away: awayOdds },
      asian: {
        handicap: [-0.5, -0.25, 0, 0.25, 0.5][Math.floor(Math.random() * 5)],
        home_odds: this.random(0.8, 1.1),
        away_odds: this.random(0.8, 1.1)
      },
      overUnder: {
        line: 2.5,
        over: this.random(0.8, 1.1),
        under: this.random(0.8, 1.1)
      },
      trend: ['rising', 'falling', 'stable'][Math.floor(Math.random() * 3)],
      change_percent: Math.random() * 10
    };
  }

  getMockTeamData(match) {
    return {
      home: this.getMockTeam(match.home),
      away: this.getMockTeam(match.away)
    };
  }

  getMockTeam(name) {
    return {
      name: name,
      recent_form: this.generateForm(5),
      recent_goals_for: Math.floor(Math.random() * 15),
      recent_goals_against: Math.floor(Math.random() * 10),
      home_record: {
        played: 10,
        won: Math.floor(Math.random() * 8),
        drawn: Math.floor(Math.random() * 3),
        lost: 10 - Math.floor(Math.random() * 8) - Math.floor(Math.random() * 3)
      },
      injuries: Math.floor(Math.random() * 3),
      missing: []
    };
  }

  getMockH2H() {
    const matches = Math.floor(Math.random() * 10) + 3;
    return {
      total_matches: matches,
      home_wins: Math.floor(Math.random() * matches * 0.4),
      away_wins: Math.floor(Math.random() * matches * 0.4),
      draws: matches - Math.floor(Math.random() * matches * 0.4) - Math.floor(Math.random() * matches * 0.4),
      recent_results: this.generateForm(5),
      avg_goals: (Math.random() * 2 + 1.5).toFixed(1)
    };
  }

  getMockWeather() {
    const conditions = ['晴', '多云', '阴', '小雨'];
    return {
      condition: conditions[Math.floor(Math.random() * conditions.length)],
      temperature: Math.floor(Math.random() * 15) + 10,
      humidity: Math.floor(Math.random() * 40) + 40,
      wind: Math.floor(Math.random() * 15)
    };
  }

  getMockTodayMatches() {
    return [
      { league: '英超', home: '曼联', away: '利物浦', time: '20:30' },
      { league: '西甲', home: '皇马', away: '巴萨', time: '03:00' },
      { league: '意甲', home: '国米', away: '尤文', time: '03:45' }
    ];
  }

  // ========== 工具方法 ==========

  random(min, max) {
    return parseFloat((Math.random() * (max - min) + min).toFixed(2));
  }

  generateForm(count) {
    const results = ['胜', '平', '负'];
    return Array(count).fill(0).map(() => results[Math.floor(Math.random() * 3)]);
  }
}

module.exports = DataCollector;
