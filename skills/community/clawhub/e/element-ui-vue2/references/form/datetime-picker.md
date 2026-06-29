---
name: "datetime-picker"
description: "DateTimePicker 日期时间选择器 -- Element UI Vue2 桌面端组件。Invoke when user needs DateTimePicker 日期时间选择器 in Vue 2.x project."
url: "https://element.eleme.cn/#/zh-CN/component/datetime-picker"
---

---

## [¶](https://element.eleme.cn/#/zh-CN/component/datetime-picker#datetimepicker-ri-qi-shi-jian-xuan-ze-qi) DateTimePicker 日期时间选择器

在同一个选择器里选择日期和时间

DateTimePicker 由 DatePicker 和 TimePicker 派生，`Picker Options` 或者其他选项可以参照 DatePicker 和 TimePicker。

### [¶](https://element.eleme.cn/#/zh-CN/component/datetime-picker#ri-qi-he-shi-jian-dian) 日期和时间点

默认

带快捷选项

设置默认时间

通过设置`type`属性为`datetime`，即可在同一个选择器里同时进行日期和时间的选择。快捷选项的使用方法与 Date Picker 相同。

```
<template>
  <div class="block">
    <span class="demonstration">默认</span>
    <el-date-picker
      v-model="value1"
      type="datetime"
      placeholder="选择日期时间">
    </el-date-picker>
  </div>
  <div class="block">
    <span class="demonstration">带快捷选项</span>
    <el-date-picker
      v-model="value2"
      type="datetime"
      placeholder="选择日期时间"
      align="right"
      :picker-options="pickerOptions">
    </el-date-picker>
  </div>
  <div class="block">
    <span class="demonstration">设置默认时间</span>
    <el-date-picker
      v-model="value3"
      type="datetime"
      placeholder="选择日期时间"
      default-time="12:00:00">
    </el-date-picker>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        pickerOptions: {
          shortcuts: [{
            text: '今天',
            onClick(picker) {
              picker.$emit('pick', new Date());
            }
          }, {
            text: '昨天',
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24);
              picker.$emit('pick', date);
            }
          }, {
            text: '一周前',
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', date);
            }
          }]
        },
        value1: '',
        value2: '',
        value3: ''
      };
    }
  };
</script>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/datetime-picker#ri-qi-he-shi-jian-fan-wei) 日期和时间范围

默认

至

带快捷选项

至

设置`type`为`datetimerange`即可选择日期和时间范围

```
<template>
  <div class="block">
    <span class="demonstration">默认</span>
    <el-date-picker
      v-model="value1"
      type="datetimerange"
      range-separator="至"
      start-placeholder="开始日期"
      end-placeholder="结束日期">
    </el-date-picker>
  </div>
  <div class="block">
    <span class="demonstration">带快捷选项</span>
    <el-date-picker
      v-model="value2"
      type="datetimerange"
      :picker-options="pickerOptions"
      range-separator="至"
      start-placeholder="开始日期"
      end-placeholder="结束日期"
      align="right">
    </el-date-picker>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        pickerOptions: {
          shortcuts: [{
            text: '最近一周',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '最近一个月',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '最近三个月',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
              picker.$emit('pick', [start, end]);
            }
          }]
        },
        value1: [new Date(2000, 10, 10, 10, 10), new Date(2000, 10, 11, 10, 10)],
        value2: ''
      };
    }
  };
</script>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/datetime-picker#mo-ren-de-qi-shi-yu-jie-shu-shi-ke) 默认的起始与结束时刻

起始日期时刻为 12:00:00

\-

起始日期时刻为 12:00:00，结束日期时刻为 08:00:00

\-

使用`datetimerange`进行范围选择时，在日期选择面板中选定起始与结束的日期，默认会使用该日期的`00:00:00`作为起始与结束的时刻；通过选项`default-time`可以控制选中起始与结束日期时所使用的具体时刻。`default-time`接受一个数组，数组每项值为字符串，形如`12:00:00`，其中第一项控制起始日期的具体时刻，第二项控制结束日期的具体时刻。

```
<template>
  <div class="block">
    <span class="demonstration">起始日期时刻为 12:00:00</span>
    <el-date-picker
      v-model="value1"
      type="datetimerange"
      start-placeholder="开始日期"
      end-placeholder="结束日期"
      :default-time="['12:00:00']">
    </el-date-picker>
  </div>
  <div class="block">
    <span class="demonstration">起始日期时刻为 12:00:00，结束日期时刻为 08:00:00</span>
    <el-date-picker
      v-model="value2"
      type="datetimerange"
      align="right"
      start-placeholder="开始日期"
      end-placeholder="结束日期"
      :default-time="['12:00:00', '08:00:00']">
    </el-date-picker>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        value1: '',
        value2: ''
      };
    }
  };
</script>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/datetime-picker#attributes) Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| value / v-model | 绑定值 | date(DateTimePicker) / array(DateTimeRangePicker) | — | — |
| readonly | 完全只读 | boolean | — | false |
| disabled | 禁用 | boolean | — | false |
| editable | 文本框可输入 | boolean | — | true |
| clearable | 是否显示清除按钮 | boolean | — | true |
| size | 输入框尺寸 | string | large, small, mini | — |
| placeholder | 非范围选择时的占位内容 | string | — | — |
| start-placeholder | 范围选择时开始日期的占位内容 | string | — | — |
| end-placeholder | 范围选择时结束日期的占位内容 | string | — | — |
| time-arrow-control | 是否使用箭头进行时间选择 | boolean | — | false |
| type | 显示类型 | string | year/month/date/week/ datetime/datetimerange/daterange | date |
| format | 显示在输入框中的格式 | string | 见[日期格式](#/zh-CN/component/date-picker#ri-qi-ge-shi) | yyyy-MM-dd HH:mm:ss |
| align | 对齐方式 | string | left, center, right | left |
| popper-class | DateTimePicker 下拉框的类名 | string | — | — |
| picker-options | 当前时间日期选择器特有的选项参考下表 | object | — | {} |
| range-separator | 选择范围时的分隔符 | string | \- | '-' |
| default-value | 可选，选择器打开时默认显示的时间 | Date | 可被`new Date()`解析 | — |
| default-time | 选中日期后的默认具体时刻 | 非范围选择时：string / 范围选择时：string\[\] | 非范围选择时：形如`12:00:00`的字符串；范围选择时：数组，长度为 2，每项值为字符串，形如`12:00:00`，第一项指定开始日期的时刻，第二项指定结束日期的时刻。不指定会使用时刻 `00:00:00` | — |
| value-format | 可选，绑定值的格式。不指定则绑定值为 Date 对象 | string | 见[日期格式](#/zh-CN/component/date-picker#ri-qi-ge-shi) | — |
| name | 原生属性 | string | — | — |
| unlink-panels | 在范围选择器里取消两个日期面板之间的联动 | boolean | — | false |
| prefix-icon | 自定义头部图标的类名 | string | — | el-icon-date |
| clear-icon | 自定义清空图标的类名 | string | — | el-icon-circle-close |

### [¶](https://element.eleme.cn/#/zh-CN/component/datetime-picker#picker-options) Picker Options

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| shortcuts | 设置快捷选项，需要传入 { text, onClick } 对象用法参考 demo 或下表 | Object\[\] | — | — |
| disabledDate | 设置禁用状态，参数为当前日期，要求返回 Boolean | Function | — | — |
| cellClassName | 设置日期的 className | Function(Date) | — | — |
| firstDayOfWeek | 周起始日 | Number | 1 到 7 | 7 |

### [¶](https://element.eleme.cn/#/zh-CN/component/datetime-picker#shortcuts) Shortcuts

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| text | 标题文本 | string | — | — |
| onClick | 选中后的回调函数，参数是 vm，可通过触发 'pick' 事件设置选择器的值。例如 vm.$emit('pick', new Date()) | function | — | — |

### [¶](https://element.eleme.cn/#/zh-CN/component/datetime-picker#events) Events

| Event Name | Description | Parameters |
| --- | --- | --- |
| change | 用户确认选定的值时触发 | 组件绑定值。格式与绑定值一致，可受 `value-format` 控制 |
| blur | 当 input 失去焦点时触发 | 组件实例 |
| focus | 当 input 获得焦点时触发 | 组件实例 |

### [¶](https://element.eleme.cn/#/zh-CN/component/datetime-picker#methods) Methods

| 方法名 | 说明 | 参数 |
| --- | --- | --- |
| focus | 使 input 获取焦点 | — |

### [¶](https://element.eleme.cn/#/zh-CN/component/datetime-picker#slots) Slots

| Name | 说明 |
| --- | --- |
| range-separator | 自定义分隔符 |

DatePicker 日期选择器 Upload 上传


