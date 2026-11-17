# typography-aesthetics.md — 字体美学:气质光谱/中西文配对/排印戏剧/资产管线

> 何时读我:给页面选字体、配中西文字对、写大字号标题,或"字发糊/发虚"要定位原因时。
> 最短路径:气质光谱→中西文配对表→假粗禁令(降级链)→排印戏剧→--fonts 资产管线→验收清单。
> 回 INDEX:SKILL.md「参考文档(30 秒路由)」。

> 边界:不替代 typography-system.md 的卫生学规则(autospace/字距/行高),本篇在其上叠加美学判断;每条规则都有渲染对照证据(_fontlab 实验),不凭感觉说话。

## 一、合成粗禁令(P0,本卷头号规则)

**判据**:页面出现 `font-weight:800/900` 且全文无 `@font-face` 声明真字重 → FAIL。lint 可判定:`font-weight\s*[=:]\s*(8|9)00` 与 `@font-face` 互斥检查。
**证据**:微软雅黑仅有 Regular/Bold/Light——w900 = 真 Bold 之上再叠合成加粗,112px 特写下"黑"字四点底粘成实心块、字腔被墨填死;宋体+合成粗会把"横细竖粗"的字族气质整体涂平。text-stroke 描边是另一种坏(圆角洇墨、笔画骨架仍是 Regular),**只许用于幽灵数字等装饰性半透明元素,禁用于标题**。
**合法降级链(宁细勿假粗)**:①子集真 Black(资产管线,见第五节)→ ②系统已装真字重(可变字体)→ ③**700 封顶**(系统栈真 Bold 是上限)→ ④SimHei 400(唯一自带"黑"的系统字)→ ⑤宋体 400+大字号(复古路线,仅 ≥28px)。

## 二、字体气质光谱

| 字族 | 代表(免费可得) | 气质 | 适用语域 | 可判定特征 |
|---|---|---|---|---|
| 宋体族·现代衬线 | 思源宋/Noto Serif SC(OFL,全字重 200-900) | 编辑权威、文化厚度 | 杂志/品牌叙事/巨标 | 横细竖粗对比鲜明;中宫收紧;一族全字重 |
| 黑体族·现代无衬线 | 思源黑/Noto Sans SC(OFL,100-900) | 工程现代、数据可信 | SaaS/数据页/UI | 笔画等粗;字面率大;中宫开 |
| 楷体/手写 | 霞鹜文楷 LXGW WenKai(OFL) | 人文手写、温度、批注 | 引文/批注/人文标题;正文 18px 实测舒适 | 起笔收笔楷书笔意;字面率小→行内留白松 |
| 黑体族·legacy | 微软雅黑/黑体 SimHei | 中性无个性 | 正文兜底;**禁止 display** | 雅黑 800/900 必合成(禁令);SimHei 仅 400 但笔画真"黑" |
| 宋体·legacy | 宋体 SimSun | 旧报纸/公文 | 复古档案特化;标题只许 400+大字号 | 小字号有位图感;无任何粗字重 |
| 仿宋/圆体 | FangSong/SIMYOU | 公文信札/软萌促销 | 政务特化/电商促销(讲究页基本禁圆体) | 均细瘦长/端点圆头 |

字体源:思源系全字重从 Google Fonts 与镜像可达,但 skill 离线铁律 → **正道是现场子集自托管**(第五节);霞鹜文楷走 GitHub releases。

## 三、中西文配对表(全部渲染目审过)

判据三件套:①笔画对比一致性(衬线配衬线);②x-height/字面率接近(混排行不忽大忽小);③数字气质合拍。

| 配对 | 判据要点 | 完整栈 |
|---|---|---|
| 思源宋 Black × Georgia(首推) | 中高对比都属;Georgia 大 x-height 扛得住中文密度;old-style 数字添编辑味 | `Georgia,'Noto Serif SC','Source Han Serif SC','Songti SC',serif` |
| 思源黑 × Segoe UI(工程首推) | 人文开口 vs 几何,刚柔互济;数字清瘦合数据页 | `'Segoe UI','Noto Sans SC','Microsoft YaHei',sans-serif` |
| 楷体(文楷)× Georgia italic | 手写斜度互相呼应;引文块 Latin 用 `font-style:italic` | `Georgia,'LXGW WenKai','KaiTi',serif` |
| 思源宋 × Constantia | 更书房/人文;old-style 数字更花 | `Constantia,'Noto Serif SC',serif` |
| 同族自托管 | 零违和最稳 | `'Noto Serif','Noto Serif SC',serif` / `'Noto Sans','Noto Sans SC',sans-serif` |
| 宋体 × Georgia(复古特化) | 报纸密度;标题仅 400 且 ≥28px | `Georgia,SimSun,serif` |

弃收:思源宋 × Cambria(display 级发闷,低对比配高对比=气质打架)。待渲染验证:思源黑×Inter、文楷 Bold、macOS 侧栈。

## 四、排印戏剧规则(渲染验证)

1. **级差张力律**:相邻级差 ≥1.25 肉眼才辨层级(1.125 三级实测"靠猜");**正文页 `--ratio:1.414` 是编辑感甜点**(typescale 默认),海报/单屏页 1.8-2;多级页用 2.0 时中间级"悬浮"。
2. **行长呼吸律**:30-38 字/行 = 甜点(`max-inline-size:30em-38em`);22 字/行碎(诗可用);46 字/行扫视成本可见上升,须行高 1.8+ 补偿。
3. **巨标三位一体**:`font-weight:900 + letter-spacing:0~0.015em + line-height:1.05-1.15` 是唯一推荐组合;lh 1.35 实测断;display 感消失;ls 0.05em 实测散;中文负字距实测笔画碰撞(再证禁令)。400 细巨字=空灵文艺路线,合法但必须配大留白;黑体 400 巨字单薄禁用。
4. **数字戏剧律**:oversized metric=数字为标签 3-5 倍、w900、line-height:1、baseline 对齐、单位缩至 0.25 倍转 muted;表格 tabular-nums(仪器读数),正文叙述保持比例数字。

## 五、字体资产管线(--fonts,0.18 接线规范)

1. **收集**:剥 `<style>/<script>/标签` 后扫 CJK 区段(`\u2E80-\u9FFF\uF900-\uFAFF\uFF00-\uFFEF`+全角标点),保序去重;
2. **子集**:fonttools varLib.instancer 实例化 VF(wght=900)→ pyftsubset `--text=<用字> --flavor=woff2`;实测 47 字=8.3KB/321 字=51KB/749 字=124KB;
3. **内嵌**:`@font-face{font-family:"Aesthete Serif";src:url(...woff2) format("woff2");font-weight:900;font-display:swap}` + `--serif:'Aesthete Serif',<原降级链>`;
4. **缓存**:`%LOCALAPPDATA%/aesthete/fontcache/serif900-<sha1(文本)>.woff2`,同文案零重复开销;
5. **预置**:随 skill 附 2 个通用子集约 60KB(高频标题字+高频 300 字,OFL 允许再分发),`--fonts preset` 零依赖可用;`auto` 缺 fonttools 时降级 preset+系统栈并提示一行 pip 安装;
6. **lint 联动**:管线激活(`--fonts preset|auto`)后才放行 900;`--fonts none` 时 type_kit 的 `--weight-hero` 钳到 700。

## 验收清单

- [ ] 无 @font-face 时全文无 800/900(禁令)
- [ ] 标题无 text-stroke(幽灵数字等装饰除外)
- [ ] 中西文配对出自第三节表格(或已渲染验证的新对)
- [ ] 巨标满足三位一体;级差 ≥1.25;行长 30-38 字
- [ ] 数字页 tabular-nums;oversized metric 合规
- [ ] 子集产物 ≤200KB 且 font-display:swap
