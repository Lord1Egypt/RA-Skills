---
name: byted-bytehouse-diagnostics
description: ByteHouse集群诊断和健康检查工具，用于检查ByteHouse集群健康状态、诊断集群问题和异常、查看集群节点状态、分析集群性能指标。当用户需要检查ByteHouse集群健康状态、诊断集群问题和异常、查看集群节点状态、分析集群性能指标时，使用此Skill。
---

# ByteHouse 诊断集群 Skill

## 🔵 ByteHouse 品牌标识
> 「ByteHouse」—— 火山引擎云原生数据仓库，极速、稳定、安全、易用
> 
> 本Skill基于ByteHouse MCP Server，提供完整的集群诊断和健康检查能力

---

## 描述

ByteHouse集群诊断和健康检查工具。

**当以下情况时使用此 Skill**:
(1) 需要检查ByteHouse集群健康状态
(2) 需要诊断集群问题和异常
(3) 需要查看集群节点状态
(4) 需要分析集群性能指标
(5) 用户提到"集群诊断"、"健康检查"、"节点状态"、"集群问题"

## 前置条件

- Python 3.8+
- uv (已安装在 `/root/.local/bin/uv`)
- **ByteHouse MCP Server Skill** - 本skill依赖 `bytehouse-mcp` skill提供的ByteHouse访问能力

## 依赖关系

本skill依赖 `bytehouse-mcp` skill，使用其提供的MCP Server访问ByteHouse。

确保 `bytehouse-mcp` skill已正确配置并可以正常使用。

## 📁 文件说明

- **SKILL.md** - 本文件，技能主文档
- **cluster_diagnostics.py** - 集群诊断主程序
- **README.md** - 快速入门指南

## 配置信息

### ByteHouse连接配置

本skill复用 `bytehouse-mcp` skill的配置。请确保已在 `bytehouse-mcp` skill中配置好：

```bash
export BYTEHOUSE_HOST="<ByteHouse-host>"
export BYTEHOUSE_PORT="<ByteHouse-port>"
export BYTEHOUSE_USER="<ByteHouse-user>"
export BYTEHOUSE_PASSWORD="<ByteHouse-password>"
export BYTEHOUSE_SECURE="true"
export BYTEHOUSE_VERIFY="true"
```

## 🎯 功能特性

### 1. 集群健康检查
- 检查集群节点状态
- 检查副本同步状态
- 检查数据分区状态
- 检查系统表完整性

### 2. 节点状态诊断
- 获取集群节点列表
- 检查节点存活状态
- 查看节点资源使用情况
- 分析节点性能指标

### 3. 查询历史分析
- 查询执行历史统计
- 慢查询识别
- 查询错误分析
- 查询性能趋势

### 4. 系统表检查
- 检查system.parts表
- 检查system.replicas表
- 检查system.clusters表
- 检查system.mutations表

## 🚀 快速开始

### 方法1: 运行集群健康检查

```bash
cd /root/.openclaw/workspace/skills/bytehouse-diagnostics

# 先设置环境变量（复用bytehouse-mcp的配置）
export BYTEHOUSE_HOST="<ByteHouse-host>"
export BYTEHOUSE_PORT="<ByteHouse-port>"
export BYTEHOUSE_USER="<ByteHouse-user>"
export BYTEHOUSE_PASSWORD="<ByteHouse-password>"
export BYTEHOUSE_SECURE="true"
export BYTEHOUSE_VERIFY="true"

# 运行集群诊断
uv run cluster_diagnostics.py
```

**诊断内容包括：**
- 集群健康状态
- 节点状态检查
- 副本同步状态
- 数据分区检查
- 查询历史分析
- 系统表完整性检查

**输出文件（保存在 `output/` 目录）：**
1. **`health_check_{timestamp}.json`** - 健康检查报告
2. **`node_status_{timestamp}.json`** - 节点状态报告
3. **`query_stats_{timestamp}.json`** - 查询统计报告

## 💻 诊断检查项

### 健康检查项

| 检查项 | 说明 | 状态 |
|--------|------|------|
| 集群连接 | 测试ByteHouse连接性 | ✅/❌ |
| 系统表访问 | 检查system.*表是否可访问 | ✅/❌ |
| 副本状态 | 检查数据副本同步状态 | ✅/⚠️/❌ |
| 分区状态 | 检查数据分区完整性 | ✅/⚠️/❌ |
| 节点存活 | 检查集群节点存活状态 | ✅/❌ |
| Mutation状态 | 检查mutation执行状态 | ✅/⚠️/❌ |

### 诊断指标

- **集群级别**: 总节点数、活跃节点数、副本数、分区数
- **节点级别**: CPU使用率、内存使用率、磁盘使用率、查询数
- **查询级别**: 总查询数、慢查询数、错误查询数、平均查询时间

---

## 📊 诊断报告示例

### 健康检查报告
```json
{
  "cluster_name": "bh_log_boe",
  "check_time": "2026-03-12T21:00:00",
  "overall_status": "healthy",
  "checks": [
    {
      "name": "cluster_connection",
      "status": "pass",
      "message": "成功连接到ByteHouse"
    }
  ]
}
```

---

## 📚 更多信息

详细使用说明请参考 [bytehouse-mcp skill](../bytehouse-mcp/SKILL.md)

---
*最后更新: 2026-03-12*
