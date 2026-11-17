# 才谷网投票 Creator Skill（caiguwang-creator）

面向「制作投票」场景的 Agent 技能：支持**投票模板检索**、**AI 一句话创建投票活动**、
**批量添加选手**、**图片上传**、**活动与投票数据查询**。通过 Python CLI 调用才谷网投票开放接口，
令牌由用户在才谷网投票管理后台生成，权限仅限本人账号下的活动。

## 适用场景

- 用户提到投票、评选、投票活动、投票模板、才谷网
- 用户想创建投票链接 / 二维码投票 / 微信投票小程序
- 用户描述"我想做个投票让大家选……"、"AI 帮我发起一个评选"

## 目录结构

| 路径 | 说明 |
|------|------|
| `SKILL.md` | 技能元数据与完整指令（name / description / read_when / 流程与边界） |
| `scripts/caiguwang_cli.py` | 命令行入口 |
| `scripts/caiguwang/` | HTTP 客户端与配置包 |

## 前置条件

1. Python 3 与 `requests`：`pip install requests`
2. 访问令牌：登录才谷网投票管理后台 →「养虾Skill」页 → 开启令牌开关 → 复制令牌

## 快速开始

```bash
# 保存令牌（或设置环境变量 X_CAIGU_TOKEN）
python scripts/caiguwang_cli.py login --token <你的令牌>

# 验证令牌
python scripts/caiguwang_cli.py auth status

# AI 一句话创建投票活动
python scripts/caiguwang_cli.py create --describe "给阳光幼儿园办一个国庆绘画比赛投票，10月1日到7日，每人每天投3票"
```

## 命令一览

| 命令 | 说明 |
|------|------|
| `auth login / auth status` | 令牌保存与验证 |
| `search` | 检索投票模板 |
| `create` | 创建投票活动（`--describe` 走 AI 生成，或手动参数） |
| `update` | 修改活动（标题/说明/时间/投票规则/分组等） |
| `item-add` | 添加选手（单次最多 200 位，支持 JSON 批量） |
| `item-update` | 修改选手名称/图片 |
| `group-rename` | 活动分组改名（不改选手归属） |
| `upload` | 上传图片（本地文件或图片链接，返回素材 URL） |
| `material` | 我的素材列表（URL 可直接复用） |
| `list` | 我的活动列表 |
| `vote-data` | 选手票数榜单 |
| `view-data` | 活动整体数据 |

详细参数与边界以 [`SKILL.md`](./SKILL.md) 为准。

## 安全边界

- 令牌只授权本人账号下的活动/素材，全部归属校验；
- 不提供删除活动、清空数据、删除选手等破坏性操作；
- 令牌可随时在后台重置，泄露后立即失效。
