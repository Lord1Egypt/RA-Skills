# 点点数据监控功能说明

> **版本**: v6.1  
> **更新时间**: 2026-03-26  
> **状态**: ✅ 完成

---

## 📋 功能概述

自动获取点点数据平台上架/下架榜单数据，支持 12 个平台（11 个安卓渠道 + App Store），自动发送到钉钉群。

---

## ✨ 核心功能

### 1. 支持平台 (12 个)

#### App Store
- **上架榜**: `https://app.diandian.com/rank/line-1-0-0-75-0-3-0`
- **下架榜**: `https://app.diandian.com/rank/line-1-1-0-75-0-3-0`

#### 安卓渠道 (11 个)
| 渠道 | 平台名称 | URL 参数 |
|------|----------|---------|
| 华为 | huawei | line-2-0-0-75-0-3-0 |
| 小米 | xiaomi | line-3-0-0-75-0-3-0 |
| vivo | vivo | line-4-0-0-75-0-3-0 |
| OPPO | oppo | line-5-0-0-75-0-3-0 |
| 魅族 | meizu | line-6-0-0-75-0-3-0 |
| 应用宝 | tencent | line-7-0-0-75-0-3-0 |
| 百度 | baidu | line-8-0-0-75-0-3-0 |
| 360 | qihoo360 | line-9-0-0-75-0-3-0 |
| 荣耀 | honor | line-17-0-0-75-0-3-0 |
| 鸿蒙 | harmony | line-9999-0-0-75-0-3-0 |
| 豌豆荚 | wandoujia | line-10-0-0-75-0-3-0 |

### 2. 智能特性

- ✅ **浏览器后台常开**: 避免重复登录
- ✅ **自动登录**: Cookie 过期自动重新登录
- ✅ **智能检查**: 当天文件已存在则跳过
- ✅ **强制获取**: 支持 `--force` 参数重新获取
- ✅ **文件验证**: 下载后验证文件内容是否匹配
- ✅ **自动重试**: 文件不匹配自动重新下载
- ✅ **钉钉通知**: Markdown 格式 + TOP20 + Excel 附件

### 3. 安全机制

- ✅ 页面标题验证（防止获取错误平台数据）
- ✅ 文件内容验证（确保数据匹配当前渠道）
- ✅ 二次验证机制（不匹配自动重新下载）
- ✅ 自动登录检测（Cookie 过期自动处理）

---

## 🚀 快速开始

### 环境准备

```bash
cd ~/.openclaw/workspace/skills/app-rank-monitor

# 安装依赖
./venv/bin/pip install -r requirements.txt
```

### 配置

1. **点点数据账号**: `config/credentials.yaml`
```yaml
diandian:
  username: your_username
  password: your_password
```

2. **钉钉配置**: `config/dingtalk.yaml`
```yaml
dingtalk:
  client_id: "your_client_id"
  client_secret: "your_client_secret"
  chat_id: "your_chat_id"
  webhook: "your_webhook"
```

### 使用方法

#### 1. 启动浏览器（首次运行）
```bash
./tools/keep_browser_alive.sh
```

#### 2. 获取上架榜单
```bash
# 正常获取（文件存在则跳过）
./venv/bin/python tools/diandian_connect.py --platform <平台名称>

# 强制重新获取
./venv/bin/python tools/diandian_connect.py --platform <平台名称> --force
```

#### 3. 获取下架榜单
```bash
# 获取下架榜单
./venv/bin/python tools/diandian_connect.py --platform <平台名称> --offline

# 强制重新获取下架榜单
./venv/bin/python tools/diandian_connect.py --platform <平台名称> --offline --force
```

#### 4. 支持的平台名称
```bash
# App Store
appstore

# 安卓渠道
huawei       # 华为
xiaomi       # 小米
vivo         # vivo
oppo         # OPPO
meizu        # 魅族
tencent      # 应用宝
baidu        # 百度
qihoo360     # 360
honor        # 荣耀
harmony      # 鸿蒙
wandoujia    # 豌豆荚
```

### 示例

```bash
# 获取 App Store 上架榜单
./venv/bin/python tools/diandian_connect.py --platform appstore

# 获取 App Store 下架榜单
./venv/bin/python tools/diandian_connect.py --platform appstore --offline

# 获取华为上架榜单
./venv/bin/python tools/diandian_connect.py --platform huawei

# 获取小米下架榜单
./venv/bin/python tools/diandian_connect.py --platform xiaomi --offline

# 强制获取 OPPO 上架榜单
./venv/bin/python tools/diandian_connect.py --platform oppo --force
```

---

## 📁 文件结构

```
app-rank-monitor/
├── tools/
│   ├── diandian_connect.py      # 主程序（连接已运行浏览器）
│   ├── diandian_auto_login.py   # 自动登录工具
│   └── keep_browser_alive.sh    # 浏览器后台运行脚本
├── config/
│   ├── diandian.yaml            # Cookie 配置
│   ├── credentials.yaml         # 账号密码配置
│   └── dingtalk.yaml            # 钉钉配置
├── reports/                     # 生成的报告
└── logs/                        # 日志文件
```

---

## 📝 注意事项

1. **Cookie 有效期**: 约 24 小时，过期会自动重新登录
2. **浏览器保持运行**: 首次运行需启动浏览器后台
3. **文件命名**: 自动生成，格式：`{platform}_{type}_apps_{date}.xlsx`
4. **钉钉通知**: 需要企业应用权限

---

## 🔧 故障排查

### Cookie 过期
```bash
# 自动处理，无需手动操作
# 检测到未登录会自动使用 credentials.yaml 中的账号密码登录
```

### 浏览器未运行
```bash
# 启动浏览器
./tools/keep_browser_alive.sh
```

### 数据不匹配
```bash
# 强制重新获取
./venv/bin/python tools/diandian_connect.py --platform huawei --force
```

### 文件验证失败
- 检查 Excel 文件列名是否包含平台关键字
- App Store 列名：`App Store_中国区_上架监控_日期`
- 安卓渠道列名：`{平台名}_上架监控_日期`

---

## 📊 输出示例

### 钉钉消息
```markdown
📊 点点数据 - 上架监控 (2026-03-26)

【上架监控】共 100 个应用

TOP 20:
1. 应用 A - 工具
2. 应用 B - 游戏
...

完整数据请查看附件 📎
```

### Excel 文件
- **文件名**: `huawei_new_apps_20260326.xlsx`
- **内容**: 排名、应用 ID、应用名称、开发者、上架类型、当前状态、价格、分类、上架监控时间

---

## 📈 更新日志

### v6.1 (2026-03-26) - 添加 App Store 渠道
- ✅ 添加 App Store 平台映射 (appstore, appstore_offline)
- ✅ 优化 Excel 验证逻辑，检查列名内容
- ✅ 支持下架榜单专用 URL 映射
- ✅ 自动登录检测功能
- ✅ Cookie 自动保存功能

### v6.0 (2026-03-26) - 自动登录检测
- ✅ 添加自动登录检测功能
- ✅ Cookie 过期自动重新登录
- ✅ 登录成功后自动保存 Cookie
- ✅ 解决 Cookie 过期导致的数据获取失败问题

---

**更新时间**: 2026-03-26  
**版本**: v6.1  
**维护者**: 钳钳 🦞
