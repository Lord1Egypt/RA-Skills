# usage examples

## 1. 扫描本机音乐软件

```bash
python3 scripts/music_skill.py scan
```

## 2. 打开 Spotify

```bash
python3 scripts/music_skill.py open --app spotify
```

## 3. 搜索《稻香》

```bash
python3 scripts/music_skill.py search "周杰伦 稻香" --app spotify --open
```

## 4. 直接控播（macOS）

```bash
python3 scripts/music_skill.py control --app spotify --action play
python3 scripts/music_skill.py control --app spotify --action next
python3 scripts/music_skill.py control --app spotify --action status
```

## 5. 按需求尽力开始播放（macOS）

```bash
python3 scripts/music_skill.py play "适合写代码的 lofi" --app spotify --control-mode macos-ui
python3 scripts/music_skill.py play "周杰伦 稻香" --app apple-music --control-mode macos-ui
```

## 6. 推荐并播放

```bash
python3 scripts/music_skill.py recommend "适合跑步的歌"
python3 scripts/music_skill.py play "workout hits" --app spotify --control-mode macos-ui
```

## 7. 播放本地文件

```bash
python3 scripts/music_skill.py play --file "~/Music/demo.mp3" --app vlc --open
```

## 8. Spotify 精确点播（推荐）

```bash
export SPOTIFY_ACCESS_TOKEN="<你的 access token>"
python3 scripts/music_skill.py play "凤凰传奇 荷塘月色" --app spotify --control-mode macos-ui --spotify-market JP
```

## 9. Spotify 无 token 退化模式

```bash
python3 scripts/music_skill.py play "凤凰传奇 荷塘月色" --app spotify --control-mode macos-ui
```
