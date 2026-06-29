/**
 * Clarity Code Subsystem - 统一入口
 *
 * 合并 6 个代码能力模块，统一导出并注册到心虫 dispatch
 *
 * 模块：
 *   - CodeGenerator  — 代码生成引擎（模板 + LLM）
 *   - CodeExecutor   — 代码执行引擎（沙箱 + 超时）
 *   - CodeVerifier   — 代码验证引擎（语法 + 逻辑 + TDD）
 *   - CodePlanner    — 任务规划引擎（分解 + 路径）
 *   - CodeKnowledge  — 代码知识库（模式库 + 搜索 + 学习）
 *   - CodeRefactor   — 代码重构引擎（检测 + 变换 + 质量度量）[v1.8.7]
 *
 * @author Clarity
 * @version 1.8.7
 */

const path = require('path');

// ─── 动态加载各模块 ───────────────────────────────────────
const { CodeGenerator }   = require('./code-generator.js');
const { CodeExecutor }    = require('./code-executor.js');
const { CodeVerifier }     = require('./code-verifier.js');
const { CodePlanner }      = require('./code-planner.js');
const { CodeKnowledge }    = require('./code-knowledge.js');
const { CodeRefactor }     = require('./code-refactor.js');

/**
 * 加载所有 code 子系统模块
 * @param {Object} opts - { hf, rootPath }
 * @returns {Object} - 各模块实例
 */
function loadAll({ hf, rootPath }) {
  return {
    codeGenerator:  new CodeGenerator({ hf }),
    codeExecutor:   new CodeExecutor({ hf }),
    codeVerifier:   new CodeVerifier({ hf }),
    codePlanner:    new CodePlanner({ hf }),
    codeKnowledge:  new CodeKnowledge({ rootPath: rootPath || hf?.rootPath }),
    codeRefactor:   new CodeRefactor({ hf }),
  };
}

/**
 * 注册 code 模块到心虫 _modules
 * - codeGenerator → 'code'（主入口）
 * - 其余映射到对应键名
 *
 * @param {Object} hf - 心虫实例
 * @param {Object} modules - loadAll() 返回的模块对象
 */
function registerToClarity(hf, modules) {
  if (!hf || !modules) {
    console.warn('[CodeIndex] registerToClarity: hf 或 modules 无效，跳过注册');
    return;
  }
  if (!hf._modules) hf._modules = {};

  // codeGenerator 作为主入口暴露为 'code'
  hf.code = modules.codeGenerator;
  hf._modules['code'] = modules.codeGenerator;

  // 其余模块
  hf.codeExecutor  = modules.codeExecutor;
  hf.codeVerifier  = modules.codeVerifier;
  hf.codePlanner   = modules.codePlanner;
  hf.codeKnowledge = modules.codeKnowledge;
  hf.codeRefactor  = modules.codeRefactor;

  hf._modules['codeExecutor']  = modules.codeExecutor;
  hf._modules['codeVerifier']  = modules.codeVerifier;
  hf._modules['codePlanner']   = modules.codePlanner;
  hf._modules['codeKnowledge'] = modules.codeKnowledge;
  hf._modules['codeRefactor']  = modules.codeRefactor;
}

// ─── ALLOWED_ROUTES 路由表 ────────────────────────────────
// 用于 clarity.js 的 dispatch 白名单
// ═══════════════════════════════════════════════════════════

const CODE_ROUTES = [
  // ── codeGenerator ──────────────────────────────────────
  'code.generate', 'code.generateFile', 'code.detectIntent',
  'code.getAvailableTemplates', 'code.getStats',
  // ── codeExecutor ──────────────────────────────────────
  'code.execute', 'code.runTests', 'code.sandbox', 'code.healthCheck', 'code.getExecutorStats',
  // ── codeVerifier ──────────────────────────────────────
  'code.verify', 'code.verifySyntax', 'code.verifyLogic', 'code.runTDD',
  'code.getQualityScore', 'code.getVerifierStats',
  // ── codePlanner ────────────────────────────────────────
  'code.plan', 'code.decompose', 'code.getPath', 'code.adapt', 'code.getPlannerStats',
  // ── codeKnowledge ─────────────────────────────────────
  'code.search', 'code.addSnippet', 'code.getPatterns',
  'code.learnFromSuccess', 'code.evolve', 'code.getKnowledgeStats',
  // ── codeRefactor ──────────────────────────────────────
  'code.detect', 'code.suggest', 'code.transform',
  'code.qualityScore', 'code.getRefactorHistory', 'code.getTransformers', 'code.getRefactorStats',
];

module.exports = {
  CodeGenerator,
  CodeExecutor,
  CodeVerifier,
  CodePlanner,
  CodeKnowledge,
  CodeRefactor,
  loadAll,
  registerToClarity,
  CODE_ROUTES,
};
