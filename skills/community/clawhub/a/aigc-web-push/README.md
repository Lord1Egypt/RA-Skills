# aigc-web-push · AI内容生成与全网推送

**版本 3.6.12**

支持通过 AI 生成文章、图文卡片与视频，并推送到微信公众号或经由云电脑推送至全球任意站点。

## 功能特性

- **扫码配置** — 授权公众号 / 默认云电脑（不预选环境或账号）
- **一作品一目录** — 产出放在 `works/<日期>-<主题>/`，技能目录只留技能与配置
- **图文生成** — `design.md` + Humanizer
- **视频创作** — 程序化绘制与公共质量底线；分流 shotcraft / talkcraft / `design-video.md`
- **地理可视化** — `geo-viz/`：地图/地形/地球/路线等；参数化、免 Key；有地理镜头时加载
- **灵活推送** — 可按名称指定云电脑 / 环境 / 账号
- **版本检查** — 推送前对照远端版本；有新版本只问是否升级

## 快速开始

### 1. 配置

打开 https://design.pcloud.ac.cn/aigc-web-push.html ，扫码后把 JSON 存为技能目录下的 `config.json`。

### 2. 建作品目录并创作

```text
works/20261117-demo/
  main.html
  main_cover.html          # 可选
  cover.png                # 可选封面图（有则优先）

works/20261117-gugong-ye-you/
  remotion/  audio/  out/gugong-ye-you.mp4  cover.html / cover.png
```

- 文章 / 贴图：按 `design.md`
- 视频：见 SKILL「视频」

### 3. 推送

在技能目录执行（路径按实际作品目录调整）：

```bash
cd aigc-web-push
node push.js wechat - html ../works/20261117-demo/main.html
node push.js wechat "我的订阅号" html ../works/20261117-demo/main.html
node push.js cloud - html ../works/20261117-demo/main.html article draft
node push.js cloud - video ../works/20261117-gugong-ye-you/out/gugong-ye-you.mp4 "故宫夜游指南" "三条路线带你逛亮灯后的故宫。" draft account "抖音主号"
node push.js cloud - list-targets video
node push.js cloud - resolve video "抖音主号" account
```

## 文档

- **SKILL.md** — 完整说明  
- **design.md** — HTML（文章 / 贴图 / 封面）  
- **design-video.md** — 兜底路径成片规范  
- **geo-viz/** — 按需地理可视化（地图/地形；见其 `SKILL.md`）  
- **config.example.json** — 配置字段  

## 注意

- 云电脑：入队即完成，勿轮询、勿重推  
- 视频仅云电脑；目标名称歧义时先确认再推  
- 勿提交真实 `config.json` / `skillKey`
