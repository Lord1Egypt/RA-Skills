# Email Marketing Skill

智能邮件营销工具，支持AI自动生成美观HTML、个性化群发、自动回信等功能。

## ✨ 核心特性

### 🤖 AI智能生成HTML
- 根据邮件文案内容自动选择合适的设计风格
- 在 OpenClaw 平台中由 AI Agent 直接将纯文本转换为 HTML
- 严格保留原文内容和变量占位符
- 响应式设计，兼容所有主流邮件客户端

### 📧 个性化群发
- 从Excel读取收件人列表
- 支持【变量名】动态替换
- 防垃圾邮件策略（随机延迟、指纹码）
- 批量发送进度跟踪

### 🔄 智能自动回信
- 扫描收件箱未读邮件
- FAQ知识库智能匹配
- 多语言自动对齐
- 商务礼仪语气生成

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 邮件发送配置（必需）
export EMAIL_SMTP_USER='your-email@example.com'
export EMAIL_SMTP_PASS='your-password'
export EMAIL_TEST_TARGET='test@example.com'

# SMTP/IMAP 服务器配置（可选）
export EMAIL_SMTP_HOST='example.com'  # 默认: example.com
export EMAIL_SMTP_PORT='123'                # 默认: 123
export EMAIL_IMAP_HOST='example.com'  # 默认: example.com
export EMAIL_IMAP_PORT='456'                # 默认: 456

# FAQ 文件路径（可选，自动回信功能需要）
export EMAIL_FAQ_PATH='~/Desktop/faq.txt'   # 默认: ~/Desktop/faq.txt
```

### 3. 检查环境

```bash
cd scripts
python3 check_setup.py
```

### 4. 准备文案

创建 `~/Desktop/邮件文案.txt`：

```text
亲爱的【kol name】，

您好！

我是来XXX的某某某

期待您的回复！
```

### 5. AI生成HTML

**重要**: 这个功能需要 AI 支持，在 openclaw 环境中可以直接使用 AI 将纯文本文案转换为 HTML。

将文案保存到 `~/Desktop/邮件文案.txt`，然后使用 AI 生成对应的 HTML 文件并保存为 `~/Desktop/邮件内容.html`。

**生成要求**:
- 根据文案内容自动选择合适的设计风格
- 响应式设计，兼容移动端和桌面端
- 严格保留【变量名】占位符
- 兼容主流邮件客户端

### 6. 测试发送

```bash
python3 final_sender.py
```

### 7. 正式群发

```bash
python3 final_sender.py run
```

## 📁 文件结构

```
email-marketing/
├── SKILL.md                    # Skill说明文档
├── README.md                   # 快速开始指南
├── requirements.txt            # Python依赖
├── scripts/
│   ├── check_setup.py         # 环境检查脚本
│   ├── final_sender.py        # 邮件群发脚本
│   ├── auto_reply_manager.py  # 自动回信管理
│   └── check_replies.py       # 统计报表
└── assets/
    ├── email_status.json      # 发送状态日志
    └── reply_stats.json       # 回信统计日志
```

## 📖 详细文档

- [SKILL.md](SKILL.md) - Skill完整说明和最佳实践

## 🎯 使用场景

### 场景1: KOL合作邀请
```bash
# 1. 准备KOL名单 (邮箱.xlsx)
# 2. 编写邀请文案 (邮件文案.txt)
# 3. 使用 AI 生成 HTML (邮件内容.html)
# 4. 测试发送
python3 final_sender.py

# 5. 批量群发
python3 final_sender.py run
```

### 场景2: 产品推广营销
```bash
# 准备推广文案，使用 AI 生成活泼风格的 HTML
# 然后执行发送流程
```

### 场景3: 商务通知邮件
```bash
# 准备商务通知，使用 AI 生成正式风格的 HTML
# 然后执行发送流程
```

## 💡 最佳实践

1. **文案编写**
   - 使用【变量名】实现个性化
   - 保持段落清晰，重点突出
   - 避免过长的句子

2. **AI生成**
   - 正式商务邮件 → 使用严肃、专业的风格
   - 营销推广邮件 → 使用活泼、吸引人的风格
   - 生成后检查一次HTML确保变量保留

3. **群发策略**
   - 先测试发送1封到自己邮箱
   - 检查邮件显示效果（移动端、桌面端）
   - 确认无误后再执行全量群发

4. **防垃圾邮件**
   - 脚本自动添加随机延迟
   - 内置指纹码干扰扫描
   - 建议每日发送量 < 500封

## 🔧 故障排查

### 问题1: 依赖包安装失败

```bash
# 检查 Python 版本（需要 3.8+）
python3 --version

# 升级 pip
pip install --upgrade pip

# 重新安装依赖
pip install -r requirements.txt
```

### 问题2: 发送失败

```bash
# 检查SMTP配置
echo $EMAIL_SMTP_USER
echo $EMAIL_SMTP_PASS

# 查看错误日志
cat assets/email_status.json
```

### 问题3: 变量未替换

- 检查Excel列名是否与【变量名】匹配
- 确保Excel文件路径正确
- 变量名不区分大小写但必须完全一致

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 License

MIT License
