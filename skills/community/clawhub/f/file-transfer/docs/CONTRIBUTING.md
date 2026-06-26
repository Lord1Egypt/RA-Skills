# 贡献指南

感谢你对 OpenClaw File Transfer Skill 项目的兴趣！我们欢迎各种形式的贡献，包括bug报告、功能建议、文档改进和代码提交。

## 🎯 如何贡献

### 1. 报告问题

如果你发现bug或有功能建议，请先检查是否已有相关issue：

1. 访问 [GitHub Issues](https://github.com/Ghostwritten/openclaw-file-transfer-skill/issues)
2. 搜索相关问题
3. 如果没有找到，创建新issue

**创建issue时请提供**：
- 清晰的问题描述
- 复现步骤
- 期望行为 vs 实际行为
- 环境信息（Node版本、操作系统等）
- 相关日志或截图

### 2. 提交代码

#### 第一步：Fork仓库

1. 访问 https://github.com/Ghostwritten/openclaw-file-transfer-skill
2. 点击右上角的 "Fork" 按钮
3. 克隆你的fork到本地：
   ```bash
   git clone https://github.com/你的用户名/openclaw-file-transfer-skill.git
   cd openclaw-file-transfer-skill
   ```

#### 第二步：设置上游仓库

```bash
git remote add upstream https://github.com/Ghostwritten/openclaw-file-transfer-skill.git
git fetch upstream
```

#### 第三步：创建功能分支

```bash
# 从main分支创建新分支
git checkout -b feature/your-feature-name

# 或修复bug
git checkout -b fix/issue-123
```

**分支命名规范**：
- `feature/` - 新功能
- `fix/` - bug修复
- `docs/` - 文档更新
- `refactor/` - 代码重构
- `test/` - 测试相关
- `chore/` - 构建或工具更新

#### 第四步：开发代码

1. 编写代码，遵循[代码规范](#代码规范)
2. 添加或更新测试
3. 更新相关文档
4. 运行测试确保通过

```bash
# 运行测试
npm test

# 代码检查
npm run lint

# 代码格式化
npm run format
```

#### 第五步：提交更改

```bash
# 添加更改
git add .

# 提交（遵循约定式提交）
git commit -m "feat: add context analysis for image files"

# 或使用交互式提交
npm run commit
```

**提交信息格式**：
```
类型(范围): 描述

正文（可选）

脚注（可选）
```

**类型**：
- `feat`: 新功能
- `fix`: bug修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具
- `perf`: 性能优化
- `ci`: CI配置

**示例**：
```
feat(core): add image file type detection

- Add support for JPEG, PNG, GIF formats
- Update file validation logic
- Add unit tests for new functionality

Closes #123
```

#### 第六步：同步上游更改

```bash
# 获取上游最新更改
git fetch upstream

# 合并到当前分支
git merge upstream/main

# 或使用rebase（保持历史整洁）
git rebase upstream/main
```

#### 第七步：推送分支

```bash
git push origin feature/your-feature-name
```

#### 第八步：创建Pull Request

1. 访问你的GitHub fork
2. 点击 "New Pull Request"
3. 选择你的分支
4. 填写PR模板
5. 等待代码审查

## 📋 Pull Request 模板

创建PR时，请使用以下模板：

```markdown
## 描述
<!-- 简要描述这个PR做了什么 -->

## 相关Issue
<!-- 关联的issue，例如：Closes #123 -->

## 类型
<!-- 选择一项 -->
- [ ] Bug修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 代码重构
- [ ] 测试相关
- [ ] 其他

## 测试
<!-- 描述你如何测试这些更改 -->

- [ ] 单元测试已添加/更新
- [ ] 集成测试已添加/更新
- [ ] 所有测试通过

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 已添加/更新相关文档
- [ ] 已添加/更新测试
- [ ] 提交信息遵循约定式提交
- [ ] 没有引入新的警告或错误
```

## 🧪 代码规范

### 通用规范

1. **使用ES6+语法**
2. **每个文件一个主要导出**
3. **使用JSDoc注释**
4. **遵循Airbnb JavaScript Style Guide**

### 文件结构

```javascript
// 1. 导入
import { something } from 'module';

// 2. 常量
const CONSTANT = 'value';

// 3. 类定义
export class MyClass {
  constructor(config) {
    this.config = config;
  }

  // 公共方法
  publicMethod() {
    // 实现
  }

  // 私有方法
  _privateMethod() {
    // 实现
  }
}

// 4. 辅助函数
function helper() {
  // 实现
}

// 5. 默认导出
export default MyClass;
```

### 测试规范

1. **每个测试文件对应一个源文件**
2. **使用描述性测试名称**
3. **遵循AAA模式** (Arrange, Act, Assert)
4. **覆盖率目标80%+**

```javascript
describe('ClassName', () => {
  let instance;

  beforeEach(() => {
    instance = new ClassName();
  });

  describe('methodName', () => {
    test('should do something', () => {
      // Arrange
      const input = 'test';
      
      // Act
      const result = instance.methodName(input);
      
      // Assert
      expect(result).toBe('expected');
    });
  });
});
```

## 📚 文档规范

### 代码注释

```javascript
/**
 * 函数描述
 * 
 * @param {string} param1 - 参数1描述
 * @param {number} param2 - 参数2描述
 * @returns {Object} 返回值描述
 * @throws {Error} 可能抛出的错误
 * @example
 * // 使用示例
 * const result = functionName('test', 123);
 */
function functionName(param1, param2) {
  // 实现
}
```

### README 更新

如果添加新功能或更改API，请更新：
- `README.md`
- `docs/API.md`
- 相关示例代码

## 🔧 开发环境

### 设置开发环境

```bash
# 1. 克隆仓库
git clone https://github.com/Ghostwritten/openclaw-file-transfer-skill.git
cd openclaw-file-transfer-skill

# 2. 安装依赖
npm install

# 3. 设置Git钩子
npm run prepare

# 4. 运行测试
npm test
```

### 常用命令

```bash
# 开发
npm run dev          # 开发模式（热重载）
npm start           # 生产模式

# 测试
npm test            # 运行所有测试
npm run test:watch  # 监视模式
npm run test:coverage # 覆盖率报告

# 代码质量
npm run lint        # 代码检查
npm run lint:fix    # 自动修复
npm run format      # 代码格式化

# 构建
npm run build       # 构建检查
npm run clean       # 清理构建产物
```

## 🐛 调试

### 测试调试

```bash
# 运行特定测试并调试
npm test -- --testNamePattern="test name" --verbose

# 使用Node调试
node --inspect node_modules/.bin/jest --runInBand
```

### 代码调试

```bash
# 使用nodemon开发调试
npm run dev

# 直接运行
node --inspect src/index.js
```

## 🤝 行为准则

### 我们的承诺

我们致力于为所有贡献者创造一个友好、尊重的环境，无论其经验水平、性别、性别认同和表达、性取向、残疾、个人外貌、体型、种族、民族、年龄、宗教或国籍如何。

### 我们的标准

积极行为示例：
- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

不可接受的行为：
- 使用性暗示语言或图像
- 挑衅、侮辱/贬损评论和个人或政治攻击
- 公开或私下骚扰
- 未经明确许可发布他人的私人信息
- 其他在专业环境中不适当的行为

### 执行责任

项目维护者有责任澄清可接受行为的标准，并对任何不可接受的行为采取适当和公平的纠正措施。

### 适用范围

本行为准则适用于所有项目空间，也适用于个人在公共空间代表项目或其社区时的行为。

### 报告问题

如果你遇到或目睹不可接受的行为，请通过以下方式报告：
- 发送邮件至：ghostwritten01@gmail.com
- 在GitHub issue中私下联系维护者

所有投诉都将被认真审查和调查，并做出必要和适当的回应。

## 📞 获取帮助

- **GitHub Discussions**: 讨论想法和问题
- **GitHub Issues**: 报告bug和请求功能
- **Discord社区**: 实时聊天和帮助

## 🙏 致谢

感谢所有为这个项目做出贡献的人！你的每一份贡献都让这个项目变得更好。

---

**让我们一起构建更好的 OpenClaw 生态系统！** 🚀