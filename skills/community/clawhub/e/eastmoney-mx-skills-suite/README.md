# mx-skills-suite - 东方财富妙想金融技能套件

> 基于 [东方财富妙想平台 API](https://mkapi2.dfcfs.com/finskillshub) 构建的一站式金融技能套件，为 AI 助手提供专业的金融数据查询、资讯搜索、智能选股、自选股管理和模拟交易能力。

## 功能概览

| 技能 | 功能 | 典型用法 |
|------|------|---------|
| **eastmoney_fin_data** | 金融数据查询 | "查一下贵州茅台的最新价"、"看看东方财富近3年营收" |
| **eastmoney_fin_search** | 金融资讯搜索 | "搜一下格力电器的最新研报"、"新能源板块有什么新闻" |
| **mx_select_stock** | 智能选股 | "帮我选市盈率低于20的股票"、"今天涨停的股票有哪些" |
| **mx_self_select** | 自选股管理 | "查看我的自选股"、"把宁德时代加到自选" |
| **eastmoney_stock_simulator** | 模拟交易 | "买入100股贵州茅台"、"查询我的模拟持仓" |

## 快速开始

### 1. 获取 API Key

首次使用需要注册东方财富妙想平台并获取 API Key：

**点击下方链接注册并领取 API Key：**

👉 **[https://marketing.dfcfs.com/views/mktemplate/route1?activityId=738&appfenxiang=1](https://marketing.dfcfs.com/views/mktemplate/route1?activityId=738&appfenxiang=1)**

流程：
1. 打开链接，下载安装**东方财富 APP**
2. 注册/登录东方财富通行证
3. 在首页搜索 **Skill**，领取 **API KEY**

### 2. 配置环境变量

获取到 API Key 后，设置环境变量 `MX_APIKEY`：

```bash
# Linux / macOS
export MX_APIKEY=你的API_KEY

# Windows PowerShell
$env:MX_APIKEY = "你的API_KEY"

# Windows CMD
set MX_APIKEY=你的API_KEY
```

> 建议将环境变量写入 shell 配置文件（`~/.bashrc`、`~/.zshrc` 等）或系统环境变量中，避免每次重启后需要重新设置。

### 3. 安装依赖（使用脚本时需要）

```bash
pip install -r scripts/requirements.txt
```

## 安装到 WorkBuddy

将 `mx-skills-suite` 文件夹复制到以下路径：

```
~/.workbuddy/skills/mx-skills-suite/
```

完整路径示例：
- Windows: `C:\Users\你的用户名\.workbuddy\skills\mx-skills-suite\`
- macOS/Linux: `~/.workbuddy/skills/mx-skills-suite/`

## 目录结构

```
mx-skills-suite/
├── SKILL.md                          # 主技能描述文件
├── README.md                         # 本文档
├── scripts/                          # 可执行脚本
│   ├── mx_data.py                    # 金融数据查询脚本
│   ├── mx_search.py                  # 资讯搜索脚本
│   ├── mx_select_stock.py            # 智能选股脚本
│   ├── mx_self_select.py             # 自选股管理脚本
│   ├── mx_stock_simulator.py         # 模拟交易脚本
│   └── requirements.txt              # Python 依赖
└── references/                       # 子技能详细参考文档
    ├── mx-data.md                    # 金融数据查询 API 文档
    ├── mx-search.md                  # 资讯搜索 API 文档
    ├── mx-select-stock.md            # 智能选股 API 文档
    ├── mx-selfselect.md              # 自选股管理 API 文档
    └── mx-stock-simulator.md         # 模拟交易 API 文档
```

## 使用脚本（独立于 AI 助手）

每个子技能都提供了独立的 Python 脚本，可以直接命令行使用：

### 金融数据查询

```bash
python scripts/mx_data.py "东方财富最新价"
python scripts/mx_data.py "贵州茅台最近3年每日收盘价"
```

### 资讯搜索

```bash
python scripts/mx_search.py "格力电器最新研报"
python scripts/mx_search.py "商业航天板块近期新闻"
```

### 智能选股

```bash
python scripts/mx_select_stock.py "今天A股价格大于10元"
python scripts/mx_select_stock.py "市盈率小于20且涨幅超过2%的股票"
```

### 自选股管理

```bash
python scripts/mx_self_select.py query                    # 查询自选股
python scripts/mx_self_select.py add "贵州茅台"           # 添加自选
python scripts/mx_self_select.py delete "贵州茅台"         # 删除自选
python scripts/mx_self_select.py "把宁德时代加入自选"      # 自然语言
```

### 模拟交易

```bash
python scripts/mx_stock_simulator.py "查询持仓"
python scripts/mx_stock_simulator.py "查询资金"
python scripts/mx_stock_simulator.py "买入600519 100股 价格1780"
python scripts/mx_stock_simulator.py "卖出600519 100股"
python scripts/mx_stock_simulator.py "撤销所有订单"
```

## API 信息

| 项目 | 值 |
|------|---|
| API 域名 | `https://mkapi2.dfcfs.com/finskillshub` |
| 认证方式 | HTTP Header `apikey: {MX_APIKEY}` |
| 请求方法 | POST |
| Content-Type | application/json |

## 常见错误

| 错误码 | 含义 | 解决方案 |
|-------|------|---------|
| 113 | 调用次数达上限 | 等待次日或更新 API Key |
| 114 | API 密钥失效 | 重新到妙想平台获取 Key |
| 115 | 未携带密钥 | 检查 `MX_APIKEY` 环境变量 |
| 116 | 密钥不存在 | 检查 Key 是否正确复制 |
| 404 | 未绑定模拟组合 | 先到[妙想平台](https://dl.dfcfs.com/m/itc4)创建模拟账户 |

## 安全说明

- 所有数据仅发送至东方财富官方域名 `mkapi2.dfcfs.com`
- API Key 通过环境变量传递，不会在任何文件中明文存储
- 模拟交易功能仅用于学习练手，不涉及真实资金

## 致谢

本套件基于东方财富妙想团队提供的原始技能包重新整理打包，去除了 API Key 信息，优化了文档结构和安装流程。

## 许可

本技能套件仅供学习和个人使用。东方财富妙想 API 的使用需遵守东方财富平台的相关服务条款。
