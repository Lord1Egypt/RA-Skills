const fs = require('fs');

const STOP_WORDS = new Set([
  'the',
  'and',
  'for',
  'with',
  'this',
  'that',
  'from',
  'into',
  'onto',
  'have',
  'has',
  'had',
  'was',
  'were',
  'are',
  'is',
  'been',
  'being',
  'will',
  'would',
  'should',
  'could',
  'a',
  'an',
  'of',
  'to',
  'in',
  'on',
  'at',
  'by',
  'we',
  'it',
  'its',
  'our',
  'their',
  '目前',
  '当前',
  '现在',
  '这个',
  '那个',
  '这周',
  '上周',
  '本周',
  '本月',
  '已经',
  '以及',
  '还有',
  '然后',
  '一个'
]);

const TOPIC_IGNORE = new Set([
  '需要',
  '完成',
  '改为',
  '计划',
  '新增',
  '反复',
  '指出',
  '之前',
  '现在',
  '问题',
  '核心',
  '当前',
  '本周',
  '这周',
  '上周',
  '已经',
  '必须'
]);

class ChangeBrief {
  readText(filePath, inlineText, label) {
    if (filePath) {
      return fs.readFileSync(filePath, 'utf-8');
    }
    if (typeof inlineText === 'string' && inlineText.trim()) {
      return inlineText;
    }
    throw new Error(`Please provide --${label}-file or --${label}-text`);
  }

  readPair(input = {}) {
    return {
      before: this.readText(input['before-file'], input['before-text'], 'before'),
      after: this.readText(input['after-file'], input['after-text'], 'after')
    };
  }

  normalizeText(text) {
    return String(text || '').replace(/\r\n/g, '\n').trim();
  }

  unique(items) {
    const seen = new Set();
    const output = [];

    for (const item of items) {
      const value = String(item || '').trim();
      if (!value) {
        continue;
      }
      if (seen.has(value)) {
        continue;
      }
      seen.add(value);
      output.push(value);
    }

    return output;
  }

  shorten(text, maxLength = 68) {
    const value = String(text || '').trim().replace(/\s+/g, ' ');
    if (value.length <= maxLength) {
      return value;
    }
    return `${value.slice(0, maxLength - 3)}...`;
  }

  normalizeStatementKey(line) {
    return this.normalizeText(line)
      .toLowerCase()
      .replace(/\s+/g, ' ')
      .replace(/[，。；;！？?!、,:："'`]/g, '')
      .trim();
  }

  collectStatements(text) {
    const normalized = this.normalizeText(text);
    const pieces = normalized
      .split('\n')
      .flatMap((line) => line.split(/[。！？?!；;，,]/g))
      .map((line) => line.replace(/^\s*[-*•\d.)]+\s*/, '').trim())
      .map((line) => line.replace(/\s+/g, ' ').trim())
      .filter((line) => line.length >= 2);

    return this.unique(pieces);
  }

  extractTokens(text) {
    const raw = String(text || '').toLowerCase().match(/[a-z0-9]+|[\u4e00-\u9fff]+/g) || [];
    const tokens = [];

    for (const chunk of raw) {
      if (STOP_WORDS.has(chunk)) {
        continue;
      }

      if (/^[\u4e00-\u9fff]+$/.test(chunk)) {
        if (chunk.length <= 2) {
          tokens.push(chunk);
          continue;
        }

        tokens.push(chunk);
        for (let i = 0; i < chunk.length - 1; i += 1) {
          const bigram = chunk.slice(i, i + 2);
          if (!STOP_WORDS.has(bigram)) {
            tokens.push(bigram);
          }
        }
        continue;
      }

      if (chunk.length >= 2) {
        tokens.push(chunk);
      }
    }

    return this.unique(tokens);
  }

  sharedTokens(tokensA, tokensB) {
    const setB = new Set(tokensB);
    return tokensA.filter((token) => setB.has(token));
  }

  similarity(metaA, metaB) {
    const shared = this.sharedTokens(metaA.tokens, metaB.tokens);
    const minLength = Math.max(1, Math.min(metaA.tokens.length || 1, metaB.tokens.length || 1));
    let score = shared.length / minLength;

    const strongShared = shared.filter((token) => token.length >= 3);
    if (strongShared.length > 0) {
      score += 0.18;
    }

    const a = metaA.line.toLowerCase();
    const b = metaB.line.toLowerCase();
    if (a.includes(b) || b.includes(a)) {
      score += 0.12;
    }

    return Math.min(1, score);
  }

  scoreImportance(line, numbers) {
    let score = 1;

    if (/风险|合规|法务|审批|安全审查|blocker|blocked|risk|security|legal|incident|outage/i.test(line)) {
      score += 4;
    }
    if (/上线|发布|beta|roadmap|路线图|排期|deadline|本周|本月|延期|改为|时间线|launch|release|timeline|ship/i.test(line)) {
      score += 3;
    }
    if (/客户|用户|销售|营收|收入|转化|成本|预算|需求|模板|pricing|customer|user|revenue|budget|conversion/i.test(line)) {
      score += 2;
    }
    if (/新增|新签|开始|加入|增加|支持|要求|必须|优先|立即|需要|变成|不再|失效|new|added|introduced|required|urgent|must/i.test(line)) {
      score += 2;
    }
    if ((numbers || []).length > 0) {
      score += 1;
    }

    return score;
  }

  scoreAction(line) {
    let score = 0;

    if (/先|立即|马上|安排|确认|更新|同步|修复|通知|决定|拍板|发起|补上|调整|回滚|推进|review|notify|update|decide|approve|fix|ship/i.test(line)) {
      score += 3;
    }
    if (/需要|必须|本周|优先|blocker|risk|deadline|法务|审批|安全审查|客户要求|冲突/i.test(line)) {
      score += 2;
    }

    return score;
  }

  classifyLine(line) {
    const normalized = String(line || '').trim();
    const lower = normalized.toLowerCase();
    const numbers = normalized.match(/\d+(?:\.\d+)?(?:%|天|周|月|小时|h|d|w|m)?/g) || [];
    const negative = /不支持|失败|延迟|延期|取消|下线|风险|阻塞|禁止|下降|不再|失效|blocker|blocked|delay|cancel|deprecated|risk/i.test(lower);
    const positive = /支持|通过|上线|增长|完成|可用|允许|降低|缩短|稳定|更快|enable|pass|launch|improve|available/i.test(lower);

    return {
      line: normalized,
      key: this.normalizeStatementKey(normalized),
      tokens: this.extractTokens(normalized),
      numbers,
      importance: this.scoreImportance(normalized, numbers),
      actionScore: this.scoreAction(normalized),
      positive,
      negative,
      blocker: /风险|法务|合规|安全审查|审批|blocker|blocked|security|legal|incident|outage/i.test(lower),
      needsDecision: /拍板|决定|取舍|冲突|待定|待确认|需要确认|需要决定|tradeoff|choose|decision/i.test(lower),
      staleCandidate: /结论|假设|计划|预计|默认|无需|已确认|判断|路线图|roadmap|assumption|plan|default/i.test(lower),
      timeline: /上线|发布|beta|roadmap|路线图|排期|deadline|本周|本月|月底|中旬|下周|timeline|launch|release|ship/i.test(lower),
      audience: /客户|用户|销售|老板|团队|法务|安全|工程|设计|运营|大客户|customer|user|sales|team/i.test(lower)
    };
  }

  hasNumberChange(beforeMeta, afterMeta) {
    if (beforeMeta.numbers.length === 0 || afterMeta.numbers.length === 0) {
      return false;
    }

    return beforeMeta.numbers.join('|') !== afterMeta.numbers.join('|');
  }

  hasPolarityFlip(beforeMeta, afterMeta) {
    if (/无需|不需要|不必|不会|不能/.test(beforeMeta.line) && /需要|必须|先完成/.test(afterMeta.line)) {
      return true;
    }
    if (/支持|允许|可用/.test(beforeMeta.line) && /不支持|禁止|下线/.test(afterMeta.line)) {
      return true;
    }
    if (/延期|取消|不再/.test(beforeMeta.line) && /上线|恢复|重新启动/.test(afterMeta.line)) {
      return true;
    }
    if (/上线|完成|可用|支持/.test(beforeMeta.line) && /延期|取消|blocker|风险|不再/.test(afterMeta.line)) {
      return true;
    }

    return (beforeMeta.positive && afterMeta.negative) || (beforeMeta.negative && afterMeta.positive);
  }

  topicLabel(beforeMeta, afterMeta) {
    const shared = this.sharedTokens(beforeMeta.tokens, afterMeta.tokens)
      .filter((token) => token.length >= 2 && !TOPIC_IGNORE.has(token))
      .sort((a, b) => b.length - a.length);

    if (shared.length > 0) {
      return shared[0];
    }

    return this.shorten(afterMeta.line, 24);
  }

  hasStrongSharedTopic(beforeMeta, afterMeta) {
    return this.sharedTokens(beforeMeta.tokens, afterMeta.tokens)
      .some((token) => token.length >= 4 && !TOPIC_IGNORE.has(token));
  }

  buildChangedPair(beforeMeta, afterMeta, similarity) {
    const reasons = [];

    if (this.hasNumberChange(beforeMeta, afterMeta)) {
      reasons.push(beforeMeta.timeline || afterMeta.timeline ? '时间线或关键数字变了' : '关键数字变了');
    }
    if (this.hasPolarityFlip(beforeMeta, afterMeta)) {
      reasons.push('判断方向反转');
    }
    if (!beforeMeta.blocker && afterMeta.blocker) {
      reasons.push('出现了新的 blocker 或风险');
    }
    if (!beforeMeta.audience && afterMeta.audience) {
      reasons.push('影响范围变大了');
    }
    if (reasons.length === 0) {
      reasons.push('同一主题出现了新说法');
    }

    return {
      before: beforeMeta.line,
      after: afterMeta.line,
      beforeMeta,
      afterMeta,
      topic: this.topicLabel(beforeMeta, afterMeta),
      reasons,
      similarity: Number(similarity.toFixed(2)),
      importance: Math.max(beforeMeta.importance, afterMeta.importance)
    };
  }

  matchChangedClaims(beforeOnly, afterOnly) {
    const matchedPairs = [];
    const usedBefore = new Set();
    const additions = [];

    const sortedAfter = [...afterOnly].sort((a, b) => b.importance - a.importance || b.actionScore - a.actionScore);

    for (const afterMeta of sortedAfter) {
      let bestIndex = -1;
      let bestScore = 0;

      for (let i = 0; i < beforeOnly.length; i += 1) {
        if (usedBefore.has(i)) {
          continue;
        }

        const beforeMeta = beforeOnly[i];
        const score = this.similarity(beforeMeta, afterMeta);

        if (score > bestScore) {
          bestScore = score;
          bestIndex = i;
        }
      }

      const bestBefore = bestIndex >= 0 ? beforeOnly[bestIndex] : null;
      const qualifies = bestBefore && (
        bestScore >= 0.55 ||
        (bestScore >= 0.33 && (this.hasNumberChange(bestBefore, afterMeta) || this.hasPolarityFlip(bestBefore, afterMeta))) ||
        (bestScore >= 0.3 && Math.max(bestBefore.importance, afterMeta.importance) >= 5) ||
        (
          bestScore >= 0.22 &&
          this.hasStrongSharedTopic(bestBefore, afterMeta) &&
          /问题|假设|结论|原因|核心|方向|判断/.test(`${bestBefore.line} ${afterMeta.line}`)
        )
      );

      if (qualifies) {
        usedBefore.add(bestIndex);
        matchedPairs.push(this.buildChangedPair(bestBefore, afterMeta, bestScore));
      } else {
        additions.push(afterMeta);
      }
    }

    const removals = beforeOnly.filter((_, index) => !usedBefore.has(index));

    return { matchedPairs, additions, removals };
  }

  buildInvalidations(changedClaims, removals) {
    const items = [];

    for (const claim of changedClaims) {
      const shouldInvalidate = claim.reasons.some((reason) => /数字|方向|blocker|风险|时间线/.test(reason))
        || claim.beforeMeta.staleCandidate
        || claim.afterMeta.blocker;

      if (!shouldInvalidate) {
        continue;
      }

      items.push({
        stale: claim.before,
        replacement: claim.after,
        why: claim.reasons.join('，'),
        importance: claim.importance + 1
      });
    }

    for (const removed of removals) {
      if (!(removed.staleCandidate || removed.importance >= 5)) {
        continue;
      }

      items.push({
        stale: removed.line,
        replacement: '最新快照里没有继续支撑这条说法，建议确认是否需要下线或改写',
        why: '旧判断没有在新材料里继续得到支撑',
        importance: removed.importance
      });
    }

    return items
      .sort((a, b) => b.importance - a.importance || a.stale.length - b.stale.length)
      .slice(0, 5);
  }

  buildDecisionText(text) {
    if (/法务|合规|审批|security|legal|安全审查/i.test(text)) {
      return '确认是否立刻发起审批，并同步调整当前时间线';
    }
    if (/上线|发布|beta|deadline|排期|timeline|launch|release/i.test(text)) {
      return '重新确认时间线、owner 和对外承诺';
    }
    if (/客户|用户|销售|模板|需求|customer|user|sales/i.test(text)) {
      return '确认是否要调整本周优先级来响应这条新需求';
    }
    if (/blocker|风险|失效|冲突|tradeoff/i.test(text)) {
      return '明确谁来拍板，以及拍板后哪条路径立即生效';
    }

    return '确认这条变化是否要改写当前计划、结论或资源分配';
  }

  buildDecisionsNeeded(changedClaims, importantAdditions) {
    const items = [];

    for (const claim of changedClaims) {
      if (!(claim.importance >= 5 || claim.afterMeta.needsDecision || claim.afterMeta.blocker)) {
        continue;
      }

      items.push({
        topic: claim.topic,
        conflict: `之前“${this.shorten(claim.before, 42)}”，现在变成“${this.shorten(claim.after, 42)}”`,
        decision: this.buildDecisionText(`${claim.before} ${claim.after}`),
        importance: claim.importance + (claim.afterMeta.blocker ? 2 : 0)
      });
    }

    for (const addition of importantAdditions) {
      if (!(addition.needsDecision || addition.blocker || addition.importance >= 6)) {
        continue;
      }

      items.push({
        topic: this.shorten(addition.line, 24),
        conflict: addition.line,
        decision: this.buildDecisionText(addition.line),
        importance: addition.importance
      });
    }

    return items
      .sort((a, b) => b.importance - a.importance || a.topic.length - b.topic.length)
      .slice(0, 5);
  }

  buildActionFromAddition(addition) {
    if (/法务|合规|审批|security|legal|安全审查/i.test(addition.line)) {
      return `立即发起风险或审批处理：${this.shorten(addition.line, 54)}`;
    }
    if (/客户|用户|销售|模板|需求|customer|user|sales/i.test(addition.line)) {
      return `把新增客户信号纳入本周优先级：${this.shorten(addition.line, 54)}`;
    }
    if (/上线|发布|beta|deadline|排期|timeline|launch|release/i.test(addition.line)) {
      return `同步并更新时间线：${this.shorten(addition.line, 54)}`;
    }

    return `同步这条新增变化并指定 owner：${this.shorten(addition.line, 54)}`;
  }

  buildActionFromInvalidation(item) {
    if (/法务|合规|审批|security|legal|安全审查/i.test(`${item.stale} ${item.replacement}`)) {
      return `撤下旧判断并切换到新的审批路径：${this.shorten(item.replacement, 52)}`;
    }
    if (/上线|发布|beta|deadline|排期|timeline|launch|release/i.test(`${item.stale} ${item.replacement}`)) {
      return `改写路线图和对外口径：${this.shorten(item.replacement, 52)}`;
    }

    return `更新仍在引用旧结论的文档或汇报：${this.shorten(item.stale, 52)}`;
  }

  buildTopActions(importantAdditions, invalidations, decisionsNeeded) {
    const candidates = [];

    for (const item of decisionsNeeded) {
      candidates.push({
        action: `${item.decision}：${item.topic}`,
        why: item.conflict,
        score: item.importance + 3
      });
    }

    for (const item of invalidations) {
      candidates.push({
        action: this.buildActionFromInvalidation(item),
        why: item.why,
        score: item.importance + 2
      });
    }

    for (const item of importantAdditions) {
      candidates.push({
        action: this.buildActionFromAddition(item),
        why: item.line,
        score: item.importance + item.actionScore
      });
    }

    const deduped = [];
    const seen = new Set();

    for (const item of candidates.sort((a, b) => b.score - a.score || a.action.length - b.action.length)) {
      if (seen.has(item.action)) {
        continue;
      }
      seen.add(item.action);
      deduped.push(item);
    }

    return deduped.slice(0, 3);
  }

  buildHeadline(analysis) {
    const topAction = analysis.topActions[0]
      ? this.shorten(analysis.topActions[0].action, 34)
      : '当前没有识别出高压变化';

    return `识别出 ${analysis.importantAdditions.length} 条高价值新增、${analysis.changedClaims.length} 处说法变化、${analysis.invalidations.length} 个旧结论风险。最值得先处理的是：${topAction}。`;
  }

  compare(input) {
    const { before, after } = this.readPair(input);
    const beforeLines = this.collectStatements(before);
    const afterLines = this.collectStatements(after);

    const beforeMeta = beforeLines.map((line) => this.classifyLine(line));
    const afterMeta = afterLines.map((line) => this.classifyLine(line));

    const beforeKeys = new Set(beforeMeta.map((item) => item.key));
    const afterKeys = new Set(afterMeta.map((item) => item.key));

    const beforeOnly = beforeMeta.filter((item) => !afterKeys.has(item.key));
    const afterOnly = afterMeta.filter((item) => !beforeKeys.has(item.key));

    const { matchedPairs, additions, removals } = this.matchChangedClaims(beforeOnly, afterOnly);

    const importantAdditions = [...additions]
      .sort((a, b) => b.importance - a.importance || b.actionScore - a.actionScore || a.line.length - b.line.length)
      .filter((item, index) => item.importance >= 4 || index < 3)
      .slice(0, 5);

    const changedClaims = matchedPairs
      .sort((a, b) => b.importance - a.importance || b.similarity - a.similarity)
      .slice(0, 5);

    const invalidations = this.buildInvalidations(changedClaims, removals);
    const decisionsNeeded = this.buildDecisionsNeeded(changedClaims, importantAdditions);
    const topActions = this.buildTopActions(importantAdditions, invalidations, decisionsNeeded);

    const analysis = {
      summary: this.buildHeadline({
        importantAdditions,
        changedClaims,
        invalidations,
        topActions
      }),
      counts: {
        before: beforeLines.length,
        after: afterLines.length,
        additions: additions.length,
        changedClaims: changedClaims.length,
        invalidations: invalidations.length,
        decisionsNeeded: decisionsNeeded.length
      },
      importantAdditions: importantAdditions.map((item) => ({
        line: item.line,
        importance: item.importance
      })),
      changedClaims: changedClaims.map((item) => ({
        before: item.before,
        after: item.after,
        topic: item.topic,
        reasons: item.reasons,
        importance: item.importance
      })),
      invalidations,
      decisionsNeeded,
      topActions,
      raw: {
        before: beforeLines,
        after: afterLines,
        unmatchedBefore: removals.map((item) => item.line),
        unmatchedAfter: additions.map((item) => item.line)
      }
    };

    return analysis;
  }

  brief(input) {
    const analysis = this.compare(input);
    return {
      mode: 'brief',
      headline: analysis.summary,
      importantAdditions: analysis.importantAdditions,
      changedClaims: analysis.changedClaims,
      invalidations: analysis.invalidations,
      decisionsNeeded: analysis.decisionsNeeded,
      topActions: analysis.topActions,
      counts: analysis.counts
    };
  }

  changes(input) {
    const analysis = this.compare(input);
    return {
      mode: 'changes',
      headline: analysis.summary,
      items: analysis.importantAdditions,
      counts: analysis.counts
    };
  }

  invalidations(input) {
    const analysis = this.compare(input);
    return {
      mode: 'invalidations',
      headline: analysis.summary,
      items: analysis.invalidations,
      counts: analysis.counts
    };
  }

  conflicts(input) {
    const analysis = this.compare(input);
    return {
      mode: 'conflicts',
      headline: analysis.summary,
      items: analysis.decisionsNeeded,
      counts: analysis.counts
    };
  }

  priorities(input) {
    const analysis = this.compare(input);
    return {
      mode: 'priorities',
      headline: analysis.summary,
      items: analysis.topActions,
      counts: analysis.counts
    };
  }

  analyze(input) {
    return this.compare(input);
  }

  renderList(items, mapper, emptyText = '无') {
    if (!items || items.length === 0) {
      return `- ${emptyText}`;
    }

    return items.map((item) => `- ${mapper(item)}`).join('\n');
  }

  render(result) {
    switch (result.mode) {
      case 'brief':
        return [
          '变化一句话',
          result.headline,
          '',
          '这周新增了哪些重要信息',
          this.renderList(result.importantAdditions, (item) => `${item.line}（重要度 ${item.importance}）`),
          '',
          '哪几处说法变了',
          this.renderList(result.changedClaims, (item) => `之前“${this.shorten(item.before, 32)}” -> 现在“${this.shorten(item.after, 32)}”（${item.reasons.join('，')}）`),
          '',
          '哪些旧结论可能失效',
          this.renderList(result.invalidations, (item) => `旧结论“${this.shorten(item.stale, 32)}” -> 新现实“${this.shorten(item.replacement, 32)}”（${item.why}）`),
          '',
          '哪些冲突需要拍板',
          this.renderList(result.decisionsNeeded, (item) => `${item.topic}：${item.decision}。证据：${item.conflict}`),
          '',
          '最值得立刻行动的 3 个变化',
          this.renderList(result.topActions, (item) => `${item.action}（原因：${this.shorten(item.why, 48)}）`)
        ].join('\n');
      case 'changes':
        return [
          '重要新增变化',
          result.headline,
          '',
          this.renderList(result.items, (item) => `${item.line}（重要度 ${item.importance}）`)
        ].join('\n');
      case 'invalidations':
        return [
          '可能失效的旧结论',
          result.headline,
          '',
          this.renderList(result.items, (item) => `旧结论“${this.shorten(item.stale, 36)}” -> ${this.shorten(item.replacement, 44)}（${item.why}）`)
        ].join('\n');
      case 'conflicts':
        return [
          '需要拍板的变化冲突',
          result.headline,
          '',
          this.renderList(result.items, (item) => `${item.topic}：${item.decision}。证据：${item.conflict}`)
        ].join('\n');
      case 'priorities':
        return [
          '优先处理的变化',
          result.headline,
          '',
          this.renderList(result.items, (item) => `${item.action}（原因：${this.shorten(item.why, 48)}）`)
        ].join('\n');
      default:
        return JSON.stringify(result, null, 2);
    }
  }
}

module.exports = ChangeBrief;
