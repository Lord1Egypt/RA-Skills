> 何时读我:需要从 the source site 收割新调色板数据时(先读 5 个实测坑)。
> 最短路径:已知事实→配方→四坑→纪律。
> 回 INDEX:SKILL.md「参考文档(30 秒路由)」。

# 从 the source site 收割调色板的浏览器配方(2026-10-15 实测)

目的:扩充 `palettes/palettes.json`。用 ZCode 内置浏览器(browser-use:control-browser)过 Cloudflare 后从 Explore 页抽取真实调色板数据。**先读完本文再动手**,四个坑都是实测踩出来的。

## 已知事实(勿重复验证)

- **无公开 API**:`the source site/api/*`、`/api/palettes/*` 等 curl 直连全部 HTTP 403(Cloudflare "Just a moment"),无论带什么 UA。WebFetch 同样 403。
- **web_reader MCP 工具能过 Cloudflare** 抓静态文本(主页/generate/contrast-checker/color-picker 都成功),但 Explore 列表页是 JS 渲染,web_reader 拿不到卡片数据——必须真浏览器。
- **每页固定 48 张**,分页按钮形同虚设(见坑③)。
- 页面 DOM 结构:`.palette-card` > `.palette-card_colors > div[style*=background] > span`(hex 文本);浅色块带 `is-light` 类(the source site 自己的黑白文字决策,收割存进 text_hint);名称 `.palette-card_name`,点赞 `.palette-card_save-btn span`。
- Style 过滤枚举:warm/cold/bright/dark/pastel/vintage/monochromatic/gradient;排序枚举:TRENDING/LATEST/POPULAR;导出格式:HEX/RGB/HSB/CMYK/LAB/NAME/RAL/HKS/COPIC/PRISMACOLOR;变体视图:COVER/COLORS/SHADES/CONTRAST/TEMPERATURE/HUE/SATURATION/BLINDNESS/LUMINANCE/GRADIENT。

## 配方

1. **开页**:`agent.browsers.getForUrl("https://the source site/palettes/trending")` → 新 tab → goto → `waitForLoadState("domcontentloaded")`。Cloudflare 挑战页标题是"请稍候…",**等 5-8 秒**自动放行(无需点击),以 `tab.title()` 变为 "Trending Color Palettes - the source site" 为准。
2. **关欢迎弹窗**(坑①):出现 "Howdy!" 弹窗时,点 `.modal.is-visible .modal_close-btn` **经常无效**(body 仍带 `has-modal` 类)。直接 DOM 手术:
   ```js
   document.querySelectorAll('.modal.is-visible').forEach(m => m.classList.remove('is-visible'));
   document.querySelectorAll('.modal').forEach(m => m.style.display='none');
   document.body.classList.remove('has-modal','has-popover');
   ```
3. **抽取**(每页 48 张,够用了):
   ```js
   JSON.stringify([...document.querySelectorAll('.palette-card')].map(c => ({
     name: c.querySelector('.palette-card_name')?.textContent.trim(),
     likes: c.querySelector('.palette-card_save-btn span')?.textContent.trim(),
     hexes: [...c.querySelectorAll('.palette-card_colors > div')].map(d => ({
       hex: d.querySelector('span')?.textContent.trim(),
       light: d.classList.contains('is-light') }))
   })))
   ```
4. **入库**:用本 skill 配套的去重+风格标签逻辑处理(参考 harvest 脚本:classify 用 HSL 统计打 warm/cool/light/dark/pastel/vivid/monochromatic/multihue/deep 标签,likes "34.9K" 解析为数值,无名卡丢弃)。

## 四个实测坑

1. **欢迎弹窗关闭按钮点击无效**(见上,直接改 class/样式)。
2. **`playwright.evaluate` 只接受单表达式**:传 `() => {...}` 箭头函数返回值会丢失(空对象),传多语句字符串报 SyntaxError。**用 IIFE 字符串** `(() => { ... return JSON.stringify(x) })()`;返回值经桥接自动反序列化成对象,不要再 JSON.parse。
3. **"Load more" 按钮点不动 + `?page=N` 被忽略**:按钮存在但 0×0 不可见,点击/滚动/改 class/URL 加 page 参数都不加载第二页(2026-10 两次实测)。匿名状态每页固定 48,别耗时间。
4. **排序 `<select>` 是隐藏控件**:DOM 里有 TRENDING/LATEST/POPULAR,但改 value+dispatch change 不触发重取,a11y 树里也没有它(自绘组件)。**但它的 option value 揭示了 URL 方案**:`/palettes/trending|latest|popular` 直接可达(48 张/页,收割主通路)。
5. **风格过滤 URL 是 SEO 克隆页(2026-10-15 二次实测)**:`/palettes/pastel|vintage|dark|...` 页面 H1 正确("Pastel Color Palettes")但卡片列表与 popular 完全相同(头部条目一致、各风格覆盖数完全均一)——真实过滤是客户端的,匿名状态搜索框/megasearch 标签点击也全部无响应。**不要用风格页数据,不要据此打官方风格标签。**

## 收割纪律

- 单次会话收割 ≤ 数页,别把站当 API 滥用(它是创作者的免费产品)。
- 入库必须带 `source` 与 `harvested` 日期,保留原始 likes;未在站上出现的调色板不许混进 harvest 来源字段。
- 收割脚本(去重/打标签/写库)复用 build_library 流水线的去重+打标逻辑。
