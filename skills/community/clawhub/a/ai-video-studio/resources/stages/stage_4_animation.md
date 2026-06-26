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

### 4.2 强制预检（渲染前的最后防线）

```bash
export PATH=./bin:$PATH
npx hyperframes@latest inspect YYYYMMDD/
```

**✅ Stage 4 退出标准（必须全部满足，才允许执行 render）：**
- [ ] `inspect` 命令退出码为 0（无报错）
- [ ] 控制台输出的 `totalDuration` 与 Stage 2.1 测量的音频时长误差 < 0.2 秒
- [ ] 无任何 `StaticGuard` 警告

### 4.3 渲染导出

```bash
export PATH=./bin:$PATH
# 强制渲染到项目renders目录下
npx hyperframes@latest render YYYYMMDD/ -o YYYYMMDD/renders/promo_video.mp4 --force-new
```
