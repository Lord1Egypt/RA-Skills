# 喜剧节奏剪辑 — Comedy Timing

> 适用：脱口秀、开放麦等喜剧视频，强调节奏感和笑点留白。

## 笑点留白原则

喜剧剪辑和普通纪录片剪辑不同：
- **纪录片**：紧凑，不留空白
- **喜剧**：笑点后留 0.3-0.8 秒喘息空间

## 节奏参数

| 笑点类型 | 建议留白 | 参数 |
|---------|---------|------|
| 大笑点（全场笑） | 0.8-1.2s | 手动调整 |
| 中等笑点 | 0.5-0.8s | 手动调整 |
| 小笑点（个别笑） | 0.3-0.5s | 手动调整 |

## 放大笑点镜头（zoompan）

笑点时刻放大画面：

```bash
ffmpeg -i "$in" -vf "zoompan=z='if(between(t,X,Y),1.4,1)':d=1:s=1920x1080:enable='between(t,A,B)'" -c:v libx264 "$out"
```

- 启用时段：`A` 到 `B`（秒）
- 放大倍数：`1.4`（1.0 = 不放大）
- 目标分辨率：`1920x1080`

## 喜剧快切节奏

快速切换多个笑点片段：

```bash
ffmpeg -i "$in" -vf "select='eq(n,X)+eq(n,Y)+eq(n,Z)',setpts=N/(FPS*TB)" -r 30 "$out"
```

## 语速加速（压缩留白）

让语速略快，拉近笑点间距：

```bash
ffmpeg -i "$in" -vf "setpts=0.9*PTS" -af "atempo=1.1" -c:v libx264 "$out"
```

- `setpts=0.9*PTS`：视频加速 10%
- `atempo=1.1`：音频加速 10%（保持音高）

## 静音/弱音处理

笑点前的铺垫略微降音量，突出笑点：

```bash
ffmpeg -i "$in" -af "volume=enable='lt(t,X)':volume=0.7" -c:v libx264 "$out"
```

- 0-B 秒音量降为 70%

## 笑点时间戳标注（输出为 JSON）

分析视频，输出一份建议剪辑点：

```bash
ffmpeg -i "$in" -af "silencedetect=noise=-30dB:d=0.3" -f null -
```

- 检测静音段（可能是观众笑声）
- 配合手动标注使用