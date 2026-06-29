---
name: "statistic"
description: "Statistic 统计组件 -- Element Plus Vue3 桌面端组件。Invoke when user needs Statistic 统计组件 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/statistic.html"
---

---

# Statistic 统计组件 [​](#statistic-统计组件)

更新日志待解决

0

显示统计数据。

## 基础用法 [​](#基础用法)

用于突出某个或某组数字时，如统计数值、金额、排名等，数值和标题前后都可以加icon、单位等元素。 可以使用 [vueuse](https://vueuse.org/core/useTransition/) 实现数值的变化动效

Daily active users

268,500

Ratio of men to women

138

/100

Total Transactions

172,000

Feedback number

562

TS

JS

_[](https://element-plus.run/?extra_packages=%40vueuse%2Fcore#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcm93IDpndXR0ZXI9XCIxNlwiPlxuICAgIDxlbC1jb2wgOnhzPVwiMjRcIiA6c209XCIxMlwiIDptZD1cIjZcIiBjbGFzcz1cInRleHQtY2VudGVyIG1iLTRcIj5cbiAgICAgIDxlbC1zdGF0aXN0aWMgdGl0bGU9XCJEYWlseSBhY3RpdmUgdXNlcnNcIiA6dmFsdWU9XCIyNjg1MDBcIiAvPlxuICAgIDwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnhzPVwiMjRcIiA6c209XCIxMlwiIDptZD1cIjZcIiBjbGFzcz1cInRleHQtY2VudGVyIG1iLTRcIj5cbiAgICAgIDxlbC1zdGF0aXN0aWMgOnZhbHVlPVwiMTM4XCI+XG4gICAgICAgIDx0ZW1wbGF0ZSAjdGl0bGU+XG4gICAgICAgICAgPGRpdiBzdHlsZT1cImRpc3BsYXk6IGlubGluZS1mbGV4OyBhbGlnbi1pdGVtczogY2VudGVyXCI+XG4gICAgICAgICAgICBSYXRpbyBvZiBtZW4gdG8gd29tZW5cbiAgICAgICAgICAgIDxlbC1pY29uIHN0eWxlPVwibWFyZ2luLWxlZnQ6IDRweFwiIDpzaXplPVwiMTJcIj5cbiAgICAgICAgICAgICAgPE1hbGUgLz5cbiAgICAgICAgICAgIDwvZWwtaWNvbj5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgICAgPHRlbXBsYXRlICNzdWZmaXg+LzEwMDwvdGVtcGxhdGU+XG4gICAgICA8L2VsLXN0YXRpc3RpYz5cbiAgICA8L2VsLWNvbD5cbiAgICA8ZWwtY29sIDp4cz1cIjI0XCIgOnNtPVwiMTJcIiA6bWQ9XCI2XCIgY2xhc3M9XCJ0ZXh0LWNlbnRlciBtYi00XCI+XG4gICAgICA8ZWwtc3RhdGlzdGljIHRpdGxlPVwiVG90YWwgVHJhbnNhY3Rpb25zXCIgOnZhbHVlPVwib3V0cHV0VmFsdWVcIiAvPlxuICAgIDwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnhzPVwiMjRcIiA6c209XCIxMlwiIDptZD1cIjZcIiBjbGFzcz1cInRleHQtY2VudGVyIG1iLTRcIj5cbiAgICAgIDxlbC1zdGF0aXN0aWMgdGl0bGU9XCJGZWVkYmFjayBudW1iZXJcIiA6dmFsdWU9XCI1NjJcIj5cbiAgICAgICAgPHRlbXBsYXRlICNzdWZmaXg+XG4gICAgICAgICAgPGVsLWljb24gc3R5bGU9XCJ2ZXJ0aWNhbC1hbGlnbjogLTAuMTI1ZW1cIj5cbiAgICAgICAgICAgIDxDaGF0TGluZVJvdW5kIC8+XG4gICAgICAgICAgPC9lbC1pY29uPlxuICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgPC9lbC1zdGF0aXN0aWM+XG4gICAgPC9lbC1jb2w+XG4gIDwvZWwtcm93PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IHVzZVRyYW5zaXRpb24gfSBmcm9tICdAdnVldXNlL2NvcmUnXG5pbXBvcnQgeyBDaGF0TGluZVJvdW5kLCBNYWxlIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG5cbmNvbnN0IHNvdXJjZSA9IHJlZigwKVxuY29uc3Qgb3V0cHV0VmFsdWUgPSB1c2VUcmFuc2l0aW9uKHNvdXJjZSwge1xuICBkdXJhdGlvbjogMTUwMCxcbn0pXG5zb3VyY2UudmFsdWUgPSAxNzIwMDBcbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/statistic/basic.vue)_

vue

```
<template>
  <el-row :gutter="16">
    <el-col :xs="24" :sm="12" :md="6" class="text-center mb-4">
      <el-statistic title="Daily active users" :value="268500" />
    </el-col>
    <el-col :xs="24" :sm="12" :md="6" class="text-center mb-4">
      <el-statistic :value="138">
        <template #title>
          <div style="display: inline-flex; align-items: center">
            Ratio of men to women
            <el-icon style="margin-left: 4px" :size="12">
              <Male />
            </el-icon>
          </div>
        </template>
        <template #suffix>/100</template>
      </el-statistic>
    </el-col>
    <el-col :xs="24" :sm="12" :md="6" class="text-center mb-4">
      <el-statistic title="Total Transactions" :value="outputValue" />
    </el-col>
    <el-col :xs="24" :sm="12" :md="6" class="text-center mb-4">
      <el-statistic title="Feedback number" :value="562">
        <template #suffix>
          <el-icon style="vertical-align: -0.125em">
            <ChatLineRound />
          </el-icon>
        </template>
      </el-statistic>
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useTransition } from '@vueuse/core'
import { ChatLineRound, Male } from '@element-plus/icons-vue'

const source = ref(0)
const outputValue = useTransition(source, {
  duration: 1500,
})
source.value = 172000
</script>
```

隐藏源代码

## 倒计时 [​](#倒计时)

倒计时组件，支持添加其他组件来控制。

Start to grab

06:59:56

Remaining VIP time

47:59:56

Reset

Still to go until next month

06 days 09:27:39

2026-07-01

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcm93IDpndXR0ZXI9XCIxNlwiPlxuICAgIDxlbC1jb2wgOnhzPVwiMjRcIiA6c209XCIxMlwiIDptZD1cIjhcIiBjbGFzcz1cInRleHQtY2VudGVyIG1iLTRcIj5cbiAgICAgIDxlbC1jb3VudGRvd24gdGl0bGU9XCJTdGFydCB0byBncmFiXCIgOnZhbHVlPVwidmFsdWVcIiAvPlxuICAgIDwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnhzPVwiMjRcIiA6c209XCIxMlwiIDptZD1cIjhcIiBjbGFzcz1cInRleHQtY2VudGVyIG1iLTRcIj5cbiAgICAgIDxlbC1jb3VudGRvd25cbiAgICAgICAgdGl0bGU9XCJSZW1haW5pbmcgVklQIHRpbWVcIlxuICAgICAgICBmb3JtYXQ9XCJISDptbTpzc1wiXG4gICAgICAgIDp2YWx1ZT1cInZhbHVlMVwiXG4gICAgICAvPlxuICAgICAgPGVsLWJ1dHRvbiBjbGFzcz1cImNvdW50ZG93bi1mb290ZXJcIiB0eXBlPVwicHJpbWFyeVwiIEBjbGljaz1cInJlc2V0XCI+XG4gICAgICAgIFJlc2V0XG4gICAgICA8L2VsLWJ1dHRvbj5cbiAgICA8L2VsLWNvbD5cbiAgICA8ZWwtY29sIDp4cz1cIjI0XCIgOnNtPVwiMTJcIiA6bWQ9XCI4XCIgY2xhc3M9XCJ0ZXh0LWNlbnRlciBtYi00XCI+XG4gICAgICA8ZWwtY291bnRkb3duIGZvcm1hdD1cIkREIFtkYXlzXSBISDptbTpzc1wiIDp2YWx1ZT1cInZhbHVlMlwiPlxuICAgICAgICA8dGVtcGxhdGUgI3RpdGxlPlxuICAgICAgICAgIDxkaXYgc3R5bGU9XCJkaXNwbGF5OiBpbmxpbmUtZmxleDsgYWxpZ24taXRlbXM6IGNlbnRlclwiPlxuICAgICAgICAgICAgPGVsLWljb24gc3R5bGU9XCJtYXJnaW4tcmlnaHQ6IDRweFwiIDpzaXplPVwiMTJcIj5cbiAgICAgICAgICAgICAgPENhbGVuZGFyIC8+XG4gICAgICAgICAgICA8L2VsLWljb24+XG4gICAgICAgICAgICBTdGlsbCB0byBnbyB1bnRpbCBuZXh0IG1vbnRoXG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICA8L2VsLWNvdW50ZG93bj5cbiAgICAgIDxkaXYgY2xhc3M9XCJjb3VudGRvd24tZm9vdGVyXCI+e3sgdmFsdWUyLmZvcm1hdCgnWVlZWS1NTS1ERCcpIH19PC9kaXY+XG4gICAgPC9lbC1jb2w+XG4gIDwvZWwtcm93PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCBkYXlqcyBmcm9tICdkYXlqcydcbmltcG9ydCB7IENhbGVuZGFyIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG5cbmNvbnN0IHZhbHVlID0gcmVmKERhdGUubm93KCkgKyAxMDAwICogNjAgKiA2MCAqIDcpXG5jb25zdCB2YWx1ZTEgPSByZWYoRGF0ZS5ub3coKSArIDEwMDAgKiA2MCAqIDYwICogMjQgKiAyKVxuY29uc3QgdmFsdWUyID0gcmVmKGRheWpzKCkuYWRkKDEsICdtb250aCcpLnN0YXJ0T2YoJ21vbnRoJykpXG5cbmZ1bmN0aW9uIHJlc2V0KCkge1xuICB2YWx1ZTEudmFsdWUgPSBEYXRlLm5vdygpICsgMTAwMCAqIDYwICogNjAgKiAyNCAqIDJcbn1cbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmNvdW50ZG93bi1mb290ZXIge1xuICBtYXJnaW4tdG9wOiA4cHg7XG59XG48L3N0eWxlPlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/statistic/countdown.vue)_

vue

```
<template>
  <el-row :gutter="16">
    <el-col :xs="24" :sm="12" :md="8" class="text-center mb-4">
      <el-countdown title="Start to grab" :value="value" />
    </el-col>
    <el-col :xs="24" :sm="12" :md="8" class="text-center mb-4">
      <el-countdown
        title="Remaining VIP time"
        format="HH:mm:ss"
        :value="value1"
      />
      <el-button class="countdown-footer" type="primary" @click="reset">
        Reset
      </el-button>
    </el-col>
    <el-col :xs="24" :sm="12" :md="8" class="text-center mb-4">
      <el-countdown format="DD [days] HH:mm:ss" :value="value2">
        <template #title>
          <div style="display: inline-flex; align-items: center">
            <el-icon style="margin-right: 4px" :size="12">
              <Calendar />
            </el-icon>
            Still to go until next month
          </div>
        </template>
      </el-countdown>
      <div class="countdown-footer">{{ value2.format('YYYY-MM-DD') }}</div>
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import dayjs from 'dayjs'
import { Calendar } from '@element-plus/icons-vue'

const value = ref(Date.now() + 1000 * 60 * 60 * 7)
const value1 = ref(Date.now() + 1000 * 60 * 60 * 24 * 2)
const value2 = ref(dayjs().add(1, 'month').startOf('month'))

function reset() {
  value1.value = Date.now() + 1000 * 60 * 60 * 24 * 2
}
</script>

<style scoped>
.countdown-footer {
  margin-top: 8px;
}
</style>
```

隐藏源代码

TIP

在格式化过程中，建议在天数范围内

## 统计卡片 [​](#统计卡片)

卡片式用法展示，可以自由组合

Daily active users

98,500

than yesterday 24%

Monthly Active Users

693,700

month on month 12%

New transactions today

72,000

than yesterday 16%

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtcm93IDpndXR0ZXI9XCIxNlwiPlxuICAgIDxlbC1jb2wgOnhzPVwiMjRcIiA6c209XCIxMlwiIDptZD1cIjhcIiBjbGFzcz1cIm1iLTRcIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJzdGF0aXN0aWMtY2FyZFwiPlxuICAgICAgICA8ZWwtc3RhdGlzdGljIDp2YWx1ZT1cIjk4NTAwXCI+XG4gICAgICAgICAgPHRlbXBsYXRlICN0aXRsZT5cbiAgICAgICAgICAgIDxkaXYgc3R5bGU9XCJkaXNwbGF5OiBpbmxpbmUtZmxleDsgYWxpZ24taXRlbXM6IGNlbnRlclwiPlxuICAgICAgICAgICAgICBEYWlseSBhY3RpdmUgdXNlcnNcbiAgICAgICAgICAgICAgPGVsLXRvb2x0aXBcbiAgICAgICAgICAgICAgICBlZmZlY3Q9XCJkYXJrXCJcbiAgICAgICAgICAgICAgICBjb250ZW50PVwiTnVtYmVyIG9mIHVzZXJzIHdobyBsb2dnZWQgaW50byB0aGUgcHJvZHVjdCBpbiBvbmUgZGF5XCJcbiAgICAgICAgICAgICAgICBwbGFjZW1lbnQ9XCJ0b3BcIlxuICAgICAgICAgICAgICA+XG4gICAgICAgICAgICAgICAgPGVsLWljb24gc3R5bGU9XCJtYXJnaW4tbGVmdDogNHB4XCIgOnNpemU9XCIxMlwiPlxuICAgICAgICAgICAgICAgICAgPFdhcm5pbmcgLz5cbiAgICAgICAgICAgICAgICA8L2VsLWljb24+XG4gICAgICAgICAgICAgIDwvZWwtdG9vbHRpcD5cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDwvdGVtcGxhdGU+XG4gICAgICAgIDwvZWwtc3RhdGlzdGljPlxuICAgICAgICA8ZGl2IGNsYXNzPVwic3RhdGlzdGljLWZvb3RlclwiPlxuICAgICAgICAgIDxkaXYgY2xhc3M9XCJmb290ZXItaXRlbVwiPlxuICAgICAgICAgICAgPHNwYW4+dGhhbiB5ZXN0ZXJkYXk8L3NwYW4+XG4gICAgICAgICAgICA8c3BhbiBjbGFzcz1cImdyZWVuXCI+XG4gICAgICAgICAgICAgIDI0JVxuICAgICAgICAgICAgICA8ZWwtaWNvbj5cbiAgICAgICAgICAgICAgICA8Q2FyZXRUb3AgLz5cbiAgICAgICAgICAgICAgPC9lbC1pY29uPlxuICAgICAgICAgICAgPC9zcGFuPlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZGl2PlxuICAgIDwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnhzPVwiMjRcIiA6c209XCIxMlwiIDptZD1cIjhcIiBjbGFzcz1cIm1iLTRcIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJzdGF0aXN0aWMtY2FyZFwiPlxuICAgICAgICA8ZWwtc3RhdGlzdGljIDp2YWx1ZT1cIjY5MzcwMFwiPlxuICAgICAgICAgIDx0ZW1wbGF0ZSAjdGl0bGU+XG4gICAgICAgICAgICA8ZGl2IHN0eWxlPVwiZGlzcGxheTogaW5saW5lLWZsZXg7IGFsaWduLWl0ZW1zOiBjZW50ZXJcIj5cbiAgICAgICAgICAgICAgTW9udGhseSBBY3RpdmUgVXNlcnNcbiAgICAgICAgICAgICAgPGVsLXRvb2x0aXBcbiAgICAgICAgICAgICAgICBlZmZlY3Q9XCJkYXJrXCJcbiAgICAgICAgICAgICAgICBjb250ZW50PVwiTnVtYmVyIG9mIHVzZXJzIHdobyBsb2dnZWQgaW50byB0aGUgcHJvZHVjdCBpbiBvbmUgbW9udGhcIlxuICAgICAgICAgICAgICAgIHBsYWNlbWVudD1cInRvcFwiXG4gICAgICAgICAgICAgID5cbiAgICAgICAgICAgICAgICA8ZWwtaWNvbiBzdHlsZT1cIm1hcmdpbi1sZWZ0OiA0cHhcIiA6c2l6ZT1cIjEyXCI+XG4gICAgICAgICAgICAgICAgICA8V2FybmluZyAvPlxuICAgICAgICAgICAgICAgIDwvZWwtaWNvbj5cbiAgICAgICAgICAgICAgPC9lbC10b29sdGlwPlxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgPC90ZW1wbGF0ZT5cbiAgICAgICAgPC9lbC1zdGF0aXN0aWM+XG4gICAgICAgIDxkaXYgY2xhc3M9XCJzdGF0aXN0aWMtZm9vdGVyXCI+XG4gICAgICAgICAgPGRpdiBjbGFzcz1cImZvb3Rlci1pdGVtXCI+XG4gICAgICAgICAgICA8c3Bhbj5tb250aCBvbiBtb250aDwvc3Bhbj5cbiAgICAgICAgICAgIDxzcGFuIGNsYXNzPVwicmVkXCI+XG4gICAgICAgICAgICAgIDEyJVxuICAgICAgICAgICAgICA8ZWwtaWNvbj5cbiAgICAgICAgICAgICAgICA8Q2FyZXRCb3R0b20gLz5cbiAgICAgICAgICAgICAgPC9lbC1pY29uPlxuICAgICAgICAgICAgPC9zcGFuPlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZGl2PlxuICAgIDwvZWwtY29sPlxuICAgIDxlbC1jb2wgOnhzPVwiMjRcIiA6c209XCIxMlwiIDptZD1cIjhcIiBjbGFzcz1cIm1iLTRcIj5cbiAgICAgIDxkaXYgY2xhc3M9XCJzdGF0aXN0aWMtY2FyZFwiPlxuICAgICAgICA8ZWwtc3RhdGlzdGljIDp2YWx1ZT1cIjcyMDAwXCIgdGl0bGU9XCJOZXcgdHJhbnNhY3Rpb25zIHRvZGF5XCI+XG4gICAgICAgICAgPHRlbXBsYXRlICN0aXRsZT5cbiAgICAgICAgICAgIDxkaXYgc3R5bGU9XCJkaXNwbGF5OiBpbmxpbmUtZmxleDsgYWxpZ24taXRlbXM6IGNlbnRlclwiPlxuICAgICAgICAgICAgICBOZXcgdHJhbnNhY3Rpb25zIHRvZGF5XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICA8L3RlbXBsYXRlPlxuICAgICAgICA8L2VsLXN0YXRpc3RpYz5cbiAgICAgICAgPGRpdiBjbGFzcz1cInN0YXRpc3RpYy1mb290ZXJcIj5cbiAgICAgICAgICA8ZGl2IGNsYXNzPVwiZm9vdGVyLWl0ZW1cIj5cbiAgICAgICAgICAgIDxzcGFuPnRoYW4geWVzdGVyZGF5PC9zcGFuPlxuICAgICAgICAgICAgPHNwYW4gY2xhc3M9XCJncmVlblwiPlxuICAgICAgICAgICAgICAxNiVcbiAgICAgICAgICAgICAgPGVsLWljb24+XG4gICAgICAgICAgICAgICAgPENhcmV0VG9wIC8+XG4gICAgICAgICAgICAgIDwvZWwtaWNvbj5cbiAgICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICA8ZGl2IGNsYXNzPVwiZm9vdGVyLWl0ZW1cIj5cbiAgICAgICAgICAgIDxlbC1pY29uIDpzaXplPVwiMTRcIj5cbiAgICAgICAgICAgICAgPEFycm93UmlnaHQgLz5cbiAgICAgICAgICAgIDwvZWwtaWNvbj5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2Rpdj5cbiAgICA8L2VsLWNvbD5cbiAgPC9lbC1yb3c+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHtcbiAgQXJyb3dSaWdodCxcbiAgQ2FyZXRCb3R0b20sXG4gIENhcmV0VG9wLFxuICBXYXJuaW5nLFxufSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuOmdsb2JhbChoMiNjYXJkLXVzYWdlIH4gLmV4YW1wbGUgLmV4YW1wbGUtc2hvd2Nhc2UpIHtcbiAgYmFja2dyb3VuZC1jb2xvcjogdmFyKC0tZWwtZmlsbC1jb2xvcikgIWltcG9ydGFudDtcbn1cblxuLmVsLXN0YXRpc3RpYyB7XG4gIC0tZWwtc3RhdGlzdGljLWNvbnRlbnQtZm9udC1zaXplOiAyOHB4O1xufVxuXG4uc3RhdGlzdGljLWNhcmQge1xuICBoZWlnaHQ6IDEwMCU7XG4gIHBhZGRpbmc6IDIwcHg7XG4gIGJvcmRlci1yYWRpdXM6IDRweDtcbiAgYmFja2dyb3VuZC1jb2xvcjogdmFyKC0tZWwtYmctY29sb3Itb3ZlcmxheSk7XG59XG5cbi5zdGF0aXN0aWMtZm9vdGVyIHtcbiAgZGlzcGxheTogZmxleDtcbiAganVzdGlmeS1jb250ZW50OiBzcGFjZS1iZXR3ZWVuO1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xuICBmbGV4LXdyYXA6IHdyYXA7XG4gIGZvbnQtc2l6ZTogMTJweDtcbiAgY29sb3I6IHZhcigtLWVsLXRleHQtY29sb3ItcmVndWxhcik7XG4gIG1hcmdpbi10b3A6IDE2cHg7XG59XG5cbi5zdGF0aXN0aWMtZm9vdGVyIC5mb290ZXItaXRlbSB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGp1c3RpZnktY29udGVudDogc3BhY2UtYmV0d2VlbjtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbn1cblxuLnN0YXRpc3RpYy1mb290ZXIgLmZvb3Rlci1pdGVtIHNwYW46bGFzdC1jaGlsZCB7XG4gIGRpc3BsYXk6IGlubGluZS1mbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xuICBtYXJnaW4tbGVmdDogNHB4O1xufVxuXG4uZ3JlZW4ge1xuICBjb2xvcjogdmFyKC0tZWwtY29sb3Itc3VjY2Vzcyk7XG59XG4ucmVkIHtcbiAgY29sb3I6IHZhcigtLWVsLWNvbG9yLWVycm9yKTtcbn1cbjwvc3R5bGU+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/statistic/card.vue)_

vue

```
<template>
  <el-row :gutter="16">
    <el-col :xs="24" :sm="12" :md="8" class="mb-4">
      <div class="statistic-card">
        <el-statistic :value="98500">
          <template #title>
            <div style="display: inline-flex; align-items: center">
              Daily active users
              <el-tooltip
                effect="dark"
                content="Number of users who logged into the product in one day"
                placement="top"
              >
                <el-icon style="margin-left: 4px" :size="12">
                  <Warning />
                </el-icon>
              </el-tooltip>
            </div>
          </template>
        </el-statistic>
        <div class="statistic-footer">
          <div class="footer-item">
            <span>than yesterday</span>
            <span class="green">
              24%
              <el-icon>
                <CaretTop />
              </el-icon>
            </span>
          </div>
        </div>
      </div>
    </el-col>
    <el-col :xs="24" :sm="12" :md="8" class="mb-4">
      <div class="statistic-card">
        <el-statistic :value="693700">
          <template #title>
            <div style="display: inline-flex; align-items: center">
              Monthly Active Users
              <el-tooltip
                effect="dark"
                content="Number of users who logged into the product in one month"
                placement="top"
              >
                <el-icon style="margin-left: 4px" :size="12">
                  <Warning />
                </el-icon>
              </el-tooltip>
            </div>
          </template>
        </el-statistic>
        <div class="statistic-footer">
          <div class="footer-item">
            <span>month on month</span>
            <span class="red">
              12%
              <el-icon>
                <CaretBottom />
              </el-icon>
            </span>
          </div>
        </div>
      </div>
    </el-col>
    <el-col :xs="24" :sm="12" :md="8" class="mb-4">
      <div class="statistic-card">
        <el-statistic :value="72000" title="New transactions today">
          <template #title>
            <div style="display: inline-flex; align-items: center">
              New transactions today
            </div>
          </template>
        </el-statistic>
        <div class="statistic-footer">
          <div class="footer-item">
            <span>than yesterday</span>
            <span class="green">
              16%
              <el-icon>
                <CaretTop />
              </el-icon>
            </span>
          </div>
          <div class="footer-item">
            <el-icon :size="14">
              <ArrowRight />
            </el-icon>
          </div>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import {
  ArrowRight,
  CaretBottom,
  CaretTop,
  Warning,
} from '@element-plus/icons-vue'
</script>

<style scoped>
:global(h2#card-usage ~ .example .example-showcase) {
  background-color: var(--el-fill-color) !important;
}

.el-statistic {
  --el-statistic-content-font-size: 28px;
}

.statistic-card {
  height: 100%;
  padding: 20px;
  border-radius: 4px;
  background-color: var(--el-bg-color-overlay);
}

.statistic-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  font-size: 12px;
  color: var(--el-text-color-regular);
  margin-top: 16px;
}

.statistic-footer .footer-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.statistic-footer .footer-item span:last-child {
  display: inline-flex;
  align-items: center;
  margin-left: 4px;
}

.green {
  color: var(--el-color-success);
}
.red {
  color: var(--el-color-error);
}
</style>
```

隐藏源代码

## Statistic API [​](#statistic-api)

### Statistic Attributes [​](#statistic-attributes)

| Attribute | 描述 | 类型 | 默认值 |
| --- | --- | --- | --- |
| value | 数字内容 | `number` | 0 |
| decimal-separator | 设置小数点符号 | `string` | . |
| formatter | 自定义数字格式化 | `Function` | — |
| group-separator | 设置千分位标识符 | `string` | , |
| precision | 数字精度 | `number` | 0 |
| prefix | 设置数字的前缀 | `string` | — |
| suffix | 设置数字的后缀 | `string` | — |
| title | 数字标题 | `string` | — |
| value-style | 数字样式 | `string` / `object` | — |

### Statistic Slots [​](#statistic-slots)

| 插槽名 | 详情 |
| --- | --- |
| prefix | 数字区之前 |
| suffix | 数字区之后 |
| title | 数字标题 |

### Statistic Exposes [​](#statistic-exposes)

| 名称 | 描述 | 类型 |
| --- | --- | --- |
| displayValue | 当前显示值 | `object` |

## Countdown API [​](#countdown-api)

### Countdown Attributes [​](#countdown-attributes)

| 属性 | 详情 | 类型 | 默认值 |
| --- | --- | --- | --- |
| value | 目标时间 | `number` / `Dayjs` | — |
| format | 格式化倒计时 | `string` | HH:mm:ss |
| prefix | 设置倒计时前缀 | `string` | — |
| suffix | 设置倒计时的后缀 | `string` | — |
| title | 倒计时标题 | `string` | — |
| value-style | 倒计时值的样式 | `string` / `object` | — |

### Countdown Events [​](#countdown-events)

| 方法名 | 描述 | 类型 |
| --- | --- | --- |
| change | 时间差改变事件 | `Function` |
| finish | 倒计时结束事件 | `Function` |

### Countdown Slots [​](#countdown-slots)

| 插槽名 | 描述 |
| --- | --- |
| prefix | 倒计时值前缀 |
| suffix | 倒计时后缀 |
| title | 倒计时标题 |

### Countdown Exposes [​](#countdown-exposes)

| 名称 | 详情 | 类型 |
| --- | --- | --- |
| displayValue | 当前显示值 | `object` |

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/statistic) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/statistic.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/statistic.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/35138018?v=4&size=64)](https://github.com/tuskermanshu)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/30883395?v=4&size=64)](https://github.com/webvs2)[![](https://avatars.githubusercontent.com/u/34681550?v=4&size=64)](https://github.com/zhixiaotong)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/56016153?v=4&size=64)](https://github.com/zzjiaxiang)

[Virtualized Tree 虚拟化树形控件](https://element-plus.org/zh-CN/component/tree-v2)

[Segmented 分段控制器](https://element-plus.org/zh-CN/component/segmented)


