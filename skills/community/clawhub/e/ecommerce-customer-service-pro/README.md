# ecommerce-customer-service-pro

一套可直接上传到 ClawHub / OpenClaw 的智能电商客服 Skill。

## 适用范围

- 电商店铺客服
- 私域运营与成交跟进
- 售前、售中、售后、投诉安抚
- FAQ / SOP / 快捷回复库
- 达人、机构、渠道商务沟通

## 设计重点

1. 支持先让用户选择行业，再匹配更稳妥的话术。
2. 不预设品牌政策，避免模型自行编造价格、时效、赔付、库存等事实。
3. 对食品、美妆、营养保健、母婴、生鲜、酒旅、跨境等高敏行业增加保守表达约束。
4. 默认输出“可直接发送版 + 加强版 + 内部处理要点 + 可替换字段”。
5. 通过 references 目录拆分行业规则、场景模板、合规规则和输出模板，便于后续扩展。

## 目录结构

```text
 ecommerce-customer-service-pro/
 ├── SKILL.md
 ├── README.md
 ├── CHANGELOG.md
 └── references/
     ├── compliance-guide.md
     ├── industry-profiles.md
     ├── output-templates.md
     ├── platform-notes.md
     └── scene-playbooks.md
```

## 上传建议

- 直接将整个文件夹压缩为 zip 上传。
- 如需改成你的品牌专用版，优先修改：
  - `SKILL.md` 的描述与触发词
  - `references/scene-playbooks.md` 中的具体政策字段
  - `references/platform-notes.md` 中的平台口吻
- 如果你有自家售后政策、发货时效、赔付标准，可继续追加到 `references/` 目录中。

## 推荐二次定制方向

- 增加你自己的品牌 FAQ
- 增加具体平台规则边界
- 增加行业专属术语与卖点库
- 增加“客服升级到主管”的判断树
- 增加“达人合作报价与寄样”模块

