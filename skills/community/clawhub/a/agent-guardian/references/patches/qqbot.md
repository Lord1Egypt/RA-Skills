# QQ Bot 渠道适配指南

本文档说明如何将 Agent Guardian 的功能集成到 QQ Bot 渠道插件中。

## 需要修改的文件

- `extensions/qqbot/src/gateway.ts` — 入站消息处理
- `extensions/qqbot/src/outbound.ts` — 出站消息处理

## gateway.ts 修改

### 1. 顶部添加导入和工具函数

在文件顶部（import 区域之后）添加：

```typescript
// ============ [CUSTOM] 语言一致性过滤 ============
import { execSync } from "child_process";

function filterLanguageMixing(text: string): string {
  try {
    const result = execSync(
      `echo ${JSON.stringify(text)} | python3 /path/to/agent-guardian/scripts/lang-filter.py`,
      { encoding: "utf-8", timeout: 3000 }
    );
    return result || text;
  } catch { return text; }
}

// ============ [CUSTOM] 新会话状态重置 ============
import * as fs from "fs";

function checkAndResetWorkState(content: string): void {
  if (/^\s*\/(new|reset)\b/i.test(content)) {
    try {
      execSync("bash /path/to/agent-guardian/scripts/reset-work-state.sh", { timeout: 3000 });
    } catch {}
  }
}
```

### 2. 入站消息处理块（C2C_MESSAGE_CREATE / GROUP_AT_MESSAGE_CREATE）

在消息处理逻辑的开头，dispatch 之前添加：

```typescript
// [CUSTOM] 更新用户活跃时间戳
try { fs.writeFileSync("/tmp/user-last-active.txt", String(Math.floor(Date.now()/1000))); } catch {}

// [CUSTOM] 新会话命令检测 → 重置工作状态
try { checkAndResetWorkState(event.content); } catch {}

// [CUSTOM] "状态"关键词 → 触发即时查询（不经过AI）
if (/^[\/]?(状态|status)\s*$/i.test(event.content.trim())) {
  try {
    fs.writeFileSync("/tmp/status-query-trigger", JSON.stringify({
      ts: Date.now(), from: senderId, msgId: event.id
    }));
  } catch {}
}

// [CUSTOM] 检测用户消息语言
try {
  const detectedLang = execSync(
    `python3 /path/to/agent-guardian/scripts/detect-language.py ${JSON.stringify(event.content)}`,
    { encoding: "utf-8", timeout: 2000 }
  ).trim();
  if (detectedLang) {
    fs.writeFileSync("/tmp/user-msg-language.txt", detectedLang);
  }
} catch {}

// [CUSTOM] 消息入队
try {
  execSync(`python3 /path/to/agent-guardian/scripts/msg-queue.py add ${JSON.stringify(event.content.slice(0, 50))}`, { timeout: 2000 });
  execSync(`python3 /path/to/agent-guardian/scripts/msg-queue.py start ""`, { timeout: 2000 });
} catch {}
```

### 3. 出站消息发送处

在文本发送前应用语言过滤：

```typescript
// [CUSTOM] 出站语言过滤
content = filterLanguageMixing(content);
```

### 4. AI 回复完成后

在 dispatch 完成的回调中添加：

```typescript
// [CUSTOM] 标记消息队列完成
try {
  execSync(`python3 /path/to/agent-guardian/scripts/msg-queue.py done`, { timeout: 2000 });
} catch {}
```

## outbound.ts 修改

### 出站消息处理

在消息发送函数中添加：

```typescript
// [CUSTOM] 语言一致性校验
try {
  const userLang = fs.readFileSync("/tmp/user-msg-language.txt", "utf8").trim();
  if (userLang === "zh") {
    // 如果用户说中文但回复是纯英文，自动包装
    const zhChars = (text.match(/[\u4e00-\u9fff]/g) || []).length;
    const totalChars = text.replace(/\s/g, "").length;
    if (totalChars > 20 && zhChars / totalChars < 0.1) {
      // 纯英文回复，可选择添加中文注释或触发翻译
      console.log("[CUSTOM] Language mismatch detected: user=zh, reply=en");
    }
  }
} catch {}

// [CUSTOM] 回复发送后标记 idle
try {
  execSync("bash /path/to/agent-guardian/scripts/update-work-state.sh done", { timeout: 2000 });
} catch {}
```

## 注意事项

1. 将 `/path/to/agent-guardian/` 替换为实际的 skill 安装路径
2. 修改后需重新编译并重启 gateway
3. 建议在修改前备份原始文件
4. OpenClaw 版本更新可能需要重新应用 patch
