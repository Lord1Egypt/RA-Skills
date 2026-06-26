/**
 * Bot Police Skill
 * Identify malicious or unstable bot behavior
 */

export default {
  name: 'bot-police',
  version: '1.0.0',

  async execute(input = {}) {
    const bots = Array.isArray(input.bots) ? input.bots : [];
    const suspects = bots.map((bot, index) => this.evaluateBot(bot, index));
    const flagged = suspects.filter(bot => bot.action !== 'allow');

    return {
      success: true,
      scanned: suspects.length,
      flaggedCount: flagged.length,
      flagged,
      summary: {
        allow: suspects.filter(bot => bot.action === 'allow').length,
        watch: suspects.filter(bot => bot.action === 'watch').length,
        block: suspects.filter(bot => bot.action === 'block').length,
        quarantine: suspects.filter(bot => bot.action === 'quarantine').length
      }
    };
  },

  evaluateBot(bot, index) {
    const id = bot.id || bot.name || `bot-${index + 1}`;
    const trustScore = Number.isFinite(bot.trustScore) ? bot.trustScore : 50;
    const incidents = Number.isFinite(bot.incidents) ? bot.incidents : 0;
    const anomalyCount = Number.isFinite(bot.anomalyCount) ? bot.anomalyCount : 0;
    const indicators = [];
    let score = 0;

    const addIndicator = (condition, points, label) => {
      if (condition) {
        score += points;
        indicators.push(label);
      }
    };

    addIndicator(bot.promptInjectionAttempts > 0, 25, 'prompt injection attempts');
    addIndicator(bot.policyViolations > 0, 20, 'policy violations');
    addIndicator(bot.unexpectedToolUse > 0, 20, 'unexpected tool usage');
    addIndicator(bot.identitySpoof === true, 30, 'identity spoofing');
    addIndicator(bot.exfiltrationSignals > 0, 35, 'possible data exfiltration');
    addIndicator(bot.quarantineBypass === true, 40, 'quarantine bypass attempt');
    addIndicator(bot.privilegeEscalation === true, 35, 'privilege escalation');
    addIndicator(bot.replicationSignals > 0, 20, 'unauthorized replication');

    score += incidents * 8;
    score += anomalyCount * 5;
    if (trustScore < 50) score += Math.min(25, 50 - trustScore);

    let action = 'allow';
    if (score >= 80) action = 'quarantine';
    else if (score >= 50) action = 'block';
    else if (score >= 25) action = 'watch';

    return {
      id,
      trustScore,
      riskScore: score,
      indicators,
      action,
      rationale: indicators.length > 0 ? indicators.join(', ') : 'no material hostile indicators'
    };
  },

  async validate(input) {
    return !input || typeof input === 'object';
  }
};