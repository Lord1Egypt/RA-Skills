# 过渡效果库

> 视频片段之间的视觉过渡方式。

## 常用过渡效果

| 效果 | 参数 | 时长建议 |
|------|------|---------|
| 淡入淡出 | `fade` | 0.3-0.8s |
| 向右滑入 | `wiperight` | 0.5-1s |
| 向左滑入 | `slideleft` | 0.5-1s |
| 矩形收缩 | `rectcrop` | 0.5s |
| 圆形扩散 | `circleclose` | 0.8s |
| 无过渡 | `none` | — |

## 使用方式（xfade）

```bash
ffmpeg -i part1.mp4 -i part2.mp4 -filter_complex \
  "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=T[outv]" \
  -map "[outv]" -c:v libx264 "$out"
```

- `transition`：过渡类型
- `duration`：过渡持续时间
- `offset`：第二个视频开始过渡的时间点

## 多段过渡（链式 xfade）

```bash
# n 段需要 n-1 次 xfade
# 每段拼接后递归应用
```

## 硬切（无过渡）

```bash
ffmpeg -f concat -safe 0 -i concat.txt -c copy "$out"
```

默认无过渡，适合快节奏内容（如喜剧快切）。

## 叠化（Cross Dissolve）

淡入淡出的电影感版本：

```bash
ffmpeg -i part1.mp4 -i part2.mp4 -filter_complex \
  "[0:v][1:v]blend=all_expr='A*if(gt(T,T0),1)+B*if(lt(T,T0),1)'[outv]" \
  -map "[outv]" -c:v libx264 "$out"
```