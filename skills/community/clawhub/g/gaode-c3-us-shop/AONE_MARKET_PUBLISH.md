# 📤 Aone Market 手动发布指南

> 由于 CLI 登录限制，请通过 Web 界面发布技能

---

## 🎯 发布方式

**Aone Market 支持两种发布方式**：
1. ✅ **Web 界面发布**（推荐）- 通过浏览器上传
2. ❌ CLI 发布 - 需要 npm 登录（当前受限）

---

## 📋 Web 界面发布步骤

### Step 1: 打开 Aone Market

访问：https://open.aone.alibaba-inc.com/market

然后点击 **"发布技能"** 或 **"创建新技能"**

---

### Step 2: 填写基本信息

| 字段 | 填写内容 |
|------|----------|
| **技能名称** | `poi-debug-orchestrator` |
| **版本号** | `0.2.0` |
| **技能描述** | POI 详情页问题排查编排器。自动执行 6 步排查流程：查代码 (sourceId)→查日志→复现请求→解析返回→阅读代码→定位问题 |
| **分类** | 开发效率 |
| **标签** | POI, 调试，日志分析，高德，编排器 |

---

### Step 3: 上传技能文件

**方式 A: 上传压缩包**

1. 将技能目录打包：
```bash
cd /app/501280/working/.claude/skills/
tar -czvf poi-debug-orchestrator.tar.gz poi-debug-orchestrator/
```

2. 在 Web 界面上传 `poi-debug-orchestrator.tar.gz`

**方式 B: 填写 Git 仓库地址**

- **仓库地址**: `https://aone.alibaba-inc.com/git/gaode.search/us-business-service`
- **分支**: `master`
- **技能路径**: `.claude/skills/poi-debug-orchestrator`

---

### Step 4: 配置触发词

在触发词配置框中输入（每行一个）：
```
POI 排查
poi 问题
详情页异常
gsid 排查
traceId 分析
poi 调试
contentPerson
手艺人模块
作品集排查
contentCaseBook
```

---

### Step 5: 上传文档

上传以下文档作为技能说明：

1. **主文档**: `PUBLISH_README.md` 内容
2. **使用文档**: `README.md` 内容
3. **FAQ**: `references/faq.md` 内容

---

### Step 6: 提交审核

点击 **"提交"** 或 **"发布"** 按钮

**审核时间**: 通常 1-2 个工作日

---

## 📦 准备发布包

### 创建压缩包

```bash
# 进入技能目录
cd /app/501280/working/.claude/skills/

# 创建压缩包
tar -czvf poi-debug-orchestrator-v0.2.0.tar.gz poi-debug-orchestrator/

# 查看压缩包内容
tar -tzvf poi-debug-orchestrator-v0.2.0.tar.gz

# 检查大小
ls -lh poi-debug-orchestrator-v0.2.0.tar.gz
```

**预期输出**:
```
poi-debug-orchestrator/
poi-debug-orchestrator/SKILL.md
poi-debug-orchestrator/README.md
poi-debug-orchestrator/package.json
poi-debug-orchestrator/scripts/poi-debug.sh
poi-debug-orchestrator/references/source_id_map.md
poi-debug-orchestrator/references/fields.md
poi-debug-orchestrator/references/faq.md
```

---

## 📝 技能元数据（复制用）

### 基本信息

```yaml
名称：poi-debug-orchestrator
版本：0.2.0
描述：POI 详情页问题排查编排器。自动执行 6 步排查流程：查代码 (sourceId)→查日志→复现请求→解析返回→阅读代码→定位问题
分类：开发效率
作者：土曜 (501280)
License: MIT
```

### 关键词/标签

```
POI, 调试，日志分析，高德，编排器，loghouse, poi 排查，自动化
```

### 触发词

```
POI 排查
poi 问题
详情页异常
gsid 排查
traceId 分析
poi 调试
contentPerson
手艺人模块
作品集排查
contentCaseBook
```

### 依赖要求

```
- aone-kit (Aone CLI)
- curl
- python3
- Loghouse 日志查询权限
- Aone Code 代码读取权限
```

---

## 📖 文档内容

### 技能详细说明

使用 `PUBLISH_README.md` 文件的内容作为技能详细说明。

该文件包含：
- ✅ 技能简介
- ✅ 适用场景
- ✅ 快速开始
- ✅ 执行流程图
- ✅ 支持模块列表
- ✅ 优化收益
- ✅ 故障排查
- ✅ 更新日志

---

## 🎨 图标/截图（可选）

如果有技能图标或演示截图，可以在 Web 界面上传：

1. **技能图标**: 128x128 PNG
2. **演示截图**: 展示排查流程的截图
3. **使用示例**: 输出报告的截图

---

## ✅ 发布后验证

### 1. 检查技能页面

访问：https://open.aone.alibaba-inc.com/market/skill/poi-debug-orchestrator

检查项：
- ✅ 基本信息正确
- ✅ 文档渲染正常
- ✅ 安装命令可用

### 2. 测试安装

```bash
aone-kit skill install poi-debug-orchestrator
```

### 3. 分享链接

发布成功后，分享链接给团队：
```
https://open.aone.alibaba-inc.com/market/skill/poi-debug-orchestrator
```

---

## 🔧 常见问题

### Q1: Web 界面找不到发布入口

**解决**: 
- 确认你有发布权限
- 联系管理员开通权限
- 或尝试直接访问：https://open.aone.alibaba-inc.com/market/publish

---

### Q2: 上传失败 "文件大小超限"

**解决**:
- 确保压缩包小于 10MB
- 移除不必要的文件（如 `.git`, `node_modules`）
- 只保留必需文件

---

### Q3: 审核被拒绝

**常见原因**:
- 描述不清晰
- 缺少使用文档
- 触发词配置不当

**解决**:
- 根据审核意见修改
- 补充完整文档
- 重新提交

---

### Q4: 如何更新版本

**步骤**:
1. 修改 `package.json` 中的版本号
2. 更新 `SKILL.md` 中的版本
3. 重新打包
4. 在 Web 界面上传新版本

---

## 📞 需要帮助？

如果遇到问题：

1. **查看 Aone Market 文档**: https://open.aone.alibaba-inc.com/help
2. **联系管理员**: 在 Aone Market 页面找"联系我们"
3. **内部群咨询**: 高德技术交流群

---

## 📋 发布清单

发布前检查：

- [ ] ✅ `SKILL.md` 已更新
- [ ] ✅ `README.md` 已完善
- [ ] ✅ `package.json` 已配置
- [ ] ✅ `PUBLISH_README.md` 已创建
- [ ] [ ] 压缩包已创建
- [ ] [ ] Web 界面已登录
- [ ] [ ] 基本信息已填写
- [ ] [ ] 触发词已配置
- [ ] [ ] 文档已上传
- [ ] [ ] 提交审核

---

_最后更新：2026-03-31_
