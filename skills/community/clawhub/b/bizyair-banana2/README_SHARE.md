# BizyAir Banana 2 分享包

## 📦 分享包内容

- ✅ 完整技能文件
- ✅ 使用文档
- ✅ 配置模板
- ❌ 不含 API Key
- ❌ 不含参考图

---

## 🚀 安装步骤

### 1. 解压

```bash
cd ~/.openclaw/workspace/skills/
tar -xzf bizyair-banana2-share.tar.gz
```

### 2. 配置 API Key

```bash
cd bizyair-banana2/
cp .env.example .env
# 编辑 .env 填入你的 API Key
```

### 3. 测试

```bash
python3 scripts/bizyair_gen.py --help
```

---

## 💡 快速使用

```bash
# 文生图
python3 scripts/bizyair_gen.py \
  --prompt "一只可爱的猫咪" \
  --image cat.png

# 参考图生图
python3 scripts/bizyair_gen.py \
  --prompt "变成卡通风格" \
  --image output.png \
  --ref input.png
```

---

## 📋 配置说明

**API Key 配置位置（优先级从高到低）：**

1. `技能目录/.env` ⭐ 推荐
2. `~/.config/bizyair-banana2/.env`
3. `~/.bizyair-banana2/.env`

---

## 💰 费用

- 1K 分辨率：5 分钱/张
- 2K/4K 分辨率：8 分钱/张
- 按量付费，生成成功才扣费

---

## 🔗 获取 API Key

访问 https://www.bizyair.cn 注册并获取

---

*分享包版本：1.0.0 | 2026-04-03*
