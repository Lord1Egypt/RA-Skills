# Provider 配置参考

`project-generate` 的 Provider 层通过 `script.json` 的 `script.provider` / `script.video_provider` 字段路由到不同的图片/视频生成服务。

## Provider 架构

```
project_commands/ 包 / video_utils.py
  └── provider_factory.create_provider(project)
        ├── script.provider → 图片生成 Provider
        └── script.video_provider → 视频生成 Provider（不设则同 provider）
```

Provider 通过 `script.json` 中的 `provider` 和 `video_provider` 字段确定。也支持从飞书文档标题自动检测（标题含"小云雀视频" → `video_provider: xiaoyunqiao`）。

## Agnes AI（默认）

| 项目 | 说明 |
|------|------|
| **provider 值** | `"agnes"` |
| **费用** | 免费无限 |
| **API Key** | `~/.agnes-api-key` 或环境变量 `AGNES_API_KEY` 或 `config.toml` |
| **生成模式** | standard / multi-image / keyframes 三种 |
| **认证** | Bearer Token |
| **端点** | `https://apihub.agnes-ai.com/v1/videos` |
| **模型** | 图片：`agnes-image-2.1-flash` / `agnes-image-2.0-flash`；视频：`agnes-video-v2.0` |
| **参考图** | GitHub raw / data URI |
| **时长** | 通过 `num_frames` 精确控制（合法值 8n+1，≤441） |

## 小云雀 Seedance 2.0

| 项目 | 说明 |
|------|------|
| **provider 值** | `"xiaoyunqiao"` |
| **费用** | 约 1 元/秒（火山引擎商业化 API） |
| **AK/SK** | `~/.xyq-access-key` + `~/.xyq-secret-key` 或环境变量 `VOLCENGINE_ACCESS_KEY` / `VOLCENGINE_SECRET_KEY` 或 `config.toml` |
| **生成模式** | 统一多图参考（不区分 mode） |
| **认证** | AK/SK 签名（volcengine SDK 自动处理） |
| **端点** | `https://visual.volcengineapi.com` |
| **SDK** | `volcengine`（`pip install volcengine`） |
| **参考图** | GitHub raw URL（公网可访问 URL 数组） |
| **时长** | 范围值：`"～15s"` / `"～30s"` / `"40～60s"` |

## 参数对比

| 参数 | Agnes AI | 小云雀 |
|------|---------|--------|
| 水印 | 无水印 | 默认有（需 `enable_watermark: false`）|
| 分辨率 | 自定义 width/height | 固定 9:16 / 16:9 等（`ratio` 参数）|
| 音频 | 无（需外部合成） | 可选 `generate_audio` |
| 多图 | extra_body.image 数组 | img_url_list 数组（最多 50 个）|
| keyframes | mode=keyframes | 不支持（统一走多图参考）|

## 前置条件

**Agnes AI**：只需 API Key，写进 `~/.agnes-api-key` 即可。

**小云雀**：
1. 注册火山引擎账号
2. 开通即梦AI / 小云雀服务
3. 创建 AccessKey 并写入 `~/.xyq-access-key` + `~/.xyq-secret-key`
4. `pip install volcengine`

## 完整配置示例

```json
{
  "script": {
    "provider": "agnes",            // 图片生成（默认 agnes）
    "video_provider": "xiaoyunqiao" // 视频生成（不设则同 provider）
  }
}
```
