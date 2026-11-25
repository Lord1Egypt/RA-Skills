# motion.md — 动效语法:进入编排/悬停反馈/滚动驱动/剂量学

> 何时读我:给页面加动效、写 hover 反馈、做滚动驱动,或"页面是海报不像产品"要定位原因时。
> 最短路径:动效三段(进入/悬停/滚动)→剂量学→验收清单。
> 回 INDEX:SKILL.md「参考文档(30 秒路由)」。

> 边界:动效是时间性的——静态截图只能验证**终态**;本篇每条规则都有 _motionlab 渲染对照(好/坏两版),时序参数按实证标定,不凭感觉。

## M1 进入编排(渲染实证:终态=无动效版,像素级一致)

**判据**:错峰 60-120ms;位移 ≤32px;进入顺序=阅读顺序(标题先、主角随、支撑句最后)。
**证据**:好版(90ms 错峰)与无动效版 virtual-time 截图 **md5 一致**——进入编排只改变"如何到达",不改变"到达哪里";坏版(同时涌入 delay 0+60px)进入顺序与阅读顺序脱节。
**代码**:`.reveal{opacity:0;transform:translateY(24px);transition:opacity .7s ease,transform .7s ease}.reveal.in{opacity:1;transform:none}.reveal.d1{transition-delay:.09s}` + IntersectionObserver 加 .in(threshold .12,过即 unobserve)。

## M2 悬停反馈

**判据**:translateY ≤4px+阴影加深;transition 150-220ms;**⛔scale/rotate**(放大与旋转挤动邻居元素,audit motion_scale_hover 检查);reduced-motion 全关。
**证据**:好版(translateY(-2px)+阴影 180ms)=手指没按下去页面已回答;坏版(scale(1.3) 600ms)=布局抖动+反馈迟钝。
**代码**:`.btn{transition:transform .18s ease,box-shadow .18s ease}.btn:hover{transform:translateY(-2px);box-shadow:0 10px 26px rgba(17,22,30,.14)}`

## M3 滚动驱动(渐进增强:降级=完整功能)

**判据**:`animation-timeline: scroll()` 只许出现在 `@supports` 内;**基础态=完整功能**(进度条基础态满条,不支持动画的浏览器看到满条,不是零宽残条——实验修正实证:基础态 scaleX(0) 的"伪渐进"恰是要防的病);reduced-motion 内重置。
**代码**:`.bar{background:var(--accent);transform-origin:0 50%}@supports (animation-timeline: scroll()){.bar{transform:scaleX(0);animation:grow linear both;animation-timeline:scroll(root)}@media (prefers-reduced-motion:reduce){.bar{transform:none;animation:none}}}`

## M4 剂量学

1. **一页一主动效**(四幕配方的滚动揭示即主角);装饰动效每屏 ≤1(marquee_count 已闸);
2. **交互反馈不算装饰**(hover/press 是应答,剂量另计);
3. 进入事件每屏 ≤3(超过=页面在"表演"不是在"交付");
4. 全部动效必须有 reduced-motion 降级(三连:`opacity:1;transform:none;transition:none`)。

## M5 动效令牌

typescale/tokens 输出的 MOTION 令牌(dur-1 150ms/dur-2 300ms/dur-3 600ms)是**时长词汇表**:悬停=dur-1,过渡=dur-2,幕转=dur-3;自定义时长先对齐令牌再偏离,偏离要有理由。

## 验收清单

- [ ] 进入编排:错峰 60-120ms、位移 ≤32px、顺序=阅读顺序、终态与无动效一致
- [ ] hover:translateY ≤4px+阴影,150-220ms,无 scale/rotate(motion_scale_hover 零命中)
- [ ] transition 无 ≥0.5s 的悬停/反馈(motion_lag 零命中)
- [ ] 滚动驱动:@supports 包裹+基础态完整+reduced-motion 重置
- [ ] 全部动效 reduced-motion 三连
- [ ] 无 JS 时内容完整可见(CSS 基础态=完整)
