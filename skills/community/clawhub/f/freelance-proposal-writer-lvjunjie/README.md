# Freelance-Proposal-Writer-Pro 🚀

**AI 驱动的 Freelancer/Upwork 投标提案生成器（专业版）**

[![Version](https://img.shields.io/npm/v/freelance-proposal-writer.svg)](https://www.npmjs.com/package/freelance-proposal-writer)
[![License](https://img.shields.io/npm/l/freelance-proposal-writer.svg)](https://opensource.org/licenses/MIT)
[![Node](https://img.shields.io/node/v/freelance-proposal-writer.svg)](https://nodejs.org)

---

## 📖 简介

Freelance-Proposal-Writer 是一款专为自由职业者设计的 AI 提案生成工具，帮助你在 Upwork、Freelancer 等平台上创建高转化率的投标提案。

**核心功能：**
- ✨ AI 生成个性化投标提案
- 📊 客户分析与匹配度评分
- 💡 成功率优化建议
- 📋 内置 5 种专业提案模板
- 🎯 关键词优化与痛点匹配

---

## 🚀 快速开始

### 安装

```bash
npm install -g freelance-proposal-writer
```

### 基础使用

```bash
# 生成提案
freelance-proposal write --job "Need a React developer for e-commerce site" --skills "React, Node.js, MongoDB"

# 分析客户
freelance-proposal analyze --client "Looking for experienced developer, budget $5000" --budget 5000

# 优化现有提案
freelance-proposal optimize "Hi, I am interested in your project..."

# 查看模板
freelance-proposal templates

# 获取优化技巧
freelance-proposal tips
```

---

## 📋 命令详解

### `write` - 生成提案

```bash
freelance-proposal write [选项]

选项:
  -j, --job <description>    职位描述（必填）
  -s, --skills <skills>      你的核心技能
  -t, --template <type>      模板类型：standard|premium|quick|followup|referral
  -n, --name <name>          客户姓名
  --save                     保存到文件
```

**示例：**
```bash
freelance-proposal write \
  --job "Need WordPress developer for custom theme" \
  --skills "WordPress, PHP, CSS, JavaScript" \
  --template premium \
  --save
```

### `analyze` - 客户分析

```bash
freelance-proposal analyze [选项]

选项:
  -c, --client <data>        客户信息/职位描述
  -b, --budget <amount>      项目预算
```

**输出包含：**
- 匹配度评分（0-100%）
- 客户痛点分析
- 投标建议
- 风险警示

### `optimize` - 提案优化

```bash
freelance-proposal optimize "<你的提案内容>"
```

**分析维度：**
- 字数检查（理想 150-300 字）
- 结构完整性
- 个性化程度
- 行动呼吁
- 关键词匹配

### `templates` - 模板库

列出所有可用模板：
- **standard** - 标准投标提案
- **premium** - 高端定制提案
- **quick** - 快速响应提案
- **followup** - 跟进提案
- **referral** - 推荐提案

### `tips` - 优化技巧

显示成功率优化技巧，包括：
- 开场白技巧
- 正文结构
- 结尾策略
- 长度控制
- 关键词优化

---

## 🎯 提案模板

### Standard（标准版）
适用于大多数项目，平衡专业性与简洁性。

### Premium（高端版）
针对高预算项目（>$3000），包含详细方案和 ROI 分析。

### Quick（快速版）
简洁直接，适合紧急项目或小额预算。

### Followup（跟进版）
用于跟进未回复的投标，友好提醒。

### Referral（推荐版）
通过推荐渠道联系，建立初始信任。

---

## 💡 成功率优化建议

根据平台数据分析，高转化率提案的共同特点：

### ✅ 必做项
- [ ] 使用客户姓名
- [ ] 提及具体项目细节
- [ ] 展示相关案例（1-2 个）
- [ ] 明确交付时间
- [ ] 提出 1-2 个专业问题
- [ ] 明确的行动呼吁

### ❌ 避免项
- [ ] 通用开场白（"I am interested"）
- [ ] 过长篇幅（>400 字）
- [ ] 过度自我吹嘘
- [ ] 模糊的时间承诺
- [ ] 拼写/语法错误

### 📊 数据洞察
- 前 3 句决定 80% 的继续阅读率
- 包含具体数字的提案转化率高 47%
- 提出问题增加 35% 的回复率
- 24 小时内投标成功率高 3 倍

---

## 🔧 配置

创建 `~/.freelance-proposal/config.json`：

```json
{
  "apiKey": "your-api-key",
  "defaultTone": "professional",
  "templatesPath": "./templates",
  "outputFormat": "markdown",
  "autoSave": true,
  "statsTracking": true
}
```

---

## 📈 订阅计划

### Pro 订阅 - $79/月

**包含：**
- ✅ 无限提案生成
- ✅ 完整模板库访问
- ✅ AI 优化建议
- ✅ 客户分析工具
- ✅ 提案统计追踪
- ✅ 优先支持

**免费试用：** 7 天

---

## 🤝 API 集成

Freelance-Proposal-Writer 可作为 OpenClaw Skill 集成：

```javascript
const { generateProposal } = require('freelance-proposal-writer');

const proposal = await generateProposal({
  jobDescription: '...',
  skills: ['React', 'Node.js'],
  template: 'premium'
});
```

---

## 📝 示例工作流

### 1. 发现合适项目
```bash
# 浏览 Upwork/Freelancer 找到匹配项目
```

### 2. 分析客户
```bash
freelance-proposal analyze \
  --client "Looking for React expert, 5+ years experience required" \
  --budget 5000
```

### 3. 生成提案
```bash
freelance-proposal write \
  --job "React developer needed for dashboard project" \
  --skills "React, TypeScript, D3.js" \
  --template premium \
  --name "John" \
  --save
```

### 4. 优化提案
```bash
freelance-proposal optimize "$(cat proposal-xxx.md)"
```

### 5. 提交并追踪
```bash
# 提交到平台，记录到追踪系统
```

---

## 🛠 开发

```bash
# 克隆仓库
git clone https://github.com/openclaw/freelance-proposal-writer.git

# 安装依赖
npm install

# 本地测试
npm start -- write --job "test" --skills "test"

# 运行测试
npm test
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 👥 作者

**OpenClaw Skills Team**

- GitHub: [@openclaw](https://github.com/openclaw)
- ClawHub: [openclaw/freelance-proposal-writer](https://clawhub.ai/openclaw/freelance-proposal-writer)

---

## 🙏 致谢

感谢所有贡献者和早期使用者！

---

## 📞 支持

遇到问题？
- 查看 [Issues](https://github.com/openclaw/freelance-proposal-writer/issues)
- 发送邮件至 support@openclaw.ai
- 加入 Discord 社区

---

**让每一次投标都更有说服力！** 🎯
