# bilibili-api-python 关键注意事项

## WBI 签名机制

B 站 API 使用 WBI 签名防爬。bilibili-api-python 内部自动处理：
- 从 B 站获取 wbi_img_key 和 wbi_sub_key
- 对请求参数排序后拼接 + MD5 签名
- 签名会定期更新，库自动缓存和刷新

无需手动处理 WBI，但需要保持库版本更新（B 站会不定期更换签名算法）。

## Cookie 格式

登录后需要保存的关键 cookie：
- **SESSDATA**: 会话凭证（最重要）
- **bili_jct**: CSRF token
- **buvid3**: 设备标识
- **DedeUserID**: 用户 ID
- **ac_time_value**: 访问控制时间戳

Cookie 有效期通常约 30 天，过期后需重新登录。
可通过 `Credential.check_valid()` 检查有效性。

## 常见错误码

| 错误码 | 含义 | 处理方式 |
|--------|------|---------|
| 412 | 风控拦截 | 需要登录获取 cookie，或等待一段时间 |
| -403 | 权限不足 | 可能需要大会员或购买课程 |
| -404 | 视频不存在 | 检查 BV/AV 号是否正确 |
| -352 | 风控验证 | 需要完成人机验证 |
| -101 | 未登录 | 需要提供有效 cookie |
| -799 | 请求过频 | 降低请求频率 |

## AI 字幕语言代码

B 站 AI 生成字幕使用 `ai-` 前缀：

| 代码 | 语言 |
|------|------|
| ai-zh | 中文 |
| ai-en | 英文 |
| ai-ja | 日文 |
| ai-ko | 韩文 |
| ai-es | 西班牙文 |
| ai-fr | 法文 |
| ai-de | 德文 |
| ai-pt | 葡萄牙文 |
| ai-ar | 阿拉伯文 |

并非所有视频都有 AI 字幕，取决于 UP 主是否开启和 B 站是否生成。

## 课程（Cheese）接口

B 站课程使用独立的 API：
- SS 号：课程 ID，用于获取课程信息和剧集列表
- EP 号：具体剧集 ID，用于获取单集字幕

课程接口需要登录，且购买课程后才能获取字幕。
使用 `bilibili_api.cheese` 模块操作。

## 音频下载注意事项

- DASH 格式：音视频分离，需要单独下载音频流
- 必须设置 Referer 头为 `https://www.bilibili.com`
- 音频格式通常为 m4a (AAC)
- 下载频率不宜过高，否则触发风控
