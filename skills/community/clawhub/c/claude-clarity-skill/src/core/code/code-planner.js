/**
 * CodePlanner - 代码规划引擎 v2.0.0
 *
 * 功能：
 * 1. 任务分析：识别任务类型（create/modify/fix/optimize/refactor）
 * 2. 依赖解析：识别导入的库/模块
 * 3. 路径规划：生成代码实现的执行计划
 * 4. 自适应：根据执行结果动态调整计划
 * 5. 多文件项目：支持多文件项目依赖图和目录结构生成（v1.1 新增）
 *
 * 与心虫 CognitiveProtocol 协同工作，利用认知协议确保先理解再行动
 *
 * v1.1 新增功能：
 * - buildDependencyGraph(): 从步骤列表构建模块依赖图，支持循环检测
 * - planMultiFile(): 多文件项目规划，生成完整的目录结构计划
 * - generateProjectStructure(): 生成完整的项目目录结构和文件内容
 * - 与 code-knowledge.js 的 getPatterns 打通
 * - adapt() 支持循环依赖检测和自动 re-plan
 */

const fs = require('fs');
const path = require('path');

/**
 * 任务类型枚举
 */
const TASK_TYPE = {
  CREATE: 'create',       // 创建新文件/模块
  MODIFY: 'modify',       // 修改现有代码
  FIX: 'fix',            // 修复bug/错误
  OPTIMIZE: 'optimize',  // 性能优化
  REFACTOR: 'refactor'    // 重构代码
};

/**
 * 任务复杂度枚举
 */
const COMPLEXITY = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high'
};

/**
 * 动作类型枚举
 */
const ACTION_TYPE = {
  CREATE: 'create',
  EDIT: 'edit',
  DELETE: 'delete',
  EXECUTE: 'execute'
};

/**
 * 任务类型识别模式注册表
 * 参考 skill-generator.js 的 PATTERN_REGISTRY 设计
 */
const TASK_TYPE_PATTERNS = {
  [TASK_TYPE.CREATE]: {
    keywords: [
      '创建', '新建', '添加', '实现', '开发', '编写',
      'create', 'new', 'add', 'implement', 'build', 'write'
    ],
    weight: 1.0
  },
  [TASK_TYPE.MODIFY]: {
    keywords: [
      '修改', '改动', '调整', '更新', '改变',
      'modify', 'change', 'update', 'alter', 'edit'
    ],
    weight: 0.9
  },
  [TASK_TYPE.FIX]: {
    keywords: [
      '修复', '解决', '改正', '排查', '调试', 'bug', '错误',
      'fix', 'repair', 'resolve', 'debug', 'solve'
    ],
    weight: 1.0
  },
  [TASK_TYPE.OPTIMIZE]: {
    keywords: [
      '优化', '性能', '提升', '加速', '改进',
      'optimize', 'performance', 'improve', 'speed', 'enhance'
    ],
    weight: 0.9
  },
  [TASK_TYPE.REFACTOR]: {
    keywords: [
      '重构', '整理', '清理', '重写',
      'refactor', 'restructure', 'cleanup', 'rewrite'
    ],
    weight: 0.85
  }
};

/**
 * 编程语言特征识别
 */
const LANGUAGE_PATTERNS = {
  javascript: {
    extensions: ['.js', '.jsx', '.mjs'],
    importPattern: /import\s+.*?from\s+['"](.*?)['"]/g,
    requirePattern: /require\s*\(\s*['"](.*?)['"]\s*\)/g,
    exportPattern: /export\s+(default\s+)?(class|function|const|let)/g
  },
  typescript: {
    extensions: ['.ts', '.tsx', '.d.ts'],
    importPattern: /import\s+.*?from\s+['"](.*?)['"]/g,
    requirePattern: /require\s*\(\s*['"](.*?)['"]\s*\)/g,
    exportPattern: /export\s+(default\s+)?(class|function|const|let)/g
  },
  python: {
    extensions: ['.py'],
    importPattern: /(?:from|import)\s+([\w.]+)\s+/g,
    requirePattern: null,
    exportPattern: /def\s+\w+|class\s+\w+/g
  },
  go: {
    extensions: ['.go'],
    importPattern: /import\s+["(](.*?)[")]/g,
    requirePattern: null,
    exportPattern: /func\s+\w+/g
  },
  rust: {
    extensions: ['.rs'],
    importPattern: /use\s+([\w:]+)/g,
    requirePattern: null,
    exportPattern: /pub\s+(fn|struct|enum|mod)/g
  }
};

class CodePlanner {
  /**
   * 构造函数
   * @param {Object} options - 配置选项
   * @param {Object} options.hf - 心虫实例（Clarity）
   * @param {Object} options.codeKnowledge - 代码知识库实例（用于获取已有模式）
   */
  constructor(options = {}) {
    this.hf = options.hf || null;
    this.codeKnowledge = options.codeKnowledge || null;

    // 内部状态
    this.currentPlan = null;
    this.taskHistory = [];
    this.executionCache = new Map();

    // 配置参数
    this.config = {
      maxStepsPerPlan: 50,           // 单个计划最大步骤数
      dependencyDepthLimit: 10,      // 依赖深度限制
      complexityFileThreshold: 500,  // 文件行数阈值（用于复杂度评估）
      complexityDepsThreshold: 5,    // 依赖数量阈值（用于复杂度评估）
      maxFilesPerProject: 100        // 多文件项目最大文件数
    };

    // 统计信息
    this.stats = {
      plansCreated: 0,
      tasksDecomposed: 0,
      adaptationsMade: 0,
      avgStepsPerPlan: 0
    };
  }

  // ═══════════════════════════════════════════════════════════════
  // 核心功能 1: 构建依赖图
  // ═══════════════════════════════════════════════════════════════

  /**
   * 从步骤列表构建模块依赖图
   *
   * 功能：
   * - 分析每个 step 的 deps 字段
   * - 生成邻接表表示的依赖图
   * - 检测循环依赖（topological sort 时检测）
   *
   * @param {Object[]} steps - 步骤数组
   * @returns {Object} {
   *   graph: { [file]: deps[] },  // 邻接表：每个文件的依赖列表
   *   cycles: [{ path: string[], message: string }],  // 检测到的循环路径
   *   order: string[]  // 拓扑排序后的文件顺序
   * }
   *
   * @example
   * // 输入步骤
   * steps = [
   *   { id: 1, file: 'src/index.js', deps: [2, 3] },
   *   { id: 2, file: 'src/routes/users.js', deps: [3] },
   *   { id: 3, file: 'src/models/user.js', deps: [] }
   * ]
   * // 输出
   * {
   *   graph: {
   *     'src/index.js': ['src/routes/users.js', 'src/models/user.js'],
   *     'src/routes/users.js': ['src/models/user.js'],
   *     'src/models/user.js': []
   *   },
   *   cycles: [],
   *   order: ['src/models/user.js', 'src/routes/users.js', 'src/index.js']
   * }
   */
  buildDependencyGraph(steps) {
    // 构建邻接表
    const graph = new Map();  // file -> deps[]
    const fileToStep = new Map();  // file -> step
    const stepToFile = new Map();  // stepId -> file
    const filesWithoutId = [];  // 没有id但有file的步骤

    // 第一遍：收集所有文件和步骤的映射关系
    for (const step of steps) {
      if (step.file) {
        // 使用 file 作为唯一标识
        if (!graph.has(step.file)) {
          graph.set(step.file, []);
        }
        fileToStep.set(step.file, step);
      }
      if (step.id !== undefined) {
        stepToFile.set(step.id, step.file);
      }
    }

    // 第二遍：根据 deps（stepId 数组）构建依赖关系
    for (const step of steps) {
      if (step.file && step.deps && step.deps.length > 0) {
        const dependencies = [];
        for (const depId of step.deps) {
          const depFile = stepToFile.get(depId);
          if (depFile && depFile !== step.file) {
            dependencies.push(depFile);
          }
        }
        graph.set(step.file, dependencies);
      }
    }

    // 检测循环依赖（DFS 方法）
    const cycles = [];
    const WHITE = 0;  // 未访问
    const GRAY = 1;   // 正在访问（在当前路径上）
    const BLACK = 2;   // 已完成

    const color = new Map();
    const parent = new Map();

    for (const file of graph.keys()) {
      color.set(file, WHITE);
      parent.set(file, null);
    }

    // DFS 检测循环
    const detectCycleDFS = (node, path = []) => {
      color.set(node, GRAY);
      path.push(node);

      const deps = graph.get(node) || [];
      for (const dep of deps) {
        if (!graph.has(dep)) {
          // 依赖的文件不在当前图中，可能是外部依赖
          continue;
        }

        if (color.get(dep) === GRAY) {
          // 发现循环：沿着 parent 找到循环的完整路径
          const cycleStart = path.indexOf(dep);
          const cyclePath = path.slice(cycleStart);
          cyclePath.push(dep);  // 完成循环

          cycles.push({
            path: cyclePath,
            message: `循环依赖: ${cyclePath.join(' → ')}`
          });
        } else if (color.get(dep) === WHITE) {
          parent.set(dep, node);
          detectCycleDFS(dep, path);
        }
      }

      path.pop();
      color.set(node, BLACK);
    };

    // 对所有节点执行检测
    for (const file of graph.keys()) {
      if (color.get(file) === WHITE) {
        detectCycleDFS(file, []);
      }
    }

    // 拓扑排序（Kahn 算法）
    // 去除有循环的节点，只对无循环的节点排序
    const cyclicFiles = new Set();
    for (const cycle of cycles) {
      for (const file of cycle.path) {
        cyclicFiles.add(file);
      }
    }

    // 计算入度
    const inDegree = new Map();
    for (const file of graph.keys()) {
      inDegree.set(file, 0);
    }
    for (const [file, deps] of graph) {
      for (const dep of deps) {
        if (inDegree.has(dep)) {
          inDegree.set(dep, inDegree.get(dep) + 1);
        }
      }
    }

    // 从入度为 0 的节点开始（BFS 拓扑排序）
    const order = [];
    const queue = [];

    for (const [file, degree] of inDegree) {
      if (degree === 0 && !cyclicFiles.has(file)) {
        queue.push(file);
      }
    }

    while (queue.length > 0) {
      const node = queue.shift();
      order.push(node);

      const deps = graph.get(node) || [];
      for (const dep of deps) {
        if (inDegree.has(dep)) {
          const newDegree = inDegree.get(dep) - 1;
          inDegree.set(dep, newDegree);
          if (newDegree === 0) {
            queue.push(dep);
          }
        }
      }
    }

    // 转换为普通对象
    const graphObj = {};
    for (const [file, deps] of graph) {
      graphObj[file] = deps;
    }

    return {
      graph: graphObj,
      cycles,
      order
    };
  }

  // ═══════════════════════════════════════════════════════════════
  // 核心功能 2: 多文件项目规划
  // ═══════════════════════════════════════════════════════════════

  /**
   * 多文件项目规划
   *
   * 输入：项目名 + 需求描述 + 语言
   * 分析需求中的模块划分（API/业务逻辑/数据层/工具函数）
   * 生成多文件目录结构计划
   *
   * @param {string} projectName - 项目名称
   * @param {string} requirements - 需求描述
   * @param {string} language - 编程语言（javascript/typescript/python/go）
   * @returns {Object} 多文件项目计划
   */
  planMultiFile(projectName, requirements, language = 'javascript') {
    // 定义语言对应的目录结构模板
    const STRUCTURE_TEMPLATES = {
      javascript: {
        base: 'src',
        layers: {
          entry: 'index.js',
          routes: 'routes',
          controllers: 'controllers',
          services: 'services',
          models: 'models',
          middleware: 'middleware',
          utils: 'utils',
          config: 'config',
          db: 'db'
        },
        extensions: { js: '.js', config: '.json' }
      },
      typescript: {
        base: 'src',
        layers: {
          entry: 'index.ts',
          routes: 'routes',
          controllers: 'controllers',
          services: 'services',
          models: 'models',
          middleware: 'middleware',
          utils: 'utils',
          config: 'config',
          db: 'db',
          types: 'types'
        },
        extensions: { ts: '.ts', config: '.json' }
      },
      python: {
        base: 'app',
        layers: {
          entry: '__init__.py',
          routes: 'api',
          controllers: 'controllers',
          services: 'services',
          models: 'models',
          middleware: 'middleware',
          utils: 'utils',
          config: 'config',
          db: 'db'
        },
        extensions: { py: '.py', config: '.py' }
      },
      go: {
        base: '',
        layers: {
          entry: 'main.go',
          routes: 'handlers',
          controllers: 'controllers',
          services: 'services',
          models: 'models',
          middleware: 'middleware',
          utils: 'utils',
          config: 'config',
          db: 'db'
        },
        extensions: { go: '.go' }
      }
    };

    const template = STRUCTURE_TEMPLATES[language] || STRUCTURE_TEMPLATES.javascript;
    const ext = template.extensions[language === 'python' ? 'py' : language === 'go' ? 'go' : 'ts'] || '.js';

    // 分析需求中的功能模块
    const moduleAnalysis = this._analyzeRequirementsModules(requirements, language);

    // 生成文件计划
    const files = [];
    let fileIdCounter = 1;

    // 入口文件
    const entryFile = `${template.base ? template.base + '/' : ''}${template.layers.entry}`;
    files.push({
      id: fileIdCounter++,
      path: entryFile,
      action: 'create',
      deps: this._getEntryDependencies(moduleAnalysis, template, language),
      layer: 'entry',
      description: `${projectName} 入口文件`
    });

    // API 路由层（如果需要）
    if (moduleAnalysis.hasAPI) {
      const routesFile = `${template.base}/${template.layers.routes}/index${ext}`;
      files.push({
        id: fileIdCounter++,
        path: routesFile,
        action: 'create',
        deps: [],
        layer: 'routes',
        description: `${projectName} API 路由`
      });

      // 根据 API 端点生成具体路由文件
      for (const api of moduleAnalysis.apis || []) {
        const routeFile = `${template.base}/${template.layers.routes}/${api.name}${ext}`;
        files.push({
          id: fileIdCounter++,
          path: routeFile,
          action: 'create',
          deps: [
            `${template.base}/${template.layers.controllers}/${api.name}${ext}`
          ],
          layer: 'routes',
          description: `${api.name} 路由`
        });
      }
    }

    // 控制器层（如果需要）
    if (moduleAnalysis.hasControllers) {
      for (const ctrl of (moduleAnalysis.controllers || [])) {
        const ctrlFile = `${template.base}/${template.layers.controllers}/${ctrl.name}${ext}`;
        files.push({
          id: fileIdCounter++,
          path: ctrlFile,
          action: 'create',
          deps: [
            `${template.base}/${template.layers.services}/${ctrl.serviceName || ctrl.name}${ext}`
          ],
          layer: 'controllers',
          description: `${ctrl.name} 控制器`
        });
      }
    }

    // 服务层（业务逻辑）
    if (moduleAnalysis.hasServices) {
      for (const service of (moduleAnalysis.services || [])) {
        const serviceFile = `${template.base}/${template.layers.services}/${service.name}${ext}`;
        files.push({
          id: fileIdCounter++,
          path: serviceFile,
          action: 'create',
          deps: [
            `${template.base}/${template.layers.models}/${service.modelName || 'index'}${ext}`,
            `${template.base}/${template.layers/utils}/logger${ext}`
          ],
          layer: 'services',
          description: `${service.name} 服务层`
        });
      }
    }

    // 模型层（数据模型）
    if (moduleAnalysis.hasModels) {
      for (const model of (moduleAnalysis.models || [])) {
        const modelFile = `${template.base}/${template.layers.models}/${model.name}${ext}`;
        files.push({
          id: fileIdCounter++,
          path: modelFile,
          action: 'create',
          deps: [
            `${template.base}/${template.layers.db}/connection${ext}`
          ],
          layer: 'models',
          description: `${model.name} 数据模型`
        });
      }
    }

    // 数据库连接（如果需要）
    if (moduleAnalysis.hasDatabase) {
      const dbFile = `${template.base}/${template.layers.db}/connection${ext}`;
      files.push({
        id: fileIdCounter++,
        path: dbFile,
        action: 'create',
        deps: [],
        layer: 'db',
        description: '数据库连接配置'
      });
    }

    // 中间件层（如果需要）
    if (moduleAnalysis.hasMiddleware) {
      for (const middleware of (moduleAnalysis.middleware || [])) {
        const mwFile = `${template.base}/${template.layers.middleware}/${middleware.name}${ext}`;
        files.push({
          id: fileIdCounter++,
          path: mwFile,
          action: 'create',
          deps: [],
          layer: 'middleware',
          description: `${middleware.name} 中间件`
        });
      }
    }

    // 工具函数层
    const utilsFile = `${template.base}/${template.layers.utils}/logger${ext}`;
    files.push({
      id: fileIdCounter++,
      path: utilsFile,
      action: 'create',
      deps: [],
      layer: 'utils',
      description: '日志工具'
    });

    const helperFile = `${template.base}/${template.layers.utils}/helpers${ext}`;
    files.push({
      id: fileIdCounter++,
      path: helperFile,
      action: 'create',
      deps: [],
      layer: 'utils',
      description: '辅助函数'
    });

    // 配置层
    const configFile = `${template.base}/${template.layers.config}/index${ext}`;
    files.push({
      id: fileIdCounter++,
      path: configFile,
      action: 'create',
      deps: [],
      layer: 'config',
      description: '项目配置'
    });

    // 构建依赖图并获取拓扑顺序
    const dependencyGraph = this.buildDependencyGraph(files);

    // 合并 cycles 到计划中
    return {
      projectName,
      files,
      entry: entryFile,
      dependencyOrder: dependencyGraph.order,
      graph: dependencyGraph.graph,
      cycles: dependencyGraph.cycles,
      template: template.layers,
      language,
      createdAt: new Date().toISOString()
    };
  }

  /**
   * 分析需求中的模块
   * @private
   */
  _analyzeRequirementsModules(requirements, language) {
    const lowerReq = requirements.toLowerCase();
    const analysis = {
      hasAPI: false,
      hasControllers: false,
      hasServices: false,
      hasModels: false,
      hasDatabase: false,
      hasMiddleware: false,
      apis: [],
      controllers: [],
      services: [],
      models: [],
      middleware: []
    };

    // 检测 API 需求
    const apiKeywords = ['api', 'endpoint', 'route', 'rest', 'graphql', 'http'];
    if (apiKeywords.some(k => lowerReq.includes(k))) {
      analysis.hasAPI = true;
      // 尝试提取 API 端点名
      const apiPatterns = [
        /users?/i,
        /auth/i,
        /products?/i,
        /orders?/i,
        /data/i
      ];
      for (const pattern of apiPatterns) {
        if (pattern.test(requirements)) {
          analysis.apis.push({
            name: requirements.match(pattern)?.[0] || 'api',
            method: lowerReq.includes('create') ? 'POST' : lowerReq.includes('delete') ? 'DELETE' : 'GET'
          });
        }
      }
      if (analysis.apis.length === 0) {
        analysis.apis.push({ name: 'index', method: 'GET' });
      }
    }

    // 检测控制器需求
    const controllerKeywords = ['controller', 'handler', '处理'];
    if (controllerKeywords.some(k => lowerReq.includes(k))) {
      analysis.hasControllers = true;
      for (const api of analysis.apis) {
        analysis.controllers.push({
          name: api.name,
          serviceName: `${api.name}Service`
        });
      }
    }

    // 检测服务层需求
    const serviceKeywords = ['service', 'business', 'logic', '业务'];
    if (serviceKeywords.some(k => lowerReq.includes(k))) {
      analysis.hasServices = true;
      for (const api of analysis.apis) {
        analysis.services.push({
          name: `${api.name}Service`,
          modelName: api.name
        });
      }
    }

    // 检测模型/数据层需求
    const modelKeywords = ['model', 'schema', 'entity', '数据模型', '表'];
    if (modelKeywords.some(k => lowerReq.includes(k)) || analysis.hasAPI) {
      analysis.hasModels = true;
      for (const api of analysis.apis) {
        analysis.models.push({ name: api.name });
      }
    }

    // 检测数据库需求
    const dbKeywords = ['database', 'db', 'mongodb', 'mysql', 'postgres', 'redis', '数据库'];
    if (dbKeywords.some(k => lowerReq.includes(k))) {
      analysis.hasDatabase = true;
    }

    // 检测中间件需求
    const mwKeywords = ['middleware', 'auth', '验证', '权限', 'cors'];
    if (mwKeywords.some(k => lowerReq.includes(k))) {
      analysis.hasMiddleware = true;
      if (lowerReq.includes('auth') || lowerReq.includes('验证')) {
        analysis.middleware.push({ name: 'auth' });
      }
      if (lowerReq.includes('cors')) {
        analysis.middleware.push({ name: 'cors' });
      }
    }

    // 默认：如果检测不到具体模块但有 API 需求，添加基础控制器和服务
    if (analysis.hasAPI && !analysis.hasControllers) {
      analysis.hasControllers = true;
      analysis.controllers.push({ name: 'index', serviceName: 'indexService' });
    }
    if (analysis.hasAPI && !analysis.hasServices) {
      analysis.hasServices = true;
      analysis.services.push({ name: 'indexService', modelName: 'index' });
    }

    return analysis;
  }

  /**
   * 获取入口文件的依赖
   * @private
   */
  _getEntryDependencies(moduleAnalysis, template, language) {
    const deps = [];
    const base = template.base ? `${template.base}/` : '';
    const ext = template.extensions[language === 'python' ? 'py' : language === 'go' ? 'go' : 'ts'] || '.js';

    if (moduleAnalysis.hasAPI) {
      deps.push(`${base}${template.layers.routes}/index.${ext}`);
    }
    if (moduleAnalysis.hasConfig) {
      deps.push(`${base}${template.layers.config}/index.${ext}`);
    }

    return deps;
  }

  // ═══════════════════════════════════════════════════════════════
  // 核心功能 3: 生成项目结构
  // ═══════════════════════════════════════════════════════════════

  /**
   * 生成完整目录结构
   *
   * 基于多文件计划生成目录树
   * 同时调用 codeKnowledge.getPatterns 检索已有模式
   * 生成的文件内容优先用已有模式，无模式再用模板
   *
   * @param {Object} multiFilePlan - 多文件项目计划（planMultiFile 的输出）
   * @param {string} basePath - 基础路径（如 './my-project'）
   * @returns {Object} {
   *   structure: { [dir]: string[] },  // 目录结构：{ 目录: [文件列表] }
   *   files: Object[],  // 完整的文件内容列表
   *   patterns: { used: string[], missing: string[] }  // 使用的模式和缺失的模式
   * }
   *
   * @example
   * const plan = codePlanner.planMultiFile('my-api', '创建用户API', 'typescript');
   * const structure = codePlanner.generateProjectStructure(plan, './my-api');
   * // structure.files[0].content 包含从 codeKnowledge 获取的模式或生成的模板
   */
  generateProjectStructure(multiFilePlan, basePath = './project') {
    // 构建目录结构
    const structure = {};
    const files = [];
    const usedPatterns = [];
    const missingPatterns = [];

    // 按目录分组
    for (const filePlan of multiFilePlan.files) {
      const dir = path.dirname(filePlan.path);
      if (!structure[dir]) {
        structure[dir] = [];
      }
      structure[dir].push(path.basename(filePlan.path));
    }

    // 为每个文件生成内容
    for (const filePlan of multiFilePlan.files) {
      const filePath = path.join(basePath, filePlan.path);

      // 尝试从 codeKnowledge 获取已有模式
      let content = null;
      let patternName = null;

      if (this.codeKnowledge?.getPatterns) {
        // 根据文件类型和层级获取对应的模式
        patternName = this._getPatternNameForFile(filePlan, multiFilePlan.language);
        const patterns = this.codeKnowledge.getPatterns(patternName);

        if (patterns && patterns.length > 0) {
          // 使用第一个匹配的模式作为模板
          const pattern = patterns[0];
          content = this._applyPatternToFile(pattern, filePlan, multiFilePlan);
          usedPatterns.push(patternName);
        } else {
          missingPatterns.push(patternName);
        }
      }

      // 如果没有找到模式，使用默认模板生成内容
      if (content === null) {
        content = this._generateFileTemplate(filePlan, multiFilePlan);
        missingPatterns.push('template:' + filePlan.layer);
      }

      files.push({
        path: filePath,
        relativePath: filePlan.path,
        layer: filePlan.layer,
        action: filePlan.action,
        deps: filePlan.deps,
        content,
        patternUsed: patternName
      });
    }

    return {
      structure,
      files,
      patterns: {
        used: usedPatterns,
        missing: missingPatterns
      },
      basePath,
      createdAt: new Date().toISOString()
    };
  }

  /**
   * 根据文件获取对应的模式名称
   * @private
   */
  _getPatternNameForFile(filePlan, language) {
    const layer = filePlan.layer;
    const lang = language || 'javascript';

    // 模式名称映射
    const patternMap = {
      entry: 'main-entry',
      routes: `${lang}-api-routes`,
      controllers: `${lang}-controller`,
      services: `${lang}-service`,
      models: `${lang}-model`,
      middleware: `${lang}-middleware`,
      utils: `${lang}-util`,
      config: `${lang}-config`,
      db: `${lang}-database`
    };

    return patternMap[layer] || `${lang}-generic`;
  }

  /**
   * 将模式应用到文件
   * @private
   */
  _applyPatternToFile(pattern, filePlan, multiFilePlan) {
    // 替换占位符
    let content = pattern.content || '';

    // 替换项目名
    content = content.replace(/\$\{projectName\}/g, multiFilePlan.projectName);
    content = content.replace(/\$PROJECT_NAME\$/g, multiFilePlan.projectName);

    // 替换文件名
    content = content.replace(/\$\{fileName\}/g, path.basename(filePlan.path, path.extname(filePlan.path)));
    content = content.replace(/\$\{FILE_NAME\}/g, path.basename(filePlan.path, path.extname(filePlan.path)).toUpperCase());

    // 替换依赖
    if (filePlan.deps && filePlan.deps.length > 0) {
      const depsImports = this._generateImportStatements(filePlan.deps, multiFilePlan.language);
      content = content.replace(/\$\{imports\}/g, depsImports);
    }

    // 替换层级
    content = content.replace(/\$\{layer\}/g, filePlan.layer);

    return content;
  }

  /**
   * 生成导入语句（根据语言）
   * @private
   */
  _generateImportStatements(deps, language) {
    const imports = [];

    for (const dep of deps) {
      const moduleName = path.basename(dep, path.extname(dep));
      const fullPath = dep.startsWith('.') ? dep : `./${dep}`;

      switch (language) {
        case 'javascript':
          imports.push(`const ${moduleName} = require('${fullPath}');`);
          break;
        case 'typescript':
          // TypeScript 默认使用 ESM 导入
          imports.push(`import ${moduleName} from '${fullPath}';`);
          break;
        case 'python':
          imports.push(`from ${moduleName} import (  # TODO: 填充具体导入名\n)`);
          break;
        case 'go':
          imports.push(`import "${moduleName}"  // 注意：Go 中请使用实际包的完整导入路径`);
          break;
        default:
          imports.push(`// import ${moduleName}`);
      }
    }

    return imports.join('\n');
  }

  /**
   * 生成文件模板
   * @private
   */
  _generateFileTemplate(filePlan, multiFilePlan) {
    const ext = path.extname(filePlan.path);
    const fileName = path.basename(filePlan.path, ext);
    const lang = multiFilePlan.language;
    const projectName = multiFilePlan.projectName;

    // 根据层级生成不同的模板内容
    switch (filePlan.layer) {
      case 'entry':
        return this._generateEntryTemplate(fileName, ext, lang, multiFilePlan);
      case 'routes':
        return this._generateRoutesTemplate(fileName, ext, lang, multiFilePlan);
      case 'controllers':
        return this._generateControllerTemplate(fileName, ext, lang, multiFilePlan);
      case 'services':
        return this._generateServiceTemplate(fileName, ext, lang, multiFilePlan);
      case 'models':
        return this._generateModelTemplate(fileName, ext, lang, multiFilePlan);
      case 'middleware':
        return this._generateMiddlewareTemplate(fileName, ext, lang, multiFilePlan);
      case 'utils':
        return this._generateUtilsTemplate(fileName, ext, lang, multiFilePlan);
      case 'config':
        return this._generateConfigTemplate(fileName, ext, lang, multiFilePlan);
      case 'db':
        return this._generateDbTemplate(fileName, ext, lang, multiFilePlan);
      default:
        return this._generateGenericTemplate(fileName, ext, lang, projectName);
    }
  }

  /**
   * 生成入口文件模板
   * @private
   */
  _generateEntryTemplate(fileName, ext, lang, plan) {
    switch (lang) {
      case 'typescript':
        return `/**
 * ${plan.projectName} - 入口文件
 * 生成时间: ${new Date().toISOString()}
 */

// 导入配置
import config from './config';
// 导入路由
import routes from './routes';

// 应用启动
const app = async () => {
  console.log('正在启动 ${plan.projectName}...');

  // 初始化中间件
  // ...

  // 注册路由
  // await app.use(routes);

  console.log('${plan.projectName} 启动完成');
};

// 导出应用
export default app;
`;
      case 'python':
        return `"""
${plan.projectName} - 入口文件
生成时间: ${new Date().toISOString()}
"""

from app.routes import api_router


def create_app():
    """创建应用实例"""
    app = FastAPI()

    # 注册路由
    app.include_router(api_router, prefix="/api")

    return app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
`;
      default:
        return `/**
 * ${plan.projectName} - 入口文件
 * 生成时间: ${new Date().toISOString()}
 */

// 导入配置
const config = require('./config');
// 导入路由
const routes = require('./routes');

// 应用启动
const app = async () => {
  console.log('正在启动 ${plan.projectName}...');

  // 初始化中间件
  // ...

  // 注册路由
  // await app.use(routes);

  console.log('${plan.projectName} 启动完成');
};

// 导出应用
module.exports = app;
`;
    }
  }

  /**
   * 生成路由模板
   * @private
   */
  _generateRoutesTemplate(fileName, ext, lang, plan) {
    const routerName = fileName === 'index' ? 'apiRouter' : `${fileName}Router`;

    switch (lang) {
      case 'typescript':
        return `/**
 * ${fileName} 路由
 */
import { Router } from 'express';
import { ${fileName}Controller } from '../controllers/${fileName}';

const router = Router();

// 定义路由
router.get('/', ${fileName}Controller.getAll);
router.get('/:id', ${fileName}Controller.getById);
router.post('/', ${fileName}Controller.create);
router.put('/:id', ${fileName}Controller.update);
router.delete('/:id', ${fileName}Controller.delete);

export default router;
`;
      default:
        return `/**
 * ${fileName} 路由
 */
const express = require('express');
const router = express.Router();
const ${fileName}Controller = require('../controllers/${fileName}');

// 定义路由
router.get('/', ${fileName}Controller.getAll);
router.get('/:id', ${fileName}Controller.getById);
router.post('/', ${fileName}Controller.create);
router.put('/:id', ${fileName}Controller.update);
router.delete('/:id', ${fileName}Controller.delete);

module.exports = router;
`;
    }
  }

  /**
   * 生成控制器模板
   * @private
   */
  _generateControllerTemplate(fileName, ext, lang, plan) {
    const serviceName = `${fileName}Service`;

    switch (lang) {
      case 'typescript':
        return `/**
 * ${fileName} 控制器
 */
import { Request, Response } from 'express';
import { ${serviceName} } from '../services/${fileName}';

const ${fileName}Controller = {
  async getAll(req: Request, res: Response) {
    try {
      const data = await ${serviceName}.getAll();
      res.json({ success: true, data });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  },

  async getById(req: Request, res: Response) {
    try {
      const { id } = req.params;
      const data = await ${serviceName}.getById(id);
      res.json({ success: true, data });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  },

  async create(req: Request, res: Response) {
    try {
      const data = await ${serviceName}.create(req.body);
      res.status(201).json({ success: true, data });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  },

  async update(req: Request, res: Response) {
    try {
      const { id } = req.params;
      const data = await ${serviceName}.update(id, req.body);
      res.json({ success: true, data });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  },

  async delete(req: Request, res: Response) {
    try {
      const { id } = req.params;
      await ${serviceName}.delete(id);
      res.json({ success: true });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  }
};

export { ${fileName}Controller };
`;
      default:
        return `/**
 * ${fileName} 控制器
 */
const ${fileName}Service = require('../services/${fileName}');

const ${fileName}Controller = {
  async getAll(req, res) {
    try {
      const data = await ${fileName}Service.getAll();
      res.json({ success: true, data });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  },

  async getById(req, res) {
    try {
      const { id } = req.params;
      const data = await ${fileName}Service.getById(id);
      res.json({ success: true, data });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  },

  async create(req, res) {
    try {
      const data = await ${fileName}Service.create(req.body);
      res.status(201).json({ success: true, data });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  },

  async update(req, res) {
    try {
      const { id } = req.params;
      const data = await ${fileName}Service.update(id, req.body);
      res.json({ success: true, data });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  },

  async delete(req, res) {
    try {
      const { id } = req.params;
      await ${fileName}Service.delete(id);
      res.json({ success: true });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  }
};

module.exports = ${fileName}Controller;
`;
    }
  }

  /**
   * 生成服务层模板
   * @private
   */
  _generateServiceTemplate(fileName, ext, lang, plan) {
    const modelName = fileName.replace(/Service$/i, '');

    switch (lang) {
      case 'typescript':
        return `/**
 * ${fileName} 服务层
 */
import { ${modelName}Model } from '../models/${modelName}';
import logger from '../utils/logger';

const ${fileName} = {
  async getAll() {
    try {
      const data = await ${modelName}Model.findAll();
      return data;
    } catch (error) {
      logger.error('获取数据失败', error);
      throw error;
    }
  },

  async getById(id) {
    try {
      const data = await ${modelName}Model.findById(id);
      return data;
    } catch (error) {
      logger.error('获取数据失败', error);
      throw error;
    }
  },

  async create(data) {
    try {
      const result = await ${modelName}Model.create(data);
      return result;
    } catch (error) {
      logger.error('创建数据失败', error);
      throw error;
    }
  },

  async update(id, data) {
    try {
      const result = await ${modelName}Model.update(id, data);
      return result;
    } catch (error) {
      logger.error('更新数据失败', error);
      throw error;
    }
  },

  async delete(id) {
    try {
      await ${modelName}Model.delete(id);
      return true;
    } catch (error) {
      logger.error('删除数据失败', error);
      throw error;
    }
  }
};

export { ${fileName} };
`;
      default:
        return `/**
 * ${fileName} 服务层
 */
const { ${modelName}Model } = require('../models/${modelName}');
const logger = require('../utils/logger');

const ${fileName} = {
  async getAll() {
    try {
      const data = await ${modelName}Model.findAll();
      return data;
    } catch (error) {
      logger.error('获取数据失败', error);
      throw error;
    }
  },

  async getById(id) {
    try {
      const data = await ${modelName}Model.findById(id);
      return data;
    } catch (error) {
      logger.error('获取数据失败', error);
      throw error;
    }
  },

  async create(data) {
    try {
      const result = await ${modelName}Model.create(data);
      return result;
    } catch (error) {
      logger.error('创建数据失败', error);
      throw error;
    }
  },

  async update(id, data) {
    try {
      const result = await ${modelName}Model.update(id, data);
      return result;
    } catch (error) {
      logger.error('更新数据失败', error);
      throw error;
    }
  },

  async delete(id) {
    try {
      await ${modelName}Model.delete(id);
      return true;
    } catch (error) {
      logger.error('删除数据失败', error);
      throw error;
    }
  }
};

module.exports = ${fileName};
`;
    }
  }

  /**
   * 生成模型层模板
   * @private
   */
  _generateModelTemplate(fileName, ext, lang, plan) {
    switch (lang) {
      case 'typescript':
        return `/**
 * ${fileName} 数据模型
 */
import { db } from '../db/connection';

// 定义数据结构接口
interface I${fileName} {
  id?: string;
  // 添加字段...
  createdAt?: Date;
  updatedAt?: Date;
}

const ${fileName}Model = {
  async findAll() {
    const query = 'SELECT * FROM ${fileName.toLowerCase()}s';
    return await db.query(query);
  },

  async findById(id: string) {
    const query = 'SELECT * FROM ${fileName.toLowerCase()}s WHERE id = ?';
    const results = await db.query(query, [id]);
    return results[0];
  },

  async create(data: I${fileName}) {
    const query = 'INSERT INTO ${fileName.toLowerCase()}s SET ?';
    const result = await db.query(query, data);
    return { id: result.insertId, ...data };
  },

  async update(id: string, data: Partial<I${fileName}>) {
    const query = 'UPDATE ${fileName.toLowerCase()}s SET ? WHERE id = ?';
    await db.query(query, [data, id]);
    return this.findById(id);
  },

  async delete(id: string) {
    const query = 'DELETE FROM ${fileName.toLowerCase()}s WHERE id = ?';
    await db.query(query, [id]);
    return true;
  }
};

export { ${fileName}Model, I${fileName} };
`;
      default:
        return `/**
 * ${fileName} 数据模型
 */
const db = require('../db/connection');

const ${fileName}Model = {
  async findAll() {
    const query = 'SELECT * FROM ${fileName.toLowerCase()}s';
    return await db.query(query);
  },

  async findById(id) {
    const query = 'SELECT * FROM ${fileName.toLowerCase()}s WHERE id = ?';
    const results = await db.query(query, [id]);
    return results[0];
  },

  async create(data) {
    const query = 'INSERT INTO ${fileName.toLowerCase()}s SET ?';
    const result = await db.query(query, data);
    return { id: result.insertId, ...data };
  },

  async update(id, data) {
    const query = 'UPDATE ${fileName.toLowerCase()}s SET ? WHERE id = ?';
    await db.query(query, [data, id]);
    return this.findById(id);
  },

  async delete(id) {
    const query = 'DELETE FROM ${fileName.toLowerCase()}s WHERE id = ?';
    await db.query(query, [id]);
    return true;
  }
};

module.exports = { ${fileName}Model };
`;
    }
  }

  /**
   * 生成中间件模板
   * @private
   */
  _generateMiddlewareTemplate(fileName, ext, lang, plan) {
    switch (lang) {
      case 'typescript':
        return `/**
 * ${fileName} 中间件
 */
import { Request, Response, NextFunction } from 'express';

const ${fileName}Middleware = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  // 中间件逻辑
  // ...

  // 继续处理
  next();
};

export default ${fileName}Middleware;
`;
      default:
        return `/**
 * ${fileName} 中间件
 */
const ${fileName}Middleware = (req, res, next) => {
  // 中间件逻辑
  // ...

  // 继续处理
  next();
};

module.exports = ${fileName}Middleware;
`;
    }
  }

  /**
   * 生成工具函数模板
   * @private
   */
  _generateUtilsTemplate(fileName, ext, lang, plan) {
    if (fileName === 'logger') {
      switch (lang) {
        case 'typescript':
          return `/**
 * 日志工具
 */
type LogLevel = 'debug' | 'info' | 'warn' | 'error';

const formatMessage = (level: LogLevel, message: string, meta?: object) => {
  const timestamp = new Date().toISOString();
  return JSON.stringify({
    timestamp,
    level,
    message,
    ...meta
  });
};

const logger = {
  debug(message: string, meta?: object) {
    console.log(formatMessage('debug', message, meta));
  },
  info(message: string, meta?: object) {
    console.log(formatMessage('info', message, meta));
  },
  warn(message: string, meta?: object) {
    console.warn(formatMessage('warn', message, meta));
  },
  error(message: string, meta?: object) {
    console.error(formatMessage('error', message, meta));
  }
};

export default logger;
`;
        default:
          return `/**
 * 日志工具
 */

/**
 * 格式化日志消息
 * @param {string} level - 日志级别
 * @param {string} message - 日志消息
 * @param {object} meta - 附加元数据
 */
const formatMessage = (level, message, meta = {}) => {
  const timestamp = new Date().toISOString();
  return JSON.stringify({
    timestamp,
    level,
    message,
    ...meta
  });
};

const logger = {
  debug(message, meta) {
    console.log(formatMessage('debug', message, meta));
  },
  info(message, meta) {
    console.log(formatMessage('info', message, meta));
  },
  warn(message, meta) {
    console.warn(formatMessage('warn', message, meta));
  },
  error(message, meta) {
    console.error(formatMessage('error', message, meta));
  }
};

module.exports = logger;
`;
      }
    } else {
      // helpers 工具文件
      switch (lang) {
        case 'typescript':
          return `/**
 * 辅助函数
 */

/**
 * 深拷贝
 */
function deepClone<T>(obj: T): T {
  return JSON.parse(JSON.stringify(obj));
}

/**
 * 防抖
 */
function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout | null = null;
  return function(this: any, ...args: Parameters<T>) {
    if (timeout) clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

/**
 * 节流
 */
function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean = false;
  return function(this: any, ...args: Parameters<T>) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

module.exports = { deepClone, debounce, throttle };
`;
        default:
          return `/**
 * 辅助函数
 */

/**
 * 深拷贝
 */
function deepClone(obj) {
  return JSON.parse(JSON.stringify(obj));
}

/**
 * 防抖
 */
function debounce(func, wait) {
  let timeout = null;
  return function(...args) {
    if (timeout) clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

/**
 * 节流
 */
function throttle(func, limit) {
  let inThrottle = false;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

module.exports = { deepClone, debounce, throttle };
`;
      }
    }
  }

  /**
   * 生成配置模板
   * @private
   */
  _generateConfigTemplate(fileName, ext, lang, plan) {
    switch (lang) {
      case 'typescript':
        return `/**
 * 项目配置
 */
export const config = {
  // 环境
  env: process.env.NODE_ENV || 'development',

  // 服务器配置
  server: {
    port: parseInt(process.env.PORT || '3000', 10),
    host: process.env.HOST || 'localhost'
  },

  // 数据库配置
  database: {
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '5432', 10),
    name: process.env.DB_NAME || '${plan.projectName}',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || ''
  },

  // 日志配置
  logging: {
    level: process.env.LOG_LEVEL || 'info'
  }
};

export default config;
`;
      default:
        return `/**
 * 项目配置
 */
module.exports = {
  // 环境
  env: process.env.NODE_ENV || 'development',

  // 服务器配置
  server: {
    port: parseInt(process.env.PORT || '3000', 10),
    host: process.env.HOST || 'localhost'
  },

  // 数据库配置
  database: {
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '5432', 10),
    name: process.env.DB_NAME || '${plan.projectName}',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || ''
  },

  // 日志配置
  logging: {
    level: process.env.LOG_LEVEL || 'info'
  }
};
`;
    }
  }

  /**
   * 生成数据库连接模板
   * @private
   */
  _generateDbTemplate(fileName, ext, lang, plan) {
    switch (lang) {
      case 'typescript':
        return `/**
 * 数据库连接
 */
import { Client } from 'pg';
import config from '../config';

let pool = null;

export const db = {
  async query(text: string, params?: any[]) {
    if (!pool) {
      pool = new Client({
        host: config.database.host,
        port: config.database.port,
        database: config.database.name,
        user: config.database.user,
        password: config.database.password
      });
      await pool.connect();
    }
    return pool.query(text, params);
  },

  async close() {
    if (pool) {
      await pool.end();
      pool = null;
    }
  }
};

export default db;
`;
      default:
        return `/**
 * 数据库连接
 */
const { Client } = require('pg');
const config = require('../config');

let pool = null;

const db = {
  async query(text, params) {
    if (!pool) {
      pool = new Client({
        host: config.database.host,
        port: config.database.port,
        database: config.database.name,
        user: config.database.user,
        password: config.database.password
      });
      await pool.connect();
    }
    return pool.query(text, params);
  },

  async close() {
    if (pool) {
      await pool.end();
      pool = null;
    }
  }
};

module.exports = db;
`;
    }
  }

  /**
   * 生成通用模板
   * @private
   */
  _generateGenericTemplate(fileName, ext, lang, projectName) {
    return `/**
 * ${fileName}
 * 项目: ${projectName}
 * 生成时间: ${new Date().toISOString()}
 */
`;
  }

  // ─────────────────────────────────────────
  // 公共调度方法
  // ─────────────────────────────────────────

  /**
   * 主规划方法
   *
   * 支持两种模式：
   * 1. 单文件模式（默认）：普通任务分解
   * 2. 多文件模式：设置 multiFile: true 和 projectName 触发
   *
   * @param {string} problem - 问题描述
   * @param {string} language - 目标编程语言
   * @param {Object} options - 可选配置
   * @param {boolean} options.multiFile - 是否启用多文件模式
   * @param {string} options.projectName - 项目名称（多文件模式必需）
   * @returns {Object} 完整执行计划
   */
  plan(problem, language = 'javascript', options = {}) {
    // 检查是否启用多文件模式
    if (options.multiFile && options.projectName) {
      return this.planMultiFile(options.projectName, problem, language);
    }

    // 1. 理解任务（CognitiveProtocol 协同）
    const understanding = this._understandTask(problem);

    // 2. 识别任务类型
    const taskType = this._identifyTaskType(problem);

    // 3. 解析依赖
    const dependencies = this._parseDependencies(problem, language);

    // 4. 分解任务
    const taskTypeObj = typeof taskType === 'string'
      ? { type: taskType, confidence: 1.0 }
      : taskType;

    const decomposition = this.decompose({
      problem,
      taskType: taskTypeObj,
      language,
      dependencies
    });

    // 5. 生成路径规划
    const plan = this._generatePathPlan(decomposition, language);

    // 6. 评估复杂度
    const complexity = this._assessComplexity(plan, dependencies);

    // 7. 构建依赖图（新增）
    const dependencyGraph = this.buildDependencyGraph(plan.steps);

    // 8. 组装完整计划
    this.currentPlan = {
      ...plan,
      originalProblem: problem,
      taskType,
      language,
      dependencies,
      estimatedComplexity: complexity,
      dependencyGraph,  // 包含 graph, cycles, order
      createdAt: new Date().toISOString()
    };

    // 更新统计
    this.stats.plansCreated++;
    this.stats.avgStepsPerPlan =
      (this.stats.avgStepsPerPlan * (this.stats.plansCreated - 1) + plan.steps.length) /
      this.stats.plansCreated;

    return this.currentPlan;
  }

  /**
   * 分解任务为子任务
   *
   * 如果返回包含 files 数组的计划，自动构建依赖图
   *
   * @param {Object} task - 任务对象
   * @returns {Object} 分解后的子任务结构
   */
  decompose(task) {
    const { problem, taskType, language } = task;
    const steps = [];
    let stepIdCounter = 1;

    // 基础步骤识别（提取文件路径）
    const baseSteps = this._extractBaseSteps(problem, taskType);
    const identifiedFiles = baseSteps.filter(s => s.file).map(s => s.file);

    // 依赖分析
    const deps = this._analyzeDependencies(task.dependencies || []);

    // 检查是否为多文件任务（检测多个文件路径）
    const multiFileTask = this._detectMultiFileTask(problem, identifiedFiles);

    // 如果检测到多文件任务，使用多文件分解逻辑
    if (multiFileTask.isMultiFile) {
      return this._decomposeMultiFileTask(task, multiFileTask, deps);
    }

    // 根据任务类型生成具体步骤（单文件模式）
    switch (taskType.type || taskType) {
      case TASK_TYPE.CREATE:
        steps.push(...this._generateCreateSteps(problem, language, deps, identifiedFiles));
        break;
      case TASK_TYPE.MODIFY:
        steps.push(...this._generateModifySteps(problem, language, deps, identifiedFiles));
        break;
      case TASK_TYPE.FIX:
        steps.push(...this._generateFixSteps(problem, language, deps, identifiedFiles));
        break;
      case TASK_TYPE.OPTIMIZE:
        steps.push(...this._generateOptimizeSteps(problem, language, deps, identifiedFiles));
        break;
      case TASK_TYPE.REFACTOR:
        steps.push(...this._generateRefactorSteps(problem, language, deps, identifiedFiles));
        break;
      default:
        steps.push(...this._generateGenericSteps(problem, language, deps, identifiedFiles));
    }

    // 拓扑排序确保依赖顺序
    const sortedSteps = this._topologicalSort(steps);

    // 重新编号
    sortedSteps.forEach((step, index) => {
      step.id = index + 1;
    });

    // 确定入口文件
    const entryFile = this._determineEntryFile(sortedSteps, language);

    // 构建依赖图（单文件模式也构建，便于后续分析）
    const dependencyGraph = this.buildDependencyGraph(sortedSteps);

    // 更新统计
    this.stats.tasksDecomposed++;

    return {
      steps: sortedSteps,
      entryFile,
      dependencies: deps,
      taskType,
      originalProblem: problem,
      files: sortedSteps.filter(s => s.file).map(s => ({ path: s.file, action: s.action, deps: s.deps })),
      dependencyGraph
    };
  }

  /**
   * 检测是否为多文件任务
   * @private
   */
  _detectMultiFileTask(problem, identifiedFiles) {
    const result = {
      isMultiFile: false,
      files: [],
      modules: []
    };

    // 方法1: 已识别的文件数量
    if (identifiedFiles.length >= 2) {
      result.isMultiFile = true;
      result.files = identifiedFiles;
    }

    // 方法2: 关键词检测
    const multiFileKeywords = [
      'api', 'controller', 'service', 'model', 'router', 'middleware',
      'routes', 'handlers', 'repository', 'repository'
    ];
    const problemLower = problem.toLowerCase();
    for (const keyword of multiFileKeywords) {
      if (problemLower.includes(keyword)) {
        result.modules.push(keyword);
      }
    }

    if (result.modules.length >= 2) {
      result.isMultiFile = true;
    }

    // 方法3: 模块化描述模式
    const modulePatterns = [
      /(?:api|模块|层)\s*[：:]\s*([\w/,]+)/gi,
      /(?:包括|包含)\s+([\w\s,]+(?:Controller|Service|Model|Route))/gi
    ];
    for (const pattern of modulePatterns) {
      const matches = problem.match(pattern);
      if (matches) {
        result.isMultiFile = true;
      }
    }

    return result;
  }

  /**
   * 多文件任务分解
   * @private
   */
  _decomposeMultiFileTask(task, multiFileAnalysis, deps) {
    const { problem, taskType, language } = task;
    const files = [];
    let fileIdCounter = 1;

    // 根据语言确定目录结构
    const dirStructure = this._getDirStructure(language);

    // 为每个识别的文件创建计划
    for (const filePath of multiFileAnalysis.files) {
      const fileName = path.basename(filePath, path.extname(filePath));
      const layer = this._classifyFileLayer(fileName, language);

      files.push({
        id: fileIdCounter++,
        path: filePath,
        action: 'create',
        deps: this._getFileDependencies(fileName, layer, dirStructure, language),
        layer,
        description: `创建 ${layer} 层文件: ${fileName}`
      });
    }

    // 为检测到的模块创建计划
    for (const moduleName of multiFileAnalysis.modules) {
      const layer = this._classifyModuleLayer(moduleName);
      const ext = this._getExtension(language);
      const filePath = `${dirStructure.base}/${dirStructure[layer]}/${moduleName}.${ext}`;

      files.push({
        id: fileIdCounter++,
        path: filePath,
        action: 'create',
        deps: this._getFileDependencies(moduleName, layer, dirStructure, language),
        layer,
        description: `创建 ${layer} 层: ${moduleName}`
      });
    }

    // 拓扑排序确保依赖顺序
    const sortedFiles = this._topologicalSortByPath(files);

    // 重新编号
    sortedFiles.forEach((file, index) => {
      file.id = index + 1;
    });

    // 构建依赖图
    const dependencyGraph = this.buildDependencyGraph(sortedFiles);

    // 确定入口文件
    const entryFile = `${dirStructure.base}/${dirStructure.entry}.${this._getExtension(language)}`;

    // 更新统计
    this.stats.tasksDecomposed++;

    return {
      steps: sortedFiles,
      entryFile,
      dependencies: deps,
      taskType,
      originalProblem: problem,
      files: sortedFiles,
      dependencyGraph,
      isMultiFile: true
    };
  }

  /**
   * 根据语言获取目录结构
   * @private
   */
  _getDirStructure(language) {
    const structures = {
      javascript: {
        base: 'src',
        entry: 'index',
        routes: 'routes',
        controllers: 'controllers',
        services: 'services',
        models: 'models',
        middleware: 'middleware',
        utils: 'utils'
      },
      typescript: {
        base: 'src',
        entry: 'index',
        routes: 'routes',
        controllers: 'controllers',
        services: 'services',
        models: 'models',
        middleware: 'middleware',
        utils: 'utils'
      },
      python: {
        base: 'app',
        entry: '__init__',
        routes: 'api',
        controllers: 'controllers',
        services: 'services',
        models: 'models',
        middleware: 'middleware',
        utils: 'utils'
      },
      go: {
        base: '',
        entry: 'main',
        routes: 'handlers',
        controllers: 'controllers',
        services: 'services',
        models: 'models',
        middleware: 'middleware',
        utils: 'utils'
      }
    };

    return structures[language] || structures.javascript;
  }

  /**
   * 获取文件扩展名
   * @private
   */
  _getExtension(language) {
    const extensions = {
      javascript: 'js',
      typescript: 'ts',
      python: 'py',
      go: 'go',
      rust: 'rs'
    };
    return extensions[language] || 'js';
  }

  /**
   * 分类文件层级
   * @private
   */
  _classifyFileLayer(fileName, language) {
    const lowerName = fileName.toLowerCase();
    const layerPatterns = {
      entry: ['index', 'main', 'app', 'server'],
      routes: ['route', 'router', 'api'],
      controllers: ['controller', 'handler'],
      services: ['service', 'business'],
      models: ['model', 'schema', 'entity'],
      middleware: ['middleware', 'middle', 'auth', 'cors'],
      utils: ['util', 'helper', 'tool']
    };

    for (const [layer, patterns] of Object.entries(layerPatterns)) {
      if (patterns.some(p => lowerName.includes(p))) {
        return layer;
      }
    }

    return 'utils';
  }

  /**
   * 分类模块层级
   * @private
   */
  _classifyModuleLayer(moduleName) {
    const lowerName = moduleName.toLowerCase();
    if (lowerName.includes('route') || lowerName.includes('api')) return 'routes';
    if (lowerName.includes('controller') || lowerName.includes('handler')) return 'controllers';
    if (lowerName.includes('service')) return 'services';
    if (lowerName.includes('model') || lowerName.includes('schema')) return 'models';
    if (lowerName.includes('middleware') || lowerName.includes('auth')) return 'middleware';
    if (lowerName.includes('util') || lowerName.includes('helper')) return 'utils';
    return 'controllers';
  }

  /**
   * 获取文件依赖
   * @private
   */
  _getFileDependencies(fileName, layer, dirStructure, language = 'javascript') {
    const deps = [];
    const base = dirStructure.base ? `${dirStructure.base}/` : '';
    const ext = this._getExtension(language);

    switch (layer) {
      case 'routes':
        deps.push(`${base}${dirStructure.controllers}/${fileName}.${ext}`);
        break;
      case 'controllers':
        deps.push(`${base}${dirStructure.services}/${fileName}Service.${ext}`);
        break;
      case 'services':
        deps.push(`${base}${dirStructure.models}/${fileName}.${ext}`);
        deps.push(`${base}${dirStructure.utils}/logger.${ext}`);
        break;
      case 'models':
        deps.push(`${base}db/connection.${ext}`);
        break;
    }

    return deps;
  }

  /**
   * 按路径拓扑排序（用于多文件分解）
   * @private
   */
  _topologicalSortByPath(steps) {
    // 按层级排序：db -> models -> services -> controllers -> routes -> entry
    const layerOrder = {
      db: 1,
      models: 2,
      utils: 3,
      config: 3,
      services: 4,
      middleware: 3,
      controllers: 5,
      routes: 6,
      entry: 7
    };

    return steps.sort((a, b) => {
      const orderA = layerOrder[a.layer] || 5;
      const orderB = layerOrder[b.layer] || 5;
      if (orderA !== orderB) {
        return orderA - orderB;
      }
      // 同层按路径排序
      return a.path.localeCompare(b.path);
    });
  }

  /**
   * 获取实现路径
   * @param {Object} task - 任务对象
   * @returns {string[]} 实现路径数组
   */
  getPath(task) {
    const { problem, language } = task;

    // 如果没有当前计划，先生成
    if (!this.currentPlan || this.currentPlan.originalProblem !== problem) {
      this.plan(problem, language);
    }

    if (!this.currentPlan) {
      return [];
    }

    // 提取文件路径
    const paths = this.currentPlan.steps
      .filter(step => step.file)
      .map(step => step.file);

    // 去重保持顺序
    return [...new Set(paths)];
  }

  /**
   * 根据执行结果调整计划
   *
   * 关键功能：
   * - 检测失败步骤是否有循环依赖
   * - 发现循环依赖时触发 re-plan
   *
   * @param {Object} plan - 当前计划
   * @param {Object} result - 执行结果
   * @returns {Object} 调整后的计划
   */
  adapt(plan, result) {
    this.stats.adaptationsMade++;

    // 分析失败原因
    const failureAnalysis = this._analyzeFailure(result);

    // 获取失败步骤
    const failedStep = plan.steps.find(s => s.id === result.failedStepId);

    // 检测是否有循环依赖导致的失败
    const cycleFailure = this._detectCycleFailure(plan, failedStep, result);

    if (cycleFailure.hasCycle) {
      // 发现循环依赖，需要重新规划
      console.log(`⚠️ 检测到循环依赖: ${cycleFailure.message}`);
      return this._replanWithCycleDetection(plan, cycleFailure);
    }

    // 根据失败类型调整策略（原有逻辑）
    // 深拷贝计划，避免修改原始对象
    let adaptedPlan = JSON.parse(JSON.stringify(plan));

    switch (failureAnalysis.type) {
      case 'dependency_missing':
        // 添加缺失的依赖
        adaptedPlan = this._handleMissingDependency(adaptedPlan, failureAnalysis);
        break;
      case 'syntax_error':
        // 简化语法错误步骤
        adaptedPlan = this._handleSyntaxError(adaptedPlan, failedStep);
        break;
      case 'logic_error':
        // 添加验证步骤
        adaptedPlan = this._handleLogicError(adaptedPlan, failedStep);
        break;
      case 'execution_error':
        // 重试或回退
        adaptedPlan = this._handleExecutionError(adaptedPlan, failedStep, result);
        break;
      default:
        // 记录未知错误类型
        adaptedPlan.steps.push({
          id: plan.steps.length + 1,
          action: ACTION_TYPE.EXECUTE,
          description: `诊断未知错误: ${failureAnalysis.message}`,
          strategy: 'investigate'
        });
    }

    // 标记调整历史
    adaptedPlan.adaptations = [
      ...(plan.adaptations || []),
      {
        timestamp: new Date().toISOString(),
        originalStepId: result.failedStepId,
        failureType: failureAnalysis.type,
        adjustment: failureAnalysis.adjustment,
        cycleDetection: cycleFailure.hasCycle
      }
    ];

    this.currentPlan = adaptedPlan;
    return adaptedPlan;
  }

  /**
   * 检测循环依赖导致的失败
   * @private
   * @param {Object} plan - 当前计划
   * @param {Object} failedStep - 失败的步骤
   * @param {Object} result - 执行结果
   * @returns {Object} { hasCycle: boolean, cycle: array, message: string }
   */
  _detectCycleFailure(plan, failedStep, result) {
    // 如果计划已经有 dependencyGraph，检查是否有 cycles
    if (plan.dependencyGraph?.cycles && plan.dependencyGraph.cycles.length > 0) {
      return {
        hasCycle: true,
        cycles: plan.dependencyGraph.cycles,
        message: plan.dependencyGraph.cycles.map(c => c.message).join('; ')
      };
    }

    // 从失败消息中检测循环依赖的迹象
    const errorMessage = result.error?.message || '';
    const cycleIndicators = [
      'circular dependency',
      '循环依赖',
      'cycle detected',
      'circular reference',
      'cannot resolve'
    ];

    const hasCycleIndicator = cycleIndicators.some(indicator =>
      errorMessage.toLowerCase().includes(indicator.toLowerCase())
    );

    if (hasCycleIndicator) {
      // 重新构建依赖图检测循环
      const depGraph = this.buildDependencyGraph(plan.steps || []);
      if (depGraph.cycles.length > 0) {
        return {
          hasCycle: true,
          cycles: depGraph.cycles,
          message: depGraph.cycles.map(c => c.message).join('; ')
        };
      }
    }

    // 检查失败步骤是否在循环路径上
    if (failedStep && plan.steps) {
      const depGraph = this.buildDependencyGraph(plan.steps);
      const failedFile = failedStep.file;

      for (const cycle of depGraph.cycles) {
        if (cycle.path.includes(failedFile)) {
          return {
            hasCycle: true,
            cycles: [cycle],
            message: `失败步骤 ${failedStep.id} 在循环路径: ${cycle.path.join(' → ')}`
          };
        }
      }
    }

    return {
      hasCycle: false,
      cycles: [],
      message: ''
    };
  }

  /**
   * 在检测到循环依赖后重新规划
   * @private
   * @param {Object} plan - 原计划
   * @param {Object} cycleFailure - 循环依赖信息
   * @returns {Object} 重新规划后的计划
   */
  _replanWithCycleDetection(plan, cycleFailure) {
    console.log('🔄 触发循环依赖重新规划...');

    // 提取循环中的文件
    const cyclicFiles = new Set();
    for (const cycle of cycleFailure.cycles) {
      for (const file of cycle.path) {
        cyclicFiles.add(file);
      }
    }

    // 过滤掉循环依赖中的文件，创建新的步骤列表
    const nonCyclicSteps = plan.steps.filter(step => {
      if (step.file) {
        return !cyclicFiles.has(step.file);
      }
      return true;
    });

    // 重新拓扑排序
    const sortedSteps = this._topologicalSort(nonCyclicSteps);

    // 重新编号
    sortedSteps.forEach((step, index) => {
      step.id = index + 1;
    });

    // 重新构建依赖图
    const dependencyGraph = this.buildDependencyGraph(sortedSteps);

    // 确定入口文件
    const entryFile = this._determineEntryFile(sortedSteps, plan.language || 'javascript');

    // 记录重新规划的原因
    const replanInfo = {
      originalCycles: cycleFailure.cycles,
      removedFiles: Array.from(cyclicFiles),
      timestamp: new Date().toISOString()
    };

    // 构建新的计划
    const newPlan = {
      ...plan,
      steps: sortedSteps,
      entryFile,
      dependencyGraph,
      cycles: dependencyGraph.cycles,
      replanCount: (plan.replanCount || 0) + 1,
      replanReason: 'circular_dependency',
      replanInfo
    };

    this.currentPlan = newPlan;
    console.log(`✅ 重新规划完成: 移除了 ${cyclicFiles.size} 个循环文件，剩余 ${sortedSteps.length} 个步骤`);

    return newPlan;
  }

  // ─────────────────────────────────────────
  // 私有方法 - 任务理解
  // ─────────────────────────────────────────

  /**
   * 理解任务（与 CognitiveProtocol 协同）
   * @param {string} problem - 问题描述
   * @returns {Object} 理解结果
   */
  _understandTask(problem) {
    // 如果有心虫实例，尝试使用认知协议
    if (this.hf?.dispatch) {
      try {
        const cognitive = this.hf.dispatch('cognitive.understand', problem);
        if (cognitive) {
          return {
            ...cognitive,
           协同: 'CognitiveProtocol'
          };
        }
      } catch (e) {
        // 降级处理
      }
    }

    // 基础理解（无认知协议时）
    return {
      iUnderstand: `我理解这件事是关于"${problem}"的`,
      understanding: problem,
     协同: '基础模式'
    };
  }

  /**
   * 识别任务类型
   * @param {string} problem - 问题描述
   * @returns {string} 任务类型
   */
  _identifyTaskType(problem) {
    const lowerProblem = problem.toLowerCase();
    const scores = {};

    // 计算各类型的匹配分数
    for (const [type, pattern] of Object.entries(TASK_TYPE_PATTERNS)) {
      let score = 0;
      for (const keyword of pattern.keywords) {
        if (lowerProblem.includes(keyword.toLowerCase())) {
          score += pattern.weight;
        }
      }
      scores[type] = score;
    }

    // 找出最高分类型
    let bestType = TASK_TYPE.CREATE;
    let maxScore = 0;

    for (const [type, score] of Object.entries(scores)) {
      if (score > maxScore) {
        maxScore = score;
        bestType = type;
      }
    }

    return {
      type: maxScore > 0 ? bestType : TASK_TYPE.CREATE,
      confidence: maxScore,
      allScores: scores
    };
  }

  // ─────────────────────────────────────────
  // 私有方法 - 依赖解析
  // ─────────────────────────────────────────

  /**
   * 解析依赖
   * @param {string} problem - 问题描述
   * @param {string} language - 编程语言
   * @returns {string[]} 依赖列表
   */
  _parseDependencies(problem, language) {
    const deps = [];
    const lowerProblem = problem.toLowerCase();

    // 通用依赖关键词
    const commonDepPatterns = [
      'react', 'vue', 'angular', 'node', 'express',
      'lodash', 'underscore', 'axios', 'fetch',
      'jest', 'mocha', 'chai', 'supertest',
      'express', 'koa', 'fastify',
      'mongoose', 'sequelize', 'prisma',
      'redux', 'mobx', 'zustand',
      'webpack', 'vite', 'rollup',
      'typescript', 'babel',
      'fs', 'path', 'crypto', 'http'
    ];

    // 检测常见依赖
    for (const dep of commonDepPatterns) {
      if (lowerProblem.includes(dep.toLowerCase())) {
        deps.push(dep);
      }
    }

    // 扫描问题中的 import 语句
    const importMatches = problem.match(/\$import\s+.*?from\s+['"](.*?)['"]/g);
    if (importMatches) {
      for (const match of importMatches) {
        const depMatch = match.match(/from\s+['"](.*?)['"]/);
        if (depMatch && !deps.includes(depMatch[1])) {
          deps.push(depMatch[1]);
        }
      }
    }

    return [...new Set(deps)];
  }

  /**
   * 分析依赖关系
   * @param {string[]} dependencies - 依赖列表
   * @returns {Object} 依赖分析结果
   */
  _analyzeDependencies(dependencies) {
    const result = {
      external: [],      // 外部依赖（npm包等）
      internal: [],       // 内部模块
      peer: [],          // 同级依赖
      builtins: []       // 内置模块
    };

    for (const dep of dependencies) {
      if (this._isExternalDep(dep)) {
        result.external.push(dep);
      } else if (this._isBuiltinDep(dep)) {
        result.builtins.push(dep);
      } else if (this._isInternalDep(dep)) {
        result.internal.push(dep);
      } else {
        result.peer.push(dep);
      }
    }

    return result;
  }

  /**
   * 检测外部依赖
   */
  _isExternalDep(dep) {
    // 非相对路径（不以 . 或 / 开头）即视为外部依赖（npm、pip 包等）
    return !dep.startsWith('.') &&
           !dep.startsWith('/');
  }

  /**
   * 检测内置依赖
   */
  _isBuiltinDep(dep) {
    const builtins = ['fs', 'path', 'crypto', 'http', 'https', 'os', 'util', 'events', 'stream', 'buffer', 'url', 'querystring', 'zlib', 'assert', 'constants', 'domain', 'dns', 'dgram', 'net', 'tls', 'child_process', 'cluster', 'vm', 'module'];
    return builtins.includes(dep);
  }

  /**
   * 检测内部依赖
   */
  _isInternalDep(dep) {
    return dep.startsWith('./') ||
           dep.startsWith('../') ||
           dep.startsWith('@/');
  }

  // ─────────────────────────────────────────
  // 私有方法 - 步骤生成
  // ─────────────────────────────────────────

  /**
   * 提取基础步骤
   * @param {string} problem - 问题描述
   * @param {Object} taskType - 任务类型
   * @returns {Object[]} 基础步骤数组
   */
  _extractBaseSteps(problem, taskType) {
    const steps = [];

    // 识别文件路径
    const fileMatches = problem.match(/[\w/.-]+\.(js|ts|py|go|rs|java|cpp|c|php)/g);
    if (fileMatches) {
      for (const file of fileMatches) {
        steps.push({
          id: steps.length + 1,
          action: taskType.type === TASK_TYPE.CREATE ? ACTION_TYPE.CREATE : ACTION_TYPE.EDIT,
          file,
          description: `处理文件: ${file}`,
          deps: []
        });
      }
    }

    return steps;
  }

  /**
   * 生成创建步骤
   */
  _generateCreateSteps(problem, language, deps, identifiedFiles) {
    const steps = [];

    // 使用识别到的文件，或提取文件名
    const fileName = identifiedFiles[0] || this._extractFileName(problem, language);

    // 1. 安装依赖
    if (deps.external.length > 0) {
      steps.push({
        id: 1,
        action: ACTION_TYPE.EXECUTE,
        description: `安装外部依赖: ${deps.external.join(', ')}`,
        command: `npm install ${deps.external.join(' ')}`,
        deps: []
      });
    }

    // 2. 创建文件（id 根据是否有前置步骤动态计算）
    const createId = deps.external.length > 0 ? 2 : 1;
    steps.push({
      id: createId,
      action: ACTION_TYPE.CREATE,
      file: fileName,
      description: `创建新文件: ${fileName}`,
      deps: deps.external.length > 0 ? [1] : []
    });

    // 3. 添加导出（deps 引用创建步骤的 id）
    steps.push({
      id: createId + 1,
      action: ACTION_TYPE.EDIT,
      file: fileName,
      description: `添加模块导出`,
      deps: [createId]
    });

    return steps;
  }

  /**
   * 生成修改步骤
   */
  _generateModifySteps(problem, language, deps, identifiedFiles) {
    const steps = [];
    const files = identifiedFiles.length > 0 ? identifiedFiles : this._extractFiles(problem, language);

    // 1. 备份原文件
    files.forEach((file, index) => {
      steps.push({
        id: index + 1,
        action: ACTION_TYPE.EXECUTE,
        description: `备份文件: ${file}`,
        command: `cp ${file} ${file}.backup`,
        deps: []
      });
    });

    // 2. 修改文件
    const editStartId = steps.length + 1;
    files.forEach((file, index) => {
      steps.push({
        id: editStartId + index,
        action: ACTION_TYPE.EDIT,
        file,
        description: `修改文件内容: ${file}`,
        deps: [index + 1]
      });
    });

    return steps;
  }

  /**
   * 生成修复步骤
   */
  _generateFixSteps(problem, language, deps, identifiedFiles) {
    const steps = [];
    const fileName = identifiedFiles[0] || this._extractFileName(problem, language);

    // 1. 复现问题
    steps.push({
      id: 1,
      action: ACTION_TYPE.EXECUTE,
      description: `复现问题场景`,
      command: this._generateReproCommand(problem),
      deps: []
    });

    // 2. 定位问题
    steps.push({
      id: 2,
      action: ACTION_TYPE.EXECUTE,
      description: `定位问题根源`,
      strategy: 'investigate',
      file: fileName,
      deps: [1]
    });

    // 3. 修复问题
    steps.push({
      id: 3,
      action: ACTION_TYPE.EDIT,
      file: fileName,
      description: `应用修复方案`,
      strategy: 'fix',
      deps: [2]
    });

    // 4. 验证修复
    steps.push({
      id: 4,
      action: ACTION_TYPE.EXECUTE,
      description: `验证修复是否生效`,
      command: this._generateVerifyCommand(problem),
      deps: [3]
    });

    return steps;
  }

  /**
   * 生成优化步骤
   */
  _generateOptimizeSteps(problem, language, deps, identifiedFiles) {
    const steps = [];
    const fileName = identifiedFiles[0] || this._extractFileName(problem, language);

    // 1. 性能基准测试
    steps.push({
      id: 1,
      action: ACTION_TYPE.EXECUTE,
      description: `运行性能基准测试`,
      strategy: 'benchmark',
      deps: []
    });

    // 2. 识别瓶颈
    steps.push({
      id: 2,
      action: ACTION_TYPE.EXECUTE,
      description: `识别性能瓶颈`,
      strategy: 'profile',
      file: fileName,
      deps: [1]
    });

    // 3. 应用优化
    steps.push({
      id: 3,
      action: ACTION_TYPE.EDIT,
      file: fileName,
      description: `应用性能优化`,
      strategy: 'optimize',
      deps: [2]
    });

    // 4. 对比验证
    steps.push({
      id: 4,
      action: ACTION_TYPE.EXECUTE,
      description: `对比优化效果`,
      strategy: 'compare',
      deps: [3]
    });

    return steps;
  }

  /**
   * 生成重构步骤
   */
  _generateRefactorSteps(problem, language, deps, identifiedFiles) {
    const steps = [];
    const fileName = identifiedFiles[0] || this._extractFileName(problem, language);

    // 1. 分析现有结构
    steps.push({
      id: 1,
      action: ACTION_TYPE.EXECUTE,
      description: `分析现有代码结构`,
      strategy: 'analyze',
      file: fileName,
      deps: []
    });

    // 2. 规划新结构
    steps.push({
      id: 2,
      action: ACTION_TYPE.EXECUTE,
      description: `规划重构方案`,
      strategy: 'plan',
      deps: [1]
    });

    // 3. 分步骤重构
    steps.push({
      id: 3,
      action: ACTION_TYPE.EDIT,
      file: fileName,
      description: `实施分步骤重构`,
      strategy: 'refactor',
      deps: [2]
    });

    // 4. 测试验证
    steps.push({
      id: 4,
      action: ACTION_TYPE.EXECUTE,
      description: `验证重构后功能正常`,
      strategy: 'test',
      deps: [3]
    });

    return steps;
  }

  /**
   * 生成通用步骤
   */
  _generateGenericSteps(problem, language, deps, identifiedFiles) {
    const fileName = identifiedFiles[0] || null;

    return [
      {
        id: 1,
        action: ACTION_TYPE.EXECUTE,
        description: `分析任务需求`,
        deps: []
      },
      {
        id: 2,
        action: ACTION_TYPE.EDIT,
        file: fileName,
        description: `实施解决方案`,
        deps: [1]
      },
      {
        id: 3,
        action: ACTION_TYPE.EXECUTE,
        description: `验证实施结果`,
        deps: [2]
      }
    ];
  }

  // ─────────────────────────────────────────
  // 私有方法 - 路径规划
  // ─────────────────────────────────────────

  /**
   * 生成路径计划
   * @param {Object} decomposition - 任务分解结果
   * @param {string} language - 编程语言
   * @returns {Object} 路径计划
   */
  _generatePathPlan(decomposition, language) {
    // 基于依赖拓扑排序生成执行顺序
    const orderedSteps = this._topologicalSort(decomposition.steps);

    return {
      steps: orderedSteps,
      entryFile: this._determineEntryFile(orderedSteps, language),
      dependencies: decomposition.dependencies,
      executionOrder: orderedSteps.map(s => s.id)
    };
  }

  /**
   * 拓扑排序（基于依赖）
   * @param {Object[]} steps - 步骤数组
   * @returns {Object[]} 排序后的步骤数组
   */
  _topologicalSort(steps) {
    const sorted = [];
    const state = new Map(); // 'white' | 'gray' | 'black'
    const stepMap = new Map(steps.map(s => [s.id, s]));

    const visit = (step) => {
      const currentState = state.get(step.id);
      if (currentState === 'black') return;
      if (currentState === 'gray') {
        console.warn(`[CodePlanner] 检测到循环依赖: ${step.id}，跳过此路径`);
        return;
      }
      state.set(step.id, 'gray');

      // 先访问依赖
      for (const depId of (step.deps || [])) {
        const depStep = stepMap.get(depId);
        if (depStep) {
          visit(depStep);
        }
      }

      state.set(step.id, 'black');
      sorted.push(step);
    };

    for (const step of steps) {
      if (state.get(step.id) !== 'black') {
        visit(step);
      }
    }

    return sorted;
  }

  /**
   * 确定入口文件
   * @param {Object[]} steps - 步骤数组
   * @param {string} language - 编程语言
   * @returns {string} 入口文件路径
   */
  _determineEntryFile(steps, language) {
    // 查找 CREATE 类型的步骤
    const createStep = steps.find(s => s.action === ACTION_TYPE.CREATE && s.file);
    if (createStep) {
      return createStep.file;
    }

    // 查找 EDIT 类型的步骤
    const editStep = steps.find(s => s.action === ACTION_TYPE.EDIT && s.file);
    if (editStep) {
      return editStep.file;
    }

    // 根据语言返回默认入口文件
    const entryFiles = {
      javascript: 'index.js',
      typescript: 'index.ts',
      python: 'main.py',
      go: 'main.go',
      rust: 'main.rs'
    };

    return entryFiles[language] || 'index.js';
  }

  // ─────────────────────────────────────────
  // 私有方法 - 复杂度评估
  // ─────────────────────────────────────────

  /**
   * 评估复杂度
   * @param {Object} plan - 执行计划
   * @param {Object} dependencies - 依赖分析结果
   * @returns {string} 复杂度级别
   */
  _assessComplexity(plan, dependencies) {
    let score = 0;

    // 步骤数量（每个步骤 +1 分）
    score += plan.steps.length;

    // 依赖深度（每层 +2 分）
    const maxDepth = this._calculateDependencyDepth(plan.steps);
    score += maxDepth * 2;

    // 外部依赖数量（每个 +3 分）
    score += (dependencies.external?.length || 0) * 3;

    // 文件数量（每个 +1 分）
    const fileCount = new Set(plan.steps.filter(s => s.file).map(s => s.file)).size;
    score += fileCount;

    // 根据分数评估复杂度
    if (score <= 10) {
      return COMPLEXITY.LOW;
    } else if (score <= 25) {
      return COMPLEXITY.MEDIUM;
    } else {
      return COMPLEXITY.HIGH;
    }
  }

  /**
   * 计算依赖深度（使用迭代避免栈溢出）
   * @param {Object[]} steps - 步骤数组
   * @returns {number} 最大依赖深度
   */
  _calculateDependencyDepth(steps) {
    const depthMap = new Map();
    const stepMap = new Map(steps.map(s => [s.id, s]));
    const maxDepthLimit = this.config.dependencyDepthLimit;

    // 迭代计算深度，使用访问栈检测循环
    const computeDepth = (stepId) => {
      if (depthMap.has(stepId)) {
        return depthMap.get(stepId);
      }

      const step = stepMap.get(stepId);
      if (!step) {
        return 1;
      }

      const deps = step.deps || [];
      if (deps.length === 0) {
        depthMap.set(stepId, 1);
        return 1;
      }

      // 迭代方式计算最大依赖深度
      let maxDepDepth = 1;
      for (const depId of deps) {
        const depDepth = computeDepth(depId);
        maxDepDepth = Math.max(maxDepDepth, depDepth + 1);
        if (maxDepDepth >= maxDepthLimit) {
          break;
        }
      }

      const depth = Math.min(maxDepDepth, maxDepthLimit);
      depthMap.set(stepId, depth);
      return depth;
    };

    // 检测循环依赖并处理
    const visiting = new Set();
    const detectCycle = (stepId, stack) => {
      if (depthMap.has(stepId)) return false;
      if (visiting.has(stepId)) return true;

      visiting.add(stepId);
      stack.push(stepId);

      const step = stepMap.get(stepId);
      if (step?.deps) {
        for (const depId of step.deps) {
          if (detectCycle(depId, stack)) {
            return true;
          }
        }
      }

      stack.pop();
      visiting.delete(stepId);
      return false;
    };

    // 检测所有步骤中的循环
    for (const step of steps) {
      if (detectCycle(step.id, [])) {
        // 存在循环依赖，设置为最大深度
        depthMap.set(step.id, maxDepthLimit);
      } else {
        computeDepth(step.id);
      }
    }

    // 返回最大深度
    let maxDepth = 1;
    for (const depth of depthMap.values()) {
      maxDepth = Math.max(maxDepth, depth);
    }

    return maxDepth;
  }

  // ─────────────────────────────────────────
  // 私有方法 - 自适应调整
  // ─────────────────────────────────────────

  /**
   * 分析失败原因
   * @param {Object} result - 执行结果
   * @returns {Object} 失败分析结果
   */
  _analyzeFailure(result) {
    const errorMessage = result.error?.message || '';
    const errorType = result.error?.type || '';

    // 依赖缺失
    if (errorMessage.includes('not found') ||
        errorMessage.includes('Cannot find module') ||
        errorMessage.includes('ENOENT')) {
      return {
        type: 'dependency_missing',
        message: '依赖模块未找到',
        adjustment: '添加缺失依赖'
      };
    }

    // 语法错误
    if (errorMessage.includes('SyntaxError') ||
        errorMessage.includes('Unexpected') ||
        errorMessage.includes('UnexpectedToken')) {
      return {
        type: 'syntax_error',
        message: '语法错误',
        adjustment: '修复语法'
      };
    }

    // 逻辑错误
    if (errorMessage.includes('TypeError') ||
        errorMessage.includes('ReferenceError') ||
        errorMessage.includes('undefined')) {
      return {
        type: 'logic_error',
        message: '逻辑错误',
        adjustment: '修复逻辑'
      };
    }

    // 执行错误
    if (errorMessage.includes('timeout') ||
        errorMessage.includes('ETIMEDOUT') ||
        errorMessage.includes('ECONNREFUSED')) {
      return {
        type: 'execution_error',
        message: '执行超时或连接错误',
        adjustment: '重试或降级'
      };
    }

    return {
      type: 'unknown',
      message: errorMessage,
      adjustment: '需要人工介入'
    };
  }

  /**
   * 处理缺失依赖
   */
  _handleMissingDependency(plan, failureAnalysis) {
    const missingDep = failureAnalysis.message.match(/module ['"](.*?)['"]/)?.[1] ||
                       failureAnalysis.message.match(/file ['"](.*?)['"]/)?.[1];

    if (missingDep) {
      plan.steps.unshift({
        id: 0,
        action: ACTION_TYPE.EXECUTE,
        description: `安装缺失依赖: ${missingDep}`,
        command: `npm install ${missingDep}`,
        deps: []
      });

      // 重新编号
      plan.steps.forEach((step, index) => {
        step.id = index + 1;
      });
    }

    return plan;
  }

  /**
   * 处理语法错误
   */
  _handleSyntaxError(plan, failedStep) {
    // 添加语法验证步骤
    const verifyStep = {
      id: plan.steps.length + 1,
      action: ACTION_TYPE.EXECUTE,
      description: `语法验证`,
      command: failedStep?.file ? `node --check ${failedStep.file}` : 'node --check',
      deps: [failedStep?.id].filter(Boolean)
    };

    plan.steps.push(verifyStep);
    return plan;
  }

  /**
   * 处理逻辑错误
   */
  _handleLogicError(plan, failedStep) {
    // 添加调试步骤
    plan.steps.push({
      id: plan.steps.length + 1,
      action: ACTION_TYPE.EXECUTE,
      description: `添加调试信息`,
      strategy: 'debug',
      deps: [failedStep?.id].filter(Boolean)
    });

    return plan;
  }

  /**
   * 处理执行错误
   */
  _handleExecutionError(plan, failedStep, result) {
    // 标记重试
    if (failedStep) {
      failedStep.retryCount = (failedStep.retryCount || 0) + 1;

      // 如果重试次数过多，添加回退步骤
      if (failedStep.retryCount > 2) {
        plan.steps.push({
          id: plan.steps.length + 1,
          action: ACTION_TYPE.EXECUTE,
          description: `执行回退策略`,
          strategy: 'fallback',
          deps: [failedStep.id]
        });
      }
    }

    return plan;
  }

  // ─────────────────────────────────────────
  // 私有方法 - 辅助工具
  // ─────────────────────────────────────────

  /**
   * 提取文件名
   */
  _extractFileName(problem, language) {
    const extensions = LANGUAGE_PATTERNS[language]?.extensions || ['.js'];

    for (const ext of extensions) {
      const match = problem.match(new RegExp(`\\w+\\${ext}`));
      if (match) {
        return match[0];
      }
    }

    // 默认文件名
    const defaultNames = {
      javascript: 'new-feature.js',
      typescript: 'new-feature.ts',
      python: 'new_feature.py',
      go: 'new_feature.go',
      rust: 'new_feature.rs'
    };

    return defaultNames[language] || 'new-feature.js';
  }

  /**
   * 提取多个文件
   */
  _extractFiles(problem, language) {
    const extensions = LANGUAGE_PATTERNS[language]?.extensions || ['.js'];
    const files = [];

    for (const ext of extensions) {
      const matches = problem.match(new RegExp(`[\\w/-]+\\${ext}`, 'g'));
      if (matches) {
        files.push(...matches);
      }
    }

    return files.length > 0 ? files : [this._extractFileName(problem, language)];
  }

  /**
   * 生成复现命令
   */
  _generateReproCommand(problem) {
    const lowerProblem = problem.toLowerCase();

    if (lowerProblem.includes('test')) {
      return 'npm test';
    }
    if (lowerProblem.includes('build')) {
      return 'npm run build';
    }

    return 'node index.js';
  }

  /**
   * 生成验证命令
   */
  _generateVerifyCommand(problem) {
    const lowerProblem = problem.toLowerCase();

    if (lowerProblem.includes('test')) {
      return 'npm test';
    }

    return 'npm run verify';
  }

  // ─────────────────────────────────────────
  // 公共工具方法
  // ─────────────────────────────────────────

  /**
   * 获取统计信息
   * @returns {Object} 统计信息
   */
  getStats() {
    return {
      ...this.stats,
      currentPlanSteps: this.currentPlan?.steps?.length || 0,
      taskHistoryCount: this.taskHistory.length,
      executionCacheSize: this.executionCache.size
    };
  }

  /**
   * 获取当前计划
   * @returns {Object} 当前计划
   */
  getCurrentPlan() {
    return this.currentPlan;
  }

  /**
   * 获取任务历史
   * @returns {Object[]} 任务历史
   */
  getTaskHistory() {
    return this.taskHistory;
  }

  /**
   * 清除执行缓存
   */
  clearCache() {
    this.executionCache.clear();
  }

  /**
   * 验证计划完整性
   * @param {Object} plan - 计划对象
   * @returns {Object} 验证结果
   */
  validatePlan(plan) {
    const issues = [];

    // 检查步骤数量
    if (!plan.steps || plan.steps.length === 0) {
      issues.push({ type: 'critical', message: '计划没有步骤' });
    }

    if (plan.steps?.length > this.config.maxStepsPerPlan) {
      issues.push({
        type: 'warning',
        message: `步骤数量(${plan.steps.length})超过建议阈值(${this.config.maxStepsPerPlan})`
      });
    }

    // 检查依赖循环
    const hasCycle = this._hasCircularDependency(plan.steps);
    if (hasCycle) {
      issues.push({ type: 'critical', message: '存在循环依赖' });
    }

    // 检查缺失的依赖引用
    for (const step of (plan.steps || [])) {
      for (const depId of (step.deps || [])) {
        const hasDep = plan.steps.some(s => s.id === depId);
        if (!hasDep) {
          issues.push({
            type: 'error',
            message: `步骤${step.id}依赖的步骤${depId}不存在`
          });
        }
      }
    }

    return {
      valid: issues.filter(i => i.type === 'critical').length === 0,
      issues,
      severityStats: {
        critical: issues.filter(i => i.type === 'critical').length,
        warning: issues.filter(i => i.type === 'warning').length,
        error: issues.filter(i => i.type === 'error').length
      }
    };
  }

  /**
   * 检查循环依赖
   */
  _hasCircularDependency(steps) {
    const visited = new Set();
    const recStack = new Set();

    const hasCycleDFS = (stepId) => {
      visited.add(stepId);
      recStack.add(stepId);

      const step = steps.find(s => s.id === stepId);
      if (step) {
        for (const depId of (step.deps || [])) {
          if (!visited.has(depId)) {
            if (hasCycleDFS(depId)) {
              return true;
            }
          } else if (recStack.has(depId)) {
            return true;
          }
        }
      }

      recStack.delete(stepId);
      return false;
    };

    for (const step of steps) {
      if (!visited.has(step.id)) {
        if (hasCycleDFS(step.id)) {
          return true;
        }
      }
    }

    return false;
  }
}

/**
 * 导出枚举常量供外部使用
 */
const TASK_TYPES = TASK_TYPE;
const COMPLEXITIES = COMPLEXITY;
const ACTIONS = ACTION_TYPE;

/**
 * 导出的功能标识（用于版本检查）
 */
const FEATURES = {
  // v1.0 基础功能
  basic: {
    plan: true,
    decompose: true,
    getPath: true,
    adapt: true
  },
  // v1.1 新增功能
  multiFile: {
    buildDependencyGraph: true,
    planMultiFile: true,
    generateProjectStructure: true
  }
};

module.exports = {
  CodePlanner,
  TASK_TYPE,
  COMPLEXITY,
  ACTION_TYPE,
  TASK_TYPES,
  COMPLEXITIES,
  ACTIONS,
  FEATURES
};