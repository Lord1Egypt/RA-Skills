# 开发指南

本文档提供 OpenClaw File Transfer Skill 的开发指南。

## 环境要求

- **Node.js**: >= 18.0.0
- **npm**: >= 9.0.0
- **Git**: 版本控制

## 快速开始

```bash
git clone https://github.com/Ghostwritten/openclaw-file-transfer-skill.git
cd openclaw-file-transfer-skill
npm install
```

### 开发模式

```bash
# 热重载
npm run dev

# 运行测试
npm test

# 运行特定测试
npm test -- context-engine.test.js
```

## 项目结构

```
openclaw-file-transfer-skill/
├── src/
│   ├── index.js                   # 主入口 - FileTransferSkill 类
│   ├── core/
│   │   ├── context-engine.js      # 智能上下文分析引擎
│   │   └── file-manager.js        # 文件验证和管理
│   ├── adapters/
│   │   └── telegram-adapter.js    # Telegram 平台适配器
│   └── utils/
│       └── format.js              # 共享工具函数
├── tests/
│   ├── unit/                      # 单元测试
│   │   ├── context-engine.test.js
│   │   └── file-manager.test.js
│   ├── integration/               # 集成测试
│   │   └── telegram-adapter.test.js
│   └── setup.js                   # Jest 全局配置
├── docs/                          # 文档
├── examples/                      # 使用示例
├── jest.config.js                 # Jest 配置
└── package.json
```

## 开发工作流

### 1. 创建功能分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/issue-123
```

### 2. 编写代码

- 使用 **ES6+ Modules** (`import/export`)
- 每个文件一个类或主要功能模块
- 使用 **JSDoc** 注释
- 遵循 **Airbnb JavaScript Style Guide**

### 3. 运行测试

```bash
npm test                    # 运行所有测试
npm run test:unit           # 单元测试
npm run test:integration    # 集成测试
npm run test:coverage       # 覆盖率报告
```

> 注意：项目使用 ES Modules，Jest 通过 `NODE_OPTIONS='--experimental-vm-modules'` 运行。

### 4. 代码检查

```bash
npm run lint                # 检查代码规范
npm run lint:fix            # 自动修复
npm run format              # 代码格式化
```

### 5. 提交代码

使用约定式提交信息：
- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具

## 测试策略

### 单元测试 (`tests/unit/`)
- 覆盖独立模块：ContextEngine、FileManager
- 目标覆盖率：80%+
- 使用 Jest

### 集成测试 (`tests/integration/`)
- 覆盖模块间交互：TelegramAdapter（含 ContextEngine + FileManager）
- 使用真实文件系统

### 测试模式

```javascript
describe('ClassName', () => {
  let instance;

  beforeEach(() => {
    instance = new ClassName(config);
  });

  describe('methodName', () => {
    test('应该完成正常操作', async () => {
      const result = await instance.method(input);
      expect(result).toBeDefined();
    });

    test('应该处理错误情况', async () => {
      await expect(instance.method(badInput)).rejects.toThrow();
    });
  });
});
```

## 添加新适配器

1. 在 `src/adapters/` 创建新文件（如 `whatsapp-adapter.js`）
2. 实现 `sendFile(params)`、`getTransferStatus(id)`、`getActiveTransfers()` 方法
3. 在 `src/index.js` 的 `initializeChannels()` 中注册
4. 添加集成测试到 `tests/integration/`
5. 更新文档

```javascript
export class WhatsAppAdapter {
  constructor(config = {}) { ... }
  async sendFile(params) { ... }
  getTransferStatus(transferId) { ... }
  getActiveTransfers() { ... }
  getInfo() { ... }
}
```

## 依赖说明

### 生产依赖
| 依赖 | 用途 |
|------|------|
| `mime-types` | MIME 类型检测 |

### 开发依赖
| 依赖 | 用途 |
|------|------|
| `jest` | 测试框架 |
| `eslint` + `airbnb-base` | 代码规范 |
| `prettier` | 代码格式化 |
| `husky` + `lint-staged` | Git hooks |
| `nodemon` | 开发热重载 |
| `standard-version` | 版本管理 |

## 发布流程

```bash
# 准备发布
npm run release

# 预发布版本
npm run release -- --prerelease beta

# 发布到 npm
npm publish
```
