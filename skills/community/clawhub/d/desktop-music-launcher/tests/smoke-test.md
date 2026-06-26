# smoke-test

## 目标

验证 Skill 在无第三方依赖环境下至少能完成：

- 脚本启动
- 扫描应用
- 推荐输出
- 搜索输出
- 非 macOS 环境下控制命令能安全失败
- macOS 环境下至少能解析 `control` 子命令

## 执行

```bash
python3 scripts/smoke_check.py
```

## 通过标准

输出 JSON，至少包含：

- `scan_apps`
- `recommendation_count`
- `search_method`
- `has_osascript`

## macOS 手工验证

在已授予“辅助功能 + 自动化”后，手工执行：

```bash
python3 scripts/music_skill.py control --app spotify --action status
python3 scripts/music_skill.py control --app spotify --action play
python3 scripts/music_skill.py play "周杰伦 稻香" --app spotify --control-mode macos-ui
```

观察：

- 是否返回 `ok: true`
- `status` 是否能拿到 state / artist / track
- `play <query>` 是否成功唤起搜索并开始播放


## 2.1 手工验证

```bash
python3 scripts/music_skill.py play "凤凰传奇 荷塘月色" --app spotify --control-mode macos-ui
SPOTIFY_ACCESS_TOKEN="<token>" python3 scripts/music_skill.py play "凤凰传奇 荷塘月色" --app spotify --control-mode macos-ui --spotify-market JP
```
