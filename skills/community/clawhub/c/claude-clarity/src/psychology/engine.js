/**
 * PsychologyEngine — 深度心理学引擎 v2.0.0（修复版）
 *
 * 整合自 mark-StillWater psychology.js（四层感知模型）与三个扩展模块：
 * - BigFivePersonality — 大五人格 OCEAN 模型（对象字面量）
 * - EmpathyAssessment — IRI 共情四维度评估（对象字面量）
 * - IntentionTracker — 意图追踪与偏差提醒
 *
 * ⚠️ 临床免责声明
 * 心虫是 AI 认知引擎，不提供医疗诊断、治疗或临床心理健康服务。
 * 任何心理健康相关的分析和建议仅供参考，不能替代专业心理医生
 * 或精神科医生的诊断和治疗。
 */

const psychology = require('../core/psychology.js');
const empathy = require('./empathy-detector.js');
const BigFivePersonality = require('../core/BigFivePersonality.js');
const EmpathyAssessment = require('../core/EmpathyAssessment.js');
const { intentionTracker } = require('../core/IntentionTracker.js');

/**
 * 深拷贝对象字面量，使每个引擎实例拥有独立的可修改副本
 * @param {object} obj - 源对象（对象字面量或类实例）
 * @returns {object} 拥有独立维度数据的新副本
 */
function cloneModule(obj) {
  const clone = Object.create(Object.getPrototypeOf(obj));
  for (const key of Object.keys(obj)) {
    const val = obj[key];
    if (key === 'dimensions' && val && typeof val === 'object') {
      clone[key] = typeof structuredClone === 'function'
        ? structuredClone(val)
        : JSON.parse(JSON.stringify(val));
    } else if (typeof val === 'function') {
      clone[key] = val.bind ? val.bind(clone) : val;
    } else {
      clone[key] = val;
    }
  }
  return clone;
}

class PsychologyEngine {
    constructor(memory) {
        this.memory = memory;
        this._crisisCount = 0;
        // BigFivePersonality 和 EmpathyAssessment 是对象字面量，需要克隆
        this._bigFive = cloneModule(BigFivePersonality);
        this._empathyAssessment = cloneModule(EmpathyAssessment);
        this._intentionTracker = intentionTracker; // singleton class
    }

    // ═══════════════════════════════════════════════════════════════
    // 1. 原有四层心理分析（intention/emotion/needs/defense/crisis）
    // ═══════════════════════════════════════════════════════════════

    /**
     * 完整心理分析
     * @param {string} input - 用户输入
     * @param {object} context - 上下文
     * @returns {object} 综合心理分析结果
     */
    analyzePsychology(input, context = {}) {
        const result = psychology.analyzePsychology(input, context);
        return {
            intention: result.intent,
            emotion: result.pad,
            needs: result.needs,
            defense: result.defenses,
            crisis: result.crisis,
            summary: result.summary,
            recommendations: result.recommendations,
            primaryNeed: result.primaryNeed,
            primaryDefense: result.primaryDefense,
            _clinicalDisclaimer: result._clinicalDisclaimer
        };
    }

    /**
     * 分类用户交互
     */
    classify(input) {
        const result = psychology.analyzePsychology(input);
        let category = result.intent.category;
        if (!category || category === 'unknown') {
            category = result.pad.pleasure > 0 ? 'positive_interaction'
                     : result.pad.pleasure < 0 ? 'negative_interaction'
                     : 'neutral';
        }
        return {
            category,
            emotion: result.pad.emotion,
            crisisLevel: result.crisis.level,
            confidence: result.intent.confidence
        };
    }

    /**
     * 检测危机等级
     */
    checkCrisis(input) {
        return psychology.assessCrisisLevel(input);
    }

    /**
     * 获取PAD情绪状态
     */
    getPAD(input) {
        return psychology.detectPADFromText(input);
    }

    /**
     * 检测Maslow需求
     */
    getNeeds(input) {
        return psychology.detectMaslowNeeds(input);
    }

    /**
     * 检测防御机制
     */
    getDefenses(input) {
        return psychology.detectDefenseMechanisms(input);
    }

    /**
     * 检测共情水平
     * 来源: Decety & Jackson (2004) - The Functional Architecture of Human Empathy
     */
    getEmpathy(input) {
        return empathy.detectEmpathy(input);
    }

    /**
     * 重置危机计数
     */
    resetCrisisCounter() {
        this._crisisCount = 0;
        psychology.resetCrisisCounter();
        return { reset: true };
    }

    // ═══════════════════════════════════════════════════════════════
    // 2. 扩展：大五人格 OCEAN
    // ═══════════════════════════════════════════════════════════════

    /**
     * 大五人格分析 — 从文本中推断人格特征
     * @param {string} input - 输入文本
     * @returns {object} 大五人格分析报告
     */
    analyzePersonality(input) {
        if (!input) return { error: '缺少输入文本' };

        const text = input;

        // 基于文本直接分析大五人格（多指标累加）
        const scores = { O: 5, C: 5, E: 5, A: 5, N: 5 };

        // 开放性 (O) — 好奇心、创造力、新体验
        const oPatterns = [
            /想法|思考|想象|创意|创造|创新|尝试|探索|发现|好奇|新鲜/, 0.4,
            /学习|研究|阅读|知识|智慧|理解|分析/, 0.3,
            /艺术|音乐|哲学|科学|理论|抽象/, 0.3,
            /变化|不同|独特|特别|新颖|有趣/, 0.2,
            /传统|习惯|固定|一成不变|老样子|照旧/, -0.3,
        ];
        // 尽责性 (C) — 自律、计划、目标导向
        const cPatterns = [
            /计划|安排|目标|完成|坚持|自律|认真|负责|仔细|按时/, 0.4,
            /组织|整理|秩序|步骤|流程|方法/, 0.3,
            /拖延|懒|随意|马虎|粗心|随便|应付/, -0.4,
            /截止|期限|承诺|保证|务必|一定/, 0.2,
        ];
        // 外向性 (E) — 社交性、活力、表达
        const ePatterns = [
            /朋友|社交|聚会|聊天|分享|交流|讨论|合作|团队/, 0.4,
            /大家|我们|一起|共同|参与|活跃/, 0.3,
            /外向|开朗|热情|活力|能量|兴奋/, 0.3,
            /独处|一个人|安静|沉默|内向|害羞|避免/, -0.4,
            /独自|单独|自己|宅|不想说话/, -0.2,
        ];
        // 宜人性 (A) — 合作、同理心、信任
        const aPatterns = [
            /帮助|支持|理解|关心|照顾|体贴|善意|友好|信任|合作/, 0.4,
            /同理心|共情|体谅|包容|宽容|原谅/, 0.3,
            /大家|共同|一起|互助|团结/, 0.2,
            /批评|指责|抱怨|讨厌|反感|怀疑|防备|攻击/, -0.4,
            /竞争|对立|冲突|愤怒|报复/, -0.3,
        ];
        // 神经质 (N) — 情绪波动、焦虑、压力敏感
        const nPatterns = [
            /焦虑|担心|紧张|恐惧|害怕|恐慌|不安|忐忑|压力|崩溃/, 0.5,
            /情绪|波动|敏感|脆弱|低落|抑郁|沮丧|难过|痛苦|委屈/, 0.4,
            /情绪稳定|冷静|淡定|从容|平和|成熟|坚强/, -0.3,
            /容易|经常|总是|一直|反复/, 0.1,
        ];

        // 应用所有匹配的模式（累加权重）
        const applyPatterns = (patterns, dim) => {
            for (let i = 0; i < patterns.length; i += 2) {
                if (patterns[i].test(text)) {
                    scores[dim] = Math.max(1, Math.min(10, scores[dim] + patterns[i + 1]));
                }
            }
        };

        applyPatterns(oPatterns, 'O');
        applyPatterns(cPatterns, 'C');
        applyPatterns(ePatterns, 'E');
        applyPatterns(aPatterns, 'A');
        applyPatterns(nPatterns, 'N');

        // 写入 BigFive 实例
        Object.entries(scores).forEach(([dim, score]) => {
            this._bigFive.updateScore(dim, score);
        });

        return {
            profile: this._bigFive.getProfile(),
            report: this._bigFive.generateReport(),
            dominant: this._dominantTrait(this._bigFive.getProfile()),
        };
    }

    /** @private 取最突出的维度 */
    _dominantTrait(profile) {
        const dims = profile.dimensions || profile;
        let max = -Infinity, key = '';
        for (const [k, v] of Object.entries(dims)) {
            const score = v.score || v || 0;
            if (score > max) { max = score; key = k; }
        }
        return { dimension: key || 'conscientiousness', score: max };
    }

    // ═══════════════════════════════════════════════════════════════
    // 3. 扩展：共情评估（IRI 四维度）
    // ═══════════════════════════════════════════════════════════════

    /**
     * 共情评估 — 从文本评估共情水平
     * @param {string} input - 输入文本
     * @returns {object} 共情评估报告
     */
    assessEmpathy(input) {
        if (!input) return { error: '缺少输入文本' };

        const text = input;
        let pt = 0, fs = 0, ec = 0, pd = 0;

        // 观点采择 (PT) — 理解他人想法和感受
        const ptPatterns = [
            /他.*?感受|她.*?感受|别人.*?想法|别人.*?感受|他人.*?视角/,
            /如果.*?会|站在.*?角度|换位思考|理解.*?立场/,
            /我觉得.*?也会|可以理解|能够体会|感同身受/,
            /他的.*?原因|她的.*?想法|背后的.*?故事/,
        ];
        //  fantasy (FS) — 移情想象
        const fsPatterns = [
            /电影|书籍|小说|故事|角色|情节|感动|打动|流泪/,
            /想象.*?场景|虚拟|虚构|代入|共情/,
            /艺术|音乐|诗歌|散文|文学/,
        ];
        // 共情关怀 (EC) — 关心他人福祉
        const ecPatterns = [
            /帮助|关心|照顾|支持|关爱|善意|温暖|心疼|可怜|同情/,
            /需要.*?帮助|给予.*?支持|提供.*?关怀/,
            /不幸|困难|痛苦|挣扎|困境|挫折/,
        ];
        // 个人痛苦 (PD) — 对他人痛苦的焦虑反应
        const pdPatterns = [
            /焦虑|不安|担忧|心疼|难受|心痛|不忍/,
            /看到.*?难过|听到.*?悲伤|面对.*?痛苦/,
            /不忍心|看不下去|于心不忍/,
        ];

        ptPatterns.forEach(p => { if (p.test(text)) pt += 1; });
        fsPatterns.forEach(p => { if (p.test(text)) fs += 1; });
        ecPatterns.forEach(p => { if (p.test(text)) ec += 1; });
        pdPatterns.forEach(p => { if (p.test(text)) pd += 1; });

        // 标准化到 1-5 分
        const normalize = (v) => Math.min(5, Math.max(1, v + 2));
        const totalScore = normalize(pt) + normalize(fs) + normalize(ec) + normalize(pd);
        const avgScore = Math.round(totalScore / 4);

        return {
            quickAssessment: {
                type: 'text-based',
                dimensions: {
                    PT: { score: normalize(pt), description: pt > 0 ? '表现出对他人视角的理解能力' : '较少体现观点采择' },
                    FS: { score: normalize(fs), description: fs > 0 ? '具有移情想象能力' : '较少体现移情想象' },
                    EC: { score: normalize(ec), description: ec > 0 ? '表现出共情关怀倾向' : '较少体现关怀倾向' },
                    PD: { score: normalize(pd), description: pd > 0 ? '对他人痛苦有情感反应' : '较少体现个人痛苦' },
                },
                totalScore: totalScore,
                averageScore: avgScore,
                level: avgScore >= 4 ? '高' : avgScore >= 3 ? '中等' : '较低',
            },
            full: this._empathyAssessment.interpretScore(avgScore * 10),
            state: this._empathyAssessment.getState(),
        };
    }

    // ═══════════════════════════════════════════════════════════════
    // 4. 扩展：意图追踪
    // ═══════════════════════════════════════════════════════════════

    /**
     * 意图追踪 — 检测对话意图是否偏离目标
     * @param {string} input - 输入文本
     * @returns {object} 意图追踪报告
     */
    trackIntention(input) {
        if (!input) return { error: '缺少输入文本' };

        const domain = this._intentionTracker.detectDomain(input);
        const keywords = this._intentionTracker.extractKeywords(input);
        const deviation = this._intentionTracker.checkDeviation(input, domain);
        const nudge = this._intentionTracker.generateNudge(deviation);

        return {
            domain,
            keywords,
            deviation,
            nudge: deviation?.deviated ? nudge : null,
            progress: this._intentionTracker.getProgress(),
            goalSummary: this._intentionTracker.generateProgressReport(),
        };
    }

    // ═══════════════════════════════════════════════════════════════
    // 5. 综合分析：大五 + 共情 + 意图全融合
    // ═══════════════════════════════════════════════════════════════

    /**
     * 综合深度心理学分析
     * 融合四层感知 + 大五人格 + 共情评估 + 意图追踪
     * @param {string} input - 输入文本
     * @returns {object} 深度心理学分析报告
     */
    analyzeDeep(input) {
        if (!input) return { error: '缺少输入文本' };

        const base = this.analyzePsychology(input);
        const personality = this.analyzePersonality(input);
        const empathyEval = this.assessEmpathy(input);
        const intention = this.trackIntention(input);

        // 合成摘要
        const profile = personality.profile?.dimensions || personality.profile || {};
        const dominantTrait = typeof personality.dominant?.dimension === 'string'
            ? personality.dominant.dimension : '未知';
        const empathyLevel = empathyEval.full?.level || '未评估';

        let synthesis = `【深度心理画像】大五人格主导维度: ${dominantTrait}`;
        synthesis += `; 当前情绪: ${base.emotion?.emotion || '中性'}`;
        synthesis += `; 共情水平: ${empathyLevel}`;
        if (intention.deviation?.deviated) {
            synthesis += `; 意图偏离提醒: ${intention.deviation.reason || '对话方向偏移'}`;
        }

        return {
            base,
            personality,
            empathy: empathyEval,
            intention,
            synthesis,
            crisisDetected: base.crisis?.level !== 'low' && base.crisis?.level !== 'none',
        };
    }

    // ═══════════════════════════════════════════════════════════════
    // 引擎状态
    // ═══════════════════════════════════════════════════════════════

    getPsychologyStats() {
        return {
            enabled: true,
            version: 'v2.0.0',
            perceptionLayers: ['intention', 'emotion', 'needs', 'defense', 'crisis', 'empathy'],
            deepLayers: ['bigFivePersonality', 'empathyIRI', 'intentionTracking'],
            padModel: psychology.PAD_MODEL,
            crisisLevels: psychology.CRISIS_LEVELS,
            defenseMechanisms: Object.keys(psychology.DEFENSE_MECHANISMS).length,
            maslowTiers: 8,
            empathyArchitecture: ['emotionalContagion', 'empathicConcern', 'perspectiveTaking', 'selfOtherDistinction'],
            bigFiveReady: typeof this._bigFive?.getProfile === 'function',
            empathyIRIReady: typeof this._empathyAssessment?.getState === 'function',
            intentionTrackerReady: !!this._intentionTracker,
        };
    }
}

module.exports = { PsychologyEngine };
