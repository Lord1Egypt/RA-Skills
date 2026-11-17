# 模式总表（完整版）

SKILL.md 的第 0 步（构建步骤：B3 预算、B4 token、B5 执行、B6 硬性检查、B7 打磨）选出一个主模式和可选的叠加风格。下表列出每个模式由哪些参考文件驱动的专属步骤。

| 用户意图 | 模式 | 路径 | 加载 | 模式专属步骤 |
|---|---|---|---|---|
| 搭建新页面/应用/组件 | **Create（创建）** | 构建 | `references/direction.md`、`references/principles.md`、`references/tokens.md` | 按 B3–B7 执行 |
| “评审 / 审查 / 这个 UI 哪里不好” | **Audit（审查）** | 评审 | `references/audit.md` | `audit.md` §1 检查 → §2 清单 → §3 报告 |
| “重新设计 / 升级 / 打磨 / 做得高级点” | **Redesign（重设计）** | 评审 → 构建 | 先 `references/audit.md` 再 `references/redesign.md` | `redesign.md` 流程 1–9（R3–R6 = 其第 2 步；B3–B7 = 其第 4–9 步） |
| “极简 / 干净 / 编辑感 / 像 Notion” | **Minimalist（极简，风格叠加）** | 同主模式 | `references/minimalist.md` | 在第 2 步（调性）和 B4（token）应用规格，在 B6 检查 |
| 需要外观的幻灯片、文档、报告、HTML 讲义 | **Theme（主题）** | 构建 | `references/theming.md` | `theming.md` 的主题配方驱动 B4–B5 |
| 海报、封面、静态艺术（PNG/PDF） | **Artifact（视觉作品）** | 构建 | `references/artifacts.md` | `artifacts.md` 的“哲学 → 画布”流程驱动 B5；适用 B6 的词数/颜色检查 |
| “评审 / 打分 / 美化这个网站 URL”、与竞品对标（评审网站、网站美化、对标） | **Site Review（网站评审）** | 评审 | `references/site-review.md`、`references/benchmarks.md`，运行 `scripts/review_site.py` | `site-review.md` §1 抓取 → §2 评分 → §3 对比 → §4 报告（§5 批量） |
| “给这张图打分 / 点评 / 哪里不好”、海报或封面评审、AI 图片点评（图片审美、图片评审、海报评审、AI 图片评价、构图） | **Image Review（图片评审）** | 评审 | `references/image-aesthetics.md`，运行 `scripts/review_image.py <img> --type …` | R3 脚本指标（§6）→ R4 8 维度 × 类型权重（§1–2）+ AI 清单（§4）→ R6 严重度（§3）→ 报告（§7） |
| 游戏截图 / 主视觉 / Steam 胶囊图 / 图标 / HUD / 概念图 / 精灵图评审，品类美术方向（游戏美术、游戏审美、游戏 UI、游戏截图评审、RPG、MOBA、二次元、像素） | **Game Art Review（游戏美术评审）** | 评审 | `references/game-aesthetics.md`、`references/game-workflows.md`，运行 `scripts/review_image.py <img> --type game-screenshot\|key-art\|capsule\|icon\|game-ui\|concept\|sprite --genre <g>` | `game-workflows.md` §1（分步）→ §2 报告；修改配方见 §3 |
| “把这张照片做成杂志页 / 产品主图 / 海报”、提取配色、图像模型提示词、科研配图（配色提取、科研配图） | **Image Restyle（图片重制）** | 构建 | `references/image-workflows.md`（+ 用 `image-aesthetics.md` 做前后打分） | `image-workflows.md` §1 四步流程 = B4–B5；§3 重制循环 = B6–B7 |

模式可以组合（如 Redesign + Minimalist）。只读你需要的文件。
