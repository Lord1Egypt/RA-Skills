# Chaoxing Auto Grade

超星（学习通）作业自动批改技能。使用 Playwright 自动化 + 通义千问 AI 进行主观题智能评分。

## 功能

- 🔐 自动登录学习通
- 📚 根据课程名选择课程
- 📝 自动找到未批改的作业
- 🤖 AI 智能评分（通义千问 API）
- ✅ 自动提交成绩
- 📄 支持翻页处理多个作业

## 配置

修改 `config.json`：

```json
{
  "username": "你的学习通账号",
  "password": "你的学习通密码",
  "courseName": "课程名称（留空选第一个）",
  "apiKey": "通义千问 API Key",
  "model": "qwen-plus",
  "minScore": 60,
  "maxScore": 99,
  "chromePath": ""
}
```

## 使用

```bash
cd scripts
npm install
npx playwright install chromium
npx playwright test auto-grade.spec.js --headed
```

## 获取 API Key

1. 访问 [阿里云百炼](https://bailian.console.aliyun.com/)
2. 开通通义千问服务
3. 创建 API Key
