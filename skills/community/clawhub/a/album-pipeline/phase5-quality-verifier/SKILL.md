# Phase 5 — Quality Verifier Skill

> 转码后全面验证，确保符合平台标准（320kbps/44.1kHz/-14 LUFS）。

---

## 触发

主 agent 完成所有 ffmpeg 转码后自动启动。

---

## 输入

| 来源 | 文件 | 内容 |
|------|------|------|
| Phase 5 | `generate/cn_320k/T{N}-曲名-pX.mp3` | 中文转码文件 |
| Phase 5 | `generate/en_320k/T{N}-曲名-pX.mp3` | 英文转码文件 |

---

## 执行

### ⚠️ 修改范围
- **读取**：`generate/cn_320k/*.mp3`、`generate/en_320k/*.mp3`
- **写入**：`generate/loudness-report.txt`
- **禁止**：修改任何 .mp3 文件

### 验证项目

#### 1. 格式验证（ffprobe）

```bash
ffprobe -v error -show_entries format=bit_rate:stream=sample_rate -of json output.mp3
```

确认：
- `bit_rate` = 320000 ✅
- `sample_rate` = 44100 ✅

#### 2. 时长验证

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 output.mp3
```

确认：
- 时长 ≥ 1:00（60 秒）✅
- 时长 ≤ 6:00（360 秒）✅

#### 3. 响度验证

使用 ffmpeg loudnorm 滤镜二次验证：

```bash
ffmpeg -i output.mp3 -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -
```

确认：
- 集成响度（I）：-14 LUFS ± 0.5 LUFS ✅
- 真实峰值（TP）：≤ -1.5 dBTP ✅

#### 4. 文件完整性

- 文件大小 ≥ 100KB
- 可正常播放（无静音/爆音/截断）

### 输出报告

生成 `generate/loudness-report.txt`：

```
[响度/时长验证报告]
日期：YYYY-MM-DD

T1-出发    CN: -13.8 LUFS | 3:24 | 320kbps | 44.1kHz | ✅
T1-出发    EN: -14.1 LUFS | 3:55 | 320kbps | 44.1kHz | ✅
T2-数据    CN: -13.9 LUFS | 2:14 | 320kbps | 44.1kHz | ✅
...

汇总：
CN版：N/N 通过
EN版：N/N 通过
总计：2N/2N 通过
```

---

## Checklist

| # | 检查项 | 打勾标准 |
|---|--------|---------|
| 1 | bit_rate = 320000 | 所有文件 ffprobe 验证通过 |
| 2 | sample_rate = 44100 | 所有文件 ffprobe 验证通过 |
| 3 | 响度 -14 ± 0.5 LUFS | 所有文件响度验证通过 |
| 4 | 时长 1:00-6:00 | 所有文件时长验证通过 |
| 5 | 文件完整性 | 无静音/爆音/截断，大小 ≥ 100KB |
| 6 | loudness-report.txt 已生成 | 包含每首的详细数据 |
| 7 | cn_320k 文件数 = 曲目数 | 无遗漏 |
| 8 | en_320k 文件数 = 曲目数（双语/英文专辑检查） | 纯音乐/纯中文专辑可能无 en_320k/ 目录，此项跳过 |

全部 ✅ → 进入 Phase 6（发布物料打包）
