#!/usr/bin/env node
/**
 * EVA Soul CLI - 夏娃之魂命令行工具
 */

const fs = require('fs');
const path = require('path');

// 使用结构化日志
const logger = require('../hooks/logger');

const stateFile = path.join(process.env.HOME || '', '.openclaw/workspace/memory/eva-soul-state.json');
const kgFile = path.join(process.env.HOME || '', '.openclaw/workspace/memory/eva-knowledge-graph.json');

function loadState() {
  try {
    return JSON.parse(fs.readFileSync(stateFile, 'utf8'));
  } catch (e) {
    return null;
  }
}

function loadKG() {
  try {
    return JSON.parse(fs.readFileSync(kgFile, 'utf8'));
  } catch (e) {
    return null;
  }
}

const cmd = process.argv[2];

switch (cmd) {
  case 'status': {
    const state = loadState();
    if (state) {
      logger.section('🎀 ' + logger.t('cli.status.title'));
      logger.item(`${logger.t('cli.status.emotion')}: ${state.currentEmotion}`);
      logger.item(`${logger.t('cli.status.personality')}: ${state.personality}`);
      logger.item(`${logger.t('cli.status.level')}: ${state.level} (${logger.t('cli.status.exp')}: ${state.experience}/${state.expNeeded})`);
      logger.item(`${logger.t('cli.status.session')}: ${state.sessionCount}`);
      logger.item(`${logger.t('cli.status.concepts')}: ${state.concepts?.length || 0}`);
      logger.item(`${logger.t('cli.status.memories')}: ${state.conceptStats?.total || 0}`);
      logger.item(`${logger.t('cli.status.patterns')}: ${state.patternStats?.total || 0}`);
      logger.item(`${logger.t('cli.status.motivations')}: ${state.motivations?.length || 0}`);
      logger.item(`${logger.t('cli.status.dreams')}: ${state.dreams?.length || 0}`);
      logger.item(`${logger.t('cli.status.values')}: ${state.values?.length || 0}`);
    }
    break;
  }

  case 'emotion': {
    const emotionArg = process.argv[3];
    if (emotionArg) {
      const s = loadState();
      if (s) {
        s.currentEmotion = emotionArg;
        s.lastUpdate = new Date().toISOString();
        fs.writeFileSync(stateFile, JSON.stringify(s, null, 2));
        logger.success(logger.t('cli.emotion.set', { emotion: emotionArg }), 'cli');
      }
    } else {
      logger.info(`${logger.t('cli.emotion.current')}: ${loadState()?.currentEmotion || 'unknown'}`, 'cli');
      logger.info(logger.t('cli.emotion.usage'), 'cli');
    }
    break;
  }

  case 'concept': {
    const conceptArg = process.argv[3];
    if (conceptArg) {
      const s = loadState();
      if (s) {
        s.concepts = s.concepts || [];
        s.concepts.push({
          type: 'fact',
          value: conceptArg,
          importance: 8,
          createdAt: new Date().toISOString()
        });
        s.lastUpdate = new Date().toISOString();
        fs.writeFileSync(stateFile, JSON.stringify(s, null, 2));
        logger.success(logger.t('cli.concept.added', { value: conceptArg }), 'cli');
      }
    } else {
      const s = loadState();
      logger.info(logger.t('cli.concept.list') + ':', 'cli');
      (s?.concepts || []).forEach((c, i) => {
        logger.item(`${i+1}. ${c.value} (${c.type})`, 'cli');
      });
    }
    break;
  }

  case 'kg': {
    const kg = loadKG();
    if (kg) {
      logger.section('🎀 ' + logger.t('cli.kg.title'));
      logger.item(`${logger.t('cli.kg.nodes')}: ${kg.nodes?.length || 0}`);
      logger.item(`${logger.t('cli.kg.edges')}: ${kg.edges?.length || 0}`);
      logger.info(logger.t('cli.kg.nodeList') + ':', 'cli');
      (kg.nodes || []).forEach(n => {
        logger.item(`${n.label} (${n.type})`, 'cli');
      });
    }
    break;
  }

  default:
    logger.section('🎀 EVA CLI');
    logger.info(logger.t('cli.help.title'), 'cli');
    logger.info('  ' + logger.t('cli.help.status'), 'cli');
    logger.info('  ' + logger.t('cli.help.emotion'), 'cli');
    logger.info('  ' + logger.t('cli.help.concept'), 'cli');
    logger.info('  ' + logger.t('cli.help.kg'), 'cli');
}
