# crayfish-sticker - 智能表情包技能

## 功能描述
安装后OpenClaw会根据对话上下文的情绪、内容自动匹配合适的表情包发送，让聊天更有意思！表情包资源托管在GitHub仓库，支持实时更新，不需要重新安装技能就能用到新表情。


## 表情包分类

- **乏/累/颓废** - 日常状态
- **牛逼/厉害** - 称赞专用
- **不中/不行** - 拒绝专用

### 通用表情
- **开心/快乐** - 高兴时刻
- **无语/无奈** - 吐槽时刻
- **工作/编程** - 干活时刻
- **思考/灵感** - 脑力时刻

## 实现原理
1. 对话时自动分析当前上下文的情绪、关键词和场景
2. 请求远程表情包仓库的索引文件（JSON格式，标签对应图片链接）
3. 匹配最合适的表情包，返回图片给用户
4. 本地缓存索引和热门表情，请求更快更省流量
5. **智能匹配**：优先匹配当前对话的关键词和情绪

## 表情包仓库结构
表情包单独托管在GitHub仓库，结构如下：
```
crayfish-stickers/
├── index.json          # 总索引文件（增强版）
├── happy/              # 开心分类
│   ├── laugh1.png
│   └── happy2.png
├── sad/                # 难过分类
│   ├── cry1.png
│   └── upset1.png
├── speechless/         # 无语分类
│   ├── eyeroll1.png
│   └── speechless1.png
├── working/            # 工作分类
│   ├── coding1.png
│   └── debugging1.png
└── thinking/           # 思考分类
    ├── thinking1.png
    └── idea1.png
```


## 配置选项
```javascript
{
  // 表情包仓库URL
  "repoUrl": "https://raw.githubusercontent.com/StudyWorkLife/crayfish-stickers/main/index.json",
  
  // 缓存时间（毫秒）
  "cacheTTL": 3600000,
  
  // 发送频率（0-1，1表示每次都发）
  "sendFrequency": 0.3,
  
}
```

## 与crayfish-uncle技能配合
同时安装`crayfish-uncle`和`crayfish-sticker`食用更佳



## 技术细节
- 使用语义分析匹配关键词
- 本地缓存减少网络请求
- 支持动态更新（修改GitHub仓库即可）
- 自动分类和优先级排序

