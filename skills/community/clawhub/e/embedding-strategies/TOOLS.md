# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics â€” the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room â†’ Main area, 180Â° wide angle
- front-door â†’ Entrance, motion-triggered

### SSH

- home-server â†’ 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---

## ?? ±¾µØÖªÊ¶¿âËÑË÷

### ¹¤×÷Ä¿Â¼
C:\Users\Xiabi\.openclaw\workspace

### ¿ìËÙËÑË÷ÃüÁî

`powershell
# ËÑË÷ÎÄ¼şÄÚÈİ£¨ÍÆ¼ö£©
Select-String -Path "C:\Users\Xiabi\.openclaw\workspace\*.md" -Pattern "¹Ø¼ü´Ê" -Recurse

# ËÑË÷ÎÄ¼şÃû
Get-ChildItem -Path "C:\Users\Xiabi\.openclaw\workspace" -Recurse -Filter "*¹Ø¼ü´Ê*"

# ËÑË÷×î½ü 7 ÌìĞŞ¸ÄµÄÎÄ¼ş
Get-ChildItem -Path "C:\Users\Xiabi\.openclaw\workspace" -Recurse | Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-7) }

# ÁĞ³öËùÓĞ Markdown ÎÄ¼ş
Get-ChildItem -Path "C:\Users\Xiabi\.openclaw\workspace" -Recurse -Filter "*.md"
`

### Ë÷ÒıÎÄ¼ş
- ÖªÊ¶¿âË÷Òı.md - ×Ô¶¯¸üĞÂµÄÎÄ¼şË÷Òı
- update-knowledge-index.ps1 - Ë÷Òı¸üĞÂ½Å±¾

### Cron ÈÎÎñ
- Ã¿Ğ¡Ê±×Ô¶¯¸üĞÂË÷Òı
