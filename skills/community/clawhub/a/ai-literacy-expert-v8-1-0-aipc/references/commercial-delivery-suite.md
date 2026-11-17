> **V7 兼容性说明**：本文件从 V6 完整继承。V7 保留所有 V6 能力，本文件内容完全有效。
> V7 新增 references 见 `references/edge-cloud-architecture.md` / `references/zero-upload-privacy.md` / `references/npu-scheduling-guide.md` / `references/edge-cloud-protocol.md` / `references/audit-report-v7.md`。
> 原始文件版本：V6 · 继承版本：V7 · 继承日期：2026-08-15

# 商用生产力交付套件

> V6 新增 · 能力九：面向商用生产力场景的完整交付体系

## 1. 概述

将 V6 的全部能力整合为面向商用场景的标准化交付物，覆盖五大生产力场景，提供可直接落地的产品级交付。

### 1.1 交付物矩阵

| 交付物 | 格式 | 场景覆盖 | 商用级别 |
|--------|------|----------|----------|
| 互动课件 | 单 HTML | 教学/培训 | 生产级 |
| 冒险游戏 | 单 HTML | 教学/培训 | 生产级 |
| 备课包 | 4格式 zip | 教学 | 生产级 |
| 评估报告 | HTML/PDF | 教学/企业 | 生产级 |
| 数据分析仪表盘 | HTML | 企业/教学 | 生产级 |
| 知识库 | 本地部署 | 企业 | 生产级 |
| 工具箱部署包 | Docker/脚本 | 企业 | 生产级 |

## 2. 交付标准

### 2.1 单文件 HTML 标准

每个 HTML 交付物必须包含：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[项目名称] v[版本号]</title>
    <!-- 元信息 -->
    <meta name="generator" content="AI通识课V6">
    <meta name="version" content="6.0.0">
    <meta name="sha256" content="[文件SHA256]">
    <meta name="offline-capable" content="true">
    
    <!-- CDN 三级降级 -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/2.0.3/p5.min.js"
            onerror="this.onerror=null;this.src='https://cdn.jsdelivr.net/npm/p5@2.0.3/lib/p5.min.js'"></script>
    <script>if(typeof p5==='undefined')document.write('<script src="./vendor/p5.min.js"><\/script>')</script>
    
    <style>/* 响应式 + 暗色模式 */</style>
</head>
<body>
    <!-- 内容 -->
    <script>
    // 完整代码 + 中文注释
    // Service Worker 注册（离线支持）
    // 错误边界处理
    </script>
</body>
</html>
```

### 2.2 README 标准

每个交付物附带 README.md：

```markdown
# [项目名称]

- **版本**: v6.0.0
- **生成时间**: YYYY-MM-DD HH:mm
- **SHA256**: [校验码]
- **依赖**: p5.js 2.0.3 / JSZip / PDF-lib
- **离线支持**: ✅ Service Worker + IndexedDB
- **兼容性**: Chrome 90+ / Firefox 88+ / Edge 90+

## 快速开始
1. 双击打开 HTML 文件
2. 首次使用需联网加载 CDN（后续可离线）

## 功能说明
[功能列表]

## 技术架构
[架构说明]

## 更新日志
- v6.0.0: 初始版本
```

## 3. 商用交付流程

### 3.1 交付检查清单

```
□ 功能完整性
  □ 所有功能可正常使用
  □ 无 JS 控制台错误
  □ 响应式布局正常

□ 性能达标
  □ 首屏加载 <3s
  □ 交互响应 <100ms
  □ 内存占用 <200MB

□ 离线支持
  □ Service Worker 注册成功
  □ 离线后可正常使用
  □ IndexedDB 数据持久化

□ 安全合规
  □ 无外部 API Key 硬编码
  □ 无敏感数据泄露
  □ CORS 配置正确

□ 文档完整
  □ README.md 包含所有信息
  □ 代码注释完整
  □ 版本号 + SHA256 标注

□ 质量门控
  □ 通过 20 维度门控检查
  □ 跨浏览器测试通过
  □ 无障碍基础检查通过
```

### 3.2 版本管理

```
语义化版本: MAJOR.MINOR.PATCH

V6.0.0 - 初始商用交付版本
V6.1.0 - 新增功能（向后兼容）
V6.0.1 - Bug 修复

文件命名: [project]-v[version].[ext]
示例: ai-courseware-module-a1-v6.0.0.html
```

## 4. 五大场景交付模板

### 4.1 办公提效场景

```
交付物清单:
├── 智能文档处理工具.html     (OCR + 文档转换)
├── 会议纪要生成器.html       (ASR + 文本摘要)
├── 数据报表自动生成.html     (数据分析 + 可视化)
├── 知识库问答系统.html       (RAG + 对话界面)
└── README.md
```

### 4.2 知识管理场景

```
交付物清单:
├── 教学知识库构建工具.html    (RAG 导入 + 管理)
├── 智能检索问答.html         (RAG 查询 + 上下文)
├── 知识点图谱可视化.html     (知识关联 + 导航)
├── 学习路径推荐.html         (个性化推荐)
└── README.md
```

### 4.3 创意内容场景

```
交付物清单:
├── 互动课件编辑器.html       (p5.js 课件创作)
├── 游戏化教学设计器.html     (冒险游戏生成)
├── 有声故事生成器.html       (TTS + 图文)
├── 多媒体教材制作.html       (OCR + TTS + 图表)
└── README.md
```

### 4.4 数据分析场景

```
交付物清单:
├── 成绩分析仪表盘.html      (统计 + 图表)
├── 学情诊断报告.html         (薄弱点 + 建议)
├── 课堂互动分析.html         (ASR + 统计)
├── 学期数据总结.html         (综合分析 + 报告)
└── README.md
```

### 4.5 开发辅助场景

```
交付物清单:
├── AI 编程教学助手.html     (代码讲解 + 练习)
├── Prompt 工程设计器.html   (提示词优化 + 测试)
├── API 调试工具.html         (接口测试 + 文档)
├── 代码审查教学.html         (示例 + 最佳实践)
└── README.md
```

## 5. 打包与分发

### 5.1 一键打包

```javascript
// 打包工具 - 生成 zip 交付包
async function packageDelivery(projectName, version, files) {
    const zip = new JSZip();
    
    // 添加项目文件
    for (const file of files) {
        zip.file(file.name, file.content);
    }
    
    // 生成 README
    const readme = generateReadme(projectName, version, files);
    zip.file('README.md', readme);
    
    // 生成校验文件
    const checksum = await calculateSHA256(zip);
    zip.file('SHA256.txt', checksum);
    
    // 导出
    const blob = await zip.generateAsync({ type: 'blob' });
    return { blob, filename: `${projectName}-v${version}.zip` };
}
```

### 5.2 分发格式

| 格式 | 用途 | 大小限制 |
|------|------|----------|
| 单 HTML | 快速分享 | <2MB |
| ZIP 包 | 完整交付 | <50MB |
| Docker 镜像 | 企业部署 | <500MB |
| 离线安装包 | 无网环境 | <1GB |

## 6. 质量门控

| 检查项 | 标准 | 验证方法 |
|--------|------|----------|
| 文件完整 | 所有清单文件存在 | 文件校验 |
| SHA256 正确 | 校验码匹配 | 哈希对比 |
| 版本标注 | 每个文件有版本号 | 元信息检查 |
| README 完整 | 包含所有必需章节 | 内容检查 |
| 离线可用 | 断网后功能正常 | 离线测试 |
| 跨浏览器 | Chrome/Firefox/Edge 通过 | 多浏览器测试 |
| 无硬编码密钥 | 无 API Key 泄露 | 代码扫描 |
| 打包大小 | 符合格式限制 | 文件大小检查 |
