# a-upload 文件上传

自定义上传，项目使用自定义请求处理。

## 自定义上传

```vue
<a-upload
  :custom-request="customUploadRequest"
  :show-file-list="false"
  multiple
>
  <template #upload-button>
    <a-button type="outline">
      <icon-upload /> 上传文件
    </a-button>
  </template>
</a-upload>
```

```typescript
import { uploadFile } from '@/api/upload';

const customUploadRequest = async (option: any) => {
  const { fileItem, onSuccess, onError } = option;
  try {
    const res = await uploadFile(fileItem.file);
    if (res.code === 0) {
      onSuccess(res.data);
      // 处理上传结果
      fileList.value.push({
        url: res.data.url,
        name: res.data.file_name,
      });
    } else {
      onError(res.msg);
    }
  } catch (error) {
    onError('上传失败');
  }
};
```

## 常用 Props

| Prop | 说明 |
|---|---|
| `custom-request` | 自定义上传方法 |
| `show-file-list` | 是否显示文件列表 |
| `multiple` | 允许多文件 |
| `accept` | 文件类型限制 |
| `#upload-button` | 自定义上传按钮 |

## 项目参考

- `src/views/supplier/components/finance-config-modal.vue` — 自定义上传
