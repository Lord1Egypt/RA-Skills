# Screen Recorder Demo Skill

## 概述

基于 Puppeteer 的自动化端到端测试录制 Skill，支持录制浏览器操作并生成演示视频/GIF。

## 功能特性

### 核心功能
- 🎥 **浏览器操作录制**：录制网页操作过程
- 🎯 **智能区域录制**：支持全屏或指定区域录制
- 🔄 **格式转换**：支持 MP4、GIF、WebM 格式
- ⚡ **自动化测试集成**：与测试框架无缝集成

### 高级功能
- 📊 **性能监控**：录制时显示FPS和文件大小
- 🎨 **视频编辑**：添加水印、字幕、片头片尾
- 🔧 **配置灵活**：支持多种录制参数配置
- 📱 **跨平台**：支持 Windows、macOS、Linux

## 安装要求

### 系统要求
- Node.js 16+
- npm 或 yarn
- Chrome/Chromium 浏览器

### 依赖安装
```bash
npm install puppeteer puppeteer-screen-recorder ffmpeg-static
# 或
yarn add puppeteer puppeteer-screen-recorder ffmpeg-static
```

## 快速开始

### 1. 基础录制
```javascript
const { ScreenRecorder } = require('./scripts/record-browser');

const recorder = new ScreenRecorder({
  outputPath: './recordings/demo.mp4',
  fps: 30,
  quality: 80
});

await recorder.startRecording('https://your-app.com');
// 执行操作...
await recorder.stopRecording();
```

### 2. 端到端测试录制
```javascript
const { recordE2ETest } = require('./scripts/record-test');

await recordE2ETest({
  url: 'http://localhost:3000',
  testSteps: [
    { action: 'click', selector: '#login-btn' },
    { action: 'type', selector: '#username', text: 'testuser' },
    { action: 'type', selector: '#password', text: 'password123' },
    { action: 'click', selector: '#submit-btn' }
  ],
  output: './recordings/login-test.mp4'
});
```

## API 文档

### ScreenRecorder 类

#### 构造函数
```javascript
new ScreenRecorder(options)
```

**options**:
- `outputPath` (string): 输出文件路径
- `fps` (number): 帧率，默认 30
- `quality` (number): 视频质量 0-100，默认 80
- `aspectRatio` (string): 宽高比，如 '16:9'
- `codec` (string): 视频编码器，默认 'libx264'

#### 方法
- `startRecording(url, options)`: 开始录制
- `stopRecording()`: 停止录制
- `pauseRecording()`: 暂停录制
- `resumeRecording()`: 恢复录制
- `addAnnotation(text, position)`: 添加标注
- `addWatermark(imagePath, position)`: 添加水印

### 工具函数

#### recordE2ETest(config)
录制端到端测试过程

**config**:
- `url` (string): 测试页面URL
- `testSteps` (Array): 测试步骤数组
- `output` (string): 输出文件路径
- `headless` (boolean): 是否无头模式，默认 false

#### convertVideo(input, output, options)
视频格式转换

#### mergeVideos(videos, output)
合并多个视频文件

## 配置示例

### 基础配置
```json
{
  "recorder": {
    "fps": 30,
    "quality": 80,
    "outputDir": "./recordings",
    "defaultFormat": "mp4"
  },
  "browser": {
    "headless": false,
    "viewport": { "width": 1920, "height": 1080 },
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

### 测试配置
```json
{
  "testSuites": {
    "login": {
      "url": "http://localhost:3000/login",
      "steps": "scripts/test-steps/login.json",
      "output": "recordings/login-test.mp4"
    },
    "dashboard": {
      "url": "http://localhost:3000/dashboard",
      "steps": "scripts/test-steps/dashboard.json",
      "output": "recordings/dashboard-test.mp4"
    }
  }
}
```

## 与测试框架集成

### Jest 集成
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

### Playwright 集成
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

## 目录结构

```
e2e-test/
├── SKILL.md                    # 技能文档
├── package.json                # 项目配置
├── scripts/
│   ├── record-browser.js       # 浏览器录制核心
│   ├── record-test.js          # 测试录制
│   ├── record-screen.js        # 屏幕录制
│   ├── convert-format.js       # 格式转换
│   ├── add-annotations.js      # 添加标注
│   └── utils.js                # 工具函数
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

## 使用示例

### 示例 1：录制登录流程
```javascript
const { recordE2ETest } = require('./scripts/record-test');

await recordE2ETest({
  url: 'http://localhost:3000',
  testName: '用户登录测试',
  steps: [
    {
      description: '访问登录页面',
      action: 'goto',
      url: '/login'
    },
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
    },
    {
      description: '验证登录成功',
      action: 'waitFor',
      selector: '.dashboard',
      timeout: 5000
    }
  ],
  output: 'recordings/login-demo.mp4',
  annotations: true
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

## 故障排除

### 常见问题

#### 1. 录制失败
- **问题**: 无法启动浏览器
- **解决**: 确保已安装 Chrome/Chromium，或设置 `executablePath`

#### 2. 视频质量差
- **问题**: 视频模糊或卡顿
- **解决**: 调整 `fps` 和 `quality` 参数，确保网络稳定

#### 3. 文件过大
- **问题**: 录制文件太大
- **解决**: 降低 `fps`、`quality`，或使用 `convertVideo` 压缩

#### 4. 内存不足
- **问题**: 录制过程中内存占用过高
- **解决**: 减少录制时长，或增加系统内存

### 调试模式
```javascript
const recorder = new ScreenRecorder({
  debug: true,  // 启用调试模式
  logLevel: 'verbose'
});
```

## 性能优化建议

### 录制优化
1. **降低帧率**: 非必要情况下使用 15-24 FPS
2. **调整分辨率**: 根据需求调整录制区域大小
3. **使用硬件加速**: 启用 GPU 加速录制

### 文件优化
1. **格式选择**: MP4 适合长视频，GIF 适合短视频
2. **压缩设置**: 使用合适的压缩参数
3. **分段录制**: 长时间录制可分段保存

## 许可证

MIT License

## 更新日志

### v1.0.0 (2026-04-11)
- 初始版本发布
- 支持基础浏览器录制
- 支持 MP4/GIF 格式输出
- 提供端到端测试录制功能

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 联系支持

- 问题反馈: [GitHub Issues](https://github.com/your-org/e2e-test/issues)
- 文档: [项目 Wiki](https://github.com/your-org/e2e-test/wiki)
- 邮件: support@example.com