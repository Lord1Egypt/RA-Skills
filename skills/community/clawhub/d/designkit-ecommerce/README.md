# Designkit Skills

🎨 Professional design assets for ecommerce teams: remove backgrounds, restore blurry images, and generate listing-ready product visuals in one workflow.  
Designkit 官方技能包：一键抠图、画质修复、商品主图与详情图生成。

## ClawHub Display Name

`Designkit: AI Product Image Studio`

## What This Skill Solves

用户搜索 design，通常是在找“马上能用”的结果。这个 Skill 专注 3 个高频场景：

1. `Cutout-Express`：智能抠图，输出透明底/白底图。
2. `Clarity-Boost`：模糊图画质修复，提升商品图清晰度。
3. `Listing-Kit`：电商商品套图多步生成（主图 + 详情图）。

## Included Skills

- `designkit-ecommerce-skills`：根路由与意图分发
- `designkit-edit-tools`：原子图片编辑（抠图、变清晰）
- `designkit-ecommerce-product-kit`：电商套图多步工作流

## Quick Start

1. 获取额度：[https://www.designkit.com/openClaw](https://www.designkit.com/openClaw)
2. 设置环境变量：

```bash
export DESIGNKIT_OPENCLAW_AK="AK"
```

3. 安装 Skill：

```bash
clawhub install designkit-ecommerce-skills
```

或：

```bash
npx -y skills add https://github.com/designkit/designkit-ecommerce-skills
```

## 30-Second Demo Script

可用于录屏/GIF，提升列表页转化：

1. 输入：`帮我把这张商品图抠成透明底`
2. 输出：透明底结果图（Markdown 图片）
3. 输入：`再把这张模糊图变清晰`
4. 输出：修复后高清图
5. 输入：`基于这张商品图做一套亚马逊主图详情图`
6. 输出：套图生成进度 + 成品图展示 + 本地下载路径

## Security & Trust

权限只保留运行能力所必需项：

- `network`：调用 Designkit/OpenClaw API
- `shell`：执行仓库内脚本入口（`bash`/`python3`）
- `filesystem`：读取本地输入图、自动下载输出图

不申请系统配置修改类权限，不写入非任务相关目录。

安全默认值：

- 默认关闭请求日志：`OPENCLAW_REQUEST_LOG=0`
- 若手动开启请求日志，脚本会对敏感请求头（如 `X-Openclaw-AK`）做打码

## SEO Keyword Matrix (Bilingual)

**English keywords**  
`AI image editing`, `background removal`, `matting`, `restore blurry image`, `ecommerce listing images`, `product hero image`, `product detail image`

**中文关键词**  
`抠图`, `去背景`, `透明底`, `白底图`, `画质修复`, `图片增强`, `电商套图`, `商品主图`, `商品详情图`

**Commonly searched for**

- `How to remove product image background with AI`
- `How to restore blurry ecommerce photos`
- `Best tool to generate Amazon listing images`
- `如何一键生成电商商品主图和详情图`
- `如何批量优化商品图清晰度`

## Repository Structure

- `SKILL.md`：根 Skill 入口
- `claw.json`：包元信息、触发词、权限配置
- `api/commands.json`：原子能力定义
- `skills/designkit-edit-tools/SKILL.md`：图片编辑子 Skill
- `skills/designkit-ecommerce-product-kit/SKILL.md`：电商套图子 Skill
- `scripts/run_command.sh`：通用图片编辑执行脚本
- `scripts/run_ecommerce_kit.sh`：电商套图执行入口
- `scripts/ecommerce_product_kit.py`：电商套图核心逻辑

## ClawHub 提交前 Checklist

1. 确认 `SKILL.md` 与子 skill frontmatter 均包含 `name`、`description`、`version` 与 `metadata.openclaw`。
2. 确认环境变量至少配置：
   - `DESIGNKIT_OPENCLAW_AK`
3. 本地 smoke test：
   - `bash scripts/run_command.sh sod --input-json '{"image":"https://example.com/photo.jpg"}'`
4. 发布：
   - `clawhub login`
   - `clawhub publish . --slug designkit-ecommerce-skills --version 1.1.2 --tags latest`

## License

MIT-0
