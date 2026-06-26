# macOS Disk Cleaner

## Folders to Clean

### Temp Files
- `/tmp`
- `~/Library/Caches`

### Browser Cache
- Chrome: `~/Library/Caches/Google/Chrome`
- Safari: `~/Library/Caches/com.apple.Safari`
- Firefox: `~/Library/Caches/Firefox`

### Trash
- `~/.Trash`

### Log Files
- `~/Library/Logs`
- `/var/log`

## Safety Rules
- Never delete anything in `/System`, `/usr`, `/bin`, `/sbin`
- Never delete user Documents, Downloads, Desktop, Pictures, Videos
- Only delete files older than 1 day
- If unsure about a file — skip it

## Steps
1. Check if folder exists before cleaning
2. Calculate folder size before deleting
3. If Confirm Mode — ask user before each folder
4. Delete all files inside the folder (not the folder itself)
5. Show how much space was freed after each step
6. Show total space freed at the end
