# 图片 / 视频 / 资产输入工作流使用参考

## 图片 workflow

典型步骤：

1. 用 `registry --agent` 找到 `output_modalities` 包含 `image` 的 workflow
2. 填写必填文本参数
3. 若 schema 中包含 `image` 字段：
   - 本机直连 bridge 时，传本机绝对路径
   - 远程 bridge 时，仍然传当前机器的本机绝对路径，skill 会自动上传
4. 调用 `run`
5. 用 `status` 读取图片输出路径；远程 bridge 场景会自动下载到当前机器

示例：

```bash
python jmcai_skill.py run --workflow demo-image --args '{"prompt_1":"a clean product photo","image_6":"/absolute/path/to/input.png"}'
```

## 视频 workflow

典型步骤：

1. 用 `registry --agent` 找到 `output_modalities` 包含 `video` 的 workflow
2. 填写必填文本参数
3. 调用 `run`
4. 用 `status` 读取视频输出路径

示例：

```bash
python jmcai_skill.py run --workflow demo-video --args '{"prompt_1":"a cinematic cat video"}'
```

## 音频 / 文件输入 workflow

典型步骤：

1. 用 `registry --agent` 找到 schema 中包含 `audio`、`video`、`file` 或 `mask` 字段的 workflow
2. 仍然传当前机器上的本机绝对路径
3. 本机直连 bridge 时，bridge 直接读取这些路径
4. 远程 bridge 时，skill 会自动上传并改写成 `upload:<id>`

示例：

```bash
python jmcai_skill.py run --workflow demo-audio --args '{"prompt_1":"clone this voice","audio_3":"/absolute/path/to/reference.wav"}'
```

注意：

- `file` 类型远程自动上传只覆盖常见 workflow 资产格式，例如媒体文件、字幕文件和常见文档资产
- 如果 workflow 需要任意绝对路径、自定义 token 或更特殊的文件类型，应优先让桌面端或 workflow author 明确约束

## 常见错误

- `No enabled workflows are currently exposed by Workflow Bridge.`
  说明桌面端当前没有公开可用 workflow

- `Cannot reach Workflow Bridge`
  说明 bridge 不可达，优先检查桌面端是否已启动

- `Bridge upload response did not include upload_id.`
  说明远程桌面端 bridge 版本过低或未正确升级到新上传接口

- `File type '...' is not allowed for File input.`
  说明当前传入的本地文件后缀不在 skill 的安全白名单内

- `未知参数`
  说明传入了 schema 之外的字段

- `缺少必填参数`
  说明必填 alias 没传齐
