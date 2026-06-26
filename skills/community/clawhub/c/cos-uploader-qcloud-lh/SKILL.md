---
name: "COS 照片上传助手"
description: "通过微信接收照片，自动上传到腾讯云 COS 低频存储，按年月归档管理"
version: 1.0.0
author: "jingronzhao"
license: MIT
keywords: ["腾讯云", "COS", "照片上传", "微信", "低频存储", "自动化"]
---

## 技能入口

- **入口脚本**: `run.sh`
- **脚本语言**: Python 3.6+
- **超时时间**: 60 秒

## 触发条件

当收到包含图片附件的微信消息时自动触发。

匹配模式：`[media attached: <路径> (image/*)]`

## 核心功能

1. **自动解析**：从 OpenClaw 消息体中提取图片本地缓存路径
2. **内网上传**：通过腾讯云内网域名上传到 COS，零流量费用
3. **低频存储**：自动设置为 STANDARD_IA 存储类型，降低存储成本
4. **智能归档**：按 `年/月/月日_随机数.扩展名` 格式自动归档
5. **全量加密**：桶名、Region、SecretId / SecretKey 等全部使用 Fernet 对称加密存储

## 配置参数

所有 COS 配置（桶名、Region、存储类型、网络模式、API 密钥）均通过 `setup_config.py` 交互式配置，加密存储在 `scripts/conf/cos_secret.enc` 中，源代码中不包含任何敏感信息。

## 依赖

- Python >= 3.6
- cos-python-sdk-v5 >= 1.9.30
- cryptography >= 41.0.0

## 文件结构

```
cos-photo-uploader/
├── SKILL.md              # 技能清单（本文件）
├── README.md             # 详细说明文档
├── run.sh                # 运行入口
├── install.sh            # 安装脚本
├── package.sh            # 打包脚本
├── scripts/              # 技能代码
│   ├── skill_handler.py  # Skill 处理入口
│   ├── cos_uploader.py   # COS 上传核心模块
│   ├── config.py         # 加密配置管理
│   ├── setup_config.py   # 一站式配置工具（桶信息 + 密钥）
│   └── requirements.txt  # Python 依赖
└── screenshots/          # 截图
    └── .gitkeep
```
