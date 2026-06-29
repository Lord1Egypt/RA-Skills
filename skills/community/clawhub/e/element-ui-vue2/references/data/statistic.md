---
name: "statistic"
description: "Statistic 统计数值 -- Element UI Vue2 桌面端组件。Invoke when user needs Statistic 统计数值 in Vue 2.x project."
url: "https://element.eleme.cn/#/zh-CN/component/statistic"
---

---

## [¶](https://element.eleme.cn/#/zh-CN/component/statistic#statistic-tong-ji-shu-zhi) Statistic 统计数值

用于突出某个或某组数字时，如显示数值，如金额，排名等。

倒计时模式

### [¶](https://element.eleme.cn/#/zh-CN/component/statistic#ji-chu-yong-fa) 基础用法

组件提供千分位的展示，不过可以通过 rate 来设置相应万分位等

增长人数

1,314.00

男女比

456/2

增长人数

4,154.56

Feedback

521

```
<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="6">
        <div>
          <el-statistic
            group-separator=","
            :precision="2"
            :value="value2"
            :title="title"
          ></el-statistic>
        </div>
      </el-col>
      <el-col :span="6">
        <div>
          <el-statistic title="男女比">
            <template slot="formatter">
              456/2
            </template>
          </el-statistic>
        </div>
      </el-col>
      <el-col :span="6">
        <div>
          <el-statistic
            group-separator=","
            :precision="2"
            decimal-separator="."
            :value="value1"
            :title="title"
          >
            <template slot="prefix">
              <i class="el-icon-s-flag" style="color: red"></i>
            </template>
            <template slot="suffix">
              <i class="el-icon-s-flag" style="color: blue"></i>
            </template>
          </el-statistic>
        </div>
      </el-col>
      <el-col :span="6">
        <div>
          <el-statistic :value="like ? 521 : 520" title="Feedback">
            <template slot="suffix">
              <span @click="like = !like" class="like">
                <i
                  class="el-icon-star-on"
                  style="color:red"
                  v-show="!!like"
                ></i>
                <i class="el-icon-star-off" v-show="!like"></i>
              </span>
            </template>
          </el-statistic>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        like: true,
        value1: 4154.564,
        value2: 1314,
        title: "增长人数",
      };
    },
  };
</script>
<style lang="scss">
  .like {
    cursor: pointer;
    font-size: 25px;
    display: inline-block;
  }
</style>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/statistic#dao-ji-shi) 倒计时

如果需要在原基础上添加时间，请注意：整体的时间（添加的时间量和原定时间）必须是**未来**的时间节点，否则依旧是倒计时结束

🎉商品降价🎉

07:59:43:763 抢购即将开始

时间游戏

00:29:43:762add 10s

🚩距离立夏还有：

00天00小时00分钟

文嘉《明日歌》 暂停

明日复明日

明日何其多

我生待明日

万事成蹉跎

距离明日：

13:17:47

通过 `value` 提供未来的时间，将开启倒计时功能

```
<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="14">
        <el-card shadow="hover" style="width: 100%;">
          <div style="width: 100%; display: inline-block; ">
            <el-statistic :value="deadline2" time-indices title="🎉商品降价🎉">
              <template slot="suffix">
                抢购即将开始
              </template>
            </el-statistic>
          </div>
        </el-card>
        <el-card shadow="hover" style="width: 100%;margin-top: 20px; ">
          <div style="width: 100%; display: inline-block; ">
            <el-statistic
              @finish="hilarity"
              :value="deadline3"
              time-indices
              title="时间游戏"
            >
              <template slot="suffix">
                <el-button type="primary " size="mini" @click="add"
                  >add 10s</el-button
                >
              </template>
            </el-statistic>
          </div>
        </el-card>
        <el-card shadow="hover" style="width: 100%;margin-top: 20px; ">
          <div style="width: 100%; display: inline-block;">
            <el-statistic
              format="DD天HH小时mm分钟"
              :value="deadline5"
              time-indices
              title="🚩距离立夏还有："
            >
            </el-statistic>
          </div>
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card shadow="hover" style="width: 100%;">
          <div slot="header" class="clearfix">
            <span>文嘉《明日歌》</span>
            <el-button
              style="float: right; padding: 3px 0"
              type="text"
              @click="clickFn"
              >暂停</el-button
            >
          </div>
          <div style="font-size: 18px;text-align: center; margin-top: 35px;">
            明日复明日
          </div>
          <div style="font-size: 18px;text-align: center;">明日何其多</div>
          <div style="font-size: 18px;text-align: center;">我生待明日</div>
          <div style="font-size: 18px;text-align: center;">万事成蹉跎</div>
          <div style="margin-top: 35px;"></div>
          <el-statistic
            ref="statistic"
            @finish="hilarity"
            format="HH:mm:ss"
            :value="deadline4"
            title="距离明日："
            time-indices
          >
          </el-statistic>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        deadline2: Date.now() + 1000 * 60 * 60 * 8,
        deadline3: Date.now() + 1000 * 60 * 30,
        deadline4: Date.now() + (new Date().setHours(23, 59, 59) - Date.now()),
        deadline5: new Date("2023-05-06"),
        stop: true,
      };
    },
    methods: {
      hilarity() {
        this.$notify({
          title: "提示",
          message: "时间已到",
          duration: 0,
        });
      },
      clickFn() {
        this.$refs.statistic.suspend(this.stop);
        this.stop = !this.stop;
      },
      add() {
        this.deadline3 = this.deadline3 + 1000 * 10;
      },
    },
  };
</script>
```

显示代码 在线运行

### [¶](https://element.eleme.cn/#/zh-CN/component/statistic#statistic-attributes) Statistic Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| value | 数值内容 | string | number | — | — |
| decimal-separator | 设置小数点 | string | — | . |
| formatter | 自定义数值展示 | v-slot |({value}) => VNode | — | — |
| group-separator | 设置千分位标识符 | string | — | , |
| precision | 数值精度 | number | — | — |
| prefix | 设置数值的前缀 | string | v-slot | — | — |
| suffix | 设置数值的后缀 | string | v-slot | — | — |
| title | 数值的标题 | string | v-slot | — | — |
| value-style | 设置数值的样式 | object | — | — |
| rate | 设置倍率 | number | — | 1000 |

### [¶](https://element.eleme.cn/#/zh-CN/component/statistic#statistic-slots) Statistic Slots

| name | 说明 |
| --- | --- |
| prefix | 数值的前缀 |
| suffix | 数值的后缀 |
| formatter | 数值内容 |
| title | 数值的标题 |

### [¶](https://element.eleme.cn/#/zh-CN/component/statistic#statistic-countdown-attributes) Statistic.Countdown Attributes

| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| time-indices | 是否开启倒计时功能 | boolean | true|false | false |
| value | 必填值，输入绑定值 | string | — | — |
| format | 格式化倒计时展示 | string | — | 'HH:mm:ss' |

### [¶](https://element.eleme.cn/#/zh-CN/component/statistic#statistic-countdown-events) Statistic.Countdown Events

| 事件名称 | 说明 | 回调参数 |
| --- | --- | --- |
| change | 在`倒计时`的功能中开启 | (value: Date) |
| finish | 在`倒计时` 完成后启动 | (value: boolean) |

### [¶](https://element.eleme.cn/#/zh-CN/component/statistic#statistic-methods) Statistic Methods

| 方法名 | 说明 | 参数 | 回调参数 |
| --- | --- | --- | --- |
| suspend | 暂停倒计时 | (value:boolean) | (value: Date) |

Result 结果 Alert 警告


