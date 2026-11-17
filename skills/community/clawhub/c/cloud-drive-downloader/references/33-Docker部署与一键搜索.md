# Docker/NAS 部署与一键搜索下载

## 一键搜索下载（search→download）

```bash
python3 scripts/pan.py search "关键词" --kind movie --json
python3 scripts/pan.py search "关键词" --kind movie --pick 1 --to ~/下载 --dry-run
python3 scripts/pan.py search "歌曲" --kind music --pick 2 --remote nas
```

- 内置公开源：archive.org（公版电影/音频）、DuckDuckGo 网页候选、yt-dlp 公开视频搜索。
- `--providers archive,duckduckgo,ytdlp` 限源；`--limit N` 调数量；`--json` 供 Agent 解析。
- 只列公开/公版/你有权下载的内容；网页候选在下载前请确认授权。不破解会员、验证码、限速或风控。

## Docker / NAS 部署

```bash
python3 scripts/pan.py docker --out /path/pan-docker
# 把 pan-docker 目录拷到 NAS（群晖 Container Manager / 威联通 / 飞牛 / TrueNAS）后：
# cd pan-docker && bash install.sh
```

- 镜像 python:3.11-slim，内置 curl、aria2、yt-dlp、ffmpeg、ssh 客户端，默认 listen 0.0.0.0:17890。
- `state/`（config/task）与 `download/` 用卷挂载持久化。
- 容器不包含、不上传本机 config.json / Cookie / Token；登录态在容器内重新配置，符合公司数据不上云红线。
- 需要改版本时 docker compose up -d 前先 `docker compose build`（Dockerfile 与 compose 都生成在目标目录）。
