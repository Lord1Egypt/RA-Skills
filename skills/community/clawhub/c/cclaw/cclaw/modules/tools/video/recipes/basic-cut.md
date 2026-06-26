# 基础剪辑 — Basic Cut

> 适用：删除片段、截取片段、简单剪切。

## 删除片段

删除第 A 秒到第 B 秒：

```bash
ffmpeg -i "$in" -vf "trim=start=X:end=Y,setpts=PTS-STARTPTS,asetpts=EXTRACT" -af "atrim=start=X:end=Y,asetpts=EXTRACT" -c:v libx264 -c:a aac "$out"
```

**快捷版**（无损流复制，需精确帧对齐）：

```bash
ffmpeg -i "$in" -c copy -avoid_negative_ts make_zero "$out"
```

## 截取片段

截取第 A 秒到第 B 秒：

```bash
ffmpeg -i "$in" -ss A -to B -c:v libx264 -c:a aac -avoid_negative_ts make_zero "$out"
```

## 删除中间段（多段）

删除 A-B 和 C-D（两段都要删除）：

```bash
ffmpeg -i "$in" \
  -vf "trim=0:end=X,setpts=PTS-STARTPTS" -t X \
  -f lavfi -t 0 -i "anullsrc=channel_layout=stereo:sample_rate=48000" \
  -vf "trim=start=Y,setpts=PTS-STARTPTS" -ss Y \
  -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0[outv]" \
  -map "[outv]" -c:v libx264 "$out"
```

## 参数速查

| 参数 | 说明 |
|------|------|
| `-ss A -to B` | 从 A 秒到 B 秒 |
| `-c copy` | 无损流复制（仅剪切无重编码） |
| `-avoid_negative_ts` | 处理时间戳负值 |
| `-setpts PTS-STARTPTS` | 重置视频 PTS |
| `-asetpts EXTRACT` | 重置音频 PTS |