# FastMoss 选品报告技能

_自动生成 TikTok 热推榜数据报告_

## 触发词

- `生成选品报告`
- `生成FastMoss报告`
- `选品报告`

## 触发条件

当用户发送包含触发词的消息时，执行完整报告生成流程。

## 环境变量

以下变量需要在 `~/.openclaw/.env` 或系统环境中配置：

```bash
# FastMoss 账号（每5天更换）
FASTMOSS_ACCOUNT=""
FASTMOSS_PASSWORD=""

# FastMoss 品类配置
# 品类ID (l1_cid):
#   8  = 时尚配件
#   6  = 美妆个护
#   3  = 女装与女士内衣
#   18 = 保健
#   14 = 运动与户外
#   16 = 手机与数码
FASTMOSS_CATEGORY=8

# 地区（默认：美国）
FASTMOSS_REGION=US

# Vercel 部署目录
VERCEL_DEPLOY_DIR="~/.openclaw/workspace/fastmoss-daily"

# 飞书群ID（管理办公室群）
FEISHU_GROUP_ID=""
```

## 执行流程

### 1. 数据获取
- 使用 browser 工具打开 FastMoss 热推榜
- 地区：使用环境变量 `FASTMOSS_REGION`（默认 US）
- 品类：使用环境变量 `FASTMOSS_CATEGORY`（默认 8=时尚配件）
- 分别获取日榜和周榜 Top 10 数据

### 2. 登录处理
如果需要登录：
- 使用环境变量 `FASTMOSS_ACCOUNT` 和 `FASTMOSS_PASSWORD`
- 账号格式：纯数字（如 11668461）
- 密码：aaa060（每5天更换，更换日期记录在 memory 中）

### 3. 数据记录
- 日榜：当天日期（如 2026-03-05）
- 周榜：当前周数（如 2026年第9周）
- 记录字段：排名、商品名称、售价、店铺、店铺销量、佣金、销量

### 4. 报告生成
生成 HTML 报告，包含：
- 玻璃拟态 UI 风格（参考现有 fastmoss-2026-03-06 样式）
- 莫兰迪色系
- 响应式布局
- 商品链接和店铺链接（中英对照）
- 数据洞察与建议

### 5. Vercel 部署
- 部署目录格式：`fastmoss-YYYY-MM-DD`
- 部署后获取 URL

### 6. 消息推送
- 发送报告链接到用户私信
- 如果 `FEISHU_GROUP_ID` 已配置，同时发送到群

## 输出格式

报告包含：
1. 数据概览（4个统计卡片）
2. 日榜 Top 10 表格
3. 周榜 Top 10 表格
4. 数据洞察
5. 选品建议
6. 风险提示

## 错误处理

- 登录失败：提示检查环境变量
- 页面加载失败：重试3次后退出
- 部署失败：保留本地文件并通知用户

## 使用示例

```
用户：生成选品报告
助手：📊 正在获取 FastMoss 数据...
      ✅ 报告已生成！
      🔗 https://fastmoss-2026-03-06.vercel.app
```
