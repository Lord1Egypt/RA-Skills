# Douyin-to-Photos 快捷指令搭建指南（逐动作）

本指南面向 iPhone/iOS 快捷指令 App，目标是：复制抖音链接后，一键下载并存入相册。

## A. 先建主快捷指令

快捷指令名建议：`Douyin-to-Photos`

在顶部 `i` 配置中：

- 打开 `在共享表单中显示`
- 接收类型勾选：`URL`、`文本`
- 关闭不必要的输入类型

## B. 动作清单（按顺序添加）

1. `词典`（Dictionary）
- 键 `api_primary`: `https://www.tikwm.com/api/`
- 键 `api_fallback`: 你的备用解析接口（可留空）
- 键 `album_name`: `Douyin`（可改）
- 键 `timeout_sec`: `20`

2. `如果`（If）
- 条件：`快捷指令输入` 有值
- 是：`设定变量 RawInput = 快捷指令输入`
- 否：
  - `获取剪贴板`
  - `设定变量 RawInput = 剪贴板`

3. `获取文本`（Get Text from Input）
- 输入：`RawInput`
- 输出变量：`InputText`

4. `匹配文本`（Match Text）
- 文本：`InputText`
- 正则：`https?://[^\s]+`
- 输出变量：`UrlCandidates`

5. `如果`
- 条件：`UrlCandidates` 的数量 `=` `0`
- 动作：`显示提醒`（链接无效，未识别到 URL）
- 动作：`停止此快捷指令`

6. `从列表获取项目`（Get Item from List）
- 列表：`UrlCandidates`
- 项目：`第一个`
- 输出变量：`ShareURL`

7. `如果`
- 条件：`ShareURL` 不包含 `douyin.com` 且 不包含 `iesdouyin.com`
- 动作：`显示提醒`（仅支持抖音分享链接）
- 动作：`停止此快捷指令`

8. `词典`
- 键 `url`: `ShareURL`
- 键 `hd`: `1`
- 键 `count`: `12`
- 输出变量：`ReqBody`

9. `获取词典值`
- 从第 1 步配置词典取 `api_primary` -> `ApiPrimary`

10. `获取 URL 内容`（Get Contents of URL）
- URL：`ApiPrimary`
- 方法：`POST`
- 请求体：`表单`（Form）
- 字段：`ReqBody` 的键值（`url/hd/count`）
- 超时：从配置取 `timeout_sec`
- 输出：`PrimaryResp`

11. `获取词典值`
- 从 `PrimaryResp` 取 `code` -> `PrimaryCode`

12. `如果`
- 条件：`PrimaryCode` 不等于 `0`
- 动作：跳到第 13 步（备用 API）
- 否：继续第 16 步解析视频地址

13. `获取词典值`
- 从配置词典取 `api_fallback` -> `ApiFallback`

14. `如果`
- 条件：`ApiFallback` 为空
- 动作：`显示提醒`（主接口失败且未配置备用接口）
- 动作：`停止此快捷指令`

15. `获取 URL 内容`
- URL：`ApiFallback`
- 方法：`POST`
- 请求体：JSON：`{"url":"ShareURL"}`
- 输出：`FallbackResp`

16. `词典`（解析统一字段）
- 先从主响应取：`data.hdplay`，空则取 `data.play`
- 若主失败，则从备用响应取：`data.video_url`（或你备用接口约定字段）
- 最终得到变量：`VideoURL`

17. `如果`
- 条件：`VideoURL` 为空
- 动作：`显示提醒`（解析失败：未获取到 MP4 地址）
- 动作：`停止此快捷指令`

18. `获取 URL 内容`
- URL：`VideoURL`
- 方法：`GET`
- 结果设为：`文件`（File）
- 输出变量：`VideoFile`

19. `存储到照片`（Save to Photo Album）
- 输入：`VideoFile`
- 相册：可固定为 `Douyin`，或用变量 `album_name`

20. `删除文件`（Delete File）
- 输入：`VideoFile`
- 打开：`立即删除`

21. `显示通知`
- 文案：`视频已保存到相册`

## C. API 绕过策略说明（可替换）

核心不是“破解本地下载按钮”，而是通过后端解析服务获取播放源地址：

1. 提交抖音分享链接到解析接口（如 tikwm）
2. 接口返回结构化 JSON，包含可播放地址（常见字段：`data.hdplay`、`data.play`）
3. 快捷指令只负责下载 MP4 并写入相册

建议做双通道：

- 主接口：`tikwm`
- 备用接口：你自己的网关（或你信任的供应商 API）

这样可应对单一服务限流、超时、区域故障。

## D. Share Sheet 一步触发

1. 打开任意抖音视频，点分享 -> 复制链接
2. 在可分享页面点击 `分享...`
3. 选 `Douyin-to-Photos`
4. 等待通知“视频已保存到相册”

## E. Back Tap 一步触发（剪贴板模式）

1. 设置 -> 辅助功能 -> 触控 -> 轻点背面
2. 选择 `轻点两下` 或 `轻点三下`
3. 绑定到 `Douyin-to-Photos`（或绑定到一个 Launcher，再调用主快捷指令）
4. 使用时先复制链接，再轻点背面即可

## F. 健壮性建议（必须加）

- 所有网络请求都加超时（15-20 秒）
- 对 `code != 0`、空地址、非 2xx 响应统一弹窗
- 失败时也执行缓存清理（删除临时文件）
- 每次完成后只提示结果，不记录历史链接

## G. 合规边界

- 仅处理你有权保存的内容
- 不移除付费、会员或受保护内容访问控制
- 权限最小化：仅允许“添加到照片”
