# E2E测试录制工具

基于 Puppeteer 的自动化端到端测试录制工具，支持录制浏览器操作并生成演示视频/GIF。

## ✨ 特性

- 🎥 **浏览器操作录制**：录制网页操作过程
- 🎯 **智能区域录制**：支持全屏或指定区域录制
- 🔄 **格式转换**：支持 MP4、GIF、WebM 格式
- ⚡ **自动化测试集成**：与测试框架无缝集成
- 📊 **性能监控**：录制时显示FPS和文件大小
- 🎨 **视频编辑**：添加水印、字幕、片头片尾
- 🔧 **配置灵活**：支持多种录制参数配置
- 📱 **跨平台**：支持 Windows、macOS、Linux

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/your-org/e2e-test-recorder.git
cd e2e-test-recorder

# 安装依赖
npm install

# 或使用 yarn
yarn install
```

### 基础使用

```javascript
const { ScreenRecorder } = require('./scripts/record-browser');

const recorder = new ScreenRecorder({
  outputPath: './recordings/demo.mp4',
  fps: 30,
  quality: 80
});

// 开始录制
await recorder.startRecording('https://your-app.com');

// 执行操作...
await recorder.page.click('#login-btn');
await recorder.page.type('#username', 'testuser');
await recorder.page.type('#password', 'password123');

// 停止录制
await recorder.stopRecording();
```

### 命令行使用

```bash
# 录制指定URL
npx e2e-test record https://example.com --timeout 30 --quality 85

# 录制端到端测试
npx e2e-test test configs/my-test.json

# 录制API测试
npx e2e-test api configs/api-test.json --format gif

# 检查系统环境
npx e2e-test check
```

## 📁 项目结构

```
e2e-test/
├── SKILL.md                    # 技能文档
├── README.md                   # 项目说明
├── package.json                # 项目配置
├── scripts/
│   ├── record-browser.js       # 浏览器录制核心
│   ├── record-test.js          # 测试录制
│   ├── record-screen.js        # 屏幕录制
│   ├── convert-format.js       # 格式转换
│   ├── add-annotations.js      # 添加标注
│   ├── utils.js                # 工具函数
│   └── cli.js                  # 命令行接口
├── configs/
│   ├── default.json            # 默认配置
│   ├── test.json               # 测试配置
│   └── production.json         # 生产配置
├── templates/
│   ├── demo-template.js        # 演示模板
│   └── test-template.js        # 测试模板
├── examples/
│   ├── basic-recording.js      # 基础录制示例
│   ├── e2e-test.js             # 端到端测试示例
│   └── api-test.js             # API测试示例
└── recordings/                 # 录制文件输出目录
```

## 🔧 配置说明

### 基础配置 (configs/default.json)

```json
{
  "recorder": {
    "fps": 30,
    "quality": 80,
    "aspectRatio": "16:9",
    "codec": "libx264",
    "outputDir": "./recordings",
    "defaultFormat": "mp4"
  },
  "browser": {
    "headless": false,
    "viewport": {
      "width": 1920,
      "height": 1080
    },
    "slowMo": 50
  },
  "annotations": {
    "enabled": true,
    "fontSize": 24,
    "fontColor": "#ffffff",
    "backgroundColor": "#00000080"
  }
}
```

### 测试配置示例

```json
{
  "testName": "用户登录测试",
  "url": "http://localhost:3000",
  "output": "./recordings/login-test.mp4",
  "testSteps": [
    {
      "description": "访问登录页面",
      "action": "goto",
      "url": "/login"
    },
    {
      "description": "输入用户名",
      "action": "type",
      "selector": "#username",
      "text": "test@example.com"
    },
    {
      "description": "输入密码",
      "action": "type",
      "selector": "#password",
      "text": "password123"
    },
    {
      "description": "点击登录按钮",
      "action": "click",
      "selector": "button[type='submit']"
    }
  ]
}
```

## 📚 API 文档

### ScreenRecorder 类

#### 构造函数
```javascript
new ScreenRecorder(options)
```

**参数**:
- `outputPath` (string): 输出文件路径
- `fps` (number): 帧率，默认 30
- `quality` (number): 视频质量 0-100，默认 80
- `aspectRatio` (string): 宽高比，如 '16:9'
- `headless` (boolean): 是否无头模式，默认 false
- `viewport` (Object): 视口尺寸 {width, height}
- `debug` (boolean): 调试模式，默认 false

#### 方法
- `startRecording(url, options)`: 开始录制
- `stopRecording()`: 停止录制
- `pauseRecording()`: 暂停录制
- `resumeRecording()`: 恢复录制
- `performActions(actions)`: 执行操作数组
- `addAnnotation(text, position)`: 添加标注
- `getStatus()`: 获取录制状态

### 工具函数

#### recordE2ETest(config)
录制端到端测试过程

#### recordAPITest(config)
录制API测试过程

#### quickRecord(url, options)
快速录制函数

## 🎯 使用示例

### 示例 1：录制登录流程
```javascript
const { recordE2ETest } = require('./scripts/record-test');

await recordE2ETest({
  url: 'http://localhost:3000',
  testName: '用户登录测试',
  steps: [
    {
      description: '输入用户名',
      action: 'type',
      selector: '#username',
      text: 'test@example.com'
    },
    {
      description: '输入密码',
      action: 'type',
      selector: '#password',
      text: 'password123'
    },
    {
      description: '点击登录按钮',
      action: 'click',
      selector: 'button[type="submit"]'
    }
  ],
  output: 'recordings/login-demo.mp4'
});
```

### 示例 2：录制API测试
```javascript
const { recordAPITest } = require('./scripts/record-test');

await recordAPITest({
  apiUrl: 'http://localhost:8000/api',
  tests: [
    {
      name: '健康检查API',
      endpoint: '/health',
      method: 'GET',
      expectedStatus: 200
    },
    {
      name: '用户注册API',
      endpoint: '/auth/register',
      method: 'POST',
      data: {
        username: 'testuser',
        email: 'test@example.com',
        password: 'Password123!'
      },
      expectedStatus: 201
    }
  ],
  output: 'recordings/api-test.gif'
});
```

## 🔌 集成指南

### 与测试框架集成

#### Jest 集成
```javascript
// jest.config.js
module.exports = {
  setupFilesAfterEnv: ['./jest.setup.js'],
  reporters: [
    'default',
    ['./scripts/jest-video-reporter', { outputDir: './test-recordings' }]
  ]
};
```

#### Playwright 集成
```javascript
// playwright.config.js
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  use: {
    video: 'on',
    screenshot: 'on',
  },
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['./scripts/playwright-video-reporter', { format: 'gif' }]
  ]
});
```

### 与 CI/CD 集成

```yaml
# GitHub Actions 示例
name: E2E Test Recording
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test
      - run: npx e2e-test record http://localhost:3000 --timeout 60
      - uses: actions/upload-artifact@v3
        with:
          name: test-recordings
          path: recordings/
```

## 🐛 故障排除

### 常见问题

#### 1. 录制失败：无法启动浏览器
**解决方案**：
- 确保已安装 Chrome/Chromium
- 设置 `executablePath` 选项
- 使用 `headless: true` 模式

#### 2. 视频质量差
**解决方案**：
- 调整 `fps` 和 `quality` 参数
- 确保网络稳定
- 使用合适的视频编码器

#### 3. 文件过大
**解决方案**：
- 降低 `fps` 和 `quality`
- 使用 `convertVideo` 压缩
- 选择 GIF 格式替代 MP4

#### 4. 内存不足
**解决方案**：
- 减少录制时长
- 增加系统内存
- 使用分段录制

### 调试模式

```javascript
const recorder = new ScreenRecorder({
  debug: true,  // 启用调试模式
  logLevel: 'verbose'
});
```

## 📈 性能优化

### 录制优化
1. **降低帧率**: 非必要情况下使用 15-24 FPS
2. **调整分辨率**: 根据需求调整录制区域大小
3. **使用硬件加速**: 启用 GPU 加速录制

### 文件优化
1. **格式选择**: MP4 适合长视频，GIF 适合短视频
2. **压缩设置**: 使用合适的压缩参数
3. **分段录制**: 长时间录制可分段保存

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目基于 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系支持

- 问题反馈: [GitHub Issues](https://github.com/your-org/e2e-test-recorder/issues)
- 文档: [项目 Wiki](https://github.com/your-org/e2e-test-recorder/wiki)
- 邮件: support@example.com

## 🙏 致谢

感谢以下开源项目：
- [Puppeteer](https://pptr.dev/) - 浏览器自动化
- [puppeteer-screen-recorder](https://github.com/adrielcodeco/puppeteer-screen-recorder) - 屏幕录制
- [FFmpeg](https://ffmpeg.org/) - 视频处理

---

**注意**: 本项目仍在积极开发中，API 可能会有变动。建议在生产环境使用前进行全面测试。