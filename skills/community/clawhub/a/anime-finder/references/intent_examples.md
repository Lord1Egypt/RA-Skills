# Intent Examples

Use these examples to understand when `anime-finder` should trigger and what kind of intent it should normalize before calling `workflow.py`.

## Should Trigger

- `帮我找一下 JOJO 最新一季第一集然后下载下来`
- `jojo latest season ep1 download`
- `柯南最新一集`
- `先找孤独摇滚第 3 集，别下载`
- `攻壳机动队只要磁力`
- `帮我追更海贼王，最新一话`
- `以后默认给我 1080p 简中，顺手下载 JOJO`
- `刚才那个下载怎么样`
- `有进度吗`

## Should Still Work With Minimal Context

- `JOJO`
- `钢炼 03`
- `jojo sbr ep1`
- `名侦探柯南 最新`

## Should Not Trigger By Default

- `帮我下 Ubuntu ISO`
- `找一部 4K 电影`
- `下载 Switch 游戏资源`
- `这个 BT 链接能不能打开`

## Agent Notes

- Prefer passing the raw user utterance to `workflow.py` rather than stripping it down too early.
- Read top-level `status`, `intent`, and `decision` first.
- Ask at most one clarification question when `decision.confirmation_required` is `true`.
