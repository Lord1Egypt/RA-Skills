# 超星（学习通）作业自动批改

> 使用 Playwright 自动化 + 通义千问 AI 进行主观题智能评分

## 功能特点

- 🔐 **自动登录** - 支持手机号/超星号登录学习通
- 📚 **课程选择** - 根据课程名自动选择课程
- 📝 **智能批改** - 自动找到未批改的作业
- 🤖 **AI 评分** - 使用通义千问 API 进行智能评分
- ✅ **自动提交** - 自动提交成绩并进入下一份
- 📄 **翻页支持** - 支持处理多页作业列表

## 安装

### 1. 安装依赖

```bash
cd scripts
npm install
npx playwright install chromium
```

### 2. 配置

修改 `config.json` 文件：

```json
{
  "username": "你的学习通账号",
  "password": "你的学习通密码",
  "courseName": "课程名称（留空选第一个）",
  "apiKey": "通义千问 API Key",
  "model": "qwen-plus",
  "minScore": 60,
  "maxScore": 99,
  "chromePath": "Chrome 浏览器路径（可选）"
}
```

### 3. 获取通义千问 API Key

1. 访问 [阿里云百炼](https://bailian.console.aliyun.com/)
2. 注册/登录阿里云账号
3. 开通「通义千问」服务
4. 在 API-KEY 管理中创建新的 API Key

## 使用方法

```bash
cd scripts
npx playwright test auto-grade.spec.js --headed
```

## 评分标准

AI 会根据以下标准进行评分：

| 标准 | 说明 |
|------|------|
| 答案完整性 | 是否回答了问题的所有部分 |
| 准确性 | 答案内容是否正确 |
| 逻辑清晰度 | 表达是否清晰有条理 |

## 配置项说明

| 配置项 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| username | string | ✅ | 学习通登录账号 |
| password | string | ✅ | 学习通登录密码 |
| courseName | string | ❌ | 课程名称，留空选择第一个课程 |
| apiKey | string | ✅ | 通义千问 API Key |
| model | string | ❌ | AI 模型，默认 qwen-plus |
| minScore | number | ❌ | 最低分数，默认 60 |
| maxScore | number | ❌ | 最高分数，默认 99 |
| chromePath | string | ❌ | Chrome 浏览器路径，留空使用系统默认 |

## 注意事项

1. **浏览器要求** - 需要安装 Chrome 浏览器
2. **网络要求** - 需要稳定的网络连接
3. **分数范围** - 默认 60-99 分，可在配置中修改
4. **API 费用** - 通义千问 API 调用会产生费用，请注意用量

## 技术栈

- [Playwright](https://playwright.dev/) - 浏览器自动化
- [通义千问 API](https://help.aliyun.com/zh/dashscope/) - AI 评分

## License

MIT
