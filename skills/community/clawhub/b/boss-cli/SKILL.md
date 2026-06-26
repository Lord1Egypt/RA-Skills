---
name: boss-cli
description: BOSS直聘 CLI 工具，支持职位搜索、求职申请管理、聊天、发送招呼等功能。通过逆向 BOSS直聘 API 实现，支持多城市、多筛选条件。当用户需要搜索 BOSS直聘 上的职位、查看公司信息、管理求职申请、联系 HR 时触发。
---

# BOSS直聘 CLI (boss-cli)

## 安装

```bash
pip install kabi-boss-cli
# 或
uv tool install kabi-boss-cli
```

## 认证

```bash
# 自动检测浏览器 Cookie（推荐）
boss login

# 指定浏览器
boss login --cookie-source chrome

# QR 码登录
boss login --qrcode
```

## 核心命令

### 搜索职位

```bash
# 基础搜索
boss search "Python" -c 北京

# 按薪资筛选
boss search "后端" --salary 20-40K

# 按经验/学历/行业/公司规模筛选
boss search "AI" --exp 3-5 --degree 本科 --industry 人工智能 --scale 1000-9999

# 分页
boss search "产品经理" -c 上海 -p 2
```

### 查看与管理

```bash
# 展示上次搜索结果（简略索引）
boss show 3

# 查看完整详情
boss detail <securityId>

# 导出结果
boss export "Python" -n 50 -o jobs.csv
boss export "Python" --format json -o jobs.json
```

### 求职助手

```bash
# 查看推荐职位
boss recommend

# 查看已投递的职位
boss applied

# 查看面试邀请
boss interviews

# 查看浏览历史
boss history

# 查看个人中心
boss me --json
```

### 联系 HR

```bash
# 发送招呼
boss greet <securityId>

# 批量招呼（搜索结果前10人）
boss batch-greet "Python" -n 10

# 预览（不实际发送）
boss batch-greet "Python" --dry-run
```

### 工具

```bash
# 查看支持的城市列表
boss cities

# 查看版本
boss -v

# 调试模式（显示请求详情）
boss -v search "Python"
```

## JSON 输出

所有命令支持 `--json` 参数，返回结构化 JSON：

```json
{
  "ok": true,
  "schema_version": "1",
  "data": { ... }
}
```

## 故障排除

- **认证失败**: 运行 `boss logout && boss login` 重新登录
- **搜索无结果**: 检查城市过滤条件，部分关键词是城市专属的，用 `boss cities` 确认支持的城市
- **rate limit (code=9)**: 自动退避等待，重试即可
