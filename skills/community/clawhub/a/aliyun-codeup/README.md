# 阿里云云效 Codeup 技能

## 📦 安装

技能已位于：`~/.openclaw/workspace/skills/aliyun-codeup/`

## 🔑 配置

在 `~/.zshrc` 中添加：

```bash
export YUNXIAO_PERSONAL_TOKEN="pt-xxx"  # 你的云效个人令牌
```

## 🚀 使用

### 查询分支

```bash
python3 skills/aliyun-codeup/codeup_cli.py <项目 URL>
```

**示例：**
```bash
python3 skills/aliyun-codeup/codeup_cli.py "https://codeup.aliyun.com/flashexpress/ard/be/tools/data-admin-api"
```

### 查询提交记录

```bash
python3 skills/aliyun-codeup/codeup_cli.py <项目 URL> commits
```

### 查询仓库统计

```bash
python3 skills/aliyun-codeup/codeup_cli.py <项目 URL> stats
```

## 📋 输出示例

```
📊 项目：data-admin-api
📊 分支总数：75

【主分支】
  ✓ master

【功能分支】(48)
  🔧 feature/common.20251211
  🔧 feature/common.20251105
  ...

【热修复分支】(18)
  🐛 hotfix/myj.250723
  ...
```

## 🔒 安全提示

- ✅ 令牌存储在环境变量
- ✅ 临时克隆自动清理
- ❌ 不要将令牌写入代码或文档

---

**版本：** 1.0.0  
**创建时间：** 2026-03-06
