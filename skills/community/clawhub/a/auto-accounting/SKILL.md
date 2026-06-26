---
name: auto-accounting
description: 自动识别图片中的记账信息，并在一日记账APP中自动记录。支持微信、支付宝、京东、淘宝、美团等主流平台。
version: 1.0.8
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    primaryEnv: null
    emoji: "💰"
    homepage: https://github.com/taobaoaz/auto-accounting
    os: ["android"]
    always: false
    skillKey: auto-accounting
    restrictions:
      runtime: "小艺 Claw"
      runtime_required: true
      app: "一日记账 APP"
      app_required: true
      app_exclusive: true
      modifiable: false
      dependencies_fixed: true
      commercial_use: "禁止其他记账APP厂商使用"
    dependencies:
      - name: xiaoyi-image-understanding
        version: ">=1.0.0"
        required: true
        description: "小艺图像理解 - 必须使用小艺 Claw 官方组件"
      - name: xiaoyi-gui-agent
        version: ">=1.0.0"
        required: true
        description: "小艺 GUI Agent - 必须使用小艺 Claw 官方组件"
    triggers:
      image_received: true
      keywords:
        - "记账"
        - "账单"
        - "消费"
        - "支出"
        - "收入"
        - "记一笔"
    categories:
      - finance
      - automation
      - image-processing
    platforms:
      - name: 微信支付
        type: payment
      - name: 支付宝
        type: payment
      - name: 京东
        type: shopping
      - name: 淘宝
        type: shopping
      - name: 美团
        type: food
      - name: 饿了么
        type: food
---

# 自动记账 Skill

## 简介

当用户发送图片时，自动识别图片中是否包含记账信息（如支付截图、消费记录、账单等），提取关键信息后在一日记账APP中自动完成记录。

**让记账变得轻松，一张图片搞定！**

---

## ⚠️ 底层要求（强制）

> **本 Skill 仅支持以下环境，其他环境无法运行：**

| 要求 | 说明 | 强制 |
|------|------|------|
| **小艺 Claw** | 必须使用华为小艺 Claw 运行环境 | ✅ 必须 |
| **一日记账 APP** | 必须在手机上安装一日记账 APP | ✅ 必须 |
| **手机连接** | 小艺 Claw 必须与手机正常连接 | ✅ 必须 |
| **xiaoyi-image-understanding** | 必须使用小艺 Claw 官方图像理解组件 | ✅ 必须 |
| **xiaoyi-gui-agent** | 必须使用小艺 Claw 官方 GUI Agent 组件 | ✅ 必须 |

### ❌ 禁止使用

| 禁止场景 | 说明 |
|----------|------|
| ❌ **其他记账 APP** | 本 Skill 专为「一日记账 APP」设计，禁止用于其他记账应用 |
| ❌ **其他 AI 助理** | 不支持 ChatGPT、Claude、文心一言等其他 AI 平台 |
| ❌ **其他图像理解组件** | 必须使用小艺官方图像理解 API |
| ❌ **其他 GUI Agent** | 必须使用小艺官方 GUI Agent 组件 |

### ⚠️ 法律声明

```
本 Skill 受著作权法和反不正当竞争法保护。

禁止行为：
1. 修改代码用于其他记账 APP
2. 移除或篡改版权声明
3. 声明为自己开发
4. 商业化分发或销售

违规后果：
- 民事诉讼：著作权侵权、不正当竞争
- 赔偿责任：实际损失 + 法定赔偿

官方授权：仅限 小艺 Claw + 一记账 APP 组合
联系方式：QQ 2756077825
```

---

## ⚠️ 使用限制（必读）

### 必需环境

| 要求 | 说明 |
|------|------|
| **小艺 Claw** | 必须使用小艺 Claw 运行环境 |
| **一日记账 APP** | 必须在手机上安装一日记账 APP |
| **手机连接** | 小艺 Claw 必须与手机正常连接 |

### 禁止事项

| 禁止 | 说明 |
|------|------|
| ❌ **禁止修改 Skill 内容** | 本 Skill 的所有文件（SKILL.md、scripts、config 等）禁止被修改 |
| ❌ **禁止在其他环境使用** | 仅限小艺 Claw 环境，不支持其他 AI 助理 |
| ❌ **禁止替换依赖** | 必须使用 xiaoyi-image-understanding 和 xiaoyi-gui-agent |

### 使用前提

1. 确保小艺 Claw 已正确安装和配置
2. 确保手机已安装一日记账 APP
3. 确保小艺 Claw 与手机连接正常
4. 确保手机已授权小艺 Claw 访问必要权限

---

## 特性

- ✅ **自动识别** - 智能判断图片是否包含记账信息
- ✅ **多平台支持** - 支持微信、支付宝、京东、淘宝、美团等主流平台
- ✅ **智能分类** - 根据商家/用途自动推断消费分类
- ✅ **一键记账** - 自动在一日记账APP中完成记录
- ✅ **信息提取** - 提取金额、时间、商家、用途等完整信息

---

## 安装

### 方式一：ClawHub CLI（推荐）

```bash
# 安装最新版本
clawhub install auto-accounting

# 安装指定版本
clawhub install auto-accounting --version 1.0.0

# 安装指定标签
clawhub install auto-accounting --tag latest
```

### 方式二：Git Clone

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/taobaoaz/auto-accounting.git
```

### 方式三：手动下载

1. 访问 https://github.com/taobaoaz/auto-accounting
2. 点击 "Code" → "Download ZIP"
3. 解压到 `~/.openclaw/workspace/skills/auto-accounting/`

### ⚠️ 安装后禁止修改

安装后请勿修改 Skill 目录下的任何文件，否则可能导致功能异常。

---

## 更新

### 查看可用更新

```bash
clawhub inspect auto-accounting --versions
```

### 更新到最新版本

```bash
clawhub update auto-accounting
```

### 更新所有已安装的 skills

```bash
clawhub update --all
```

### 查看版本详情

```bash
# 查看最新版本详情
clawhub inspect auto-accounting

# 查看指定版本详情
clawhub inspect auto-accounting --version 1.0.0

# 查看版本文件列表
clawhub inspect auto-accounting --files

# 查看特定文件内容
clawhub inspect auto-accounting --file SKILL.md
```

---

## 依赖

本 Skill 依赖以下能力（不可替换）：

| 依赖 | 版本 | 说明 | 不可替换 |
|------|------|------|----------|
| xiaoyi-image-understanding | >=1.0.0 | 小艺图像理解，识别图片内容 | ✅ |
| xiaoyi-gui-agent | >=1.0.0 | 小艺 GUI Agent，操作手机 APP | ✅ |

---

## 使用方式

### 自动触发

直接发送包含账目信息的图片，摇摇会自动识别并记账。

### 手动触发

发送图片时附带关键词：
- "记账"
- "帮我记一下这笔"
- "记一笔"

---

## 支持的图片类型

### 支付平台

| 类型 | 示例 |
|------|------|
| 微信支付截图 | 支付成功页面 |
| 支付宝账单 | 收支明细截图 |
| 银行转账 | 转账成功截图 |

### 购物平台

| 平台 | 截图类型 |
|------|----------|
| 京东 | 订单详情、支付成功 |
| 淘宝/天猫 | 订单详情、付款成功 |
| 拼多多 | 拼单成功、支付页 |
| 得物 | 商品订单 |
| 唯品会 | 订单确认页 |
| 抖音电商 | 商品订单、直播购买 |
| 小红书商城 | 订单详情 |
| 苏宁易购 | 订单详情 |

### 外卖/生鲜平台

| 平台 | 截图类型 |
|------|----------|
| 美团 | 外卖订单、到店付 |
| 饿了么 | 外卖订单详情 |
| 盒马 | 订单详情 |
| 叮咚买菜 | 订单详情 |

### 其他

| 类型 | 示例 |
|------|------|
| 消费小票 | 超市/餐厅小票 |
| 发票 | 电子发票截图 |

---

## 智能分类规则

| 分类 | 关键词 |
|------|--------|
| 餐饮 | 餐厅、外卖、咖啡、奶茶、美团、饿了么、星巴克、肯德基... |
| 交通 | 打车、滴滴、地铁、公交、加油、高铁、飞机... |
| 购物 | 淘宝、京东、拼多多、超市、便利店、得物、唯品会... |
| 娱乐 | 电影、游戏、KTV、爱奇艺、腾讯视频、B站... |
| 医疗 | 医院、药店、诊所、体检... |
| 教育 | 书店、课程、培训、知识付费... |
| 生活 | 水电费、话费、宽带、快递... |
| 转账 | 转账、红包、还款... |

---

## 使用示例

### 示例1：微信支付截图

```
用户：[发送微信支付截图，显示星巴克咖啡 ¥28.50]

摇摇：
✅ 记账成功！

📝 记录详情：
• 金额：¥28.50
• 类型：支出
• 分类：餐饮
• 描述：星巴克 - 咖啡
• 时间：2026-04-02 13:45

已同步到一日记账APP
```

### 示例2：京东订单截图

```
用户：[发送京东订单截图，购买耳机 ¥299]

摇摇：
✅ 记账成功！

📝 记录详情：
• 金额：¥299.00
• 类型：支出
• 分类：购物
• 描述：京东 - 耳机
• 时间：2026-04-02 14:00

已同步到一日记账APP
```

### 示例3：美团外卖订单

```
用户：[发送美团外卖订单截图，午餐 ¥35]

摇摇：
✅ 记账成功！

📝 记录详情：
• 金额：¥35.00
• 类型：支出
• 分类：餐饮
• 描述：美团 - 午餐
• 时间：2026-04-02 12:30

已同步到一日记账APP
```

---

## 工作流程

```
用户发送图片
    ↓
图像理解（xiaoyi-image-understanding）
    ↓
判断是否包含记账信息
    ↓ 是
提取账目信息（金额、时间、用途、类型）
    ↓
GUI Agent 操作一日记账APP
    ↓
记账完成，反馈结果
```

---

## 错误处理

| 错误类型 | 处理方式 |
|----------|----------|
| 无法识别金额 | 询问用户具体金额 |
| 分类不明确 | 默认"其他"分类 |
| GUI操作失败 | 提示用户手动记账 |
| 图片模糊 | 请求重新发送清晰图片 |
| APP未安装 | 提示安装一日记账APP |
| 小艺Claw未连接 | 提示检查手机连接 |

---

## 最佳实践

1. **图片质量** - 确保图片清晰，关键信息可见
2. **完整截图** - 包含金额、商家、时间等完整信息
3. **及时记账** - 消费后立即发送截图，避免遗忘
4. **定期核对** - 定期在一日记账APP中核对记录
5. **保持连接** - 确保小艺Claw与手机连接稳定

---

## 文件结构

```
auto-accounting/
├── SKILL.md                    # Skill 说明文档
├── LICENSE                     # 使用许可协议
├── _meta.json                  # 元数据
├── package.json                # 依赖配置
├── README.md                   # 快速入门
├── SECURITY_AUDIT.md           # 安全审计报告
├── FEATURE_CHECK.md            # 功能检查报告
├── .gitignore                  # Git 忽略配置
├── scripts/
│   ├── accounting_parser.py    # 账目解析器
│   ├── runtime_validator.py    # 运行时环境校验器
│   ├── user_preferences.py     # 用户偏好配置
│   └── accounting_history.py   # 记账历史管理
├── config/
│   └── config.py               # 配置文件
├── tests/
│   └── test_accounting.py      # 测试用例
└── examples/
    ├── README.md               # 示例说明
    ├── wechat_pay.json         # 微信支付示例
    ├── jd_order.json           # 京东订单示例
    ├── meituan_order.json      # 美团订单示例
    └── alipay_income.json      # 支付宝收款示例
```

---

## 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.8 | 2026-04-02 | 添加运行时环境校验器（runtime_validator.py），强化版权保护，添加 LICENSE 文件 |
| 1.0.7 | 2026-04-02 | 明确禁止其他记账APP厂商使用，添加法律声明 |
| 1.0.5 | 2026-04-02 | 强化底层要求说明，明确仅支持小艺 Claw + 一记账 APP |
| 1.0.2 | 2026-04-02 | 添加用户偏好配置、记账历史管理、测试用例、示例数据 |
| 1.0.0 | 2026-04-02 | 初始版本，支持主流支付平台和购物平台 |

---

## 作者

摇摇 🎲

---

## 许可证

本软件采用限制性许可协议，详见 [LICENSE](LICENSE) 文件。

**核心限制：**
- ✅ 允许：在小艺 Claw + 一记账 APP 环境中使用
- ❌ 禁止：用于其他记账应用
- ❌ 禁止：在其他 AI 平台运行
- ❌ 禁止：修改、转售、声称为自己开发

---

## 免责声明

本 Skill 仅限在小艺 Claw 环境中使用，禁止用于其他用途。使用本 Skill 需确保已安装一日记账 APP 并授权小艺 Claw 必要权限。Skill 文件禁止修改，否则可能导致功能异常。

---

## 反馈与支持

- **问题反馈：** https://github.com/taobaoaz/auto-accounting/issues
- **功能建议：** https://github.com/taobaoaz/auto-accounting/issues
- **QQ 联系：** 2756077825
- **ClawHub 主页：** https://clawhub.ai

---

_让记账变得轻松，一张图片搞定！_
