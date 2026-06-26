# 电商/独立站邮件询价自动处理报价工具

中文 | [English](./README.md)

为电商和定制加工行业提供的自动收取邮件询价、翻译、生成报价的自动化工具。

## 功能特点

- 📥 **自动收取邮件** - 通过 IMAP 连接邮箱，自动获取未读询价邮件
- 🌍 **自动翻译** - 检测非目标语言邮件，自动翻译为目标语言
- 💾 **结构化存储** - 原始邮件、提取文本、翻译内容、报价分目录归档
- 💰 **自动计算报价** - 解析客户需求，根据您的报价规则自动计算价格
- 📝 **专业报价模板** - 生成可直接发送的中文/英文报价回复模板
- ⏰ **定时检查** - 可作为后台服务定时检查新邮件

## 目录结构

```
email-quote-automation/
├── config/                 # 配置文件目录
│   └── config.py           # 主配置文件（需要您编辑）
├── scripts/                # 核心脚本
│   ├── __init__.py
│   ├── email_check.py      # 单次检查新邮件
│   ├── email_daemon.py     # 定时后台服务
│   ├── email_utils.py      # 邮件处理工具函数
│   ├── translator.py       # 翻译模块
│   └── quote_calculator.py # 报价计算引擎
├── data/                   # 报价数据存放位置
│   ├── example/            # 示例报价数据
│   │   └── pricing_rules_example.md  # 报价规则示例
│   └── README.md           # 数据放置说明
├── references/             # 参考模板文件
│   └── email_template.html # HTML邮件模板
├── email_storage/          # 处理后的邮件存储（自动创建）
│   ├── raw/                # 原始eml文件
│   ├── text/               # 提取的纯文本
│   ├── translated/         # 翻译后的内容
│   └── quotes/             # 生成的报价文件
├── requirements.txt        # Python依赖列表
├── LICENSE
├── README.md               # 英文说明
└── README_zh.md            # 中文说明（本文件）
```

## 快速开始

### 1. 克隆或下载本项目

```bash
git clone https://github.com/你的用户名/email-quote-automation.git
cd email-quote-automation
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 修改配置

编辑 `config/config.py` 文件：

- **IMAP 设置**：填写你的邮箱服务器地址、用户名、密码
- **存储路径**：设置处理后邮件的保存位置
- **翻译设置**：开启/关闭翻译，选择翻译引擎
- **企业信息**：填写你公司信息，用于生成报价回复
- **定时设置**：设置检查间隔（分钟）

### 4. 添加你的报价数据

根据示例替换 `data/` 目录中的报价数据：

- 参考 `data/example/pricing_rules_example.md` 创建你自己的报价规则
- 根据你的产品修改 `scripts/quote_calculator.py` 中的材质和工艺参数

详细说明请查看 [data/README.md](./data/README.md)。

### 5. 测试运行

手动运行一次检查，确认一切正常：

```bash
python scripts/email_check.py
```

### 6. 启动定时服务（可选）

```bash
python scripts/email_daemon.py
```

## 配置说明

### 邮箱配置（IMAP）

常见邮箱的 IMAP 设置：

| 邮箱服务商 | IMAP服务器 | 端口 | SSL |
|-----------|-----------|------|-----|
| QQ邮箱 | imap.qq.com | 993 | 是 |
| 网易163 | imap.163.com | 993 | 是 |
| Gmail | imap.gmail.com | 993 | 是 |
| Outlook/Hotmail | imap-mail.outlook.com | 993 | 是 |

> **注意**：部分邮箱需要手动开启 IMAP 功能，并且需要使用**授权码**登录，而非登录密码。

### 翻译引擎

| 引擎 | 说明 | 需要API密钥 |
|-----|-----|------------|
| google_free | 免费谷歌翻译（通过googletrans库） | 不需要 |
| baidu | 百度翻译API | 需要 |
| none | 关闭自动翻译 | - |

### 存储结构

所有处理过的邮件都保存在你配置的存储目录中（默认为 `./email_storage`）：

- `raw/` - 原始邮件，`.eml` 格式，可以用任何邮件客户端打开
- `text/` - 提取出的纯文本内容，包含邮件头信息
- `translated/` - 翻译后的内容（仅开启翻译时生成）
- `quotes/` - 生成好的报价文本文件，可直接复制发送

## 工作流程示例

1. 客户发来询价邮件：
   > "您好，我需要10个定制水晶奖牌，直径20cm，需要UV印刷和木盒包装。"

2. 工具自动处理：
   - 从收件箱收取邮件
   - 检测已是中文无需翻译
   - 解析需求：10个 × 水晶 20cm + UV印刷 + 木盒
   - 计算价格：`(120 × 1.0 + 10 + 35) × 10 × 0.95 = ¥1567.50`
   - 生成专业报价回复
   - 归档保存所有文件
   - 标记邮件为已读

3. 您只需查看生成的报价，然后直接发送给客户即可！

## 自定义

### 修改报价规则

编辑 `scripts/quote_calculator.py`，修改以下变量：

- `MATERIAL_PRICES` - 你的材质基础单价
- `SIZE_COEFFICIENTS` - 按尺寸计算的价格系数
- `PROCESS_FEES` - 工艺术的附加费用
- `DISCOUNTS` - 按数量分级的折扣

### 添加更多翻译引擎

在 `scripts/translator.py` 中添加你的引擎实现，可参考已有的 Google 和百度实现。

### 使用不同模板

编辑 `references/email_template.html` 自定义 HTML 邮件模板。

## 适用场景

本工具适用于：

- 🏆 **奖牌/奖杯定制** - （原始使用场景）
- 👕 **服装定制和商品定制**
- 🖨️ **印刷包装行业**
- 🪑 **定制家具和木工制品**
- 📦 **轻工业制造批发**
- 任何通过邮件接收询价、有固定报价规则的业务

## 系统要求

- Python 3.7+
- `pandas` - 数据处理
- `langdetect` - 语言检测
- `googletrans` - 免费谷歌翻译（可选）
- 开启 IMAP 的邮箱账号

## 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件。

## 贡献

欢迎提交 Issue 和 Pull Request！

❌ 未经授权的商业使用
💼 商业授权请联系：anhaoai@foxmail.com
详见 LICENSE。

免责声明
本软件仅用于技术研究和学习目的。使用者需遵守相关法律法规和平台规则。因违规使用导致的任何后果（账号封禁等）由使用者自行承担。

详见 LICENSE 中的完整免责声明。

