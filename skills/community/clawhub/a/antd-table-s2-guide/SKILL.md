---
name: antd-table-s2-guide
description: AntV S2 海量数据表格实战指南。当需要渲染大量数据表格、交叉表、明细表时使用。涵盖S2核心概念（Sheet/Spreadsheet/DataCell/Style）、配置优化、大数据量性能调优（虚拟滚动、冻结列、条件格式）、Vue3集成方案。适用于半导体数据看板、财务报表、运营分析等场景。

**使用时机**：
(1) 用户问AntV S2的配置和用法
(2) 需要渲染大量行列数据（1万+单元格）
(3) 需要交叉分析表、明细表、多维透视
(4) S2性能优化（渲染慢、卡顿）
(5) Vue3 + AntV S2 集成
---

# AntV S2 海量数据表格指南

## 核心概念

```typescript
import { PivotSheet, TableSheet, S2Options, S2Event } from '@antv/s2'

// PivotSheet - 透视分析表（行头+列头交叉）
// TableSheet - 明细表（扁平数据，无行列头）
```

## Vue3 集成模板

```vue
<template>
  <div ref="containerRef" class="s2-container" />
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { PivotSheet } from '@antv/s2'

const containerRef = ref<HTMLDivElement>()

let s2Instance: PivotSheet | null = null

onMounted(() => {
  const container = containerRef.value!
  s2Instance = new PivotSheet(container, s2Options)
  s2Instance.render()
})

onBeforeUnmount(() => {
  s2Instance?.dispose()
})
</script>

<style scoped>
.s2-container {
  width: 100%;
  height: 600px; /* 必须有明确高度 */
}
</style>
```

## 透视表配置

```typescript
const s2Options: S2Options = {
  width: 800,
  height: 600,
  hierarchyType: 'grid', // 'grid' | 'tree'

  // 数据字段定义
  fields: {
    rows: ['province', 'city'],      // 行维度
    columns: ['category', 'product'], // 列维度
    values: ['sales', 'profit'],      // 度量值
    valueInCols: true,                // 指标在列头展示
  },

  // 数据
  data: rawData,

  // 主题
  theme: {
    name: 'default',
    palette: {
      // 自定义条件格式色阶
      condition: {
        positive: { fill: '#29A294' },
        negative: { fill: '#E86452' },
      },
    },
  },

  // 交互
  interaction: {
    hoverHighlight: true,
    selectedCellsSpotlight: true,
    linkFields: ['product'], // 可点击的字段
  },
}
```

## 性能优化

### 1. 虚拟滚动（大数据量必备）

```typescript
const s2Options: S2Options = {
  // S2 默认开启虚拟滚动，但需要确保：
  // 1. 容器有明确高度
  // 2. 不要关闭 frozenRowCount / frozenColCount 中的大量行列
  frozenRowCount: 1,   // 只冻结表头
  frozenColCount: 0,   // 冻结列越多性能越差
  scrollSpeedRatio: {
    horizontal: 0.3,    // 水平滚动速度
    vertical: 0.3,
  },
}
```

### 2. 条件格式优化

```typescript
// ❌ 避免：每个单元格都计算样式
// ✅ 正确：用内置条件格式规则
const conditions = {
  text: [
    {
      field: 'status',
      mapping: (value) => {
        if (value === '异常') return { fill: '#E86452', textFill: '#fff' }
        return {}
      },
    },
  ],
  background: [
    {
      field: 'sales',
      mapping: (value) => {
        // 用线性插值，不要用分段判断
        const ratio = Math.min(Math.abs(value) / 10000, 1)
        return { fill: `rgba(232, 100, 82, ${ratio * 0.3})` }
      },
    },
  ],
}
```

### 3. 大数据量数据准备

```typescript
// ❌ 前端一次性处理 10 万+ 行
// ✅ 分页加载 + 服务端聚合
async function loadData(page: number, size: number) {
  const res = await fetch(`/api/data?page=${page}&size=${size}`)
  return res.json()
}

// S2 支持动态更新数据
s2Instance.setData(newData)
```

### 4. 减少不必要的重渲染

```typescript
// ❌ 频繁更新
watch(searchQuery, () => {
  s2Instance.setData(filteredData) // 每次输入都触发
})

// ✅ 防抖更新
import { useDebounceFn } from '@vueuse/core'
const debouncedUpdate = useDebounceFn((data) => {
  s2Instance.setData(data)
}, 300)

watch(searchQuery, () => {
  debouncedUpdate(filteredData.value)
})
```

## 明细表（TableSheet）

```typescript
import { TableSheet } from '@antv/s2'

const tableSheet = new TableSheet(container, {
  fields: {
    columns: ['id', 'name', 'value', 'status', 'date'],
  },
  data: tableData,
  // 明细表专用配置
  style: {
    cellCfg: {
      width: 120,
      height: 36,
    },
  },
})
```

## 常用事件

```typescript
// 单元格点击
s2Instance.on(S2Event.DATA_CELL_CLICK, (event) => {
  console.log('clicked:', event)
})

// 链接字段点击
s2Instance.on(S2Event.GLOBAL_LINK_FIELD_JUMP, (data) => {
  window.open(data.fieldValue)
})

// 排序
s2Instance.on(S2Event.RANGE_SORTED, (data) => {
  console.log('sorted:', data)
})
```

## 踩坑记录

1. **容器必须有明确高度**，否则 S2 无法计算虚拟滚动区域
2. **frozenColCount 不要超过 3**，冻结列越多渲染压力越大
3. **setData 会重新渲染**，大数据量时配合防抖使用
4. **theme 修改要重新调用 setTheme()**，不能直接改 options
5. **Vue3 中要在 onBeforeUnmount 调用 dispose()**，否则内存泄漏
