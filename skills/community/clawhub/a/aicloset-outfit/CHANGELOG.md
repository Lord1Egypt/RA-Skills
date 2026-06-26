# Changelog

## [0.8.0] - 2026-03-13

- 移除 `requires.env` 声明，安装后直接 `ready`，不再因缺少 API Key 而标记为 `missing`
- API Key 缺失时由脚本运行时友好提示配置方法

## [0.7.2] - 2026-03-13

- 脚本新增 `MEDIA:<path>` 输出，IM 渠道（飞书/钉钉等）自动上传并发送图片到聊天
- 修正图片发送机制：使用 OpenClaw 原生 MEDIA 标记，替代 message 工具方式
- 更新展示结果规则，确保 MEDIA 行不被删除

## [0.7.1] - 2026-03-13

- 新增 IM 聊天渠道图片发送说明（飞书/钉钉/Discord/Slack 等）
- 支持通过 message 工具的 send action + media 参数发送图片到 IM 聊天
- 区分 CLI 终端模式与 IM 渠道模式的图片展示方式

## [0.6.0] - 2026-03-13

- 全流程改用 Python 标准库 + ImageMagick subprocess，零 pip 依赖
- 跨平台兼容 macOS / Windows / Linux（路径、图片预览、下载）
- 合并认证检查、API 调用、图片合成、边框、预览为一个脚本
- 内置网络重试、ImageMagick 检测

## [0.5.0] - 2026-03-12

- 回退 Python 方案，还原为 curl + ImageMagick（避免用户 pip 网络问题）
- 保留 v0.4.5 的所有功能：进度提示、open 预览、默认参数

## [0.4.0] - 2026-03-12

- 搭配结果改为 ImageMagick 图片合成展示
- 按 API 返回的画布坐标（center/size/z_index）精准定位单品
- 4 套搭配自动拼接为总览图
- 逐套展示单品组合图片

## [0.3.0] - 2026-03-12

- 支持 OpenClaw `openclaw.json` 配置文件方式设置 API Key 和 Token
- 添加 `metadata.openclaw.primaryEnv` 声明，实现 apiKey 自动注入
- 认证检查增加配置文件回退读取

## [0.2.0] - 2026-03-12

- 拆分为独立 Skill 目录，支持多技能并行迭代
- 项目结构调整为 monorepo 多 Skill 模式

## [0.1.0] - 2026-03-12

- 初始版本
- 支持系统搭配推荐 API 调用
- 支持自定义 API Key 和 Token 环境变量配置
- 智能提取日期、城市、风格参数
- 4 套搭配结果图文画布展示
- 错误处理：未配置引导、API 错误提示、网络重试
