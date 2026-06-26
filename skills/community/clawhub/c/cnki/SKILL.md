---
name: cnki
version: 1.0.0
description: 中国知网 (CNKI) 统一入口 - 搜索、下载、导出、详情查询一体化技能
license: MIT
author: OpenClaw Community
argument-hint: "[命令] [参数] - 例如：search 振动控制, download, export zotero, detail [URL]"
---

# CNKI 统一入口技能

**版本:** 1.0.0  
**整合自:** cnki-search, cnki-advanced-search, cnki-paper-detail, cnki-download, cnki-export, cnki-journal-search, cnki-journal-toc, cnki-parse-results

---

## 🎯 功能概览

| 命令 | 功能 | 原技能 |
|------|------|--------|
| `search` | 基础搜索 | cnki-search |
| `advsearch` | 高级搜索（作者/期刊/年份/SCI/EI 等） | cnki-advanced-search |
| `detail` | 获取论文详情 | cnki-paper-detail |
| `download` | 下载 PDF/CAJ | cnki-download |
| `export` | 导出到 Zotero 或 RIS | cnki-export |
| `journal` | 期刊搜索 | cnki-journal-search |
| `toc` | 期刊目录 | cnki-journal-toc |

---

## 📖 使用方式

### 1️⃣ 基础搜索
```
search [关键词]
search 振动控制
search 实时混合试验 RTHS
```

### 2️⃣ 高级搜索
```
advsearch [自然语言描述条件]
advsearch 作者 张三 期刊 建筑结构学报 2020-2025
advsearch 主题 振动控制 来源类别 SCI,EI
```

### 3️⃣ 论文详情
```
detail [URL]
detail https://kns.cnki.net/kcms2/article/abstract?xxx
```
（如已在论文详情页，可省略 URL）

### 4️⃣ 下载论文
```
download pdf [URL]
download caj [URL]
```
（如已在论文详情页，可省略 URL）

### 5️⃣ 导出文献
```
export zotero [URL]     # 导出到 Zotero（默认）
export ris [URL]        # 保存为 RIS 文件
export gb [URL]         # 输出 GB/T 7714 格式引用
```

### 6️⃣ 期刊相关
```
journal [期刊名]        # 搜索期刊
toc [期刊名] [年份]     # 查看期刊目录
```

---

## 🛠️ 工作流程

### search 命令流程
```
1. 导航到搜索页 (kns.cnki.net/kns8s/search)
2. 填入关键词并搜索
3. 提取结果（标题/作者/期刊/日期/引用/下载）
4. 返回结构化结果
```

### advsearch 命令流程
```
1. 导航到高级搜索页 (kns.cnki.net/kns/AdvSearch)
2. 解析自然语言条件 → 填充表单字段
   - 主题/篇名/关键词
   - 作者/期刊
   - 年份范围
   - 来源类别 (SCI/EI/北大核心/CSSCI/CSCD)
3. 执行搜索并返回结果
```

### detail 命令流程
```
1. 导航到论文页（如提供 URL）
2. 检查验证码（滑块拼图）
3. 提取完整元数据：
   - 标题/作者/单位
   - 摘要/关键词
   - 基金/分类号
   - DOI/URL
```

### download 命令流程
```
1. 导航到论文页（如提供 URL）
2. 检查登录状态和验证码
3. 点击下载链接（PDF 或 CAJ）
4. 确认下载开始
```

### export 命令流程
```
1. 检查当前页面类型（详情页/列表页）
2. 单篇模式：从详情页提取引用数据
3. 批量模式：从列表页批量导出
4. 推送到 Zotero 或保存 RIS 文件
```

---

## ⚠️ 注意事项

### 验证码处理
- **滑块拼图：** 需手动在 Chrome 中完成
- **检测逻辑：** 仅检查可见验证码（排除隐藏的 SDK 验证）
- **提示：** 发现验证码时立即通知用户

### 登录要求
- **下载：** 必须登录 CNKI 且有下载权限
- **导出：** 部分功能需要登录
- **搜索：** 无需登录

### 浏览器要求
- **必须：** Chrome + chrome-devtools MCP
- **推荐：** 保持登录状态

---

## 📊 效率优化

### 工具调用次数对比

| 场景 | 原多技能 | 统一入口 | 节省 |
|------|---------|---------|------|
| 搜索 + 详情 | 2 次调用 | 1 次调用 | 50% |
| 搜索 + 下载 | 3 次调用 | 2 次调用 | 33% |
| 搜索 + 导出 | 3 次调用 | 2 次调用 | 33% |
| 批量导出 | N×3 次 | N+1 次 | ~66% |

### 批量导出优化
**原流程：** 每篇论文单独导航 → 3 次调用 × N 篇  
**新流程：** 列表页直接批量导出 → 2 次调用总计

---

## 🔧 技术实现

### 核心 JavaScript 函数

所有浏览器操作通过单个 `evaluate_script` 完成，避免多次 `wait_for`：

```javascript
async () => {
  // 1. 等待页面加载（轮询检测）
  await new Promise((r, j) => {
    let n = 0;
    const c = () => {
      if (document.querySelector('目标选择器')) r();
      else if (++n > 30) j('timeout');
      else setTimeout(c, 500);
    };
    c();
  });

  // 2. 检查验证码（仅可见区域）
  const captcha = document.querySelector('#tcaptcha_transform_dy');
  if (captcha && captcha.getBoundingClientRect().top >= 0) {
    return { error: 'captcha', message: '需要手动完成验证' };
  }

  // 3. 执行操作并返回结果
  // ...
}
```

### 统一错误处理
```javascript
return {
  success: true/false,
  data: { ... },
  error: '错误类型',
  message: '用户友好提示',
  nextStep: '建议下一步操作'
}
```

---

## 📋 示例对话

### 示例 1：搜索文献
```
用户：search 振动台控制
CNKI：搜索完成，找到 1,234 条结果（第 1/50 页）

1. 地震模拟振动台控制系统的研究进展
   作者：张三，李四 | 期刊：建筑结构学报 | 2024
   引用：45 | 下载：1,234

2. 基于 RTHS 的混合试验方法
   作者：王五 | 期刊：土木工程学报 | 2023
   引用：32 | 下载：876

需要查看详情、下载或导出吗？
```

### 示例 2：高级搜索
```
用户：advsearch 主题 振动控制 作者 纪志斌 期刊 建筑结构学报 2020-2025
CNKI：高级搜索完成，找到 8 条结果

[结果列表]

符合条件的论文较少，是否扩大搜索范围？
```

### 示例 3：下载论文
```
用户：download pdf https://kns.cnki.net/kcms2/article/abstract?xxx
CNKI：开始下载 PDF...

✅ 下载已开始，请检查浏览器下载文件夹

需要导出到 Zotero 吗？
```

### 示例 4：批量导出
```
用户：export zotero
CNKI：检测到当前在搜索结果页（10 篇论文）

选项：
1. 导出全部 10 篇
2. 导出选中的（请勾选）
3. 导出前 N 篇（指定 N）

请选择 → 用户：1
CNKI：正在推送到 Zotero...

✅ 成功导出 10 篇到 Zotero 桌面版
```

---

## 🚀 后续扩展

### 计划功能
- [ ] 批量下载（需登录验证）
- [ ] 引文网络分析
- [ ] 学者主页查询
- [ ] 机构知识库搜索
- [ ] 跨库检索（期刊/学位/会议/专利）

### 性能优化
- [ ] 结果缓存（减少重复搜索）
- [ ] 分页预加载
- [ ] 并发提取详情

---

_整合时间：2026-04-08_  
_整合者：SuperMike_  
_原技能保留：是（向后兼容）_
