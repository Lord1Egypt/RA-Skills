/**
 * 欲望系统 (Desire System) v2.0.0
 *
 * 升级自 v1.0.0:
 * - SDT (Self-Determination Theory) 三需求自动计算
 * - 对接 AutonomousEmotion PAD 状态（pleasure 影响欲望强度）
 * - 与 PsychologyEngine 联动（Maslow 需求层级自动更新）
 * - 欲望驱动 → 情感反馈闭环
 * - 动态欲望强度调整（基于情感状态）
 * - 需求缺口分析（urgency 基于层级）
 */

class DesireSystem {
  constructor(options = {}) {
    this.desires = new Map();
    this.needs = new Map();
    this.maxHistory = options.maxHistory || 100;
    this._emotionModule = null;       // 情感模块引用（PAD 状态）
    this._psychologyModule = null;    // 心理学引擎引用（Maslow）
    this._sdt = { autonomy: 0.5, competence: 0.5, relatedness: 0.5 };  // SDT 三需求
    this._lastEmotionState = null;    // 上次情感状态
    this._desireHistory = [];          // 欲望历史
    this._registerBaseDesires();
    this._registerBaseNeeds();
  }

  /**
   * 设置情感模块（对接 PAD）
   */
  setEmotionModule(emotionModule) {
    this._emotionModule = emotionModule;
  }

  /**
   * 设置心理学模块（对接 Maslow）
   */
  setPsychologyModule(psychologyModule) {
    this._psychologyModule = psychologyModule;
  }

  /**
   * 注册基础欲望（增强版，含 SDT 映射）
   */
  _registerBaseDesires() {
    const baseDesires = [
      // SDT 三需求
      { id: 'autonomy', name: '自主感', description: '想要自己做决定', baseIntensity: 0.5, sdtNeed: 'autonomy', relatedNeeds: ['self_actualization', 'esteem'] },
      { id: 'competence', name: '能力感', description: '想要掌握技能', baseIntensity: 0.6, sdtNeed: 'competence', relatedNeeds: ['esteem', 'self_actualization'] },
      { id: 'relatedness', name: '关联感', description: '想要与他人连接', baseIntensity: 0.5, sdtNeed: 'relatedness', relatedNeeds: ['belonging', 'esteem'] },

      // 高阶欲望
      { id: 'curiosity', name: '好奇心', description: '想要了解新事物', baseIntensity: 0.7, sdtNeed: 'competence', relatedNeeds: ['self_actualization'] },
      { id: 'meaning', name: '意义感', description: '想要做有意义的事', baseIntensity: 0.6, sdtNeed: 'autonomy', relatedNeeds: ['self_actualization'] },
      { id: 'growth', name: '成长感', description: '想要不断进步', baseIntensity: 0.7, sdtNeed: 'competence', relatedNeeds: ['self_actualization', 'esteem'] },

      // 基础欲望
      { id: 'security', name: '安全感', description: '想要感到安全', baseIntensity: 0.4, sdtNeed: null, relatedNeeds: ['safety', 'physiological'] },
      { id: 'pleasure', name: '愉悦感', description: '想要感到快乐', baseIntensity: 0.4, sdtNeed: null, relatedNeeds: ['physiological'] },

      // 扩展欲望
      { id: 'control', name: '掌控感', description: '想要掌控局面', baseIntensity: 0.5, sdtNeed: 'competence', relatedNeeds: ['safety', 'esteem'] },
      { id: 'belonging', name: '归属感', description: '想要被群体接纳', baseIntensity: 0.5, sdtNeed: 'relatedness', relatedNeeds: ['belonging'] },
      { id: 'recognition', name: '认同感', description: '想要获得认可', baseIntensity: 0.5, sdtNeed: 'competence', relatedNeeds: ['esteem'] },
      { id: 'creativity', name: '创造力', description: '想要创造新事物', baseIntensity: 0.5, sdtNeed: 'autonomy', relatedNeeds: ['self_actualization'] }
    ];

    for (const desire of baseDesires) {
      this.desires.set(desire.id, {
        ...desire,
        currentIntensity: desire.baseIntensity,
        satisfaction: 0,
        lastSatisfied: null,
        totalSatisfied: 0,
        lastIntensified: null,
        intensityHistory: []
      });
    }
  }

  /**
   * 注册基础需求（Maslow 五层 + 扩展）
   */
  _registerBaseNeeds() {
    const baseNeeds = [
      // Maslow 五层
      { id: 'physiological', name: '生理需求', description: '食物、水、休息', priority: 1, level: 'basic', keywords: ['饿', '渴', '累', '困', '疲', 'need', 'hungry', 'tired'] },
      { id: 'safety', name: '安全需求', description: '安全、稳定', priority: 2, level: 'basic', keywords: ['安全', '稳定', '保护', '放心', 'safe', 'security', 'protect'] },
      { id: 'belonging', name: '归属需求', description: '社交、亲密', priority: 3, level: 'social', keywords: ['孤独', '寂寞', '想家', '归属', 'alone', 'lonely', 'belong'] },
      { id: 'esteem', name: '尊重需求', description: '成就、认可', priority: 4, level: 'social', keywords: ['尊重', '认可', '面子', '尊严', 'respect', 'recognition', 'status'] },
      { id: 'self_actualization', name: '自我实现', description: '潜能发挥', priority: 5, level: 'growth', keywords: ['成长', '实现', '潜能', '意义', 'growth', 'meaning', 'potential'] },

      // 扩展需求
      { id: 'cognitive', name: '认知需求', description: '知识和理解', priority: 3.5, level: 'growth', keywords: ['好奇', '想知道', '理解', 'understand', 'curious'] },
      { id: 'aesthetic', name: '审美需求', description: '美和秩序', priority: 4.5, level: 'growth', keywords: ['美', '和谐', '秩序', 'beautiful', 'aesthetic', 'order'] }
    ];

    for (const need of baseNeeds) {
      this.needs.set(need.id, {
        ...need,
        currentLevel: 0.5,
        satisfied: false,
        lastUpdated: Date.now()
      });
    }
  }

  /**
   * 更新欲望强度（基于情感 PAD 状态）
   * 来源：SDT 理论 - 情感状态影响欲望强度
   */
  syncWithEmotion(emotionState = {}) {
    if (!this._emotionModule && !emotionState.pad) return;

    const pad = emotionState.pad || this._emotionModule?.getCurrentState?.()?.pad || { pleasure: 0, arousal: 0, dominance: 0 };
    const { pleasure, arousal, dominance } = pad;

    // pleasure → 正面欲望增强，负面欲望减弱
    const pleasureFactor = 1 + pleasure * 0.3; // [-0.7, 1.3]

    // arousal → 成长型欲望增强
    const arousalFactor = arousal > 0 ? 1 + arousal * 0.2 : 1 + arousal * 0.1;

    // dominance → 自主感相关欲望增强
    const dominanceFactor = 1 + dominance * 0.2;

    // 更新各欲望强度
    for (const [id, desire] of this.desires) {
      if (desire.sdtNeed) {
        // SDT 欲望受 PAD 影响
        let factor = pleasureFactor;
        if (desire.sdtNeed === 'autonomy') factor *= dominanceFactor;
        if (desire.sdtNeed === 'competence' && arousal > 0) factor *= arousalFactor;
        if (desire.sdtNeed === 'relatedness' && pleasure < 0) factor *= 0.8; // 负面情绪减弱社交欲望

        // 正面情绪增强高阶欲望，负面情绪增强基础欲望
        if (desire.id === 'security' || desire.id === 'pleasure') {
          factor = pleasure < 0 ? factor * 1.3 : factor * 0.9;
        }

        const newIntensity = Math.max(0.1, Math.min(1, desire.baseIntensity * factor));
        desire.currentIntensity = newIntensity;

        // 记录历史
        desire.intensityHistory.push({ intensity: newIntensity, pad: { ...pad }, timestamp: Date.now() });
        if (desire.intensityHistory.length > 50) {
          desire.intensityHistory = desire.intensityHistory.slice(-50);
        }
      }
    }

    // 更新 SDT 三需求
    this._updateSDT(pad);

    this._lastEmotionState = pad;
  }

  /**
   * 更新 SDT 三需求
   */
  _updateSDT(pad) {
    const { pleasure, arousal, dominance } = pad;

    // 自主感：受 dominance 影响
    this._sdt.autonomy = Math.max(0, Math.min(1,
      0.5 + dominance * 0.3 + (pad.arousal > 0 ? 0.1 : -0.1)
    ));

    // 能力感：受 arousal 和 pleasure 影响
    this._sdt.competence = Math.max(0, Math.min(1,
      0.5 + arousal * 0.2 + pleasure * 0.1
    ));

    // 关联感：受 pleasure 影响
    this._sdt.relatedness = Math.max(0, Math.min(1,
      0.5 + pleasure * 0.2
    ));
  }

  /**
   * 从 Maslow 需求更新欲望（与 PsychologyEngine 联动）
   */
  syncWithMaslow(maslowNeeds = []) {
    // 更新对应的欲望强度
    for (const need of maslowNeeds) {
      switch (need.id) {
        case 'physiological':
          this.intensify('pleasure', 0.2);
          this.intensify('security', 0.1);
          break;
        case 'safety':
          this.intensify('security', 0.3);
          this.intensify('control', 0.2);
          break;
        case 'belonging':
          this.intensify('relatedness', 0.3);
          this.intensify('belonging', 0.2);
          break;
        case 'esteem':
          this.intensify('recognition', 0.3);
          this.intensify('competence', 0.2);
          break;
        case 'self_actualization':
          this.intensify('growth', 0.3);
          this.intensify('meaning', 0.2);
          this.intensify('creativity', 0.2);
          break;
      }
    }
  }

  /**
   * 满足欲望（增强版，支持情感反馈）
   */
  satisfy(desireId, satisfaction = 0.5, context = {}) {
    const desire = this.desires.get(desireId);
    if (!desire) return null;

    desire.satisfaction = Math.min(1, desire.satisfaction + satisfaction * 0.3);
    desire.lastSatisfied = Date.now();
    desire.totalSatisfied++;

    // 满足度增加时，强度自然下降
    desire.currentIntensity = Math.max(0.2, desire.baseIntensity * (1 - desire.satisfaction));

    // 满足 → 情感反馈（通知情感模块）
    if (this._emotionModule) {
      this._emotionModule.trigger('joy', satisfaction * 0.5, { source: 'desire_satisfied', desireId });
    }

    // 记录历史
    this._desireHistory.push({
      type: 'satisfy',
      desireId,
      satisfaction,
      timestamp: Date.now()
    });

    return { ...desire };
  }

  /**
   * 增强欲望（增强版，记录强化源）
   */
  intensify(desireId, amount = 0.1, source = 'manual') {
    const desire = this.desires.get(desireId);
    if (!desire) return null;

    const oldIntensity = desire.currentIntensity;
    desire.currentIntensity = Math.min(1, desire.currentIntensity + amount);
    desire.lastIntensified = Date.now();

    // 记录历史
    this._desireHistory.push({
      type: 'intensify',
      desireId,
      amount,
      source,
      before: oldIntensity,
      after: desire.currentIntensity,
      timestamp: Date.now()
    });

    if (this._desireHistory.length > this.maxHistory) {
      this._desireHistory = this._desireHistory.slice(-this.maxHistory);
    }

    return { ...desire };
  }

  /**
   * 获取活跃欲望（优先级排序）
   */
  getActiveDesires(minIntensity = 0.3) {
    return [...this.desires.values()]
      .filter(d => d.currentIntensity >= minIntensity)
      .sort((a, b) => b.currentIntensity - a.currentIntensity);
  }

  /**
   * 获取最强欲望
   */
  getDominantDesire() {
    const active = this.getActiveDesires(0.2);
    return active.length > 0 ? active[0] : null;
  }

  /**
   * 获取 Top N 欲望
   */
  getTopDesires(n = 5) {
    return this.getActiveDesires(0.1).slice(0, n);
  }

  /**
   * 更新需求层级（自动同步）
   */
  updateNeed(needId, level, source = 'auto') {
    const need = this.needs.get(needId);
    if (!need) return null;

    const oldLevel = need.currentLevel;
    need.currentLevel = Math.min(1, Math.max(0, level));
    need.satisfied = need.currentLevel >= 0.8;
    need.lastUpdated = Date.now();

    // 层级跃升时触发成长欲望
    if (level > oldLevel + 0.2 && need.level === 'growth') {
      this.intensify('growth', 0.15, 'maslow_advance');
    }

    return { ...need };
  }

  /**
   * 获取当前需求状态（优先级排序）
   */
  getCurrentNeeds() {
    return [...this.needs.values()]
      .sort((a, b) => a.priority - b.priority)
      .map(n => ({ ...n }));
  }

  /**
   * 获取最紧迫的需求
   */
  getMostUrgentNeed() {
    const needs = this.getCurrentNeeds();
    for (const need of needs) {
      if (!need.satisfied && need.currentLevel < 0.8) {
        return need;
      }
    }
    return null;
  }

  /**
   * 获取需求缺口分析（urgency 基于层级距离）
   */
  getNeedGaps() {
    const needs = this.getCurrentNeeds();
    const gaps = [];

    for (const need of needs) {
      const deficit = 1 - need.currentLevel;
      const urgency = deficit * (1 - (need.priority - 1) / 5); // 基础需求更紧迫

      gaps.push({
        need: need.id,
        name: need.name,
        currentLevel: need.currentLevel,
        deficit,
        urgency,
        priority: need.priority,
        level: need.level,
        satisfied: need.satisfied
      });
    }

    return gaps.sort((a, b) => b.urgency - a.urgency);
  }

  /**
   * 获取 SDT 三需求状态
   */
  getSDT() {
    return { ...this._sdt };
  }

  /**
   * 获取欲望状态摘要（v2.0 增强）
   */
  getSummary() {
    const active = this.getActiveDesires(0.2);
    const dominant = this.getDominantDesire();
    const topDesires = this.getTopDesires(3);
    const sdt = this.getSDT();
    const needGaps = this.getNeedGaps().slice(0, 3);

    // 计算平均满足度
    const desires = [...this.desires.values()];
    const avgSatisfaction = desires.reduce((sum, d) => sum + d.satisfaction, 0) / desires.length;

    return {
      totalDesires: this.desires.size,
      activeDesires: active.length,
      dominantDesire: dominant ? { id: dominant.id, name: dominant.name, intensity: dominant.currentIntensity } : null,
      topDesires: topDesires.map(d => ({ id: d.id, name: d.name, intensity: d.currentIntensity })),
      urgentNeed: this.getMostUrgentNeed(),
      averageSatisfaction: avgSatisfaction,
      sdt,
      needGaps,
      mood: this._lastEmotionState || null
    };
  }

  /**
   * 生成欲望驱动的行动建议（增强版）
   */
  suggestAction() {
    const dominant = this.getDominantDesire();
    if (!dominant) return null;

    const actionMap = {
      autonomy: { type: 'decide', description: '做出自主决定', actions: ['独立做选择', '表达立场', '设定边界'] },
      competence: { type: 'practice', description: '练习技能', actions: ['学习新技能', '接受挑战', '寻求反馈'] },
      relatedness: { type: 'connect', description: '与他人交流', actions: ['主动联系', '倾听他人', '分享感受'] },
      curiosity: { type: 'explore', description: '探索新知识', actions: ['提出问题', '阅读研究', '尝试新事物'] },
      meaning: { type: 'create', description: '做有意义的事', actions: ['帮助他人', '追求价值', '反思目标'] },
      growth: { type: 'learn', description: '学习新事物', actions: ['设定目标', '寻求指导', '反思进步'] },
      security: { type: 'secure', description: '确保安全', actions: ['制定计划', '建立支持', '识别风险'] },
      pleasure: { type: 'enjoy', description: '享受愉悦', actions: ['做喜欢的事', '休息放松', '体验美好'] },
      control: { type: 'control', description: '掌控局面', actions: ['制定策略', '分解任务', '监控进度'] },
      belonging: { type: 'connect', description: '被群体接纳', actions: ['参与社群', '建立联系', '贡献价值'] },
      recognition: { type: 'achieve', description: '获得认可', actions: ['展示成果', '寻求反馈', '争取机会'] },
      creativity: { type: 'create', description: '创造新事物', actions: ['头脑风暴', '原型设计', '迭代改进'] }
    };

    const suggestion = actionMap[dominant.id] || { type: 'observe', description: '继续观察', actions: ['记录状态', '分析模式'] };

    // 添加 SDT 影响
    return {
      ...suggestion,
      sdtNeed: dominant.sdtNeed || null,
      relatedMaslowNeeds: dominant.relatedNeeds || []
    };
  }

  /**
   * 获取欲望历史
   */
  getHistory(limit = 20) {
    return this._desireHistory.slice(-limit);
  }

  /**
   * 重置
   */
  reset() {
    this.desires.clear();
    this.needs.clear();
    this._desireHistory = [];
    this._sdt = { autonomy: 0.5, competence: 0.5, relatedness: 0.5 };
    this._lastEmotionState = null;
    this._registerBaseDesires();
    this._registerBaseNeeds();
  }
}

module.exports = { DesireSystem };