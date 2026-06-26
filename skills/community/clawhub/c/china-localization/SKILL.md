# China Localization Pack v2 - 中国本地化包（安全优化版）

**全中文界面 + 本地服务集成 + 百度搜索支持**

> 🛡️ **安全认证**: 符合 ClawHub 安全规范，无硬编码敏感信息

## 🌟 功能特性

- 🀄 **中文语言包** - 全中文界面和提示
- 🔍 **百度搜索集成** - 专为中国用户优化的中文搜索
- 📅 **飞书集成** - 日历/任务/文档/会议
- 🌤️ **本地天气** - 中文天气查询
- 💬 **微信/钉钉集成** - 消息推送（可选）
- 🗺️ **高德地图** - 地理服务（可选）
- 💳 **支付宝集成** - 支付服务（可选）

## 🔒 安全特性

- ✅ **无硬编码 API keys** - 所有敏感信息通过环境变量配置
- ✅ **符合 ClawHub 安全规范** - 已通过安全扫描
- ✅ **明确的凭证声明** - `_meta.json` 中声明所有必需和可选凭证
- ✅ **环境变量驱动** - 安全的配置管理方式

## 📥 安装

```bash
# 克隆到 dev-skills 目录（开发中版本）
git clone https://github.com/vincentlau2046-sudo/china-localization.git /home/Vincent/.openclaw/workspace/dev-skills/china-localization-v2

# 安装依赖
cd /home/Vincent/.openclaw/workspace/dev-skills/china-localization-v2
npm install
```

## ⚙️ 配置

### 环境变量配置

创建 `.env` 文件或设置环境变量：

```bash
# 必需的凭证
TAVILY_API_KEY=tvly-your-api-key

# 可选的本地服务集成
FEISHU_ENABLED=true
FEISHU_APP_ID=cli_xxxxx
FEISHU_APP_SECRET=xxxxx

WECHAT_ENABLED=true
WECHAT_APP_ID=wx_xxxxx
WECHAT_APP_SECRET=xxxxx

DINGTALK_ENABLED=true
DINGTALK_WEBHOOK=https://oapi.dingtalk.com/robot/send?access_token=xxxxx

AMAP_ENABLED=true
AMAP_API_KEY=xxxxx

ALIPAY_ENABLED=true
ALIPAY_APP_ID=xxxxx
ALIPAY_PRIVATE_KEY=xxxxx
ALIPAY_PUBLIC_KEY=xxxxx
ALIPAY_SANDBOX=true
```

### 在 OpenClaw 中使用

将环境变量添加到 OpenClaw 配置中：

```bash
# 编辑 ~/.openclaw/.env 文件
echo "TAVILY_API_KEY=tvly-your-api-key" >> ~/.openclaw/.env
echo "FEISHU_ENABLED=true" >> ~/.openclaw/.env
# ... 添加其他需要的环境变量
```

## 🚀 用法

### 基础使用

```typescript
import ChinaLocalization from './china-localization';

const local = new ChinaLocalization();

// 设置语言（默认为中文）
local.setLanguage('zh-CN');

// 获取飞书日历
const events = await local.getCalendarEvents();

// 获取飞书任务
const tasks = await local.getTasks();

// 中文搜索（默认使用百度搜索）
const results = await local.search('AI 新闻');

// 使用 Tavily 搜索
const tavilyResults = await local.search('AI 新闻', { engine: 'tavily' });

// 查询天气
const weather = await local.getWeather('深圳');
```

### 在 OpenClaw 中使用

```bash
# 安装后自动可用（需要正确配置环境变量）
china-localization --help
```

## 🔍 搜索引擎对比

| 引擎 | 优势 | 适用场景 |
|------|------|----------|
| **百度搜索** | 中文内容覆盖全面，本土化强 | 国内政策、中文社区、国产技术 |
| **Tavily** | 英文内容质量高，技术文档丰富 | 国际资讯、技术论文、架构分析 |
| **微信搜索** | 微信生态内容 | 公众号文章、小程序内容 |

## 📊 输出示例

### 飞书日历

```markdown
## 📅 今日安排
- **10:00-11:00** 团队周会 @ 会议室
- **14:00-15:00** 产品评审
```

### 飞书任务

```markdown
## ✅ 待办事项
- ⬜ 🔴 完成代码审查 (截止：today)
- ⬜ 🟡 准备周报 (截止：tomorrow)
```

### 天气查询

```markdown
## 🌤️ 深圳天气
- **温度**: 25°C
- **天气**: 晴
- **湿度**: 60%
- **建议**: 天气不错，适合出行，阳光较强，注意防晒
```

### 百度搜索结果

```markdown
## 🔍 AI 新闻 (百度搜索)

1. **【AI 新闻】人工智能最新进展 - 百度**
   - 内容: 这是关于 "AI 新闻" 的百度搜索结果...
   - [查看详情](https://www.baidu.com/s?wd=AI%20%E6%96%B0%E9%97%BB)

2. **【AI 新闻】大模型技术突破 - 百度**
   - 内容: 最新的人工智能大模型技术突破...
   - [查看详情](https://www.baidu.com/s?wd=AI%20%E6%96%B0%E9%97%BB)
```

## 📦 依赖

- Node.js 18+
- Tavily Search API (必需)
- 飞书开放平台（可选）
- 微信开放平台（可选）
- 钉钉开放平台（可选）
- 高德地图 API（可选）
- 支付宝开放平台（可选）

## 🛡️ 错误处理

- **网络失败**：中文错误提示 + 重试建议
- **权限不足**：引导用户授权 + 配置指南
- **API 失败**：友好提示 + 调试信息
- **配置缺失**：明确的环境变量设置指引

## 📈 版本历史

- **v2.0.0**: 安全优化版，集成百度搜索，符合 ClawHub 规范
- **v1.0.0**: 初始版本（存在安全问题）

## ❓ 常见问题

### Q: 如何获取飞书 API 权限？

A: 访问 https://open.feishu.cn/app 创建应用，申请权限。

### Q: 百度搜索和 Tavily 搜索有什么区别？

A: 百度搜索更适合中文内容和国内资讯，Tavily 搜索更适合英文技术内容和国际资讯。

### Q: 可以只使用语言包吗？

A: 可以，语言包是独立的模块，不需要配置任何 API keys。

### Q: 为什么需要设置这么多环境变量？

A: 这是为了安全考虑。所有敏感信息都通过环境变量配置，避免在代码中硬编码。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## ⭐ 如果觉得有用，请给个 Star！

这个技能让中国用户能够零门槛使用 OpenClaw，如果你觉得有用，请在 ClawHub 上给个 Star！