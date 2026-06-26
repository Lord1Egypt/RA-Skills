# Stage 4：动画集成与预检发版

### 4.1 加入 GSAP 动画

在静态验收通过后，才可加入动效。可用动画菜单：

| 动效 | 代码模板 | 适用场景 |
|------|---------|--------|
| Ken Burns 缩放 | `fromTo(img, {scale:1.0}, {scale:1.06, ease:"none"})` | 所有场景默认 |
| Ken Burns 平移 | `fromTo(img, {x:-20}, {x:0, ease:"none"})` | 宽场景横向扫描 |
| 字幕淡入 | `from(sub, {opacity:0, y:20, duration:0.8, ease:"power2.out"})` | 所有场景可选 |
| 场景交叉淡化 | `to(div, {opacity:0, duration:0.5}, start+duration-0.25)` | 场景过渡 |
| 光晕脉冲 | `to(glow, {opacity:0.4, repeat:-1, yoyo:true, duration:2})` | 火焰/光源场景 |

### 4.1.1 情绪驱动转场匹配

场景之间的转场不应千篇一律。根据**下一幕的情绪档位**选择对应转场：

| 下一幕情绪档位 | 转场方式 | GSAP 代码 | 视觉效果 |
|-------------|---------|----------|--------|
| 1（舒缓叙事） | 慢溶解 | `fromTo(next, {opacity:0}, {opacity:1, duration:1.2, ease:"power1.inOut"})` | 平静过渡，如水墨晕染 |
| 2（紧张蓄力） | 标准交叉淡化 | `fromTo(next, {opacity:0}, {opacity:1, duration:0.5, ease:"none"})` | 默认节奏 |
| 3（高潮爆发） | 硬切 + 微缩放 | `tl.set(next, {opacity:1}); fromTo(next, {scale:1.05}, {scale:1.0, duration:0.3})` | 冲击感 |
| 4（沉默留白） | 淡入黑 → 淡出黑 | `先 to(prev, {opacity:0, duration:0.8}), 延迟 0.5s, 再 fromTo(next, {opacity:0}, {opacity:1, duration:1.0})` | 呼吸感，给观众消化时间 |

### 4.1.2 场景生命周期显隐控制与变量自适应绑定（重大动效架构红线）

为了彻底杜绝多个大场景在时序切换时的 DOM 重合堆叠冲突，必须在 GSAP 动画设计中无条件执行生命周期隐藏控制：
1. **隐藏状态机规范**：
   在 `style.css` 中将所有非活动分镜的内部容器（如 `.scene-content`）默认设为 `opacity: 0; visibility: hidden;`。
2. **GSAP 显隐切换控制**：
   在 GSAP timeline 编写中，必须在每个分镜场景切入的瞬间通过 `tl.set` 激活，并在退出的瞬间隐藏：
   ```javascript
   // 当场景 scene1 激活时开启可见，退出或到下一场景 scene2 时隐藏，防止 DOM 悬空堆叠
   tl.set("#scene1-content", { visibility: "visible" }, SCENE_START.scene1);
   tl.set("#scene1-content", { visibility: "hidden" }, SCENE_START.scene2);
   ```
3. **变量化解耦绑定**：
   禁止在 GSAP timeline 的动效注册中使用任何绝对硬编码的时间戳数值（如 `12.0`）。必须在 JS 头部声明自适应时间变量 `const SCENE_START` 并将所有动效与其绑定偏移（例如 `SCENE_START.scene1 + 2.78`），确保音频时间轴微调时动效自动、平滑地整体平移。


### 4.2 强制预检（渲染前的最后防线）

```bash
export PATH=./bin:$PATH
npx hyperframes@latest inspect YYYYMMDD/
```

**✅ Stage 4 退出标准（必须全部满足，才允许执行 render）：**
- [ ] `inspect` 命令退出码为 0（无报错）
- [ ] 控制台输出的 `totalDuration` 与 Stage 2.1 测量的音频时长误差 < 0.2 秒
- [ ] 无任何 `StaticGuard` 警告

### 4.2.1 渲染前集成检查清单（⛔ 全部通过方可执行 render）

在执行 `npx hyperframes render` 之前，必须逐一确认以下事项。**任意一项未通过，严禁渲染。**

| # | 检查项 | 验证方法 |
|---|--------|---------|
| 1 | 封面标题幕存在 | `grep 'scene_cover' index.html` 返回结果 |
| 2 | 封底互动幕存在 | `grep 'scene_end' index.html` 返回结果 |
| 3 | 逐字同步字幕存在 | `grep 'subtitles-track' index.html` 且 `grep 'caption-word\|CAPTIONS_DATA' index.html` 返回结果 |
| 4 | 配音音频就位 | `ffprobe assets/narration.wav` 成功且时长 > 0 |
| 5 | BGM 就位且为新文件 | `ffprobe assets/bgm.mp3` 成功，且 `视频脚本.md` 中有本集 BGM 署名（含曲名和来源） |
| 6 | 所有视频素材就位 | `ls assets/scene*.mp4 \| wc -l` == 剧本分镜数，且每个文件通过 `ffprobe` 校验 |
| 7 | 素材为本集新下载 | `download_and_process.py` 中 URL 不与任何旧集重复 |
| 8 | lint 零错误 | `npx hyperframes lint` 报 0 error(s) |

### 4.3 渲染导出

```bash
export PATH=./bin:$PATH
# 强制渲染到项目renders目录下
npx hyperframes@latest render YYYYMMDD/ -o YYYYMMDD/renders/promo_video.mp4 --force-new
```
