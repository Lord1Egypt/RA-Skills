# feishu-wechat-publish

飞书文档 → 微信公众号草稿箱发布技能。

## 文件结构

```
feishu-wechat-publish/
├── SKILL.md                          # 技能指令（agent 加载入口）
├── README.md                         # 本文件
├── scripts/
│   └── fetch-feishu-images.sh        # 批量下载飞书图片并生成 assets JSON
└── examples/
    └── publish-request.json          # relay 请求体示例
```

## 工作流程

1. 用户发飞书文档 → agent 读取内容
2. agent 下载图片并编码为 base64
3. agent 发送 Markdown + assets 到 relay
4. relay 渲染并创建微信公众号草稿

## Relay

`https://feishu.shing19.cc/api/publish`
