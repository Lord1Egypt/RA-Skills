/**
 * EVA Soul - 核心模块汇总
 */

// 核心模块
const { DEFAULT_CONFIG, loadConfig, getDefaultConfig, expandPath } = require('./core/config');
const { 
  DEFAULT_STATE, createState, loadState, saveState,
  updateEmotion, updatePersonality, recordInteraction, incrementSession,
  setSleepState, recordToolUsage, addConcept, addPattern,
  addImportantDate, updateOwnerInfo, getStateSummary
} = require('./core/state');

// 情感模块
const { 
  EMOTIONS, detectEmotion, getIntensityLevel, analyzeEmotionTrend,
  expressEmotion, predictEmotion, getEmotionContext,
  getEmotionData, getAllEmotions
} = require('./emotion/emotion');

// 性格模块
const { 
  PERSONALITIES, getPersonality, getTraitWeights,
  adjustPersonalityForScene, buildPersonalityPrompt,
  switchPersonality, getAllPersonalities, getPersonalityAdvice
} = require('./personality/personality');

// 记忆模块
const { MemoryStore, MEMORY_TIERS, MEMORY_TYPES } = require('./memory/memory');

// 认知模块
const { 
  ConceptSystem, PatternSystem, KnowledgeGraph, 
  EmbeddingConceptEnhancer 
} = require('./cognition/cognition');

// 决策模块
const { 
  DecisionSystem, MotivationSystem, ValuesSystem,
  evaluateImportance 
} = require('./decision/decision');

module.exports = {
  // 核心
  DEFAULT_CONFIG,
  loadConfig,
  getDefaultConfig,
  expandPath,
  DEFAULT_STATE,
  createState,
  loadState,
  saveState,
  updateEmotion,
  updatePersonality,
  recordInteraction,
  incrementSession,
  setSleepState,
  recordToolUsage,
  addConcept,
  addPattern,
  addImportantDate,
  updateOwnerInfo,
  getStateSummary,
  
  // 情感
  EMOTIONS,
  detectEmotion,
  getIntensityLevel,
  analyzeEmotionTrend,
  expressEmotion,
  predictEmotion,
  getEmotionContext,
  getEmotionData,
  getAllEmotions,
  
  // 性格
  PERSONALITIES,
  getPersonality,
  getTraitWeights,
  adjustPersonalityForScene,
  buildPersonalityPrompt,
  switchPersonality,
  getAllPersonalities,
  getPersonalityAdvice,
  
  // 记忆
  MemoryStore,
  MEMORY_TIERS,
  MEMORY_TYPES,
  
  // 认知
  EmbeddingConceptEnhancer,
  ConceptSystem,
  PatternSystem,
  KnowledgeGraph,
  
  // 决策
  DecisionSystem,
  MotivationSystem,
  ValuesSystem,
  evaluateImportance
};
