# 排错与省积分

## 报错对照

| 现象 | 原因 | 处理 |
|---|---|---|
| `unauthorized` / 401 | key 缺失或失效 | `dlazy login`，或从 dashboard 取新 key `dlazy auth set KEY` |
| `insufficient_balance` | 组织积分不足 | 去 dashboard 充值，告知用户，不要重试 |
| 400，提示 prompt 超长 | 超出该模型上限 | 查 `models.md` 的上限表；精简或换 2000 档模型 |
| 400，提示 size / 参数无效 | 用了别的模型的尺寸写法 | 查 `models.md` 的尺寸对照；注意 `--aspectRatio` 与 `--aspect_ratio` |
| `invalid_tool` | 模型名拼错 | `dlazy --help` 看当前可用工具名 |
| 426 | CLI 版本过低 | 升级到 `@dlazy/cli@1.2.3` 或更高 |
| 任务卡住不返回 | 异步任务还在跑 | `dlazy status <generateId> --wait`，多数模型 30-90 秒 |
| `Prompt violates safety policy` | 内容被安全策略拒 | 改写提示词，不要重试原文——重试仍然会被拒且可能扣费 |
| 出图是竖的但要横的 | 用了默认值 | 显式写尺寸，见下 |

## 不报错但结果不对

**出图方向不对** —— `viduq2-t2i` 默认 9:16、`jimeng-t2i` 默认 1440*2560，都是竖屏。做横屏内容一定要显式指定。

**图很糊** —— `banana2` 默认 `--imageSize 512`。至少给 `1K`，正式用 `2K`。

**中文是乱码字形** —— 换 `gpt-image-2` 或 `qwen-image-2-pro`，其余模型的中文不可靠。

**同一提示词每次差很多** —— `mj-imagine` 尤其明显。要稳定就把构图和光线写死，或改用 seedream / gpt-image-2。

**参考图被无视** —— 提示词里没说清参考图的角色。见 `editing.md`。

**透明背景是灰白格子** —— 模型画了"格子图案"而不是 alpha 通道。改用纯色背景 + `imageseg`。

## 省积分

按见效程度排：

**1. 先 `--dry-run`。** 参数拿不准时零成本验证。批量任务前必做——一个参数写错乘以 100 张就是 100 次失败。

**2. 便宜模型选稿，贵模型定稿。** 用 `seedream-5.0-lite`（5）出 5 张看构图，选中后再用 `banana-pro`（18）或 `gpt-image-2` 出终稿。总价 25 + 18 < 直接用贵模型试 5 次的 90。

**3. 能后处理就别重新生成。** 抠图 1 积分、矢量化 2 积分、放大 10 积分，而重新生成一张 5–30 积分且要重新对齐风格。

**4. 4K 走便宜路线。** `seedream-5.0 --resolution 4k` 是 8 积分，`gpt-image-2 --size 3840x2160` 是 37。没有准确中文需求时不要用后者。

**5. 改图而不是重画。** 一张图 90% 对了，用 `gpt-image-2 --images` 改（33）比重画再对齐风格便宜。

**6. 别对被安全策略拒绝的提示词重试。** 它不会因为重试而通过。

## 查实时价格

这里的积分数会随定价调整过时。给用户报价前用 `--dry-run` 现场确认：

```bash
dlazy banana-pro --prompt "test" --imageSize 4K --dry-run
```

它打印将要发送的参数和积分估算，不产图、不扣费。
