# Theme Slots

安装到目标工作区后，主题槽位固定映射到这些文件：

- 主助手头像: `customizations/openclaw-control-ui/assets/avatar2.png`
- Tool 头像: `customizations/openclaw-control-ui/assets/avatar1.png`
- Help / 历史消息头像: `customizations/openclaw-control-ui/assets/history-avatar.png`
- 用户头像: `customizations/openclaw-control-ui/assets/header.png`
- 聊天背景大图: `customizations/openclaw-control-ui/assets/chat-bg-cyberpunk.jpg`
- 梦境头像: `customizations/openclaw-control-ui/assets/bao-dream.gif`
- 梦境背景大图: `customizations/openclaw-control-ui/dreaming-bg.png`

对应安装参数：

- `--assistant-avatar`
- `--tool-avatar`
- `--help-avatar`
- `--user-avatar`
- `--chat-background`
- `--dream-avatar`
- `--dream-background`

推荐把这七个槽位理解成：

- `--assistant-avatar`：主助手立绘
- `--tool-avatar`：工具消息立绘
- `--help-avatar`：Help / 历史消息立绘
- `--user-avatar`：用户立绘
- `--chat-background`：聊天主背景大图
- `--dream-avatar`：梦境页中心角色图
- `--dream-background`：梦境页环境背景图

## Recommended Image Geometry

当前 Control UI 主题的聊天立绘框在桌面端统一为 `160x240`，比例 `2:3`：

- `--assistant-avatar`
- `--tool-avatar`
- `--help-avatar`
- `--user-avatar`

推荐给这四个立绘槽位准备 `2:3` 竖图，至少 `1024x1536`。当前默认素材中 `avatar1.png`、`header.png`、`avatar2.png`、`history-avatar.png` 都是 `1024x1536`，会被当前 CSS 放进同一个 `160x240` 框里显示。最稳妥的新增素材仍然按 `2:3` 做，人物主体放在中上部，避免头顶和脚边贴边。

背景和梦境槽位建议：

- `--chat-background`：聊天页内容区背景，当前默认素材是 `1536x1024`，比例 `3:2`。CSS 使用 `cover` 和 `center bottom`，适合横向大图，关键主体建议避开最边缘。
- `--dream-background`：梦境页主舞台背景，当前默认素材是 `2752x1536`，约 `16:9`。CSS 使用 `cover` 和 `center 52%`，适合宽屏环境图。
- `--dream-avatar`：梦境页中心圆形角色图，显示框约 `226x226`，当前默认素材是 `240x240` GIF。推荐方图或方形 GIF。

完整安装命令模板（先把所有 `/path/to/...` 替换成真实路径再运行）：

`python3 scripts/install_cyberpunk_theme.py --workspace /path/to/workspace --assistant-avatar /path/to/main.png --tool-avatar /path/to/tool.png --help-avatar /path/to/help.png --user-avatar /path/to/user.png --chat-background /path/to/chat.jpg --dream-avatar /path/to/dream.gif --dream-background /path/to/dream-bg.png`

只改单个槽位的命令模板（先替换路径再运行）：

`python3 scripts/install_cyberpunk_theme.py --workspace /path/to/workspace --assistant-avatar /path/to/new-main.png`

如果想用 JSON 配置文件，先复制示例文件并把里面所有 `/path/to/...` 占位符改成真实路径，再运行：

`python3 scripts/install_cyberpunk_theme.py --from-config /absolute/path/to/your-theme-config.json`

配置模板见：

- `references/theme-config.example.json`

如果用户只是想换图，不想改 CSS/JS：

1. 直接重跑安装脚本并传覆盖参数
2. 或者手工替换上面这些目标文件，再运行 `python3 scripts/apply_cyberpunk_theme.py`

当前 skill 默认主题素材全部位于：

- `assets/theme/`
- `assets/theme/assets/`
