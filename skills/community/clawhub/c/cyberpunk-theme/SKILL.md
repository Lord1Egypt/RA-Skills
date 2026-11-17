---
name: cyberpunk-theme
description: Install, repair, or customize this OpenClaw cyberpunk chat and dream theme. Use when the user wants this exact theme, needs compatibility restored after an OpenClaw update, wants to import it into another workspace, or wants to swap the bundled avatars and background images.
---

# 赛博朋克主题

这个 skill 用来安装或更新一套 OpenClaw 赛博朋克聊天 + 梦境主题。

## 当前包含

- 赛博朋克 + P5 风格聊天页视觉层
- 聊天背景、助手头像、用户头像替换
- 梦境页背景与梦境头像替换
- 聊天页助手 / 用户肖像固定在输入控制台左右两侧，并保持对称水平间距与底部对齐
- 浮动 composer 上方的 context usage、compaction、run status 层级修正
- 安全默认 runtime：只启用 HUD、头像、header、底部 composer 布局同步；默认关闭 quota badge、session fallback、消息时间线重排
- OpenClaw 2026.6.9 chat composer 适配：恢复 HUD / 头像替换，兼容 `chat-workbench` 嵌套输入区，模型选择器靠左贴近输入工具，使用情况、设置与发送按钮靠右顺序排列
- OpenClaw 2026.7.1 chat composer 适配：识别 `agent-chat__composer-shell` 新包裹层，将完整输入控制台稳定锚定在聊天区底部
- OpenClaw 2026.8.1 chat / new-session 适配：兼容 `chat-main__conversation` 与 `new-session-page__composer` 共用的 composer shell，释放旧版强制的 transcript 全高，避免模型与思考等级选择器重叠，并防止展开的工具调用被 flex 压缩裁切

## 能配置什么

支持替换这五个槽位：

- 主助手头像
- 用户头像
- 聊天背景大图
- 梦境头像
- 梦境背景大图

具体文件映射见 `references/theme-slots.md`。

## 素材尺寸建议

- 聊天页主助手 / 用户立绘框桌面为 `132x198`，较窄窗口为 `112x168`，比例 `2:3`；移动端或宽度不足 `650px` 的聊天面板隐藏立绘。推荐原图也使用 `2:3` 竖图，至少 `1024x1536`，避免在框内裁切或放大后糊化。
- 聊天背景用于整张聊天页内容区铺底，当前素材为 `1536x1024`，比例 `3:2`，CSS 使用 `cover` + `center bottom`。推荐使用横向 `3:2` 或更宽的高分辨率图，底部主体不要贴边。
- 梦境背景用于梦境页主舞台铺底，当前素材为 `2752x1536`，约 `16:9`，CSS 使用 `cover` + `center 52%`。推荐使用 `16:9` 或接近 `16:9` 的大图。
- 梦境头像显示在 `226x226` 圆形框内，推荐方图或方形 GIF，当前素材为 `240x240`。

## 怎么用

默认安装：

`python3 scripts/install_cyberpunk_theme.py --workspace <target-workspace>`

带素材覆盖安装：

`python3 scripts/install_cyberpunk_theme.py --workspace <target-workspace> --assistant-avatar /path/to/main.png --user-avatar /path/to/user.png --chat-background /path/to/chat.jpg --dream-avatar /path/to/dream.gif --dream-background /path/to/dream-bg.png`

如果不想在命令行里写长串参数，用 JSON 配置。先复制示例并把里面所有 `/path/to/...` 占位符改成真实路径，再运行：

`python3 scripts/install_cyberpunk_theme.py --from-config /absolute/path/to/your-theme-config.json`

配置模板在：

- `references/theme-config.example.json`

如果主题源已经更新到匹配版本，只需重新挂载，在目标工作区执行：

`python3 scripts/apply_cyberpunk_theme.py`

2026.10.3 梦境入口为 `/settings/memory/dreams`，包含场景、日记与高级页签；回归时测试日期切换和三个日记子页签即可，维护/重置按钮会修改业务数据，不用于主题验证。

2026.10.3 的内建 UI 按网关生命周期缓存入口；apply 后先核对 HTTP 返回是否包含主题，再决定是否重启网关，最后强制刷新并验证实际页面。安装器按 Control UI build id 保留入口原件，回滚时只恢复当前 build 的备份，避免恢复旧版入口。新版入口上限为 256 KiB；安装器仅压缩交付 CSS（保留源文件可读），并在超限时拒绝写入现有入口。

## 兼容说明

- 主题通过 `<style id="openclaw-workspace-theme">` 和 `<script id="openclaw-workspace-theme-script">` 注入 live Control UI。
- 不使用 `openclaw-custom-theme` id，避免和 OpenClaw 内建自定义主题注入器冲突。
- 当前主题源适配 OpenClaw 2026.5 系列 chat/control UI，并已补齐 OpenClaw 2026.6.1、2026.6.5、2026.6.9、2026.7.1、2026.8.1 与 2026.10.3 chat/control UI 结构变化。
- ClawHub 轻量包不重复上传五份大型素材备份；全新安装且本地没有默认素材时，安装器会从官方 `cyberpunk-theme@1.0.21` 冻结版本包下载仍在使用的素材，并逐一校验 SHA-256。已有主题素材或已覆盖全部五个素材槽位时不会下载。

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
- `references/theme-slots.md`：五个视觉槽位与落地文件名
- `references/theme-config.example.json`：`--from-config` 的示例配置

## Changelog

- `1.0.28`：补齐 2026.10.3 梦境页适配：限制记忆设置网格的最小宽度，避免长日期列表将日记正文挤出屏幕；适配新版 hub 页签、移除日记胶囊下多余的原生轨道线、日期滚动和窄屏标题；修复中屏场景状态与头像重叠、手机高级页操作和元信息溢出；压缩交付 CSS 并在写入前校验 256 KiB 入口上限，避免重启后 UI 被网关拒绝。

- `1.0.27`：适配 OpenClaw 2026.10.3 workbench、虚拟滚动与 chat-footer 层级；恢复背景/HUD、双侧立绘和输入区，按面板同步底边，窄面板隐藏立绘；保留原生虚拟列表几何尺寸与新版输入工具布局；入口备份按 build id 隔离。

- `1.0.26`：修复 OpenClaw 2026.8.1 两处 Control UI 兼容回归：让聊天页与新会话页的模型/思考级别选择器共享 composer 可用宽度而不重叠，并阻止展开的工具调用在限高 flex 容器内收缩裁切，使每条工具记录保持自然高度并正常滚动。
- `1.0.25`：集中适配 OpenClaw 2026.8.1 的 `chat-main__conversation` 与 composer shell：释放旧 transcript 全高约束，修正聊天顶栏、progress/input 表面和模型/思考级别选择器堆叠；退役新版不再渲染的 Tool 与 Help / 历史肖像槽位及其 runtime、CSS 和默认素材，保留助手、用户、聊天背景、梦境头像与梦境背景五个有效槽位；将无铭牌助手与用户肖像固定在 composer 两侧，严格采用“肖像 + `24px` + composer + `24px` + 肖像”的网格与底边对齐，空间不足时同步收窄 transcript/composer，移动端继续隐藏肖像。
- `1.0.22`：适配 OpenClaw 2026.7.1 新增的 `agent-chat__composer-shell` 包裹层，恢复聊天页底部完整输入控制台，并让 runtime 尺寸同步优先测量新 composer 容器；ClawHub 轻量包在新装缺少素材时，从固定的 1.0.21 官方包下载并校验七份默认素材，规避当前发布入口的实际包体限制。
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
