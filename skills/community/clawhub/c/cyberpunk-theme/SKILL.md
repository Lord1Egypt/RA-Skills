---
name: 赛博朋克主题
description: Install or customize this OpenClaw cyberpunk chat and dream theme. Use when the user wants this exact theme, wants to import it into another workspace, or wants to swap the bundled avatars and background images.
---

# 赛博朋克主题

这个 skill 用来安装或更新一套 OpenClaw 赛博朋克聊天 + 梦境主题。

## 当前包含

- 赛博朋克 + P5 风格聊天页视觉层
- 聊天背景、助手头像、工具头像、帮助/历史头像、用户头像替换
- 梦境页背景与梦境头像替换
- 聊天消息头像自动纠偏
- 浮动 composer 上方的 context usage、compaction、run status 层级修正
- 安全默认 runtime：只启用 HUD、头像、header、底部 composer 布局同步；默认关闭 quota badge、session fallback、消息时间线重排
- OpenClaw 2026.6.9 chat composer 适配：恢复 HUD / 头像替换，兼容 `chat-workbench` 嵌套输入区，模型选择器靠左贴近输入工具，使用情况、设置与发送按钮靠右顺序排列

## 能配置什么

支持替换这七个槽位：

- 主助手头像
- Tool 头像
- Help / 历史消息头像
- 用户头像
- 聊天背景大图
- 梦境头像
- 梦境背景大图

具体文件映射见 `references/theme-slots.md`。

## 素材尺寸建议

- 聊天页主助手 / Tool / Help 历史 / 用户立绘框当前为 `160x240`，比例 `2:3`。推荐原图也使用 `2:3` 竖图，至少 `1024x1536`，避免在框内裁切或放大后糊化。
- 聊天背景用于整张聊天页内容区铺底，当前素材为 `1536x1024`，比例 `3:2`，CSS 使用 `cover` + `center bottom`。推荐使用横向 `3:2` 或更宽的高分辨率图，底部主体不要贴边。
- 梦境背景用于梦境页主舞台铺底，当前素材为 `2752x1536`，约 `16:9`，CSS 使用 `cover` + `center 52%`。推荐使用 `16:9` 或接近 `16:9` 的大图。
- 梦境头像显示在 `226x226` 圆形框内，推荐方图或方形 GIF，当前素材为 `240x240`。

## 怎么用

默认安装：

`python3 scripts/install_cyberpunk_theme.py --workspace <target-workspace>`

带素材覆盖安装：

`python3 scripts/install_cyberpunk_theme.py --workspace <target-workspace> --assistant-avatar /path/to/main.png --tool-avatar /path/to/tool.png --help-avatar /path/to/help.png --user-avatar /path/to/user.png --chat-background /path/to/chat.jpg --dream-avatar /path/to/dream.gif --dream-background /path/to/dream-bg.png`

如果不想在命令行里写长串参数，用 JSON 配置。先复制示例并把里面所有 `/path/to/...` 占位符改成真实路径，再运行：

`python3 scripts/install_cyberpunk_theme.py --from-config /absolute/path/to/your-theme-config.json`

配置模板在：

- `references/theme-config.example.json`

如果主题已经装好了，只是 OpenClaw 更新后需要重新挂载：

`python3 scripts/apply_cyberpunk_theme.py`

## 兼容说明

- 主题通过 `<style id="openclaw-workspace-theme">` 和 `<script id="openclaw-workspace-theme-script">` 注入 live Control UI。
- 不使用 `openclaw-custom-theme` id，避免和 OpenClaw 内建自定义主题注入器冲突。
- 当前主题源适配 OpenClaw 2026.5 系列 chat/control UI，并已补齐 OpenClaw 2026.6.1、2026.6.5 与 2026.6.9 chat/control UI 结构变化。

## 安装后效果

安装脚本会：

1. 把主题文件装进目标工作区的 `customizations/openclaw-control-ui/`
2. 按传入参数或 JSON 配置替换素材槽位
3. 生成目标工作区内可重复执行的 `scripts/apply_cyberpunk_theme.py`
4. 默认立即把主题 apply 到 live OpenClaw control-ui

## 文件说明

- `assets/theme/`：主题默认源文件与默认素材
- `assets/theme/assets/`：聊天页立绘、聊天背景、梦境头像默认素材
- `assets/theme/dreaming-bg.png`：梦境背景默认素材
- `assets/cyberpunk-theme-small.svg` / `assets/cyberpunk-theme-large.svg`：skill 图标
- `scripts/install_cyberpunk_theme.py`：安装、覆盖槽位、生成 apply 脚本、执行 apply
- `references/theme-slots.md`：七个视觉槽位与落地文件名
- `references/theme-config.example.json`：`--from-config` 的示例配置

## Changelog

- `1.0.21`：修正 OpenClaw 2026.6.9 composer 右侧控制区排序，把 `使用情况 -> 聊天设置 -> 发送` 固定在同一行，避免 usage badge 被浏览器排进隐式列后掉到右下角。
- `1.0.20`：适配 OpenClaw 2026.6.9 `chat-workbench` 嵌套 composer DOM，恢复底部输入框、附件 / Talk / 模型 / 设置 / 发送控件可见；修正 runtime footer 量测对新版嵌套定位的反馈漂移，避免 `--oc-chat-composer-bottom` 被越推越大。
- `1.0.19`：同步 OpenClaw 2026.6.5 聊天页稳定性热修，默认关闭 quota badge、session fallback 与消息时间线重排，只保留 HUD / 头像 / header / 底部布局同步；修正带属性 `<style>` / `<script>` 注入块无法去重的问题，并把底部模型选择器移回左侧工具区。
- `1.0.18`：整理 OpenClaw 2026.6.1 chat 热修为单一适配段，恢复聊天壁纸直显，隐藏 workspace files rail，透明化聊天与 tool 气泡，动态测量 composer/footer 预留高度，并收窄右侧 Markdown 抽屉。
- `1.0.17`：重新发布完整的文本化默认素材包，修正 `1.0.16` 发布记录中安装脚本已带还原逻辑但 `encoded-assets/*.txt` 未进入 ClawHub 文件列表的问题。
- `1.0.16`：修正 ClawHub skill 只上传文本文件导致默认 PNG/JPG/GIF 素材缺失的问题，随包提供文本化素材备份并在安装时自动还原，避免从 ClawHub 安装后主题缺默认立绘/背景图。
- `1.0.15`：修正 WebChat 聊天页 session 下拉选择框的层级链路，移除会裁切菜单的旧 `overflow`，并把 `.content-header`、`.chat-controls`、`.chat-session-picker` 整体抬到消息时间线之上，避免下拉被 transcript 盖住。
- `1.0.14`：修正主题重新注入时的 live `dist/control-ui` 目标发现逻辑，自动兼容本机 OpenClaw 安装路径；同时彻底移除梦境页主舞台残留的毛玻璃遮罩与额外底色，实现 changelog 承诺的直贴背景图效果。
- `1.0.13`：移除梦境页主舞台的毛玻璃与额外底色，让梦境内容直接贴合背景图，不再额外罩一层特殊面板。
- `1.0.12`：修正 WebUI 聊天时间线在 `chatMessages` 和 `chatToolMessages` 合流时的稳定排序，强制同时间戳消息保持 `user -> assistant tool -> toolResult -> assistant 文本`，避免官方前端把最终回复插到工具流前面。
- `1.0.11`：把 tool / helper 立绘从纯 CSS 背景图切到真实 `<img>` 填充层，避免这两路头像在浏览器合成时出现明显糊化 / 压缩感。
- `1.0.10`：修正聊天铭牌来源，helper 固定显示为 `消息助手 helper`，主助手铭牌改为从 `IDENTITY.md` / `SOUL.md` 解析，并同步去掉前端对“菠萝包”名字的硬编码匹配。
- `1.0.9`：微调右侧抽屉展开态上下间距，让顶部控制区和底部输入框避让后的视觉留白保持一致。
- `1.0.8`：新增 Help / 历史消息头像槽位 `--help-avatar` / `helpAvatar`，用于替换聊天里非主助手的帮助立绘。
- `1.0.7`：同步 2026.5 chat 顶栏用量修复，Codex 用量按钮显示 `5h xx / 周 xx`，并保留 tooltip reset 信息。
- `1.0.6`：保留为已发布小版本。
- `1.0.5`：适配 OpenClaw 2026.5 footer status layer，让 context usage、compaction、run-status 在浮动 composer 上方稳定可见。
