# 常见问题 FAQ

## 本地文件上传失败
1. 确认依赖已安装：`pip install tos Pillow requests`
2. 确认 `TOS_ACCESS_KEY` 和 `TOS_SECRET_KEY` 已正确配置
3. 确认 TOS 存储桶有写入权限
4. 检查网络连接是否正常

## 图片转换失败
1. 确认 Pillow 已安装：`pip install Pillow`
2. 确认图片格式正确（支持 PNG/JPG/JPEG/GIF/BMP/WEBP/TIFF）
3. 超大图片可能需要更多内存，请尝试缩小图片尺寸

## 任务提交失败（401 未授权）
1. 确认 `LAS_API_KEY` 已正确配置
2. 确认 API Key 未过期且有权限调用 LAS PDF 解析服务
3. 确认区域配置正确（cn-beijing / cn-shanghai）

## 任务一直处于 processing 状态
1. 大文件/复杂文档解析需要更长时间，请耐心等待
2. 如果怀疑任务卡死，可以尝试使用同样的参数重新执行 `check-and-notify --poll` 命令
3. 如果超过 10 分钟仍未完成，请提交新的解析任务

## 解析结果格式不对
1. 确认使用的是最新版本的 skill
2. 尝试使用 `detail` 解析模式获得更精确的结构化结果
3. 如果是扫描件，请确保图片清晰度足够
