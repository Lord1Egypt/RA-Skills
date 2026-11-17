# aigc-web-push · AI内容生成与全网推送

[ClawHub](https://clawhub.ai/lihengdao/aigc-web-push) · [虾评Skill](https://xiaping.coze.com/skill/015db5c8-8dc6-4c44-b16c-b865ea3c06f0)

支持通过 AI 生成文章、图文卡片与视频，并推送到微信公众号或经由云电脑推送至全球任意站点。

## 功能特性

- **扫码配置** — 授权公众号 / 默认云电脑（不预选环境或账号）
- **一作品一目录** — 产出放在 `works/<日期>-<主题>/`，技能目录只留技能与配置
- **图文生成** — `design.md` + Humanizer
- **视频创作** — `remotion-video.md` + Remotion Agent Skills
- **灵活推送** — 可按名称指定云电脑 / 环境 / 账号
- **自动升级** — 推送前对齐 ClawHub（保留 `config.json`）

## 安装

```bash
npx skills add lihengdao/aigc-web-push
```

或发送 https://clawhub.ai/lihengdao/aigc-web-push 给 AI。

## 快速开始

### 1. 配置

打开 https://design.pcloud.ac.cn/aigc-web-push.html ，扫码后把 JSON 存为技能目录下的 `config.json`。

### 2. 建作品目录并创作

```text
works/20261117-demo/
  main.html
  main_cover.html          # 可选
  cover.png                # 可选封面图（有则优先）
  # 或视频：
  remotion/  audio/  out/aigc-video.mp4  cover.html / cover.png
```

- 文章 / 贴图：按 `design.md`
- 视频：按 `remotion-video.md`，先装并加载 Remotion Skills

### 3. 推送

在技能目录执行（路径按实际作品目录调整）：

```bash
cd aigc-web-push
node push.js wechat - html ../works/20261117-demo/main.html
node push.js wechat "我的订阅号" html ../works/20261117-demo/main.html
node push.js cloud - html ../works/20261117-demo/main.html article draft
node push.js cloud - video ../works/20261117-demo/out/aigc-video.mp4 "标题" draft account "抖音主号"
node push.js cloud - list-targets video
node push.js cloud - resolve video "抖音主号" account
```

## 文档

- **SKILL.md** — 完整说明  
- **design.md** — HTML（文章 / 贴图 / 封面）  
- **remotion-video.md** — 视频成片规范  
- **config.example.json** — 配置字段  

## 注意

- 云电脑：入队即完成，勿轮询、勿重推  
- 视频仅云电脑；目标名称歧义时先确认再推  
- 勿提交真实 `config.json` / `skillKey`

## 维护者

[@lihengdao](https://clawhub.ai/users/lihengdao)
