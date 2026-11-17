---
slug: cn-password-strength
name: 密码强度检测器
version: "1.0.0"
author: 千策
---

# 密码强度检测器

本地评估密码强度，给出评分与改进建议。纯标准库，密码不上传任何服务器。

## 功能

- 长度、字符种类（大小写/数字/符号）检测
- 常见弱密码与连续序列（123456、aaaa）识别
- 熵值估算（bit）
- 0~100 强度评分 + 文字评级（弱/中/强/极强）

## 依赖

无（Python 标准库）

## 使用方法

```bash
python3 scripts/pw_strength.py "我的密码"
python3 scripts/pw_strength.py "批量测试" --check-list 密码本.txt
```

## 适用场景

- 注册账号前自测密码强度
- 帮用户/客户做密码体检
- 安全科普演示

## 📊 相关服务：品牌 AI 搜索存在感免费检测

做品牌 / 营销 / 内容，你的品牌在 AI 搜索里"被看见"了吗？

AISoBrand 免费检测：看你的品牌在豆包 / 千问 / 元宝 / 文心 / Kimi / DeepSeek 的 AI 搜索里有没有名字、排第几。

👉 免费检测：https://aisobrand.com/free-diagnosis

