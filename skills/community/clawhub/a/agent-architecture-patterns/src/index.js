/**
 * Agent Architecture Patterns - Main Entry Point
 * 
 * Export all agent implementations
 */

const { ReActAgent } = require('./agents/react-agent');
const { ReflectionAgent } = require('./agents/reflection-agent');
const { SelfCritiqueAgent } = require('./agents/self-critique-agent');
const { PlanAndSolveAgent } = require('./agents/plan-and-solve-agent');
const { TreeOfThoughtsAgent } = require('./agents/tree-of-thoughts-agent');
const { ManagerAgent, WorkerAgent } = require('./agents/manager-worker-agent');

module.exports = {
  // Single-Agent Patterns
  ReActAgent,
  ReflectionAgent,
  SelfCritiqueAgent,
  PlanAndSolveAgent,
  TreeOfThoughtsAgent,
  
  // Multi-Agent Patterns
  ManagerAgent,
  WorkerAgent
};
