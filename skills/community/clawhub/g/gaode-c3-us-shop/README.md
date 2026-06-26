# POI Debug Orchestrator v0.2

**POI 详情页问题排查编排器** — 自动执行 6 步排查流程

## 快速开始

```bash
# 基础用法
./scripts/poi-debug.sh <gsid> <poiid>

# 指定模块名 (使用 sourceId 映射表)
./scripts/poi-debug.sh <gsid> <poiid> contentPerson

# 指定环境
./scripts/poi-debug.sh <gsid> <poiid> online

# 指定时间范围
./scripts/poi-debug.sh <gsid> <poiid> gray "2h ago"

# 完整参数
./scripts/poi-debug.sh <gsid> <poiid> [module] [env] [timeRange] [pageIndex]
```

## 功能特性

✅ **6 步自动排查**: 查代码 (sourceId) → 查日志 → 复现请求 → 解析返回 → 阅读代码 → 生成报告  
✅ **sourceId 映射表**: 从 `ShopNodeNameEnum` 提取 58 个模块映射  
✅ **结构化输出**: 清晰的步骤标记和问题定位  
✅ **多环境支持**: gray / online 环境切换  
✅ **结果持久化**: 自动保存排查结果到 `/tmp/poi-debug-results/`

## 目录结构

```
poi-debug-orchestrator/
├── SKILL.md              # 技能说明（Agent 读取）
├── README.md             # 本文档
├── scripts/
│   └── poi-debug.sh      # 执行脚本
└── references/
    ├── source_id_map.md  # 🆕 sourceId 映射表 (58 个模块)
    ├── fields.md         # 关键字段说明
    └── faq.md            # 常见问题
```

## 输出示例

```
========================================
  POI Debug Orchestrator
========================================
  GSID:  31033080013090177494736367500059940538728
  POIID: B0LR4UPN4M
  ENV:   gray
  Time:  1h ago
========================================

[1/5] 查询 Loghouse 日志...
✓ 找到 2 条日志
✓ TraceID: 1774947317749473634001001b7360 | 耗时：0.112s

[2/5] 复现请求...
✓ 请求成功 | 响应大小：34885 bytes

[3/5] 解析响应...
发现 1 个问题:
  1. shopSettlement 为空

[4/5] 定位相关代码...
✓ 定位到：us-platform/src/main/java/com/amap/us/platform/node/model/shop/ShopSettlementDTO.java

[5/5] 生成排查报告...

========================================
  📋 排查报告
========================================

**GSID**: 31033080013090177494736367500059940538728
**POIID**: B0LR4UPN4M
**TraceID**: 1774947317749473634001001b7360
**环境**: gray

### 日志查询
- 找到日志数：2
- 上游耗时：0.112s

### 请求复现
- 目标地址：http://gray-us-business.amap.com
- 响应大小：34885 bytes

### 响应解析
- shopSettlement: null

⚠️  异常字段:
  - shopSettlement 为空

### 代码定位
- 相关文件：`us-platform/src/main/java/com/amap/us/platform/node/model/shop/ShopSettlementDTO.java`

### 建议操作
1. 如 shopSettlement 为空 → 检查商家入驻状态
2. 如 shopId 为空 → 检查 POI-Shop 绑定关系
3. 如字段缺失 → 查看代码逻辑或 AB 实验配置

========================================

✓ 排查完成！
完整结果已保存：/tmp/poi-debug-results/poi_debug_75000599_20260331_173045.json
```

## 前置要求

- ✅ Loghouse MCP 授权
- ✅ Code MCP 授权
- ✅ 内网环境（VPN 或办公网）
- ✅ `aone-kit` CLI 已安装
- ✅ Python 3.6+

## 常见问题

**Q: 日志查询为空？**  
A: 检查 GSID 是否正确，或扩大时间范围：`./scripts/poi-debug.sh <gsid> <poiid> gray "4h ago"`

**Q: 请求复现失败？**  
A: 确保在内网环境，灰度环境仅限内网访问

**Q: 如何查看完整 JSON？**  
A: `cat /tmp/poi_response_*.json | jq '.'`

更多问题参考 [references/faq.md](references/faq.md)

## 相关文档

- [字段说明](references/fields.md) — POI 详情页关键字段详解
- [FAQ](references/faq.md) — 常见问题解答
- [SKILL.md](SKILL.md) — 技能定义（Agent 使用）

## 版本历史

- **v0.1.0** (2026-03-31) — 初始版本
  - 5 步排查流程
  - 支持 gray/online 环境
  - 自动保存排查结果

---

**作者**: 土曜 (501280)  
**最后更新**: 2026-03-31
