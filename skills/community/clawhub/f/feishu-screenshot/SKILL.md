---
name: feishu-screenshot
description: |
  截取屏幕并发送到飞书。当用户说"截屏发给飞书"、"截图"、"屏幕截图"时使用这个技能。
---

# 飞书截图发送

截取屏幕并快速发送到飞书。

## 核心流程

**第一步：截屏（PowerShell）**
```bash
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -Command "Add-Type -AssemblyName System.Windows.Forms; \$bmp = New-Object System.Drawing.Bitmap([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height); \$graphics = [System.Drawing.Graphics]::FromImage(\$bmp); \$graphics.CopyFromScreen([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Location, (New-Object System.Drawing.Point(0,0)), [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Size); \$bmp.Save('C:\Users\edy\Pictures\screenshot.png', [System.Drawing.Imaging.ImageFormat]::Png); \$bmp.Dispose()"
```

**第二步：复制到 workspace**
```bash
cp /mnt/c/Users/edy/Pictures/screenshot.png /home/edy/.openclaw/workspace/截图.png
```

**第三步：发送到飞书**
```json
{
  "action": "send",
  "channel": "feishu",
  "filePath": "/home/edy/.openclaw/workspace/截图.png"
}
```

## 注意事项

- 截屏会保存到 `C:\Users\edy\Pictures\screenshot.png`
- 然后复制到 workspace 才能正常发送附件
- 发送完成后可以删除 workspace 里的临时文件