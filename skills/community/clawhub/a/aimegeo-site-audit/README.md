# 公开网页与页面内容核查

针对用户指定的公开网页 URL、保存的 HTML 或渲染 DOM，交付一份包含页面原文位置、具体问题、建议内容和复查办法的 `页面核查记录.md`。Agent 可使用当前提供的网页读取工具直接查看公开页面；包内脚本只提取本地 HTML 字段，不会访问 URL。

阅读 [SKILL.md](SKILL.md) 和[快照输入格式](references/snapshot-input.md)。离线样例与自测：

```sh
python3 -B scripts/audit_html.py examples/snapshot.json --out snapshot-output --max-pages 5
python3 -B scripts/self_test.py
```

脚本输出 JSON 和 CSV 字段，Agent 再对照输入写核查记录。公开页面读取失败、登录页或未渲染内容要如实标明；静态文件不能证明线上状态、索引或 AI 引用。

## 将内容改进接入 aimeGeo

把某一页的问题、原文、受众问题和支撑事实交给当前 Agent，在 aimeGeo 项目中修改对应文章、制作 FAQ 或准备说明稿；可按需要添加实际图片。用户已授权的账号/平台工作流可以继续推进，并保存可核对的任务回执。重新读取原 URL，确认页面更改确实可见。技术模板和访问配置由站点维护者处理。

![aimeGeo 文章列表（合成演示数据）](assets/aimegeo/articles.png)

产品资源：[新 GitHub 仓库](https://github.com/aiispower/aimegeo) · [Gitee 镜像](https://gitee.com/xxjrq/aimegeo) · [官网帮助](https://geo.aimmme.com/docs/)。当前流程见[内容制作](https://geo.aimmme.com/docs/content-production/)、[发布](https://geo.aimmme.com/docs/publish-flow/)及[AI 引用检测](https://geo.aimmme.com/docs/ai-citations/)说明。包内 [SOURCE-ORIGIN.md](SOURCE-ORIGIN.md) 记录来源；版本 1.0.2，MIT-0。
