#!/bin/bash
# 自动应用 QQ Bot 插件 patch

set -e

PLUGIN_DIR="/root/.openclaw/extensions/qqbot"
SRC="$PLUGIN_DIR/src"
SKILL_DIR="$(dirname "$0")/.."

echo "Applying QQ Bot patch for Agent Guardian..."

# 备份原文件
cp "$SRC/gateway.ts" "$SRC/gateway.ts.bak"
cp "$SRC/outbound.ts" "$SRC/outbound.ts.bak"
echo "✅ Backed up original files"

# 获取 skill 绝对路径
SKILL_ABS="$(cd "$SKILL_DIR" && pwd)"

# 1. gateway.ts - 添加 import 和函数定义（在文件顶部，最后一个 import 之后）
awk -i inplace '
/import from "openclaw\/plugin-sdk";/ && !added {
    print;
    print "";
    print "// ============ [CUSTOM] Agent Guardian - Language Filtering ============";
    print "import { execSync } from \"child_process\";";
    print "";
    print "function filterLanguageMixing(text: string): string {";
    print "  try {";
    print "    const result = execSync(`echo \${JSON.stringify(text)} | python3 '"$SKILL_ABS"'/scripts/lang-filter.py`, { encoding: \"utf-8\", timeout: 3000 });";
    print "    return result || text;";
    print "  } catch { return text; }";
    print "}";
    print "";
    print "// ============ [CUSTOM] Agent Guardian - Session Reset ============";
    print "import * as fs from \"fs\";";
    print "";
    print "function checkAndResetWorkState(content: string): void {";
    print "  if (/^s*\/(new|reset)b/i.test(content)) {";
    print "    try { execSync(\"bash '"$SKILL_ABS"'/scripts/reset-work-state.sh\", { timeout: 3000 }); } catch {}";
    print "  }";
    print "}";
    print "";
    added = 1;
    next;
}
{ print }
' "$SRC/gateway.ts"
echo "✅ Added imports and helper functions to gateway.ts"

# 2. gateway.ts - 在 C2C_MESSAGE_CREATE 处理块中添加 hooks
# 找到 dispatch 调用前的位置插入
sed -i '/C2C_MESSAGE_CREATE/,+50' "$SRC/gateway.ts" | cat  # just to re-sync
# 更可靠的方式：在 dispatch 调用前插入
dispatch_line=$(grep -n "dispatch(" "$SRC/gateway.ts" | head -5 | tail -1 | cut -d: -f1)
if [ -n "$dispatch_line" ]; then
    insert_line=$((dispatch_line - 1))
    sed -i "${insert_line}r /dev/stdin" "$SRC/gateway.ts" << 'DISPATCHEOF'
    // [CUSTOM] Agent Guardian - inbound hooks
    try { fs.writeFileSync("/tmp/user-last-active.txt", String(Math.floor(Date.now()/1000))); } catch {}
    try { checkAndResetWorkState(event.content); } catch {}
    if (/^[\/]?(状态|status)\s*$/i.test(event.content.trim())) {
      try { fs.writeFileSync("/tmp/status-query-trigger", JSON.stringify({ ts: Date.now(), from: senderId, msgId: event.id })); } catch {}
    }
    try {
      const detectedLang = execSync(`python3 '"$SKILL_ABS"'/scripts/detect-language.py ${JSON.stringify(event.content)}`, { encoding: "utf-8", timeout: 2000 }).trim();
      if (detectedLang) { fs.writeFileSync("/tmp/user-msg-language.txt", detectedLang); }
    } catch {}
    try { execSync(`python3 '"$SKILL_ABS"'/scripts/msg-queue.py add ${JSON.stringify(event.content.slice(0, 50))}`, { timeout: 2000 }); execSync(`python3 '"$SKILL_ABS"'/scripts/msg-queue.py start ""`, { timeout: 2000 }); } catch {}
    // [END CUSTOM]
DISPATCHEOF
    echo "✅ Added inbound hooks before dispatch"
fi

# 3. outbound.ts - 添加语言过滤
sed -i '/function.*send.*Message/,+100' "$SRC/outbound.ts" | cat
process_line=$(grep -n "process.*text\|content.*=.*text" "$SRC/outbound.ts" | head -5 | tail -1 | cut -d: -f1)
if [ -n "$process_line" ]; then
    sed -i "${process_line}r // [CUSTOM] Agent Guardian - outbound language filtering\ncontent = filterLanguageMixing(content);\n// [END CUSTOM]" "$SRC/outbound.ts"
    echo "✅ Added language filtering to outbound"
fi

# 4. 在 dispatch 完成的回调中添加 msg-queue.py done
done_line=$(grep -n "\.then\(\)\s*=>\s*{" "$SRC/gateway.ts" | head -3 | tail -1 | cut -d: -f1)
if [ -n "$done_line" ]; then
    sed -i "${done_line}r // [CUSTOM] Agent Guardian - mark message done\ntry { execSync(`python3 '"$SKILL_ABS"'/scripts/msg-queue.py done`, { timeout: 2000 }); } catch {}\n// [END CUSTOM]" "$SRC/gateway.ts"
    echo "✅ Added message done marker"
fi

echo ""
echo "🎉 Patch applied successfully!"
echo "⚠️ 需要重新编译并重启 gateway 才能生效"
echo "   cd $PLUGIN_DIR && npm run build && openclaw gateway restart"
