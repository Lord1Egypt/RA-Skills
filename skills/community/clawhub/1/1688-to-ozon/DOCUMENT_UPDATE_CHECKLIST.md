# 文档更新检查清单

**更新日期**: 2026-03-29  
**原因**: 参数默认值修改（-w/-p 必需，-s 默认 0）

---

## 已更新文件 ✅

| 文件 | 更新内容 | 状态 |
|------|----------|------|
| `skills/ozon-publisher/scripts/full-workflow.js` | 移除默认值，添加参数验证 | ✅ 已完成 |
| `skills/ozon-publisher/SKILL.md` | 参数表更新（-w/-p 必需，-s 默认 0） | ✅ 已完成 |
| `skills/ozon-publisher/README.md` | 参数说明更新 | ✅ 已完成 |
| `skills/ozon-pricer/SKILL.md` | 参数表更新（-w/-p 必需） | ✅ 已完成 |
| `skills/ozon-publisher/SKILL.md` | 添加 triggers 配置 | ✅ 已完成 |

---

## 待检查文件 ⏳

| 文件 | 检查项 | 状态 |
|------|--------|------|
| `skills/ozon-image-translator/SKILL.md` | 触发词配置 | ⏳ 待检查 |
| `skills/1688-tt/SKILL.md` | 触发词配置 | ⏳ 待检查 |
| `skills/ozon-publisher/OPTIMIZATION_REPORT_v2.0.md` | 参数说明 | ⏳ 待检查 |

---

## 关键修改点

### ozon-publisher (op)

**修改前**:
```javascript
let weight = '100g';
let purchasePrice = '10';
let shippingCost = '15';
```

**修改后**:
```javascript
let weight = null;          // 必需参数
let purchasePrice = null;   // 必需参数
let shippingCost = null;    // 可选，默认 0

// 验证逻辑
if (!weight) {
  console.error('❌ 错误：必须指定重量参数 -w 或 --weight');
  process.exit(1);
}

if (!purchasePrice) {
  console.error('❌ 错误：必须指定采购价参数 -p 或 --purchase-price');
  process.exit(1);
}

if (!shippingCost) {
  shippingCost = '0';  // 默认 0 元
}
```

### 参数默认值对比

| 参数 | 旧默认值 | 新默认值 | 修改原因 |
|------|---------|---------|---------|
| `-w` | `100g` | ❌ 必需 | 重量直接影响运费计算 |
| `-p` | `10` | ❌ 必需 | 采购价是成本核心 |
| `-s` | `15` | `0` | 国内运费不固定，不应设默认值 |

---

## 其他 Agent 使用指南

### 正确调用方式

```javascript
// ✅ 正确：提供必需参数
sessions_spawn({
  task: `https://detail.1688.com/offer/XXX.html op -w 650g -p 30`
});

// ❌ 错误：缺少必需参数
sessions_spawn({
  task: `https://detail.1688.com/offer/XXX.html op`
  // → 会报错：缺少 -w 和 -p
});
```

### 错误处理

```javascript
try {
  execSync(`URL op -w 650g -p 30`);
} catch (error) {
  // 检查错误信息
  if (error.stdout.includes('必须指定重量参数')) {
    // 提示用户提供 -w
  }
  if (error.stdout.includes('必须指定采购价参数')) {
    // 提示用户提供 -p
  }
}
```

---

## 测试验证

```bash
# 测试 1: 缺少 -w（应报错）
https://detail.1688.com/offer/XXX.html op -p 30
# → ❌ 错误：必须指定重量参数

# 测试 2: 缺少 -p（应报错）
https://detail.1688.com/offer/XXX.html op -w 650g
# → ❌ 错误：必须指定采购价参数

# 测试 3: 完整参数（应成功）
https://detail.1688.com/offer/XXX.html op -w 650g -p 30
# → ✅ 执行成功

# 测试 4: 默认运费（应为 0）
https://detail.1688.com/offer/XXX.html op -w 650g -p 30
# → 国内运费：0 元（不是 15 元）
```

---

**下次修改代码时，必须同步更新所有相关文档！**
