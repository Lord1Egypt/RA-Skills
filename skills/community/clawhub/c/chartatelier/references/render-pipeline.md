# 渲染与导出管线

> 管线分四段：抽取独立 SVG → 定画布 → 渲染 PNG → 校验像素。任一段跳过都会得到“看起来有文件、实际不能用”的废品。

## 一、四段管线

| 段 | 动作 | 产物 | 完成判据 |
|---|---|---|---|
| 1. 抽取 | 从 HTML 里取出 `<svg>`，补上 `xmlns`、显式 `width` / `height` | `diagram.svg` | 单独打开 SVG 显示完整、不裁切 |
| 2. 定画布 | viewBox 收紧到内容外接框 + 10–20px | 更新后的 `diagram.svg` | 内容覆盖画布 ≥95% |
| 3. 渲染 | Playwright 或 Chrome 无头截图，倍数 2 或 3 | `diagram@2x.png` | 像素宽 = 逻辑宽 × 倍数 |
| 4. 校验 | 读回 PNG，查尺寸与覆盖率 | `qa-report.json` | 五项全绿 |

## 二、抽取独立 SVG 的三条规则

1. **width / height 必须是显式像素**，等于 viewBox 的第三、四个数。写 `100%` 在 `file://` 下不会填满视口，截图只剩左上角一小块。
2. **补全命名空间**：`<svg xmlns="http://www.w3.org/2000/svg" ...>`，否则独立打开时部分渲染器不解析 marker 与 pattern。
3. **样式内联**：把外部 `<style>` 的规则改成属性（`fill` / `stroke` / `font-size` / `font-weight`）或写进 `<style>` 块内。引用外部 CSS 的 SVG 换台机器就掉样式。

## 三、三种渲染后端

| 后端 | 命令要点 | 优点 | 限制 |
|---|---|---|---|
| Playwright（首选） | `new_page(device_scale_factor=2)` 后对元素截图 | 元素级截图天然贴合内容边界，无需猜窗口尺寸 | 需 `pip install playwright` 与浏览器内核 |
| Chrome / Edge 无头 | `--headless=new --window-size=W,H --force-device-scale-factor=N --screenshot=` | 零依赖，装了浏览器即可 | 窗口尺寸必须等于 SVG 固有尺寸，否则内容缩在左上角 |
| wkhtmltoimage（兜底） | `--zoom N --width W` | 老环境可用 | 不支持 `devicePixelRatio`，现代 CSS 与部分 SVG 特性会丢，只能应急 |

降级顺序：Playwright → Chrome → Edge → wkhtmltoimage。降级必须在交付说明里注明，因为后两种对复杂 SVG 的还原度明显下降。

## 四、参数与 DPI 换算

`像素 = 毫米 ÷ 25.4 × DPI`

| 交付场景 | 目标 DPI | 逻辑宽 | 所需像素 | 导出倍数 |
|---|---|---|---|---|
| PPT / 网页 / 微信预览 | 96–144 | 1520 | 3040 | 2× |
| 标书正文（A4，190mm 版面） | 300 | 1520 | 约 2244 → 取 3040 | 2× |
| 白皮书整页（A4 满版） | 300 | 1240 | 2480 | 2× |
| 展板 / 大屏（A1 以上） | 150 | 1520 | 4560 | 3× |

固定参数：

- 页面外壳 `body { margin: 0; padding: 0; background: #ffffff; }`，否则默认 8px 外边距会进 PNG。
- 截图前 `document.fonts.ready` 后等 300ms；有 Web 字体时改为等 `networkidle`。
- 并发渲染必须给每个进程独立的浏览器数据目录，否则实例互相锁死。
- 临时目录用系统临时目录并在结束时清理，不要在交付目录里留中间文件。

## 五、字体与中文

| 平台 | 字体栈命中顺序 | 缺失时的回退 |
|---|---|---|
| macOS | Inter → PingFang SC | 华文黑体 Hiragino Sans GB |
| Windows | Inter → Microsoft YaHei | 等线 DengXian |
| Linux / 容器 | Inter → Noto Sans SC | 思源黑体 Source Han Sans |

- 缺字体时**不要回退到 `monospace`**：等宽字体会让汉字字宽不一致，对齐全乱。
- 容器内渲染前先确认中文字体已安装（`fc-list :lang=zh`），否则中文会渲染成方框或回退到衬线体。
- 字重只用 400 与 600；700 在小字号下发糊，且部分系统中文字体没有真正的 700 字重，会被合成加粗。

## 六、常见失败模式

1. **窗口尺寸 ≠ SVG 固有尺寸**：内容按原尺寸画在左上角，四周全白，覆盖率只有 40–50%。
2. **SVG 写了 `width="100%"`**：独立打开或截图时坍缩，必须改成显式像素。
3. **viewBox 小于内容**：底部或右侧被静默裁掉，没有任何报错。收紧 viewBox 后必须重跑越界检查。
4. **`--force-device-scale-factor` 与窗口尺寸同时翻倍**：得到 4× 而不是 2×，文件体积翻四倍且毫无必要。
5. **Playwright 少传 `device_scale_factor`**：元素截图静默变成 1×，只有读回像素尺寸才能发现。
6. **背景矩形参与 bbox 计算**：一个 `width="100%" height="100%"` 的底图会让内容外接框恒等于整张画布，留白永远“达标”。
7. **按亮度分桶判断留白**：浅色填充（`#f0f9ff` 一类）会被判成空白，覆盖率虚低。用饱和度判据（`max(r,g,b) - min(r,g,b) > 30`）。
8. **旋转文本撑出画布**：`transform="rotate(90 …)"` 的标签会超出逻辑宽高，优先改横排或重新定位。
9. **中文路径或空格**：`file:///` URL 需要引号，并把反斜杠换成正斜杠。
10. **并发实例共用数据目录**：第二个实例启动即失败或截到空白页。
11. **字体未就绪就截图**：拿到的是回退字体版本，字形宽度不同，文字看起来“挤”或“散”。
12. **只检查“文件已写出”**：Chrome 无头即使渲染失败也会写出一张空白 PNG。必须读回尺寸与覆盖率。

## 七、校验命令

```bash
# 2× 导出
python scripts/render_diagram.py diagram.html --out diagram@2x.png --scale 2

# 3× 印刷版
python scripts/render_diagram.py diagram.html --out diagram@3x.png --scale 3
```

脚本会打印 JSON 报告：`logical`（逻辑尺寸）、`expected_px`、`actual_px`、`cover_w` / `cover_h`（覆盖率）、`ok`（布尔）。`ok` 为 false 时不得交付，先按第六节逐条排查。

无 PIL 环境时覆盖率一栏显示 `skipped`，此时必须人工确认尺寸，并补测一次覆盖率。
