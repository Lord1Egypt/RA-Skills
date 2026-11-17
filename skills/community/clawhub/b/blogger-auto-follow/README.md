# Blogger Auto-Follow

将用户提供的博主名单整理为单个平台、固定范围的关注批次。用户审阅完整名单并
在前台浏览器中连续执行该名单；默认每批最多 30 人，较长名单会自动分批。

## 使用方式

先预览和校验名单：

```bash
python3 scripts/blogger_auto_follow.py \
  --platform bilibili \
  --file examples/bilibili_10_bloggers.json \
  --dry-run
```

确认名单后执行：

```bash
python3 scripts/blogger_auto_follow.py \
  --platform bilibili \
  --file examples/bilibili_10_bloggers.json \
  --max-follows 30
```

首次运行时，浏览器打开平台首页后，请自行登录并核对账号。登录状态会保存到
`data/browser_profiles/<platform>/` 这一专用资料目录，后续同平台批次会复用它；不会
接管日常 Chrome。终端会展示各批名单，并在每一批开始前要求输入与该批数量一致的确认口令，例如
`EXECUTE 30`。

## 执行范围

- 每次仅处理一个平台和一个固定名单，不会增加候选或切换平台。
- 名单重复项会自动去重；超过 30 人时会按每批最多 30 人自动连续处理。
- 页面显示的账号与名单不匹配时，工具不会执行关注。
- 服务要求额外验证、页面异常或浏览器不可用时，工具停止当前批次并写出结果。
- 结果保存在 `data/batch_results/`；成功及已关注的账号可按用户意图写入本地资产库。

更多面向 Agent 的触发条件与边界见 [SKILL.md](SKILL.md)。

\## 📄 License

本项目采用 [MIT License](LICENSE) 开源协议
