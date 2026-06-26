# 🚀 快速开始指南

## 1. 安装

```bash
# 方式1: 通过ClawHub安装
npx clawhub@latest install feishu-bitable-plus

# 方式2: 手动安装
git clone https://github.com/openclaw/feishu-bitable-plus.git
cd feishu-bitable-plus
npm install
npm link
```

## 2. 配置飞书应用

### 2.1 创建飞书应用
1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 申请权限：
   - `bitable:app` - 读取多维表格
   - `bitable:record` - 操作记录
   - `bitable:table` - 操作表格
4. 发布应用版本

### 2.2 配置凭证
```bash
fbt config
# 输入 App ID 和 App Secret
```

### 2.3 获取App Token
1. 打开你的多维表格
2. 从URL中复制 `app_token`：
   ```
   https://example.feishu.cn/base/<app_token>?table=<table_id>
   ```

## 3. 基本使用

### 列出所有表格
```bash
fbt tables --app <your-app-token>
```

### 列出记录
```bash
fbt records --app <your-app-token> --table <table-id>
```

### 自然语言查询
```bash
fbt query "列出客户表的所有记录"
fbt query "查找订单表中状态为已完成的记录"
```

### 交互模式
```bash
fbt interactive
```

## 4. 示例命令

```bash
# 创建记录
fbt create --app <token> --table <id> --data '{"客户名":"张三","金额":1000}'

# 更新记录
fbt update --app <token> --table <id> --record <record-id> --data '{"状态":"已完成"}'

# 删除记录
fbt delete --app <token> --table <id> --record <record-id>

# 批量导入
fbt import --app <token> --table <id> --file data.json

# 导出记录
fbt export --app <token> --table <id> --file backup.json
```

## 5. 获取帮助

```bash
# 查看所有命令
fbt --help

# 查看具体命令帮助
fbt query --help
fbt create --help
```

## 6. 常见问题

### Q: 提示"未配置飞书凭证"
A: 运行 `fbt config` 配置App ID和App Secret

### Q: 提示"权限不足"
A: 检查飞书应用是否申请了必要的权限，并确认已将应用添加到多维表格

### Q: 自然语言查询识别不准确
A: 当前版本使用规则匹配，建议使用更简洁明确的表达。如：
- ✅ "列出客户表的所有记录"
- ❌ "能不能帮我看一下客户表里面有什么数据"

## 7. 反馈与支持

- 📧 邮箱: support@openclaw.ai
- 🐛 Issue: https://github.com/openclaw/feishu-bitable-plus/issues

---

**祝您使用愉快！** 🎉
