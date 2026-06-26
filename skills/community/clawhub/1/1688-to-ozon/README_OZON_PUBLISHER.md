# OZON 全自动上架流程 - 完整文档

**完成日期**: 2026-03-29  
**开发周期**: 1 个月  
**状态**: ✅ 生产就绪

---

## 📋 流程概览

```
1688 商品链接
    ↓
1688-tt (抓取产品信息 + 图片 + OCR + 文案生成)
    ↓
ozon-image-translator (图片翻译 + 图床上传)
    ↓
ozon-pricer (定价计算)
    ↓
ozon-publisher (字段映射 + OZON 上传)
    ↓
✅ OZON 商品上架成功
```

---

## 💰 货币显示规范


---

## 💰 货币显示规范

**所有价格输出遵循统一格式**（2026-04-01 起）：

| 主货币 | 显示格式 | 示例 |
|--------|---------|------|
| **卢布 (RUB)** | `X₽ (¥Y)` | `193.96₽ (¥16.16)` |
| **人民币 (CNY)** | `¥X (Y₽)` | `¥100.00 (1200₽)` |

**汇率配置**: `1 CNY = 12.0 RUB`（固定汇率）

**详细说明**: 参见 `~/.openclaw/skills/ozon-system/CURRENCY_STANDARD.md`

**示例输出**:
```
✓ 符合：3966620224 - 原价:193.96₽ (¥16.16) → 促销价:116.38₽ (¥9.70)
```

---


## 🛠️ 技能列表

| 技能 | 触发词 | 功能 | 输出目录 |
|------|--------|------|----------|
| **1688-tt** | `tt` | 1688 商品抓取 + OCR + 俄语文案生成 | `projects/1688-tt/` |
| **ozon-image-translator** | `oit` | 图片翻译 + ImgBB 图床上传 | `projects/ozon-image-translator/` |
| **ozon-pricer** | `ope` | OZON 售价计算器 | `projects/ozon-pricer/` |
| **ozon-publisher** | `op` | 完整上架流程控制器 | `projects/ozon-publisher/` |

---

## 🚀 使用方法

### 方式一：完整流程（推荐）

```bash
# 触发词：URL op -w 重量 -p 采购价
https://detail.1688.com/offer/XXX.html op -w 650g -p 30
```

**参数说明**：
- `-w, --weight`: 商品重量（支持 `650g` 或 `0.65kg` 格式）**（必需）**
- `-p, --purchase-price`: 采购价（元）**（必需）**
- `-s, --shipping`: 运费（元，默认 0）
- `--debug`: Debug 模式（使用 Mock 数据，不消耗 API）

**示例**：
```bash
https://detail.1688.com/offer/960468314331.html op -w 650g -p 30
```

### 方式二：分步执行

```bash
# Step 1: 1688 抓取
https://detail.1688.com/offer/XXX.html tt

# Step 2: 图片翻译
oit --source-dir "projects/1688-tt/images" --output-dir "projects/ozon-image-translator"

# Step 3: 定价计算
ope -w 650g -p 30

# Step 4: OZON 上传
cd ~/.openclaw/skills/ozon-publisher && node scripts/upload.js
```

---

## 📂 目录规范

### 固定输出目录

```
~/.openclaw/workspace-developer/projects/
├── 1688-tt/                    # 1688-tt 输出
│   ├── product_info.md         # 产品信息
│   ├── ocr_result.md           # OCR 识别结果
│   ├── copy_writing.md         # 中俄双语文案
│   ├── image_classification.md # 图片分类
│   ├── execution_report.md     # 执行报告
│   └── images/                 # 原始图片（main_XX.jpg, detail_XX.jpg）
│
├── ozon-image-translator/      # 图片翻译输出
│   ├── images/                 # 翻译后图片（main_XX_ru.jpg, detail_XX_ru.jpg）
│   └── images.json             # ImgBB 图床 URL
│
├── ozon-pricer/                # 定价计算输出
│   └── pricing.json            # 价格计算结果
│
└── ozon-publisher/             # OZON 上传输出
    ├── input/                  # 输入数据（自动复制）
    │   ├── 1688-tt/
    │   ├── ozon-image-translator/
    │   └── ozon-pricer/
    ├── mapping_result.json     # 字段映射结果
    ├── upload-request.json     # OZON API 请求数据
    ├── upload_result.md        # 上传结果
    └── progress.json           # 实时进度
```

### 目录清理规则

- ✅ 每次执行前自动清空输出目录
- ✅ Debug 模式和正常模式都清理
- ✅ 确保目录状态一致，避免旧文件干扰

---

## ⚙️ 配置说明

### ozon-publisher/config/ozon.json

```json
{
  "client_id": "2129141",
  "api_key": "YOUR_API_KEY",
  "warehouse_id": "1020002303736000",
  "default_stock": 500,
  "default_discount": 50
}
```

### 默认尺寸

所有商品统一使用固定尺寸（除非手动调整）：
- **长度**: 20cm
- **宽度**: 10cm
- **高度**: 15cm

### 图片限制

- **最多 15 张**: 主图 5 张 + 详情图 10 张
- **格式**: JPG/PNG
- **图床**: ImgBB（自动上传）

---

## 📊 OZON API 关键点

### 图片上传格式

```json
{
  "primary_image": "https://catbox.moe/main_01.jpg",
  "images": [
    "https://catbox.moe/main_01.jpg",
    "https://catbox.moe/main_02.jpg",
    ...
  ]
}
```

**注意**：
- `primary_image`: 第 1 张图（主图）
- `images`: 所有图片数组（最多 15 张）
- 不需要 `rich_content` 字段（暂时移除）

### 属性格式

```json
{
  "attributes": [
    {
      "id": 4389,
      "complex_id": 0,
      "values": [{
        "dictionary_value_id": 90296,
        "value": "Китай"
      }]
    }
  ]
}
```

**关键**：
- `dictionary_value_id`: 字典值 ID（必须从 OZON API 动态查询）
- `value`: 俄文值
- `complex_id`: 固定为 0

### 物流尺寸

```json
{
  "weight": 650,
  "weight_unit": "g",
  "length": 20,
  "width": 10,
  "height": 15,
  "dimension_unit": "cm"
}
```

---

## 🔧 故障排查

### 1. 图片上传失败

**症状**: OZON 后台图片显示为 null

**原因**: 图床 URL 不可访问或格式错误

**解决**:
1. 检查 `images.json` 中的 URL 是否可访问
2. 确认 URL 是 HTTPS 格式
3. 重新执行图片翻译步骤

### 2. 属性警告

**症状**: OZON 后台显示属性错误

**原因**: `value_id` 格式错误（应为 `dictionary_value_id`）

**解决**:
1. 确认 `map.js` 使用 `dictionary_value_id + value` 格式
2. 确认 `complex_id: 0` 已添加
3. 重新执行上传

### 3. 物流尺寸错误

**症状**: `missing_dimension` 错误

**原因**: weight/length/width/height 字段为 null

**解决**:
1. 检查命令行参数 `--weight`
2. 确认 mapping 中 fallback 值已设置
3. 默认尺寸：20×10×15cm, 650g

### 4. 商品创建成功但库存设置失败

**症状**: `PRODUCT_IS_NOT_CREATED` 错误

**原因**: OZON API 时序问题（商品刚创建还未完全就绪）

**解决**:
- ✅ 商品已成功创建，可忽略此错误
- 稍后在 OZON 后台手动设置库存

---

## 📖 其他 Agent 使用指南

### 前置条件

1. **API 密钥**: 配置 `ozon-publisher/config/ozon.json`
2. **象寄 API**: 图片翻译服务（需充值）
3. **Oracle CLI**: 俄语文案生成（LLM 调用）

### 调用方式

**推荐**: 使用 `ozon-publisher` 完整流程

```javascript
// Node.js 示例
const { execSync } = require('child_process');

const url = 'https://detail.1688.com/offer/XXX.html';
const weight = '650g';
const price = '30';

execSync(`node scripts/full-workflow.js "${url}" -w ${weight} -p ${price}`, {
  cwd: '/Users/bzm/.openclaw/skills/ozon-publisher',
  stdio: 'inherit'
});
```

**分步调用**:

```javascript
// Step 1: 1688 抓取
execSync(`node scripts/index.js "${url}"`, {
  cwd: '/Users/bzm/.openclaw/skills/1688-tt'
});

// Step 2: 图片翻译
execSync(`./scripts/ozon-img-trans batch --source-dir "projects/1688-tt/images" --output-dir "projects/ozon-image-translator"`, {
  cwd: '/Users/bzm/.openclaw/skills/ozon-image-translator'
});

// Step 3: 定价计算
execSync(`node scripts/calculate.js -w ${weight} -p ${price}`, {
  cwd: '/Users/bzm/.openclaw/skills/ozon-pricer'
});

// Step 4: OZON 上传
execSync(`node scripts/upload.js`, {
  cwd: '/Users/bzm/.openclaw/skills/ozon-publisher'
});
```

### 错误处理

```javascript
try {
  execSync('...', { stdio: 'inherit' });
  console.log('✅ 成功');
} catch (error) {
  console.error('❌ 失败:', error.message);
  // 读取 progress.json 查看详细进度
  const progress = JSON.parse(fs.readFileSync('projects/ozon-publisher/progress.json'));
  console.log('进度:', progress);
}
```

---

## 📝 开发经验总结

### 踩过的坑

1. **富文本格式**: OZON 的 `rich_content` 字段格式复杂，暂时移除
2. **属性值格式**: 必须用 `dictionary_value_id + value`，不是 `value_id`
3. **图片上传**: OZON 不会自动下载外部 URL，需要先用图床
4. **物流尺寸**: 必须提供 weight/length/width/height，否则报错
5. **原产国**: 必须用俄文 `Китай`，不能用中文 `中国`

### 最佳实践

1. **固定目录**: 所有技能使用固定输出目录，不创建时间戳子目录
2. **输入自包含**: 每个技能的输入都在 `input/` 目录下
3. **串行执行**: ozon-publisher 作为主控制器，内部调用所有子技能
4. **Debug 模式**: 使用 Mock 数据避免重复消耗 API
5. **进度报告**: 写入 `progress.json` 实时进度文件，支持外部监控

---

## 🎯 后续优化方向

1. **批量上架**: 支持多个 1688 链接批量处理
2. **自动库存**: 商品创建后自动设置库存（轮询等待商品就绪）
3. **价格同步**: 定期同步 OZON 价格（根据汇率/成本调整）
4. **错误重试**: 网络错误自动重试机制
5. **日志聚合**: 集中日志管理，便于排查问题

---

## 📞 支持

**技能位置**:
- `~/.openclaw/skills/1688-tt/`
- `~/.openclaw/skills/ozon-image-translator/`
- `~/.openclaw/skills/ozon-pricer/`
- `~/.openclaw/skills/ozon-publisher/`

**文档位置**:
- `~/.openclaw/workspace-developer/OZON-全流程总结文档.md`
- `~/.openclaw/workspace-developer/MEMORY.md`

**问题反馈**: 查看 `projects/ozon-publisher/progress.json` 和 `upload_result.md`

---

*开发完成：2026-03-29 | 版本：v6.0 | 状态：生产就绪*
