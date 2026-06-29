---
name: "collapse"
description: "Collapse 折叠面板 -- Element Plus Vue3 桌面端组件。Invoke when user needs Collapse 折叠面板 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/collapse.html"
---

---

# Collapse 折叠面板 [​](#collapse-折叠面板)

更新日志待解决

12

通过折叠面板收纳内容区域

## 基础用法 [​](#基础用法)

可同时展开多个面板，面板之间不影响

Consistency

Consistent with real life: in line with the process and logic of real life, and comply with languages and habits that the users are used to;

Consistent within interface: all elements should be consistent, such as: design style, icons and texts, position of elements, etc.

Feedback

Operation feedback: enable the users to clearly perceive their operations by style updates and interactive effects;

Visual feedback: reflect current state by updating or rearranging elements of the page.

Efficiency

Simplify the process: keep operating process simple and intuitive;

Definite and clear: enunciate your intentions clearly so that the users can quickly understand and make decisions;

Easy to identify: the interface should be straightforward, which helps the users to identify and frees them from memorizing and recalling.

Controllability

Decision making: giving advice about operations is acceptable, but do not make decisions for the users;

Controlled consequences: users should be granted the freedom to operate, including canceling, aborting or terminating current operation.

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1jb2xsYXBzZVwiPlxuICAgIDxlbC1jb2xsYXBzZSB2LW1vZGVsPVwiYWN0aXZlTmFtZXNcIiBAY2hhbmdlPVwiaGFuZGxlQ2hhbmdlXCI+XG4gICAgICA8ZWwtY29sbGFwc2UtaXRlbSB0aXRsZT1cIkNvbnNpc3RlbmN5XCIgbmFtZT1cIjFcIj5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBDb25zaXN0ZW50IHdpdGggcmVhbCBsaWZlOiBpbiBsaW5lIHdpdGggdGhlIHByb2Nlc3MgYW5kIGxvZ2ljIG9mIHJlYWxcbiAgICAgICAgICBsaWZlLCBhbmQgY29tcGx5IHdpdGggbGFuZ3VhZ2VzIGFuZCBoYWJpdHMgdGhhdCB0aGUgdXNlcnMgYXJlIHVzZWQgdG87XG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2PlxuICAgICAgICAgIENvbnNpc3RlbnQgd2l0aGluIGludGVyZmFjZTogYWxsIGVsZW1lbnRzIHNob3VsZCBiZSBjb25zaXN0ZW50LCBzdWNoXG4gICAgICAgICAgYXM6IGRlc2lnbiBzdHlsZSwgaWNvbnMgYW5kIHRleHRzLCBwb3NpdGlvbiBvZiBlbGVtZW50cywgZXRjLlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZWwtY29sbGFwc2UtaXRlbT5cbiAgICAgIDxlbC1jb2xsYXBzZS1pdGVtIHRpdGxlPVwiRmVlZGJhY2tcIiBuYW1lPVwiMlwiPlxuICAgICAgICA8ZGl2PlxuICAgICAgICAgIE9wZXJhdGlvbiBmZWVkYmFjazogZW5hYmxlIHRoZSB1c2VycyB0byBjbGVhcmx5IHBlcmNlaXZlIHRoZWlyXG4gICAgICAgICAgb3BlcmF0aW9ucyBieSBzdHlsZSB1cGRhdGVzIGFuZCBpbnRlcmFjdGl2ZSBlZmZlY3RzO1xuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBWaXN1YWwgZmVlZGJhY2s6IHJlZmxlY3QgY3VycmVudCBzdGF0ZSBieSB1cGRhdGluZyBvciByZWFycmFuZ2luZ1xuICAgICAgICAgIGVsZW1lbnRzIG9mIHRoZSBwYWdlLlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZWwtY29sbGFwc2UtaXRlbT5cbiAgICAgIDxlbC1jb2xsYXBzZS1pdGVtIHRpdGxlPVwiRWZmaWNpZW5jeVwiIG5hbWU9XCIzXCI+XG4gICAgICAgIDxkaXY+XG4gICAgICAgICAgU2ltcGxpZnkgdGhlIHByb2Nlc3M6IGtlZXAgb3BlcmF0aW5nIHByb2Nlc3Mgc2ltcGxlIGFuZCBpbnR1aXRpdmU7XG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2PlxuICAgICAgICAgIERlZmluaXRlIGFuZCBjbGVhcjogZW51bmNpYXRlIHlvdXIgaW50ZW50aW9ucyBjbGVhcmx5IHNvIHRoYXQgdGhlXG4gICAgICAgICAgdXNlcnMgY2FuIHF1aWNrbHkgdW5kZXJzdGFuZCBhbmQgbWFrZSBkZWNpc2lvbnM7XG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2PlxuICAgICAgICAgIEVhc3kgdG8gaWRlbnRpZnk6IHRoZSBpbnRlcmZhY2Ugc2hvdWxkIGJlIHN0cmFpZ2h0Zm9yd2FyZCwgd2hpY2ggaGVscHNcbiAgICAgICAgICB0aGUgdXNlcnMgdG8gaWRlbnRpZnkgYW5kIGZyZWVzIHRoZW0gZnJvbSBtZW1vcml6aW5nIGFuZCByZWNhbGxpbmcuXG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9lbC1jb2xsYXBzZS1pdGVtPlxuICAgICAgPGVsLWNvbGxhcHNlLWl0ZW0gdGl0bGU9XCJDb250cm9sbGFiaWxpdHlcIiBuYW1lPVwiNFwiPlxuICAgICAgICA8ZGl2PlxuICAgICAgICAgIERlY2lzaW9uIG1ha2luZzogZ2l2aW5nIGFkdmljZSBhYm91dCBvcGVyYXRpb25zIGlzIGFjY2VwdGFibGUsIGJ1dCBkb1xuICAgICAgICAgIG5vdCBtYWtlIGRlY2lzaW9ucyBmb3IgdGhlIHVzZXJzO1xuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBDb250cm9sbGVkIGNvbnNlcXVlbmNlczogdXNlcnMgc2hvdWxkIGJlIGdyYW50ZWQgdGhlIGZyZWVkb20gdG9cbiAgICAgICAgICBvcGVyYXRlLCBpbmNsdWRpbmcgY2FuY2VsaW5nLCBhYm9ydGluZyBvciB0ZXJtaW5hdGluZyBjdXJyZW50XG4gICAgICAgICAgb3BlcmF0aW9uLlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZWwtY29sbGFwc2UtaXRlbT5cbiAgICA8L2VsLWNvbGxhcHNlPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmltcG9ydCB0eXBlIHsgQ29sbGFwc2VNb2RlbFZhbHVlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBhY3RpdmVOYW1lcyA9IHJlZihbJzEnXSlcbmNvbnN0IGhhbmRsZUNoYW5nZSA9ICh2YWw6IENvbGxhcHNlTW9kZWxWYWx1ZSkgPT4ge1xuICBjb25zb2xlLmxvZyh2YWwpXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/collapse/basic.vue)_

vue

```
<template>
  <div class="demo-collapse">
    <el-collapse v-model="activeNames" @change="handleChange">
      <el-collapse-item title="Consistency" name="1">
        <div>
          Consistent with real life: in line with the process and logic of real
          life, and comply with languages and habits that the users are used to;
        </div>
        <div>
          Consistent within interface: all elements should be consistent, such
          as: design style, icons and texts, position of elements, etc.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Feedback" name="2">
        <div>
          Operation feedback: enable the users to clearly perceive their
          operations by style updates and interactive effects;
        </div>
        <div>
          Visual feedback: reflect current state by updating or rearranging
          elements of the page.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Efficiency" name="3">
        <div>
          Simplify the process: keep operating process simple and intuitive;
        </div>
        <div>
          Definite and clear: enunciate your intentions clearly so that the
          users can quickly understand and make decisions;
        </div>
        <div>
          Easy to identify: the interface should be straightforward, which helps
          the users to identify and frees them from memorizing and recalling.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Controllability" name="4">
        <div>
          Decision making: giving advice about operations is acceptable, but do
          not make decisions for the users;
        </div>
        <div>
          Controlled consequences: users should be granted the freedom to
          operate, including canceling, aborting or terminating current
          operation.
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { CollapseModelValue } from 'element-plus'

const activeNames = ref(['1'])
const handleChange = (val: CollapseModelValue) => {
  console.log(val)
}
</script>
```

隐藏源代码

## 手风琴效果 [​](#手风琴效果)

每次只能展开一个面板

通过 `accordion` 属性来设置是否以手风琴模式显示。

Consistency

Consistent with real life: in line with the process and logic of real life, and comply with languages and habits that the users are used to;

Consistent within interface: all elements should be consistent, such as: design style, icons and texts, position of elements, etc.

Feedback

Operation feedback: enable the users to clearly perceive their operations by style updates and interactive effects;

Visual feedback: reflect current state by updating or rearranging elements of the page.

Efficiency

Simplify the process: keep operating process simple and intuitive;

Definite and clear: enunciate your intentions clearly so that the users can quickly understand and make decisions;

Easy to identify: the interface should be straightforward, which helps the users to identify and frees them from memorizing and recalling.

Controllability

Decision making: giving advices about operations is acceptable, but do not make decisions for the users;

Controlled consequences: users should be granted the freedom to operate, including canceling, aborting or terminating current operation.

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1jb2xsYXBzZVwiPlxuICAgIDxlbC1jb2xsYXBzZSB2LW1vZGVsPVwiYWN0aXZlTmFtZVwiIGFjY29yZGlvbj5cbiAgICAgIDxlbC1jb2xsYXBzZS1pdGVtIHRpdGxlPVwiQ29uc2lzdGVuY3lcIiBuYW1lPVwiMVwiPlxuICAgICAgICA8ZGl2PlxuICAgICAgICAgIENvbnNpc3RlbnQgd2l0aCByZWFsIGxpZmU6IGluIGxpbmUgd2l0aCB0aGUgcHJvY2VzcyBhbmQgbG9naWMgb2YgcmVhbFxuICAgICAgICAgIGxpZmUsIGFuZCBjb21wbHkgd2l0aCBsYW5ndWFnZXMgYW5kIGhhYml0cyB0aGF0IHRoZSB1c2VycyBhcmUgdXNlZCB0bztcbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXY+XG4gICAgICAgICAgQ29uc2lzdGVudCB3aXRoaW4gaW50ZXJmYWNlOiBhbGwgZWxlbWVudHMgc2hvdWxkIGJlIGNvbnNpc3RlbnQsIHN1Y2hcbiAgICAgICAgICBhczogZGVzaWduIHN0eWxlLCBpY29ucyBhbmQgdGV4dHMsIHBvc2l0aW9uIG9mIGVsZW1lbnRzLCBldGMuXG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9lbC1jb2xsYXBzZS1pdGVtPlxuICAgICAgPGVsLWNvbGxhcHNlLWl0ZW0gdGl0bGU9XCJGZWVkYmFja1wiIG5hbWU9XCIyXCI+XG4gICAgICAgIDxkaXY+XG4gICAgICAgICAgT3BlcmF0aW9uIGZlZWRiYWNrOiBlbmFibGUgdGhlIHVzZXJzIHRvIGNsZWFybHkgcGVyY2VpdmUgdGhlaXJcbiAgICAgICAgICBvcGVyYXRpb25zIGJ5IHN0eWxlIHVwZGF0ZXMgYW5kIGludGVyYWN0aXZlIGVmZmVjdHM7XG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2PlxuICAgICAgICAgIFZpc3VhbCBmZWVkYmFjazogcmVmbGVjdCBjdXJyZW50IHN0YXRlIGJ5IHVwZGF0aW5nIG9yIHJlYXJyYW5naW5nXG4gICAgICAgICAgZWxlbWVudHMgb2YgdGhlIHBhZ2UuXG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9lbC1jb2xsYXBzZS1pdGVtPlxuICAgICAgPGVsLWNvbGxhcHNlLWl0ZW0gdGl0bGU9XCJFZmZpY2llbmN5XCIgbmFtZT1cIjNcIj5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBTaW1wbGlmeSB0aGUgcHJvY2Vzczoga2VlcCBvcGVyYXRpbmcgcHJvY2VzcyBzaW1wbGUgYW5kIGludHVpdGl2ZTtcbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXY+XG4gICAgICAgICAgRGVmaW5pdGUgYW5kIGNsZWFyOiBlbnVuY2lhdGUgeW91ciBpbnRlbnRpb25zIGNsZWFybHkgc28gdGhhdCB0aGVcbiAgICAgICAgICB1c2VycyBjYW4gcXVpY2tseSB1bmRlcnN0YW5kIGFuZCBtYWtlIGRlY2lzaW9ucztcbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXY+XG4gICAgICAgICAgRWFzeSB0byBpZGVudGlmeTogdGhlIGludGVyZmFjZSBzaG91bGQgYmUgc3RyYWlnaHRmb3J3YXJkLCB3aGljaCBoZWxwc1xuICAgICAgICAgIHRoZSB1c2VycyB0byBpZGVudGlmeSBhbmQgZnJlZXMgdGhlbSBmcm9tIG1lbW9yaXppbmcgYW5kIHJlY2FsbGluZy5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2VsLWNvbGxhcHNlLWl0ZW0+XG4gICAgICA8ZWwtY29sbGFwc2UtaXRlbSB0aXRsZT1cIkNvbnRyb2xsYWJpbGl0eVwiIG5hbWU9XCI0XCI+XG4gICAgICAgIDxkaXY+XG4gICAgICAgICAgRGVjaXNpb24gbWFraW5nOiBnaXZpbmcgYWR2aWNlcyBhYm91dCBvcGVyYXRpb25zIGlzIGFjY2VwdGFibGUsIGJ1dCBkb1xuICAgICAgICAgIG5vdCBtYWtlIGRlY2lzaW9ucyBmb3IgdGhlIHVzZXJzO1xuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBDb250cm9sbGVkIGNvbnNlcXVlbmNlczogdXNlcnMgc2hvdWxkIGJlIGdyYW50ZWQgdGhlIGZyZWVkb20gdG9cbiAgICAgICAgICBvcGVyYXRlLCBpbmNsdWRpbmcgY2FuY2VsaW5nLCBhYm9ydGluZyBvciB0ZXJtaW5hdGluZyBjdXJyZW50XG4gICAgICAgICAgb3BlcmF0aW9uLlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZWwtY29sbGFwc2UtaXRlbT5cbiAgICA8L2VsLWNvbGxhcHNlPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IGFjdGl2ZU5hbWUgPSByZWYoJzEnKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/collapse/accordion.vue)_

vue

```
<template>
  <div class="demo-collapse">
    <el-collapse v-model="activeName" accordion>
      <el-collapse-item title="Consistency" name="1">
        <div>
          Consistent with real life: in line with the process and logic of real
          life, and comply with languages and habits that the users are used to;
        </div>
        <div>
          Consistent within interface: all elements should be consistent, such
          as: design style, icons and texts, position of elements, etc.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Feedback" name="2">
        <div>
          Operation feedback: enable the users to clearly perceive their
          operations by style updates and interactive effects;
        </div>
        <div>
          Visual feedback: reflect current state by updating or rearranging
          elements of the page.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Efficiency" name="3">
        <div>
          Simplify the process: keep operating process simple and intuitive;
        </div>
        <div>
          Definite and clear: enunciate your intentions clearly so that the
          users can quickly understand and make decisions;
        </div>
        <div>
          Easy to identify: the interface should be straightforward, which helps
          the users to identify and frees them from memorizing and recalling.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Controllability" name="4">
        <div>
          Decision making: giving advices about operations is acceptable, but do
          not make decisions for the users;
        </div>
        <div>
          Controlled consequences: users should be granted the freedom to
          operate, including canceling, aborting or terminating current
          operation.
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const activeName = ref('1')
</script>
```

隐藏源代码

## 自定义面板标题 [​](#自定义面板标题)

除了可以通过 `title` 属性以外，还可以通过具名 `slot` 来实现自定义面板的标题内容，以实现增加图标等效果。

TIP

从版本 2.9.10开始， `title` 插槽提供一个 `isActive` 属性，显示当前折叠项是否活跃。

Consistency

Consistent with real life: in line with the process and logic of real life, and comply with languages and habits that the users are used to;

Consistent within interface: all elements should be consistent, such as: design style, icons and texts, position of elements, etc.

Feedback

Operation feedback: enable the users to clearly perceive their operations by style updates and interactive effects;

Visual feedback: reflect current state by updating or rearranging elements of the page.

Efficiency

Simplify the process: keep operating process simple and intuitive;

Definite and clear: enunciate your intentions clearly so that the users can quickly understand and make decisions;

Easy to identify: the interface should be straightforward, which helps the users to identify and frees them from memorizing and recalling.

Controllability

Decision making: giving advices about operations is acceptable, but do not make decisions for the users;

Controlled consequences: users should be granted the freedom to operate, including canceling, aborting or terminating current operation.

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1jb2xsYXBzZVwiPlxuICAgIDxlbC1jb2xsYXBzZSBhY2NvcmRpb24+XG4gICAgICA8ZWwtY29sbGFwc2UtaXRlbSBuYW1lPVwiMVwiPlxuICAgICAgICA8dGVtcGxhdGUgI3RpdGxlPVwieyBpc0FjdGl2ZSB9XCI+XG4gICAgICAgICAgPGRpdiA6Y2xhc3M9XCJbJ3RpdGxlLXdyYXBwZXInLCB7ICdpcy1hY3RpdmUnOiBpc0FjdGl2ZSB9XVwiPlxuICAgICAgICAgICAgQ29uc2lzdGVuY3lcbiAgICAgICAgICAgIDxlbC1pY29uIGNsYXNzPVwiaGVhZGVyLWljb25cIj5cbiAgICAgICAgICAgICAgPGluZm8tZmlsbGVkIC8+XG4gICAgICAgICAgICA8L2VsLWljb24+XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICAgIDxkaXY+XG4gICAgICAgICAgQ29uc2lzdGVudCB3aXRoIHJlYWwgbGlmZTogaW4gbGluZSB3aXRoIHRoZSBwcm9jZXNzIGFuZCBsb2dpYyBvZiByZWFsXG4gICAgICAgICAgbGlmZSwgYW5kIGNvbXBseSB3aXRoIGxhbmd1YWdlcyBhbmQgaGFiaXRzIHRoYXQgdGhlIHVzZXJzIGFyZSB1c2VkIHRvO1xuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBDb25zaXN0ZW50IHdpdGhpbiBpbnRlcmZhY2U6IGFsbCBlbGVtZW50cyBzaG91bGQgYmUgY29uc2lzdGVudCwgc3VjaFxuICAgICAgICAgIGFzOiBkZXNpZ24gc3R5bGUsIGljb25zIGFuZCB0ZXh0cywgcG9zaXRpb24gb2YgZWxlbWVudHMsIGV0Yy5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2VsLWNvbGxhcHNlLWl0ZW0+XG4gICAgICA8ZWwtY29sbGFwc2UtaXRlbSB0aXRsZT1cIkZlZWRiYWNrXCIgbmFtZT1cIjJcIj5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBPcGVyYXRpb24gZmVlZGJhY2s6IGVuYWJsZSB0aGUgdXNlcnMgdG8gY2xlYXJseSBwZXJjZWl2ZSB0aGVpclxuICAgICAgICAgIG9wZXJhdGlvbnMgYnkgc3R5bGUgdXBkYXRlcyBhbmQgaW50ZXJhY3RpdmUgZWZmZWN0cztcbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXY+XG4gICAgICAgICAgVmlzdWFsIGZlZWRiYWNrOiByZWZsZWN0IGN1cnJlbnQgc3RhdGUgYnkgdXBkYXRpbmcgb3IgcmVhcnJhbmdpbmdcbiAgICAgICAgICBlbGVtZW50cyBvZiB0aGUgcGFnZS5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2VsLWNvbGxhcHNlLWl0ZW0+XG4gICAgICA8ZWwtY29sbGFwc2UtaXRlbSB0aXRsZT1cIkVmZmljaWVuY3lcIiBuYW1lPVwiM1wiPlxuICAgICAgICA8ZGl2PlxuICAgICAgICAgIFNpbXBsaWZ5IHRoZSBwcm9jZXNzOiBrZWVwIG9wZXJhdGluZyBwcm9jZXNzIHNpbXBsZSBhbmQgaW50dWl0aXZlO1xuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBEZWZpbml0ZSBhbmQgY2xlYXI6IGVudW5jaWF0ZSB5b3VyIGludGVudGlvbnMgY2xlYXJseSBzbyB0aGF0IHRoZVxuICAgICAgICAgIHVzZXJzIGNhbiBxdWlja2x5IHVuZGVyc3RhbmQgYW5kIG1ha2UgZGVjaXNpb25zO1xuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBFYXN5IHRvIGlkZW50aWZ5OiB0aGUgaW50ZXJmYWNlIHNob3VsZCBiZSBzdHJhaWdodGZvcndhcmQsIHdoaWNoIGhlbHBzXG4gICAgICAgICAgdGhlIHVzZXJzIHRvIGlkZW50aWZ5IGFuZCBmcmVlcyB0aGVtIGZyb20gbWVtb3JpemluZyBhbmQgcmVjYWxsaW5nLlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZWwtY29sbGFwc2UtaXRlbT5cbiAgICAgIDxlbC1jb2xsYXBzZS1pdGVtIHRpdGxlPVwiQ29udHJvbGxhYmlsaXR5XCIgbmFtZT1cIjRcIj5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBEZWNpc2lvbiBtYWtpbmc6IGdpdmluZyBhZHZpY2VzIGFib3V0IG9wZXJhdGlvbnMgaXMgYWNjZXB0YWJsZSwgYnV0IGRvXG4gICAgICAgICAgbm90IG1ha2UgZGVjaXNpb25zIGZvciB0aGUgdXNlcnM7XG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2PlxuICAgICAgICAgIENvbnRyb2xsZWQgY29uc2VxdWVuY2VzOiB1c2VycyBzaG91bGQgYmUgZ3JhbnRlZCB0aGUgZnJlZWRvbSB0b1xuICAgICAgICAgIG9wZXJhdGUsIGluY2x1ZGluZyBjYW5jZWxpbmcsIGFib3J0aW5nIG9yIHRlcm1pbmF0aW5nIGN1cnJlbnRcbiAgICAgICAgICBvcGVyYXRpb24uXG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9lbC1jb2xsYXBzZS1pdGVtPlxuICAgIDwvZWwtY29sbGFwc2U+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IEluZm9GaWxsZWQgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLnRpdGxlLXdyYXBwZXIge1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xuICBnYXA6IDRweDtcbn1cblxuLnRpdGxlLXdyYXBwZXIuaXMtYWN0aXZlIHtcbiAgY29sb3I6IHZhcigtLWVsLWNvbG9yLXByaW1hcnkpO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/collapse/customization.vue)_

vue

```
<template>
  <div class="demo-collapse">
    <el-collapse accordion>
      <el-collapse-item name="1">
        <template #title="{ isActive }">
          <div :class="['title-wrapper', { 'is-active': isActive }]">
            Consistency
            <el-icon class="header-icon">
              <info-filled />
            </el-icon>
          </div>
        </template>
        <div>
          Consistent with real life: in line with the process and logic of real
          life, and comply with languages and habits that the users are used to;
        </div>
        <div>
          Consistent within interface: all elements should be consistent, such
          as: design style, icons and texts, position of elements, etc.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Feedback" name="2">
        <div>
          Operation feedback: enable the users to clearly perceive their
          operations by style updates and interactive effects;
        </div>
        <div>
          Visual feedback: reflect current state by updating or rearranging
          elements of the page.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Efficiency" name="3">
        <div>
          Simplify the process: keep operating process simple and intuitive;
        </div>
        <div>
          Definite and clear: enunciate your intentions clearly so that the
          users can quickly understand and make decisions;
        </div>
        <div>
          Easy to identify: the interface should be straightforward, which helps
          the users to identify and frees them from memorizing and recalling.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Controllability" name="4">
        <div>
          Decision making: giving advices about operations is acceptable, but do
          not make decisions for the users;
        </div>
        <div>
          Controlled consequences: users should be granted the freedom to
          operate, including canceling, aborting or terminating current
          operation.
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script setup lang="ts">
import { InfoFilled } from '@element-plus/icons-vue'
</script>

<style scoped>
.title-wrapper {
  display: flex;
  align-items: center;
  gap: 4px;
}

.title-wrapper.is-active {
  color: var(--el-color-primary);
}
</style>
```

隐藏源代码

## 自定义图标 2.8.3 [​](#自定义图标)

除了使用 `icon` 属性外，您还可以自定义面板项目图标，从而添加自定义内容。

Consistency

Consistent with real life: in line with the process and logic of real life, and comply with languages and habits that the users are used to;

Consistent within interface: all elements should be consistent, such as: design style, icons and texts, position of elements, etc.

FeedbackCollapsed

Operation feedback: enable the users to clearly perceive their operations by style updates and interactive effects;

Visual feedback: reflect current state by updating or rearranging elements of the page.

Efficiency

Simplify the process: keep operating process simple and intuitive;

Definite and clear: enunciate your intentions clearly so that the users can quickly understand and make decisions;

Easy to identify: the interface should be straightforward, which helps the users to identify and frees them from memorizing and recalling.

Controllability

Decision making: giving advices about operations is acceptable, but do not make decisions for the users;

Controlled consequences: users should be granted the freedom to operate, including canceling, aborting or terminating current operation.

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1jb2xsYXBzZVwiPlxuICAgIDxlbC1jb2xsYXBzZSB2LW1vZGVsPVwiYWN0aXZlTmFtZXNcIiBAY2hhbmdlPVwiaGFuZGxlQ2hhbmdlXCI+XG4gICAgICA8ZWwtY29sbGFwc2UtaXRlbSB0aXRsZT1cIkNvbnNpc3RlbmN5XCIgbmFtZT1cIjFcIiA6aWNvbj1cIkNhcmV0UmlnaHRcIj5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBDb25zaXN0ZW50IHdpdGggcmVhbCBsaWZlOiBpbiBsaW5lIHdpdGggdGhlIHByb2Nlc3MgYW5kIGxvZ2ljIG9mIHJlYWxcbiAgICAgICAgICBsaWZlLCBhbmQgY29tcGx5IHdpdGggbGFuZ3VhZ2VzIGFuZCBoYWJpdHMgdGhhdCB0aGUgdXNlcnMgYXJlIHVzZWQgdG87XG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2PlxuICAgICAgICAgIENvbnNpc3RlbnQgd2l0aGluIGludGVyZmFjZTogYWxsIGVsZW1lbnRzIHNob3VsZCBiZSBjb25zaXN0ZW50LCBzdWNoXG4gICAgICAgICAgYXM6IGRlc2lnbiBzdHlsZSwgaWNvbnMgYW5kIHRleHRzLCBwb3NpdGlvbiBvZiBlbGVtZW50cywgZXRjLlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZWwtY29sbGFwc2UtaXRlbT5cbiAgICAgIDxlbC1jb2xsYXBzZS1pdGVtIHRpdGxlPVwiRmVlZGJhY2tcIiBuYW1lPVwiMlwiPlxuICAgICAgICA8dGVtcGxhdGUgI2ljb249XCJ7IGlzQWN0aXZlIH1cIj5cbiAgICAgICAgICA8c3BhbiBjbGFzcz1cImljb24tZWxlXCI+XG4gICAgICAgICAgICB7eyBpc0FjdGl2ZSA/ICdFeHBhbmRlZCcgOiAnQ29sbGFwc2VkJyB9fVxuICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBPcGVyYXRpb24gZmVlZGJhY2s6IGVuYWJsZSB0aGUgdXNlcnMgdG8gY2xlYXJseSBwZXJjZWl2ZSB0aGVpclxuICAgICAgICAgIG9wZXJhdGlvbnMgYnkgc3R5bGUgdXBkYXRlcyBhbmQgaW50ZXJhY3RpdmUgZWZmZWN0cztcbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXY+XG4gICAgICAgICAgVmlzdWFsIGZlZWRiYWNrOiByZWZsZWN0IGN1cnJlbnQgc3RhdGUgYnkgdXBkYXRpbmcgb3IgcmVhcnJhbmdpbmdcbiAgICAgICAgICBlbGVtZW50cyBvZiB0aGUgcGFnZS5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2VsLWNvbGxhcHNlLWl0ZW0+XG4gICAgICA8ZWwtY29sbGFwc2UtaXRlbSB0aXRsZT1cIkVmZmljaWVuY3lcIiBuYW1lPVwiM1wiPlxuICAgICAgICA8ZGl2PlxuICAgICAgICAgIFNpbXBsaWZ5IHRoZSBwcm9jZXNzOiBrZWVwIG9wZXJhdGluZyBwcm9jZXNzIHNpbXBsZSBhbmQgaW50dWl0aXZlO1xuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBEZWZpbml0ZSBhbmQgY2xlYXI6IGVudW5jaWF0ZSB5b3VyIGludGVudGlvbnMgY2xlYXJseSBzbyB0aGF0IHRoZVxuICAgICAgICAgIHVzZXJzIGNhbiBxdWlja2x5IHVuZGVyc3RhbmQgYW5kIG1ha2UgZGVjaXNpb25zO1xuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBFYXN5IHRvIGlkZW50aWZ5OiB0aGUgaW50ZXJmYWNlIHNob3VsZCBiZSBzdHJhaWdodGZvcndhcmQsIHdoaWNoIGhlbHBzXG4gICAgICAgICAgdGhlIHVzZXJzIHRvIGlkZW50aWZ5IGFuZCBmcmVlcyB0aGVtIGZyb20gbWVtb3JpemluZyBhbmQgcmVjYWxsaW5nLlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZWwtY29sbGFwc2UtaXRlbT5cbiAgICAgIDxlbC1jb2xsYXBzZS1pdGVtIHRpdGxlPVwiQ29udHJvbGxhYmlsaXR5XCIgbmFtZT1cIjRcIj5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBEZWNpc2lvbiBtYWtpbmc6IGdpdmluZyBhZHZpY2VzIGFib3V0IG9wZXJhdGlvbnMgaXMgYWNjZXB0YWJsZSwgYnV0IGRvXG4gICAgICAgICAgbm90IG1ha2UgZGVjaXNpb25zIGZvciB0aGUgdXNlcnM7XG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2PlxuICAgICAgICAgIENvbnRyb2xsZWQgY29uc2VxdWVuY2VzOiB1c2VycyBzaG91bGQgYmUgZ3JhbnRlZCB0aGUgZnJlZWRvbSB0b1xuICAgICAgICAgIG9wZXJhdGUsIGluY2x1ZGluZyBjYW5jZWxpbmcsIGFib3J0aW5nIG9yIHRlcm1pbmF0aW5nIGN1cnJlbnRcbiAgICAgICAgICBvcGVyYXRpb24uXG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9lbC1jb2xsYXBzZS1pdGVtPlxuICAgIDwvZWwtY29sbGFwc2U+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IENhcmV0UmlnaHQgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuaW1wb3J0IHR5cGUgeyBDb2xsYXBzZU1vZGVsVmFsdWUgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IGFjdGl2ZU5hbWVzID0gcmVmKFsnMSddKVxuY29uc3QgaGFuZGxlQ2hhbmdlID0gKHZhbDogQ29sbGFwc2VNb2RlbFZhbHVlKSA9PiB7XG4gIGNvbnNvbGUubG9nKHZhbClcbn1cbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmljb24tZWxlIHtcbiAgbWFyZ2luOiAwIDhweCAwIGF1dG87XG4gIGNvbG9yOiAjNDA5ZWZmO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/collapse/custom-icon.vue)_

vue

```
<template>
  <div class="demo-collapse">
    <el-collapse v-model="activeNames" @change="handleChange">
      <el-collapse-item title="Consistency" name="1" :icon="CaretRight">
        <div>
          Consistent with real life: in line with the process and logic of real
          life, and comply with languages and habits that the users are used to;
        </div>
        <div>
          Consistent within interface: all elements should be consistent, such
          as: design style, icons and texts, position of elements, etc.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Feedback" name="2">
        <template #icon="{ isActive }">
          <span class="icon-ele">
            {{ isActive ? 'Expanded' : 'Collapsed' }}
          </span>
        </template>
        <div>
          Operation feedback: enable the users to clearly perceive their
          operations by style updates and interactive effects;
        </div>
        <div>
          Visual feedback: reflect current state by updating or rearranging
          elements of the page.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Efficiency" name="3">
        <div>
          Simplify the process: keep operating process simple and intuitive;
        </div>
        <div>
          Definite and clear: enunciate your intentions clearly so that the
          users can quickly understand and make decisions;
        </div>
        <div>
          Easy to identify: the interface should be straightforward, which helps
          the users to identify and frees them from memorizing and recalling.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Controllability" name="4">
        <div>
          Decision making: giving advices about operations is acceptable, but do
          not make decisions for the users;
        </div>
        <div>
          Controlled consequences: users should be granted the freedom to
          operate, including canceling, aborting or terminating current
          operation.
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { CaretRight } from '@element-plus/icons-vue'

import type { CollapseModelValue } from 'element-plus'

const activeNames = ref(['1'])
const handleChange = (val: CollapseModelValue) => {
  console.log(val)
}
</script>

<style scoped>
.icon-ele {
  margin: 0 8px 0 auto;
  color: #409eff;
}
</style>
```

隐藏源代码

## 自定义图标位置 2.9.10 [​](#自定义图标位置)

使用 `expand-icon-position` 属性，您可以自定义图标位置。

expand icon position:

leftright

Consistency

Consistent with real life: in line with the process and logic of real life, and comply with languages and habits that the users are used to;

Consistent within interface: all elements should be consistent, such as: design style, icons and texts, position of elements, etc.

Feedback

Operation feedback: enable the users to clearly perceive their operations by style updates and interactive effects;

Visual feedback: reflect current state by updating or rearranging elements of the page.

Efficiency

Simplify the process: keep operating process simple and intuitive;

Definite and clear: enunciate your intentions clearly so that the users can quickly understand and make decisions;

Easy to identify: the interface should be straightforward, which helps the users to identify and frees them from memorizing and recalling.

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZGVtby1jb2xsYXBzZS1wb3NpdGlvblwiPlxuICAgIDxkaXYgY2xhc3M9XCJmbGV4IGl0ZW1zLWNlbnRlciBtYi00XCI+XG4gICAgICA8c3BhbiBjbGFzcz1cIm1yLTRcIj5leHBhbmQgaWNvbiBwb3NpdGlvbjogPC9zcGFuPlxuICAgICAgPGVsLXN3aXRjaFxuICAgICAgICB2LW1vZGVsPVwicG9zaXRpb25cIlxuICAgICAgICBpbmFjdGl2ZS12YWx1ZT1cImxlZnRcIlxuICAgICAgICBhY3RpdmUtdmFsdWU9XCJyaWdodFwiXG4gICAgICAgIGluYWN0aXZlLXRleHQ9XCJsZWZ0XCJcbiAgICAgICAgYWN0aXZlLXRleHQ9XCJyaWdodFwiXG4gICAgICAgIHN0eWxlPVwiLS1lbC1zd2l0Y2gtb2ZmLWNvbG9yOiAjODhiOGZlXCJcbiAgICAgIC8+XG4gICAgPC9kaXY+XG5cbiAgICA8ZWwtY29sbGFwc2UgOmV4cGFuZC1pY29uLXBvc2l0aW9uPVwicG9zaXRpb25cIj5cbiAgICAgIDxlbC1jb2xsYXBzZS1pdGVtIHRpdGxlPVwiQ29uc2lzdGVuY3lcIiBuYW1lPVwiMVwiPlxuICAgICAgICA8ZGl2PlxuICAgICAgICAgIENvbnNpc3RlbnQgd2l0aCByZWFsIGxpZmU6IGluIGxpbmUgd2l0aCB0aGUgcHJvY2VzcyBhbmQgbG9naWMgb2YgcmVhbFxuICAgICAgICAgIGxpZmUsIGFuZCBjb21wbHkgd2l0aCBsYW5ndWFnZXMgYW5kIGhhYml0cyB0aGF0IHRoZSB1c2VycyBhcmUgdXNlZCB0bztcbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXY+XG4gICAgICAgICAgQ29uc2lzdGVudCB3aXRoaW4gaW50ZXJmYWNlOiBhbGwgZWxlbWVudHMgc2hvdWxkIGJlIGNvbnNpc3RlbnQsIHN1Y2hcbiAgICAgICAgICBhczogZGVzaWduIHN0eWxlLCBpY29ucyBhbmQgdGV4dHMsIHBvc2l0aW9uIG9mIGVsZW1lbnRzLCBldGMuXG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9lbC1jb2xsYXBzZS1pdGVtPlxuICAgICAgPGVsLWNvbGxhcHNlLWl0ZW0gdGl0bGU9XCJGZWVkYmFja1wiIG5hbWU9XCIyXCI+XG4gICAgICAgIDxkaXY+XG4gICAgICAgICAgT3BlcmF0aW9uIGZlZWRiYWNrOiBlbmFibGUgdGhlIHVzZXJzIHRvIGNsZWFybHkgcGVyY2VpdmUgdGhlaXJcbiAgICAgICAgICBvcGVyYXRpb25zIGJ5IHN0eWxlIHVwZGF0ZXMgYW5kIGludGVyYWN0aXZlIGVmZmVjdHM7XG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2PlxuICAgICAgICAgIFZpc3VhbCBmZWVkYmFjazogcmVmbGVjdCBjdXJyZW50IHN0YXRlIGJ5IHVwZGF0aW5nIG9yIHJlYXJyYW5naW5nXG4gICAgICAgICAgZWxlbWVudHMgb2YgdGhlIHBhZ2UuXG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9lbC1jb2xsYXBzZS1pdGVtPlxuICAgICAgPGVsLWNvbGxhcHNlLWl0ZW0gdGl0bGU9XCJFZmZpY2llbmN5XCIgbmFtZT1cIjNcIj5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBTaW1wbGlmeSB0aGUgcHJvY2Vzczoga2VlcCBvcGVyYXRpbmcgcHJvY2VzcyBzaW1wbGUgYW5kIGludHVpdGl2ZTtcbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXY+XG4gICAgICAgICAgRGVmaW5pdGUgYW5kIGNsZWFyOiBlbnVuY2lhdGUgeW91ciBpbnRlbnRpb25zIGNsZWFybHkgc28gdGhhdCB0aGVcbiAgICAgICAgICB1c2VycyBjYW4gcXVpY2tseSB1bmRlcnN0YW5kIGFuZCBtYWtlIGRlY2lzaW9ucztcbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXY+XG4gICAgICAgICAgRWFzeSB0byBpZGVudGlmeTogdGhlIGludGVyZmFjZSBzaG91bGQgYmUgc3RyYWlnaHRmb3J3YXJkLCB3aGljaCBoZWxwc1xuICAgICAgICAgIHRoZSB1c2VycyB0byBpZGVudGlmeSBhbmQgZnJlZXMgdGhlbSBmcm9tIG1lbW9yaXppbmcgYW5kIHJlY2FsbGluZy5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2VsLWNvbGxhcHNlLWl0ZW0+XG4gICAgPC9lbC1jb2xsYXBzZT5cbiAgPC9kaXY+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IENvbGxhcHNlSWNvblBvc2l0aW9uVHlwZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgcG9zaXRpb24gPSByZWY8Q29sbGFwc2VJY29uUG9zaXRpb25UeXBlPignbGVmdCcpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/collapse/custom-icon-position.vue)_

vue

```
<template>
  <div class="demo-collapse-position">
    <div class="flex items-center mb-4">
      <span class="mr-4">expand icon position: </span>
      <el-switch
        v-model="position"
        inactive-value="left"
        active-value="right"
        inactive-text="left"
        active-text="right"
        style="--el-switch-off-color: #88b8fe"
      />
    </div>

    <el-collapse :expand-icon-position="position">
      <el-collapse-item title="Consistency" name="1">
        <div>
          Consistent with real life: in line with the process and logic of real
          life, and comply with languages and habits that the users are used to;
        </div>
        <div>
          Consistent within interface: all elements should be consistent, such
          as: design style, icons and texts, position of elements, etc.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Feedback" name="2">
        <div>
          Operation feedback: enable the users to clearly perceive their
          operations by style updates and interactive effects;
        </div>
        <div>
          Visual feedback: reflect current state by updating or rearranging
          elements of the page.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Efficiency" name="3">
        <div>
          Simplify the process: keep operating process simple and intuitive;
        </div>
        <div>
          Definite and clear: enunciate your intentions clearly so that the
          users can quickly understand and make decisions;
        </div>
        <div>
          Easy to identify: the interface should be straightforward, which helps
          the users to identify and frees them from memorizing and recalling.
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { CollapseIconPositionType } from 'element-plus'

const position = ref<CollapseIconPositionType>('left')
</script>
```

隐藏源代码

## 阻止折叠 2.9.11 [​](#阻止折叠)

设置 `beforeChange` 属性，若返回 false 或者返回 `Promise` 且被 `reject` ，则停止切换。

before collapse return:

falsetrue

Consistency

Consistent with real life: in line with the process and logic of real life, and comply with languages and habits that the users are used to;

Consistent within interface: all elements should be consistent, such as: design style, icons and texts, position of elements, etc.

Feedback

Operation feedback: enable the users to clearly perceive their operations by style updates and interactive effects;

Visual feedback: reflect current state by updating or rearranging elements of the page.

Efficiency

Simplify the process: keep operating process simple and intuitive;

Definite and clear: enunciate your intentions clearly so that the users can quickly understand and make decisions;

Easy to identify: the interface should be straightforward, which helps the users to identify and frees them from memorizing and recalling.

Controllability

Decision making: giving advices about operations is acceptable, but do not make decisions for the users;

Controlled consequences: users should be granted the freedom to operate, including canceling, aborting or terminating current operation.

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IHYtbG9hZGluZz1cImxvYWRpbmdcIiBjbGFzcz1cImRlbW8tY29sbGFwc2VcIj5cbiAgICA8ZGl2IGNsYXNzPVwiZmxleCBpdGVtcy1jZW50ZXIgbWItNFwiPlxuICAgICAgPHNwYW4gY2xhc3M9XCJtci00XCI+YmVmb3JlIGNvbGxhcHNlIHJldHVybjogPC9zcGFuPlxuICAgICAgPGVsLXN3aXRjaFxuICAgICAgICB2LW1vZGVsPVwiYmVmb3JlXCJcbiAgICAgICAgOmluYWN0aXZlLXZhbHVlPVwiZmFsc2VcIlxuICAgICAgICA6YWN0aXZlLXZhbHVlPVwidHJ1ZVwiXG4gICAgICAgIGluYWN0aXZlLXRleHQ9XCJmYWxzZVwiXG4gICAgICAgIGFjdGl2ZS10ZXh0PVwidHJ1ZVwiXG4gICAgICAvPlxuICAgIDwvZGl2PlxuXG4gICAgPGVsLWNvbGxhcHNlIHYtbW9kZWw9XCJhY3RpdmVOYW1lc1wiIDpiZWZvcmUtY29sbGFwc2U9XCJiZWZvcmVDb2xsYXBzZVwiPlxuICAgICAgPGVsLWNvbGxhcHNlLWl0ZW0gdGl0bGU9XCJDb25zaXN0ZW5jeVwiIG5hbWU9XCIxXCI+XG4gICAgICAgIDxkaXY+XG4gICAgICAgICAgQ29uc2lzdGVudCB3aXRoIHJlYWwgbGlmZTogaW4gbGluZSB3aXRoIHRoZSBwcm9jZXNzIGFuZCBsb2dpYyBvZiByZWFsXG4gICAgICAgICAgbGlmZSwgYW5kIGNvbXBseSB3aXRoIGxhbmd1YWdlcyBhbmQgaGFiaXRzIHRoYXQgdGhlIHVzZXJzIGFyZSB1c2VkIHRvO1xuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBDb25zaXN0ZW50IHdpdGhpbiBpbnRlcmZhY2U6IGFsbCBlbGVtZW50cyBzaG91bGQgYmUgY29uc2lzdGVudCwgc3VjaFxuICAgICAgICAgIGFzOiBkZXNpZ24gc3R5bGUsIGljb25zIGFuZCB0ZXh0cywgcG9zaXRpb24gb2YgZWxlbWVudHMsIGV0Yy5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2VsLWNvbGxhcHNlLWl0ZW0+XG4gICAgICA8ZWwtY29sbGFwc2UtaXRlbSB0aXRsZT1cIkZlZWRiYWNrXCIgbmFtZT1cIjJcIj5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBPcGVyYXRpb24gZmVlZGJhY2s6IGVuYWJsZSB0aGUgdXNlcnMgdG8gY2xlYXJseSBwZXJjZWl2ZSB0aGVpclxuICAgICAgICAgIG9wZXJhdGlvbnMgYnkgc3R5bGUgdXBkYXRlcyBhbmQgaW50ZXJhY3RpdmUgZWZmZWN0cztcbiAgICAgICAgPC9kaXY+XG4gICAgICAgIDxkaXY+XG4gICAgICAgICAgVmlzdWFsIGZlZWRiYWNrOiByZWZsZWN0IGN1cnJlbnQgc3RhdGUgYnkgdXBkYXRpbmcgb3IgcmVhcnJhbmdpbmdcbiAgICAgICAgICBlbGVtZW50cyBvZiB0aGUgcGFnZS5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2VsLWNvbGxhcHNlLWl0ZW0+XG4gICAgICA8ZWwtY29sbGFwc2UtaXRlbSB0aXRsZT1cIkVmZmljaWVuY3lcIiBuYW1lPVwiM1wiPlxuICAgICAgICA8ZGl2PlxuICAgICAgICAgIFNpbXBsaWZ5IHRoZSBwcm9jZXNzOiBrZWVwIG9wZXJhdGluZyBwcm9jZXNzIHNpbXBsZSBhbmQgaW50dWl0aXZlO1xuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBEZWZpbml0ZSBhbmQgY2xlYXI6IGVudW5jaWF0ZSB5b3VyIGludGVudGlvbnMgY2xlYXJseSBzbyB0aGF0IHRoZVxuICAgICAgICAgIHVzZXJzIGNhbiBxdWlja2x5IHVuZGVyc3RhbmQgYW5kIG1ha2UgZGVjaXNpb25zO1xuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBFYXN5IHRvIGlkZW50aWZ5OiB0aGUgaW50ZXJmYWNlIHNob3VsZCBiZSBzdHJhaWdodGZvcndhcmQsIHdoaWNoIGhlbHBzXG4gICAgICAgICAgdGhlIHVzZXJzIHRvIGlkZW50aWZ5IGFuZCBmcmVlcyB0aGVtIGZyb20gbWVtb3JpemluZyBhbmQgcmVjYWxsaW5nLlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZWwtY29sbGFwc2UtaXRlbT5cbiAgICAgIDxlbC1jb2xsYXBzZS1pdGVtIHRpdGxlPVwiQ29udHJvbGxhYmlsaXR5XCIgbmFtZT1cIjRcIj5cbiAgICAgICAgPGRpdj5cbiAgICAgICAgICBEZWNpc2lvbiBtYWtpbmc6IGdpdmluZyBhZHZpY2VzIGFib3V0IG9wZXJhdGlvbnMgaXMgYWNjZXB0YWJsZSwgYnV0IGRvXG4gICAgICAgICAgbm90IG1ha2UgZGVjaXNpb25zIGZvciB0aGUgdXNlcnM7XG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8ZGl2PlxuICAgICAgICAgIENvbnRyb2xsZWQgY29uc2VxdWVuY2VzOiB1c2VycyBzaG91bGQgYmUgZ3JhbnRlZCB0aGUgZnJlZWRvbSB0b1xuICAgICAgICAgIG9wZXJhdGUsIGluY2x1ZGluZyBjYW5jZWxpbmcsIGFib3J0aW5nIG9yIHRlcm1pbmF0aW5nIGN1cnJlbnRcbiAgICAgICAgICBvcGVyYXRpb24uXG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9lbC1jb2xsYXBzZS1pdGVtPlxuICAgIDwvZWwtY29sbGFwc2U+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgYmVmb3JlID0gcmVmKHRydWUpXG5jb25zdCBhY3RpdmVOYW1lcyA9IHJlZihbJzEnXSlcbmNvbnN0IGxvYWRpbmcgPSByZWYoZmFsc2UpXG5cbmNvbnN0IGJlZm9yZUNvbGxhcHNlID0gKCk6IFByb21pc2U8Ym9vbGVhbj4gPT4ge1xuICBsb2FkaW5nLnZhbHVlID0gdHJ1ZVxuICByZXR1cm4gbmV3IFByb21pc2UoKHJlc29sdmUpID0+IHtcbiAgICBzZXRUaW1lb3V0KCgpID0+IHtcbiAgICAgIGxvYWRpbmcudmFsdWUgPSBmYWxzZVxuICAgICAgcmV0dXJuIHJlc29sdmUoYmVmb3JlLnZhbHVlKVxuICAgIH0sIDEwMDApXG4gIH0pXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/collapse/prevent-collapsing.vue)_

vue

```
<template>
  <div v-loading="loading" class="demo-collapse">
    <div class="flex items-center mb-4">
      <span class="mr-4">before collapse return: </span>
      <el-switch
        v-model="before"
        :inactive-value="false"
        :active-value="true"
        inactive-text="false"
        active-text="true"
      />
    </div>

    <el-collapse v-model="activeNames" :before-collapse="beforeCollapse">
      <el-collapse-item title="Consistency" name="1">
        <div>
          Consistent with real life: in line with the process and logic of real
          life, and comply with languages and habits that the users are used to;
        </div>
        <div>
          Consistent within interface: all elements should be consistent, such
          as: design style, icons and texts, position of elements, etc.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Feedback" name="2">
        <div>
          Operation feedback: enable the users to clearly perceive their
          operations by style updates and interactive effects;
        </div>
        <div>
          Visual feedback: reflect current state by updating or rearranging
          elements of the page.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Efficiency" name="3">
        <div>
          Simplify the process: keep operating process simple and intuitive;
        </div>
        <div>
          Definite and clear: enunciate your intentions clearly so that the
          users can quickly understand and make decisions;
        </div>
        <div>
          Easy to identify: the interface should be straightforward, which helps
          the users to identify and frees them from memorizing and recalling.
        </div>
      </el-collapse-item>
      <el-collapse-item title="Controllability" name="4">
        <div>
          Decision making: giving advices about operations is acceptable, but do
          not make decisions for the users;
        </div>
        <div>
          Controlled consequences: users should be granted the freedom to
          operate, including canceling, aborting or terminating current
          operation.
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const before = ref(true)
const activeNames = ref(['1'])
const loading = ref(false)

const beforeCollapse = (): Promise<boolean> => {
  loading.value = true
  return new Promise((resolve) => {
    setTimeout(() => {
      loading.value = false
      return resolve(before.value)
    }, 1000)
  })
}
</script>
```

隐藏源代码

## Collapse API [​](#collapse-api)

### Collapse Attributes [​](#collapse-attributes)

| 属性名 | 详情 | 类型 | 默认值 |
| --- | --- | --- | --- |
| model-value / v-model | 当前活动面板，在手风琴模式下其类型是`string`，在其他模式下是`array` | `string` / `array` | \[\] |
| accordion | 是否手风琴模式 | `boolean` | false |
| expand-icon-position 2.9.10 | 设置展开图标位置 | `enum` | right |
| before-collapse 2.9.11 | 折叠状态更改之前的折叠钩子。 返回 `false` 或者返回 `Promise` 且被 reject 则停止切换 | `Function` | — |

### Collapse Events [​](#collapse-events)

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| change | 切换当前活动面板，在手风琴模式下其类型是`string`，在其他模式下是`array` | `Function` |

### Collapse Slots [​](#collapse-slots)

| 插槽名 | Description | 子标签 |
| --- | --- | --- |
| default | 自定义默认内容 | Collapse Item |

### Collapse Exposes [​](#collapse-exposes)

| 方法名 | 说明 | 类型 |
| --- | --- | --- |
| activeNames | 当前活动的面板名称 | `object` |
| setActiveNames | 设置活动面板名称 | `Function` |

## Collapse Item API [​](#collapse-item-api)

### Collapse Item Attributes [​](#collapse-item-attributes)

| 属性名 | 说明 | Type | 默认值 |
| --- | --- | --- | --- |
| name | 唯一标志符 | `string` / `number` | — |
| title | 面板标题 | `string` | '' |
| icon 2.8.3 | 折叠项目的图标 | `string` / `Component` | ArrowRight |
| disabled | 是否禁用 | `boolean` | false |

### Collapse Item Slot [​](#collapse-item-slot)

| Name | Description | Type |
| --- | --- | --- |
| default | Collapse Item 的内容 | — |
| title | Collapse Item 的标题 | `object` |
| icon 2.8.3 | 折叠项目图标的内容 | `object` |

### Collapse Item Exposes [​](#collapse-item-exposes)

| Name | Description | Type |
| --- | --- | --- |
| isActive | 当前折叠项是否激活 | `object` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/collapse) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/collapse.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/collapse.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/57785259?v=4&size=64)](https://github.com/w2xi)[![](https://avatars.githubusercontent.com/u/108655466?v=4&size=64)](https://github.com/Karolis-Stoncius)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/154399795?v=4&size=64)](https://github.com/rhodi2436)[![](https://avatars.githubusercontent.com/u/43257608?v=4&size=64)](https://github.com/Liao-js)[![](https://avatars.githubusercontent.com/u/121680374?v=4&size=64)](https://github.com/kaine0923)[![](https://avatars.githubusercontent.com/u/32761502?v=4&size=64)](https://github.com/kimverchan)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/103868381?v=4&size=64)](https://github.com/kinggq)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)

[Carousel 走马灯](https://element-plus.org/zh-CN/component/carousel)

[Descriptions 描述列表](https://element-plus.org/zh-CN/component/descriptions)


