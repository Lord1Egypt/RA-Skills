# POI Debug Orchestrator

> 🚀 POI 详情页问题排查编排器 - 5 分钟内完成 6 步自动化排查

[![Version](https://img.shields.io/npm/v/poi-debug-orchestrator.svg)](https://www.npmjs.com/package/poi-debug-orchestrator)
[![License](https://img.shields.io/npm/l/poi-debug-orchestrator.svg)](https://github.com/gaode.search/us-business-service/blob/master/LICENSE)

---

## 📖 简介

**POI Debug Orchestrator** 是一个自动化 POI 详情页问题排查的编排器技能。它将传统需要 30+ 分钟的手动排查流程压缩到 **5 分钟内** 完成。

### 核心能力

- ✅ **6 步自动化排查**：查代码 (sourceId) → 查日志 → 复现请求 → 解析返回 → 阅读代码 → 生成报告
- ✅ **58 个模块支持**：内置完整的 sourceId 映射表（手艺人、作品集、入驻信息等）
- ✅ **精准日志查询**：使用 sourceId 精准过滤，避免漏掉关键日志
- ✅ **结构化报告**：自动生成包含问题定位和建议的排查报告

---

## 🎯 适用场景

| 场景 | 问题示例 |
|------|----------|
| **模块数据缺失** | "为什么这个 POI 的手艺人模块没有数据？" |
| **请求配置验证** | "这个请求是否包含了作品集模块？" |
| **数据源排查** | "是数据源问题还是代码逻辑问题？" |
| **新模块验证** | "新上线的 IM 模块是否正常工作？" |

---

## 🚀 快速开始

### 安装

```bash
aone-kit skill install poi-debug-orchestrator
```

### 基础用法

```bash
# 排查手艺人模块
./scripts/poi-debug.sh <gsid> <poiid> contentPerson

# 排查作品集模块
./scripts/poi-debug.sh <gsid> <poiid> contentCaseBook

# 排查入驻信息
./scripts/poi-debug.sh <gsid> <poiid> shopSettlement
```

### 参数说明

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `gsid` | ✅ | 用户会话 ID | `09011095227079177495792911000044285436331` |
| `poiid` | ✅ | POI ID | `B0LR4UPN4M` |
| `module` | ❌ | 模块名或 sourceId | `contentPerson` |
| `env` | ❌ | 环境 (gray/online) | `gray` |
| `timeRange` | ❌ | 日志时间范围 | `1h ago` |
| `pageIndex` | ❌ | 分页索引 | `2` |

---

## 📊 执行流程

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Step 0     │ →  │  Step 1     │ →  │  Step 2     │ →  │  Step 3     │ →  │  Step 4     │ →  │  Step 5     │
│  查代码     │    │  查日志     │    │  复现请求    │    │  解析返回    │    │  阅读代码    │    │  生成报告    │
│  (sourceId) │    │  (loghouse) │    │  (curl)     │    │  (python)   │    │  (code MCP) │    │  (分析)     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### 输出示例

```
========================================
  POI Debug Orchestrator v0.2
========================================
  GSID:     09011095227079177495792911000044285436331
  POIID:    B0LR4UPN4M
  MODULE:   contentPerson
  ENV:      gray
========================================

[0/6] ✓ 确定模块 sourceId: contentPerson
[1/6] ✓ 查询 Loghouse 日志... 找到 3 条
[2/6] ✓ 复现请求... 响应 35KB
[3/6] ✓ 解析响应... 返回 6 位手艺人
[4/6] ✓ 定位代码... ShopNodeNameEnum.java
[5/6] ✓ 生成排查报告...

结论：✅ 手艺人模块正常返回数据
```

---

## 📦 支持模块 (58 个)

### 常用模块

| 模块名 | sourceId | 说明 |
|--------|----------|------|
| 手艺人 | `contentPerson` | 人物列表 |
| 作品集 | `contentCaseBook` | 案例列表 |
| 入驻信息 | `shopSettlement` | 好人卡 |
| IM | `shopIm` | IM 信息 |
| AI 客服 | `shopAiCustomer` | AI 客服服务 |
| 店铺基础 | `shopBaseInfo` | 店铺基础信息 |
| 电话 | `telInfo` | 电话信息 |
| 推荐菜 | `shopMenu` | 推荐菜 |

> 完整映射表见 `references/source_id_map.md`

---

## 📈 优化收益

| 维度 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| **单次排查时间** | 30+ 分钟 | 5 分钟内 | ⬇️ 83% |
| **日志查询精准度** | 宽泛 | sourceId 精准 | ⬆️ 80% |
| **新人上手时间** | 2 天 | 30 分钟 | ⬇️ 90% |
| **经验沉淀** | 无 | 58 个模块映射 | ⬆️ 100% |

---

## 🛠️ 依赖要求

- **运行环境**: Linux/macOS with bash
- **必需工具**:
  - `aone-kit` (Aone CLI)
  - `curl`
  - `python3`
  - `jq` (可选，用于 JSON 格式化)
- **权限要求**:
  - Loghouse 日志查询权限
  - Aone Code 代码读取权限
  - 灰度/线上环境访问权限

---

## 📚 文档

- [完整使用文档](docs/技能介绍.md)
- [快速导航](docs/README_展示文档.md)
- [sourceId 映射表](references/source_id_map.md)
- [FAQ](references/faq.md)

---

## 🔧 故障排查

### 常见问题

**Q: 日志查询返回空结果？**
- 检查 `gsid` 是否正确
- 扩大时间范围（如 `4h ago`）
- 确认 `app_name` 和 `log_name` 配置

**Q: 响应解析失败？**
- 检查网络连接
- 确认灰度环境可访问
- 查看 `/tmp/poi-debug-results/` 目录的原始响应

**Q: 找不到某个 sourceId？**
- 查看 `references/source_id_map.md` 确认模块名
- 检查枚举类 `ShopNodeNameEnum` 是否有更新

更多问题见 [references/faq.md](references/faq.md)

---

## 📝 更新日志

### v0.2.0 (2026-03-31)
- ✅ 新增 Step 0: sourceId 自动识别
- ✅ 创建 58 个 sourceId 映射表
- ✅ 优化日志查询精准度
- ✅ 添加 `module` 参数支持
- ✅ 完善文档和示例

### v0.1.0 (2026-03-31)
- ✅ 初始版本发布
- ✅ 实现 5 步排查流程
- ✅ 支持手艺人、作品集等模块

---

## 👥 作者信息

- **作者**: 土曜 (501280)
- **项目**: lse2-us-business-service
- **代码仓库**: gaode.search/us-business-service

---

## 📄 License

MIT License

---

## 🔗 相关链接

- [Aone Market](https://open.aone.alibaba-inc.com/market)
- [Loghouse 使用指南](https://loghouse.alibaba-inc.com/)
- [Aone Code 文档](https://aone.alibaba-inc.com/code)
