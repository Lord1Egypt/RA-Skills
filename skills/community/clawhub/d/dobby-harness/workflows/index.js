/**
 * Workflows - 生产级工作流索引
 * 
 * 导出所有可用的工作流
 */

export {
  CodeReviewWorkflow,
  codeReview,
} from './code-review.js';
export { default as CodeReviewWorkflowDefault } from './code-review.js';

export {
  TestGenWorkflow,
  generateTests,
  generateTestForFile,
} from './test-gen.js';
export { default as TestGenWorkflowDefault } from './test-gen.js';

export {
  DocGenWorkflow,
  generateDocs,
  generateApiDocs,
  generateReadme,
} from './doc-gen.js';
export { default as DocGenWorkflowDefault } from './doc-gen.js';

export {
  CICDWorkflow,
  setupCICD,
  generateGitHubActions,
  generateGitLabCI,
  generateDockerConfig,
} from './cicd.js';
export { default as CICDWorkflowDefault } from './cicd.js';

/**
 * 工作流注册表
 */
export const workflows = {
  'code-review': CodeReviewWorkflow,
  'test-gen': TestGenWorkflow,
  'doc-gen': DocGenWorkflow,
  'cicd': CICDWorkflow,
};

/**
 * 获取工作流
 * @param {string} name - 工作流名称
 * @returns {Class} 工作流类
 */
export function getWorkflow(name) {
  const Workflow = workflows[name];
  if (!Workflow) {
    const available = Object.keys(workflows).join(', ');
    throw new Error(`Unknown workflow: ${name}. Available: ${available}`);
  }
  return Workflow;
}

/**
 * 快速执行工作流
 * @param {string} name - 工作流名称
 * @param {Object} options - 执行选项
 * @returns {Promise<Object>} 执行结果
 */
export async function runWorkflow(name, options) {
  const Workflow = getWorkflow(name);
  const workflow = new Workflow(options?.config);
  return workflow.execute(options);
}

export default workflows;
