---
name: feishu-accounting
description: 飞书多维表格记账系统完整技能包。包含两步：1）运行 feishu-accounting-setup 引导用户完成飞书应用创建、多维表格搭建、凭证获取；2）使用 record_bill.py 进行日常记账（支持本地存储 + 飞书多维表格同步）。**同步使用永久有效的 Tenant Token。单表模式：所有记录写入明细表，通过「类型」字段区分支出和收入。**
version: 1.3.4
author: Naeem
homepage: https://github.com/NaeemTC/feishu-accounting-skill
tags: [feishu, bitable, accounting, setup, permissions]
---

# 飞书多维表格记账系统

## 概述

本技能是完整的飞书记账解决方案，分两个阶段：

| 阶段 | 触发条件 | 做什么 |
|------|----------|--------|
| **Setup** | 用户请求配置记账系统 | 引导创建飞书应用 → 一键搭建多维表格 → 输出凭证 |
| **Usage** | 用户记账（说金额/上传图片/查账单） | 解析记账输入 → 写本地 bills/ → 同步飞书明细表（单表模式） |

---

## 第一阶段：Setup（首次配置）

### 触发词

用户说以下内容时执行 Setup：

- "配置飞书记账"
- "帮我搭建记账系统"
- "飞书记账怎么配置"
- "setup feishu accounting"
- "我想用飞书记账"

### Step 1：引导用户创建飞书自建应用

**把以下内容发给用户：**

> **请在飞书开放平台创建一个自建应用：**
>
> 1. 打开 https://open.feishu.cn/app
> 2. 点击「创建企业自建应用」
> 3. 填写应用名称（如「记账助手」）和描述
> 4. 创建完成后，在「凭证与基础信息」页面复制 **App ID** 和 **App Secret**
>
> 复制好后发给我。

等待用户提供 App ID 和 App Secret。

### Step 2：一键开通权限（Agent 自动生成授权链接，用户只需点击确认）

**AI 执行** `apply_permissions.py`（自动获取 Tenant Token、生成一键授权链接）：

```bash
cd /path/to/feishu-accounting/
python3 scripts/apply_permissions.py \
  --app-id "cli_用户的AppID" \
  --app-secret "用户的AppSecret"
```

脚本输出一个 **一键授权链接**，AI 直接把脚本输出的完整链接原样发给用户

> ⚠️ **AI 注意**：不要自己拼链接！必须运行 `apply_permissions.py`，取 stdout 里的链接，原样发给用户。链接里必须包含以下全部 19 个权限，一个不能少：
>
> `base:app:read,base:app:update,base:app:create,base:table:read,base:table:create,base:table:update,base:table:delete,base:field:read,base:field:create,base:field:update,base:field:delete,base:record:read,base:record:create,base:record:update,base:record:delete,base:view:read,base:view:write_only,bitable:app:readonly,bitable:app`
>
> 用户点击链接 → 页面列出所有权限 → 全选后点击 **「确认开通权限」** → 完成。

**然后 AI 调用** `scopes/apply` API 提交管理员审批申请。

---

### Step 3：一键搭建多维表格

用户提供 App ID + App Secret 后，运行 `setup_bitable.py`（无需安装任何外部工具，直接调飞书 API）：

```bash
cd /path/to/feishu-accounting/
python3 scripts/setup_bitable.py \
  --app-id "cli_用户的AppID" \
  --app-secret "用户的AppSecret"
```

脚本会自动完成：
1. 获取 Tenant Token（永久有效）
2. 创建多维表格「个人记账本」
3. 创建一张明细表（单表模式，支出和收入共用）
4. 创建所有字段（文本/月份/金额/分类/类型）+ 补充选项（18个分类 + 收支类型选项）

输出 4 个凭证：App ID / App Secret / Base Token / 明细表 Table ID

### Step 4：输出凭证给用户

**AI 必须将以下 4 个凭证填入实际值后发送给用户（App ID / App Secret 来自 Step 1 用户提供的值，Base Token / Table ID 来自 Step 3 脚本输出的）：**

> ✅ 飞书记账配置完成！
>
> 请保存以下 4 个凭证——首次打开手机 App 时需要按顺序输入：
>
> 1. **App ID**：`你的App_ID`
> 2. **App Secret**：`你的App_Secret`
> 3. **Base Token**：`你的Base_Token`
> 4. **明细表 Table ID**：`你的明细表ID`
>
> 输入后 App 就能正常查看你的账单数据了。
>
> 📊 **多维表格链接**：https://bytedance.feishu.cn/base/`你的Base_Token`
> （浏览器打开就能直接看到你建的全量账本数据）

### Step 5：配置凭证（让 record_bill.py 能用）

**AI 执行**，在 skill 目录下创建 `.env` 文件（`record_bill.py` 启动时会自动加载）：

```bash
# 在技能目录创建 .env（record_bill.py 会自动从同目录读取）
cat > /path/to/feishu-accounting/.env << 'EOF'
FEISHU_APP_ID=你的App_ID
FEISHU_APP_SECRET=你的App_Secret
FEISHU_BASE_TOKEN=你的Base_Token
FEISHU_DETAIL_TABLE_ID=你的明细表ID
EOF
```

### Step 6：询问用户是否安装 App（仪表盘）

配置完成后，**询问用户**要不要装 Android 仪表盘 App 来看图表和数据：

> 飞书记账后台已经配好了！要不要装个手机 App 来看图表？
>
> - **📦 下载发布版**（推荐，即装即用）：https://github.com/NaeemTC/feishu-accounting-skill/releases/latest/download/app-release.apk
> - **🔧 从源码构建**：需要 Node.js + Android SDK，克隆仓库后执行 `bash sync.sh`

用户选发布版就直接发下载链接，选自己打就引导构建。

---

## 第二阶段：Usage（日常记账）

### 触发词

- "记账"、"花了X元"、"支出X"
- "收入X元"
- 上传账单图片（无文字说明）
- "查账单"、"本月花了多少"、"月度统计"

### 凭证检查

每次记账前确认环境变量已设置：

```bash
# 检查凭证
echo "FEISHU_BASE_TOKEN=${FEISHU_BASE_TOKEN:-未设置}"
echo "FEISHU_DETAIL_TABLE_ID=${FEISHU_DETAIL_TABLE_ID:-未设置}"
```

**如果未设置**，跳回第一阶段（Setup）流程，重新引导用户获取凭证。

### 记账命令

```bash
# 方式一：直接调用（脚本自动加载同目录 .env）
python3 /path/to/scripts/record_bill.py \
  --amount 23.40 --type expense --category 餐饮 --note "午饭"

# 方式二：环境变量注入（适合临时调用）
FEISHU_BASE_TOKEN=xxx FEISHU_DETAIL_TABLE_ID=xxx \
  python3 /path/to/scripts/record_bill.py \
  --amount 23.40 --type expense --category 餐饮 --note "午饭"
```

**⚠️ Python 版本**：确保本机已安装 `python3`（Python 3.9+ 均可），可通过 `python3 --version` 确认。

### 完整命令参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--amount` | ✅ | 金额（元） |
| `--type` | ✅ | `expense`（支出）或 `income`（收入） |
| `--category` | | 分类，默认「其他」 |
| `--note` | | 备注 |
| `--date` | | 日期 YYYY-MM-DD，默认今天 |
| `--feishu` | | 同步飞书（默认开启） |

> **⚠️ 单表模式**：支出和收入均写入同一张明细表，通过「类型」字段区分。App 端按类型字段分组聚合计算月度收支。

### 查询命令

```bash
# 今日账单
python3 scripts/record_bill.py --list

# 指定日期
python3 scripts/record_bill.py --list --date 2026-05-15

# 月度汇总
python3 scripts/record_bill.py --summary --month 2026-05
```

### 图片记账

用户发送账单图片（无文字）时：
1. 用 vision 模型看图识别金额
2. 直接按识别结果执行记账命令，不需要询问用户确认

### 数据管理（查看 / 删除记录）

**查看记录：**
```bash
# 列出当日账单（含序号，用于定位要删除的记录）
python3 scripts/record_bill.py --list

# 列出指定日期账单
python3 scripts/record_bill.py --list --date 2026-05-22

# 月度汇总
python3 scripts/record_bill.py --summary --month 2026-05
```

`--list` 输出中每条记录有一个 `index` 字段（1起算），用于删除定位。

**删除记录：**
```bash
# 删除指定日期的第 N 条记录（同时从本地文件和飞书明细表移除）
python3 scripts/record_bill.py --delete --date 2026-05-22 --index 2
```

> **注意**：删除操作会同时从本地 `bills/YYYY-MM-DD.md` 和飞书明细表移除记录，**不可撤销**，请先确认 index 序号正确。

### 分类关键词（AI 解析参考）

详见 `references/categories.md` 和 `references/feishu-permissions-api.md`（飞书权限 API 模式），核心规则：

| 类型 | 分类 | 关键词 |
|------|------|--------|
| 支出 | 餐饮 | 早饭/午饭/晚饭/外卖/咖啡/奶茶/餐厅 |
| 支出 | 购物 | 超市/衣服/鞋子/电商/淘宝/京东/日用品 |
| 支出 | 交通 | 打车/地铁/公交/停车/加油/滴滴 |
| 支出 | 娱乐 | 电影/KTV/旅游/游戏氪金/彩票 |
| 支出 | 通讯 | 话费/流量/套餐 |
| 支出 | 医疗 | 医院/药店/挂号/体检 |
| 支出 | 住房 | 房租/水电/物业/宽带 |
| 支出 | 教育 | 学费/课程/书/培训 |
| 支出 | 服饰 | 衣服/鞋子/包包/穿搭/配饰 |
| 支出 | 生活 | 日用/日用品/理发/洗衣/五金 |
| 支出 | 数码 | 手机/数码/充电器/耳机/硬盘 |
| 支出 | 运动 | 健身/运动/游泳/羽毛球/球鞋 |
| 支出 | 宠物 | 宠物/猫粮/狗粮/猫砂/疫苗 |
| 收入 | 工资 | 工资/薪资/月薪 |
| 收入 | 兼职 | 兼职/副业/接单 |
| 收入 | 投资 | 理财/股票/基金/利息 |

**飞书分类映射**：13个支出分类 + 5个收入分类（工资/奖金/兼职/投资/其他），在飞书明细表中均有对应选项，无需映射损耗。

---

## 目录结构

```
feishu-accounting/
├── SKILL.md                   # 本文件
├── scripts/
│   ├── record_bill.py         # 记账核心脚本
│   ├── setup_bitable.py       # 一键搭建多维表格脚本
│   ├── cleanup_bitable.py     # 清空多维表格数据（重置/测试用）
│   └── apply_permissions.py   # 一键权限申请——生成授权链接 + 调 scopes/apply
└── references/
    └── categories.md                # 分类关键词参考
    └── feishu-base-api-pitfalls.md   # base/v3 API 踩坑记录（分页/字段/格式）
    └── feishu-permissions-api.md     # 飞书权限一键授权 API 模式
```

## 环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `FEISHU_APP_ID` | 飞书应用 App ID（必填） | `cli_xxxxxxxxxxxxxxxx` |
| `FEISHU_APP_SECRET` | 飞书应用 App Secret（必填） | `xxxxxxxxxxxxxxxxxx` |
| `FEISHU_BASE_TOKEN` | 多维表格 Base Token | `your_base_token_here` |
| `FEISHU_DETAIL_TABLE_ID` | 明细表 ID（单表，含类型字段区分收支） | `tblxxxxxxxxxxxxxxxx` |

> **无需 User Access Token**：record_bill.py 使用永久有效的 Tenant Token（自动从 App ID + Secret 获取），不再有 7 天过期问题。


