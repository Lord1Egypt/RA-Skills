---
name: "cascader"
description: "Cascader 级联选择器 -- Element Plus Vue3 桌面端组件。Invoke when user needs Cascader 级联选择器 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/cascader.html"
---

---

# Cascader 级联选择器 [​](#cascader-级联选择器)

更新日志待解决

33

当一个数据集合有清晰的层级结构时，可通过级联选择器逐级查看并选择。

## 基础用法 [​](#基础用法)

有两种触发子菜单的方式

只需为 Cascader 的`options`属性指定选项数组即可渲染出一个级联选择器。 通过 `props.expandTrigger` 属性控制子节点的展开方式

Child options expand when clicked (default)

Child options expand when hovered

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgPHA+Q2hpbGQgb3B0aW9ucyBleHBhbmQgd2hlbiBjbGlja2VkIChkZWZhdWx0KTwvcD5cbiAgICA8ZWwtY2FzY2FkZXIgdi1tb2RlbD1cInZhbHVlXCIgOm9wdGlvbnM9XCJvcHRpb25zXCIgQGNoYW5nZT1cImhhbmRsZUNoYW5nZVwiIC8+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgPHA+Q2hpbGQgb3B0aW9ucyBleHBhbmQgd2hlbiBob3ZlcmVkPC9wPlxuICAgIDxlbC1jYXNjYWRlclxuICAgICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICAgIDpvcHRpb25zPVwib3B0aW9uc1wiXG4gICAgICA6cHJvcHM9XCJwcm9wc1wiXG4gICAgICBAY2hhbmdlPVwiaGFuZGxlQ2hhbmdlXCJcbiAgICAvPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKFtdKVxuXG5jb25zdCBwcm9wcyA9IHtcbiAgZXhwYW5kVHJpZ2dlcjogJ2hvdmVyJyBhcyBjb25zdCxcbn1cblxuY29uc3QgaGFuZGxlQ2hhbmdlID0gKHZhbHVlKSA9PiB7XG4gIGNvbnNvbGUubG9nKHZhbHVlKVxufVxuXG5jb25zdCBvcHRpb25zID0gW1xuICB7XG4gICAgdmFsdWU6ICdndWlkZScsXG4gICAgbGFiZWw6ICdHdWlkZScsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdkaXNjaXBsaW5lcycsXG4gICAgICAgIGxhYmVsOiAnRGlzY2lwbGluZXMnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY29uc2lzdGVuY3knLFxuICAgICAgICAgICAgbGFiZWw6ICdDb25zaXN0ZW5jeScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2ZlZWRiYWNrJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRmVlZGJhY2snLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdlZmZpY2llbmN5JyxcbiAgICAgICAgICAgIGxhYmVsOiAnRWZmaWNpZW5jeScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NvbnRyb2xsYWJpbGl0eScsXG4gICAgICAgICAgICBsYWJlbDogJ0NvbnRyb2xsYWJpbGl0eScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnbmF2aWdhdGlvbicsXG4gICAgICAgIGxhYmVsOiAnTmF2aWdhdGlvbicsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdzaWRlIG5hdicsXG4gICAgICAgICAgICBsYWJlbDogJ1NpZGUgTmF2aWdhdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RvcCBuYXYnLFxuICAgICAgICAgICAgbGFiZWw6ICdUb3AgTmF2aWdhdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnY29tcG9uZW50JyxcbiAgICBsYWJlbDogJ0NvbXBvbmVudCcsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdiYXNpYycsXG4gICAgICAgIGxhYmVsOiAnQmFzaWMnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbGF5b3V0JyxcbiAgICAgICAgICAgIGxhYmVsOiAnTGF5b3V0JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY29sb3InLFxuICAgICAgICAgICAgbGFiZWw6ICdDb2xvcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3R5cG9ncmFwaHknLFxuICAgICAgICAgICAgbGFiZWw6ICdUeXBvZ3JhcGh5JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnaWNvbicsXG4gICAgICAgICAgICBsYWJlbDogJ0ljb24nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdidXR0b24nLFxuICAgICAgICAgICAgbGFiZWw6ICdCdXR0b24nLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJ2Zvcm0nLFxuICAgICAgICBsYWJlbDogJ0Zvcm0nLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAncmFkaW8nLFxuICAgICAgICAgICAgbGFiZWw6ICdSYWRpbycsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NoZWNrYm94JyxcbiAgICAgICAgICAgIGxhYmVsOiAnQ2hlY2tib3gnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdpbnB1dCcsXG4gICAgICAgICAgICBsYWJlbDogJ0lucHV0JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnaW5wdXQtbnVtYmVyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnSW5wdXROdW1iZXInLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdzZWxlY3QnLFxuICAgICAgICAgICAgbGFiZWw6ICdTZWxlY3QnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdjYXNjYWRlcicsXG4gICAgICAgICAgICBsYWJlbDogJ0Nhc2NhZGVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc3dpdGNoJyxcbiAgICAgICAgICAgIGxhYmVsOiAnU3dpdGNoJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc2xpZGVyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnU2xpZGVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndGltZS1waWNrZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdUaW1lUGlja2VyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnZGF0ZS1waWNrZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdEYXRlUGlja2VyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnZGF0ZXRpbWUtcGlja2VyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRGF0ZVRpbWVQaWNrZXInLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd1cGxvYWQnLFxuICAgICAgICAgICAgbGFiZWw6ICdVcGxvYWQnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdyYXRlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnUmF0ZScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2Zvcm0nLFxuICAgICAgICAgICAgbGFiZWw6ICdGb3JtJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdkYXRhJyxcbiAgICAgICAgbGFiZWw6ICdEYXRhJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RhYmxlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVGFibGUnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0YWcnLFxuICAgICAgICAgICAgbGFiZWw6ICdUYWcnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdwcm9ncmVzcycsXG4gICAgICAgICAgICBsYWJlbDogJ1Byb2dyZXNzJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndHJlZScsXG4gICAgICAgICAgICBsYWJlbDogJ1RyZWUnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdwYWdpbmF0aW9uJyxcbiAgICAgICAgICAgIGxhYmVsOiAnUGFnaW5hdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2JhZGdlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQmFkZ2UnLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJ25vdGljZScsXG4gICAgICAgIGxhYmVsOiAnTm90aWNlJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2FsZXJ0JyxcbiAgICAgICAgICAgIGxhYmVsOiAnQWxlcnQnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdsb2FkaW5nJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTG9hZGluZycsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ21lc3NhZ2UnLFxuICAgICAgICAgICAgbGFiZWw6ICdNZXNzYWdlJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbWVzc2FnZS1ib3gnLFxuICAgICAgICAgICAgbGFiZWw6ICdNZXNzYWdlQm94JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbm90aWZpY2F0aW9uJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTm90aWZpY2F0aW9uJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICduYXZpZ2F0aW9uJyxcbiAgICAgICAgbGFiZWw6ICdOYXZpZ2F0aW9uJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ21lbnUnLFxuICAgICAgICAgICAgbGFiZWw6ICdNZW51JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndGFicycsXG4gICAgICAgICAgICBsYWJlbDogJ1RhYnMnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdicmVhZGNydW1iJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQnJlYWRjcnVtYicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2Ryb3Bkb3duJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRHJvcGRvd24nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdzdGVwcycsXG4gICAgICAgICAgICBsYWJlbDogJ1N0ZXBzJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdvdGhlcnMnLFxuICAgICAgICBsYWJlbDogJ090aGVycycsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdkaWFsb2cnLFxuICAgICAgICAgICAgbGFiZWw6ICdEaWFsb2cnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0b29sdGlwJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVG9vbHRpcCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3BvcG92ZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdQb3BvdmVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY2FyZCcsXG4gICAgICAgICAgICBsYWJlbDogJ0NhcmQnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdjYXJvdXNlbCcsXG4gICAgICAgICAgICBsYWJlbDogJ0Nhcm91c2VsJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY29sbGFwc2UnLFxuICAgICAgICAgICAgbGFiZWw6ICdDb2xsYXBzZScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAncmVzb3VyY2UnLFxuICAgIGxhYmVsOiAnUmVzb3VyY2UnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnYXh1cmUnLFxuICAgICAgICBsYWJlbDogJ0F4dXJlIENvbXBvbmVudHMnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdza2V0Y2gnLFxuICAgICAgICBsYWJlbDogJ1NrZXRjaCBUZW1wbGF0ZXMnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdkb2NzJyxcbiAgICAgICAgbGFiZWw6ICdEZXNpZ24gRG9jdW1lbnRhdGlvbicsXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/cascader/basic.vue)_

vue

```
<template>
  <div class="m-4">
    <p>Child options expand when clicked (default)</p>
    <el-cascader v-model="value" :options="options" @change="handleChange" />
  </div>
  <div class="m-4">
    <p>Child options expand when hovered</p>
    <el-cascader
      v-model="value"
      :options="options"
      :props="props"
      @change="handleChange"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref([])

const props = {
  expandTrigger: 'hover' as const,
}

const handleChange = (value) => {
  console.log(value)
}

const options = [
  {
    value: 'guide',
    label: 'Guide',
    children: [
      {
        value: 'disciplines',
        label: 'Disciplines',
        children: [
          {
            value: 'consistency',
            label: 'Consistency',
          },
          {
            value: 'feedback',
            label: 'Feedback',
          },
          {
            value: 'efficiency',
            label: 'Efficiency',
          },
          {
            value: 'controllability',
            label: 'Controllability',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'side nav',
            label: 'Side Navigation',
          },
          {
            value: 'top nav',
            label: 'Top Navigation',
          },
        ],
      },
    ],
  },
  {
    value: 'component',
    label: 'Component',
    children: [
      {
        value: 'basic',
        label: 'Basic',
        children: [
          {
            value: 'layout',
            label: 'Layout',
          },
          {
            value: 'color',
            label: 'Color',
          },
          {
            value: 'typography',
            label: 'Typography',
          },
          {
            value: 'icon',
            label: 'Icon',
          },
          {
            value: 'button',
            label: 'Button',
          },
        ],
      },
      {
        value: 'form',
        label: 'Form',
        children: [
          {
            value: 'radio',
            label: 'Radio',
          },
          {
            value: 'checkbox',
            label: 'Checkbox',
          },
          {
            value: 'input',
            label: 'Input',
          },
          {
            value: 'input-number',
            label: 'InputNumber',
          },
          {
            value: 'select',
            label: 'Select',
          },
          {
            value: 'cascader',
            label: 'Cascader',
          },
          {
            value: 'switch',
            label: 'Switch',
          },
          {
            value: 'slider',
            label: 'Slider',
          },
          {
            value: 'time-picker',
            label: 'TimePicker',
          },
          {
            value: 'date-picker',
            label: 'DatePicker',
          },
          {
            value: 'datetime-picker',
            label: 'DateTimePicker',
          },
          {
            value: 'upload',
            label: 'Upload',
          },
          {
            value: 'rate',
            label: 'Rate',
          },
          {
            value: 'form',
            label: 'Form',
          },
        ],
      },
      {
        value: 'data',
        label: 'Data',
        children: [
          {
            value: 'table',
            label: 'Table',
          },
          {
            value: 'tag',
            label: 'Tag',
          },
          {
            value: 'progress',
            label: 'Progress',
          },
          {
            value: 'tree',
            label: 'Tree',
          },
          {
            value: 'pagination',
            label: 'Pagination',
          },
          {
            value: 'badge',
            label: 'Badge',
          },
        ],
      },
      {
        value: 'notice',
        label: 'Notice',
        children: [
          {
            value: 'alert',
            label: 'Alert',
          },
          {
            value: 'loading',
            label: 'Loading',
          },
          {
            value: 'message',
            label: 'Message',
          },
          {
            value: 'message-box',
            label: 'MessageBox',
          },
          {
            value: 'notification',
            label: 'Notification',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'menu',
            label: 'Menu',
          },
          {
            value: 'tabs',
            label: 'Tabs',
          },
          {
            value: 'breadcrumb',
            label: 'Breadcrumb',
          },
          {
            value: 'dropdown',
            label: 'Dropdown',
          },
          {
            value: 'steps',
            label: 'Steps',
          },
        ],
      },
      {
        value: 'others',
        label: 'Others',
        children: [
          {
            value: 'dialog',
            label: 'Dialog',
          },
          {
            value: 'tooltip',
            label: 'Tooltip',
          },
          {
            value: 'popover',
            label: 'Popover',
          },
          {
            value: 'card',
            label: 'Card',
          },
          {
            value: 'carousel',
            label: 'Carousel',
          },
          {
            value: 'collapse',
            label: 'Collapse',
          },
        ],
      },
    ],
  },
  {
    value: 'resource',
    label: 'Resource',
    children: [
      {
        value: 'axure',
        label: 'Axure Components',
      },
      {
        value: 'sketch',
        label: 'Sketch Templates',
      },
      {
        value: 'docs',
        label: 'Design Documentation',
      },
    ],
  },
]
</script>
```

隐藏源代码

## 有禁用选项 [​](#有禁用选项)

通过在数据源中设置 `disabled` 字段来声明该选项是禁用的

本例中，`options`指定的数组中的第一个元素含有`disabled: true`键值对，因此是禁用的。 在默认情况下，Cascader 会检查数据中每一项的`disabled`字段是否为`true`，如果你的数据中表示禁用含义的字段名不为`disabled`，可以通过`props.disabled`属性来指定（详见下方 API 表格）。 当然，`value`、`label`和`children`这三个字段名也可以通过同样的方式指定。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2FzY2FkZXIgOm9wdGlvbnM9XCJvcHRpb25zXCIgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5jb25zdCBvcHRpb25zID0gW1xuICB7XG4gICAgdmFsdWU6ICdndWlkZScsXG4gICAgbGFiZWw6ICdHdWlkZScsXG4gICAgZGlzYWJsZWQ6IHRydWUsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdkaXNjaXBsaW5lcycsXG4gICAgICAgIGxhYmVsOiAnRGlzY2lwbGluZXMnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY29uc2lzdGVuY3knLFxuICAgICAgICAgICAgbGFiZWw6ICdDb25zaXN0ZW5jeScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2ZlZWRiYWNrJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRmVlZGJhY2snLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdlZmZpY2llbmN5JyxcbiAgICAgICAgICAgIGxhYmVsOiAnRWZmaWNpZW5jeScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NvbnRyb2xsYWJpbGl0eScsXG4gICAgICAgICAgICBsYWJlbDogJ0NvbnRyb2xsYWJpbGl0eScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnbmF2aWdhdGlvbicsXG4gICAgICAgIGxhYmVsOiAnTmF2aWdhdGlvbicsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdzaWRlIG5hdicsXG4gICAgICAgICAgICBsYWJlbDogJ1NpZGUgTmF2aWdhdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RvcCBuYXYnLFxuICAgICAgICAgICAgbGFiZWw6ICdUb3AgTmF2aWdhdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnY29tcG9uZW50JyxcbiAgICBsYWJlbDogJ0NvbXBvbmVudCcsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdiYXNpYycsXG4gICAgICAgIGxhYmVsOiAnQmFzaWMnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbGF5b3V0JyxcbiAgICAgICAgICAgIGxhYmVsOiAnTGF5b3V0JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY29sb3InLFxuICAgICAgICAgICAgbGFiZWw6ICdDb2xvcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3R5cG9ncmFwaHknLFxuICAgICAgICAgICAgbGFiZWw6ICdUeXBvZ3JhcGh5JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnaWNvbicsXG4gICAgICAgICAgICBsYWJlbDogJ0ljb24nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdidXR0b24nLFxuICAgICAgICAgICAgbGFiZWw6ICdCdXR0b24nLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJ2Zvcm0nLFxuICAgICAgICBsYWJlbDogJ0Zvcm0nLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAncmFkaW8nLFxuICAgICAgICAgICAgbGFiZWw6ICdSYWRpbycsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NoZWNrYm94JyxcbiAgICAgICAgICAgIGxhYmVsOiAnQ2hlY2tib3gnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdpbnB1dCcsXG4gICAgICAgICAgICBsYWJlbDogJ0lucHV0JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnaW5wdXQtbnVtYmVyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnSW5wdXROdW1iZXInLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdzZWxlY3QnLFxuICAgICAgICAgICAgbGFiZWw6ICdTZWxlY3QnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdjYXNjYWRlcicsXG4gICAgICAgICAgICBsYWJlbDogJ0Nhc2NhZGVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc3dpdGNoJyxcbiAgICAgICAgICAgIGxhYmVsOiAnU3dpdGNoJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc2xpZGVyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnU2xpZGVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndGltZS1waWNrZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdUaW1lUGlja2VyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnZGF0ZS1waWNrZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdEYXRlUGlja2VyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnZGF0ZXRpbWUtcGlja2VyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRGF0ZVRpbWVQaWNrZXInLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd1cGxvYWQnLFxuICAgICAgICAgICAgbGFiZWw6ICdVcGxvYWQnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdyYXRlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnUmF0ZScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2Zvcm0nLFxuICAgICAgICAgICAgbGFiZWw6ICdGb3JtJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdkYXRhJyxcbiAgICAgICAgbGFiZWw6ICdEYXRhJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RhYmxlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVGFibGUnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0YWcnLFxuICAgICAgICAgICAgbGFiZWw6ICdUYWcnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdwcm9ncmVzcycsXG4gICAgICAgICAgICBsYWJlbDogJ1Byb2dyZXNzJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndHJlZScsXG4gICAgICAgICAgICBsYWJlbDogJ1RyZWUnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdwYWdpbmF0aW9uJyxcbiAgICAgICAgICAgIGxhYmVsOiAnUGFnaW5hdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2JhZGdlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQmFkZ2UnLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJ25vdGljZScsXG4gICAgICAgIGxhYmVsOiAnTm90aWNlJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2FsZXJ0JyxcbiAgICAgICAgICAgIGxhYmVsOiAnQWxlcnQnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdsb2FkaW5nJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTG9hZGluZycsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ21lc3NhZ2UnLFxuICAgICAgICAgICAgbGFiZWw6ICdNZXNzYWdlJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbWVzc2FnZS1ib3gnLFxuICAgICAgICAgICAgbGFiZWw6ICdNZXNzYWdlQm94JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbm90aWZpY2F0aW9uJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTm90aWZpY2F0aW9uJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICduYXZpZ2F0aW9uJyxcbiAgICAgICAgbGFiZWw6ICdOYXZpZ2F0aW9uJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ21lbnUnLFxuICAgICAgICAgICAgbGFiZWw6ICdNZW51JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndGFicycsXG4gICAgICAgICAgICBsYWJlbDogJ1RhYnMnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdicmVhZGNydW1iJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQnJlYWRjcnVtYicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2Ryb3Bkb3duJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRHJvcGRvd24nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdzdGVwcycsXG4gICAgICAgICAgICBsYWJlbDogJ1N0ZXBzJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdvdGhlcnMnLFxuICAgICAgICBsYWJlbDogJ090aGVycycsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdkaWFsb2cnLFxuICAgICAgICAgICAgbGFiZWw6ICdEaWFsb2cnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0b29sdGlwJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVG9vbHRpcCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3BvcG92ZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdQb3BvdmVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY2FyZCcsXG4gICAgICAgICAgICBsYWJlbDogJ0NhcmQnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdjYXJvdXNlbCcsXG4gICAgICAgICAgICBsYWJlbDogJ0Nhcm91c2VsJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY29sbGFwc2UnLFxuICAgICAgICAgICAgbGFiZWw6ICdDb2xsYXBzZScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAncmVzb3VyY2UnLFxuICAgIGxhYmVsOiAnUmVzb3VyY2UnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnYXh1cmUnLFxuICAgICAgICBsYWJlbDogJ0F4dXJlIENvbXBvbmVudHMnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdza2V0Y2gnLFxuICAgICAgICBsYWJlbDogJ1NrZXRjaCBUZW1wbGF0ZXMnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdkb2NzJyxcbiAgICAgICAgbGFiZWw6ICdEZXNpZ24gRG9jdW1lbnRhdGlvbicsXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/cascader/option-disabling.vue)_

vue

```
<template>
  <el-cascader :options="options" />
</template>

<script lang="ts" setup>
const options = [
  {
    value: 'guide',
    label: 'Guide',
    disabled: true,
    children: [
      {
        value: 'disciplines',
        label: 'Disciplines',
        children: [
          {
            value: 'consistency',
            label: 'Consistency',
          },
          {
            value: 'feedback',
            label: 'Feedback',
          },
          {
            value: 'efficiency',
            label: 'Efficiency',
          },
          {
            value: 'controllability',
            label: 'Controllability',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'side nav',
            label: 'Side Navigation',
          },
          {
            value: 'top nav',
            label: 'Top Navigation',
          },
        ],
      },
    ],
  },
  {
    value: 'component',
    label: 'Component',
    children: [
      {
        value: 'basic',
        label: 'Basic',
        children: [
          {
            value: 'layout',
            label: 'Layout',
          },
          {
            value: 'color',
            label: 'Color',
          },
          {
            value: 'typography',
            label: 'Typography',
          },
          {
            value: 'icon',
            label: 'Icon',
          },
          {
            value: 'button',
            label: 'Button',
          },
        ],
      },
      {
        value: 'form',
        label: 'Form',
        children: [
          {
            value: 'radio',
            label: 'Radio',
          },
          {
            value: 'checkbox',
            label: 'Checkbox',
          },
          {
            value: 'input',
            label: 'Input',
          },
          {
            value: 'input-number',
            label: 'InputNumber',
          },
          {
            value: 'select',
            label: 'Select',
          },
          {
            value: 'cascader',
            label: 'Cascader',
          },
          {
            value: 'switch',
            label: 'Switch',
          },
          {
            value: 'slider',
            label: 'Slider',
          },
          {
            value: 'time-picker',
            label: 'TimePicker',
          },
          {
            value: 'date-picker',
            label: 'DatePicker',
          },
          {
            value: 'datetime-picker',
            label: 'DateTimePicker',
          },
          {
            value: 'upload',
            label: 'Upload',
          },
          {
            value: 'rate',
            label: 'Rate',
          },
          {
            value: 'form',
            label: 'Form',
          },
        ],
      },
      {
        value: 'data',
        label: 'Data',
        children: [
          {
            value: 'table',
            label: 'Table',
          },
          {
            value: 'tag',
            label: 'Tag',
          },
          {
            value: 'progress',
            label: 'Progress',
          },
          {
            value: 'tree',
            label: 'Tree',
          },
          {
            value: 'pagination',
            label: 'Pagination',
          },
          {
            value: 'badge',
            label: 'Badge',
          },
        ],
      },
      {
        value: 'notice',
        label: 'Notice',
        children: [
          {
            value: 'alert',
            label: 'Alert',
          },
          {
            value: 'loading',
            label: 'Loading',
          },
          {
            value: 'message',
            label: 'Message',
          },
          {
            value: 'message-box',
            label: 'MessageBox',
          },
          {
            value: 'notification',
            label: 'Notification',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'menu',
            label: 'Menu',
          },
          {
            value: 'tabs',
            label: 'Tabs',
          },
          {
            value: 'breadcrumb',
            label: 'Breadcrumb',
          },
          {
            value: 'dropdown',
            label: 'Dropdown',
          },
          {
            value: 'steps',
            label: 'Steps',
          },
        ],
      },
      {
        value: 'others',
        label: 'Others',
        children: [
          {
            value: 'dialog',
            label: 'Dialog',
          },
          {
            value: 'tooltip',
            label: 'Tooltip',
          },
          {
            value: 'popover',
            label: 'Popover',
          },
          {
            value: 'card',
            label: 'Card',
          },
          {
            value: 'carousel',
            label: 'Carousel',
          },
          {
            value: 'collapse',
            label: 'Collapse',
          },
        ],
      },
    ],
  },
  {
    value: 'resource',
    label: 'Resource',
    children: [
      {
        value: 'axure',
        label: 'Axure Components',
      },
      {
        value: 'sketch',
        label: 'Sketch Templates',
      },
      {
        value: 'docs',
        label: 'Design Documentation',
      },
    ],
  },
]
</script>
```

隐藏源代码

## 可清空 [​](#可清空)

通过 `clearable` 设置输入框可清空

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2FzY2FkZXIgOm9wdGlvbnM9XCJvcHRpb25zXCIgY2xlYXJhYmxlIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuY29uc3Qgb3B0aW9ucyA9IFtcbiAge1xuICAgIHZhbHVlOiAnZ3VpZGUnLFxuICAgIGxhYmVsOiAnR3VpZGUnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnZGlzY2lwbGluZXMnLFxuICAgICAgICBsYWJlbDogJ0Rpc2NpcGxpbmVzJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NvbnNpc3RlbmN5JyxcbiAgICAgICAgICAgIGxhYmVsOiAnQ29uc2lzdGVuY3knLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdmZWVkYmFjaycsXG4gICAgICAgICAgICBsYWJlbDogJ0ZlZWRiYWNrJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnZWZmaWNpZW5jeScsXG4gICAgICAgICAgICBsYWJlbDogJ0VmZmljaWVuY3knLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdjb250cm9sbGFiaWxpdHknLFxuICAgICAgICAgICAgbGFiZWw6ICdDb250cm9sbGFiaWxpdHknLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJ25hdmlnYXRpb24nLFxuICAgICAgICBsYWJlbDogJ05hdmlnYXRpb24nLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc2lkZSBuYXYnLFxuICAgICAgICAgICAgbGFiZWw6ICdTaWRlIE5hdmlnYXRpb24nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0b3AgbmF2JyxcbiAgICAgICAgICAgIGxhYmVsOiAnVG9wIE5hdmlnYXRpb24nLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ2NvbXBvbmVudCcsXG4gICAgbGFiZWw6ICdDb21wb25lbnQnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnYmFzaWMnLFxuICAgICAgICBsYWJlbDogJ0Jhc2ljJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2xheW91dCcsXG4gICAgICAgICAgICBsYWJlbDogJ0xheW91dCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NvbG9yJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQ29sb3InLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0eXBvZ3JhcGh5JyxcbiAgICAgICAgICAgIGxhYmVsOiAnVHlwb2dyYXBoeScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2ljb24nLFxuICAgICAgICAgICAgbGFiZWw6ICdJY29uJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnYnV0dG9uJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQnV0dG9uJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdmb3JtJyxcbiAgICAgICAgbGFiZWw6ICdGb3JtJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3JhZGlvJyxcbiAgICAgICAgICAgIGxhYmVsOiAnUmFkaW8nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdjaGVja2JveCcsXG4gICAgICAgICAgICBsYWJlbDogJ0NoZWNrYm94JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnaW5wdXQnLFxuICAgICAgICAgICAgbGFiZWw6ICdJbnB1dCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2lucHV0LW51bWJlcicsXG4gICAgICAgICAgICBsYWJlbDogJ0lucHV0TnVtYmVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc2VsZWN0JyxcbiAgICAgICAgICAgIGxhYmVsOiAnU2VsZWN0JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY2FzY2FkZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdDYXNjYWRlcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3N3aXRjaCcsXG4gICAgICAgICAgICBsYWJlbDogJ1N3aXRjaCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3NsaWRlcicsXG4gICAgICAgICAgICBsYWJlbDogJ1NsaWRlcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RpbWUtcGlja2VyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVGltZVBpY2tlcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2RhdGUtcGlja2VyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRGF0ZVBpY2tlcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2RhdGV0aW1lLXBpY2tlcicsXG4gICAgICAgICAgICBsYWJlbDogJ0RhdGVUaW1lUGlja2VyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndXBsb2FkJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVXBsb2FkJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAncmF0ZScsXG4gICAgICAgICAgICBsYWJlbDogJ1JhdGUnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdmb3JtJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRm9ybScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnZGF0YScsXG4gICAgICAgIGxhYmVsOiAnRGF0YScsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0YWJsZScsXG4gICAgICAgICAgICBsYWJlbDogJ1RhYmxlJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndGFnJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVGFnJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAncHJvZ3Jlc3MnLFxuICAgICAgICAgICAgbGFiZWw6ICdQcm9ncmVzcycsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RyZWUnLFxuICAgICAgICAgICAgbGFiZWw6ICdUcmVlJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAncGFnaW5hdGlvbicsXG4gICAgICAgICAgICBsYWJlbDogJ1BhZ2luYXRpb24nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdiYWRnZScsXG4gICAgICAgICAgICBsYWJlbDogJ0JhZGdlJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdub3RpY2UnLFxuICAgICAgICBsYWJlbDogJ05vdGljZScsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdhbGVydCcsXG4gICAgICAgICAgICBsYWJlbDogJ0FsZXJ0JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbG9hZGluZycsXG4gICAgICAgICAgICBsYWJlbDogJ0xvYWRpbmcnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdtZXNzYWdlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTWVzc2FnZScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ21lc3NhZ2UtYm94JyxcbiAgICAgICAgICAgIGxhYmVsOiAnTWVzc2FnZUJveCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ25vdGlmaWNhdGlvbicsXG4gICAgICAgICAgICBsYWJlbDogJ05vdGlmaWNhdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnbmF2aWdhdGlvbicsXG4gICAgICAgIGxhYmVsOiAnTmF2aWdhdGlvbicsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdtZW51JyxcbiAgICAgICAgICAgIGxhYmVsOiAnTWVudScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RhYnMnLFxuICAgICAgICAgICAgbGFiZWw6ICdUYWJzJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnYnJlYWRjcnVtYicsXG4gICAgICAgICAgICBsYWJlbDogJ0JyZWFkY3J1bWInLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdkcm9wZG93bicsXG4gICAgICAgICAgICBsYWJlbDogJ0Ryb3Bkb3duJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc3RlcHMnLFxuICAgICAgICAgICAgbGFiZWw6ICdTdGVwcycsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnb3RoZXJzJyxcbiAgICAgICAgbGFiZWw6ICdPdGhlcnMnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnZGlhbG9nJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRGlhbG9nJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndG9vbHRpcCcsXG4gICAgICAgICAgICBsYWJlbDogJ1Rvb2x0aXAnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdwb3BvdmVyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnUG9wb3ZlcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NhcmQnLFxuICAgICAgICAgICAgbGFiZWw6ICdDYXJkJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY2Fyb3VzZWwnLFxuICAgICAgICAgICAgbGFiZWw6ICdDYXJvdXNlbCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NvbGxhcHNlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQ29sbGFwc2UnLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ3Jlc291cmNlJyxcbiAgICBsYWJlbDogJ1Jlc291cmNlJyxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICB2YWx1ZTogJ2F4dXJlJyxcbiAgICAgICAgbGFiZWw6ICdBeHVyZSBDb21wb25lbnRzJyxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnc2tldGNoJyxcbiAgICAgICAgbGFiZWw6ICdTa2V0Y2ggVGVtcGxhdGVzJyxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnZG9jcycsXG4gICAgICAgIGxhYmVsOiAnRGVzaWduIERvY3VtZW50YXRpb24nLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/cascader/clearable.vue)_

vue

```
<template>
  <el-cascader :options="options" clearable />
</template>

<script lang="ts" setup>
const options = [
  {
    value: 'guide',
    label: 'Guide',
    children: [
      {
        value: 'disciplines',
        label: 'Disciplines',
        children: [
          {
            value: 'consistency',
            label: 'Consistency',
          },
          {
            value: 'feedback',
            label: 'Feedback',
          },
          {
            value: 'efficiency',
            label: 'Efficiency',
          },
          {
            value: 'controllability',
            label: 'Controllability',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'side nav',
            label: 'Side Navigation',
          },
          {
            value: 'top nav',
            label: 'Top Navigation',
          },
        ],
      },
    ],
  },
  {
    value: 'component',
    label: 'Component',
    children: [
      {
        value: 'basic',
        label: 'Basic',
        children: [
          {
            value: 'layout',
            label: 'Layout',
          },
          {
            value: 'color',
            label: 'Color',
          },
          {
            value: 'typography',
            label: 'Typography',
          },
          {
            value: 'icon',
            label: 'Icon',
          },
          {
            value: 'button',
            label: 'Button',
          },
        ],
      },
      {
        value: 'form',
        label: 'Form',
        children: [
          {
            value: 'radio',
            label: 'Radio',
          },
          {
            value: 'checkbox',
            label: 'Checkbox',
          },
          {
            value: 'input',
            label: 'Input',
          },
          {
            value: 'input-number',
            label: 'InputNumber',
          },
          {
            value: 'select',
            label: 'Select',
          },
          {
            value: 'cascader',
            label: 'Cascader',
          },
          {
            value: 'switch',
            label: 'Switch',
          },
          {
            value: 'slider',
            label: 'Slider',
          },
          {
            value: 'time-picker',
            label: 'TimePicker',
          },
          {
            value: 'date-picker',
            label: 'DatePicker',
          },
          {
            value: 'datetime-picker',
            label: 'DateTimePicker',
          },
          {
            value: 'upload',
            label: 'Upload',
          },
          {
            value: 'rate',
            label: 'Rate',
          },
          {
            value: 'form',
            label: 'Form',
          },
        ],
      },
      {
        value: 'data',
        label: 'Data',
        children: [
          {
            value: 'table',
            label: 'Table',
          },
          {
            value: 'tag',
            label: 'Tag',
          },
          {
            value: 'progress',
            label: 'Progress',
          },
          {
            value: 'tree',
            label: 'Tree',
          },
          {
            value: 'pagination',
            label: 'Pagination',
          },
          {
            value: 'badge',
            label: 'Badge',
          },
        ],
      },
      {
        value: 'notice',
        label: 'Notice',
        children: [
          {
            value: 'alert',
            label: 'Alert',
          },
          {
            value: 'loading',
            label: 'Loading',
          },
          {
            value: 'message',
            label: 'Message',
          },
          {
            value: 'message-box',
            label: 'MessageBox',
          },
          {
            value: 'notification',
            label: 'Notification',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'menu',
            label: 'Menu',
          },
          {
            value: 'tabs',
            label: 'Tabs',
          },
          {
            value: 'breadcrumb',
            label: 'Breadcrumb',
          },
          {
            value: 'dropdown',
            label: 'Dropdown',
          },
          {
            value: 'steps',
            label: 'Steps',
          },
        ],
      },
      {
        value: 'others',
        label: 'Others',
        children: [
          {
            value: 'dialog',
            label: 'Dialog',
          },
          {
            value: 'tooltip',
            label: 'Tooltip',
          },
          {
            value: 'popover',
            label: 'Popover',
          },
          {
            value: 'card',
            label: 'Card',
          },
          {
            value: 'carousel',
            label: 'Carousel',
          },
          {
            value: 'collapse',
            label: 'Collapse',
          },
        ],
      },
    ],
  },
  {
    value: 'resource',
    label: 'Resource',
    children: [
      {
        value: 'axure',
        label: 'Axure Components',
      },
      {
        value: 'sketch',
        label: 'Sketch Templates',
      },
      {
        value: 'docs',
        label: 'Design Documentation',
      },
    ],
  },
]
</script>
```

隐藏源代码

## 自定义清除图标2.11.0 [​](#自定义清除图标)

你可以通过`clear-icon`属性自定义清除图标

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2FzY2FkZXJcbiAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgIGNsZWFyYWJsZVxuICAgIDpjbGVhci1pY29uPVwiQ2xvc2VCb2xkXCJcbiAgICBwbGFjZWhvbGRlcj1cIkN1c3RvbSBjbGVhciBpY29uXCJcbiAgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBDbG9zZUJvbGQgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuY29uc3Qgb3B0aW9ucyA9IFtcbiAge1xuICAgIHZhbHVlOiAnZ3VpZGUnLFxuICAgIGxhYmVsOiAnR3VpZGUnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnZGlzY2lwbGluZXMnLFxuICAgICAgICBsYWJlbDogJ0Rpc2NpcGxpbmVzJyxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/cascader/clear-icon.vue)_

vue

```
<template>
  <el-cascader
    :options="options"
    clearable
    :clear-icon="CloseBold"
    placeholder="Custom clear icon"
  />
</template>

<script lang="ts" setup>
import { CloseBold } from '@element-plus/icons-vue'

const options = [
  {
    value: 'guide',
    label: 'Guide',
    children: [
      {
        value: 'disciplines',
        label: 'Disciplines',
      },
    ],
  },
]
</script>
```

隐藏源代码

## 仅显示最后一级 [​](#仅显示最后一级)

可以仅在输入框中显示选中项最后一级的标签，而不是选中项所在的完整路径。

属性`show-all-levels`定义了是否显示完整的路径， 将其赋值为 `false` 则仅显示最后一级。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2FzY2FkZXIgOm9wdGlvbnM9XCJvcHRpb25zXCIgOnNob3ctYWxsLWxldmVscz1cImZhbHNlXCIgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5jb25zdCBvcHRpb25zID0gW1xuICB7XG4gICAgdmFsdWU6ICdndWlkZScsXG4gICAgbGFiZWw6ICdHdWlkZScsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdkaXNjaXBsaW5lcycsXG4gICAgICAgIGxhYmVsOiAnRGlzY2lwbGluZXMnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY29uc2lzdGVuY3knLFxuICAgICAgICAgICAgbGFiZWw6ICdDb25zaXN0ZW5jeScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2ZlZWRiYWNrJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRmVlZGJhY2snLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdlZmZpY2llbmN5JyxcbiAgICAgICAgICAgIGxhYmVsOiAnRWZmaWNpZW5jeScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NvbnRyb2xsYWJpbGl0eScsXG4gICAgICAgICAgICBsYWJlbDogJ0NvbnRyb2xsYWJpbGl0eScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnbmF2aWdhdGlvbicsXG4gICAgICAgIGxhYmVsOiAnTmF2aWdhdGlvbicsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdzaWRlIG5hdicsXG4gICAgICAgICAgICBsYWJlbDogJ1NpZGUgTmF2aWdhdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RvcCBuYXYnLFxuICAgICAgICAgICAgbGFiZWw6ICdUb3AgTmF2aWdhdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnY29tcG9uZW50JyxcbiAgICBsYWJlbDogJ0NvbXBvbmVudCcsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdiYXNpYycsXG4gICAgICAgIGxhYmVsOiAnQmFzaWMnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbGF5b3V0JyxcbiAgICAgICAgICAgIGxhYmVsOiAnTGF5b3V0JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY29sb3InLFxuICAgICAgICAgICAgbGFiZWw6ICdDb2xvcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3R5cG9ncmFwaHknLFxuICAgICAgICAgICAgbGFiZWw6ICdUeXBvZ3JhcGh5JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnaWNvbicsXG4gICAgICAgICAgICBsYWJlbDogJ0ljb24nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdidXR0b24nLFxuICAgICAgICAgICAgbGFiZWw6ICdCdXR0b24nLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJ2Zvcm0nLFxuICAgICAgICBsYWJlbDogJ0Zvcm0nLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAncmFkaW8nLFxuICAgICAgICAgICAgbGFiZWw6ICdSYWRpbycsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NoZWNrYm94JyxcbiAgICAgICAgICAgIGxhYmVsOiAnQ2hlY2tib3gnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdpbnB1dCcsXG4gICAgICAgICAgICBsYWJlbDogJ0lucHV0JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnaW5wdXQtbnVtYmVyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnSW5wdXROdW1iZXInLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdzZWxlY3QnLFxuICAgICAgICAgICAgbGFiZWw6ICdTZWxlY3QnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdjYXNjYWRlcicsXG4gICAgICAgICAgICBsYWJlbDogJ0Nhc2NhZGVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc3dpdGNoJyxcbiAgICAgICAgICAgIGxhYmVsOiAnU3dpdGNoJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc2xpZGVyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnU2xpZGVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndGltZS1waWNrZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdUaW1lUGlja2VyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnZGF0ZS1waWNrZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdEYXRlUGlja2VyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnZGF0ZXRpbWUtcGlja2VyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRGF0ZVRpbWVQaWNrZXInLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd1cGxvYWQnLFxuICAgICAgICAgICAgbGFiZWw6ICdVcGxvYWQnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdyYXRlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnUmF0ZScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2Zvcm0nLFxuICAgICAgICAgICAgbGFiZWw6ICdGb3JtJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdkYXRhJyxcbiAgICAgICAgbGFiZWw6ICdEYXRhJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RhYmxlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVGFibGUnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0YWcnLFxuICAgICAgICAgICAgbGFiZWw6ICdUYWcnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdwcm9ncmVzcycsXG4gICAgICAgICAgICBsYWJlbDogJ1Byb2dyZXNzJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndHJlZScsXG4gICAgICAgICAgICBsYWJlbDogJ1RyZWUnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdwYWdpbmF0aW9uJyxcbiAgICAgICAgICAgIGxhYmVsOiAnUGFnaW5hdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2JhZGdlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQmFkZ2UnLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJ25vdGljZScsXG4gICAgICAgIGxhYmVsOiAnTm90aWNlJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2FsZXJ0JyxcbiAgICAgICAgICAgIGxhYmVsOiAnQWxlcnQnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdsb2FkaW5nJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTG9hZGluZycsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ21lc3NhZ2UnLFxuICAgICAgICAgICAgbGFiZWw6ICdNZXNzYWdlJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbWVzc2FnZS1ib3gnLFxuICAgICAgICAgICAgbGFiZWw6ICdNZXNzYWdlQm94JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbm90aWZpY2F0aW9uJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTm90aWZpY2F0aW9uJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICduYXZpZ2F0aW9uJyxcbiAgICAgICAgbGFiZWw6ICdOYXZpZ2F0aW9uJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ21lbnUnLFxuICAgICAgICAgICAgbGFiZWw6ICdNZW51JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndGFicycsXG4gICAgICAgICAgICBsYWJlbDogJ1RhYnMnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdicmVhZGNydW1iJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQnJlYWRjcnVtYicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2Ryb3Bkb3duJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRHJvcGRvd24nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdzdGVwcycsXG4gICAgICAgICAgICBsYWJlbDogJ1N0ZXBzJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdvdGhlcnMnLFxuICAgICAgICBsYWJlbDogJ090aGVycycsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdkaWFsb2cnLFxuICAgICAgICAgICAgbGFiZWw6ICdEaWFsb2cnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0b29sdGlwJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVG9vbHRpcCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3BvcG92ZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdQb3BvdmVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY2FyZCcsXG4gICAgICAgICAgICBsYWJlbDogJ0NhcmQnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdjYXJvdXNlbCcsXG4gICAgICAgICAgICBsYWJlbDogJ0Nhcm91c2VsJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY29sbGFwc2UnLFxuICAgICAgICAgICAgbGFiZWw6ICdDb2xsYXBzZScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAncmVzb3VyY2UnLFxuICAgIGxhYmVsOiAnUmVzb3VyY2UnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnYXh1cmUnLFxuICAgICAgICBsYWJlbDogJ0F4dXJlIENvbXBvbmVudHMnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdza2V0Y2gnLFxuICAgICAgICBsYWJlbDogJ1NrZXRjaCBUZW1wbGF0ZXMnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdkb2NzJyxcbiAgICAgICAgbGFiZWw6ICdEZXNpZ24gRG9jdW1lbnRhdGlvbicsXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/cascader/last-level.vue)_

vue

```
<template>
  <el-cascader :options="options" :show-all-levels="false" />
</template>

<script lang="ts" setup>
const options = [
  {
    value: 'guide',
    label: 'Guide',
    children: [
      {
        value: 'disciplines',
        label: 'Disciplines',
        children: [
          {
            value: 'consistency',
            label: 'Consistency',
          },
          {
            value: 'feedback',
            label: 'Feedback',
          },
          {
            value: 'efficiency',
            label: 'Efficiency',
          },
          {
            value: 'controllability',
            label: 'Controllability',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'side nav',
            label: 'Side Navigation',
          },
          {
            value: 'top nav',
            label: 'Top Navigation',
          },
        ],
      },
    ],
  },
  {
    value: 'component',
    label: 'Component',
    children: [
      {
        value: 'basic',
        label: 'Basic',
        children: [
          {
            value: 'layout',
            label: 'Layout',
          },
          {
            value: 'color',
            label: 'Color',
          },
          {
            value: 'typography',
            label: 'Typography',
          },
          {
            value: 'icon',
            label: 'Icon',
          },
          {
            value: 'button',
            label: 'Button',
          },
        ],
      },
      {
        value: 'form',
        label: 'Form',
        children: [
          {
            value: 'radio',
            label: 'Radio',
          },
          {
            value: 'checkbox',
            label: 'Checkbox',
          },
          {
            value: 'input',
            label: 'Input',
          },
          {
            value: 'input-number',
            label: 'InputNumber',
          },
          {
            value: 'select',
            label: 'Select',
          },
          {
            value: 'cascader',
            label: 'Cascader',
          },
          {
            value: 'switch',
            label: 'Switch',
          },
          {
            value: 'slider',
            label: 'Slider',
          },
          {
            value: 'time-picker',
            label: 'TimePicker',
          },
          {
            value: 'date-picker',
            label: 'DatePicker',
          },
          {
            value: 'datetime-picker',
            label: 'DateTimePicker',
          },
          {
            value: 'upload',
            label: 'Upload',
          },
          {
            value: 'rate',
            label: 'Rate',
          },
          {
            value: 'form',
            label: 'Form',
          },
        ],
      },
      {
        value: 'data',
        label: 'Data',
        children: [
          {
            value: 'table',
            label: 'Table',
          },
          {
            value: 'tag',
            label: 'Tag',
          },
          {
            value: 'progress',
            label: 'Progress',
          },
          {
            value: 'tree',
            label: 'Tree',
          },
          {
            value: 'pagination',
            label: 'Pagination',
          },
          {
            value: 'badge',
            label: 'Badge',
          },
        ],
      },
      {
        value: 'notice',
        label: 'Notice',
        children: [
          {
            value: 'alert',
            label: 'Alert',
          },
          {
            value: 'loading',
            label: 'Loading',
          },
          {
            value: 'message',
            label: 'Message',
          },
          {
            value: 'message-box',
            label: 'MessageBox',
          },
          {
            value: 'notification',
            label: 'Notification',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'menu',
            label: 'Menu',
          },
          {
            value: 'tabs',
            label: 'Tabs',
          },
          {
            value: 'breadcrumb',
            label: 'Breadcrumb',
          },
          {
            value: 'dropdown',
            label: 'Dropdown',
          },
          {
            value: 'steps',
            label: 'Steps',
          },
        ],
      },
      {
        value: 'others',
        label: 'Others',
        children: [
          {
            value: 'dialog',
            label: 'Dialog',
          },
          {
            value: 'tooltip',
            label: 'Tooltip',
          },
          {
            value: 'popover',
            label: 'Popover',
          },
          {
            value: 'card',
            label: 'Card',
          },
          {
            value: 'carousel',
            label: 'Carousel',
          },
          {
            value: 'collapse',
            label: 'Collapse',
          },
        ],
      },
    ],
  },
  {
    value: 'resource',
    label: 'Resource',
    children: [
      {
        value: 'axure',
        label: 'Axure Components',
      },
      {
        value: 'sketch',
        label: 'Sketch Templates',
      },
      {
        value: 'docs',
        label: 'Design Documentation',
      },
    ],
  },
]
</script>
```

隐藏源代码

## 多选 [​](#多选)

在标签中添加 `:props="props"` 并设置 `props = { multiple: true }` 来开启多选模式。

正确用法：

vue

```
<template>
  <el-cascader :props="props" />
</template>

<script lang="ts" setup>
const props = { multiple: true }
</script>
```

错误用法：

vue

```
<template>
  <!--  Object literal binging here is invalid syntax for cascader  -->
  <el-cascader :props="{ multiple: true }" />
</template>
```

使用多选时，所有选中的标签将默认显示。 您可以设置 `collapse = true` 将选中的标签折叠。 您可以设置 `max-collapse-tags` 来显示最大tag数量，默认1。 您可以使用 `collapse-tags-tooltip` 属性来启用鼠标悬停折叠文字以显示具体所选值的行为。

Display all tags (default)

Collapse tags

Collapse tags tooltip

Max Collapse Tags

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgPHA+RGlzcGxheSBhbGwgdGFncyAoZGVmYXVsdCk8L3A+XG4gICAgPGVsLWNhc2NhZGVyIDpvcHRpb25zPVwib3B0aW9uc1wiIDpwcm9wcz1cInByb3BzXCIgY2xlYXJhYmxlIC8+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgPHA+Q29sbGFwc2UgdGFnczwvcD5cbiAgICA8ZWwtY2FzY2FkZXIgOm9wdGlvbnM9XCJvcHRpb25zXCIgOnByb3BzPVwicHJvcHNcIiBjb2xsYXBzZS10YWdzIGNsZWFyYWJsZSAvPlxuICA8L2Rpdj5cbiAgPGRpdiBjbGFzcz1cIm0tNFwiPlxuICAgIDxwPkNvbGxhcHNlIHRhZ3MgdG9vbHRpcDwvcD5cbiAgICA8ZWwtY2FzY2FkZXJcbiAgICAgIDpvcHRpb25zPVwib3B0aW9uc1wiXG4gICAgICA6cHJvcHM9XCJwcm9wc1wiXG4gICAgICBjb2xsYXBzZS10YWdzXG4gICAgICBjb2xsYXBzZS10YWdzLXRvb2x0aXBcbiAgICAgIGNsZWFyYWJsZVxuICAgIC8+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgPHA+TWF4IENvbGxhcHNlIFRhZ3M8L3A+XG4gICAgPGVsLWNhc2NhZGVyXG4gICAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgICAgOnByb3BzPVwicHJvcHNcIlxuICAgICAgY29sbGFwc2UtdGFnc1xuICAgICAgY29sbGFwc2UtdGFncy10b29sdGlwXG4gICAgICA6bWF4LWNvbGxhcHNlLXRhZ3M9XCIzXCJcbiAgICAgIGNsZWFyYWJsZVxuICAgIC8+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmNvbnN0IHByb3BzID0geyBtdWx0aXBsZTogdHJ1ZSB9XG5cbmNvbnN0IG9wdGlvbnMgPSBbXG4gIHtcbiAgICB2YWx1ZTogMSxcbiAgICBsYWJlbDogJ0FzaWEnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAyLFxuICAgICAgICBsYWJlbDogJ0NoaW5hJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7IHZhbHVlOiAzLCBsYWJlbDogJ0JlaWppbmcnIH0sXG4gICAgICAgICAgeyB2YWx1ZTogNCwgbGFiZWw6ICdTaGFuZ2hhaScgfSxcbiAgICAgICAgICB7IHZhbHVlOiA1LCBsYWJlbDogJ0hhbmd6aG91JyB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6IDYsXG4gICAgICAgIGxhYmVsOiAnSmFwYW4nLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHsgdmFsdWU6IDcsIGxhYmVsOiAnVG9reW8nIH0sXG4gICAgICAgICAgeyB2YWx1ZTogOCwgbGFiZWw6ICdPc2FrYScgfSxcbiAgICAgICAgICB7IHZhbHVlOiA5LCBsYWJlbDogJ0t5b3RvJyB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6IDEwLFxuICAgICAgICBsYWJlbDogJ0tvcmVhJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7IHZhbHVlOiAxMSwgbGFiZWw6ICdTZW91bCcgfSxcbiAgICAgICAgICB7IHZhbHVlOiAxMiwgbGFiZWw6ICdCdXNhbicgfSxcbiAgICAgICAgICB7IHZhbHVlOiAxMywgbGFiZWw6ICdUYWVndScgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAxNCxcbiAgICBsYWJlbDogJ0V1cm9wZScsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6IDE1LFxuICAgICAgICBsYWJlbDogJ0ZyYW5jZScsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAgeyB2YWx1ZTogMTYsIGxhYmVsOiAnUGFyaXMnIH0sXG4gICAgICAgICAgeyB2YWx1ZTogMTcsIGxhYmVsOiAnTWFyc2VpbGxlJyB9LFxuICAgICAgICAgIHsgdmFsdWU6IDE4LCBsYWJlbDogJ0x5b24nIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogMTksXG4gICAgICAgIGxhYmVsOiAnVUsnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHsgdmFsdWU6IDIwLCBsYWJlbDogJ0xvbmRvbicgfSxcbiAgICAgICAgICB7IHZhbHVlOiAyMSwgbGFiZWw6ICdCaXJtaW5naGFtJyB9LFxuICAgICAgICAgIHsgdmFsdWU6IDIyLCBsYWJlbDogJ01hbmNoZXN0ZXInIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogMjMsXG4gICAgbGFiZWw6ICdOb3J0aCBBbWVyaWNhJyxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICB2YWx1ZTogMjQsXG4gICAgICAgIGxhYmVsOiAnVVMnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHsgdmFsdWU6IDI1LCBsYWJlbDogJ05ldyBZb3JrJyB9LFxuICAgICAgICAgIHsgdmFsdWU6IDI2LCBsYWJlbDogJ0xvcyBBbmdlbGVzJyB9LFxuICAgICAgICAgIHsgdmFsdWU6IDI3LCBsYWJlbDogJ1dhc2hpbmd0b24nIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogMjgsXG4gICAgICAgIGxhYmVsOiAnQ2FuYWRhJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7IHZhbHVlOiAyOSwgbGFiZWw6ICdUb3JvbnRvJyB9LFxuICAgICAgICAgIHsgdmFsdWU6IDMwLCBsYWJlbDogJ01vbnRyZWFsJyB9LFxuICAgICAgICAgIHsgdmFsdWU6IDMxLCBsYWJlbDogJ090dGF3YScgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/cascader/multiple-selection.vue)_

vue

```
<template>
  <div class="m-4">
    <p>Display all tags (default)</p>
    <el-cascader :options="options" :props="props" clearable />
  </div>
  <div class="m-4">
    <p>Collapse tags</p>
    <el-cascader :options="options" :props="props" collapse-tags clearable />
  </div>
  <div class="m-4">
    <p>Collapse tags tooltip</p>
    <el-cascader
      :options="options"
      :props="props"
      collapse-tags
      collapse-tags-tooltip
      clearable
    />
  </div>
  <div class="m-4">
    <p>Max Collapse Tags</p>
    <el-cascader
      :options="options"
      :props="props"
      collapse-tags
      collapse-tags-tooltip
      :max-collapse-tags="3"
      clearable
    />
  </div>
</template>

<script lang="ts" setup>
const props = { multiple: true }

const options = [
  {
    value: 1,
    label: 'Asia',
    children: [
      {
        value: 2,
        label: 'China',
        children: [
          { value: 3, label: 'Beijing' },
          { value: 4, label: 'Shanghai' },
          { value: 5, label: 'Hangzhou' },
        ],
      },
      {
        value: 6,
        label: 'Japan',
        children: [
          { value: 7, label: 'Tokyo' },
          { value: 8, label: 'Osaka' },
          { value: 9, label: 'Kyoto' },
        ],
      },
      {
        value: 10,
        label: 'Korea',
        children: [
          { value: 11, label: 'Seoul' },
          { value: 12, label: 'Busan' },
          { value: 13, label: 'Taegu' },
        ],
      },
    ],
  },
  {
    value: 14,
    label: 'Europe',
    children: [
      {
        value: 15,
        label: 'France',
        children: [
          { value: 16, label: 'Paris' },
          { value: 17, label: 'Marseille' },
          { value: 18, label: 'Lyon' },
        ],
      },
      {
        value: 19,
        label: 'UK',
        children: [
          { value: 20, label: 'London' },
          { value: 21, label: 'Birmingham' },
          { value: 22, label: 'Manchester' },
        ],
      },
    ],
  },
  {
    value: 23,
    label: 'North America',
    children: [
      {
        value: 24,
        label: 'US',
        children: [
          { value: 25, label: 'New York' },
          { value: 26, label: 'Los Angeles' },
          { value: 27, label: 'Washington' },
        ],
      },
      {
        value: 28,
        label: 'Canada',
        children: [
          { value: 29, label: 'Toronto' },
          { value: 30, label: 'Montreal' },
          { value: 31, label: 'Ottawa' },
        ],
      },
    ],
  },
]
</script>
```

隐藏源代码

## 选择任意一级选项 [​](#选择任意一级选项)

在单选模式下，你只能选择叶子节点；而在多选模式下，勾选父节点真正选中的都是叶子节点。 启用该功能后，可让父子节点取消关联，选择任意一级选项。

可通过 `props.checkStrictly = true` 来设置父子节点取消选中关联，从而达到选择任意一级选项的目的。

Select any level of options (Single selection)

Select any level of options (Multiple selection)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgPHA+U2VsZWN0IGFueSBsZXZlbCBvZiBvcHRpb25zIChTaW5nbGUgc2VsZWN0aW9uKTwvcD5cbiAgICA8ZWwtY2FzY2FkZXIgOm9wdGlvbnM9XCJvcHRpb25zXCIgOnByb3BzPVwicHJvcHMxXCIgY2xlYXJhYmxlIC8+XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgPHA+U2VsZWN0IGFueSBsZXZlbCBvZiBvcHRpb25zIChNdWx0aXBsZSBzZWxlY3Rpb24pPC9wPlxuICAgIDxlbC1jYXNjYWRlciA6b3B0aW9ucz1cIm9wdGlvbnNcIiA6cHJvcHM9XCJwcm9wczJcIiBjbGVhcmFibGUgLz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuY29uc3QgcHJvcHMxID0ge1xuICBjaGVja1N0cmljdGx5OiB0cnVlLFxufVxuXG5jb25zdCBwcm9wczIgPSB7XG4gIG11bHRpcGxlOiB0cnVlLFxuICBjaGVja1N0cmljdGx5OiB0cnVlLFxufVxuXG5jb25zdCBvcHRpb25zID0gW1xuICB7XG4gICAgdmFsdWU6ICdndWlkZScsXG4gICAgbGFiZWw6ICdHdWlkZScsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdkaXNjaXBsaW5lcycsXG4gICAgICAgIGxhYmVsOiAnRGlzY2lwbGluZXMnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY29uc2lzdGVuY3knLFxuICAgICAgICAgICAgbGFiZWw6ICdDb25zaXN0ZW5jeScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2ZlZWRiYWNrJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRmVlZGJhY2snLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdlZmZpY2llbmN5JyxcbiAgICAgICAgICAgIGxhYmVsOiAnRWZmaWNpZW5jeScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NvbnRyb2xsYWJpbGl0eScsXG4gICAgICAgICAgICBsYWJlbDogJ0NvbnRyb2xsYWJpbGl0eScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnbmF2aWdhdGlvbicsXG4gICAgICAgIGxhYmVsOiAnTmF2aWdhdGlvbicsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdzaWRlIG5hdicsXG4gICAgICAgICAgICBsYWJlbDogJ1NpZGUgTmF2aWdhdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RvcCBuYXYnLFxuICAgICAgICAgICAgbGFiZWw6ICdUb3AgTmF2aWdhdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnY29tcG9uZW50JyxcbiAgICBsYWJlbDogJ0NvbXBvbmVudCcsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdiYXNpYycsXG4gICAgICAgIGxhYmVsOiAnQmFzaWMnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbGF5b3V0JyxcbiAgICAgICAgICAgIGxhYmVsOiAnTGF5b3V0JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY29sb3InLFxuICAgICAgICAgICAgbGFiZWw6ICdDb2xvcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3R5cG9ncmFwaHknLFxuICAgICAgICAgICAgbGFiZWw6ICdUeXBvZ3JhcGh5JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnaWNvbicsXG4gICAgICAgICAgICBsYWJlbDogJ0ljb24nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdidXR0b24nLFxuICAgICAgICAgICAgbGFiZWw6ICdCdXR0b24nLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJ2Zvcm0nLFxuICAgICAgICBsYWJlbDogJ0Zvcm0nLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAncmFkaW8nLFxuICAgICAgICAgICAgbGFiZWw6ICdSYWRpbycsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NoZWNrYm94JyxcbiAgICAgICAgICAgIGxhYmVsOiAnQ2hlY2tib3gnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdpbnB1dCcsXG4gICAgICAgICAgICBsYWJlbDogJ0lucHV0JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnaW5wdXQtbnVtYmVyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnSW5wdXROdW1iZXInLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdzZWxlY3QnLFxuICAgICAgICAgICAgbGFiZWw6ICdTZWxlY3QnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdjYXNjYWRlcicsXG4gICAgICAgICAgICBsYWJlbDogJ0Nhc2NhZGVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc3dpdGNoJyxcbiAgICAgICAgICAgIGxhYmVsOiAnU3dpdGNoJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc2xpZGVyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnU2xpZGVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndGltZS1waWNrZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdUaW1lUGlja2VyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnZGF0ZS1waWNrZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdEYXRlUGlja2VyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnZGF0ZXRpbWUtcGlja2VyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRGF0ZVRpbWVQaWNrZXInLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd1cGxvYWQnLFxuICAgICAgICAgICAgbGFiZWw6ICdVcGxvYWQnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdyYXRlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnUmF0ZScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2Zvcm0nLFxuICAgICAgICAgICAgbGFiZWw6ICdGb3JtJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdkYXRhJyxcbiAgICAgICAgbGFiZWw6ICdEYXRhJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RhYmxlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVGFibGUnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0YWcnLFxuICAgICAgICAgICAgbGFiZWw6ICdUYWcnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdwcm9ncmVzcycsXG4gICAgICAgICAgICBsYWJlbDogJ1Byb2dyZXNzJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndHJlZScsXG4gICAgICAgICAgICBsYWJlbDogJ1RyZWUnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdwYWdpbmF0aW9uJyxcbiAgICAgICAgICAgIGxhYmVsOiAnUGFnaW5hdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2JhZGdlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQmFkZ2UnLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJ25vdGljZScsXG4gICAgICAgIGxhYmVsOiAnTm90aWNlJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2FsZXJ0JyxcbiAgICAgICAgICAgIGxhYmVsOiAnQWxlcnQnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdsb2FkaW5nJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTG9hZGluZycsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ21lc3NhZ2UnLFxuICAgICAgICAgICAgbGFiZWw6ICdNZXNzYWdlJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbWVzc2FnZS1ib3gnLFxuICAgICAgICAgICAgbGFiZWw6ICdNZXNzYWdlQm94JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbm90aWZpY2F0aW9uJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTm90aWZpY2F0aW9uJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICduYXZpZ2F0aW9uJyxcbiAgICAgICAgbGFiZWw6ICdOYXZpZ2F0aW9uJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ21lbnUnLFxuICAgICAgICAgICAgbGFiZWw6ICdNZW51JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndGFicycsXG4gICAgICAgICAgICBsYWJlbDogJ1RhYnMnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdicmVhZGNydW1iJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQnJlYWRjcnVtYicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2Ryb3Bkb3duJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRHJvcGRvd24nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdzdGVwcycsXG4gICAgICAgICAgICBsYWJlbDogJ1N0ZXBzJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdvdGhlcnMnLFxuICAgICAgICBsYWJlbDogJ090aGVycycsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdkaWFsb2cnLFxuICAgICAgICAgICAgbGFiZWw6ICdEaWFsb2cnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0b29sdGlwJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVG9vbHRpcCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3BvcG92ZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdQb3BvdmVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY2FyZCcsXG4gICAgICAgICAgICBsYWJlbDogJ0NhcmQnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdjYXJvdXNlbCcsXG4gICAgICAgICAgICBsYWJlbDogJ0Nhcm91c2VsJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY29sbGFwc2UnLFxuICAgICAgICAgICAgbGFiZWw6ICdDb2xsYXBzZScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAncmVzb3VyY2UnLFxuICAgIGxhYmVsOiAnUmVzb3VyY2UnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnYXh1cmUnLFxuICAgICAgICBsYWJlbDogJ0F4dXJlIENvbXBvbmVudHMnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdza2V0Y2gnLFxuICAgICAgICBsYWJlbDogJ1NrZXRjaCBUZW1wbGF0ZXMnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdkb2NzJyxcbiAgICAgICAgbGFiZWw6ICdEZXNpZ24gRG9jdW1lbnRhdGlvbicsXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/cascader/any-level.vue)_

vue

```
<template>
  <div class="m-4">
    <p>Select any level of options (Single selection)</p>
    <el-cascader :options="options" :props="props1" clearable />
  </div>
  <div class="m-4">
    <p>Select any level of options (Multiple selection)</p>
    <el-cascader :options="options" :props="props2" clearable />
  </div>
</template>

<script lang="ts" setup>
const props1 = {
  checkStrictly: true,
}

const props2 = {
  multiple: true,
  checkStrictly: true,
}

const options = [
  {
    value: 'guide',
    label: 'Guide',
    children: [
      {
        value: 'disciplines',
        label: 'Disciplines',
        children: [
          {
            value: 'consistency',
            label: 'Consistency',
          },
          {
            value: 'feedback',
            label: 'Feedback',
          },
          {
            value: 'efficiency',
            label: 'Efficiency',
          },
          {
            value: 'controllability',
            label: 'Controllability',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'side nav',
            label: 'Side Navigation',
          },
          {
            value: 'top nav',
            label: 'Top Navigation',
          },
        ],
      },
    ],
  },
  {
    value: 'component',
    label: 'Component',
    children: [
      {
        value: 'basic',
        label: 'Basic',
        children: [
          {
            value: 'layout',
            label: 'Layout',
          },
          {
            value: 'color',
            label: 'Color',
          },
          {
            value: 'typography',
            label: 'Typography',
          },
          {
            value: 'icon',
            label: 'Icon',
          },
          {
            value: 'button',
            label: 'Button',
          },
        ],
      },
      {
        value: 'form',
        label: 'Form',
        children: [
          {
            value: 'radio',
            label: 'Radio',
          },
          {
            value: 'checkbox',
            label: 'Checkbox',
          },
          {
            value: 'input',
            label: 'Input',
          },
          {
            value: 'input-number',
            label: 'InputNumber',
          },
          {
            value: 'select',
            label: 'Select',
          },
          {
            value: 'cascader',
            label: 'Cascader',
          },
          {
            value: 'switch',
            label: 'Switch',
          },
          {
            value: 'slider',
            label: 'Slider',
          },
          {
            value: 'time-picker',
            label: 'TimePicker',
          },
          {
            value: 'date-picker',
            label: 'DatePicker',
          },
          {
            value: 'datetime-picker',
            label: 'DateTimePicker',
          },
          {
            value: 'upload',
            label: 'Upload',
          },
          {
            value: 'rate',
            label: 'Rate',
          },
          {
            value: 'form',
            label: 'Form',
          },
        ],
      },
      {
        value: 'data',
        label: 'Data',
        children: [
          {
            value: 'table',
            label: 'Table',
          },
          {
            value: 'tag',
            label: 'Tag',
          },
          {
            value: 'progress',
            label: 'Progress',
          },
          {
            value: 'tree',
            label: 'Tree',
          },
          {
            value: 'pagination',
            label: 'Pagination',
          },
          {
            value: 'badge',
            label: 'Badge',
          },
        ],
      },
      {
        value: 'notice',
        label: 'Notice',
        children: [
          {
            value: 'alert',
            label: 'Alert',
          },
          {
            value: 'loading',
            label: 'Loading',
          },
          {
            value: 'message',
            label: 'Message',
          },
          {
            value: 'message-box',
            label: 'MessageBox',
          },
          {
            value: 'notification',
            label: 'Notification',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'menu',
            label: 'Menu',
          },
          {
            value: 'tabs',
            label: 'Tabs',
          },
          {
            value: 'breadcrumb',
            label: 'Breadcrumb',
          },
          {
            value: 'dropdown',
            label: 'Dropdown',
          },
          {
            value: 'steps',
            label: 'Steps',
          },
        ],
      },
      {
        value: 'others',
        label: 'Others',
        children: [
          {
            value: 'dialog',
            label: 'Dialog',
          },
          {
            value: 'tooltip',
            label: 'Tooltip',
          },
          {
            value: 'popover',
            label: 'Popover',
          },
          {
            value: 'card',
            label: 'Card',
          },
          {
            value: 'carousel',
            label: 'Carousel',
          },
          {
            value: 'collapse',
            label: 'Collapse',
          },
        ],
      },
    ],
  },
  {
    value: 'resource',
    label: 'Resource',
    children: [
      {
        value: 'axure',
        label: 'Axure Components',
      },
      {
        value: 'sketch',
        label: 'Sketch Templates',
      },
      {
        value: 'docs',
        label: 'Design Documentation',
      },
    ],
  },
]
</script>
```

隐藏源代码

## 动态加载 [​](#动态加载)

当选中某一级时，动态加载该级下的选项。

通过`lazy`开启动态加载，并通过`lazyload`来设置加载数据源的方法。 `lazyload`方法有两个参数，第一个参数`node`为当前点击的节点，第二个`resolve`为数据加载完成的回调(必须调用)。 为了更准确的显示节点的状态，还可以对节点数据添加是否为叶子节点的标志位 (默认字段为`leaf`，可通过`props.leaf`修改)。 否则，将以有无子节点来判断其是否为叶子节点。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2FzY2FkZXIgOnByb3BzPVwicHJvcHNcIiAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB0eXBlIHsgQ2FzY2FkZXJQcm9wcyB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxubGV0IGlkID0gMFxuY29uc3QgcHJvcHM6IENhc2NhZGVyUHJvcHMgPSB7XG4gIGxhenk6IHRydWUsXG4gIGxhenlMb2FkKG5vZGUsIHJlc29sdmUpIHtcbiAgICBjb25zdCB7IGxldmVsIH0gPSBub2RlXG4gICAgc2V0VGltZW91dCgoKSA9PiB7XG4gICAgICBjb25zdCBub2RlcyA9IEFycmF5LmZyb20oeyBsZW5ndGg6IGxldmVsICsgMSB9KS5tYXAoKGl0ZW0pID0+ICh7XG4gICAgICAgIHZhbHVlOiArK2lkLFxuICAgICAgICBsYWJlbDogYE9wdGlvbiAtICR7aWR9YCxcbiAgICAgICAgbGVhZjogbGV2ZWwgPj0gMixcbiAgICAgIH0pKVxuICAgICAgLy8gSW52b2tlIGByZXNvbHZlYCBjYWxsYmFjayB0byByZXR1cm4gdGhlIGNoaWxkIG5vZGVzIGRhdGEgYW5kIGluZGljYXRlIHRoZSBsb2FkaW5nIGlzIGZpbmlzaGVkLlxuICAgICAgcmVzb2x2ZShub2RlcylcbiAgICB9LCAxMDAwKVxuICB9LFxufVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/cascader/dynamic-loading.vue)_

vue

```
<template>
  <el-cascader :props="props" />
</template>

<script lang="ts" setup>
import type { CascaderProps } from 'element-plus'

let id = 0
const props: CascaderProps = {
  lazy: true,
  lazyLoad(node, resolve) {
    const { level } = node
    setTimeout(() => {
      const nodes = Array.from({ length: level + 1 }).map((item) => ({
        value: ++id,
        label: `Option - ${id}`,
        leaf: level >= 2,
      }))
      // Invoke `resolve` callback to return the child nodes data and indicate the loading is finished.
      resolve(nodes)
    }, 1000)
  },
}
</script>
```

隐藏源代码

## 可搜索 [​](#可搜索)

可以快捷地搜索选项并选择。

通过添加`filterable`来启用过滤。 Cascader 会匹配所有节点的标签和它们的亲节点的标签，是否包含有输入的关键字。 你也可以用`filter-method`自定义搜索逻辑，接受一个函数，第一个参数是节点`node`，第二个参数是搜索关键词`keyword`，通过返回布尔值表示是否命中。

Filterable (Single selection)

Filterable (Multiple selection)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgPHA+RmlsdGVyYWJsZSAoU2luZ2xlIHNlbGVjdGlvbik8L3A+XG4gICAgPGVsLWNhc2NhZGVyXG4gICAgICBwbGFjZWhvbGRlcj1cIlRyeSBzZWFyY2hpbmdMIEd1aWRlXCJcbiAgICAgIDpvcHRpb25zPVwib3B0aW9uc1wiXG4gICAgICBmaWx0ZXJhYmxlXG4gICAgLz5cbiAgPC9kaXY+XG4gIDxkaXYgY2xhc3M9XCJtLTRcIj5cbiAgICA8cD5GaWx0ZXJhYmxlIChNdWx0aXBsZSBzZWxlY3Rpb24pPC9wPlxuICAgIDxlbC1jYXNjYWRlclxuICAgICAgcGxhY2Vob2xkZXI9XCJUcnkgc2VhcmNoaW5nTCBHdWlkZVwiXG4gICAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgICAgOnByb3BzPVwicHJvcHNcIlxuICAgICAgZmlsdGVyYWJsZVxuICAgIC8+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmNvbnN0IHByb3BzID0ge1xuICBtdWx0aXBsZTogdHJ1ZSxcbn1cblxuY29uc3Qgb3B0aW9ucyA9IFtcbiAge1xuICAgIHZhbHVlOiAnZ3VpZGUnLFxuICAgIGxhYmVsOiAnR3VpZGUnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnZGlzY2lwbGluZXMnLFxuICAgICAgICBsYWJlbDogJ0Rpc2NpcGxpbmVzJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NvbnNpc3RlbmN5JyxcbiAgICAgICAgICAgIGxhYmVsOiAnQ29uc2lzdGVuY3knLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdmZWVkYmFjaycsXG4gICAgICAgICAgICBsYWJlbDogJ0ZlZWRiYWNrJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnZWZmaWNpZW5jeScsXG4gICAgICAgICAgICBsYWJlbDogJ0VmZmljaWVuY3knLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdjb250cm9sbGFiaWxpdHknLFxuICAgICAgICAgICAgbGFiZWw6ICdDb250cm9sbGFiaWxpdHknLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJ25hdmlnYXRpb24nLFxuICAgICAgICBsYWJlbDogJ05hdmlnYXRpb24nLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc2lkZSBuYXYnLFxuICAgICAgICAgICAgbGFiZWw6ICdTaWRlIE5hdmlnYXRpb24nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0b3AgbmF2JyxcbiAgICAgICAgICAgIGxhYmVsOiAnVG9wIE5hdmlnYXRpb24nLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ2NvbXBvbmVudCcsXG4gICAgbGFiZWw6ICdDb21wb25lbnQnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnYmFzaWMnLFxuICAgICAgICBsYWJlbDogJ0Jhc2ljJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2xheW91dCcsXG4gICAgICAgICAgICBsYWJlbDogJ0xheW91dCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NvbG9yJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQ29sb3InLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0eXBvZ3JhcGh5JyxcbiAgICAgICAgICAgIGxhYmVsOiAnVHlwb2dyYXBoeScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2ljb24nLFxuICAgICAgICAgICAgbGFiZWw6ICdJY29uJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnYnV0dG9uJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQnV0dG9uJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdmb3JtJyxcbiAgICAgICAgbGFiZWw6ICdGb3JtJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3JhZGlvJyxcbiAgICAgICAgICAgIGxhYmVsOiAnUmFkaW8nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdjaGVja2JveCcsXG4gICAgICAgICAgICBsYWJlbDogJ0NoZWNrYm94JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnaW5wdXQnLFxuICAgICAgICAgICAgbGFiZWw6ICdJbnB1dCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2lucHV0LW51bWJlcicsXG4gICAgICAgICAgICBsYWJlbDogJ0lucHV0TnVtYmVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc2VsZWN0JyxcbiAgICAgICAgICAgIGxhYmVsOiAnU2VsZWN0JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY2FzY2FkZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdDYXNjYWRlcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3N3aXRjaCcsXG4gICAgICAgICAgICBsYWJlbDogJ1N3aXRjaCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3NsaWRlcicsXG4gICAgICAgICAgICBsYWJlbDogJ1NsaWRlcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RpbWUtcGlja2VyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVGltZVBpY2tlcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2RhdGUtcGlja2VyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRGF0ZVBpY2tlcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2RhdGV0aW1lLXBpY2tlcicsXG4gICAgICAgICAgICBsYWJlbDogJ0RhdGVUaW1lUGlja2VyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndXBsb2FkJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVXBsb2FkJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAncmF0ZScsXG4gICAgICAgICAgICBsYWJlbDogJ1JhdGUnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdmb3JtJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRm9ybScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnZGF0YScsXG4gICAgICAgIGxhYmVsOiAnRGF0YScsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0YWJsZScsXG4gICAgICAgICAgICBsYWJlbDogJ1RhYmxlJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndGFnJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVGFnJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAncHJvZ3Jlc3MnLFxuICAgICAgICAgICAgbGFiZWw6ICdQcm9ncmVzcycsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RyZWUnLFxuICAgICAgICAgICAgbGFiZWw6ICdUcmVlJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAncGFnaW5hdGlvbicsXG4gICAgICAgICAgICBsYWJlbDogJ1BhZ2luYXRpb24nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdiYWRnZScsXG4gICAgICAgICAgICBsYWJlbDogJ0JhZGdlJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdub3RpY2UnLFxuICAgICAgICBsYWJlbDogJ05vdGljZScsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdhbGVydCcsXG4gICAgICAgICAgICBsYWJlbDogJ0FsZXJ0JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbG9hZGluZycsXG4gICAgICAgICAgICBsYWJlbDogJ0xvYWRpbmcnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdtZXNzYWdlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTWVzc2FnZScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ21lc3NhZ2UtYm94JyxcbiAgICAgICAgICAgIGxhYmVsOiAnTWVzc2FnZUJveCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ25vdGlmaWNhdGlvbicsXG4gICAgICAgICAgICBsYWJlbDogJ05vdGlmaWNhdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnbmF2aWdhdGlvbicsXG4gICAgICAgIGxhYmVsOiAnTmF2aWdhdGlvbicsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdtZW51JyxcbiAgICAgICAgICAgIGxhYmVsOiAnTWVudScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RhYnMnLFxuICAgICAgICAgICAgbGFiZWw6ICdUYWJzJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnYnJlYWRjcnVtYicsXG4gICAgICAgICAgICBsYWJlbDogJ0JyZWFkY3J1bWInLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdkcm9wZG93bicsXG4gICAgICAgICAgICBsYWJlbDogJ0Ryb3Bkb3duJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc3RlcHMnLFxuICAgICAgICAgICAgbGFiZWw6ICdTdGVwcycsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnb3RoZXJzJyxcbiAgICAgICAgbGFiZWw6ICdPdGhlcnMnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnZGlhbG9nJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRGlhbG9nJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndG9vbHRpcCcsXG4gICAgICAgICAgICBsYWJlbDogJ1Rvb2x0aXAnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdwb3BvdmVyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnUG9wb3ZlcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NhcmQnLFxuICAgICAgICAgICAgbGFiZWw6ICdDYXJkJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY2Fyb3VzZWwnLFxuICAgICAgICAgICAgbGFiZWw6ICdDYXJvdXNlbCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NvbGxhcHNlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQ29sbGFwc2UnLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ3Jlc291cmNlJyxcbiAgICBsYWJlbDogJ1Jlc291cmNlJyxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICB2YWx1ZTogJ2F4dXJlJyxcbiAgICAgICAgbGFiZWw6ICdBeHVyZSBDb21wb25lbnRzJyxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnc2tldGNoJyxcbiAgICAgICAgbGFiZWw6ICdTa2V0Y2ggVGVtcGxhdGVzJyxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnZG9jcycsXG4gICAgICAgIGxhYmVsOiAnRGVzaWduIERvY3VtZW50YXRpb24nLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/cascader/filterable.vue)_

vue

```
<template>
  <div class="m-4">
    <p>Filterable (Single selection)</p>
    <el-cascader
      placeholder="Try searchingL Guide"
      :options="options"
      filterable
    />
  </div>
  <div class="m-4">
    <p>Filterable (Multiple selection)</p>
    <el-cascader
      placeholder="Try searchingL Guide"
      :options="options"
      :props="props"
      filterable
    />
  </div>
</template>

<script lang="ts" setup>
const props = {
  multiple: true,
}

const options = [
  {
    value: 'guide',
    label: 'Guide',
    children: [
      {
        value: 'disciplines',
        label: 'Disciplines',
        children: [
          {
            value: 'consistency',
            label: 'Consistency',
          },
          {
            value: 'feedback',
            label: 'Feedback',
          },
          {
            value: 'efficiency',
            label: 'Efficiency',
          },
          {
            value: 'controllability',
            label: 'Controllability',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'side nav',
            label: 'Side Navigation',
          },
          {
            value: 'top nav',
            label: 'Top Navigation',
          },
        ],
      },
    ],
  },
  {
    value: 'component',
    label: 'Component',
    children: [
      {
        value: 'basic',
        label: 'Basic',
        children: [
          {
            value: 'layout',
            label: 'Layout',
          },
          {
            value: 'color',
            label: 'Color',
          },
          {
            value: 'typography',
            label: 'Typography',
          },
          {
            value: 'icon',
            label: 'Icon',
          },
          {
            value: 'button',
            label: 'Button',
          },
        ],
      },
      {
        value: 'form',
        label: 'Form',
        children: [
          {
            value: 'radio',
            label: 'Radio',
          },
          {
            value: 'checkbox',
            label: 'Checkbox',
          },
          {
            value: 'input',
            label: 'Input',
          },
          {
            value: 'input-number',
            label: 'InputNumber',
          },
          {
            value: 'select',
            label: 'Select',
          },
          {
            value: 'cascader',
            label: 'Cascader',
          },
          {
            value: 'switch',
            label: 'Switch',
          },
          {
            value: 'slider',
            label: 'Slider',
          },
          {
            value: 'time-picker',
            label: 'TimePicker',
          },
          {
            value: 'date-picker',
            label: 'DatePicker',
          },
          {
            value: 'datetime-picker',
            label: 'DateTimePicker',
          },
          {
            value: 'upload',
            label: 'Upload',
          },
          {
            value: 'rate',
            label: 'Rate',
          },
          {
            value: 'form',
            label: 'Form',
          },
        ],
      },
      {
        value: 'data',
        label: 'Data',
        children: [
          {
            value: 'table',
            label: 'Table',
          },
          {
            value: 'tag',
            label: 'Tag',
          },
          {
            value: 'progress',
            label: 'Progress',
          },
          {
            value: 'tree',
            label: 'Tree',
          },
          {
            value: 'pagination',
            label: 'Pagination',
          },
          {
            value: 'badge',
            label: 'Badge',
          },
        ],
      },
      {
        value: 'notice',
        label: 'Notice',
        children: [
          {
            value: 'alert',
            label: 'Alert',
          },
          {
            value: 'loading',
            label: 'Loading',
          },
          {
            value: 'message',
            label: 'Message',
          },
          {
            value: 'message-box',
            label: 'MessageBox',
          },
          {
            value: 'notification',
            label: 'Notification',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'menu',
            label: 'Menu',
          },
          {
            value: 'tabs',
            label: 'Tabs',
          },
          {
            value: 'breadcrumb',
            label: 'Breadcrumb',
          },
          {
            value: 'dropdown',
            label: 'Dropdown',
          },
          {
            value: 'steps',
            label: 'Steps',
          },
        ],
      },
      {
        value: 'others',
        label: 'Others',
        children: [
          {
            value: 'dialog',
            label: 'Dialog',
          },
          {
            value: 'tooltip',
            label: 'Tooltip',
          },
          {
            value: 'popover',
            label: 'Popover',
          },
          {
            value: 'card',
            label: 'Card',
          },
          {
            value: 'carousel',
            label: 'Carousel',
          },
          {
            value: 'collapse',
            label: 'Collapse',
          },
        ],
      },
    ],
  },
  {
    value: 'resource',
    label: 'Resource',
    children: [
      {
        value: 'axure',
        label: 'Axure Components',
      },
      {
        value: 'sketch',
        label: 'Sketch Templates',
      },
      {
        value: 'docs',
        label: 'Design Documentation',
      },
    ],
  },
]
</script>
```

隐藏源代码

## 自定义节点内容 [​](#自定义节点内容)

可以自定义备选项的节点内容

你可以通过 `scoped slot` 自定义节点的内容。 您可以访问 scope 中的 `node` 和 `data` 属性，分别表示当前节点的 Node 对象和当前节点的数据。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2FzY2FkZXIgOm9wdGlvbnM9XCJvcHRpb25zXCI+XG4gICAgPHRlbXBsYXRlICNkZWZhdWx0PVwieyBub2RlLCBkYXRhIH1cIj5cbiAgICAgIDxzcGFuPnt7IGRhdGEubGFiZWwgfX08L3NwYW4+XG4gICAgICA8c3BhbiB2LWlmPVwiIW5vZGUuaXNMZWFmXCI+ICh7eyBkYXRhLmNoaWxkcmVuLmxlbmd0aCB9fSkgPC9zcGFuPlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtY2FzY2FkZXI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuY29uc3Qgb3B0aW9ucyA9IFtcbiAge1xuICAgIHZhbHVlOiAnZ3VpZGUnLFxuICAgIGxhYmVsOiAnR3VpZGUnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnZGlzY2lwbGluZXMnLFxuICAgICAgICBsYWJlbDogJ0Rpc2NpcGxpbmVzJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NvbnNpc3RlbmN5JyxcbiAgICAgICAgICAgIGxhYmVsOiAnQ29uc2lzdGVuY3knLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdmZWVkYmFjaycsXG4gICAgICAgICAgICBsYWJlbDogJ0ZlZWRiYWNrJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnZWZmaWNpZW5jeScsXG4gICAgICAgICAgICBsYWJlbDogJ0VmZmljaWVuY3knLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdjb250cm9sbGFiaWxpdHknLFxuICAgICAgICAgICAgbGFiZWw6ICdDb250cm9sbGFiaWxpdHknLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJ25hdmlnYXRpb24nLFxuICAgICAgICBsYWJlbDogJ05hdmlnYXRpb24nLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc2lkZSBuYXYnLFxuICAgICAgICAgICAgbGFiZWw6ICdTaWRlIE5hdmlnYXRpb24nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0b3AgbmF2JyxcbiAgICAgICAgICAgIGxhYmVsOiAnVG9wIE5hdmlnYXRpb24nLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ2NvbXBvbmVudCcsXG4gICAgbGFiZWw6ICdDb21wb25lbnQnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnYmFzaWMnLFxuICAgICAgICBsYWJlbDogJ0Jhc2ljJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2xheW91dCcsXG4gICAgICAgICAgICBsYWJlbDogJ0xheW91dCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NvbG9yJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQ29sb3InLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0eXBvZ3JhcGh5JyxcbiAgICAgICAgICAgIGxhYmVsOiAnVHlwb2dyYXBoeScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2ljb24nLFxuICAgICAgICAgICAgbGFiZWw6ICdJY29uJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnYnV0dG9uJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQnV0dG9uJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdmb3JtJyxcbiAgICAgICAgbGFiZWw6ICdGb3JtJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3JhZGlvJyxcbiAgICAgICAgICAgIGxhYmVsOiAnUmFkaW8nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdjaGVja2JveCcsXG4gICAgICAgICAgICBsYWJlbDogJ0NoZWNrYm94JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnaW5wdXQnLFxuICAgICAgICAgICAgbGFiZWw6ICdJbnB1dCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2lucHV0LW51bWJlcicsXG4gICAgICAgICAgICBsYWJlbDogJ0lucHV0TnVtYmVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc2VsZWN0JyxcbiAgICAgICAgICAgIGxhYmVsOiAnU2VsZWN0JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY2FzY2FkZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdDYXNjYWRlcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3N3aXRjaCcsXG4gICAgICAgICAgICBsYWJlbDogJ1N3aXRjaCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3NsaWRlcicsXG4gICAgICAgICAgICBsYWJlbDogJ1NsaWRlcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RpbWUtcGlja2VyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVGltZVBpY2tlcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2RhdGUtcGlja2VyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRGF0ZVBpY2tlcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2RhdGV0aW1lLXBpY2tlcicsXG4gICAgICAgICAgICBsYWJlbDogJ0RhdGVUaW1lUGlja2VyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndXBsb2FkJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVXBsb2FkJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAncmF0ZScsXG4gICAgICAgICAgICBsYWJlbDogJ1JhdGUnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdmb3JtJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRm9ybScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnZGF0YScsXG4gICAgICAgIGxhYmVsOiAnRGF0YScsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0YWJsZScsXG4gICAgICAgICAgICBsYWJlbDogJ1RhYmxlJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndGFnJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVGFnJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAncHJvZ3Jlc3MnLFxuICAgICAgICAgICAgbGFiZWw6ICdQcm9ncmVzcycsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RyZWUnLFxuICAgICAgICAgICAgbGFiZWw6ICdUcmVlJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAncGFnaW5hdGlvbicsXG4gICAgICAgICAgICBsYWJlbDogJ1BhZ2luYXRpb24nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdiYWRnZScsXG4gICAgICAgICAgICBsYWJlbDogJ0JhZGdlJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdub3RpY2UnLFxuICAgICAgICBsYWJlbDogJ05vdGljZScsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdhbGVydCcsXG4gICAgICAgICAgICBsYWJlbDogJ0FsZXJ0JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbG9hZGluZycsXG4gICAgICAgICAgICBsYWJlbDogJ0xvYWRpbmcnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdtZXNzYWdlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTWVzc2FnZScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ21lc3NhZ2UtYm94JyxcbiAgICAgICAgICAgIGxhYmVsOiAnTWVzc2FnZUJveCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ25vdGlmaWNhdGlvbicsXG4gICAgICAgICAgICBsYWJlbDogJ05vdGlmaWNhdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnbmF2aWdhdGlvbicsXG4gICAgICAgIGxhYmVsOiAnTmF2aWdhdGlvbicsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdtZW51JyxcbiAgICAgICAgICAgIGxhYmVsOiAnTWVudScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RhYnMnLFxuICAgICAgICAgICAgbGFiZWw6ICdUYWJzJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnYnJlYWRjcnVtYicsXG4gICAgICAgICAgICBsYWJlbDogJ0JyZWFkY3J1bWInLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdkcm9wZG93bicsXG4gICAgICAgICAgICBsYWJlbDogJ0Ryb3Bkb3duJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc3RlcHMnLFxuICAgICAgICAgICAgbGFiZWw6ICdTdGVwcycsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnb3RoZXJzJyxcbiAgICAgICAgbGFiZWw6ICdPdGhlcnMnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnZGlhbG9nJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRGlhbG9nJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndG9vbHRpcCcsXG4gICAgICAgICAgICBsYWJlbDogJ1Rvb2x0aXAnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdwb3BvdmVyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnUG9wb3ZlcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NhcmQnLFxuICAgICAgICAgICAgbGFiZWw6ICdDYXJkJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY2Fyb3VzZWwnLFxuICAgICAgICAgICAgbGFiZWw6ICdDYXJvdXNlbCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NvbGxhcHNlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQ29sbGFwc2UnLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ3Jlc291cmNlJyxcbiAgICBsYWJlbDogJ1Jlc291cmNlJyxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICB2YWx1ZTogJ2F4dXJlJyxcbiAgICAgICAgbGFiZWw6ICdBeHVyZSBDb21wb25lbnRzJyxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnc2tldGNoJyxcbiAgICAgICAgbGFiZWw6ICdTa2V0Y2ggVGVtcGxhdGVzJyxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnZG9jcycsXG4gICAgICAgIGxhYmVsOiAnRGVzaWduIERvY3VtZW50YXRpb24nLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/cascader/custom-content.vue)_

vue

```
<template>
  <el-cascader :options="options">
    <template #default="{ node, data }">
      <span>{{ data.label }}</span>
      <span v-if="!node.isLeaf"> ({{ data.children.length }}) </span>
    </template>
  </el-cascader>
</template>

<script lang="ts" setup>
const options = [
  {
    value: 'guide',
    label: 'Guide',
    children: [
      {
        value: 'disciplines',
        label: 'Disciplines',
        children: [
          {
            value: 'consistency',
            label: 'Consistency',
          },
          {
            value: 'feedback',
            label: 'Feedback',
          },
          {
            value: 'efficiency',
            label: 'Efficiency',
          },
          {
            value: 'controllability',
            label: 'Controllability',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'side nav',
            label: 'Side Navigation',
          },
          {
            value: 'top nav',
            label: 'Top Navigation',
          },
        ],
      },
    ],
  },
  {
    value: 'component',
    label: 'Component',
    children: [
      {
        value: 'basic',
        label: 'Basic',
        children: [
          {
            value: 'layout',
            label: 'Layout',
          },
          {
            value: 'color',
            label: 'Color',
          },
          {
            value: 'typography',
            label: 'Typography',
          },
          {
            value: 'icon',
            label: 'Icon',
          },
          {
            value: 'button',
            label: 'Button',
          },
        ],
      },
      {
        value: 'form',
        label: 'Form',
        children: [
          {
            value: 'radio',
            label: 'Radio',
          },
          {
            value: 'checkbox',
            label: 'Checkbox',
          },
          {
            value: 'input',
            label: 'Input',
          },
          {
            value: 'input-number',
            label: 'InputNumber',
          },
          {
            value: 'select',
            label: 'Select',
          },
          {
            value: 'cascader',
            label: 'Cascader',
          },
          {
            value: 'switch',
            label: 'Switch',
          },
          {
            value: 'slider',
            label: 'Slider',
          },
          {
            value: 'time-picker',
            label: 'TimePicker',
          },
          {
            value: 'date-picker',
            label: 'DatePicker',
          },
          {
            value: 'datetime-picker',
            label: 'DateTimePicker',
          },
          {
            value: 'upload',
            label: 'Upload',
          },
          {
            value: 'rate',
            label: 'Rate',
          },
          {
            value: 'form',
            label: 'Form',
          },
        ],
      },
      {
        value: 'data',
        label: 'Data',
        children: [
          {
            value: 'table',
            label: 'Table',
          },
          {
            value: 'tag',
            label: 'Tag',
          },
          {
            value: 'progress',
            label: 'Progress',
          },
          {
            value: 'tree',
            label: 'Tree',
          },
          {
            value: 'pagination',
            label: 'Pagination',
          },
          {
            value: 'badge',
            label: 'Badge',
          },
        ],
      },
      {
        value: 'notice',
        label: 'Notice',
        children: [
          {
            value: 'alert',
            label: 'Alert',
          },
          {
            value: 'loading',
            label: 'Loading',
          },
          {
            value: 'message',
            label: 'Message',
          },
          {
            value: 'message-box',
            label: 'MessageBox',
          },
          {
            value: 'notification',
            label: 'Notification',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'menu',
            label: 'Menu',
          },
          {
            value: 'tabs',
            label: 'Tabs',
          },
          {
            value: 'breadcrumb',
            label: 'Breadcrumb',
          },
          {
            value: 'dropdown',
            label: 'Dropdown',
          },
          {
            value: 'steps',
            label: 'Steps',
          },
        ],
      },
      {
        value: 'others',
        label: 'Others',
        children: [
          {
            value: 'dialog',
            label: 'Dialog',
          },
          {
            value: 'tooltip',
            label: 'Tooltip',
          },
          {
            value: 'popover',
            label: 'Popover',
          },
          {
            value: 'card',
            label: 'Card',
          },
          {
            value: 'carousel',
            label: 'Carousel',
          },
          {
            value: 'collapse',
            label: 'Collapse',
          },
        ],
      },
    ],
  },
  {
    value: 'resource',
    label: 'Resource',
    children: [
      {
        value: 'axure',
        label: 'Axure Components',
      },
      {
        value: 'sketch',
        label: 'Sketch Templates',
      },
      {
        value: 'docs',
        label: 'Design Documentation',
      },
    ],
  },
]
</script>
```

隐藏源代码

## 自定义建议项2.9.5 [​](#自定义建议项)

你可以通过 `suggestion-item` 插槽自定义建议项。 你可以在作用域中访问 `item`，它代表建议项。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2FzY2FkZXIgOm9wdGlvbnM9XCJvcHRpb25zXCIgZmlsdGVyYWJsZSBwbGFjZWhvbGRlcj1cIlRyeSBzZWFyY2hpbmc6IEd1aWRlXCI+XG4gICAgPHRlbXBsYXRlICNzdWdnZXN0aW9uLWl0ZW09XCJ7IGl0ZW0gfVwiPlxuICAgICAgPHNwYW4+8J+UjSB7eyBpdGVtLnBhdGhMYWJlbHMuam9pbignID4gJykgfX08L3NwYW4+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC1jYXNjYWRlcj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5jb25zdCBvcHRpb25zID0gW1xuICB7XG4gICAgdmFsdWU6ICdndWlkZScsXG4gICAgbGFiZWw6ICdHdWlkZScsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdkaXNjaXBsaW5lcycsXG4gICAgICAgIGxhYmVsOiAnRGlzY2lwbGluZXMnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY29uc2lzdGVuY3knLFxuICAgICAgICAgICAgbGFiZWw6ICdDb25zaXN0ZW5jeScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2ZlZWRiYWNrJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRmVlZGJhY2snLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdlZmZpY2llbmN5JyxcbiAgICAgICAgICAgIGxhYmVsOiAnRWZmaWNpZW5jeScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NvbnRyb2xsYWJpbGl0eScsXG4gICAgICAgICAgICBsYWJlbDogJ0NvbnRyb2xsYWJpbGl0eScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnbmF2aWdhdGlvbicsXG4gICAgICAgIGxhYmVsOiAnTmF2aWdhdGlvbicsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdzaWRlIG5hdicsXG4gICAgICAgICAgICBsYWJlbDogJ1NpZGUgTmF2aWdhdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RvcCBuYXYnLFxuICAgICAgICAgICAgbGFiZWw6ICdUb3AgTmF2aWdhdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnY29tcG9uZW50JyxcbiAgICBsYWJlbDogJ0NvbXBvbmVudCcsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdiYXNpYycsXG4gICAgICAgIGxhYmVsOiAnQmFzaWMnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbGF5b3V0JyxcbiAgICAgICAgICAgIGxhYmVsOiAnTGF5b3V0JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY29sb3InLFxuICAgICAgICAgICAgbGFiZWw6ICdDb2xvcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3R5cG9ncmFwaHknLFxuICAgICAgICAgICAgbGFiZWw6ICdUeXBvZ3JhcGh5JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnaWNvbicsXG4gICAgICAgICAgICBsYWJlbDogJ0ljb24nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdidXR0b24nLFxuICAgICAgICAgICAgbGFiZWw6ICdCdXR0b24nLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJ2Zvcm0nLFxuICAgICAgICBsYWJlbDogJ0Zvcm0nLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAncmFkaW8nLFxuICAgICAgICAgICAgbGFiZWw6ICdSYWRpbycsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NoZWNrYm94JyxcbiAgICAgICAgICAgIGxhYmVsOiAnQ2hlY2tib3gnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdpbnB1dCcsXG4gICAgICAgICAgICBsYWJlbDogJ0lucHV0JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnaW5wdXQtbnVtYmVyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnSW5wdXROdW1iZXInLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdzZWxlY3QnLFxuICAgICAgICAgICAgbGFiZWw6ICdTZWxlY3QnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdjYXNjYWRlcicsXG4gICAgICAgICAgICBsYWJlbDogJ0Nhc2NhZGVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc3dpdGNoJyxcbiAgICAgICAgICAgIGxhYmVsOiAnU3dpdGNoJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc2xpZGVyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnU2xpZGVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndGltZS1waWNrZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdUaW1lUGlja2VyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnZGF0ZS1waWNrZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdEYXRlUGlja2VyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnZGF0ZXRpbWUtcGlja2VyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRGF0ZVRpbWVQaWNrZXInLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd1cGxvYWQnLFxuICAgICAgICAgICAgbGFiZWw6ICdVcGxvYWQnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdyYXRlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnUmF0ZScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2Zvcm0nLFxuICAgICAgICAgICAgbGFiZWw6ICdGb3JtJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdkYXRhJyxcbiAgICAgICAgbGFiZWw6ICdEYXRhJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RhYmxlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVGFibGUnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0YWcnLFxuICAgICAgICAgICAgbGFiZWw6ICdUYWcnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdwcm9ncmVzcycsXG4gICAgICAgICAgICBsYWJlbDogJ1Byb2dyZXNzJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndHJlZScsXG4gICAgICAgICAgICBsYWJlbDogJ1RyZWUnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdwYWdpbmF0aW9uJyxcbiAgICAgICAgICAgIGxhYmVsOiAnUGFnaW5hdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2JhZGdlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQmFkZ2UnLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJ25vdGljZScsXG4gICAgICAgIGxhYmVsOiAnTm90aWNlJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2FsZXJ0JyxcbiAgICAgICAgICAgIGxhYmVsOiAnQWxlcnQnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdsb2FkaW5nJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTG9hZGluZycsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ21lc3NhZ2UnLFxuICAgICAgICAgICAgbGFiZWw6ICdNZXNzYWdlJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbWVzc2FnZS1ib3gnLFxuICAgICAgICAgICAgbGFiZWw6ICdNZXNzYWdlQm94JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbm90aWZpY2F0aW9uJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTm90aWZpY2F0aW9uJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICduYXZpZ2F0aW9uJyxcbiAgICAgICAgbGFiZWw6ICdOYXZpZ2F0aW9uJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ21lbnUnLFxuICAgICAgICAgICAgbGFiZWw6ICdNZW51JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndGFicycsXG4gICAgICAgICAgICBsYWJlbDogJ1RhYnMnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdicmVhZGNydW1iJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQnJlYWRjcnVtYicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2Ryb3Bkb3duJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRHJvcGRvd24nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdzdGVwcycsXG4gICAgICAgICAgICBsYWJlbDogJ1N0ZXBzJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdvdGhlcnMnLFxuICAgICAgICBsYWJlbDogJ090aGVycycsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdkaWFsb2cnLFxuICAgICAgICAgICAgbGFiZWw6ICdEaWFsb2cnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0b29sdGlwJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVG9vbHRpcCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3BvcG92ZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdQb3BvdmVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY2FyZCcsXG4gICAgICAgICAgICBsYWJlbDogJ0NhcmQnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdjYXJvdXNlbCcsXG4gICAgICAgICAgICBsYWJlbDogJ0Nhcm91c2VsJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY29sbGFwc2UnLFxuICAgICAgICAgICAgbGFiZWw6ICdDb2xsYXBzZScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAncmVzb3VyY2UnLFxuICAgIGxhYmVsOiAnUmVzb3VyY2UnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnYXh1cmUnLFxuICAgICAgICBsYWJlbDogJ0F4dXJlIENvbXBvbmVudHMnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdza2V0Y2gnLFxuICAgICAgICBsYWJlbDogJ1NrZXRjaCBUZW1wbGF0ZXMnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdkb2NzJyxcbiAgICAgICAgbGFiZWw6ICdEZXNpZ24gRG9jdW1lbnRhdGlvbicsXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/cascader/custom-suggestion-item.vue)_

vue

```
<template>
  <el-cascader :options="options" filterable placeholder="Try searching: Guide">
    <template #suggestion-item="{ item }">
      <span>🔍 {{ item.pathLabels.join(' > ') }}</span>
    </template>
  </el-cascader>
</template>

<script lang="ts" setup>
const options = [
  {
    value: 'guide',
    label: 'Guide',
    children: [
      {
        value: 'disciplines',
        label: 'Disciplines',
        children: [
          {
            value: 'consistency',
            label: 'Consistency',
          },
          {
            value: 'feedback',
            label: 'Feedback',
          },
          {
            value: 'efficiency',
            label: 'Efficiency',
          },
          {
            value: 'controllability',
            label: 'Controllability',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'side nav',
            label: 'Side Navigation',
          },
          {
            value: 'top nav',
            label: 'Top Navigation',
          },
        ],
      },
    ],
  },
  {
    value: 'component',
    label: 'Component',
    children: [
      {
        value: 'basic',
        label: 'Basic',
        children: [
          {
            value: 'layout',
            label: 'Layout',
          },
          {
            value: 'color',
            label: 'Color',
          },
          {
            value: 'typography',
            label: 'Typography',
          },
          {
            value: 'icon',
            label: 'Icon',
          },
          {
            value: 'button',
            label: 'Button',
          },
        ],
      },
      {
        value: 'form',
        label: 'Form',
        children: [
          {
            value: 'radio',
            label: 'Radio',
          },
          {
            value: 'checkbox',
            label: 'Checkbox',
          },
          {
            value: 'input',
            label: 'Input',
          },
          {
            value: 'input-number',
            label: 'InputNumber',
          },
          {
            value: 'select',
            label: 'Select',
          },
          {
            value: 'cascader',
            label: 'Cascader',
          },
          {
            value: 'switch',
            label: 'Switch',
          },
          {
            value: 'slider',
            label: 'Slider',
          },
          {
            value: 'time-picker',
            label: 'TimePicker',
          },
          {
            value: 'date-picker',
            label: 'DatePicker',
          },
          {
            value: 'datetime-picker',
            label: 'DateTimePicker',
          },
          {
            value: 'upload',
            label: 'Upload',
          },
          {
            value: 'rate',
            label: 'Rate',
          },
          {
            value: 'form',
            label: 'Form',
          },
        ],
      },
      {
        value: 'data',
        label: 'Data',
        children: [
          {
            value: 'table',
            label: 'Table',
          },
          {
            value: 'tag',
            label: 'Tag',
          },
          {
            value: 'progress',
            label: 'Progress',
          },
          {
            value: 'tree',
            label: 'Tree',
          },
          {
            value: 'pagination',
            label: 'Pagination',
          },
          {
            value: 'badge',
            label: 'Badge',
          },
        ],
      },
      {
        value: 'notice',
        label: 'Notice',
        children: [
          {
            value: 'alert',
            label: 'Alert',
          },
          {
            value: 'loading',
            label: 'Loading',
          },
          {
            value: 'message',
            label: 'Message',
          },
          {
            value: 'message-box',
            label: 'MessageBox',
          },
          {
            value: 'notification',
            label: 'Notification',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'menu',
            label: 'Menu',
          },
          {
            value: 'tabs',
            label: 'Tabs',
          },
          {
            value: 'breadcrumb',
            label: 'Breadcrumb',
          },
          {
            value: 'dropdown',
            label: 'Dropdown',
          },
          {
            value: 'steps',
            label: 'Steps',
          },
        ],
      },
      {
        value: 'others',
        label: 'Others',
        children: [
          {
            value: 'dialog',
            label: 'Dialog',
          },
          {
            value: 'tooltip',
            label: 'Tooltip',
          },
          {
            value: 'popover',
            label: 'Popover',
          },
          {
            value: 'card',
            label: 'Card',
          },
          {
            value: 'carousel',
            label: 'Carousel',
          },
          {
            value: 'collapse',
            label: 'Collapse',
          },
        ],
      },
    ],
  },
  {
    value: 'resource',
    label: 'Resource',
    children: [
      {
        value: 'axure',
        label: 'Axure Components',
      },
      {
        value: 'sketch',
        label: 'Sketch Templates',
      },
      {
        value: 'docs',
        label: 'Design Documentation',
      },
    ],
  },
]
</script>
```

隐藏源代码

## 级联面板 [​](#级联面板)

级联面板是级联选择器的核心组件，与级联选择器一样，有单选、多选、动态加载等多种功能。

和级联选择器一样，通过 `options` 来指定选项，也可通过 `props` 来设置多选、动态加载等功能，具体详情见下方API表格。

-   Guide
-   Component
-   Resource

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2FzY2FkZXItcGFuZWwgOm9wdGlvbnM9XCJvcHRpb25zXCIgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5jb25zdCBvcHRpb25zID0gW1xuICB7XG4gICAgdmFsdWU6ICdndWlkZScsXG4gICAgbGFiZWw6ICdHdWlkZScsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdkaXNjaXBsaW5lcycsXG4gICAgICAgIGxhYmVsOiAnRGlzY2lwbGluZXMnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY29uc2lzdGVuY3knLFxuICAgICAgICAgICAgbGFiZWw6ICdDb25zaXN0ZW5jeScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2ZlZWRiYWNrJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRmVlZGJhY2snLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdlZmZpY2llbmN5JyxcbiAgICAgICAgICAgIGxhYmVsOiAnRWZmaWNpZW5jeScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NvbnRyb2xsYWJpbGl0eScsXG4gICAgICAgICAgICBsYWJlbDogJ0NvbnRyb2xsYWJpbGl0eScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnbmF2aWdhdGlvbicsXG4gICAgICAgIGxhYmVsOiAnTmF2aWdhdGlvbicsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdzaWRlIG5hdicsXG4gICAgICAgICAgICBsYWJlbDogJ1NpZGUgTmF2aWdhdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RvcCBuYXYnLFxuICAgICAgICAgICAgbGFiZWw6ICdUb3AgTmF2aWdhdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnY29tcG9uZW50JyxcbiAgICBsYWJlbDogJ0NvbXBvbmVudCcsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdiYXNpYycsXG4gICAgICAgIGxhYmVsOiAnQmFzaWMnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbGF5b3V0JyxcbiAgICAgICAgICAgIGxhYmVsOiAnTGF5b3V0JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY29sb3InLFxuICAgICAgICAgICAgbGFiZWw6ICdDb2xvcicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3R5cG9ncmFwaHknLFxuICAgICAgICAgICAgbGFiZWw6ICdUeXBvZ3JhcGh5JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnaWNvbicsXG4gICAgICAgICAgICBsYWJlbDogJ0ljb24nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdidXR0b24nLFxuICAgICAgICAgICAgbGFiZWw6ICdCdXR0b24nLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJ2Zvcm0nLFxuICAgICAgICBsYWJlbDogJ0Zvcm0nLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAncmFkaW8nLFxuICAgICAgICAgICAgbGFiZWw6ICdSYWRpbycsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NoZWNrYm94JyxcbiAgICAgICAgICAgIGxhYmVsOiAnQ2hlY2tib3gnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdpbnB1dCcsXG4gICAgICAgICAgICBsYWJlbDogJ0lucHV0JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnaW5wdXQtbnVtYmVyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnSW5wdXROdW1iZXInLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdzZWxlY3QnLFxuICAgICAgICAgICAgbGFiZWw6ICdTZWxlY3QnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdjYXNjYWRlcicsXG4gICAgICAgICAgICBsYWJlbDogJ0Nhc2NhZGVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc3dpdGNoJyxcbiAgICAgICAgICAgIGxhYmVsOiAnU3dpdGNoJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc2xpZGVyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnU2xpZGVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndGltZS1waWNrZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdUaW1lUGlja2VyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnZGF0ZS1waWNrZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdEYXRlUGlja2VyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnZGF0ZXRpbWUtcGlja2VyJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRGF0ZVRpbWVQaWNrZXInLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd1cGxvYWQnLFxuICAgICAgICAgICAgbGFiZWw6ICdVcGxvYWQnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdyYXRlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnUmF0ZScsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2Zvcm0nLFxuICAgICAgICAgICAgbGFiZWw6ICdGb3JtJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdkYXRhJyxcbiAgICAgICAgbGFiZWw6ICdEYXRhJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3RhYmxlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVGFibGUnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0YWcnLFxuICAgICAgICAgICAgbGFiZWw6ICdUYWcnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdwcm9ncmVzcycsXG4gICAgICAgICAgICBsYWJlbDogJ1Byb2dyZXNzJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndHJlZScsXG4gICAgICAgICAgICBsYWJlbDogJ1RyZWUnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdwYWdpbmF0aW9uJyxcbiAgICAgICAgICAgIGxhYmVsOiAnUGFnaW5hdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2JhZGdlJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQmFkZ2UnLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJ25vdGljZScsXG4gICAgICAgIGxhYmVsOiAnTm90aWNlJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2FsZXJ0JyxcbiAgICAgICAgICAgIGxhYmVsOiAnQWxlcnQnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdsb2FkaW5nJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTG9hZGluZycsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ21lc3NhZ2UnLFxuICAgICAgICAgICAgbGFiZWw6ICdNZXNzYWdlJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbWVzc2FnZS1ib3gnLFxuICAgICAgICAgICAgbGFiZWw6ICdNZXNzYWdlQm94JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbm90aWZpY2F0aW9uJyxcbiAgICAgICAgICAgIGxhYmVsOiAnTm90aWZpY2F0aW9uJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICduYXZpZ2F0aW9uJyxcbiAgICAgICAgbGFiZWw6ICdOYXZpZ2F0aW9uJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ21lbnUnLFxuICAgICAgICAgICAgbGFiZWw6ICdNZW51JyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAndGFicycsXG4gICAgICAgICAgICBsYWJlbDogJ1RhYnMnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdicmVhZGNydW1iJyxcbiAgICAgICAgICAgIGxhYmVsOiAnQnJlYWRjcnVtYicsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2Ryb3Bkb3duJyxcbiAgICAgICAgICAgIGxhYmVsOiAnRHJvcGRvd24nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdzdGVwcycsXG4gICAgICAgICAgICBsYWJlbDogJ1N0ZXBzJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdvdGhlcnMnLFxuICAgICAgICBsYWJlbDogJ090aGVycycsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdkaWFsb2cnLFxuICAgICAgICAgICAgbGFiZWw6ICdEaWFsb2cnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0b29sdGlwJyxcbiAgICAgICAgICAgIGxhYmVsOiAnVG9vbHRpcCcsXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3BvcG92ZXInLFxuICAgICAgICAgICAgbGFiZWw6ICdQb3BvdmVyJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY2FyZCcsXG4gICAgICAgICAgICBsYWJlbDogJ0NhcmQnLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdjYXJvdXNlbCcsXG4gICAgICAgICAgICBsYWJlbDogJ0Nhcm91c2VsJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY29sbGFwc2UnLFxuICAgICAgICAgICAgbGFiZWw6ICdDb2xsYXBzZScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAncmVzb3VyY2UnLFxuICAgIGxhYmVsOiAnUmVzb3VyY2UnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnYXh1cmUnLFxuICAgICAgICBsYWJlbDogJ0F4dXJlIENvbXBvbmVudHMnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdza2V0Y2gnLFxuICAgICAgICBsYWJlbDogJ1NrZXRjaCBUZW1wbGF0ZXMnLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdkb2NzJyxcbiAgICAgICAgbGFiZWw6ICdEZXNpZ24gRG9jdW1lbnRhdGlvbicsXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/cascader/panel.vue)_

vue

```
<template>
  <el-cascader-panel :options="options" />
</template>

<script lang="ts" setup>
const options = [
  {
    value: 'guide',
    label: 'Guide',
    children: [
      {
        value: 'disciplines',
        label: 'Disciplines',
        children: [
          {
            value: 'consistency',
            label: 'Consistency',
          },
          {
            value: 'feedback',
            label: 'Feedback',
          },
          {
            value: 'efficiency',
            label: 'Efficiency',
          },
          {
            value: 'controllability',
            label: 'Controllability',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'side nav',
            label: 'Side Navigation',
          },
          {
            value: 'top nav',
            label: 'Top Navigation',
          },
        ],
      },
    ],
  },
  {
    value: 'component',
    label: 'Component',
    children: [
      {
        value: 'basic',
        label: 'Basic',
        children: [
          {
            value: 'layout',
            label: 'Layout',
          },
          {
            value: 'color',
            label: 'Color',
          },
          {
            value: 'typography',
            label: 'Typography',
          },
          {
            value: 'icon',
            label: 'Icon',
          },
          {
            value: 'button',
            label: 'Button',
          },
        ],
      },
      {
        value: 'form',
        label: 'Form',
        children: [
          {
            value: 'radio',
            label: 'Radio',
          },
          {
            value: 'checkbox',
            label: 'Checkbox',
          },
          {
            value: 'input',
            label: 'Input',
          },
          {
            value: 'input-number',
            label: 'InputNumber',
          },
          {
            value: 'select',
            label: 'Select',
          },
          {
            value: 'cascader',
            label: 'Cascader',
          },
          {
            value: 'switch',
            label: 'Switch',
          },
          {
            value: 'slider',
            label: 'Slider',
          },
          {
            value: 'time-picker',
            label: 'TimePicker',
          },
          {
            value: 'date-picker',
            label: 'DatePicker',
          },
          {
            value: 'datetime-picker',
            label: 'DateTimePicker',
          },
          {
            value: 'upload',
            label: 'Upload',
          },
          {
            value: 'rate',
            label: 'Rate',
          },
          {
            value: 'form',
            label: 'Form',
          },
        ],
      },
      {
        value: 'data',
        label: 'Data',
        children: [
          {
            value: 'table',
            label: 'Table',
          },
          {
            value: 'tag',
            label: 'Tag',
          },
          {
            value: 'progress',
            label: 'Progress',
          },
          {
            value: 'tree',
            label: 'Tree',
          },
          {
            value: 'pagination',
            label: 'Pagination',
          },
          {
            value: 'badge',
            label: 'Badge',
          },
        ],
      },
      {
        value: 'notice',
        label: 'Notice',
        children: [
          {
            value: 'alert',
            label: 'Alert',
          },
          {
            value: 'loading',
            label: 'Loading',
          },
          {
            value: 'message',
            label: 'Message',
          },
          {
            value: 'message-box',
            label: 'MessageBox',
          },
          {
            value: 'notification',
            label: 'Notification',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'menu',
            label: 'Menu',
          },
          {
            value: 'tabs',
            label: 'Tabs',
          },
          {
            value: 'breadcrumb',
            label: 'Breadcrumb',
          },
          {
            value: 'dropdown',
            label: 'Dropdown',
          },
          {
            value: 'steps',
            label: 'Steps',
          },
        ],
      },
      {
        value: 'others',
        label: 'Others',
        children: [
          {
            value: 'dialog',
            label: 'Dialog',
          },
          {
            value: 'tooltip',
            label: 'Tooltip',
          },
          {
            value: 'popover',
            label: 'Popover',
          },
          {
            value: 'card',
            label: 'Card',
          },
          {
            value: 'carousel',
            label: 'Carousel',
          },
          {
            value: 'collapse',
            label: 'Collapse',
          },
        ],
      },
    ],
  },
  {
    value: 'resource',
    label: 'Resource',
    children: [
      {
        value: 'axure',
        label: 'Axure Components',
      },
      {
        value: 'sketch',
        label: 'Sketch Templates',
      },
      {
        value: 'docs',
        label: 'Design Documentation',
      },
    ],
  },
]
</script>
```

隐藏源代码

## 自定义标签 2.10.3 [​](#自定义标签)

您可以自定义标签。

将自定义的标签插入 `el-cascader` 的 slot 中即可。 `collapse-tags`, `collapse-tags-tooltip`, `max-collapse-tags` 在此模式下不生效.

Using slots allows for more flexible control over the display.

Display top-level tags only

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgPHA+VXNpbmcgc2xvdHMgYWxsb3dzIGZvciBtb3JlIGZsZXhpYmxlIGNvbnRyb2wgb3ZlciB0aGUgZGlzcGxheS48L3A+XG4gICAgPGVsLWNhc2NhZGVyIDpvcHRpb25zPVwib3B0aW9uc1wiIDpwcm9wcz1cInByb3BzXCIgY2xlYXJhYmxlPlxuICAgICAgPHRlbXBsYXRlICN0YWc9XCJ7IGRhdGEgfVwiPlxuICAgICAgICA8ZWwtdGFnXG4gICAgICAgICAgdi1mb3I9XCIoaXRlbSwgaW5kZXgpIGluIGdldFRhZ3MoZGF0YSlcIlxuICAgICAgICAgIDprZXk9XCJpdGVtXCJcbiAgICAgICAgICA6Y29sb3I9XCJpbmRleCAlIDIgPT09IDAgPyAnI0ZGREUwQScgOiAnJ1wiXG4gICAgICAgID5cbiAgICAgICAgICB7eyBpdGVtIH19XG4gICAgICAgIDwvZWwtdGFnPlxuICAgICAgPC90ZW1wbGF0ZT5cbiAgICA8L2VsLWNhc2NhZGVyPlxuICAgIDxwPkRpc3BsYXkgdG9wLWxldmVsIHRhZ3Mgb25seTwvcD5cbiAgICA8ZWwtY2FzY2FkZXIgOm9wdGlvbnM9XCJvcHRpb25zXCIgOnByb3BzPVwicHJvcHNcIiBjbGVhcmFibGU+XG4gICAgICA8dGVtcGxhdGUgI3RhZz1cInsgZGF0YSB9XCI+XG4gICAgICAgIDxlbC10YWcgdi1mb3I9XCJpdGVtIGluIGdldFRvcExldmVsVGFncyhkYXRhKVwiIDprZXk9XCJpdGVtXCI+XG4gICAgICAgICAge3sgaXRlbSB9fVxuICAgICAgICA8L2VsLXRhZz5cbiAgICAgIDwvdGVtcGxhdGU+XG4gICAgPC9lbC1jYXNjYWRlcj5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHR5cGUgeyBUYWcgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IHByb3BzID0geyBtdWx0aXBsZTogdHJ1ZSB9XG5jb25zdCBvcHRpb25zID0gW1xuICB7XG4gICAgdmFsdWU6IDEsXG4gICAgbGFiZWw6ICdBc2lhJyxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICB2YWx1ZTogMixcbiAgICAgICAgbGFiZWw6ICdDaGluYScsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAgeyB2YWx1ZTogMywgbGFiZWw6ICdCZWlqaW5nJyB9LFxuICAgICAgICAgIHsgdmFsdWU6IDQsIGxhYmVsOiAnU2hhbmdoYWknIH0sXG4gICAgICAgICAgeyB2YWx1ZTogNSwgbGFiZWw6ICdIYW5nemhvdScgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiA2LFxuICAgICAgICBsYWJlbDogJ0phcGFuJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7IHZhbHVlOiA3LCBsYWJlbDogJ1Rva3lvJyB9LFxuICAgICAgICAgIHsgdmFsdWU6IDgsIGxhYmVsOiAnT3Nha2EnIH0sXG4gICAgICAgICAgeyB2YWx1ZTogOSwgbGFiZWw6ICdLeW90bycgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAxMCxcbiAgICAgICAgbGFiZWw6ICdLb3JlYScsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAgeyB2YWx1ZTogMTEsIGxhYmVsOiAnU2VvdWwnIH0sXG4gICAgICAgICAgeyB2YWx1ZTogMTIsIGxhYmVsOiAnQnVzYW4nIH0sXG4gICAgICAgICAgeyB2YWx1ZTogMTMsIGxhYmVsOiAnVGFlZ3UnIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogMTQsXG4gICAgbGFiZWw6ICdFdXJvcGUnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAxNSxcbiAgICAgICAgbGFiZWw6ICdGcmFuY2UnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHsgdmFsdWU6IDE2LCBsYWJlbDogJ1BhcmlzJyB9LFxuICAgICAgICAgIHsgdmFsdWU6IDE3LCBsYWJlbDogJ01hcnNlaWxsZScgfSxcbiAgICAgICAgICB7IHZhbHVlOiAxOCwgbGFiZWw6ICdMeW9uJyB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6IDE5LFxuICAgICAgICBsYWJlbDogJ1VLJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7IHZhbHVlOiAyMCwgbGFiZWw6ICdMb25kb24nIH0sXG4gICAgICAgICAgeyB2YWx1ZTogMjEsIGxhYmVsOiAnQmlybWluZ2hhbScgfSxcbiAgICAgICAgICB7IHZhbHVlOiAyMiwgbGFiZWw6ICdNYW5jaGVzdGVyJyB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuICB7XG4gICAgdmFsdWU6IDIzLFxuICAgIGxhYmVsOiAnTm9ydGggQW1lcmljYScsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6IDI0LFxuICAgICAgICBsYWJlbDogJ1VTJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7IHZhbHVlOiAyNSwgbGFiZWw6ICdOZXcgWW9yaycgfSxcbiAgICAgICAgICB7IHZhbHVlOiAyNiwgbGFiZWw6ICdMb3MgQW5nZWxlcycgfSxcbiAgICAgICAgICB7IHZhbHVlOiAyNywgbGFiZWw6ICdXYXNoaW5ndG9uJyB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6IDI4LFxuICAgICAgICBsYWJlbDogJ0NhbmFkYScsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAgeyB2YWx1ZTogMjksIGxhYmVsOiAnVG9yb250bycgfSxcbiAgICAgICAgICB7IHZhbHVlOiAzMCwgbGFiZWw6ICdNb250cmVhbCcgfSxcbiAgICAgICAgICB7IHZhbHVlOiAzMSwgbGFiZWw6ICdPdHRhd2EnIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG5dXG5jb25zdCBnZXRUYWdzID0gKGRhdGE6IFRhZ1tdKSA9PiB7XG4gIHJldHVybiBkYXRhLm1hcCgoaXRlbSkgPT4gaXRlbS50ZXh0KVxufVxuY29uc3QgZ2V0VG9wTGV2ZWxUYWdzID0gKGRhdGE6IFRhZ1tdKSA9PiB7XG4gIGNvbnN0IHNldDogU2V0PHN0cmluZz4gPSBuZXcgU2V0KClcbiAgZm9yIChjb25zdCBkYXR1bSBvZiBkYXRhKSB7XG4gICAgbGV0IHBhcmVudCA9IGRhdHVtLm5vZGU/LnBhcmVudFxuICAgIHdoaWxlIChwYXJlbnQgJiYgcGFyZW50LmxldmVsICE9PSAxKSB7XG4gICAgICBwYXJlbnQgPSBwYXJlbnQucGFyZW50XG4gICAgfVxuICAgIGNvbnN0IGxhYmVsID0gcGFyZW50Py5kYXRhPy5sYWJlbFxuICAgIGxhYmVsICYmIHNldC5hZGQobGFiZWwpXG4gIH1cbiAgcmV0dXJuIFsuLi5zZXRdXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/cascader/custom-tag.vue)_

vue

```
<template>
  <div class="m-4">
    <p>Using slots allows for more flexible control over the display.</p>
    <el-cascader :options="options" :props="props" clearable>
      <template #tag="{ data }">
        <el-tag
          v-for="(item, index) in getTags(data)"
          :key="item"
          :color="index % 2 === 0 ? '#FFDE0A' : ''"
        >
          {{ item }}
        </el-tag>
      </template>
    </el-cascader>
    <p>Display top-level tags only</p>
    <el-cascader :options="options" :props="props" clearable>
      <template #tag="{ data }">
        <el-tag v-for="item in getTopLevelTags(data)" :key="item">
          {{ item }}
        </el-tag>
      </template>
    </el-cascader>
  </div>
</template>

<script lang="ts" setup>
import type { Tag } from 'element-plus'

const props = { multiple: true }
const options = [
  {
    value: 1,
    label: 'Asia',
    children: [
      {
        value: 2,
        label: 'China',
        children: [
          { value: 3, label: 'Beijing' },
          { value: 4, label: 'Shanghai' },
          { value: 5, label: 'Hangzhou' },
        ],
      },
      {
        value: 6,
        label: 'Japan',
        children: [
          { value: 7, label: 'Tokyo' },
          { value: 8, label: 'Osaka' },
          { value: 9, label: 'Kyoto' },
        ],
      },
      {
        value: 10,
        label: 'Korea',
        children: [
          { value: 11, label: 'Seoul' },
          { value: 12, label: 'Busan' },
          { value: 13, label: 'Taegu' },
        ],
      },
    ],
  },
  {
    value: 14,
    label: 'Europe',
    children: [
      {
        value: 15,
        label: 'France',
        children: [
          { value: 16, label: 'Paris' },
          { value: 17, label: 'Marseille' },
          { value: 18, label: 'Lyon' },
        ],
      },
      {
        value: 19,
        label: 'UK',
        children: [
          { value: 20, label: 'London' },
          { value: 21, label: 'Birmingham' },
          { value: 22, label: 'Manchester' },
        ],
      },
    ],
  },
  {
    value: 23,
    label: 'North America',
    children: [
      {
        value: 24,
        label: 'US',
        children: [
          { value: 25, label: 'New York' },
          { value: 26, label: 'Los Angeles' },
          { value: 27, label: 'Washington' },
        ],
      },
      {
        value: 28,
        label: 'Canada',
        children: [
          { value: 29, label: 'Toronto' },
          { value: 30, label: 'Montreal' },
          { value: 31, label: 'Ottawa' },
        ],
      },
    ],
  },
]
const getTags = (data: Tag[]) => {
  return data.map((item) => item.text)
}
const getTopLevelTags = (data: Tag[]) => {
  const set: Set<string> = new Set()
  for (const datum of data) {
    let parent = datum.node?.parent
    while (parent && parent.level !== 1) {
      parent = parent.parent
    }
    const label = parent?.data?.label
    label && set.add(label)
  }
  return [...set]
}
</script>
```

隐藏源代码

## 已勾选项显示策略 2.10.5 [​](#已勾选项显示策略)

控制在多选模式下已选值的显示方式。

在多选模式下，你可以使用 `show-checked-strategy` 来控制已选值的显示方式。 默认策略为 `child`，即显示所有已选中的子节点。 `parent` 策略仅在其所有子节点都被选中时显示父节点。

Strategy: child (default, show all selected child nodes)

Strategy: parent (show only parent nodes when all children are selected)

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgPHA+U3RyYXRlZ3k6IGNoaWxkIChkZWZhdWx0LCBzaG93IGFsbCBzZWxlY3RlZCBjaGlsZCBub2Rlcyk8L3A+XG4gICAgPGVsLWNhc2NhZGVyXG4gICAgICB2LW1vZGVsPVwidmFsdWUxXCJcbiAgICAgIDpvcHRpb25zPVwib3B0aW9uc1wiXG4gICAgICA6cHJvcHM9XCJwcm9wc1wiXG4gICAgICBzaG93LWNoZWNrZWQtc3RyYXRlZ3k9XCJjaGlsZFwiXG4gICAgICBjbGVhcmFibGVcbiAgICAgIEBjaGFuZ2U9XCJoYW5kbGVDaGFuZ2UxXCJcbiAgICAvPlxuICA8L2Rpdj5cblxuICA8ZGl2IGNsYXNzPVwibS00XCI+XG4gICAgPHA+XG4gICAgICBTdHJhdGVneTogcGFyZW50IChzaG93IG9ubHkgcGFyZW50IG5vZGVzIHdoZW4gYWxsIGNoaWxkcmVuIGFyZSBzZWxlY3RlZClcbiAgICA8L3A+XG4gICAgPGVsLWNhc2NhZGVyXG4gICAgICB2LW1vZGVsPVwidmFsdWUyXCJcbiAgICAgIDpvcHRpb25zPVwib3B0aW9uc1wiXG4gICAgICA6cHJvcHM9XCJwcm9wc1wiXG4gICAgICBzaG93LWNoZWNrZWQtc3RyYXRlZ3k9XCJwYXJlbnRcIlxuICAgICAgY2xlYXJhYmxlXG4gICAgICBAY2hhbmdlPVwiaGFuZGxlQ2hhbmdlMlwiXG4gICAgLz5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZTEgPSByZWYoW10pXG5jb25zdCB2YWx1ZTIgPSByZWYoW10pXG5jb25zdCBwcm9wcyA9IHtcbiAgbXVsdGlwbGU6IHRydWUsXG59XG5cbmNvbnN0IGhhbmRsZUNoYW5nZTEgPSAodmFsdWUpID0+IHtcbiAgY29uc29sZS5sb2coJ0NoaWxkIHN0cmF0ZWd5OicsIHZhbHVlKVxufVxuXG5jb25zdCBoYW5kbGVDaGFuZ2UyID0gKHZhbHVlKSA9PiB7XG4gIGNvbnNvbGUubG9nKCdQYXJlbnQgc3RyYXRlZ3k6JywgdmFsdWUpXG59XG5cbmNvbnN0IG9wdGlvbnMgPSBbXG4gIHtcbiAgICB2YWx1ZTogJ2d1aWRlJyxcbiAgICBsYWJlbDogJ0d1aWRlJyxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICB2YWx1ZTogJ2Rpc2NpcGxpbmVzJyxcbiAgICAgICAgbGFiZWw6ICdEaXNjaXBsaW5lcycsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdjb25zaXN0ZW5jeScsXG4gICAgICAgICAgICBsYWJlbDogJ0NvbnNpc3RlbmN5JyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICduYXZpZ2F0aW9uJyxcbiAgICAgICAgbGFiZWw6ICdOYXZpZ2F0aW9uJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3NpZGUgbmF2JyxcbiAgICAgICAgICAgIGxhYmVsOiAnU2lkZSBOYXZpZ2F0aW9uJyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuICB7XG4gICAgdmFsdWU6ICdjb21wb25lbnQnLFxuICAgIGxhYmVsOiAnQ29tcG9uZW50JyxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICB2YWx1ZTogJ2Jhc2ljJyxcbiAgICAgICAgbGFiZWw6ICdCYXNpYycsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdsYXlvdXQnLFxuICAgICAgICAgICAgbGFiZWw6ICdMYXlvdXQnLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJ2Zvcm0nLFxuICAgICAgICBsYWJlbDogJ0Zvcm0nLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAncmFkaW8nLFxuICAgICAgICAgICAgbGFiZWw6ICdSYWRpbycsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAncmVzb3VyY2UnLFxuICAgIGxhYmVsOiAnUmVzb3VyY2UnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnYXh1cmUnLFxuICAgICAgICBsYWJlbDogJ0F4dXJlIENvbXBvbmVudHMnLFxuICAgICAgfSxcbiAgICBdLFxuICB9LFxuXVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/cascader/show-checked-strategy.vue)_

vue

```
<template>
  <div class="m-4">
    <p>Strategy: child (default, show all selected child nodes)</p>
    <el-cascader
      v-model="value1"
      :options="options"
      :props="props"
      show-checked-strategy="child"
      clearable
      @change="handleChange1"
    />
  </div>

  <div class="m-4">
    <p>
      Strategy: parent (show only parent nodes when all children are selected)
    </p>
    <el-cascader
      v-model="value2"
      :options="options"
      :props="props"
      show-checked-strategy="parent"
      clearable
      @change="handleChange2"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref([])
const value2 = ref([])
const props = {
  multiple: true,
}

const handleChange1 = (value) => {
  console.log('Child strategy:', value)
}

const handleChange2 = (value) => {
  console.log('Parent strategy:', value)
}

const options = [
  {
    value: 'guide',
    label: 'Guide',
    children: [
      {
        value: 'disciplines',
        label: 'Disciplines',
        children: [
          {
            value: 'consistency',
            label: 'Consistency',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'side nav',
            label: 'Side Navigation',
          },
        ],
      },
    ],
  },
  {
    value: 'component',
    label: 'Component',
    children: [
      {
        value: 'basic',
        label: 'Basic',
        children: [
          {
            value: 'layout',
            label: 'Layout',
          },
        ],
      },
      {
        value: 'form',
        label: 'Form',
        children: [
          {
            value: 'radio',
            label: 'Radio',
          },
        ],
      },
    ],
  },
  {
    value: 'resource',
    label: 'Resource',
    children: [
      {
        value: 'axure',
        label: 'Axure Components',
      },
    ],
  },
]
</script>
```

隐藏源代码

## 点击选中节点 2.10.5 [​](#点击选中节点)

只使用 `multiple` 或 `checkStrictly` 属性。

你可以添加 `checkOnClickNode`，使节点本身也能被点击（不仅限于前缀图标）。 通过 `showPrefix` 来切换前缀的显示与隐藏。 :::tip 添加 `checkOnClickLeaf` 属性可以仅勾选叶子节点（最末级子节点），该功能默认启用。 :::

hide prefixshow prefix

checkStrictly | Single mode

Multiple mode

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LWNvbCBpdGVtcy1jZW50ZXJcIj5cbiAgICA8ZWwtc3dpdGNoXG4gICAgICB2LW1vZGVsPVwic2hvd1ByZWZpeFwiXG4gICAgICBhY3RpdmUtdGV4dD1cInNob3cgcHJlZml4XCJcbiAgICAgIGluYWN0aXZlLXRleHQ9XCJoaWRlIHByZWZpeFwiXG4gICAgLz5cbiAgICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXBcIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJtLTRcIj5cbiAgICAgICAgPHA+Y2hlY2tTdHJpY3RseSB8IFNpbmdsZSBtb2RlPC9wPlxuICAgICAgICA8ZWwtY2FzY2FkZXJcbiAgICAgICAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgICAgICAgIDpvcHRpb25zPVwib3B0aW9uc1wiXG4gICAgICAgICAgOnByb3BzPVwicHJvcHMxXCJcbiAgICAgICAgICBjbGVhcmFibGVcbiAgICAgICAgLz5cbiAgICAgIDwvZGl2PlxuICAgICAgPGRpdiBjbGFzcz1cIm0tNFwiPlxuICAgICAgICA8cD5NdWx0aXBsZSBtb2RlPC9wPlxuICAgICAgICA8ZWwtY2FzY2FkZXJcbiAgICAgICAgICB2LW1vZGVsPVwidmFsdWUyXCJcbiAgICAgICAgICBzaG93LWNoZWNrZWQtc3RyYXRlZ3k9XCJwYXJlbnRcIlxuICAgICAgICAgIDpvcHRpb25zPVwib3B0aW9uc1wiXG4gICAgICAgICAgOnByb3BzPVwicHJvcHMyXCJcbiAgICAgICAgICBjbGVhcmFibGVcbiAgICAgICAgLz5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBjb21wdXRlZCwgcmVmIH0gZnJvbSAndnVlJ1xuXG5jb25zdCB2YWx1ZSA9IHJlZigpXG5jb25zdCB2YWx1ZTIgPSByZWYoKVxuY29uc3Qgc2hvd1ByZWZpeCA9IHJlZih0cnVlKVxuXG5jb25zdCBwcm9wczEgPSBjb21wdXRlZCgoKSA9PiAoe1xuICBzaG93UHJlZml4OiBzaG93UHJlZml4LnZhbHVlLFxuICBjaGVja1N0cmljdGx5OiB0cnVlLFxuICBjaGVja09uQ2xpY2tOb2RlOiB0cnVlLFxufSkpXG5jb25zdCBwcm9wczIgPSBjb21wdXRlZCgoKSA9PiAoe1xuICBzaG93UHJlZml4OiBzaG93UHJlZml4LnZhbHVlLFxuICBtdWx0aXBsZTogdHJ1ZSxcbiAgY2hlY2tPbkNsaWNrTm9kZTogdHJ1ZSxcbn0pKVxuXG5jb25zdCBvcHRpb25zID0gW1xuICB7XG4gICAgdmFsdWU6ICdndWlkZScsXG4gICAgbGFiZWw6ICdHdWlkZScsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdkaXNjaXBsaW5lcycsXG4gICAgICAgIGxhYmVsOiAnRGlzY2lwbGluZXMnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnY29uc2lzdGVuY3knLFxuICAgICAgICAgICAgbGFiZWw6ICdDb25zaXN0ZW5jeScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnbmF2aWdhdGlvbicsXG4gICAgICAgIGxhYmVsOiAnTmF2aWdhdGlvbicsXG4gICAgICAgIGNoaWxkcmVuOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdzaWRlIG5hdicsXG4gICAgICAgICAgICBsYWJlbDogJ1NpZGUgTmF2aWdhdGlvbicsXG4gICAgICAgICAgfSxcbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbiAge1xuICAgIHZhbHVlOiAnY29tcG9uZW50JyxcbiAgICBsYWJlbDogJ0NvbXBvbmVudCcsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdiYXNpYycsXG4gICAgICAgIGxhYmVsOiAnQmFzaWMnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnbGF5b3V0JyxcbiAgICAgICAgICAgIGxhYmVsOiAnTGF5b3V0JyxcbiAgICAgICAgICB9LFxuICAgICAgICBdLFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdmb3JtJyxcbiAgICAgICAgbGFiZWw6ICdGb3JtJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ3JhZGlvJyxcbiAgICAgICAgICAgIGxhYmVsOiAnUmFkaW8nLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG4gIHtcbiAgICB2YWx1ZTogJ3Jlc291cmNlJyxcbiAgICBsYWJlbDogJ1Jlc291cmNlJyxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICB2YWx1ZTogJ2F4dXJlJyxcbiAgICAgICAgbGFiZWw6ICdBeHVyZSBDb21wb25lbnRzJyxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/cascader/check-on-click-node.vue)_

vue

```
<template>
  <div class="flex flex-col items-center">
    <el-switch
      v-model="showPrefix"
      active-text="show prefix"
      inactive-text="hide prefix"
    />
    <div class="flex flex-wrap">
      <div class="m-4">
        <p>checkStrictly | Single mode</p>
        <el-cascader
          v-model="value"
          :options="options"
          :props="props1"
          clearable
        />
      </div>
      <div class="m-4">
        <p>Multiple mode</p>
        <el-cascader
          v-model="value2"
          show-checked-strategy="parent"
          :options="options"
          :props="props2"
          clearable
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue'

const value = ref()
const value2 = ref()
const showPrefix = ref(true)

const props1 = computed(() => ({
  showPrefix: showPrefix.value,
  checkStrictly: true,
  checkOnClickNode: true,
}))
const props2 = computed(() => ({
  showPrefix: showPrefix.value,
  multiple: true,
  checkOnClickNode: true,
}))

const options = [
  {
    value: 'guide',
    label: 'Guide',
    children: [
      {
        value: 'disciplines',
        label: 'Disciplines',
        children: [
          {
            value: 'consistency',
            label: 'Consistency',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'side nav',
            label: 'Side Navigation',
          },
        ],
      },
    ],
  },
  {
    value: 'component',
    label: 'Component',
    children: [
      {
        value: 'basic',
        label: 'Basic',
        children: [
          {
            value: 'layout',
            label: 'Layout',
          },
        ],
      },
      {
        value: 'form',
        label: 'Form',
        children: [
          {
            value: 'radio',
            label: 'Radio',
          },
        ],
      },
    ],
  },
  {
    value: 'resource',
    label: 'Resource',
    children: [
      {
        value: 'axure',
        label: 'Axure Components',
      },
    ],
  },
]
</script>
```

隐藏源代码

## 自定义头部与底部 2.10.5 [​](#自定义头部与底部)

你可以通过插槽来自定义下拉菜单的头部和底部。

使用插槽自定义内容。

Custom header content

Custom footer content

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiY2FzY2FkZXItY3VzdG9tLWhlYWRlci1mb290ZXJcIj5cbiAgICA8ZGl2PlxuICAgICAgPHA+Q3VzdG9tIGhlYWRlciBjb250ZW50PC9wPlxuICAgICAgPGVsLWNhc2NhZGVyXG4gICAgICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgICAgIHBvcHBlci1jbGFzcz1cImNhc2NhZGVyLWN1c3RvbS1oZWFkZXJcIlxuICAgICAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgICAgICA6cHJvcHM9XCJwcm9wc1wiXG4gICAgICAgIGNsZWFyYWJsZVxuICAgICAgPlxuICAgICAgICA8dGVtcGxhdGUgI2hlYWRlcj5cbiAgICAgICAgICA8ZWwtY2hlY2tib3hcbiAgICAgICAgICAgIHYtbW9kZWw9XCJjaGVja0FsbFwiXG4gICAgICAgICAgICA6aW5kZXRlcm1pbmF0ZT1cImluZGV0ZXJtaW5hdGVcIlxuICAgICAgICAgICAgQGNoYW5nZT1cImhhbmRsZUNoZWNrQWxsXCJcbiAgICAgICAgICA+XG4gICAgICAgICAgICBBbGxcbiAgICAgICAgICA8L2VsLWNoZWNrYm94PlxuICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgPC9lbC1jYXNjYWRlcj5cbiAgICA8L2Rpdj5cbiAgICA8ZGl2PlxuICAgICAgPHA+Q3VzdG9tIGZvb3RlciBjb250ZW50PC9wPlxuICAgICAgPGVsLWNhc2NhZGVyIHYtbW9kZWw9XCJ2YWx1ZVwiIDpvcHRpb25zPVwib3B0aW9uc1wiIDpwcm9wcz1cInByb3BzXCIgY2xlYXJhYmxlPlxuICAgICAgICA8dGVtcGxhdGUgI2Zvb3Rlcj5cbiAgICAgICAgICA8ZWwtYnV0dG9uIGxpbmsgc2l6ZT1cInNtYWxsXCIgQGNsaWNrPVwiaGFuZGxlQ2xlYXJcIj4gQ2xlYXIgPC9lbC1idXR0b24+XG4gICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICA8L2VsLWNhc2NhZGVyPlxuICAgIDwvZGl2PlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyBjb21wdXRlZCwgcmVmLCB3YXRjaCB9IGZyb20gJ3Z1ZSdcblxuaW1wb3J0IHR5cGUgeyBDYXNjYWRlck9wdGlvbiwgQ2hlY2tib3hWYWx1ZVR5cGUgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IHByb3BzID0geyBtdWx0aXBsZTogdHJ1ZSB9XG5jb25zdCBjaGVja0FsbCA9IHJlZihmYWxzZSlcbmNvbnN0IGluZGV0ZXJtaW5hdGUgPSByZWYoZmFsc2UpXG5jb25zdCB2YWx1ZSA9IHJlZjxzdHJpbmdbXVtdPihbXSlcbmNvbnN0IG9wdGlvbnMgPSByZWYoW1xuICB7XG4gICAgdmFsdWU6ICdndWlkZScsXG4gICAgbGFiZWw6ICdHdWlkZScsXG4gICAgY2hpbGRyZW46IFtcbiAgICAgIHtcbiAgICAgICAgdmFsdWU6ICdkaXNjaXBsaW5lcycsXG4gICAgICAgIGxhYmVsOiAnRGlzY2lwbGluZXMnLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHsgdmFsdWU6ICdjb25zaXN0ZW5jeScsIGxhYmVsOiAnQ29uc2lzdGVuY3knIH0sXG4gICAgICAgICAgeyB2YWx1ZTogJ2ZlZWRiYWNrJywgbGFiZWw6ICdGZWVkYmFjaycgfSxcbiAgICAgICAgICB7IHZhbHVlOiAnZWZmaWNpZW5jeScsIGxhYmVsOiAnRWZmaWNpZW5jeScgfSxcbiAgICAgICAgICB7IHZhbHVlOiAnY29udHJvbGxhYmlsaXR5JywgbGFiZWw6ICdDb250cm9sbGFiaWxpdHknIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG5dKVxuXG5jb25zdCBnZXRBbGxWYWx1ZVBhdGhzID0gY29tcHV0ZWQoKCkgPT4ge1xuICBjb25zdCByZXN1bHQ6IHN0cmluZ1tdW10gPSBbXVxuICBjb25zdCBxdWV1ZTogeyBub2RlOiBDYXNjYWRlck9wdGlvbjsgcGF0aDogc3RyaW5nW10gfVtdID0gb3B0aW9ucy52YWx1ZS5tYXAoXG4gICAgKG5vZGUpID0+ICh7IG5vZGUsIHBhdGg6IFtub2RlLnZhbHVlXSB9KVxuICApXG5cbiAgd2hpbGUgKHF1ZXVlLmxlbmd0aCA+IDApIHtcbiAgICBjb25zdCB7IG5vZGUsIHBhdGggfSA9IHF1ZXVlLnNoaWZ0KCkhXG4gICAgaWYgKG5vZGUuY2hpbGRyZW4/Lmxlbmd0aCkge1xuICAgICAgbm9kZS5jaGlsZHJlbi5mb3JFYWNoKChjaGlsZCkgPT4ge1xuICAgICAgICBxdWV1ZS5wdXNoKHsgbm9kZTogY2hpbGQsIHBhdGg6IFsuLi5wYXRoLCBjaGlsZC52YWx1ZSBhcyBzdHJpbmddIH0pXG4gICAgICB9KVxuICAgIH0gZWxzZSB7XG4gICAgICByZXN1bHQucHVzaChwYXRoKVxuICAgIH1cbiAgfVxuICByZXR1cm4gcmVzdWx0XG59KVxuXG53YXRjaCh2YWx1ZSwgKHZhbCkgPT4ge1xuICBpZiAodmFsLmxlbmd0aCA9PT0gMCkge1xuICAgIGNoZWNrQWxsLnZhbHVlID0gZmFsc2VcbiAgICBpbmRldGVybWluYXRlLnZhbHVlID0gZmFsc2VcbiAgfSBlbHNlIGlmICh2YWwubGVuZ3RoID09PSBnZXRBbGxWYWx1ZVBhdGhzLnZhbHVlLmxlbmd0aCkge1xuICAgIGNoZWNrQWxsLnZhbHVlID0gdHJ1ZVxuICAgIGluZGV0ZXJtaW5hdGUudmFsdWUgPSBmYWxzZVxuICB9IGVsc2Uge1xuICAgIGluZGV0ZXJtaW5hdGUudmFsdWUgPSB0cnVlXG4gIH1cbn0pXG5cbmNvbnN0IGhhbmRsZUNoZWNrQWxsID0gKHZhbDogQ2hlY2tib3hWYWx1ZVR5cGUpID0+IHtcbiAgaW5kZXRlcm1pbmF0ZS52YWx1ZSA9IGZhbHNlXG4gIHZhbHVlLnZhbHVlID0gdmFsID8gZ2V0QWxsVmFsdWVQYXRocy52YWx1ZSA6IFtdXG59XG5cbmNvbnN0IGhhbmRsZUNsZWFyID0gKCkgPT4ge1xuICB2YWx1ZS52YWx1ZSA9IFtdXG59XG48L3NjcmlwdD5cblxuPHN0eWxlIHNjb3BlZD5cbi5jYXNjYWRlci1jdXN0b20taGVhZGVyLWZvb3RlciB7XG4gIGRpc3BsYXk6IGZsZXg7XG59XG5cbi5jYXNjYWRlci1jdXN0b20taGVhZGVyLWZvb3RlciA+IGRpdiB7XG4gIGZsZXg6IDE7XG4gIHRleHQtYWxpZ246IGNlbnRlcjtcbn1cblxuLmNhc2NhZGVyLWN1c3RvbS1oZWFkZXItZm9vdGVyID4gZGl2Om5vdCg6bGFzdC1jaGlsZCkge1xuICBib3JkZXItcmlnaHQ6IDFweCBzb2xpZCB2YXIoLS1lbC1ib3JkZXItY29sb3IpO1xufVxuXG4uY2FzY2FkZXItY3VzdG9tLWhlYWRlciAuZWwtY2hlY2tib3gge1xuICBkaXNwbGF5OiBmbGV4O1xuICBoZWlnaHQ6IHVuc2V0O1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/cascader/custom-header-footer.vue)_

vue

```
<template>
  <div class="cascader-custom-header-footer">
    <div>
      <p>Custom header content</p>
      <el-cascader
        v-model="value"
        popper-class="cascader-custom-header"
        :options="options"
        :props="props"
        clearable
      >
        <template #header>
          <el-checkbox
            v-model="checkAll"
            :indeterminate="indeterminate"
            @change="handleCheckAll"
          >
            All
          </el-checkbox>
        </template>
      </el-cascader>
    </div>
    <div>
      <p>Custom footer content</p>
      <el-cascader v-model="value" :options="options" :props="props" clearable>
        <template #footer>
          <el-button link size="small" @click="handleClear"> Clear </el-button>
        </template>
      </el-cascader>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref, watch } from 'vue'

import type { CascaderOption, CheckboxValueType } from 'element-plus'

const props = { multiple: true }
const checkAll = ref(false)
const indeterminate = ref(false)
const value = ref<string[][]>([])
const options = ref([
  {
    value: 'guide',
    label: 'Guide',
    children: [
      {
        value: 'disciplines',
        label: 'Disciplines',
        children: [
          { value: 'consistency', label: 'Consistency' },
          { value: 'feedback', label: 'Feedback' },
          { value: 'efficiency', label: 'Efficiency' },
          { value: 'controllability', label: 'Controllability' },
        ],
      },
    ],
  },
])

const getAllValuePaths = computed(() => {
  const result: string[][] = []
  const queue: { node: CascaderOption; path: string[] }[] = options.value.map(
    (node) => ({ node, path: [node.value] })
  )

  while (queue.length > 0) {
    const { node, path } = queue.shift()!
    if (node.children?.length) {
      node.children.forEach((child) => {
        queue.push({ node: child, path: [...path, child.value as string] })
      })
    } else {
      result.push(path)
    }
  }
  return result
})

watch(value, (val) => {
  if (val.length === 0) {
    checkAll.value = false
    indeterminate.value = false
  } else if (val.length === getAllValuePaths.value.length) {
    checkAll.value = true
    indeterminate.value = false
  } else {
    indeterminate.value = true
  }
})

const handleCheckAll = (val: CheckboxValueType) => {
  indeterminate.value = false
  value.value = val ? getAllValuePaths.value : []
}

const handleClear = () => {
  value.value = []
}
</script>

<style scoped>
.cascader-custom-header-footer {
  display: flex;
}

.cascader-custom-header-footer > div {
  flex: 1;
  text-align: center;
}

.cascader-custom-header-footer > div:not(:last-child) {
  border-right: 1px solid var(--el-border-color);
}

.cascader-custom-header .el-checkbox {
  display: flex;
  height: unset;
}
</style>
```

隐藏源代码

## 虚拟滚动 2.14.0 [​](#虚拟滚动)

当处理大量数据时，您可以启用虚拟滚动以提高性能。

将 `virtual-scroll` 设置为 `true` 以启用虚拟滚动。 您还可以使用 `height` 自定义菜单高度，并使用 `item-size` 自定义节点高度。 默认高度为 204px，默认节点大小为 34px。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2FzY2FkZXJcbiAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgIDpvcHRpb25zPVwib3B0aW9uc1wiXG4gICAgOmZpbHRlci1tZXRob2Q9XCJmaWx0ZXJNZXRob2RcIlxuICAgIGZpbHRlcmFibGVcbiAgICB2aXJ0dWFsLXNjcm9sbFxuICAgIGNsZWFyYWJsZVxuICAgIHBsYWNlaG9sZGVyPVwiU2VsZWN0IHdpdGggbGFyZ2UgZGF0YVwiXG4gIC8+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IENhc2NhZGVyTm9kZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuaW50ZXJmYWNlIENhc2NhZGVyRXhhbXBsZU9wdGlvbiB7XG4gIHZhbHVlOiBzdHJpbmdcbiAgbGFiZWw6IHN0cmluZ1xuICBjaGlsZHJlbj86IENhc2NhZGVyRXhhbXBsZU9wdGlvbltdXG59XG5cbmNvbnN0IHZhbHVlID0gcmVmPHN0cmluZ1tdPihbXSlcblxuY29uc3QgZmlsdGVyTWV0aG9kID0gKG5vZGU6IENhc2NhZGVyTm9kZSwga2V5d29yZDogc3RyaW5nKSA9PiB7XG4gIHJldHVybiBub2RlLnRleHQudG9Mb3dlckNhc2UoKS5pbmNsdWRlcyhrZXl3b3JkLnRvTG93ZXJDYXNlKCkpXG59XG5cbmNvbnN0IGdlbmVyYXRlT3B0aW9ucyA9IChjb3VudDogbnVtYmVyKTogQ2FzY2FkZXJFeGFtcGxlT3B0aW9uW10gPT4ge1xuICByZXR1cm4gQXJyYXkuZnJvbSh7IGxlbmd0aDogY291bnQgfSkubWFwKChfLCBpbmRleCkgPT4gKHtcbiAgICB2YWx1ZTogYG9wdGlvbi0ke2luZGV4fWAsXG4gICAgbGFiZWw6IGBPcHRpb24gJHtpbmRleCArIDF9YCxcbiAgICBjaGlsZHJlbjogW1xuICAgICAge1xuICAgICAgICB2YWx1ZTogYGNoaWxkLSR7aW5kZXh9LTFgLFxuICAgICAgICBsYWJlbDogYENoaWxkICR7aW5kZXggKyAxfS0xYCxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogYGdyYW5kY2hpbGQtJHtpbmRleH0tMS0xYCxcbiAgICAgICAgICAgIGxhYmVsOiBgR3JhbmRjaGlsZCAke2luZGV4ICsgMX0tMS0xYCxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiBgZ3JhbmRjaGlsZC0ke2luZGV4fS0xLTJgLFxuICAgICAgICAgICAgbGFiZWw6IGBHcmFuZGNoaWxkICR7aW5kZXggKyAxfS0xLTJgLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogYGNoaWxkLSR7aW5kZXh9LTJgLFxuICAgICAgICBsYWJlbDogYENoaWxkICR7aW5kZXggKyAxfS0yYCxcbiAgICAgIH0sXG4gICAgXSxcbiAgfSkpXG59XG5cbmNvbnN0IG9wdGlvbnMgPSByZWY8Q2FzY2FkZXJFeGFtcGxlT3B0aW9uW10+KGdlbmVyYXRlT3B0aW9ucygyMDAwMCkpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/cascader/virtual-scroll.vue)_

vue

```
<template>
  <el-cascader
    v-model="value"
    :options="options"
    :filter-method="filterMethod"
    filterable
    virtual-scroll
    clearable
    placeholder="Select with large data"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { CascaderNode } from 'element-plus'

interface CascaderExampleOption {
  value: string
  label: string
  children?: CascaderExampleOption[]
}

const value = ref<string[]>([])

const filterMethod = (node: CascaderNode, keyword: string) => {
  return node.text.toLowerCase().includes(keyword.toLowerCase())
}

const generateOptions = (count: number): CascaderExampleOption[] => {
  return Array.from({ length: count }).map((_, index) => ({
    value: `option-${index}`,
    label: `Option ${index + 1}`,
    children: [
      {
        value: `child-${index}-1`,
        label: `Child ${index + 1}-1`,
        children: [
          {
            value: `grandchild-${index}-1-1`,
            label: `Grandchild ${index + 1}-1-1`,
          },
          {
            value: `grandchild-${index}-1-2`,
            label: `Grandchild ${index + 1}-1-2`,
          },
        ],
      },
      {
        value: `child-${index}-2`,
        label: `Child ${index + 1}-2`,
      },
    ],
  }))
}

const options = ref<CascaderExampleOption[]>(generateOptions(20000))
</script>
```

隐藏源代码

## 自定义建议面板宽度 2.14.0 [​](#自定义建议面板宽度)

建议面板（筛选时）的宽度默认会根据匹配到的选项中的最大宽度自动计算。 如果您通过 `suggestion-item` 插槽自定义建议选项，选项中显示的文本很可能不等于 `label` 的值，从而导致计算错误。 在这种情况下，您可以使用 `fit-input-width` 属性来固定其宽度。 当值为 `number` 时，宽度为固定的具体像素值。

TIP

`fit-input-width` 属性仅控制搜索时建议面板的宽度，不影响默认的级联面板。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LXdyYXAgZ2FwLTQgaXRlbXMtY2VudGVyXCI+XG4gICAgPGVsLWNhc2NhZGVyXG4gICAgICB2LW1vZGVsPVwidmFsdWVcIlxuICAgICAgOm9wdGlvbnM9XCJvcHRpb25zXCJcbiAgICAgIHBsYWNlaG9sZGVyPVwiRGVmYXVsdCBleHBhbmRpbmcgcGFuZWxcIlxuICAgICAgZmlsdGVyYWJsZVxuICAgIC8+XG5cbiAgICA8ZWwtY2FzY2FkZXJcbiAgICAgIHYtbW9kZWw9XCJ2YWx1ZVwiXG4gICAgICA6b3B0aW9ucz1cIm9wdGlvbnNcIlxuICAgICAgcGxhY2Vob2xkZXI9XCJGaXQgaW5wdXQgd2lkdGhcIlxuICAgICAgZmlsdGVyYWJsZVxuICAgICAgZml0LWlucHV0LXdpZHRoXG4gICAgLz5cblxuICAgIDxlbC1jYXNjYWRlclxuICAgICAgdi1tb2RlbD1cInZhbHVlXCJcbiAgICAgIDpvcHRpb25zPVwib3B0aW9uc1wiXG4gICAgICBwbGFjZWhvbGRlcj1cIkZpeGVkIHdpZHRoICg0MDBweClcIlxuICAgICAgZmlsdGVyYWJsZVxuICAgICAgOmZpdC1pbnB1dC13aWR0aD1cIjQwMFwiXG4gICAgPlxuICAgICAgPHRlbXBsYXRlICNzdWdnZXN0aW9uLWl0ZW09XCJ7IGl0ZW0gfVwiPlxuICAgICAgICA8ZGl2Pnt7IGl0ZW0udGV4dCB9fSAoQ3VzdG9tIGNvbnRlbnQgdGhhdCBpcyB2ZXJ5IGxvbmcpPC9kaXY+XG4gICAgICA8L3RlbXBsYXRlPlxuICAgIDwvZWwtY2FzY2FkZXI+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgdmFsdWUgPSByZWYoKVxuY29uc3Qgb3B0aW9ucyA9IFtcbiAge1xuICAgIHZhbHVlOiAnZ3VpZGUnLFxuICAgIGxhYmVsOiAnR3VpZGUnLFxuICAgIGNoaWxkcmVuOiBbXG4gICAgICB7XG4gICAgICAgIHZhbHVlOiAnZGlzY2lwbGluZXMnLFxuICAgICAgICBsYWJlbDogJ0Rpc2NpcGxpbmVzJyxcbiAgICAgICAgY2hpbGRyZW46IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICB2YWx1ZTogJ2NvbnNpc3RlbmN5JyxcbiAgICAgICAgICAgIGxhYmVsOiAnQ29uc2lzdGVuY3knLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdmZWVkYmFjaycsXG4gICAgICAgICAgICBsYWJlbDogJ0ZlZWRiYWNrJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnZWZmaWNpZW5jeScsXG4gICAgICAgICAgICBsYWJlbDogJ0VmZmljaWVuY3knLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdjb250cm9sbGFiaWxpdHknLFxuICAgICAgICAgICAgbGFiZWw6ICdDb250cm9sbGFiaWxpdHknLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICB2YWx1ZTogJ25hdmlnYXRpb24nLFxuICAgICAgICBsYWJlbDogJ05hdmlnYXRpb24nLFxuICAgICAgICBjaGlsZHJlbjogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIHZhbHVlOiAnc2lkZSBuYXYnLFxuICAgICAgICAgICAgbGFiZWw6ICdTaWRlIE5hdmlnYXRpb24nLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICd0b3AgbmF2JyxcbiAgICAgICAgICAgIGxhYmVsOiAnVG9wIE5hdmlnYXRpb24nLFxuICAgICAgICAgIH0sXG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgIF0sXG4gIH0sXG5dXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/cascader/fit-input-width.vue)_

vue

```
<template>
  <div class="flex flex-wrap gap-4 items-center">
    <el-cascader
      v-model="value"
      :options="options"
      placeholder="Default expanding panel"
      filterable
    />

    <el-cascader
      v-model="value"
      :options="options"
      placeholder="Fit input width"
      filterable
      fit-input-width
    />

    <el-cascader
      v-model="value"
      :options="options"
      placeholder="Fixed width (400px)"
      filterable
      :fit-input-width="400"
    >
      <template #suggestion-item="{ item }">
        <div>{{ item.text }} (Custom content that is very long)</div>
      </template>
    </el-cascader>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref()
const options = [
  {
    value: 'guide',
    label: 'Guide',
    children: [
      {
        value: 'disciplines',
        label: 'Disciplines',
        children: [
          {
            value: 'consistency',
            label: 'Consistency',
          },
          {
            value: 'feedback',
            label: 'Feedback',
          },
          {
            value: 'efficiency',
            label: 'Efficiency',
          },
          {
            value: 'controllability',
            label: 'Controllability',
          },
        ],
      },
      {
        value: 'navigation',
        label: 'Navigation',
        children: [
          {
            value: 'side nav',
            label: 'Side Navigation',
          },
          {
            value: 'top nav',
            label: 'Top Navigation',
          },
        ],
      },
    ],
  },
]
</script>
```

隐藏源代码

## Cascader API [​](#cascader-api)

### Cascader Attributes [​](#cascader-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| model-value / v-model | 选中项绑定值 | `string` / `number` /`array` | — |
| options | 选项的数据源， `value` 和 `label` 可以通过 `CascaderProps` 自定义. | `array` | — |
| [props](#cascaderprops) | 配置选项, 请参阅下面 `CascaderProps` 表。 | `object` | — |
| size | 尺寸 | `enum` | — |
| placeholder | 输入框占位文本 | `string` | — |
| disabled | 是否禁用 | `boolean` | — |
| clearable | 是否支持清空选项 | `boolean` | — |
| clear-icon 2.11.0 | 自定义清除图标 | `string` / `object` | CircleClose |
| show-all-levels | 输入框中是否显示选中值的完整路径 | `boolean` | true |
| collapse-tags | 多选模式下是否折叠Tag | `boolean` | — |
| collapse-tags-tooltip | 当鼠标悬停于折叠标签的文本时，是否显示所有选中的标签。 要使用此属性，`collapse-tags`属性必须设定为 true | `boolean` | false |
| max-collapse-tags-tooltip-height 2.10.2 | collapse tags 的最大高度 | `string` / `number` | — |
| separator | 用于分隔选项的字符 | `string` | ' / ' |
| filterable | 该选项是否可以被搜索 | `boolean` | — |
| filter-method | 自定义搜索逻辑，第一个参数是`node`，第二个参数是`keyword`，返回的布尔值表示是否保留该选项 | `Function` | — |
| debounce | 搜索关键词正在输入时的去抖延迟，单位为毫秒 | `number` | 300 |
| before-filter | 过滤函数调用前，所要调用的钩子函数，该函数接收要过滤的值作为参数。 如果该函数的返回值是 `false` 或者是一个被拒绝的 `Promise`，那么接下来的过滤逻辑便不会执行。 | `Function` | — |
| popper-class | Cascader 下拉菜单和标签提示的自定义类名 | `string` | '' |
| popper-style | Cascader 下拉菜单和标签提示的自定义样式 | `string` / `object` | — |
| teleported | 弹层是否使用 teleport | `boolean` | true |
| effect 2.10.5 | tooltip 主题，内置了 `dark` / `light` 两种 | `enum` / `string` | light |
| tag-type | 标签类型 | `enum` | info |
| tag-effect 2.7.8 | tag effect | `enum` | light |
| validate-event | 输入时是否触发表单的校验 | `boolean` | true |
| max-collapse-tags 2.3.10 | 需要显示的 Tag 的最大数量 要使用此功能，`collapse-tags`的值必须为true | `number` | 1 |
| empty-values 2.7.0 | 组件的空值配置， [参考config-provider](https://element-plus.org/zh-CN/component/config-provider#empty-values-configurations) | `array` | — |
| value-on-clear 2.7.0 | 清空选项的值， [参考config-provider](https://element-plus.org/zh-CN/component/config-provider#empty-values-configurations) | `string` / `number` / `boolean` / `Function` | — |
| persistent 2.7.8 | 当下拉框未被激活并且`persistent`设置为`false`，下拉框容器会被删除。 | `boolean` | true |
| fallback-placements 2.8.1 | Tooltip 可用的 positions 请查看[popper.js 文档](https://popper.js.org/docs/v2/modifiers/flip/#fallbackplacements) | `array` | — |
| placement 2.8.1 | 下拉框出现的位置 | `enum` | bottom-start |
| popper-append-to-body deprecated | 是否将弹出的内容直接插入到 body 元素。 在弹出内容的边框定位出现问题时，可将该属性设置为 false | `boolean` | true |
| show-checked-strategy 2.10.5 | 多选模式下已选节点的展示策略。 当你想让显示更简洁时，使用 `parent`。 当你想显示每个子项时，使用 `child`。 | `enum` | child |
| virtual-scroll 2.14.0 | 是否为大数据启用虚拟滚动 | `boolean` | false |
| fit-input-width 2.14.0 | 建议面板的宽度是否与输入框一致；如果值为 `number`，则宽度为固定值。 | `boolean` / `number` | false |
| item-size 2.14.0 | 虚拟滚动的节点高度 (px) | `number` | 34 |
| height 2.14.0 | 虚拟滚动的菜单高度 (px) | `number` | 204 |

### Cascader Events [​](#cascader-events)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 当绑定值变化时触发的事件 | `Function` |
| expand-change | 当展开节点发生变化时触发 | `Function` |
| blur | 当失去焦点时触发 | `Function` |
| focus | 当获得焦点时触发 | `Function` |
| clear 2.7.7 | 可清空的单选模式下用户点击清空按钮时触发 | `Function` |
| visible-change | 下拉框出现/隐藏时触发 | `Function` |
| remove-tag | 在多选模式下，移除Tag时触发 | `Function` |

### Cascader Slots [​](#cascader-slots)

| 插槽名 | 说明 | Type |
| --- | --- | --- |
| default | 自定义备选项的节点内容，分别为当前节点的 Node 对象和数据 | `object` |
| empty | 无匹配选项时的内容 | — |
| prefix 2.9.4 | 输入框头部内容 | — |
| suggestion-item 2.9.5 | 搜索时自定义建议项内容 | `object` |
| tag 2.10.3 | 自定义tag样式 | `object` |
| header 2.10.5 | 下拉列表顶部的内容 | — |
| footer 2.10.5 | 下拉列表底部的内容 | — |

### Cascader Exposes [​](#cascader-exposes)

| 方法名 | 说明 | 类型 |
| --- | --- | --- |
| getCheckedNodes | 获取一个当前选中节点的数组。(仅仅是传单) 是否只返回叶选中的节点，默认是 `false` | `Function` |
| cascaderPanelRef | cascader 面板的 ref | `object` |
| togglePopperVisible 2.2.31 | 切换 popper 可见状态 | `Function` |
| contentRef | cascader 内容的 ref | `object` |
| presentText 2.8.4 | 选中的内容文本 | `object` |
| focus 2.11.8 | 使 input 获取焦点 | `Function` |
| blur 2.11.8 | 使 input 失去焦点 | `Function` |

## CascaderPanel API [​](#cascaderpanel-api)

### CascaderPanel Attributes [​](#cascaderpanel-attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| model-value / v-model | 选中项绑定值 | `string`/`number`/`array` | — |
| options | 选项的数据源， `value` 和 `label` 可以通过 `CascaderProps` 自定义. | `array` | — |
| [props](#cascaderprops) | 配置选项, 请参阅下面 `CascaderProps` 表。 | `object` | — |
| virtual-scroll 2.14.0 | 是否为大数据启用虚拟滚动 | `boolean` | false |
| item-size 2.14.0 | 虚拟滚动的节点高度 (px) | `number` | 34 |
| height 2.14.0 | 虚拟滚动的菜单高度 (px) | `number` | 204 |

### CascaderPanel Events [​](#cascaderpanel-events)

| 方法名 | Description | Type |
| --- | --- | --- |
| change | 当选中节点变化时触发 | `Function` |
| update:modelValue | 当绑定值变化时触发的事件 | `Function` |
| expand-change | 当展开节点发生变化时触发 | `Function` |
| close | 面板的关闭事件，提供给 Cascader 以便做更好的判断。 | `Function` |

### CascaderPanel Slots [​](#cascaderpanel-slots)

| 事件名 | 说明 | Type |
| --- | --- | --- |
| default | 下级节点的自定义内容，它们分别是当前节点对象和节点数据。 | `object` |
| empty 2.8.3 | 没有数据时面板的内容。 | — |

### CascaderPanel Exposes [​](#cascaderpanel-exposes)

| 属性名 | 说明 | Type |
| --- | --- | --- |
| getCheckedNodes | 获取一个当前选中节点的数组。(仅仅是传单) 是否只返回叶选中的节点，默认是 `false` | `Function` |
| clearCheckedNodes | 清空选中的节点 | `Function` |

## CascaderProps [​](#cascaderprops)

| 属性 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| expandTrigger | 次级菜单的展开方式 | `enum` | click |
| multiple | 是否多选 | `boolean` | false |
| checkStrictly | 是否严格的遵守父子节点不互相关联 | `boolean` | 你好 |
| emitPath | 在选中节点改变时，是否返回由该节点所在的各级菜单的值所组成的数组，若设置 false，则只返回该节点的值 | `boolean` | true |
| lazy | 是否动态加载子节点，需与 lazyLoad 方法结合使用 | `boolean` | 你好 |
| lazyLoad | 加载动态数据的方法，仅在 lazy 为 true 时有效 reject 参数在 2.11.5 版本及以上支持。 | `Function` | — |
| value | 指定选项的值为选项对象的某个属性值 | `string` | value |
| label | 指定选项标签为选项对象的某个属性值 | `string` | label |
| children | 指定选项的子选项为选项对象的某个属性值 | `string` | children |
| disabled | 指定选项的禁用为选项对象的某个属性值 | `string` | disabled |
| leaf | 指定选项的叶子节点的标志位为选项对象的某个属性值 | `string` | leaf |
| hoverThreshold | hover 时展开菜单的灵敏度阈值 | `number` | 500 |
| checkOnClickNode 2.10.5 | 点击节点时是否选中或取消选中该节点 | `boolean` | 你好 |
| checkOnClickLeaf 2.10.5 | 点击叶子节点（最后一级子节点）时，是否选中或取消选中该节点 | `boolean` | true |
| showPrefix 2.10.5 | 是否显示单选框或复选框的前缀（图标） | `boolean` | true |

## 类型声明 [​](#类型声明)

显示类型声明

ts

```
type CascaderNodeValue = string | number
type CascaderNodePathValue = CascaderNodeValue[]
type CascaderValue =
  | CascaderNodeValue
  | CascaderNodePathValue
  | (CascaderNodeValue | CascaderNodePathValue)[]

type Resolve = (data: any) => void

type ExpandTrigger = 'click' | 'hover'

type LazyLoad = (node: Node, resolve: Resolve, reject: () => void) => void

type isDisabled = (data: CascaderOption, node: Node) => boolean

type isLeaf = (data: CascaderOption, node: Node) => boolean

interface CascaderOption extends Record<string, unknown> {
  label?: string
  value?: CascaderNodeValue
  children?: CascaderOption[]
  disabled?: boolean
  leaf?: boolean
}

interface CascaderProps {
  expandTrigger?: ExpandTrigger
  multiple?: boolean
  checkStrictly?: boolean
  emitPath?: boolean
  lazy?: boolean
  lazyLoad?: LazyLoad
  value?: string
  label?: string
  children?: string
  disabled?: string | isDisabled
  leaf?: string | isLeaf
  hoverThreshold?: number
}

class Node {
  readonly uid: number
  readonly level: number
  readonly value: CascaderNodeValue
  readonly label: string
  readonly pathNodes: Node[]
  readonly pathValues: CascaderNodePathValue
  readonly pathLabels: string[]

  childrenData: ChildrenData
  children: Node[]
  text: string
  loaded: boolean
  /**
   * Is it checked
   *
   * @default false
   */
  checked: boolean
  /**
   * Used to indicate the intermediate state of unchecked and fully checked child nodes
   *
   * @default false
   */
  indeterminate: boolean
  /**
   * Loading Status
   *
   * @default false
   */
  loading: boolean

  // getter
  isDisabled: boolean
  isLeaf: boolean
  valueByOption: CascaderNodeValue | CascaderNodePathValue

  // method
  appendChild(childData: CascaderOption): Node
  calcText(allLevels: boolean, separator: string): string
  broadcast(): void
  emit(): void
  onParentCheck(checked: boolean): void
  onChildCheck(): void
  setCheckState(checked: boolean): void
  doCheck(checked: boolean): void
}

Node as CascaderNode
```

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/cascader) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/cascader.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/cascader.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/36978416?v=4&size=64)](https://github.com/SimonaliaChen)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/82012629?v=4&size=64)](https://github.com/0song)[![](https://avatars.githubusercontent.com/u/22659150?v=4&size=64)](https://github.com/ntnyq)[![](https://avatars.githubusercontent.com/u/30046649?v=4&size=64)](https://github.com/MrWeilian)[![](https://avatars.githubusercontent.com/u/109908413?v=4&size=64)](https://github.com/sleepyShen1989)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/33827314?v=4&size=64)](https://github.com/gjfei)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/179441993?v=4&size=64)](https://github.com/lw56777)[![](https://avatars.githubusercontent.com/u/19850462?v=4&size=64)](https://github.com/jeff-fe)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/117748716?v=4&size=64)](https://github.com/thinkasany)[![](https://avatars.githubusercontent.com/u/75473409?v=4&size=64)](https://github.com/lxKylin)[![](https://avatars.githubusercontent.com/u/16513587?v=4&size=64)](https://github.com/oooah)[![](https://avatars.githubusercontent.com/u/49630878?v=4&size=64)](https://github.com/a869246700)[![](https://avatars.githubusercontent.com/u/67454874?v=4&size=64)](https://github.com/nigiwen)[![](https://avatars.githubusercontent.com/u/163709439?v=4&size=64)](https://github.com/upthen)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/9692408?v=4&size=64)](https://github.com/DiamondYuan)[![](https://avatars.githubusercontent.com/u/63226115?v=4&size=64)](https://github.com/DavidKitano)[![](https://avatars.githubusercontent.com/u/35138018?v=4&size=64)](https://github.com/tuskermanshu)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/15872986?v=4&size=64)](https://github.com/chenweiyi)[![](https://avatars.githubusercontent.com/u/169252980?v=4&size=64)](https://github.com/xiaochenchen-igg-com)[![](https://avatars.githubusercontent.com/u/73569598?v=4&size=64)](https://github.com/sechi747)[![](https://avatars.githubusercontent.com/u/127809872?v=4&size=64)](https://github.com/123outsider)[![](https://avatars.githubusercontent.com/u/54931083?v=4&size=64)](https://github.com/wjp980108)[![](https://avatars.githubusercontent.com/u/26999792?v=4&size=64)](https://github.com/plainheart)[![](https://avatars.githubusercontent.com/u/17698194?v=4&size=64)](https://github.com/nieyuyao)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/57179957?v=4&size=64)](https://github.com/yeonjulee1005)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/121680374?v=4&size=64)](https://github.com/kaine0923)[![](https://avatars.githubusercontent.com/u/101238421?v=4&size=64)](https://github.com/acyza)[![](https://avatars.githubusercontent.com/u/30114549?v=4&size=64)](https://github.com/loosheng)[![](https://avatars.githubusercontent.com/u/10278227?v=4&size=64)](https://github.com/HeftyKoo)[![](https://avatars.githubusercontent.com/u/6134068?v=4&size=64)](https://github.com/CarterLi)[![](https://avatars.githubusercontent.com/u/57385187?v=4&size=64)](https://github.com/opengraphica)[![](https://avatars.githubusercontent.com/u/62927479?v=4&size=64)](https://github.com/anflower)[![](https://avatars.githubusercontent.com/u/2883231?v=4&size=64)](https://github.com/HerringtonDarkholme)[![](https://avatars.githubusercontent.com/u/23303044?v=4&size=64)](https://github.com/imswk)[![](https://avatars.githubusercontent.com/u/39672197?v=4&size=64)](https://github.com/bchen1029)

[Autocomplete 自动补全输入框](https://element-plus.org/zh-CN/component/autocomplete)

[Checkbox 多选框](https://element-plus.org/zh-CN/component/checkbox)


