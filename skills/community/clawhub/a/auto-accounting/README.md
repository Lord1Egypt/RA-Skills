# 自动记账 Skill

> 自动识别图片中的记账信息，并在一日记账APP中自动记录

[![ClawHub](https://img.shields.io/badge/ClawHub-auto--accounting-blue)](https://clawhub.ai)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](https://github.com/taobaoaz/auto-accounting)
[![License](https://img.shields.io/badge/license-MIT--0-orange)](LICENSE)

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
| ❌ **禁止修改 Skill 内容** | 本 Skill 的所有文件禁止被修改 |
| ❌ **禁止在其他环境使用** | 仅限小艺 Claw 环境 |
| ❌ **禁止替换依赖** | 必须使用 xiaoyi 系列依赖 |

---

## 快速开始

### 安装

```bash
# 使用 ClawHub CLI 安装（推荐）
clawhub install auto-accounting

# 或使用 Git Clone
cd ~/.openclaw/workspace/skills
git clone https://github.com/taobaoaz/auto-accounting.git
```

### 更新

```bash
# 查看可用版本
clawhub inspect auto-accounting --versions

# 更新到最新版本
clawhub update auto-accounting
```

### 使用

直接发送包含账目信息的图片即可：

- 微信/支付宝支付截图
- 京东、淘宝等购物平台订单
- 美团、饿了么外卖订单
- 消费小票、发票

---

## 支持平台

### 支付平台
- 微信支付
- 支付宝
- 银联

### 购物平台
- 京东
- 淘宝/天猫
- 拼多多
- 得物
- 唯品会
- 抖音电商
- 小红书商城
- 苏宁易购

### 外卖/生鲜
- 美团
- 饿了么
- 盒马
- 叮咚买菜

---

## 智能分类

| 分类 | 关键词 |
|------|--------|
| 餐饮 | 餐厅、外卖、咖啡、奶茶... |
| 交通 | 打车、地铁、加油... |
| 购物 | 淘宝、京东、超市... |
| 娱乐 | 电影、游戏、会员... |
| 医疗 | 医院、药店... |
| 教育 | 课程、书籍... |
| 生活 | 水电费、话费... |

---

## 依赖（不可替换）

- xiaoyi-image-understanding >=1.0.0
- xiaoyi-gui-agent >=1.0.0

---

## CLI 命令参考

```bash
# 安装
clawhub install auto-accounting

# 查看详情
clawhub inspect auto-accounting

# 查看版本列表
clawhub inspect auto-accounting --versions

# 查看文件列表
clawhub inspect auto-accounting --files

# 更新
clawhub update auto-accounting

# 卸载
clawhub uninstall auto-accounting
```

---

## 作者

摇摇 🎲

---

## 许可证

MIT-0

---

## 反馈

- **Issues:** https://github.com/taobaoaz/auto-accounting/issues
- **QQ:** 2756077825
- **ClawHub:** https://clawhub.ai

---

**免责声明**：本 Skill 仅限小艺 Claw 环境使用，禁止修改 Skill 文件。
