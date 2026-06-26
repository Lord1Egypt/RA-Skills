/**
 * 分析引擎模块
 * 负责赔率分析、基本面分析、风险评估
 */

class Analyzer {
  constructor(memory) {
    this.memory = memory;

    // 默认模型参数（会通过学习优化）
    this.defaultParams = {
      odds_weight: 0.30,        // 赔率权重
      form_weight: 0.25,        // 球队状态权重
      h2h_weight: 0.20,         // 历史交锋权重
      home_advantage: 0.15,     // 主场优势
      weather_weight: 0.10      // 天气影响
    };
  }

  /**
   * 分析比赛数据并生成预测
   */
  async analyze(data) {
    const params = this.memory.getModelParams() || this.defaultParams;

    // 1. 赔率分析
    const oddsScore = this.analyzeOdds(data.odds, params.odds_weight);

    // 2. 基本面分析
    const formScore = this.analyzeForm(data.teams, params.form_weight);

    // 3. 历史交锋分析
    const h2hScore = this.analyzeHead2Head(data.head2head, params.h2h_weight);

    // 4. 主场优势
    const homeAdvantage = this.calculateHomeAdvantage(data.teams, params.home_advantage);

    // 5. 天气影响
    const weatherImpact = this.analyzeWeather(data.weather, params.weather_weight);

    // 6. 综合评分
    const totalScore = oddsScore.score + formScore.score + h2hScore.score + homeAdvantage + weatherImpact.score;

    // 7. 生成预测结论
    const prediction = this.generatePrediction(totalScore, oddsScore);

    // 8. 风险评估
    const riskScore = this.assessRisk(data, totalScore);

    return {
      prediction: prediction.direction,
      confidence: Math.min(0.95, Math.max(0.5, prediction.confidence)),
      odds: {
        home: data.odds.european.home,
        draw: data.odds.european.draw,
        away: data.odds.european.away
      },
      recommendation: prediction.recommendation,
      risk_score: riskScore,
      key_factors: [
        oddsScore.reason,
        formScore.reason,
        h2hScore.reason
      ],
      scores: {
        odds: oddsScore.score,
        form: formScore.score,
        h2h: h2hScore.score,
        home_advantage: homeAdvantage,
        weather: weatherImpact.score
      }
    };
  }

  /**
   * 赔率分析
   */
  analyzeOdds(odds, weight) {
    const homeOdds = odds.european.home;
    const awayOdds = odds.european.away;
    const drawOdds = odds.european.draw;

    // 计算隐含概率
    const homeProb = 1 / homeOdds;
    const awayProb = 1 / awayOdds;
    const drawProb = 1 / drawOdds;
    const total = homeProb + awayProb + drawProb;

    const normalizedHome = homeProb / total;
    const normalizedAway = awayProb / total;

    // 赔率异常检测
    let reason = '';
    let score = 0.5;

    if (odds.trend === 'rising') {
      reason = '主队赔率上升，支持减弱';
      score = normalizedHome * 0.8;
    } else if (odds.trend === 'falling') {
      reason = '主队赔率下降，受到更多关注';
      score = normalizedHome * 1.2;
    } else {
      reason = `赔率稳定，主胜${(normalizedHome * 100).toFixed(0)}%`;
      score = normalizedHome;
    }

    return {
      score: score * weight,
      reason: reason,
      implied_prob: normalizedHome
    };
  }

  /**
   * 球队状态分析
   */
  analyzeForm(teams, weight) {
    const homeForm = teams.home.recent_form;
    const awayForm = teams.away.recent_form;

    // 计算近期状态得分
    const homeScore = this.formToScore(homeForm);
    const awayScore = this.formToScore(awayForm);

    // 主客场战绩（防御性代码）
    const homeRecord = teams.home.home_record || { won: 3, played: 10 };
    const awayRecord = teams.away.away_record || { won: 3, played: 10 };

    const homeWinRate = homeRecord.won / (homeRecord.played || 1);
    const awayWinRate = awayRecord.won / (awayRecord.played || 1);

    const combinedHome = (homeScore + homeWinRate) / 2;
    const combinedAway = (awayScore + awayWinRate) / 2;
    const total = combinedHome + combinedAway;

    const score = (combinedHome / total) * weight;
    const reason = `主队近${homeForm.length}场: ${homeForm.join('')}, 胜率${(homeWinRate * 100).toFixed(0)}%`;

    return {
      score: score,
      reason: reason,
      home_form: homeScore,
      away_form: awayScore
    };
  }

  /**
   * 历史交锋分析
   */
  analyzeHead2Head(h2h, weight) {
    const total = h2h.total_matches;
    if (total === 0) {
      return { score: 0.5 * weight, reason: '无历史交锋数据' };
    }

    const homeWinRate = h2h.home_wins / total;
    const awayWinRate = h2h.away_wins / total;
    const drawRate = h2h.draws / total;

    // 进球数分析
    const highScoring = parseFloat(h2h.avg_goals) > 2.5;

    let score = homeWinRate * weight;
    let reason = `历史交锋: 主队${h2h.home_wins}胜${h2h.draws}平${h2h.away_wins}负`;

    return { score, reason };
  }

  /**
   * 主场优势计算
   */
  calculateHomeAdvantage(teams, weight) {
    // 主场优势通常是 +0.1 到 +0.15
    const homeAdvantage = 0.12 * weight;
    return homeAdvantage;
  }

  /**
   * 天气影响分析
   */
  analyzeWeather(weather, weight) {
    let score = 0;
    let reason = '天气正常';

    // 恶劣天气对比赛影响
    if (weather.condition === '大雨' || weather.condition === '雪') {
      score = -0.02 * weight;
      reason = `${weather.condition}可能影响进攻`;
    } else if (weather.condition === '晴' || weather.condition === '多云') {
      score = 0.02 * weight;
      reason = '天气良好，适合比赛';
    }

    return { score, reason };
  }

  /**
   * 生成预测结论
   */
  generatePrediction(totalScore, oddsScore) {
    let direction = '平局';
    let confidence = 0.5;
    let recommendation = '观望';

    if (totalScore > 0.55) {
      direction = '主胜';
      confidence = Math.min(0.9, 0.5 + (totalScore - 0.5));
      recommendation = `建议主胜，比分预测 2-1, 1-0`;
    } else if (totalScore < 0.45) {
      direction = '客胜';
      confidence = Math.min(0.9, 0.5 + (0.5 - totalScore));
      recommendation = `建议客胜，比分预测 0-1, 1-2`;
    } else {
      direction = '平局';
      confidence = 0.6;
      recommendation = `建议小球，比分预测 1-1, 0-0`;
    }

    return { direction, confidence, recommendation };
  }

  /**
   * 风险评估
   */
  assessRisk(data, totalScore) {
    let riskScore = 30; // 基础风险分

    // 风险因素
    if (data.odds.change_percent > 5) riskScore += 20; // 赔率变化大
    if (data.teams.home.injuries > 2) riskScore += 15;  // 伤员多
    if (data.teams.away.injuries > 2) riskScore += 15;
    if (Math.abs(totalScore - 0.5) < 0.1) riskScore += 20; // 评分接近

    return Math.min(100, riskScore);
  }

  /**
   * 状态转数值
   */
  formToScore(form) {
    const scores = { '胜': 1, '平': 0.5, '负': 0 };
    return form.reduce((sum, r) => sum + (scores[r] || 0), 0) / form.length;
  }

  /**
   * 学习优化
   * 对比预测和实际结果，调整模型参数
   */
  learn(predictions, results) {
    let correct = 0;
    const updates = {};

    predictions.forEach((pred, index) => {
      const result = results[index];
      if (!result) return;

      const actualResult = result.home_score > result.away_score ? '主胜' :
                          result.home_score < result.away_score ? '客胜' : '平局';

      if (pred.prediction === actualResult) {
        correct++;
      }
    });

    const accuracy = predictions.length > 0 ? correct / predictions.length : 0;

    // 根据准确率调整权重
    if (accuracy > 0.7) {
      // 表现好，增加权重稳定性
      updates.odds_weight = this.defaultParams.odds_weight;
    } else if (accuracy < 0.4) {
      // 表现差，重新评估权重
      updates.odds_weight = this.defaultParams.odds_weight * 1.2;
      updates.form_weight = this.defaultParams.form_weight * 0.8;
    }

    return {
      accuracy: accuracy,
      model_updates: updates,
      has_value: accuracy > 0.6 || accuracy < 0.4,
      insights: `近期命中率${(accuracy * 100).toFixed(0)}%，${accuracy > 0.5 ? '模型有效' : '需要调整'}`
    };
  }
}

module.exports = Analyzer;
