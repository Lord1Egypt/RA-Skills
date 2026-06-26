# Workflow Bridge 参考

在使用这个 skill 时，始终把 JMCAI Comfypet 桌面应用内置的 Workflow Bridge 当作唯一调用面。

## 调用顺序

1. 先运行 `doctor`
2. 再运行 `registry --agent`
3. 选中最合适的 workflow
4. 用 alias schema 组装 `args`
5. 提交 `run`
6. 单次调用 `status` 轮询
7. 如有需要再读 `history`

## Alias Schema 规则

- 只能使用 `registry --agent` 返回的 alias 字段名
- 不能构造 `node_id.field`
- `required: true` 的参数必须补齐
- 本机直连 bridge 时，`image | mask | video | audio | file` 参数都应传本机绝对路径
- 远程 bridge 场景下，skill 会先调用 `POST /api/v1/uploads`，再把资产参数改写为 `upload:<id>`
- `choices`、`min`、`max`、`step` 仍由 bridge 在主应用侧强校验
- `file` 类型远程上传只覆盖常见 workflow 资产格式，不支持任意本地文件外传

## Outputs 规则

`status` 和 `history` 返回的 `outputs` 是 typed output 数组：

- `path`: 本地绝对路径；对远程 bridge 场景，skill 会自动下载到当前机器后重写为当前机器路径
- `download_path`: bridge 侧输出下载接口相对路径
- `media_kind`: `image | video | file`
- `file_name`: 输出文件名
- `mime_type`: 可选 MIME 类型
- `warnings`: 可选；远程任务已成功，但自动下载输出到当前机器失败时返回

对图片 workflow，优先读取 `media_kind == "image"` 的项。  
对视频 workflow，优先读取 `media_kind == "video"` 的项。  
对音频或其他文件输出 workflow，优先读取 `media_kind == "file"` 的项。
