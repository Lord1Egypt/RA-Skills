---
name: aidlc-bug-killer
description: 多Agent协作Bug修复工作流。用于三个Agent协作修bug：SubAgent发现bug，主Agent修复，ReviewAgent确认。当需要协调多个Agent修复项目bug时使用此skill。
---

# AIDLC Bug Killer - 三Agent协作Bug修复系统

## 目录结构

```
card-tower/
└── aidlc-docs/
    └── bug-reports/
        ├── pending/           # 待处理bug (SubAgent写入)
        ├── waiting_confirm/   # 修复中/待确认 (主Agent写入)
        └── confirmed/         # 已确认完成 (ReviewAgent确认)
```

## 角色分工

| 角色 | 职责 | 写入目录 |
|------|------|----------|
| SubAgent | 分析代码，发现bug，生成报告 | pending/ |
| 主Agent | 读取bug，修复代码，更新状态 | waiting_confirm/ |
| ReviewAgent | 验证修复，确认通过 | confirmed/ |

## 工作流

### 1. SubAgent发现Bug

创建文件：`aidlc-docs/bug-reports/pending/B-XXX-title.md`

使用模板：`references/bug-template.md`

### 2. 主Agent修复Bug

1. 读取 `pending/` 下的bug文件
2. 分析并修复代码
3. 更新bug文件状态
4. 移动到 `waiting_confirm/`

### 3. ReviewAgent确认

1. 读取 `waiting_confirm/` 下的修复文件
2. 运行测试验证
3. 检查修复是否符合预期
4. 移动到 `confirmed/`

## Changelog 必须更新规则

**每次合并代码到 master 后，必须更新 `aidlc-docs/aidlc-state.md` 的 changelog：**

```
### YYYY-MM-DD
| 时间 | commit | 变更内容 |
|------|--------|----------|
| HH:MM | abc1234 | 描述 |
```

这是 Sub-Agent 获取主Agent进展的唯一入口。即使只改了一行代码也要写。

## 关键规则

1. **一个bug一个文件** - 便于并行处理
2. **状态同步** - 文件状态必须与实际一致
3. **不删除bug** - 已确认的移入confirmed，不删除
4. **详细记录** - 便于追溯和复盘
