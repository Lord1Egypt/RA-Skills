---
name: "calendar"
description: "Calendar 日历 -- Element Plus Vue3 桌面端组件。Invoke when user needs Calendar 日历 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/calendar.html"
---

---

# Calendar 日历 [​](#calendar-日历)

更新日志待解决

2

显示日期

## 基础用法 [​](#基础用法)

设置 `value` 来指定当前显示的月份。 如果 `value` 未指定，则显示当月。 `value` 支持 `v-model` 双向绑定。

2026 June

Previous MonthTodayNext Month

| Sun | Mon | Tue | Wed | Thu | Fri | Sat |
| --- | --- | --- | --- | --- | --- | --- |
|
31

 |

1

 |

2

 |

3

 |

4

 |

5

 |

6

 |
|

7

 |

8

 |

9

 |

10

 |

11

 |

12

 |

13

 |
|

14

 |

15

 |

16

 |

17

 |

18

 |

19

 |

20

 |
|

21

 |

22

 |

23

 |

24

 |

25

 |

26

 |

27

 |
|

28

 |

29

 |

30

 |

1

 |

2

 |

3

 |

4

 |

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2FsZW5kYXIgdi1tb2RlbD1cInZhbHVlXCIgLz5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKG5ldyBEYXRlKCkpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/calendar/basic.vue)_

vue

```
<template>
  <el-calendar v-model="value" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref(new Date())
</script>
```

隐藏源代码

## 控制器类型 2.13.1 [​](#控制器类型)

您可以设置日历头部的控制器类型。 设置 `select`时，您可以使用 `formatter` 自定义 `label`。

selectbutton

2026 June

2026

6

Today

| Sun | Mon | Tue | Wed | Thu | Fri | Sat |
| --- | --- | --- | --- | --- | --- | --- |
|
31

 |

1

 |

2

 |

3

 |

4

 |

5

 |

6

 |
|

7

 |

8

 |

9

 |

10

 |

11

 |

12

 |

13

 |
|

14

 |

15

 |

16

 |

17

 |

18

 |

19

 |

20

 |
|

21

 |

22

 |

23

 |

24

 |

25

 |

26

 |

27

 |
|

28

 |

29

 |

30

 |

1

 |

2

 |

3

 |

4

 |

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcmFkaW8tZ3JvdXAgdi1tb2RlbD1cImNvbnRyb2xsZXJUeXBlXCI+XG4gICAgPGVsLXJhZGlvLWJ1dHRvbiBsYWJlbD1cInNlbGVjdFwiIHZhbHVlPVwic2VsZWN0XCIgLz5cbiAgICA8ZWwtcmFkaW8tYnV0dG9uIGxhYmVsPVwiYnV0dG9uXCIgdmFsdWU9XCJidXR0b25cIiAvPlxuICA8L2VsLXJhZGlvLWdyb3VwPlxuXG4gIDxlbC1jYWxlbmRhciB2LW1vZGVsPVwidmFsdWVcIiA6Y29udHJvbGxlci10eXBlPVwiY29udHJvbGxlclR5cGVcIiAvPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcblxuY29uc3QgY29udHJvbGxlclR5cGUgPSByZWY8J3NlbGVjdCcgfCAnYnV0dG9uJz4oJ3NlbGVjdCcpXG5jb25zdCB2YWx1ZSA9IHJlZihuZXcgRGF0ZSgpKVxuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/calendar/controller-type.vue)_

vue

```
<template>
  <el-radio-group v-model="controllerType">
    <el-radio-button label="select" value="select" />
    <el-radio-button label="button" value="button" />
  </el-radio-group>

  <el-calendar v-model="value" :controller-type="controllerType" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const controllerType = ref<'select' | 'button'>('select')
const value = ref(new Date())
</script>
```

隐藏源代码

## 自定义内容 [​](#自定义内容)

通过设置名为 `date-cell` 的 `scoped-slot` 来自定义日历单元格中显示的内容。 在 `scoped-slot` 可以获取到 date（当前单元格的日期）, data（包括 type，isSelected，day 属性）。 详情解释参考下方的 API 文档。

2026 June

Previous MonthTodayNext Month

| Sun | Mon | Tue | Wed | Thu | Fri | Sat |
| --- | --- | --- | --- | --- | --- | --- |
|
05-31

 |

06-01

 |

06-02

 |

06-03

 |

06-04

 |

06-05

 |

06-06

 |
|

06-07

 |

06-08

 |

06-09

 |

06-10

 |

06-11

 |

06-12

 |

06-13

 |
|

06-14

 |

06-15

 |

06-16

 |

06-17

 |

06-18

 |

06-19

 |

06-20

 |
|

06-21

 |

06-22

 |

06-23

 |

06-24

 |

06-25

 |

06-26

 |

06-27

 |
|

06-28

 |

06-29

 |

06-30

 |

07-01

 |

07-02

 |

07-03

 |

07-04

 |

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2FsZW5kYXI+XG4gICAgPHRlbXBsYXRlICNkYXRlLWNlbGw9XCJ7IGRhdGEgfVwiPlxuICAgICAgPHAgOmNsYXNzPVwiZGF0YS5pc1NlbGVjdGVkID8gJ2lzLXNlbGVjdGVkJyA6ICcnXCI+XG4gICAgICAgIHt7IGRhdGEuZGF5LnNwbGl0KCctJykuc2xpY2UoMSkuam9pbignLScpIH19XG4gICAgICAgIHt7IGRhdGEuaXNTZWxlY3RlZCA/ICfinJTvuI8nIDogJycgfX1cbiAgICAgIDwvcD5cbiAgICA8L3RlbXBsYXRlPlxuICA8L2VsLWNhbGVuZGFyPlxuPC90ZW1wbGF0ZT5cblxuPHN0eWxlPlxuLmlzLXNlbGVjdGVkIHtcbiAgY29sb3I6ICMxOTg5ZmE7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/calendar/customize.vue)_

vue

```
<template>
  <el-calendar>
    <template #date-cell="{ data }">
      <p :class="data.isSelected ? 'is-selected' : ''">
        {{ data.day.split('-').slice(1).join('-') }}
        {{ data.isSelected ? '✔️' : '' }}
      </p>
    </template>
  </el-calendar>
</template>

<style>
.is-selected {
  color: #1989fa;
}
</style>
```

隐藏源代码

## 范围 [​](#范围)

设置 `range` 属性指定日历的显示范围。 开始时间必须是周起始日，结束时间必须是周结束日，且时间跨度不能超过两个月。

2019 March

| Sun | Mon | Tue | Wed | Thu | Fri | Sat |
| --- | --- | --- | --- | --- | --- | --- |
|
3

 |

4

 |

5

 |

6

 |

7

 |

8

 |

9

 |
|

10

 |

11

 |

12

 |

13

 |

14

 |

15

 |

16

 |
|

17

 |

18

 |

19

 |

20

 |

21

 |

22

 |

23

 |
|

24

 |

25

 |

26

 |

27

 |

28

 |

29

 |

30

 |

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2FsZW5kYXIgOnJhbmdlPVwiW25ldyBEYXRlKDIwMTksIDIsIDQpLCBuZXcgRGF0ZSgyMDE5LCAyLCAyNCldXCIgLz5cbjwvdGVtcGxhdGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/calendar/range.vue)_

vue

```
<template>
  <el-calendar :range="[new Date(2019, 2, 4), new Date(2019, 2, 24)]" />
</template>
```

隐藏源代码

## 自定义日历头部 [​](#自定义日历头部)

Custom header content2026 June

Previous Year Previous Month Today Next Month Next Year

| Sun | Mon | Tue | Wed | Thu | Fri | Sat |
| --- | --- | --- | --- | --- | --- | --- |
|
31

 |

1

 |

2

 |

3

 |

4

 |

5

 |

6

 |
|

7

 |

8

 |

9

 |

10

 |

11

 |

12

 |

13

 |
|

14

 |

15

 |

16

 |

17

 |

18

 |

19

 |

20

 |
|

21

 |

22

 |

23

 |

24

 |

25

 |

26

 |

27

 |
|

28

 |

29

 |

30

 |

1

 |

2

 |

3

 |

4

 |

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtY2FsZW5kYXIgcmVmPVwiY2FsZW5kYXJcIj5cbiAgICA8dGVtcGxhdGUgI2hlYWRlcj1cInsgZGF0ZSB9XCI+XG4gICAgICA8c3Bhbj5DdXN0b20gaGVhZGVyIGNvbnRlbnQ8L3NwYW4+XG4gICAgICA8c3Bhbj57eyBkYXRlIH19PC9zcGFuPlxuICAgICAgPGVsLWJ1dHRvbi1ncm91cD5cbiAgICAgICAgPGVsLWJ1dHRvbiBzaXplPVwic21hbGxcIiBAY2xpY2s9XCJzZWxlY3REYXRlKCdwcmV2LXllYXInKVwiPlxuICAgICAgICAgIFByZXZpb3VzIFllYXJcbiAgICAgICAgPC9lbC1idXR0b24+XG4gICAgICAgIDxlbC1idXR0b24gc2l6ZT1cInNtYWxsXCIgQGNsaWNrPVwic2VsZWN0RGF0ZSgncHJldi1tb250aCcpXCI+XG4gICAgICAgICAgUHJldmlvdXMgTW9udGhcbiAgICAgICAgPC9lbC1idXR0b24+XG4gICAgICAgIDxlbC1idXR0b24gc2l6ZT1cInNtYWxsXCIgQGNsaWNrPVwic2VsZWN0RGF0ZSgndG9kYXknKVwiPlRvZGF5PC9lbC1idXR0b24+XG4gICAgICAgIDxlbC1idXR0b24gc2l6ZT1cInNtYWxsXCIgQGNsaWNrPVwic2VsZWN0RGF0ZSgnbmV4dC1tb250aCcpXCI+XG4gICAgICAgICAgTmV4dCBNb250aFxuICAgICAgICA8L2VsLWJ1dHRvbj5cbiAgICAgICAgPGVsLWJ1dHRvbiBzaXplPVwic21hbGxcIiBAY2xpY2s9XCJzZWxlY3REYXRlKCduZXh0LXllYXInKVwiPlxuICAgICAgICAgIE5leHQgWWVhclxuICAgICAgICA8L2VsLWJ1dHRvbj5cbiAgICAgIDwvZWwtYnV0dG9uLWdyb3VwPlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtY2FsZW5kYXI+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IENhbGVuZGFyRGF0ZVR5cGUsIENhbGVuZGFySW5zdGFuY2UgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IGNhbGVuZGFyID0gcmVmPENhbGVuZGFySW5zdGFuY2U+KClcbmNvbnN0IHNlbGVjdERhdGUgPSAodmFsOiBDYWxlbmRhckRhdGVUeXBlKSA9PiB7XG4gIGlmICghY2FsZW5kYXIudmFsdWUpIHJldHVyblxuICBjYWxlbmRhci52YWx1ZS5zZWxlY3REYXRlKHZhbClcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/calendar/header.vue)_

vue

```
<template>
  <el-calendar ref="calendar">
    <template #header="{ date }">
      <span>Custom header content</span>
      <span>{{ date }}</span>
      <el-button-group>
        <el-button size="small" @click="selectDate('prev-year')">
          Previous Year
        </el-button>
        <el-button size="small" @click="selectDate('prev-month')">
          Previous Month
        </el-button>
        <el-button size="small" @click="selectDate('today')">Today</el-button>
        <el-button size="small" @click="selectDate('next-month')">
          Next Month
        </el-button>
        <el-button size="small" @click="selectDate('next-year')">
          Next Year
        </el-button>
      </el-button-group>
    </template>
  </el-calendar>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { CalendarDateType, CalendarInstance } from 'element-plus'

const calendar = ref<CalendarInstance>()
const selectDate = (val: CalendarDateType) => {
  if (!calendar.value) return
  calendar.value.selectDate(val)
}
</script>
```

隐藏源代码

## 国际化 [​](#国际化)

由于 Element Plus 的默认语言为英语，如果你需要设置其它的语言，请参考[国际化](https://element-plus.org/zh-CN/guide/i18n)文档。

要注意的是：日期相关的文字（月份，每一周的第一天等等）也都是通过国际化来配置的。

## API [​](#api)

### Attributes [​](#attributes)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| model-value / v-model | 选中项绑定值 | `Date` | — |
| range | 时间范围，包括开始时间与结束时间。 开始时间必须是周起始日，结束时间必须是周结束日，且时间跨度不能超过两个月。 | `array` | — |
| controller-type 2.13.1 | 日历头部的控制器类型 | `enum` | button |
| formatter 2.13.1 | 当 `controller-type` 为“select”时的格式标签 | `Function` | — |

### Slots [​](#slots)

| 插槽名 | 说明 | 类型 |
| --- | --- | --- |
| date-cell | `type` 表示该日期的所属月份，可选值有 prev-month、current-month 和 next-month；`isSelected` 标明该日期是否被选中；`day` 是格式化的日期，格式为 `yyyy-MM-dd`；`date` 是单元格的日期 | `object` |
| header | 卡片标题内容 | `object` |

### Exposes [​](#exposes)

| 名称 | 说明 | 类型 |
| --- | --- | --- |
| selectedDay | 当前已选日期 | `object` |
| pickDay | 选择一个具体日期 | `Function` |
| selectDate | 选择日期 | `Function` |
| calculateValidatedDateRange | 根据开始与结束日期计算验证日期范围 | `Function` |

## 类型声明 [​](#类型声明)

显示类型声明

ts

```
type CalendarDateType =
  | 'prev-month'
  | 'next-month'
  | 'prev-year'
  | 'next-year'
  | 'today'
```

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/calendar) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/calendar.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/calendar.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/33687038?v=4&size=64)](https://github.com/guozi9999)[![](https://avatars.githubusercontent.com/u/56141625?v=4&size=64)](https://github.com/micaiguai)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/140705167?v=4&size=64)](https://github.com/zhongli-kira)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/35426360?v=4&size=64)](https://github.com/Jungzl)[![](https://avatars.githubusercontent.com/u/38392315?v=4&size=64)](https://github.com/kooriookami)[![](https://avatars.githubusercontent.com/u/31850793?v=4&size=64)](https://github.com/ModyQyW)[![](https://avatars.githubusercontent.com/u/16495064?v=4&size=64)](https://github.com/sunyuu)[![](https://avatars.githubusercontent.com/u/50739490?v=4&size=64)](https://github.com/Chuck-Lau)[![](https://avatars.githubusercontent.com/u/59350883?v=4&size=64)](https://github.com/init-qy)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/23378455?v=4&size=64)](https://github.com/Dreamcreative)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/11409069?v=4&size=64)](https://github.com/freedomlang)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/2883231?v=4&size=64)](https://github.com/HerringtonDarkholme)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/10731096?v=4&size=64)](https://github.com/zazzaz)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)[![](https://avatars.githubusercontent.com/u/38106851?v=4&size=64)](https://github.com/LAMMUpro)

[Badge 徽章](https://element-plus.org/zh-CN/component/badge)

[Card 卡片](https://element-plus.org/zh-CN/component/card)


