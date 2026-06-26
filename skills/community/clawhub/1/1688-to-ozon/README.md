# 1688-to-OZON 使用指南

快速开始使用 1688-to-OZON 技能。

## 🚀 快速开始

### 1. 技能位置

技能已安装在：`~/.openclaw/skills/1688-to-ozon/`

**注意**：技能目录是共享的，所有 agent 都可以使用。项目数据输出到各自 workspace 的 `projects/` 目录。

### 2. 配置 OZON API

复制配置模板并填写你的 API 密钥：

```bash
cd ~/.openclaw/skills/1688-to-ozon
cp config/user.json.example config/user.json
# 编辑 config/user.json，填入你的 clientId 和 apiKey
```

**配置说明**：
- `clientId`: OZON Seller API 客户端 ID
- `apiKey`: OZON Seller API 密钥
- `warehouseId`: 仓库 ID（可选，默认使用 OZON 默认仓库）

### 3. 执行上架

**通过 OpenClaw 触发**（推荐）：
```
https://detail.1688.com/offer/XXX.html op -w 100g -p 30
```

**或直接运行脚本**：
```bash
# 基本用法
node ~/.openclaw/skills/1688-to-ozon/scripts/index.js "https://detail.1688.com/offer/XXX.html" -w 100g -p 30

# 完整参数
node scripts/index.js "URL" -w 100g -p 30 -s 10 --profit 0.25 --category toy_set
```

**注意**：项目数据输出到当前 agent 的 workspace 目录：
- Developer: `~/.openclaw/workspace-developer/projects/`
- Ops Specialist: `~/.openclaw/workspace-ops-specialist/projects/`

## 📋 执行步骤

执行过程会分 4 步，每步完成后暂停等待确认：

1. **Step 1: 1688 商品抓取**（约 1-2 分钟）
   - 下载商品图片
   - 提取商品信息
   - OCR 识别
   - 生成文案

2. **Step 2: 图片翻译**（约 2-5 分钟）
   - 翻译图片文字
   - 上传图床

3. **Step 3: 定价计算**（约 10-30 秒）
   - 计算物流费用
   - 计算售价

4. **Step 4: OZON 上传**（约 1-3 分钟）
   - 字段映射
   - API 上传
   - 设置库存

## 🧪 Debug 模式

使用 Mock 数据测试（不消耗 API）：

```bash
node scripts/index.js "URL" -w 100g -p 30 --debug
```

## 📊 查看进度

```bash
# 查看进度文件
cat projects/progress.json | jq .

# 查看日志
ls -la projects/
```

## ❓ 常见问题

### Q: 如何修改默认利润率？

A: 编辑 `config/user.json`：
```json
{
  "pricing": {
    "defaultProfit": 0.25
  }
}
```

### Q: 如何跳过某一步？

A: 使用 `--step` 参数：
```bash
# 从 Step 2 开始
node scripts/index.js "URL" -w 100g -p 30 --step 2
```

### Q: 上传失败怎么办？

A: 检查：
1. OZON API 密钥是否正确
2. 商品类目是否正确
3. 图片是否都上传成功
4. 查看详细错误日志

---

**更多文档**: `SKILL.md`
