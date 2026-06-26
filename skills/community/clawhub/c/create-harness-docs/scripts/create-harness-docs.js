#!/usr/bin/env node

/**
 * Create Harness Engineering Documentation (智能版)
 * 
 * 自动检测项目类型，生成对应的文档模板
 * 
 * 使用方法:
 *   node create-harness-docs.js --init          # 创建所有文档
 *   node create-harness-docs.js --agents         # 仅创建 AGENTS.md
 *   node create-harness-docs.js --architecture  # 仅创建架构文档
 *   node create-harness-docs.js --quality       # 仅创建质量评级
 *   node create-harness-docs.js --validate      # 验证现有文档
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const PROJECT_ROOT = process.cwd();

const colors = {
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  blue: '\x1b[36m',
  cyan: '\x1b[36m',
  reset: '\x1b[0m'
};

function log(msg, color = 'green') {
  console.log(`${colors[color]}▶${colors.reset} ${msg}`);
}

function error(msg) {
  console.error(`${colors.red}✗${colors.reset} ${msg}`);
}

function success(msg) {
  console.log(`${colors.green}✓${colors.reset} ${msg}`);
}

// 项目类型配置
const PROJECT_TYPES = {
  // Java 后端
  'spring-boot': {
    name: 'Spring Boot',
    language: 'Java',
    buildTool: 'Maven/Gradle',
    layers: ['Entity', 'DAO', 'Service', 'Controller'],
    layerOrder: ['entity', 'dao', 'service', 'controller'],
    test: 'JUnit 5 + Mockito',
    lint: 'Checkstyle',
    archTest: 'ArchUnit',
    packages: ['src/main/java'],
    testPackages: ['src/test/java'],
    srcDirs: ['src/main/java'],
    packagePatterns: ['**/src/main/java/**/*.java']
  },
  
  // JavaScript/TypeScript 前端
  'react': {
    name: 'React',
    language: 'TypeScript',
    buildTool: 'Vite/Webpack',
    layers: ['Types', 'Components', 'Hooks', 'Pages'],
    layerOrder: ['types', 'components', 'hooks', 'pages'],
    test: 'Jest + React Testing Library',
    lint: 'ESLint',
    archTest: null,
    packages: ['src'],
    testPackages: ['src', '__tests__'],
    srcDirs: ['src'],
    packagePatterns: ['**/src/**/*.{ts,tsx}']
  },
  
  'vue': {
    name: 'Vue',
    language: 'TypeScript',
    buildTool: 'Vite',
    layers: ['Types', 'Components', 'Composables', 'Views'],
    layerOrder: ['types', 'components', 'composables', 'views'],
    test: 'Vitest + Vue Test Utils',
    lint: 'ESLint',
    archTest: null,
    packages: ['src'],
    testPackages: ['src'],
    srcDirs: ['src'],
    packagePatterns: ['**/src/**/*.{ts,vue}']
  },
  
  // Node.js 后端
  'node-express': {
    name: 'Express',
    language: 'TypeScript',
    buildTool: 'npm',
    layers: ['Types', 'DAO', 'Service', 'Controller'],
    layerOrder: ['types', 'dao', 'service', 'controller'],
    test: 'Jest',
    lint: 'ESLint',
    archTest: null,
    packages: ['src'],
    testPackages: ['src', '__tests__'],
    srcDirs: ['src'],
    packagePatterns: ['**/src/**/*.ts']
  },
  
  'nestjs': {
    name: 'NestJS',
    language: 'TypeScript',
    buildTool: 'npm',
    layers: ['Entities', 'Repositories', 'Services', 'Controllers', 'Modules'],
    layerOrder: ['entities', 'repositories', 'services', 'controllers', 'modules'],
    test: 'Jest',
    lint: 'ESLint + Prettier',
    archTest: null,
    packages: ['src'],
    testPackages: ['src'],
    srcDirs: ['src'],
    packagePatterns: ['**/src/**/*.ts']
  },
  
  // Python 后端
  'django': {
    name: 'Django',
    language: 'Python',
    buildTool: 'pip/poetry',
    layers: ['Models', 'Views', 'Serializers', 'Urls'],
    layerOrder: ['models', 'views', 'serializers', 'urls'],
    test: 'pytest',
    lint: 'flake8',
    archTest: null,
    packages: ['app'],
    testPackages: ['tests'],
    srcDirs: ['app'],
    packagePatterns: ['**/app/**/*.py']
  },
  
  'fastapi': {
    name: 'FastAPI',
    language: 'Python',
    buildTool: 'pip/poetry',
    layers: ['Models', 'Schemas', 'Services', 'Routes'],
    layerOrder: ['models', 'schemas', 'services', 'routes'],
    test: 'pytest',
    lint: 'ruff',
    archTest: null,
    packages: ['app'],
    testPackages: ['tests'],
    srcDirs: ['app'],
    packagePatterns: ['**/app/**/*.py']
  },
  
  // Go 后端
  'go-gin': {
    name: 'Gin',
    language: 'Go',
    buildTool: 'Go modules',
    layers: ['Models', 'Repository', 'Service', 'Handler'],
    layerOrder: ['models', 'repository', 'service', 'handler'],
    test: 'testing',
    lint: 'golangci-lint',
    archTest: null,
    packages: ['internal'],
    testPackages: ['internal'],
    srcDirs: ['internal', 'cmd'],
    packagePatterns: ['**/*.go']
  },
  
  // Rust 后端
  'rust-actix': {
    name: 'Actix-web',
    language: 'Rust',
    buildTool: 'Cargo',
    layers: ['Models', 'Repository', 'Service', 'Handlers'],
    layerOrder: ['models', 'repository', 'service', 'handlers'],
    test: 'Rust test',
    lint: 'clippy',
    archTest: null,
    packages: ['src'],
    testPackages: ['tests'],
    srcDirs: ['src'],
    packagePatterns: ['**/*.rs']
  }
};

// 分析项目结构 - 智能检测
function analyzeProject() {
  log('分析项目结构...', 'blue');
  
  const result = {
    name: path.basename(PROJECT_ROOT),
    type: 'unknown',
    config: null,
    framework: 'unknown',
    language: 'unknown',
    buildTool: 'unknown',
    hasTests: false,
    hasDocs: false,
    hasCI: false,
    domains: [],
    fileCount: 0,
    layers: [],
    test: '',
    lint: ''
  };
  
  // 检测项目类型
  const detectedType = detectProjectType(result);
  if (detectedType && PROJECT_TYPES[detectedType]) {
    result.type = detectedType;
    result.config = PROJECT_TYPES[detectedType];
    result.framework = result.config.name;
    result.language = result.config.language;
    result.buildTool = result.config.buildTool;
    result.layers = result.config.layers;
    result.test = result.config.test;
    result.lint = result.config.lint;
  }
  
  // 检测测试
  const testDirs = ['tests', 'test', '__tests__', 'src/test', 'src/tests'];
  result.hasTests = testDirs.some(d => fs.existsSync(path.join(PROJECT_ROOT, d)));
  
  // 检测文档
  result.hasDocs = fs.existsSync(path.join(PROJECT_ROOT, 'docs'));
  
  // 检测 CI
  result.hasCI = fs.existsSync(path.join(PROJECT_ROOT, '.github'));
  
  // 扫描业务域
  result.domains = scanDomains(result);
  
  // 统计文件数
  result.fileCount = countFiles(result);
  
  log(`  项目类型: ${result.type}`, 'blue');
  log(`  框架: ${result.framework}`, 'blue');
  log(`  语言: ${result.language}`, 'blue');
  log(`  构建: ${result.buildTool}`, 'blue');
  log(`  业务域: ${result.domains.join(', ') || '无'}`, 'blue');
  log(`  文件数: ${result.fileCount}`, 'blue');
  
  return result;
}

function detectProjectType(result) {
  // 检查 package.json (Node.js 项目)
  if (fs.existsSync(path.join(PROJECT_ROOT, 'package.json'))) {
    try {
      const pkg = JSON.parse(fs.readFileSync(path.join(PROJECT_ROOT, 'package.json'), 'utf-8'));
      const deps = { ...pkg.dependencies, ...pkg.devDependencies };
      
      if (deps['react'] || deps['react-dom']) return 'react';
      if (deps['vue']) return 'vue';
      if (deps['@nestjs/core']) return 'nestjs';
      if (deps['express']) return 'node-express';
    } catch (e) {}
  }
  
  // 检查 pom.xml (Java Maven)
  if (fs.existsSync(path.join(PROJECT_ROOT, 'pom.xml'))) {
    const pom = fs.readFileSync(path.join(PROJECT_ROOT, 'pom.xml'), 'utf-8');
    if (pom.includes('<groupId>org.springframework.boot</groupId>')) {
      return 'spring-boot';
    }
  }
  
  // 检查 build.gradle (Java Gradle)
  if (fs.existsSync(path.join(PROJECT_ROOT, 'build.gradle'))) {
    const gradle = fs.readFileSync(path.join(PROJECT_ROOT, 'build.gradle'), 'utf-8');
    if (gradle.includes('org.springframework.boot')) {
      return 'spring-boot';
    }
  }
  
  // 检查 go.mod (Go)
  if (fs.existsSync(path.join(PROJECT_ROOT, 'go.mod'))) {
    return 'go-gin';
  }
  
  // 检查 Cargo.toml (Rust)
  if (fs.existsSync(path.join(PROJECT_ROOT, 'Cargo.toml'))) {
    return 'rust-actix';
  }
  
  // 检查 Django
  if (fs.existsSync(path.join(PROJECT_ROOT, 'manage.py'))) {
    return 'django';
  }
  
  // 检查 FastAPI
  if (fs.existsSync(path.join(PROJECT_ROOT, 'main.py')) || 
      fs.existsSync(path.join(PROJECT_ROOT, 'app'))) {
    const files = fs.readdirSync(PROJECT_ROOT);
    if (files.some(f => f.endsWith('.py'))) {
      const pyContent = fs.readFileSync(path.join(PROJECT_ROOT, files.find(f => f.endsWith('.py'))), 'utf-8');
      if (pyContent.includes('fastapi') || pyContent.includes('FastAPI')) {
        return 'fastapi';
      }
    }
  }
  
  return 'unknown';
}

function scanDomains(result) {
  if (!result.config) return [];
  
  const domains = [];
  for (const srcDir of result.config.srcDirs) {
    const fullPath = path.join(PROJECT_ROOT, srcDir);
    if (!fs.existsSync(fullPath)) continue;
    
    try {
      const items = fs.readdirSync(fullPath);
      for (const item of items) {
        const itemPath = path.join(fullPath, item);
        const stat = fs.statSync(itemPath);
        
        // 跳过常见非业务目录
        if (['node_modules', 'dist', 'build', 'target', '.git', 'utils', 'common', 'shared'].includes(item)) {
          continue;
        }
        
        if (stat.isDirectory()) {
          domains.push(item);
        }
      }
    } catch (e) {}
  }
  
  return [...new Set(domains)];
}

function countFiles(result) {
  if (!result.config) return 0;
  
  try {
    const patterns = result.config.packagePatterns;
    let total = 0;
    
    for (const pattern of patterns) {
      const output = execSync(`find . -name "${pattern.split('*')[1]}" -type f 2>/dev/null | wc -l`, {
        cwd: PROJECT_ROOT,
        encoding: 'utf-8',
        timeout: 5000
      });
      total += parseInt(output.trim()) || 0;
    }
    
    return total;
  } catch (e) {
    return 0;
  }
}

// 创建目录结构
function createDirs() {
  const dirs = [
    'docs/architecture/domains',
    'docs/design/adr',
    'docs/plans/active',
    'docs/plans/completed',
    'docs/plans/debt',
    'docs/quality',
    'scripts',
    '.github/workflows'
  ];
  
  for (const dir of dirs) {
    const fullPath = path.join(PROJECT_ROOT, dir);
    if (!fs.existsSync(fullPath)) {
      fs.mkdirSync(fullPath, { recursive: true });
      log(`创建目录: ${dir}`);
    }
  }
}

// 创建 AGENTS.md
function createAgentsMd(project) {
  const layers = project.layers.length > 0 
    ? project.layers.join(' → ') 
    : 'Types → Config → Repo → Service → Runtime → UI';
  
  const domainsList = project.domains.length > 0 
    ? project.domains.map(d => `- [${capitalize(d)}](docs/architecture/domains/${d}.md)`).join('\n')
    : '- (扫描到后自动添加)';
  
  const content = `# AGENTS.md

> 本项目采用 Harness Engineering 模式开发 (${project.framework})

## 快速入口

| 资源 | 位置 | 用途 |
|------|------|------|
| 架构图 | [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md) | 系统结构 |
| 质量状态 | [docs/quality/grades.md](docs/quality/grades.md) | 各域健康度 |
| 活跃计划 | [docs/plans/active/](docs/plans/active/) | 当前工作 |
| 技术债务 | [docs/plans/debt/](docs/plans/debt/) | 待清理 |

## 核心原则

1. **人类指挥，Agent 执行** - 人描述任务，Agent 完成代码
2. **零手写代码** - 所有代码由 Agent 生成
3. **知识在 repo 内** - 决策记录在 docs/design/adr/
4. **约束即法律** - 架构规则不可违反
5. **持续清理** - 技术债务定期偿还

## 架构约束 (${project.framework})

### 严格分层

\`\`\`
${layers}
\`\`\`

**规则：**
- 同层可相互依赖
- 只能向前依赖
- 跨域通过 Application Service 编排
- 违反则 CI 失败

### 业务域

${domainsList}

## 技术栈

| 类别 | 技术 |
|------|------|
| 语言 | ${project.language} |
| 框架 | ${project.framework} |
| 构建 | ${project.buildTool} |
| 测试 | ${project.test} |
| Lint | ${project.lint} |

## 工作流

\`\`\`
1. 人类描述任务
2. Agent 写计划 (docs/plans/active/plan-xxx.md)
3. Agent 执行代码
4. Agent 自审 (lint + test)
5. Agent 请求其他 Agent 审查
6. Agent 响应反馈 (循环直到通过)
7. Agent 合并 PR
\`\`\`

## 禁止事项

- ❌ 直接手写代码提交
- ❌ 在 repo 外讨论决策
- ❌ 忽略 CI 失败
- ❌ 跳过测试
- ❌ 单一文件 > 500 行

## 质量标准

| 指标 | 目标 |
|------|------|
| 测试覆盖率 | >70% |
| Lint | 0 警告 |
| 文档 freshness | <30天 |
| 架构层级合规 | 100% |

---

*本项目采用 OpenAI Harness Engineering 模式*
`;
  
  const filePath = path.join(PROJECT_ROOT, 'AGENTS.md');
  fs.writeFileSync(filePath, content);
  success(`创建 AGENTS.md`);
}

// 创建架构文档
function createArchitectureMd(project) {
  const layers = project.layers;
  
  const domainsTable = project.domains.length > 0
    ? project.domains.map(d => {
        const layerRows = layers.map(layer => {
          const fileName = getFileName(d, layer, project);
          return `| ${layer} | \`${fileName}\` | ✅ A |`;
        }).join('\n');
        return `### ${capitalize(d)}\n\n| 层级 | 文件 | 状态 |\n|------|------|------|\n${layerRows}`;
      }).join('\n\n')
    : '*扫描项目后自动生成*';
  
  const content = `# 架构总览

## 项目信息

| 属性 | 值 |
|------|-----|
| 项目名称 | ${project.name} |
| 类型 | ${project.type} |
| 语言 | ${project.language} |
| 框架 | ${project.framework} |
| 构建工具 | ${project.buildTool} |
| 代码文件数 | ${project.fileCount} |

## 系统拓扑

${getTopology(project)}

## 业务域

${domainsTable}

## 分层结构

\`\`\`
${layers.join(' → ')}
\`\`\`

跨域依赖: 通过 Application Service 编排

## 技术栈

- **语言**: ${project.language}
- **框架**: ${project.framework}
- **构建**: ${project.buildTool}
- **测试**: ${project.test}
- **Linting**: ${project.lint}

## CI 命令

\`\`\`bash
${getCICommands(project)}
\`\`\`

## 最后更新

${new Date().toISOString().split('T')[0]}
`;
  
  const filePath = path.join(PROJECT_ROOT, 'docs/architecture/ARCHITECTURE.md');
  fs.writeFileSync(filePath, content);
  success(`创建 docs/architecture/ARCHITECTURE.md`);
  
  // 为每个业务域创建文档
  for (const domain of project.domains) {
    const domainContent = generateDomainDoc(domain, project);
    const domainPath = path.join(PROJECT_ROOT, `docs/architecture/domains/${domain}.md`);
    fs.writeFileSync(domainPath, domainContent);
    success(`创建 docs/architecture/domains/${domain}.md`);
  }
}

function getFileName(domain, layer, project) {
  const name = capitalize(domain);
  switch (project.type) {
    case 'spring-boot':
      if (layer === 'Entity') return `${name}.java`;
      if (layer === 'DAO') return `${name}Dao.java`;
      if (layer === 'Service') return `${name}Service.java`;
      if (layer === 'Controller') return `${name}Controller.java`;
      return `${name}${layer}.java`;
    case 'react':
    case 'vue':
      if (layer === 'Components') return `${name}/*.tsx`;
      if (layer === 'Pages') return `${name}/*.tsx`;
      if (layer === 'Hooks') return `use${name}.ts`;
      return `${layer.toLowerCase()}/${name}.ts`;
    case 'nestjs':
      return `${name}${layer}.ts`;
    case 'django':
      if (layer === 'Models') return `models.py`;
      if (layer === 'Views') return `views.py`;
      if (layer === 'Serializers') return `serializers.py`;
      return `${layer.toLowerCase()}.py`;
    case 'fastapi':
      if (layer === 'Models') return `models.py`;
      if (layer === 'Schemas') return `schemas.py`;
      if (layer === 'Services') return `services.py`;
      if (layer === 'Routes') return `routes.py`;
      return `${layer.toLowerCase()}.py`;
    case 'go-gin':
      return `${layer.toLowerCase()}/${domain}.go`;
    default:
      return `${name}${layer}.*`;
  }
}

function getTopology(project) {
  switch (project.type) {
    case 'react':
    case 'vue':
      return `\`\`\`
        ┌──────────────┐
        │   Browser   │
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │   Pages      │  ← 路由页面
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │ Components   │  ← 可复用组件
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │    Hooks     │  ← 状态/逻辑
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │    Types     │  ← 类型定义
        └──────────────┘
\`\`\``;
    case 'spring-boot':
      return `\`\`\`
        ┌──────────────┐
        │   Clients   │
        │(Web/Mobile) │
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │ Controller   │  ← REST API
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │  Service    │  ← 业务逻辑
        └──────┬───────┘
               │
  ┌────────┐  ┌──────▼───────┐         ┌────────┐
  │  S3    │◄─│     DAO      │────────►│  DB    │
  └────────┘  └───────────────┘         └────────┘
\`\`\``;
    default:
      return `\`\`\`
        ┌──────────────┐
        │   Clients   │
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │   Handler    │
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │   Service    │
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │  Repository  │
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │    Model     │
        └──────────────┘
\`\`\``;
  }
}

function getCICommands(project) {
  switch (project.type) {
    case 'spring-boot':
      return `./mvnw clean compile\n./mvnw checkstyle:check\n./mvnw test`;
    case 'react':
    case 'vue':
    case 'nestjs':
    case 'node-express':
      return `npm run lint\nnpm test\nnpm run build`;
    case 'django':
      return `python -m flake8\npytest`;
    case 'fastapi':
      return `ruff check .\npytest`;
    case 'go-gin':
      return `go build ./...\ngolangci-lint run\ngo test ./...`;
    default:
      return `# 根据项目配置\nnpm run lint && npm test`;
  }
}

function generateDomainDoc(domain, project) {
  const layers = project.layers;
  const layerRows = layers.map(layer => {
    const fileName = getFileName(domain, layer, project);
    return `| ${layer} | \`${fileName}\` | ✅ |`;
  }).join('\n');
  
  return `# ${capitalize(domain)} 域

## 概述

业务域: ${domain}

## 分层详情

| 层级 | 文件 | 状态 |
|------|------|------|
${layerRows}

## 依赖

- 同域: ${layers.slice().reverse().join(' → ')}
- 跨域: 通过 Application Service

## 技术债务

暂无记录

## 相关计划

- [活跃计划](../plans/active/)
- [已完成](../plans/completed/)
`;
}

// 创建质量评级
function createQualityGrades(project) {
  const layers = project.layers;
  
  const domainsTable = project.domains.length > 0
    ? project.domains.map(d => {
        const layerRows = layers.map(layer => {
          return `| ${layer} | A | ${today()} | - |`;
        }).join('\n');
        return `### ${capitalize(d)}\n\n| 层级 | 评分 | 最后评审 | 债务 |\n|------|------|----------|------|\n${layerRows}`;
      }).join('\n\n')
    : '*暂无业务域*';
  
  const content = `# 质量评级

## 评分标准

| 等级 | 含义 | 要求 |
|------|------|------|
| A | 生产就绪 | 测试>80%, 文档完整, 无已知债务 |
| B | 功能完整 | 测试>60%, 少量债务需处理 |
| C | 可用但需改进 | 测试>40%, 有明显技术债务 |
| D | 需重构 | 测试不足, 架构有问题 |

## 当前评级

${domainsTable}

## 质量趋势

*追踪最近30天的变化*

| 域/层 | 趋势 |
|-------|------|
| (新建) | - |

## 清理清单

- [ ] 本周: 审查所有 C 级组件
- [ ] 本月: 技术债务审查
- [ ] 本季度: 架构一致性审计

## 更新频率

每周一更新质量评级
`;
  
  const filePath = path.join(PROJECT_ROOT, 'docs/quality/grades.md');
  fs.writeFileSync(filePath, content);
  success(`创建 docs/quality/grades.md`);
}

// 创建 CI 配置
function createCIConfig(project) {
  const content = generateCIConfig(project);
  
  const filePath = path.join(PROJECT_ROOT, '.github/workflows/harness-ci.yml');
  fs.writeFileSync(filePath, content);
  success(`创建 .github/workflows/harness-ci.yml`);
}

function generateCIConfig(project) {
  switch (project.type) {
    case 'spring-boot':
      return `name: CI (Spring Boot)

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up JDK
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
          
      - name: Build
        run: ./mvnw clean compile -q
        
      - name: Checkstyle
        run: ./mvnw checkstyle:check -q
        
      - name: Test
        run: ./mvnw test -q`;

    case 'react':
    case 'vue':
    case 'nestjs':
    case 'node-express':
      return `name: CI (${project.framework})

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          
      - name: Install
        run: npm ci
        
      - name: Lint
        run: npm run lint
        
      - name: Test
        run: npm test -- --coverage
        
      - name: Build
        run: npm run build`;

    case 'django':
    case 'fastapi':
      return `name: CI (${project.framework})

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
        
      - name: Lint
        run: flake8 . || ruff check .
        
      - name: Test
        run: pytest`;

    case 'go-gin':
      return `name: CI (Go)

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.21'
          
      - name: Build
        run: go build ./...
        
      - name: Lint
        run: golangci-lint run
        
      - name: Test
        run: go test ./...`;

    default:
      return `name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and Test
        run: |
          echo "Configure CI for your project type: ${project.type}"
`;
  }
}

// 创建架构测试 (如果适用)
function createArchTest(project) {
  if (project.type === 'spring-boot') {
    const content = `package com.example.arch;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.lang.ArchRule;
import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.*;

import org.junit.jupiter.api.Test;

class ArchitectureTest {

    private final JavaClasses classes = new ClassFileImporter()
        .importPackages("com.example..");

    @Test
    void controllers_should_only_depend_on_services() {
        ArchRule rule = classes()
            .that().resideInPackage("..controller..")
            .should().onlyDependOnClassesThat()
            .resideInAnyPackage("..service..", "..entity..", "..dto..");
        
        rule.check(classes);
    }

    @Test
    void services_should_only_depend_on_dao_and_entity() {
        ArchRule rule = classes()
            .that().resideInPackage("..service..")
            .should().onlyDependOnClassesThat()
            .resideInAnyPackage("..dao..", "..entity..", "..dto..");
        
        rule.check(classes);
    }
}
`;
    
    const testDir = path.join(PROJECT_ROOT, 'src/test/java/com/example/arch');
    if (!fs.existsSync(testDir)) {
      fs.mkdirSync(testDir, { recursive: true });
    }
    
    fs.writeFileSync(path.join(testDir, 'ArchitectureTest.java'), content);
    success(`创建 src/test/java/com/example/arch/ArchitectureTest.java`);
    
    console.log(`\n注意: 添加 ArchUnit 依赖到 pom.xml:
<dependency>
    <groupId>com.tngtech.archunit</groupId>
    <artifactId>archunit-junit5</artifactId>
    <version>1.2.1</version>
    <scope>test</scope>
</dependency>`);
  }
}

// 验证现有文档
function validateDocs() {
  log('验证文档规范...', 'blue');
  
  const checks = [
    { name: 'AGENTS.md', path: 'AGENTS.md', maxLines: 150 },
    { name: '架构文档', path: 'docs/architecture/ARCHITECTURE.md' },
    { name: '质量评级', path: 'docs/quality/grades.md' },
    { name: 'CI 配置', path: '.github/workflows/harness-ci.yml' }
  ];
  
  let allPassed = true;
  
  for (const check of checks) {
    const fullPath = path.join(PROJECT_ROOT, check.path);
    
    if (!fs.existsSync(fullPath)) {
      error(`缺少: ${check.path}`);
      allPassed = false;
      continue;
    }
    
    if (check.maxLines) {
      const content = fs.readFileSync(fullPath, 'utf-8');
      const lines = content.split('\n').length;
      if (lines > check.maxLines) {
        error(`${check.name} 超过 ${check.maxLines} 行 (当前: ${lines})`);
        allPassed = false;
      } else {
        success(`${check.name} ✓`);
      }
    } else {
      success(`${check.name} ✓`);
    }
  }
  
  return allPassed;
}

// 工具函数
function capitalize(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}

function today() {
  return new Date().toISOString().split('T')[0];
}

// Main
function main() {
  const args = process.argv.slice(2);
  const command = args[0] || '--init';
  
  console.log('\n🚀 Harness Engineering 文档生成器 (智能版)\n');
  
  switch (command) {
    case '--init':
      const project = analyzeProject();
      createDirs();
      createAgentsMd(project);
      createArchitectureMd(project);
      createQualityGrades(project);
      createCIConfig(project);
      createArchTest(project);
      console.log(`\n✅ 所有文档创建完成！ (项目类型: ${project.type || 'unknown'})\n`);
      break;
      
    case '--agents':
      const p1 = analyzeProject();
      createDirs();
      createAgentsMd(p1);
      break;
      
    case '--architecture':
      const p2 = analyzeProject();
      createDirs();
      createArchitectureMd(p2);
      break;
      
    case '--quality':
      const p3 = analyzeProject();
      createDirs();
      createQualityGrades(p3);
      break;
      
    case '--validate':
      validateDocs();
      break;
      
    default:
      console.log('使用方法:');
      console.log('  node create-harness-docs.js --init          # 创建所有文档');
      console.log('  node create-harness-docs.js --agents         # 仅创建 AGENTS.md');
      console.log('  node create-harness-docs.js --architecture  # 仅创建架构文档');
      console.log('  node create-harness-docs.js --quality       # 仅创建质量评级');
      console.log('  node create-harness-docs.js --validate      # 验证现有文档');
  }
}

main();
