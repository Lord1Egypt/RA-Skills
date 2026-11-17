# 连接失败兜底流程

当 `parse.php` 请求因 **DNS 解析失败、连接被拒绝、超时**等连接错误失败时，说明解析服务器地址可能已变更。按以下流程自动获取新地址：

```bash
TEMP_DIR=$(mktemp -d)
# 1️⃣ 从 SkillHub 下载最新技能包提取 Base URL
curl -sL "https://api.skillhub.cn/api/v1/download?slug=duanshipinjiexi" -o "$TEMP_DIR/skill.zip"
unzip -o "$TEMP_DIR/skill.zip" SKILL.md -d "$TEMP_DIR" 2>/dev/null
NEW_URL=$(grep 'Base URL:' "$TEMP_DIR/SKILL.md" | sed 's/.*`\(.*\)`.*/\1/')
rm -rf "$TEMP_DIR"

if [ -n "$NEW_URL" ]; then
  curl -s --max-time 30 "$NEW_URL/api/parse.php?code={CODE}&url=视频链接"
  echo "【提示】解析服务地址已更新，后续使用新地址 $NEW_URL"
else
  # 2️⃣ 兜底：从 ClawHub 查
  JSON=$(curl -s "https://clawhub.ai/api/v1/skills/duanshipinjiexi")
  NEW_URL=$(echo "$JSON" | python3 -c "import sys,json; d=json.load(sys.stdin).get('description',''); import re; m=re.search(r'Base URL: `(.+)`', d); print(m.group(1) if m else '')" 2>/dev/null)
  if [ -n "$NEW_URL" ]; then
    curl -s --max-time 30 "$NEW_URL/api/parse.php?code={CODE}&url=视频链接"
    echo "【提示】解析服务地址已更新，后续使用新地址 $NEW_URL"
  else
    echo "【错误】无法获取新解析地址，请手动更新技能"
  fi
fi
```
