# BizyAir Banana 2 图像生成技能

使用 BizyAir API 和 Nano Banana 2 模型生成高质量图片。支持参考图、表情包生成。按量付费，无需本地 GPU。

---

## 🚀 快速开始

### 1. 获取 API Key

访问 https://www.bizyair.cn 注册账号并获取 API Key

### 2. 配置 API Key

**方式 A：创建.env 文件（推荐）**

在技能目录创建 `.env` 文件：
```bash
BIZYAIR_API_KEY=你的_API_Key
```

**方式 B：环境变量**
```bash
export BIZYAIR_API_KEY="你的_API_Key"
```

### 3. 开始生成

```bash
python3 scripts/bizyair_gen.py \
  --prompt "一只可爱的猫咪" \
  --image cat.png
```

---

## 💡 使用示例

### 文生图

```bash
python3 scripts/bizyair_gen.py \
  --prompt "一只可爱的猫咪" \
  --image cat.png \
  --ar 1:1
```

### 参考图生图

```bash
python3 scripts/bizyair_gen.py \
  --prompt "变成卡通风格" \
  --image output.png \
  --ref input.png
```

### 表情包生成

```bash
python3 scripts/bizyair_gen.py \
  --prompt "搞笑表情" \
  --image emoji.png \
  --ref portrait.jpg \
  --web-app-id 47091
```

---

## 📋 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-p, --prompt` | 提示词（必需） | - |
| `-i, --image` | 输出路径（必需） | - |
| `-r, --ref` | 参考图（可多个） | - |
| `--ar` | 宽高比 | `9:16` |
| `--resolution` | 分辨率 | `1k` |
| `--web-app-id` | Web App ID | `47091` |
| `--timeout` | 超时时间 | `120` |

---

## 💰 费用说明

- **1K 分辨率**：5 分钱/张
- **2K/4K 分辨率**：8 分钱/张
- **参考图**：同分辨率价格
- **按量付费**：生成成功才扣费

---

## ❓ 常见问题

### Q: API Key 在哪里配置？

**A:** 在技能目录创建 `.env` 文件：
```bash
BIZYAIR_API_KEY=你的_API_Key
```

### Q: 支持哪些宽高比？

**A:** `1:1`, `16:9`, `9:16`, `3:4`, `4:3`, `21:9` 等

### Q: 生成失败怎么办？

**A:** 检查：
1. API Key 是否正确
2. 余额是否充足
3. 提示词是否合规

---

## 🔗 相关链接

- **官网：** https://www.bizyair.cn
- **文档：** https://docs.bizyair.cn
- **价格：** https://docs.bizyair.cn/pricing/introduce.html

---

*版本：1.0.0 | 更新时间：2026-04-03*
