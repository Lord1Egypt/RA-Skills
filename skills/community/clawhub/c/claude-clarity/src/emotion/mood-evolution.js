/**
 * 心境演化 (Mood Evolution) v2.0.0
 *
 * 升级自 v1.0.0:
 * - Markov 链情绪轨迹预测（对标 StillWater v2.0 前瞻预测引擎）
 * - 与 crisis-level 联动预警
 * - 基线漂移检测
 * - 波动性趋势分析
 * - 前瞻预测（短期/中期/长期）
 * - 情绪转折点检测
 */

class MoodEvolution {
  constructor(options = {}) {
    this.moodSnapshots = [];
    this.moodTrends = [];
    this.maxSnapshots = options.maxSnapshots || 1000;
    this.baseline = null;
    this._crisisLevel = 'low';
    this._baselineDrift = null;

    // Markov 状态转移矩阵（4个情绪状态）
    // 状态: 0=neg_high(负向高唤醒), 1=neg_low(负向低唤醒), 2=pos_high(正向高唤醒), 3=pos_low(正向低唤醒)
    this._transitionMatrix = [
      // →0    →1    →2    →3    (to)
      [0.50,  0.25,  0.10,  0.15], // from 0 (neg_high)
      [0.20,  0.50,  0.15,  0.15], // from 1 (neg_low)
      [0.10,  0.15,  0.50,  0.25], // from 2 (pos_high)
      [0.15,  0.15,  0.25,  0.45]  // from 3 (pos_low)
    ];

    // 状态标签
    this._stateLabels = ['negative_high', 'negative_low', 'positive_high', 'positive_low'];
  }

  /**
   * 设置危机等级（与 autonomous-emotion 联动）
   */
  setCrisisLevel(level) {
    this._crisisLevel = level;
  }

  /**
   * 将 PAD → Markov 状态索引
   */
  _padToState(pad) {
    const { pleasure, arousal } = pad;
    if (pleasure < 0 && arousal > 0) return 0;
    if (pleasure < 0 && arousal <= 0) return 1;
    if (pleasure >= 0 && arousal > 0) return 2;
    return 3;
  }

  /**
   * 状态索引 → 标签
   */
  _stateToLabel(state) {
    return this._stateLabels[state] || 'unknown';
  }

  /**
   * 记录心境快照（增强版）
   */
  snapshot(mood, context = {}) {
    const valence = mood.valence ?? mood.pleasure ?? mood.pleasantness ?? 0;
    const arousal = mood.arousal ?? 0;
    const dominance = mood.dominance ?? 0;

    const snapshot = {
      id: `snapshot-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      mood: typeof mood === 'object' ? mood : { value: mood },
      valence,
      arousal,
      dominance,
      context,
      timestamp: Date.now()
    };

    // Markov 状态
    snapshot.markovState = this._padToState({ pleasure: valence, arousal });
    snapshot.stateLabel = this._stateToLabel(snapshot.markovState);

    this.moodSnapshots.push(snapshot);

    if (this.moodSnapshots.length > this.maxSnapshots) {
      this.moodSnapshots = this.moodSnapshots.slice(-this.maxSnapshots);
    }

    this._updateBaseline();
    this._detectTrend();
    this._updateTransitionMatrix();
    this._detectBaselineDrift();

    return snapshot;
  }

  /**
   * 更新基线（增强版）
   */
  _updateBaseline() {
    if (this.moodSnapshots.length < 10) return;

    const recent = this.moodSnapshots.slice(-50);
    const avgValence = recent.reduce((sum, s) => sum + s.valence, 0) / recent.length;
    const avgArousal = recent.reduce((sum, s) => sum + s.arousal, 0) / recent.length;
    const avgDominance = recent.reduce((sum, s) => sum + s.dominance, 0) / recent.length;

    // 基线漂移检测
    if (this.baseline) {
      this._baselineDrift = {
        valence: avgValence - this.baseline.valence,
        arousal: avgArousal - this.baseline.arousal,
        dominance: avgDominance - (this.baseline.dominance || 0)
      };
    }

    this.baseline = {
      valence: avgValence,
      arousal: avgArousal,
      dominance: avgDominance,
      updatedAt: Date.now()
    };
  }

  /**
   * 基于历史快照更新转移矩阵（在线学习）
   */
  _updateTransitionMatrix() {
    if (this.moodSnapshots.length < 20) return;

    const recent = this.moodSnapshots.slice(-100);
    // 统计状态转移次数
    const transitions = Array(4).fill(null).map(() => Array(4).fill(0));
    const totalFrom = [0, 0, 0, 0];

    for (let i = 1; i < recent.length; i++) {
      const fromState = recent[i - 1].markovState;
      const toState = recent[i].markovState;
      if (fromState !== undefined && toState !== undefined) {
        transitions[fromState][toState]++;
        totalFrom[fromState]++;
      }
    }

    // 归一化
    for (let from = 0; from < 4; from++) {
      if (totalFrom[from] > 0) {
        for (let to = 0; to < 4; to++) {
          this._transitionMatrix[from][to] = transitions[from][to] / totalFrom[from];
        }
      }
    }
  }

  /**
   * 检测基线漂移
   */
  _detectBaselineDrift(threshold = 0.3) {
    if (!this._baselineDrift) return;

    const mag = Math.sqrt(
      this._baselineDrift.valence ** 2 +
      this._baselineDrift.arousal ** 2
    );

    if (mag > threshold) {
      this._driftWarning = {
        drifting: true,
        magnitude: mag,
        threshold,
        direction: this._baselineDrift.valence > 0 ? 'positive' : 'negative',
        details: { ...this._baselineDrift }
      };
    } else {
      this._driftWarning = { drifting: false, magnitude: mag };
    }
  }

  /**
   * 检测趋势
   */
  _detectTrend() {
    if (this.moodSnapshots.length < 5) return;

    const recent = this.moodSnapshots.slice(-10);
    const old = this.moodSnapshots.slice(-20, -10);

    if (old.length < 3) return;

    const recentAvgValence = recent.reduce((sum, s) => sum + s.valence, 0) / recent.length;
    const oldAvgValence = old.reduce((sum, s) => sum + s.valence, 0) / old.length;

    const recentAvgArousal = recent.reduce((sum, s) => sum + s.arousal, 0) / recent.length;
    const oldAvgArousal = old.reduce((sum, s) => sum + s.arousal, 0) / old.length;

    let trend = 'stable';
    if (recentAvgValence - oldAvgValence > 0.1) trend = 'improving';
    else if (recentAvgValence - oldAvgValence < -0.1) trend = 'declining';

    let arousalTrend = 'stable';
    if (recentAvgArousal - oldAvgArousal > 0.15) arousalTrend = 'increasing';
    else if (recentAvgArousal - oldAvgArousal < -0.15) arousalTrend = 'decreasing';

    this.moodTrends.push({
      valenceTrend: trend,
      arousalTrend,
      valenceChange: recentAvgValence - oldAvgValence,
      arousalChange: recentAvgArousal - oldAvgArousal,
      timestamp: Date.now()
    });

    if (this.moodTrends.length > 100) {
      this.moodTrends = this.moodTrends.slice(-100);
    }
  }

  /**
   * 获取当前趋势
   */
  getCurrentTrend() {
    if (this.moodTrends.length === 0) return null;
    return this.moodTrends[this.moodTrends.length - 1];
  }

  /**
   * 获取基线
   */
  getBaseline() {
    return this.baseline;
  }

  /**
   * 获取基线漂移
   */
  getBaselineDrift() {
    return this._baselineDrift ? {
      valence: this._baselineDrift.valence.toFixed(3),
      arousal: this._baselineDrift.arousal.toFixed(3),
      magnitude: Math.sqrt(this._baselineDrift.valence ** 2 + this._baselineDrift.arousal ** 2).toFixed(3),
      drifting: this._driftWarning?.drifting || false
    } : null;
  }

  /**
   * 计算与基线的偏差
   */
  getDeviation(currentMood) {
    if (!this.baseline) return null;

    const valence = currentMood.valence ?? currentMood.pleasure ?? 0;
    const arousal = currentMood.arousal ?? 0;

    return {
      valenceDeviation: valence - this.baseline.valence,
      arousalDeviation: arousal - this.baseline.arousal,
      magnitude: Math.sqrt(
        (valence - this.baseline.valence) ** 2 +
        (arousal - this.baseline.arousal) ** 2
      )
    };
  }

  /**
   * Markov 链轨迹预测（核心方法）
   */
  predictTrajectory(steps = 5) {
    if (this.moodSnapshots.length < 5) {
      return { error: '数据不足，无法预测', available: this.moodSnapshots.length };
    }

    // 当前状态 = 最新快照的 Markov 状态
    const currentState = this.moodSnapshots[this.moodSnapshots.length - 1].markovState;
    const trajectory = [];

    const state = currentState;
    let stateProb = [1, 0, 0, 0]; // 当前状态概率分布

    // 危机等级影响：危机时预测更保守
    const crisisFactor = this._crisisLevel === 'critical' ? 0.5 :
                        this._crisisLevel === 'high' ? 0.7 : 1.0;

    for (let i = 1; i <= steps; i++) {
      // 计算下一步概率分布
      const nextProb = [0, 0, 0, 0];
      for (let from = 0; from < 4; from++) {
        for (let to = 0; to < 4; to++) {
          nextProb[to] += stateProb[from] * this._transitionMatrix[from][to];
        }
      }

      // 取概率最高的状态
      let maxProb = 0, dominantState = 0;
      for (let s = 0; s < 4; s++) {
        if (nextProb[s] > maxProb) {
          maxProb = nextProb[s];
          dominantState = s;
        }
      }

      // 计算期望 PAD（加权平均）
      const statePads = [
        { pleasure: -0.7, arousal: 0.5 },  // neg_high
        { pleasure: -0.4, arousal: -0.3 }, // neg_low
        { pleasure: 0.6, arousal: 0.4 },   // pos_high
        { pleasure: 0.3, arousal: -0.2 }  // pos_low
      ];

      const expectedPad = { pleasure: 0, arousal: 0 };
      for (let s = 0; s < 4; s++) {
        expectedPad.pleasure += nextProb[s] * statePads[s].pleasure;
        expectedPad.arousal += nextProb[s] * statePads[s].arousal;
      }

      trajectory.push({
        step: i,
        predictedState: this._stateToLabel(dominantState),
        confidence: maxProb * crisisFactor,
        probability: nextProb.map((p, s) => ({ state: this._stateToLabel(s), probability: p })),
        expectedPad: {
          pleasure: expectedPad.pleasure.toFixed(2),
          arousal: expectedPad.arousal.toFixed(2)
        }
      });

      // 更新状态分布
      stateProb = nextProb;
    }

    return { trajectory, currentState: this._stateToLabel(currentState), steps };
  }

  /**
   * 查询状态转移概率
   */
  getTransitionProbability(from, to) {
    const fromIdx = this._stateLabels.indexOf(from);
    const toIdx = this._stateLabels.indexOf(to);
    if (fromIdx === -1 || toIdx === -1) return null;
    return this._transitionMatrix[fromIdx][toIdx];
  }

  /**
   * 获取危机预警
   */
  getCrisisWarning() {
    if (this.moodSnapshots.length < 5) return { crisis: false };

    // 检测连续负面情绪
    const recent = this.moodSnapshots.slice(-5);
    const negativeCount = recent.filter(s => s.valence < 0).length;

    // 检测情绪持续下降
    let decliningStreak = 0;
    for (let i = 1; i < recent.length; i++) {
      if (recent[i].valence < recent[i - 1].valence) decliningStreak++;
    }

    // 检测高波动性
    const volatility = this._calculateVolatility();
    const highVolatility = volatility > 0.3;

    // 综合预警
    const warning = {
      crisis: this._crisisLevel === 'high' || this._crisisLevel === 'critical',
      crisisLevel: this._crisisLevel,
      signals: [],
      riskScore: 0,
      recommendations: []
    };

    if (negativeCount >= 3) {
      warning.signals.push('连续负面情绪');
      warning.riskScore += 0.3;
    }
    if (decliningStreak >= 3) {
      warning.signals.push('情绪持续下降');
      warning.riskScore += 0.3;
    }
    if (highVolatility) {
      warning.signals.push('情绪高波动');
      warning.riskScore += 0.2;
    }
    if (this._driftWarning?.drifting) {
      warning.signals.push('基线漂移');
      warning.riskScore += 0.2;
    }

    // 风险分数超过阈值
    if (warning.riskScore >= 0.5) {
      warning.recommendations.push('建议关注情绪状态变化');
    }
    if (warning.riskScore >= 0.7) {
      warning.recommendations.push('建议寻求专业支持');
    }

    return warning;
  }

  /**
   * 波动性趋势
   */
  getVolatilityTrend() {
    if (this.moodSnapshots.length < 20) return null;

    const recent = this.moodSnapshots.slice(-50, -25);
    const older = this.moodSnapshots.slice(-100, -50);

    if (recent.length < 5 || older.length < 5) return null;

    const recentVol = this._calcVolatilityForSet(recent);
    const olderVol = this._calcVolatilityForSet(older);

    const change = recentVol - olderVol;
    return {
      trend: change > 0.05 ? 'increasing' : change < -0.05 ? 'decreasing' : 'stable',
      change: change.toFixed(3),
      recentVol: recentVol.toFixed(3),
      olderVol: olderVol.toFixed(3)
    };
  }

  _calcVolatilityForSet(snapshots) {
    const valences = snapshots.map(s => s.valence);
    const mean = valences.reduce((a, b) => a + b, 0) / valences.length;
    const variance = valences.map(v => (v - mean) ** 2).reduce((a, b) => a + b, 0) / valences.length;
    return Math.sqrt(variance);
  }

  /**
   * 情绪稳定性评分
   */
  getEmotionalStability() {
    const volatility = this._calculateVolatility();
    const stability = Math.max(0, 1 - volatility * 2);
    return {
      stability: Math.min(1, stability).toFixed(2),
      volatility: volatility.toFixed(3),
      level: stability > 0.8 ? 'high' : stability > 0.5 ? 'medium' : 'low'
    };
  }

  /**
   * 前瞻预测（短期/中期/长期）
   */
  getFutureOutlook() {
    if (this.moodSnapshots.length < 5) return { error: '数据不足' };

    const shortTerm = this.predictTrajectory(3);
    const mediumTerm = this.predictTrajectory(7);
    const currentTrend = this.getCurrentTrend();
    const volatilityTrend = this.getVolatilityTrend();

    // 趋势推断
    let shortTermOutlook, mediumTermOutlook;

    if (currentTrend?.valenceTrend === 'improving') {
      shortTermOutlook = '积极向好';
    } else if (currentTrend?.valenceTrend === 'declining') {
      shortTermOutlook = '需要注意';
    } else {
      shortTermOutlook = '相对稳定';
    }

    // 中期趋势判断
    if (shortTerm.trajectory && mediumTerm.trajectory) {
      const lastShort = shortTerm.trajectory[shortTerm.trajectory.length - 1];
      const lastMedium = mediumTerm.trajectory[mediumTerm.trajectory.length - 1];
      if (lastMedium.expectedPad.pleasure > lastShort.expectedPad.pleasure) {
        mediumTermOutlook = '持续改善';
      } else if (lastMedium.expectedPad.pleasure < lastShort.expectedPad.pleasure) {
        mediumTermOutlook = '可能回落';
      } else {
        mediumTermOutlook = '维持稳定';
      }
    } else {
      mediumTermOutlook = '趋势不明';
    }

    return {
      shortTerm: {
        outlook: shortTermOutlook,
        dominantState: shortTerm.trajectory?.[2]?.predictedState || 'unknown',
        confidence: shortTerm.trajectory?.[2]?.confidence || 0
      },
      mediumTerm: {
        outlook: mediumTermOutlook,
        dominantState: mediumTerm.trajectory?.[6]?.predictedState || 'unknown',
        confidence: mediumTerm.trajectory?.[6]?.confidence || 0
      },
      longTerm: {
        outlook: mediumTermOutlook,
        trend: currentTrend?.valenceTrend || 'unknown'
      },
      trend: currentTrend,
      volatilityTrend
    };
  }

  /**
   * 情绪转折点检测
   */
  getTurningPoints() {
    if (this.moodSnapshots.length < 10) return { turningPoints: [], hasUpcoming: false };

    const recent = this.moodSnapshots.slice(-20);
    const turningPoints = [];

    for (let i = 2; i < recent.length; i++) {
      const prev = recent[i - 2];
      const curr = recent[i - 1];
      const next = recent[i];

      // 检测趋势反转
      const delta1 = curr.valence - prev.valence;
      const delta2 = next.valence - curr.valence;

      if (delta1 > 0 && delta2 < 0) {
        // 高点
        turningPoints.push({
          type: 'peak',
          timestamp: curr.timestamp,
          valence: curr.valence,
          relative: 'high'
        });
      } else if (delta1 < 0 && delta2 > 0) {
        // 低点
        turningPoints.push({
          type: 'trough',
          timestamp: curr.timestamp,
          valence: curr.valence,
          relative: 'low'
        });
      }
    }

    // 预测下一个转折点
    const trajectory = this.predictTrajectory(5);
    let nextTurningPoint = null;

    if (trajectory.trajectory && trajectory.trajectory.length >= 3) {
      const t = trajectory.trajectory;
      for (let i = 1; i < t.length - 1; i++) {
        const p1 = parseFloat(t[i - 1].expectedPad.pleasure);
        const p2 = parseFloat(t[i].expectedPad.pleasure);
        const p3 = parseFloat(t[i + 1].expectedPad.pleasure);
        if ((p2 > p1 && p2 > p3) || (p2 < p1 && p2 < p3)) {
          nextTurningPoint = {
            predictedAt: `step ${i + 1}`,
            type: p2 > p1 ? 'predicted_peak' : 'predicted_trough',
            expectedPleasure: p2
          };
          break;
        }
      }
    }

    return {
      turningPoints: turningPoints.slice(-5),
      hasUpcoming: !!nextTurningPoint,
      nextTurningPoint,
      count: turningPoints.length
    };
  }

  /**
   * 基于预测推荐干预措施
   */
  getRecommendedInterventions() {
    const warning = this.getCrisisWarning();
    const stability = this.getEmotionalStability();
    const future = this.getFutureOutlook();
    const interventions = [];

    if (warning.crisis || warning.riskScore >= 0.5) {
      interventions.push({
        priority: 'high',
        type: 'containment',
        action: '情绪确认',
        description: '先接住情绪，不急于分析'
      });
    }

    if (stability.level === 'low') {
      interventions.push({
        priority: 'medium',
        type: 'stabilization',
        action: '稳定性训练',
        description: '呼吸练习或正念冥想'
      });
    }

    if (future.shortTerm?.outlook === '需要注意') {
      interventions.push({
        priority: 'medium',
        type: 'exploration',
        action: '开放式探索',
        description: '温和地询问感受，支持表达'
      });
    }

    if (warning.signals.includes('情绪高波动')) {
      interventions.push({
        priority: 'medium',
        type: 'grounding',
        action: '接地练习',
        description: '帮助回到当下，减少焦虑'
      });
    }

    if (interventions.length === 0) {
      interventions.push({
        priority: 'low',
        type: 'maintenance',
        action: '保持现状',
        description: '当前状态良好，维持现有策略'
      });
    }

    return {
      interventions,
      crisisWarning: warning,
      stability
    };
  }

  /**
   * 获取历史快照
   */
  getSnapshots(since = null, limit = 50) {
    let snapshots = this.moodSnapshots;
    if (since) snapshots = snapshots.filter(s => s.timestamp >= since);
    return snapshots.slice(-limit);
  }

  /**
   * 获取统计
   */
  getStats() {
    if (this.moodSnapshots.length === 0) {
      return {
        totalSnapshots: 0,
        baseline: null,
        currentTrend: null,
        averageValence: 0,
        averageArousal: 0,
        volatility: 0
      };
    }

    const recent = this.moodSnapshots.slice(-100);
    return {
      totalSnapshots: this.moodSnapshots.length,
      baseline: this.baseline,
      currentTrend: this.getCurrentTrend(),
      averageValence: recent.reduce((sum, s) => sum + s.valence, 0) / recent.length,
      averageArousal: recent.reduce((sum, s) => sum + s.arousal, 0) / recent.length,
      volatility: this._calculateVolatility(),
      crisisLevel: this._crisisLevel,
      baselineDrift: this.getBaselineDrift(),
      stability: this.getEmotionalStability()
    };
  }

  /**
   * 计算波动性
   */
  _calculateVolatility() {
    if (this.moodSnapshots.length < 10) return 0;
    const recent = this.moodSnapshots.slice(-50);
    const valences = recent.map(s => s.valence);
    const mean = valences.reduce((a, b) => a + b, 0) / valences.length;
    const variance = valences.map(v => (v - mean) ** 2).reduce((a, b) => a + b, 0) / valences.length;
    return Math.sqrt(variance);
  }

  /**
   * 获取时间段内的平均心境
   */
  getAverageForPeriod(startTime, endTime) {
    const snapshots = this.moodSnapshots.filter(
      s => s.timestamp >= startTime && s.timestamp <= endTime
    );
    if (snapshots.length === 0) return null;
    return {
      valence: snapshots.reduce((sum, s) => sum + s.valence, 0) / snapshots.length,
      arousal: snapshots.reduce((sum, s) => sum + s.arousal, 0) / snapshots.length,
      dominance: snapshots.reduce((sum, s) => sum + s.dominance, 0) / snapshots.length,
      count: snapshots.length
    };
  }

  /**
   * 重置
   */
  reset() {
    this.moodSnapshots = [];
    this.moodTrends = [];
    this.baseline = null;
    this._baselineDrift = null;
    this._crisisLevel = 'low';
  }
}

module.exports = { MoodEvolution };