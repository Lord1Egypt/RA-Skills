# 广告账户管理 Skill

通过浏览器自动化（Cookie登录），实现多平台广告账户的统一管理。

## 功能特性

1. **扫码登录**：支持广点通（广告主/服务商）和巨量引擎的扫码登录
2. **Cookie保存**：登录后自动保存Cookie到本地，下次可直接使用
3. **一键登录**：使用已存储的Cookie自动登录对应广告后台
4. **账户状态总览**：查看所有账户的余额、消耗、预算等信息，异常账户标红提醒

## 安装依赖

```bash
pip install -r requirements.txt
playwright install chromium
```

## 使用方法

运行交互式命令行界面：

```bash
python main.py
```

## 目录结构

```
ad_accounts/
├── __init__.py          # 模块初始化
├── ad_manager.py        # 账户管理核心模块
├── browser_helper.py    # 浏览器自动化辅助模块
├── main.py              # 主入口，交互式命令行界面
├── requirements.txt     # 依赖包列表
├── README.md            # 使用说明
└── data/                # 数据存储目录（自动创建）
    └── accounts.json    # 账户数据文件
```

## 支持的平台

- **广点通**：广告主后台 (`https://e.qq.com/ads`)、服务商后台 (`https://e.qq.com/agency`)
- **巨量引擎**：`https://ad.oceanengine.com`
