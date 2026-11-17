# 小红书笔记配图

> 调用方式及异步轮询见 SKILL.md「调用方式」「异步任务轮询」

## 参数

```json
{
  "image_urls": ["https://cdn.example.com/ref.jpg"],  // 可选，默认 null：参考图URL数组
  "number": 2,                                         // 必填：生成图数量
  "prompt": "请生成2张在小红书使用的图片...",            // 必填：描述笔记内容和风格
  "resolution": "1728x2304"                            // 可选，默认 null：宽x高，如 1728x2304
}
```

## 关键约束

- ⚠️ `prompt` **不可修改用户原文**，不要改写、总结或优化
