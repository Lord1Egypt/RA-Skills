## Transfer 穿梭框 ​

**URL:** https://element-plus.org/zh-CN/component/transfer

**Contents:**
- Transfer 穿梭框 ​
- 基础用法 ​
- 可搜索过滤 ​
- 自定义 ​
- 自定义空内容 2.9.0 ​
- 数据项属性别名 ​
- Virtual Scroll 2.14.3 ​
- Transfer API ​
  - Transfer Attributes ​
  - Transfer Events ​

Transfer 的数据通过 data 属性传入。 数据需要是一个对象数组，每个对象有以下属性：key 为数据的唯一性标识，label 为显示文本，disabled 表示该项数据是否禁止被操作。 目标列表中的数据项会同步到绑定至 v-model 的变量，值为数据项的 key 所组成的数组。 当然，如果希望在初始状态时目标列表不为空，可以像本例一样为 v-model 绑定的变量赋予一个初始值。

在数据很多的情况下，可以对数据进行搜索和过滤。

设置 filterable 为 true 即可开启搜索模式。 默认情况下，若数据项的 label 属性包含搜索关键字，则会在搜索结果中显示。 你也可以使用 filter-method 定义自己的搜索逻辑。 filter-method 接收一个方法，当搜索关键字变化时，会将当前的关键字和每个数据项传给该方法。 若方法返回 true，则会在搜索结果中显示对应的数据项。

可以对列表标题文案、按钮文案、数据项的渲染函数、列表底部的勾选状态文案、列表底部的内容区等进行自定义。

可以使用 titles、button-texts、render-content 和 format 属性分别对列表标题文案、按钮文案、数据项的渲染函数和列表顶部的勾选状态文案进行自定义。 数据项的渲染还可以使用 scoped-slot 进行自定义。 对于列表底部的内容区，提供了两个具名 slot：left-footer 和 right-footer。 此外，如果希望某些数据项在初始化时就被勾选，可以使用 left-default-checked 和 right-default-checked 属性。 最后，本例还展示了 change 事件的用法。 注意，由于 JSFiddle 不支持 JSX 语法，故该示例无法在 JSFiddle 运行。 但是在实际的项目中，只要正确地配置了相关依赖，就可以正常运行。

Customize data items using render-content

Customize data items using scoped slot

您可以自定义列表为空或未找到筛选结果时显示的内容。

使用 left-empty 和 right-empty 插槽来自定义每个面板的空内容。

默认情况下，Transfer 仅能识别数据项中的 key、label 和 disabled 字段。 如果你的数据的字段名不同，可以使用 props 属性为它们设置别名。

本例中的数据源没有 key 和 label 字段，在功能上与它们相同的字段名为 value 和 desc。 因此可以使用props 属性为 key 和 label 设置别名。

当处理大量数据时，您可以启用虚拟滚动以提高性能。

将 virtual-scroll 设置为 true 以启用虚拟滚动。 You can also customize the item height with item-size. Default item size is 30px.

**Examples:**

Example 1 (typescript):
```typescript
<template>
  <el-transfer v-model="value" :data="data" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

interface Option {
  key: number
  label: string
  disabled: boolean
}

const generateData = () => {
  const data: Option[] = []
  for (let i = 1; i <= 15; i++) {
    data.push({
      key: i,
      label: `Option ${i}`,
      disabled: i % 4 === 0,
    })
  }
  return data
}

const data = ref<Option[]>(generateData())
const value = ref([])
</script>
```

Example 2 (typescript):
```typescript
<template>
  <el-transfer
    v-model="value"
    filterable
    :filter-method="filterMethod"
    filter-placeholder="State Abbreviations"
    :data="data"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

interface Option {
  key: number
  label: string
  initial: string
}

const generateData = () => {
  const data: Option[] = []
  const states = [
    'California',
    'Illinois',
    'Maryland',
    'Texas',
    'Florida',
    'Colorado',
    'Connecticut ',
  ]
  const initials = ['CA', 'IL', 'MD', 'TX', 'FL', 'CO', 'CT']
  states.forEach((city, index) => {
    data.push({
      label: city,
      key: index,
      initial: initials[index],
    })
  })
  return data
}

const data = ref<Option[]>(generateData())
const value = ref([])

const filterMethod = (query, item) => {
  return item.initial.toLowerCase().includes(query.toLowerCase())
}
</script>
```

Example 3 (typescript):
```typescript
<template>
  <p style="text-align: center; margin: 0 0 20px">
    Customize data items using render-content
  </p>
  <div style="text-align: center">
    <el-transfer
      v-model="leftValue"
      style="text-align: left; display: inline-block"
      filterable
      :left-default-checked="[2, 3]"
      :right-default-checked="[1]"
      :render-content="renderFunc"
      :titles="['Source', 'Target']"
      :button-texts="['To left', 'To right']"
      :format="{
        noChecked: '${total}',
        hasChecked: '${checked}/${total}',
      }"
      :data="data"
      @change="handleChange"
    >
      <template #left-footer>
        <el-button class="transfer-footer" size="small">Operation</el-button>
      </template>
      <template #right-footer>
        <el-button class="transfer-footer" size="small">Operation</el-button>
      </template>
    </el-transfer>
    <p style="text-align: center; margin: 50px 0 20px">
      Customize data items using scoped slot
    </p>
    <div style="text-align: center">
      <el-transfer
        v-model="rightValue"
        style="text-align: left; display: inline-block"
        filterable
        :left-default-checked="[2, 3]"
        :right-default-checked="[1]"
        :titles="['Source', 'Target']"
        :button-texts="['To left', 'To right']"
        :format="{
          noChecked: '${total}',
          hasChecked: '${checked}/${total}',
        }"
        :data="data"
        @change="handleChange"
      >
        <template #default="{ option }">
          <span>{{ option.key }} - {{ option.label }}</span>
        </template>
        <template #left-footer>
          <el-button class="transfer-footer" size="small">Operation</el-button>
        </template>
        <template #right-footer>
          <el-button class="transfer-footer" size="small">Operation</el-button>
        </template>
      </el-transfer>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type {
  TransferDirection,
  TransferKey,
  renderContent,
} from 'element-plus'

interface Option {
  key: number
  label: string
  disabled: boolean
}

const generateData = (): Option[] => {
  const data: Option[] = []
  for (let i = 1; i <= 15; i++) {
    data.push({
      key: i,
      label: `Option ${i}`,
      disabled: i % 4 === 0,
    })
  }
  return data
}

const data = ref(generateData())
const rightValue = ref([1])
const leftValue = ref([1])

const renderFunc: renderContent = (h, option) => h('span', null, option.label)

const handleChange = (
  value: TransferKey[],
  direction: TransferDirection,
  movedKeys: TransferKey[]
) => {
  console.log(value, direction, movedKeys)
}
</script>

<style>
.transfer-footer {
  margin-left: 15px;
  padding: 6px 5px;
}
</style>
```

Example 4 (typescript):
```typescript
<template>
  <el-transfer v-model="value" :data="data">
    <template #left-empty>
      <el-empty :image-size="60" description="No data" />
    </template>
    <template #right-empty>
      <el-empty :image-size="60" description="No data" />
    </template>
  </el-transfer>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

interface DataItem {
  key: number
  label: string
  disabled: boolean
}
const generateData = (): DataItem[] => {
  const data: DataItem[] = []
  for (let i = 1; i <= 15; i++) {
    data.push({
      key: i,
      label: `Option ${i}`,
      disabled: i % 4 === 0,
    })
  }
  return data
}

const data = ref(generateData())
const value = ref([])
</script>
```

---
