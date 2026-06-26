# Amber Url to Markdown v3.2.0 发布说明

## 📦 发布信息

- **版本**: 3.2.0
- **发布时间**: 2026-03-25
- **发布 ID**: k9795tjrt431w1ddk1db83sa2x83krmx
- **发布状态**: ✅ 成功

## 🎉 核心更新

### 新增 url-auto-fetch Hook

实现了**真正的自动触发功能**，通过 OpenClaw Hooks 系统监听用户消息，自动检测并抓取 URL 链接。

#### 触发方式

1. **纯 URL 消息**
   ```
   https://mp.weixin.qq.com/s/xxx
   ```

2. **URL + 意图关键词**
   ```
   帮我把这篇文章转成 Markdown：https://mp.weixin.qq.com/s/xxx
   解析这个链接：https://zhuanlan.zhihu.com/p/xxx
   ```

#### Hook 特性

- ✅ 监听 `message:received` 事件
- ✅ 自动检测 URL 链接
- ✅ 智能判断触发条件
- ✅ 异步执行，不阻塞消息处理
- ✅ 自动发送抓取进度提示
- ✅ 支持微信公众号、知乎、掘金等 7+ 网站

## 📚 新增文件

```
hooks/
└── url-auto-fetch/
    ├── HOOK.md                     # Hook 元数据 + 文档
    └── handler.ts                  # Hook 实现（ESM 模块）

CHANGELOG.md                        # 版本更新日志
PUBLISH_GUIDE.md                    # 发布指南
HOOK_AUTO_TRIGGER_README.md         # Hook 自动触发方案说明
优化方案总结.md                      # 技术总结文档
RELEASE_3.2.0.md                    # 本文件
```

## 🔧 用户安装指南

### 新用户

```bash
# 1. 安装技能
clawhub install amber-url-to-markdown

# 2. 安装依赖
pip install playwright beautifulsoup4 markdownify requests scrapling
playwright install chromium

# 3. 启用自动触发 Hook
openclaw hooks enable url-auto-fetch

# 4. 重启 Gateway
openclaw gateway restart

# 完成！现在发送 URL 会自动抓取
```

### 老用户升级

```bash
# 1. 更新技能
clawhub update amber-url-to-markdown

# 2. 启用新 Hook
openclaw hooks enable url-auto-fetch

# 3. 重启 Gateway
openclaw gateway restart

# 完成！
```

## 📊 测试结果

### 测试场景

| 测试项 | 结果 | 说明 |
|--------|------|------|
| Hook 发现 | ✅ 成功 | OpenClaw 成功发现 url-auto-fetch Hook |
| Hook 启用 | ✅ 成功 | 通过 `openclaw hooks enable` 启用 |
| URL 检测 | ✅ 成功 | 成功检测纯 URL 消息 |
| 触发判断 | ✅ 成功 | 正确判断触发条件 |
| 脚本查找 | ✅ 成功 | 成功找到 Python 脚本 |
| 异步执行 | ✅ 成功 | 脚本异步执行，不阻塞 |
| 结果保存 | ✅ 成功 | 文章保存到指定目录 |

### 实际测试数据

**测试链接**: https://mp.weixin.qq.com/s/_sv0ZfpecYzNOB-pFs_EcQ

**抓取结果**:
```
✅ 抓取成功（方案一：Playwright 无头浏览器）
📄 标题：MiniMax 官方开源 Skills 技能库：让 AI 写代码从实习生变资深工程师
📊 字数：3388
🖼️ 图片：2 张
⏱️ 耗时：11.4 秒
📝 文件：/root/openclaw/urltomarkdown/MiniMax_官方开源_Skills_技能库_让 AI 写代码从实习生变资深工程师.md
```

## 🎯 技术实现

### Hook 架构

```
用户发送消息
    ↓
Gateway 接收 (message:received)
    ↓
Hook handler 执行
    ↓
检测 URL (正则匹配)
    ↓
判断触发条件
├─ 纯 URL → 触发
├─ URL + 关键词 → 触发
└─ 其他 → 跳过
    ↓
执行 Python 脚本 (异步)
    ↓
保存 Markdown 文件
    ↓
(可选) 发送完成通知
```

### Handler.ts 核心代码

```typescript
import { exec } from "child_process";
import * as fs from "fs";

const handler = async (event: any) => {
  // 只处理 message:received 事件
  if (event.type !== "message" || event.action !== "received") {
    return;
  }

  const content = event.context?.content || "";
  
  // URL 匹配正则
  const urlPattern = /https?:\/\/[^\s<>"{}|\\^`\[\]]+/gi;
  
  // 检测 URL
  const urls = content.match(urlPattern);
  if (!urls || urls.length === 0) {
    return;
  }
  
  // 判断触发条件
  const isPureUrl = content.trim().replace(urlPattern, "").trim().length === 0;
  if (!isPureUrl) {
    return;
  }
  
  // 执行脚本（异步）
  const { exec } = require("child_process");
  exec(`python3 "${scriptPath}" "${targetUrl}"`, ...);
};

export default handler;
```

## 📝 更新日志

详见 `CHANGELOG.md`

### 3.2.0 (2026-03-25)

- ✅ 新增 url-auto-fetch Hook
- ✅ 支持纯 URL 和 URL+ 关键词触发
- ✅ 异步执行，不阻塞消息处理
- ✅ 优化 SKILL.md 文档
- ✅ 添加完整的安装和启用指南

## 🚀 后续计划

### 3.3.0 (计划中)

- [ ] 支持自定义触发关键词
- [ ] 支持 URL 白名单/黑名单
- [ ] 支持完成通知（可选配置）

### 3.4.0 (计划中)

- [ ] 支持并发控制
- [ ] 支持缓存机制
- [ ] 支持批量抓取

## 📖 相关文档

- [HOOK_AUTO_TRIGGER_README.md](./HOOK_AUTO_TRIGGER_README.md) - Hook 自动触发方案详细说明
- [PUBLISH_GUIDE.md](./PUBLISH_GUIDE.md) - 发布指南
- [优化方案总结.md](./优化方案总结.md) - 技术总结
- [OpenClaw Hooks 文档](https://docs.openclaw.ai/automation/hooks)

## 🎊 总结

v3.2.0 版本通过引入 OpenClaw Hooks 系统，实现了真正的自动触发功能，解决了之前技能无法自动调用的问题。现在用户只需安装技能并启用 Hook，即可享受自动抓取的便利！

---

**发布成功** ✅
**ClawHub 包 ID**: k9795tjrt431w1ddk1db83sa2x83krmx
