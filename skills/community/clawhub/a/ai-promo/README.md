# AI Promo - 大模型平台优惠信息 Skill

查询大模型平台优惠信息，支持分类查询、订阅推送、提交优惠。

## 访问地址

- API: https://cli.aipromo.workers.dev
- Landing: https://cli.aipromo.workers.dev/landing

## 功能

- 分类查询：推荐/新客/限时/免费
- 订阅管理：每日推送
- 提交优惠：用户提交新优惠

## 文件结构

```
ai-promo/
├── SKILL.md              # Skill 文档
├── cache.json            # 离线缓存
├── scripts/
│   ├── promo_user.sh     # User_id 管理
│   ├── promo_query.sh    # 查询优惠
│   ├── promo_subscribe.sh # 订阅管理
│   ├── promo_submit.sh   # 提交优惠
│   └── promo_push.sh     # 每日推送
└── .gitignore
```

## 数据来源

- 数据库: `~/projects/promo-api/db/seeds/`
- 文档: `~/documents/2026-03-31-token-promo-summary.md`
