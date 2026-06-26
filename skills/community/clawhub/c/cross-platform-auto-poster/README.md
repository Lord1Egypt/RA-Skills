# 跨平台内容自动发布

全自动化跨平台内容发布工作流，支持AI原创内容生产 + 自动发布，也支持国内视频搬运去重后发布到海外平台。

## 快速开始

### 1. 安装依赖

```bash
# 确保已安装 playwright
npm install -g playwright
npx playwright install chromium

# 安装 ffmpeg (用于视频处理)
# Windows: 下载ffmpeg并添加到PATH
# https://ffmpeg.org/download.html
```

### 2. 配置账号

编辑 `config/accounts.json` 添加你的账号：

```json
{
  "xiaohongshu": [
    {
      "name": "我的小红书账号",
      "cookiePath": "xiaohongshu-account1.json"
    }
  ]
}
```

### 3. 首次登录保存认证

```javascript
const { addXiaohongshuAccount } = require('cross-platform-auto-poster');
await addXiaohongshuAccount('账号名', 'xiaohongshu-account1.json');
```

会打开浏览器让你扫码登录，登录完成后自动保存 cookies。

### 4. 运行AI原创图文发布

```javascript
const { XiaohongshuTextImageWorkflow } = require('cross-platform-auto-poster');

const workflow = new XiaohongshuTextImageWorkflow();
const result = await workflow.run({
  topic: "新手健身5个常见误区",
  style: "干货",
  accountIndex: 0
});

console.log(result);
```

## 支持的工作流

- ✅ AI原创小红书图文（选题→文案→封面→发布）
- 🚧 AI原创小红书口播视频（开发中）
- 🚧 抖音/快手视频搬运去重到TikTok/YouTube（开发中）

## 目录结构

```
cross-platform-auto-poster/
├── SKILL.md                 # 技能说明
├── package.json             # npm 配置
├── index.js                 # 主入口
├── README.md                # 这个文件
├── src/
│   ├── workflows/           # 完整工作流
│   │   └── xiaohongshu-text-image.js
│   └── platforms/          # 各平台发布实现
│       └── xiaohongshu-publisher.js
├── config/
│   └── accounts.json       # 账号配置
├── auth/                    # 保存认证信息 (gitignore)
└── output/                  # 发布输出记录
```

## 注意事项

1. **账号安全**：不要频繁发布，控制发布频率，避免触发风控
2. **内容质量**：AI生成的内容建议人工检查后再发布
3. **遵守规则**：遵守各平台社区规范，不要发布违规内容
4. **法律合规**：搬运内容请遵守原作者版权规定

## License

MIT
