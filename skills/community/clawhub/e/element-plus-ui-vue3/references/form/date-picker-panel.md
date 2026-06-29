---
name: "date-picker-panel"
description: "DatePickerPanel 日期选择器面板 -- Element Plus Vue3 桌面端组件。Invoke when user needs DatePickerPanel 日期选择器面板 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/date-picker-panel.html"
---

---

# DatePickerPane 日期选择器面板 beta [​](#datepickerpane-日期选择器面板)

更新日志待解决

2

`DatePickerPanel`是`DatePicker`的核心组件。

## 选择某一天 [​](#选择某一天)

以”日“为基本单位，基础的日期选择控件

2026 June

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

10

 |

11

 |

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBqdXN0aWZ5LWNlbnRlclwiPlxuICAgIDxlbC1kYXRlLXBpY2tlci1wYW5lbCB2LW1vZGVsPVwidmFsdWVcIiAvPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKClcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/date-picker-panel/basic.vue)_

vue

```
<template>
  <div class="flex justify-center">
    <el-date-picker-panel v-model="value" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref()
</script>
```

隐藏源代码

## 边框 [​](#边框)

默认情况下，边框是默认的，如果你不想要边框请参考示例。 例如，`DatePicker`不继承`border`。

No border:

2026 June

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

10

 |

11

 |

2026 June

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

10

 |

11

 |

TS

JS

_[](https://element-plus.run/?extra_packages=%40vueuse%2Fcore#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2XG4gICAgcmVmPVwiY29udGFpbmVyUmVmXCJcbiAgICA6Y2xhc3M9XCJbJ2RhdGUtcGlja2VyLS1leGFtcGxlJywgeyAnaXMtbmFycm93JzogaXNOYXJyb3cgfV1cIlxuICA+XG4gICAgPGRpdiBjbGFzcz1cInRleHQtY2VudGVyXCI+Tm8gYm9yZGVyOjwvZGl2PlxuICAgIDxlbC1kaXZpZGVyIC8+XG4gICAgPGRpdiBjbGFzcz1cImRhdGUtcGlja2VyLS1mbGV4LWNvbnRhaW5lclwiPlxuICAgICAgPGRpdiBjbGFzcz1cInAtWzIwcHhdXCI+XG4gICAgICAgIDxlbC1kYXRlLXBpY2tlci1wYW5lbCB2LW1vZGVsPVwidmFsdWVcIiA6Ym9yZGVyPVwiZmFsc2VcIiAvPlxuICAgICAgPC9kaXY+XG4gICAgICA8ZWwtZGl2aWRlclxuICAgICAgICBjbGFzcz1cImRpdmlkZXJcIlxuICAgICAgICA6ZGlyZWN0aW9uPVwiaXNOYXJyb3cgPyAnaG9yaXpvbnRhbCcgOiAndmVydGljYWwnXCJcbiAgICAgIC8+XG4gICAgICA8ZWwtY2FyZD5cbiAgICAgICAgPGVsLWRhdGUtcGlja2VyLXBhbmVsIHYtbW9kZWw9XCJ2YWx1ZVwiIDpib3JkZXI9XCJmYWxzZVwiIC8+XG4gICAgICA8L2VsLWNhcmQ+XG4gICAgPC9kaXY+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IGNvbXB1dGVkLCByZWYgfSBmcm9tICd2dWUnXG5pbXBvcnQgeyB1c2VFbGVtZW50U2l6ZSB9IGZyb20gJ0B2dWV1c2UvY29yZSdcblxuY29uc3QgdmFsdWUgPSByZWYoKVxuY29uc3QgY29udGFpbmVyUmVmID0gcmVmPEhUTUxFbGVtZW50PigpXG5cbmNvbnN0IHsgd2lkdGggfSA9IHVzZUVsZW1lbnRTaXplKGNvbnRhaW5lclJlZilcblxuY29uc3QgaXNOYXJyb3cgPSBjb21wdXRlZCgoKSA9PiB3aWR0aC52YWx1ZSA8IDgxNSlcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmRhdGUtcGlja2VyLS1mbGV4LWNvbnRhaW5lciB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGZsZXgtd3JhcDogd3JhcDtcbiAgZ2FwOiAxNnB4O1xuICBqdXN0aWZ5LWNvbnRlbnQ6IGNlbnRlcjtcbn1cbi5kaXZpZGVyIHtcbiAgaGVpZ2h0OiBhdXRvO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/date-picker-panel/border.vue)_

vue

```
<template>
  <div
    ref="containerRef"
    :class="['date-picker--example', { 'is-narrow': isNarrow }]"
  >
    <div class="text-center">No border:</div>
    <el-divider />
    <div class="date-picker--flex-container">
      <div class="p-[20px]">
        <el-date-picker-panel v-model="value" :border="false" />
      </div>
      <el-divider
        class="divider"
        :direction="isNarrow ? 'horizontal' : 'vertical'"
      />
      <el-card>
        <el-date-picker-panel v-model="value" :border="false" />
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue'
import { useElementSize } from '@vueuse/core'

const value = ref()
const containerRef = ref<HTMLElement>()

const { width } = useElementSize(containerRef)

const isNarrow = computed(() => width.value < 815)
</script>

<style scoped>
.date-picker--flex-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
}
.divider {
  height: auto;
}
</style>
```

隐藏源代码

## 禁用 [​](#禁用)

"禁用"属性决定日期选择器是否完全禁用。

EnabledDisabled

2026 June

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

10

 |

11

 |

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LWNvbCBpdGVtcy1jZW50ZXJcIj5cbiAgICA8ZWwtc3dpdGNoXG4gICAgICB2LW1vZGVsPVwiZGlzYWJsZWRcIlxuICAgICAgYWN0aXZlLXRleHQ9XCJEaXNhYmxlZFwiXG4gICAgICBpbmFjdGl2ZS10ZXh0PVwiRW5hYmxlZFwiXG4gICAgLz5cbiAgICA8ZWwtZGF0ZS1waWNrZXItcGFuZWwgdi1tb2RlbD1cInZhbHVlXCIgOmRpc2FibGVkPVwiZGlzYWJsZWRcIiAvPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKClcbmNvbnN0IGRpc2FibGVkID0gcmVmKHRydWUpXG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/date-picker-panel/disabled.vue)_

vue

```
<template>
  <div class="flex flex-col items-center">
    <el-switch
      v-model="disabled"
      active-text="Disabled"
      inactive-text="Enabled"
    />
    <el-date-picker-panel v-model="value" :disabled="disabled" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref()
const disabled = ref(true)
</script>
```

隐藏源代码

## 展示类型 [​](#展示类型)

时间面板的类型由 `type` 属性指定。

Type:

date

2026 June

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

10

 |

11

 |

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZGl2PlxuICAgIDxkaXYgY2xhc3M9XCJmbGV4IGdhcC00XCI+XG4gICAgICA8ZGl2IGNsYXNzPVwiZmxleCBmbGV4LWNvbCBiYXNpcy0xNTBweCBnYXAtMVwiPlxuICAgICAgICA8c3Bhbj5UeXBlOjwvc3Bhbj5cbiAgICAgICAgPGVsLXNlbGVjdCB2LW1vZGVsPVwidHlwZVwiPlxuICAgICAgICAgIDxlbC1vcHRpb25cbiAgICAgICAgICAgIHYtZm9yPVwib3B0aW9uVHlwZSBpbiB0eXBlc1wiXG4gICAgICAgICAgICA6a2V5PVwib3B0aW9uVHlwZVwiXG4gICAgICAgICAgICA6dmFsdWU9XCJvcHRpb25UeXBlXCJcbiAgICAgICAgICAvPlxuICAgICAgICA8L2VsLXNlbGVjdD5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PlxuICAgIDxlbC1kaXZpZGVyIC8+XG4gICAgPGRpdiBjbGFzcz1cImZsZXgganVzdGlmeS1jZW50ZXJcIj5cbiAgICAgIDxlbC1kYXRlLXBpY2tlci1wYW5lbCB2LW1vZGVsPVwiZGF0ZVwiIDp0eXBlPVwidHlwZVwiIC8+XG4gICAgPC9kaXY+XG4gIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiwgd2F0Y2ggfSBmcm9tICd2dWUnXG5cbmltcG9ydCB0eXBlIHsgRGF0ZVBpY2tlclR5cGUgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IGRhdGUgPSByZWYoKVxuY29uc3QgdHlwZSA9IHJlZjxEYXRlUGlja2VyVHlwZT4oJ2RhdGUnKVxuXG53YXRjaCh0eXBlLCAoKSA9PiB7XG4gIGRhdGUudmFsdWUgPSB1bmRlZmluZWRcbn0pXG5cbmNvbnN0IHR5cGVzOiBEYXRlUGlja2VyVHlwZVtdID0gW1xuICAneWVhcicsXG4gICd5ZWFycycsXG4gICdtb250aCcsXG4gICdtb250aHMnLFxuICAnZGF0ZScsXG4gICdkYXRlcycsXG4gICd3ZWVrJyxcbiAgJ2RhdGV0aW1lJyxcbiAgJ2RhdGV0aW1lcmFuZ2UnLFxuICAnZGF0ZXJhbmdlJyxcbiAgJ21vbnRocmFuZ2UnLFxuICAneWVhcnJhbmdlJyxcbl1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/date-picker-panel/all-types.vue)_

vue

```
<template>
  <div>
    <div class="flex gap-4">
      <div class="flex flex-col basis-150px gap-1">
        <span>Type:</span>
        <el-select v-model="type">
          <el-option
            v-for="optionType in types"
            :key="optionType"
            :value="optionType"
          />
        </el-select>
      </div>
    </div>
    <el-divider />
    <div class="flex justify-center">
      <el-date-picker-panel v-model="date" :type="type" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'

import type { DatePickerType } from 'element-plus'

const date = ref()
const type = ref<DatePickerType>('date')

watch(type, () => {
  date.value = undefined
})

const types: DatePickerType[] = [
  'year',
  'years',
  'month',
  'months',
  'date',
  'dates',
  'week',
  'datetime',
  'datetimerange',
  'daterange',
  'monthrange',
  'yearrange',
]
</script>
```

隐藏源代码

## 本地化 [​](#本地化)

由于 Element Plus 的默认语言为英语，如果你需要设置其它的语言，请参考[国际化](https://element-plus.org/zh-CN/guide/i18n)文档。

要注意的是：日期相关的文字（月份，每一周的第一天等等） 也都进行了本地化配置。

## 应用开发接口（API） [​](#应用开发接口-api)

### 属性 [​](#属性)

| 属性名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| model-value / v-model | 绑定值，如果是 `range` 选择器，数组长度应为 2 | `number` / `string` / `Date` / `array` | '' |
| border | 日期选择器是否有边框 | `boolean` | true |
| disabled | 禁用 | `boolean` | false |
| clearable | 是否显示清除按钮 | `boolean` | true |
| editable 2.13.0 | 文本框可输入 | `boolean` | true |
| type | 选择器类型，默认是普通选择器 | `enum` | date |
| default-value | 可选，选择器打开时默认显示的时间 | `object` | — |
| default-time | 范围选择时选中日期所使用的当日内具体时刻 | `object` | — |
| value-format | 可选，绑定值的格式。 不指定则绑定值为 Date 对象 | `string` | — |
| date-format | 可选，输入框内部面板中显示的日期格式 | `string` see [date formats](https://day.js.org/docs/en/display/format) | YYYY-MM-DD |
| time-format | 可选，输入框内部面板中显示的时间格式 | `string` see [date formats](https://day.js.org/docs/en/display/format) | HH:mm:ss |
| unlink-panels | 在范围选择器里取消两个日期面板之间的联动 | `boolean` | false |
| single-panel 2.14.0 | 在范围选择器中只显示一个面板 | `boolean` | false |
| disabled-date | 一个用来判断该日期是否被禁用的函数，接受一个 Date 对象作为参数。 应该返回一个 Boolean 值。 | `Function` | — |
| shortcuts | 设置快捷选项，需要传入数组对象 | `array` | \[\] |
| cell-class-name | 设置自定义类名 | `Function` | — |
| show-footer | 是否在日期选择器中显示页脚 `enum` | `boolean` | false |
| show-confirm | 是否显示确定按钮 | `boolean` | false |
| show-week-number | 显示周数(除周外) | `boolean` | false |

### Events [​](#events)

| 名称 | 详情 | 类型 |
| --- | --- | --- |
| calendar-change | 在日历所选日期更改时触发 仅限“range”类型。 | `Function` |
| panel-change | 当日期面板改变时触发。 | `Function` |
| clear 2.13.1 | 当点击清除按钮时触发 | `Function` |

### 插槽 [​](#插槽)

| 名称 | 详情 |
| --- | --- |
| default | 自定义单元格内容 |
| prev-month | 上个月的图标 |
| next-month | 下个月的图标 |
| prev-year | 上一年图标 |
| next-year | 下一年图标 |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/date-picker-panel) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/date-picker-panel.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/date-picker-panel.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/61937205?v=4&size=64)](https://github.com/keeplearning66)[![](https://avatars.githubusercontent.com/u/24487727?v=4&size=64)](https://github.com/LostElkByte)[![](https://avatars.githubusercontent.com/u/56141625?v=4&size=64)](https://github.com/micaiguai)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/7835220?v=4&size=64)](https://github.com/tjyuanpeng)[![](https://avatars.githubusercontent.com/u/70922464?v=4&size=64)](https://github.com/shanecranor)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/128720752?v=4&size=64)](https://github.com/cjn021)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/110156942?v=4&size=64)](https://github.com/a92126)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)

[Color Picker 颜色选择器](https://element-plus.org/zh-CN/component/color-picker)

[Date Picker 日期选择器](https://element-plus.org/zh-CN/component/date-picker)


