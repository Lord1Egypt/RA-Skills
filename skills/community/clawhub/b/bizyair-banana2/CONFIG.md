# BizyAir Banana 2 配置指南

## ⚙️ API Key 配置

### 方式 1：.env 文件（推荐）

在技能目录创建 `.env` 文件：
```bash
BIZYAIR_API_KEY=你的_API_Key
```

### 方式 2：环境变量

```bash
export BIZYAIR_API_KEY="你的_API_Key"
```

---

## 📁 配置文件位置

优先级从高到低：

1. `技能目录/.env` ⭐ 推荐
2. `~/.config/bizyair-banana2/.env`
3. `~/.bizyair-banana2/.env`

---

## ✅ 验证配置

```bash
python3 scripts/bizyair_gen.py --help
```

显示帮助信息即配置成功。

---

## 🔧 可选配置

编辑 `.env` 文件：
```bash
# API Key（必需）
BIZYAIR_API_KEY=你的_API_Key

# 基础 URL（可选）
# BIZYAIR_BASE_URL=https://api.bizyair.cn
```

---

## ❓ 故障排查

### 提示"未配置 BIZYAIR_API_KEY"

**检查：**
1. `.env` 文件是否存在
2. `.env` 文件格式：`BIZYAIR_API_KEY=xxx`（无空格）
3. API Key 是否正确

### 生成失败

**检查：**
1. API Key 是否有效
2. 余额是否充足
3. 提示词是否合规

---

*配置指南 | 2026-04-03*
