---
name: "upload"
description: "Upload 上传 -- Element Plus Vue3 桌面端组件。Invoke when user needs Upload 上传 in Vue 3.x project."
url: "https://element-plus.org/zh-CN/component/upload.html"
---

---

# Upload 上传 [​](#upload-上传)

更新日志待解决

11

通过点击或者拖拽上传文件。

## 基础用法 [​](#基础用法)

通过 `slot` 你可以传入自定义的上传按钮类型和文字提示。 可通过设置 `limit` 和 `on-exceed` 来限制上传文件的个数和定义超出限制时的行为。 可通过设置 `before-remove` 来阻止文件移除操作。

Click to upload

jpg/png files with a size less than 500KB.

-   element-plus-logo.svg

    _press delete to remove_
-   element-plus-logo2.svg

    _press delete to remove_

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdXBsb2FkXG4gICAgdi1tb2RlbDpmaWxlLWxpc3Q9XCJmaWxlTGlzdFwiXG4gICAgY2xhc3M9XCJ1cGxvYWQtZGVtb1wiXG4gICAgYWN0aW9uPVwiaHR0cHM6Ly9ydW4ubW9ja3kuaW8vdjMvOWQwNTliZjktNDY2MC00NWYyLTkyNWQtY2U4MGFkNmM0ZDE1XCJcbiAgICBtdWx0aXBsZVxuICAgIDpvbi1wcmV2aWV3PVwiaGFuZGxlUHJldmlld1wiXG4gICAgOm9uLXJlbW92ZT1cImhhbmRsZVJlbW92ZVwiXG4gICAgOmJlZm9yZS1yZW1vdmU9XCJiZWZvcmVSZW1vdmVcIlxuICAgIDpsaW1pdD1cIjNcIlxuICAgIDpvbi1leGNlZWQ9XCJoYW5kbGVFeGNlZWRcIlxuICA+XG4gICAgPGVsLWJ1dHRvbiB0eXBlPVwicHJpbWFyeVwiPkNsaWNrIHRvIHVwbG9hZDwvZWwtYnV0dG9uPlxuICAgIDx0ZW1wbGF0ZSAjdGlwPlxuICAgICAgPGRpdiBjbGFzcz1cImVsLXVwbG9hZF9fdGlwXCI+XG4gICAgICAgIGpwZy9wbmcgZmlsZXMgd2l0aCBhIHNpemUgbGVzcyB0aGFuIDUwMEtCLlxuICAgICAgPC9kaXY+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC11cGxvYWQ+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgRWxNZXNzYWdlLCBFbE1lc3NhZ2VCb3ggfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmltcG9ydCB0eXBlIHsgVXBsb2FkUHJvcHMsIFVwbG9hZFVzZXJGaWxlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBmaWxlTGlzdCA9IHJlZjxVcGxvYWRVc2VyRmlsZVtdPihbXG4gIHtcbiAgICBuYW1lOiAnZWxlbWVudC1wbHVzLWxvZ28uc3ZnJyxcbiAgICB1cmw6ICdodHRwczovL2VsZW1lbnQtcGx1cy5vcmcvaW1hZ2VzL2VsZW1lbnQtcGx1cy1sb2dvLnN2ZycsXG4gIH0sXG4gIHtcbiAgICBuYW1lOiAnZWxlbWVudC1wbHVzLWxvZ28yLnN2ZycsXG4gICAgdXJsOiAnaHR0cHM6Ly9lbGVtZW50LXBsdXMub3JnL2ltYWdlcy9lbGVtZW50LXBsdXMtbG9nby5zdmcnLFxuICB9LFxuXSlcblxuY29uc3QgaGFuZGxlUmVtb3ZlOiBVcGxvYWRQcm9wc1snb25SZW1vdmUnXSA9IChmaWxlLCB1cGxvYWRGaWxlcykgPT4ge1xuICBjb25zb2xlLmxvZyhmaWxlLCB1cGxvYWRGaWxlcylcbn1cblxuY29uc3QgaGFuZGxlUHJldmlldzogVXBsb2FkUHJvcHNbJ29uUHJldmlldyddID0gKHVwbG9hZEZpbGUpID0+IHtcbiAgY29uc29sZS5sb2codXBsb2FkRmlsZSlcbn1cblxuY29uc3QgaGFuZGxlRXhjZWVkOiBVcGxvYWRQcm9wc1snb25FeGNlZWQnXSA9IChmaWxlcywgdXBsb2FkRmlsZXMpID0+IHtcbiAgRWxNZXNzYWdlLndhcm5pbmcoXG4gICAgYFRoZSBsaW1pdCBpcyAzLCB5b3Ugc2VsZWN0ZWQgJHtmaWxlcy5sZW5ndGh9IGZpbGVzIHRoaXMgdGltZSwgYWRkIHVwIHRvICR7XG4gICAgICBmaWxlcy5sZW5ndGggKyB1cGxvYWRGaWxlcy5sZW5ndGhcbiAgICB9IHRvdGFsbHlgXG4gIClcbn1cblxuY29uc3QgYmVmb3JlUmVtb3ZlOiBVcGxvYWRQcm9wc1snYmVmb3JlUmVtb3ZlJ10gPSAodXBsb2FkRmlsZSwgdXBsb2FkRmlsZXMpID0+IHtcbiAgcmV0dXJuIEVsTWVzc2FnZUJveC5jb25maXJtKFxuICAgIGBDYW5jZWwgdGhlIHRyYW5zZmVyIG9mICR7dXBsb2FkRmlsZS5uYW1lfSA/YFxuICApLnRoZW4oXG4gICAgKCkgPT4gdHJ1ZSxcbiAgICAoKSA9PiBmYWxzZVxuICApXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/upload/basic.vue)_

vue

```
<template>
  <el-upload
    v-model:file-list="fileList"
    class="upload-demo"
    action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
    multiple
    :on-preview="handlePreview"
    :on-remove="handleRemove"
    :before-remove="beforeRemove"
    :limit="3"
    :on-exceed="handleExceed"
  >
    <el-button type="primary">Click to upload</el-button>
    <template #tip>
      <div class="el-upload__tip">
        jpg/png files with a size less than 500KB.
      </div>
    </template>
  </el-upload>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

import type { UploadProps, UploadUserFile } from 'element-plus'

const fileList = ref<UploadUserFile[]>([
  {
    name: 'element-plus-logo.svg',
    url: 'https://element-plus.org/images/element-plus-logo.svg',
  },
  {
    name: 'element-plus-logo2.svg',
    url: 'https://element-plus.org/images/element-plus-logo.svg',
  },
])

const handleRemove: UploadProps['onRemove'] = (file, uploadFiles) => {
  console.log(file, uploadFiles)
}

const handlePreview: UploadProps['onPreview'] = (uploadFile) => {
  console.log(uploadFile)
}

const handleExceed: UploadProps['onExceed'] = (files, uploadFiles) => {
  ElMessage.warning(
    `The limit is 3, you selected ${files.length} files this time, add up to ${
      files.length + uploadFiles.length
    } totally`
  )
}

const beforeRemove: UploadProps['beforeRemove'] = (uploadFile, uploadFiles) => {
  return ElMessageBox.confirm(
    `Cancel the transfer of ${uploadFile.name} ?`
  ).then(
    () => true,
    () => false
  )
}
</script>
```

隐藏源代码

## 覆盖前一个文件 [​](#覆盖前一个文件)

设置 `limit` 和 `on-exceed` 可以在选中时自动替换上一个文件。

select file

upload to server

limit 1 file, new file will cover the old file

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdXBsb2FkXG4gICAgcmVmPVwidXBsb2FkXCJcbiAgICBjbGFzcz1cInVwbG9hZC1kZW1vXCJcbiAgICBhY3Rpb249XCJodHRwczovL3J1bi5tb2NreS5pby92My85ZDA1OWJmOS00NjYwLTQ1ZjItOTI1ZC1jZTgwYWQ2YzRkMTVcIlxuICAgIDpsaW1pdD1cIjFcIlxuICAgIDpvbi1leGNlZWQ9XCJoYW5kbGVFeGNlZWRcIlxuICAgIDphdXRvLXVwbG9hZD1cImZhbHNlXCJcbiAgPlxuICAgIDx0ZW1wbGF0ZSAjdHJpZ2dlcj5cbiAgICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIj5zZWxlY3QgZmlsZTwvZWwtYnV0dG9uPlxuICAgIDwvdGVtcGxhdGU+XG4gICAgPGVsLWJ1dHRvbiBjbGFzcz1cIm1sLTNcIiB0eXBlPVwic3VjY2Vzc1wiIEBjbGljaz1cInN1Ym1pdFVwbG9hZFwiPlxuICAgICAgdXBsb2FkIHRvIHNlcnZlclxuICAgIDwvZWwtYnV0dG9uPlxuICAgIDx0ZW1wbGF0ZSAjdGlwPlxuICAgICAgPGRpdiBjbGFzcz1cImVsLXVwbG9hZF9fdGlwIHRleHQtcmVkXCI+XG4gICAgICAgIGxpbWl0IDEgZmlsZSwgbmV3IGZpbGUgd2lsbCBjb3ZlciB0aGUgb2xkIGZpbGVcbiAgICAgIDwvZGl2PlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtdXBsb2FkPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IGdlbkZpbGVJZCB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuaW1wb3J0IHR5cGUgeyBVcGxvYWRJbnN0YW5jZSwgVXBsb2FkUHJvcHMsIFVwbG9hZFJhd0ZpbGUgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IHVwbG9hZCA9IHJlZjxVcGxvYWRJbnN0YW5jZT4oKVxuXG5jb25zdCBoYW5kbGVFeGNlZWQ6IFVwbG9hZFByb3BzWydvbkV4Y2VlZCddID0gKGZpbGVzKSA9PiB7XG4gIHVwbG9hZC52YWx1ZSEuY2xlYXJGaWxlcygpXG4gIGNvbnN0IGZpbGUgPSBmaWxlc1swXSBhcyBVcGxvYWRSYXdGaWxlXG4gIGZpbGUudWlkID0gZ2VuRmlsZUlkKClcbiAgdXBsb2FkLnZhbHVlIS5oYW5kbGVTdGFydChmaWxlKVxufVxuXG5jb25zdCBzdWJtaXRVcGxvYWQgPSAoKSA9PiB7XG4gIHVwbG9hZC52YWx1ZSEuc3VibWl0KClcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/upload/limit-cover.vue)_

vue

```
<template>
  <el-upload
    ref="upload"
    class="upload-demo"
    action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
    :limit="1"
    :on-exceed="handleExceed"
    :auto-upload="false"
  >
    <template #trigger>
      <el-button type="primary">select file</el-button>
    </template>
    <el-button class="ml-3" type="success" @click="submitUpload">
      upload to server
    </el-button>
    <template #tip>
      <div class="el-upload__tip text-red">
        limit 1 file, new file will cover the old file
      </div>
    </template>
  </el-upload>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { genFileId } from 'element-plus'

import type { UploadInstance, UploadProps, UploadRawFile } from 'element-plus'

const upload = ref<UploadInstance>()

const handleExceed: UploadProps['onExceed'] = (files) => {
  upload.value!.clearFiles()
  const file = files[0] as UploadRawFile
  file.uid = genFileId()
  upload.value!.handleStart(file)
}

const submitUpload = () => {
  upload.value!.submit()
}
</script>
```

隐藏源代码

## 用户头像 [​](#用户头像)

在 `before-upload` 钩子中限制用户上传文件的格式和大小。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdXBsb2FkXG4gICAgY2xhc3M9XCJhdmF0YXItdXBsb2FkZXJcIlxuICAgIGFjdGlvbj1cImh0dHBzOi8vcnVuLm1vY2t5LmlvL3YzLzlkMDU5YmY5LTQ2NjAtNDVmMi05MjVkLWNlODBhZDZjNGQxNVwiXG4gICAgOnNob3ctZmlsZS1saXN0PVwiZmFsc2VcIlxuICAgIDpvbi1zdWNjZXNzPVwiaGFuZGxlQXZhdGFyU3VjY2Vzc1wiXG4gICAgOmJlZm9yZS11cGxvYWQ9XCJiZWZvcmVBdmF0YXJVcGxvYWRcIlxuICA+XG4gICAgPGltZyB2LWlmPVwiaW1hZ2VVcmxcIiA6c3JjPVwiaW1hZ2VVcmxcIiBjbGFzcz1cImF2YXRhclwiIC8+XG4gICAgPGVsLWljb24gdi1lbHNlIGNsYXNzPVwiYXZhdGFyLXVwbG9hZGVyLWljb25cIj48UGx1cyAvPjwvZWwtaWNvbj5cbiAgPC9lbC11cGxvYWQ+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgRWxNZXNzYWdlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuaW1wb3J0IHsgUGx1cyB9IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuXG5pbXBvcnQgdHlwZSB7IFVwbG9hZFByb3BzIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBpbWFnZVVybCA9IHJlZignJylcblxuY29uc3QgaGFuZGxlQXZhdGFyU3VjY2VzczogVXBsb2FkUHJvcHNbJ29uU3VjY2VzcyddID0gKFxuICByZXNwb25zZSxcbiAgdXBsb2FkRmlsZVxuKSA9PiB7XG4gIGltYWdlVXJsLnZhbHVlID0gVVJMLmNyZWF0ZU9iamVjdFVSTCh1cGxvYWRGaWxlLnJhdyEpXG59XG5cbmNvbnN0IGJlZm9yZUF2YXRhclVwbG9hZDogVXBsb2FkUHJvcHNbJ2JlZm9yZVVwbG9hZCddID0gKHJhd0ZpbGUpID0+IHtcbiAgaWYgKHJhd0ZpbGUudHlwZSAhPT0gJ2ltYWdlL2pwZWcnKSB7XG4gICAgRWxNZXNzYWdlLmVycm9yKCdBdmF0YXIgcGljdHVyZSBtdXN0IGJlIEpQRyBmb3JtYXQhJylcbiAgICByZXR1cm4gZmFsc2VcbiAgfSBlbHNlIGlmIChyYXdGaWxlLnNpemUgLyAxMDI0IC8gMTAyNCA+IDIpIHtcbiAgICBFbE1lc3NhZ2UuZXJyb3IoJ0F2YXRhciBwaWN0dXJlIHNpemUgY2FuIG5vdCBleGNlZWQgMk1CIScpXG4gICAgcmV0dXJuIGZhbHNlXG4gIH1cbiAgcmV0dXJuIHRydWVcbn1cbjwvc2NyaXB0PlxuXG48c3R5bGUgc2NvcGVkPlxuLmF2YXRhci11cGxvYWRlciAuYXZhdGFyIHtcbiAgd2lkdGg6IDE3OHB4O1xuICBoZWlnaHQ6IDE3OHB4O1xuICBkaXNwbGF5OiBibG9jaztcbn1cbjwvc3R5bGU+XG5cbjxzdHlsZT5cbi5hdmF0YXItdXBsb2FkZXIgLmVsLXVwbG9hZCB7XG4gIGJvcmRlcjogMXB4IGRhc2hlZCB2YXIoLS1lbC1ib3JkZXItY29sb3IpO1xuICBib3JkZXItcmFkaXVzOiA2cHg7XG4gIGN1cnNvcjogcG9pbnRlcjtcbiAgcG9zaXRpb246IHJlbGF0aXZlO1xuICBvdmVyZmxvdzogaGlkZGVuO1xuICB0cmFuc2l0aW9uOiB2YXIoLS1lbC10cmFuc2l0aW9uLWR1cmF0aW9uLWZhc3QpO1xufVxuXG4uYXZhdGFyLXVwbG9hZGVyIC5lbC11cGxvYWQ6aG92ZXIge1xuICBib3JkZXItY29sb3I6IHZhcigtLWVsLWNvbG9yLXByaW1hcnkpO1xufVxuXG4uZWwtaWNvbi5hdmF0YXItdXBsb2FkZXItaWNvbiB7XG4gIGZvbnQtc2l6ZTogMjhweDtcbiAgY29sb3I6ICM4YzkzOWQ7XG4gIHdpZHRoOiAxNzhweDtcbiAgaGVpZ2h0OiAxNzhweDtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xufVxuPC9zdHlsZT5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/upload/avatar.vue)_

vue

```
<template>
  <el-upload
    class="avatar-uploader"
    action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
    :show-file-list="false"
    :on-success="handleAvatarSuccess"
    :before-upload="beforeAvatarUpload"
  >
    <img v-if="imageUrl" :src="imageUrl" class="avatar" />
    <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
  </el-upload>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

import type { UploadProps } from 'element-plus'

const imageUrl = ref('')

const handleAvatarSuccess: UploadProps['onSuccess'] = (
  response,
  uploadFile
) => {
  imageUrl.value = URL.createObjectURL(uploadFile.raw!)
}

const beforeAvatarUpload: UploadProps['beforeUpload'] = (rawFile) => {
  if (rawFile.type !== 'image/jpeg') {
    ElMessage.error('Avatar picture must be JPG format!')
    return false
  } else if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('Avatar picture size can not exceed 2MB!')
    return false
  }
  return true
}
</script>

<style scoped>
.avatar-uploader .avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}
</style>
```

隐藏源代码

## 照片墙 [​](#照片墙)

使用 `list-type` 属性来设定文件列表的样式。

-   ![](https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100)_press delete to remove_
-   ![](https://element-plus.org/images/plant-1.png)_press delete to remove_
-   ![](https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100)_press delete to remove_
-   ![](https://element-plus.org/images/plant-2.png)_press delete to remove_
-   ![](https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100)_press delete to remove_
-   ![](https://element-plus.org/images/figure-1.png)_press delete to remove_
-   ![](https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100)_press delete to remove_
-   ![](https://element-plus.org/images/figure-2.png)_press delete to remove_

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdXBsb2FkXG4gICAgdi1tb2RlbDpmaWxlLWxpc3Q9XCJmaWxlTGlzdFwiXG4gICAgYWN0aW9uPVwiaHR0cHM6Ly9ydW4ubW9ja3kuaW8vdjMvOWQwNTliZjktNDY2MC00NWYyLTkyNWQtY2U4MGFkNmM0ZDE1XCJcbiAgICBsaXN0LXR5cGU9XCJwaWN0dXJlLWNhcmRcIlxuICAgIDpvbi1wcmV2aWV3PVwiaGFuZGxlUGljdHVyZUNhcmRQcmV2aWV3XCJcbiAgICA6b24tcmVtb3ZlPVwiaGFuZGxlUmVtb3ZlXCJcbiAgPlxuICAgIDxlbC1pY29uPjxQbHVzIC8+PC9lbC1pY29uPlxuICA8L2VsLXVwbG9hZD5cblxuICA8ZWwtZGlhbG9nIHYtbW9kZWw9XCJkaWFsb2dWaXNpYmxlXCI+XG4gICAgPGltZyB3LWZ1bGwgOnNyYz1cImRpYWxvZ0ltYWdlVXJsXCIgYWx0PVwiUHJldmlldyBJbWFnZVwiIC8+XG4gIDwvZWwtZGlhbG9nPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBsYW5nPVwidHNcIiBzZXR1cD5cbmltcG9ydCB7IHJlZiB9IGZyb20gJ3Z1ZSdcbmltcG9ydCB7IFBsdXMgfSBmcm9tICdAZWxlbWVudC1wbHVzL2ljb25zLXZ1ZSdcblxuaW1wb3J0IHR5cGUgeyBVcGxvYWRQcm9wcywgVXBsb2FkVXNlckZpbGUgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IGZpbGVMaXN0ID0gcmVmPFVwbG9hZFVzZXJGaWxlW10+KFtcbiAge1xuICAgIG5hbWU6ICdmb29kLmpwZWcnLFxuICAgIHVybDogJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS8zLzYzLzRlN2YzYTE1NDI5YmZkYTk5YmNlNDJhMThjZGQxanBlZy5qcGVnP2ltYWdlTW9ncjIvdGh1bWJuYWlsLzM2MHgzNjAvZm9ybWF0L3dlYnAvcXVhbGl0eS8xMDAnLFxuICB9LFxuICB7XG4gICAgbmFtZTogJ3BsYW50LTEucG5nJyxcbiAgICB1cmw6ICcvaW1hZ2VzL3BsYW50LTEucG5nJyxcbiAgfSxcbiAge1xuICAgIG5hbWU6ICdmb29kLmpwZWcnLFxuICAgIHVybDogJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS8zLzYzLzRlN2YzYTE1NDI5YmZkYTk5YmNlNDJhMThjZGQxanBlZy5qcGVnP2ltYWdlTW9ncjIvdGh1bWJuYWlsLzM2MHgzNjAvZm9ybWF0L3dlYnAvcXVhbGl0eS8xMDAnLFxuICB9LFxuICB7XG4gICAgbmFtZTogJ3BsYW50LTIucG5nJyxcbiAgICB1cmw6ICcvaW1hZ2VzL3BsYW50LTIucG5nJyxcbiAgfSxcbiAge1xuICAgIG5hbWU6ICdmb29kLmpwZWcnLFxuICAgIHVybDogJ2h0dHBzOi8vZnVzczEwLmVsZW1lY2RuLmNvbS8zLzYzLzRlN2YzYTE1NDI5YmZkYTk5YmNlNDJhMThjZGQxanBlZy5qcGVnP2ltYWdlTW9ncjIvdGh1bWJuYWlsLzM2MHgzNjAvZm9ybWF0L3dlYnAvcXVhbGl0eS8xMDAnLFxuICB9LFxuICB7XG4gICAgbmFtZTogJ2ZpZ3VyZS0xLnBuZycsXG4gICAgdXJsOiAnL2ltYWdlcy9maWd1cmUtMS5wbmcnLFxuICB9LFxuICB7XG4gICAgbmFtZTogJ2Zvb2QuanBlZycsXG4gICAgdXJsOiAnaHR0cHM6Ly9mdXNzMTAuZWxlbWVjZG4uY29tLzMvNjMvNGU3ZjNhMTU0MjliZmRhOTliY2U0MmExOGNkZDFqcGVnLmpwZWc/aW1hZ2VNb2dyMi90aHVtYm5haWwvMzYweDM2MC9mb3JtYXQvd2VicC9xdWFsaXR5LzEwMCcsXG4gIH0sXG4gIHtcbiAgICBuYW1lOiAnZmlndXJlLTIucG5nJyxcbiAgICB1cmw6ICcvaW1hZ2VzL2ZpZ3VyZS0yLnBuZycsXG4gIH0sXG5dKVxuXG5jb25zdCBkaWFsb2dJbWFnZVVybCA9IHJlZignJylcbmNvbnN0IGRpYWxvZ1Zpc2libGUgPSByZWYoZmFsc2UpXG5cbmNvbnN0IGhhbmRsZVJlbW92ZTogVXBsb2FkUHJvcHNbJ29uUmVtb3ZlJ10gPSAodXBsb2FkRmlsZSwgdXBsb2FkRmlsZXMpID0+IHtcbiAgY29uc29sZS5sb2codXBsb2FkRmlsZSwgdXBsb2FkRmlsZXMpXG59XG5cbmNvbnN0IGhhbmRsZVBpY3R1cmVDYXJkUHJldmlldzogVXBsb2FkUHJvcHNbJ29uUHJldmlldyddID0gKHVwbG9hZEZpbGUpID0+IHtcbiAgZGlhbG9nSW1hZ2VVcmwudmFsdWUgPSB1cGxvYWRGaWxlLnVybCFcbiAgZGlhbG9nVmlzaWJsZS52YWx1ZSA9IHRydWVcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/upload/photo-wall.vue)_

vue

```
<template>
  <el-upload
    v-model:file-list="fileList"
    action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
    list-type="picture-card"
    :on-preview="handlePictureCardPreview"
    :on-remove="handleRemove"
  >
    <el-icon><Plus /></el-icon>
  </el-upload>

  <el-dialog v-model="dialogVisible">
    <img w-full :src="dialogImageUrl" alt="Preview Image" />
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'

import type { UploadProps, UploadUserFile } from 'element-plus'

const fileList = ref<UploadUserFile[]>([
  {
    name: 'food.jpeg',
    url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100',
  },
  {
    name: 'plant-1.png',
    url: '/images/plant-1.png',
  },
  {
    name: 'food.jpeg',
    url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100',
  },
  {
    name: 'plant-2.png',
    url: '/images/plant-2.png',
  },
  {
    name: 'food.jpeg',
    url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100',
  },
  {
    name: 'figure-1.png',
    url: '/images/figure-1.png',
  },
  {
    name: 'food.jpeg',
    url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100',
  },
  {
    name: 'figure-2.png',
    url: '/images/figure-2.png',
  },
])

const dialogImageUrl = ref('')
const dialogVisible = ref(false)

const handleRemove: UploadProps['onRemove'] = (uploadFile, uploadFiles) => {
  console.log(uploadFile, uploadFiles)
}

const handlePictureCardPreview: UploadProps['onPreview'] = (uploadFile) => {
  dialogImageUrl.value = uploadFile.url!
  dialogVisible.value = true
}
</script>
```

隐藏源代码

## 自定义缩略图 [​](#自定义缩略图)

使用 `scoped-slot` 属性来改变默认的缩略图模板样式。

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdXBsb2FkIGFjdGlvbj1cIiNcIiBsaXN0LXR5cGU9XCJwaWN0dXJlLWNhcmRcIiA6YXV0by11cGxvYWQ9XCJmYWxzZVwiPlxuICAgIDxlbC1pY29uPjxQbHVzIC8+PC9lbC1pY29uPlxuXG4gICAgPHRlbXBsYXRlICNmaWxlPVwieyBmaWxlIH1cIj5cbiAgICAgIDxkaXY+XG4gICAgICAgIDxpbWcgY2xhc3M9XCJlbC11cGxvYWQtbGlzdF9faXRlbS10aHVtYm5haWxcIiA6c3JjPVwiZmlsZS51cmxcIiBhbHQ9XCJcIiAvPlxuICAgICAgICA8c3BhbiBjbGFzcz1cImVsLXVwbG9hZC1saXN0X19pdGVtLWFjdGlvbnNcIj5cbiAgICAgICAgICA8c3BhblxuICAgICAgICAgICAgY2xhc3M9XCJlbC11cGxvYWQtbGlzdF9faXRlbS1wcmV2aWV3XCJcbiAgICAgICAgICAgIEBjbGljaz1cImhhbmRsZVBpY3R1cmVDYXJkUHJldmlldyhmaWxlKVwiXG4gICAgICAgICAgPlxuICAgICAgICAgICAgPGVsLWljb24+PHpvb20taW4gLz48L2VsLWljb24+XG4gICAgICAgICAgPC9zcGFuPlxuICAgICAgICAgIDxzcGFuXG4gICAgICAgICAgICB2LWlmPVwiIWRpc2FibGVkXCJcbiAgICAgICAgICAgIGNsYXNzPVwiZWwtdXBsb2FkLWxpc3RfX2l0ZW0tZGVsZXRlXCJcbiAgICAgICAgICAgIEBjbGljaz1cImhhbmRsZURvd25sb2FkKGZpbGUpXCJcbiAgICAgICAgICA+XG4gICAgICAgICAgICA8ZWwtaWNvbj48RG93bmxvYWQgLz48L2VsLWljb24+XG4gICAgICAgICAgPC9zcGFuPlxuICAgICAgICAgIDxzcGFuXG4gICAgICAgICAgICB2LWlmPVwiIWRpc2FibGVkXCJcbiAgICAgICAgICAgIGNsYXNzPVwiZWwtdXBsb2FkLWxpc3RfX2l0ZW0tZGVsZXRlXCJcbiAgICAgICAgICAgIEBjbGljaz1cImhhbmRsZVJlbW92ZShmaWxlKVwiXG4gICAgICAgICAgPlxuICAgICAgICAgICAgPGVsLWljb24+PERlbGV0ZSAvPjwvZWwtaWNvbj5cbiAgICAgICAgICA8L3NwYW4+XG4gICAgICAgIDwvc3Bhbj5cbiAgICAgIDwvZGl2PlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtdXBsb2FkPlxuXG4gIDxlbC1kaWFsb2cgdi1tb2RlbD1cImRpYWxvZ1Zpc2libGVcIj5cbiAgICA8aW1nIHctZnVsbCA6c3JjPVwiZGlhbG9nSW1hZ2VVcmxcIiBhbHQ9XCJQcmV2aWV3IEltYWdlXCIgLz5cbiAgPC9lbC1kaWFsb2c+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuaW1wb3J0IHsgRGVsZXRlLCBEb3dubG9hZCwgUGx1cywgWm9vbUluIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG5cbmltcG9ydCB0eXBlIHsgVXBsb2FkRmlsZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgZGlhbG9nSW1hZ2VVcmwgPSByZWYoJycpXG5jb25zdCBkaWFsb2dWaXNpYmxlID0gcmVmKGZhbHNlKVxuY29uc3QgZGlzYWJsZWQgPSByZWYoZmFsc2UpXG5cbmNvbnN0IGhhbmRsZVJlbW92ZSA9IChmaWxlOiBVcGxvYWRGaWxlKSA9PiB7XG4gIGNvbnNvbGUubG9nKGZpbGUpXG59XG5cbmNvbnN0IGhhbmRsZVBpY3R1cmVDYXJkUHJldmlldyA9IChmaWxlOiBVcGxvYWRGaWxlKSA9PiB7XG4gIGRpYWxvZ0ltYWdlVXJsLnZhbHVlID0gZmlsZS51cmwhXG4gIGRpYWxvZ1Zpc2libGUudmFsdWUgPSB0cnVlXG59XG5cbmNvbnN0IGhhbmRsZURvd25sb2FkID0gKGZpbGU6IFVwbG9hZEZpbGUpID0+IHtcbiAgY29uc29sZS5sb2coZmlsZSlcbn1cbjwvc2NyaXB0PlxuIn0=)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/upload/custom-thumbnail.vue)_

vue

```
<template>
  <el-upload action="#" list-type="picture-card" :auto-upload="false">
    <el-icon><Plus /></el-icon>

    <template #file="{ file }">
      <div>
        <img class="el-upload-list__item-thumbnail" :src="file.url" alt="" />
        <span class="el-upload-list__item-actions">
          <span
            class="el-upload-list__item-preview"
            @click="handlePictureCardPreview(file)"
          >
            <el-icon><zoom-in /></el-icon>
          </span>
          <span
            v-if="!disabled"
            class="el-upload-list__item-delete"
            @click="handleDownload(file)"
          >
            <el-icon><Download /></el-icon>
          </span>
          <span
            v-if="!disabled"
            class="el-upload-list__item-delete"
            @click="handleRemove(file)"
          >
            <el-icon><Delete /></el-icon>
          </span>
        </span>
      </div>
    </template>
  </el-upload>

  <el-dialog v-model="dialogVisible">
    <img w-full :src="dialogImageUrl" alt="Preview Image" />
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { Delete, Download, Plus, ZoomIn } from '@element-plus/icons-vue'

import type { UploadFile } from 'element-plus'

const dialogImageUrl = ref('')
const dialogVisible = ref(false)
const disabled = ref(false)

const handleRemove = (file: UploadFile) => {
  console.log(file)
}

const handlePictureCardPreview = (file: UploadFile) => {
  dialogImageUrl.value = file.url!
  dialogVisible.value = true
}

const handleDownload = (file: UploadFile) => {
  console.log(file)
}
</script>
```

隐藏源代码

## 图片列表缩略图 [​](#图片列表缩略图)

Click to upload

jpg/png files with a size less than 500kb

-   ![](https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100)

    food.jpeg

    _press delete to remove_
-   ![](https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100)

    food2.jpeg

    _press delete to remove_

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdXBsb2FkXG4gICAgdi1tb2RlbDpmaWxlLWxpc3Q9XCJmaWxlTGlzdFwiXG4gICAgY2xhc3M9XCJ1cGxvYWQtZGVtb1wiXG4gICAgYWN0aW9uPVwiaHR0cHM6Ly9ydW4ubW9ja3kuaW8vdjMvOWQwNTliZjktNDY2MC00NWYyLTkyNWQtY2U4MGFkNmM0ZDE1XCJcbiAgICA6b24tcHJldmlldz1cImhhbmRsZVByZXZpZXdcIlxuICAgIDpvbi1yZW1vdmU9XCJoYW5kbGVSZW1vdmVcIlxuICAgIGxpc3QtdHlwZT1cInBpY3R1cmVcIlxuICA+XG4gICAgPGVsLWJ1dHRvbiB0eXBlPVwicHJpbWFyeVwiPkNsaWNrIHRvIHVwbG9hZDwvZWwtYnV0dG9uPlxuICAgIDx0ZW1wbGF0ZSAjdGlwPlxuICAgICAgPGRpdiBjbGFzcz1cImVsLXVwbG9hZF9fdGlwXCI+XG4gICAgICAgIGpwZy9wbmcgZmlsZXMgd2l0aCBhIHNpemUgbGVzcyB0aGFuIDUwMGtiXG4gICAgICA8L2Rpdj5cbiAgICA8L3RlbXBsYXRlPlxuICA8L2VsLXVwbG9hZD5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQgbGFuZz1cInRzXCIgc2V0dXA+XG5pbXBvcnQgeyByZWYgfSBmcm9tICd2dWUnXG5cbmltcG9ydCB0eXBlIHsgVXBsb2FkUHJvcHMsIFVwbG9hZFVzZXJGaWxlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCBmaWxlTGlzdCA9IHJlZjxVcGxvYWRVc2VyRmlsZVtdPihbXG4gIHtcbiAgICBuYW1lOiAnZm9vZC5qcGVnJyxcbiAgICB1cmw6ICdodHRwczovL2Z1c3MxMC5lbGVtZWNkbi5jb20vMy82My80ZTdmM2ExNTQyOWJmZGE5OWJjZTQyYTE4Y2RkMWpwZWcuanBlZz9pbWFnZU1vZ3IyL3RodW1ibmFpbC8zNjB4MzYwL2Zvcm1hdC93ZWJwL3F1YWxpdHkvMTAwJyxcbiAgfSxcbiAge1xuICAgIG5hbWU6ICdmb29kMi5qcGVnJyxcbiAgICB1cmw6ICdodHRwczovL2Z1c3MxMC5lbGVtZWNkbi5jb20vMy82My80ZTdmM2ExNTQyOWJmZGE5OWJjZTQyYTE4Y2RkMWpwZWcuanBlZz9pbWFnZU1vZ3IyL3RodW1ibmFpbC8zNjB4MzYwL2Zvcm1hdC93ZWJwL3F1YWxpdHkvMTAwJyxcbiAgfSxcbl0pXG5cbmNvbnN0IGhhbmRsZVJlbW92ZTogVXBsb2FkUHJvcHNbJ29uUmVtb3ZlJ10gPSAodXBsb2FkRmlsZSwgdXBsb2FkRmlsZXMpID0+IHtcbiAgY29uc29sZS5sb2codXBsb2FkRmlsZSwgdXBsb2FkRmlsZXMpXG59XG5cbmNvbnN0IGhhbmRsZVByZXZpZXc6IFVwbG9hZFByb3BzWydvblByZXZpZXcnXSA9IChmaWxlKSA9PiB7XG4gIGNvbnNvbGUubG9nKGZpbGUpXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/upload/file-list-with-thumbnail.vue)_

vue

```
<template>
  <el-upload
    v-model:file-list="fileList"
    class="upload-demo"
    action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
    :on-preview="handlePreview"
    :on-remove="handleRemove"
    list-type="picture"
  >
    <el-button type="primary">Click to upload</el-button>
    <template #tip>
      <div class="el-upload__tip">
        jpg/png files with a size less than 500kb
      </div>
    </template>
  </el-upload>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { UploadProps, UploadUserFile } from 'element-plus'

const fileList = ref<UploadUserFile[]>([
  {
    name: 'food.jpeg',
    url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100',
  },
  {
    name: 'food2.jpeg',
    url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100',
  },
])

const handleRemove: UploadProps['onRemove'] = (uploadFile, uploadFiles) => {
  console.log(uploadFile, uploadFiles)
}

const handlePreview: UploadProps['onPreview'] = (file) => {
  console.log(file)
}
</script>
```

隐藏源代码

## 上传文件列表控制 [​](#上传文件列表控制)

通过 `on-change` 钩子函数来对上传文件的列表进行控制。

Click to upload

jpg/png files with a size less than 500kb

-   food.jpeg

    _press delete to remove_
-   food2.jpeg

    _press delete to remove_

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdXBsb2FkXG4gICAgdi1tb2RlbDpmaWxlLWxpc3Q9XCJmaWxlTGlzdFwiXG4gICAgY2xhc3M9XCJ1cGxvYWQtZGVtb1wiXG4gICAgYWN0aW9uPVwiaHR0cHM6Ly9ydW4ubW9ja3kuaW8vdjMvOWQwNTliZjktNDY2MC00NWYyLTkyNWQtY2U4MGFkNmM0ZDE1XCJcbiAgICA6b24tY2hhbmdlPVwiaGFuZGxlQ2hhbmdlXCJcbiAgPlxuICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIj5DbGljayB0byB1cGxvYWQ8L2VsLWJ1dHRvbj5cbiAgICA8dGVtcGxhdGUgI3RpcD5cbiAgICAgIDxkaXYgY2xhc3M9XCJlbC11cGxvYWRfX3RpcFwiPlxuICAgICAgICBqcGcvcG5nIGZpbGVzIHdpdGggYSBzaXplIGxlc3MgdGhhbiA1MDBrYlxuICAgICAgPC9kaXY+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC11cGxvYWQ+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IFVwbG9hZFByb3BzLCBVcGxvYWRVc2VyRmlsZSB9IGZyb20gJ2VsZW1lbnQtcGx1cydcblxuY29uc3QgZmlsZUxpc3QgPSByZWY8VXBsb2FkVXNlckZpbGVbXT4oW1xuICB7XG4gICAgbmFtZTogJ2Zvb2QuanBlZycsXG4gICAgdXJsOiAnaHR0cHM6Ly9mdXNzMTAuZWxlbWVjZG4uY29tLzMvNjMvNGU3ZjNhMTU0MjliZmRhOTliY2U0MmExOGNkZDFqcGVnLmpwZWc/aW1hZ2VNb2dyMi90aHVtYm5haWwvMzYweDM2MC9mb3JtYXQvd2VicC9xdWFsaXR5LzEwMCcsXG4gIH0sXG4gIHtcbiAgICBuYW1lOiAnZm9vZDIuanBlZycsXG4gICAgdXJsOiAnaHR0cHM6Ly9mdXNzMTAuZWxlbWVjZG4uY29tLzMvNjMvNGU3ZjNhMTU0MjliZmRhOTliY2U0MmExOGNkZDFqcGVnLmpwZWc/aW1hZ2VNb2dyMi90aHVtYm5haWwvMzYweDM2MC9mb3JtYXQvd2VicC9xdWFsaXR5LzEwMCcsXG4gIH0sXG5dKVxuXG5jb25zdCBoYW5kbGVDaGFuZ2U6IFVwbG9hZFByb3BzWydvbkNoYW5nZSddID0gKHVwbG9hZEZpbGUsIHVwbG9hZEZpbGVzKSA9PiB7XG4gIGZpbGVMaXN0LnZhbHVlID0gZmlsZUxpc3QudmFsdWUuc2xpY2UoLTMpXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/upload/file-list.vue)_

vue

```
<template>
  <el-upload
    v-model:file-list="fileList"
    class="upload-demo"
    action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
    :on-change="handleChange"
  >
    <el-button type="primary">Click to upload</el-button>
    <template #tip>
      <div class="el-upload__tip">
        jpg/png files with a size less than 500kb
      </div>
    </template>
  </el-upload>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { UploadProps, UploadUserFile } from 'element-plus'

const fileList = ref<UploadUserFile[]>([
  {
    name: 'food.jpeg',
    url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100',
  },
  {
    name: 'food2.jpeg',
    url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100',
  },
])

const handleChange: UploadProps['onChange'] = (uploadFile, uploadFiles) => {
  fileList.value = fileList.value.slice(-3)
}
</script>
```

隐藏源代码

## 拖拽上传 [​](#拖拽上传)

你可以将文件拖拽到特定区域以进行上传。

Drop file here or _click to upload_

jpg/png files with a size less than 500kb

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdXBsb2FkXG4gICAgY2xhc3M9XCJ1cGxvYWQtZGVtb1wiXG4gICAgZHJhZ1xuICAgIGFjdGlvbj1cImh0dHBzOi8vcnVuLm1vY2t5LmlvL3YzLzlkMDU5YmY5LTQ2NjAtNDVmMi05MjVkLWNlODBhZDZjNGQxNVwiXG4gICAgbXVsdGlwbGVcbiAgPlxuICAgIDxlbC1pY29uIGNsYXNzPVwiZWwtaWNvbi0tdXBsb2FkXCI+PHVwbG9hZC1maWxsZWQgLz48L2VsLWljb24+XG4gICAgPGRpdiBjbGFzcz1cImVsLXVwbG9hZF9fdGV4dFwiPlxuICAgICAgRHJvcCBmaWxlIGhlcmUgb3IgPGVtPmNsaWNrIHRvIHVwbG9hZDwvZW0+XG4gICAgPC9kaXY+XG4gICAgPHRlbXBsYXRlICN0aXA+XG4gICAgICA8ZGl2IGNsYXNzPVwiZWwtdXBsb2FkX190aXBcIj5cbiAgICAgICAganBnL3BuZyBmaWxlcyB3aXRoIGEgc2l6ZSBsZXNzIHRoYW4gNTAwa2JcbiAgICAgIDwvZGl2PlxuICAgIDwvdGVtcGxhdGU+XG4gIDwvZWwtdXBsb2FkPlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdCBzZXR1cCBsYW5nPVwidHNcIj5cbmltcG9ydCB7IFVwbG9hZEZpbGxlZCB9IGZyb20gJ0BlbGVtZW50LXBsdXMvaWNvbnMtdnVlJ1xuPC9zY3JpcHQ+XG4ifQ==)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/upload/drag-and-drop.vue)_

vue

```
<template>
  <el-upload
    class="upload-demo"
    drag
    action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
    multiple
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">
      Drop file here or <em>click to upload</em>
    </div>
    <template #tip>
      <div class="el-upload__tip">
        jpg/png files with a size less than 500kb
      </div>
    </template>
  </el-upload>
</template>

<script setup lang="ts">
import { UploadFilled } from '@element-plus/icons-vue'
</script>
```

隐藏源代码

## 上传目录 2.13.1 [​](#上传目录)

通过 `directory` 属性启用文件夹上传。

启用后，只能选择文件夹；选择文件夹后，文件夹内的文件将被扁平化处理。

Drop directory here or _click to upload_

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdXBsb2FkXG4gICAgY2xhc3M9XCJ1cGxvYWQtZGVtb1wiXG4gICAgZHJhZ1xuICAgIGFjdGlvbj1cImh0dHBzOi8vcnVuLm1vY2t5LmlvL3YzLzlkMDU5YmY5LTQ2NjAtNDVmMi05MjVkLWNlODBhZDZjNGQxNVwiXG4gICAgZGlyZWN0b3J5XG4gICAgbXVsdGlwbGVcbiAgICA6b24tY2hhbmdlPVwiaGFuZGxlQ2hhbmdlXCJcbiAgPlxuICAgIDxlbC1pY29uIGNsYXNzPVwiZWwtaWNvbi0tdXBsb2FkXCI+PHVwbG9hZC1maWxsZWQgLz48L2VsLWljb24+XG4gICAgPGRpdiBjbGFzcz1cImVsLXVwbG9hZF9fdGV4dFwiPlxuICAgICAgRHJvcCBkaXJlY3RvcnkgaGVyZSBvciA8ZW0+Y2xpY2sgdG8gdXBsb2FkPC9lbT5cbiAgICA8L2Rpdj5cbiAgPC9lbC11cGxvYWQ+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IHNldHVwIGxhbmc9XCJ0c1wiPlxuaW1wb3J0IHsgVXBsb2FkRmlsbGVkIH0gZnJvbSAnQGVsZW1lbnQtcGx1cy9pY29ucy12dWUnXG5cbmltcG9ydCB0eXBlIHsgVXBsb2FkRmlsZSwgVXBsb2FkRmlsZXMgfSBmcm9tICdlbGVtZW50LXBsdXMnXG5cbmNvbnN0IGhhbmRsZUNoYW5nZSA9ICh1cGxvYWRGaWxlOiBVcGxvYWRGaWxlLCB1cGxvYWRGaWxlczogVXBsb2FkRmlsZXMpID0+IHtcbiAgY29uc29sZS5sb2codXBsb2FkRmlsZSwgdXBsb2FkRmlsZXMpXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/upload/directory.vue)_

vue

```
<template>
  <el-upload
    class="upload-demo"
    drag
    action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
    directory
    multiple
    :on-change="handleChange"
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">
      Drop directory here or <em>click to upload</em>
    </div>
  </el-upload>
</template>

<script setup lang="ts">
import { UploadFilled } from '@element-plus/icons-vue'

import type { UploadFile, UploadFiles } from 'element-plus'

const handleChange = (uploadFile: UploadFile, uploadFiles: UploadFiles) => {
  console.log(uploadFile, uploadFiles)
}
</script>
```

隐藏源代码

## 手动上传 [​](#手动上传)

select file

upload to server

jpg/png files with a size less than 500kb

TS

JS

_[](https://element-plus.run/#eyJBcHAudnVlIjoiPHRlbXBsYXRlPlxuICA8ZWwtdXBsb2FkXG4gICAgcmVmPVwidXBsb2FkUmVmXCJcbiAgICBjbGFzcz1cInVwbG9hZC1kZW1vXCJcbiAgICBhY3Rpb249XCJodHRwczovL3J1bi5tb2NreS5pby92My85ZDA1OWJmOS00NjYwLTQ1ZjItOTI1ZC1jZTgwYWQ2YzRkMTVcIlxuICAgIDphdXRvLXVwbG9hZD1cImZhbHNlXCJcbiAgPlxuICAgIDx0ZW1wbGF0ZSAjdHJpZ2dlcj5cbiAgICAgIDxlbC1idXR0b24gdHlwZT1cInByaW1hcnlcIj5zZWxlY3QgZmlsZTwvZWwtYnV0dG9uPlxuICAgIDwvdGVtcGxhdGU+XG5cbiAgICA8ZWwtYnV0dG9uIGNsYXNzPVwibWwtM1wiIHR5cGU9XCJzdWNjZXNzXCIgQGNsaWNrPVwic3VibWl0VXBsb2FkXCI+XG4gICAgICB1cGxvYWQgdG8gc2VydmVyXG4gICAgPC9lbC1idXR0b24+XG5cbiAgICA8dGVtcGxhdGUgI3RpcD5cbiAgICAgIDxkaXYgY2xhc3M9XCJlbC11cGxvYWRfX3RpcFwiPlxuICAgICAgICBqcGcvcG5nIGZpbGVzIHdpdGggYSBzaXplIGxlc3MgdGhhbiA1MDBrYlxuICAgICAgPC9kaXY+XG4gICAgPC90ZW1wbGF0ZT5cbiAgPC9lbC11cGxvYWQ+XG48L3RlbXBsYXRlPlxuXG48c2NyaXB0IGxhbmc9XCJ0c1wiIHNldHVwPlxuaW1wb3J0IHsgcmVmIH0gZnJvbSAndnVlJ1xuXG5pbXBvcnQgdHlwZSB7IFVwbG9hZEluc3RhbmNlIH0gZnJvbSAnZWxlbWVudC1wbHVzJ1xuXG5jb25zdCB1cGxvYWRSZWYgPSByZWY8VXBsb2FkSW5zdGFuY2U+KClcblxuY29uc3Qgc3VibWl0VXBsb2FkID0gKCkgPT4ge1xuICB1cGxvYWRSZWYudmFsdWUhLnN1Ym1pdCgpXG59XG48L3NjcmlwdD5cbiJ9)__[](https://github.com/element-plus/element-plus/edit/dev/docs/examples/upload/manual.vue)_

vue

```
<template>
  <el-upload
    ref="uploadRef"
    class="upload-demo"
    action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
    :auto-upload="false"
  >
    <template #trigger>
      <el-button type="primary">select file</el-button>
    </template>

    <el-button class="ml-3" type="success" @click="submitUpload">
      upload to server
    </el-button>

    <template #tip>
      <div class="el-upload__tip">
        jpg/png files with a size less than 500kb
      </div>
    </template>
  </el-upload>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

import type { UploadInstance } from 'element-plus'

const uploadRef = ref<UploadInstance>()

const submitUpload = () => {
  uploadRef.value!.submit()
}
</script>
```

隐藏源代码

## API [​](#api)

### 属性 [​](#属性)

| 名称 | 描述 | 类型 | 默认值 |
| --- | --- | --- | --- |
| action required | 请求 URL | `string` | # |
| headers | 设置上传的请求头部 | `object` | — |
| method | 设置上传请求方法 | `string` | post |
| multiple | 是否支持多选文件 | `boolean` | false |
| data | 上传时附带的额外参数 从 v2.3.13 支持 `Awaitable` 数据，和 `Function` | `object` / `Function` | {} |
| name | 上传的文件字段名 | `string` | file |
| with-credentials | 支持发送 cookie 凭证信息 | `boolean` | false |
| show-file-list | 是否显示已上传文件列表 | `boolean` | true |
| drag | 是否启用拖拽上传 | `boolean` | false |
| accept | 接受上传的[文件类型](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#attr-accept)（thumbnail-mode 模式下此参数无效） | `string` | '' |
| crossorigin | 原生属性 [crossorigin](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/crossorigin) | `enum` | — |
| on-preview | 点击文件列表中已上传的文件时的钩子 | `Function` | — |
| on-remove | 文件列表移除文件时的钩子 | `Function` | — |
| on-success | 文件上传成功时的钩子 | `Function` | — |
| on-error | 文件上传失败时的钩子 | `Function` | — |
| on-progress | 文件上传时的钩子 | `Function` | — |
| on-change | 文件状态改变时的钩子，添加文件、上传成功和上传失败时都会被调用 | `Function` | — |
| on-exceed | 当超出限制时，执行的钩子函数 | `Function` | — |
| before-upload | 上传文件之前的钩子，参数为上传的文件， 若返回`false`或者返回 `Promise` 且被 reject，则停止上传。 | `Function` | — |
| before-remove | 删除文件之前的钩子，参数为上传的文件和文件列表， 若返回 `false` 或者返回 `Promise` 且被 reject，则停止删除。 | `Function` | — |
| file-list / v-model:file-list | 默认上传文件 | `array` | \[\] |
| list-type | 文件列表的类型 | `enum` | text |
| auto-upload | 是否自动上传文件 | `boolean` | true |
| http-request | 覆盖默认的 Xhr 行为，允许自行实现上传文件的请求 | `Function` | [请参考ajaxUpload](https://github.com/element-plus/element-plus/blob/dev/packages/components/upload/src/ajax.ts#L55) |
| disabled | 是否禁用上传 | `boolean` | false |
| limit | 允许上传文件的最大数量 | `number` | — |
| directory 2.13.1 | 是否支持上传文件夹。 启用后，只能选择文件夹；选择文件夹后，文件夹内的文件将被扁平化处理。 | `boolean` | false |

### 插槽 [​](#插槽)

| 名称 | 描述 | 类型 |
| --- | --- | --- |
| default | 自定义默认内容 | \- |
| trigger | 触发文件选择框的内容 | \- |
| tip | 提示说明文字 | \- |
| file | 缩略图模板的内容 | `object` |

### 外部方法 [​](#外部方法)

| 名称 | 描述 | 类型 |
| --- | --- | --- |
| abort | 取消上传请求。 当指定了文件时，中止相应的待上传文件；当未指定文件时，中止所有待上传文件。 | `Function` |
| submit | 手动上传文件列表 | `Function` |
| clearFiles | 清空已上传的文件列表（该方法不支持在 `before-upload` 中调用） | `Function` |
| handleStart | 手动选择文件 | `Function` |
| handleRemove | 手动移除文件。 `file` 和`rawFile` 已被合并。 `rawFile` 将在 `v2.2.0` 中移除 | `Function` |

## 类型声明 [​](#类型声明)

显示类型声明

ts

```
type UploadFiles = UploadFile[]

type UploadUserFile = Omit<UploadFile, 'status' | 'uid'> &
  Partial<Pick<UploadFile, 'status' | 'uid'>>

type UploadStatus = 'ready' | 'uploading' | 'success' | 'fail'

type Awaitable<T> = Promise<T> | T

type Mutable<T> = { -readonly [P in keyof T]: T[P] }

interface UploadFile {
  name: string
  percentage?: number
  status: UploadStatus
  size?: number
  response?: unknown
  uid: number
  url?: string
  raw?: UploadRawFile
}

interface UploadProgressEvent extends ProgressEvent {
  percent: number
}

interface UploadRawFile extends File {
  uid: number
  isDirectory?: boolean
}

interface UploadRequestOptions {
  action: string
  method: string
  data: Record<string, string | Blob | [string | Blob, string] | string[]>
  filename: string
  file: UploadRawFile
  headers: Headers | Record<string, string | number | null | undefined>
  onError: (evt: UploadAjaxError) => void
  onProgress: (evt: UploadProgressEvent) => void
  onSuccess: (response: any) => void
  withCredentials: boolean
}
```

## 源代码 [​](#源代码)

[组件](https://github.com/element-plus/element-plus/tree/dev/packages/components/upload) • [样式](https://github.com/element-plus/element-plus/tree/dev/packages/theme-chalk/src/upload.scss) • [文档](https://github.com/element-plus/element-plus/blob/dev/docs/en-US/component/upload.md)

## 贡献者 [​](#贡献者)

[![](https://avatars.githubusercontent.com/u/6481596?v=4&size=64)](https://github.com/sxzz)[![](https://avatars.githubusercontent.com/u/25154432?v=4&size=64)](https://github.com/YunYouJun)[![](https://avatars.githubusercontent.com/u/15975785?v=4&size=64)](https://github.com/jw-foss)[![](https://avatars.githubusercontent.com/u/24516654?v=4&size=64)](https://github.com/btea)[![](https://avatars.githubusercontent.com/u/58726932?v=4&size=64)](https://github.com/rzzf)[![](https://avatars.githubusercontent.com/u/93767616?v=4&size=64)](https://github.com/makedopamine)[![](https://avatars.githubusercontent.com/u/23313167?v=4&size=64)](https://github.com/tolking)[![](https://avatars.githubusercontent.com/u/45450994?v=4&size=64)](https://github.com/warmthsea)[![](https://avatars.githubusercontent.com/u/30518686?v=4&size=64)](https://github.com/emojiiii)[![](https://avatars.githubusercontent.com/u/27342882?v=4&size=64)](https://github.com/ryuhangyeong)[![](https://avatars.githubusercontent.com/u/26833520?v=4&size=64)](https://github.com/josonho)[![](https://avatars.githubusercontent.com/u/91417411?v=4&size=64)](https://github.com/Dsaquel)[![](https://avatars.githubusercontent.com/u/33646534?v=4&size=64)](https://github.com/SevenDreamYang)[![](https://avatars.githubusercontent.com/u/49601167?v=4&size=64)](https://github.com/jianjunyuu)[![](https://avatars.githubusercontent.com/u/10278227?v=4&size=64)](https://github.com/HeftyKoo)[![](https://avatars.githubusercontent.com/u/23251408?v=4&size=64)](https://github.com/chenxch)[![](https://avatars.githubusercontent.com/u/23100055?v=4&size=64)](https://github.com/holazz)[![](https://avatars.githubusercontent.com/u/21104054?v=4&size=64)](https://github.com/Alanscut)[![](https://avatars.githubusercontent.com/u/29560987?v=4&size=64)](https://github.com/adaex)[![](https://avatars.githubusercontent.com/u/109521682?v=4&size=64)](https://github.com/snowbitx)[![](https://avatars.githubusercontent.com/u/54931083?v=4&size=64)](https://github.com/wjp980108)[![](https://avatars.githubusercontent.com/u/33254923?v=4&size=64)](https://github.com/yicheny)[![](https://avatars.githubusercontent.com/u/29867660?v=4&size=64)](https://github.com/yuhengshen)[![](https://avatars.githubusercontent.com/u/69418751?v=4&size=64)](https://github.com/selicens)[![](https://avatars.githubusercontent.com/u/186382194?v=4&size=64)](https://github.com/ly-yewu)[![](https://avatars.githubusercontent.com/u/35426360?v=4&size=64)](https://github.com/Jungzl)[![](https://avatars.githubusercontent.com/u/43257608?v=4&size=64)](https://github.com/Liao-js)[![](https://avatars.githubusercontent.com/u/126888254?v=4&size=64)](https://github.com/zhuchaoling)[![](https://avatars.githubusercontent.com/u/62926576?v=4&size=64)](https://github.com/ma-shuo)[![](https://avatars.githubusercontent.com/u/70570907?v=4&size=64)](https://github.com/chouchouji)[![](https://avatars.githubusercontent.com/u/10903843?v=4&size=64)](https://github.com/klren0312)[![](https://avatars.githubusercontent.com/u/63360587?v=4&size=64)](https://github.com/wkasunsampath)[![](https://avatars.githubusercontent.com/u/69044080?v=4&size=64)](https://github.com/wzc520pyfm)[![](https://avatars.githubusercontent.com/u/3642589?v=4&size=64)](https://github.com/youpinyao)[![](https://avatars.githubusercontent.com/u/1442212?v=4&size=64)](https://github.com/hhucqian)[![](https://avatars.githubusercontent.com/u/39689863?v=4&size=64)](https://github.com/GenerQAQ)[![](https://avatars.githubusercontent.com/u/101238421?v=4&size=64)](https://github.com/acyza)[![](https://avatars.githubusercontent.com/u/59350883?v=4&size=64)](https://github.com/init-qy)[![](https://avatars.githubusercontent.com/u/169252980?v=4&size=64)](https://github.com/xiaochenchen-igg-com)[![](https://avatars.githubusercontent.com/u/144010?v=4&size=64)](https://github.com/purepear)[![](https://avatars.githubusercontent.com/u/17268607?v=4&size=64)](https://github.com/LYlanfeng)[![](https://avatars.githubusercontent.com/u/26672484?v=4&size=64)](https://github.com/msidolphin)[![](https://avatars.githubusercontent.com/u/65154?v=4&size=64)](https://github.com/exherb)[![](https://avatars.githubusercontent.com/u/39730999?v=4&size=64)](https://github.com/buqiyuan)[![](https://avatars.githubusercontent.com/u/3841747?v=4&size=64)](https://github.com/sumy7)[![](https://avatars.githubusercontent.com/u/13826607?v=4&size=64)](https://github.com/wxyong)[![](https://avatars.githubusercontent.com/u/17539193?v=4&size=64)](https://github.com/gaoyia)[![](https://avatars.githubusercontent.com/u/44761321?v=4&size=64)](https://github.com/xiaoxian521)[![](https://avatars.githubusercontent.com/u/1181011?v=4&size=64)](https://github.com/qdechochen)[![](https://avatars.githubusercontent.com/u/46493087?v=4&size=64)](https://github.com/FrontEndDog)[![](https://avatars.githubusercontent.com/u/145281501?v=4&size=64)](https://github.com/typed-sigterm)[![](https://avatars.githubusercontent.com/u/34408516?v=4&size=64)](https://github.com/betavs)[![](https://avatars.githubusercontent.com/u/31885971?v=4&size=64)](https://github.com/wonderl17)[![](https://avatars.githubusercontent.com/u/17680888?v=4&size=64)](https://github.com/iamkun)[![](https://avatars.githubusercontent.com/u/28811207?v=4&size=64)](https://github.com/fanhefeng)[![](https://avatars.githubusercontent.com/u/10802869?v=4&size=64)](https://github.com/Chris-Kin)[![](https://avatars.githubusercontent.com/u/12124478?v=4&size=64)](https://github.com/Hades-li)[![](https://avatars.githubusercontent.com/u/37203836?v=4&size=64)](https://github.com/PikiLee)[![](https://avatars.githubusercontent.com/u/226283245?v=4&size=64)](https://github.com/E66Crisp)[![](https://avatars.githubusercontent.com/u/1836701?v=4&size=64)](https://github.com/HADB)[![](https://avatars.githubusercontent.com/u/41336612?v=4&size=64)](https://github.com/liulinboyi)[![](https://avatars.githubusercontent.com/u/33344586?v=4&size=64)](https://github.com/Meglody)[![](https://avatars.githubusercontent.com/u/30743104?v=4&size=64)](https://github.com/marcovelarde)

[TreeSelect 树形选择](https://element-plus.org/zh-CN/component/tree-select)

[Avatar 头像](https://element-plus.org/zh-CN/component/avatar)


