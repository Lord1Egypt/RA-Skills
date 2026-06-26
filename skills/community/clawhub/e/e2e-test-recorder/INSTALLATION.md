# E2E测试录制Skill安装指南

## 📦 安装步骤

### 1. 前置要求
- Node.js 16+ 
- npm 或 yarn
- Chrome/Chromium浏览器

### 2. 安装依赖
由于网络问题可能导致直接安装失败，建议使用以下方法：

#### 方法A：使用国内镜像
```bash
# 设置npm镜像
npm config set registry https://registry.npmmirror.com

# 安装依赖
cd D:\knowledge\coding\e2e-test
npm install
```

#### 方法B：手动安装核心依赖
```bash
# 安装基础依赖
npm install puppeteer@21.0.0
npm install fs-extra@11.0.0
npm install chalk@4.0.0
npm install commander@11.0.0
npm install inquirer@8.0.0
npm install ora@5.0.0

# 安装录制相关依赖（可能需要单独下载）
# puppeteer-screen-recorder 和 ffmpeg-static 可能需要手动下载
```

#### 方法C：使用预构建版本
如果网络问题无法解决，可以使用简化版本：

```javascript
// 修改 scripts/record-browser.js
// 注释掉 puppeteer-screen-recorder 相关代码
// 使用替代方案或手动录制
```

### 3. 验证安装
```bash
# 检查Node.js版本
node --version

# 检查依赖
cd D:\knowledge\coding\e2e-test
node scripts/utils.js
```

## 🚀 快速使用

### 基础使用（无需安装依赖）
```javascript
// 创建简化版本的录制器
const fs = require('fs-extra');
const path = require('path');

class SimpleRecorder {
  constructor(options = {}) {
    this.options = options;
    this.outputDir = options.outputDir || './recordings';
    fs.ensureDirSync(this.outputDir);
  }
  
  async recordManual(testName, steps) {
    console.log(`📝 测试: ${testName}`);
    console.log(`📋 步骤数: ${steps.length}`);
    
    // 生成测试报告
    const report = {
      testName,
      timestamp: new Date().toISOString(),
      steps: steps.map((step, i) => ({
        step: i + 1,
        description: step.description,
        status: 'manual'
      })),
      instructions: [
        '1. 使用屏幕录制工具（如Windows Game Bar）录制测试过程',
        '2. 保存为MP4或GIF格式',
        '3. 将文件放入 recordings/ 目录'
      ]
    };
    
    const reportPath = path.join(this.outputDir, `${testName}_report.json`);
    await fs.writeJson(reportPath, report, { spaces: 2 });
    
    console.log(`📄 测试报告已生成: ${reportPath}`);
    return reportPath;
  }
}

// 使用示例
const recorder = new SimpleRecorder();
await recorder.recordManual('登录测试', [
  { description: '访问登录页面' },
  { description: '输入用户名' },
  { description: '输入密码' },
  { description: '点击登录按钮' }
]);
```

### 命令行使用（简化版）
```bash
# 生成测试配置
node scripts/cli.js config --name "登录测试" --url "http://localhost:3000"

# 查看帮助
node scripts/cli.js --help
```

## 🔧 配置说明

### 配置文件位置
- `configs/default.json` - 默认配置
- `configs/test.json` - 测试配置（示例）

### 自定义配置
创建 `configs/custom.json`：
```json
{
  "recorder": {
    "fps": 24,
    "quality": 80,
    "outputDir": "./my-recordings"
  },
  "browser": {
    "headless": false,
    "viewport": {
      "width": 1280,
      "height": 720
    }
  }
}
```

## 📝 使用示例

### 示例1：录制前端测试
```javascript
const { SimpleRecorder } = require('./scripts/simple-recorder');

const recorder = new SimpleRecorder({
  outputDir: './recordings/frontend-tests'
});

// 录制Multi-Agent Flow前端测试
await recorder.recordManual('Multi-Agent Flow前端测试', [
  {
    description: '访问 http://localhost:8001/docs',
    note: '查看API文档'
  },
  {
    description: '测试健康检查API',
    note: '检查 /health 端点'
  },
  {
    description: '测试模板匹配API',
    note: '使用查询词 "TODO任务管理"'
  },
  {
    description: '查看系统信息',
    note: '验证系统状态'
  }
]);
```

### 示例2：录制API测试
```javascript
await recorder.recordManual('API测试录制', [
  {
    description: '健康检查API测试',
    note: '预期状态码: 200'
  },
  {
    description: '用户注册API测试',
    note: '测试数据: {username: "test", email: "test@example.com"}'
  },
  {
    description: '模板匹配API测试',
    note: '测试查询: "网页制作"'
  }
]);
```

## 🎥 屏幕录制替代方案

### Windows平台
1. **Windows Game Bar** (Win + G)
   - 内置屏幕录制功能
   - 支持录制任意应用
   - 输出为MP4格式

2. **OBS Studio** (免费)
   - 专业级录制软件
   - 支持多种格式
   - 可录制特定窗口

3. **ShareX** (免费)
   - 截图和录制工具
   - 支持GIF录制
   - 开源免费

### 录制步骤
1. 打开屏幕录制工具
2. 设置录制区域（浏览器窗口）
3. 开始录制
4. 执行测试步骤
5. 停止录制
6. 保存文件到 `recordings/` 目录

## 📊 测试报告生成

即使无法自动录制，工具仍可生成详细的测试报告：

```bash
# 生成测试报告
node scripts/cli.js report --name "安全测试" --type "p0"

# 查看报告
cat recordings/安全测试_report.json
```

## 🔍 故障排除

### 常见问题

#### 1. 依赖安装失败
**解决方案**：
```bash
# 清理npm缓存
npm cache clean --force

# 使用yarn替代
npm install -g yarn
yarn install

# 或使用cnpm
npm install -g cnpm --registry=https://registry.npmmirror.com
cnpm install
```

#### 2. Puppeteer无法启动
**解决方案**：
```javascript
// 修改配置，使用系统Chrome
const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: false
});
```

#### 3. 内存不足
**解决方案**：
- 关闭其他应用程序
- 增加Node.js内存限制：`node --max-old-space-size=4096 script.js`
- 减少录制时长

### 调试模式
```bash
# 启用调试日志
set DEBUG=*
node scripts/cli.js --debug check
```

## 📈 后续计划

### 短期改进
1. 添加离线安装包支持
2. 提供简化版本（无需puppeteer-screen-recorder）
3. 增强手动录制工作流

### 长期目标
1. 集成更多录制后端（OBS、FFmpeg等）
2. 添加云录制支持
3. 开发Web界面

## 🤝 获取帮助

- 查看 `README.md` 获取完整文档
- 参考 `examples/` 目录中的示例
- 查看 `SKILL.md` 了解技能协议
- 如有问题，创建简化版本或使用手动录制

---

**注意**：如果遇到网络问题无法安装完整依赖，建议使用简化版本或手动录制方案。核心的测试报告生成和配置管理功能仍可正常使用。