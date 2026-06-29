---
name: "calendar"
description: "Calendar 日历 -- Element UI Vue2 桌面端组件。Invoke when user needs Calendar 日历 in Vue 2.x project."
url: "https://element.eleme.cn/#/zh-CN/component/calendar"
---

---

## [¶](https://element.eleme.cn/#/zh-CN/component/calendar#calendar-ri-li) Calendar 日历

显示日期

### [¶](https://element.eleme.cn/#/zh-CN/component/calendar#ji-ben) 基本

2026 年 6 月

上个月 今天 下个月

| 一 | 二 | 三 | 四 | 五 | 六 | 日 |
| --- | --- | --- | --- | --- | --- | --- |
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

7

 |
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

14

 |
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

21

 |
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

28

 |
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

5

 |
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

12

 |

设置 `value` 来指定当前显示的月份。如果 `value` 未指定，则显示当月。`value` 支持 `v-model` 双向绑定。

```
<el-calendar v-model="value">
</el-calendar>

<script>
  export default {
    data() {
      return {
        value: new Date()
      }
    }
  }
</script>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/calendar#zi-ding-yi-nei-rong) 自定义内容

2026 年 6 月

上个月 今天 下个月

| 一 | 二 | 三 | 四 | 五 | 六 | 日 |
| --- | --- | --- | --- | --- | --- | --- |
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

06-07

 |
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

06-14

 |
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

06-21

 |
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

06-28

 |
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

07-05

 |
|

07-06

 |

07-07

 |

07-08

 |

07-09

 |

07-10

 |

07-11

 |

07-12

 |

通过设置名为 `dateCell` 的 `scoped-slot` 来自定义日历单元格中显示的内容。在 `scoped-slot` 可以获取到 date（当前单元格的日期）, data（包括 type，isSelected，day 属性）。详情解释参考下方的 API 文档。

```
<el-calendar>
  <!-- 这里使用的是 2.5 slot 语法，对于新项目请使用 2.6 slot 语法-->
  <template
    slot="dateCell"
    slot-scope="{date, data}">
    <p :class="data.isSelected ? 'is-selected' : ''">
      {{ data.day.split('-').slice(1).join('-') }} {{ data.isSelected ? '✔️' : ''}}
    </p>
  </template>
</el-calendar>
<style>
  .is-selected {
    color: #1989FA;
  }
</style>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/calendar#zi-ding-yi-fan-wei) 自定义范围

2019 年 3 月

| 一 | 二 | 三 | 四 | 五 | 六 | 日 |
| --- | --- | --- | --- | --- | --- | --- |
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

10

 |
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

17

 |
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

24

 |

设置 `range` 属性指定日历的显示范围。开始时间必须是周起始日，结束时间必须是周结束日，且时间跨度不能超过两个月。

```
<el-calendar :range="['2019-03-04', '2019-03-24']">
</el-calendar>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/calendar#attributes) Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| value / v-model | 绑定值 | Date/string/number | — | — |
| range | 时间范围，包括开始时间与结束时间。开始时间必须是周一，结束时间必须是周日，且时间跨度不能超过两个月。 | Array | — | — |
| first-day-of-week | 周起始日 | Number | 1 到 7 | 1 |

### [¶](https://element.eleme.cn/#/zh-CN/component/calendar#datecell-scoped-slot-can-shu) dateCell scoped slot 参数

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| date | 单元格代表的日期 | Date | — | — |
| data | { type, isSelected, day}，`type` 表示该日期的所属月份，可选值有 prev-month，current-month，next-month；`isSelected` 标明该日期是否被选中；`day` 是格式化的日期，格式为 yyyy-MM-dd | Object | — | — |

Divider 分割线 Image 图片


