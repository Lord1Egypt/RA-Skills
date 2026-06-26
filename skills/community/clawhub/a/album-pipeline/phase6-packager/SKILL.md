# Phase 6 — Packager Skill

> 最终打包：将所有文档文件压缩为宣传物料 zip 包，完成专辑流水线。

---

## 触发

phase6-platform-checker 全部通过后自动启动。

---

## 输入

| 来源 | 文件 | 内容 |
|------|------|------|
| Phase 6 | `docs/album-overview.md` | 专辑统筹文档（完整更新） |
| Phase 6 | `docs/promotional-materials.md` | 宣传文档 |
| Phase 6 | `docs/artist-story-cn.md` | 艺人说中文长版 |
| Phase 6 | `docs/artist-story-en.md` | 艺人说英文长版 |
| Phase 6 | `docs/artist-story-short.md` | 艺人说中英文短版 |
| Phase 6 | `docs/artist-story-quotes.md` | 金句提取 |
| Phase 6 | `docs/cover-concept.md` | 封面概念方案 |
| Phase 6 | `docs/platform-check.txt` | 平台适配检查报告 |

---

## 执行

### ⚠️ 修改范围
- **读取**：Phase 6 所有文档文件 + `generate/covers/` 封面图 + `docs/promo-video*.mp4` 宣传视频
- **写入**：`<专辑名>-宣传物料.zip`
- **禁止**：修改任何源文档文件

### 打包命令

```bash
cd <project-root>
zip -r <专辑名>-宣传物料.zip \
  docs/album-overview.md \
  docs/promotional-materials.md \
  docs/cover-concept.md \
  docs/artist-story-cn.md \
  docs/artist-story-en.md \
  docs/artist-story-short.md \
  docs/artist-story-quotes.md \
  docs/platform-check.txt \
  generate/covers/album-cover-p1.png \
  generate/covers/album-cover-p2.png \
  generate/covers/album-cover-p3.png \
  generate/covers/tracks/ \
  docs/promo-video.mp4 \
  docs/promo-video-15s.mp4
```

### 最终交付物清单

**文档（zip 内）：**

| 文件 | 内容 | 状态 |
|------|------|------|
| `docs/album-overview.md` | 专辑统筹文档（完整） | ✅ |
| `docs/promotional-materials.md` | 宣传文档 | ✅ |
| `docs/artist-story-cn.md` | 艺人说中文长版 | ✅ |
| `docs/artist-story-en.md` | 艺人说英文长版 | ✅（纯中文/纯英文专辑仍建议生成，用于国际发行参考） |
| `docs/artist-story-short.md` | 艺人说中英文短版 | ✅ |
| `docs/artist-story-quotes.md` | 金句提取 | ✅ |
| `docs/cover-concept.md` | 封面概念方案 | ✅ |
| `docs/platform-check.txt` | 平台适配检查 | ✅ |

**封面图（zip 内）：**

| 文件 | 内容 | 状态 |
|------|------|------|
| `generate/covers/album-cover-p1.png` | 专辑封面 版本1（概念忠实型） | ✅ |
| `generate/covers/album-cover-p2.png` | 专辑封面 版本2（情绪氛围型） | ✅ |
| `generate/covers/album-cover-p3.png` | 专辑封面 版本3（极简符号型） | ✅ |
| `generate/covers/tracks/T{N}-曲名-p{1,2,3}.png` | 单曲封面（N首 × 3版本） | ✅ |

**宣传视频（zip 内）：**

| 文件 | 内容 | 状态 |
|------|------|------|
| `docs/promo-video.mp4` | 宣传视频完整版（25-30秒） | ✅ |
| `docs/promo-video-15s.mp4` | 宣传视频精简版（15秒） | ✅ |

**音频（独立目录，不在 zip 内）：**

| 目录 | 内容 | 状态 |
|------|------|------|
| `generate/cn_320k/` | 中文最终音频（N 首） | ✅ |
| `generate/en_320k/` | 英文最终音频（N 首） | ✅ |

**其他：**

| 文件 | 内容 | 状态 |
|------|------|------|
| `<专辑名>-宣传物料.zip` | 文档压缩包 | ✅ |
| `generate/loudness-report.txt` | 响度/时长报告 | ✅ |

### 上传清单（给用户）

生成一份上传元数据清单，方便用户手动上传到平台：

```
[网易云音乐上传清单]

专辑名：《{中文名}》
艺人：{艺人名}
专辑描述：{from album-overview.md}
**封面（新增）：**
封面：`generate/covers/album-cover-p1.png`（推荐版本1，另有 p2/p3 备选）
单曲封面：`generate/covers/tracks/T{N}-曲名-p{1,2,3}.png`

**宣传视频（新增）：**
完整版：`docs/promo-video.mp4`
精简版：`docs/promo-video-15s.mp4`

曲目列表：
01. T1 {曲名} - {时长}
02. T2 {曲名} - {时长}
...
{N}. TN {曲名} - {时长}

音频文件路径：
generate/cn_320k/T1-曲名-pX.mp3
generate/cn_320k/T2-曲名-pX.mp3
...

歌词文件路径：
generate/lyrics/cn/T1-曲名.txt
generate/lyrics/cn/T2-曲名.txt
...
```

---

## Checklist

| # | 检查项 | 打勾标准 |
|---|--------|---------|
| 1 | zip 内容完整 | 包含全部 8 个文档文件 |
| 2 | zip 可正常解压 | 无损坏，文件完整 |
| 3 | 音频目录齐全 | cn_320k/ N 首 + en_320k/ N 首 |
| 4 | 上传清单已生成 | 包含专辑名/曲目列表/文件路径 |
| 5 | 所有 Phase 待办标记 [x] | `docs/album-overview.md` 待办事项全部完成 |

全部 ✅ → 🎉 Phase 6 完成，专辑流水线全部结束！
